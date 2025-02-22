import cv2
from deepface import DeepFace
import random

# Task categories based on detected emotions
task_recommendations = {
    "happy": ["Brainstorm new ideas", "Lead a team meeting", "Start a creative project"],
    "neutral": ["Review documents", "Respond to emails", "Update reports"],
    "sad": ["Simple data entry", "Organize files", "Listen to relaxing music"],
    "angry": ["Go for a walk", "Work independently", "Write down thoughts"],
    "fear": ["Follow a structured checklist", "Work on familiar tasks", "Talk to a mentor"],
    "surprise": ["Try learning something new", "Take a short break", "Read an interesting article"],
}

# Initialize webcam
cap = cv2.VideoCapture(0)
previous_emotion = None  # Store previous detected emotion

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show webcam feed
    cv2.imshow("Real-Time Face Detection", frame)

    try:
        # Perform emotion analysis
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        dominant_emotion = analysis[0]['dominant_emotion']

        # Only print if emotion has changed
        if dominant_emotion != previous_emotion:
            previous_emotion = dominant_emotion  # Update previous emotion
            recommended_task = random.choice(task_recommendations.get(dominant_emotion, ["No recommendation available"]))
            print(f"Detected Emotion: {dominant_emotion} | Recommended Task: {recommended_task}")

    except Exception as e:
        print(f"Error detecting emotion: {e}")

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
