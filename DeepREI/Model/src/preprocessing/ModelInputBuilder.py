from src.preprocessing.ModelInputDimReduc import ModelInputDimReduc

import pandas as pd


class ModelInputBuilder(ModelInputDimReduc):
    def __init__(self, dataset, target_var='', cont_num_columns=[], discrete_num_columns=[], nominal_cat_columns=[],
                 verbose_columns=[], verbose_threshold=[], verbose_most_common=[], pca_columns=[], pca_expl_var=.95, operation='model'):
        """Instantiate Model Input Table."""
        super().__init__(dataset, target_var, cont_num_columns, discrete_num_columns,
                         nominal_cat_columns, verbose_columns, verbose_threshold, verbose_most_common, pca_columns, pca_expl_var, operation)

    def build_model_input(self):
        """Build Model Input Table."""
        self._drop_nan_rows()
        self._etl_dataset()
        self._feature_limit_filters()
        self._train_valid_test_split()
        
        if self.operation == 'model':
            self._scale_train_valid_test()
            self._pca_transform()
