from django.urls import path
from . import views

urlpatterns = [
    # ── Основное ──────────────────────────────────────────────────────────────
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',           views.custom_login,    name='custom_login'),
    path('change-password/', views.change_password, name='change_password'),

    # ── Панель преподавателя ───────────────────────────────────────────────────
    path('teacher/', views.admin_panel, name='admin_panel'),
    path('teacher/approve/<int:user_id>/',    views.approve_user,    name='approve_user'),
    path('teacher/reject/<int:user_id>/',     views.reject_user,     name='reject_user'),
    path('teacher/deactivate/<int:user_id>/', views.deactivate_user, name='deactivate_user'),

    # ── Практические работы ───────────────────────────────────────────────────
    path('works/', views.work_list, name='work_list'),
    path('works/<int:work_id>/', views.work_detail, name='work_detail'),
    path('works/<int:work_id>/submit/', views.submission, name='work_submit'),
    path('submission/<int:work_id>/', views.submission, name='submission'),
    path('solution/<int:solution_id>/', views.solution_detail, name='solution_detail'),
    path('results/', views.results, name='results'),
    path('progress/', views.works_userprogress, name='works_userprogress'),

    # ── Профиль ───────────────────────────────────────────────────────────────
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),

    # ── Теория ────────────────────────────────────────────────────────────────
    path('theory/', views.theory_list, name='theory_list'),
    path('theory/lesson/<int:lesson_id>/', views.theory_lesson, name='theory_lesson'),
    path('theory/lesson/<int:lesson_id>/done/', views.mark_lesson_done, name='mark_lesson_done'),
    path('theory/lesson/<int:lesson_id>/notes/', views.save_notes, name='save_notes'),

    # ── Предметы ──────────────────────────────────────────────────────────────
    path('subject/<slug:slug>/', views.switch_subject, name='switch_subject'),

    # ── Объявления ────────────────────────────────────────────────────────────
    path('announcements/', views.announcement_list, name='announcement_list'),
    path('announcements/create/', views.create_announcement, name='create_announcement'),
    path('announcements/<int:pk>/deactivate/', views.deactivate_announcement, name='deactivate_announcement'),

    # ── Тесты ─────────────────────────────────────────────────────────────────
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),


    # ── Уведомления ──────────────────────────────────────────────────────────────
    path('notifications/',               views.notifications_view,     name='notifications'),
    path('notifications/count/',         views.notifications_count,    name='notifications_count'),
    path('notifications/<int:notif_id>/read/', views.mark_notification_read, name='mark_notification_read'),

    # ── Рейтинг ───────────────────────────────────────────────────────────────────
    path('leaderboard/', views.leaderboard, name='leaderboard'),

    # ── Поиск по теории ───────────────────────────────────────────────────────────
    path('theory/search/', views.theory_search, name='theory_search'),

    # ── Журнал и ручная проверка (преподаватель) ──────────────────────────────────
    path('teacher/gradebook/',                    views.gradebook,          name='gradebook'),
    path('teacher/solutions/',                    views.teacher_solutions,  name='teacher_solutions'),
    path('teacher/grade/<int:solution_id>/',      views.manual_grade,       name='manual_grade'),

    # ── Аналитика и Excel ──────────────────────────────────────────────────────
    path('teacher/analytics/',         views.teacher_analytics,      name='teacher_analytics'),
    path('teacher/export/excel/',      views.export_gradebook_excel, name='export_gradebook_excel'),

    # ── История решений ─────────────────────────────────────────────────────────
    path('works/<int:work_id>/history/', views.solution_history, name='solution_history'),

    # ── API ───────────────────────────────────────────────────────────────────
    path('api/session-time/', views.get_session_time, name='get_session_time'),
    path('api/activity-data/', views.get_activity_data, name='get_activity_data'),
    path('api/check-code/<int:solution_id>/', views.check_code, name='check_code'),
    path('api/check-status/<int:check_id>/', views.get_check_status, name='get_check_status'),
    path('api/test-code/<int:work_id>/', views.test_code_locally, name='test_code_locally'),
    path('api/run-code/', views.run_code_snippet, name='run_code_snippet'),
    path('api/unlock-hint/<int:hint_id>/', views.unlock_hint, name='unlock_hint'),

    # ── Продление дедлайна ────────────────────────────────────────────────────
    path('works/<int:work_id>/request-extension/', views.request_deadline_extension, name='request_deadline_extension'),
    path('teacher/extension/<int:ext_id>/action/', views.approve_deadline_extension, name='approve_deadline_extension'),

    # ── Dev auto-reload (только при DEBUG=True) ───────────────────────────────
    path('dev-reload/', views.dev_reload, name='dev_reload'),
]
