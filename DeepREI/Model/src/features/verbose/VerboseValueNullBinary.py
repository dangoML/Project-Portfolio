from src.features.FeatureETLEngineering import FeatureETLEngineering
from collections import Counter
import re
import pandas as pd


class VerboseValueNullBinary(FeatureETLEngineering):
    def __init__(self, col_series, verbose_threshold, verbose_most_common):
        """Instantiate Verbose Feature."""
        super().__init__(col_series)
        self.verbose_most_common = verbose_most_common
        self.verbose_threshold = verbose_threshold

    def run_etl(self):
        """Run ETL of the column."""
        self._replace_nans()
        self._add_is_null_column_df()
        self._clean_string_to_list()
        self._word_count_catergorical()
        self._build_feature_etl_df()

    def _clean_string_to_list(self):
        """Clean up strings and transform them into list of strings."""

        def _remove_punctuation_make_list(row):
            try:
                clean = re.sub(r'[^\w\s]', '', row.lower()).split(' ')
                clean = [x.replace('\n', '') for x in clean]
                return clean

            except:
                # Run it and see if there are many rows with parse error
                return ['none']

        # Lower case string, Remove Punctuation, and Split on ' '
        self.col_etl = self.col_etl.apply(
            lambda x: _remove_punctuation_make_list(x))

    def _word_count_catergorical(self):
        """Create Catergorical columns based on word count thresholds and
        whether or not the current observation contains said word."""

        # Count all instances of a word
        results = Counter()
        self.col_etl.apply(results.update)

        # Make list of words over threshold if most_common = True
        if self.verbose_most_common:
            word_feats = [(x) for (x, y) in results.most_common()
                          if y > self.verbose_threshold]

        # Else Make list of words below threshold if most_common = False
        else:
            word_feats = [(x) for (x, y) in results.most_common()
                          if y <= self.verbose_threshold]

        # For Each word in list, make column and assign Binary value
        for word in word_feats:

            # Return binary, whether iteration is in list of strings
            self.df_etl[f'{self.col_etl.name}_verb_{word}'] = self.col_etl.apply(
                lambda x: 1 if word in x else 0)
