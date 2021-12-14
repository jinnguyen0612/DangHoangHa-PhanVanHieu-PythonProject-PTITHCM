from django.urls import path
from results.views import ViewResult, exportResult

app_name='results'
urlpatterns = [
    path('', ViewResult.as_view(),name='view_result'),
    # path('save_result/',save_result,name='save_result'),
    path('export_result/<pk>/',exportResult,name='export_result')
]