from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from unittest.mock import patch

# This function is used to find the project's user model.
User = get_user_model()


class LoginViewTest(TestCase):

	# patch decorator lets you specify an object to mock out
	# Here we are mocking out are authenticate function
    @patch('accounts.views.authenticate')
	# Decorator adds the mock object as an additional argument to the function
    def test_calls_authenticate_with_assertion_from_post(
        self, mock_authenticate
    ):
		# We cab configure the mock to have certain behaviors
		# Here we set our mock to return None
        mock_authenticate.return_value = None  #3
        self.client.post('/accounts/login', {'assertion': 'assert this'})
		# Mocks can make assertions!
        mock_authenticate.assert_called_once_with(assertion='assert this')
        
    @patch('accounts.views.authenticate')
    def test_returns_OK_when_user_found(
        self, mock_authenticate
    ):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_authenticate.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(response.content.decode(), 'OK')
        
    @patch('accounts.views.authenticate')
    def test_gets_logged_in_session_if_authenticate_returns_a_user(
        self, mock_authenticate
    ):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'a'})
        # Django test client keeps track of the session for its user.
        # We check that user ID is associated with the session
        self.assertEqual(self.client.session[SESSION_KEY], user.pk)


    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_None(
        self, mock_authenticate
    ):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        # We check that the SESSION_KEY does not appear in their session
        self.assertNotIn(SESSION_KEY, self.client.session)
    