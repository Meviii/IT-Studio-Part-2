import ast
import Program as prg
import Course as crs
import Semester as sem
import csv
from User import User, Student, Admin

# def student_list():
#         with open('data/students.csv') as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',',)
#             line_count = 0
#             for row in csv_reader:
#                 print(f'{row[0]} is a student of {row[1]}')
#                 line_count += 1
#         print('Done.')


def open_students_for_id(id):
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)

        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                return False
    f.close()

def student_info_list(id):
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        #student_lst = []
        for lines in reader:
            if lines[0] == id:
                student_lst = [i.strip() for i in lines]
            else:
                print('Error')
        f.close()
        return student_lst
        
def student_object(id):
    
    student = Student(student_info_list(id)[0], student_info_list(id)[1], student_info_list(id)[2],
               student_info_list(id)[3], student_info_list(id)[4], student_info_list(id)[5], student_info_list(id)[6])
    return student

def login():
    try:
    
        login_type = str(input('Login as Admin or Student? ')).lower()

        if login_type == 'Admin'.lower(): # Needs implementation
            id = str(input('Please enter your Admin ID: '))
            print('==================================')
            if open_students_for_id(id) == True:
                print('Welcome', '\n')
                admin_menu(id)
            else:
                print('User does not exist')

        elif login_type == 'Student'.lower():
            id = str(input('Please enter your Student ID: '))
            
            print('==================================')
            if open_students_for_id(id):
                student = student_object(id)

                print(f'        Welcome {student.name} \n')
                student_menu(id)
            else:
                print('Incorrect Student User')
        else:
            raise ValueError
    except ValueError:
        print('Incorrect selection')
        return False

def student_information():
    return False

def student_menu(id):
    print('     *STUDENT MENU*      ')
    
    print('1. View your Academic History')
    print('2. View available courses')
    print('3. Enrol/UnEnrol in an Offering')
    print('4. Get all information')
    print('5. View your Academic History')
    print('0. Exit')
    print('==================================')
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

def admin_menu(id):
    print('     *ADMIN MENU*      ')
    print('=======================')