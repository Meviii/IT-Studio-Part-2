# TO DO: Confirm how to calculate Program Credit points

import csv
from Course import Course

class UserInputError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

class Program:
    def __init__(self, prg_code, prg_title):
        self.code = prg_code
        self.title = prg_title
        self.credit_points = 0
        self.courses_core = []
        self.courses_elect = []

    def default(self, o):
        return o.__dict__  

    # Program Code Setters and Getters

    def set_code(self, prg_code):
        # Details of prg_code - numbers and letters
        try:
            if len(prg_code) != 5:
                raise Exception('Program Code must contain 2 letters then 3 numbers')
            else:
                self.code = prg_code.upper()
        except UserInputError as error:
            print(error)

    def get_code(self):
        return self.code

    # Program Title Setters and Getters

    def set_title(self, prg_title):
        try:
            if prg_title == '':
                raise UserInputError ('Please enter a Program title. Cannot be blank')
            else:
                self.title = prg_title.upper()
        except UserInputError as error:
            print(error)

    def get_title(self):
        return self.title

    # Program Credits Setters and Getters

    def calc_credit_points(self):
        total_pts = 0
        for i in range(len(self.courses)):
            pts = int(self.courses[i].cred_points)
            total_pts = total_pts + pts 
        return total_pts
        
    def set_credit_points(self):
        try:
            if self.calc_credit_points() == 0:
                raise UserInputError ('Error: Program contains no Courses. Unable to set Credit Points')
            else:
                self.credit_points = self.calc_credit_points()
                
        except UserInputError as error:
            print(error)

    def get_credit_points(self):
        return self.credit_points

    def add_courses(self, course):
        try:
            if not isinstance(course, Course):
                raise UserInputError ('Please add a valid Course. Course does not exist.')
            elif course.type.upper() == 'CORE':
                self.courses_core.append(course)
            elif course.type.upper() == 'ELECTIVE':
                self.courses_elect.append(course)

        except UserInputError as error:
            print(error)    
        
    def remove_courses(self, course):
        try:
            if course not in self.courses_core and self.courses_elect:
                raise UserInputError ('Cannot remove course. Course does not exist.')
            elif course in self.courses_core:
                self.courses_core.remove(course)
            elif course in self.courses_elect:
                self.courses_elect.remove(course)
        except UserInputError as error:
            print(error)   

    def get_courses_core(self):
        formatted_str = '\n'
        for i in range(len(self.courses_core)):
            formatted_str += '      - ' + str(self.courses_core[i].title) + '\n'
        return formatted_str

    def get_courses_elect(self):
        formatted_str = '\n'
        for i in range(len(self.courses_elect)):
            formatted_str += '      - ' + str(self.courses_elect[i].title) + '\n'
        return formatted_str

    def __eq__(self, other):
        return (self.code.lower() == other.code.lower())
      
    def __str__(self):
        formatted_str = "Program Code: " + self.code + "\n"
        if not self.title == '':
            formatted_str += "Program Title: " + self.title + "\n"
        if not self.credit_points == 0:
            formatted_str += "Credit Points: " + str(self.cred_points) + "\n"    
        if not self.courses_core == []:
            formatted_str += "\nCore Courses:" + str(self.get_courses_core()) + "\n" 
        if not self.courses_core == []:
            formatted_str += "Elective Courses:" + str(self.get_courses_elect()) + "\n" 
        return formatted_str

    def programId_list(): # Returns only prgram id from all programs in programs.csv
        with open('data/programs.csv', 'r') as f:
            reader = csv.reader(f)
            programs_lst = []
            for lines in reader:
                programs_lst.append(lines[0])
        f.close()
        return programs_lst

    def show_programsID_list():
        print("============\nProgram IDs:")
        with open("data/programs.csv", 'r') as f:
            reader =csv.reader(f)
            for lines in reader:
                print("-", lines[0])
        f.close()
        print("============")

    def program_name_list(): # Returns only prgram name in lowercase (for case insensitive comparisons) from all programs in programs.csv
        with open('data/programs.csv', 'r') as f:
            reader = csv.reader(f)
            programs_lst = []
            for lines in reader:
                programs_lst.append(lines[1].lower())
        f.close()
        return programs_lst
    
    def is_program_true(self):
        if self.get_program() != '':
            return True
        else:
            return False
            
    def open_program_by_id(pro_id):
        with open('data/programs.csv', 'r') as f:
            reader = csv.reader(f)
            for lines in reader:
                if str(lines[0]) == str(pro_id):
                    return True
                else:
                    continue
            f.close()
            return False

# ProgB1 = Course('COSC2801','Programming Bootcamp 1','12','NA','S1 & S2','BP0924', 'Core')
# It_Studio2 = Course('COSC2800', 'IT STUDIO 2', '24', 'NA', 'S1 & S2','BP0924', 'Core')
# Math2411 = Course('MATH2411','Mathematics for Computing 1','12','NA','S1 & S2','BP0924','CORE')
# Studio1 = Course('COSC2803','Programming Studio 1','24','NA','S1','BP0924', 'CORE')
# Graphics = Course('COSC1187','Interactive 3D Graphics and Animation','12','NA','S1','BP0924', 'ELECTIVE')

# BA_CS = Program('BP094', 'Bachelor of Computer Science')
# BA_CS.add_courses(ProgB1)
# BA_CS.add_courses(It_Studio2)
# BA_CS.add_courses(Math2411)
# BA_CS.add_courses(Studio1)
# BA_CS.add_courses(Graphics)

# print(BA_CS.get_courses())
#print(BA_CS)

# print(BA_CS.calc_credit_points())
# pts = BA_CS.calc_credit_points()
# BA_CS.set_credit_points()
# print(BA_CS.get_credit_points())
