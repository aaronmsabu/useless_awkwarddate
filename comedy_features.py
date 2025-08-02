# save as: comedy_features.py
import cv2
import mediapipe as mp
import time
import random
import json
from datetime import datetime

class ComedyFeaturesSystem:
    def __init__(self):
        # Previous setup code
        self.mp_face = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
        self.awkwardness_score = 0
        
        # Comedy features
        self.meme_mode = False
        self.meme_timer = 0
        self.current_meme = ""
        
        # Statistics tracking
        self.session_stats = {
            'start_time': time.time(),
            'peak_awkwardness': 0,
            'total_fidgets': 0,
            'face_touches': 0,
            'eye_contact_breaks': 0,
            'awkward_moments': 0,
            'smooth_moments': 0
        }
        
        # Meme database
        self.memes = [
            "This is fine. 🔥🐕🔥",
            "Why are you like this? 🤷",
            "Congratulations, you played yourself 🎉",
            "Awkwardness level: It's over 9000! 💥",
            "Error 404: Social skills not found 🤖",
            "Smooth move, Shakespeare 📚",
            "Netflix: Are you still watching? Someone's daughter: 😴",
            "Me trying to be social: 🤡",
            "Current mood: Existential crisis 💀",
            "Social battery: 1% remaining 🔋"
        ]
        
        # Fake scientific explanations
        self.scientific_nonsense = [
            "Detecting elevated cringe particles in atmosphere",
            "Social awkwardness quantum field fluctuation detected",
            "Initiating emergency conversation protocol",
            "Measuring social entropy - increasing rapidly",
            "Warning: Approaching awkwardness event horizon",
            "Calculating optimal escape trajectory",
            "Social skills framework has encountered an error",
            "Activating emergency small talk subroutines"
        ]
        
        self.current_science_index = 0
    
    def toggle_meme_mode(self):
        """Toggle meme mode on/off"""
        self.meme_mode = not self.meme_mode
        if self.meme_mode:
            self.current_meme = random.choice(self.memes)
            self.meme_timer = time.time()
            print("🎭 MEME MODE ACTIVATED!")
        else:
            print("🎭 Meme mode deactivated")
    
    def update_statistics(self, frame_awkwardness, face_detected, hands_detected):
        """Update session statistics"""
        self.session_stats['peak_awkwardness'] = max(
            self.session_stats['peak_awkwardness'], 
            self.awkwardness_score
        )
        
        if hands_detected:
            self.session_stats['total_fidgets'] += 1
            
        if not face_detected:
            self.session_stats['eye_contact_breaks'] += 1
            
        if frame_awkwardness > 5:
            self.session_stats['awkward_moments'] += 1
        elif frame_awkwardness == 0:
            self.session_stats['smooth_moments'] += 1
    
    def generate_fake_analysis(self):
        """Generate hilariously fake psychological analysis"""
        session_time = time.time() - self.session_stats['start_time']
        
        analysis = [
            f"📊 COMPREHENSIVE AWKWARDNESS ANALYSIS 📊",
            f"Session Duration: {session_time/60:.1f} minutes",
            f"Peak Cringe Level: {self.session_stats['peak_awkwardness']:.1f}/100",
            f"Fidget Count: {self.session_stats['total_fidgets']} (excessive)",
            f"Eye Contact Breaks: {self.session_stats['eye_contact_breaks']} (concerning)",
            f"Awkward/Smooth Ratio: {self.session_stats['awkward_moments']}/{self.session_stats['smooth_moments']}",
            "",
            "🔬 PROFESSIONAL RECOMMENDATIONS:",
            "• Consider professional small talk training",
            "• Practice conversations with houseplants",
            "• Watch more rom-coms for inspiration",
            "• Emergency topic: Ask about their favorite pizza toppings",
            "",
            "📈 PERSONALITY ASSESSMENT:",
            f"Social Confidence: {random.randint(1, 4)}/10 (needs improvement)",
            f"Awkwardness Tolerance: {random.randint(2, 6)}/10",
            f"Fidget Factor: {random.randint(6, 10)}/10 (concerning)",
            f"Eye Contact Skills: {random.randint(1, 5)}/10 (avoid mirrors)"
        ]
        
        return analysis
    
    def draw_meme_overlay(self, frame):
        """Draw meme text overlay"""
        if not self.meme_mode:
            return
        
        # Change meme every 5 seconds
        if time.time() - self.meme_timer > 5:
            self.current_meme = random.choice(self.memes)
            self.meme_timer = time.time()
        
        # Draw meme text with background
        h, w, _ = frame.shape
        text_size = cv2.getTextSize(self.current_meme, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        
        # Background rectangle
        cv2.rectangle(frame, (10, h - 80), (text_size[0] + 20, h - 20), (0, 0, 0), -1)
        
        # Meme text
        cv2.putText(frame, self.current_meme, (15, h - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    
    def draw_fake_science(self, frame):
        """Display rotating fake scientific explanations"""
        science_text = self.scientific_nonsense[self.current_science_index % len(self.scientific_nonsense)]
        
        cv2.putText(frame, science_text, (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Change every 3 seconds
        if random.random() < 0.01:  # Small chance each frame
            self.current_science_index += 1
    
    def process_frame_with_comedy(self, frame):
        """Main processing with all comedy features"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detection
        face_results = self.face_detector.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        
        frame_awkwardness = 0
        face_detected = bool(face_results.detections)
        hands_detected = bool(hand_results.multi_hand_landmarks)
        
        # Calculate awkwardness
        if not face_detected:
            frame_awkwardness += 3
        if hands_detected:
            frame_awkwardness += 2
        
        # Update score and stats
        self.awkwardness_score += frame_awkwardness * 0.3
        self.awkwardness_score = max(0, self.awkwardness_score - 0.1)
        self.update_statistics(frame_awkwardness, face_detected, hands_detected)
        
        # Draw detections
        if face_results.detections:
            for detection in face_results.detections:
                self.mp_draw.draw_detection(frame, detection)
        
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        # Draw comedy features
        self.draw_meme_overlay(frame)
        self.draw_fake_science(frame)
        
        # Main display
        cv2.putText(frame, f"Awkwardness: {self.awkwardness_score:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Meme mode indicator
        if self.meme_mode:
            cv2.putText(frame, "🎭 MEME MODE", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        
        return frame
    
    def save_session_report(self):
        """Save a funny session report"""
        analysis = self.generate_fake_analysis()
        
        with open(f"awkwardness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 'w') as f:
            f.write("\n".join(analysis))
        
        print("📝 Session report saved!")
        for line in analysis:
            print(line)

# Main execution with keyboard controls
comedy_system = ComedyFeaturesSystem()
camera = cv2.VideoCapture(0)

print("🎭 Comedy Features System Online!")
print("Controls:")
print("- Press 'm' to toggle Meme Mode")
print("- Press 'r' to generate analysis report")
print("- Press 'q' to quit")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    frame = comedy_system.process_frame_with_comedy(frame)
    
    cv2.imshow("Comedy-Enhanced Awkwardness Detector", frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('m'):
        comedy_system.toggle_meme_mode()
    elif key == ord('r'):
        comedy_system.save_session_report()

camera.release()
cv2.destroyAllWindows()