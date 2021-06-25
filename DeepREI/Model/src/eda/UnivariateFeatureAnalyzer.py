from src.eda.univariate_feature_analysis.ContinuousUnivariateAnalyzer import ContinuousUnivariateAnalyzer
from src.eda.univariate_feature_analysis.DiscreteUnivariateAnalyzer import DiscreteUnivariateAnalyzer


class UnivariateFeatureAnalyzer():
    def __init__(self, dataset=None, target_col_name='', feature_type=None, suffix="", feature_col_name='',
                 bins=100, x_axis_limit=None, feature_col_names=[]):
        """Univariate Visualizations and Statistics for Continuous/Categorical Features."""

        # Inputs
        self.dataset = dataset
        self.feature_type = feature_type.lower()
        self.feature_col_name = feature_col_name
        self.feature_col_names = feature_col_names
        self.suffix = suffix
        self.bins = bins
        self.x_axis_limit = x_axis_limit
        self.target_col_name = target_col_name

        # Run EDA
        if self.feature_type == 'continuous':
            continuous = ContinuousUnivariateAnalyzer(dataset=self.dataset, feature_col_name=self.feature_col_name,
                                                      suffix=self.suffix, bins=self.bins, x_axis_limit=self.x_axis_limit)
            continuous.run_eda()

        if self.feature_type == 'discrete':
            discrete = DiscreteUnivariateAnalyzer(dataset=self.dataset, target_col_name=self.target_col_name,
                                                  suffix=self.suffix, feature_col_names=self.feature_col_names)
            discrete.run_eda()
