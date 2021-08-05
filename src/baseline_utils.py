import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def add_hue_labels(data):
    """utility function: adds categorical labels for plotting"""
    output = "no change"
    
    if data > 0:
        output = "increase salary"
    elif data < 0:
        output = "decrease salary"
    
    return output


def visualize_numeric_fit(data: pd.Series, plt_figsize = (10,8)):
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
    sns.scatterplot(
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
    plt.ylabel("Impact to predicted categorical salary")
    plt.title(f"Prediction impact behavior - {variable_name}")
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
        
    data['final_residuals'] = data.salary - data.salary_preds
    data['category_residuals'] = data.salary - data.category_preds_tmp
    
    # Use the absolute value to compare the magnitude of residual values
    data['final_error_higher'] = data.final_residuals.abs() > data.category_residuals.abs()
    
    if not add_to_df:
        data = data.loc[:, required_cols + ['final_residuals', 'category_residuals', 'final_error_higher']]
    
    return data