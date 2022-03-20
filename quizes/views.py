import re
from django.shortcuts import redirect, render
from quizes.forms import QuizForm
from .models import Quiz
from django.views.generic import ListView, CreateView
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quizes/main.html'
    login_url = 'authentication/login'
    redirect_field_name = ''
    form_class = QuizForm

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        quiz_count = Quiz.objects.all().count()
        context["quiz_count"] = quiz_count
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            form = self.form_class()
            return render(request, self.template_name, self.get_context_data())

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = 'quizes/quiz_modal_form.html'
    fields = ['name', 
    'topic', 
    'number_of_questions', 
    'time', 
    'required_score_to_pass', 
    'difficulty'
    ]
    success_url = '/'

class QuizDeleteView(LoginRequiredMixin, DeleteView):
    model = Quiz
    success_url = '/'
    

@login_required(login_url="authentication:login-view")
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.html', {'obj':quiz})

@login_required(login_url="authentication:login-view")
def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data':questions,
        'time':quiz.time
    })

@login_required(login_url="authentication:login-view")
def save_quiz_view(request, pk):
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    if not requested_html:
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
            
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})