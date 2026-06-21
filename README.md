Exploratory Data Analysis and Anomaly Detection of New York City Airbnb Listings 

Abstract 

The growth of short-term rental platforms such as Airbnb has generated large amounts of data that can be analyzed to understand pricing patterns, host characteristics, and neighborhood trends. However, real-world datasets often contain missing values, inconsistencies, duplicates, and extreme observations that can affect analytical results. 

The purpose of this study was to perform an exploratory analysis of the New York City Airbnb dataset using descriptive statistical methods and data visualization techniques. The study focused on data preprocessing procedures, including cleaning the price variable, handling missing values, removing duplicate records, and identifying anomalies. Descriptive statistics and visualizations were used to examine relationships among variables such as price, room type, neighborhood, property type, number of reviews and host characteristics. 

The findings provide insights into Airbnb pricing behavior while demonstrating the importance of data preprocessing and exploratory analytics when working with large real-world data sets. 

Data Description 
The dataset used in this study was the New York City Airbnb Listings Dataset obtained from the Inside Airbnb project. The dataset contains detailed information about Airbnb properties located throughout New York City. There were approximately 40,000 – 50,000 listings and more than 70 variables. The file format was CSV (.csv.gz) and the data type is structured tabular data. 

The variables that were examined included  
Listing information: name, property_type, room_type, and accommodates 
Pricing information: price 
Location information: latitude, longitude, neighbourhood_cleansed, host _neighbourhood 
Host information: host_is_superhost 
Review information: number_of_reviews 
Availability information: availability_365 
Methods Used (with reason for selection) 

Data Preprocessing 
Price Cleaning: The price variable was initially stored as text containing dollar signs and commas. These symbols were removed and the variable was converted into a numeric data type. The statistical calculations require numeric values. Converting the price variable allowed descriptive analysis and visualization. 

Missing Value Imputation: Missing values in the price variable were replaced with the median price. The distribution of Airbnb prices is highly skewed due to extremely expensive listings. The median is less sensitive to outliers than the mean and therefore provides a more representative measure of central tendency. 

Duplicate records: Duplicate records were identified using: df.duplicated().sum(), Duplicates were removed if they existed. Duplicate observations can distort statistical summaries and produce misleading results. 
Removal of Completely Missing Variables: Variables containing 100% missing values were removed. Columns with no information do not contribute to analysis and unnecessarily increase complexity. 

Descriptive Statistics 
The following descriptive statistics were calculated: 
Measures of Central Tendency: mean and median 
Measures of Variability: Minimum, Maximum, Range, Variance, and Standard Deviation. 
Descriptive statistics summarize large datasets and provide information regarding the center, spread, and variability of numerical variables. 

Grouped Analysis 
Average prices were calculated by: Neighborhood, room type, property type, and Superhost status. 
Grouping observations allows comparison across categories and helps identify factors associated with higher listing prices. 

Conclusion 
This study analyzed the New York City Airbnb Dataset using exploratory data analysis and descriptive statistical techniques. Data preprocessing procedures identify missing values, duplicate observations, and variables containing incomplete information. Cleaning procedures improved data quality and prepared the dataset for analysis. 

Descriptive statistics and visualizations revealed substantial variability in listing prices and indicated the presence of numerous extreme observations. Group comparisons showed that the average prices varied considerably by room type, property type, neighborhood, and super host status. Scatter plots suggested that the listings accommodating more guests generally command higher prices. The relationship between price and number of reviews was relatively weak. 

Overall, the analysis demonstrates that real-world datasets frequently require extensive preprocessing, and that descriptive statistics and visualizations are valuable tools for identifying patterns, anomalies, and discrepancies. These findings provide meaningful insights into New York City’s Airbnb market and illustrate the importance of exploratory analytics as a foundation for more advanced predictive modeling and business decision-making. 
Correlation Analysis 
Pearson’s correlation coefficient was calculated between Price and Number of Reviews. Correlation analysis measures the strength and direction of relationships between numerical variables. 
