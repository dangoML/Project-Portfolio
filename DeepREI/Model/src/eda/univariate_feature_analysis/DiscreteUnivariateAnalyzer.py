import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker


class DiscreteUnivariateAnalyzer():
    def __init__(self, dataset, target_col_name='', suffix='', feature_col_names=[]):
        '''Continuous Numeric Univariate Feature Analysis: Statistics and Visualizations'''
        # Inputs
        self.dataset = dataset
        self.suffix = suffix
        self.feature_col_names = feature_col_names
        self.target_col_name = target_col_name

    def run_eda(self):
        '''Run EDA'''
        self._discrete_univariate_statistics()

    def _discrete_univariate_statistics(self):
        '''Visualize Discrete Univariate Statistics'''
        plt.figure(figsize=(10, 5))

        # Loop through each column name
        for feature in self.feature_col_names:

            plt.figure(figsize=(20, 5))

            ### Frequency Plot ###
            plt.subplot(1, 2, 1)
            feature += self.suffix
            ax = sns.countplot(
                x=feature, data=self.dataset[self.dataset[feature] > 0])
            plt.title(f"{feature}")
            plt.xlabel(feature)
            plt.ylabel('Count')

            # Make twin axis
            ax2 = ax.twinx()

            # Switch so count axis is on right, frequency on left
            ax2.yaxis.tick_left()
            ax.yaxis.tick_right()

            # Also switch the labels over
            ax.yaxis.set_label_position('right')
            ax2.yaxis.set_label_position('left')
            ax2.set_ylabel('Frequency [%]')

            # Add Frequency values to Plot
            ncount = len(self.dataset[self.dataset[feature] > 0])
            for p in ax.patches:
                x = p.get_bbox().get_points()[:, 0]
                y = p.get_bbox().get_points()[1, 1]
                ax.annotate('{:.1f}%'.format(100.*y/ncount), (x.mean(), y),
                            ha='center', va='bottom')  # set the alignment of the text

            # Use a LinearLocator to ensure the correct number of ticks
            ax.yaxis.set_major_locator(ticker.LinearLocator(10))

            # Fix the frequency range to 0-100
            ax2.set_ylim(0, 100)
            ax.set_ylim(0, ncount)

            # And use a MultipleLocator to ensure a tick spacing of 10
            ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))

            # ### TargetVar Box Plot Split on cats ###
            # plt.subplot(1, 2, 2)
            # sns.boxplot(data=self.dataset, x=feature, y=self.target_col_name)
            # plt.title(f"{feature}")
            plt.show()
