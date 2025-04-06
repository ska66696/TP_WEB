from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer, Tag
from django.db.models import Count
    
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

# Create your views here.
def index(request):
    questions_list = Question.objects.new().prefetch_related('author', 'tags').annotate(likes_count=Count('questionlike'))
    page = paginate(questions_list, request, per_page=5)
    popular_tags = Tag.objects.get_popular_tags()

    context = {
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': popular_tags,
    }
    return render(request, template_name='index.html', context=context)


def hot(request):
    questions_list = Question.objects.best().prefetch_related('author', 'tags')
    page = paginate(questions_list, request, per_page=5)
    popular_tags = Tag.objects.get_popular_tags()

    context = {
        'questions' : page.object_list,
        'page_obj' : page,
        'popular_tags': popular_tags
        }
    return render(request, template_name = 'hot.html', context = context)

def question(request, question_id):
    question_item = get_object_or_404(
        Question.objects.prefetch_related('author', 'tags')
        .annotate(likes_count=Count('questionlike')),
        pk=question_id
    )
    answers_list = Answer.objects.best_for_question(question_id)
    page = paginate(answers_list, request, per_page=5)
    popular_tags = Tag.objects.get_popular_tags()

    context = {
        'answers' : page.object_list,
        'page_obj' : page,
        'question' : question_item,
        'popular_tags': popular_tags
        }
    return render(request, template_name = 'question.html', context = context)

def tag(request, tag_name):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    questions_list = Question.objects.by_tag(tag_obj).annotate(likes_count=Count('questionlike'))
    page = paginate(questions_list, request, per_page=5)
    popular_tags = Tag.objects.get_popular_tags()

    context = {
        'questions': page.object_list,
        'page_obj': page,
        'tag_name': tag_obj,
        'popular_tags': popular_tags
    }
    return render(request, 'tag.html', context = context)

def ask(request):
    popular_tags = Tag.objects.get_popular_tags()
    context = {'popular_tags': popular_tags}
    return render(request, template_name = 'ask.html', context = context)

def login(request):
    popular_tags = Tag.objects.get_popular_tags()
    context = {'popular_tags': popular_tags}
    return render(request, template_name = 'login.html', context = context)

def signup(request):
    popular_tags = Tag.objects.get_popular_tags()
    context = {'popular_tags': popular_tags}
    return render(request, template_name = 'signup.html', context = context)