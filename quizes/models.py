from django.contrib.auth.models import User
from django.db import models


# Create your models here.
DIFF_CHOIES = (
    ('easy','easy'),
    ('medium','medium'),
    ('hard','hard'),
)
class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    topic = models.CharField(max_length=120)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of the quiz in minutes ")
    required_score_to_pass = models.IntegerField(help_text="requires score is %")
    difficulty = models.CharField(max_length= 6,choices=DIFF_CHOIES)

    def __str__(self):
        return f"{self.name}-{self.topic}"

    def get_questions(self):
        return self.question_set.all()[:self.number_of_questions]

    def is_empty(self):
        return len(self.get_questions())==0

    class Meta:
        verbose_name_plural = 'Quizes'
