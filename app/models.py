"""
Defines the object / DB models.
"""
from django.db import models


class ClassRoom(models.Model):
    """
    Manages the running classroom. :TODO: add the delete method.
    """
    class_number = models.IntegerField()
    professor_name = models.TextField(max_length=30)
    professor_email = models.EmailField()
    class_running = models.BooleanField(default=True)

    def __str__(self):
        return self.class_number

    @property
    def is_running(self):
        return self.class_running

    @property
    def group_name(self):
        return "room-%s" % self.class_number

    @staticmethod
    def acknowledge(student):
        """
        :param student: the student to acknowledge.
        :return: Nothing.
        """
        student.acknowledged += 1
        student.modifier = 1


class Student(models.Model):
    """
    The student model.
    """
    student_name = models.TextField(max_length=30)
    acknowledged = models.IntegerField(default=0)
    modifier = models.FloatField()
    class_room = models.ForeignKey(ClassRoom,
                                   on_delete=models.CASCADE)
    hand = models.BooleanField(default=False)

    def __str__(self):
        """
        Overrides default str method to return student_name.
        :return: student_name
        """
        return self.student_name
