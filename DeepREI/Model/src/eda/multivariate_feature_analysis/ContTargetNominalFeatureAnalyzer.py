import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker
import statsmodels.api as sm
from statsmodels.formula.api import ols


class ContTargetNominalFeatureAnalyzer():
    def __init__(self, dataset, target_col_name='', suffix='', feature_col_names=[]):
        '''Continuous vs Categorical Feature Analysis: Statistics and Visualizations'''
        # Inputs
        self.dataset = dataset
        self.suffix = suffix
        self.feature_col_names = feature_col_names
        self.target_col_name = target_col_name

    def run_eda(self):
        '''Run EDA'''
        self._filter_non_num_target()
        self._cont_target_vs_nominal_features()

    def _filter_non_num_target(self):
        '''Filter out all non-numeric target values'''
        self.dataset[self.target_col_name] = pd.to_numeric(self.dataset[self.target_col_name],errors='coerce')
        self.dataset = self.dataset[self.dataset[self.target_col_name] > 0]

    def _cont_target_vs_nominal_features(self):
        '''Visualize Discrete Univariate Statistics'''

        # Loop through each column name
        for feature in self.feature_col_names:
            plt.figure(figsize=(15, 5))

            # Frequency Plot ###
            plt.subplot(1, 2, 1)
            feature += self.suffix
            ax = sns.countplot(
                x=feature, data=self.dataset)
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
            ncount = len(self.dataset)
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

            ### TargetVar Box Plot Split on cats ###
            plt.subplot(1, 2, 2)
            sns.boxplot(data=self.dataset, x=feature, y=self.target_col_name)
            plt.title(f"{feature}")

            plt.show()

            ### ANOVA 1-Way Analysis ###
            mod = ols(f'lastsoldprice ~ {feature}', data=self.dataset[[
                self.target_col_name, feature]]).fit()
            aov_table = sm.stats.anova_lm(mod, typ=2)
            display(aov_table)
            print('''
            ''')
