# save as: face_detector.py
import cv2
import mediapipe as mp

# Initialize the "Face Judgment System"
mp_face = mp.solutions.face_detection
mp_draw = mp.solutions.drawing_utils

face_detector = mp_face.FaceDetection(min_detection_confidence=0.5)

camera = cv2.VideoCapture(0)

print("🎭 Face Detection Active!")
print("Now I can see your face... and judge it!")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    # Convert color (MediaPipe likes RGB, OpenCV uses BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detect faces (the magic happens here!)
    results = face_detector.process(rgb_frame)
    
    # Draw boxes around detected faces
    if results.detections:
        for detection in results.detections:
            # Draw face box with judgment
            mp_draw.draw_detection(frame, detection)
            
            # Add funny labels
            cv2.putText(frame, f"SUSPICIOUS FACE DETECTED", 
                       (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame, f"Awkwardness Level: LOADING...", 
                       (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    else:
        cv2.putText(frame, "NO FACE DETECTED - ARE YOU HIDING?", 
                   (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    cv2.imshow("Face Judgment System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
