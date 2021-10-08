class User:
    def __init__(self, user_id, user_name, user_mobile, user_birth, user_gender):
        self.id = user_id
        self.name = user_name
        self.mobile = user_mobile
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
    
    def set_mobile(self, user_mobile):
        self.name = user_mobile

    def get_mobile(self):
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
    def __init__(self, user_id, user_name, user_mobile, user_birth, user_gender, stu_program, stu_acad_history, stu_curr_enrol, stu_study_plan):

        User.__init__(self, user_id, user_name, user_mobile, user_birth, user_gender)
        self.program = stu_program
        self.acad_history = stu_acad_history
        self.curr_enrol = stu_curr_enrol
        self.study_plan = stu_study_plan

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

class Admin(User):
    def __init__(self, user_id, user_name, user_mobile, user_birth, user_gender, adm_role = 'Admin'):
        User.__init__(self, user_id, user_name, user_mobile, user_birth, user_gender)
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