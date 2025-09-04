from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor
import threading

# Thread-safe cache for translations
_translation_cache = {}
_cache_lock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=4)


def translate_text_sync(text, target_lang="en"):
    """Synchronous translation with caching."""
    key = (text, target_lang)
    with _cache_lock:
        if key in _translation_cache:
            return _translation_cache[key]

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        with _cache_lock:
            _translation_cache[key] = translated
        return translated
    except Exception as e:
        return f"Error: {e}"


def translate_text_async(text, target_lang="en", callback=None):
    """
    Runs translation in background thread (non-blocking).
    Callback will be called once done. Returns Future object.
    """
    def _translate():
        return translate_text_sync(text, target_lang)

    future = _executor.submit(_translate)
    if callback:
        def _call_cb(fut):
            result = fut.result()
            callback(result)
        future.add_done_callback(_call_cb)
    return future


def translate_to_english_sync(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        return f"Error: {e}"
