import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Xử lý video với face detection và face swap"""
    
    def __init__(self):
        """Khởi tạo MediaPipe Face Detection"""
        self.mp_face_detection = mp.solutions.face_detection
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )
    
    def detect_faces(self, image: np.ndarray) -> list:
        """Phát hiện khuôn mặt trong ảnh"""
        h, w, c = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_image)
        
        faces = []
        if results.detections:
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Thêm padding
                x = max(0, x - 10)
                y = max(0, y - 10)
                width = min(w - x, width + 20)
                height = min(h - y, height + 20)
                
                faces.append({
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'confidence': detection.score[0]
                })
        
        return faces
    
    def blur_face(self, image: np.ndarray, face: dict, blur_strength: int = 30) -> np.ndarray:
        """Làm mờ khuôn mặt"""
        x, y, w, h = face['x'], face['y'], face['width'], face['height']
        
        # Kích thước blur phải lẻ
        if blur_strength % 2 == 0:
            blur_strength += 1
        
        # Lấy vùng khuôn mặt
        face_region = image[y:y+h, x:x+w]
        
        # Blur
        blurred = cv2.blur(face_region, (blur_strength, blur_strength))
        
        # Đặt lại vào ảnh
        image[y:y+h, x:x+w] = blurred
        
        return image
    
    def swap_faces(self, image: np.ndarray, face1: dict, face2: dict) -> np.ndarray:
        """Hoán đổi hai khuôn mặt (phiên bản đơn giản)"""
        try:
            x1, y1, w1, h1 = face1['x'], face1['y'], face1['width'], face1['height']
            x2, y2, w2, h2 = face2['x'], face2['y'], face2['width'], face2['height']
            
            # Lấy vùng khuôn mặt
            face1_region = image[y1:y1+h1, x1:x1+w1].copy()
            face2_region = image[y2:y2+h2, x2:x2+w2].copy()
            
            # Resize để kích thước giống nhau
            if face1_region.shape != face2_region.shape:
                face2_region = cv2.resize(face2_region, (w1, h1))
                face1_region_for_swap = face1_region.copy()
                face1_region = cv2.resize(face1_region, (w2, h2))
            else:
                face1_region_for_swap = face1_region.copy()
            
            # Hoán đổi
            image[y1:y1+h1, x1:x1+w1] = face2_region
            image[y2:y2+h2, x2:x2+w2] = face1_region
            
            return image
        except Exception as e:
            logger.error(f"Error in swap_faces: {e}")
            return image
    
    def process_face_blur(self, input_path: str, output_path: str) -> bool:
        """Xử lý video: làm mờ khuôn mặt"""
        try:
            cap = cv2.VideoCapture(input_path)
            
            if not cap.isOpened():
                logger.error(f"Cannot open video: {input_path}")
                return False
            
            # Lấy thông tin video
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Codec
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            if not out.isOpened():
                logger.error(f"Cannot create video writer: {output_path}")
                cap.release()
                return False
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Phát hiện khuôn mặt
                faces = self.detect_faces(frame)
                
                # Làm mờ từng khuôn mặt
                for face in faces:
                    frame = self.blur_face(frame, face, blur_strength=30)
                
                # Ghi frame
                out.write(frame)
                frame_count += 1
                
                # Log progress
                if frame_count % 30 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames")
            
            cap.release()
            out.release()
            
            logger.info(f"Video processed successfully: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return False
    
    def process_face_swap(self, input_path: str, output_path: str) -> bool:
        """Xử lý video: hoán đổi khuôn mặt"""
        try:
            cap = cv2.VideoCapture(input_path)
            
            if not cap.isOpened():
                logger.error(f"Cannot open video: {input_path}")
                return False
            
            # Lấy thông tin video
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Codec
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            if not out.isOpened():
                logger.error(f"Cannot create video writer: {output_path}")
                cap.release()
                return False
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Phát hiện khuôn mặt
                faces = self.detect_faces(frame)
                
                # Hoán đổi nếu có ít nhất 2 khuôn mặt
                if len(faces) >= 2:
                    frame = self.swap_faces(frame, faces[0], faces[1])
                
                # Ghi frame
                out.write(frame)
                frame_count += 1
                
                # Log progress
                if frame_count % 30 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames")
            
            cap.release()
            out.release()
            
            logger.info(f"Video processed successfully: {output_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error processing video: {e}")
            return False
