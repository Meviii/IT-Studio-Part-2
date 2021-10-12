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
        student = []
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                return False

def create_student_object(id):
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        #student_lst = []
        for lines in reader:
            if lines[0] == id:
                student_lst = [i.strip() for i in lines]
                #student_lst.append(lines)
            else:
                print('Error')
        #student = Student([i for i in student_lst])
        return student_lst
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
                student = Student(create_student_object(id)[0], create_student_object(id)[1], create_student_object(id)[3],
                create_student_object(id)[4], create_student_object(id)[5], create_student_object(id)[6], create_student_object(id)[7])
                
                print(f'Welcome {student.name} \n')
                student_menu(id)
            else:
                print('Incorrect Student User')
        else:
            raise ValueError
    except ValueError:
        print('Incorrect selection')

def student_menu(id):
    print('     *STUDENT MENU*      ')
    
    print('1. View your Academic History')
    print('2. View available courses')
    print('3. Enrol/UnEnrol in an Offering')
    print('4. View your Academic History')
    print('5. View your Academic History')
    print('0. Exit')
    print('=========================')
    try:
        input = int('Please pick by index:')
        if 0 > input > 5:
            raise ValueError
        elif input == 1:
            print(input)
        elif input == 2:
            print(input)
        elif input == 3:
            print(input)
        elif input == 4:
            print(input)
        elif input == 5:
            print(input)
        else:
            print('Error')
    except ValueError:
        print('Invalid index') 
        
def admin_menu(id):
    print('     *ADMIN MENU*      ')
    print('=======================')