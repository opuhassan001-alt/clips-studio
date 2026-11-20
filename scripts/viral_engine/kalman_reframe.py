"""
MediaPipe FaceMesh + Kalman Filter 9:16 Smooth Auto-Reframe.
Module 4 of Universal Master Spec 3.0.
"""

import cv2
import numpy as np
from pathlib import Path


class KalmanSmoothBox:
    """Smooths 9:16 crop window panning using a Kalman Filter to prevent jarring cuts."""
    def __init__(self, initial_x: float):
        self.kf = cv2.KalmanFilter(2, 1)
        self.kf.measurementMatrix = np.array([[1, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 1], [0, 1]], np.float32)
        self.kf.processNoiseCov = np.array([[1e-2, 0], [0, 5e-2]], np.float32)
        self.kf.measurementNoiseCov = np.array([[1e-1]], np.float32)
        self.kf.statePre = np.array([[initial_x], [0]], np.float32)
        self.kf.statePost = np.array([[initial_x], [0]], np.float32)

    def update(self, target_x: float) -> int:
        self.kf.predict()
        corrected = self.kf.correct(np.array([[np.float32(target_x)]]))
        return int(corrected[0][0])


def auto_reframe_to_916(input_video: str, output_video: str, sample_step: int = 1) -> bool:
    """
    Reframes landscape 16:9 or arbitrary video to 9:16 vertical using face tracking + Kalman smoothing.
    Falls back gracefully if MediaPipe is not present by using OpenCV Haar/YuNet or center crop.
    """
    input_path = Path(input_video)
    output_path = Path(output_video)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        print(f"❌ Error opening video: {input_video}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    target_w = int(h * (9 / 16))

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (target_w, h))

    kalman = KalmanSmoothBox(w // 2)

    # Initialize face detector: MediaPipe with OpenCV Cascade fallback
    mp_face_mesh = None
    try:
        import mediapipe as mp
        mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=2,
            refine_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
    except Exception:
        mp_face_mesh = None

    # OpenCV Haar Cascade fallback if MediaPipe unavailable
    face_cascade = None
    if mp_face_mesh is None:
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(cascade_path)

    last_target_x = w // 2
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_idx += 1
        target_x = last_target_x

        # Track face every sample_step frames to maintain high rendering speed
        if frame_idx % sample_step == 0:
            if mp_face_mesh is not None:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = mp_face_mesh.process(rgb)
                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0].landmark
                    xs = [lm.x * w for lm in landmarks]
                    target_x = int(np.mean(xs))
            elif face_cascade is not None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                if len(faces) > 0:
                    fx, fy, fw, fh = faces[0]
                    target_x = fx + (fw // 2)

            last_target_x = target_x

        smooth_x = kalman.update(target_x)
        start_x = max(0, min(smooth_x - (target_w // 2), w - target_w))
        cropped = frame[:, start_x : start_x + target_w]
        out.write(cropped)

    cap.release()
    out.release()
    if mp_face_mesh is not None:
        mp_face_mesh.close()

    return output_path.exists() and output_path.stat().st_size > 0
