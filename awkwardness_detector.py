# save as: awkwardness_detector.py
import cv2
import mediapipe as mp
import time
import random

class AwkwardnessDetector:
    def __init__(self):
        # Initialize face and hand detection
        self.mp_face = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
        # Awkwardness tracking variables
        self.awkwardness_score = 0
        self.face_touch_count = 0
        self.no_face_time = 0
        self.last_face_time = time.time()
        
        # Fun awkwardness categories
        self.awkwardness_levels = [
            (0, "😊 Smooth Operator"),
            (5, "😐 Slightly Uncomfortable"), 
            (15, "😅 Getting Weird"),
            (30, "😰 Major Cringe Alert"),
            (50, "🚨 SOCIAL DISASTER"),
            (100, "💀 ABORT MISSION!")
        ]
        
        # Silly awkward behaviors to detect
        self.behaviors_detected = []
    
    def get_awkwardness_level(self, score):
        """Convert score to funny description"""
        for threshold, description in reversed(self.awkwardness_levels):
            if score >= threshold:
                return description
        return "😊 Smooth Operator"
    
    def detect_awkwardness(self, frame):
        """The main awkwardness detection algorithm"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_results = self.face_detector.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        
        frame_awkwardness = 0
        current_behaviors = []
        
        # Check if face is visible
        if face_results.detections:
            self.last_face_time = time.time()
            self.no_face_time = 0
            
            # Draw face detection
            for detection in face_results.detections:
                self.mp_draw.draw_detection(frame, detection)
        else:
            # No face detected - are they looking away?
            self.no_face_time = time.time() - self.last_face_time
            if self.no_face_time > 2:  # Looking away for 2+ seconds
                frame_awkwardness += 5
                current_behaviors.append("👀 AVOIDING EYE CONTACT")
        
        # Check hand positions (fidgeting/face touching)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Get fingertip position
                index_tip = hand_landmarks.landmark[8]
                h, w, _ = frame.shape
                finger_y = int(index_tip.y * h)
                
                # Face touching detection
                if finger_y < h // 3:  # Upper third of screen
                    self.face_touch_count += 1
                    frame_awkwardness += 2
                    current_behaviors.append("🤚 NERVOUS FACE TOUCHING")
                
                # Random awkward gesture detection (for fun)
                if random.random() < 0.01:  # 1% chance per frame
                    awkward_gestures = [
                        "✋ WEIRD HAND GESTURE",
                        "👆 POINTING AT NOTHING", 
                        "🤝 AWKWARD ARM POSITION",
                        "🤷 CONFUSED GESTURING"
                    ]
                    current_behaviors.append(random.choice(awkward_gestures))
                    frame_awkwardness += 3
        
        # Update overall awkwardness score
        self.awkwardness_score += frame_awkwardness
        
        # Slowly decrease score over time (forgiveness algorithm)
        if frame_awkwardness == 0:
            self.awkwardness_score = max(0, self.awkwardness_score - 0.1)
        
        # Update behavior list
        self.behaviors_detected = current_behaviors[-5:]  # Keep last 5 behaviors
        
        return frame_awkwardness

# Main program
detector = AwkwardnessDetector()
camera = cv2.VideoCapture(0)

print("🔬 Scientific Awkwardness Analysis System Activated!")
print("Preparing to judge your social performance...")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    # Detect awkwardness in current frame
    frame_awkwardness = detector.detect_awkwardness(frame)
    
    # Get current awkwardness level
    current_level = detector.get_awkwardness_level(detector.awkwardness_score)
    
    # Display results on screen
    cv2.putText(frame, f"Awkwardness Score: {detector.awkwardness_score:.1f}", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Status: {current_level}", 
               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # Show recent awkward behaviors
    y_pos = 90
    for behavior in detector.behaviors_detected:
        cv2.putText(frame, behavior, (10, y_pos), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        y_pos += 25
    
    # Add warning for high awkwardness
    if detector.awkwardness_score > 30:
        cv2.putText(frame, "⚠️ CRINGE WARNING ⚠️", 
                   (10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    
    cv2.imshow("Scientific Awkwardness Analyzer", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print(f"📊 Final Awkwardness Score: {detector.awkwardness_score:.1f}")
print("Analysis complete. Please consider social skills training. 😉")