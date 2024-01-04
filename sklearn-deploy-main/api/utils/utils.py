
# Function to remove outliers using IQR method
def remove_outliers_iqr(data, col):
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    initial_rows = data.shape[0]
    data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
    removed_rows = initial_rows - data.shape[0]
    print(f"Removed {removed_rows} rows from '{col}' column.")
    return data
