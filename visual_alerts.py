# save as: visual_alerts.py
import cv2
import mediapipe as mp
import time
import random
import numpy as np

class VisualAlertSystem:
    def __init__(self):
        # Previous detector code here (face + hand detection)
        self.mp_face = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
        self.awkwardness_score = 0
        self.alert_active = False
        self.alert_start_time = 0
        
        # Alert visual effects
        self.colors = [(0, 0, 255), (255, 0, 0), (0, 255, 255), (255, 0, 255)]
        self.current_color = 0
        
        # Floating emojis system
        self.floating_emojis = []
        self.emoji_list = ["😰", "😅", "🤦", "💀", "🚨", "⚠️", "😳", "🤷", "👀"]
    
    def add_floating_emoji(self, emoji_type="random"):
        """Add a floating emoji to the screen"""
        if emoji_type == "random":
            emoji = random.choice(self.emoji_list)
        else:
            emoji = emoji_type
            
        # Random position and movement
        emoji_data = {
            'emoji': emoji,
            'x': random.randint(50, 550),
            'y': random.randint(100, 400),
            'speed_x': random.randint(-2, 2),
            'speed_y': random.randint(-3, -1),
            'life': 100  # How long it lasts
        }
        self.floating_emojis.append(emoji_data)
    
    def update_floating_emojis(self, frame):
        """Update and draw floating emojis"""
        for emoji in self.floating_emojis[:]:  # Copy list to modify during iteration
            # Move emoji
            emoji['x'] += emoji['speed_x']
            emoji['y'] += emoji['speed_y']
            emoji['life'] -= 1
            
            # Draw emoji (using text since we can't easily draw actual emojis)
            cv2.putText(frame, emoji['emoji'], 
                       (int(emoji['x']), int(emoji['y'])), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
            
            # Remove dead emojis
            if emoji['life'] <= 0 or emoji['y'] < 0:
                self.floating_emojis.remove(emoji)
    
    def draw_alert_border(self, frame):
        """Draw flashing border for high alert"""
        if not self.alert_active:
            return
            
        h, w, _ = frame.shape
        color = self.colors[self.current_color % len(self.colors)]
        thickness = 10
        
        # Draw flashing border
        cv2.rectangle(frame, (0, 0), (w, h), color, thickness)
        
        # Flash effect
        if time.time() - self.alert_start_time > 0.5:
            self.current_color += 1
            self.alert_start_time = time.time()
    
    def draw_awkwardness_meter(self, frame):
        """Draw a visual awkwardness meter"""
        h, w, _ = frame.shape
        
        # Meter background
        meter_x, meter_y = w - 200, 50
        meter_w, meter_h = 150, 20
        
        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + meter_w, meter_y + meter_h), 
                     (100, 100, 100), -1)
        
        # Meter fill based on awkwardness score
        fill_width = int((self.awkwardness_score / 100) * meter_w)
        fill_width = min(fill_width, meter_w)  # Cap at meter width
        
        # Color changes based on level
        if self.awkwardness_score < 20:
            meter_color = (0, 255, 0)  # Green
        elif self.awkwardness_score < 50:
            meter_color = (0, 255, 255)  # Yellow
        else:
            meter_color = (0, 0, 255)  # Red
        
        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + fill_width, meter_y + meter_h), 
                     meter_color, -1)
        
        # Meter label
        cv2.putText(frame, "CRINGE METER", (meter_x, meter_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def process_frame(self, frame):
        """Main processing function"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces and hands (simplified version)
        face_results = self.face_detector.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        
        frame_awkwardness = 0
        
        # Face detection and awkwardness calculation
        if face_results.detections:
            for detection in face_results.detections:
                self.mp_draw.draw_detection(frame, detection)
        else:
            frame_awkwardness += 2  # No face = awkward
        
        # Hand detection
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                frame_awkwardness += 1  # Hands visible = fidgeting
        
        # Update awkwardness score
        self.awkwardness_score += frame_awkwardness * 0.5
        self.awkwardness_score = max(0, self.awkwardness_score - 0.2)  # Slow decay
        
        # Trigger visual alerts
        if self.awkwardness_score > 30 and not self.alert_active:
            self.alert_active = True
            self.alert_start_time = time.time()
            # Add some emojis for dramatic effect
            for _ in range(3):
                self.add_floating_emoji()
        
        if self.awkwardness_score < 10:
            self.alert_active = False
        
        # Add random emojis occasionally
        if random.random() < 0.02:  # 2% chance per frame
            self.add_floating_emoji()
        
        # Draw all visual elements
        self.draw_alert_border(frame)
        self.draw_awkwardness_meter(frame)
        self.update_floating_emojis(frame)
        
        # Main awkwardness display
        level_text = self.get_awkwardness_level()
        cv2.putText(frame, f"Awkwardness: {self.awkwardness_score:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(frame, level_text, 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        return frame
    
    def get_awkwardness_level(self):
        """Get current awkwardness description"""
        if self.awkwardness_score < 5:
            return "😊 Smooth & Confident"
        elif self.awkwardness_score < 15:
            return "😐 Slightly Nervous"
        elif self.awkwardness_score < 30:
            return "😅 Getting Uncomfortable"
        elif self.awkwardness_score < 50:
            return "😰 Major Awkwardness"
        else:
            return "🚨 SOCIAL CATASTROPHE!"

# Main execution
alert_system = VisualAlertSystem()
camera = cv2.VideoCapture(0)

print("🎨 Visual Alert System Online!")
print("Prepare for emoji explosions and flashing lights!")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    # Process frame with all visual effects
    frame = alert_system.process_frame(frame)
    
    cv2.imshow("Awkwardness Alert System", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
