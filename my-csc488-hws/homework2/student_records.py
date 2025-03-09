

import os

def add_student_record():
    """Add a new student record to grades.txt."""
    student_name = input("Enter student name: ")
    student_id = input("Enter student ID: ")
    course = input("Enter course name: ")
    grade = input("Enter grade: ")
    
    with open("grades.txt", "a") as file:
        file.write(f"{student_name}, {student_id}, {course}, {grade}\n")
    
    print("Student record added successfully!\n")

def display_records():
    """Display all student records from grades.txt."""
    if not os.path.exists("grades.txt"):
        print("No records found.\n")
        return
    
    with open("grades.txt", "r") as file:
        records = file.readlines()
        if not records:
            print("No records found.\n")
        else:
            print("Student Records:")
            for record in records:
                print(record.strip())
            print()

def search_student_by_id():
    """Search for a student record by ID."""
    student_id = input("Enter student ID to search: ")
    if not os.path.exists("grades.txt"):
        print("No records found.\n")
        return
    
    with open("grades.txt", "r") as file:
        records = file.readlines()
        found = False
        for record in records:
            if student_id in record:
                print("Student Record Found:")
                print(record.strip())
                found = True
                break
        
        if not found:
            print("No record found for the given Student ID.\n")

def main():
    while True:
        print("1. Add Student Record")
        print("2. Display Records")
        print("3. Search Student by ID")
        print("4. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_student_record()
        elif choice == "2":
            display_records()
        elif choice == "3":
            search_student_by_id()
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()

