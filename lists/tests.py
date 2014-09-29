from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from lists.models import Item
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
        
class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item_text = 'The first (ever) list item'
        first_item.text = first_item_text
        first_item.save()
        
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, first_item_text)
        self.assertEqual(second_saved_item.text, 'Item the second')
        
class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')
        
        ## Instead of calling the view function directly, we use the Django
        ## test client
        response = self.client.get('/lists/the-only-list-in-the-world/')
        
        # Django provides the assertContains method which knows how to deal
        # with responses and the bytes of their content
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        
class NewListTest(TestCase):
    
        
    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        
    def test_redirects_after_POST(self):
        print("here")
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
        