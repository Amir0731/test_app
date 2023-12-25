from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    avatar = models.ImageField(default='default_user_ava.png')


class Teacher(models.Model):
    user = models.ForeignKey(to='User', related_name='teacher', on_delete=models.CASCADE)
    subject = models.ForeignKey(to='Subject', related_name='teacher', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.subject}'


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Variant(models.Model):
    title = models.CharField(max_length=200)
    subject_id = models.ForeignKey(to=Subject, related_name='variants', on_delete=models.CASCADE)
    teacher = models.ForeignKey(to='Teacher', related_name='variants', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    text = models.TextField()
    variant = models.ForeignKey(to=Variant, related_name='exercises', on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    class AnswerOption(models.TextChoices):
        A = "A", _('A variant')
        B = "B", _('B variant')
        C = "C", _('C variant')
        D = "D", _('D variant')

    option = models.CharField(max_length=1, choices=AnswerOption.choices)
    text = models.TextField()
    is_True = models.BooleanField(default=False)
    exercise = models.ForeignKey(to=Exercise, related_name='answer', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.option}) {self.text}'


# select form qilish
"""
class Student(models.Model):
    class YearInSchool(models.TextChoices):
        FRESHMAN = "FR", _("Freshman")
        SOPHOMORE = "SO", _("Sophomore")
        JUNIOR = "JR", _("Junior")
        SENIOR = "SR", _("Senior")
        GRADUATE = "GR", _("Graduate")

    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {
            self.YearInSchool.JUNIOR,
            self.YearInSchool.SENIOR,
        }
"""


class MainResult(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    subject_id = models.IntegerField()
    subject_variant = models.CharField(max_length=100)
    subject_variant_id = models.IntegerField()
    true_resolved_exercise_amount = models.IntegerField(default=0)


class InfoResult(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    subject_name = models.CharField(max_length=100)
    subject_id = models.IntegerField()
    subject_variant = models.CharField(max_length=100)
    subject_variant_id = models.IntegerField()
    exercise_id = models.IntegerField()
    exercise_text = models.TextField()
    user_selected_variant_id = models.IntegerField()
    is_resolved_true = models.BooleanField()
