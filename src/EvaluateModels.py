import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from IPython.display import display
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate, GridSearchCV

class EvaluateModels:
    def __init__(self, test_models: list, constant_model, test_type, scoring, tuning_parameters = {}):
        """
        Base class used to test components of an ML pipeline. Should not be used directly. Instead refer to
        the subclasses 'EvaluatePreprocessors', 'EvaluateEstimators', 'EvaluatePipelines'
        
        Parameters
        ----------
        
        test_models: A list of (name, model) tuples to be evaluated.
        constant_model: Either a preprocessing Pipeline object, or an estimator; depending on which subclass is instantiated
        scoring: Used within modeling functions. Must be a valid sklearn scoring parameter
        test_type: {'estimator', 'preprocessing', 'pipeline'}. Provided by the particular subclass that gets instantiated. This argument shouldn't get used manually.
        """
        
        # Initialize variables to control tests
        self.test_type = test_type
        self.test_models = test_models
        self.constant_model = constant_model
        self.scoring = scoring
        self.tuning_parameters = tuning_parameters
        
        # variables to be filled in during evaluation process
        self.test_results = None
        self.best_model = None
        self.best_score = None
        
    def make_model_pipe(self, model_part):
        """
        Parameters
        ----------
        model_part: (name, model) tuple that is an iterable item from the self.test_models list
        
        """
        # If the test_type is 'preprocessing', then the model_part is a preprocessing pipeline
        # If the test_type is 'estimator', then the model_part is an sklearn estimator with predict methods
        if self.test_type == 'preprocessing':
            # Add preprocessing pipeline to the constant model
            mdl_pipeline = Pipeline([
                model_part,
                ('estimator', self.constant_model)
            ])
            
        elif self.test_type == 'estimator':
            # Add the estimator to the preprocessing pipeline
            mdl_pipeline = Pipeline([
                ('preprocessing', self.constant_model),
                model_part
            ])
            
        return mdl_pipeline
    
    def run(self, X, y, verbose = False):
        """
        Evaluate each model in the test_models attribute, compute cross validated scores and save resutls to a table
        
        parameters
        -----------
        X: The feature matrix of a dataset to be used in cross validation
        y: Target vector corresponding to the feature matrix X
        verbose: Boolean; print the progress and scores during evaluation
        """
        
        cv_results = []
        cv_index = []
        
        # Iterate over each model in the test_models array, compute scores and save results
        for model_test in self.test_models:

            # When running a pipeline test, the model_test variable is a full pipeline and doesn't need to get built
            # and is extracted from the 2nd element of model_test
            if self.test_type == 'pipeline':
                model = model_test[1]
            else:
                # Make the model object for testing
                model = self.make_model_pipe(model_test)

            # Check if tuning parameters have been given
            if model_test[0] in self.tuning_parameters.keys():
                # Tune parameters and return model with the best params
                model = self.tune_parameters(model, X, y, name = model_test[0]) 
            
            # Compute cross validation scores
            cv_values = cross_validate(model, X, y = y, scoring = self.scoring, cv = 5, return_train_score = True)
            
            # Append results to dataframe list - cv_values is a dictionary of arrays
            # so this dictionary comprehension computes the mean of each array and saves a new dictionary
            scores = {name:np.mean(value) for name, value in cv_values.items()}
            
            cv_results.append(scores)
            cv_index.append(model_test[0])
            
            # Check for best score and save if best score found
            # currently assumes bigger scores are better 
            # (works with sklearn since squared error is negated)
            if not self.best_score:
                self.best_score = scores['test_score']
                self.best_model = model
            elif scores['test_score'] > self.best_score:
                self.best_score = scores['test_score']
                self.best_model = model
            
            if verbose:
                EvaluateModels.print_progress(model_name = model_test[0], metrics = scores) 
            
        # Make output dataframe sorted by test score in descending order
        self.test_results = (
            pd.DataFrame(data = cv_results, index = cv_index)
            .sort_values('test_score', ascending = False)
            .reindex(columns = ['test_score', 'train_score', 'fit_time', 'score_time'])
        )
        
        # print end results
        print('::'*30)
        print("Best model found:")
        print(self.best_model, end = '\n\n')
        print(f"Model score (using '{self.scoring}')")
        print(self.best_score, end = '\n\n')
        display(self.test_results)

    def tune_parameters(self, model, X, y, name):
        """Perform hyperparameter tuning and return the model after setting params to the best found.
        
        Parameters
        ----------

        model : (name, model) tuple, an item from the self.test_models list.
        X : training feature dataset
        y : target vector of labels
        """
        print(f'Parameter grid found for {name} - performing grid search')
        # run grid search
        grid_search = GridSearchCV(model,
                                   param_grid = self.tuning_parameters[name],
                                   scoring = self.scoring, refit = False, cv = 5)

        grid_search.fit(X, y)

        print(f"Best parameters found for {name}")
        print(grid_search.best_params_)

        # Set the parameters of the model
        model.set_params(**grid_search.best_params_)

        return model

    @staticmethod
    def print_progress(model_name, metrics):
        # print progress after each model test
        print('-'*30)
        print(f"Finished training: {model_name}")
        print(f"Test score  : {metrics['test_score']}")
        print(f"Train score : {metrics['train_score']}", end = '\n\n')

    def plot_results(self, best_score = None):
        """Plot the results of an evaluation test"""
        
        # check to see if all the scores are negative (using a negative scoring metric in sklearn)
        # if so, change it to the absolute value
        if all(self.test_results.test_score.lt(0)):
            scores = self.test_results.test_score.abs()
        else:
            scores = self.test_results.test_score
        
        sns.barplot(x = scores, y = self.test_results.index, orient = 'h', color = 'lightblue')
        
        if best_score:
            plt.axvline(x = best_score, linestyle = '--', color = 'black', label = f'Best score: {round(best_score, 2)}')
            plt.legend(bbox_to_anchor = (1,1))
    
    
class EvaluatePreprocessors(EvaluateModels):
    def __init__(self, preprocessors: list, estimator, scoring, **kwargs):
        """Wrapper class that feeds the approriate arguments to the __init__ method of EvaluateModels.

        Creates an object to test multiple preprocessing pipelines with an estimator. Not used for hyperparameter tuning. You can use this
        to test, for example, multiple types of categorical encodings for the same model.
        
        """
        super().__init__(test_models = preprocessors, constant_model = estimator, test_type = 'preprocessing', scoring = scoring, **kwargs)


class EvaluateEstimators(EvaluateModels):
    def __init__(self, estimators: list, preprocessing, scoring, **kwargs):
        """Wrapper class that feeds the approriate arguments to the __init__ method of EvaluateModels.

        Creates an object to test multiple estimators with a given preprocessing pipeline. Not used for hyperparameter tuning. You can use this
        to test, for example, linear and tree based estimators with the same preprocessing steps.
        
        """
        super().__init__(test_models = estimators, constant_model = preprocessing, test_type = 'estimator', scoring = scoring, **kwargs)


class EvaluatePipelines(EvaluateModels):
    def __init__(self, pipelines: list, scoring, **kwargs):
        """Wrapper class that feeds the approriate arguments to the __init__ method of EvaluateModels.

        Creates an object to test multiple model pipelines. Not used for hyperperameter tuning. You can use this to test full model pipelines
        against each other to find the best performing one
        
        """
        super().__init__(test_models = pipelines, constant_model = None, test_type = 'pipeline', scoring = scoring, **kwargs)
