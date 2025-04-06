import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from app.models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike

fake = Faker()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']

        num_users = ratio
        num_tags = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_question_likes = ratio * 100
        num_answer_likes = ratio * 100

        self.stdout.write(f'Starting database fill with ratio: {ratio}...')
        self.stdout.write(f'Will create: {num_users} users, {num_tags} tags, {num_questions} questions, {num_answers} answers, {num_question_likes + num_answer_likes} likes.')


        # --- Создание Пользователей и Профилей ---
        self.stdout.write('Creating users and profiles...')
        users = []
        profiles = []
        for i in range(num_users):
            username = f'{fake.user_name()}_{i}'
            email = fake.email()
            password = 'password123'
            user = User.objects.create_user(username, email, password)
            profile = Profile.objects.create(user=user)
            users.append(user)
            profiles.append(profile)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(profiles)} users and profiles.'))


        # --- Создание Тегов ---
        self.stdout.write('Creating tags...')
        tags = []
        tags_to_create = []
        for i in range(num_tags):
            tag_name = f'{fake.word()}_{i}'
            tags_to_create.append(Tag(name=tag_name))
            if len(tags_to_create) >= 1000:
                Tag.objects.bulk_create(tags_to_create, ignore_conflicts=True)
                tags_to_create = []
                self.stdout.write(f'  ...batch of tags created')

        if tags_to_create:
            Tag.objects.bulk_create(tags_to_create, ignore_conflicts=True)

        tags = list(Tag.objects.all())
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(tags)} tags.'))


        # --- Создание Вопросов ---
        self.stdout.write('Creating questions...')
        questions_list = []
        questions_bulk = []
        tags_for_questions = []

        for i in range(num_questions):
            author = random.choice(profiles)
            question = Question(
                author=author,
                title=fake.sentence(nb_words=6),
                text=fake.paragraph(nb_sentences=3)
            )
            questions_bulk.append(question)

            if len(questions_bulk) >= 500:
                created_batch = Question.objects.bulk_create(questions_bulk)
                questions_list.extend(created_batch)
                if tags:
                    for q in created_batch:
                        num_q_tags = random.randint(1, 5)
                        question_tags_sample = random.sample(tags, min(num_q_tags, len(tags)))
                        for tag in question_tags_sample:
                            tags_for_questions.append(
                                Question.tags.through(question_id=q.id, tag_id=tag.id)
                            )
                questions_bulk = []
                self.stdout.write(f'  ...batch of questions created ({len(questions_list)} total)')

        if questions_bulk:
            created_batch = Question.objects.bulk_create(questions_bulk)
            questions_list.extend(created_batch)
            if tags:
                for q in created_batch:
                    num_q_tags = random.randint(1, 5)
                    question_tags_sample = random.sample(tags, min(num_q_tags, len(tags)))
                    for tag in question_tags_sample:
                        tags_for_questions.append(
                            Question.tags.through(question_id=q.id, tag_id=tag.id)
                        )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(questions_list)} questions.'))

        if tags_for_questions:
            self.stdout.write('Assigning tags to questions...')
            Question.tags.through.objects.bulk_create(tags_for_questions, ignore_conflicts=True, batch_size=1000)
            self.stdout.write(self.style.SUCCESS('Tags assigned.'))

        # --- Создание Ответов ---
        self.stdout.write('Creating answers...')
        answers_list = []
        answers_bulk = []
        for i in range(num_answers):
            author = random.choice(profiles)
            question = random.choice(questions_list)
            answer = Answer(
                author=author,
                question=question,
                text=fake.paragraph(nb_sentences=2),
                is_correct=random.choices([True, False], weights=[10, 90], k=1)[0]
            )
            answers_bulk.append(answer)

            if len(answers_bulk) >= 1000:
                created_answers = Answer.objects.bulk_create(answers_bulk)
                answers_list.extend(created_answers)
                answers_bulk = []
                self.stdout.write(f'  ...batch of answers created ({len(answers_list)} total)')

        if answers_bulk:
            created_answers = Answer.objects.bulk_create(answers_bulk)
            answers_list.extend(created_answers)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(answers_list)} answers.'))


        # --- Создание Лайков для Вопросов ---
        self.stdout.write('Creating question likes...')
        q_likes_bulk = []
        created_q_like_count = 0
        for i in range(num_question_likes):
            user_profile = random.choice(profiles)
            question = random.choice(questions_list)
            like = QuestionLike(user=user_profile, question=question)
            q_likes_bulk.append(like)

            if len(q_likes_bulk) >= 1000:
                QuestionLike.objects.bulk_create(q_likes_bulk, ignore_conflicts=True)
                created_q_like_count += len(q_likes_bulk)
                q_likes_bulk = []
                self.stdout.write(f'  ...attempted batch of question likes ({created_q_like_count} total attempts)')

        if q_likes_bulk:
            QuestionLike.objects.bulk_create(q_likes_bulk, ignore_conflicts=True)
            created_q_like_count += len(q_likes_bulk)

        self.stdout.write(self.style.SUCCESS(f'Attempted to create {created_q_like_count} question likes (duplicates ignored).'))


        # --- Создание Лайков для Ответов ---
        if answers_list:
            self.stdout.write('Creating answer likes...')
            a_likes_bulk = []
            created_a_like_count = 0
            for i in range(num_answer_likes):
                user_profile = random.choice(profiles)
                answer = random.choice(answers_list)
                like = AnswerLike(user=user_profile, answer=answer)
                a_likes_bulk.append(like)

                if len(a_likes_bulk) >= 1000:
                    AnswerLike.objects.bulk_create(a_likes_bulk, ignore_conflicts=True)
                    created_a_like_count += len(a_likes_bulk)
                    a_likes_bulk = []
                    self.stdout.write(f'  ...attempted batch of answer likes ({created_a_like_count} total attempts)')

            if a_likes_bulk:
                AnswerLike.objects.bulk_create(a_likes_bulk, ignore_conflicts=True)
                created_a_like_count += len(a_likes_bulk)

            self.stdout.write(self.style.SUCCESS(f'Attempted to create {created_a_like_count} answer likes (duplicates ignored).'))


        self.stdout.write(self.style.SUCCESS(f'Successfully finished filling the database for ratio {ratio}!'))