import cv2
import random
import smtplib
import pandas as pd
import os
from deepface import DeepFace
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet

# Load OpenCV Face Detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Define stress-related emotions
stress_emotions = ["sad", "fear", "angry"]

# Email Configuration (Replace with your details)
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
EMAIL_RECEIVER = "hr-manager@example.com"

# Generate or load encryption key
key_file = "encryption.key"
if not os.path.exists(key_file):
    key = Fernet.generate_key()
    with open(key_file, "wb") as key_out:
        key_out.write(key)
else:
    with open(key_file, "rb") as key_in:
        key = key_in.read()

cipher = Fernet(key)

# Function to encrypt data
def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

# Function to send email alerts
def send_alert_email(dominant_emotion):
    try:
        subject = "⚠ Stress Alert: Employee Needs Attention"
        body = f"An employee has been detected with high stress levels ({dominant_emotion}). Please check on their well-being."
        
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        
        print("📩 Alert email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Initialize webcam
cap = cv2.VideoCapture(0)
stress_count = 0  # To track consecutive stress detections
stress_threshold = 3  # Number of times stress must be detected before alert
csv_file = "employee_mood_data.csv"

def log_encrypted_data(timestamp, emotion, task):
    encrypted_data = f"{encrypt_data(timestamp)},{encrypt_data(emotion)},{encrypt_data(task)}\n"
    with open(csv_file, "a") as file:
        file.write(encrypted_data)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    try:
        if len(faces) > 0:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']
            print(f"Detected Emotion: {dominant_emotion}")

            # If stress-related emotion detected, increase count
            if dominant_emotion in stress_emotions:
                stress_count += 1
            else:
                stress_count = 0  # Reset if non-stress emotion detected

            # Trigger alert if stress detected multiple times in a row
            if stress_count >= stress_threshold:
                print("🚨 Stress Alert Triggered!")
                send_alert_email(dominant_emotion)
                stress_count = 0  # Reset after alert

            # Log encrypted data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            recommended_task = "Confidential Task Assigned"
            log_encrypted_data(timestamp, dominant_emotion, recommended_task)

    except Exception as e:
        print(f"Error detecting emotion: {e}")

    cv2.imshow("Stress Monitoring System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
