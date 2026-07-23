import os
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def ensure_directories():
    """Tạo các thư mục cần thiết"""
    directories = ['uploads', 'outputs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def get_file_size(file_path: str) -> str:
    """Lấy kích thước file dạng human-readable"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def cleanup_old_files(directory: str, max_age_hours: int = 24):
    """Xóa các file cũ hơn max_age_hours"""
    import time
    current_time = time.time()
    for file in Path(directory).glob('*'):
        file_age = current_time - os.path.getmtime(file)
        if file_age > max_age_hours * 3600:
            try:
                file.unlink()
                logging.info(f"Deleted old file: {file}")
            except Exception as e:
                logging.error(f"Error deleting file {file}: {e}")
