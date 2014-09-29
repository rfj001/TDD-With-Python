from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page # Function we write in views.py

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        # django uses resolve to resolve URLS and find what
        # functions they should map to.
        found = resolve('/') 
        # Here we check that resolve called with '/' finds a 
        # function called home_page
        self.assertEqual(found.func, home_page)
        