from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler

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

