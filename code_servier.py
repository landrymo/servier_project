
import numpy as np
import pandas as pd
import re 
import json
import warnings




class Servier():
    
    def __init__(self,
                 drugs_filepath,
                clinical_filepath,
                pubmed_filepath):
        
        
        self.drugs_df = pd.read_csv(drugs_filepath)
        self.clinical_df = pd.read_csv(clinical_filepath)
        self.pubmed_df = pd.read_csv(pubmed_filepath)
        
        self.drugs = self.drugs_df['drug'].map(lambda x : x.lower()).to_list()
        
        
        
    def create_graph(self):
    
            #'''
            #drugs: liste des médicaments que nous voulons retrouver 

            #Retourner le Dataframe que nous utilisons pour modéliser le graphique..

            #Créer un pd.Dataframe pour représenter le graphique. Nous choisissons d'utiliser un pd.Dataframe
            #La fonction to_json() permet de transformer le dataframe en objet json dict.

            #'''

        df = pd.DataFrame()
        df['drugs'] = self.drugs
        df['(PubMed,Date)'] = pd.Series([[] for i in range(len(self.drugs))])
        df['(Science,Date)'] = pd.Series([[] for i in range(len(self.drugs))])
        df['(Journal,Date)'] = pd.Series([[] for i in range(len(self.drugs))])
        df.set_index('drugs', drop = True, inplace=True)
        
        return df



    def preprocessing(self, var:str) -> pd.DataFrame:
    
        '''
        var: str, Le nom du dataset que nous voulons prétraiter doit être 'Science' ou 'PubMed'
        Retourne le dataset prétraité.
        '''
        
        if var == 'Science':
            Dataset = self.clinical_df
            Title_Column_Name = 'scientific_title'
        
        elif var == 'PubMed':
            Dataset = self.pubmed_df
            Title_Column_Name = 'title'
            
        else:
            warnings.warn("Attention, l'entrée var doit être 'Science' ou 'PubMed'.")
            
            
        # Suppression des doublons
        Dataset.drop_duplicates(subset=[Title_Column_Name], inplace=True)
        
        # Conversion de la colonne 'date' en datetime et remplacement de toutes les dates dans le même format.
        Dataset['date'] = pd.to_datetime(Dataset['date']).dt.strftime('%d/%m/%Y')
        
        #Suppression de NaN dans les titres, conversion des autres NaN en 'Inconnu' pour informer les utilisateurs
        
        Dataset.dropna(subset=[Title_Column_Name], inplace=True)
        Dataset.replace(float("NaN"), 'Unknown', inplace=True)
        
        
        # Transformation et uniformisation des caractères UNICODE
        Dataset[Title_Column_Name] = Dataset[Title_Column_Name].apply(lambda x: x.encode("ascii", "ignore").decode())
        Dataset['journal'] = Dataset['journal'].apply(lambda x: x.encode("ascii", "ignore").decode())
        
            
        
        # Pour uniformiser les journaux sans prendre en considération la ponctuation 
        # On utilise une regex pour ne garder que les lettres
        Dataset['journal'] = Dataset['journal'].apply(lambda x : re.sub(r'[^\w\s]','',x))
    
        if var == 'Science':
            self.clinical_df = Dataset
        else:
            self.pubmed_df = Dataset
            



    def Extraction(self, df:pd.DataFrame, var: str, preprop: bool = True) -> pd.DataFrame:
    
    
        '''
        df: pd.Dataframe, Le Dataframe que nous voulons compléter, il représente notre graphique.
        var: str, Nous devons nous focaliser sur publication scientifique ou publication médicale, nous devons utiliser 'Science' ou 'PubMed'.
        preprop: bool, True, si nous voulons prétraiter nos données avant l'extraction
    
        La fonction d'extraction a relié les médicaments aux articles et aux journaux qui les citent sous la forme d'une liste de tuple de la forme [(article or newspaper,date)].
        '''
    
        
        if preprop == True:
            self.preprocessing(var)
        
        if var == 'Science':
            Dataset = self.clinical_df
            Title_Column_Name = 'scientific_title'
        
        elif var == 'PubMed':
            Dataset = self.pubmed_df
            Title_Column_Name = 'title'
        
        else:
            warnings.warn("Attention, l'entrée var doit être 'Science' ou 'PubMed'.")
            
            
        for j in range(len(self.drugs)):
            
            print(f'{self.drugs[j]} est en cours de traitement')
            
            condition = Dataset[Title_Column_Name].apply(lambda x : x.lower().find(self.drugs[j])) != -1
            IS_CITED = Dataset[condition].index.tolist()
            
            for element in zip(
                Dataset[Title_Column_Name][IS_CITED].tolist(),
                Dataset['date'][IS_CITED].tolist()
            ):
                df[f'({var},Date)'].loc[self.drugs[j]].append(element)
                 
            for element in zip(
                Dataset['journal'][IS_CITED].tolist(),
                Dataset['date'][IS_CITED].tolist()
            ):
                df['(Journal,Date)'].loc[self.drugs[j]].append(element)
            
        return df
        



