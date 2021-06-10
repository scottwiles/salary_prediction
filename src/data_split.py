import warnings

warnings.filterwarnings('ignore', message = "^.*sharex")  # ignore seaborn's catplot warning about using 'sharex = False' and 'color = None'

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def test_split(data, test_size, random_state = None):
    X = data.drop(columns = 'salary')
    y = data['salary']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = random_state)
    _report_split(X_train, 'train')
    _report_split(X_test, 'test')


def visualize_split(data, sharex = False, sharey = False):
    
    # Drop these columns from the visualization as they won't be needed
    _droppable_columns = ['jobId', 'companyId', 'salary']
    
    cols_to_drop = [i for i in _droppable_columns if i in data.columns]
    
    if cols_to_drop:
        data = data.drop(columns = cols_to_drop)
        
    data_melted = pd.melt(data)
    
    sns.catplot(x = 'value', col = 'variable', data = data_melted, kind = 'count', sharex = sharex, sharey = sharey, col_wrap = 3)
    plt.show()
    
    
def _report_split(data, split):
    
    if not split in ['test', 'train']:
        raise ValueError("The 'split' argument must be one of 'test' or 'train'")
    
    split_end = "TEST" if split == "test" else "TRAIN"
    
    print("-"*30)
    print(f"{split_end} DATA shape: {data.shape}")
    print(f"{split_end} DATA distributions")
    visualize_split(data)
    
    print(f"{split_end} DATA: Value counts for 'major' column:")
    print(data.major.value_counts())