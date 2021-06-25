from src.features.targetvar.TargetVariableContinuous import TargetVariableContinuous

import pandas as pd


class TargetVariableCreator():
    def __init__(self, dataset, target_var):
        """Create Target Variable."""
        # Inputs
        self.dataset = dataset
        self.target_var = target_var

        # Outputs
        self.target_cont_column = self.dataset[self.target_var] # How Can I Pull in Dataset to here???
        self.df_etl = pd.DataFrame()

    def run_feature_etl(self):
        self._create_target_variable()

    def _create_target_variable(self):
        """ETL our Continuous Target Variable."""
        target = TargetVariableContinuous(self.target_cont_column)
        target.run_etl()
        self.df_etl = pd.concat(
                [self.df_etl, target.df_etl], axis=1)
