from src.eda.multivariate_feature_analysis.ContTargetContFeatureAnalyzer import ContTargetContFeatureAnalyzer
from src.eda.multivariate_feature_analysis.ContTargetDiscreteFeatureAnalyzer import ContTargetDiscreteFeatureAnalyzer
from src.eda.multivariate_feature_analysis.ContTargetNominalFeatureAnalyzer import ContTargetNominalFeatureAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt


class MultivariateFeatureAnalyzer():
    def __init__(self, dataset=None, targetvar_type='', feature_type='', target_col_name='',
                 feature_col_names=[], suffix=""):
        """Bivariate Statistics and Visualizations for Continuous/Categorical Features."""

        # Inputs
        self.targetvar_type = targetvar_type
        self.feature_type = feature_type
        self.dataset = dataset
        self.target_col_name = target_col_name
        self.feature_col_names = feature_col_names
        self.suffix = suffix

        # Run EDA
        if self.targetvar_type == 'continuous' and feature_type == 'continuous':
            eda = ContTargetContFeatureAnalyzer(dataset=self.dataset, target_col_name=self.target_col_name,
                                                suffix=self.suffix, feature_col_names=self.feature_col_names)
            eda.run_eda()

            # Run EDA
        if self.targetvar_type == 'continuous' and feature_type == 'discrete':
            eda = ContTargetDiscreteFeatureAnalyzer(dataset=self.dataset, target_col_name=self.target_col_name,
                                                    suffix=self.suffix, feature_col_names=self.feature_col_names)
            eda.run_eda()

            # Run EDA
        if self.targetvar_type == 'continuous' and feature_type == 'nominal':
            eda = ContTargetNominalFeatureAnalyzer(dataset=self.dataset, target_col_name=self.target_col_name,
                                                   suffix=self.suffix, feature_col_names=self.feature_col_names)
            eda.run_eda()
