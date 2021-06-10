from django.test import TestCase
from django.utils import timezone

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


