from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys


class FunctionalTest(StaticLiveServerTestCase):
    
    # Class method similar to setUp, but only executed once, rather
    # than before each test method
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            # Look for liveserver command-line argument
            if 'liveserver' in arg:
                # If we find it, tell test class to skip the normal setUpClass
                # and just store away our staging server URL in a variable
                # server_url instead
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url
    
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    
    def setUp(self): # setUp and tearDown are run before and after each test
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3) # Tells selenium to wait a few seconds if it needs to, so that pages can complete loading before it tries to do anything
    
    def tearDown(self):
        self.browser.quit()
        
    # Note: does not start with test_, so will not be run as a test.
    # Solely for my own purposes
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
        
    def wait_to_be_logged_in(self, email):
        self.wait_for_element_with_id('id_logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(email, navbar.text)


    def wait_to_be_logged_out(self, email):
        self.wait_for_element_with_id('id_login')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(email, navbar.text)