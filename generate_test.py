import os
import django
import random
import pytz
from datetime import datetime, timedelta


def create_categories():
    from api.models import Category
    Category.objects.create(name='reverse')
    Category.objects.create(name='web')
    Category.objects.create(name='crypto')
    Category.objects.create(name='joy')
    Category.objects.create(name='stego')
    Category.objects.create(name='pwn')
    Category.objects.create(name='ppc')
    Category.objects.create(name='admin')


def create_groups():
    from api.models import GroupAdditional
    from django.contrib.auth.models import Group
    groups = []
    for i in range(4):
        gr = Group.objects.create(name='Group #' + str(i + 1))
        GroupAdditional.objects.create(group=gr, invite_code='12345')
        groups.append(gr)
    return groups


def create_contests(allowed_groups):
    from api.models import Contest
    tz = pytz.timezone('Europe/Moscow')
    for i in range(10):
        meta = {
            'name': 'Contest #' + str(i + 1),
            'start_datetime': datetime.now(tz),
            'finish_datetime': datetime.now(tz) + timedelta(10),
            'training': False,
        }
        c = Contest.objects.create(**meta)
        c.allowed_groups.set(allowed_groups)
        c.save()


def create_trainings(allowed_groups):
    from api.models import Contest
    for i in range(10):
        meta = {
            'name': 'Training #' + str(i + 1),
            'start_datetime': None,
            'finish_datetime': None,
            'training': True,
        }
        c = Contest.objects.create(**meta)
        c.allowed_groups.set(allowed_groups)
        c.save()


def create_tasks():
    from api.models import Contest, Category, Task
    category_count = Category.objects.count()
    contest_count = Contest.objects.count()
    for i in range(200):
        Task.objects.create(
            name='Task ' + str(i + 1),
            score=random.randint(1, 5) * 100,
            description="task " + str(i + 1) + "description test text",
            flag="ctf{test_flag_test_flag}",
            category=Category.objects.get(id=random.randint(1, category_count)),
            contest=Contest.objects.get(id=random.randint(1, contest_count))
        )


def create_news():
    from api.models import News
    for i in range(10):
        News.objects.create(text='news text #' + str(i + 1))


def create_users():
    from django.contrib.auth.models import User
    admin = User(username='admin', is_staff=True)
    admin.set_password('admin')
    admin.save()
    user = User(username='user')
    user.set_password('user')
    user.save()


def main():
    create_categories()
    create_news()
    allowed_groups = create_groups()
    create_contests(allowed_groups)
    create_trainings(allowed_groups)
    create_tasks()
    create_users()
    

if __name__ == '__main__':
    os.environ["DJANGO_SETTINGS_MODULE"] = 'ctf_platform.settings'
    django.setup()
    main()
