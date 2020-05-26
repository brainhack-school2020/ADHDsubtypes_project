import pandas as pd
import numpy as np
import glob

def process_all_excel_files():
    df_full = pd.DataFrame()
    files = glob.glob('excel_files/*.xlsx')
    for file in files:
        df_full = df_full.append(process_excel_file(file))
    return df_full.reset_index(drop=True)


def process_excel_file(path):
    df = pd.read_excel(path, #file
                   header=None,
                   usecols="A:O") #selecting columns of interest
    brain_oscil = df.iloc[63].values
    freq_bands = df.iloc[64].values

    df = df.iloc[63:86] # selecting rows of interest
    col_names = {} # create dictionary for column names 
    for i in range(14+1):
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
    df["id"]=path.split("/")[1].split(".")[0] #WARNING!!! IF USING WINDOWS, CHANGE "/" TO "\\". No additionnal changes are needed.
    df["electrode"]= df["electrode"].apply(lambda x: x.split('-')[0])#splitting for not a string
    return df
