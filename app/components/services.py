import os
import time
from werkzeug.utils import secure_filename


def handle_file_upload(icon_file):
    # Extract original extension
    ext = os.path.splitext(icon_file.filename)[1]
    
    # Use current timestamp as filename
    timestamp = str(int(time.time()))
    filename = f"{timestamp}{ext}"
    save_folder = os.path.join("app", "static", "images")
    os.makedirs(save_folder, exist_ok=True)
    save_path = os.path.join(save_folder, filename)
    icon_file.save(save_path)
    icon_path = f"images/{filename}"
    return icon_path
