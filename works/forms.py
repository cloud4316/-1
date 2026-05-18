from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
from .models import Solution
import os
import re
import unicodedata

ALLOWED_EXTENSIONS = {".py", ".cpp", ".c", ".java", ".kt", ".js", ".cs"}
MAX_FILE_SIZE_MB   = 2


# ── Форма загрузки решения ─────────────────────────────────────────────────
class SolutionForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        label="Комментарий",
    )

    class Meta:
        model  = Solution
        fields = ["code_file", "comment"]
        labels = {"code_file": "Загрузите файл с решением"}

    def clean_code_file(self):
        f = self.cleaned_data.get("code_file")
        if not f:
            raise ValidationError("Файл обязателен")
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(f"Недопустимое расширение. Разрешено: {', '.join(ALLOWED_EXTENSIONS)}")
        if f.size > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationError(f"Размер файла превышает {MAX_FILE_SIZE_MB} МБ")
        return f


# ── Вспомогательная функция — генерация username ───────────────────────────
_TRANSLIT = {
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"yo","ж":"zh",
    "з":"z","и":"i","й":"j","к":"k","л":"l","м":"m","н":"n","о":"o",
    "п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"kh","ц":"ts",
    "ч":"ch","ш":"sh","щ":"sch","ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya",
}

def _translit(text: str) -> str:
    text = text.lower().strip()
    return "".join(_TRANSLIT.get(ch, ch) for ch in text)

def generate_username(last_name: str, first_name: str) -> str:
    """Генерирует уникальный username из ФИО (транслитерация)."""
    base = f"{_translit(last_name)}_{_translit(first_name)}"
    base = re.sub(r"[^a-z0-9_]", "", base) or "user"
    username = base
    counter  = 1
    while User.objects.filter(username=username).exists():
        username = f"{base}_{counter}"
        counter += 1
    return username


# ── Форма регистрации ──────────────────────────────────────────────────────
class RegistrationForm(forms.Form):
    last_name  = forms.CharField(
        max_length=50, label="Фамилия",
        widget=forms.TextInput(attrs={"placeholder": "Иванов", "autofocus": True}),
    )
    first_name = forms.CharField(
        max_length=50, label="Имя",
        widget=forms.TextInput(attrs={"placeholder": "Иван"}),
    )
    middle_name = forms.CharField(
        max_length=50, label="Отчество (необязательно)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Иванович"}),
    )
    group = forms.CharField(
        max_length=20, label="Группа",
        widget=forms.TextInput(attrs={"placeholder": "ИТ-21"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Придумайте пароль"}),
        min_length=6,
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
    )

    def clean_last_name(self):
        v = self.cleaned_data["last_name"].strip()
        if not re.match(r"^[А-ЯЁа-яёA-Za-z\-]+$", v):
            raise ValidationError("Фамилия должна содержать только буквы")
        return v.capitalize()

    def clean_first_name(self):
        v = self.cleaned_data["first_name"].strip()
        if not re.match(r"^[А-ЯЁа-яёA-Za-z\-]+$", v):
            raise ValidationError("Имя должно содержать только буквы")
        return v.capitalize()

    def clean(self):
        data = super().clean()
        p1 = data.get("password1", "")
        p2 = data.get("password2", "")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают")

        last  = data.get("last_name", "")
        first = data.get("first_name", "")
        if last and first:
            exists = User.objects.filter(
                last_name__iexact=last,
                first_name__iexact=first,
            ).exists()
            if exists:
                raise ValidationError(
                    f"Пользователь «{last} {first}» уже зарегистрирован. "
                    "Обратитесь к преподавателю."
                )
        return data


# ── Форма входа (Фамилия Имя + пароль) ────────────────────────────────────
class FullNameLoginForm(forms.Form):
    full_name = forms.CharField(
        label="Фамилия и Имя",
        widget=forms.TextInput(attrs={
            "placeholder": "Иванов Иван",
            "autofocus": True,
            "autocomplete": "off",
        }),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Ваш пароль"}),
    )
