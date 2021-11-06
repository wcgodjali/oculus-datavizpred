# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:20:03 2020

@author: william
"""

def sarima_crowd ():
    # Importing the libraries
    import warnings
    import itertools
    import pandas as pd
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    import cv2
    
    plt.style.use('fivethirtyeight')
    # Importing the dataset
    df = pd.read_csv("data.csv") #pay attention to the encoding
    df.head()
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
        if (int((time_new[i])[3:5]) < 15) :
            time_new[i] = float(time_new[i][0:2])
            # time_new[i] = (time_new[i][0:2]) + ":00:00"
        elif (int((time_new[i])[3:5]) >= 15) and (int((time_new[i])[3:5]) < 45):
            time_new[i] = float(time_new[i][0:2]) + 0.30
            # time_new[i] = (time_new[i])[0:2] + ":30:00"
        else:
            time_new[i] = float(time_new[i][0:2]) + 1.00
            '''
            add_1 = int((time_new[i])[0:2])
            add_1 += 1
            if (add_1 < 10) :
                time_new[i] = "0" + str(add_1) + ":00:00"
            else:
                time_new[i] = str(add_1) + ":00:00"
                '''
    # inserting new column with values of list made above         
    df.insert(0, 'New Time', time_new)
    dfmean_hour = df.groupby('New Time').mean()
    dfmean_hour = dfmean_hour[['Count']] 
    # Testing bagi 100 data
    for i in range(len(dfmean_hour)):
        dfmean_hour.iloc[i]['Count'] = dfmean_hour.iloc[i]['Count'] / 100
    '''
    dfmean_hour.plot(figsize=(15, 6))
    plt.show()
    '''
    
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 2)
    
    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))
    
    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    
    # specify to ignore warning messages
    warnings.filterwarnings("ignore")
    
    # Analyzing model with AIC values
    Min_AIC = 10000
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(dfmean_hour,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
    
                results = mod.fit()
                if (results.aic < Min_AIC ) :
                    Min_AIC = results.aic
                    p_min = param[0]
                    d_min = param[1]
                    q_min = param[2]
                    s_p_min = param_seasonal[0]
                    s_d_min = param_seasonal[1]
                    s_q_min = param_seasonal[2]
                    s_min = param_seasonal[3]
                    #print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue 
        
    mod = sm.tsa.statespace.SARIMAX(dfmean_hour,
                                    order=(p_min, d_min, q_min),
                                    seasonal_order=(s_p_min, s_d_min, s_q_min, s_min),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    
    results = mod.fit()
    # print(results.summary().tables[1])`
    results.plot_diagnostics(lags = 5, figsize=(15,7))
    plt.savefig("Forecast_Diagnostic.png", dpi=300)
    img=cv2.imread('Forecast_Diagnostic.png')
    resized=cv2.resize(img,(720,480))
    cv2.imwrite("send_Forecast_Diagnostic.jpg",resized)
    plt.show()
    
    # Get forecast 500 steps ahead in future
    pred_uc = results.get_prediction(start=2, end=32)
    # Get confidence intervals of forecasts
    pred_ci = pred_uc.conf_int()
    ax = dfmean_hour.plot(label='observed', figsize=(20, 10))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Time')
    ax.set_ylabel('People Count')
    ax.set_title('Daily Pass Over Traffic Forecasting', fontdict={'fontsize': '25', 'fontweight' : '3'})
    plt.legend()
    plt.savefig("Count_Forecast.png", dpi=300)
    img=cv2.imread('Count_Forecast.png')
    resized=cv2.resize(img,(720,480))
    cv2.imwrite("send_Count_Forecast.jpg",resized)
    plt.show()
