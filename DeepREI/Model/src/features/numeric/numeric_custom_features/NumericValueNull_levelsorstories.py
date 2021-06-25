import pandas as pd
from src.features.FeatureETLEngineering import FeatureETLEngineering


class NumericValueNull_levelsorstories(FeatureETLEngineering):
    def __init__(self, col_series):
        """Instantiate categorical feature."""
        super().__init__(col_series)

    def run_etl(self):
        """Run ETL of the column."""
        self._replace_strings_with_floats()
        self._add_value_column_df()
        self._add_is_null_column_df()
        self._build_feature_etl_df()

    def _replace_strings_with_floats(self):
        """Replace specific string values with float equivalent"""
        
        self.col_etl = self.col_etl.str.replace('1, 1','1.0')
        self.col_etl = self.col_etl.str.replace('1, 2','1.0')
        self.col_etl = self.col_etl.str.replace('2, 1','2.0')
        self.col_etl = self.col_etl.str.replace('2, 3','2.0')