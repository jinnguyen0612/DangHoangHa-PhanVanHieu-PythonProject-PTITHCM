from django.forms import ModelForm
from .models import Question,Answer

class AddQuestionsForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text','quiz']

class AddAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text','correct','question']