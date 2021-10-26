import ast
import csv
from User import User, Student, Admin
import os
from Program import *
from Course import *
from Semester import *

def login(): # Login function for Admin or Student login BY ID
    try:
        login_type = str(input('Login as Admin or Student? ')).lower()

        if login_type == 'Admin'.lower(): # Needs implementation
            id = str(input('Please enter your Admin ID: '))
            print('==================================')
            if Admin.open_admins_for_id(id) == True:
                admin = Admin.admin_object(id)
                print(f'Welcome {admin.name}\n')
                admin_menu(id)
            else:
                print('Incorrect Admin ID')

        elif login_type == 'Student'.lower():
            id = str(input('Please enter your Student ID: '))
            
            print('==================================')
            if Student.open_students_for_id(id) == True:
                student = Student.student_object(id)

                print(f'        Welcome {student.name} \n')
                return student_menu(id)
            else:
                print('Incorrect Student ID')
        else:
            raise ValueError
    except ValueError:
        print('Incorrect selection')
        return False

def student_menu_option(id): # Allows student to return to student_menu() without ending program
    return_main = str(input('Return to main menu? Y/N \n'))
    if return_main.lower() == 'y':
        return student_menu(id)
    else:
        return False

def student_program(id): # Returns True if student is in program, else, False
    with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if lines[0] == id:
                   if lines[4] == 'NA':
                       return False
            return True

def student_menu(id): # Student menu with choices and inner functions

    print('     *STUDENT MENU*      ')
    print()
    print('1. View your Academic History')
    print('2. View available courses') # should display courses which are not completed
    print('3. View and enrol in an offering')
    print('4. Un-enrol from an offering')
    print('5. Get all information')
    print('6. Update your Information')
    print('7. Fees')
    print('8. Check elgibility to graduate')
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
        all_courses = set(Course.courses_name_list())
        stu_courses = sorted(res.intersection(all_courses))
        s.set_curr_enrol(stu_courses)

        if 0 > choice > 12:
            raise ValueError
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
            
            print('Sem 1: ')
            for i in Course.filtered_courses_list(id):
                if 'S1' in i[4]:
                    print(f'{i[1]}, Semester: {i[4]}')
            print('Sem 2: ')
            for i in Course.filtered_courses_list(id):
                if 'S2' in i[4]:
                    print(f'{i[1]}, Semester: {i[4]}')
            print()
            student_menu_option(id)
        elif choice == 3: # View current enrollments, add course
                print('You are currently enrolled in: \n')
                for i in Course.courses_list():
                    if i[0] in s.get_curr_enrol():
                        print(f'{i[0]}: {i[1]}')
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
                        print('Error')
                        return False
            else:
                print('Incorrect Semester')
                return student_menu(id)
            print()            
        elif choice == 5: # View all personal information
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
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
                for i in courses_list():
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
            print(s.get_program())
            if Student.check_grad_eligility(id) == True and not s.get_program() == 'NA':
                print('You can graduate!')
                student_menu_option(id)
            elif Student.check_grad_eligility(id) == True and s.get_program() == 'NA':
                print('You are not apart of any program')
                student_menu_option(id)
            elif Student.check_grad_eligility(id) == False:
                print('You cannot graduate yet.')
            else:
                raise ValueError
        elif choice == 9: # Apply for leave of absence
            if not s.get_stu_absence() == 'NA':
                print(f'You have already applied or accepted for leave of absence. \n Current Status: {s.get_stu_absence}')
            elif s.get_stu_absence() == 'NA':
                type_absence = str(input('Please select how long you would like to leave for (semester or academic year): '))
                print(f'Your application for leave has been processed. Pending for: {type_absence}')
                Student.apply_for_absence(id, type_absence)
        elif choice == 10: # View course progress(Currently enrolled and academic history which are passed.)
            print('Current successfully completed courses: \n')
            for i in Student.course_progress_stu(id):
                print(i)
        elif choice == 11: # Calculate current GPA
            if s.get_acad_history() is None:
                print('You do not have any previous course history')
                return student_menu(id)
            else:
                print(f'Your current gpa is {Student.curr_gpa_stu(id)}\n')
                history = ast.literal_eval(s.get_acad_history())
                for i in history:
                    print(f'Course: {i[0]} Mark: {i[1]}')
                student_menu_option(id)
        elif choice == 12: # Cancel Program
            if student_program(id) == False:
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
            return False
    except ValueError:
        print('Invalid selection')
        return False

def admin_menu(id): # Admin menu with choices and inner functions

    print('     *ADMIN MENU*      ')
    print('1. Add/Remove/Amend Student')
    print('2. Add/Remove/Amend Course')
    print('3. Add/Remove/Amend Program')
    print('4. Add/Remove/Amend Semester')
    print('5. View student information')
    print('6. Amend Study plan for student')
    print('7. Validate student study plan')
    print('8. Generate study plan for student')
    print('9. View all students achievements of course')
    print('0. Exit')
    print('=======================')
    
    try:
        choice = int(input('Please pick by index: '))
        unknown_choice = print("Please type 'Add', 'Remove' or 'Ammend' then hit Enter")
        if 0 > choice > 5:
            raise ValueError
        elif choice == 1:
            print(choice)
            student_choice = input("Would you like to Add, Remove or Ammend Student")
            if student_choice.lower() == "add":
                with open('data/students.csv', 'a') as f:
                    new_studentID = input("Enter Student ID: ")
                    new_studentName = input("Enter Student Name: ")
                    new_studentDOB = input("Enter Student Date of Birth: ")
                    new_studentGender = input("Enter Student Gender: ")
                    new_studentProgram = input("Enter Student Program: ")
                    new_studentEnrolled = input("Enter Course Enrolled: ")
                    writer = csv.writer(f)
                    writer.writerow([new_studentID, new_studentName, new_studentDOB, new_studentGender, new_studentProgram, [], new_studentEnrolled, []])
                f.close()
            elif student_choice.lower() == "remove":
                deleted_studentID = input("Enter Student ID to be Removed: ")
                with open('data/students.csv', 'r+') as f:
                    reader = csv.reader(f)
                    students = []
                    for lines in reader:
                        if lines[0] != deleted_studentID:
                            students.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/students_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in students:
                        writer.writerow(i) #write the new students list into a temp csv file


                #swap the outdated csv with the updated students.csv
                os.remove('data/students.csv')
                os.rename('data/students_temp.csv', 'data/students.csv') 
                
            elif student_choice.lower() == "ammend":
                # show admin what is currently in the students.csv
                with open("data/students.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        print(lines)
                f.close()

                with open("data/students.csv", 'r') as inf, open("data/students.csv", 'w') as outf:
                    reader = csv.reader(inf)
                    writer = csv.writer(outf)
                    ammend_student = input("Select which Student you would like to Ammend by entering the Student ID: ")
                    for lines in reader:
                        if ammend_student not in studentId_list(): #if trying to ammend a student that is not already in the file
                            print("Please Enter a Valid Student ID: ")
                        else:
                            ammend_choice = input("What would you like to change? (Student ID / Student Name / Student DOB / Student Gender / Student Program / Student History / Student Enrolled Course / Student Study Plan)")
                            if ammend_choice.lower() == "student id":
                                upd_StudentID = input("What would you like to change this Student's Student ID to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuID_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuID_lst.append(lines)
                                        else:
                                            lines[0] = upd_StudentID
                                            upd_stuID_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuID_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student name":
                                upd_stuName = input("What would you like to change this Student's Name to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuName_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuName_lst.append(lines)
                                        else:
                                            lines[1] = upd_stuName
                                            upd_stuName_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuName_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student dob":
                                upd_stuDOB = input("What would you like to change this Student's Name to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuDOB_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuDOB_lst.append(lines)
                                        else:
                                            lines[2] = upd_stuDOB
                                            upd_stuDOB_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuDOB_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student gender":
                                upd_stuGend = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuGend_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuGend_lst.append(lines)
                                        else:
                                            lines[3] = upd_stuGend
                                            upd_stuGend_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuGend_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student program":
                                upd_stuProg = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuProg_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuProg_lst.append(lines)
                                        else:
                                            lines[4] = upd_stuProg
                                            upd_stuProg_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuProg_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student history":
                                upd_stuHist = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuHist_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuHist_lst.append(lines)
                                        else:
                                            lines[5] = upd_stuHist
                                            upd_stuHist_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuHist_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student enrolled course":
                                upd_stuEnrol = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuEnrol_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuEnrol_lst.append(lines)
                                        else:
                                            lines[6] = upd_stuEnrol
                                            upd_stuEnrol_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuEnrol_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student study plan":
                                upd_stuStudPlan = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuStudPlan_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuStudPlan_lst.append(lines)
                                        else:
                                            lines[7] = upd_stuStudPlan
                                            upd_stuStudPlan_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuStudPlan_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            else:
                                print("Please Enter Valid Choice (Student ID / Student Name / Student DOB / Student Gender / Student Program / Student History / Student Enrolled Course / Student Study Plan)")


            else:
                unknown_choice

        elif choice == 2:
            print(choice)
            course_choice = input("Would you like to Add, Remove or Ammend Course")
            if course_choice.lower() == "add":
                with open('data/courses.csv', 'a') as f:
                    new_courseID = input("Enter New Course ID: ")
                    new_courseName = input("Enter New Course Name: ")
                    new_CourseCred = input("Enter Course Credit: ")
                    new_CoursePrereq = input("Enter Course Prerequisites: ")
                    new_CourseAvail = input("Enter Course Availability: ")
                    new_CourseFee = input("Enter Course Fees: ")
                    writer = csv.writer(f)
                    writer.writerow([new_courseID, new_courseName, new_CourseCred, new_CoursePrereq, new_CourseAvail, new_CourseFee])
                f.close()

            elif course_choice.lower() == "remove":
                deleted_course = input("Enter Course Code of Course to be deleted: ")
                with open('data/courses.csv', 'r+') as f:
                    reader = csv.reader(f)
                    courses = []
                    for lines in reader:
                        if lines[0] != deleted_course:
                            courses.append(lines) #appends courses to a list, excluding the specified one 

                f.close()

                with open('data/courses_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in courses:
                        writer.writerow(i) #write the new course list into a temp csv file

                #swaps the outdated courses.csv file with the updated one
                os.remove('data/courses.csv')
                os.rename('data/courses_temp.csv', 'data/courses.csv')
            elif course_choice.lower() == "ammend":
                # show admin what is currently in the courses.csv
                with open("data/courses.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        print(lines)
                f.close()

                with open("data/courses.csv", 'r') as f:
                    reader = csv.reader(f)
                    ammend_course = input("Select which Course you would like to Ammend by entering the Course Code: ")
                    for lines in reader:
                        if ammend_course not in courses_name_list(): #if trying to ammend a student that is not already in the file
                            input("Please Enter a Valid Student ID: ")
                        else:
                            ammend_choice = input("What would you like to change? (Course Code / Course Name / Course Credit / Course Prerequisites / Course Availability / Course Fees) ")
                            if ammend_choice.lower() == "course code":
                                changed_code = input("What would you like to change the Course Code to? ") 
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    crs_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            crs_lst.append(lines)
                                        else:
                                            lines[0] = changed_code
                                            crs_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in crs_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course name":
                                changed_cname = input("What would you like to change the Course Name to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cname_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cname_lst.append(lines)
                                        else:
                                            lines[1] = changed_cname
                                            cname_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cname_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course credit":
                                changed_credit = input("What would you like to change the Course Credit to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    ccredit_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            ccredit_lst.append(lines)
                                        else:
                                            lines[2] = changed_credit
                                            ccredit_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in ccredit_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course prerequisite":
                                changed_prereq = input("What would you like to change the Prerequisites to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprereq_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cprereq_lst.append(lines)
                                        else:
                                            lines[3] = changed_prereq
                                            cprereq_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprereq_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course availability":
                                changed_avail = input("What would you like to change the Course Availability to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cavail_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cavail_lst.append(lines)
                                        else:
                                            lines[4] = changed_avail
                                            cavail_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cavail_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course fees":
                                changed_fee = input("What would you like to change the Course Fees to? ") 
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cfees_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cfees_lst.append(lines)
                                        else:
                                            lines[5] = changed_fee
                                            cfees_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cfees_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            else:
                                print("Please Enter Valid Choice (Course Code / Course Name / Course Credit / Course Prerequisites / Course Availability / Course Fees)")

            else:
                unknown_choice
            
        elif choice == 3:
            print(choice)
            program_choice = input("Would you like to Add, Remove or Ammend Program")
            if program_choice.lower() == "add":
                with open('data/programs.csv', 'a') as f:
                    new_progID = input("Enter New Program ID: ")
                    new_progName = input("Enter New Program Name: ")
                    new_progCred = input("Enter Program Credit Points: ")
                    new_progCourse = input("Enter Program Courses: ")
                    writer = csv.writer(f)
                    writer.writerow([new_progID, new_progName, new_progCred, new_progCourse])
                f.close()

            elif program_choice.lower() == "remove":
                deleted_Program = input("Enter Program Name to be Removed: ")
                with open('data/programs.csv', 'r+') as f:
                    reader = csv.reader(f)
                    programs = []
                    for lines in reader:
                        if lines[0] != deleted_Program:
                            programs.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/programs_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in programs:
                        writer.writerow(i) #write the new students list into a temp csv file


                #swap the outdated csv with the updated students.csv
                os.remove('data/programs.csv')
                os.rename('data/programs_temp.csv', 'data/programs.csv') 
                
            elif program_choice.lower() == "ammend":
                # show admin what is currently in the programs.csv
                with open("data/programs.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        print(lines)
                f.close()
                
                with open("data/programs.csv", 'r') as inf, open("data/programs.csv", 'w') as outf:
                    reader = csv.reader(inf)
                    writer = csv.writer(outf)
                    ammend_programs = input("Select which Course you would like to Ammend by entering the Course Code: ")
                    for lines in reader:
                        if ammend_programs not in program_Id_list(): #if trying to ammend a student that is not already in the file
                            print("Please Enter a Program Name: ")
                        else:
                            ammend_choice = input("What would you like to change? (Program Name)")
                            if ammend_choice.lower() == "program id":
                                changed_progId = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogId_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogId_lst.append(lines)
                                        else:
                                            lines[0] = changed_progId
                                            cprogId_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogId_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                            elif ammend_choice.lower() == "program name":
                                changed_progName = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogName_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogName_lst.append(lines)
                                        else:
                                            lines[1] = changed_progName
                                            cprogName_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogName_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                            elif ammend_choice.lower() == "program credit points":
                                changed_progCred = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogCred_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogCred_lst.append(lines)
                                        else:
                                            lines[2] = changed_progCred
                                            cprogCred_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogCred_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                            elif ammend_choice.lower() == "program courses":
                                changed_progCourse = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogCourse_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogCourse_lst.append(lines)
                                        else:
                                            lines[3] = changed_progCourse 
                                            cprogCourse_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogCourse_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 
                                    
                            else:
                                print("Please Enter Valid Choice (Program Name)")
                
            else:
                unknown_choice

        elif choice == 4:
            print(choice)
            semester_choice = input("Would you like to Add, Remove or Ammend Semester")
            if semester_choice.lower() == "add":
                #remove studentadd
                print(10)
            elif semester_choice.lower() == "remove":
                #remove student
                print(11)
            elif semester_choice.lower() == "ammend":
                #ammend  studentsd
                print(12)
            else:
                unknown_choice
    
        elif choice == 5:
            s = student_object(id)
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
        else:
            return -1
    except ValueError:
        print('Invalid index')

