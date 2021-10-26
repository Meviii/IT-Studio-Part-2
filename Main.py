import csv
import main_func
import os
from User import User, Student, Admin
from Course import *
from Program import *
from Semester import *
if __name__ == '__main__':

    def remove_program(id='s123'): # Removed enrolled courses and study plan, changed program to 'NA'

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
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(program)+',"'+ str(student[5]) +'",' + '"[]"'+','+ '"[]"')
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

    #Student.curr_gpa_stu(id='s123')
    main_func.login()