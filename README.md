# IoTDeviceIdentification
**Instructions:** 

Download Dataset:

1. Download the dataset from the UNSW website and combine all CSV files into a single file named combined.csv.

2. Run Feature Extraction Script:

       Execute the following command in your terminal or command prompt:
       python feature_extraction.py combined.csv FeatureData


This script will extract features from the combined CSV file and store them in a folder named FeatureData.

Review Extracted Features:

After running the script, you'll find a folder named FeatureData containing individual CSV files for each device, named devicename.csv.

Notes:
combined.csv should be the combined form of all CSV data from the UNSW website.
The extracted features for each device are listed in separate CSV files within the FeatureData folder.
