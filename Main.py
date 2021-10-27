import Program as prg
from Course import Course
from Semester import Semester
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

    # FOR ADDING STUDENT 
    # def add_student_history(): # fix to csv and student to new line
        
    #     with open('test.csv', 'a+',newline='') as f:
    #         write = csv.writer(f)
    #         final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses)+'"'+','+ '"' +str(student[7])+'"')
    #         write.writerow(final.strip(','))
    #     with open('test.csv', 'r') as f:
    #         reader = csv.reader(f)
    #         for lines in reader:
    #             print(lines)

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

    # get course
    # for i in reader, if COSC2801 = i[0], append the preqs to list, preqs
    # check if pres is NA, or course preq is in academic history of student, add course

    def check_prereqs(id='s123', course='COSC2801'):
        with open('data/courses.csv', 'r') as cf:
            cfreader = csv.reader(cf)
            courses = []
            course_prereqs = []
            for lines in cfreader:
                if lines[0] == course:
                    courses.append(lines[3]) #appends prereqs of course 
            for i in courses:
                course_prereqs = ast.literal_eval(i) #makes prereqs of course a list
            
            if course_prereqs is []:
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
                    print('false')
                    return False
                elif not z is None:
                    print(z)
                    if len(course_prereqs) == len(z):
                        for i in stu_history:
                            for x in course_prereqs:
                                if str(i[0]) == str(x):
                                    if i[1] >= 50:
                                        print('passed')
                                        return True
                                    else:
                                        print('failed')
                                        return False
                    else:
                        print('len false')
                        return False

            # if z is not none, if INT stu_history[1] is >= 50, add course ## Might need to check if this compliments >1 prereq courses 
            # else if z is none, return false                              # maybe check len(pre reqs) with len(set) for >1 prereq courses

            # COSC123 has preq SCIE2411, ACAD DOES NOT HAVE(s123)
            # COSC123 has preq SCIE2411, ACAD HAS(s1234)

    #check_prereqs()

    def mark_for_course(id='s123', course='COSC2703'):
        temp1 = []
        prereqs = []
        with open('data/courses.csv', 'r') as f1:
            reader1 = csv.reader(f1)
            for lines in reader1:
                if lines[0] == course:
                    temp1.append(lines[3])
            for i in temp1:
                prereqs = [i.strip() for i in temp1]
            for i in prereqs:
                if i == 'NA':
                    print('no prereqs')
                    return True

        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            student_acad_history = []
            temp = []
            for lines in reader:
                if lines[0] == str(id):
                    temp.append(lines[5])
            for i in temp:
                student_acad_history = ast.literal_eval(i)
            print(student_acad_history)

            for i in student_acad_history:
                if course == i[0]:
                    if i[1] >= 50:
                        print('passed')
                        return True
                    else:
                        print('failed')
                        return False
                else:
                    print('Course not found')
                    return False
    #mark_for_course()
    # #add_student_history()
    #test_edit_value()
    #main_func.add_prereq()

    # check if acad history course in prereq + score is > 50

    # Study plan = [COSC, SCIENCE, MATH]
    # Academic H = [(COSC, 58)]
    def check_prereq_empty(course):
        with open('data/courses.csv', 'r') as cf:
            cfreader = csv.reader(cf)
            courses = []
            course_prereqs = []
            for lines in cfreader:
                if lines[0] == course:
                    courses.append(lines[3]) #appends prereqs of course 
            for i in courses:
                if i == '[]':
                    return True
                else:
                    return False
    #check_prereq_empty()
    def courses_list(): # Returns all info from each line in courses.csv (Sorted)
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            course_lst = []
            for lines in reader:
                course_lst.append(lines)
        f.close()
        return sorted(course_lst)
        print('Sem 1: ')
        for i in courses_list():
            if 'S1' in i[4]:
                print(f'{i[1]}, {i[4]}')
        print('Sem 2: ')
        for i in courses_list():
            if 'S2' in i[4]:
                print(f'{i[1]}, {i[4]}')
    def get_stu_program_courses(id, program):
        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if lines[0] == id:
                    student_program = lines[4]
                else:
                    continue
            f.close()
        with open('data/programs.csv', 'r') as f1:
            reader1 = csv.reader(f1)
            for lines in reader1:
                print(lines)
    
    def test(semester_code='SEM12021', course='COSC2801'):
        with open('data/semesters.csv', 'r+') as f1:
            reader1 = csv.reader(f1)
            alist = []
            final = ''
            for lines in reader1:
                if lines[0] == semester_code:
                    sem_info = [i.strip() for i in lines]
                    alist.append(lines[1])
            for i in alist:
                sem_courses = ast.literal_eval(i)
            courses= []
            for i in sem_courses:
                if i[0] == course:
                    final = f"('{i[0]}', {str(int(sem_courses[0][1]) + 1)}, {i[2]})"
            # remove i[1][i] where i == course and append new final.

    def course_info_list(id): # Returns all info of a specific line by id from students.csv
        with open('data/semesters.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if lines[0] == id:
                    course_lst = [i.strip() for i in lines]
                else:
                    continue
            f.close()
            return course_lst

    def sem_object(id): # Creates an Student object using per info from student_info_list(id)
        sem = Semester(course_info_list(id)[0], course_info_list(id)[1],course_info_list(id)[2],course_info_list(id)[3])
        return sem
    

    #sem = sem_object('SEM12021')
    #print(sem.get_curr_student())
    main_func.login()

    # s123 COSC2703 > 50, MATH2411 < 50, wants to enroll into COSC2801, should allow, else:
    # wants to enroll into COSC2803, with prereq MATH2411, shouldnt allow

