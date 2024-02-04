from datetime import datetime, timedelta
import json
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from users.models import User
from iprs.models import Ipr, Task, Comment

SUPERIOR_LOGIN = 'superior'
SUBORDINATE_LOGIN = 'subordinate'
TEST_PASSWORD = 'superhardpassword1'

IPR_TITLE_1 = 'Качаем софт скиллы'
IPR_DESC_1 = 'Вот список всех книг, которые ты должен прочесть до пятницы...'
IPR_END_DATE_1 = datetime.now()

IPR_TITLE_2 = 'Качаем софт скиллы'
IPR_DESC_2 = 'Вот список всех книг, которые ты должен прочесть до пятницы...'
IPR_END_DATE_2 = datetime.now()

TASK_TITLE_1 = 'Качай!!'
TASK_DESC_1 = 'Огонь!'
TASK_START_1 = timezone.now()
TASK_END_1 = TASK_START_1 + timedelta(days=3)

COMMENT_TEXT_1 = 'Кхм'

AUTH_URL = reverse('api:auth')
GET_USER_URL = reverse('api:users-detail', args=('me',))
GET_SUBORDINATES = reverse('api:users-get_subordinates')

GET_IPRS_LIST_URL = reverse('api:my_iprs-list')
GET_SUBORDINATES_IPRS_LIST_URL = reverse('api:iprs-list')


class TestCaseWithMockData(TestCase):
    def setUp(self):
        self.superior = User.objects.create(
            username=SUPERIOR_LOGIN,
            first_name='Василий',
            last_name='Иванов'
        )
        self.superior.set_password(TEST_PASSWORD)
        self.superior.save()

        self.subordinate = User.objects.create(
            username=SUBORDINATE_LOGIN,
            first_name='Петр',
            last_name='Сидоров'
        )
        self.subordinate.superiors.add(self.superior)
        self.subordinate.set_password(TEST_PASSWORD)
        self.subordinate.save()

        self.client = APIClient()


class AuthApiTest(TestCaseWithMockData):
    def test_login(self):
        response = self.client.post(
            path=AUTH_URL,
            data=json.dumps(
                {
                    'username': SUPERIOR_LOGIN,
                    'password': TEST_PASSWORD
                }
            ),
            content_type='application/json'
        )
        assert response.status_code == 200
        response_dict = response.json()
        assert response_dict.get('token')


class UserApiTest(TestCaseWithMockData):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.superior)

    def test_get_user_obj(self):
        response = self.client.get(
            path=GET_USER_URL.format(pk=self.superior.pk),
        )
        assert response.status_code == 200
        data = response.json()
        assert data.keys() == {
            'id', 'photo', 'username', 'first_name',
            'last_name', 'patronymic', 'email',
            'position', 'superiors', 'subordinates'
        }
        assert data.get('id') == self.superior.id

    def test_get_get_subordinates(self):
        response = self.client.get(
            path=GET_SUBORDINATES
        )
        assert response.status_code == 200
        data = response.json()
        assert type(data) == list
        assert len(data) == 1
        assert data[0].keys() == {
            'id', 'photo', 'username', 'first_name',
            'last_name', 'patronymic', 'email',
            'position', 'superiors', 'subordinates'
        }

        
class IprApiTests(TestCaseWithMockData):
    def setUp(self):
        super().setUp()

        self.client.force_authenticate(user=self.superior)

        self.ipr = Ipr.objects.create(
            title=IPR_TITLE_1,
            employee=self.subordinate,
            author=self.superior,
            description=IPR_DESC_1,
            end_date=IPR_END_DATE_1
        )

        self.task = Task.objects.create(
            title=TASK_TITLE_1,
            description=TASK_DESC_1,
            author=self.superior,
            ipr=self.ipr,
            start_date=TASK_START_1,
            end_date=TASK_END_1
        )

        self.comment = Comment.objects.create(
            author=self.superior,
            task=self.task,
            text=COMMENT_TEXT_1
        )

    def test_ipr_get_list(self):
        self.client.force_authenticate(user=self.subordinate)
        response = self.client.get(
            path=GET_IPRS_LIST_URL
        )

        data = response.json()
        assert response.status_code == 200
        assert data.keys() == {
            'count',
            'next',
            'previous',
            'results'
        }
        results = data.get('results')
        assert type(results) == list
        assert len(results) == 1

    def test_ipr_subordinates_get_list(self):
        response = self.client.get(
            path=GET_SUBORDINATES_IPRS_LIST_URL
        )

        data = response.json()
        assert response.status_code == 200
        assert data.keys() == {
            'count',
            'next',
            'previous',
            'results'
        }
        results = data.get('results')
        assert type(results) == list
        assert len(results) == 1

    def test_ipr_get_obj(self):
        response = self.client.get(
            path=reverse(
                'api:iprs-detail',
                args=(self.ipr.pk,)
            )
        )
        data = response.json()
        assert response.status_code == 200
        assert data.keys() == {
            'id', 'title', 'employee', 'author',
            'description', 'status', 'created_date',
            'start_date', 'end_date'
        }

    def test_ipr_update(self):
        response = self.client.patch(
            reverse(
                'api:iprs-detail',
                args=(self.ipr.pk,)
            ),
            data=json.dumps(
                {
                    'status': Ipr.DONE,
                }
            ),
            content_type='application/json'
        )
        data = response.json()
        assert response.status_code == 200
        assert data.get('status') == Ipr.DONE
    
    def test_ipr_delete(self):
        response = self.client.delete(
            reverse(
                'api:iprs-detail',
                args=(self.ipr.pk,)
            )
        )
        assert response.status_code == 204

    def test_task_get_list(self):
        response = self.client.get(
            path=reverse(
                'api:task-list', args=(self.ipr.pk,)
            )
        )
        data = response.json()
        assert response.status_code == 200
        assert type(data) == list
        assert len(data) == 1
    
    def test_task_get(self):
        response = self.client.get(
            path=reverse(
                'api:task-detail',
                args=(self.ipr.pk, self.task.pk)
            )
        )
        data = response.json()
        assert response.status_code == 200
        assert data.keys() == {
            'id', 'title', 'description', 'status',
            'author', 'ipr', 'end_date', 'created_date',
            'start_date'
        }

    def test_task_update(self):
        response = self.client.patch(
            path=reverse(
                'api:task-detail',
                args=(self.ipr.pk, self.task.pk)
            ),
            data=json.dumps(
                {
                    'status': Task.CANCELED,
                }
            ),
            content_type='application/json'
        )
        data = response.json()
        assert response.status_code == 200
        assert data.keys() == {
            'id', 'title', 'description', 'status',
            'author', 'end_date', 'created_date',
            'start_date'
        }
        assert data.get('status') == Task.CANCELED

    def test_task_delete(self):
        response = self.client.delete(
            path=reverse(
                'api:task-detail',
                args=(self.ipr.pk, self.task.pk)
            )
        )
        assert response.status_code == 204
