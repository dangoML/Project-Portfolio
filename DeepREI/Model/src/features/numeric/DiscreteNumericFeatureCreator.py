from src.features.numeric.NumericValueNull import NumericValueNull
from src.features.numeric.numeric_custom_features.NumericValueNull_levelsorstories import NumericValueNull_levelsorstories
# from src.features.numeric.numeric_custom_features.NumericValueNull_longlat import NumericValueNull_longlat
# from src.features.numeric.numeric_custom_features.NumericValueNull_longlatxyz import NumericValueNull_longlatxyz

import pandas as pd

class DiscreteNumericFeatureCreator():
    def __init__(self, dataset, discrete_num_columns=[]):
        """Create Numeric Features."""
        # Inputs
        self.dataset = dataset
        self.num_columns = discrete_num_columns

        # Outputs
        self.df_etl = pd.DataFrame()
        self.numeric_custom_columns = []
        self.remaining_numeric_columns = []

    def run_feature_etl(self):
        self._create_custom_numeric_features()
        self._remaining_numeric_columns()
        self._create_numeric_features()

    def _remaining_numeric_columns(self):
        '''Create list of all columns that didn't have a custom handler'''
        self.remaining_numeric_columns = set(self.num_columns).difference(
            set(self.numeric_custom_columns))
    
    def _create_custom_numeric_features(self):
        """Create custom categorical nominal features and add to Model Input DF."""

        # levelsorstories Handler
        numeric = NumericValueNull_levelsorstories(
            self.dataset['levelsorstories'])
        numeric.run_etl()
        self.numeric_custom_columns += ['levelsorstories']
        self.df_etl = pd.concat(
                [self.df_etl, numeric.df_etl], axis=1)

    def _create_numeric_features(self):
        """ETL our Numeric Features."""
        # Loop through each column and create numeric feature
        if self.remaining_numeric_columns is not None:
            for column in self.remaining_numeric_columns:
                numeric = NumericValueNull(self.dataset[column])
                numeric.run_etl()
                self.df_etl = pd.concat([self.df_etl, numeric.df_etl], axis=1)