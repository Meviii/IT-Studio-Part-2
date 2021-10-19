class Program:
    def __init__(self, prg_code, prg_credit_points, prg_courses):
        self.code = prg_code
        self.title = prg_credit_points
        self.credit = prg_courses

    def default(self, o):
        return o.__dict__  

    def set_code(self, prg_code):
        self.code = prg_code

    def get_code(self):
        return self.code

    def set_title(self, prg_credit_points):
        self.credit_points = prg_credit_points

    def get_title(self):
        return self.credit_points

    def set_credit(self, prg_courses):
        self.courses = prg_courses

    def get_credit(self):
        return self.courses

    def __eq__(self, other):
        return (self.code.lower() == other.code.lower())
      
    def __str__(self):
        return None

