from django.urls import path

from questions.views import AddQuestions, questionView, viewListQuestion, viewAnswer, changeQuestion, \
    saveUpdateQuestion, deleteQuestion

app_name = 'questions'
urlpatterns = [
    path('view_list_question/<pk>/', viewListQuestion, name="view_list_question"),
    path('question_view/<pk>/', questionView, name="question_view"),
    path('add_question/',AddQuestions.as_view(),name="add_question"),
    path('add_new/<pk>/',AddQuestions.as_view(), name="add_new"),
    path('view_answer/<pk>/', viewAnswer, name='view_answer'),
    path('change_question/<pk1>/<pk2>/', changeQuestion, name='change_question'),
    path('save_update_question/', saveUpdateQuestion, name='save_update_question'),
    path('delete_questions/<pk>/', deleteQuestion, name='delete_question'),
]