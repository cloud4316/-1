"""
Утилиты для работы с файлами и кодировками
"""
import os
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def fix_file_encoding(file_path: str) -> str:
    """
    Исправляет кодировку файла и возвращает исправленное содержимое
    """
    try:
        # Читаем файл как байты
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        # Определяем кодировку
        if HAS_CHARDET:
            detected = chardet.detect(raw_data)
        else:
            # Fallback: пробуем utf-8, потом cp1251
            for enc in ('utf-8', 'cp1251', 'latin-1'):
                try:
                    raw_data.decode(enc)
                    detected = {'encoding': enc, 'confidence': 1.0}
                    break
                except UnicodeDecodeError:
                    continue
            else:
                detected = {'encoding': 'utf-8', 'confidence': 0.5}
        encoding = detected.get('encoding', 'utf-8')
        confidence = detected.get('confidence', 0)
        
        # Если уверенность низкая, пробуем разные кодировки
        if confidence < 0.7:
            encodings_to_try = ['utf-8', 'cp1251', 'latin1', 'iso-8859-1']
            for enc in encodings_to_try:
                try:
                    content = raw_data.decode(enc)
                    # Проверяем, что это не кракозябры
                    if is_valid_text(content):
                        encoding = enc
                        break
                except (UnicodeDecodeError, UnicodeError):
                    continue
        
        # Декодируем с правильной кодировкой
        content = raw_data.decode(encoding, errors='replace')
        
        # Если все еще есть кракозябры, пытаемся исправить
        if has_corrupted_text(content):
            content = fix_corrupted_text(content)
        
        return content
        
    except Exception as e:
        print(f"Ошибка исправления кодировки файла {file_path}: {e}")
        # Возвращаем содержимое с заменой ошибок
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        return raw_data.decode('utf-8', errors='replace')


def is_valid_text(text: str) -> bool:
    """Проверяет, что текст не содержит кракозябр"""
    # Проверяем на наличие русских букв в правильной кодировке
    russian_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    russian_chars += russian_chars.upper()
    
    # Если есть русские символы, проверяем, что они читаемые
    if any(char in text.lower() for char in russian_chars):
        # Проверяем, что нет кракозябр типа "Р'РІРµРґРёС‚Рµ"
        if 'Р' in text and 'РІ' in text:
            return False
    
    return True


def has_corrupted_text(text: str) -> bool:
    """Проверяет, есть ли в тексте кракозябры"""
    corrupted_patterns = [
        'Р' + 'РІ',  # Типичный паттерн кракозябр
        'РІРµРґРёС‚Рµ',  # "введите" в кракозябрах
        'РґР»СЏ',  # "для" в кракозябрах
        'СЃС‚СЂРѕРєРё',  # "строки" в кракозябрах
        'Р±РµРіСѓС‰РµР№',  # "бегущей" в кракозябрах
        'С‚РµРєСЃС‚',  # "текст" в кракозябрах
        'Р' + 'РІРµРґРёС‚Рµ',  # "введите" в кракозябрах
    ]
    
    return any(pattern in text for pattern in corrupted_patterns)


def fix_corrupted_text(text: str) -> str:
    """Пытается исправить кракозябры в тексте"""
    # Расширенный словарь для замены кракозябр на правильный текст
    replacements = {
        # Основные слова
        'Р' + 'РІРµРґРёС‚Рµ': 'введите',
        'РґР»СЏ': 'для',
        'СЃС‚СЂРѕРєРё': 'строки',
        'Р±РµРіСѓС‰РµР№': 'бегущей',
        'С‚РµРєСЃС‚': 'текст',
        'РІРІРµРґРёС‚Рµ': 'введите',
        'РІРІРµРґРёС‚Рµ': 'введите',
        
        # Дополнительные паттерны
        'Р' + 'РІРµРґРёС‚Рµ С‚РµРєСЃС‚ РґР»СЏ Р±РµРіСѓС‰РµР№ СЃС‚СЂРѕРєРё': 'введите текст для бегущей строки',
        'Р' + 'РІРµРґРёС‚Рµ': 'введите',
        'С‚РµРєСЃС‚': 'текст',
        'РґР»СЏ': 'для',
        'Р±РµРіСѓС‰РµР№': 'бегущей',
        'СЃС‚СЂРѕРєРё': 'строки',
        
        # Буквы по отдельности
        'Р' + 'РІ': 'в',
        'Рµ': 'е',
        'Рґ': 'д',
        'Рё': 'и',
        'С‚': 'т',
        'Рµ': 'е',
        'СЃ': 'с',
        'СЂ': 'р',
        'Рѕ': 'о',
        'Рє': 'к',
        'Рё': 'и',
        'Р±': 'б',
        'Рі': 'г',
        'Сѓ': 'у',
        'С‰': 'щ',
        'Рµ': 'е',
        'Р№': 'й',
    }
    
    # Применяем замены
    for corrupted, correct in replacements.items():
        text = text.replace(corrupted, correct)
    
    return text


def save_file_with_correct_encoding(file_path: str, content: str) -> str:
    """
    Сохраняет файл с правильной кодировкой UTF-8
    """
    try:
        # Создаем новый файл с правильной кодировкой
        new_file_path = file_path + '.utf8'
        
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Заменяем старый файл новым
        if os.path.exists(file_path):
            os.remove(file_path)
        os.rename(new_file_path, file_path)
        
        return file_path
        
    except Exception as e:
        print(f"Ошибка сохранения файла с правильной кодировкой: {e}")
        return file_path