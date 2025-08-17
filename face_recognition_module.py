import cv2

def face_authenticate(voter_name):
    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False

    print("Press 's' to capture and authenticate, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        cv2.imshow("Face Authentication - Press 's' to Capture", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):  # 's' key to simulate capture
            # Optional: Save captured image (uncomment if you want to store)
            # cv2.imwrite(f"{voter_name}_auth.jpg", frame)
            print(f"Face captured for {voter_name}!")
            cap.release()
            cv2.destroyAllWindows()
            return True  # Simulate successful authentication
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False  # Return false if exited without capture

# Uncomment below lines to test module independently
# if _name_ == "_main_":
#     result = face_authenticate("test_user")
#     print("Authentication Result:", result)