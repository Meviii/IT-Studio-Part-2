import Program as prg
import Course as crs
import Semester as sem
import Student as stu
import Admin as adm
import csv
import main_func 

if __name__ == '__main__':
    stu1 = stu.Student(123, 'Tom Tommy', '20/02/2000', 'Male', 'Program1', 'Acad history', 'some courses', 'b312')

    # file = open('data/students.csv')
    # csv_reader = csv.reader(file)
    # stu_list = []
    # for row in csv_reader:
    #     stu_list.append(row)
    # print(stu_list)

    main_func.login()
    