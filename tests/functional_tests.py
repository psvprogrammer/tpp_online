from selenium import webdriver
import unittest
import sys

# try:
#     HOSTNAME = sys.argv[1]
#     print(HOSTNAME)
# except:
#     HOSTNAME = 'http://localhost:8000'


class StartTests(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.addCleanup(self.browser.quit)

    def test_first(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Django', self.browser.title)
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')


