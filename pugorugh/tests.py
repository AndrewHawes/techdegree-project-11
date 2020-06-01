from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from .models import Dog, UserDog, UserPref
from .choices import Age, Gender, Size, Type

from .views import (
    CreateDogView, DeleteDogView, NextStatusView, PrevStatusView, SetStatusView,
    HideDogView, SetPrefView, UserRegisterView
)

test_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
test_image = SimpleUploadedFile('small.gif', test_gif, content_type='image/gif')

DOG1 = {
    'name': 'Dog1',
    'image': test_image,
    'age': 20,
    'gender': 'm',
    'size': 'l',
    'type': 'm'
}


# MODELS

class DogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Dog.objects.create(
            name='Max',
            image='images/dogs/testdog.jpg',
            breed='Labrador',
            age=27,
            gender='m',
            size='l',
            type='m',
        )

    def test_name(self):
        dog = Dog.objects.get(pk=1)
        self.assertEquals(dog.name, 'Max')

    def test_choices(self):
        dog = Dog.objects.get(pk=1)
        self.assertEqual(dog.gender, Gender.Choices.MALE)
        self.assertEqual(dog.size, Size.Choices.LARGE)
        self.assertEqual(dog.type, Type.Choices.MAMMAL)

    def test_image_filename(self):
        dog = Dog.objects.get(pk=1)
        self.assertEquals(dog.image_filename, 'testdog.jpg')

    def test_age(self):
        dog = Dog.objects.get(pk=1)
        self.assertEqual(dog.age, 27)
        dog.age = 35
        self.assertEqual(dog.age, 35)


class UserDogModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = get_user_model().objects.create(username='User1')
        dog1 = Dog.objects.create(name='Dog1', age=25)
        UserDog.objects.create(user=user1, dog=dog1, status='l')

    def test_userdog_status(self):
        userdog1 = UserDog.objects.get(pk=1)

        self.assertEqual(userdog1.user.username, 'User1')
        self.assertEqual(userdog1.dog.name, 'Dog1')
        self.assertEqual(userdog1.status, 'l')


class UserPrefModelTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create(username='User1')
        self.user2 = get_user_model().objects.create(username='User2')
        self.user3 = get_user_model().objects.create(username='User3')
        self.user4 = get_user_model().objects.create(username='User4')
        self.user5 = get_user_model().objects.create(username='User5')
        self.user6 = get_user_model().objects.create(username='User6')
        self.user7 = get_user_model().objects.create(username='User7')

        self.dog1 = Dog.objects.create(name='Dog1', age=6, gender='m', size='s')
        self.dog2 = Dog.objects.create(name='Dog2', age=42, gender='f', size='s')
        self.dog3 = Dog.objects.create(name='Dog3', age=42, gender='f', size='m', type='r')
        self.dog4 = Dog.objects.create(name='Dog4', age=100, gender='u', size='u')

        self.user1.userpref = UserPref()
        self.user2.userpref = UserPref(age=Age.Choices.YOUNG)
        self.user3.userpref = UserPref(age=Age.Choices.ADULT)
        self.user4.userpref = UserPref(gender=Gender.Choices.FEMALE)
        self.user5.userpref = UserPref(size=Size.Choices.SMALL)
        self.user6.userpref = UserPref(type=Type.Choices.ROBOT)
        self.user7.userpref = UserPref(age=Age.Choices.ADULT, size=Size.Choices.MEDIUM)

    def test_no_filters(self):
        dogs = self.user1.userpref.get_preferred_dogs()
        self.assertEqual(len(dogs), 4)

    def test_age_filter(self):
        dogs = self.user2.userpref.get_preferred_ages()
        preferred_dogs = self.user2.userpref.get_preferred_dogs()
        dogs2 = self.user3.userpref.get_preferred_ages()

        self.assertEqual(len(dogs), 1)
        self.assertQuerysetEqual(dogs, map(repr, preferred_dogs))
        self.assertEqual(len(dogs2), 2)

    def test_gender_filter(self):
        dogs = self.user4.userpref.get_preferred_dogs()
        self.assertEqual(len(dogs), 2)

    def test_size_filter(self):
        dogs = self.user5.userpref.get_preferred_dogs()
        self.assertEqual(len(dogs), 2)

    def test_type_filter(self):
        dogs = self.user6.userpref.get_preferred_dogs()
        self.assertEqual(len(dogs), 1)

    def test_multiple_filters(self):
        dogs = self.user7.userpref.get_preferred_dogs()
        self.assertEqual(len(dogs), 1)

# VIEWS


class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_registration(self):
        data = {'username': 'TestUser', 'password': 'TestPass'}
        url = 'api/user/'
        request = self.factory.post(url, data)
        view = UserRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], 'TestUser')

    def test_bad_username(self):
        data = {'username': 'Test User', 'password': 'TestPass'}
        url = 'api/user/'
        request = self.factory.post(url, data)
        view = UserRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter a valid username.', response.data['username'][0])

    def test_blank_password(self):
        data = {'username': 'TestUser', 'password': ''}
        url = 'api/user/'
        request = self.factory.post(url, data)
        view = UserRegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('field may not be blank', response.data['password'][0])


class CreateDogViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='User1')
        self.factory = APIRequestFactory()

        test_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        test_image = SimpleUploadedFile('small.gif', test_gif, content_type='image/gif')

        self.dog1 = {
            'name': 'Dog1',
            'image': test_image,
            'age': 20,
            'gender': 'm',
            'size': 'l',
            'type': 'm'
        }

    def tearDown(self):
        Dog.objects.filter(name='Dog1').delete()

    def test_create(self):
        url = 'api/dog/new/'
        request = self.factory.post(url, self.dog1, format='multipart')
        view = CreateDogView.as_view()

        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_create_error(self):
        url = 'api/dog/new/'
        invalid_dog = {'name': 'Invalid Dog'}
        request = self.factory.post(url, invalid_dog, format='multipart')
        view = CreateDogView.as_view()

        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 400)


class DeleteDogViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='TestUser')
        self.dog = Dog.objects.create(
            name='DelDog', age=10, gender='m', size='s', added_by=self.user
        )
        self.factory = APIRequestFactory()

    def test_delete(self):
        pk = self.dog.pk
        url = 'api/dog/{}/delete/'.format(pk)
        request = self.factory.delete(url)
        view = DeleteDogView.as_view()

        force_authenticate(request, user=self.user)
        response = view(request, pk=pk)
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Dog.DoesNotExist):
            Dog.objects.get(pk=pk)


class StatusViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='TestUser')
        self.user.userpref = UserPref()

        dog = {'age': 10, 'gender': 'm', 'size': 's'}
        self.udog1 = Dog.objects.create(name='Undecided Dog 1', **dog)
        self.udog2 = Dog.objects.create(name='Undecided Dog 2', **dog)
        self.ldog1 = Dog.objects.create(name='Liked Dog 1', **dog)
        self.ldog2 = Dog.objects.create(name='Liked Dog 2', **dog)
        self.ddog1 = Dog.objects.create(name='Disliked Dog 1', **dog)
        self.ddog2 = Dog.objects.create(name='Disliked Dog 2', **dog)

        UserDog.objects.create(user=self.user, dog=self.ldog1, status='l')
        UserDog.objects.create(user=self.user, dog=self.ldog2, status='l')
        UserDog.objects.create(user=self.user, dog=self.ddog1, status='d')
        UserDog.objects.create(user=self.user, dog=self.ddog2, status='d')

        self.factory = APIRequestFactory()

    def get_response(self, pk, status, url, view, user=None):
        request = self.factory.get(url)
        if not user:
            user = self.user

        force_authenticate(request, user=user)
        response = view(request, pk=pk, status=status)
        return response

    def next_status(self, pk, status, user=None):
        url = f'api/dog/{pk}/{status}/next/'
        view = NextStatusView.as_view()
        return self.get_response(pk, status, url, view, user)

    def prev_status(self, pk, status, user=None):
        url = f'api/dog/{pk}/{status}/prev/'
        view = PrevStatusView.as_view()
        return self.get_response(pk, status, url, view, user)

    def test_next(self):
        u_response = self.next_status(self.udog1.pk, 'undecided')
        l_response = self.next_status(self.ldog1.pk, 'liked')
        d_response = self.next_status(self.ddog1.pk, 'disliked')

        self.assertEqual(u_response.status_code, 200)
        self.assertEqual(u_response.data['name'], 'Undecided Dog 2')
        self.assertEqual(l_response.status_code, 200)
        self.assertEqual(l_response.data['name'], 'Liked Dog 2')
        self.assertEqual(d_response.status_code, 200)
        self.assertEqual(d_response.data['name'], 'Disliked Dog 2')

    def test_prev(self):
        u_response = self.prev_status(self.udog2.pk, 'undecided')
        l_response = self.prev_status(self.ldog2.pk, 'liked')
        d_response = self.prev_status(self.ddog2.pk, 'disliked')

        self.assertEqual(u_response.status_code, 200)
        self.assertEqual(u_response.data['name'], 'Undecided Dog 1')
        self.assertEqual(l_response.status_code, 200)
        self.assertEqual(l_response.data['name'], 'Liked Dog 1')
        self.assertEqual(d_response.status_code, 200)
        self.assertEqual(d_response.data['name'], 'Disliked Dog 1')
        self.assertTrue(d_response.data['first'])

    def test_last(self):
        u_response = self.next_status(5, 'undecided')

        self.assertEqual(u_response.status_code, 404)
        self.assertEqual(u_response.data['detail'], 'Last Entry')

    def test_first(self):
        u_response = self.prev_status(1, 'undecided')
        l_response = self.prev_status(0, 'liked')

        self.assertEqual(u_response.status_code, 200)
        self.assertEqual(u_response.data['name'], 'Undecided Dog 1')
        self.assertTrue(u_response.data['first'])

        self.assertEqual(l_response.status_code, 200)
        self.assertEqual(l_response.data['name'], 'Liked Dog 1')
        self.assertTrue(l_response.data['first'])

    def test_no_liked_or_disliked_dogs(self):
        user = get_user_model().objects.create(username='NewTestUser')

        next_l_response = self.next_status(1, 'liked', user)
        prev_l_response = self.prev_status(1, 'liked', user)
        next_d_response = self.next_status(1, 'disliked', user)
        prev_d_response = self.prev_status(1, 'disliked', user)

        self.assertEqual(next_l_response.status_code, 404)
        self.assertEqual(next_l_response.data['detail'], 'No Results')
        self.assertEqual(prev_l_response.data['detail'], 'No Results')
        self.assertEqual(next_d_response.data['detail'], 'No Results')
        self.assertEqual(prev_d_response.data['detail'], 'No Results')


class ModifyUserDogTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='TestUser')

        dog = {'age': 10, 'gender': 'm', 'size': 's'}
        self.udog = Dog.objects.create(name='Undecided Dog 1', **dog)
        self.ldog = Dog.objects.create(name='Liked Dog 1', **dog)
        self.ddog = Dog.objects.create(name='Disliked Dog 1', **dog)

        UserDog.objects.create(user=self.user, dog=self.ldog, status='l')
        UserDog.objects.create(user=self.user, dog=self.ddog, status='d')

        self.factory = APIRequestFactory()

    def set_status(self, dog, status):
        pk = dog.pk
        url = f'api/dog/{pk}/{status}/'
        request = self.factory.put(url)
        view = SetStatusView.as_view()

        force_authenticate(request, user=self.user)
        response = view(request, pk=pk, status=status)
        return response

    def test_set_status(self):
        res1 = self.set_status(self.udog, 'disliked')
        res2 = self.set_status(self.ldog, 'undecided')
        res3 = self.set_status(self.ddog, 'liked')
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res3.status_code, 200)

        udog = UserDog.objects.get(user=self.user, dog=self.udog)
        ddog = UserDog.objects.get(user=self.user, dog=self.ddog)
        self.assertEqual(udog.status, 'd')
        self.assertEqual(ddog.status, 'l')

        with self.assertRaises(UserDog.DoesNotExist):
            UserDog.objects.get(user=self.user, dog=self.ldog)

    def hide_dog(self, dog):
        pk = dog.pk
        url = f'api/dog/{pk}/hide/'
        request = self.factory.put(url)
        view = HideDogView.as_view()

        force_authenticate(request, user=self.user)
        response = view(request, pk=pk)
        return response

    def test_hide_dog(self):
        res1 = self.hide_dog(self.udog)
        res2 = self.hide_dog(self.ldog)

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

        ud1 = UserDog.objects.get(user=self.user, dog=self.udog)
        ud2 = UserDog.objects.get(user=self.user, dog=self.ldog)
        ud3 = UserDog.objects.get(user=self.user, dog=self.ddog)

        self.assertTrue(ud1.hidden)
        self.assertTrue(ud2.hidden)
        self.assertFalse(ud3.hidden)


class SetPrefViewTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='TestUser')
        self.factory = APIRequestFactory()
        self.view = SetPrefView.as_view()

    def test_get_and_set_prefs(self):
        url = 'api/user/preferences/'

        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

        new_prefs = {'age': 'b,y', 'gender': 'f', 'size': 's', 'type': 'r'}
        request = self.factory.put(url, new_prefs)
        force_authenticate(request, user=self.user)
        response = self.view(request)

        userpref = response.data
        userpref.pop('id')
        self.assertDictEqual(userpref, new_prefs)
