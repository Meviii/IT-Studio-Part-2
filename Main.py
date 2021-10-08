import Program as prg
import Course as crs
import Semester as sem

import csv
from User import User, Student, Admin
import main_func 

if __name__ == '__main__':
    #TEST CHANGE FOR GIT

    u1 = User('u3717232', 'test1', '042312320', '02/10/20', 'Male')
    s1 = Student('s3717232', 'test2', '042312322', '02/10/20', 'Male', 'stu_program', 'stu_acad_history', 'stu_curr_enrol', 'stu_study_plan')
    a1 = Admin('a3717232', 'test3', '042312324', '02/10/20', 'Male', 'Admin')

    # file = open('data/students.csv')
    # csv_reader = csv.reader(file)
    # stu_list = []
    # for row in csv_reader:
    #     stu_list.append(row)
    # print(stu_list)
    print(u1)
    print(s1)
    print(a1)

    #main_func.login()
    