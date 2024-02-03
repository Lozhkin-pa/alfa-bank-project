from random import choice

from django.core.management.base import BaseCommand

from users.models import User

NAMES = ('Иван', 'Олег', 'Петр', 'Михаил', 'Максим')
SURNAMES = ('Олегович', 'Кириллович', 'Александрович', 'Павлович')
LAST_NAMES = ('Иванов', 'Петров', 'Сидоров', 'Козлов', 'Майоров')
PASSWORD = 'superhardpassword1'


class Command(BaseCommand):
    help = 'Creates fake data for testing'

    def handle(self, *args, **options):
        superior = self.create_superior()
        self.create_subordinates(superior)
        self.stdout.write(self.style.SUCCESS('Тестовые пользователи созданы'))

    def create_superior(self) -> User:
        user = User.objects.create(
            username="superior",
            first_name="Кирилл",
            last_name="Сидоров",
            patronymic="Иванович",
            position="Team Lead",
            photo="users/superior.jpg",
        )
        user.set_password(PASSWORD)
        user.save()
        return user

    def create_subordinates(self, superior: User) -> None:
        for i in range(1, 10):
            user = User.objects.create(
                username=f"subordinate{i}",
                first_name=choice(NAMES),
                last_name=choice(LAST_NAMES),
                patronymic=choice(SURNAMES),
                position="Python developer",
                photo=f"users/subordinates_{i}",
            )
            user.superiors.add(superior)
            user.set_password(PASSWORD)
            user.save()
