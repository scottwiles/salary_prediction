import matplotlib.pyplot as plt
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler

from sklearn.model_selection import validation_curve, learning_curve

# Add the residual plot from baseline_utils here

# Utility function for categorical encoding
def make_categorical_encoding(category_levels, ord_cols, oh_cols, scaling_cols = ['yearsExperience', 'milesFromMetropolis']) -> ColumnTransformer:
    """Utility function to help make many column transformers for testing categorical encoding
    
    Parameters
    ---------
    category_levels : (list or None) Ordinal levels for each categorical column (used in OrdinalEncoder)
    ord_cols : (list or None) The columns to perform ordinal encoding
    oh_cols : (list or None) The columns to perform one hot encoding
    scaling_cols : numeric columsn to feed into StandardScaler
    
    """
    # Appending each step to the list makes it so that ordinal and one hot encoding are optional
    # setting the arguments for either ordinal or one hot encoding to None will not include that 
    # encoder from the output column transformer
    transformer_steps = []
    
    if (category_levels and ord_cols):
        transformer_steps.append(('ordinal_encoding', OrdinalEncoder(categories = category_levels), ord_cols))
    
    if oh_cols:
        transformer_steps.append(('one_hot_encoding', OneHotEncoder(), oh_cols))
    
    transformer_steps.append(('std_scaler', StandardScaler(), scaling_cols))
    
    return ColumnTransformer(transformer_steps, remainder='passthrough')



# Plot learning curve, wrapper for the sklearn learning_curve() function that plots the results
def plot_learning_curve(model, X, y, scoring, fig_size = (8, 5), **kwargs) -> None:
    """Calculate learning curve metrics and plot results
    
    Parameters:
    -----------
    model : Estimator that is compatible with sklearn learning_curve()
    X : Feature matrix of training data
    y : Target vector of values
    scoring : Scoring metric to use, must be a valid sklearn scoring parameter
    fig_size : Output size of the plot
    kwargs : Extra keyword arguments are passed to the learning_curve() function
    """
    sizes, train_scores, test_scores = learning_curve(model, X, y, scoring = scoring, **kwargs)

    # If all the scores are negative (using negative scoring metric in sklearn)
    # use the absolute value instead 
    if all([i < 0 for i in train_scores[0]]):
        train_scores = np.abs(train_scores)
        test_scores = np.abs(test_scores)

    train_scores_mean = np.mean(train_scores, axis = 1)
    test_scores_mean = np.mean(test_scores, axis = 1)
    train_std = np.std(train_scores, axis = 1)
    test_std = np.std(test_scores, axis = 1)

    _, ax = plt.subplots(figsize = fig_size)

    ax.plot(sizes, train_scores_mean, 'o-b', label = 'Train')
    ax.plot(sizes, test_scores_mean, 'o-r', label = 'Test')
    ax.fill_between(sizes, train_scores_mean - train_std, train_scores_mean + train_std, alpha = 0.2, color = 'b')
    ax.fill_between(sizes, test_scores_mean - test_std, test_scores_mean + test_std, alpha = 0.2, color = 'r')

    ax.set_xlabel('Training set size')
    ax.set_ylabel(scoring)

    plt.title("Learning curve")
    plt.legend(loc = 'best')
    plt.show()


# Plot validation curve
def plot_validation_curve(model, X, y, param_name, param_range, scoring, fig_size = (8, 5), **kwargs) -> None:
    """Calculate validation curve metrics and plot output
    
    Parameters:
    -----------
    model : Estimator that is compatible with sklearn validation_curve()
    X : Feature matrix of training data
    y : Target vector of values
    scoring : Scoring metric to use, must be a valid sklearn scoring parameter
    fig_size : Output size of the plot
    kwargs : Extra keyword arguments are passed to the validation_curve() function
    """
    train_scores, test_scores = validation_curve(model, X, y, param_name = param_name, param_range = param_range, scoring = scoring, **kwargs)

    # If all the scores are negative (using negative scoring metric in sklearn)
    # use the absolute value instead 
    if all([i < 0 for i in train_scores[0]]):
        train_scores = np.abs(train_scores)
        test_scores = np.abs(test_scores)

    train_scores_mean = np.mean(train_scores, axis = 1)
    test_scores_mean = np.mean(test_scores, axis = 1)
    train_scores_std = np.std(train_scores, axis = 1)
    test_scores_std = np.std(test_scores, axis = 1)

    _, ax = plt.subplots(figsize = fig_size)

    ax.plot(param_range, train_scores_mean, 'o-b', label = 'Train')
    ax.plot(param_range, test_scores_mean, 'o-r', label = 'Test')
    ax.fill_between(param_range, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha = 0.2, color = 'b')
    ax.fill_between(param_range, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha = 0.2, color = 'r')

    ax.set_xlabel(param_name)
    ax.set_ylabel(scoring)

    plt.title('Validation curve')
    plt.legend(loc = 'best')
    plt.show()