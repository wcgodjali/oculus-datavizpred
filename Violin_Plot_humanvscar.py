# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 09:38:08 2020

@author: william
"""

def violin_crowd ():
    # Importing the libraries
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    import cv2
    #Importing the dataset
    df = pd.read_csv("data.csv")
    # Changing the index into time index
    time_new = pd.Series([]) 
    
    # Function to convert the date format 
    def convert24(str1): 
          
        # Checking if last two elements of time 
        # is AM and first two elements are 12 
        if str1[-2:] == "AM" and str1[:2] == "12": 
            return "00" + str1[2:-2] 
              
        # remove the AM     
        elif str1[-2:] == "AM": 
            return str1[:-2] 
          
        # Checking if last two elements of time 
        # is PM and first two elements are 12    
        elif str1[-2:] == "PM" and str1[:2] == "12": 
            return str1[:-2] 
              
        else: 
              
            # add 12 to hours and remove PM 
            return str(int(str1[:2]) + 12) + str1[2:8] 
    
    for i in range(len(df)):
        _,_,_,_,time=df["Date"][i].split()
        time=time[:-2]+":00 "+time[-2:]
        time_new[i] = (convert24(time))
        if (int((time_new[i])[0:2]) < 6) :
            time_new[i] = "0-5"
        elif (int((time_new[i])[0:2]) >= 6) and (int((time_new[i])[0:2]) < 13):
            time_new[i] = "6-12"
        elif (int((time_new[i])[0:2]) >= 13) and (int((time_new[i])[0:2]) < 19):
            time_new[i] = "13-18"
        else:
            time_new[i] = "18-23"
    
    # inserting new column with values of list made above   
    df.insert(0, 'Time(0-23)', time_new)
    df_globcatdens = df[['People Density', 'Car Density', 'Time(0-23)']] 
    
    # Concate the Car Density Value below People Density value
    
    # Adding Hue
    df_globcatdens.insert(3, 'Category', 'Human')
    
    for i in range(len(df_globcatdens)):
        df_globcatdens = df_globcatdens.append(pd.Series([df.iloc[i]['Car Density'], 0, df.iloc[i]['Time(0-23)'], 'Car'], index=df_globcatdens.columns ), ignore_index=True)
    df_globcatdens.columns = ['Density', 'Car Density', 'Time(0-23)', 'Category']   
    ax = sns.violinplot(x="Time(0-23)", y="Density", hue="Category", data=df_globcatdens, palette="muted", split=True, scale='width')
    ax.set_title('Distribution of Overall Traffic on a day', fontsize=16);
    plt.savefig("Violin_Density.png", dpi=300, bbox_inches = 'tight')
    img=cv2.imread('Violin_Density.png')
    resized=cv2.resize(img,(720,480))
    cv2.imwrite("send_Violin_Density.jpg",resized)