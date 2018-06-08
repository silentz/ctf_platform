import os
import django
import random

def main():
    from api.models import Task, Category, Contest
    category_count = Category.objects.count()
    contest_count = Contest.objects.count()
    for i in range(40):
        Task.objects.create(
            name='Task ' + str(i + 1),
            score=random.randint(1, 6) * 100,
            description="task " + str(i + 1),
            flag="ctf{test_task_flag}",
            category=Category.objects.get(id=random.randint(1, category_count)),
            contest=Contest.objects.get(id=random.randint(1, contest_count))
        )


os.environ["DJANGO_SETTINGS_MODULE"] = 'ctf_platform.settings'
django.setup()
main()
