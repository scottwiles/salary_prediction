import pandas as pd
import numpy as np

from IPython.display import display
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_validate

class EvaluateModel:
    def __init__(self, test_models: list, constant_model, test_type, scoring):
        
        """
        Base class used to test components of an ML pipeline. Should not be used directly. Instead refer to
        the subclasses 'EvaluatePreprocessors' and 'EvaluateEstimators'
        
        Parameters
        ----------
        
        test_models: A list of (name, model) tuples to be evaluated.
        constant_model: Either a preprocessing Pipeline object, or an estimator; depending on which subclass is instantiated
        test_type: argument is provided directly by the subclass which runs this __init__ method
        scoring: Used within modeling functions. Must be a valid sklearn scoring parameter
        
        """
        
        # Initialize variables to control tests
        self.test_type = test_type
        self.test_models = test_models
        self.constant_model = constant_model
        self.scoring = scoring
        
        # temp variables to be filled in during evaluation process
        self.test_results = None
        self.best_model = None
        self.best_score = None
        
    def make_model_pipe(self, model_part):
        """
        Parameters
        ----------
        model_part: (name, model) tuple that is an iterable item from the test_models list
        
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
        
        # Iterate over each item in the test_models array, compute scores and save results
        for model_test in self.test_models:

            # TODO: We can easily modify this to make the class be able to test whole pipelines as well (i.e. testing lin reg vs rf vs SGDRegressor)
            # check self.test_type, if it is 'pipeline' model can just be assigned by the variable model_test
            # Make the model object for testing
            model = self.make_model_pipe(model_test)
            
            # Compute cross validation scores
            cv_values = cross_validate(model, X, y = y, scoring = self.scoring, cv = 5, return_train_score = True)
            
            # Append results to dataframe list - cv_values is a dictionary of arrays
            # so this dictionary comprehension computes the mean of each array and saves a new dictionary
            scores = {name:np.mean(value) for name, value in cv_values.items()}
            
            cv_results.append(scores)
            cv_index.append(model_test[0])
            
            # Check for best score and save if best score found
            if not self.best_score:
                self.best_score = scores['test_score']
                self.best_model = model
            elif scores['test_score'] > self.best_score:
                self.best_score = scores['test_score']
                self.best_model = model
            
            if verbose:
                EvaluateModel.print_progress(model_name = model_test[0], metrics = scores) 
            
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
        
        return
    
    @staticmethod
    def print_progress(model_name, metrics):
        # print progress after each model test
        print('-'*30)
        print(f"Finished training: {model_name}")
        print(f"Test score  : {metrics['test_score']}")
        print(f"Train score : {metrics['train_score']}", end = '\n\n')
    
    
class EvaluatePreprocessors(EvaluateModel):
    def __init__(self, preprocessors: list, estimator, scoring):
        """Creates an object to test multiple preprocessing pipelines with an estimator.
        
        Wrapper for EvaluateModel this class feeds the approriate arguments to the __init__ method.
        """
        super().__init__(test_models = preprocessors, constant_model = estimator, test_type = 'preprocessing', scoring = scoring)


class EvaluateEstimators(EvaluateModel):
    def __init__(self, estimators: list, preprocessing, scoring):
        """Creates an object to test multiple estimators with a given preprocessing pipeline
        
        Wrapper for EvaluateModel this class feeds the approriate arguments to the __init__ method.
        """
        super().__init__(test_models = estimators, constant_model = preprocessing, test_type = 'estimator', scoring = scoring)
