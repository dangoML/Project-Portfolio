import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


class ContinuousUnivariateAnalyzer():
    def __init__(self, dataset, feature_col_name='', suffix="", bins=100, x_axis_limit=None):
        '''Continuous Numeric Univariate Feature Analysis: Statistics and Visualizations'''
        # Inputs
        self.dataset = dataset[feature_col_name + suffix]
        self.feature_col_name = feature_col_name + suffix
        self.bins = bins
        self.x_axis_limit = x_axis_limit

        # Outputs
        self.data_min = 0
        self.data_max = 0
        self.five_num_sum = pd.DataFrame()

    def run_eda(self):
        '''Run EDA'''
        self._continuous_univariate_statistics()
        self._continuous_univariate_visualizations()

    def _continuous_univariate_statistics(self):
        '''Visualize Discrete Univariate Statistics'''
        # Calculate Max and Min
        self.data_min = self.dataset.min()
        self.data_max = self.dataset.max()

        # Set X-Axis Limit
        if self.x_axis_limit is None:
            self.x_axis_limit = self.data_max

        # Calculate a 5-Number summary for each Continuous Varaible
        self.five_num_sum = pd.DataFrame(
            columns=['Feature', 'Min', 'Q1', 'Median', 'Q3', 'Max'])

        # Calculate Quartiles
        quartiles = np.percentile(self.dataset, [25, 50, 75])
        self.five_num_sum = self.five_num_sum.append(pd.DataFrame(data=[[self.feature_col_name, self.data_min, quartiles[0], quartiles[1], quartiles[2], self.data_max]],
                                                                  columns=['Feature', 'Min', 'Q1', 'Median', 'Q3', 'Max']))

        # Return results
        display(self.five_num_sum)

    def _continuous_univariate_visualizations(self):
        """Continuous Univariate Visualizations"""

        plt.figure(figsize=(20, 5))

        # Histogram
        plt.subplot(1, 3, 1)
        sns.histplot(self.dataset, bins=self.bins)
        plt.xlim([1, self.x_axis_limit])

        # Boxplot
        plt.subplot(1, 3, 2)
        sns.boxplot(self.dataset)
        plt.xlim([1, self.x_axis_limit])
