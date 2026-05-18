from django.contrib import admin
from django.db.models import Count, Avg
from django.utils.html import format_html
from django.utils import timezone
from .models import (
    PracticalWork, Solution, UserProgress, UserSession, PageView, CodeCheck,
    TheoryModule, TheoryLesson, LessonProgress,
    Quiz, Question, AnswerChoice, QuizAttempt,
    Notification, TeacherComment,
    Achievement, UserAchievement,
    WorkHint, UserHintUnlock,
    DeadlineExtension,
)

# ── Настройка заголовков admin-сайта ──────────────────────────────────────────
admin.site.site_header = "AlgorithmMaster — Управление"
admin.site.site_title  = "AlgorithmMaster Admin"
admin.site.index_title = "Панель управления"


# ══════════════════════════════════════════════════════════════════════════════
# ПРАКТИЧЕСКИЕ РАБОТЫ
# ══════════════════════════════════════════════════════════════════════════════

class WorkHintInline(admin.TabularInline):
    model  = WorkHint
    extra  = 0
    fields = ('order', 'title', 'text', 'xp_cost')


@admin.register(PracticalWork)
class PracticalWorkAdmin(admin.ModelAdmin):
    list_display  = ('order', 'title', 'topic', 'difficulty', 'language',
                     'is_active', 'max_score', 'solutions_count')
    list_display_links = ('title',)
    list_filter   = ('topic', 'difficulty', 'language', 'is_active')
    search_fields = ('title', 'description')
    ordering      = ('order',)
    list_editable = ('is_active', 'order')
    inlines       = [WorkHintInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_sol=Count('solution'))

    @admin.display(description='Решений', ordering='_sol')
    def solutions_count(self, obj):
        return obj._sol


# ══════════════════════════════════════════════════════════════════════════════
# РЕШЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

@admin.action(description='Одобрить выбранные решения')
def approve_solutions(modeladmin, request, queryset):
    queryset.update(status='approved')


@admin.action(description='Вернуть на доработку')
def reject_solutions(modeladmin, request, queryset):
    queryset.update(status='rejected')


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display    = ('student', 'work', 'status_badge', 'score',
                       'attempt_number', 'submitted_at')
    list_filter     = ('status', 'work', 'work__topic')
    search_fields   = ('student__username', 'student__last_name', 'work__title')
    ordering        = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'created_at', 'compile_log')
    date_hierarchy  = 'submitted_at'
    actions         = [approve_solutions, reject_solutions]
    list_per_page   = 30

    @admin.display(description='Статус')
    def status_badge(self, obj):
        colors = {
            'submitted': '#f0ad4e',
            'approved':  '#5cb85c',
            'rejected':  '#d9534f',
            'pending':   '#5bc0de',
        }
        color = colors.get(obj.status, '#aaa')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:0.85em">{}</span>',
            color, obj.get_status_display()
        )


# ══════════════════════════════════════════════════════════════════════════════
# ПРОГРЕСС ПОЛЬЗОВАТЕЛЕЙ
# ══════════════════════════════════════════════════════════════════════════════

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display    = ('user', 'level', 'total_score', 'completed_works',
                       'total_works', 'streak_days', 'current_xp')
    search_fields   = ('user__username', 'user__last_name')
    readonly_fields = ('user',)
    ordering        = ('-total_score',)
    list_per_page   = 50


# ══════════════════════════════════════════════════════════════════════════════
# СЕССИИ И ПРОСМОТРЫ
# ══════════════════════════════════════════════════════════════════════════════

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display   = ('user', 'start_time', 'duration_display',
                      'page_views', 'is_active')
    list_filter    = ('is_active',)
    search_fields  = ('user__username', 'user__last_name')
    ordering       = ('-start_time',)
    date_hierarchy = 'start_time'
    readonly_fields = ('session_key', 'start_time', 'created_at')
    list_per_page  = 50

    @admin.display(description='Длительность')
    def duration_display(self, obj):
        m = obj.duration_minutes
        if m >= 60:
            return f'{obj.duration_hours} ч'
        return f'{m} мин'


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display   = ('user', 'page_title', 'page_url', 'time_spent_display', 'view_time')
    search_fields  = ('user__username', 'page_title', 'page_url')
    ordering       = ('-view_time',)
    date_hierarchy = 'view_time'
    readonly_fields = ('view_time',)
    list_per_page  = 100

    @admin.display(description='Время (сек)')
    def time_spent_display(self, obj):
        return f'{obj.time_spent} с'


# ══════════════════════════════════════════════════════════════════════════════
# ПРОВЕРКА КОДА
# ══════════════════════════════════════════════════════════════════════════════

@admin.register(CodeCheck)
class CodeCheckAdmin(admin.ModelAdmin):
    list_display    = ('solution', 'status', 'score', 'check_type', 'created_at')
    list_filter     = ('status', 'check_type')
    search_fields   = ('solution__student__username',)
    ordering        = ('-created_at',)
    date_hierarchy  = 'created_at'
    readonly_fields = ('created_at', 'completed_at', 'errors', 'warnings', 'suggestions')
    list_per_page   = 50


# ══════════════════════════════════════════════════════════════════════════════
# ТЕОРИЯ
# ══════════════════════════════════════════════════════════════════════════════

class TheoryLessonInline(admin.TabularInline):
    model  = TheoryLesson
    extra  = 1
    fields = ('order', 'title', 'estimated_minutes')


@admin.register(TheoryModule)
class TheoryModuleAdmin(admin.ModelAdmin):
    list_display       = ('order', 'title', 'icon', 'lessons_count',
                          'is_active', 'requires_quiz_pass')
    list_display_links = ('title',)
    list_editable      = ('order', 'is_active')
    list_filter        = ('is_active', 'requires_quiz_pass')
    search_fields      = ('title', 'description')
    inlines            = [TheoryLessonInline]


@admin.register(TheoryLesson)
class TheoryLessonAdmin(admin.ModelAdmin):
    list_display  = ('module', 'order', 'title', 'estimated_minutes')
    list_filter   = ('module',)
    search_fields = ('title',)
    ordering      = ('module__order', 'order')
    list_per_page = 50


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display   = ('user', 'lesson_module', 'lesson', 'completed', 'created_at')
    list_filter    = ('completed', 'lesson__module')
    search_fields  = ('user__username', 'user__last_name', 'lesson__title')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    list_per_page  = 100

    @admin.display(description='Раздел', ordering='lesson__module')
    def lesson_module(self, obj):
        return obj.lesson.module.title


# ══════════════════════════════════════════════════════════════════════════════
# ТЕСТЫ
# ══════════════════════════════════════════════════════════════════════════════

class AnswerChoiceInline(admin.TabularInline):
    model  = AnswerChoice
    extra  = 4
    fields = ('order', 'text', 'is_correct')


class QuestionInline(admin.StackedInline):
    model  = Question
    extra  = 1
    fields = ('order', 'text', 'code_snippet', 'q_type', 'explanation')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display  = ('title', 'module', 'questions_count', 'pass_score', 'is_active')
    list_filter   = ('is_active', 'module')
    search_fields = ('title',)
    list_editable = ('is_active', 'pass_score')
    inlines       = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display  = ('quiz', 'order', 'text', 'q_type')
    list_filter   = ('quiz', 'q_type')
    search_fields = ('text',)
    inlines       = [AnswerChoiceInline]


@admin.register(AnswerChoice)
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'text', 'is_correct')
    list_filter  = ('is_correct', 'question__quiz')
    search_fields = ('text',)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display    = ('user', 'quiz', 'score', 'passed', 'created_at')
    list_filter     = ('passed', 'quiz')
    search_fields   = ('user__username', 'user__last_name')
    date_hierarchy  = 'created_at'
    readonly_fields = ('created_at',)
    ordering        = ('-created_at',)


# ══════════════════════════════════════════════════════════════════════════════
# УВЕДОМЛЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

@admin.action(description='Отметить как прочитанные')
def mark_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


@admin.action(description='Отметить как непрочитанные')
def mark_unread(modeladmin, request, queryset):
    queryset.update(is_read=False)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display   = ('user', 'n_type', 'title', 'is_read', 'created_at')
    list_filter    = ('n_type', 'is_read')
    search_fields  = ('user__username', 'user__last_name', 'title', 'message')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    ordering       = ('-created_at',)
    actions        = [mark_read, mark_unread]
    list_per_page  = 50


# ══════════════════════════════════════════════════════════════════════════════
# КОММЕНТАРИИ ПРЕПОДАВАТЕЛЯ
# ══════════════════════════════════════════════════════════════════════════════

@admin.register(TeacherComment)
class TeacherCommentAdmin(admin.ModelAdmin):
    list_display    = ('teacher', 'solution', 'score', 'created_at')
    search_fields   = ('teacher__username', 'teacher__last_name',
                       'solution__student__last_name')
    date_hierarchy  = 'created_at'
    readonly_fields = ('created_at',)
    ordering        = ('-created_at',)
    list_per_page   = 30


# ══════════════════════════════════════════════════════════════════════════════
# ДОСТИЖЕНИЯ
# ══════════════════════════════════════════════════════════════════════════════

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display  = ('icon', 'key', 'title', 'xp_reward', 'description')
    search_fields = ('key', 'title', 'description')
    ordering      = ('key',)


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display   = ('user', 'achievement', 'earned_at')
    list_filter    = ('achievement',)
    search_fields  = ('user__username', 'user__last_name')
    date_hierarchy = 'earned_at'
    readonly_fields = ('earned_at',)
    ordering       = ('-earned_at',)


# ══════════════════════════════════════════════════════════════════════════════
# ПОДСКАЗКИ
# ══════════════════════════════════════════════════════════════════════════════

@admin.register(WorkHint)
class WorkHintAdmin(admin.ModelAdmin):
    list_display  = ('work', 'order', 'title', 'xp_cost')
    list_filter   = ('work',)
    search_fields = ('title', 'text', 'work__title')
    ordering      = ('work', 'order')


@admin.register(UserHintUnlock)
class UserHintUnlockAdmin(admin.ModelAdmin):
    list_display    = ('user', 'hint_work', 'hint', 'unlocked_at')
    search_fields   = ('user__username', 'user__last_name')
    date_hierarchy  = 'unlocked_at'
    readonly_fields = ('unlocked_at',)
    ordering        = ('-unlocked_at',)

    @admin.display(description='Работа', ordering='hint__work')
    def hint_work(self, obj):
        return obj.hint.work.title


# ══════════════════════════════════════════════════════════════════════════════
# ПРОДЛЕНИЕ ДЕДЛАЙНА
# ══════════════════════════════════════════════════════════════════════════════

@admin.action(description='Одобрить выбранные запросы')
def approve_extensions(modeladmin, request, queryset):
    queryset.update(status='approved', reviewed_at=timezone.now())


@admin.action(description='Отклонить выбранные запросы')
def reject_extensions(modeladmin, request, queryset):
    queryset.update(status='rejected', reviewed_at=timezone.now())


@admin.register(DeadlineExtension)
class DeadlineExtensionAdmin(admin.ModelAdmin):
    list_display    = ('user', 'work', 'status_badge', 'new_deadline',
                       'requested_at', 'reviewed_at')
    list_filter     = ('status',)
    search_fields   = ('user__username', 'user__last_name', 'work__title')
    date_hierarchy  = 'requested_at'
    readonly_fields = ('requested_at', 'reviewed_at')
    ordering        = ('-requested_at',)
    actions         = [approve_extensions, reject_extensions]

    @admin.display(description='Статус')
    def status_badge(self, obj):
        colors = {
            'pending':  '#f0ad4e',
            'approved': '#5cb85c',
            'rejected': '#d9534f',
        }
        color = colors.get(obj.status, '#aaa')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;'
            'border-radius:4px;font-size:0.85em">{}</span>',
            color, obj.get_status_display()
        )
