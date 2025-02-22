import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the stored emotions from CSV
csv_file = "employee_mood_data.csv"

def plot_team_mood_analytics():
    try:
        # Read CSV data
        df = pd.read_csv(csv_file)

        # Check if the dataset is empty
        if df.empty:
            print("⚠ No data available for analysis. Ensure employee_mood_data.csv has recorded emotions.")
            return

        # Convert 'Timestamp' to datetime format
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

        # Drop rows with missing or invalid timestamps
        df = df.dropna(subset=['Timestamp'])

        # Extract date for grouping
        df['Date'] = df['Timestamp'].dt.date

        # Count occurrences of each emotion per day
        mood_counts = df.groupby(['Date', 'Emotion']).size().reset_index(name='Count')

        # Check if there is valid data to plot
        if mood_counts.empty:
            print("⚠ No valid mood data available for visualization.")
            return

        # Plot team mood trends over time
        plt.figure(figsize=(12, 6))
        lineplot = sns.lineplot(x='Date', y='Count', hue='Emotion', data=mood_counts, marker='o')

        # Fix empty legend issue
        if len(lineplot.get_legend().texts) == 0:
            print("⚠ No moods found to plot. Ensure valid emotion data is recorded.")

        plt.title("Team Mood Trends Over Time")
        plt.xlabel("Date")
        plt.ylabel("Mood Frequency")
        plt.xticks(rotation=45)
        plt.legend(title="Emotions", loc='upper left')
        plt.grid()
        plt.show()

        # Create a pivot table for heatmap
        mood_pivot = df.pivot_table(index='Date', columns='Emotion', values='Timestamp', aggfunc='count')

        # Check if the pivot table has valid data
        if mood_pivot.empty:
            print("⚠ Not enough data for heatmap visualization.")
            return

        # Plot heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(mood_pivot, cmap="coolwarm", annot=True, fmt=".0f", linewidths=0.5)
        plt.title("Team Mood Distribution Heatmap")
        plt.xlabel("Emotion")
        plt.ylabel("Date")
        plt.show()

    except Exception as e:
        print(f"⚠ Error generating team mood analytics: {e}")

# Run the function to display team mood trends
plot_team_mood_analytics()
