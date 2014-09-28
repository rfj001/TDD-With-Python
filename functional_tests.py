# The comments tell our human-readable story for our functional test

from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase): # Tests are organized into classes inherited from unittest.TestCase
    
    def setUp(self): # setUp and tearDown are run before and after each test
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3) # Tells selenium to wait a few seconds if it needs to, so that pages can complete loading before it tries to do anything
    
    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self): # Any method whose name starts with test is a test method, and is run by the test runner. Descriptive names are good, too.
        # Edith has heard about a cool new online to-do app. She goes to
        # check out its homepage
        self.browser.get('http://localhost:8000')
        
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title) # Asserts that the text 'To-Do' is found within self.browser.title. We have other test assertions as well, like assertEqual, assertTrue, etc.
        self.fail('Finish the test!') # Fails no matter what, displaying the message
	

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" inot a text box (Edith's hobby is tying
        # fly-fishing lures)

        # When she hits enter, the page updates, and now the page lists "1: Buy peacock
        # feathers" as an item in a to-do list

        # There is still a text box inviting her to add another item. She enters 
        # "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees that
        # the site has generated a unique URL for her -- there is some explanatory
        # text to that effect

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.

        browser.quit()
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
