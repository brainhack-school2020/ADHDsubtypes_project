import pandas as pd
import numpy as np
import glob
import os
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import permutation_test_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

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

def pca_features_df(df, pool):
    eeg_trimmed = df.loc[df['electrode_pool'] == pool]
    eeg_transp = pd.pivot_table(eeg_trimmed,values='fft_abs_power', index=['id'], columns=['brain_oscillation'])
    return eeg_transp

def pca_package(df_agg,pool, labels):
    eeg_transp = pca_features_df(df_agg, pool)

    
    standardized_data = StandardScaler().fit_transform(eeg_transp)#standardize data
    
    pca = PCA(n_components=2) #PCA
    principalComponents = pca.fit_transform(eeg_transp)
    principalDf = pd.DataFrame(data = principalComponents
                , columns = ['principal component 1', 'principal component 2'], index=eeg_transp.index.values)
    
    graph_data = pd.merge(principalDf ,labels, left_index=True, right_index=True) #2D PCA visualization
    graph_data["subtype"]= graph_data['subtype'].astype(str)
    fig = px.scatter(graph_data, x='principal component 1', y='principal component 2', color='subtype')
    
    return principalDf, fig, pca.explained_variance_ratio_

def knn_testing(principalDf, labels):
    features = principalDf[['principal component 1','principal component 2']].to_numpy()
    #create train, test sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels.to_numpy(), test_size=0.2, random_state=2)
     #Create KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=2)
    #Train the model using the training sets
    knn.fit(X_train, y_train.ravel())
    #Predict the response for test dataset
    y_pred = knn.predict(X_test)
    # Model Accuracy, how often is the classifier correct?
    
    accuracy = (metrics.accuracy_score(y_test, y_pred))
    
    score, permutation_scores, pvalue = permutation_test_score(
    knn, X_train, y_train.ravel(), scoring="accuracy",  n_permutations=100, n_jobs=1)

    return accuracy, score, pvalue