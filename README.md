# SNF_ADHDsubtypes_project

This project will be conducted for BrainHack school 2020

## Background

Attention deficit/hyperactivity disorder (ADHD) is one of the most common neurodevelopmental disorders among children and adolescents. It manifests itself through a variety of cognitive and behavioral symptoms, such as (but not limited to) hyperactivity, lack attention, impulsivity, lack of inhibition and diminished working memory. Subtype classification of ADHD has not reach consensus whithin the litterature and research on the correlates of ADHD subtypes show incoherent findings.Those subtypes are for the majority based on criteria derived from behavioral and-self-report data and lack of neurophysiological assessment is prominent([Hegerl et al. 2016](https://pubmed.ncbi.nlm.nih.gov/27178310/); [Olbrich, Dinteren & Arns, 2015](https://pubmed.ncbi.nlm.nih.gov/26901357/)).

## Project definition

This project will aim to investigate the presence of subtypes of ADHD from the possible associations between different types of measurements, pairing common behavioral and self-reporting measures to electrophysiological (EEG) data, as well as exploring complementary attributes. To do so, a Similarity Network Fusion (SNF) will be used to integrate these different types of data in a non-linear fashion, guided by the tutorial from Ross Markello. SNF permits the construction of similarity networks of samples (ADHD participants) for each data type, which are then iteratively integrated into in one novel network ([Wang et al., 2014](https://pubmed.ncbi.nlm.nih.gov/24464287/)). Integrating data with this method allows the exploration of common and complementary information between these different types of data. 

## Data

The sample consisted of 97 college students with an ADHD condition. Different types of measurements are included in this data sample. EEG data recording was performed using a 19-channel electrode cap (international 10-20 system) and consisted of eyes-opened at-rest recording of 5-minute duration. Time-frequency analyses were conducted for each electrode in order to extract amplitude means for each frequency band. Neuropsychological assessment measures included were Conners questionnaire (self-report) and IVA-II behavioral test.

## Tools


 * Git and GitHub
 * Jupyter Notebook
 * Python : main packages : pandas,MNE-BIDS, SNFpy based on previous [markdown](https://github.com/rmarkello/snfpy)
 * Visualization packages via python
 * MNE
 * Seaborn


## Deliverables

At the end of this project, we will have:

 - A Jupyter notebook markdown describing thoroughly all the steps of our project 
 - Python script of main analyses .
 - OSF project management 
 - Complete published repository access to all commits and changes of our projects
- A blog post describing the project
- An interactive platform to present the different data and analysis

  

## Progress overview

As of may 26 2020; the data has been preprocessed and organized into pandas dataframes. 

## Tools I learned during this project

 * Git and Github
 * Jupyter Notebook
 * Debugging
