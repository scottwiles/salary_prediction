import seaborn as sns
import matplotlib.pyplot as plt


def salary_per_category_table(category, df, target = 'salary'):
    """Aggregate the salaries dataframe grouped by the specified category and calculate the mean salary"""
    
    aggregated_table = df.groupby(category).salary.mean().to_frame().reset_index()
    aggregated_table.sort_values(by = target, inplace = True, ignore_index = True)
    
    return aggregated_table


def salary_per_category_plot(category, df, target = 'salary', order = None, hue_order = None):
    """Plot the average salary per the specified category, does not handle creating or showing figures (plt.figure/ plt.show)"""
    
    if isinstance(category, list) and len(category) > 2:
        return print("Category must be either a 'str', or a 'list' type of length 2")
    
    category_is_str = isinstance(category, str)
    
    plot_title = category if category_is_str else ' and '.join(category)  # Accomodate the plots with subgroups
    plot_x = category if category_is_str else category[0]
    plot_hue = None if category_is_str else category[1]
    
    sns.barplot(x = plot_x, y = target, hue = plot_hue, data = df, order = order, hue_order = hue_order)
    plt.title('Avg salary per ' + plot_title)
    plt.xticks(rotation = 45)