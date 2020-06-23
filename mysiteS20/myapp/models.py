from django.db import models
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank=False, null=False)


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)



class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
    ('CG', 'Calgery'),
    ('MR', 'Montreal'),
    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

class Order(models.Model):
    ORDER_STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, related_name='student', on_delete=models.CASCADE, max_length=200)
    levels = models.PositiveIntegerField(default=0)
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(auto_now_add=True, editable=False)




