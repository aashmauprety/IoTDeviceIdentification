import os
import pandas as pd
import numpy as np 
import argparse
import matplotlib as plt


# Mapping of MAC addresses to device names
# Mapping mac address to device name while saving csv for clarity
mac_device_mapping = {
    'd0:52:a8:00:67:5e': 'Smart Things',
    '44:65:0d:56:cc:d3': 'Amazon Echo',
    '70:ee:50:18:34:43': 'Netatmo Welcome',
    'f4:f2:6d:93:51:f1': 'TP-Link Day Night Cloud camera',
    '00:16:6c:ab:6b:88': 'Samsung SmartCam',
    '30:8c:fb:2f:e4:b2': 'Dropcam',
    '00:62:6e:51:27:2e': 'Insteon Camera',
    '00:24:e4:11:18:a8': 'Withings Smart Baby Monitor', 
    'ec:1a:59:79:f4:89': 'Belkin Wemo switch', 
    '50:c7:bf:00:56:39': 'TP-Link Smart plug',
    '74:c6:3b:29:d7:1d': 'ihome',
    'ec:1a:59:83:28:11': 'Belkin wemo motion sensor',
    '18:b4:30:25:be:e4': 'NEST Protect smoke alarm',
    '70:ee:50:03:b8:ac': 'Netatmo weather station',
    '00:24:e4:1b:6f:96': 'Withings Smart scale',
    '74:6a:89:00:2e:25': 'Blipcare Blood Pressure meter',
    '00:24:e4:20:28:c6': 'Withings Aura smart sleep sensor',
    'd0:73:d5:01:83:08': 'Light Bulbs LiFX Smart Bulb',
    '18:b7:9e:02:20:44': 'Triby Speaker',
    'e0:76:d0:33:bb:85': 'PIX-STAR Photo-frame',
    '70:5a:0f:e4:9b:c0': 'HP Printer',
    '08:21:ef:3b:fc:e3': 'Samsung Galaxy Tab',
    '30:8c:fb:b6:ea:45': 'Nest Dropcam',

}

def extract_feature(file, output_folder):
    print("Script to extract feature")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    df = pd.read_csv(file)

    # Find unique devices
    a = df['eth.src'].unique()
    b = df['eth.dst'].unique()
    devices = pd.unique(np.concatenate((a, b)))

    # Create a directory named "FeatureSet" if it doesn't exist
    feature_set_dir = output_folder
    if not os.path.exists(feature_set_dir):
        os.makedirs(feature_set_dir)

    # Define a function to apply the filtering and save CSV for each device
    def filter_and_save(device):
     
        filtered_df = df[(df['eth.src'] == device) | (df['eth.dst'] == device)]
        filtered_df['flow'] = filtered_df.apply(lambda row: -row['Size'] if row['eth.src'] == device else row['Size'], axis=1)
        filtered_df = filtered_df.dropna(subset=['flow'])
        data = filtered_df
        flow_values = data['flow'].values
        num_values_to_keep = len(flow_values) // 100 * 100
        flow_values_truncated = flow_values[:num_values_to_keep]
        reshaped_flow = flow_values_truncated.reshape(-1, 100)
        reshaped_df = pd.DataFrame(reshaped_flow)
        column_names = [f'column{i+1}' for i in range(reshaped_df.shape[1])]
        reshaped_df.columns = column_names
        device_name = mac_device_mapping.get(device, 'Unknown Device')
        reshaped_df.to_csv(os.path.join(feature_set_dir, f'{device_name}.csv'), index=False)

    # Apply the function for each device
    for device in devices:
        filter_and_save(device)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to extract sequence of features for each device ")
    parser.add_argument("file", type=str, help="Name of the combine csv file, for example combined.csv")
    parser.add_argument("output_folder", type=str, help="Path to the folder to save the feature set for each devices")
    args = parser.parse_args()

    extract_feature(args.file, args.output_folder)

