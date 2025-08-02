# save as: audio_alerts.py
import cv2
import mediapipe as mp
import pygame
import time
import random
import requests
import threading

class AudioAlertSystem:
    def __init__(self):
        # Initialize pygame for sound
        pygame.mixer.init()
        
        # Previous detection setup
        self.mp_face = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
        
        self.awkwardness_score = 0
        self.last_sound_time = 0
        
        # Create some basic sound effects (using pygame's built-in tones)
        self.create_sound_effects()
        
        # Funny voice lines
        self.voice_lines = [
            "Awkward silence detected!",
            "Warning: Cringe levels rising!",
            "Social skills malfunction!",
            "Emergency! Call backup conversation topics!",
            "Abort mission! Abort mission!",
            "Awkwardness overload detected!",
            "Please remain calm during this social disaster.",
            "Have you tried talking about the weather?"
        ]
        
        self.current_voice_line = 0
    
    def create_sound_effects(self):
        """Create basic sound effects using pygame"""
        # Create different frequency sounds for different alerts
        self.sounds = {}
        
        # We'll use simple beep sounds since creating complex sounds is advanced
        # In a real project, you'd load .wav or .mp3 files
        
        # For now, we'll just use pygame's basic sound generation
        print("🔊 Sound system initialized!")
        print("Note: Using basic beep sounds. For better sounds, add .wav files!")
    
    def play_awkward_sound(self, awkwardness_level):
        """Play different sounds based on awkwardness level"""
        current_time = time.time()
        
        # Don't play sounds too frequently
        if current_time - self.last_sound_time < 2:
            return
        
        self.last_sound_time = current_time
        
        # Play different "sounds" based on level (just print for now)
        if awkwardness_level < 15:
            print("🔔 *ding* - Mild awkwardness detected")
        elif awkwardness_level < 30:
            print("📢 *buzzer* - Awkwardness increasing!")
        elif awkwardness_level < 50:
            print("🚨 *alarm* - HIGH CRINGE ALERT!")
        else:
            print("💥 *EXPLOSION* - SOCIAL MELTDOWN!")
        
        # In a real implementation, you'd play actual sound files:
        # pygame.mixer.Sound('awkward_sound.wav').play()
    
    def speak_voice_line(self):
        """Play a funny voice line (simulated)"""
        line = self.voice_lines[self.current_voice_line % len(self.voice_lines)]
        print(f"🗣️ Voice Alert: '{line}'")
        self.current_voice_line += 1
        
        # In a real implementation, you could use text-to-speech:
        # import pyttsx3
        # engine = pyttsx3.init()
        # engine.say(line)
        # engine.runAndWait()
    
    def process_frame_with_audio(self, frame):
        """Process frame and trigger audio alerts"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Face and hand detection (simplified)
        face_results = self.face_detector.process(rgb_frame)
        hand_results = self.hands.process(rgb_frame)
        
        frame_awkwardness = 0
        
        # Calculate awkwardness
        if not face_results.detections:
            frame_awkwardness += 3  # No face visible
        
        if hand_results.multi_hand_landmarks:
            frame_awkwardness += 2  # Hands visible (fidgeting)
        
        # Update score
        self.awkwardness_score += frame_awkwardness * 0.3
        self.awkwardness_score = max(0, self.awkwardness_score - 0.15)
        
        # Trigger audio alerts
        if self.awkwardness_score > 25:
            self.play_awkward_sound(self.awkwardness_score)
        
        # Trigger voice lines for extreme awkwardness
        if self.awkwardness_score > 50 and random.random() < 0.01:
            self.speak_voice_line()
        
        # Draw detection results
        if face_results.detections:
            for detection in face_results.detections:
                self.mp_draw.draw_detection(frame, detection)
        
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        # Display current status
        cv2.putText(frame, f"Awkwardness: {self.awkwardness_score:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Show audio status
        if self.awkwardness_score > 25:
            cv2.putText(frame, "🔊 AUDIO ALERT ACTIVE", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame

# Enhanced version with downloadable sounds
def download_sound_effect(url, filename):
    """Download a sound effect from the internet"""
    try:
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except:
        return False

# Main execution
audio_system = AudioAlertSystem()
camera = cv2.VideoCapture(0)

print("🎵 Audio Alert System Starting!")
print("Prepare for sound effects and voice alerts!")
print("(Note: This demo uses text alerts - add real sound files for audio)")

while True:
    ret, frame = camera.read()
    if not ret:
        break
    
    frame = audio_system.process_frame_with_audio(frame)
    
    cv2.imshow("Audio-Enhanced Awkwardness Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()