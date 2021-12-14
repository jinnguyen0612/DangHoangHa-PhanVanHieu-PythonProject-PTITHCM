from django.forms import ModelForm
from .models import Quiz


class AddQuizThemeForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name','topic','number_of_questions','time','required_score_to_pass','difficulty']