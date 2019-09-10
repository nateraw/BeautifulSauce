from bs4 import BeautifulSoup
from BeautifulSauce import NavigableString
import requests


class Sauce(BeautifulSoup):
    """Sauce is BeautifulSoup's saucy sibling.

    Sauce's purpose is to featurize HTML so you can
    analyze the contents. It functions the same as
    BeautifulSoup, but is there for you when you need
    to dive deep into the details of HTML.

    For the sake of readability, you can treat Sauce
    as if it were BeautifulSoup. So, we still call
    Sauce objects 'soup' unless we are using both
    libraries at the same time.
    """

    def __init__(
            self, markup="", features='lxml',
            builder=None, parse_only=None,
            from_encoding=None,
            exclude_encodings=None, **kwargs):

        super().__init__(markup, features)
        self.assign_idxs()

    @classmethod
    def from_file(
            cls, filepath, features='lxml',
            builder=None, parse_only=None,
            from_encoding=None,
            exclude_encodings=None, **kwargs):
        """Alternate constructor to init soup from filepath.

        Args:
            filepath (str): Path to file holding HTML.

        Returns:
            Sauce: A soup object with added functionality.
        """
        with open(filepath, 'r') as f:
            return cls(f, features, builder,
                       parse_only, from_encoding,
                       exclude_encodings, **kwargs)

    @classmethod
    def from_url(
            cls, url, features='lxml',
            builder=None, parse_only=None,
            from_encoding=None,
            exclude_encodings=None, **kwargs):
        """Alternate constructor to init soup requested url.

        Args:
            url (str): URL to request and sauceify.

        Returns:
            Sauce: A soup object with added functionality.
        """
        r = requests.get(url)

        return cls(r.text, features, builder,
                   parse_only, from_encoding,
                   exclude_encodings, **kwargs)

    def assign_idxs(self):
        """Assigns tree indices to Tag objects.

        Once this function is run, all tags will have
        the .idx attribute so you can access the indices.

        >>> soup = Sauce('<html><body><div></div><p></p></body></html>')
        >>> tags = list(soup.find_all())
        >>> tags[3].name, tags[3].idx
        ('p', None)
        >>> soup.assign_idxs()
        >>> tags[3].idx
        [0, 0, 1]
        """
        for i, tag in enumerate(self.find_all()):
            # In first example, some parent tags not found.
            prev_sibs = len(list(tag.find_previous_siblings()))

            # Here, we incorporate their indexes in the tree.
            if i == 0:
                for p, parent in enumerate(reversed(list(tag.parents))):
                    parent.idx = [p]
                tag.idx = [tag.parent.idx[0]]
            else:
                tag.idx = tag.parent.idx + [prev_sibs]

    def get_from_idx(self, indices, node=None):
        if node is None:
            node = self
        index, *rest = indices
        target = [t for t in list(node.children)
                  if not isinstance(t, NavigableString)][index]
        if len(indices) == 1:
            return target
        else:
            return self.get_from_idx(rest, node=target)

    def __str__(self):
        return self.prettify()
