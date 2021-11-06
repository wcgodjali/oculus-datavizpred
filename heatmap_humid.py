# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 18:39:08 2020

@author: william
"""


def humid_map():
    # Importing the libraries
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import geopandas as gpd
    import cv2
    # Set the filepath and load in a shapefile
    fp = "Admin_Kec_AR_RBI25K/Admin_Kec_AR_RBI25K.shp"
    map_df = gpd.read_file(fp)
    
    # Check map
    #map_df.head()
    #map_df.plot()
    
    # load the density data
    df = pd.read_csv("data.csv") #pay attention to the encoding
    df.head()
    
    # Adding kecamatab column for Big data collection simulation
    df.insert(10, "kecamatan", "dummy")
    
    # Filling kecamatan column with random values
    kecamatan_list = "Gedangsari", "Girisubo", "Karangmojo", "Ngawen", "Bambanglipuro", "Banguntapan","Galur", "Girimulyo", "Kalasan", "Minggir", "Danurejan", "Kraton" 
    df["kecamatan"] = np.random.choice(kecamatan_list, size=len(df))
    
    # Merata-ratakan data kuantitatif yang didapat
    dfmean = df.groupby('kecamatan').mean()
    
    # Menambahkan kolom kecamatan sesuai dengan index yang hilang karena groupby
    listindexdfmean = list(dfmean.index.values)
    dfmean.insert(9, "kecamatan", listindexdfmean)
    
    # Merging (join the geodataframe with the cleaned up csv dataframe)
    merged = map_df.set_index('WADMKC').join(dfmean.set_index('kecamatan'))
    merged.head()
    
    # set a variable that will call whatever column we want to visualise on the map
    variable = 'Humidity'
    # set the range for the choropleth
    vmin, vmax = 50, 150
    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(10, 6))
    
    merged.plot(column=variable, cmap='Blues', ax=ax, linewidth=0.8, edgecolor='0.8')
    
    # remove the axis
    ax.axis('off')
    
    # add a title
    ax.set_title('Real-time Average Humidity in D.I.Y. Yogyakarta', fontdict={'fontsize': '18', 'fontweight' : '3'})
    # create an annotation for the data source
    ax.annotate('Source: OpenStreetMap, 2019',xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
                
    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    cbar = fig.colorbar(sm)
    # saving densitymap as an image file
    fig.savefig("map_hum.png", dpi=300)
    img=cv2.imread('map_hum.png')
    resized=cv2.resize(img,(720,480))
    cv2.imwrite("send_map_hum.jpg",resized)