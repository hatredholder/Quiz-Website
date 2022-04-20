from django.forms import ModelForm
from questions.models import Answer, Question

from .models import Quiz


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'topic', 'number_of_questions', 'time', 'required_score_to_pass', 'difficulty']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'correct', 'question']
