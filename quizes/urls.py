from django.urls import path
from .views import (
    QuizCreateView,
    QuestionCreateView,
    AnswerCreateView,
    QuizListView,
    QuizDeleteView,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
)

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('createquiz/', QuizCreateView.as_view(), name='quiz-create-view'),
    path('createquestion/', QuestionCreateView.as_view(), name='question-create-view'),
    path('createanswer/', AnswerCreateView.as_view(), name='answer-create-view'),
    path('<pk>/', quiz_view, name="quiz-view"),
    path('<pk>/delete', QuizDeleteView.as_view(), name="quiz-delete-view"),
    path('<pk>/save', save_quiz_view, name="save-view"),
    path('<pk>/data', quiz_data_view, name="quiz-data-view"),
]