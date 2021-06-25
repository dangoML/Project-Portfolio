import pandas as pd
import numpy as np
from src.features.FeatureETLEngineering import FeatureETLEngineering


class NumericValueNull_longlat_xyz(FeatureETLEngineering):
    def __init__(self, col_series):
        """Instantiate categorical feature."""
        super().__init__(col_series)

    def run_etl(self):
        """Run ETL of the column."""
        self._add_is_null_column_df()
        self._LatLong_to_sphere_coor()
        self._build_feature_etl_df()

    def _LatLong_to_sphere_coor(self):
        """LatLong to 3-D Spherical Coordinates via Sin and Cos operations"""
        self.df_value['latlong_x_value'] = np.cos(self.col_etl['Latitude']) * np.cos(self.col_etl['Longitude'])
        self.df_value['latlong_y_value'] = np.cos(self.col_etl['Latitude']) * np.sin(self.col_etl['Longitude']) 
        self.df_value['latlong_z_value'] = np.sin(self.col_etl['Latitude'])