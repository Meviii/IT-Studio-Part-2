import ast
import csv
from User import User, Student, Admin
import os
from Program import *
from Course import *
from Semester import *

# Project start date - end date: 04/10/2021 - 30/10/2021
# Mevlut Saluk, S3717696
# Alexander Tan, S3849729
# Dion Tartaglione, S3239216
# Cesar Jude Quitazol, S3844561
# Haotian Shen, S3770488

# Program Description: Enrollment system with 3 menus: Login, Student, Admin. Each menu has its own features.
# Video: https://youtu.be/fjaIVcREm5w

def login(): # Login function for Admin or Student login BY ID
    try:
        print('Demo Link: https://youtu.be/fjaIVcREm5w')
        print()
        login_type = str(input('Login as Admin or Student(0 to exit)? ')).lower()

        if login_type == 'Admin'.lower(): # Needs implementation
            id = str(input('Please enter your Admin ID: '))
            print('==================================')
            if Admin.open_admins_for_id(id) == True:
                admin = Admin.admin_object(id)
                print(f'     *Welcome {admin.name}*      ')
                admin_menu(id)
            else:
                print('Incorrect Admin ID')

        elif login_type == 'Student'.lower():
            id = str(input('Please enter your Student ID: '))
            
            print('==================================')
            if Student.open_students_for_id(id) == True:
                student = Student.student_object(id)

                print(f'     *Welcome {student.name}*      ')
                return student_menu(id)
            else:
                print('Incorrect Student ID')
        elif login_type == '0':
            return False
        else:
            print('Invalid login type')
            return login()
    except ValueError:
        print('Incorrect selection')
        return False

def student_menu_option(id): # Allows student to return to student_menu() without ending program
    return_main = str(input('Return to main menu? Y/N \n'))
    if return_main.lower() == 'y':
        return student_menu(id)
    else:
        return False

def admin_menu_option(id): # Allows admin to return to student_menu() without ending program
    return_main = str(input('Return to main menu? Y/N \n'))
    if return_main.lower() == 'y':
        return admin_menu(id)
    else:
        return False

def student_menu(id): # Student menu with choices and inner functions

    print()
    print('1. View your Academic History')
    print('2. View available courses') 
    print('3. View and enrol in an offering')
    print('4. Un-enrol from an offering')
    print('5. Get all information')
    print('6. Update your Information')
    print('7. Fees')
    print('8. Check eligibility to graduate')
    print('9. Apply for Leave of Absence')
    print('10. Course Progress')
    print('11. Current GPA')
    print('12. Cancel Program')
    print('0. Exit')
    print('==================================')

    try:
        s = Student.student_object(id)
        choice = int(input('Please pick by index: '))
        res = set(ast.literal_eval(s.get_curr_enrol()))
        all_courses = set(Course.coursesId_list())
        stu_courses = sorted(res.intersection(all_courses))
        s.set_curr_enrol(stu_courses)

        if 1 >= choice >= 13:
            print('Invalid Choice')
            print()
            return student_menu(id)
        elif choice == 0:
            return False
        elif choice == 1: # Academic History
            with open('data/students.csv', 'r') as f:
                reader = csv.reader(f)
                student = []
                for lines in reader:
                    if lines[0] == id:
                        student.append(lines)
                    else:
                        continue
                for i in student:
                    history = ast.literal_eval(i[5]) # or [i.strip() for i[5] in student]
                print('Academic History: ')
                print(f'    {s.get_program()}: ')
                for c in history:
                    print(f'        Course: {c[0]}, Mark: {c[1]}')
                f.close()
            student_menu_option(id)
        elif choice == 2: # Available Courses to enroll into
            print('All available courses for you are: ')
            
            print('Sem 1: \n')
            for i in Course.filtered_courses_list(id):
                if 'S1' in i[4]:
                    print(f'{i[1]}, Semester: {i[4]}')
            print('Sem 2: \n')
            for i in Course.filtered_courses_list(id):
                if 'S2' in i[4]:
                    print(f'{i[1]}, Semester: {i[4]}')
            print()
            student_menu_option(id)
        elif choice == 3: # View current enrollments, add course
                print('You are currently enrolled in: \n')
                for i in Course.courses_list():
                    if i[0] in Student.student_info_list(id)[6]:
                        print(f'{i[0]}: {i[1]}')
                print()
                print()
                selection = str(input('Would you like to add a course? Y/N \n'))
                if selection.lower() == 'n':
                    student_menu_option(id)
                elif selection.lower() == 'y':
                    year_sem = str(input('Which sem would you like to enrol into? SEM12021/SEM22021/SEM12022/SEM22022\n'))
                    if Semester.open_semester_for_id(year_sem) == True:
                        count = 1
                        for i in Course.courses_list():
                            print(f'{count}. {i[0]}: {i[1]}, Credit: {i[2]}\n')
                            count += 1
                        selection = int(input('Enter the index you would like to add. 0 to exit\n'))
                        if selection == 0:
                            return student_menu(id)
                        else:
                            curr_enrolment = s.get_curr_enrol()
                            for x, value in enumerate(sorted(Course.courses_list()),1):
                                if int(selection) == int(x):
                                    if Student.check_prereqs(id, value[0]) == True or Course.check_prereq_empty(value[0]) == True:
                                        Student.remove_from_plan(id, value[0])
                                        Student.add_student_course(id, value[0], year_sem)
                                        return student_menu_option(id)
                                    elif Student.check_prereqs(id, value[0]) == False:
                                        print('You do not meet the requirments\n')
                                        return student_menu(id)
                                    else:
                                        print('Uknown Error')
                    else:
                        print('Invalid Semester')
                        return student_menu(id)
                else:
                    raise ValueError
        elif choice == 4: # View current enrollments, drop course
            print('Enrolled courses: \n')
            count = 1
            for i in Course.courses_list():
                if i[0] in s.get_curr_enrol():
                    print(f'{count}. {i[0]}: {i[1]}')
                    count += 1
            year_sem = str(input('Which course sem would you like to drop? SEM12021/SEM22021/SEM12022/SEM22022\n'))
            if Semester.open_semester_for_id(year_sem) == True:
                selection = int(input(("Enter the index you would like to drop. 0 to exit \n")))
                for x, value in enumerate(sorted(stu_courses),1):
                    if selection == int(x):
                        print(f'{value} dropped.')
                        curr_enrolment = s.get_curr_enrol()
                        for i in curr_enrolment:
                            if str(i) == str(value):
                                curr_enrolment.remove(i)
                                Semester.sem_remove_count(id, i, year_sem)
                                Student.add_to_plan(id, i)
                                Student.remove_course(id, i)
                                break
                        student_menu_option(id)
                    elif selection == 0:
                        return student_menu(id)
                    else:
                        continue
            else:
                print('Incorrect Semester')
                return student_menu(id)
            print()            
        elif choice == 5: # View all personal information
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
            print("Academic Hisory:")
            with open("data/students.csv", 'r') as f:
                reader = csv.reader(f)
                for lines in reader:
                    if lines[0] == id:
                        AHlst = ast.literal_eval(lines[5])
                for i in AHlst:
                    print("   - Course:",i[0], "Mark:",i[1] )
            f.close()

            print("\nCurrent Enrolments:")
            with open("data/students.csv", 'r') as f:
                reader = csv.reader(f)
                for lines in reader:
                    if lines[0] == id:
                        CElst = ast.literal_eval(lines[6])
                for i in range(len(CElst)):
                    print("   -",CElst[i])
            f.close()

            print("\nStudy Plan:")
            with open("data/students.csv", 'r') as f:
                reader = csv.reader(f)
                for lines in reader:
                    if lines[0] == id:
                        SPlst = ast.literal_eval(lines[7])
                for i in range(len(SPlst)):
                    print("   -",SPlst[i])
            f.close()

            print(f"\nAbsence: {s.get_stu_absence()}")
            print()
            student_menu_option(id)
        elif choice == 6: # Update personal information
            print('1. Name\n2. Birth\n3. Gender\n')
            update_sel = int(input('Which detail would you like to update(pick index)? 0 to exit\n'))
            if 0 > update_sel > 3: 
                raise ValueError
            elif update_sel == 0:
                return student_menu(id)
            else:
                if update_sel == 1:
                    name = str(input('Please enter your name: '))
                    if name.isalpha:
                        print('Name changed to '+ name)
                        Student.change_student_name(id, name)
                        return student_menu_option(id)
                    else:
                        print('Please ignore digits')
                        return student_menu(id)
                if update_sel == 2:
                    birth = str(input('Please enter your birth (DD/MM/YYYY): '))
                    print('Birth date changed to ' + birth)
                    Student.change_student_birth(id, birth)
                    return student_menu_option(id)
                if update_sel == 3:
                    gender = str(input('Please enter your gender: '))
                    if gender.isalpha:
                        print('Gender changed to ' + gender)
                        Student.change_student_gender(id, gender)
                        return student_menu_option(id)
                    else:
                        print('Please ignore digits')
                        return student_menu(id)
            #student_menu_option(id)
        elif choice == 7: # View Fees
            print()
            print('The fees for your current enrollment is: \n')
            if not s.get_curr_enrol() is None:
                fees_total = 0
                for i in Course.courses_list():
                    if i[0] in s.get_curr_enrol():
                        print(f'{i[0]}: {i[1]} Fee: ${i[5]}')
                        fees_total += int(i[5])
                print()
                print(f'Total: ${fees_total}')
                print()
                student_menu_option(id)
            else:
                return student_menu(id)
        elif choice == 8: # Check eligibilty to graduate 
            print(f'Program: {s.get_program()}')
            if Student.check_grad_eligility(id) == True and not s.get_program() == 'NA':
                print('You can graduate!')
                student_menu_option(id)
            elif Student.check_grad_eligility(id) == True and s.get_program() == 'NA':
                print('You are not apart of any program')
                student_menu_option(id)
            elif Student.check_grad_eligility(id) == False:
                print('You cannot graduate yet.')
                student_menu_option(id)
            else:
                raise ValueError
        elif choice == 9: # Apply for leave of absence
            if not s.get_stu_absence() == 'NA':
                print(f'You have already applied or accepted for leave of absence. \n Current Status: {s.get_stu_absence()}\n')
                return student_menu(id)
            elif s.get_stu_absence() == 'NA':
                print('Enter 0 anytime to return to main menu.')
                type_absence = str(input('Please select how long you would like to leave for (semester or academic year): '))
                if type_absence == str(0):
                    return student_menu(id)
                elif type_absence == '':
                    print('Invalid time\n')
                    return student_menu(id)
                else:
                    print()
                    print(f'Your application for leave has been processed. Pending for: {type_absence}')
                    Student.apply_for_absence(id, type_absence)
                    return student_menu_option(id)
        elif choice == 10: # View course progress(Currently enrolled and academic history which are passed.)
            print('Current enrolled and successfully passed courses: \n')
            for i in Student.course_progress_stu(id):
                print(i)
            print()
            return student_menu_option(id)
        elif choice == 11: # Calculate current GPA
            if s.get_acad_history() is None:
                print('You do not have any previous course history')
                print()
                return student_menu(id)
            else:
                print(f'Your current gpa is {Student.curr_gpa_stu(id)}\n')
                history = ast.literal_eval(s.get_acad_history())
                for i in history:
                    print(f'Course: {i[0]} Mark: {i[1]}')
                print()
                student_menu_option(id)
        elif choice == 12: # Cancel Program
            if Program.student_program(id) == False:
                print('You are currently not a student of any program.')
                return student_menu(id)
            else:
                print(f'You are currently a student of {s.get_program()}. Are you sure you want to cancel this? Y/N')
                program_update = str(input())
                if program_update.lower() == 'y':
                    Student.remove_stu_program(id)
                    student_menu_option(id)
                elif program_update.lower() == 'n':
                    return student_menu(id)
                else:
                    raise ValueError
        else:
            print('Invalid choice')
            return student_menu(id)
    except ValueError:
        print('Invalid selection')
        return False

def admin_menu(id): # Admin menu with choices and inner functions

    print()
    print('1. Add/Remove/Amend Student')
    print('2. Add/Remove/Amend Course')
    print('3. Add/Remove/Amend Program')
    print('4. Add/Remove/Amend Semester')
    print('5. View student information')
    print('6. Amend study plan for student')
    print('7. Validate student study plan')
    print('8. Generate study plan for a student')
    print('9. View all students achievements of course')
    print('10. Student leave of absence')
    print('11. Set or Remove student program.')
    print('0. Exit')
    print('=======================')
    
    try:
        choice = int(input('Please pick by index: '))
        if 1 >= choice >= 12:
            print('Invalid Choice')
            print()
            return admin_menu(id)
        elif choice == 0:
            return False
        elif choice == 1: # Add/Remove or amend a student
            print(choice)
            student_choice = int(input("Would you like to: \n1. Add Student\n2. Remove Student \n3. Amend Student \n0. Return to Admin Menu\n"))
            if student_choice == 0:
                return admin_menu(id)

            elif student_choice == 1: #adding student
                with open('data/students.csv', 'a+', newline="") as f:
                    new_studentID = input("Enter Student ID (s...): ")
                    while new_studentID.lower() in Student.studentId_list():
                        stuExists = int(input('Student ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if stuExists == 0:
                            return admin_menu(id)
                        elif stuExists == 1:
                            new_studentID = input("Enter Student ID (s...): ")
                        else:
                            input('Please enter a Valid Index (0-1)')
                       
                    new_studentName = input("Enter Student Name: ")
                    new_studentDOB = input("Enter Student Date of Birth (Day/Month/Year): ")
                    new_studentGender = input("Enter Student Gender: ")

                    writer = csv.writer(f, quoting = csv.QUOTE_NONE, quotechar = None)
                    final =  str(str(new_studentID) +','+ str(new_studentName)+','+ str(new_studentDOB)+','+str(new_studentGender)+','+ "NA"+',' +'"'+"[]"+'"' +',' +'"'+"[]"+'"'+','+ '"'+"[]"+'"'+ ','+"NA")
                    writer.writerow(final.split(','))
                f.close()
                print("\nStudent Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))
            elif student_choice == 2: #Removing Student
                Student.show_studentID_list()
                deleted_studentID = input("Enter Student ID to be Removed: ")
                with open('data/students.csv', 'r+') as f:
                    reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    students = []
                    for lines in reader:
                        if lines[0] != deleted_studentID:
                            students.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/students_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    for i in students:
                        writer.writerow(i) #write the new students list into a temp csv file

                f.close()
                #swap the outdated csv with the updated students.csv
                os.remove('data/students.csv')
                os.rename('data/students_temp.csv', 'data/students.csv') 
                
                print("\nStudent Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif student_choice == 3: #Amending Student
                Student.show_studentID_list()

                ammend_student = input("Select which Student you would like to Amend by entering the Student ID: ")

                while_counter = 3
                while ammend_student.lower() not in Student.studentId_list(): #if trying to amend a student that is not already in the file
                    ammend_student = input("Please Enter a Valid Student ID: ")
                    while_counter -= 1
                    if while_counter == 0: #3 attempts before being asked to exit or try again.
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Student.show_studentID_list()
                            ammend_student = input("Select which Student you would like to Amend by entering the Student ID: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    
                    
                ammend_choice = int(input("What would you like to change?\n1. Student Name \n2. Student Gender \n0. Return to Admin Menu \n"))
                if ammend_choice == 0:
                    return admin_menu(id)
     
                elif ammend_choice == 1:
                    upd_stuName = input("What would you like to change this Student's Name to? ") 
                    with open("data/students.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        upd_stuName_lst = []
                        for lines in reader:
                            if lines[0] != ammend_student:
                                upd_stuName_lst.append(lines)
                            else:
                                lines[1] = upd_stuName
                                upd_stuName_lst.append(lines)
                        
                        with open('data/students_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in upd_stuName_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 2:
                    upd_stuGend = input("What would you like to change this Student's Gender to? ") 
                    with open("data/students.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        upd_stuGend_lst = []
                        for lines in reader:
                            if lines[0] != ammend_student:
                                upd_stuGend_lst.append(lines)
                            else:
                                lines[3] = upd_stuGend
                                upd_stuGend_lst.append(lines)
                        
                        with open('data/students_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in upd_stuGend_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                else:
                    input("Please Enter Valid Index (0-2)")

                print("\nStudent Successfully Amended!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            else:
                input("Please Enter Valid Index (0-3), then hit Enter")
        elif choice == 2: # Add/Remove or amend a course
            print(choice)
            course_choice = int(input("Would you like to: \n1. Add Course\n2. Remove Course \n3. Amend Course \n0. Return to Admin Menu\n"))
            if course_choice == 0:
                return admin_menu(id)
            elif course_choice == 1: #Adding Course
                with open('data/courses.csv', 'a+', newline="") as f:
                    new_courseID = input("Enter New Course ID: ")
                    while new_courseID.upper() in Course.coursesId_list(): #makes sure that new course ID does not match with a course Id that already exists.
                        courseExists = int(input('Course ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if courseExists == 0:
                            return admin_menu(id)
                        elif courseExists == 1:
                            new_courseID = input("Enter New Course ID: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_courseName = input("Enter New Course Name: ")
                    while new_courseName.lower() in Course.courses_name_list(): #makes sure that new course ID does not match with a course Id that already exists.
                        courseNameExists = int(input('Course Name already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if courseNameExists == 0:
                            return admin_menu(id)
                        elif courseNameExists == 1:
                            new_courseID = input("Enter New Course Name: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_CourseCred = int(input("Enter Course Credit: "))
                    while not (new_CourseCred == 12 or new_CourseCred ==24): #checks validity of input
                        new_CourseCred = int(input("Please enter a valid Credit Score (12 or 24): "))

                    print("Enter Course Prerequisites: ") #prerequisite input code
                    new_CoursePrereq_amount = int(input("How Many Prerequisites would you like to add? "))
                    new_CoursePrereq_lst = []
                    for i in range(0, new_CoursePrereq_amount):
                        prereq_input = input("Enter the Course Code of Prerequisite: ")
                        while prereq_input.upper() not in Course.coursesId_list():
                            prereq_input = input("Please enter a valid Course Code: ")

                        new_CoursePrereq_lst.append(prereq_input)
                    print("New Prerequisites:", new_CoursePrereq_lst)

                    print("Enter Course Availability: ") #availability input code
                    new_CourseAvail_amount = int(input("Is the course available for 1 or 2 Semesters "))
                    while not (new_CourseAvail_amount == 1 or new_CourseAvail_amount == 2):
                        new_CourseAvail_amount = int(input("Please enter 1 or 2: "))
                    new_CourseAvail_lst = []
                    if new_CourseAvail_amount == 2:
                        new_CourseAvail_lst.append("S1")
                        new_CourseAvail_lst.append("S2")
                    else:
                        avail_input = input("Enter the Semester this Course is available for (S1 / S2): ")        
                        new_CourseAvail_lst.append(avail_input)
                    print("New Course Availabilities:", new_CourseAvail_lst)

                    new_CourseFee = input("Enter Course Fees: ")
                    writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    final =  str(str(new_courseID).upper() +','+ str(new_courseName)+','+ str(new_CourseCred)+',' +'"'+str(new_CoursePrereq_lst)+'"'+','+'"'+ str(new_CourseAvail_lst)+'"'+','+ str(new_CourseFee))
                    writer.writerow(final.split(','))
                f.close()
                print("\nCourse Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif course_choice == 2: #Removing Course
                Course.show_courseID_list()

                deleted_course = input("Enter Course Code of Course to be deleted: ")
                with open('data/courses.csv', 'r+') as f:
                    reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    courses = []
                    for lines in reader:
                        if lines[0] != deleted_course.upper():
                            courses.append(lines) #appends courses to a list, excluding the specified one 

                f.close()
                with open('data/courses_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    for i in courses:
                        writer.writerow(i) #write the new course list into a temp csv file

                f.close()
                #swaps the outdated courses.csv file with the updated one
                os.remove('data/courses.csv')
                os.rename('data/courses_temp.csv', 'data/courses.csv')

                print("\nCourse Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif course_choice == 3: #Amending Course
                Course.show_courseID_list()

                ammend_course = input("Select which Course you would like to Amend by entering the Course Code: ")

                while_counter = 3
                while ammend_course.upper() not in Course.coursesId_list(): #if trying to amend a student that is not already in the file
                    ammend_course = input("Please Enter a Valid Course Code: ")
                    while_counter -= 1
                    if while_counter == 0: #3 attempts before being asked to exit or try again.
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Course.show_courseID_list()
                            ammend_course = input("Select which Course you would like to Amend by entering the Course Code: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    
                ammend_choice = int(input("What would you like to change? \n1. Course Credit \n2. Course Prerequisites \n3. Course Availability \n4. Course Fees \n0. Return to Admin Menu \n"))
                
                if ammend_choice == 0:
                    return admin_menu(id)

                elif ammend_choice == 1:
                    changed_credit = int(input("What would you like to change the Course Credit to? "))
                    while not (changed_credit == 12 or changed_credit == 24):
                        changed_credit = int(input("Please enter a valid Credit Score (12 or 24): "))

                    with open("data/courses.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        ccredit_lst = []
                        for lines in reader:
                            if lines[0] != ammend_course.upper():
                                ccredit_lst.append(lines)
                            else:
                                lines[2] = changed_credit
                                ccredit_lst.append(lines)
                        
                        with open('data/courses_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in ccredit_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 2:
                    print("Enter Course Prerequisites: ") #prerequisite input code
                    ammend_CoursePrereq_amount = int(input("How many prerequisites would you like the Course to have? "))
                    ammend_CoursePrereq_lst = []
                    for i in range(0, ammend_CoursePrereq_amount):
                        ammendprereq_input = input("Enter the Course Code of Prerequisite: ")
                        while ammendprereq_input.upper() not in Course.coursesId_list():
                            ammendprereq_input = input("Please enter a valid Course Code: ")
                        ammend_CoursePrereq_lst.append(ammendprereq_input)
                    print("New Prerequisites:", ammend_CoursePrereq_lst)
                    changed_prereq = ('"'+ str(ammend_CoursePrereq_lst)+'"')
                    
                    with open("data/courses.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        cprereq_lst = []
                        for lines in reader:
                            if lines[0] != ammend_course.upper():
                                cprereq_lst.append(lines)
                            else:
                                lines[3] = changed_prereq
                                cprereq_lst.append(lines)
                        
                        with open('data/courses_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in cprereq_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 3:
                    print("Change the Course Availability to: ")
                    courseAvail_amount = int(input("Is the course available for 1 or 2 Semesters "))
                    while not (courseAvail_amount == 1 or courseAvail_amount == 2):
                        courseAvail_amount = int(input("Please enter 1 or 2: "))
                    courseAvail_lst = []
                    if courseAvail_amount == 2:
                        courseAvail_lst.append("S1")
                        courseAvail_lst.append("S2")
                    else:
                        avail_input = input("Enter the Semester this Course is available for (S1 / S2): ")        
                        courseAvail_lst.append(avail_input)
                    print("New Course Availabilities:", courseAvail_lst)
                    changed_avail = str('"'+str(courseAvail_lst)+'"')

                    with open("data/courses.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        cavail_lst = []
                        for lines in reader:
                            if lines[0] != ammend_course.upper():
                                cavail_lst.append(lines)
                            else:
                                lines[4] = changed_avail
                                cavail_lst.append(lines)
                        
                        with open('data/courses_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in cavail_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 4:
                    changed_fee = input("What would you like to change the Course Fees to? ") 
                    with open("data/courses.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        cfees_lst = []
                        for lines in reader:
                            if lines[0] != ammend_course.upper():
                                cfees_lst.append(lines)
                            else:
                                lines[5] = changed_fee
                                cfees_lst.append(lines)
                        
                        with open('data/courses_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in cfees_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                else:
                    input("Please Enter Valid Index (0-4)")

                print("\nCourse Successfully Amended!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            else:
                input("Please Enter Valid Index (0-3), then hit Enter")
        elif choice == 3: # Add/Remove or amend a program
            print(choice)
            program_choice = int(input("Would you like to: \n1. Add Program\n2. Remove Program \n3. Amend Program \n0. Return to Admin Menu\n"))
            if program_choice == 0:
                return admin_menu(id)
            elif program_choice == 1: #Adding Program
                with open('data/programs.csv', 'a', newline = "") as f:
                    new_progID = input("Enter New Program ID: ")
                    while new_progID.upper() in Program.program_Id_list(): #makes sure that new program ID does not match with a program Id that already exists.
                        progIdExists = int(input('Program ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if progIdExists == 0:
                            return admin_menu(id)
                        elif progIdExists == 1:
                            new_progID = input("Enter New Program ID: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_progName = input("Enter New Program Name: ")
                    while new_progName.upper() in Program.program_Id_list(): #makes sure that new program ID does not match with a program Id that already exists.
                        progNameExists = int(input('Program Name already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if progNameExists == 0:
                            return admin_menu(id)
                        elif progNameExists == 1:
                            new_progName = input("Enter New Program Name: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_progCred = int(input("Enter Program Credit Points: "))

                    print("Enter Program Courses: ")
                    new_progCouse_amount = int(input("How many courses would you like to add: "))
                    new_progCourse_lst =[]
                    for i in range(0, new_progCouse_amount):
                        course_input = input("Enter Course Code of Course you would like to add: ")
                        while course_input.upper() not in Course.coursesId_list():
                            course_input = input("Please enter a valid Course Code: ")
                        new_progCourse_lst.append(course_input)

                    print("Enter Program Courses: ")
                    new_progElec_amount = int(input("How many courses would you like to add: "))
                    new_progElec_lst =[]
                    for i in range(0, new_progElec_amount):
                        course_input = input("Enter Course Code of Course you would like to add: ")
                        while course_input.upper() not in Course.coursesId_list():
                            course_input = input("Please enter a valid Course Code: ")
                        new_progElec_lst.append(course_input)

                    writer = csv.writer(f, quoting = csv.QUOTE_NONE, quotechar = None)
                    final =  str(str(new_progID) +','+ str(new_progName)+','+str(new_progCred)+','+'"'+str(new_progCourse_lst)+'"'+','+ '"'+str(new_progElec_lst)+'"')
                    writer.writerow(final.split(','))
                f.close()
                print("\nProgram Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)")) 

            elif program_choice == 2: #Removing Program
                Program.show_programsID_list()

                deleted_Program = input("Enter Program ID to be Removed: ")
                with open('data/programs.csv', 'r+') as f:
                    reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    programs = []
                    for lines in reader:
                        if lines[0] != deleted_Program.upper():
                            programs.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/programs_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    for i in programs:
                        writer.writerow(i) #write the new students list into a temp csv file

                f.close()
                #swap the outdated csv with the updated students.csv
                os.remove('data/programs.csv')
                os.rename('data/programs_temp.csv', 'data/programs.csv') 

                print("\nProgram Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif program_choice == 3: #Ammeding Program
                Program.show_programsID_list()
                ammend_programs = input("Select which Program you would like to Amend by entering the Program Code: ")
                
                while_counter = 3 
                while ammend_programs.upper() not in Program.program_Id_list(): #if trying to amend a student that is not already in the file
                    ammend_programs = input("Please Enter a Valid Program Code: ")
                    while_counter -= 1
                    if while_counter == 0: #3 attempts before being asked to exit or try again.
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Program.show_programsID_list()
                            ammend_programs = input("Select which Program you would like to Amend by entering the Program Code: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    
                ammend_choice = int(input("What would you like to change? \n1. Program Credit Points \n2. Program Courses \n3. Program Elective Courses \n0. Return to Admin Menu \n"))
                if ammend_choice ==0:
                    return admin_menu(id)

                elif ammend_choice == 1:
                    changed_progCred = int(input("What would you like to change the Program Credit Points to? ")) 
                    with open("data/programs.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        cprogCred_lst = []
                        for lines in reader:
                            if lines[0] != ammend_programs.upper():
                                cprogCred_lst.append(lines)
                            else:
                                lines[2] = changed_progCred
                                cprogCred_lst.append(lines)
                        
                        with open('data/programs_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in cprogCred_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv')  

                elif ammend_choice == 2:
                    changed_progCourse = input("What would you like to change the Program Courses to? ") 
                    with open("data/programs.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        cprogCourse_lst = []
                        for lines in reader:
                            if lines[0] != ammend_programs.upper():
                                cprogCourse_lst.append(lines)
                            else:
                                lines[3] = changed_progCourse 
                                cprogCourse_lst.append(lines)
                        
                        with open('data/programs_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in cprogCourse_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                elif ammend_choice == 3:
                    changed_progElecCourse = input("What would you like to change the Elective Program Courses to? ") 
                    with open("data/programs.csv", 'r') as f:
                        reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        cprogElecCourse_lst = []
                        for lines in reader:
                            if lines[0] != ammend_programs.upper():
                                cprogElecCourse_lst.append(lines)
                            else:
                                lines[4] = changed_progElecCourse 
                                cprogElecCourse_lst.append(lines)
                        
                        with open('data/programs_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                            for i in cprogElecCourse_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv') 
                        
                else:
                    input("Please Enter Valid Index (0-3)")

                print("\nProgram Successfully Amended!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))
        
            else:
                input("Please Enter Valid Index (0-3), then hit Enter")
        elif choice == 4: # Add/Remove or amend a semester
            print(choice)
            semester_choice = int(input("Would you like to: \n1. Add Semester\n2. Remove Semester \n3. Amend Semester \n0. Return to Admin Menu\n"))
            if semester_choice == 0:
                return admin_menu(id)
            elif semester_choice == 1: #Adding Semester
                with open('data/semesters.csv', 'a', newline = "") as f:
                    new_semProg = input("Enter New Semester Program Code: ")
                    new_semID = input("Enter New Semester ID: ")
                    while new_semID.upper() in Semester.semesterID_list():
                        semIdExists = int(input('Semester ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if semIdExists == 0:
                            return admin_menu(id)
                        elif semIdExists == 1:
                            new_semID = input("Enter New Semester ID: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    print("Enter New Semester Offers: ")
                    new_semOffer_amount = int(input("How many courses would you like to add: "))
                    new_semOffer_lst =[]
                    for i in range(0, new_semOffer_amount):
                        sem_input = input("Enter Course Code of Course you would like to add: ")
                        while sem_input.upper() not in Course.coursesId_list():
                            sem_input = input("Please enter a valid Course Code: ")
                        new_semOffer_lst.append(sem_input)
                    
                    new_semCurStu = input("Enter Current Enrolled Students for Semester: ")
                    new_semMaxStu = input("Enter Max Students for Semester: ")
                    writer = csv.writer(f, quoting = csv.QUOTE_NONE, quotechar = None)
                    final =  str(str(new_semProg).upper() +','+ str(new_semID).upper()+','+ '"'+str(new_semOffer_lst)+'"'+','+str(new_semCurStu)+','+ str(new_semMaxStu))
                    writer.writerow(final.split(','))
                f.close()
                print("\nSemester Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif semester_choice == 2: #Removing Semester
                Semester.show_semesterID_list()

                deleted_semester1 = input("Enter Program Code of Semester to be Removed: ")
                deleted_semester2 = input("Enter Semester ID to be Removed: ")
                with open('data/semesters.csv', 'r+') as f:
                    reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    semesters = []
                    for lines in reader:
                        if (lines[0], lines[1]) != (deleted_semester1.upper(), deleted_semester2.upper()):
                            semesters.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/semesters_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    for i in semesters:
                        writer.writerow(i) #write the new students list into a temp csv file

                f.close()
                #swap the outdated csv with the updated students.csv
                os.remove('data/semesters.csv')
                os.rename('data/semesters_temp.csv', 'data/semesters.csv') 

                print("\nSemester Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif semester_choice == 3: #Amending Semester
                Semester.show_semesterID_list()
                
                ammend_semester1 = input("Select which Program you would like to Amend by entering the Program Code: ")  
                while_counter = 3
                while ammend_semester1.upper() not in Semester.programCode_list(): #if trying to amend a student that is not already in the file
                    ammend_semester1 = input("Please Enter a valid Program Code: ")
                    while_counter -= 1
                    if while_counter == 0: #3 attempts before being asked to exit or try again.
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Semester.show_semesterID_list()
                            ammend_semester1 = input("Select which Program you would like to Amend by entering the Program Code: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))

                ammend_semester2 = input("Select which Semester you would like to Amend by entering the Semester ID: ")   
                while_counter = 3
                while ammend_semester2.upper() not in Semester.semesterID_list(): #if trying to amend a student that is not already in the file
                    ammend_semester2 = input("Please Enter a valid Semester ID: ")
                    while_counter -= 1
                    if while_counter == 0: #3 attempts before being asked to exit or try again.
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Semester.show_semesterID_list()
                            ammend_semester2 = input("Select which Semester you would like to Amend by entering the Semester ID: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))

                changed_maxStu = input("What would you like to change the Semester Max Students to? ") 
                with open("data/semesters.csv", 'r') as f:
                    reader = csv.reader(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                    cmaxStu_lst = []
                    for lines in reader:
                        if (lines[0], lines[1]) != (ammend_semester1.upper(), ammend_semester2.upper()):
                            cmaxStu_lst.append(lines)
                        else:
                            lines[4] = changed_maxStu
                            cmaxStu_lst.append(lines)
                    
                    with open('data/semesters_temp.csv', 'w+', newline='') as f:
                        writer = csv.writer(f,quoting = csv.QUOTE_NONE, quotechar = None, escapechar='\\')
                        for i in cmaxStu_lst:
                            writer.writerow(i) #write the new students list into a temp csv file
                f.close()
                os.remove('data/semesters.csv')
                os.rename('data/semesters_temp.csv', 'data/semesters.csv') 


                print("\nSemester Successfully Amended!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            else:
                input("Please Enter Valid Index (0-3), then hit Enter")
        elif choice == 5: # View information of a student
            student_id = str(input('Please enter a student id: '))
            if Student.open_students_for_id(student_id) == True:
                s = Student.student_object(student_id)
                print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}\n')
                
                print("Academic Hisory:")
                with open("data/students.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        if lines[0] == student_id:
                            AHlst = ast.literal_eval(lines[5])
                    for i in AHlst:
                        print("   - Course:",i[0], "Mark:",i[1] )
                f.close()

                print("\nCurrent Enrolments:")
                with open("data/students.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        if lines[0] == student_id:
                            CElst = ast.literal_eval(lines[6])
                    for i in range(len(CElst)):
                        print("   -",CElst[i])
                f.close()

                print("\nStudy Plan:")
                with open("data/students.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        if lines[0] == student_id:
                            SPlst = ast.literal_eval(lines[7])
                    for i in range(len(SPlst)):
                        print("   -",SPlst[i])
                f.close()

                print(f"\nAbsence: {s.get_stu_absence()}")
                print()
                return admin_menu_option(id)
            else:
                print('Invalid student id')
                return admin_menu(id)
        elif choice == 6: # Add or Remove from a student's study plan
            print()
            print('You can exit any time by entering 0.\n')
            print('1. Add course to plan\n2. Remove course from plan\n')
            plan_choice = int(input('Please enter the index you would like to amend for the student: \n'))
            if plan_choice == 0:
                return admin_menu(id)
            if plan_choice == 1:
                # should ignore the check if student passed the subject already as it should be able to be altered
                print('Note: Adding a course to study plan which is enrolled by the student will drop that subject.\n')
                student_choice = str(input('Please enter the student id you would like to amend for: '))
                if str(student_choice) == str(0):
                    return admin_menu(id)
                if Student.open_students_for_id(student_choice) == True:
                    course_choice = str(input('Please enter the course code of the course you would like to add: '))
                    if str(course_choice) == str(0):
                        return admin_menu(id)
                    if Course.open_for_courseid(course_choice) == True:
                        study_plan = ast.literal_eval(Student.student_info_list(student_choice)[7])
                        stu_enrolment = ast.literal_eval(Student.student_info_list(student_choice)[6])
                        if not course_choice in study_plan:
                            if course_choice in stu_enrolment:
                                print('Course added to plan and removed from enrollment.')
                                Student.add_to_plan(student_choice, course_choice)
                                Student.remove_course(student_choice, course_choice)
                                return admin_menu_option(id)
                            else:
                                print('Course added to plan')
                                Student.add_to_plan(student_choice, course_choice)
                                return admin_menu_option(id)
                        else:
                            print('Course already in study plan')
                            return admin_menu(id)
                    else:
                        print('Course does not exist')
                        return admin_menu(id)
                else:
                    print('Student does not exist')
                    return admin_menu(id)
            elif plan_choice == 2:
                print('Note: Removing a course to study plan which is enrolled by the student will drop that subject.\n')
                student_choice = str(input('Please enter the student id you would like to amend for: '))
                if int(student_choice) == 0:
                    return admin_menu(id)
                if Student.open_students_for_id(student_choice) == True:
                    course_choice = str(input('Please enter the course code of the course you would like to remove: '))
                    if int(course_choice) == 0:
                        return admin_menu(id)
                    if Course.open_for_courseid(course_choice) == True:
                        study_plan = ast.literal_eval(Student.student_info_list(student_choice)[7])
                        stu_enrolment = ast.literal_eval(Student.student_info_list(student_choice)[6])
                        if course_choice in study_plan:
                            if course_choice in stu_enrolment:
                                print('Course removed from plan and enrollment')
                                Student.remove_from_plan(student_choice, course_choice)
                                Student.remove_course(student_choice, course_choice)
                                return admin_menu_option(id)
                            else:
                                print('Course removed from plan')
                                Student.remove_from_plan(student_choice, course_choice)
                                return admin_menu_option(id)
                        else:
                            print('Course already in student plan.')
                            return admin_menu(id)
                    else:
                        print('Course does not exist')
                        return admin_menu(id)
                else:
                    print('Student does not exist')
                    return admin_menu(id)
            else:
                raise ValueError
        elif choice == 7: # Check if study plan is correct for student. Checks if student enroled into >5 courses
            print('You can exit any time by entering 0.\n')
            student_id = str(input('Please enter the student id you would like to validate: '))
            if str(student_id) == str(0):
                return admin_menu(id)
            else:
                if Student.open_students_for_id(student_id) == True:
                    stu_cur_enrolment = ast.literal_eval(Student.student_info_list(student_id)[6])
                    if len(stu_cur_enrolment) >4:
                        val_choice = int(input('Please pick an index of what you would like to do: '))
                        print('1. Drop all subjects of student\n0. Exit')
                        print('')
                        if val_choice == 0:
                            return admin_menu(id)
                        elif val_choice == 1:
                            print('All enrollments have been dropped.')
                            Student.drop_stu_enrolment(student_id)
                            return admin_menu_option(id)
                        else:
                            print('Invalid choice')
                            return admin_menu(id)
                    else:
                        print('Student enrollment is correct.')
                        return admin_menu_option(id)
        elif choice == 8: # Remove courses from study plan if passed in academic history else if failed, re add
            stu_id = str(input('Please enter the student id of the student: '))
            if Student.open_students_for_id(stu_id) == True:
                study_plan = ast.literal_eval(Student.student_info_list(stu_id)[7])
                print()
                for i in Student.stu_failed_couses(stu_id):
                    if i in study_plan:
                        print('Already in study plan.')
                        break
                    else:
                        print(f'{i} added to study plan.')
                        Student.add_to_plan(stu_id, i)
                study_plan_new = ast.literal_eval(Student.student_info_list(stu_id)[7])
                print()
                print('Student needs to complete the following to graduate: ')
                for i in study_plan_new:
                    print(i)
                return admin_menu_option(id)
            else:
                print('Invalid student')
                return admin_menu(id)
        elif choice == 9: # Student academic history of a course for all students who completed a specific course
            course_code = str(input('Please enter the course code: '))
            if Course.open_for_courseid(course_code) == True:
                print(f'The current achievements for each student for course {course_code}: \n')
                Admin.achievement_by_course(course_code)
                print()
                return admin_menu_option(id)
            else:
                print('Course not found')
                return admin_menu(id)
        elif choice == 10: # Leave of absence of student
            print('Current students who applied for a leave of absence: \n')
            #print a for loop of all students who do not have NA in stu[8]
            for i in Student.all_students():
                if not i[8] == 'NA':
                    print(f'Stu ID: {i[0]}, Name: {i[1]}, Reason: {i[8]}')

            print()
            stu_id = str(input('Please enter the student id of which you want to validate leave of absence.'))

            if Student.open_students_for_id(stu_id) == True:
                option = str(input('Would you like to accept or deny the leave of absence? accept/deny '))
                if option.lower() == 'accept':
                    print('Student application accepted.')
                    Admin.absence_accept(stu_id)
                    return admin_menu_option(id)
                elif option.lower() == 'deny':
                    print('Student application denied.')
                    Admin.absence_deny(stu_id)
                    return admin_menu_option(id)
                else:
                    print('Invalid option')
                    return admin_menu(id)
            else:
                print('Invalid student id')
                return admin_menu(id)
        elif choice == 11: # Set a students program or remove.
            print('You can exit anytime by entering 0')
            print()
            stu_id_prog = str(input('Please enter the id of the student: '))
            if stu_id_prog == str(0):
                return admin_menu(id)
            if Student.open_students_for_id(stu_id_prog) == True:
                remove_program_choice = str(input('Would you like to remove the students program? Y/N'))
                if remove_program_choice.lower() == 'y':
                    print('Student removed from program.')
                    Student.remove_stu_program(stu_id_prog)
                    admin_menu_option(id)
                elif remove_program_choice.lower() == 'n':
                    program_set = str(input('Please enter the program code to set to: '))
                    if program_set == str(0):
                        return admin_menu(id)
                    if Program.open_program_by_id(program_set) == True:
                        if Student.student_info_list(stu_id_prog)[4] == 'NA':
                            print('Program set for ' + stu_id_prog)
                            Admin.add_stu_program(stu_id_prog, program_set)
                            print()
                            return admin_menu_option(id)
                        else:
                            print('Student already a part of a program.\n')
                            choice = str(input('Would you like to remove and add a new program? Y/N'))
                            if choice.lower() == 'y':
                                print('Program set for ' + stu_id_prog)
                                Admin.add_stu_program(stu_id_prog, program_set)
                                print()
                                return admin_menu_option(id)
                            elif choice.lower() == 'n':
                                return admin_menu(id)
                            else:
                                print('Invalid choice')
                                return admin_menu(id)
                    else:
                        print('Invalid choice')
                        return admin_menu(id)
                else:
                    print('Invalid program')
                    return admin_menu(id)
            else:
                print('Invalid student')
                return admin_menu(id)
        else:
            print('Invalid choice')
            return admin_menu(id)
    except ValueError:
        print('Invalid index')

