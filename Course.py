
# Course Class: 
# Constructor, string methods, getter and setters, methods to add or remove prereqs and available sems
# UserInputError(Exception) class used
# TO DO - want to fix printing prerequisite courses not in list
# TO CONFIRM: set_code - Whether the system will check for 4 char then 4 ints

import ast
import csv
import os
import main_func

class UserInputError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

class Course:
    def __init__(self, crs_code, crs_title, crs_cred_points, crs_prereq, crs_avail, crs_program, crs_type):
        self.code = crs_code
        self.title = crs_title
        self.cred_points = crs_cred_points
        self.prereq = crs_prereq
        self.avail = crs_avail
        self.program = crs_program
        self.type = crs_type

    def default(self, o):
        return o.__dict__  

    def set_code(self, crs_code):
        # Course code is made up of 4 characters then 4 numbers
        # TO CONFIRM: Whether the system will check for 4 char then 4 ints
        try:
            if len(crs_code) != 8:
                raise Exception('Course Code must contain four letters then four numbers')
            else:
                # crs_chars = crs_code[0:4]
                # crs_nums = crs_code[4:8] 
                self.code = crs_code.upper()
        except UserInputError as error:
            print(error)

    def get_code(self):
        return self.code

    def set_title(self, crs_title):
        # Title cannot be an empty string
        try:
            if crs_title == '':
                raise UserInputError ('Please enter a course title. Cannot be blank')
            else:
                self.title = crs_title.upper()
        except UserInputError as error:
            print(error)

    def get_title(self):
        return self.title
    
    def set_cred_points(self, crs_cred_points):
        # Credit Points can either be 12 or 24 points
        # Raise error if credits points are not 12 or 24
        pts = ['12', '24']
        try:
            if crs_cred_points not in pts:
                raise UserInputError ('Error: Credit Points can either be 12 or 24 points')
            else:
                self.cred_points = crs_cred_points
        except UserInputError as error:
            print(error)
    
    def get_cred_points(self):
        return self.cred_points

    def set_prereq(self, crs_prereq):
        # Prerequisites cannot be an empty string
        # Prerequisites to be seperated by a comma ',' else raise execption
        try:
            if crs_prereq == '':
                raise UserInputError ('Please enter a course title as a prerequisite. Cannot be blank')
            elif crs_prereq.upper() == 'NA':
                self.prereq = 'No Prerequisites'
            else:
                crs_prereq = crs_prereq.upper()
                prereq_list = crs_prereq.split(',')
                self.prereq = prereq_list
        except UserInputError as error:
            print(error)

    def get_prereq(self):
        return self.prereq
    
    def remove_prereq(self):
        try:
            if self.prereq == 'No Prerequisites':
                raise UserInputError ('There are no prerequisites to remove.')
            elif self.prereq == '':
                raise UserInputError ('No prerequisites have been set. Unable to remove')
            else:
                self.set_prereq('NA')
        except UserInputError as error:
            print(error)
        

    def set_avail(self, crs_avail):
        # Course can be available in either Semester 1 'S1', Semester 2 'S2' or both 'S1 & S2'
        avail_sems = ['S1', 'S2', 'S1 & S2']
        try:
            if crs_avail.upper() not in avail_sems:
                raise UserInputError ('Error: Please enter either \'S1\', \'S2\', \'S1 & S2\'')
            else:
                self.avail = crs_avail.upper()
        except UserInputError as error:
            print(error)

    def get_avail(self):
        return self.avail

    def remove_avail(self):
        avail_sems = ['S1', 'S2', 'S1 & S2']
        try:
            if self.avail not in avail_sems:
                raise UserInputError ('Course is not currently available')
            else:
                self.avail = 'Not available'
        except UserInputError as error:
            print(error)

    def set_type(self, crs_type):
        # Course can be available in either be a core subject or elective subject
        type = ['CORE', 'ELECTIVE']
        try:
            if crs_type.upper() not in type:
                raise UserInputError ('Error: Please enter either \'Core\' or \'Elective\'')
            else:
                self.type = crs_type.upper()
        except UserInputError as error:
            print(error)

    def get_type(self):
        return self.type


    def __eq__(self, other):
        return (self.title.lower() == other.title.lower())
      
    def __str__(self):
        formatted_str = "Course Code: " + self.code + "\n"
        if not self.title == '':
            formatted_str += "Course Title: " + self.title + "\n"
        if not self.cred_points == '':
            formatted_str += "Credit Points: " + str(self.cred_points) + "\n"    
        if not self.prereq == '':
            # want to fix printing prerequisite courses not in list
            formatted_str += "Prerequisite Courses: " + str(self.prereq) + "\n" 
        if not self.avail == '':
            formatted_str += "Availability: " + self.avail + "\n"
        return formatted_str
    
    def filtered_courses_list(id): # Returns courses which are needed to be completed by the student
        # need to return sorted course list of all courses of a program which are not completed by student
        with open('data/courses.csv', 'r') as courf, open('data/programs.csv', 'r') as progf, open('data/students.csv', 'r') as stuf:
            stu_reader = csv.reader(stuf)
            stu_acad_history = []
            stu_program = ''
            stu_passed_courses = []
            for lines in stu_reader:
                if lines[0] == id:
                    stu_program = lines[4]
                    stu_acad_history = ast.literal_eval(lines[5])
            
            # need to remove the courses which student passed in acad history from avail courses
            for i in stu_acad_history:
                if i[1] >=50:
                    stu_passed_courses.append(i[0]) 
            
            prog_reader = csv.reader(progf, skipinitialspace=True)
            core_prog_courses = []
            elec_prog_courses = []
            merged_courses = []
            for lines in prog_reader:
                if lines[0] == stu_program:
                    core_prog_courses = ast.literal_eval(lines[3])
                    elec_prog_courses = ast.literal_eval(lines[4])
            merged_courses = core_prog_courses
            merged_courses.extend(elec_prog_courses)

            final_list = [x for x in merged_courses if x not in stu_passed_courses]

            cour_reader = csv.reader(courf)
            course_filtered_info = []
            for i in cour_reader:
                course_filtered_info = [x for x in cour_reader if x[0] in final_list]
        return course_filtered_info

    def check_prereq_empty(course): # Returns True if prereq list is empty meaning no prereq
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

    def add_course(code, title, credits, sem, fee, prereq=[]): # Adds a course to courses.csv
        final = str(str(code) +','+ str(title) +','+ str(credits) +',' + '"'+str(prereq)+'"'+','+ str(sem) +','+ str(fee))
            
        with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)

            writer.writerow(final.split(','))
            writer.writerows(reader)

        os.remove('data/courses.csv')
        os.rename('data/courses_temp.csv', 'data/courses.csv')

    def add_prereq(code, prereq): # Adds a prereq for a course in courses.csv
        with open('data/courses.csv', 'r+') as f:
            reader = csv.reader(f)
            final = ''
            prereq_courses = []
            for lines in reader:
                if str(lines[0]) == str(code):
                    courses = [i.strip() for i in lines]
                    if not prereq in lines[3]:
                        prereq_courses = ast.literal_eval(lines[3])
                        prereq_courses.append(str(prereq))
                    else:
                        print('Already a prereq')
                        #return admin_menu(id)
                        return False
                        
            final = str(str(courses[0]) +','+ str(courses[1]) +','+ str(courses[2]) +',' + '"'+str(prereq_courses)+'"'+','+ str(courses[4]) +','+ str(courses[5]))
            f.close()

        with open('data/courses.csv', 'r') as inf, open('data/courses_temp.csv', 'w+', newline='') as outf:
            reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
            writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
            for lines in reader:
                if lines[0] == str(code):
                    writer.writerow(final.split(','))
                    break
                else:
                    writer.writerow(lines)
            writer.writerows(reader)

        os.remove('data/courses.csv')
        os.rename('data/courses_temp.csv', 'data/courses.csv')

    def coursesId_list(): # Returns only course codes from all courses in courses.csv
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            coursesId_list = []
            for lines in reader:
                coursesId_list.append(lines[0])
        f.close()
        return coursesId_list

    def courses_name_list(): # Returns only course names from all courses in courses.csv
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            course_name_lst = []
            for lines in reader:
                course_name_lst.append(lines[1].lower())
        f.close()
        return course_name_lst

    def courses_list(): # Returns all info from each line in courses.csv (Sorted)
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            course_lst = []
            for lines in reader:
                course_lst.append(lines)
        f.close()
        return sorted(course_lst)

    def open_for_courseid(course):
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(course):
                    return True
                else:
                    continue
            f.close()
            return False

    def show_courseID_list():
        print("============\nCourse IDs:")
        with open("data/courses.csv", 'r') as f:
            reader =csv.reader(f)
            for lines in reader:
                print("-", lines[0])
        f.close()
        print("============")

# It_Studio2 = Course('COSC2800', 'IT STUDIO 2', '24', 'NA', 'S1 & S2','BP0924', 'Core')
# print(It_Studio2)

# # test set_title
# crs_title = str(input("Name of Course Code. (Cannot be blank): "))
# It_Studio2.set_title(crs_title)
# print('\nName of course is:', It_Studio2.get_title(), ' \n')

# # test set_code
# crs_code = str(input("Set Course Code. (Four letters then Four numbers): "))
# It_Studio2.set_code(crs_code)
# print('\nName of course is:', It_Studio2.get_code(), ' \n')

# # test set_cred_points
# crs_cred_points = str(input("Set Credit Points. (Please enter either 12 or 24): "))
# It_Studio2.set_cred_points(crs_cred_points)
# print('\nCourse is now set to:', It_Studio2.get_cred_points(), 'pts \n')

# test set_prereq
# crs_prereq = str(input("Set Prerequisite for Course. (Seperate by comma or NA for none): "))
# It_Studio2.set_prereq(crs_prereq)
# print('\nPrereqs for course are:', It_Studio2.get_prereq(),'\n')

# test remove_prereq
# It_Studio2.remove_prereq()
# print('\nPrereq removed:', It_Studio2.get_prereq(),'\n')

# test set_avail
# crs_avail = str(input("Semester Availability of course: (Semester 1 'S1', Semester 2 'S2' or both 'S1 & S2'):"))
# It_Studio2.set_avail(crs_avail)
# print('\nAvailability for course are:', It_Studio2.get_avail(), '\n')

# test remove_avail
# print('Availability for course are:', It_Studio2.get_avail(), '\n')
# It_Studio2.remove_avail()
# print('Availability removed:', It_Studio2.get_avail(),'\n')

# print(It_Studio2)