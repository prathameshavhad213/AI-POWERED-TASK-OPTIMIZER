import pandas as pd
import matplotlib.pyplot as plt

employee_data = {
    'Date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
    'Mood': [3, 4, 5, 2, 3, 4, 3, 4, 5, 2, 3, 5, 4, 4, 5, 3, 2, 4, 3, 5, 4, 4, 3, 2, 4, 5, 3, 3, 2, 4]
}

employee_df = pd.DataFrame(employee_data)

plt.figure(figsize=(12, 6))
plt.plot(employee_df['Date'], employee_df['Mood'], marker='o', linestyle='-', color='g')
plt.title('Historical Mood Tracking for Employee')
plt.xlabel('Date')
plt.ylabel('Mood Rating')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

employee_df['Rolling_Avg_Mood'] = employee_df['Mood'].rolling(window=7).mean()

# Plot rolling average mood trends to identify long-term patterns
plt.figure(figsize=(12, 6))
plt.plot(employee_df['Date'], employee_df['Rolling_Avg_Mood'], marker='o', linestyle='-', color='r')
plt.title('Rolling Average of Employee Mood (7-Day Window)')
plt.xlabel('Date')
plt.ylabel('Rolling Average Mood Rating')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()