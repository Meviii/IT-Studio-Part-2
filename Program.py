# TO DO: Confirm how to calculate Program Credit points

import Course

class UserInputError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

class Program:
    def __init__(self, prg_code, prg_title, prg_credit_points, prg_courses):
        self.code = prg_code
        self.title = prg_title
        self.credit_points = prg_credit_points
        self.courses = []

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
    # Confirm how to calculate Program Credit points
    def calc_credit_points(self):
        pass

    # def set_credit(self, prg_credit_points):
    #     pts = ['999', '24']
    #     try:
    #         if prg_credit_points not in pts:
    #             raise UserInputError ('Error: Program Credit Points can either be 999 or 999 points')
    #         else:
    #             self.credit_points = prg_credit_points
    #     except UserInputError as error:
    #         print(error)

    def get_credit(self):
        return self.credit

    def add_courses(self, course):
        try:
            if not isinstance(course, Course):
                raise UserInputError ('Please add a valid Course. Course does not exist.')
            else:
                self.courses.append(course)
        except UserInputError as error:
            print(error)    
        
    def remove_courses(self, course):
        try:
            if course not in self.courses:
                raise UserInputError ('Cannot remove course. Course does not exist.')
            else:
                self.courses.remove(course)
        except UserInputError as error:
            print(error)    


    def __eq__(self, other):
        return (self.code.lower() == other.code.lower())
      
    # def __str__(self):
    #     formatted_str = "Course Code: " + self.code + "\n"
    #     if not self.title == '':
    #         formatted_str += "Course Title: " + self.title + "\n"
    #     if not self.cred_points == '':
    #         formatted_str += "Credit Points: " + str(self.cred_points) + "\n"    
    #     if not self.prereq == '':
    #         # want to fix printing prerequisite courses not in list
    #         formatted_str += "Prerequisite Courses: " + str(self.prereq) + "\n" 
    #     if not self.avail == '':
    #         formatted_str += "Availability: " + self.avail + "\n"
    #     return formatted_str