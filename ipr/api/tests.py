from datetime import datetime
from django.test import TestCase
from django.urls import reverse
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

TASK_TITLE_1 = ''

AUTH_URL = reverse()
GET_USER_URL = reverse()

GET_IPRS_LIST_URL = reverse()
GET_IPR_URL = reverse()
CREATE_IPR_URL = reverse()
UPDATE_IPR_URL = reverse()
DELETE_IPR_URL = reverse()

GET_TASKS_URL = reverse()
GET_TASK_URL = reverse()
CREATE_TASK_URL = reverse()
UPDATE_TASK_URL = reverse()
DELETE_TASK_URL = reverse()

CREATE_COMMENT_URL = reverse()


class TestCaseWithMockData(TestCase):
    def setUp(self):
        self.superior = User.objects.create(
            username=SUPERIOR_LOGIN,
            first_name='Василий',
            last_name='Иванов'
        )
        self.superior.set_password(TEST_PASSWORD)

        self.subordinate = User.objects.create(
            username=SUBORDINATE_LOGIN,
            first_name='Петр',
            last_name='Сидоров'
        )
        self.subordinate.superior.add(self.superior)
        self.subordinate.set_password(TEST_PASSWORD)
        self.subordinate.save()

        self.client = APIClient()


class AuthApiTest(TestCaseWithMockData):
    def test_login(self):
        response = self.client.post(
            path=AUTH_URL,
            data={
                'username': SUPERIOR_LOGIN,
                'password': TEST_PASSWORD
            },
            content_type='application/json'
        )
        assert response.status_code == 200
        response_dict = response.json()
        token_type = response_dict.get('token_type')
        assert token_type == 'Bearer'


class UserApiTest(TestCaseWithMockData):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.superior)

    def test_get_user_obj(self):
        response = self.client.get(
            path=GET_USER_URL.format(pk=self.superior.pk),
        )


class IprApiTests(TestCaseWithMockData):
    def setUp(self):
        super().setUp()

        self.client.force_authenticate(user=self.superior)

        self.IPR_TITLE_1
        self.ipr = Ipr.objects.create(
            title=IPR_TITLE_1,
            employee=self.subordinate,
            author=self.superior,
            description=IPR_DESC_1,
            status=Ipr.NOT_STARTED,
            end_date=IPR_END_DATE_1
        )

        self.task = Task.objects.create(

        )

        self.comment = Comment.objects.create(

        )

    def test_ipr_get_list(self):
        response = self.client.get(
            path=GET_IPRS_LIST_URL
        )

    def test_ipr_get_obj(self):
        response = self.client.get(
            path=GET_IPR_URL.format(pk=self.ipr.pk)
        )

    def test_ipr_update(self):
        response = self.client.patch(
            path=UPDATE_IPR_URL.format(pk=self.ipr.pk),
            data={}
        )
    
    def test_ipr_delete(self):
        response = self.client.delete(
            path=DELETE_IPR_URL.format(pk=self.ipr.pk)
        )

    def test_task_get_list(self):
        response = self.client.get(
            path=GET_TASKS_URL
        )
    
    def test_task_get(self):
        response = self.client.get(
            path=GET_TASK_URL.format(pk=self.task.pk)
        )

    def test_task_update(self):
        response = self.client.patch(
            path=UPDATE_TASK_URL.format(pk=self.task.pk)
        )
    
    def test_task_delete(self):
        response = self.client.delete(
            path=DELETE_TASK_URL.format(pk=self.task.pk)
        )

    def test_comment_create(self):
        response = self.client.post(
            path=CREATE_COMMENT_URL,
            data={}
        )
