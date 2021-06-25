from src.preprocessing.ModelInputPreprocessor import ModelInputPreprocessor
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np


class ModelInputDimReduc(ModelInputPreprocessor):
    def __init__(self, dataset, target_var='', cont_num_columns=[], discrete_num_columns=[], nominal_cat_columns=[], 
                        verbose_columns=[], verbose_threshold=[], verbose_most_common=[], pca_columns=[], pca_expl_var=.95, operation='model'):
        """Instantiate Model Input Table."""
        super().__init__(dataset, target_var, cont_num_columns, discrete_num_columns,
                         nominal_cat_columns, verbose_columns, verbose_threshold, verbose_most_common, pca_columns, pca_expl_var, operation)

    def _pca_transform(self):
        print('Performing PCA on Select Features')
        """PCA Transfrom Columns."""

        for key,value in self.pca_columns.items():
            if key in self.cont_num_columns+self.discrete_num_columns+self.nominal_cat_columns+self.verbose_columns:
                # Return DF filtered on orig columns
                orig_columns = [x for x in self.df_X_train.columns if key+'_' in x and '_is_null' not in x]
                orig_columns_train = self.df_X_train[orig_columns].dropna()
                orig_columns_valid = self.df_X_valid[orig_columns].dropna()
                orig_columns_test = self.df_X_test[orig_columns].dropna()

                # PCA Fit-Transform
                value = self.pca_columns[key]
                pca = PCA(n_components=value)
                pca.fit(orig_columns_train)
                new_columns_train = pd.DataFrame(pca.transform(orig_columns_train))
                new_columns_valid = pd.DataFrame(pca.transform(orig_columns_valid))
                new_columns_test = pd.DataFrame(pca.transform(orig_columns_test))

                # Drop original pre-PCA columns
                self.df_X_train = self.df_X_train.drop(orig_columns,axis=1)
                self.df_X_valid = self.df_X_valid.drop(orig_columns,axis=1)
                self.df_X_test = self.df_X_test.drop(orig_columns,axis=1)

                # Drop original pre-PCA columns
                new_columns_train.columns = [key + '_pca_' + str(col) for col in new_columns_train.columns]
                new_columns_valid.columns = [key + '_pca_' + str(col) for col in new_columns_valid.columns]
                new_columns_test.columns = [key + '_pca_' + str(col) for col in new_columns_test.columns]

                # Re-assign indexes
                new_columns_train.index = self.df_X_train.index
                new_columns_valid.index = self.df_X_valid.index
                new_columns_test.index = self.df_X_test.index

                # Combine PCA df with train,valid,test dfs
                self.df_X_train = pd.concat([self.df_X_train,new_columns_train],axis=1)
                self.df_X_valid = pd.concat([self.df_X_valid,new_columns_valid],axis=1)
                self.df_X_test = pd.concat([self.df_X_test,new_columns_test],axis=1)        