class Admin:
    def __init__(self, adm_id, adm_name, adm_birth, adm_gender):
        self.id = adm_id
        self.name = adm_name
        self.birth = adm_birth
        self.gender = adm_gender

    def default(self, o):
        return o.__dict__
    
    def set_id(self, adm_id):
        self.id = adm_id

    def get_id(self):
        return self.id

    def set_name(self, adm_name):
        self.name = adm_name

    def get_name(self):
        return self.name

    def set_birth(self, adm_birth):
        self.birth = adm_birth

    def get_birth(self):
        return self.birth
    
    def set_gender(self, adm_gender):
        self.gender = adm_gender

    def get_gender(self):
        return self.gender
    
    def __eq__(self, other):
        return (self.name.lower() == other.name.lower())
      
    def __str__(self):
        # formatted_str = "Name: " + self.name + "\n"
        # if not self.mobile == '':
        #     formatted_str += "Mobile: " + self.mobile + "\n"
        # if not self.landline == '':
        #     formatted_str += "Landline: " + self.landline + "\n"
        # return formatted_str
        return None