import Program as prg
from Course import Course
import Semester as sem

import csv
from User import User, Student, Admin
import main_func 
import json
import ast

if __name__ == '__main__':
    #TEST CHANGE FOR GIT

    # u1 = User('u3717232', 'test1', '042312320', '02/10/20', 'Male')
    # s1 = Student('s3717232', 'test2', '042312322', '02/10/20', 'Male', 'stu_program', 'stu_acad_history', 'stu_curr_enrol', 'stu_study_plan')
    # a1 = Admin('a3717232', 'test3', '042312324', '02/10/20', 'Male', 'Admin')
    
    #print(u1)
    #print(s1)
    #print(a1)

    student1 = (['s1234567','Tom Tommy3','22/02/2000','Male','BP094', [('COSC1243', 10),('COSC8569', 30),('COSC7895', 20)],['COSC12434','COSC85694','COSC78954'],['COSC124341','COSC856942','COSC789543']])
    student2 = (['s123','Tom Tommy5','22/02/2000','Male','BP094', [('COSC1243',89),('COSC8569',56),('COSC7895',60)],['COSC12434','COSC85694','COSC78954'],['COSC124341','COSC856942','COSC789543']])
    def get_list_history_csv(id):
        
        with open('data/students.csv', 'w+',newline='') as f:
            write = csv.writer(f)
            write.writerow(student1)

        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            student = []
            for lines in reader:
                print(lines[0])
                student.append(lines)
            for i in student:
                history = ast.literal_eval(i[5]) # or [i.strip() for i[5] in student]
            #print(history)
            f.close()

    def add_student_history(id): # fix to csv and student to new line
        
        with open('data/students.csv', 'a+',newline='') as f:
            write = csv.writer(f)
            write.writerow(student2)
        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                print(lines)

    #id = 's1234567'
    # Test with actual student variables
    #get_list_history_csv(id)
    #add_student_history(id)

    # Test with student objects
    s1 = Student('s1234567','Tom Tommy3','22/02/2000','Male','BP094', [('COSC1243', 10),('COSC8569', 30),('COSC7895', 20)],['COSC2800','COSC85694','COSC78954'],['COSC124341','COSC856942','COSC789543'])
    s2 = Student('s1334527','Tom Tommy5','22/02/2000','Male','BP094', [('COSC1243',89),('COSC8569',56),('COSC7895',60)],['COSC2800','COSC85694','COSC78954'],['COSC124341','COSC856942','COSC789543'])
    #s1.get_acad_history(id)

    # Test for Course object
    # def courses_list():
    #     with open('data/courses.csv', 'r') as f:
    #         reader = csv.reader(f)
    #         course_lst = []
    #         for lines in reader:
    #             course_lst.append(lines[0])
    #     f.close()
    #     return course_lst
    # print(courses_list())
    
    main_func.login()