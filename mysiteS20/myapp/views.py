from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    # top_list = Topic.objects.all().order_by('id')[:10]
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, "myapp/index0.html", {'top_list': top_list})


def about(request):
    # response = HttpResponse()
    # para = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    # response.write(para)
    return render(request, "myapp/about0.html")


def detail(request, top_no):
    top_details = Topic.objects.filter(pk=top_no)
    response = HttpResponse()
    if top_details:
        for topic in top_details:
            course_list = Course.objects.filter(topic__name=topic.name)
            para1 = '<p>' + 'Category' + ': ' + str(topic.category)
            response.write(para1)
            para2 = '<p>' + 'Course List' + ':'
            response.write(para2)
            for course in course_list:
                para = '<p>' + str(course) + '</p>'
                response.write(para)
    else:
        get_object_or_404(Topic, pk=top_no)
    return response



