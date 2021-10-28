import csv
import ast
import os
import main_func
from User import *

# Project start date - end date: 04/10/2021 - 30/10/2021
# Mevlut Saluk, S3717696
# Alexander Tan, S3849729
# Dion Tartaglione, S3239216
# Cesar Jude Quitazol, S3844561
# Haotian Shen, S3770488


class UserInputError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

class Semester:
    def __init__(self, sem_id, sem_offering, sem_max_student, sem_curr_student):
        self.id = sem_id
        self.offering = sem_offering
        self.max_student = sem_max_student
        self.curr_student = sem_curr_student

    def default(self, o):
        return o.__dict__  

    def set_id(self, sem_id, crs_code):
        #TEST METHOD
        #import csv
        #import ast
        #from Course import Course
        #import os
        #crs_code = 'MATH2411'
        #sem_id = 'S1'

        with open('data/courses.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            course = []
            id = []
            for lines in reader:
                if str(lines[0]) == str(crs_code):
                    course = [i.strip() for i in lines]

                    if len(ast.literal_eval(lines[4])) == 0:
                        id = ast.literal_eval(lines[4])
                        id.append(str(sem_id))
                    else:

                        if len(ast.literal_eval(lines[4])) == 2:
                            print('Course is already being offered for ' + sem_id)
                            id = ast.literal_eval(lines[4])
                        
                        else:
                            if ast.literal_eval(lines[4])[0] == 'S1':
                                id = ast.literal_eval(lines[4])
                                id.append(str(sem_id))
                            else:
                                id = ast.literal_eval(lines[4])
                                id.insert(0, str(sem_id))
            final = str(str(course[0]) +','+ str(course[1])+','+ str(course[2])+',"'+ str(course[3])+'","'+ str(id)+'",'+ str(course[5]) +',' + '"'+str(course[6])+'"')
            print(final)
            f.close()

        with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == str(crs_code):
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/courses.csv')
        os.rename('data/courses_temp.csv', 'data/courses.csv')

    def get_id(self, crs_code):

        import csv
        import ast
        from Course import Course
        import os
        crs_code = 'MATH2411'

        with open('data/courses.csv', 'r+') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(crs_code):
                    id = ast.literal_eval(lines[4])
                    #self.id = id
                    print(id)
          
            f.close()
        if len(id) == 2:
            print('This course is being offered during both semesters')
        else:
            if id[0] == 'S1':
                print('This course is being offered during semester 1.')
            else:
                print('This course is being offered during semester 2.')
            

    def set_offering(self, sem_offering):
        self.offering = sem_offering

    def get_offering(self):
        return self.offering

    def set_max_student(self, sem_id, crs_code, sem_max_student):
        #TEST METHOD
        #import csv
        #import ast
        #from Course import Course
        #import os
        #sem_id = 'S1 2021'
        #crs_code = 'MATH2411'
        #sem_max_student = 10

        with open('data/courses.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            course = []
            max_stu = []
            for lines in reader:
                if str(lines[0]) == str(crs_code):
                    course = [i.strip() for i in lines]
                    if ast.literal_eval(lines[4])[0] in sem_id:
                        max_stu = ast.literal_eval(lines[6])
                        max_stu[0] = sem_max_student
                    elif ast.literal_eval(lines[4])[1] in sem_id:
                        max_stu = ast.literal_eval(lines[6])
                        max_stu[1] = sem_max_student
                    else:
                        print('Invalid semester ID')
            
            final = str(str(course[0]) +','+ str(course[1])+','+ str(course[2])+',"'+ str(course[3])+'","'+ str(course[4])+'",'+ str(course[5]) +',' + '"'+str(max_stu)+'"')
            f.close()

        with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == str(crs_code):
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/courses.csv')
        os.rename('data/courses_temp.csv', 'data/courses.csv')
        print('The maximum number of students has been set to ' + max_stu + '.')

    def get_max_student(self, crs_code, sem_id):

        with open('data/courses.csv', 'r+') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(crs_code):
                    if ast.literal_eval(lines[4])[0] in sem_id:
                        max_stu = ast.literal_eval(lines[6])[0]
                        #self.max_student = max_stu
                        print('The maximum number of students that can be enrolled into ' + crs_code + ' is ' + max_stu + '.')
                    elif ast.literal_eval(lines[4])[1] in sem_id:
                        max_stu = ast.literal_eval(lines[6])[1]
                        #self.max_student = max_stu
                        print('The maximum number of students that can be enrolled into ' + crs_code + ' is ' + max_stu + '.') 
                    else:
                        print('Invalid semester ID')
            f.close()
        
    def get_curr_student(self, crs_code):
        counter = 0
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            for lines in reader:
                print(ast.literal_eval(lines[6]))
                if crs_code in ast.literal_eval(lines[6]):
                    print(ast.literal_eval(lines[6]))
                    counter = counter + 1
            f.close()
        self.curr_student = counter
        print('There are currently ' + counter + ' students enrolled in ' + crs_code + '.')
        return self.curr_student
 
    def add_student(self, crs_code, student_id):
        if self.curr_student < self.max_student:
            Student.add_student_course(student_id, crs_code)
        else:
            print('This course has already reached the maximum number of students')

        print('Student ' + student_id + 'has been added to ' + crs_code + '.')

    def show_semesterID_list(): #prints list of Semester ID
        print("Program Codes:\n=============")
        with open("data/semesters.csv", "r") as f:
            reader = csv.reader(f)
            for lines in reader:
                print('- Program Code:', lines[0], ' Semester ID:', lines[1])
        print("=============")

    def remove_student(self, student_id, crs_code):
        Student.remove_course(student_id, crs_code)
        print('Student ' + student_id + 'has been removed from ' + crs_code + '.')

    def sem_add_count(id, stu_course, semester_code): # Adds a student count in semesters.csv

        with open('data/semesters.csv', 'r+') as f, open('data/students.csv', 'r') as stuf:
            reader1 = csv.reader(stuf)
            for lines in reader1:
                if lines[0] == id:
                    stu_program = lines[4]
                    break

            reader = csv.reader(f)
            final = ''
            semester = []
            # read courses where stu_course == course, if course code in sem courses[1], stu_count in sem + 1
            for lines in reader:
                if str(lines[1]) == str(semester_code):
                    semester = [i.strip() for i in lines]
                    if lines[0] == stu_program:
                        if stu_course in semester[2]:
                            break
                        else:
                            print('Not in any semester')
                            return False
                    else:
                        print('Program does not exist')
                        return False
            #SEM12021,['COS2801'],0,1000
            new_count = int(semester[3]) + 1
            final = str(semester[0]+','+semester[1] +','+ '"'+ semester[2]+'",'+ str(new_count)+ ','+ semester[4])
            f.close()

        with open('data/semesters.csv', 'r') as inf, open('data/semesters_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[1] == semester_code:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/semesters.csv')
        os.rename('data/semesters_temp.csv', 'data/semesters.csv')

    def sem_remove_count(id, stu_course, semester_code): # Removes a student count in semesters.csv

        with open('data/semesters.csv', 'r+') as f, open('data/students.csv', 'r') as stuf:
            reader1 = csv.reader(stuf)
            for lines in reader1:
                if lines[0] == id:
                    stu_program = lines[4]
                    break

            reader = csv.reader(f)
            final = ''
            semester = []
            # read courses where stu_course == course, if course code in sem courses[1], stu_count in sem + 1
            for lines in reader:
                if str(lines[1]) == str(semester_code):
                    semester = [i.strip() for i in lines]
                    if lines[0] == stu_program:
                        if stu_course in semester[2]:
                            break
                        else:
                            print('Not in any semester')
                            return False
                    else:
                        print('Program does not exist')
                        return False
            #SEM12021,['COS2801'],0,1000
            new_count = int(semester[3]) - 1
            final = str(semester[0]+','+semester[1] +','+ '"'+ semester[2]+'",'+ str(new_count)+ ','+ semester[4])
            f.close()

        with open('data/semesters.csv', 'r') as inf, open('data/semesters_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[1] == semester_code:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/semesters.csv')
        os.rename('data/semesters_temp.csv', 'data/semesters.csv')

    def course_list_by_sem(semid): # Returns courses in a certain semester as list
        with open('data/semesters.csv', 'r') as f:
            reader = csv.reader(f)
            sem_list = []
            specific_sem_course_name = []
            course_info = []
            for lines in reader:
                if lines[0] == semid:
                    sem_list.append(lines)
            for i in sem_list:
                course_info = ast.literal_eval(i[1])
            for i in course_info:
                specific_sem_course_name.append(i[0])
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            course_name_lst = []
            for lines in reader:
                course_name_lst.append(lines[0])

        sem_courses = set(course_name_lst).intersection(set(specific_sem_course_name))
        return sem_courses

    def open_semester_for_id(sem_id): # Returns if id exists in semesters.csv
        with open('data/semesters.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[1]) == str(sem_id):
                    return True
                else:
                    continue
            f.close()
            return False

    def programCode_list(): # Returns only semesterID from all semesters in semesters.csv
        with open('data/semesters.csv', 'r') as f:
            reader = csv.reader(f)
            semesterID_lst = []
            for lines in reader:
                semesterID_lst.append(lines[0])
        f.close()
        return semesterID_lst
 
    def semesterID_list(): # Returns only semesterID from all semesters in semesters.csv
        with open('data/semesters.csv', 'r') as f:
            reader = csv.reader(f)
            semesterID_lst = []
            for lines in reader:
                semesterID_lst.append(lines[1])
        f.close()
        return semesterID_lst