from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from collections import OrderedDict

import regex as re


# Create your views here.
def index(request):
    questions = Ask.objects.all()
    context = {
        'questions': questions
    }
    return render(request, 'index.html', context)


def test(request):
    questions = Ask.objects.all()
    Answers = Ans.objects.all()

    context = {
        'questions': questions,
        'answers': Answers
    }

    return render(request, 'test.html', context)


def testall(request):
    Answers = Ans.objects.all()

    context = {

        'answers': Answers
    }

    return render(request, "testall.html", context)


def ans(request):
    questions = Ask.objects.all()
    answers = Ans.objects.all()

    context = {
        'questions': questions,
        'answers': answers
    }
    return render(request, 'Ans.html', context)


def login_check(request):
    if request.user.is_superuser == 0:
       #   return HttpResponse(request.user.is_superuser)
        return redirect('ans')


    else:
      #  return HttpResponse(request.user.is_superuser)

        # return HttpResponse("admin page")
        return index(request)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('ans')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/registration.html', context)


def create(request):
    print(request.POST)
    title = request.GET['name']
    content = request.GET['content']
    source_id = request.GET['source']
    source = Source.objects.get(pk=source_id)
    type = request.GET['type']
    question_details = Ask(name=title, content=content,is_visible=True,Answer_type = type ,Source_fk=source)
    question_details.save()
    return redirect('/myadmin')



def add_question(request):
    return render(request, 'add_question.html')


def delete(request, id):
    questions = Ask.objects.get(pk=id)
    questions.is_visible = False
    questions.save()
    return redirect('/myadmin')


def answer(request):
    rate = int(request.POST.get('rate'))
    user_id = int(request.POST.get('user_id'))
    user = User.objects.get(pk=user_id)
    question_id = int(request.POST.get('question_id'))
    question = Ask.objects.get(pk=question_id)
    done = True
    user_answer = Ans(user_id=user, done=done, rate=rate, Question_id=question)
    user_answer.save()

    return redirect('ans')


def group(request):
    questions = Ask.objects.all()
    answers = Ans.objects.all()
    mydict = {}
    for question in questions:
        mylist = ['', 0, 0, 0, 0, 0, '', 0.0]
        for answer in answers:
            if question.id == answer.Question_id.id:
                mylist[0] = question.name
                mylist[6] = question.content
                # could be for loop depends on integer neeed change at model
                if answer.rate == '1':
                    mylist[1] = mylist[1] + 1

                if answer.rate == '2':
                    mylist[2] = mylist[2] + 1

                if answer.rate == '3':
                    mylist[3] = mylist[3] + 1

                if answer.rate == '4':
                    mylist[4] = mylist[4] + 1

                if answer.rate == '5':
                    mylist[5] = mylist[5] + 1
        if mylist[0] != '':
            key = mylist[0]
            # del mylist[0]
            avg = mylist[1:6]
            pw = 0
            sum = 0
            for i in range(5):
                sum = sum + mylist[i + 1]
                pw =pw + mylist[i + 1] * i + 1
            if pw / 5 > sum:
                mylist[7] = 5;
            else:
                mylist[7] = round(pw / sum,2)
            new = {key: mylist}
            mydict.update(new)

    context = {
        'questions': questions,
        'mydict': mydict
    }

    return render(request, 'test.html', context)
    # return HttpResponse(mydict)


def home(request):
    return render(request, 'home.html')


def scann(request):
    return render(request, 'scann.html')


def scann_info(request,qr,place,branch,waiter):

   #return HttpResponse(qr+place+branch+waiter)
    source=Source.objects.get(pk=place)
    branch = Branch.objects.get(pk=branch)
    waiter = Waiters.objects.get(pk=waiter)
    questions = Ask.objects.all()
    answers = Ans.objects.all()
    context = {
            'source': source,
            'branch': branch,
            'waiter': waiter,
            'questions': questions,
            'answers': answers
        }
    return render(request, 'Ans.html', context)
    #return HttpResponse( waiter.W_Name)





