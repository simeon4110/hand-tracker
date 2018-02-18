"""
Defines the object / DB models.
"""
from django.db import models


class Student(models.Model):
    """
    The student model.
    """
    student_name = models.TextField(max_length=30)
    acknowledged = models.IntegerField(default=0)
    modifier = models.FloatField()

    def __str__(self):
        """
        Overrides default str method to return student_name.
        :return: student_name
        """
        return self.student_name


class ClassRoom(models.Model):
    """
    Manages the running classroom. :TODO: add the delete method.
    """
    class_number = models.IntegerField()
    professor_name = models.TextField(max_length=30)
    professor_email = models.EmailField()
    student_list = models.ManyToManyField(Student)
    class_running = models.BooleanField(default=True)

    def __str__(self):
        """
        :return: class_number
        """
        return self.class_number

    def get_professor(self):
        """
        :return: professor_name
        """
        return self.professor_name

    def add_student(self, student):
        """
        Adds a student to the class_list.
        :param student: The student to add.
        :return: Nothing.
        """
        self.student_list += student

    @staticmethod
    def acknowledge(student):
        """
        :param student: the student to acknowledge.
        :return: Nothing.
        """
        student.acknowledged += 1
        student.modifier = 1
