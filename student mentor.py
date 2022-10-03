class Student:
    def __init__(self, name: str, surname: str, gender: str):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        avg = self.__avg_grades_hw()
        courses_in_progress = ', '.join(course for course in self.courses_in_progress)
        finished_courses = ', '.join(course for course in self.finished_courses)

        return f'Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за домашние задания: {avg:.1f}\n' \
               f'Курсы в процессе изучения: {courses_in_progress}\nЗавершенные курсы: {finished_courses}'

    def rate_lecture(self, lecturer: object, course: str, grade: int):
        if (isinstance(lecturer, Lecturer) and
                course in lecturer.courses_attached and
                course in self.courses_in_progress):
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __avg_grades_hw(self) -> float:
        """Вычисление средней оценки за домашние задания"""
        rates_list = [item for grade in self.grades.values() for item in grade]
        self.avg = sum(rates_list) / len(rates_list)

        return self.avg


class Mentor:
    def __init__(self, name: str, surname: str):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


class Lecturer(Mentor):
    def __init__(self, name: str, surname: str):
        Mentor.__init__(self, name, surname)
        self.grades = {}

    def __str__(self) -> str:
        avg = self.__avg_grades_lecture()
        return Mentor.__str__(self) + f'\nСредняя оценка за лекции : {avg:.1f}'

    def __avg_grades_lecture(self) -> float:
        rates_list = [item for grade in self.grades.values() for item in grade]
        self.avg = float(sum(rates_list) / len(rates_list))

        return self.avg

class Reviewer(Mentor):
    def rate_hw(self, student: object, course: str, grade: int):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def avg_rate_students(obj_list: list, course: str) -> dict:
    """Подсчитывает среднюю оценку на определенном курсе"""
    avg_students = {}

    for obj in obj_list:
        if isinstance(obj, Student) and course in obj.courses_in_progress and course in obj.grades:
            avg_rate_hw = sum(obj.grades[course]) / len(obj.grades[course])
            avg_students[f'{obj.name} {obj.surname}'] = avg_rate_hw

    return avg_students


def avg_rate_lecturers(obj_list: list, course: str) -> dict:
    """Подсчитывает среднюю оценку на определенном курсе"""
    avg_lectures = {}

    for obj in obj_list:
        if isinstance(obj, Lecturer) and course in obj.courses_attached and course in obj.grades:
            avg_rate_lecture = sum(obj.grades[course]) / len(obj.grades[course])
            avg_lectures[f'{obj.name} {obj.surname}'] = avg_rate_lecture

    return avg_lectures


if __name__ == '__main__':
    student_1 = Student(name='Aleksandr', surname='Petrov', gender='Male')
    student_2 = Student(name='Anna', surname='Fedina', gender='Female')

    student_1.courses_in_progress += ['Python', 'Git']
    student_1.finished_courses += ['Basics of HTML and CSS']
    student_2.courses_in_progress += ['Python']
    student_2.finished_courses += ['Git']

    lecture_1 = Lecturer(name='Kike', surname='Romero')
    lecture_2 = Lecturer(name='Ien', surname='Stoltenberg')

    lecture_1.courses_attached += ['Python']
    lecture_2.courses_attached += ['Git']

    reviewer_1 = Reviewer(name='Tom', surname='Klark')
    reviewer_2 = Reviewer(name='Fedor', surname='Ivanov')

    reviewer_1.courses_attached += ['Python']
    reviewer_2.courses_attached += ['Python', 'Git']

    student_1.rate_lecture(lecture_1, 'Python', 10)
    student_1.rate_lecture(lecture_2, 'Git', 10)

    student_2.rate_lecture(lecture_1, 'Python', 8)
    student_2.rate_lecture(lecture_2, 'Git', 1)

    reviewer_1.rate_hw(student_1, 'Python', 10)
    reviewer_2.rate_hw(student_1, 'Git', 9)
    reviewer_1.rate_hw(student_2, 'Python', 10)
    reviewer_1.rate_hw(student_2, 'Python', 9)

    print('Студенты:')
    print(student_1)
    print(f'\n{student_2}')

    print('-' * 20)

    print('Лекторы:')
    print(lecture_1)
    print(f'\n{lecture_2}')

    print('-' * 20)

    print('Проверяющие:')
    print(reviewer_1)
    print(f'\n{reviewer_2}')

    print(f'\nВывод средней оценки студентов по курсу Python:')
    avg_rates_students = avg_rate_students([student_1, student_2], 'Python')
    for k, v in avg_rates_students.items():
        print(f'Средняя оценка по курсу Python студента {k} - {v:.1f}')

    print(f'\nВывод средней оценки лекторов по курсу Python:')
    avg_rates_lectures = avg_rate_lecturers([lecture_1, lecture_2], 'Python')
    for k, v in avg_rates_lectures.items():
        print(f'Средняя оценка у лектора {k} в рамках курса Python - {v:.1f}')


