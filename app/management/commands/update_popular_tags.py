from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from django.db.models import Q

from app.models import Tag, Question

class Command(BaseCommand):
    help = 'Calculates and caches popular tags for the last 3 months.'

    CACHE_KEY = 'popular_tags_sidebar'



    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to update popular tags cache...'))

        three_months_ago = timezone.now() - timedelta(days=3*30)
        
        popular_tags_data = Tag.objects.annotate(
            recent_questions_count=Count(
                'questions',
                filter=Q(questions__created_at__gte=three_months_ago)
            )
        ).filter(recent_questions_count__gt=0).order_by('-recent_questions_count')[:10]

        tags_for_cache = []
        for tag_obj in popular_tags_data:
            tags_for_cache.append({
                'name': tag_obj.name,
            })

        cache.set(self.CACHE_KEY, tags_for_cache) 

        self.stdout.write(self.style.SUCCESS(f'Successfully updated cache for key "{self.CACHE_KEY}" with {len(tags_for_cache)} tags.'))
        if tags_for_cache:
            self.stdout.write(str(tags_for_cache))