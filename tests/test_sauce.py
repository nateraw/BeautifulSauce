import unittest
from BeautifulSauce import Sauce
from bs4 import BeautifulSoup as bs
import requests


class TestSauce(unittest.TestCase):
    """Tests of Sauce objects"""

    args = {
        "testfile_1": "tests/test_files/example_1.html",
        "testfile_2": "tests/test_files/example_2.html"
    }

    def test_init(self):
        with open(self.args['testfile_1'], "r") as f:
            soup = bs(f, 'lxml')

        with open(self.args['testfile_1'], "r") as f:
            sauce = Sauce(f)

        self.assertEqual(soup, sauce)

    def test_from_file(self):

        with open(self.args['testfile_1'], "r") as f:
            soup = bs(f, 'lxml')

        sauce = Sauce.from_file(self.args['testfile_1'])
        self.assertEqual(soup, sauce)

    def test_from_url(self):
        url = "https://en.wikipedia.org/wiki/Grace_Hopper"
        r = requests.get(url)
        content = r.text
        soup = bs(content, 'lxml')

        sauce = Sauce.from_url(url)
        self.assertEqual(soup, sauce)

    def test_assign_idxs(self):
        sauce = Sauce.from_file(self.args['testfile_1'])
        tags = list(sauce.find_all())
        self.assertEqual(tags[0].idx, [0])
        self.assertEqual(tags[2].idx, [0, 0, 0])
        self.assertEqual(tags[7].idx, [0, 1, 3])

        sauce = Sauce.from_file(self.args['testfile_2'])
        tags = list(sauce.find_all())
        self.assertEqual(tags[0].idx, [0])
        self.assertEqual(tags[5].idx, [0, 1, 1])
        self.assertEqual(tags[11].idx, [0, 1, 2, 0])
        self.assertEqual(tags[13].idx, [0, 1, 4])

    def test_get_from_idx(self):
        soup = Sauce.from_file(self.args['testfile_1'])
        tags = list(soup.find_all())
        self.assertEqual(tags[0], soup.get_from_idx([0]))
        self.assertEqual(tags[2], soup.get_from_idx([0, 0, 0]))
        self.assertEqual(tags[7], soup.get_from_idx([0, 1, 3]))

        soup = Sauce.from_file(self.args['testfile_2'])
        tags = list(soup.find_all())
        self.assertEqual(tags[0], soup.get_from_idx([0]))
        self.assertEqual(tags[5], soup.get_from_idx([0, 1, 1]))
        self.assertEqual(tags[11], soup.get_from_idx([0, 1, 2, 0]))
        self.assertEqual(tags[13], soup.get_from_idx([0, 1, 4]))

if __name__ == '__main__':
    unittest.main()
