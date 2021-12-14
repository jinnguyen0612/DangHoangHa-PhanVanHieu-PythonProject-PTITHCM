import re
from datetime import datetime

from django.views import View
from quizes.models import Quiz
from results.models import Result
from django.shortcuts import render, redirect


# Create your views here.
class ViewResult(View):
    # login_url = '/user/Login/'
    def get(self,request):
        return render(request, 'results/view_results.html')

    def post(self,request):
        user_current = request.user
        quiz_pk = request.POST.get('quiz_pk')
        # score = request.POST.get('score')
        quiz = Quiz.objects.get(pk=quiz_pk)
        selects = request.POST.get('selected')
        print(selects)
        if selects!= None:
            selects = list(selects.split(','))
        while(len(selects)<quiz.number_of_questions):
            selects.append('-1')
        score = 0
        i = 0
        for q in quiz.get_questions():
            j = 0
            for a in q.get_answers():
                if a.correct == True and str(j) == selects[i]:
                    score +=1
                    break
                j += 1
            i+=1

        i = len(quiz.get_questions())
        # print(score)
        # print(i)
        score = (100.0/i)*score
        result = ""
        if user_current.username != '':
              result = Result.objects.create(quiz=quiz, user=user_current, score=score)
        return render(request, 'results/view_results.html', {'quize': quiz, 'score': int(score), 'result':result})

def exportResult(request,pk):
    if request.user.username!='':
        result = Result.objects.get(pk=pk)
        with open('result_'+str(result.user)+'_'+ re.sub(r"[^a-zA-Z0-9]","",result.quiz.name) + '_' + str(datetime.now().strftime('%YY%MM%dD_%Hh%Mm%Ss')) + '.csv', 'w', encoding='utf-8') as wf:
            wf.write('Name test,User name,Score' + '\n')
            wf.write(str(result.quiz) + ',' + str(result.user) + ',' + str(result.score) + '\n')
        return render(request, 'results/view_results.html', {'quize': result.quiz, 'score': int(result.score), 'result':result})
    return redirect("/user/Login/")