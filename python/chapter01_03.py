# Chapter01-3
# 파이썬 심화
# 클래스 메소드, 인스턴스 메소드 스테틱 메소드

# 기본 인스턴스 메소드

class Student(object):
    '''
    Student Class
    Author : Kim
    Date : 2020.11.27
    Description : Class, Static, Instance Method
    '''

    # Class Variable
    tuition_per = 1.0

    def __init__(self, id, first_name, last_name, email, grade, tuition, gpa):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._grade = grade
        self._tuition = tuition
        self._gpa = gpa

    # Instance Method
    def full_name(self):
        return '{}, {}'.format(self._first_name, self._last_name)

    # Instance Method
    def detail_info(self):
        return 'Student Detail Info : {}, {}, {}, {}, {}, {}'.format(self._id, self.full_name(), self._email, self._grade, self._tuition, self._gpa)

    # Instance Method
    def get_fee(self):
        return 'Before Tuition -> Id : {}, fee : {}'.format(self._id, self._tuition)

    # Instance Method
    def get_fee_calc(self):
        return 'After tuition -> Id : {}, fee : {}'.format(self._id, self._tuition * Student.tuition_per)

    # Instance Method
    def __str__(self):
        return 'Student Info -> name : {}, grade : {}, email : {}'.format(self.full_name(), self._grade, self._gpa)

    # Class method
    @classmethod
    def raise_fee(cls, per):
        if per < 1:
            print('Please Enter 1 or More')
            return
        cls.tuition_per = per
        print('Succed! tuition increased')


student_1 = Student(1, 'Kim', 'Sarang', 'student1@naver.com', '1', 400, 3.5)
student_2 = Student(2, 'Lee', 'Myungho', 'student2@daum.net', '2', 500, 4.3)

# 기본정보
print(student_1.__dict__)
print(student_2.__str__)

print()

# 전체 정보
print(student_1.detail_info())
print(student_2.detail_info())

# 학비 정보 (인상전)
print(student_1.get_fee())
print(student_2.get_fee())

print()

# 학비 인상(클래스 메소드 미사용)
# Student.tuition_per = 1.2

# 학비 인상(클래스 메소드 사용)
Student.raise_fee(1.5)

# 학비 정보 (인상후)
print(student_1.get_fee_calc())
print(student_2.get_fee_calc())








