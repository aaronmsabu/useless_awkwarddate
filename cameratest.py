# save as: camera_test.py
import cv2

# Access your "awkwardness surveillance device" (aka webcam)
camera = cv2.VideoCapture(0)

print("🕵️ Awkwardness Detection Camera Test!")
print("Press 'q' to quit when you're done looking awkward")

while True:
    # Capture your potentially awkward face
    ret, frame = camera.read()
    
    if not ret:
        print("❌ Camera not found! Check if another app is using it")
        break
    
    # Add some fun text
    cv2.putText(frame, "AWKWARDNESS SURVEILLANCE ACTIVE", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow("Your Future Date Monitor", frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
print("📹 Camera test complete! Ready for awkwardness detection!")
