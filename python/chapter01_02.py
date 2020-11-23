# Chapter01-2
# 파이썬 심화
# 객체 지향 프로그래밍(OOP) -> 코드의 재사용, 코드 중복 방지 등
# 클래스 상세 설명
# 클래스 변수, 인스턴스 변수

# 클래스 재 선언
class Student():
    """
    Student Class
    Author : Jack
    Date : 2020.11.23
    """

    # 클래스 변수
    student_count = 0

    def __init__(self, name, number, grade, details, email=None):
        # 인스턴스 변수
        self._name = name
        self._number = number
        self._grade = grade
        self._details = details
        self._email = email

        Student.student_count += 1

    def __str__(self):
        return 'str {}'.format(self._name)

    def __repr__(self):
        return 'repr {}'.format(self._name)

    def detail_info(self):
        print('Current Id : {}'.format(id(self)))
        print('Student Detail Info : {} {} {}'.format(self._name, self._email, self._details))

    def __del__(self):
        Student.student_count -= 1


# Self 의미
student1 = Student('Cho', 2, 3, {'gender' : 'Male', 'Score1' : 65, 'Score2' : 44})
student2 = Student('Chang', 2, 3, {'gender' : 'Female', 'Score1' : 85, 'Score2' : 74}, 'student2@naver.com')

print(id(student1))
print(id(student2))

a = 'ABC'
b = a


print(student1._name == student2._name)
print(student1 is student2)

print(a is b)
print(a == b)

# dir & __dict__ 확인

print(dir(student1))
print(dir(student2))

print()
print()

print(student1.__dict__)
print(student2.__dict__)

# doctring
print(Student.__doc__)
print()

# 실행
student1.detail_info()
student2.detail_info()

# 에러
Student.detail_info()









