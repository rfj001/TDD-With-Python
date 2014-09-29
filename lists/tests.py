from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page # Function we write in views.py

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        # django uses resolve to resolve URLS and find what
        # functions they should map to.
        found = resolve('/') 
        # Here we check that resolve called with '/' finds a 
        # function called home_page
        self.assertEqual(found.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        # Create HttpRequest object, which is what Django sees when
        # user asks for a page
        request = HttpRequest()
        # Pass request to our home_page view, giving us a response.
        # Response is of type HttpResponse
        response = home_page(request)
        # Assert that the content of the response has certain
        # properties
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)
        # Since we specify this criteria in our functional test, we should
        # check it here in our view's unit test
        # Unit test is driven by the functional test
        self.assertIn(b'<title>To-Do lists</title>', response.content)    
        