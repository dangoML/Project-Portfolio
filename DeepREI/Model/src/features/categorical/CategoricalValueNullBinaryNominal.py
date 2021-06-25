from src.features.FeatureETLEngineering import FeatureETLEngineering
import pandas as pd


class CategoricalValueNullBinaryNominal(FeatureETLEngineering):
    def __init__(self, col_series):
        """Instantiate categorical feature."""
        super().__init__(col_series)

    def run_etl(self):
        """Run ETL of the column."""
        self._replace_nans()
        self._add_is_null_column_df()
        self._one_hot_encode_df()
        self._build_feature_etl_df()
