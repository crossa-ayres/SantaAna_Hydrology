import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os
from utils.process_data import load_data, clean_data, linear_regression_analysis, linear_regression_analysis_max, generate_yearly_flow_plot, generate_box_whisker_plot
import seaborn as sns

paths = [r'C:\Users\smitha\github\SantaAna_Hydrology\Data\rio_above.csv']
current_dir=os.getcwd()
print(current_dir)
folders_dir=os.path.join(current_dir,"Images")
if not os.path.exists(folders_dir):
    os.makedirs(folders_dir)


for path in paths:
    data = load_data(path)
    cleaned_data, unique_years, location, max_flow_val, annual_average, max_flow = clean_data(data)

    generate_box_whisker_plot(cleaned_data, location)

    annual_average = linear_regression_analysis(annual_average)
    max_flow = linear_regression_analysis_max(max_flow)

    plt.plot(annual_average['Year'], annual_average['mean_flow'], marker='o')
    plt.plot(annual_average['Year'], annual_average['regression_line'], color='red', linestyle='--')
    plt.title(f'Annual Average Flow with Linear Regression for Site: {location}')
    plt.xlabel('Year')
    plt.ylabel('Mean Flow (cfs)')
    plt.legend(['Mean Flow', 'Linear Regression'])
    #add text box showing the slope of the regression line
    slope = (annual_average['regression_line'].iloc[-1] - annual_average['regression_line'].iloc[0]) / (annual_average['Year'].iloc[-1] - annual_average['Year'].iloc[0])
    plt.text(0.85, 0.95, f'Slope: {slope:.2f} cfs/year', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    plt.grid(True)
    plt.show()
    
    plt.plot(max_flow['Year'], max_flow['max_flow'], marker='o')
    plt.plot(max_flow['Year'], max_flow['regression_line'], color='red', linestyle='--')
    plt.title(f'Annual Maximum Flow with Linear Regression for Site: {location}')
    plt.xlabel('Year')
    plt.ylabel('Max Flow (cfs)')
    plt.legend(['Max Flow', 'Linear Regression'])
    #add text box showing the slope of the regression line
    slope = (max_flow['regression_line'].iloc[-1] - max_flow['regression_line'].iloc[0]) / (max_flow['Year'].iloc[-1] - max_flow['Year'].iloc[0])
    plt.text(0.85, 0.95, f'Slope: {slope:.2f} cfs/year', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    plt.grid(True)
    plt.show()

    generate_yearly_flow_plot(cleaned_data, unique_years, location, max_flow_val)
