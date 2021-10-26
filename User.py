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

    def is_program_true(self):
        if self.get_program() != '':
            return True
        else:
            return False
      
    def __str__(self):
        formatted_str = "Student ID: " + str(self.id) + "\n"
        if not self.name == '':
            formatted_str += "Name: " + str(self.name) + "\n"
        if not self.program == '':
            formatted_str += "Program: " + str(self.program) + "\n"
        return formatted_str

    def change_student_name(id, name):
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

    def change_student_gender(id, gender):
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

    def change_student_birth(id, birth):
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

    def add_to_plan(id, course_code):
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

    def remove_from_plan(id, course_code):
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

    def apply_for_absence(id, type):
        with open('data/students.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            student = []
            for lines in reader:
                if lines[0] == id:
                    student = [i.strip() for i in lines]
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"'+ ','+str(f'PENDING:{type}'))
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
