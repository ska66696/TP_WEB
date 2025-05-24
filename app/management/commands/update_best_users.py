from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, QuestionLike, AnswerLike 
from django.db.models import Count, Sum, F, OuterRef, Subquery, Exists
from django.db.models.functions import Coalesce
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from collections import defaultdict

class Command(BaseCommand):
    help = 'Calculates and caches best users for the last week.'

    CACHE_KEY = 'best_users_sidebar'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to update best users cache...'))

        one_week_ago = timezone.now() - timedelta(days=7)

        user_scores = defaultdict(int)
        
        recent_questions = Question.objects.filter(created_at__gte=one_week_ago)
        for q in recent_questions.annotate(num_likes=Count('questionlike')):
            if q.num_likes > 0:
                user_scores[q.author_id] += q.num_likes

        recent_answers = Answer.objects.filter(created_at__gte=one_week_ago)
        for a in recent_answers.annotate(num_likes=Count('answerlike')):
            if a.num_likes > 0:
                user_scores[a.author_id] += a.num_likes

        valid_user_scores = {pid: score for pid, score in user_scores.items() if score > 0}

        sorted_user_ids = sorted(valid_user_scores, key=valid_user_scores.get, reverse=True)[:10]
        
        best_users_profiles = Profile.objects.filter(id__in=sorted_user_ids).select_related('user')
        
        users_for_cache = []
        for profile_id in sorted_user_ids:
            profile = next((p for p in best_users_profiles if p.id == profile_id), None)
            if profile:
                users_for_cache.append({
                    'id': profile.id,
                    'nickname': profile.nickname if profile.nickname else profile.user.username,
                    'avatar_url': profile.get_avatar_url(),
                    'score': valid_user_scores[profile_id]
                })
        
        cache.set(self.CACHE_KEY, users_for_cache)

        self.stdout.write(self.style.SUCCESS(f'Successfully updated cache for key "{self.CACHE_KEY}" with {len(users_for_cache)} users.'))
        if users_for_cache:
            self.stdout.write(f"Cached best users: {users_for_cache}")