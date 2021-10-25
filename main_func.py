import ast
import Program as prg
from Course import Course
import Semester as sem
import csv
from User import User, Student, Admin
import os
def add_to_plan(id, course_code):
    with open('data/students.csv', 'r+') as stuf:
        stu_reader = csv.reader(stuf,skipinitialspace=True)
        student =[]
        final = ''
        for lines in stu_reader:
            if lines[0] == id:
                student = [i.strip() for i in lines]
                study_plan  = ast.literal_eval(lines[7])
        
        if not course_code in study_plan: 
            study_plan.append(course_code)
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(study_plan)+'"')
        else:
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"')
    stuf.close()

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

def remove_from_plan(id, course_code):
    with open('data/students.csv', 'r+') as stuf:
        stu_reader = csv.reader(stuf,skipinitialspace=True)
        student =[]
        final = ''
        for lines in stu_reader:
            if lines[0] == id:
                student = [i.strip() for i in lines]
                study_plan  = ast.literal_eval(lines[7])
        
        if course_code in study_plan: 
            study_plan.remove(course_code)
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(study_plan)+'"')
        else:
            final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"')
    stuf.close()

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

def sem_add_count(id, stu_course, semester_code): # Adds a course to a student line by id in students.csv
    with open('data/semesters.csv', 'r+') as f, open('data/students.csv', 'r') as stuf:
        reader1 = csv.reader(stuf)
        for lines in reader1:
            if lines[0] == id:
                stu_program = lines[4]
                break

        reader = csv.reader(f)
        final = ''
        semester = []
        # read courses where stu_course == course, if course code in sem courses[1], stu_count in sem + 1
        for lines in reader:
            if str(lines[1]) == str(semester_code):
                semester = [i.strip() for i in lines]
                if lines[0] == stu_program:
                    if stu_course in semester[2]:
                        break
                    else:
                        print('Not in any semester')
                        return False
                else:
                    print('Program does not exist')
                    return False
        #SEM12021,['COS2801'],0,1000
        new_count = int(semester[3]) + 1
        final = str(semester[0]+','+semester[1] +','+ '"'+ semester[2]+'",'+ str(new_count)+ ','+ semester[4])
        f.close()

    with open('data/semesters.csv', 'r') as inf, open('data/semesters_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
        for lines in reader:
            if lines[1] == semester_code:
                writer.writerow(final.split(','))
                break
            else:
                writer.writerow(lines)
        writer.writerows(reader)

    os.remove('data/semesters.csv')
    os.rename('data/semesters_temp.csv', 'data/semesters.csv')

def sem_remove_count(id, stu_course, semester_code): # Adds a course to a student line by id in students.csv
    with open('data/semesters.csv', 'r+') as f, open('data/students.csv', 'r') as stuf:
        reader1 = csv.reader(stuf)
        for lines in reader1:
            if lines[0] == id:
                stu_program = lines[4]
                break

        reader = csv.reader(f)
        final = ''
        semester = []
        # read courses where stu_course == course, if course code in sem courses[1], stu_count in sem + 1
        for lines in reader:
            if str(lines[1]) == str(semester_code):
                semester = [i.strip() for i in lines]
                if lines[0] == stu_program:
                    if stu_course in semester[2]:
                        break
                    else:
                        print('Not in any semester')
                        return False
                else:
                    print('Program does not exist')
                    return False
        #SEM12021,['COS2801'],0,1000
        new_count = int(semester[3]) - 1
        final = str(semester[0]+','+semester[1] +','+ '"'+ semester[2]+'",'+ str(new_count)+ ','+ semester[4])
        f.close()

    with open('data/semesters.csv', 'r') as inf, open('data/semesters_temp.csv', 'w+', newline='') as outf:
        reader = csv.reader(inf, quoting=csv.QUOTE_NONE, quotechar=None)
        writer = csv.writer(outf, quoting=csv.QUOTE_NONE, quotechar=None)
        for lines in reader:
            if lines[1] == semester_code:
                writer.writerow(final.split(','))
                break
            else:
                writer.writerow(lines)
        writer.writerows(reader)

    os.remove('data/semesters.csv')
    os.rename('data/semesters_temp.csv', 'data/semesters.csv')

def course_list_by_sem(semid):
        with open('data/semesters.csv', 'r') as f:
            reader = csv.reader(f)
            sem_list = []
            specific_sem_course_name = []
            course_info = []
            for lines in reader:
                if lines[0] == semid:
                    sem_list.append(lines)
            for i in sem_list:
                course_info = ast.literal_eval(i[1])
            for i in course_info:
                specific_sem_course_name.append(i[0])
        with open('data/courses.csv', 'r') as f:
            reader = csv.reader(f)
            course_name_lst = []
            for lines in reader:
                course_name_lst.append(lines[0])

        sem_courses = set(course_name_lst).intersection(set(specific_sem_course_name))
        return sem_courses

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

def check_prereqs(id, course): # Checks if prereq is completed(passed and in acad history) by student, and returns True, else False 
    with open('data/courses.csv', 'r') as cf:
        cfreader = csv.reader(cf)
        courses = []
        course_prereqs = []
        for lines in cfreader:
            if lines[0] == course:
                courses.append(lines[3]) #appends prereqs of course 
        for i in courses:
            course_prereqs = ast.literal_eval(i) #makes prereqs of course a list
        
        if courses is None:
            print('empty')
            return True


    with open('data/students.csv', 'r') as sf:
        sfreader = csv.reader(sf)
        stu_history = []
        temp = []

        for lines in sfreader:
            if str(lines[0]) == str(id):
                temp.append(lines[5])
                
        for i in temp:
            stu_history = ast.literal_eval(i) # makes student academic history a list
        
        course_name_history = []
        for i in stu_history:
            course_name_history.append(i[0]) # makes a list for only names of courses in academic history

        z = set(course_name_history).intersection(set(course_prereqs)) # Set of intersection of course_prereqs and course_name
        
        if z is None:
            return False
        elif not z is None:
            if len(course_prereqs) == len(z):
                for i in stu_history:
                    for x in course_prereqs:
                        if str(i[0]) == str(x):
                            if i[1] >= 50:
                                return True
                            else:
                                return False
            else:
                return False

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

def open_admins_for_id(id): # Returns if id exists in admins.csv
    with open('data/admins.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                continue
        f.close()
        return False

def admin_info_list(id): # Returns all info of a specific line by id from admins.csv
    with open('data/admins.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if lines[0] == id:
                admin_lst = [i.strip() for i in lines]
            else:
                continue
        f.close()
        return admin_lst

def open_semester_for_id(sem_id): # Returns if id exists in students.csv
    with open('data/semesters.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[1]) == str(sem_id):
                return True
            else:
                continue
        f.close()
        return False

def open_students_for_id(id): # Returns if id exists in students.csv
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if str(lines[0]) == str(id):
                return True
            else:
                continue
        f.close()
        return False

def student_info_list(id): # Returns all info of a specific line by id from students.csv
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        for lines in reader:
            if lines[0] == id:
                student_lst = [i.strip() for i in lines]
            else:
                continue
        f.close()
        return student_lst

def admin_object(id): # Creates an Admin object using per info from admin_info_list(id)
    admin = Admin(admin_info_list(id)[0], admin_info_list(id)[1], admin_info_list(id)[2],
               admin_info_list(id)[3])
    return admin

def student_object(id): # Creates an Student object using per info from student_info_list(id)
    student = Student(student_info_list(id)[0], student_info_list(id)[1], student_info_list(id)[2],
               student_info_list(id)[3], student_info_list(id)[4], student_info_list(id)[5], student_info_list(id)[6])
    return student

def studentId_list(): # Returns only studentID from all students in students.csv
    with open('data/students.csv', 'r') as f:
        reader = csv.reader(f)
        studentsID_lst = []
        for lines in reader:
            studentsID_lst.append(lines[0])
    f.close()
    return studentsID_lst

def courses_name_list(): # Returns only course codes from all courses in courses.csv
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f)
        course_name_lst = []
        for lines in reader:
            course_name_lst.append(lines[0])
    f.close()
    return course_name_lst

def program_Id_list(): # Returns only course codes from all courses in courses.csv
    with open('data/programs.csv', 'r') as f:
        reader = csv.reader(f)
        programs_lst = []
        for lines in reader:
            programs_lst.append(lines[0])
    f.close()
    return programs_lst

def courses_list(): # Returns all info from each line in courses.csv (Sorted)
    with open('data/courses.csv', 'r') as f:
        reader = csv.reader(f)
        course_lst = []
        for lines in reader:
            course_lst.append(lines)
    f.close()
    return sorted(course_lst)

def add_student_course(id, stu_course, year_sem): # Adds a course to a student line by id in students.csv

    with open('data/students.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        student = []
        courses = []
        for lines in reader:
            if str(lines[0]) == str(id):
                student = [i.strip() for i in lines]
                if not stu_course in lines[6]:
                    courses = ast.literal_eval(lines[6])
                    courses.append(str(stu_course))
                    sem_add_count(id, stu_course, year_sem)
                    print(f'{stu_course} added')
                else:
                    print('Already enrolled')
                    return student_menu(id)
        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses)+'"'+','+ '"' +str(student[7])+'"')
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

def remove_course(id, stu_course): # Removes a course to a student line by id in students.csv

    with open('data/students.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        student = []
        for lines in reader:
            if lines[0] == id:
                student = [i.strip() for i in lines]
                if stu_course in lines[6]:
                    courses = ast.literal_eval(lines[6])
        courses.remove(stu_course)
        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(student[4])+',"'+ str(student[5]) +'",' + '"'+str(courses)+'"'+','+ '"' +str(student[7])+'"')
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

def remove_program(id): # Resets program of student to '' in students.csv. Cancels program

    with open('data/students.csv', 'r+') as f:
        reader = csv.reader(f)
        final = ''
        student = []
        for lines in reader:
            if lines[0] == id:
                student = [i.strip() for i in lines]
                if not lines[4] == '':
                    program = ''
                else:
                    print('You are not a part of any program')
                    return student_menu_option(id)
        final = str(str(student[0]) +','+ str(student[1])+','+ str(student[2])+','+ str(student[3])+','+ str(program)+',"'+ str(student[5]) +'",' + '"'+str(student[6])+'"'+','+ '"' +str(student[7])+'"')
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

def login(): # Login function for Admin or Student login BY ID
    try:
        login_type = str(input('Login as Admin or Student? ')).lower()

        if login_type == 'Admin'.lower(): # Needs implementation
            id = str(input('Please enter your Admin ID: '))
            print('==================================')
            if open_admins_for_id(id) == True:
                admin = admin_object(id)
                print(f'Welcome {admin.name}\n')
                admin_menu(id)
            else:
                print('Incorrect Admin ID')

        elif login_type == 'Student'.lower():
            id = str(input('Please enter your Student ID: '))
            
            print('==================================')
            if open_students_for_id(id) == True:
                student = student_object(id)

                print(f'        Welcome {student.name} \n')
                return student_menu(id)
            else:
                print('Incorrect Student ID')
        else:
            raise ValueError
    except ValueError:
        print('Incorrect selection')
        return False

def student_menu_option(id): # Allows student to return to student_menu() without ending program
    return_main = str(input('Return to main menu? Y/N \n'))
    if return_main.lower() == 'y':
        return student_menu(id)
    else:
        return False

def student_menu(id): # Student menu with choices and inner functions

    print('     *STUDENT MENU*      ')
    print()
    print('1. View your Academic History')
    print('2. View available courses') # should display courses which are not completed
    print('3. View and enrol in an offering')
    print('4. Un-enrol from an offering')
    print('5. Get all information')
    print('6. Update your Information')
    print('7. Fees')
    print('8. Cancel Program')
    print('0. Exit')
    print('==================================')

    try:
        s = student_object(id)
        choice = int(input('Please pick by index: '))
        res = set(ast.literal_eval(s.get_curr_enrol()))
        all_courses = set(courses_name_list())
        stu_courses = sorted(res.intersection(all_courses))
        s.set_curr_enrol(stu_courses)

        if 0 > choice > 8:
            raise ValueError
        elif choice == 1: # Academic History
            with open('data/students.csv', 'r') as f:
                reader = csv.reader(f)
                student = []
                for lines in reader:
                    if lines[0] == id:
                        student.append(lines)
                    else:
                        continue
                for i in student:
                    history = ast.literal_eval(i[5]) # or [i.strip() for i[5] in student]
                print('Academic History: ')
                print(f'    {s.get_program()}: ')
                for c in history:
                    print(f'        Course: {c[0]}, Mark: {c[1]}')
                f.close()
            student_menu_option(id)
        elif choice == 2: # Available Courses to enroll into
            print('All available courses for you are: ')
            
            print('Sem 1: ')
            for i in filtered_courses_list(id):
                if 'S1' in i[4]:
                    print(f'{i[1]}, Semester: {i[4]}')
            print('Sem 2: ')
            for i in filtered_courses_list(id):
                if 'S2' in i[4]:
                    print(f'{i[1]}, Semester: {i[4]}')
            print()
            student_menu_option(id)
        elif choice == 3: # View current enrollments, add course
                print('You are currently enrolled in: \n')
                for i in courses_list():
                    if i[0] in s.get_curr_enrol():
                        print(f'{i[0]}: {i[1]}')
                print()
                selection = str(input('Would you like to add a course? Y/N \n'))
                if selection.lower() == 'n':
                    student_menu_option(id)
                elif selection.lower() == 'y':
                    year_sem = str(input('Which sem would you like to enrol into? SEM12021/SEM22021/SEM12022/SEM22022\n'))
                    if open_semester_for_id(year_sem) == True:
                        count = 1
                        for i in courses_list():
                            print(f'{count}. {i[0]}: {i[1]}, Credit: {i[2]}\n')
                            count += 1
                        selection = int(input('Enter the index you would like to add. 0 to exit\n'))
                        if selection == 0:
                            return student_menu(id)
                        else:
                            curr_enrolment = s.get_curr_enrol()
                            for x, value in enumerate(sorted(courses_list()),1):
                                if int(selection) == int(x):
                                    if check_prereqs(id, value[0]) == True or check_prereq_empty(value[0]) == True:
                                        remove_from_plan(id, value[0])
                                        add_student_course(id, value[0], year_sem)
                                        return student_menu_option(id)
                                    elif check_prereqs(id, value[0]) == False:
                                        print('You do not meet the requirments\n')
                                        return student_menu(id)
                                    else:
                                        print('Uknown Error')
                    else:
                        print('Invalid Semester')
                        return student_menu(id)
        elif choice == 4: # View current enrollments, drop course
            print('Enrolled courses: \n')
            count = 1
            for i in courses_list():
                if i[0] in s.get_curr_enrol():
                    print(f'{count}. {i[0]}: {i[1]}')
                    count += 1
            year_sem = str(input('Which course sem would you like to drop? SEM12021/SEM22021/SEM12022/SEM22022\n'))
            if open_semester_for_id(year_sem) == True:
                selection = int(input(("Enter the index you would like to drop. 0 to exit \n")))
                for x, value in enumerate(sorted(stu_courses),1):
                    if selection == int(x):
                        print(f'{value} dropped.')
                        curr_enrolment = s.get_curr_enrol()
                        for i in curr_enrolment:
                            if str(i) == str(value):
                                curr_enrolment.remove(i)
                                sem_remove_count(id, i, year_sem)
                                add_to_plan(id, i)
                                remove_course(id, i)
                                break
                        student_menu_option(id)
                    elif selection == 0:
                        return student_menu(id)
                    else:
                        print('Error')
                        return False
            else:
                print('Incorrect Semester')
                return student_menu(id)
            print()            
        elif choice == 5: # View all personal information
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
            print()
            student_menu_option(id)
        elif choice == 6: # Update personal information
            update_sel = int(input('Which detail would you like to update?\n'))
            print('Please enter one of the following: ')
            print('1. Name\n2. Birth\n3. Gender\n')
            if not update_sel.isdigit():
                raise ValueError
            else:
                if update_sel == 1:
                    pass
                if update_sel == 2:
                    pass
                if update_sel == 3:
                    pass
            #student_menu_option(id)
        elif choice == 7: # View Fees
            print()
            print('The fees for your current enrollment is: \n')
            if not s.get_curr_enrol() is None:
                fees_total = 0
                for i in courses_list():
                    if i[0] in s.get_curr_enrol():
                        print(f'{i[0]}: {i[1]} Fee: ${i[5]}')
                        fees_total += int(i[5])
                print()
                print(f'Total: ${fees_total}')
                print()
                student_menu_option(id)
            else:
                return student_menu(id)
        elif choice == 8: # Cancel program
            print(f'You are currently a student of {s.get_program()}. Do you want to cancel this? Y/N')
            program_update = str(input())
            if program_update.lower() == 'y':
                s.set_program('')
                # read line of id
                # if s.getprogram in line:
                # edit the program to ''
                with open('data/students.csv', 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        if lines[0] == id:
                            #fix
                            pass
                        else:
                            continue
                    f.close()
                print(f'You have been removed from the program.\n')
                student_menu_option(id)
            elif program_update.lower() == 'n':
                return student_menu(id)
            else:
                raise ValueError
        else:
            return -1
    except ValueError:
        print('Invalid selection')
        return False

def admin_menu(id): # Admin menu with choices and inner functions

    print('     *ADMIN MENU*      ')
    print('1. Add/Remove/Amend Student')
    print('2. Add/Remove/Amend Course')
    print('3. Add/Remove/Amend Program')
    print('4. Add/Remove/Amend Semester')
    print('5. View student information')
    print('6. Amend Study plan for student')
    print('7. Validate student study plan')
    print('8. Generate study plan for student')
    print('9. View all students achievements of course')
    print('0. Exit')
    print('=======================')
    
    try:
        choice = int(input('Please pick by index: '))
        unknown_choice = print("Please type 'Add', 'Remove' or 'Ammend' then hit Enter")
        if 0 > choice > 5:
            raise ValueError
        elif choice == 1:
            print(choice)
            student_choice = input("Would you like to Add, Remove or Ammend Student")
            if student_choice.lower() == "add":
                with open('data/students.csv', 'a') as f:
                    new_studentID = input("Enter Student ID: ")
                    new_studentName = input("Enter Student Name: ")
                    new_studentDOB = input("Enter Student Date of Birth: ")
                    new_studentGender = input("Enter Student Gender: ")
                    new_studentProgram = input("Enter Student Program: ")
                    new_studentEnrolled = input("Enter Course Enrolled: ")
                    writer = csv.writer(f)
                    writer.writerow([new_studentID, new_studentName, new_studentDOB, new_studentGender, new_studentProgram, [], new_studentEnrolled, []])
                f.close()
            elif student_choice.lower() == "remove":
                deleted_studentID = input("Enter Student ID to be Removed: ")
                with open('data/students.csv', 'r+') as f:
                    reader = csv.reader(f)
                    students = []
                    for lines in reader:
                        if lines[0] != deleted_studentID:
                            students.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/students_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in students:
                        writer.writerow(i) #write the new students list into a temp csv file


                #swap the outdated csv with the updated students.csv
                os.remove('data/students.csv')
                os.rename('data/students_temp.csv', 'data/students.csv') 
                
            elif student_choice.lower() == "ammend":
                # show admin what is currently in the students.csv
                with open("data/students.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        print(lines)
                f.close()

                with open("data/students.csv", 'r') as inf, open("data/students.csv", 'w') as outf:
                    reader = csv.reader(inf)
                    writer = csv.writer(outf)
                    ammend_student = input("Select which Student you would like to Ammend by entering the Student ID: ")
                    for lines in reader:
                        if ammend_student not in studentId_list(): #if trying to ammend a student that is not already in the file
                            print("Please Enter a Valid Student ID: ")
                        else:
                            ammend_choice = input("What would you like to change? (Student ID / Student Name / Student DOB / Student Gender / Student Program / Student History / Student Enrolled Course / Student Study Plan)")
                            if ammend_choice.lower() == "student id":
                                upd_StudentID = input("What would you like to change this Student's Student ID to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuID_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuID_lst.append(lines)
                                        else:
                                            lines[0] = upd_StudentID
                                            upd_stuID_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuID_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student name":
                                upd_stuName = input("What would you like to change this Student's Name to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuName_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuName_lst.append(lines)
                                        else:
                                            lines[1] = upd_stuName
                                            upd_stuName_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuName_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student dob":
                                upd_stuDOB = input("What would you like to change this Student's Name to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuDOB_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuDOB_lst.append(lines)
                                        else:
                                            lines[2] = upd_stuDOB
                                            upd_stuDOB_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuDOB_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student gender":
                                upd_stuGend = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuGend_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuGend_lst.append(lines)
                                        else:
                                            lines[3] = upd_stuGend
                                            upd_stuGend_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuGend_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student program":
                                upd_stuProg = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuProg_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuProg_lst.append(lines)
                                        else:
                                            lines[4] = upd_stuProg
                                            upd_stuProg_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuProg_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student history":
                                upd_stuHist = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuHist_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuHist_lst.append(lines)
                                        else:
                                            lines[5] = upd_stuHist
                                            upd_stuHist_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuHist_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student enrolled course":
                                upd_stuEnrol = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuEnrol_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuEnrol_lst.append(lines)
                                        else:
                                            lines[6] = upd_stuEnrol
                                            upd_stuEnrol_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuEnrol_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            elif ammend_choice.lower() == "student study plan":
                                upd_stuStudPlan = input("What would you like to change this Student's Gender to? ") 
                                with open("data/students.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    upd_stuStudPlan_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_student:
                                            upd_stuStudPlan_lst.append(lines)
                                        else:
                                            lines[7] = upd_stuStudPlan
                                            upd_stuStudPlan_lst.append(lines)
                                    
                                    with open('data/students_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in upd_stuStudPlan_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/students.csv')
                                    os.rename('data/students_temp.csv', 'data/students.csv')

                            else:
                                print("Please Enter Valid Choice (Student ID / Student Name / Student DOB / Student Gender / Student Program / Student History / Student Enrolled Course / Student Study Plan)")


            else:
                unknown_choice

        elif choice == 2:
            print(choice)
            course_choice = input("Would you like to Add, Remove or Ammend Course")
            if course_choice.lower() == "add":
                with open('data/courses.csv', 'a') as f:
                    new_courseID = input("Enter New Course ID: ")
                    new_courseName = input("Enter New Course Name: ")
                    new_CourseCred = input("Enter Course Credit: ")
                    new_CoursePrereq = input("Enter Course Prerequisites: ")
                    new_CourseAvail = input("Enter Course Availability: ")
                    new_CourseFee = input("Enter Course Fees: ")
                    writer = csv.writer(f)
                    writer.writerow([new_courseID, new_courseName, new_CourseCred, new_CoursePrereq, new_CourseAvail, new_CourseFee])
                f.close()

            elif course_choice.lower() == "remove":
                deleted_course = input("Enter Course Code of Course to be deleted: ")
                with open('data/courses.csv', 'r+') as f:
                    reader = csv.reader(f)
                    courses = []
                    for lines in reader:
                        if lines[0] != deleted_course:
                            courses.append(lines) #appends courses to a list, excluding the specified one 

                f.close()

                with open('data/courses_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in courses:
                        writer.writerow(i) #write the new course list into a temp csv file

                #swaps the outdated courses.csv file with the updated one
                os.remove('data/courses.csv')
                os.rename('data/courses_temp.csv', 'data/courses.csv')
            elif course_choice.lower() == "ammend":
                # show admin what is currently in the courses.csv
                with open("data/courses.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        print(lines)
                f.close()

                with open("data/courses.csv", 'r') as f:
                    reader = csv.reader(f)
                    ammend_course = input("Select which Course you would like to Ammend by entering the Course Code: ")
                    for lines in reader:
                        if ammend_course not in courses_name_list(): #if trying to ammend a student that is not already in the file
                            input("Please Enter a Valid Student ID: ")
                        else:
                            ammend_choice = input("What would you like to change? (Course Code / Course Name / Course Credit / Course Prerequisites / Course Availability / Course Fees) ")
                            if ammend_choice.lower() == "course code":
                                changed_code = input("What would you like to change the Course Code to? ") 
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    crs_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            crs_lst.append(lines)
                                        else:
                                            lines[0] = changed_code
                                            crs_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in crs_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course name":
                                changed_cname = input("What would you like to change the Course Name to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cname_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cname_lst.append(lines)
                                        else:
                                            lines[1] = changed_cname
                                            cname_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cname_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course credit":
                                changed_credit = input("What would you like to change the Course Credit to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    ccredit_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            ccredit_lst.append(lines)
                                        else:
                                            lines[2] = changed_credit
                                            ccredit_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in ccredit_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course prerequisite":
                                changed_prereq = input("What would you like to change the Prerequisites to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprereq_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cprereq_lst.append(lines)
                                        else:
                                            lines[3] = changed_prereq
                                            cprereq_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprereq_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course availability":
                                changed_avail = input("What would you like to change the Course Availability to? ")
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cavail_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cavail_lst.append(lines)
                                        else:
                                            lines[4] = changed_avail
                                            cavail_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cavail_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            elif ammend_choice.lower() == "course fees":
                                changed_fee = input("What would you like to change the Course Fees to? ") 
                                with open("data/courses.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cfees_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_course:
                                            cfees_lst.append(lines)
                                        else:
                                            lines[5] = changed_fee
                                            cfees_lst.append(lines)
                                    
                                    with open('data/courses_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cfees_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/courses.csv')
                                    os.rename('data/courses_temp.csv', 'data/courses.csv') 
                                    
                            else:
                                print("Please Enter Valid Choice (Course Code / Course Name / Course Credit / Course Prerequisites / Course Availability / Course Fees)")

            else:
                unknown_choice
            
        elif choice == 3:
            print(choice)
            program_choice = input("Would you like to Add, Remove or Ammend Program")
            if program_choice.lower() == "add":
                with open('data/programs.csv', 'a') as f:
                    new_progID = input("Enter New Program ID: ")
                    new_progName = input("Enter New Program Name: ")
                    new_progCred = input("Enter Program Credit Points: ")
                    new_progCourse = input("Enter Program Courses: ")
                    writer = csv.writer(f)
                    writer.writerow([new_progID, new_progName, new_progCred, new_progCourse])
                f.close()

            elif program_choice.lower() == "remove":
                deleted_Program = input("Enter Program Name to be Removed: ")
                with open('data/programs.csv', 'r+') as f:
                    reader = csv.reader(f)
                    programs = []
                    for lines in reader:
                        if lines[0] != deleted_Program:
                            programs.append(lines) #appends students to a list, excluding the specified one 
                f.close()

                with open('data/programs_temp.csv', 'w+', newline='') as f:
                    writer = csv.writer(f)
                    for i in programs:
                        writer.writerow(i) #write the new students list into a temp csv file


                #swap the outdated csv with the updated students.csv
                os.remove('data/programs.csv')
                os.rename('data/programs_temp.csv', 'data/programs.csv') 
                
            elif program_choice.lower() == "ammend":
                # show admin what is currently in the programs.csv
                with open("data/programs.csv", 'r') as f:
                    reader = csv.reader(f)
                    for lines in reader:
                        print(lines)
                f.close()
                
                with open("data/programs.csv", 'r') as inf, open("data/programs.csv", 'w') as outf:
                    reader = csv.reader(inf)
                    writer = csv.writer(outf)
                    ammend_programs = input("Select which Course you would like to Ammend by entering the Course Code: ")
                    for lines in reader:
                        if ammend_programs not in program_Id_list(): #if trying to ammend a student that is not already in the file
                            print("Please Enter a Program Name: ")
                        else:
                            ammend_choice = input("What would you like to change? (Program Name)")
                            if ammend_choice.lower() == "program id":
                                changed_progId = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogId_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogId_lst.append(lines)
                                        else:
                                            lines[0] = changed_progId
                                            cprogId_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogId_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                            elif ammend_choice.lower() == "program name":
                                changed_progName = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogName_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogName_lst.append(lines)
                                        else:
                                            lines[1] = changed_progName
                                            cprogName_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogName_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                            elif ammend_choice.lower() == "program credit points":
                                changed_progCred = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogCred_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogCred_lst.append(lines)
                                        else:
                                            lines[2] = changed_progCred
                                            cprogCred_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogCred_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 

                            elif ammend_choice.lower() == "program courses":
                                changed_progCourse = input("What would you like to change the Course Fees to? ") 
                                with open("data/programs.csv", 'r') as f:
                                    reader = csv.reader(f)
                                    cprogCourse_lst = []
                                    for lines in reader:
                                        if lines[0] != ammend_programs:
                                            cprogCourse_lst.append(lines)
                                        else:
                                            lines[3] = changed_progCourse 
                                            cprogCourse_lst.append(lines)
                                    
                                    with open('data/programs_temp.csv', 'w+', newline='') as f:
                                        writer = csv.writer(f)
                                        for i in cprogCourse_lst:
                                            writer.writerow(i) #write the new students list into a temp csv file

                                    os.remove('data/programs.csv')
                                    os.rename('data/programs_temp.csv', 'data/programs.csv') 
                                    
                            else:
                                print("Please Enter Valid Choice (Program Name)")
                
            else:
                unknown_choice

        elif choice == 4:
            print(choice)
            semester_choice = input("Would you like to Add, Remove or Ammend Semester")
            if semester_choice.lower() == "add":
                #remove studentadd
                print(10)
            elif semester_choice.lower() == "remove":
                #remove student
                print(11)
            elif semester_choice.lower() == "ammend":
                #ammend  studentsd
                print(12)
            else:
                unknown_choice
    
        elif choice == 5:
            s = student_object(id)
            print(f'ID: {s.id}\nName: {s.name}\nBirth: {s.birth}\nGender: {s.gender}\nProgram: {s.program}')
        else:
            return -1
    except ValueError:
        print('Invalid index')

