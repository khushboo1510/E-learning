from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from myapp.forms import OrderForm
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    # top_list = Topic.objects.all().order_by('id')[:10]
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, "myapp/index.html", {'top_list': top_list})


def about(request):
    # response = HttpResponse()
    # para = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    # response.write(para)
    return render(request, "myapp/about.html")


def detail(request, top_no):
    # response = HttpResponse()
    # topic  = Topic.objects.get(id=top_no)
    topic = get_object_or_404(Topic, id=top_no)  # Gives 404 if Topic not found
    course_list = Course.objects.filter(topic__id=top_no)
    # response.write(topic)
    # response.write('<p>' + Course List: ' + '</p>')
    # for course in Course.objects.filter(topic__id=top_no):
    #     if course.for_everyone:
    #         for_str = "This Course is For Everyone!"
    #     else:
    #         for_str = "This Course is not For Everyone!"
    #     response.write('<p>' + str(course.id) + ': ' + str(course) + for_str + '</p>')
    # return response
    return render(request, "myapp/detail.html", {'topic': topic, 'course_list': course_list})


def courses(request):
    courselist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courselist': courselist})


def place_order(request):
    msg = ''
    courselist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            print(order)
            if order.levels <= order.course.stages:
                form.save()
                msg = 'Your course has been ordered successfully.'
                if float(order.course.price) > 150:
                    order.course.discounted_price = Course.discount(order.course)
                    order.course.save()
                    msg = msg + 'Price for order updated to $' + str(order.course.discounted_price)
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courselist': courselist})


