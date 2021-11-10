import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
from siuba import _, group_by, summarize, mutate, ungroup

from warnings import filterwarnings

# Ignore a warning that comes up in the '_large_error_axes_plot'
# I think it has something to do with the setting of the x tick labels
# There seems to be no negative effects to the plot by not addressing the warning.
filterwarnings('ignore', message = '^.*FixedFormatter')

def add_hue_labels(data):
    """utility function: adds categorical labels for plotting"""
    output = "no change"
    
    if data > 0:
        output = "increase salary"
    elif data < 0:
        output = "decrease salary"
    
    return output


def visualize_numeric_fit(data: pd.Series, plt_figsize = (10,8), save_img_path = None):
    """Plots the numeric fitted salaries created by BaselineModel()"""
    hues_and_styles = ['decrease salary', 'no change','increase salary']
    
    # Rounding and using integers makes the plot easier to read
    plot_df = pd.DataFrame(data.astype(int)) 
    
    # Pull out the variable names for plotting and calculations
    variable_name = data.index.name
    diff_col_name = data.name
   
    # Add labels for scatterplot hue, take absolute value of the diff column for scatterplot size
    plot_df['prediction_impact'] = plot_df.loc[:, diff_col_name].apply(add_hue_labels)
    plot_df['prediction_impact_amount'] = abs(plot_df.loc[:, diff_col_name])
    plot_df.reset_index(inplace=True)
   
    plt.figure(figsize = plt_figsize)
    g = sns.scatterplot(
        x = variable_name,
        y = diff_col_name,
        hue = "prediction_impact",
        hue_order = hues_and_styles,
        style = "prediction_impact",
        style_order = hues_and_styles,
        data = plot_df,
        markers = ['v', '.', '^'],
        palette = ['red', 'black','green'],
        size = "prediction_impact_amount",
        sizes = (50, 300)
    )
    # add triangle markers to legend (workaround)
    handles, labels = g.get_legend_handles_labels()

    new_handles = []
    new_labels = []

    for h, l in zip(handles, labels):
        # ugly workaround
        if l.isdigit():
            new_h = h.legend_elements(prop = 'sizes')[0][0]
            new_h.set_marker('^')
            new_handles.append(new_h)


        else:
            new_handles.append(h)
    
        new_labels.append(l)

    plt.legend(new_handles, new_labels)

    plt.ylabel("Impact to predicted categorical salary")
    plt.title(f"Prediction impact behavior - {variable_name}")

    if save_img_path:
        plt.savefig(save_img_path, bbox_inches = 'tight')
    plt.show()


def get_residuals(data: pd.DataFrame, add_to_df = False) -> pd.DataFrame:
    """Given a dataframe of baseline predictions, return a dataframe with residual columns added
    
    Must set return_all_cols=True when predicting with BaselineModel().predict
    """
    # required columns for this to work
    required_cols = ['jobId', 'salary', 'salary_preds', 'category_preds_tmp']
    # If there are any required columns missing, raise error
    if [i for i in required_cols if i not in data.columns]:
        raise ValueError(f'Prediction columns seem to be missing. Be sure to set "return_all_cols" when predicting from BaselineModel()')
        
    # Calculate error for final predictions as well as for the categorical averages
    data['final_residuals'] = data.salary - data.salary_preds
    data['category_residuals'] = data.salary - data.category_preds_tmp
    
    # Use the absolute value to compare the magnitude of residual values
    data['final_error_higher'] = data.final_residuals.abs() > data.category_residuals.abs()
    
    if not add_to_df:
        data = data.loc[:, required_cols + ['final_residuals', 'category_residuals', 'final_error_higher']]
    
    return data


def describe_residuals(resids: pd.DataFrame):
    """Prints out and reports summary statistics on the residuals.
    
    Meant to work with the output of 'get_residuals()' function
    """
    print("Residual info")
    print("-"*20)
    
    print("Summary Stats:")
    print(resids.final_residuals.describe(), end = '\n\n')
    
    # Setup, figure, grid, and axes objects
    fig, ax = plt.subplots(2,2, figsize=(10, 7), gridspec_kw = {'height_ratios': [2,3]})
    grid_shape = (2,2)
    resid_v_fitted = plt.subplot2grid(grid_shape, (0,0))
    scale_location = plt.subplot2grid(grid_shape, (0,1))
    resid_distn = plt.subplot2grid(grid_shape, (1,0), colspan = 2)
    
    # Residuals vs fitted
    sns.scatterplot(x = 'salary_preds', y = 'final_residuals', data = resids, alpha = 0.2, color = 'grey', ax = resid_v_fitted)
    resid_v_fitted.axhline(resids.final_residuals.mean(), color = 'blue')
    resid_v_fitted.set_xlabel('Fitted Values')
    resid_v_fitted.set_ylabel('Residuals')
    resid_v_fitted.set_title('Residuals vs fitted')
    
    # Scale-Location
    # standardize residuals
    std_resids = (resids.final_residuals - resids.final_residuals.mean()) / resids.final_residuals.std()
    std_resids = np.sqrt(std_resids.abs())
    # fit loess curve
    delta = 0.00005 * len(resids) # For computational efficiency, with lowess, on large data 
    loess = lowess(std_resids, resids.salary_preds, it = 0, delta = delta, return_sorted = False)
    # plot
    sns.scatterplot(x = resids.salary_preds, y = std_resids, alpha = 0.2, color = 'grey', ax = scale_location)
    sns.lineplot(x = resids.salary_preds, y = loess, ci = None, color = "blue", ax = scale_location)
    
    scale_location.set_ylabel('$\sqrt{|Standardized Residuals|}$')
    scale_location.set_xlabel('Fitted Values')
    scale_location.set_title('Scale-Location')
    
    # Residual distribution
    sns.histplot(x = 'final_residuals', data = resids, ax = resid_distn, color = 'grey')
    resid_distn.set_title('Distribution')
    resid_distn.set_ylabel('')
    resid_distn.set_xlabel('Residuals')
    
    plt.tight_layout()
    plt.show()
    
def plot_large_error_percentage(data, threshold):
    """
    calculate overall high error percentage based on 2 std devations from the mean 
        abs(resid_mean - resid) > 2 * resid.std()
        
    gather long form data of the columns, filter to only large errors and their percentages
    
    setup facet grid and pass in axes plotting function
    """
    resid_mean = data.final_residuals.mean()
    
    # Calculate distance from average and apply a threshold to indicate large errors
    data['high_error'] = (resid_mean - data.final_residuals).abs() > threshold
    
    # Percentage of large errors in the overall data set
    overall_large_error_percent = data.high_error.mean()
    
    # long form plotting data
    # Use siuba library to help with R/dplyr style aggregations
    data_melted = (data
     .loc[:, ['jobType', 'industry', 'degree', 'major', 'milesFromMetropolis', 'yearsExperience', 'high_error']]
     .melt(id_vars = 'high_error', var_name = 'column')
     >> group_by('column', 'value', 'high_error')
     >> summarize(total = _.value_counts())
     >> group_by('column', 'value')
     >> mutate(percent = _.total / _.total.sum())
     >> ungroup()
    )
    
    # Filter for only large error percentages and apply a grouped sort to prepare for plotting
    data_melted = (data_melted
                   .loc[data_melted.high_error, :]
                   .groupby('column')
                   .apply(lambda x: x.sort_values('percent', ascending = False))
                   .reset_index(drop = True)
                  )
    
    plot_title = f"Percentage of large errors per category\nLarge error threshold = {round(threshold, 1)}"
    plotGrid = sns.FacetGrid(data_melted, col = 'column', sharey = False, col_wrap=3, height = 4, aspect = 1.2)
    plotGrid.map(_large_error_axes_plot, 'percent', 'value', error_threshold = overall_large_error_percent)
    plotGrid.set_xlabels('Percentage of large errors')
    plotGrid.set_ylabels('')
    plotGrid.add_legend(loc = 'upper center', bbox_to_anchor = (0.5, 0), fancybox = True, frameon = True)
    plt.suptitle(plot_title, y = 1.05)
    plt.show()


def _large_error_axes_plot(percent, value, error_threshold = None, **kwargs):
    """helper function to be used within sns.FacetGrid"""
    above_overall_percent = None
    # Create a series that indicates if a particular value has higher percentage of large errors than the overall average
    if error_threshold:
        above_overall_percent = percent.apply(lambda x: "Above overall percent" if x > error_threshold else "Below overall percent")
    
    bar_plt = sns.barplot(x = percent, y = value, hue = above_overall_percent, orient = 'h',
                          palette=['grey', 'red'], dodge = False, hue_order=["Below overall percent", "Above overall percent"], **kwargs)
    plt.axvline(x = error_threshold, color = 'black', linestyle = '--', label = f'{round(error_threshold * 100, 1)}% (Overall large error rate)')
    # Round percentages for x-axis
    bar_plt.set_xticklabels([f"{round(i * 100, 1)}" for i in bar_plt.get_xticks()])
    
    # Reduce the number y-labels for 'milesFromMetropolis' for readability
    if len(value) > 50:
        bar_plt.set_yticklabels([str(i) if i % 5 == 0 else "" for i in bar_plt.get_yticks()])