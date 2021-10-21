import csv
import ast
import os
from main_func import add_student_course
from main_func import remove_course
from Semester import get_curr_student

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
            add_student_course(student_id, crs_code)
        else:
            print('This course has already reached the maximum number of students')

        print('Student ' + student_id + 'has been added to ' + crs_code + '.')



    def remove_student(self, student_id, crs_code):
        remove_course(student_id, crs_code)
        print('Student ' + student_id + 'has been removed from ' + crs_code + '.')

    def __str__(self):
        # formatted_str = "Name: " + self.name + "\n"
        # if not self.mobile == '':
        #     formatted_str += "Mobile: " + self.mobile + "\n"
        # if not self.landline == '':
        #     formatted_str += "Landline: " + self.landline + "\n"
        # return formatted_str
        return None
