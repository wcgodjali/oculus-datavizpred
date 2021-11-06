# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 17:44:11 2020

@author: william
"""
# Importing the library
import time

# Importing all of the modules with python intrepreter
import heatmap_crowd
import heatmap_humid
import heatmap_temp
import konkat
import SARIMA_human_crowd_pred
import Violin_Plot_humanvscar

# Program

while(True):
    heatmap_crowd.crowd_map()
    time.sleep(2)
    heatmap_humid.humid_map()
    time.sleep(2)
    heatmap_temp.temp_map()
    time.sleep(2)
    SARIMA_human_crowd_pred.sarima_crowd()
    time.sleep(2)
    Violin_Plot_humanvscar.violin_crowd()
    time.sleep(2)
    konkat.konkat()
    