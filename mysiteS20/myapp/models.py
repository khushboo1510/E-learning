from django.core.exceptions import ValidationError
from django.db import models
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '{ Name: ' + self.name + \
               '; Category: ' + self.category + ' }'


def validate_limit(value):
    if not 100 <= value <= 200:
        raise ValidationError(('Please enter value between 100 and 200 , %(value)  is not in the defined range '),
                              params={'value': value}, )


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_limit])
    hours = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=1)
    stages = models.PositiveIntegerField(default=3)

    def discount(self):
        return float(self.price) * 0.9

    def __str__(self):
        return '{ Name: ' + self.name + \
               '; Price: ' + str(self.price) + \
               '; For Everyone: ' + str(self.for_everyone) + \
               '; Topic: ' + self.topic.name + \
               '; Description: ' + (self.description or 'NA') + '} '


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
    ('CG', 'Calgery'),
    ('MR', 'Montreal'),
    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return '{ Name: ' + self.first_name + ' ' + self.last_name + \
               '; School: ' + self.school + \
               '; City: ' + self.city + \
               '; Interested in: ' + str(self.interested_in.values_list('name')) + '} '


class Order(models.Model):
    ORDER_STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE, max_length=200)
    levels = models.PositiveIntegerField(default=0)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=datetime.date.today)

    def total_cost(self):
        return sum(course.price for course in self.course.all())

    def __str__(self):
        return '{ Student: ' + self.student.first_name + ' ' + self.student.last_name + \
               '; Courses: ' + self.course.name + \
               '; Levels: ' + str(self.levels) + \
               '; Order Status: ' + str(self.order_status) + \
               '; Order Date: ' + str(self.order_date) + '}'


