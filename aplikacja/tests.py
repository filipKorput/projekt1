from django.test import TestCase
from django.utils import timezone
import json

from .models import *



class DirectoryModelTests(TestCase):
    def setUp(self):
        admin = User.objects.create(username="tempAdmin", password="pass")
        Directory.objects.create(name="tempParent", owner=admin, parent=None, creation_date=timezone.now(), availability=True)
        parent = Directory.objects.get(name="tempParent")
        Directory.objects.create(name="tempDir", owner=admin, parent=parent, creation_date=timezone.now(), availability=True, description="someDescription")

    def testBasics(self):
        tempDir = Directory.objects.get(name="tempDir")
        self.assertTrue(tempDir.availability)
        self.assertTrue(tempDir.validity)
        self.assertEqual(tempDir.description, "someDescription")
        self.assertIsNotNone(tempDir.parent)

    def testOwner(self):
        admin = User.objects.get(username="tempAdmin")
        tempDir = Directory.objects.get(name="tempDir")
        self.assertEqual(admin, tempDir.owner)

    def testParent(self):
        parent = Directory.objects.get(name="tempParent")
        tempDir = Directory.objects.get(name="tempDir")
        self.assertEqual(parent, tempDir.parent)


class FileModelTests(TestCase):
    def setUp(self):
        admin = User.objects.create(username="tempAdmin", password="pass")
        Directory.objects.create(name="tempParent", owner=admin, parent=None, creation_date=timezone.now(), availability=True)
        parent = Directory.objects.get(name="tempParent")
        File.objects.create(name="tempFile", owner=admin, parent=parent, creation_date=timezone.now(), availability=True, description="someDescription")

    def testBasics(self):
        tempFile = File.objects.get(name="tempFile")
        self.assertTrue(tempFile.availability)
        self.assertTrue(tempFile.validity)
        self.assertEqual(tempFile.description, "someDescription")
        self.assertIsNotNone(tempFile.parent)

    def testOwner(self):
        admin = User.objects.get(username="tempAdmin")
        tempFile = File.objects.get(name="tempFile")
        self.assertEqual(admin, tempFile.owner)

    def testParent(self):
        parent = Directory.objects.get(name="tempParent")
        tempFile = File.objects.get(name="tempFile")
        self.assertEqual(parent, tempFile.parent)


class FileSectionTestCase(TestCase):
    def setUp(self):
        admin = User.objects.create(username="tempAdmin", password="pass")
        dir = Directory.objects.create(name="tempParent", owner=admin, parent=None, creation_date=timezone.now(), availability=True)
        file = File.objects.create(name="tempFile", owner=admin, parent=dir, creation_date=timezone.now(), availability=True, description="someDescription")
        data = Status_Data.objects.create(field='', user=admin)
        Section.objects.create(name="tempSection", parent=file, creation_date=timezone.now(), category="procedure", status="Proved", line=1, status_data=data)

    def testBasics(self):
        section = Section.objects.get(name="tempSection")
        self.assertTrue(section.validity)
        self.assertEquals(section.description, '')

    def testPArent(self):
        file = File.objects.get(name="tempFile")
        section = Section.objects.get(name="tempSection")

        self.assertEquals(section.parent, file)



class AuthenticationTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', password='testPass')

    def testBasic(self):
        response = self.client.post('/aplikacja/authentication/', {'username': 'testUser', 'password': 'testPass'})
        self.assertRedirects(response, '/aplikacja/')

    def testWrongUsername(self):
        response = self.client.post('/aplikacja/authentication/', {'username': 'WRONG', 'password': 'testPass'})
        print(response)
        self.assertRedirects(response, '/aplikacja/login/')

    def test_incorrect_password(self):
        response = self.client.post('/authentication/', {'username': 'testuser', 'password': '123456789'})
        self.assertRedirects(response, '/login/')

    def test_no_username(self):
        response = self.client.post('/authentication/', {'password': '12345678'})
        self.assertRedirects(response, '/login/')


class FileTestCase(TestCase):
    def setUp(self):
        tempUser1 = User.objects.create_user(username="tempUser1", password="pass1")
        tempUser2 = User.objects.create_user(username="tempUser2", password="pass2")

        dir1 = Directory.objects.create(name="tempDir1", owner=tempUser1, parent=None, creation_date=timezone.now(), availability=True)
        self.dir2 = Directory.objects.create(name="tempDir2", owner=tempUser1, parent=dir1, creation_date=timezone.now(), availability=True)
        self.dir3 = Directory.objects.create(name="tempDir3", owner=tempUser2, parent=None, creation_date=timezone.now(), availability=True)

        file1 = File.objects.create(name="tempFile1", owner=tempUser1, parent=dir1, creation_date=timezone.now(), availability=True)
        file2 = File.objects.create(name="tempFile2", owner=tempUser1, parent=dir1, creation_date=timezone.now(), availability=True)
        self.file3 = File.objects.create(name="tempFile3", owner=tempUser1, parent=self.dir2, creation_date=timezone.now(), availability=True)
        self.file4 = File.objects.create(name="tempFile4", owner=tempUser2, parent=self.dir3, creation_date=timezone.now(), availability=True)

    def testGetFile(self):
        file1 = File.objects.get(name="tempFile1")
        self.client.login(username='tempUser1', password='pass1')
        response = self.client.get('/aplikacja/get/ajax/file/', {'fileName': file1.name})
        print(response.content)
        self.assertJSONEqual(response.content, {'title': file1.name, 'sectionList': []})
        self.assertEqual(response.status_code, 200)

