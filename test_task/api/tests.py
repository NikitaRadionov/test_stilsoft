from django.test import TestCase
from django.test import Client
from .models import ApiUser, Section, UserSection

# Create your tests here.
class TestCreateSection(TestCase):

    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/sections/create"

        nikita_response = nikita.post(path, {"title": "section1"})
        radion_response = radion.post(path, {"title": "section2"})
        dmitry_response = dmitry.post(path, {"title": "section3"})

        Section.objects.get(title="section2").delete()
        Section.objects.get(title="section3").delete()

        self.assertFalse(nikita_response.json()['success'])
        self.assertTrue(radion_response.json()['success'])
        self.assertTrue(dmitry_response.json()['success'])


    def test_DoubleCreateSection(self):
        radion, dmitry = Client(), Client()
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/sections/create"

        radion_response = radion.post(path, {"title": "section"})
        dmitry_response = dmitry.post(path, {"title": "section"})

        Section.objects.get(title="section").delete()
        self.assertTrue(radion_response.json()['success'])
        self.assertFalse(dmitry_response.json()['success'])


class TestDeleteSection(TestCase):


    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            try:
                Section.objects.get(title=f"section{i}").delete()
            except Section.DoesNotExist:
                pass


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/sections/delete"

        nikita_response = nikita.delete(path, {"title": "section1"}, content_type='application/json')
        radion_response = radion.delete(path, {"title": "section2"}, content_type='application/json')
        dmitry_response = dmitry.delete(path, {"title": "section3"}, content_type='application/json')

        self.assertFalse(nikita_response.json()['success'])
        self.assertFalse(radion_response.json()['success'])
        self.assertTrue(dmitry_response.json()['success'])


    def test_DoubleDeleteSection(self):
        dmitry = Client()
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/sections/delete"

        dmitry_firstResponse = dmitry.delete(path, {"title": "section1"}, content_type='application/json')
        dmitry_secondResponse = dmitry.delete(path, {"title": "section1"}, content_type='application/json')

        self.assertTrue(dmitry_firstResponse.json()['success'])
        self.assertFalse(dmitry_secondResponse.json()['success'])


class TestJoinSection(TestCase):

    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            Section.objects.get(title=f"section{i}").delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/student/joinSection"

        nikita_response = nikita.post(path, {"title": "section1"})
        radion_response = radion.post(path, {"title": "section2"})
        dmitry_response = dmitry.post(path, {"title": "section3"})

        UserSection.objects.get(section=Section.objects.get(title="section1")).delete()

        self.assertTrue(nikita_response.json()["success"])
        self.assertFalse(radion_response.json()["success"])
        self.assertFalse(dmitry_response.json()["success"])


    def test_DoubleJoinSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        path = "/api/student/joinSection"

        nikita_firstResponse = nikita.post(path, {"title": "section1"})
        nikita_secondResponse = nikita.post(path, {"title": "section1"})

        UserSection.objects.get(section=Section.objects.get(title="section1")).delete()

        self.assertTrue(nikita_firstResponse.json()['success'])
        self.assertFalse(nikita_secondResponse.json()['success'])


    def test_JoinNonExistentSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        path = "/api/student/joinSection"

        nikita_response = nikita.post(path, {"title": "nonExistentSection"})

        self.assertFalse(nikita_response.json()["success"])


class TestLeaveSection(TestCase):


    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")

        UserSection.objects.create(student = ApiUser.objects.get(username="test_nikita"),
                                   section = Section.objects.get(title="section1"))


    def tearDown(self):

        try:
            UserSection.objects.get(student = ApiUser.objects.get(username="test_nikita"),
                                    section= Section.objects.get(title="section1"))
        except UserSection.DoesNotExist:
            pass

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            Section.objects.get(title=f"section{i}").delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/student/leaveSection"

        nikita_response = nikita.delete(path, {"title": "section1"}, content_type='application/json')
        radion_response = radion.delete(path, {"title": "section2"}, content_type='application/json')
        dmitry_response = dmitry.delete(path, {"title": "section3"}, content_type='application/json')

        self.assertTrue(nikita_response.json()["success"])
        self.assertFalse(radion_response.json()["success"])
        self.assertFalse(dmitry_response.json()["success"])


    def test_DoubleLeaveSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        path = "/api/student/leaveSection"

        nikita_firstResponse = nikita.delete(path, {"title": "section1"}, content_type='application/json')
        nikita_secondResponse = nikita.delete(path, {"title": "section1"}, content_type='application/json')

        self.assertTrue(nikita_firstResponse.json()['success'])
        self.assertFalse(nikita_secondResponse.json()['success'])


    def test_LeaveNonExistentSection(self):
        nikita = Client()
        nikita.login(username='test_nikita', password='1234')

        path = "/api/student/leaveSection"

        nikita_response = nikita.delete(path, {"title": "nonExistentSection"}, content_type='application/json')

        self.assertFalse(nikita_response.json()["success"])


class TestLeadeSection(TestCase):


    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            Section.objects.create(title=f"section{i}")


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            Section.objects.get(title=f"section{i}").delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/teacher/leadSection"

        nikita_response = nikita.patch(path, {"title": "section1"}, content_type='application/json')
        radion_response = radion.patch(path, {"title": "section2"}, content_type='application/json')
        dmitry_response = dmitry.patch(path, {"title": "section3"}, content_type='application/json')

        self.assertFalse(nikita_response.json()["success"])
        self.assertTrue(radion_response.json()["success"])
        self.assertFalse(dmitry_response.json()["success"])


    def test_DoubleLeadeSection(self):
        radion = Client()
        radion.login(username='test_radion', password='1234')

        path = "/api/teacher/leadSection"

        radion_firstResponse = radion.patch(path, {"title": "section1"}, content_type='application/json')
        radion_secondResponse = radion.patch(path, {"title": "section1"}, content_type='application/json')

        self.assertTrue(radion_firstResponse.json()['success'])
        self.assertFalse(radion_secondResponse.json()['success'])


    def test_LeadeNonExistentSection(self):
        radion = Client()
        radion.login(username='test_radion', password='1234')

        path = "/api/teacher/leadSection"

        radion_response = radion.patch(path, {"title": "nonExistentSection"}, content_type='application/json')

        self.assertFalse(radion_response.json()["success"])


class TestUnleadeSection(TestCase):


    def setUp(self):

        users_data = (('test_nikita', '1234' ,'STUDENT'),
                      ('test_radion', '1234', 'TEACHER'),
                      ('test_dmitry', '1234', 'MODERATOR'))

        for username, password, role in users_data:
            ApiUser.objects.create_user(username=username, password=password, role=role)

        for i in range(1, 4):
            if i == 2:
                Section.objects.create(title=f"section{i}", teacher=ApiUser.objects.get(username='test_radion'))
            else:
                Section.objects.create(title=f"section{i}")


    def tearDown(self):

        usernames = ('test_nikita', 'test_radion', 'test_dmitry')

        for username in usernames:
            ApiUser.objects.get(username=username).delete()

        for i in range(1, 4):
            Section.objects.get(title=f"section{i}").delete()


    def test_RoleRequest(self):
        nikita, radion, dmitry = Client(), Client(), Client()
        nikita.login(username='test_nikita', password='1234')
        radion.login(username='test_radion', password='1234')
        dmitry.login(username='test_dmitry', password='1234')

        path = "/api/teacher/leaveSection"

        nikita_response = nikita.patch(path, {"title": "section1"}, content_type='application/json')
        radion_response = radion.patch(path, {"title": "section2"}, content_type='application/json')
        dmitry_response = dmitry.patch(path, {"title": "section3"}, content_type='application/json')

        self.assertFalse(nikita_response.json()["success"])
        self.assertTrue(radion_response.json()["success"])
        self.assertFalse(dmitry_response.json()["success"])


    def test_DoubleLeadeSection(self):
        radion = Client()
        radion.login(username='test_radion', password='1234')

        path = "/api/teacher/leaveSection"

        radion_firstResponse = radion.patch(path, {"title": "section2"}, content_type='application/json')
        radion_secondResponse = radion.patch(path, {"title": "section2"}, content_type='application/json')

        self.assertTrue(radion_firstResponse.json()['success'])
        self.assertFalse(radion_secondResponse.json()['success'])


    def test_LeadeNonExistentSection(self):
        radion = Client()
        radion.login(username='test_radion', password='1234')

        path = "/api/teacher/leaveSection"

        radion_response = radion.patch(path, {"title": "nonExistentSection"}, content_type='application/json')

        self.assertFalse(radion_response.json()["success"])
