import csv
import random
import tkinter as tk
from tkinter import filedialog

# Sample student names
names = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ian", "Jack",
    "Katherine", "Leo", "Mia", "Nathan", "Olivia", "Peter", "Quinn", "Rachel", "Sam", "Tina",
    "Umar", "Violet", "Will", "Xander", "Yasmine", "Zane", "Liam", "Sophia", "Noah", "Emma",
    "Mason", "Ava", "James", "Isabella", "Benjamin", "Mia", "Elijah", "Charlotte", "Lucas", "Amelia",
    "Henry", "Harper", "Alexander", "Evelyn", "Sebastian", "Abigail", "Daniel", "Ella", "Matthew", "Scarlett"
]

# Subjects offered
subjects = ["Math", "Science", "History", "English", "Biology", "Physics", "Chemistry", "Art", "Music", "PE"]

# Function to generate random students
def generate_students():
    students = []
    for _ in range(50):
        name = random.choice(names)
        age = random.randint(14, 18)  # High school student ages
        subject = random.choice(subjects)
        grade = random.randint(50, 100)  # Grades out of 100
        hours_per_week = random.randint(1, 20)  # Study hours per week
        students.append([name, age, subject, grade, hours_per_week])
    return students

# Function to save CSV with file dialog
def save_csv_with_dialog():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save Students CSV",
        initialfile="students.csv"
    )

    if file_path:
        students = generate_students()
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "age", "subject", "grade", "hours_per_week"])
            writer.writerows(students)
        print(f"CSV file saved successfully at: {file_path}")
    else:
        print("File save canceled by user.")

# Run the save function
if __name__ == "__main__":
    save_csv_with_dialog()
