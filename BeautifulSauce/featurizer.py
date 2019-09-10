import pandas as pd
import numpy as np
import cssutils
import logging
import os
from os.path import dirname, abspath

cssutils.log.setLevel(logging.CRITICAL)


class Featurizer():
    def __init__(
            self,
            keep_css_attrs=None):

        css_attrs_file = os.path.join(
            dirname(abspath(__file__)),
            'css_attrs.csv'
        )

        self.features = {
            'categorical': {},
            'numerical': {},
            'text': {}
        }

        self.css_attrs_info = pd.read_csv(css_attrs_file) \
                                .set_index('attr')['inherited'].to_dict()

        if not keep_css_attrs:
            self.keep_css_attrs = list(self.css_attrs_info.keys())
        else:
            self.keep_css_attrs = keep_css_attrs

    def add_categorical_feature(self, feature_name):
        """Decorator factory for adding features.

        Normally you would do a closure here for your decorated function
        since we are just abusing decorators, we don't need to actually
        modify the function at all, so we simply return it as-is after
        adding it to our dictionary of features.

        Args:
            feature_name (str): Feature name

        Returns:
            function: The function to be decorated with given name.
        """
        def decorator(fn):

            if feature_name in self.features['categorical']:
                raise RuntimeError(
                    'Feature name %s already in use!' % feature_name
                )
            else:
                self.features['categorical'][feature_name] = fn
            return fn
        return decorator

    def add_numerical_feature(self, feature_name):
        def decorator(fn):

            if feature_name in self.features['numerical']:
                raise RuntimeError(
                    'Feature name %s already in use!' % feature_name
                )
            else:
                self.features['numerical'][feature_name] = fn
            return fn
        return decorator

    def add_text_feature(self, feature_name):
        def decorator(fn):

            if feature_name in self.features['text']:
                raise RuntimeError(
                    'Feature name %s already in use!' % feature_name
                )
            else:
                self.features['text'][feature_name] = fn
            return fn
        return decorator

    def label(self, sauce_root):
        for sauce_node in list(sauce_root.find_all()):

            # TODO - Could  be done in the BeautifulSauce class instead?
            if sauce_node.features is None:
                sauce_node.features = {
                    'categorical': {},
                    'numerical': {},
                    'text': {}
                }

            for category in self.features.keys():
                sauce_node.features[category] = {
                    feature_name: fn(sauce_node)
                    for feature_name, fn in self.features[category].items()
                }

    def get_css_attrs(self, node):
        css_attrs = {}
        style = node.get('style', None)
        if style:
            css = dict(cssutils.parseStyle(style))
            css_attrs = {k: css.get(k, None)
                         for k in self.keep_css_attrs}
        if node.name in ['i', 'em']:
            css_attrs['font-style'] = 'italic'
        if node.name in ['b', 'strong']:
            css_attrs['font-weight'] = 'bold'

        if css_attrs:
            return css_attrs
        else:
            return None

    def apply_css_attrs(self, sauce_root):
        # loop over all soup
        for sauce_node in list(sauce_root.find_all()):
            # Extract css attributes
            css_attrs = self.get_css_attrs(sauce_node)
            if css_attrs:
                css_attrs = {k: css_attrs.get(k, None)
                             for k in self.keep_css_attrs}
                sauce_node.css_attrs = css_attrs

                for k, v in css_attrs.items():
                    if self.css_attrs_info[k]:
                        for child_node in sauce_node.find_all():
                            if not child_node.css_attrs:
                                child_node.css_attrs = {k: v}
                            else:
                                child_node.css_attrs[k] = v
            else:
                if sauce_node.css_attrs is None:
                    sauce_node.css_attrs = {k: None
                                            for k in self.keep_css_attrs}
                else:
                    for attr in self.keep_css_attrs:
                        if sauce_node.css_attrs.get(attr, None) is None:
                            sauce_node.css_attrs[attr] = None

    def featurize(self, soup):
        self.apply_css_attrs(soup)
        self.label(soup)

    def to_dataframe(self, sauce_root, include_css=False, normalize=False):

        column_names = []
        for category in self.features.keys():
            for feature_name in self.features[category].keys():
                column_names.append(feature_name)

        if len(column_names) < 1:
            raise RuntimeError(
                'No features to extract.'
            )

        # List that will initialize our dataframe
        data = []
        for i, sauce_node in enumerate(sauce_root.find_all()):
            row_data = []

            for category in ['categorical', 'numerical', 'text']:
                for feature, value in sauce_node.features[category].items():
                    row_data.append(value)

            if include_css:
                for attr, value in sauce_node.css_attrs.items():
                    if i == 0:
                        column_names.append(attr)
                    row_data.append(value)

            data.append(row_data)

        df = pd.DataFrame(data, columns=column_names)

        if normalize:
            dummy_df = self.dummify(df)
            normed_df = self.normalize(df)

            if dummy_df is None and normed_df is not None:
                df = normed_df
            elif dummy_df is not None and normed_df is None:
                df = dummy_df
            elif dummy_df is None and normed_df is None:
                raise RuntimeError(
                    'No features to normalize.'
                )
            else:
                df = pd.concat([normed_df, dummy_df], axis=1)

        return df

    def dummify(self, df):
        cat_attrs = list(self.features['categorical'].keys())
        if len(cat_attrs) == 0:
            return None
        dummy_df = pd.get_dummies(df[cat_attrs])
        return dummy_df

    def normalize(self, df):
        num_attrs = list(self.features['numerical'].keys())
        if len(num_attrs) == 0:
            return None
        num_df = df[num_attrs] + 1e-4
        num_df = num_df.apply(np.log)
        num_df = (num_df - num_df.min()) / (num_df.max() - num_df.min())
        return num_df
