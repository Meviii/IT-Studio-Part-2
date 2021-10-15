
# Course Class: 
# Constructor, string methods, getter and setters, methods to add or remove prereqs and available sems
# UserInputError(Exception) class used
# TO DO - want to fix printing prerequisite courses not in list
# TO CONFIRM: set_code - Whether the system will check for 4 char then 4 ints

class UserInputError(Exception):
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

class Course:
    def __init__(self, crs_code, crs_title, crs_cred_points, crs_prereq, crs_avail):
        self.code = crs_code
        self.title = crs_title
        self.cred_points = crs_cred_points
        self.prereq = crs_prereq
        self.avail = crs_avail

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
                raise UserInputError ('Please enter a course title. Cannot be blank')
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
        return self.crs_avail

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
        

It_Studio2 = Course('COSC2800', 'IT STUDIO 2', '24', 'NA', 'S1 & S2' )
print(It_Studio2)

# test set_title
crs_title = str(input("Name of Course Code. (Cannot be blank): "))
It_Studio2.set_title(crs_title)
print('\nName of course is:', It_Studio2.get_title(), ' \n')

# test set_code
crs_code = str(input("Set Course Code. (Four letters then Four numbers): "))
It_Studio2.set_code(crs_code)
print('\nName of course is:', It_Studio2.get_code(), ' \n')

# test set_cred_points
crs_cred_points = str(input("Set Credit Points. (Please enter either 12 or 24): "))
It_Studio2.set_cred_points(crs_cred_points)
print('\nCourse is now set to:', It_Studio2.get_cred_points(), 'pts \n')

# test set_prereq
crs_prereq = str(input("Set Prerequisite for Course. (Seperate by comma or NA for none): "))
It_Studio2.set_prereq(crs_prereq)
print('\nPrereqs for course are:', It_Studio2.get_prereq(),'\n')

# test set_avail
crs_avail = str(input("Semester Availability of course: (Semester 1 'S1', Semester 2 'S2' or both 'S1 & S2'):"))
It_Studio2.set_avail(crs_avail)
print('\nAvailability for course are:', It_Studio2.get_prereq(), '\n')

print(It_Studio2)