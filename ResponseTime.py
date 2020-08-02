# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Required columns 
col_list=['Call Date','Received DtTm','On Scene DtTm','Battalion']

# Load only necessary columns in dataframe
fire_dept_data=pd.read_csv('Fire_Department_Calls_for_Service.csv',usecols=col_list)

# Convert Call date column to datetime type
fire_dept_data['Call Date']=pd.to_datetime(fire_dept_data['Call Date'])

# Create Year_Month column
fire_dept_data['Year_Month'] = fire_dept_data['Call Date'].apply(lambda x: x.strftime('%Y-%m'))  

# sort the dataframe, change the index to Call date, and filter only 12 months record,
# remove row if atleast one NaN value is present  
fire_dept_data_12Month = fire_dept_data.sort_values(by="Call Date",ascending=True) \
                                    .set_index("Call Date")\
                                    .last("12M")\
                                    .dropna()

# Create Response Time seconds column  
fire_dept_data_12Month.insert(0,"Response Time seconds",\
   (pd.to_datetime(fire_dept_data_12Month['On Scene DtTm'])-pd.to_datetime(fire_dept_data_12Month['Received DtTm']))\
   .dt.total_seconds())
   
# Drop unnecessary columns and the index 
fire_dept_data_12Month=fire_dept_data_12Month.drop(['Received DtTm','On Scene DtTm'],axis=1)
fire_dept_data_12Month=fire_dept_data_12Month.reset_index(drop=True)

# Percentile Function
def Percentile90(x):
    return x.quantile(0.9)

# groupby,collect the percentile information, and save to csv file 
fire_dept_data_12Month.groupby(['Year_Month','Battalion'])\
                      .agg({'Response Time seconds': Percentile90})\
                      .rename(columns={'Response Time seconds':'90th percentile Response Time'})\
                      .to_csv('ResponseTime_Percentile90.csv')

# VISUALIZATION
# Read data from prepared table 
fire_dept_data_12Month_visualize=pd.read_csv('ResponseTime_Percentile90.csv')

# Create unique combination of Year_Month 
Year_Month_Combo=fire_dept_data_12Month_visualize.Year_Month.unique()

# Loop through every Unique Year_Month combination, create new dataframe for respective combination and generate
# Scatter plots indicating monthly 90th percentile response times by "Battalion" 
for x in Year_Month_Combo:
    fire_dep_data_month=fire_dept_data_12Month_visualize[fire_dept_data_12Month_visualize['Year_Month']==x]
    plt.scatter(fire_dep_data_month['Battalion'], fire_dep_data_month['90th percentile Response Time'])
    plt.title(x)
    plt.xlabel("Battalian")
    plt.ylabel("90th Percentile-Response time seconds")
    plt.show()
