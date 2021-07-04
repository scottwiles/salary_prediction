from sklearn.metrics import mean_squared_error
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.eda_utils import salary_per_category_table


class BaselineModel:
    def __init__(self, category_vars, numeric_vars = None, id_var = 'jobId', target = 'salary'):
        
        self.fitted_category_salaries = None
        self.id_var = id_var
        self.target = target
        self.numeric_vars = numeric_vars
        self.output_pred_col = self.target + "_preds"  # Column name of the predictions
        self.is_fitted = False
        
        self.category_vars = BaselineModel._check_variable_arguments(category_vars)
        self.variables_for_fitting = self.category_vars.copy()  # copy to avoid reference
        
        # If numeric_vars is given, check the values passed and initialize dictionary to store fitted values
        if numeric_vars:
            self.numeric_vars =  BaselineModel._check_variable_arguments(numeric_vars)
            # Store the fitted values for the numeric columns in a dictionary where the key is the column name 
            # and the value is a series of fitted values - initialized to None before fitting.
            self.fitted_numeric_salaries = {column:None for column in self.numeric_vars}
            self.variables_for_fitting.extend(self.numeric_vars)
    
    
    def fit(self, data: pd.DataFrame):
        
        # Check types
        BaselineModel._check_input_data_type(data)

        if not self.target in data.columns:
            raise ValueError("The specified target column is not found in the data, consider setting it manually with BaselineModel().target")
        
        # Check that the specified variables are in the data
        self._ensure_variables_in_data(data.columns)
        
        # Calculate category averages and store fitted averages
        category_averages = salary_per_category_table(self.category_vars, data, target = self.target)
        self.fitted_category_salaries = category_averages.set_index(self.category_vars).rename(columns = {self.target: self.output_pred_col})
        
        # If numeric variables are given, get grouped averages and subtract from overall salary mean
        if self.numeric_vars:
            # Calculate the overall average salary
            self.avg_salary_overall = data[self.target].mean()
    
            for column in self.fitted_numeric_salaries.keys():
                # Calculate the grouped average salary, and subtract the overall average salary from it
                fitted_values = data.groupby(column)[self.target].mean() - self.avg_salary_overall
                self.fitted_numeric_salaries[column] = fitted_values.rename(f"{column}_diff")
        
        self.is_fitted = True
        
    
    def predict(self, new_data: pd.DataFrame, return_only_preds = False, return_all_cols = False, numeric_combo = "sum"):
        
        # Check that the model is fitted
        if not self.is_fitted:
            return print("There are no fitted values, make a call to BaselineModel().fit() before predicting.")
        
        # Ensure data is pd.DataFrame
        BaselineModel._check_input_data_type(new_data)

        if not numeric_combo in ["sum", "mean"]:
            raise ValueError("The numeric_combo argument must be one of: 'sum', 'mean'")
        
        # Check that the grouping variables used during fitting are present in the new data
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

            predictions['preds_with_sum'] = predictions[self.output_pred_col] + predictions['sum_numeric_diff']
            predictions['preds_with_mean'] = predictions[self.output_pred_col] + predictions['mean_numeric_diff']
            predictions['category_preds_tmp'] = predictions[self.output_pred_col]

            if numeric_combo == "sum":
                predictions[self.output_pred_col] = predictions['preds_with_sum']
            else:
                predictions[self.output_pred_col] = predictions['preds_with_mean']
            
            # By default drop the intermediary columns that were added for the numeric predictions
            if not return_all_cols:
                cols_to_drop = [col for col in predictions.columns if col.endswith(("_diff", "mean", "sum", "_tmp"))]
                predictions = predictions.drop(columns = cols_to_drop)
        
        if return_only_preds:
            predictions = predictions.loc[:, [self.id_var, self.output_pred_col]]
        
        return predictions
        
    
    def evaluate(self, train_data, test_data, **predict_kwargs):
        """Evaluate test and training set error in terms of MSE.

        predict_kwargs are passed to the BaselineModel().predict() method
        """
        if not self.is_fitted:
            self.fit(train_data)
        
        # Training error 
        train_error = mean_squared_error(train_data[self.target], self.predict(train_data, **predict_kwargs)[self.output_pred_col])

        # Test error
        test_error = mean_squared_error(test_data[self.target], self.predict(test_data, **predict_kwargs)[self.output_pred_col])

        return {'training_error': train_error, 'test_error': test_error}


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
    def _check_input_data_type(data):
        if not isinstance(data, pd.DataFrame):
            raise TypeError('The data must be in a pandas dataframe')
            

    @staticmethod
    def _check_variable_arguments(variable_argument):
        """Utility function to check for valid argument formats for: grouping_vars, numeric_vars
        
        Check that the passed argument is either in the form of a list or a string. 
        If the argument is a string, return it as a list of one string, otherwise return the list of variables.

        Returns a list
        """
        is_str = isinstance(variable_argument, str)
        
        if not ( is_str or isinstance(variable_argument, list) ):
            raise TypeError("The 'grouping_vars' and 'numeric_vars' arguments must be either str or list")
        
        # If the argument was passed as a string return it as a list length 1
        if is_str:
            variable_argument = [variable_argument]
        
        return variable_argument


class TestModels():

    def __init__(self, train_data, test_data, category_combos, plot = True):
        self.best_model_score = 1e6
        self.best_model_params = {
            'category_vars': None,
            'numeric_vars': None,
            'numeric_combo': None
        }

        model_names = ['only_categorical', 'add_yearsExperience', 'add_milesFromMetropolis', 'add_both']
        numeric_combos = [None, 'yearsExperience', 'milesFromMetropolis', ['yearsExperience', 'milesFromMetropolis']]

        df_index = []
        df_data = []

        for categories in category_combos:
            df_row = {}
            df_index.append(", ".join(categories))
            
            models = {model_names[i]: BaselineModel(categories, numeric_combos[i]) for i in range(len(model_names))}
            
            for mdl in models:
                # For both numeric cols calculate mean and sum methods of combining the numeric predictors
                if mdl == 'add_both':
                    for combo in ['mean', 'sum']:
                        score = models[mdl].evaluate(train_data, test_data, numeric_combo = combo)['test_error']
                        df_row[f'{mdl}_{combo}'] = score
                        self.test_best_score(score, models[mdl], combo)
                else:
                    score = models[mdl].evaluate(train_data, test_data)['test_error']
                    df_row[mdl] = score
                    self.test_best_score(score, models[mdl])
            
            df_data.append(df_row)

        self.df_output = pd.DataFrame(df_data, index = df_index)

        # Print best score and params
        print(f"Best model score: {self.best_model_score}\n")
        print("Best model parameters:")
        print(self.best_model_params)
        print("\n\n")

        if plot:
            self.plot_outcome()
        
    def test_best_score(self, score, model: BaselineModel, numeric_combo = None):
        """Compare a new model score with the saved best score. If the new score is lower, then update the saved best score."""

        if score < self.best_model_score:
            self.best_model_score = score
            self.best_model_params = {
                'category_vars': model.category_vars,
                'numeric_vars': model.numeric_vars,
                'numeric_combo': numeric_combo
            }

    def plot_outcome(self):
        plt.figure(figsize=(7,7))
        ax = sns.heatmap(self.df_output, annot = True, fmt = '.0f', cmap = 'Reds', linewidths = 0.5)
        ax.set_xlabel('numeric variable combinations')
        ax.set_ylabel('categorical variable combinations')
        ax.tick_params('x', rotation = 45)
        plt.title("Mean squared error for each model")
        plt.show()