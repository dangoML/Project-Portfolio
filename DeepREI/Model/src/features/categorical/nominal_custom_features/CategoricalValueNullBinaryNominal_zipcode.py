import pandas as pd
from src.features.FeatureETLEngineering import FeatureETLEngineering


class CategoricalValueNullBinaryNominal_zipcode(FeatureETLEngineering):
    def __init__(self, col_series):
        """Instantiate categorical feature."""
        super().__init__(col_series)

    def run_etl(self):
        """Run ETL of the column."""
        self._replace_nans()
        self._add_is_null_column_df()
        self._extract_zipcode()
        self._one_hot_encode_df()
        self._build_feature_etl_df()

    def _extract_zipcode(self):
        """Replace specific string values with float equivalent"""
        self.col_etl = self.col_etl.str.split('_FL_', expand = True)[1]
        self.col_etl = self.col_etl.str.slice(0, 5)
        self.col_etl.name = 'zipcode'
        # self.col_etl.to_csv('zipcodes.csv')