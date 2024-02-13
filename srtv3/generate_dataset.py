import random
from faker import Faker
from datetime import datetime, timedelta
import pandas as pd

fake = Faker()

def generate_random_student():
    grade = random.randint(0, 12)
    age = random.randint(6 + grade, 18)
    grad_class = datetime.now().year + (12 - grade)
    
    student_id = random.randint(100000, 999999)
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random.choice(['M', 'F'])
    start_date = fake.date_between(start_date='-5y', end_date='today')
    
    # Correlate GPA with gender
    if gender == 'M':
        gpa_mean = 2.9
        gpa_stddev = 0.5
    else:
        gpa_mean = 3.1
        gpa_stddev = 0.4
    gpa = round(max(2.0, min(random.gauss(gpa_mean, gpa_stddev), 4.0)), 2)
    
    # Correlate entry score with GPA
    entry_score = round(max(0.0, min(random.gauss(gpa / 4.0, 0.2), 1.0)), 2)
    
    # Correlate entry test with grade level
    entry_test = max(1, min(12, grade - 1))
    
    location = random.choice(['La Jolla', 'S4 Ranch', 'Carslbad'])

    student = {
        'Id': student_id,
        'First': first_name,
        'Last': last_name,
        'Age': age,
        'Grade': grade,
        'Gender': gender,
        'Start Date': start_date.strftime('%m/%d/%y'),
        'GPA': gpa,
        'Entry Test': entry_test,
        'Entry Score': entry_score,
        'Location': location,
        'Grad Class': grad_class
    }
    
    return student

# Generate 100 random students
students = [generate_random_student() for _ in range(100)]

# Create a DataFrame
df = pd.DataFrame(students)

# Display the DataFrame
print(df)
