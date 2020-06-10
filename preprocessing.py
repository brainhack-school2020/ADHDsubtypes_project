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
import scipy
from scipy import stats
from scipy.stats import mannwhitneyu
from statsmodels.sandbox.stats.multicomp import multipletests

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

    confusion_matrix = metrics.confusion_matrix(y_test, y_pred, normalize='true')

    return accuracy, score, pvalue, confusion_matrix

def plot_matrix():
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    titles_options = [("Confusion matrix, without normalization", None),
                    ("Normalized confusion matrix", 'true')]
    for title, normalize in titles_options:
        disp = metrics.plot_confusion_matrix(knn, X_test, y_test,
                                    display_labels=['1','2'],
                                    cmap=plt.cm.Blues,
                                    normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()

def knn_testing_nopca(eeg_transp, labels):
    features = eeg_transp.to_numpy()
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



def validate_con():
    if Gender.value in df_conners['Gender'].unique() and adhdtype.value in df_conners['adhdtype'].unique():
        return True
    else:
        return False

def response_con(change):
 if validate_con():
    filter_list = [i and j for i, j in
                      zip(df_conners['Gender'] == Gender.value, df_conners['adhdtype'] == adhdtype.value)]
    temp_df = df_conners[filter_list]
    x1 = temp_df['cIM']
    x2 = temp_df['cHR']
    x3 = temp_df['cIE']
    x4 = temp_df['cSC']
    with g.batch_update():
        g.data[0].x = x1
        g.data[1].x = x2
        g.data[2].x = x3
        g.data[3].x = x4
        g.layout.barmode = 'overlay'
        g.layout.xaxis.title = 'Subject iD'
        g.layout.yaxis.title = 'Cognitive Scores'

def validate_beha():
    if Gender.value in df_behavioral['Gender'].unique() and adhdtype.value in df_behavioral['adhdtype'].unique():
        return True
    else:
        return False

def response_beha(change):
 if validate_beha():
    filter_list = [i and j for i, j in
                      zip(df_behavioral['Gender'] == Gender.value, df_behavioral['adhdtype'] == adhdtype.value)]
    temp_df = df_behavioral[filter_list]
    x1 = temp_df['Aqtot']
    x2 = temp_df['Aqaudi']
    x3 = temp_df['Aqvis']
    x4 = temp_df['RCQtot']
    x5 = temp_df['RCQaudi']
    x6 = temp_df['RCQvis']
    with g.batch_update():
        g.data[0].x = x1
        g.data[1].x = x2
        g.data[2].x = x3
        g.data[3].x = x4
        g.data[4].x = x5
        g.data[5].x = x6
        g.layout.barmode = 'overlay'
        g.layout.xaxis.title = 'Subject iD'
        g.layout.yaxis.title = 'Behavioral Scores'

def createdf_by_gender(brain_oscillation, df_analysis):
    df_oscillation = df_analysis.loc[df_analysis['brain_oscillation'] == brain_oscillation].reset_index(drop=True)
    df1 = df_oscillation.loc[df_oscillation['Gender'] == 1].reset_index(drop=True)
    df2 = df_oscillation.loc[df_oscillation['Gender'] == 2].reset_index(drop=True)
    return df1, df2

def createdf_by_subtype(brain_oscillation, df_analysis):
    df_oscillation = df_analysis.loc[df_analysis['brain_oscillation'] == brain_oscillation].reset_index(drop=True)
    df1 = df_oscillation.loc[df_oscillation['adhdtype'] == 1].reset_index(drop=True)
    df2 = df_oscillation.loc[df_oscillation['adhdtype'] == 2].reset_index(drop=True)
    return df1, df2


def mann_whitney(df1, df2, pvals):
    for i in range(df1.shape[1]): # for column i in df1 excluding column 0 (ids)
        data1 = df1.iloc[: , i]  #data 1 = column i
       #print('Column Contents : ', data1.values) # used if you want to verify that your columns are accurate
    for i in range(df2.shape[1]): # for column i in df2 excluding column 0 (ids)
        data2 = df2.iloc[: , i] #data 2 = column i
       #print('Column Contents : ', data2.values)  # used if you want to verify that your columns are accurate
        stat, p = mannwhitneyu(data1, data2) #mann-whitney test (non-param equivalent to 2 sampled t-test)
        #print('Statistics=%.3f, p=%.3f' % (stat, p)) #use if you want to check all your test scores
        pvals.append(p) # append each new p-value (1 for each column, so 19) into 1 array
        #print(pvals) # if you want to see your p-values
    return pvals