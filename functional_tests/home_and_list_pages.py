# It's usually best to have a separate file for each Page object.
# In this case, HomePage and ListPage are so closely related it's easier
# to keep them together.

ITEM_INPUT_ID = 'id_text'

class HomePage(object):

    def __init__(self, test):
        ## Initialize with an object representing the current test
        self.test = test

    ## Most page objects have a "go to this page" function
    def go_to_home_page(self):
        self.test.browser.get(self.test.server_url)
        self.test.wait_for(self.get_item_input)
        ## Returning just as a convience to enable method chaining
        return self


    def get_item_input(self):
        return self.test.browser.find_element_by_id('id_text')

    ## Function to start a new list. Goes to home page, finds input box, and
    ## sends the new item text to it, as well as a carriage return. Then it 
    ## waits to check that the interaction has completed.
    def start_new_list(self, item_text):  #4
        self.go_to_home_page()
        inputbox = self.get_item_input()
        inputbox.send_keys(item_text + '\n')
        ## The ListPage, initialized just like a HomePage
        list_page = ListPage(self.test)
        ## Wait for a new item. Specify the expected text and expected position
        list_page.wait_for_new_item_in_list(item_text, 1) 
        ## Finally, return list_page object to caller, because they will 
        ## probably find it useful.
        return list_page
        
    def go_to_my_list_page(self):
        self.test.browser.find_element_by_link_text('My lists').click()
        self.test.wait_for(lambda: self.test.assertEqual(
            self.test.browser.find_element_by_tag_name('h1').text,
            'My Lists'
        ))
        
    def get_item_input(self):
        return self.test.browser.find_element_by_id(ITEM_INPUT_ID)
        
class ListPage(object):

    def __init__(self, test):
        self.test = test

    def get_list_table_rows(self):
        return self.test.browser.find_elements_by_css_selector(
            '#id_list_table tr'
        )

    def wait_for_new_item_in_list(self, item_text, position):
        expected_row = '{}: {}'.format(position, item_text)
        self.test.wait_for(lambda: self.test.assertIn(
            expected_row,
            [row.text for row in self.get_list_table_rows()]
        ))
        
    def get_share_box(self):
        return self.test.browser.find_element_by_css_selector(
            'input[name=email]'
        )
        
    def get_shared_with_list(self):
        return self.test.browser.find_elements_by_css_selector(
            '.list-sharee'
        )
        
    def share_list_with(self, email):
        self.get_share_box().send_keys(email + '\n')
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))
        
    def get_item_input(self):
        return self.test.browser.find_element_by_id(ITEM_INPUT_ID)
        
    def add_new_item(self, item_text):
        current_post = len(self.get_list_table_rows())
        self.get_item_input().send_keys(item_text + '\n')
        self.wait_for_new_item_in_list(item_text, current_post + 1)
        
    def get_list_owner(self):
        return self.test.browser.find_element_by_id('id_list_owner').text