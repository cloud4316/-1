from django.contrib import admin
from .models import (Notification, TeacherComment,
    PracticalWork, Solution, UserProgress, UserSession, PageView, CodeCheck,
    TheoryModule, TheoryLesson, LessonProgress,
    Quiz, Question, AnswerChoice, QuizAttempt,
)


@admin.register(PracticalWork)
class PracticalWorkAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'topic', 'difficulty', 'language', 'is_active', 'max_score')
    list_display_links = ('title',)
    list_filter = ('topic', 'difficulty', 'language', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('order',)
    list_editable = ('is_active', 'order')


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('student', 'work', 'status', 'score', 'submitted_at')
    list_filter = ('status', 'work')
    search_fields = ('student__username', 'work__title')
    ordering = ('-submitted_at',)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed_works', 'total_works', 'total_score', 'streak_days', 'level')
    search_fields = ('user__username',)


admin.site.register(UserSession)
admin.site.register(PageView)
admin.site.register(CodeCheck)


# ── Теория ────────────────────────────────────────────────────────────────────

class TheoryLessonInline(admin.TabularInline):
    model = TheoryLesson
    extra = 1
    fields = ('order', 'title', 'estimated_minutes')


@admin.register(TheoryModule)
class TheoryModuleAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'lessons_count', 'is_active')
    list_display_links = ('title',)
    list_editable = ('order', 'is_active')
    inlines = [TheoryLessonInline]


@admin.register(TheoryLesson)
class TheoryLessonAdmin(admin.ModelAdmin):
    list_display = ('module', 'order', 'title', 'estimated_minutes')
    list_filter = ('module',)
    search_fields = ('title',)
    ordering = ('module', 'order')


admin.site.register(LessonProgress)


# ── Тесты ─────────────────────────────────────────────────────────────────────

class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4
    fields = ('order', 'text', 'is_correct')


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ('order', 'text', 'code_snippet', 'q_type', 'explanation')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'questions_count', 'pass_score', 'is_active')
    list_filter = ('is_active', 'module')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'order', 'text', 'q_type')
    list_filter = ('quiz', 'q_type')
    inlines = [AnswerChoiceInline]


admin.site.register(QuizAttempt)

admin.site.register(Notification)
admin.site.register(TeacherComment)
