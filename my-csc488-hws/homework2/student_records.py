

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

def update_student_grade():
    """Update a student's grade by ID."""
    student_id = input("Enter student ID to update grade: ")
    new_grade = input("Enter new grade: ")
    if not os.path.exists("grades.txt"):
        print("No records found.\n")
        return
    
    updated_records = []
    found = False
    with open("grades.txt", "r") as file:
        records = file.readlines()
        for record in records:
            data = record.strip().split(", ")
            if data[1] == student_id:
                data[3] = new_grade
                found = True
            updated_records.append(", ".join(data) + "\n")
    
    with open("grades.txt", "w") as file:
        file.writelines(updated_records)
    
    if found:
        print("Grade updated successfully!\n")
    else:
        print("No record found for the given Student ID.\n")

def delete_student_record():
    """Delete a student's record by ID."""
    student_id = input("Enter student ID to delete record: ")
    if not os.path.exists("grades.txt"):
        print("No records found.\n")
        return
    
    updated_records = []
    found = False
    with open("grades.txt", "r") as file:
        records = file.readlines()
        for record in records:
            if student_id not in record:
                updated_records.append(record)
            else:
                found = True
    
    with open("grades.txt", "w") as file:
        file.writelines(updated_records)
    
    if found:
        print("Student record deleted successfully!\n")
    else:
        print("No record found for the given Student ID.\n")

def main():
    while True:
        print("1. Add Student Record")
        print("2. Display Records")
        print("3. Search Student by ID")
        print("4. Update Student Grade")
        print("5. Delete Student Record")
        print("6. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == "1":
            add_student_record()
        elif choice == "2":
            display_records()
        elif choice == "3":
            search_student_by_id()
        elif choice == "4":
            update_student_grade()
        elif choice == "5":
            delete_student_record()
        elif choice == "6":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":

    main()

