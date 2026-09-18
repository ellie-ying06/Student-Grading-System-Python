"""
A student grading system with 7 functions including exit
allow for adding student, adding courses, entering grades.
allow for displaying students performance, course performance
allow for extracting the performance report for a course or all courses
"""
import os
import re
folder = os.path.dirname(os.path.abspath(__file__))

line = "-------------------------------------------------------"
studentList = []
previousID = None
courseList= {}

#variable
max_stu_digit = "5"
gpa = 0.0

#checking ******
def is_valid_name(name: str) -> bool:
    pattern = r"^[A-Za-z\s]+$"
    return bool(re.fullmatch(pattern, name))

def is_valid_student_id(student_id: str) -> bool:
    pattern = r"^\d{" + max_stu_digit + "}$"     # exactly  max_stu_digits
    return bool(re.fullmatch(pattern, student_id)) 

def is_valid_email(student_id: str ,email: str) -> bool:
    pattern = rf"^{student_id}@imail\.sunway\.edu\.my$" #same ID from studentID
    return bool(re.fullmatch(pattern, email))

def is_valid_course_id(course_id: str) -> bool:
    pattern = r"^[A-Za-z]{3}\d{4}$"
    return bool(re.fullmatch(pattern, course_id))

def save_invalid_line(filename, line):
    with open(filename, "a") as f:
        f.write(f"{line}\n")
                
def overwrite_file(filename, lines):
    with open(filename, "w") as f:
        for line in lines:
            f.write(line +"\n")
    
def load_students():
    error_count = 0
    invalid_lines = []
    overwrite_file("invalid_students.txt", invalid_lines)
    
    try:
        with open("students.txt", "r") as file:
            for line in file:
                raw_line = line.strip()
                if not raw_line:
                    continue
                
                parts = raw_line.split(",")
                if len(parts) != 3:
                    save_invalid_line("invalid_students.txt", raw_line)
                    error_count += 1
                    continue  

                stuID, name, email = parts
                
                if not is_valid_student_id(stuID) or not is_valid_name(name) or not is_valid_email(stuID, email):
                    save_invalid_line("invalid_students.txt", raw_line)
                    error_count += 1
                    continue
                

                student = {
                    "Student ID": stuID,
                    "Name": name,
                    "Email Address": email,
                    "Course": [],
                    "Grades": {},
                    "GPA": 0.0
                }
                studentList.append(student)
                
              
        print(f"Total invalid line in students text file: {error_count}")

    except FileNotFoundError:
        print("File not found. Please make sure the file exists in the program directory before proceeding.")
        
def load_courses():
    global courseList
    invalid_lines = []
    overwrite_file("invalid_courses.txt", invalid_lines)
    error_count = 0
    
    try:
        with open("courses.txt", "r") as file:
            for line in file:

                raw_line = line.strip()
                
                if not raw_line:      #skip empty lines 
                    continue

                parts = raw_line.split(":")

                if len(parts) != 2:
                    save_invalid_line("invalid_courses.txt", raw_line)
                    error_count += 1
                    continue
                
                cid, cname = parts
                
                #validation ******
                if not is_valid_course_id(cid):
                    save_invalid_line("invalid_courses.txt", raw_line)
                    error_count += 1
                    continue

                courseList[cid] = cname  #If valid, save it
                
                
    except FileNotFoundError:
        print("File not found. Please make sure the file exists in the program directory before proceeding.")
    
    print(f"Total invalid line in courses text file: {error_count}")
    
def markGrade(str_mark):
    pattern = r"^(100|[1-9]?\d|0)$"  # check string only accepts 0–100
    if bool(re.fullmatch(pattern, str_mark)):
        mark = int(str_mark) #from string to number
        if mark > 100 or mark < 0:
            grade = None
        if 80 <= mark <= 100:
            grade = "A+"
        elif 75 <= mark < 80:
            grade = "A"
        elif 70 <= mark < 75:
            grade = "A-"
        elif 65 <= mark < 70:
            grade = "B+"
        elif 60 <= mark < 65:
            grade = "B"
        elif 55 <= mark < 60:
            grade = "B-"
        elif 40 <= mark < 55:
            grade = "C"
        else:
            grade = "F"
    else:
        grade = None
    return grade

def load_grades():
    error_count = 0
    invalid_lines = []
    overwrite_file("invalid_grades.txt", invalid_lines)
    
    try:
        with open("grades.txt", "r") as file:
            for line in file:
                raw_line = line.strip() 
                
                if not raw_line:      #skip empty lines 
                    continue

                parts = raw_line.split(",")

                if len(parts) != 4:
                    save_invalid_line("invalid_grades.txt", raw_line)
                    error_count += 1
                    continue
                
                stuID, courseID, mark_str, grade = parts

               # validations ******
                if not is_valid_student_id(stuID):
                    save_invalid_line("invalid_grades.txt", raw_line)
                    error_count += 1
                    continue

                if not is_valid_course_id(courseID):
                    save_invalid_line("invalid_grades.txt", raw_line)
                    error_count += 1
                    continue
                
                chk_grade = markGrade(mark_str)
                
                if chk_grade is None:
                    save_invalid_line("invalid_grades.txt", raw_line)
                    error_count += 1
                    continue
                
                mark = float(mark_str)
                
               #find student
                student = next((s for s in studentList if s["Student ID"] == stuID), None)
                
                if not student:
                    save_invalid_line("invalid_grades.txt", raw_line)
                    error_count += 1
                    continue

                #add course if not already in student["Course"]
                if courseID not in [list(c.keys())[0] for c in student["Course"]]:
                        student["Course"].append({courseID: courseList.get(courseID, "Unknown Course")})

                #add grade
                student["Grades"][courseID] = [mark, grade]

                #recalculate GPA
                total_points = sum(gpaGrade(g[1]) for g in student["Grades"].values())
                student["GPA"] = total_points / len(student["Grades"]) if student["Grades"] else 0.0

        print(f"Total invalid line in grades text file: {error_count}")
                                 
    except FileNotFoundError:
        print("File not found. Please make sure the file exists in the program directory before proceeding.")
    
def gpaGrade(grade):
    gpaPoint = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0,
                "B-": 2.7, "C+": 2.3, "C": 2.0, "D": 1.0, "F": 0.0}
    return gpaPoint.get(grade, 0.0)
    
load_students()
load_courses()
load_grades()

def register():
    global previousID
    print("Welcome for registering a student account!")

    # --- NAME VALIDATION ---
    while True:
        name = input("Enter your full name as per IC: ").title()

        if any(n["Name"] == name for n in studentList):  #check is name already exists
            print(f"Student name {name} has been used! Please use a different name.\n")
            continue
        
        if is_valid_name(name):
            break
        print("Invalid name! Letters and spaces only.\n")

    # --- STUDENT ID VALIDATION ---
    while True:
        stuID = input("Enter your student ID (" + max_stu_digit + " digits): ")

        if any(student["Student ID"] == stuID for student in studentList): #check is stuID already exists
            print(f"Student ID {stuID} is already registered! Please use a different ID.\n")
            continue
        
        if is_valid_student_id(stuID):
            break
        print("Invalid student ID! Must be exactly " + max_stu_digit + " digits.\n")
    previousID = stuID

    # --- EMAIL VALIDATION ---
    while True:
        email = input("Enter your student email address: ")
        if any(m["Email Address"] == email for m in studentList): #check is email already exists
            print(f"Sorry {email} has been used! Please use a different email address.\n")
            continue
        
        if is_valid_email(stuID, email):
            break
        
        print("Invalid email format! Please try again.")
        print("Please use imail (Example: 24123@imail.sunway.edu.my)\n")
        
    # --- STORE STUDENT INFO ---
    student = {
        "Name": name,
        "Student ID": stuID,
        "Email Address": email,
        "Course": [],
        "Grades": {},
        "GPA": 0.0
    }

    studentList.append(student)

    print(line)
    print("This is your student profile:")
    print("    --- Student Profile --- ")
    print(f"{"Name: "}{name:<8}")
    print(f"Student ID: ",stuID)
    print("Student account: ",email)
    print(line)
    print("Your student account has been registered successfully!")

    # Save to file
    with open("students.txt", "a") as file:
        file.write(f"{stuID},{name},{email}\n")

    # RETURN the new student ID 
    return previousID


def studentConfirm():
    global previousID
    print("Before we start, let's confirm your data.")
    if previousID is None:
        newID = input("Please enter your student ID: ")
        previousID = newID
    else:
        print("Are you the students with ID:",previousID, "?") #check is it the same student
        ans = input("Enter 'y' for yes, 'n' for no: ").lower()
        if ans == 'y':
            pass
        else:
            newID = input("Please enter your student ID: ")
            # access to that student profile
            previousID = newID

def findStuID(stuID):
    for student in studentList:
        if student["Student ID"] == stuID:
            return student
    return None

def courseAdd():
    print("Welcome for registering the new courses!")
    studentConfirm()
    student = findStuID(previousID)

    if student is None:
        print("Student not found, please try again.")
        return
    
    try:  #load existing courses
        with open("courses.txt","r") as file:
            for i in file:
                if ":" in i:
                    SyscouID, SyscouName = i.strip().split(":") #system course ID and system course name

                    #validation ******
                    if is_valid_course_id(SyscouID):
                        courseList[SyscouID] = SyscouName
                    else:
                        save_invalid_line("invalid_courses.txt", i.strip())
                        
    except FileNotFoundError:
        print("No Course Available")

    # provide the courses for student
    print("Available Courses:")
    for syscouID, syscouName in courseList.items(): #system course ID and system course name
        print(f"{syscouID}:{syscouName}")

    print("Provide the course ID that you want to add or press 0 to stop.")
    while True:
        courseID = input("Course ID: ").upper()
        if courseID == "0":
            break
        
        # validate courseID ******
        if not is_valid_course_id(courseID):
            print("Invalid Course ID format! Must be 3 letters + 4 digits (example: CSC1024).")
            continue

        #courseID exists
        elif courseID in courseList:
            newCourse = {courseID: courseList[courseID]}
            student["Course"].append(newCourse)
            print("--- ",end="")
            print(courseList[courseID],end=" ")
            print("has been added successfully! --- ")
            
        else:
            print("Course not found.")
            ans = input("Do you want to add this course? (y/n): ").lower()
            
            if ans == "y":
                courseName = input("Enter course name: ")
                
                # Save new course to txt file
                with open("courses.txt", "a") as file:
                    file.write(f"{courseID}:{courseName}\n")
                    
                # Update in-memory list
                courseList[courseID] = courseName
                
                # Add course to student
                student["Course"].append({courseID: courseName})
                print(f"--- {courseName} ({courseID}) has been added successfully! ---")


def gpaGrade(grade):
    gpaPoint = {"A+": 4.0,
        "A": 4.0,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3.0,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2.0,
        "D": 1.0,
        "F": 0.0}
    return gpaPoint.get(grade, 0.0)

def gradeCalculation():
    totalMark = 0
    numCourse = 0
    print("Welcome for updating your marks")
    studentConfirm()
    student = findStuID(previousID)

    if student is None:
        print("Student Not Found")
        return

    subGrade = {}
    print("Enter the Course ID and the mark for each course.\nPress '0' to stop")
    while True:
        course = input("Course ID: ")
        if course == "0":
            break
        # check whether this student has registered their course
        if not student.get("Course") or student["Course"] == [{}]:
            print("There are no courses recorded in this student profile")
            print("Please register your courses before entering grades")
            menu()
            return
        elif course not in [list(i.keys())[0] for i in student["Course"]]: # get the key of the courses and convert into list
            print("Student has not register for this course.")
        elif course in courseList.keys():
            if course in student["Grades"]:
                print(f"Your mark for {course} course has been uploaded.")
                print("Kindly enter mark for other courses.\n")
                continue

            while True: #loop valid mark
                mark = input("Mark for this course (0-100): ") #string

                if not mark.isdigit(): #only digits no characters no symbols no decimal
                    print("Invalid mark, mark must be digit.")
                    continue
                
                grade = markGrade(mark)
            
                if grade is None:
                    print("Invalid mark, mark must between 0 to 100.")
                    continue
                break
            subGrade[course] = [mark, grade]

            try:
                with open("grades.txt", "a") as file:
                    file.write(f"{student['Student ID']},{course},{mark},{grade}\n")
                student["Grades"][course] = [mark, grade]

            except FileNotFoundError:
                print("File not found. Please make sure the file exists in the program directory before proceeding.")

            points = gpaGrade(grade)
            totalMark += points
            numCourse += 1
        else:
            print("Course not found")
            continue
    print(line)

    student["Grades"].update(subGrade)

    try:
        student["GPA"] = totalMark / numCourse
    except ZeroDivisionError:
        pass
    else:
        print("Your grades has been updated!")
    return

def stuPerformance():
    studentConfirm()
    student = findStuID(previousID)
    
    # make the grade part into one line
    if student is None:
        print("Student not found, please try again")
        return
    
    print("Student Performance: ")
    print(line)
    print(f"Student ID: {student['Student ID']}")
    print(f"Name: {student['Name']}")
    print(f"Email: {student['Email Address']}")
    print("Courses and Grades:\n")
    
    for course_dict in student["Course"]:
        for courseID, courseName in course_dict.items():
            mark, grade = student["Grades"].get(courseID, ["N/A", "N/A"])
            print(f"{courseID} - {courseName}")
            print(f"Mark = {str(mark)+'%'}")
            print(f"Grade = {grade}")
            print(line) 

    print(f"GPA: {student['GPA']:.2f}")
    if student["GPA"] <= 1.0:
        print("You may need to retake this course")
    input("Press Enter to return to main menu ---")

def couPerformance():
    print("--- Course Performance Summary ---")
    courseSelect = input("Course ID for the course report: ")

    # Validate course ID format
    if not is_valid_course_id(courseSelect):
        print("Invalid Course ID format! Must be 3 letters + 4 digits.")
        return

    # Check if course exists
    if courseSelect not in courseList:
        print("Course not found in system.")
        return

    stuMark = {}        # new empty dictionary { stuID : mark }
    marks = []          # a list for calculating avg, highest, lowest

    # Loop through loaded student data (NO file reading)
    for stu in studentList:
        if courseSelect in stu["Grades"]:
            mark = stu["Grades"][courseSelect][0]      # [0] --> give us 80 --> {"CSC1024" : [80 , "A"] 
            stuMark[stu["Student ID"]] = mark        # store in dictionary {"25001": 80}
            marks.append(int(mark))

    # Print marks for each student
    for stuid, mark in stuMark.items():
        student = findStuID(stuid)
        if student:
            print(f"{stuid:} {student['Name']:<20} {str(int(mark))+'%':<5}")
        else:
            print(f"{stuid} {"Unknown Student":<20} {str(int(mark))+'%':<5}")
    print(line)
    # Print summary
    if marks:
        avg = sum(marks) / len(marks)
        highest = max(marks)
        lowest = min(marks)

        print(f"Course {courseSelect}: \nStudents: {len(marks)}\nAverage mark: {avg:.2f}")
        print(f"Highest score: {highest}\nLowest score: {lowest}")
    else:
        print(f"No grades found for course {courseSelect}")

    input("Press Enter to return to main menu --- ")

def exportReport():
    global line
    option = input("What performance report? \nPress 1 for Individual Student Performance Report\nPress 2 for Overall Performance Report\nEnter: ")
    if option == '1':
        opStu = input("Please enter the student ID for the report: ")
        student = findStuID(opStu)
        if student is None:
            print("Student not found. Please try again")
            menu()

        Student_Report_Folder = os.path.join(folder, "Students Report Folder")
        os.makedirs(Student_Report_Folder, exist_ok=True)
        stuReport = os.path.join(Student_Report_Folder, f"{student['Student ID']}_report.txt")

        with open(stuReport,"w") as file:
            file.write(f"--- Student Performance of {student["Student ID"]} ---\n")
            print(line + "\n")
            file.write(f"Student ID: {student['Student ID']}\n")
            file.write(f"Name: {student['Name']}\n")
            file.write(f"Email: {student['Email Address']}\n")
            file.write("Courses and Grades:\n")

            for course_dict in student["Course"]:
                for courseID, courseName in course_dict.items():
                    mark, grade = student["Grades"].get(courseID, ["N/A", "N/A"])
                    file.write(f"{courseID} - {courseName}\n")
                    file.write(f"Mark = {str(mark)+'%'}\n")
                    file.write(f"Grade = {grade}\n")
                    file.write(line + "\n")

            file.write(f"GPA: {student['GPA']:.2f}\n")
            if student["GPA"] <= 1.0:
                file.write("You may need to retake this course")
        print('Please refer to your file under the folder "Students Report Folder"')
        print("Report saved at:", stuReport)  # for individual student
        input("Press Enter to return to main menu --- ")

    elif option == "2":
        courseWithMarks = {}

        Reports_Folder = os.path.join(folder, "Summary Report Folder")
        os.makedirs(Reports_Folder, exist_ok=True)  # creates folder if it doesn't exist
        sumReport = os.path.join(Reports_Folder, "Performance_Report.txt")

        # we get all the courses higher, lower, avg marks
        with open("grades.txt", "r") as file:
            for line in file:
                raw_line = line.strip() 
            
                if not raw_line:      #skip empty lines 
                    continue

                parts = raw_line.split(",")

                if len(parts) != 4:
                    save_invalid_line("invalid_grades.txt", raw_line)
                    continue
            
                stuID, courseID, mark_str, grade = parts
                line = "-------------------------------------------------------"

           # validations ******
                if not is_valid_student_id(stuID):
                    save_invalid_line("invalid_grades.txt", raw_line)
                    continue

                if not is_valid_course_id(courseID):
                    save_invalid_line("invalid_grades.txt", raw_line)
                    continue
            
                chk_grade = markGrade(mark_str)
            
                if chk_grade is None:
                    save_invalid_line("invalid_grades.txt", raw_line)
                    continue
            
                mark = float(mark_str)
                
                if courseID not in courseWithMarks:
                    courseWithMarks[courseID] = [] # create a list for each courseID to store students mark
                courseWithMarks[courseID].append(mark) # add those marks into the list


        with open(sumReport,"w") as file:
            #headings
            file.write(" --- Overall Performance Report ---\n")
            file.write(f'{"Course ID":<12}{"Course Name":<28}{"Average":>10}{"Highest":>10}{"Lowest":>10}\n')
            file.write("-------------------------------------------------------------------------\n")
            # data
            for courseID, marks in courseWithMarks.items():
                courseName = courseList.get(courseID)
                    
                avg = round((sum(marks) / len(marks)),2)
                highest = round(max(marks),2)
                lowest = round(min(marks),2)
                file.write(f'{courseID:<12}{courseName:<28}{str(avg)+'%':>10}{str(highest)+'%':>10}{str(lowest)+'%':>10}\n')

        print('Please refer to your file under the folder "Summary Report Folder"')
        print("Report saved at:", sumReport)  # for overall
        input("Press Enter to return to main menu --- ")
        
def viewInvalid_files(filename: str):
    global line
    option = input("Which invalid text files would you like to review? \nPress 1 for students\nPress 2 for grades\nPress 3 for courses\nEnter: ")
    if option == '1':
        filename = "invalid_students.txt"  #string
    elif option == '2':
        filename = "invalid_grades.txt"
    elif option == '3':
        filename = "invalid_courses.txt"
    else:
        print("Invalid input please try again!")
        return

    try:
        with open(filename, "r") as f:
            content = f.read().strip()
            if not content:
                print(f"No invalid data found in {filename}.")
            else:
                print(f"--- Contents of {filename} ---")
                print(content)

    except FileNotFoundError:
        print(f"File{filename} does not exist. Please make sure the file exists in the program directory before proceeding.")
    
def programEnd():
    return "Program end"

# Option pane
def menu():
    # wait for 3 seconds only continue or ask user whether they want to go back main menu
    while True:
        print(line)
        print("Welcome to Student Grading System")
        option = input("Main Menu:\n1 --- Student registration\n2 --- Course Adding\n3 --- Grade recording\n4 --- Student's Performance Report\n5 --- Course's Performance Summary\n6 --- Export Performance Report\n7 --- Review Invalid Text Files\n0 --- Exit the System\nWhat would you like to do? ")
        match option:
            case "1":
                print(line)
                register()
            case "2":
                print(line)
                courseAdd()
            case "3":
                print(line)
                gradeCalculation()
            case "4":
                print(line)
                stuPerformance()
            case "5":
                print(line)
                couPerformance()
            case "6":
                print(line)
                exportReport()
            case "7":
                print(line)
                viewInvalid_files("all")
            case "0":
                print(line)
                programEnd()
                print(line)
                break
            case _:
                print("Oops! That's not a valid menu option. Try again.")
menu()
