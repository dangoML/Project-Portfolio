from src.features.categorical.CategoricalValueNullBinaryNominal import CategoricalValueNullBinaryNominal
from src.features.categorical.nominal_custom_features.CategoricalValueNullBinaryNominal_area import CategoricalValueNullBinaryNominal_area
from src.features.categorical.nominal_custom_features.CategoricalValueNullBinaryNominal_zipcode import CategoricalValueNullBinaryNominal_zipcode
from src.features.categorical.nominal_custom_features.CategoricalValueNullBinaryNominal_zipcode_suffix import CategoricalValueNullBinaryNominal_zipcode_suffix
import pandas as pd


class CategoricalFeatureCreator():
    def __init__(self, dataset, nominal_cat_columns=[]):
        """Create Categorical Nominal Features."""
        # Inputs
        self.dataset = dataset
        self.nominal_cat_columns = nominal_cat_columns

        # Outputs
        self.cat_custom_nominals = []
        self.remaining_cat_columns = []
        self.df_etl = pd.DataFrame()

    def run_feature_etl(self):
        """ETL our Categorical Features."""
        self._create_custom_categorical_nominal_features()
        self._remaining_cat_columns()
        self._create_categorical_nominal_features()

    def _remaining_cat_columns(self):
        '''Create list of all columns that didn't have a custom handler'''
        self.remaining_cat_columns = set(self.nominal_cat_columns).difference(
            set(self.cat_custom_nominals))
    
    def _create_custom_categorical_nominal_features(self):
        """Create custom categorical nominal features and add to Model Input DF."""

        # Area Custom Handler
        categorical = CategoricalValueNullBinaryNominal_area(
            self.dataset['area'])
        categorical.run_etl()
        self.cat_custom_nominals += ['area']
        self.df_etl = pd.concat(
                [self.df_etl, categorical.df_etl], axis=1)

        # Zipcode Custom Handler
        categorical = CategoricalValueNullBinaryNominal_zipcode(
            self.dataset['propertyurl'])
        categorical.run_etl()
        self.cat_custom_nominals += ['zipcode']
        self.df_etl = pd.concat(
                [self.df_etl, categorical.df_etl], axis=1)

        # Zipcode Delivery Sector Custom Handler
        categorical = CategoricalValueNullBinaryNominal_zipcode_suffix(
            self.dataset['zipcode_suffix'])
        categorical.run_etl()
        self.cat_custom_nominals += ['zipcode_suffix']
        self.df_etl = pd.concat(
                [self.df_etl, categorical.df_etl], axis=1)

    def _create_categorical_nominal_features(self):
        """Create categorical nominal features and add to Model Input DF."""
        # Loop through each column and create categorical feature
        for column in self.remaining_cat_columns:
            categorical= CategoricalValueNullBinaryNominal(self.dataset[column])
            categorical.run_etl()
            self.df_etl = pd.concat(
                [self.df_etl, categorical.df_etl], axis=1)