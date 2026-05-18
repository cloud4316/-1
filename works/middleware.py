from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserSession, PageView
import time
import threading


class TimeTrackingMiddleware(MiddlewareMixin):
    """Middleware для отслеживания времени, проведенного пользователем на сайте"""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self._session_timers = {}  # Храним таймеры для каждой сессии
    
    def process_request(self, request):
        # Пропускаем статические файлы и API запросы для ускорения
        if (request.path.startswith('/static/') or 
            request.path.startswith('/media/') or 
            request.path.startswith('/favicon.ico') or
            request.path.startswith('/api/')):
            return None
            
        if request.user.is_authenticated:
            # Получаем или создаем активную сессию
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            
            # Проверяем, есть ли активная сессия
            active_session = UserSession.objects.filter(
                user=request.user,
                session_key=session_key,
                is_active=True
            ).first()
            
            if not active_session:
                # Создаем новую сессию
                active_session = UserSession.objects.create(
                    user=request.user,
                    session_key=session_key,
                    start_time=timezone.now()
                )
            
            # Сохраняем сессию в request для использования в process_response
            request._active_session = active_session
            request._session_start_time = time.time()
            
            # Запускаем таймер для обновления времени в реальном времени
            self._start_session_timer(active_session)
    
    def _start_session_timer(self, session):
        """Запускает таймер для обновления времени сессии каждые 60 секунд"""
        def update_session_time():
            try:
                # Обновляем время сессии
                session.refresh_from_db()
                if session.is_active:
                    session.duration_seconds += 60
                    session.save()
                    
                    # Планируем следующее обновление
                    timer = threading.Timer(60.0, update_session_time)
                    timer.daemon = True
                    timer.start()
                    self._session_timers[session.id] = timer
            except Exception:
                pass  # Игнорируем ошибки при обновлении
        
        # Запускаем таймер только если его еще нет
        if session.id not in self._session_timers:
            timer = threading.Timer(60.0, update_session_time)
            timer.daemon = True
            timer.start()
            self._session_timers[session.id] = timer
    
    def process_response(self, request, response):
        if hasattr(request, '_active_session') and request._active_session and request.user.is_authenticated:
            session = request._active_session
            
            # Обновляем время сессии
            if hasattr(request, '_session_start_time'):
                time_spent = int(time.time() - request._session_start_time)
                session.duration_seconds += time_spent
            
            # Увеличиваем счетчик просмотров страниц
            session.page_views += 1
            session.save()
            
            # Логируем просмотр страницы только для важных страниц (не для статических файлов)
            if (hasattr(request, '_session_start_time') and 
                not request.path.startswith('/static/') and 
                not request.path.startswith('/media/') and
                not request.path.startswith('/favicon.ico')):
                PageView.objects.create(
                    user=request.user,
                    session=session,
                    page_url=request.get_full_path(),
                    page_title=getattr(response, 'title', 'Unknown'),
                    time_spent=time_spent
                )
        elif hasattr(request, '_active_session') and request._active_session and not request.user.is_authenticated:
            # Пользователь вышел из системы, завершаем сессию
            session = request._active_session
            session.is_active = False
            session.end_time = timezone.now()
            session.save()
            
            # Останавливаем таймер
            if session.id in self._session_timers:
                timer = self._session_timers[session.id]
                timer.cancel()
                del self._session_timers[session.id]
        
        return response


class SessionTimeoutMiddleware(MiddlewareMixin):
    """Middleware для автоматического завершения неактивных сессий"""
    
    def process_request(self, request):
        # Пропускаем статические файлы и API запросы для ускорения
        if (request.path.startswith('/static/') or 
            request.path.startswith('/media/') or 
            request.path.startswith('/favicon.ico') or
            request.path.startswith('/api/')):
            return None
            
        if request.user.is_authenticated:
            # Завершаем сессии, которые неактивны более 30 минут
            from datetime import timedelta
            timeout_threshold = timezone.now() - timedelta(minutes=30)
            
            UserSession.objects.filter(
                user=request.user,
                is_active=True,
                start_time__lt=timeout_threshold
            ).update(
                is_active=False,
                end_time=timezone.now()
            )
