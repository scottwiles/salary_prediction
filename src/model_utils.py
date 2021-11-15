import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from statsmodels.nonparametric.smoothers_lowess import lowess

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


def plot_residuals(true: str, preds: str, resids: pd.DataFrame, save_path = None):
    """plots residuals from a model. 

    Makes 3 plots: resids vs fitted, scale-location, and histogram of residuals

    Parameters:
    -----------
    true : name of the column that holds the true values
    preds : name of the column that holds the predicted values
    resids : dataframe which contains predicted and true values
    """
    resids = resids.copy()

    # Setup, figure, grid, and axes objects
    fig, ax = plt.subplots(2,2, figsize=(10, 7), gridspec_kw = {'height_ratios': [2,3]})
    grid_shape = (2,2)
    resid_v_fitted = plt.subplot2grid(grid_shape, (0,0))
    scale_location = plt.subplot2grid(grid_shape, (0,1))
    resid_distn = plt.subplot2grid(grid_shape, (1,0), colspan = 2)
    

    # Residuals vs fitted
    resids['residuals'] = resids[true] - resids[preds]
    sns.scatterplot(x = preds, y = 'residuals', data = resids, alpha = 0.2, color = 'grey', ax = resid_v_fitted)
    resid_v_fitted.axhline(resids['residuals'].mean(), color = 'blue')
    resid_v_fitted.set_xlabel('Fitted Values')
    resid_v_fitted.set_ylabel('Residuals')
    resid_v_fitted.set_title('Residuals vs fitted')
    
    # Scale-Location
    # standardize residuals
    std_resids = (resids.residuals - resids.residuals.mean()) / resids.residuals.std()
    std_resids = np.sqrt(std_resids.abs())
    # fit loess curve
    delta = 0.00005 * len(resids) # For computational efficiency, with lowess, on large data 
    loess = lowess(std_resids, resids[preds], it = 0, delta = delta, return_sorted = False)
    # plot
    sns.scatterplot(x = resids[preds], y = std_resids, alpha = 0.2, color = 'grey', ax = scale_location)
    sns.lineplot(x = resids[preds], y = loess, ci = None, color = "blue", ax = scale_location)
    
    scale_location.set_ylabel('$\sqrt{|Standardized Residuals|}$')
    scale_location.set_xlabel('Fitted Values')
    scale_location.set_title('Scale-Location')
    
    # Residual distribution
    sns.histplot(x = 'residuals', data = resids, ax = resid_distn, color = 'grey')
    resid_distn.set_title('Distribution')
    resid_distn.set_ylabel('')
    resid_distn.set_xlabel('Residuals')
    
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches = 'tight')

    plt.show()