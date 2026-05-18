from django.db import OperationalError
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserSession, PageView
import time
import threading


class OptimizedTimeTrackingMiddleware(MiddlewareMixin):
    """Оптимизированный middleware для отслеживания времени"""
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        self._session_timers = {}
        self._last_activity = {}  # Отслеживаем последнюю активность для каждой сессии
        self._skip_paths = {
            '/static/', '/media/', '/favicon.ico', '/api/', 
            '/.well-known/', '/__debug__/', '/admin/'
        }
    
    def should_skip_request(self, request):
        """Проверяем, нужно ли пропустить запрос"""
        if request.method != 'GET':
            return True
            
        for path in self._skip_paths:
            if request.path.startswith(path):
                return True
                
        return False
    
    def process_request(self, request):
        try:
            return self._process_request_safe(request)
        except OperationalError:
            # Таблицы ещё не созданы (migrate не запущен) — пропускаем
            return None
        except Exception:
            return None

    def _process_request_safe(self, request):
        if self.should_skip_request(request):
            return None
            
        if not request.user.is_authenticated:
            return None
            
        # Получаем или создаем активную сессию
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        
        # Проверяем, есть ли активная сессия
        try:
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
                    start_time=timezone.now(),
                    is_active=True
                )
            
            # Запускаем таймер для сессии только если его еще нет
            if session_key not in self._session_timers:
                self._session_timers[session_key] = time.time()
                self._last_activity[session_key] = timezone.now()
            
        except Exception:
            # В случае ошибки пропускаем обработку
            pass
    
    def process_response(self, request, response):
        try:
            return self._process_response_safe(request, response)
        except (OperationalError, Exception):
            return response

    def _process_response_safe(self, request, response):
        if self.should_skip_request(request):
            return response
            
        if not request.user.is_authenticated:
            return response
            
        try:
            session_key = request.session.session_key
            if not session_key:
                return response
                
            # Получаем активную сессию
            active_session = UserSession.objects.filter(
                user=request.user,
                session_key=session_key,
                is_active=True
            ).first()
            
            if active_session and session_key in self._session_timers:
                # Обновляем время сессии
                time_spent = time.time() - self._session_timers[session_key]
                active_session.duration_seconds += int(time_spent)
                active_session.page_views += 1
                active_session.save()
                
                # Создаем запись о просмотре страницы
                PageView.objects.create(
                    user=request.user,
                    session=active_session,
                    page_url=request.path,
                    page_title=getattr(response, 'title', ''),
                    time_spent=int(time_spent)
                )
                
                # Обновляем таймер для следующего запроса (НЕ удаляем!)
                self._session_timers[session_key] = time.time()
                self._last_activity[session_key] = timezone.now()
                    
        except Exception:
            # В случае ошибки пропускаем обработку
            pass
            
        return response


class SessionTimeoutMiddleware(MiddlewareMixin):
    """Middleware для автоматического завершения неактивных сессий"""
    
    def process_request(self, request):
        if not request.user.is_authenticated:
            return None
            
        try:
            # Завершаем сессии, которые неактивны более 2 часов (увеличено с 30 минут)
            timeout_threshold = timezone.now() - timezone.timedelta(hours=2)
            
            # Получаем сессии для завершения
            inactive_sessions = UserSession.objects.filter(
                user=request.user,
                is_active=True,
                start_time__lt=timeout_threshold
            )
            
            # Завершаем неактивные сессии
            for session in inactive_sessions:
                session.is_active = False
                session.end_time = timezone.now()
                session.save()
                
        except Exception:
            pass
