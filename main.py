from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import os
from pathlib import Path
import asyncio
from utils.video_processor import VideoProcessor

# Tạo thư mục nếu chưa tồn tại
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="AI Video Swap App")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Khởi tạo video processor
video_processor = VideoProcessor()

@app.get("/")
async def root():
    """Trả về trang chính"""
    return FileResponse("static/index.html")

@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Upload video"""
    try:
        # Kiểm tra định dạng file
        allowed_formats = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_formats:
            raise HTTPException(status_code=400, detail=f"Định dạng không hỗ trợ. Chỉ hỗ trợ: {', '.join(allowed_formats)}")
        
        # Kiểm tra kích thước (500MB)
        contents = await file.read()
        if len(contents) > 500 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File quá lớn (max 500MB)")
        
        # Lưu file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {
            "filename": file.filename,
            "size": len(contents),
            "message": "Upload thành công"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/process")
async def process_video(filename: str, action: str = "swap"):
    """Xử lý video"""
    try:
        input_path = UPLOAD_DIR / filename
        
        if not input_path.exists():
            raise HTTPException(status_code=404, detail="File không tìm thấy")
        
        if action not in ["swap", "blur"]:
            raise HTTPException(status_code=400, detail="Action không hợp lệ")
        
        # Tạo tên file output
        output_filename = f"{Path(filename).stem}_processed_{action}.mp4"
        output_path = OUTPUT_DIR / output_filename
        
        # Xử lý video
        if action == "swap":
            success = await asyncio.to_thread(video_processor.process_face_swap, str(input_path), str(output_path))
        else:  # blur
            success = await asyncio.to_thread(video_processor.process_face_blur, str(input_path), str(output_path))
        
        if not success:
            raise HTTPException(status_code=500, detail="Lỗi khi xử lý video")
        
        return {
            "status": "success",
            "output_filename": output_filename,
            "message": "Xử lý thành công"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{filename}")
async def download_video(filename: str):
    """Download video đã xử lý"""
    try:
        file_path = OUTPUT_DIR / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File không tìm thấy")
        
        return FileResponse(file_path, filename=filename)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/list-outputs")
async def list_outputs():
    """Liệt kê video đã xử lý"""
    try:
        files = list(OUTPUT_DIR.glob("*.mp4"))
        return {
            "files": [f.name for f in files],
            "count": len(files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check"""
    return {"status": "ok", "service": "AI Video Swap App"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
