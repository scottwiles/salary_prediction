import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def salary_per_category_table(category, df, target = 'salary'):
    """Aggregate the salaries dataframe grouped by the specified category and calculate the mean salary"""
    
    aggregated_table = df.groupby(category).salary.mean().to_frame().reset_index()
    aggregated_table.sort_values(by = target, inplace = True, ignore_index = True)
    
    return aggregated_table


def salary_per_category_plot(category, df, target = 'salary', order = None, hue_order = None, **kwargs):
    """Plot the average salary per the specified category, does not handle creating or showing figures (plt.figure/ plt.show)"""
    
    if isinstance(category, list) and len(category) > 2:
        raise TypeError("Category must be either a 'str', or a 'list' of length 2")
    
    category_is_str = isinstance(category, str)
    
    plot_title = category if category_is_str else ' and '.join(category)  # Accomodate the plots with subgroups
    plot_x = category if category_is_str else category[0]
    plot_hue = None if category_is_str else category[1]
    
    sns.barplot(x = plot_x, y = target, hue = plot_hue, data = df, order = order, hue_order = hue_order, **kwargs)
    plt.title('Avg salary per ' + plot_title)
    plt.xticks(rotation = 45)
    
    
def faceted_histogram_plot(data, grid_col, grid_kwargs = {}, plot_kwargs = {}, target = 'salary'):
    
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The data should be a pandas dataframe.")
    
    plotGrid = sns.FacetGrid(data, col = grid_col, **grid_kwargs)
    plotGrid.map(_faceted_IQR_histogram_figure, target, **plot_kwargs)
    plt.legend(bbox_to_anchor = (1,1))
    plt.show()
    
    
def _faceted_IQR_histogram_figure(x, plot_stats = None, y_text_scale = 0.20, x_text_coord = 170, **kwargs):
    """This plotting function is for internal use within the 'faceted_histogram_plot' function and gets fed into the FacetGrid().map() method"""
    
    if not 0 <= y_text_scale <= 1:
        raise ValueError("The 'y_text_scale' argument should be between 0 and 1.")
    
    sns.histplot(x, **kwargs)
    # add text to display the sample mean and standard deviation corresponding to each facet in the grid
    _, y_scale_top = plt.ylim()
    y_scale_top -= y_scale_top * y_text_scale  # Scale down the placement of the y-coordinate of text so that it is slightly lower than the limit of the y-axis
    subset_mean = int(x.mean())
    subset_std = int(x.std())
    plt.text(x = x_text_coord, y = y_scale_top, s = f"Avg: {subset_mean}\nStd: {subset_std}")
    
    if plot_stats:
        if not isinstance(plot_stats, PlotStats):
            raise TypeError("The 'plot_stats' argument must be an instance of the 'PlotStats' class")
            
        plot_stats.plot_IQR(x_axis = True)
    
    
class PlotStats:
    def __init__(self, df, target_col):
        
        if not isinstance(df, pd.DataFrame):
            raise TypeError("The input data should be a pandas dataframe")
        
        if not target_col in df.columns:
            raise ValueError("Target column not found in the data frame")
        
        target = df[target_col]
        
        self.mean = target.mean()
        self.median = target.median()
        self.lower_quartile = target.quantile(0.25)
        self.upper_quartile = target.quantile(0.75)
        
    def plot_IQR(self, x_axis = False):
        """Add IQR range to plot based on y-axis variable, does not handle creating or showing figures (plt.figure/ plt.show)"""
        
        plot_labels = {
            'median': 'Overall median',
            'lower_qt': 'Overall 25%',
            'upper_qt': 'Overall 75%',
            'IQR': 'Overall IQR'
        }
        
        # If 'x_axis' is False draw horizontal lines and spans, otherwise draw vertical ones
        if not x_axis:

            plt.axhline(y = self.median, linestyle = ":", label = plot_labels['median'], zorder = 0, alpha = 0.5)
            plt.axhline(y = self.lower_quartile, label = plot_labels['lower_qt'], linestyle = "--", zorder = 0, alpha = 0.5)
            plt.axhline(y = self.upper_quartile, label = plot_labels['upper_qt'], linestyle = "-.", zorder = 0, alpha = 0.5)
            plt.axhspan(ymin = self.lower_quartile, ymax = self.upper_quartile, color = 'grey', label = plot_labels['IQR'], zorder = 0, alpha = 0.15)
            plt.legend(bbox_to_anchor = (1,1))
            
        else:
 
            plt.axvline(x = self.median, linestyle = ":", label = plot_labels['median'], zorder = 0, alpha = 0.5)
            plt.axvline(x = self.lower_quartile, label = plot_labels['lower_qt'], linestyle = "--", zorder = 0, alpha = 0.5)
            plt.axvline(x = self.upper_quartile, label = plot_labels['upper_qt'], linestyle = "-.", zorder = 0, alpha = 0.5)
            plt.axvspan(xmin = self.lower_quartile, xmax = self.upper_quartile, color = 'grey', label = plot_labels['IQR'], zorder = 0, alpha = 0.15)
            plt.legend(bbox_to_anchor = (1,1))