from _typeshed import WriteableBuffer
import ast
import Program as prg
from Course import Course
import Semester as sem
import csv
from User import User, Student, Admin
import os

def check_prereqs(id, course):
    with open('data/courses.csv', 'r') as cf:
        cfreader = csv.reader(cf)
        courses = []
        course_prereqs = []
        for lines in cfreader:
            if lines[0] == course:
                courses.append(lines[3]) #appends prereqs of course 
        for i in courses:
            course_prereqs = ast.literal_eval(i) #makes prereqs of course a list
        
        if courses is []:
            print('empty')
            return True


    with open('data/students.csv', 'r') as sf:
        sfreader = csv.reader(sf)
        stu_history = []
        temp = []

        for lines in sfreader:
            if str(lines[0]) == str(id):
                temp.append(lines[5])
                
        for i in temp:
            stu_history = ast.literal_eval(i) # makes student academic history a list
        
        course_name_history = []
        for i in stu_history:
            course_name_history.append(i[0]) # makes a list for only names of courses in academic history

        z = set(course_name_history).intersection(set(course_prereqs)) # Set of intersection of course_prereqs and course_name
        
        if z is None:
            return False
        elif not z is None:
            if len(course_prereqs) == len(z):
                for i in stu_history:
                    for x in course_prereqs:
                        if str(i[0]) == str(x):
                            if i[1] >= 50:
                                return True
                            else:
                                return False
            else:
                print('len false')
                return False

def add_course(code, title, credits, sem, fee, prereq=[]): # Adds a course to courses.csv
    final = str(str(code) +','+ str(title) +','+ str(credits) +',' + '"'+str(prereq)+'"'+','+ str(sem) +','+ str(fee))
        
    with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)

        writer.writerow(final.split(','))
        writer.writerows(reader)

    os.remove('data/courses.csv')
    os.rename('data/courses_temp.csv', 'data/courses.csv')

def add_prereq(code, prereq): # Adds a prereq for a course in courses.csv
    with open('data/courses.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        prereq_courses = []
        for lines in reader:
            if str(lines[0]) == str(code):
                courses = [i.strip() for i in lines]
                if not prereq in lines[3]:
                    prereq_courses = ast.literal_eval(lines[3])
                    prereq_courses.append(str(prereq))
                else:
                    print('Already a prereq')
                    #return admin_menu(id)
                    return False
                    
        final = str(str(courses[0]) +','+ str(courses[1]) +','+ str(courses[2]) +',' + '"'+str(prereq_courses)+'"'+','+ str(courses[4]) +','+ str(courses[5]))
        f.close()

    with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
        for lines in reader:
            if lines[0] == str(code):
                writer.writerow(final.split(','))
                break
            else:
                writer.writerow(lines)
        writer.writerows(reader)

    os.remove('data/courses.csv')
    os.rename('data/courses_temp.csv', 'data/courses.csv')

def open_admins_for_id(id): # Returns if id exists in admins.csv
    with open('data/admins.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                continue
        f.close()
        return False

def admin_info_list(id): # Returns all info of a specific line by id from admins.csv
    with open('data/admins.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if lines[0] == id:
                admin_lst = [i.strip() for i in lines]
            else:
                continue
        f.close()
        return admin_lst

def open_students_for_id(id): # Returns if id exists in students.csv
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                continue
        f.close()
        return False

def student_info_list(id): # Returns all info of a specific line by id from students.csv
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if lines[0] == id:
                student_lst = [i.strip() for i in lines]
            else:
                continue
        f.close()
        return student_lst

def admin_object(id): # Creates an Admin object using per info from admin_info_list(id)
    admin = Admin(admin_info_list(id)[0], admin_info_list(id)[1], admin_info_list(id)[2],
               admin_info_list(id)[3])
    return admin

def student_object(id): # Creates an Student object using per info from student_info_list(id)
    student = Student(student_info_list(id)[0], student_info_list(id)[1], student_info_list(id)[2],
               student_info_list(id)[3], student_info_list(id)[4], student_info_list(id)[5], student_info_list(id)[6])
    return student

def courses_name_list(): # Returns only course codes from all courses in courses.csv
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f)
        course_name_lst = []
        for lines in reader:
            course_name_lst.append(lines[0])
    f.close()
    return course_name_lst

def courses_list(): # Returns all info from each line in courses.csv (Sorted)
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f)
        course_lst = []
        for lines in reader:
            course_lst.append(lines)
    f.close()
    return sorted(course_lst)

def add_student_course(id, stu_course): # Adds a course to a student line by id in students.csv

    with open('data/students.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        student = []
        courses = []
        for lines in reader:
            if str(lines[0]) == str(id):
                student = [i.strip() for i in lines]
                if not stu_course in lines[6]:
                    courses = ast.literal_eval(lines[6])
                    courses.append(str(stu_course))
                else:
                    print('Already enrolled')
                    return student_menu(id)
        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses)+'"'+','+ '"' +str(student[7])+'"')
        f.close()

    with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
        for lines in reader:
            if lines[0] == id:
                writer.writerow(final.split(','))
                break
            else:
                writer.writerow(lines)
        writer.writerows(reader)

    os.remove('data/students.csv')
    os.rename('data/students_temp.csv', 'data/students.csv')

def remove_course(id, stu_course): # Removes a course to a student line by id in students.csv

    with open('data/students.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        student = []
        for lines in reader:
            if lines[0] == id:
                student = [i.strip() for i in lines]
                if stu_course in lines[6]:
                    courses = ast.literal_eval(lines[6])
        courses.remove(stu_course)
        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses[6])+'"'+','+ '"' +str(student[7])+'"')
        f.close()

    with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
        for lines in reader:
            if lines[0] == id:
                writer.writerow(final.split(','))
                break
            else:
                writer.writerow(lines)
        writer.writerows(reader)

    os.remove('data/students.csv')
    os.rename('data/students_temp.csv', 'data/students.csv')

def remove_program(id): # Resets program of student to '' in students.csv. Cancels program

    with open('data/students.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        student = []
        for lines in reader:
            if lines[0] == id:
                student = [i.strip() for i in lines]
                if not lines[4] == '':
                    program = ''
                else:
                    print('You are not a part of any program')
                    return student_menu_option(id)
        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(program)+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"')
        f.close()

    with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
        for lines in reader:
            if lines[0] == id:
                writer.writerow(final.split(','))
                break
            else:
                writer.writerow(lines)
        writer.writerows(reader)

    os.remove('data/students.csv')
    os.rename('data/students_temp.csv', 'data/students.csv')

def login(): # Login function for Admin or Student login BY ID
    try:
        login_type = str(input('Login as Admin or Student? ')).lower()

        if login_type == 'Admin'.lower(): # Needs implementation
            id = str(input('Please enter your Admin ID: '))
            print('==================================')
            if open_admins_for_id(id) == True:
                admin = admin_object(id)
                print(f'Welcome {admin.name}\n')
                admin_menu(id)
            else:
                print('Incorrect Admin ID')

        elif login_type == 'Student'.lower():
            id = str(input('Please enter your Student ID: '))
            
            print('==================================')
            if open_students_for_id(id) == True:
                student = student_object(id)

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

def student_menu(id): # Student menu with choices and inner functions
    print('     *STUDENT MENU*      ')
    print()
    print('1. View your Academic History')
    print('2. View available courses')
    print('3. View and enrol in an offering')
    print('4. Un-enrol from an offering')
    print('5. Get all information')
    print('6. Update your Information')
    print('7. Fees')
    print('8. Cancel Program')
    print('0. Exit')
    print('==================================')

    try:
        s = student_object(id)

        choice = int(input('Please pick by index: '))
        res = set(ast.literal_eval(s.get_curr_enrol()))
        all_courses = set(courses_name_list())
        stu_courses = sorted(res.intersection(all_courses))
        s.set_curr_enrol(stu_courses)

        if 0 > choice > 8:
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
            print()
            print()
            student_menu_option(id)
        elif choice == 3: # View current enrollments, add course

            if not s.get_curr_enrol() is None:
                print('You are currently enrolled in: \n')
                for i in courses_list():
                    if i[0] in s.get_curr_enrol():
                        print(f'{i[0]}: {i[1]}')
                print()
                selection = str(input('Would you like to add a course? Y/N \n'))
                if selection.lower() == 'n':
                    student_menu_option(id)
                elif selection.lower() == 'y':
                    count = 1
                    for i in courses_list():
                        print(f'{count}. {i[0]}: {i[1]}, Credit: {i[2]}\n')
                        count += 1
                    selection = int(input('Enter the index you would like to add. 0 to exit\n'))
                    if selection == 0:
                        return student_menu(id)
                    else:
                        curr_enrolment = s.get_curr_enrol()
                        for x, value in enumerate(sorted(courses_list()),1):
                            if int(selection) == int(x):
                                if check_prereqs(id, value[0]) == True:
                                    for i in curr_enrolment:
                                        if str(i) != str(value[0]):
                                            print(f'{value[0]} added.')
                                            add_student_course(id, value[0])
                                            return student_menu_option(id)
                                        else:
                                            print('Already Enrolled\n')
                                            return student_menu(id)
                                elif check_prereqs(id, value[0]) == False:
                                    print('You do not meet the requirments\n')
                                    return student_menu(id)
                                else:
                                    print('error')
            elif s.get_curr_enrol() is None: # need to add a way to add course into student and possibly need if statement for Sem
                selection = int(input('Enter the index you would like to add. 0 to exit \n'))
                count = 1
                for i in courses_list():
                    print(f'{count}. {i[0]}: {i[1]}, Credit: {i[2]}\n')
                    count += 1
                if selection == 0:
                    return student_menu(id)
                else:
                    for x, value in enumerate(sorted(courses_list()),1):
                        if selection == int(x):
                            curr_enrolment = s.get_curr_enrol()
                            if check_prereqs(id, value) == True:
                                for i in curr_enrolment:
                                    if str(i) != str(value[0]):
                                        print(f'{value[0]} added.')
                                        add_student_course(id, value[0])
                                        student_menu_option(id)
                                    else:
                                        print('Already Enrolled\n')
                                        student_menu(id)
                            elif check_prereqs(id, value) == False:
                                    print('You do not meet the requirments\n')
                                    student_menu(id)
        elif choice == 4: # View current enrollments, drop course
            print('Enrolled courses: \n')
            count = 1
            for i in courses_list():
                if i[0] in s.get_curr_enrol():
                    print(f'{count}. {i[0]}: {i[1]}')
                    count += 1
            selection = int(input(("Enter the index you would like to drop. 0 to exit \n")))
            for x, value in enumerate(sorted(stu_courses),1):
                if selection == int(x):
                    print(f'{value} dropped.')
                    curr_enrolment = s.get_curr_enrol()
                    for i in curr_enrolment:
                        if str(i) == str(value):
                            curr_enrolment.remove(i)
                            remove_course(id, i)
                            break
                    student_menu_option(id)
                elif selection == 0:
                    return student_menu(id)
                else:
                    print('Error')
                    return False
                
            print('You are corrently not enrolled into any courses')
            print()            
        elif choice == 5: # View all personal information
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
            print()
            student_menu_option(id)
        elif choice == 6: # Update personal information
            update_sel = str(input('Which detail would you like to update?'))
            print('Please enter one of the following: ')
            print('1. Name\n2. Birth\n3. Gender')
            student_menu_option(id)
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
        elif choice == 8: # Cancel program
            print(f'You are currently a student of {s.get_program()}. Do you want to cancel this? Y/N')
            program_update = str(input())
            if program_update.lower() == 'y':
                s.set_program('')
                # read line of id
                # if s.getprogram in line:
                # edit the program to ''
                with open('data/students.csv', 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        if lines[0] == id:
                            #fix
                            pass
                        else:
                            continue
                    f.close()
                print(f'You have been removed from the program.\n')
                student_menu_option(id)
            elif program_update.lower() == 'n':
                return student_menu(id)
            else:
                raise ValueError
        else:
            return -1
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
<<<<<<< HEAD
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
                        if ammend_student != lines[0]: #if trying to ammend a student that is not already in the file
                            print("Please Enter a Valid Student ID: ")
                        else:
                            ammend_choice = input("What would you like to change? (Student ID / Student Name / Student DOB / Student Gender / Student Program / Student History / Student Enrolled Course / Student Study Plan)")
                            if ammend_choice.lower() == "student id":
                                print(1)
                            elif ammend_choice.lower() == "student name":
                                print(2)
                            elif ammend_choice.lower() == "student dob":
                                print(3)
                            elif ammend_choice.lower() == "student gender":
                                print(4)
                            elif ammend_choice.lower() == "student program":
                                print(5)
                            elif ammend_choice.lower() == "student history":
                                print(6)
                            elif ammend_choice.lower() == "student enrolled course":
                                print(7)
                            elif ammend_choice.lower() == "student study plan":
                                print(8)
                            else:
                                print("Please Enter Valid Choice (Student ID / Student Name / Student DOB / Student Gender / Student Program / Student History / Student Enrolled Course / Student Study Plan)")


=======
                    new_studentCourse = input("Enter Student Course: ")
                    writer = csv.writer(f)
                    writer.writerow([new_studentID, new_studentName, new_studentDOB, new_studentGender, new_studentCourse, [], []])
                f.close()
            elif student_choice.lower() == "remove":
                deleted_studentID = input("Enter Student ID to be Removed: ")
                with open('data/student.csv', 'r+') as f:
                    reader = csv.reader(f)
                    final = ''
                    students = []
                    for lines in reader:
                        for i in lines:
                            if i[0] != deleted_studentID:
                                students.append(lines)

                    final = ",".join(str(students[e]) for e in range(len(students)))
                f.close()

                with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
                    reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
                    writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
                    for lines in reader:
                        if lines[0] == id:
                            writer.writerow(final.split(','))
                            break
                        else:
                            writer.writerow(lines)
                    writer.writerows(reader)

                os.remove('data/students.csv')
                os.rename('data/students_temp.csv', 'data/students.csv')
                #remove student
            elif student_choice.lower() == "ammend":
                #ammend student
                print(3)
>>>>>>> 51319a548611d8dd4f54734b3de072fd6767f8a2
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
<<<<<<< HEAD
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

                with open("data/courses.csv", 'r') as inf, open("data/courses.csv", 'w') as outf:
                    reader = csv.reader(inf)
                    writer = csv.writer(outf)
                    ammend_course = input("Select which Course you would like to Ammend by entering the Course Code: ")
                    for lines in reader:
                        if ammend_course != lines[0]: #if trying to ammend a student that is not already in the file
                            print("Please Enter a Valid Student ID: ")
                        else:
                            ammend_choice = input("What would you like to change? (Course Code / Course Name / Course Credit / Course Prerequisites / Course Availability / Course Fees)")
                            if ammend_choice.lower() == "course code":
                                print(1)
                            elif ammend_choice.lower() == "course name":
                                print(2)
                            elif ammend_choice.lower() == "course credit":
                                print(3)
                            elif ammend_choice.lower() == "course prerequisite":
                                print(4)
                            elif ammend_choice.lower() == "course availability":
                                print(5)
                            elif ammend_choice.lower() == "course fees":
                                print(6)
                            else:
                                print("Please Enter Valid Choice (Course Code / Course Name / Course Credit / Course Prerequisites / Course Availability / Course Fees)")

=======
                    final = ''
                    courses = []
                    for lines in reader:
                        for i in lines:
                            if i[0] != deleted_course:
                                courses.append(lines)

                    final = ",".join(str(courses[e]) for e in range(len(courses)))
                f.close()

                with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
                    reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
                    writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
                    for lines in reader:
                        if lines[0] == id:
                            writer.writerow(final.split(','))
                            break
                        else:
                            writer.writerow(lines)
                    writer.writerows(reader)

                os.remove('data/courses.csv')
                os.rename('data/courses_temp.csv', 'data/courses.csv')
            elif course_choice.lower() == "ammend":
                print(3)
>>>>>>> 51319a548611d8dd4f54734b3de072fd6767f8a2
            else:
                unknown_choice
            
        elif choice == 3:
            print(choice)
            program_choice = input("Would you like to Add, Remove or Ammend Program")
            if program_choice.lower() == "add":
                with open('data/students.csv', 'a') as f:
                    new_program = input("Enter New Program Name: ")
                    writer = csv.writer(f)
                    writer.writerow(new_program)
                f.close()
            elif program_choice.lower() == "remove":
                deleted_Program = input("Enter Program Name to be Removed: ")
                with open('data/programs.csv', 'r+') as f:
                    reader = csv.reader(f)
<<<<<<< HEAD
                    programs = []
                    for lines in reader:
                        if lines[0] != deleted_Program:
                            programs.append(lines) #appends programs to a list, excluding the specified one 
                f.close()

                with open('data/programs_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in programs:
                        writer.writerow(i) #write the new programs list into a temp csv file

=======
                    final = ''
                    programs = []
                    for lines in reader:
                        for i in lines:
                            if i[0] != deleted_Program:
                                programs.append(lines)

                    final = ",".join(str(programs[e]) for e in range(len(programs)))
                f.close()

                with open('data/programs.csv', 'r') as inf, open('data/programs_temp.csv', 'w+', newline='') as outf:
                    reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
                    writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
                    for lines in reader:
                        if lines[0] == id:
                            writer.writerow(final.split(','))
                            break
                        else:
                            writer.writerow(lines)
                    writer.writerows(reader)
>>>>>>> 51319a548611d8dd4f54734b3de072fd6767f8a2

                os.remove('data/programs.csv')
                os.rename('data/programs_temp.csv', 'data/programs.csv')
            elif program_choice.lower() == "ammend":
<<<<<<< HEAD
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
                        if ammend_programs != lines: #if trying to ammend a student that is not already in the file
                            print("Please Enter a Program Name: ")
                        else:
                            ammend_choice = input("What would you like to change? (Program Name)")
                            if ammend_choice.lower() == "program name":
                                print(1)
                            else:
                                print("Please Enter Valid Choice (Program Name)")
                
=======
                #ammend student
                print(9)
>>>>>>> 51319a548611d8dd4f54734b3de072fd6767f8a2
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

