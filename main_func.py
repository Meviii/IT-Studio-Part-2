import ast
import Program as prg
from Course import Course
import Semester as sem
import csv
from User import User, Student, Admin

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
    return course_lst

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
                student_menu(id)
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
        choice = int(input('Please pick by index: '))
        s = student_object(id)
        res = set(ast.literal_eval(s.get_curr_enrol()))
        all_courses = set(courses_name_list())
        stu_courses = res.intersection(all_courses)

        if 0 > choice > 8:
            raise ValueError
        elif choice == 1:
            s.get_acad_history(id)
            student_menu_option()
        elif choice == 2:
            print('All available courses for you are: ')
            print()
            student_menu_option(id)
        elif choice == 3: # possible option to add more courses
                if not s.get_curr_enrol() is None:
                    print('You are currently enrolled in: \n')
                    for i in courses_list():
                        if i[0] in stu_courses:
                            print(f'{i[0]}: {i[1]}')
                    print()
                    student_menu_option(id)
                elif s.get_curr_enrol() is None: # need to add a way to add course into student and possibly need if statement for Sem
                    print(f'Please pick the courses you would like to enrol into: ')
                    for i in courses_list():
                        print(f'{i[0]}: {i[1]}, Sem: {i[4]}, Credit: {i[2]}, Pre-req: {i[3]}\n')
        elif choice == 4:
            print('Please pick the course you would like to drop: \n')
            for count, i in enumerate(courses_list(), 1):
                if i[0] in stu_courses:
                    print(f'{count}. {i[0]}: {i[1]}')
            print()
            print("Enter the index('s) you would like to drop. 0 to exit")
            # selection input
            # save input(1 2 3) into list
            # if selection > len(stu_courses) <= 0 : false, else:
            # for list(1 2 3), if count enum(stu_courses, 1) == list[i], remove from student object if i == coursecode
            sel_list = []
            for i in range(len(stu_courses)):
                selection = int(input(''))
                if not selection in range(len(stu_courses)+1):
                    print('Selection not in list')
                elif selection in range(len(stu_courses)+1):
                    sel_list.append(selection)
                else:
                    continue
        elif choice == 5:
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
            student_menu_option(id)
        elif choice == 6:
            print(choice)
            student_menu_option(id)
        elif choice == 7:
            print()
            print('The fees for your current enrollment is: \n')
            if not s.get_curr_enrol() is None:
                fees_total = 0
                for i in courses_list():
                    if i[0] in stu_courses:
                        print(f'{i[0]}: {i[1]} Fee: ${i[5]}')
                        fees_total += int(i[5])
                print()
                print(f'Total: ${fees_total}')
                print()
                student_menu_option(id)
            else:
                return student_menu(id)
        elif choice == 8:
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