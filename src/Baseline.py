from src.eda_utils import salary_per_category_table
import pandas as pd
from sklearn.metrics import mean_squared_error


class BaselineModel:
    def __init__(self, category_vars, numeric_vars = None, id_var = 'jobId', target = 'salary'):
        
        self.fitted_category_salaries = None
        self.id_var = id_var
        self.target = target
        self.numeric_vars = numeric_vars
        
        self.category_vars = BaselineModel._check_variable_arguments(category_vars)
        self.variables_for_fitting = self.category_vars.copy()  # copy to avoid reference
        
        # If numeric_vars is given, check the values passed and initialize dictionary to store fitted values
        if numeric_vars:
            self.numeric_vars =  BaselineModel._check_variable_arguments(numeric_vars)
            # Store the fitted values for the numeric columns in a dictionary where the key is the column name 
            # and the value is a series of fitted values - initialized to None before fitting.
            self.fitted_numeric_salaries = {column:None for column in self.numeric_vars}
            self.variables_for_fitting.extend(numeric_vars)
    
    
    def fit(self, data):
        
        # Check types
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data must be a pandas dataframe")

        if not self.target in data.columns:
            raise ValueError("The specified target column is not found in the data, consider setting it manually with BaselineModel().target")
        
        # Check that the specified variables are in the data
        self._ensure_variables_in_data(data.columns)
        
        # Calculate category averages and store fitted averages
        category_averages = salary_per_category_table(self.category_vars, data, target = self.target)
        self.fitted_category_salaries = category_averages.set_index(self.category_vars).rename(columns = {self.target: self.target + "_preds"})
        
        # If numeric variables are given, get grouped averages and subtract overall salary mean
        if self.numeric_vars:
            # Calculate the overall average salary
            self.avg_salary_overall = data[self.target].mean()
    
            for column in self.fitted_numeric_salaries.keys():
                # Calculate the grouped average salary and subtract the overall average salary from it
                fitted_values = data.groupby(column)[self.target].mean() - self.avg_salary_overall
                self.fitted_numeric_salaries[column] = fitted_values.rename(f"{column}_diff")
        
    
    def predict(self, new_data, return_only_preds = False, return_all_cols = False, numeric_combo = "sum"):
        
        # Check that the model is fitted
        if not isinstance(self.fitted_category_salaries, pd.DataFrame):
            return print("There are no fitted values, make a call to BaselineModel().fit() before predicting.")
        
        if not isinstance(new_data, pd.DataFrame):
            raise TypeError('The data must be in a pandas dataframe')

        if not numeric_combo in ["sum", "mean"]:
            raise ValueError("The numeric_combo argument must be one of: sum, mean")
        
        # Check that the grouping variables used during fitting are in the columns of new data
        self._ensure_variables_in_data(new_data.columns)
        
        # Add categorical predictions by left joining the average categorical salaries 
        predictions = new_data.join(self.fitted_category_salaries, on = self.category_vars)

        # Add numeric predictions by left joining the average numeric salaries
        if self.numeric_vars:
            # For each of the numeric columns, join the predicted salaries using the values of the column as the key
            for column in self.fitted_numeric_salaries.keys():
                predictions = predictions.join(self.fitted_numeric_salaries[column], on = column)

            numeric_diff_cols = [col for col in predictions.columns if col.endswith("_diff")]
            predictions['sum_numeric_diff'] = predictions[numeric_diff_cols].sum(axis = 1)
            predictions['mean_numeric_diff'] = predictions[numeric_diff_cols].mean(axis = 1)

            predictions['preds_with_sum'] = predictions[self.target + "_preds"] + predictions['sum_numeric_diff']
            predictions['preds_with_mean'] = predictions[self.target + "_preds"] + predictions['mean_numeric_diff']

            if numeric_combo == "sum":
                predictions[self.target + "_preds"] = predictions['preds_with_sum']
            else:
                predictions[self.target + "_preds"] = predictions['preds_with_mean']
            
            # By default drop the intermediary columns that were added for the numeric predictions
            if not return_all_cols:
                cols_to_drop = [col for col in predictions.columns if col.endswith(("_diff", "mean", "sum"))]
                predictions = predictions.drop(columns = cols_to_drop)
        
        if return_only_preds:
            predictions =  predictions.loc[:, [self.id_var, self.target + "_preds"]]
        
        return predictions
        
    
    def evaluate_fit(self, data, numeric_combination = None):
        """This should test a set of parameters (i.e. combo of categorical and numeric variables) and return main metrics

        takes in the training data set, test data set
        fits the model to the training data
        gives MSE for training data and test data for mean and sum numeric combo (if applicable)

        """

        pass


    def _ensure_variables_in_data(self, new_columns):
        """Internal helper function to verify the presence of required columns.
        
        Take a set difference, on the columns in the prediction data, from the 'self.grouping_vars' variable.
        If there are any values present in 'self.category_vars' but not in the columns of the new data raise a ValueError.
        """
        
        # Set difference
        variable_difference = set(self.variables_for_fitting) - set(new_columns)
        
        # If there is a difference raise ValueError
        if variable_difference:
            missing_vars = ", ".join(variable_difference)
            column_s = "columns are" if len(variable_difference) > 1 else "column is"
            
            raise ValueError(f"The following required {column_s} not in the data: {missing_vars}")
            

    @staticmethod
    def _check_variable_arguments(variable_argument):
        """Utility function to check for valid argument formats for: grouping_vars, numeric_vars
        
        Check that the passed argument is either in the form of a list or a string. 
        If the argument is a string, return it as a list of one string, otherwise return the list of variables.

        Returns a list
        """
        
        is_str = isinstance(variable_argument, str)
        
        if not ( is_str or isinstance(variable_argument, list) ):
            raise TypeError("The 'grouping_vars' and 'numeric_vars' arguments must be either str or list type")
        
        # If the argument was passed as a string return it as a list length 1
        if is_str:
            variable_argument = [variable_argument]
        
        return variable_argument