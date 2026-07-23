# AI Video Swap App

Ứng dụng hoán đổi khuôn mặt trong video sử dụng AI.

## Tính năng
- 🎥 Upload video (MP4, AVI, MOV)
- 😊 Phát hiện và hoán đổi khuôn mặt tự động
- ⚡ Xử lý nhanh với MediaPipe
- 💾 Tải video đã xử lý
- 🌐 Web interface thân thiện

## Cài đặt

### Yêu cầu
- Python 3.8+
- ffmpeg

### Bước 1: Clone repository
```bash
git clone https://github.com/levansangbahai-alt/video-swap-app.git
cd video-swap-app
```

### Bước 2: Tạo virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# hoặc
venv\Scripts\activate  # Windows
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Cài đặt ffmpeg
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows (qua chocolatey)
choco install ffmpeg
```

## Chạy ứng dụng

### Khởi động server
```bash
python main.py
```

### Mở trình duyệt
Go to `http://localhost:8000`

## Cách sử dụng

1. **Tải video lên**: Click "Chọn video" hoặc kéo thả file
2. **Chọn hành động**: Swap face hoặc blur face
3. **Xử lý**: Click "Xử lý" và đợi
4. **Tải xuống**: Download video đã xử lý

## Cấu trúc dự án

```
video-swap-app/
├── main.py                 # FastAPI server
├── requirements.txt        # Dependencies
├── static/
│   ├── index.html         # Frontend
│   ├── style.css          # Styling
│   └── script.js          # JavaScript
├── uploads/               # Thư mục lưu video tải lên
├── outputs/               # Thư mục lưu video xử lý
└── utils/
    ├── face_swap.py       # Xử lý swap face
    ├── video_processor.py # Xử lý video
    └── helpers.py         # Hàm hỗ trợ
```

## Công nghệ sử dụng

- **FastAPI**: Web framework
- **OpenCV**: Xử lý video
- **MediaPipe**: Phát hiện khuôn mặt
- **dlib**: Face recognition
- **numpy**: Tính toán
- **ffmpeg**: Encode/decode video

## Lưu ý

- Video được xử lý lần lượt (tuỳ theo kích thước)
- Thư mục `uploads/` và `outputs/` tự động tạo
- Giới hạn file upload: 500MB
- Định dạng hỗ trợ: MP4, AVI, MOV, MKV

## Troubleshooting

### Lỗi "ffmpeg not found"
```bash
# Cài đặt ffmpeg
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
```

### Lỗi port 8000 đã được sử dụng
```bash
python main.py --port 8001
```

## Licenense

MIT
