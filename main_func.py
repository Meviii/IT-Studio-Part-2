import Program as prg
import Course as crs
import Semester as sem
import Student as stu
import Admin as adm
import csv

stu1 = stu.Student(123, 'Tom Tommy', '20/02/2000', 'Male', 'Program1', 'Acad history', 'some courses', 'b312')

def student_list():
        with open('data/students.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',',)
            line_count = 0
            for row in csv_reader:
                print(f'{row[0]} is a student of {row[1]}')
                line_count += 1
        print('Done.')
    
def login():
    try:
        login_type = str(input('Login as Admin or Student? ')).lower()
        if login_type == 'Admin'.lower():
            id = int(input('Please enter your Admin ID: '))
            print('==================================')
            if adm.Admin.get_id() == id:
                print('Welcome', stu1.__dict__.get('name'), '\n')
                admin_menu(id)
        elif login_type == 'Student'.lower():
            id = int(input('Please enter your Student ID: '))
            print('==================================')
            if stu1.get_id() == id:
                print('Welcome', stu1.__dict__.get('name'), '\n')
                student_menu(id)
            else:
                print('Not found')
    except ValueError:
        print('ID is an int')

def student_menu(id):
    print(stu1)
def admin_menu(id):
    return None