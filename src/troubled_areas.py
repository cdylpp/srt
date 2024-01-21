import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
data = pd.read_csv('src/student_data.csv')

# Specify the StudentID you want to analyze
student_id_to_analyze = 12345678 

# Select the data for the specified student
selected_student = data[data['Student_ID'] == student_id_to_analyze]

# Drop irrelevant columns for the analysis
selected_student = selected_student.drop(['Student_ID', 'FirstName', 'LastName', 'Retention_Score'], axis=1)

# Convert the "StudyHoursPerWeek" metric to a percentage by dividing by 15
selected_student['Study_Hours_Per_Week'] = (selected_student['Study_Hours_Per_Week'] / 15) * 100

# Normalize the data to show relative impact on retention score
normalized_data = selected_student.div(selected_student.sum(axis=1), axis=0) * 100

# Define word replacements (specify the words you want to change and their replacements)
word_replacements = {'Avg_Test_Score': 'Average Test Score', 'Study_Hours_Per_Week': 'Study Hours Per Week'}

# Apply word replacements to metric names
adjusted_metric_names = [word_replacements.get(metric, metric) for metric in normalized_data.columns]

# Plotting the bar graph without legend with adjusted x-axis labels
ax = normalized_data.transpose().plot(kind='bar', stacked=True)
ax.get_legend().remove()  # This line removes the legend

# Set adjusted x-axis labels
plt.xticks(range(len(adjusted_metric_names)), adjusted_metric_names, rotation=0)

plt.title(f'Impact of Metrics on Retention Score (Student ID: {student_id_to_analyze})')
plt.ylabel('Relative Impact (%)')
plt.tight_layout()  # Adjust layout to prevent text cutoff
plt.show()
