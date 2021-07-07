from django.test import TestCase
from django.utils import timezone
import json

from .models import *
from .forms import *



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



class LoginTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', password='testPass')

    def testBasic(self):
        response = self.client.post('/aplikacja/authentication/', {'username': 'testUser', 'password': 'testPass'})
        self.assertRedirects(response, '/aplikacja/')

    def testEmptyUsername(self):
        response = self.client.post('/aplikacja/authentication/', {'password': 'testPass'})
        self.assertRedirects(response, '/aplikacja/login/')

    def testEmptyPassword(self):
        response = self.client.post('/aplikacja/authentication/', {'username': 'testUser'})
        self.assertRedirects(response, '/aplikacja/login/')

    def testBothEmpty(self):
        response = self.client.post('/aplikacja/authentication/', {})
        self.assertRedirects(response, '/aplikacja/login/')

    def testWrongUsername(self):
        response = self.client.post('/aplikacja/authentication/', {'username': 'WRONG', 'password': 'testPass'})
        self.assertRedirects(response, '/aplikacja/login/')

    def testWrongPassword(self):
        response = self.client.post('/aplikacja/authentication/', {'username': 'testUser', 'password': 'WRONG'})
        self.assertRedirects(response, '/aplikacja/login/')


class FileTests(TestCase):
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
        response = self.client.post('/aplikacja/get/ajax/file/', {'fileName': file1.name})
        print(response.content)
        self.assertJSONEqual(response.content, {'fileContent': None, 'sectionList': [], 'summary': None, 'title': 'tempFile1'})
        self.assertEqual(response.status_code, 200)

    def testFileDoesntExist(self):
        self.client.login(username='tempUser1', password='pass1')
        response = self.client.post('/aplikacja/get/ajax/file/', {'fileName': "nonExistingFile"})
        self.assertJSONEqual(response.content, {'error': ''})
        self.assertEqual(response.status_code, 404)





class FileFormTests(TestCase):
    def setUp(self):
        tempUser1 = User.objects.create_user(username="tempUser1", password="pass1")
        Directory.objects.create(name="parentDir", owner=tempUser1, parent=None, creation_date=timezone.now(), availability=True)


    def testEmptyBlob(self):
        parentDir = Directory.objects.get(name="parentDir")
        form = FileForm(data={'name': "someNAme", 'description': 'some Description', 'parent': parentDir, 'blob': None})
        self.assertFalse(form.is_valid())

    def testEmptyFields(self):
        form = FileForm(data={})
        self.assertFalse(form.is_valid())
        form = FileForm(data={'description': 'nice dir', 'parent': 5})
        self.assertFalse(form.is_valid())



class DirectoryFormTests(TestCase):

    def testBasic(self):
        form = DirectoryForm(data={'name': 'someName', 'descrption': "something", 'parent': None})
        self.assertTrue(form.is_valid())
        form = DirectoryForm(data={'name': 'something'})
        self.assertTrue(form.is_valid())
        form = DirectoryForm(data={'name': 'something', 'description': 'blabla'})
        self.assertTrue(form.is_valid())

    def testEmptyFields(self):
        form = DirectoryForm(data={})
        self.assertFalse(form.is_valid())
        form = DirectoryForm(data={'name': 'something', 'parent': 'somestring'})
        self.assertFalse(form.is_valid())

