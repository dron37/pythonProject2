class Student:
    def __init__(self, name: str, surname: str, gender: str):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        courses_in_progress = ', '.join(course for course in self.courses_in_progress)
        finished_courses = ', '.join(course for course in self.finished_courses)
        avg = self.__avg_grades_hw()
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
        if not self.grades:
            return 0
        rates_list = [item for grade in self.grades.values() for item in grade]
        return sum(rates_list) / len(rates_list)

    def __lt__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка' #Возвращаем сообщение об ошибке
        return self.__avg_grades_hw() < other.__avg_grades_hw()

    def __le__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка'
        return self.__avg_grades_hw() <= other.__avg_grades_hw()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return 'Ошибка'
        return self.__avg_grades_hw() == other.__avg_grades_hw()


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
        if not self.grades:
            return 0
        rates_list = [item for grade in self.grades.values() for item in grade]
        return sum(rates_list) / len(rates_list)

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        return self.__avg_grades_lecture() < other.__avg_grades_lecture()

    def __le__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        return self.__avg_grades_lecture() <= other.__avg_grades_lecture()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return 'Ошибка'
        return self.__avg_grades_lecture() == other.__avg_grades_lecture()

class Reviewer(Mentor):
    def rate_hw(self, student: object, course: str, grade: int):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def avg_rate_persons(persons, course):
    if not isinstance(persons, list):
        return "Not list"
    person_grades = [] #Определяемпустойсписок, кудабудемскладыватьоценки (обычная переменная без `self`)
    for person in persons:
        person_grades.extend(person.grades.get(course, [])) #Используя extend, добавляем оценки в список. Также используем метод get к словарю с оценками с дефолтным значением [], чтобы исключить ошибку в случае, если студент еще не получал оценок по данному курсу
    if not person_grades: #Проверям не пустой ли список
        return "По такому курсу ни у кого нет оценок"
    return round(sum(person_grades) / len(person_grades), 2)#Сумму оценок списка делим на длину списка (для этого используем "sum" и "len"), 2)


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

    print(f'\nCредняя оценка студентов по курсу Python:')
    print(avg_rate_persons([student_1, student_2], 'Python'))

    print(f'\nCредняя оценка лекторов по курсу Python:')
    print(avg_rate_persons([lecture_1, lecture_2], 'Python'))

    print(f'\nСравнение средней оценки студентов')
    print(student_1 > student_2)
    print(f'\nСравнение средней оценки лекторов')
    print(lecture_1 < lecture_2)