# Hướng dẫn cài đặt AI Video Swap App

## Yêu cầu hệ thống

- Python 3.8+
- ffmpeg
- pip (package manager Python)
- RAM: 4GB+ (khuyến nghị 8GB+)
- Dung lượng ổ cứng: 10GB+ (cho file tạm)

## Bước 1: Clone Repository

```bash
git clone https://github.com/levansangbahai-alt/video-swap-app.git
cd video-swap-app
```

## Bước 2: Cài đặt ffmpeg

### macOS
```bash
brew install ffmpeg
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### Windows (qua Chocolatey)
```bash
choco install ffmpeg
```

### Windows (tải trực tiếp)
1. Tải từ: https://ffmpeg.org/download.html
2. Giải nén
3. Thêm vào PATH

### Kiểm tra
```bash
ffmpeg -version
```

## Bước 3: Tạo Virtual Environment

### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

## Bước 4: Cài đặt Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Lưu ý cho Windows
Nếu gặp lỗi cài đặt dlib, bạn có thể:

```bash
# Cách 1: Cài đặt pre-built wheels
pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a665ba43d8435d6de63144746b846ee140e38688d4b475c0/dlib-19.8.1-cp36-cp36m-win_amd64.whl

# Cách 2: Bỏ qua dlib (sử dụng MediaPipe thay thế)
pip install -r requirements_minimal.txt
```

## Bước 5: Chạy ứng dụng

```bash
python main.py
```

Sau đó mở trình duyệt và truy cập:
```
http://localhost:8000
```

## Troubleshooting

### Lỗi: "ffmpeg not found"
```bash
# Kiểm tra ffmpeg
ffmpeg -version

# Nếu chưa cài, cài đặt theo hướng dẫn trên
```

### Lỗi: "ModuleNotFoundError: No module named 'mediapipe'"
```bash
pip install mediapipe --upgrade
```

### Lỗi: "Port 8000 already in use"
```bash
# Chạy trên port khác
python main.py --port 8001
```

### Lỗi: "Out of memory"
- Giảm độ phân giải video đầu vào
- Đóng các ứng dụng không cần thiết
- Tăng RAM nếu có thể

### Lỗi: "CUDA not found" (nếu dùng GPU)
```bash
pip install mediapipe[gpu]
```

## Cấu hình nâng cao

### Sử dụng GPU (NVIDIA CUDA)
```bash
pip install mediapipe[gpu]
```

### Thay đổi cấu hình
Chỉnh sửa file `.env`:
```bash
cp .env.example .env
# Chỉnh sửa .env theo ý muốn
```

## Test ứng dụng

```bash
# Kiểm tra kết nối
curl http://localhost:8000/api/health

# Kết quả mong đợi
{"status":"ok","service":"AI Video Swap App"}
```

## Dừng ứng dụng

Nhấn `Ctrl + C` trong terminal

## Cập nhật dependencies

```bash
pip install --upgrade -r requirements.txt
```
