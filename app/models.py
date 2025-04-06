from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse

# Create your models here.

class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-created_at')

    def best(self):
        return self.annotate(likes_count=Count('questionlike')).order_by('-likes_count', '-created_at')

    def by_tag(self, tag_object):
        query = self.filter(tags__name=tag_object)
        query = query.prefetch_related('tags', 'author')
        return query
    

class AnswerManager(models.Manager):
    def best_for_question(self, question_id):
        return self.filter(question_id=question_id)\
                   .annotate(likes_count=Count('answerlike'))\
                   .order_by('-is_correct', '-likes_count', '-created_at')\
                   .select_related('author')


class TagManager(models.Manager):
    def get_popular_tags(self, limit=10):
        return self.annotate(num_questions=Count('questions')).order_by('-num_questions')[:limit]


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    
    avatar = models.ImageField(
        upload_to='static/img/%Y/%m/%d/',
        blank=True,
        null=True,
        default='static/img/default_avatar.png'
    )


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def get_absolute_url(self):
        return reverse('question', kwargs={'question_id': self.pk})

    def get_answers_count(self):
        return self.answers.count()


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()


class QuestionLike(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='question_likes'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')


class AnswerLike(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='answer_likes'
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')