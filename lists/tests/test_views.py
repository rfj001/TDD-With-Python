from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from lists.models import Item, List
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
        
class ListViewTest(TestCase):
    
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id))
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        
        ## Instead of calling the view function directly, we use the Django
        ## test client
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        
        # Django provides the assertContains method which knows how to deal
        # with responses and the bytes of their content
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
        
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
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        
class NewItemTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)
        
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
        