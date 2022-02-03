import json
from json import loads
import numpy as np
import pandas as pd
import re 

import warnings
from collections import Counter

from utils import *
from Preprocessing import *
from Extraction import *
from Pipeline import *

def Count_Drugs_Journal(drugs_publication_json_file):
    
    #'''
    #Compte le nombre de médicaments différents cités par chaque journal.

    #Retourne trois éléments :
    # -> le journal qui cite le plus de médicaments différents
    # -> le nombre de citations pour ce journal
    # -> un dictionnaire qui contient le nombre de médicaments différents cités par chaque journal.
    #'''
    
    parsed = loads(drugs_publication_json_file)

    liste_journal = []
    
    for drug, items in parsed.items():
        journals = set([journal[0] for journal in items['(Journal,Date)']])
        liste_journal = liste_journal + list(journals)
    
    nombre_journal = Counter(liste_journal)
    nombre_journal = sorted(nombre_journal.items(), key=lambda x: x[1], reverse=True)
    meilleur_journal, citation = nombre_journal[0][0], nombre_journal[0][1]
    
    print(f'Le journal qui cite le plus de médicaments différents est {nombre_journal[0][0]}, il cite {nombre_journal[0][1]} médicaments.')
        
    return meilleur_journal, citation , nombre_journal




