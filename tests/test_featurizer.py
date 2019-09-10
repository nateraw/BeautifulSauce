import unittest
from BeautifulSauce import Sauce
from BeautifulSauce.featurizer import Featurizer
import re


class TestFeaturizer(unittest.TestCase):
    """Tests featurizer and feature creation."""

    args = {
        "testfile_1": "tests/test_files/example_3.html"
    }

    def test_init(self):
        ftrs = Featurizer()
        ftrs = Featurizer(keep_css_attrs=['font-weight', 'margin'])

    def test_add_categorical_ft(self):
        ftrs = Featurizer()

        @ftrs.add_categorical_feature("tag_name")
        def f_tag_name(tag):
            return tag.name

        self.assertEqual(f_tag_name, ftrs.features['categorical']['tag_name'])

    def test_add_numerical_ft(self):
        ftrs = Featurizer()

        @ftrs.add_numerical_feature('is_bold')
        def f_is_bold(tag):
            if tag.css_attrs['font-weight'] == 'bold':
                return True
            else:
                return False
        self.assertEqual(f_is_bold, ftrs.features['numerical']['is_bold'])

    def test_add_text_ft(self):
        ftrs = Featurizer()

        @ftrs.add_text_feature('text')
        def f_text(tag):
            if tag.name in ['head', 'meta', 'script']:
                return ""
            texts = list(tag.find_all(text=True, recursive=False))
            if len(texts) < 1:
                return ""
            texts = " ".join(texts).strip()
            texts = re.sub("\n", " ", texts)
            return texts

        self.assertEqual(f_text, ftrs.features['text']['text'])

    def test_featurize(self):
        ftrs = Featurizer()
        soup = Sauce.from_file(self.args['testfile_1'])

        @ftrs.add_categorical_feature("tag_name")
        def f_tag_name(tag):
            return tag.name

        @ftrs.add_numerical_feature('is_bold')
        def f_is_bold(tag):
            if tag.css_attrs['font-weight'] == 'bold':
                return True
            else:
                return False

        @ftrs.add_text_feature('text')
        def f_text(tag):
            if tag.name in ['head', 'meta', 'script']:
                return ""
            texts = list(tag.find_all(text=True, recursive=False))
            if len(texts) < 1:
                return ""
            texts = " ".join(texts).strip()
            texts = re.sub("\n", " ", texts)
            return texts

        ftrs.featurize(soup)

    def test_to_dataframe(self):
        ftrs = Featurizer()
        soup = Sauce.from_file(self.args['testfile_1'])

        @ftrs.add_categorical_feature("tag_name")
        def f_tag_name(tag):
            return tag.name

        @ftrs.add_numerical_feature('is_bold')
        def f_is_bold(tag):
            if tag.css_attrs['font-weight'] == 'bold':
                return True
            else:
                return False

        @ftrs.add_text_feature('text')
        def f_text(tag):
            if tag.name in ['head', 'meta', 'script']:
                return ""
            texts = list(tag.find_all(text=True, recursive=False))
            if len(texts) < 1:
                return ""
            texts = " ".join(texts).strip()
            texts = re.sub("\n", " ", texts)
            return texts

        ftrs.featurize(soup)
        df = ftrs.to_dataframe(soup)

        filtered = df[df.text.str.contains('bold')]
        self.assertEqual(filtered.is_bold.sum(),
                         len(filtered))

        filtered = df[df.text.str.contains('normal')]
        self.assertEqual(filtered.is_bold.sum(), 0)

    def test_dummify(self):
        ftrs = Featurizer()
        soup = Sauce.from_file(self.args['testfile_1'])

        @ftrs.add_categorical_feature("tag_name")
        def f_tag_name(tag):
            return tag.name

        ftrs.featurize(soup)
        df = ftrs.to_dataframe(soup, normalize=True)

        self.assertEqual(df['tag_name_div'].sum(), 6)
        self.assertEqual(df['tag_name_html'].sum(), 1)
        self.assertEqual(df['tag_name_p'].sum(), 2)

    def test_normalize(self):
        ftrs = Featurizer()
        soup = Sauce.from_file(self.args['testfile_1'])

        @ftrs.add_numerical_feature('char_cnt')
        def f_text(tag):
            if tag.name in ['head', 'meta', 'script']:
                return 0
            texts = list(tag.find_all(text=True, recursive=False))
            if len(texts) < 1:
                return 0
            texts = " ".join(texts).strip()
            texts = re.sub("\n", " ", texts)
            return len(texts)

        ftrs.featurize(soup)
        df = ftrs.to_dataframe(soup, normalize=True)
        self.assertEqual(df['char_cnt'].max(), 1.)
        self.assertEqual(df['char_cnt'].min(), 0.)

if __name__ == '__main__':
    unittest.main()
