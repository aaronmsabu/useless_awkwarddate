# save as: testing_scenarios.py
import cv2
import time

class AwkwardnessTrainingAcademy:
    def __init__(self):
        # Use your completed detection system from previous parts
        from comedy_features import ComedyFeaturesSystem
        self.detector = ComedyFeaturesSystem()
        
        # Training scenarios
        self.scenarios = [
            {
                'name': "The Forced Smile Test",
                'instructions': "Smile awkwardly for 10 seconds. Make it look forced!",
                'duration': 10,
                'expected_behavior': "Should detect fake facial expressions"
            },
            {
                'name': "The Face Touch Challenge",
                'instructions': "Touch your face nervously 5 times in 15 seconds",
                'duration': 15,
                'expected_behavior': "Should trigger fidget detection"
            },
            {
                'name': "The Eye Contact Avoidance",
                'instructions': "Look away from the camera for 5 seconds, then back",
                'duration': 10,
                'expected_behavior': "Should detect loss of eye contact"
            },
            {
                'name': "The Nervous Fidget",
                'instructions': "Play with your hair and touch your neck repeatedly",
                'duration': 12,
                'expected_behavior': "Should increase awkwardness score rapidly"
            },
            {
                'name': "The Silent Treatment",
                'instructions': "Just sit still and stare blankly at the camera",
                'duration': 8,
                'expected_behavior': "Should detect uncomfortable silence"
            },
            {
                'name': "The Overcompensation",
                'instructions': "Nod enthusiastically and gesture wildly with your hands",
                'duration': 10,
                'expected_behavior': "Should detect excessive hand movement"
            }
        ]
        
        self.current_scenario = 0
        self.scenario_active = False
        self.scenario_start_time = 0
        
    def start_scenario(self, scenario_index):
        """Start a specific training scenario"""
        if scenario_index < len(self.scenarios):
            self.current_scenario = scenario_index
            self.scenario_active = True
            self.scenario_start_time = time.time()
            scenario = self.scenarios[scenario_index]
            
            print(f"\n🎬 SCENARIO {scenario_index + 1}: {scenario['name']}")
            print(f"📋 Instructions: {scenario['instructions']}")
            print(f"⏱️ Duration: {scenario['duration']} seconds")
            print(f"🎯 Expected: {scenario['expected_behavior']}")
            print("Starting in 3... 2... 1... GO!")
            return True
        return False
    
    def update_scenario(self, frame):
        """Update current scenario status"""
        if not self.scenario_active:
            return frame
        
        scenario = self.scenarios[self.current_scenario]
        elapsed = time.time() - self.scenario_start_time
        remaining = max(0, scenario['duration'] - elapsed)
        
        # Draw scenario info on frame
        cv2.putText(frame, f"SCENARIO: {scenario['name']}", 
                   (10, frame.shape[0] - 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Time Remaining: {remaining:.1f}s", 
                   (10, frame.shape[0] - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, scenario['instructions'], 
                   (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        # Check if scenario is complete
        if remaining <= 0:
            self.scenario_active = False
            print(f"\n✅ Scenario complete! Final awkwardness score: {self.detector.awkwardness_score:.1f}")
            print("Press 'n' for next scenario or any other key to continue free play")
        
        return frame
    
    def run_training_session(self):
        """Run the complete training session"""
        camera = cv2.VideoCapture(0)
        
        print("🎓 WELCOME TO THE AWKWARDNESS TRAINING ACADEMY! 🎓")
        print("We'll help you practice being awkward so you can recognize it!")
        print("\nControls:")
        print("- Press '1-6' to start specific scenarios")
        print("- Press 'n' for next scenario")
        print("- Press 'm' to toggle meme mode")
        print("- Press 'q' to quit")
        print("\nPress any number key (1-6) to start your first scenario!")
        
        while True:
            ret, frame = camera.read()
            if not ret:
                break
            
            # Process frame with detection
            frame = self.detector.process_frame_with_comedy(frame)
            
            # Update scenario overlay
            frame = self.update_scenario(frame)
            
            # Show available scenarios when not active
            if not self.scenario_active:
                cv2.putText(frame, "Press 1-6 to start scenarios, 'n' for next", 
                           (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.imshow("Awkwardness Training Academy", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('m'):
                self.detector.toggle_meme_mode()
            elif key == ord('n'):
                next_scenario = (self.current_scenario + 1) % len(self.scenarios)
                self.start_scenario(next_scenario)
            elif ord('1') <= key <= ord('6'):
                scenario_num = key - ord('1')
                self.start_scenario(scenario_num)
        
        camera.release()
        cv2.destroyAllWindows()
        
        # Final report
        print("\n🏆 TRAINING SESSION COMPLETE!")
        self.detector.save_session_report()

# Additional testing utilities
def create_test_videos():
    """Record test videos for different scenarios"""
    print("📹 Test Video Creator")
    print("This would help you create videos to test your detector")
    print("Ideas for test videos:")
    print("- Record yourself doing awkward things")
    print("- Find awkward interview clips on YouTube")
    print("- Stage fake awkward conversations with friends")
    print("- Test with different lighting conditions")

def benchmark_performance():
    """Test detection accuracy and performance"""
    print("⚡ Performance Benchmarking")
    print("Testing detection speed and accuracy...")
    
    # Simple performance test
    import time
    start_time = time.time()
    frame_count = 0
    
    camera = cv2.VideoCapture(0)
    
    while frame_count < 100:  # Test 100 frames
        ret, frame = camera.read()
        if ret:
            frame_count += 1
    
    camera.release()
    
    elapsed = time.time() - start_time
    fps = frame_count / elapsed
    
    print(f"📊 Performance Results:")
    print(f"Processed {frame_count} frames in {elapsed:.2f} seconds")
    print(f"Average FPS: {fps:.1f}")
    print(f"Frame processing time: {1000/fps:.1f}ms per frame")

if __name__ == "__main__":
    academy = AwkwardnessTrainingAcademy()
    academy.run_training_session()