from src.eda_utils import salary_per_category_table
import pandas as pd


class BaselineModel:
    def __init__(self, category_vars, numeric_vars = None, id_var = 'jobId', target = 'salary'):
        
        self.fitted_category_salaries = None
        self.id_var = id_var
        self.target = target
        self.numeric_vars = numeric_vars
        
        self.category_vars = BaselineModel._check_variable_arguments(category_vars)
        self.variables_for_fitting = self.category_vars.copy()  # copy to avoid reference
        # If numeric_vars is given, check the values passed, and initialize dictionary to store fitted values
        if numeric_vars:
            self.numeric_vars =  BaselineModel._check_variable_arguments(numeric_vars)
            # Store the fitted values for the numeric columns in a dictionary where the key is
            # the column name and the value is a series of fitted values - initialized to None before fitting.
            self.fitted_numeric_salaries = {column:None for column in self.numeric_vars}
            self.variables_for_fitting.extend(numeric_vars)
    
    
    def fit(self, data):
        
        # Check types
        if not isinstance(data, pd.DataFrame):
            raise TypeError("The data must be a pandas dataframe")
        
        # Check that the specified variables are in the data
        self._ensure_variables_in_data(data.columns)
        
        # Calculate category averages and store fitted averages
        category_averages = salary_per_category_table(self.category_vars, data, target = self.target)
        self.fitted_category_salaries = category_averages.set_index(self.category_vars)
        
        # If numeric variables are given, get grouped averages and subtract overall salary mean
        if self.numeric_vars:
            # Calculate the overall average salary
            self.avg_salary_overall = data[self.target].mean()
    
            for column in self.fitted_numeric_salaries.keys():
                # Calculate the grouped average salary and subtract the overall average salary from it
                fitted_values = data.groupby(column)[self.target].mean() - self.avg_salary_overall
                self.fitted_numeric_salaries[column] = fitted_values
        
    
    def predict(self, data, return_only_preds = False):
        
        # Check that the model is fitted
        if not isinstance(self.fitted_category_salaries, pd.DataFrame):
            return print("There are no fitted values, make a call to BaselineModel().fit() before predicting.")
        
        if not isinstance(data, pd.DataFrame):
            raise TypeError('The data must be in a pandas dataframe')
        
        # Check that the grouping variables that were used for fitting are in the columns of the table
        self._ensure_variables_in_data(data.columns)
        
        # Predict 
        predictions = data.join(self.fitted_category_salaries, on = self.category_vars, rsuffix = "_preds")

        # Add numeric predictions
        if self.numeric_vars:
            # For each of the numeric columns, join the predicted salaries using the values of the column as the key
            for column in self.fitted_numeric_salaries.keys():
                column_suffix = f"_{column}_diff"
                predictions = predictions.join(self.fitted_numeric_salaries[column], on = column, rsuffix = column_suffix)
        
        if return_only_preds:
            predictions =  predictions.loc[:, [self.id_var, self.target + "_preds"]]
        
        return predictions
        
    
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
        