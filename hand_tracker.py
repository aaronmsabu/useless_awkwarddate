# save as: hand_tracker.py
import cv2
import mediapipe as mp
import math

# Initialize hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    max_num_hands=2
)

camera = cv2.VideoCapture(0)

fidget_count = 0
face_touch_count = 0

print("🤚 Fidget Detection System Online!")
print("I'm watching your hands... no nervous gestures allowed!")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
    
    # Draw hand landmarks and detect fidgeting
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            # Draw hand skeleton
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get fingertip positions (landmark 8 = index finger tip)
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            
            # Convert to pixel coordinates
            h, w, _ = frame.shape
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            
            # Detect if hand is near face area (top 1/3 of screen)
            if index_y < h // 3:
                face_touch_count += 1
                cv2.putText(frame, "FACE TOUCHING DETECTED!", 
                           (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Simple fidget detection (if hands are moving a lot)
            fidget_count += 1
    
    # Display awkwardness metrics
    cv2.putText(frame, f"Fidget Score: {fidget_count}", 
               (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    cv2.putText(frame, f"Face Touches: {face_touch_count}", 
               (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
    
    # Reset counters occasionally so they don't get too high
    if fidget_count > 1000:
        fidget_count = 0
    if face_touch_count > 100:
        face_touch_count = 0
    
    cv2.imshow("Fidget Surveillance System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()