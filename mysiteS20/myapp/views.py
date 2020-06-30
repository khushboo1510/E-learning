from django.shortcuts import render

from django.http import HttpResponse
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    # top_list = Topic.objects.all().order_by('id')[:10]
    top_list = Course.objects.all().order_by('price').reverse()[:5]
    response = HttpResponse()
    heading1 = '<p>' + 'List of courses in the respective topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        if not topic.for_everyone:
            para = '<p>' + str(topic.id) + ': ' + str(topic) + 'This Course is Not For Everyone!' + '</p>'
            response.write(para)
        else:
            para = '<p>' + str(topic.id) + ': ' + str(topic) + 'This Course is For Everyone!' + '</p>'
            response.write(para)
    return response


def about(request):
    response = HttpResponse()
    para = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    response.write(para)
    return response
