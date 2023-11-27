from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from .forms import SearchForm


class RedactorListViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='admin.user',
            years_of_experience=5,
            first_name='Admin',
            last_name='User',
            password='1qazcde3',
        )
        self.client.force_login(self.user)

        self.redactor1 = get_user_model().objects.create(
            username='testuser1',
            first_name='John',
            last_name='Doe',
            years_of_experience=1,
        )
        self.redactor2 = get_user_model().objects.create(
            username='testuser2',
            first_name='Jane',
            last_name='Doe',
            years_of_experience=2,
        )

    def test_search_view_with_results(self) -> None:
        search_query = 'testuser1'
        response = self.client.get(
            reverse('newspaper:redactor-list'), {'search': search_query}
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn('search_form', response.context)

        self.assertIsInstance(response.context['search_form'], SearchForm)

        self.assertIn(self.redactor1, response.context['redactor_list'])

        self.assertContains(response, self.redactor1.username)
        self.assertContains(response, self.redactor1.first_name)
        self.assertContains(response, self.redactor1.last_name)

    def test_search_view_with_no_results(self) -> None:
        search_query = 'nonexistentuser'
        response = self.client.get(
            reverse('newspaper:redactor-list'), {'search': search_query}
        )

        self.assertEqual(response.status_code, 200)

        self.assertIn('search_form', response.context)

        self.assertIsInstance(response.context['search_form'], SearchForm)

        self.assertQuerysetEqual(response.context['redactor_list'], [])

    def test_search_view_with_empty_query(self) -> None:
        response = self.client.get(reverse('newspaper:redactor-list'))

        self.assertEqual(response.status_code, 200)

        self.assertIn('search_form', response.context)

        self.assertIsInstance(response.context['search_form'], SearchForm)

        self.assertIn(self.redactor1, response.context['redactor_list'])
        self.assertIn(self.redactor2, response.context['redactor_list'])

        self.assertContains(response, self.redactor1.username)
        self.assertContains(response, self.redactor2.username)
