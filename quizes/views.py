from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView
from questions.models import Answer, Question
from results.models import Result

from quizes.forms import QuestionForm, QuizForm

from .models import Quiz


class QuizListView(LoginRequiredMixin, ListView):
    model = Quiz
    template_name = 'quizes/main.html'
    login_url = 'authentication/login'
    redirect_field_name = ''
    form_class = QuizForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            request.session['errorQuiz'] = False
            return redirect('/')
        else:
            request.session['errorQuiz'] = True
            return redirect('/')

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        quiz_count = Quiz.objects.all().count()
        context["quiz_count"] = quiz_count
        return context

class QuizCreateView(LoginRequiredMixin, CreateView):
    model = Quiz
    template_name = 'quizes/quiz_modal_form.html'
    fields = [
        'name', 
        'topic', 
        'number_of_questions', 
        'time', 
        'required_score_to_pass', 
        'difficulty'
    ]
    success_url = '/'

def question_create_view(request, pk):
    q = Quiz.objects.get(pk=pk)
    form = QuestionForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.quiz = q
            form.save()
            form = QuestionForm()
            return redirect('/')
    form = QuestionForm()
    return render(request, 'quizes/question_modal_form.html', {'form':form})

class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    template_name = 'quizes/answer_modal_form.html'
    fields = [
        'text', 
        'correct', 
        'question'
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
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if is_ajax:
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

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

def logout_view(request):
    return render(request, 'quizes/logout_confirm.html')
