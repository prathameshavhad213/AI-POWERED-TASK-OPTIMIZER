import cv2
import random
from deepface import DeepFace
import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd
from datetime import datetime

# Load OpenCV Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Task recommendations based on emotions
task_recommendations = {
    "happy": ["Brainstorm new ideas", "Lead a team meeting", "Start a creative project"],
    "neutral": ["Review documents", "Respond to emails", "Update reports"],
    "sad": ["Simple data entry", "Organize files", "Listen to relaxing music"],
    "angry": ["Go for a walk", "Work independently", "Write down thoughts"],
    "fear": ["Follow a structured checklist", "Work on familiar tasks", "Talk to a mentor"],
    "surprise": ["Try learning something new", "Take a short break", "Read an interesting article"],
}

# Initialize CSV file
csv_file = "employee_mood_data.csv"
df = pd.DataFrame(columns=["Timestamp", "Emotion", "Task"])
df.to_csv(csv_file, index=False, mode='w', header=True)

# Tkinter GUI
root = tk.Tk()
root.title("Emotion Detection & Task Recommendation")

# Video Frame
video_label = tk.Label(root)
video_label.pack()

# Text Output
emotion_label = tk.Label(root, text="Emotion: Detecting...", font=("Arial", 14))
emotion_label.pack()
task_label = tk.Label(root, text="Task: Waiting for detection...", font=("Arial", 14))
task_label.pack()

cap = cv2.VideoCapture(0)
previous_emotion = None
frame_count = 0  # To process every 10th frame

def detect_emotion():
    global previous_emotion, frame_count
    ret, frame = cap.read()
    if not ret:
        return

    frame_count += 1

    # Convert to grayscale and detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    if len(faces) > 0 and frame_count % 10 == 0:  # Analyze every 10th frame only when a face is detected
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']
            
            if dominant_emotion != previous_emotion:
                previous_emotion = dominant_emotion
                recommended_task = random.choice(task_recommendations.get(dominant_emotion, ["No recommendation available"]))

                # Update GUI Labels
                emotion_label.config(text=f"Emotion: {dominant_emotion}")
                task_label.config(text=f"Task: {recommended_task}")

                # Save to CSV
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_data = pd.DataFrame([[timestamp, dominant_emotion, recommended_task]], columns=df.columns)
                new_data.to_csv(csv_file, index=False, mode='a', header=False)

            # Draw bounding box around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        except Exception as e:
            print(f"Error detecting emotion: {e}")
    
    # Convert frame to Image for Tkinter
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=img)
    video_label.img = img
    video_label.config(image=img)

    root.after(10, detect_emotion)

# Start detection
detect_emotion()

# Run Tkinter Loop
root.mainloop()
cap.release()
cv2.destroyAllWindows()
