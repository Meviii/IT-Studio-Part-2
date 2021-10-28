import ast
import csv
import os
from Semester import *
import main_func

class User:
    def __init__(self, user_id, user_name, user_birth, user_gender):
        self.id = user_id
        self.name = user_name
        self.birth = user_birth
        self.gender = user_gender

    def set_id(self, user_id):
        self.id = user_id

    def get_id(self):
        return self.id

    def set_name(self, user_name):
        self.name = user_name

    def get_name(self):
        return self.name

    def set_birth(self, user_birth):
        self.birth = user_birth

    def get_birth(self):
        return self.birth
    
    def set_gender(self, user_gender):
        self.gender = user_gender

    def get_gender(self):
        return self.gender

    def __eq__(self, other):
        return (self.id == other.id)
      
    def __str__(self):
        formatted_str = "User ID: " + str(self.id) + "\n"
        if not self.name == '':
            formatted_str += "Name: " + self.name + "\n"
        if not self.mobile == '':
            formatted_str += "Mobile: " + self.mobile + "\n"
        return formatted_str
class Student(User):
    def __init__(self, user_id, user_name, user_birth, user_gender, stu_program='', stu_acad_history=[], stu_curr_enrol=[], stu_study_plan=[],stu_absence='NA'):

        User.__init__(self, user_id, user_name, user_birth, user_gender)
        self.program = stu_program
        self.acad_history = stu_acad_history
        self.curr_enrol = stu_curr_enrol
        self.study_plan = stu_study_plan
        self.absence = stu_absence

    def set_program(self, stu_program):
        with open('data/programs.csv') as pro_file:
            reader = csv.reader(pro_file)
            for lines in reader:
                if stu_program in lines:
                    self.program = stu_program
                    print(f'Student program set to {stu_program} \n')

    def get_program(self):
        return self.program

    def get_acad_history(self):
        return self.acad_history
    
    def set_curr_enrol(self, stu_curr_enrol=[]):
        self.curr_enrol = stu_curr_enrol

    def get_curr_enrol(self):
        return self.curr_enrol
    
    def set_study_plan(self, stu_study_plan):
        self.study_plan = stu_study_plan

    def get_study_plan(self):
        return self.study_plan

    def get_stu_absence(self):
        return self.absence

    def __eq__(self, other):
        return (self.id == other.id)
      
    def __str__(self):
        formatted_str = "Student ID: " + str(self.id) + "\n"
        if not self.name == '':
            formatted_str += "Name: " + str(self.name) + "\n"
        if not self.program == '':
            formatted_str += "Program: " + str(self.program) + "\n"
        return formatted_str

    def change_student_name(id, name): # Will overwrite student current name
        with open('data/students.csv', 'r') as stuf:
            reader = csv.reader(stuf)
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]

        final = str(str(student[0]) +','+ str(name)+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
        
        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def change_student_gender(id, gender): # Will overwrite student current gender
        with open('data/students.csv', 'r') as stuf:
            reader = csv.reader(stuf)
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]

        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(gender)+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
        
        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def change_student_birth(id, birth): # Will overwrite student current birth
        with open('data/students.csv', 'r') as stuf:
            reader = csv.reader(stuf)
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]

        final = str(str(student[0]) +','+ str(student[1])+','+ str(birth)+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
        
        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def add_to_plan(id, course_code): # Adds a course to student study plan
        with open('data/students.csv', 'r+') as stuf:
            stu_reader = csv.reader(stuf,skipinitialspace=True)
            student =[]
            final = ''
            for lines in stu_reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
                    study_plan  = ast.literal_eval(lines[7])
            
            if not course_code in study_plan: 
                study_plan.append(course_code)
                final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(study_plan)+'"'+ ','+str(student[8]))
            else:
                final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
        stuf.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def remove_from_plan(id, course_code): # Removes a course from student study plan
        with open('data/students.csv', 'r+') as stuf:
            stu_reader = csv.reader(stuf,skipinitialspace=True)
            student =[]
            final = ''
            for lines in stu_reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
                    study_plan  = ast.literal_eval(lines[7])
            
            if course_code in study_plan: 
                study_plan.remove(course_code)
                final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(study_plan)+'"'+ ','+str(student[8]))
            else:
                final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
        stuf.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def open_students_for_id(id): # Returns if id exists in students.csv
        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(id):
                    return True
                else:
                    continue
            f.close()
            return False

    def student_info_list(id): # Returns all info of a specific line by id from students.csv
        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if lines[0] == id:
                    student_lst = [i.strip() for i in lines]
                else:
                    continue
            f.close()
            return student_lst

    def student_object(id): # Creates an Student object using per info from student_info_list(id)
        student = Student(Student.student_info_list(id)[0], Student.student_info_list(id)[1], Student.student_info_list(id)[2],
                Student.student_info_list(id)[3], Student.student_info_list(id)[4], Student.student_info_list(id)[5], Student.student_info_list(id)[6],Student.student_info_list(id)[7],Student.student_info_list(id)[8])
        return student

    def studentId_list(): # Returns only studentID from all students in students.csv
        with open('data/students.csv', 'r') as f:
            reader = csv.reader(f)
            studentsID_lst = []
            for lines in reader:
                studentsID_lst.append(lines[0])
        f.close()
        return studentsID_lst

    def add_student_course(id, stu_course, year_sem): # Adds a course to a student line by id in students.csv

        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            courses = []
            for lines in reader:
                if str(lines[0]) == str(id):
                    student = [i.strip() for i in lines]
                    if not stu_course in lines[6]:
                        courses = ast.literal_eval(lines[6])
                        courses.append(str(stu_course))
                        Semester.sem_add_count(id, stu_course, year_sem)
                        print(f'{stu_course} added')
                    else:
                        print('Already enrolled')
                        return main_func.student_menu(id)
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses)+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
            f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def remove_course(id, stu_course): # Removes a course to a student line by id in students.csv

        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
                    if stu_course in lines[6]:
                        courses = ast.literal_eval(lines[6])
            courses.remove(stu_course)
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses)+'"'+','+ '"' +str(student[7])+'"'+ ','+str(student[8]))
            f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def remove_stu_program(id): # Removed enrolled courses and study plan, changed program to 'NA'
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
                    if not lines[4] == 'NA':
                        program = 'NA'
                    else:
                        print('You are not a part of any program')
                        return False
            print('You have been removed from your program.')
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(program)+',"'+ str(student[5]) +'",' + '"[]"'+','+ '"[]"'+ ','+str(student[8]))
            f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')
    
    def check_prereqs(id, course): # Checks if prereq is completed(passed and in acad history) by student, and returns True, else False 
        with open('data/courses.csv', 'r') as cf:
            cfreader = csv.reader(cf)
            courses = []
            course_prereqs = []
            for lines in cfreader:
                if lines[0] == course:
                    courses.append(lines[3]) #appends prereqs of course 
            for i in courses:
                course_prereqs = ast.literal_eval(i) #makes prereqs of course a list
            
            if courses is None:
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
                return False
            elif not z is None:
                if len(course_prereqs) == len(z):
                    for i in stu_history:
                        for x in course_prereqs:
                            if str(i[0]) == str(x):
                                if i[1] >= 50:
                                    return True
                                else:
                                    return False
                else:
                    return False

    def check_grad_eligility(id): # Returns True if study plan is empty, else False.
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(id):
                    if str(lines[7]) == '[]':
                        return True
                    else:
                        return False
        f.close

    def apply_for_absence(id, type): # Changes student[8] to PENDING application with set days
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+f'PENDING:{type}')
            f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def course_progress_stu(id): # Returns the course progress(passed courses in acad history and curr enrollments) in a list
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
            curr_courses = []
            stu_history=[]
            for i in student:
                stu_history = ast.literal_eval(student[5])
                current_course = ast.literal_eval(student[6])

            for i in stu_history:
                if i[1] >= 50:
                    curr_courses.append(i[0])
            
            curr_courses.extend(current_course)
            return curr_courses

    def curr_gpa_stu(id): # Returns gpa grade of student calculated by courses in academic history
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]

            marks = []
            stu_history=[]
            for i in student:
                stu_history = ast.literal_eval(student[5])
            courses = []
            for i in stu_history:
                courses.append(i[0])
                marks.append(i[1])
            gpv = []
            for i in marks:
                if i >= 80:
                    gpv.append(4)
                elif 70 <= i <= 79:
                    gpv.append(3)
                elif 60 <= i <= 69:
                    gpv.append(2)
                elif 50 <= i <= 59:
                    gpv.append(1)
                else:
                    gpv.append(0)

            gpa = round((sum((gpv)) / (len(gpv))), 2)
            return gpa

    def drop_stu_enrolment(id): # Drops all currently enrollments of a student

        with open('data/students.csv', 'r+') as f:
                reader = csv.reader(f)
                final = ''
                student = []
                for lines in reader:
                    if lines[0] == id:
                        student = [i.strip() for i in lines]
                final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"[]"'+',"'+ str(student[7]) +'",'+str(student[8]))
                f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def all_students(): # returns list of all lines in students.csv

        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            students = []
            for lines in reader:
                students.append(lines)
        f.close
        return students

    def stu_failed_couses(id): # returns list of failed courses by student
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
            curr_courses = []
            stu_history=[]
            for i in student:
                stu_history = ast.literal_eval(student[5])
            for i in stu_history:
                if i[1] < 50:
                    curr_courses.append(i[0])

            return curr_courses

    def show_studentID_list():
        print("============\nStudent IDs:")
        with open("data/students.csv", 'r') as f:
            reader =csv.reader(f)
            for lines in reader:
                print("-", lines[0])
        f.close()
        print("============")

class Admin(User):
    def __init__(self, user_id, user_name, user_birth, user_gender, adm_role = 'Admin'):
        User.__init__(self, user_id, user_name, user_birth, user_gender)
        self.role = adm_role
    
    def set_admin_role(self, adm_role):
        self.role = adm_role

    def get_admin_role(self):
        return self.role

    def __eq__(self, other):
        return (self.id == other.id)
      
    def __str__(self):
        formatted_str = "Admin ID: " + str(self.id) + "\n"
        if not self.name == '':
            formatted_str += "Name: " + self.name + "\n"
        if not self.name == '':
            formatted_str += "Role: " + self.role + "\n"
        return formatted_str
    
    def open_admins_for_id(id): # Returns if id exists in admins.csv
        with open('data/admins.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(id):
                    return True
                else:
                    continue
            f.close()
            return False

    def admin_info_list(id): # Returns all info of a specific line by id from admins.csv
        with open('data/admins.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if lines[0] == id:
                    admin_lst = [i.strip() for i in lines]
                else:
                    continue
            f.close()
            return admin_lst

    def admin_object(id): # Creates an Admin object using per info from admin_info_list(id)
        admin = Admin(Admin.admin_info_list(id)[0], Admin.admin_info_list(id)[1], Admin.admin_info_list(id)[2],
                Admin.admin_info_list(id)[3])
        return admin

    def absence_accept(id): # Edits student[8] to accepted and drops all currently enrolled courses
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"[]"'+','+ '"' +str(student[7])+'"'+ ','+f'Accepted: {student[8]}')
            f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')
    
    def absence_deny(id): # Edits student[8] to NA meaning application is denied

        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+f'NA')
            f.close()

        with open('data/students.csv', 'r') as inf, open('data/students_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == id:
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/students.csv')
        os.rename('data/students_temp.csv', 'data/students.csv')

    def achievement_by_course(course): # Returns all student and mark of a course by each student who completed it
        with open('data/students.csv', 'r') as stuf:
            reader = csv.reader(stuf)
            student=[]
            stu_details = []
            for lines in reader:
                student.append(lines)

            for i in student:
                stu_history = ast.literal_eval(i[5])
                for history in stu_history:
                    if course in history[0]:
                        print(f'Student: {i[0]}, Mark: {history[1]}')
    
