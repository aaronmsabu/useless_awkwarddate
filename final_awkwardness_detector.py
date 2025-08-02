# save as: final_awkwardness_detector.py
import cv2
import mediapipe as mp
import time
import random
import json
from datetime import datetime
import argparse

class UltimateAwkwardnessDetector:
    def __init__(self, enable_memes=True, enable_audio=True):
        print("🚀 Initializing Ultimate Awkwardness Detector...")
        
        # Core detection setup
        self.mp_face = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.5,
            max_num_hands=2
        )
        
        # Core metrics
        self.awkwardness_score = 0
        self.session_start = time.time()
        
        # Feature toggles
        self.meme_mode = enable_memes
        self.audio_enabled = enable_audio
        
        # All our comedy features combined
        self.setup_comedy_features()
        self.setup_statistics()
        self.setup_alerts()
        
        print("✅ System ready! Prepare for awkwardness detection!")
    
    def setup_comedy_features(self):
        """Initialize all comedy features"""
        self.memes = [
            "This is fine. 🔥🐕🔥",
            "Awkwardness level: It's over 9000! 💥",
            "Error 404: Social skills not found 🤖",
            "Current mood: Existential crisis 💀",
            "Me trying to be social: 🤡"
        ]
        
        self.current_meme = random.choice(self.memes)
        self.meme_timer = time.time()
        
        self.floating_emojis = []
        self.emoji_list = ["😰", "😅", "🤦", "💀", "🚨", "⚠️", "😳"]
    
    def setup_statistics(self):
        """Initialize statistics tracking"""
        self.stats = {
            'total_frames': 0,
            'awkward_frames': 0,
            'face_touches': 0,
            'eye_contact_breaks': 0,
            'peak_awkwardness': 0,
            'smooth_moments': 0
        }
    
    def setup_alerts(self):
        """Initialize alert system"""
        self.alert_active = False
        self.last_alert_time = 0
        self.alert_colors = [(0, 0, 255), (255, 0, 0), (0, 255, 255)]
        self.alert_color_index = 0
    
    def process_frame(self, frame):
        """Main processing pipeline"""
        self.stats['total_frames'] += 1
        
        # Convert for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces and hands
        face_results = self.face_detector.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        
        # Calculate awkwardness for this frame
        frame_awkwardness = self.calculate_awkwardness(face_results, hand_results)
        
        # Update overall score
        self.update_awkwardness_score(frame_awkwardness)
        
        # Update statistics
        self.update_statistics(frame_awkwardness, face_results, hand_results)
        
        # Draw all visual elements
        frame = self.draw_detections(frame, face_results, hand_results)
        frame = self.draw_ui_elements(frame)
        
        if self.meme_mode:
            frame = self.draw_comedy_elements(frame)
        
        return frame
    
    def calculate_awkwardness(self, face_results, hand_results):
        """Calculate awkwardness score for current frame"""
        awkwardness = 0
        
        # No face detected (looking away?)
        if not face_results.detections:
            awkwardness += 3
            self.stats['eye_contact_breaks'] += 1
        
        # Hands visible (potential fidgeting)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Check if hand is near face area
                index_tip = hand_landmarks.landmark[8]  # Index finger tip
                if index_tip.y < 0.4:  # Upper part of image
                    awkwardness += 4
                    self.stats['face_touches'] += 1
                else:
                    awkwardness += 1  # General fidgeting
        
        return awkwardness
    
    def update_awkwardness_score(self, frame_awkwardness):
        """Update the overall awkwardness score"""
        # Add current frame's awkwardness
        self.awkwardness_score += frame_awkwardness * 0.5
        
        # Natural decay over time
        self.awkwardness_score = max(0, self.awkwardness_score - 0.2)
        
        # Update peak
        self.stats['peak_awkwardness'] = max(
            self.stats['peak_awkwardness'], 
            self.awkwardness_score
        )
        
        # Count frame types
        if frame_awkwardness > 2:
            self.stats['awkward_frames'] += 1
        elif frame_awkwardness == 0:
            self.stats['smooth_moments'] += 1
    
    def update_statistics(self, frame_awkwardness, face_results, hand_results):
        """Update session statistics"""
        # Statistics are updated in other methods
        pass
    
    def draw_detections(self, frame, face_results, hand_results):
        """Draw face and hand detection results"""
        # Draw face detections
        if face_results.detections:
            for detection in face_results.detections:
                self.mp_draw.draw_detection(frame, detection)
        
        # Draw hand landmarks
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        return frame
    
    def draw_ui_elements(self, frame):
        """Draw main UI elements"""
        h, w, _ = frame.shape
        
        # Main awkwardness display
        cv2.putText(frame, f"Awkwardness Score: {self.awkwardness_score:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Status based on score
        if self.awkwardness_score < 5:
            status = "😊 Smooth & Confident"
            color = (0, 255, 0)
        elif self.awkwardness_score < 15:
            status = "😐 Slightly Nervous"
            color = (0, 255, 255)
        elif self.awkwardness_score < 30:
            status = "😅 Getting Uncomfortable"
            color = (0, 165, 255)
        elif self.awkwardness_score < 50:
            status = "😰 Major Awkwardness"
            color = (0, 100, 255)
        else:
            status = "🚨 SOCIAL CATASTROPHE!"
            color = (0, 0, 255)
        
        cv2.putText(frame, status, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Awkwardness meter
        meter_x, meter_y = w - 200, 50
        meter_w, meter_h = 150, 20
        
        # Meter background
        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + meter_w, meter_y + meter_h), 
                     (100, 100, 100), -1)
        
        # Meter fill
        fill_width = int(min(self.awkwardness_score / 100, 1.0) * meter_w)
        cv2.rectangle(frame, (meter_x, meter_y), (meter_x + fill_width, meter_y + meter_h), 
                     color, -1)
        
        cv2.putText(frame, "CRINGE LEVEL", (meter_x, meter_y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Alert border for high awkwardness
        if self.awkwardness_score > 40:
            border_color = self.alert_colors[self.alert_color_index % len(self.alert_colors)]
            cv2.rectangle(frame, (0, 0), (w-1, h-1), border_color, 5)
            
            if time.time() - self.last_alert_time > 0.5:
                self.alert_color_index += 1
                self.last_alert_time = time.time()
        
        return frame
    
    def draw_comedy_elements(self, frame):
        """Draw memes and floating emojis"""
        h, w, _ = frame.shape
        
        # Update meme every 5 seconds
        if time.time() - self.meme_timer > 5:
            self.current_meme = random.choice(self.memes)
            self.meme_timer = time.time()
        
        # Draw meme with background
        text_size = cv2.getTextSize(self.current_meme, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(frame, (10, h - 60), (text_size[0] + 20, h - 20), (0, 0, 0), -1)
        cv2.putText(frame, self.current_meme, (15, h - 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Add floating emojis occasionally
        if random.random() < 0.01:  # 1% chance per frame
            emoji_data = {
                'emoji': random.choice(self.emoji_list),
                'x': random.randint(100, w-100),
                'y': h - 100,
                'speed_y': random.randint(-3, -1),
                'life': 60
            }
            self.floating_emojis.append(emoji_data)
        
        # Update and draw floating emojis
        for emoji in self.floating_emojis[:]:
            emoji['y'] += emoji['speed_y']
            emoji['life'] -= 1
            
            cv2.putText(frame, emoji['emoji'], (int(emoji['x']), int(emoji['y'])), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            
            if emoji['life'] <= 0 or emoji['y'] < 0:
                self.floating_emojis.remove(emoji)
        
        return frame
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        session_time = time.time() - self.session_start
        
        report = [
            "🎭 ULTIMATE AWKWARDNESS ANALYSIS REPORT 🎭",
            "=" * 50,
            f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"⏱️ Session Duration: {session_time/60:.1f} minutes",
            f"🎯 Frames Analyzed: {self.stats['total_frames']}",
            "",
            "📊 AWKWARDNESS METRICS:",
            f"• Peak Cringe Level: {self.stats['peak_awkwardness']:.1f}/100",
            f"• Final Score: {self.awkwardness_score:.1f}/100",
            f"• Awkward Frames: {self.stats['awkward_frames']} ({100*self.stats['awkward_frames']/max(1,self.stats['total_frames']):.1f}%)",
            f"• Smooth Moments: {self.stats['smooth_moments']}",
            f"• Face Touches: {self.stats['face_touches']} (concerning)",
            f"• Eye Contact Breaks: {self.stats['eye_contact_breaks']}",
            "",
            "🔬 BEHAVIORAL ANALYSIS:",
            f"• Fidget Factor: {random.randint(6, 10)}/10 (high)",
            f"• Social Confidence: {max(1, 10 - int(self.stats['peak_awkwardness']/10))}/10",
            f"• Awkwardness Resilience: {random.randint(3, 7)}/10",
            "",
            "💡 RECOMMENDATIONS:",
            "• Practice conversations with houseplants first",
            "• Emergency topic: Ask about their favorite pizza toppings",
            "• Consider professional small talk training",
            "• Watch more rom-coms for inspiration",
            "• Remember: Everyone is awkward sometimes!",
            "",
            "🎪 ENTERTAINMENT VALUE: 10/10 ⭐",
            "Successfully turned social anxiety into comedy!"
        ]
        
        # Save report
        filename = f"awkwardness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write('\n'.join(report))
        
        print(f"\n📝 Report saved as: {filename}")
        return report
    
    def run(self):
        """Main execution loop"""
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("❌ Could not open camera!")
            return
        
        print("\n🎬 ULTIMATE AWKWARDNESS DETECTOR ONLINE!")
        print("Controls:")
        print("- Press 'm' to toggle meme mode")
        print("- Press 'r' to generate report") 
        print("- Press 'q' to quit")
        print("\nStart acting awkward and watch the magic happen! 🪄")
        
        while True:
            ret, frame = camera.read()
            if not ret:
                print("❌ Failed to read from camera")
                break
            
            # Process frame
            frame = self.process_frame(frame)
            
            # Display
            cv2.imshow("Ultimate Awkwardness Detector", frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                self.meme_mode = not self.meme_mode
                print(f"🎭 Meme mode: {'ON' if self.meme_mode else 'OFF'}")
            elif key == ord('r'):
                report = self.generate_final_report()
                for line in report:
                    print(line)
        
        camera.release()
        cv2.destroyAllWindows()
        
        # Final report
        print("\n🎉 Session Complete!")
        final_report = self.generate_final_report()

if __name__ == "__main__":
    # Command line options
    parser = argparse.ArgumentParser(description="Ultimate Awkwardness Detector")
    parser.add_argument("--no-memes", action="store_true", help="Disable meme mode")
    parser.add_argument("--no-audio", action="store_true", help="Disable audio alerts")
    
    args = parser.parse_args()
    
    # Create and run detector
    detector = UltimateAwkwardnessDetector(
        enable_memes=not args.no_memes,
        enable_audio=not args.no_audio
    )
    
    detector.run()