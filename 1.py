import random

# Step 1: Define task categories based on mood
task_recommendations = {
    "happy": ["Brainstorm new ideas", "Lead a team meeting", "Start a creative project"],
    "neutral": ["Review documents", "Respond to emails", "Update reports"],
    "sad": ["Simple data entry", "Organize files", "Listen to relaxing music"],
    "stressed": ["Take a short break", "Do breathing exercises", "Work on low-priority tasks"],
    "angry": ["Go for a walk", "Work independently", "Write down thoughts"],
    "anxious": ["Follow a structured checklist", "Work on familiar tasks", "Talk to a mentor"]
}

# Step 2: Function to recommend a task based on mood
def recommend_task(mood):
    mood = mood.lower()  # Convert input to lowercase
    if mood in task_recommendations:
        return random.choice(task_recommendations[mood])
    else:
        return "No recommendation available. Try relaxation techniques."

# Step 3: Take user input and suggest a task
user_mood = input("Enter your current mood: ")  # Get mood from user
suggested_task = recommend_task(user_mood)
print(f"Recommended Task: {suggested_task}")
