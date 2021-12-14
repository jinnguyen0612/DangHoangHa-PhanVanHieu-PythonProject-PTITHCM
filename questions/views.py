from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from quizes.models import Quiz
from django.views import View
from .models import Question, Answer


# Create your views here.
def viewListQuestion(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = Question.objects.all()
    question_list=[q for q in questions if q.quiz == quiz]
    return render(request, 'questions/view_list_questions.html',{'object_list': question_list, 'quiz_data': quiz})

def questionView(request, pk):
    question = Question.objects.get(pk=pk)
    return render(request,'questions/question.html',{'obj': question})

def changeQuestion(request, pk1, pk2):
    if request.user.has_perm('questions.change_question'):
        quiz = Quiz.objects.get(pk=pk1)
        question = Question.objects.get(pk=pk2)
        question_len = len(Question.objects.filter(quiz=quiz))
        return render(request,'questions/change_questions.html',{'question': question,'quiz_data':quiz, 'current_len': question_len })
    return redirect("/user/Login/")

def saveUpdateQuestion(request):
    if request.user.has_perm('questions.change_question'):
        quiz_pk = request.POST.get('quiz_pk')
        question_pk = request.POST.get('question_pk')
        question_text = request.POST.get('question')
        question_text = " ".join(question_text.split())
        answer_list = request.POST.get('answer_list')
        corect_answer = request.POST.get('correct_answer')
        answer_list = list(answer_list.split(','))

        question = Question.objects.get(pk=question_pk)
        answer = Answer.objects.all()
        for a in answer:
            if a.question == question:
                Answer.objects.filter(pk=a.pk).delete()

        Question.objects.filter(pk=question_pk).update(text=question_text)
        question = Question.objects.get(pk=question_pk)

        for i in range(len(answer_list)):
            corect = False
            if str(i) == corect_answer:
                corect = True
            Answer.objects.create(text=answer_list[i], correct=corect, question=question)

        quiz = Quiz.objects.get(pk=quiz_pk)
        questions = Question.objects.all()
        question_list = [q for q in questions if q.quiz == quiz]
        return render(request, 'questions/view_list_questions.html', {'object_list': question_list, 'quiz_data': quiz})
    return redirect("/user/Login/")

def addNew(request, pk):
    if request.user.has_perm('questions.add_question'):
        quiz = Quiz.objects.get(pk=pk)
        question_len = len(Question.objects.filter(quiz=quiz)) + 1
        return render(request, 'questions/add_questions.html', {'quiz_data': quiz, 'current_len': question_len })
    return redirect("/user/Login/")

class AddQuestions(LoginRequiredMixin,View):
    login_url = '/user/Login/'
    def get(self, request,pk):
        quiz = Quiz.objects.get(pk=pk)
        question_len = len(Question.objects.filter(quiz=quiz)) + 1
        return render(request, 'questions/add_questions.html', {'quiz_data': quiz, 'curren_len': question_len })

    def post(self, request):
        quiz_pk = request.POST.get('quiz_pk')
        question_text = request.POST.get('question')
        question_text = " ".join(question_text.split())
        answer_list = request.POST.get('answer_list')
        corect_answer = request.POST.get('correct_answer')
        quiz = Quiz.objects.get(pk=quiz_pk)
        # question_list = Question.objects.filter(quiz=quiz)
        # for q in question_list:
        #     if question_text == q.text:
        #         return
        question = Question.objects.create(text=question_text,quiz=quiz)
        question_len = len(Question.objects.filter(quiz=quiz))
        answer_list = list(answer_list.split(','))
        for i in range(len(answer_list)):
            corect = False
            if str(i)==corect_answer:
                corect = True
            Answer.objects.create(text=answer_list[i], correct=corect, question=question)
        if question_len == quiz.number_of_questions:
            return redirect("/questions/view_list_question/"+str(quiz_pk)+"/")
        question_len +=1
        return render(request,'questions/add_questions.html',{'quiz_data': quiz, 'curren_len': question_len})


def viewAnswer(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/view_answer.html', {"quize": quiz})

def deleteQuestion(request, pk):
    if request.user.has_perm('questions.delete_question'):
        question = Question.objects.get(pk=pk)
        quiz_pk = question.quiz.pk
        question.delete()
        return redirect("/questions/view_list_question/"+str(quiz_pk)+"/")
    return redirect("/user/Login/")
