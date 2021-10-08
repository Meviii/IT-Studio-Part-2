class Student:
    def __init__(self, stu_id, stu_name, stu_birth, stu_gender, stu_program, stu_acad_history, stu_curr_enrol, stu_study_plan):
        self.id = stu_id
        self.name = stu_name
        self.birth = stu_birth
        self.gender = stu_gender
        self.program = stu_program
        self.acad_history = stu_acad_history
        self.curr_enrol = stu_curr_enrol
        self.study_plan = stu_study_plan

    def default(self, o):
        return o.__dict__  

    def set_id(self, stu_id):
        self.id = stu_id

    def get_id(self):
        return self.id

    def set_name(self, stu_name):
        self.name = stu_name

    def get_name(self):
        return self.name

    def set_birth(self, stu_birth):
        self.birth = stu_birth

    def get_birth(self):
        return self.birth
    
    def set_gender(self, stu_gender):
        self.gender = stu_gender

    def get_gender(self):
        return self.gender

    def set_program(self, stu_program):
        self.program = stu_program

    def get_program(self):
        return self.program
    
    def set_acad_history(self, stu_acad_history):
        self.acad_history = stu_acad_history

    def get_acad_history(self):
        return self.acad_history
    
    def set_curr_enrol(self, stu_curr_enrol):
        self.curr_enrol = stu_curr_enrol

    def get_curr_enrol(self):
        return self.curr_enrol
    
    def set_study_plan(self, stu_study_plan):
        self.study_plan = stu_study_plan

    def get_study_plan(self):
        return self.study_plan

    def __eq__(self, other):
        return (self.id == other.id)
      
    def __str__(self):
        formatted_str = "Student ID: " + str(self.id) + "\n"
        if not self.name == '':
            formatted_str += "Name: " + self.name + "\n"
        if not self.program == '':
            formatted_str += "Program: " + self.program + "\n"
        return formatted_str
