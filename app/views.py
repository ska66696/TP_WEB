from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from math import ceil

from .models import Question, Answer, Tag, Profile
from .forms import LoginForm, SignUpForm, ProfileEditForm, AskForm, AnswerForm
    
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
        Question.objects.prefetch_related('author__user', 'tags')
        .annotate(likes_count=Count('questionlike')),
        pk=question_id
    )
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            login_url = reverse('login') + f'?continue={request.path}'
            return redirect(login_url)

        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            profile = request.user.profile

            new_answer = Answer(
                question=question_item,
                author=profile,
                text=answer_form.cleaned_data['text']
            )
            new_answer.save()

            all_answers_sorted_ids = list(Answer.objects.best_for_question(question_id).values_list('id', flat=True))
            new_answer_index = all_answers_sorted_ids.index(new_answer.id)
            target_page_num = ceil((new_answer_index + 1) / 5)

            redirect_url = reverse('question', kwargs={'question_id': question_id})
            redirect_url += f'?page={target_page_num}#answer-{new_answer.id}'

            return redirect(redirect_url)
    else:
        answer_form = AnswerForm()

    answers_list = Answer.objects.best_for_question(question_id)
    page = paginate(answers_list, request, per_page=5)

    popular_tags = Tag.objects.get_popular_tags()

    context = {
        'answers': page.object_list,
        'page_obj': page,
        'question': question_item,
        'popular_tags': popular_tags,
        'answer_form': answer_form
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

@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            profile = request.user.profile

            new_question = Question(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=profile
            )
            new_question.save()

            tag_names = form.cleaned_data.get('tags', [])
            for tag_name in tag_names:
                tag = Tag.objects.get_or_create(name=tag_name)
                new_question.tags.add(tag)

            return redirect(reverse('question', kwargs={'question_id': new_question.id}))
    else:
        form = AskForm()

    popular_tags = Tag.objects.get_popular_tags()
    context = {
        'form': form,
        'popular_tags': popular_tags
    }
    return render(request, template_name = 'ask.html', context = context)

def login(request):
    redirect_to = request.GET.get('continue', reverse('index'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(redirect_to)
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    popular_tags = Tag.objects.get_popular_tags()
    context = {
        'form': form,
        'popular_tags': popular_tags
    }
    return render(request, template_name = 'login.html', context = context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile_data = {
                'user': user,
                'nickname': form.cleaned_data['nickname'],
            }
            uploaded_avatar = form.cleaned_data.get('avatar')

            if uploaded_avatar:
                 profile_data['avatar'] = uploaded_avatar

            Profile.objects.create(**profile_data)

            auth.login(request, user)

            return redirect(reverse('index'))
    else:
        form = SignUpForm()

    popular_tags = Tag.objects.get_popular_tags()
    context = {
        'form': form,
        'popular_tags': popular_tags
    }
    return render(request, template_name = 'signup.html', context = context)

def logout(request):
    auth.logout(request)
    referer = request.META.get('HTTP_REFERER')
    return redirect(referer or reverse('index'))

@login_required
def profile_edit(request):
    user = request.user    
    profile = user.profile

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, user=user)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            profile.nickname = form.cleaned_data['nickname']

            if 'avatar' in request.FILES:
                profile.avatar = form.cleaned_data['avatar']

            user.save()
            profile.save()

            messages.success(request, 'Profile updated successfully!')

            return redirect(reverse('profile_edit'))
    else:
        initial_data = {
            'email': user.email,
            'nickname': profile.nickname,
            'avatar': profile.avatar
        }
        form = ProfileEditForm(initial=initial_data, user=user)

    popular_tags = Tag.objects.get_popular_tags()
    context = {
        'form': form,
        'popular_tags': popular_tags
    }
    return render(request, template_name = 'profile_edit.html', context = context)

