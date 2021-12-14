import re
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

import quizes
from questions.models import Question
from .models import Quiz


# Create your views here.
def viewHome(request):
    global option_sort
    option_sort = {'Test Name-ASC': 'name', 'Test Name-DESC': '-name', 'Author-ASC': 'user', 'Author-DESC': '-user'}
    quiz = Quiz.objects.all().order_by(option_sort['Test Name-ASC'])
    return render(request, 'quizes/home.html',{'object_list':quiz,'sort_by': 'Test Name-ASC','request': request })

def viewDoTest(request):
    return render(request,'quizes/makeTest.html')

class ViewSerch(View):

    def get(self,request):
        quiz = Quiz.objects.all().order_by('Test Name-ASC')
        return render(request, 'quizes/home.html', {'object_list': quiz,'sort_by': 'Test Name-ASC'})
    def post(self,request):
        key_search = request.POST.get('input_search')
        if key_search != None:
            try:
                quiz_search = [Quiz.objects.get(name__iexact=key_search)]
            except:
                quiz_search = Quiz.objects.all().filter(name__icontains=key_search)

            return render(request, 'quizes/home.html', {'object_list': quiz_search})

        key_sort = request.POST.get('button_sort')
        if key_sort != "":
            sort_k = key_sort
            quiz = Quiz.objects.all().order_by(option_sort[key_sort])
            return render(request, 'quizes/home.html', {'object_list': quiz, 'sort_by': key_sort})


def quizView(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if request.method == 'POST':
        quiz.name  =request.POST.get('name')
        quiz.name = " ".join(quiz.name.split())
        quiz.topic =request.POST.get('topic')
        quiz.topic = " ".join(quiz.topic.split())
        quiz.number_of_questions = request.POST.get('number_of_questions')
        quiz.time = request.POST.get('time')
        quiz.required_score_to_pass = request.POST.get('required_score_to_pass')
        quiz.difficulty = request.POST.get('difficulty')
        quiz.save()
        return redirect("/questions/")
    return render(request, 'quizes/change_quiz.html', {'obj': quiz})

def deleteQuiz(request, pk):
    if request.user.has_perm('quizes.change_quiz'):
        Quiz.objects.get(pk=pk).delete()
        return redirect("/")
    return redirect("/user/Login/")


def quizDataView(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions_list = []
    for q in quiz.get_questions():
        answers = []
        correct = 0
        dem = 0
        for a in q.get_answers():

            answers.append(a.text)
            if a.correct:
                correct=dem
            dem += 1
        questions_list.append({'question':str(q),'choices':answers,'correctAnswer': correct })

    r = json.dumps(questions_list)
    return render(request,'quizes/makeTest.html',{"data_test":r,"quize": quiz})


def saveResult(request):
    # user = request.user
    # quiz_pk = request.POST.get('quiz_pk')
    # score = request.POST.get('score')
    # quiz = Quiz.objects.get(pk=quiz_pk)
    # Result.objects.create(quiz=quiz, user=user, score=score)

    selects = request.POST.get('selected')
    selects = list(selects.split(','))
    print(selects)
    print(type(selects))
    return HttpResponse("Thanh cong")


class AddTest(LoginRequiredMixin,View):
    login_url = '/user/Login/'
    def get(self, request):
        pass

    def post(self, request):
        test_name = request.POST.get('testName')
        test_name = " ".join(test_name.split())
        test_topic = request.POST.get('topic')
        test_topic = " ".join(test_topic.split())
        test_num_question= request.POST.get('num_question')
        test_time = request.POST.get('time_test')
        test_required_score = request.POST.get('required_score')
        if int(test_required_score)>100:
            test_required_score = "100"
        test_level = request.POST.get('test_level')
        quiz = Quiz.objects.create(user=request.user,name=test_name,topic= test_topic,number_of_questions=test_num_question,
                           time=test_time, required_score_to_pass =test_required_score, difficulty=test_level)
        question_len = len(Question.objects.filter(quiz=quiz)) + 1
        return render(request,'questions/add_questions.html',{'quiz_data': quiz, 'curren_len': question_len })

class ChangeQuiz(LoginRequiredMixin, View):
    login_url = '/user/Login'
    def get(self, request):
        pass

    def post(self, request, pk):
        test_name = request.POST.get('testName')
        test_name = " ".join(test_name.split())
        test_topic = request.POST.get('topic')
        test_topic = " ".join(test_topic.split())
        test_num_question= request.POST.get('num_question')
        test_time = request.POST.get('time_test')
        test_required_score = request.POST.get('required_score')
        test_level = request.POST.get('test_level')

        Quiz.objects.filter(pk=pk).update(name=test_name,topic= test_topic,number_of_questions=test_num_question,
                           time=test_time, required_score_to_pass =test_required_score, difficulty=test_level)
        quiz = Quiz.objects.get(pk=pk)
        question_len = len(Question.objects.filter(quiz=quiz))
        if question_len == quiz.number_of_questions:
            return redirect("/questions/view_list_question/"+str(pk)+"/")
        question_len +=1
        return render(request,'questions/add_questions.html',{'quiz_data': quiz, 'curren_len':question_len})

def viewTest(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/view_test.html', {"quize": quiz})

def exportFile(request,pk):
    quiz = Quiz.objects.get(pk=pk)
    correct = ''
    with open('test_'+str(request.user)+'_'+re.sub(r"[^a-zA-Z0-9]","",quiz.name)+ '_' + str(datetime.now().strftime('%YY%MM%dD_%Hh%Mm%Ss')) + '.csv', 'w',encoding='utf-8') as wf:
        wf.write(str(quiz.name)+','+str(quiz.topic)+','+str(quiz.number_of_questions)+','+str(quiz.time)+','+str(quiz.required_score_to_pass)+','+str(quiz.difficulty)+'\n')
        for question in quiz.get_questions():
            wf.write(str(question.text)+'\n')
            for answer in question.get_answers():
                wf.write(str(answer.text)+',')
                if answer.correct==True:
                    correct = answer.text

            wf.write(str(correct)+'\n')

    return redirect('/view_test/'+str(pk)+'/')

def about(request):
    return render(request,'quizes/about.html')

def tryTest(request):
    return render(request,'quizes/try_test.html')
