from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        # Asserts that the text 'To-Do' is found within self.browser.title. We have other test assertions as well, like assertEqual, assertTrue, etc.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" inot a text box (Edith's hobby is tying
        # fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists "1: Buy peacock
        # feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn(
            '2: Use peacock feathers to make a fly',
            [row.text for row in rows]
        )

        # There is still a text box inviting her to add another item. She enters 
        # "Use peacock feathers to make a fly" (Edith is very methodical)
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. Then she sees that
        # the site has generated a unique URL for her -- there is some explanatory
        # text to that effect

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep.

        browser.quit()
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
