# Data_Prep
This repo is preparing the data.
1) Use the 'PM_Average_by_Window' to format the PM2.5 according to MODIS satellite flyover times.
2) Use the 'CSV_to_FC' to convert the PM2.5 data from a CSV file into a Google Earth Engine tabular data structure (ee.FeatureCollection).
3) Use the 'Combine_PM25_and_Satellite_Data' to colocate the ground-station PM2.5 and the satellite variables.
4) Use the 'Split_Data_for_CV' to split the data into 10 folds for consistent cross-validation in Google Earth Engine.
