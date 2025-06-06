from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Note


class NoteAPITestCase(APITestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')

        # Authenticate user1 by default
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

        # Create a sample note for user1
        self.note = Note.objects.create(
            owner=self.user1,
            title='Test Note',
            content='This is a test note.'
        )

    def test_authentication_required(self):
        unauth_client = APIClient()
        response = unauth_client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_notes(self):
        response = self.client.get('/api/notes/', format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_create_note(self):
        data = {
            "data": {
                "type": "Note",
                "attributes": {
                    "title": "New Note",
                    "content": "This is a new note."
                }
            }
        }
        response = self.client.post('/api/notes/', data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(Note.objects.last().title, 'New Note')

    def test_retrieve_note_detail(self):
        response = self.client.get(f'/api/notes/{self.note.id}/', format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.note.title)

    def test_update_note(self):
        data = {
            "data": {
                "type": "Note",
                "id": str(self.note.id),
                "attributes": {
                    "title": "Updated Note",
                    "content": "Updated content."
                }
            }
        }
        response = self.client.put(f'/api/notes/{self.note.id}/', data, format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note')

    def test_delete_note(self):
        response = self.client.delete(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_see_others_notes(self):
        # Login as user2
        self.client.logout()
        self.client.force_authenticate(user=self.user2)

        response = self.client.get('/api/notes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # Try to access user1's note
        response = self.client.get(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_others_notes(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user2)

        data = {'title': 'Hacked', 'content': 'Hacked content'}
        response = self.client.put(f'/api/notes/{self.note.id}/', data,format='vnd.api+json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_delete_others_notes(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(f'/api/notes/{self.note.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)