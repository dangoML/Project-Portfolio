import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker


class ContTargetContFeatureAnalyzer():
    def __init__(self, dataset, target_col_name='', suffix='', feature_col_names=[]):
        '''Continuous Numeric Univariate Feature Analysis: Statistics and Visualizations'''
        # Inputs
        self.dataset = dataset
        self.suffix = suffix
        self.feature_col_names = feature_col_names
        self.target_col_name = target_col_name

    def run_eda(self):
        '''Run EDA'''
        self._cont_target_vs_cont_features()

    def _cont_target_vs_cont_features(self):
        '''Cont TargetVar vs Cont Feature: Visuals and Statistics'''
        # Create list of Feature Names + Suffix
        num_columns_value = [x+self.suffix for x in self.feature_col_names]

        # Plot Target vs all Features
        g = sns.pairplot(self.dataset[[self.target_col_name]+num_columns_value],
                    y_vars=self.target_col_name,
                    x_vars=num_columns_value)
        g.fig.suptitle(
            f"{self.target_col_name} vs Continuous Features", y=1.08)

        # get correlation matrix
        num_columns_data = self.dataset[[
            self.target_col_name]+num_columns_value]
        num_columns_data = num_columns_data.corr().abs()

        # draw the heatmap using seaborn.
        plt.figure(figsize=(10, 6))
        sns.heatmap(num_columns_data, square=True, annot=True, linewidths=.5)
        plt.title("correlation matrix (Title)")
        plt.show()
