import pandas as pd


class FeatureETLEngineering:
    def __init__(self, col_series):
        """Instantiate new feature class.

        'col' must be a pandas Series object.
        """
        # ETL Inputs
        self.col_series = col_series
        self.col_etl = col_series.copy()
        
        try:
            self.name = self.col_etl.name
        except:
            pass

        # ETL Outputs
        self.df_etl = pd.DataFrame()
        self.df_value = pd.DataFrame()
        self.df_null = pd.DataFrame()

    def _replace_nans(self, values_to_replace=["None"]):
        """Replace specified values with None values."""
        for value in values_to_replace:
            self.col_etl.loc[self.col_etl == value] = None

    def _add_value_column_df(self):
        """Create an _value column."""
        # Grab indexes of null columns
        null_indexes = pd.isna(self.col_etl)

        # Create 'value' column variant name
        value_key = "_".join([self.name, "value"])

        # Create Binary 'value' and 'null' column variants in DataFrame
        self.df_value[value_key] = self.col_etl.fillna(0)

    def _add_is_null_column_df(self):
        """Create an is_null column."""

        # Check if instance is DF or Series and handle appropriately
        if isinstance(self.col_etl, pd.DataFrame):
            for column in self.col_etl.columns:
                # Grab indexes of null values
                null_indexes = pd.isna(self.col_etl[column])

                # Create 'null' column variant names
                null_key = "_".join([column, "is_null"])

                # Create Binary 'null' column variants in DataFrame
                self.df_null[null_key] = self.col_etl[column].fillna(1)
                self.df_null[null_key].loc[~null_indexes] = 0

        else:
            # Grab indexes of null values
            null_indexes = pd.isna(self.col_etl)

            # Create 'null' column variant names
            null_key = "_".join([self.name, "is_null"])

            # Create Binary 'null' column variants in DataFrame
            self.df_null[null_key] = self.col_etl.fillna(1)
            self.df_null[null_key].loc[~null_indexes] = 0

    def _one_hot_encode_df(self):
        """One Hot Encode and add new columns to df_etl"""
        # One-Hot-Encode all Categorical Columns
        temp_dummies_df = pd.get_dummies(
            self.col_etl, prefix=f'{self.col_etl.name}_', drop_first=True)

        # Concat One-Hot Columns to df
        self.df_etl = pd.concat([self.df_etl, temp_dummies_df], axis=1)
    
    def _build_feature_etl_df(self):
        """Combine all dfs into one and cast as float"""
        self.df_etl = pd.concat(
            [self.df_etl, self.df_null, self.df_value], axis=1)
        self.df_etl = self.df_etl.astype(float)