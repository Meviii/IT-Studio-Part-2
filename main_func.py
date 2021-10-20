import ast
import Program as prg
from Course import Course
import Semester as sem
import csv
from User import User, Student, Admin
import os

def open_admins_for_id(id):
    with open('data/admins.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                continue
        f.close()
        return False

def admin_info_list(id):
    with open('data/admins.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if lines[0] == id:
                student_lst = [i.strip() for i in lines]
            else:
                continue
        f.close()
        return student_lst

def open_students_for_id(id):
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                continue
        f.close()
        return False

def student_info_list(id):
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if lines[0] == id:
                student_lst = [i.strip() for i in lines]
            else:
                continue
        f.close()
        return student_lst

def admin_object(id):
    admin = Admin(admin_info_list(id)[0], admin_info_list(id)[1], admin_info_list(id)[2],
               admin_info_list(id)[3])
    return admin

def student_object(id):
    student = Student(student_info_list(id)[0], student_info_list(id)[1], student_info_list(id)[2],
               student_info_list(id)[3], student_info_list(id)[4], student_info_list(id)[5], student_info_list(id)[6])
    return student

def courses_name_list():
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f)
        course_name_lst = []
        for lines in reader:
            course_name_lst.append(lines[0])
    f.close()
    return course_name_lst

def courses_list():
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f)
        course_lst = []
        for lines in reader:
            course_lst.append(lines)
    f.close()
    return sorted(course_lst)

def add_student_course(id, stu_course):

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

def remove_course(id, stu_course):

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

def remove_program(id):

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

def login():
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

def student_information():
    return False

def student_menu_option(id):
    return_main = str(input('Return to main menu? Y/N \n'))
    if return_main.lower() == 'y':
        return student_menu(id)
    else:
        return False

def student_menu(id):
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
                    selection = str(input('Would you like to add a course? Y/N '))
                    if selection.lower() == 'n':
                        student_menu_option(id)
                    elif selection.lower() == 'y':
                        count = 1
                        for i in courses_list():
                            print(f'{count}. {i[0]}: {i[1]}, Sem: {i[4]}, Credit: {i[2]}, Pre-req: {i[3]}\n')
                            count += 1
                        selection = int(input('Enter the index you would like to add. 0 to exit\n'))
                        if selection == 0:
                            return student_menu(id)
                        else:
                            for x, value in enumerate(sorted(courses_list()),1):
                                if selection == int(x):
                                    curr_enrolment = s.get_curr_enrol()
                                    for i in curr_enrolment:
                                        if str(i) != str(value[0]):
                                            print(f'{value[0]} added.')
                                            add_student_course(id, value[0])
                                            return student_menu_option(id)
                                        else:
                                            print('Already Enrolled\n')
                                            return student_menu(id)
                elif s.get_curr_enrol() is None: # need to add a way to add course into student and possibly need if statement for Sem
                    selection = int(input('Enter the index you would like to add. 0 to exit '))
                    count = 1
                    for i in courses_list():
                        print(f'{count}. {i[0]}: {i[1]}, Sem: {i[4]}, Credit: {i[2]}, Pre-req: {i[3]}\n')
                        count += 1
                    if selection == 0:
                        return student_menu(id)
                    else:
                        for x, value in enumerate(sorted(courses_list()),1):
                            if selection == int(x):
                                curr_enrolment = s.get_curr_enrol()
                                for i in curr_enrolment:
                                    if str(i) != str(value[0]):
                                        print(f'{value[0]} added.')
                                        add_student_course(id, value[0])
                                        return student_menu_option(id)
                                    else:
                                        print('Already Enrolled\n')
                                        return student_menu(id)
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

def admin_menu(id):

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
        if 0 > choice > 5:
            raise ValueError
        elif choice == 1:
            print(choice)
        elif choice == 2:
            print(choice)
        elif choice == 3:
            print(choice)
        elif choice == 4:
            s = student_object(id)
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
        elif choice == 5:
            print(choice)
        else:
            return -1
    except ValueError:
        print('Invalid index') 
