import Program as prg
from Course import Course
import Semester as sem
import csv
from User import User, Student, Admin
import main_func
import ast
import fileinput
import os
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
        
        with open('test.csv', 'w+',newline='') as f:
            write = csv.writer(f)
            write.writerow(student1)

        with open('test.csv', 'r') as f:
            reader = csv.reader(f)
            student = []
            for lines in reader:
                print(lines[0])
                student.append(lines)
            for i in student:
                history = ast.literal_eval(i[5]) # or [i.strip() for i[5] in student]
            #print(history)
            f.close()

    def add_student_history(): # fix to csv and student to new line
        
        with open('test.csv', 'a+',newline='') as f:
            write = csv.writer(f)
            write.writerow(student2)
        with open('test.csv', 'r') as f:
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

    # find student id from reading lines
    # add lines to list
    # edit the list where course = list element
    # append new list to students file
    # remove line of student id
    def test_edit_value(id='s123'):
        with open('test.csv', 'r+') as f:
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
                        return False
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(program)+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"')
            f.close()

        with open('test.csv', 'r') as inf, open('test_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('test.csv')
        os.rename('test_temp.csv', 'test.csv')
    #add_student_history()
    #test_edit_value()