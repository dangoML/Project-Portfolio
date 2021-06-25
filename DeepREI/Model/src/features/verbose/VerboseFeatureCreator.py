from src.features.verbose.VerboseValueNullBinary import VerboseValueNullBinary
import pandas as pd


class VerboseFeatureCreator():
    def __init__(self, dataset, verbose_columns=[], verbose_threshold=[], verbose_most_common=True):
        """Create Features from Raw Data."""
        # Inputs
        self.dataset = dataset
        self.verbose_columns = verbose_columns
        self.verbose_threshold = verbose_threshold
        self.verbose_most_common = verbose_most_common

        # Outputs
        self.df_etl = pd.DataFrame()

    def run_feature_etl(self):
        self._create_verbose_features()

    def _create_verbose_features(self):
        """ETL our Verbose Features."""
        # Loop through each column and create verbose feature
        for column in self.verbose_columns:
            verbose = VerboseValueNullBinary(self.dataset[column], verbose_threshold=self.verbose_threshold, verbose_most_common=self.verbose_most_common)
            verbose.run_etl()
            self.df_etl = pd.concat([self.df_etl, verbose.df_etl], axis=1)
