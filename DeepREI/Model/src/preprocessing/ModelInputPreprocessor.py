from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.preprocessing.ModelInputETL import ModelInputETL
import pandas as pd
import numpy as np


class ModelInputPreprocessor(ModelInputETL):
    def __init__(self, dataset, target_var='', cont_num_columns=[], discrete_num_columns=[], nominal_cat_columns=[], 
                        verbose_columns=[], verbose_threshold=[], verbose_most_common=[], pca_columns=[], pca_expl_var=.95, operation='model'):
        """Instantiate Model Input Table."""
        super().__init__(dataset, target_var, cont_num_columns, discrete_num_columns,
                         nominal_cat_columns, verbose_columns, verbose_threshold, verbose_most_common, pca_columns, pca_expl_var, operation)

        # Outputs
        self.df_X_train = pd.DataFrame()
        self.df_y_train = pd.DataFrame()
        self.df_X_valid = pd.DataFrame()
        self.df_y_valid = pd.DataFrame()
        self.df_X_test = pd.DataFrame()
        self.df_y_test = pd.DataFrame()

    def _drop_nan_rows(self):
        print('Dropping Nan Rows')
        """Drop rows that have atleast 3 non-nan values."""
        # Target Value must be greater than zero
        self.dataset = self.dataset.replace(to_replace='None', value=np.nan).dropna(thresh=3)

    def _feature_limit_filters(self):
        print('Applying Feature Limit Filters')
        """Filter for all property values greater than zero."""
        # Target Value must be greater than zero
        self.df_model = self.df_model[self.df_model[self.target_var] > 0]

        # Garagespaces must be less 20
        self.df_model = self.df_model[self.df_model['garagespaces_value'] < 20]

    def _train_valid_test_split(self):
        print('Performing Train, Valid, Test Split')
        """Split dataset into training, validation, test"""

        # Specify X and y
        self.df_model = self.df_model.sample(frac = 1)
        y = self.df_model[self.target_var]
        X = self.df_model.drop(self.target_var, axis=1)

        # Re-Order X columns
        cont_value_columns = [x for x in self.df_model.columns if '_value' in x]
        rest_of_columns = set(X.columns).difference(set(cont_value_columns))
        rest_of_columns = sorted(list(rest_of_columns))
        X = X[cont_value_columns+rest_of_columns]

        # Clear df_model memory
        del self.df_model

        # Create Test Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2)

        # Clear X and y from memory
        del X, y

        # Create Train and Validation Split
        X_train, X_valid, y_train, y_valid = train_test_split(
            X_train, y_train, test_size=0.25)  # 0.25 x 0.8 = 0.2

        # Assign splits to respective tuple objects
        self.df_X_train, self.df_y_train = X_train, y_train
        self.df_X_valid, self.df_y_valid = X_valid, y_valid
        self.df_X_test, self.df_y_test = X_test, y_test

    def _scale_train_valid_test(self):
        print('Scaling Data')
        """Scale all Ind. Variable (Features)"""
        scaler = StandardScaler()
        index = len(self.cont_num_columns+self.discrete_num_columns)
        columns = self.df_X_train.iloc[:,:index].columns

        scaled_features = self.df_X_train.copy()
        features = scaled_features[columns]
        scaler = StandardScaler().fit(features.values)
        features = scaler.transform(features.values)
        scaled_features[columns] = features
        self.df_X_train = scaled_features.copy()

        scaled_features = self.df_X_valid.copy()
        features = scaled_features[columns]
        features = scaler.transform(features.values)
        scaled_features[columns] = features
        self.df_X_valid = scaled_features.copy()

        scaled_features = self.df_X_test.copy()
        features = scaled_features[columns]
        features = scaler.transform(features.values)
        scaled_features[columns] = features
        self.df_X_test = scaled_features.copy()

        del scaled_features, features