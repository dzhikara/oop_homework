class Student:

  def __init__(self, name, surname, gender):
    self.name = name
    self.surname = surname
    self.gender = gender
    self.finished_courses = []
    self.courses_in_progress = []
    self.grades = {}

  def rate_lect(self, lecturer, course, grade):  # оценка лекторов
    if isinstance(lecturer,
                  Lecturer) and course in lecturer.courses_attached and (
                      course in self.courses_in_progress
                      or course in self.finished_courses):
      if course in lecturer.grades:
        lecturer.grades[course] += [grade]
      else:
        lecturer.grades[course] = [grade]
    else:
      return "Ошибка при оценке"

  def avg_grade_hw(self):  # средняя оценка за ДЗ
    total_grades = sum(sum(grades) for grades in self.grades.values())
    total_count = sum(len(grades) for grades in self.grades.values())
    return round(total_grades /
                 total_count, 1) if total_count > 0 else "Нет оценок"

  def __lt__(self, other):  # сравнение студентов по средней оценке за ДЗ
    if not isinstance(other, Student):
      print("Сравнение некорректно")
      return
    return self.avg_grade_hw() < other.avg_grade_hw()

  def __str__(self):
    courses_in_progress = ", ".join(self.courses_in_progress)
    finished_courses = ", ".join(self.finished_courses)
    res = (f"Имя: {self.name}\n"
           f"Фамилия: {self.surname}\n"
           f"Средняя оценка за домашнее задание: {self.avg_grade_hw()}\n"
           f"Курсы в процессе обучения: {courses_in_progress}\n"
           f"Завершенные курсы: {finished_courses}\n")
    return res


class Mentor:

  def __init__(self, name, surname):
    self.name = name
    self.surname = surname
    self.courses_attached = []


class Lecturer(Mentor):

  def __init__(self, name, surname):
    super().__init__(name, surname)
    self.grades = {}

  def avg_grade(self):  # средняя оценка за лекции
    total_grades = sum(sum(grades) for grades in self.grades.values())
    total_count = sum(len(grades) for grades in self.grades.values())
    return round(total_grades /
                 total_count, 1) if total_count > 0 else "Нет оценок"

  def __lt__(self, other):  # сравнение лекторов по средней оценке за лекции
    if not isinstance(other, Lecturer):
      print("Сравнение некорректно")
      return
    return self.avg_grade() < other.avg_grade()

  def __str__(self):
    res = (f"Имя: {self.name}\n"
           f"Фамилия: {self.surname}\n"
           f"Средняя оценка за лекции: {self.avg_grade()}\n")
    return res


class Reviewer(Mentor):

  def rate_hw(self, student, course,
              grade):  # проверяющий оценивает ДЗ студента
    if isinstance(student, Student) and course in self.courses_attached and (
        course in student.courses_in_progress
        or course in student.finished_courses):
      if course in student.grades:
        student.grades[course] += [grade]
      else:
        student.grades[course] = [grade]
    else:
      return "Ошибка оценки"

  def __str__(self):
    res = f"Имя: {self.name}\nФамилия: {self.surname}\n"
    return res


# студенты
student_1 = Student("Biba", "Lupa", "male")
student_1.courses_in_progress += ["Python"]
student_1.finished_courses += ["Git"]

student_2 = Student("Boba", "Pupa", "male")
student_2.courses_in_progress += ["Java"]
student_2.finished_courses += ["Git"]

# проверяющие
reviewer_1 = Reviewer("John", "Black")
reviewer_1.courses_attached += ["Python", "Java", "Git"]

reviewer_2 = Reviewer("Jack", "Brown")
reviewer_2.courses_attached += ["Python", "Java", "Git"]

# лекторы
lecturer_1 = Lecturer("James", "White")
lecturer_1.courses_attached += ["Python", "Java", "Git"]

lecturer_2 = Lecturer("Jane", "Red")
lecturer_2.courses_attached += ["Python", "Java", "Git"]

# проверяющие оценивают ДЗ студентов
reviewer_1.rate_hw(student_1, "Python", 7)
reviewer_1.rate_hw(student_1, "Git", 6)
reviewer_2.rate_hw(student_1, "Python", 8)
reviewer_2.rate_hw(student_1, "Git", 5)

reviewer_1.rate_hw(student_2, "Java", 9)
reviewer_1.rate_hw(student_2, "Git", 7)
reviewer_2.rate_hw(student_2, "Java", 6)
reviewer_2.rate_hw(student_2, "Git", 4)

# студенты оценивают лекторов
student_1.rate_lect(lecturer_1, "Python", 9)
student_1.rate_lect(lecturer_1, "Git", 6)
student_1.rate_lect(lecturer_2, "Python", 10)
student_1.rate_lect(lecturer_2, "Git", 2)

student_2.rate_lect(lecturer_1, "Java", 10)
student_2.rate_lect(lecturer_1, "Git", 8)
student_2.rate_lect(lecturer_2, "Java", 7)
student_2.rate_lect(lecturer_2, "Git", 4)

# проверка
print("Проверяющий 1:", reviewer_1, sep="\n")
print("Проверяющий 2:", reviewer_2, sep="\n")
print("Лектор 1:", lecturer_1, sep="\n")
print("Лектор 2:", lecturer_2, sep="\n")
print("Студент 1:", student_1, sep="\n")
print("Студент 2:", student_2, sep="\n")

# сравнение успеваемости студентов по средней оценке за ДЗ
if student_1 < student_2:
  print(
      f"Студент {student_2.name} {student_2.surname} имеет более высокую среднюю оценку за домашние задания."
  )
elif student_1 > student_2:
  print(
      f"Студент {student_1.name} {student_1.surname} имеет более высокую среднюю оценку за домашние задания."
  )
else:
  print(
      f"Студенты {student_1.name} и {student_2.name} имеют одинаковую среднюю оценку за домашние задания."
  )
print()

# подсчет средней оценки за ДЗ по всем студентам в рамках конкретного курса
students_list = [student_1, student_2]


def avg_grade_for_course(students_list, course):
  total_grades = 0
  total_count = 0
  for student in students_list:
    if course in student.grades:
      total_grades += sum(student.grades[course])
      total_count += len(student.grades[course])
    if (course in student.finished_courses and course not in student.grades):
      total_grades += sum(student.grades.get(course, []))
      total_count += len(student.grades.get(course, []))
  if total_count > 0:
    return round(total_grades / total_count, 1)
  else:
    return "Нет оценок"


print(
    "Средняя оценка за домашние задания по курсу Python:",
    avg_grade_for_course([student_1, student_2], "Python"),
)
print(
    "Средняя оценка за домашние задания по курсу Git:",
    avg_grade_for_course([student_1, student_2], "Git"),
)
print(
    "Средняя оценка за домашние задания по курсу Java:",
    avg_grade_for_course([student_1, student_2], "Java"),
)
print()

# подсчет средней оценки за лекции всех лекторов в рамках курса
lecturers_list = [lecturer_1, lecturer_2]


def avg_grade_lecturers(lecturers_list, course):
  total_grades = 0
  total_count = 0
  for lecturer in lecturers_list:
    if course in lecturer.grades:
      total_grades += sum(lecturer.grades[course])
      total_count += len(lecturer.grades[course])
  if total_count > 0:
    return round(total_grades / total_count, 1)
  else:
    return "Нет оценок"


print(
    "Средняя оценка за лекции по курсу Python:",
    avg_grade_lecturers([lecturer_1, lecturer_2], "Python"),
)
print(
    "Средняя оценка за лекции по курсу Git:",
    avg_grade_lecturers([lecturer_1, lecturer_2], "Git"),
)
print(
    "Средняя оценка за лекции по курсу Java:",
    avg_grade_lecturers([lecturer_1, lecturer_2], "Java"),
)
