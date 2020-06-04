import pandas as pd
import numpy as np
import glob
import os

def process_all_excel_files():
    df_full = pd.DataFrame()
    files = glob.glob('excel_files/*.xlsx')
    for file in files:
        df_full = df_full.append(process_excel_file(file))
    return df_full.reset_index(drop=True)


def process_excel_file(path):
    df = pd.read_excel(path, #file
                   header=None,
                   usecols="A:L") #selecting columns of interest
    brain_oscil = df.iloc[63].values
    freq_bands = df.iloc[64].values

    df = df.iloc[63:84] # selecting rows of interest
    col_names = {} # create dictionary for column names 
    for i in range(11+1):
        if i == 0:
            col_name = 'electrode'
        else:
            col_name = brain_oscil[i]+'_'+freq_bands[i]#merge rows to create columns in order to pivot the table
            col_name = col_name.replace(' ', '')

        #add the generated col name
        col_names[i] = col_name

    df.rename(columns=col_names, inplace=True)
    df = df.iloc[2:23]
    #extract all column names (.column), transform in array (.values) and convert to a list (.tolist()). 
    #Then we removed electrode as it doesnt need to be melted
    df_col = df.columns.values.tolist()
    df_col.remove('electrode')
    #melt has to be performed on a fixed element, here the column electrode stays as is so = id_vars
    df = pd.melt(df, id_vars="electrode", value_vars=df_col, var_name="brain_oscillation", value_name='fft_abs_power')
    df['freq_band'] = df['brain_oscillation'].apply(lambda x: x.split('_')[1])#split into two columns
    df['brain_oscillation'] = df['brain_oscillation'].apply(lambda x: x.split('_')[0])
    df["id"]=path.split("/")[1].split(".")[0]
    df["electrode"]= df["electrode"].apply(lambda x: x.split('-')[0])#splitting for not a string
    return df

def categorize_subtypes(inat, hyper, std_dev=5.72):# clinical std_dev as threshold for classification (std_dev, pearson)
    if abs(inat-hyper)<std_dev:
        return 'mixed'
    else:
        if inat>hyper:
            return 'inat'
        else:
            return 'hyper'

def electrode_pools(electrode):
    if electrode in ['FP2', 'FP1', 'Fz', 'F3', 'F4', 'F7', 'F8']:
        return 'frontal'
    if electrode in ['C3','C4','Cz']:
        return 'central'
    if electrode in ['T3', 'T4', 'T5', 'T6']:
        return 'temporal'
    if electrode in ['P3', 'P4', 'Pz']:
        return 'parietal'
    if electrode in ['O1', 'O2']:
        return 'occipital'
    else:
        return 'N/A'
    