from django.urls import path
from .views import quizDataView, viewHome, deleteQuiz, \
    ViewSerch, viewDoTest, AddTest, ChangeQuiz, viewTest, tryTest, saveResult, exportFile, about

app_name = 'quizes'
urlpatterns = [
    path('', viewHome, name='home'),
    path('delete_quiz/<pk>/', deleteQuiz, name='delete_quiz'),
    path('quiz_data_view/<pk>/', quizDataView, name='quiz_data_view'),
    path('add_test',AddTest.as_view(),name='add_test'),
    path('view_search/',ViewSerch.as_view(),name='view_search'),
    path('make_test/', viewDoTest, name='make_test'),
    path('save_result/', saveResult, name='save_result'),
    path('change_quiz/<pk>/', ChangeQuiz.as_view(), name='change_quiz'),
    path('view_test/<pk>/', viewTest, name='view_test'),
    path('try_test/', tryTest, name='try_test'),
    path('export_file/<pk>/', exportFile, name='export_file'),
    path('about/',about,name='about')
]