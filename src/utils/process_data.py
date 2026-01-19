import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def load_data(file_path):
    """Load data from a CSV file into a pandas DataFrame."""

    return pd.read_csv(file_path)

def clean_data(df):
    """Perform basic data cleaning on the DataFrame."""
  
    #add column with just the year
    df['Year'] = pd.to_datetime(df['Date & Time']).dt.year
    df["Month"] = pd.to_datetime(df['Date & Time']).dt.month
    df["Day"] = pd.to_datetime(df['Date & Time']).dt.day
    #add day of calendar year
    df["DayOfYear"] = pd.to_datetime(df['Date & Time']).dt.dayofyear
    location = df["Location"][0]
    unique_years = df['Year'].unique()
    max_flow_val = df['Flow (cfs)'].max()
    annual_average = pd.DataFrame()
    annual_average['Year'] = unique_years
    annual_average['mean_flow'] = annual_average['Year'].apply(
        lambda year: df[df['Year'] == year]['Flow (cfs)'].mean()
    )
    max_flow = pd.DataFrame()
    max_flow['Year'] = unique_years
    max_flow['max_flow'] = max_flow['Year'].apply(
        lambda year: df[df['Year'] == year]['Flow (cfs)'].max()
    )

    return df, unique_years, location, max_flow_val, annual_average, max_flow


def generate_yearly_flow_plot(cleaned_data, unique_years, location, max_flow_val):
    # Plotting yearly flow data
    plt.figure(figsize=(12, 6))

    for year in unique_years:
        if len(unique_years) > 20:
            if year % 2 == 0:
                #plot flow data in the Flow (cfs) column as individual lines for each year
                yearly_data = cleaned_data[cleaned_data['Year'] == year]
                plt.plot(yearly_data["DayOfYear"], yearly_data['Flow (cfs)'], label=str(year))
                #label the x axis with the months
                plt.xticks(ticks=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335], 
                        labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        else:
            #plot flow data in the Flow (cfs) column as individual lines for each year
            yearly_data = cleaned_data[cleaned_data['Year'] == year]
            plt.plot(yearly_data["DayOfYear"], yearly_data['Flow (cfs)'], label=str(year))
            #label the x axis with the months
            plt.xticks(ticks=[1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335], 
                    labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.xlabel('Month')
    plt.ylabel('Flow (cfs)')
    plt.ylim(-5, max_flow_val + max_flow_val*0.25)
    plt.title(f'Yearly Flow Data for Site: {location}')
    #make legend outside of plot
    plt.legend(ncol=8)
    plt.grid()
    plt.show()


def generate_box_whisker_plot(cleaned_data, location):
    """Generate box and whisker plot for monthly flow data."""
    cleaned_data['Month'] = pd.to_datetime(cleaned_data['Date & Time']).dt.month
    monthly_data = [cleaned_data[cleaned_data['Month'] == month]['Flow (cfs)'] for month in range(1, 13)]
    plt.figure(figsize=(10, 6))
    plt.boxplot(monthly_data, labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.xlabel('Month')
    plt.ylabel('Flow (cfs)')
    plt.title(f'Monthly Flow Distribution for Site: {location}')
    plt.grid(True)
    plt.show()

def linear_regression_analysis(annual_average):
    """Perform linear regression analysis on annual average flow data."""
    annual_average = annual_average.dropna()
    slope, intercept, r_value, p_value, std_err = stats.linregress(annual_average['Year'], annual_average['mean_flow'])
    regression_line = intercept + slope * annual_average['Year']
    annual_average['regression_line'] = regression_line
    return annual_average
def linear_regression_analysis_max(max_flow):
    """Perform linear regression analysis on annual average flow data."""
    max_flow = max_flow.dropna()
    slope, intercept, r_value, p_value, std_err = stats.linregress(max_flow['Year'], max_flow['max_flow'])
    regression_line = intercept + slope * max_flow['Year']
    max_flow['regression_line'] = regression_line
    return max_flow
