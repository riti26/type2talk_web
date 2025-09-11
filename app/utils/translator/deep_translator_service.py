from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
import threading

from app.utils.add_data_manager import AppDataManager

# Thread-safe cache for translations
_translation_cache = {}
_cache_lock = threading.Lock()

_executor = ThreadPoolExecutor(max_workers=4)

def _translate_sync(text, target_lang="en"):
    if target_lang == 'en':
        return text
    try:
        # Check cache first
        key = (text, target_lang)
        with _cache_lock:
            if key in _translation_cache:
                return _translation_cache[key]

        # If not cached, do translation
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)

        # Cache result
        with _cache_lock:
            _translation_cache[key] = translated

        return translated
    except Exception as e:
        return f"Error: {e}"

def translate_text_async(text, target_lang="en", callback=None):
    """
    Submit translation to thread pool.
    If callback is provided, call it with the translated text once ready.
    Returns a Future object.
    """
    if target_lang == 'en':
        return text
    future = _executor.submit(_translate_sync, text, target_lang)
    if callback:
        def _call_cb(fut):
            result = fut.result()
            callback(result)
        future.add_done_callback(_call_cb)
    return future

def translate_to_english_sync(text):
    currentLanguage = AppDataManager.get_language()
    if currentLanguage == 'en':
        return text
    try:
        return GoogleTranslator(currentLanguage, target='en').translate(text)
    except Exception as e:
        return f"Error: {e}"
