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

def student_program(id): # Returns True if student is in program, else, False
    with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if lines[0] == id:
                   if lines[4] == 'NA':
                       return False
            return True

def student_menu(id): # Student menu with choices and inner functions

    print()
    print('1. View your Academic History')
    print('2. View available courses') 
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
                    if i[0] in Student.student_info_list(id)[6]:
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
    print('11. Set student program.')
    print('0. Exit')
    print('=======================')
    
    try:
        choice = int(input('Please pick by index: '))
        if 0 > choice > 11:
            raise ValueError
        elif choice == 1: # Add/Remove or amend a student
            print(choice)
            student_choice = int(input("Would you like to: \n1. Add Student\n2. Remove Student \n3. Ammend Student \n0. Return to Admin Menu\n"))
            if student_choice == 0:
                return admin_menu(id)

            elif student_choice == 1:
                with open('data/students.csv', 'a', newline="\n") as f:
                    new_studentID = input("Enter Student ID: ")
                    while new_studentID in Student.studentId_list():
                        stuExists = int(input('Student ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if stuExists == 0:
                            return admin_menu(id)
                        elif stuExists == 1:
                            new_studentID = input("Enter Student ID: ")
                        else:
                            input('Please enter a Valid Index (0-1)')
                       
                    new_studentName = input("Enter Student Name: ")
                    new_studentDOB = input("Enter Student Date of Birth: ")
                    new_studentGender = input("Enter Student Gender: ")

                    writer = csv.writer(f)
                    writer.writerow([new_studentID, new_studentName, new_studentDOB, new_studentGender, "''", "[]" , "[]", "[]", 'NA'])
                f.close()
                print("\nStudent Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))
            elif student_choice == 2:
                Student.show_studentID_list()
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
                
                print("\nStudent Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif student_choice == 3:
                Student.show_studentID_list()

                ammend_student = input("Select which Student you would like to Ammend by entering the Student ID: ")

                while_counter = 3
                while ammend_student not in Semester.semesterID_list(): #if trying to ammend a student that is not already in the file
                    ammend_student = input("Please Enter a Valid Student ID: ")
                    while_counter -= 1
                    if while_counter == 0:
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Student.show_studentID_list()
                            ammend_student = input("Select which Student you would like to Ammend by entering the Student ID: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    
                    
                ammend_choice = int(input("What would you like to change?\n1. Student ID \n2. Student Name \n3. Student DOB \n4. Student Gender \n5. Student Program \n6. Student History \n7. Student Enrolled Course \n8. Student Study Plan \n9. Student Absence \n0. Return to Admin Menu \n "))
                if ammend_choice == 0:
                    return admin_menu(id)
                elif ammend_choice == 1:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')
                    
                elif ammend_choice == 2:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 3:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 4:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 5:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 6:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 7:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 8:
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
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                elif ammend_choice == 9:
                    upd_stuAbs = input("What would you like to change this Student's Absence to? ") 
                    with open("data/students.csv", 'r') as f:
                        reader = csv.reader(f)
                        upd_stuAbs_lst = []
                        for lines in reader:
                            if lines[0] != ammend_student:
                                upd_stuAbs_lst.append(lines)
                            else:
                                lines[8] = upd_stuAbs
                                upd_stuAbs_lst.append(lines)
                        
                        with open('data/students_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f)
                            for i in upd_stuAbs_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/students.csv')
                    os.rename('data/students_temp.csv', 'data/students.csv')

                else:
                    input("Please Enter Valid Index (0-9)")

                print("\nStudent Successfully Ammended!\n===========================")
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
            course_choice = int(input("Would you like to: \n1. Add Course\n2. Remove Course \n3. Ammend Course \n0. Return to Admin Menu\n"))
            if course_choice == 0:
                return admin_menu(id)
            elif course_choice == 1:
                with open('data/courses.csv', 'a') as f:
                    new_courseID = input("Enter New Course ID: ")
                    while new_courseID in Course.coursesId_list(): #makes sure that new course ID does not match with a course Id that already exists.
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

                    new_CourseCred = input("Enter Course Credit: ")
                    new_CoursePrereq = input("Enter Course Prerequisites: ")
                    new_CourseAvail = input("Enter Course Availability: ")
                    new_CourseFee = input("Enter Course Fees: ")
                    writer = csv.writer(f)
                    writer.writerow([new_courseID, new_courseName, new_CourseCred, new_CoursePrereq, new_CourseAvail, new_CourseFee])
                f.close()
                print("\nCourse Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif course_choice == 2:
                Course.show_courseID_list()

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

                print("\nCourse Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif course_choice == 3:
                Course.show_courseID_list()

                ammend_course = input("Select which Course you would like to Ammend by entering the Course Code: ")

                while_counter = 3
                while ammend_course not in Semester.semesterID_list(): #if trying to ammend a student that is not already in the file
                    ammend_course = input("Please Enter a Valid Course Code: ")
                    while_counter -= 1
                    if while_counter == 0:
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Course.show_courseID_list()
                            ammend_course = input("Select which Course you would like to Ammend by entering the Course Code: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    
                ammend_choice = int(input("What would you like to change? \n1. Course Code \n2. Course Name \n3. Course Credit \n4. Course Prerequisites \n5. Course Availability \n6. Course Fees \n0. Return to Admin Menu \n"))
                
                if ammend_choice == 0:
                    return admin_menu(id)

                elif ammend_choice == 1:
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
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 2:
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
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 3:
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
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 4:
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
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 5:
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
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                elif ammend_choice == 6:
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
                    f.close()
                    os.remove('data/courses.csv')
                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                        
                else:
                    input("Please Enter Valid Index (0-6)")

                print("\nCourse Successfully Ammended!\n===========================")
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
            program_choice = int(input("Would you like to: \n1. Add Program\n2. Remove Program \n3. Ammend Program \n0. Return to Admin Menu\n"))
            if program_choice == 0:
                return admin_menu(id)
            if program_choice == 1:
                with open('data/programs.csv', 'a') as f:
                    new_progID = input("Enter New Program ID: ")
                    while new_progID in Program.programId_list(): #makes sure that new program ID does not match with a program Id that already exists.
                        progIdExists = int(input('Program ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if progIdExists == 0:
                            return admin_menu(id)
                        elif progIdExists == 1:
                            new_progID = input("Enter New Program ID: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_progName = input("Enter New Program Name: ")
                    while new_progName.lower() in Program.programId_list(): #makes sure that new program ID does not match with a program Id that already exists.
                        progNameExists = int(input('Program Name already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if progNameExists == 0:
                            return admin_menu(id)
                        elif progNameExists == 1:
                            new_progName = input("Enter New Program Name: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_progCred = input("Enter Program Credit Points: ")
                    new_progCourse = input("Enter Program Courses: ")
                    writer = csv.writer(f)
                    writer.writerow([new_progID, new_progName, new_progCred, new_progCourse])
                f.close()
                print("\nProgram Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif program_choice == 2:
                Program.show_programsID_list()

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

                print("\nProgram Successfully Removed!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif program_choice == 3:
                Program.show_programsID_list()
                ammend_programs = input("Select which Program you would like to Ammend by entering the Program Code: ")
                
                while_counter = 3
                while ammend_programs not in Semester.semesterID_list(): #if trying to ammend a student that is not already in the file
                    ammend_programs = input("Please Enter a Valid Program Code: ")
                    while_counter -= 1
                    if while_counter == 0:
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Program.show_programsID_list()
                            ammend_programs = input("Select which Program you would like to Ammend by entering the Program Code: ")
                            while_counter = 3
                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    
                ammend_choice = int(input("What would you like to change? \n1. Program ID \n2. Program Name \n3. Program Credit Points \n4. Program Courses \n5. Program Elective Courses \n0. Return to Admin Menu \n)"))
                if ammend_choice ==0:
                    return admin_menu(id)
                elif ammend_choice == 1:
                    changed_progId = input("What would you like to change the Program ID to? ") 
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
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                elif ammend_choice == 2:
                    changed_progName = input("What would you like to change the Program Name to? ") 
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
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                elif ammend_choice == 3:
                    changed_progCred = input("What would you like to change the Program Credit Points to? ") 
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
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv')  

                elif ammend_choice == 4:
                    changed_progCourse = input("What would you like to change the Program Courses to? ") 
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
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                elif ammend_choice == 5:
                    changed_progElecCourse = input("What would you like to change the Program Courses to? ") 
                    with open("data/programs.csv", 'r') as f:
                        reader = csv.reader(f)
                        cprogElecCourse_lst = []
                        for lines in reader:
                            if lines[0] != ammend_programs:
                                cprogElecCourse_lst.append(lines)
                            else:
                                lines[4] = changed_progElecCourse 
                                cprogElecCourse_lst.append(lines)
                        
                        with open('data/programs_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f)
                            for i in cprogElecCourse_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/programs.csv')
                    os.rename('data/programs_temp.csv', 'data/programs.csv') 
                        
                else:
                    input("Please Enter Valid Index (0-5)")

                print("\nProgram Successfully Ammended!\n===========================")
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
            semester_choice = int(input("Would you like to: \n1. Add Semester\n2. Remove Semester \n3. Ammend Semester \n0. Return to Admin Menu\n"))
            if semester_choice == 0:
                return admin_menu(id)
            if semester_choice == 1:
                with open('data/semesters.csv', 'a') as f:
                    new_semProg = input("Enter New Semester Program Code")
                    new_semID = input("Enter New Semester ID: ")
                    while new_semID in Semester.semesterID_list:
                        semIdExists = int(input('Semester ID already exists. Would you like to \n1. Try Again \n0. Return to Admin Menu \n'))
                        if semIdExists == 0:
                            return admin_menu(id)
                        elif semIdExists == 1:
                            new_semID = input("Enter New Semester ID: ")
                        else:
                            input('Please enter a Valid Index (0-1)')

                    new_semOffer = input("Enter New Semester Offers: ")
                    new_semMaxStu = input("Enter Max Students for Semester: ")
                    new_semCurStu = input("Enter Current Enrolled Students for Semester: ")
                    writer = csv.writer(f)
                    writer.writerow([new_semProg, new_semID, new_semOffer, new_semMaxStu, new_semCurStu])
                f.close()
                print("\nSemester Successfully Added!\n===========================")
                close_input = int(input("What would you like to do next?:\n1. Exit\n0. Return to Admin Menu\n"))
                if close_input == 0:
                    return admin_menu(id)
                elif close_input == 1:
                    return True
                else:
                    close_input = int(input("Please enter a Valid Index (0-1)"))

            elif semester_choice == 2:
                Semester.show_semesterID_list()

                deleted_semester = input("Enter Semester ID to be Removed: ")
                with open('data/semesters.csv', 'r+') as f:
                    reader = csv.reader(f)
                    semesters = []
                    for lines in reader:
                        if lines[0] != deleted_semester:
                            semesters.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/semesters_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in semesters:
                        writer.writerow(i) #write the new students list into a temp csv file


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

            elif semester_choice == 3:
                Semester.show_semesterID_list()
                
                ammend_semester = input("Select which Semester you would like to Ammend by entering the Semester ID: ")
                
                while_counter = 3
                while ammend_semester not in Semester.semesterID_list(): #if trying to ammend a student that is not already in the file
                    ammend_semester = input("Please Enter a Valid Semeseter ID: ")
                    while_counter -= 1
                    if while_counter == 0:
                        cont = int(input("Would you like to :\n1. Try Again\n2. Exit\n0. Return to Admin Menu\n"))
                        if cont == 0:
                            return admin_menu(id)
                        elif cont == 1:
                            Semester.show_semesterID_list()
                            ammend_semester = input("Select which Semester you would like to Ammend by entering the Semester ID: ")
                            while_counter = 3

                        elif cont ==2:
                            return True
                        else:
                            cont = int(input("Please enter a Valid Index (0-2)"))
                    

                ammend_choice = int(input("What would you like to change?\n1. Semester ID \n2. Semester Offers \n3. Semester Max Students \n4. Semester Current Students\n0. Return to Admin Menu \n"))
                if ammend_choice == 0:
                    return admin_menu(id)
                elif ammend_choice == 1:
                    changed_semId = input("What would you like to change the Semester ID to? ") 
                    with open("data/semesters.csv", 'r') as f:
                        reader = csv.reader(f)
                        csemId_lst = []
                        for lines in reader:
                            if lines[0] != ammend_semester:
                                csemId_lst.append(lines)
                            else:
                                lines[0] = changed_semId
                                csemId_lst.append(lines)
                        
                        with open('data/semesters_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f)
                            for i in csemId_lst:
                                writer.writerow(i) #write the new semester list into a temp csv file
                    f.close()
                    os.remove('data/semesters.csv')
                    os.rename('data/semesters_temp.csv', 'data/semesters.csv') 

                elif ammend_choice == 2:
                    changed_semOff = input("What would you like to change the Semester Offers to? ") 
                    with open("data/semesters.csv", 'r') as f:
                        reader = csv.reader(f)
                        csemOff_lst = []
                        for lines in reader:
                            if lines[0] != ammend_semester:
                                csemOff_lst.append(lines)
                            else:
                                lines[1] = changed_semOff
                                csemOff_lst.append(lines)
                        
                        with open('data/semesters_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f)
                            for i in csemOff_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/semesters.csv')
                    os.rename('data/semesters_temp.csv', 'data/semesters.csv') 

                elif ammend_choice == 3:
                    changed_maxStu = input("What would you like to change the Semester Max Students to? ") 
                    with open("data/semesters.csv", 'r') as f:
                        reader = csv.reader(f)
                        cmaxStu_lst = []
                        for lines in reader:
                            if lines[0] != ammend_semester:
                                cmaxStu_lst.append(lines)
                            else:
                                lines[2] = changed_maxStu
                                cmaxStu_lst.append(lines)
                        
                        with open('data/semesters_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f)
                            for i in cmaxStu_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/semesters.csv')
                    os.rename('data/semesters_temp.csv', 'data/semesters.csv') 

                elif ammend_choice == 4:
                    changed_curStu = input("What would you like to change the Semester Current Students to? ") 
                    with open("data/semesters.csv", 'r') as f:
                        reader = csv.reader(f)
                        ccurStu_lst = []
                        for lines in reader:
                            if lines[0] != ammend_semester:
                                ccurStu_lst.append(lines)
                            else:
                                lines[3] = changed_curStu 
                                ccurStu_lst.append(lines)
                        
                        with open('data/semesters_temp.csv', 'w+', newline='') as f:
                            writer = csv.writer(f)
                            for i in ccurStu_lst:
                                writer.writerow(i) #write the new students list into a temp csv file
                    f.close()
                    os.remove('data/semesters.csv')
                    os.rename('data/semesters_temp.csv', 'data/semesters.csv') 

                else:
                    input("Please Enter Valid Index (0-4)")

                print("\nSemester Successfully Ammended!\n===========================")
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
        elif choice == 11: # Set a students program
            print('You can exit anytim by entering 0')
            print()
            stu_id_prog = str(input('Please enter the id of the student: '))
            if stu_id_prog == str(0):
                return admin_menu(id)
            if Student.open_students_for_id(stu_id_prog) == True:
                program_set = str(input('Please enter the program code to set to: '))
                if program_set == str(0):
                    return admin_menu(id)
                if Program.open_program_by_id(program_set) == True:
                    #check if student already has program, ask if override which resets study plan.
                    #add to student program
                    #give study plan of program to student
                    pass
                else:
                    print('Invalid program')
                    return admin_menu(id)
            else:
                print('Invalid student')
                return admin_menu(id)
        else:
            return -1
    except ValueError:
        print('Invalid index')

