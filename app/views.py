from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random

all_tags = ['Go', 'Python', 'C++', 'Java', 'HTML', 'CSS', 'Bootstrap', 'JavaScript', 'Django', 'SQL', 'Linux']
popular_tags = ['Python', 'Java', 'JavaScript', 'C++', 'HTML', 'CSS', 'Django', 'Go', 'Bootstrap']

questions = []
for i in range(0,100):
    num_tags = random.randint(1, 4)
    q_tags = random.sample(all_tags, num_tags)
    questions.append({
    'title': 'Q_title ' + str(i),
    'id': i,
    'text': 'Q_text' + str(i),
    'tags': q_tags
  })

answers = []
for i in range(0,100):
    answers.append({
    'title': 'A_title ' + str(i),
    'id': i,
    'text': 'A_text' + str(i)
  })
    
def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page_num = request.GET.get('page', 1)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

#Сделать пагинацию отдельной функцией и обработать несуществующие значения и сделать гит игнор и отправить на портал
# Create your views here.
def index(request):
    page = paginate(questions, request, per_page=5)

    context = {
        'questions' : page.object_list,
        'page_obj' : page,
        'popular_tags': popular_tags
        }
    return render(request, template_name = 'index.html', context = context)

def hot(request):
    page = paginate(questions, request, per_page=5)

    context = {
        'questions' : page.object_list,
        'page_obj' : page,
        'popular_tags': popular_tags
        }
    return render(request, template_name = 'hot.html', context = context)

def question(request, question_id):
    page = paginate(answers, request, per_page=5)

    context = {
        'answers' : page.object_list,
        'page_obj' : page,
        'question' : questions[question_id],
        'popular_tags': popular_tags
        }
    return render(request, template_name = 'question.html', context = context)

def tag(request, tag_name):
    tagged_questions = [q for q in questions if tag_name in q.get('tags', [])]

    page = paginate(tagged_questions, request, per_page=5)

    context = {
        'questions': page.object_list,
        'page_obj': page,
        'tag_name': tag_name,
        'popular_tags': popular_tags
    }
    return render(request, 'tag.html', context = context)

def ask(request):
    context = {'popular_tags': popular_tags}
    return render(request, template_name = 'ask.html', context = context)

def login(request):
    context = {'popular_tags': popular_tags}
    return render(request, template_name = 'login.html', context = context)

def signup(request):
    context = {'popular_tags': popular_tags}
    return render(request, template_name = 'signup.html', context = context)