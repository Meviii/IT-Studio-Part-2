class Course:
    def __init__(self, crs_code, crs_title, crs_credit, crs_cred_points, crs_prereq, crs_avail):
        self.code = crs_code
        self.title = crs_title
        self.credit = crs_credit
        self.cred_points = crs_cred_points
        self.prereq = crs_prereq
        self.avail = crs_avail

    def default(self, o):
        return o.__dict__  

    def set_code(self, crs_code):
        self.code = crs_code

    def get_code(self):
        return self.code

    def set_title(self, crs_title):
        self.title = crs_title

    def get_title(self):
        return self.title

    def set_credit(self, crs_credit):
        self.credit = crs_credit

    def get_credit(self):
        return self.code
    
    def set_cred_points(self, crs_cred_points):
        self.cred_points = crs_cred_points

    def get_cred_points(self):
        return self.cred_points

    def set_prereq(self, crs_prereq):
        self.prereq = crs_prereq

    def get_prereq(self):
        return self.prereq
    
    def set_avail(self, crs_avail):
        self.avail = crs_avail

    def get_avail(self):
        return self.cred_points

    def __eq__(self, other):
        return (self.title.lower() == other.title.lower())
      
    def __str__(self):
        # formatted_str = "Name: " + self.name + "\n"
        # if not self.mobile == '':
        #     formatted_str += "Mobile: " + self.mobile + "\n"
        # if not self.landline == '':
        #     formatted_str += "Landline: " + self.landline + "\n"
        # return formatted_str
        return None