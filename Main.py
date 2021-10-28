import csv
import main_func
import os
from User import User, Student, Admin
from Course import *
from Program import *
from Semester import *

# Project start date - end date: 04/10/2021 - 30/10/2021
# Mevlut Saluk, S3717696
# Alexander Tan, S3849729
# Dion Tartaglione, S3239216
# Cesar Jude Quitazol, S3844561
# Haotian Shen, S3770488

# Program Description: Enrollment system with 3 menus: Login, Student, Admin. Each menu has its own features.

if __name__ == '__main__':

    #Student.stu_failed_couses(id='s123')
    #Admin.achievement_by_course(course='MATH2411')
    #print(Course.courses_name_list())
    #Student.course_progress_stu(id='s123')
    main_func.login()