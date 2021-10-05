import Program as prg
import Course as crs
import Semester as sem
import Student as st
import Admin as adm
import csv

if __name__ == '__main__':
    def student_list():
        with open('data/students.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',',)
            line_count = 0
            for row in csv_reader:
                print(f'{row[0]} is a student of {row[1]}')
                line_count += 1
        print('Done.')

    def main():
        id = str(input('Login as Admin or student?'))
        if id == adm.Admin.get_id():
            print(id)

    main()