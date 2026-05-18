from .models import Subject


def subjects(request):
    """Передаёт список активных предметов и текущий предмет во все шаблоны."""
    all_subjects = list(Subject.objects.filter(is_active=True))
    current_slug = request.session.get('subject_slug', 'python')
    return {
        'subjects': all_subjects,
        'current_subject_slug': current_slug,
    }
