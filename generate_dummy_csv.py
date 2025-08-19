import csv
import random

# Creates a CSV with 50 dummy students
with open('dummy_students.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['name', 'attendance', 'assignment_score', 'test_score', 'teacher_feedback'])

    for i in range(1, 51):
        name = f"Student {i}"
        attendance = random.randint(50, 100)
        assignment_score = random.randint(40, 100)
        test_score = random.randint(30, 100)
        feedback = "Good" if assignment_score > 70 else "Needs Improvement"

        writer.writerow([name, attendance, assignment_score, test_score, feedback])

print("CSV created successfully!")
