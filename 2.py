import tkinter as tk
import random

task_recommendations = {
    "happy": ["Brainstorm new ideas", "Lead a team meeting", "Start a creative project"],
    "neutral": ["Review documents", "Respond to emails", "Update reports"],
    "sad": ["Simple data entry", "Organize files", "Listen to relaxing music"],
    "stressed": ["Take a short break", "Do breathing exercises", "Work on low-priority tasks"],
    "angry": ["Go for a walk", "Work independently", "Write down thoughts"],
    "anxious": ["Follow a structured checklist", "Work on familiar tasks", "Talk to a mentor"]
}

def recommend_task():
    mood = mood_entry.get().lower()
    if mood in task_recommendations:
        task = random.choice(task_recommendations[mood])
    else:
        task = "No recommendation available. Try relaxation techniques."
    result_label.config(text=f"Recommended Task: {task}")

# Create GUI window
root = tk.Tk()
root.title("Task Recommendation System")

tk.Label(root, text="Enter your mood:").pack()
mood_entry = tk.Entry(root)
mood_entry.pack()

tk.Button(root, text="Get Task", command=recommend_task).pack()
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
