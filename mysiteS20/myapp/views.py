import datetime

from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from myapp.forms import OrderForm, InterestForm, LoginForm
from .models import Topic, Course, Student, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
def index(request):
    # top_list = Topic.objects.all().order_by('id')[:10]
    top_list = Topic.objects.all().order_by('id')[:10]
    last_login = request.session['last_login'] if 'last_login' in request.session else 'Your last login was more than one hour ago'
    return render(request, "myapp/index.html", {'top_list': top_list, 'last_login': last_login})


def about(request):
    # response = HttpResponse()
    # para = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses.' + '</p>'
    # response.write(para)
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
        request.session.set_expiry(300)
    else:
        request.session['about_visits'] = 1
    return render(request, "myapp/about.html", {'number_of_visits': request.session['about_visits']})


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


def coursedetail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            # request.POST.get('interested') is '1'
            if form.cleaned_data['interested'] == '1':
                course.interested = course.interested + 1
                course.save()
            return index(request)
    else:
        # if a GET (or any other method) we'll create a blank form
        form = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form': form, 'course': course})


def user_login(request):
    context = {}
    context['form'] = LoginForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.datetime.now())
                # request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html', context)


@login_required
def user_logout(request):
    request.session.clear()
    #logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


def myaccount(request):
    if request.user.is_authenticated:
        current_user = request.user

        if Student.objects.filter(pk=current_user.id):
            first_name = current_user.first_name
            last_name = current_user.last_name
            ordered_course = Order.objects.filter(student_id=current_user.id).values_list('course__name', flat=True)
            interested = Student.objects.filter(id=current_user.id).values_list('interested_in__courses__name', flat=True)
            return render(request, 'myapp/myaccount.html',
                          {'ordered_course': ordered_course, 'first_name': first_name, 'last_name': last_name,
                           'interested': interested})
        else:
            return HttpResponse('You are not a registered student!')
    else:
        return user_login(request)
