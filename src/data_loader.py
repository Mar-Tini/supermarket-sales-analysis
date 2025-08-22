import pandas as pd
import requests
import sqlite3
from pathlib import Path
from functools import reduce

class LoadData: 
    """
    Classe pour charger des données depuis différentes sources.
    """
    
    def __init__(self, source, source_type="csv", validate=False, size=None):
        self.source = source
        self.source_type = source_type
        self.validate = validate
        self.size = size  # Définir size avant load_data
        self.data = self.load_data()  # Charge automatiquement les données
            
    def load_data(self):
        """
        Charge les données depuis différentes sources (CSV, Excel, API, SQL)
        en utilisant les attributs self.source et self.source_type.
        
        """
        try:
            if self.source_type == "csv":
                if not Path(self.source).is_file():
                    raise FileNotFoundError(f"Le fichier {self.source} n'existe pas.")
                df = pd.read_csv(self.source)
                print(f"Données CSV chargées depuis {self.source}")

            elif self.source_type == "excel":
                if not Path(self.source).is_file():
                    raise FileNotFoundError(f"Le fichier {self.source} n'existe pas.")
                df = pd.read_excel(self.source)
                print(f"Données Excel chargées depuis {self.source}")

            elif self.source_type == "api":
                response = requests.get(self.source)
                response.raise_for_status()
                df = pd.DataFrame(response.json())
                print(f"Données chargées depuis l'API {self.source}")

            elif self.source_type == "sql":
                conn = sqlite3.connect(self.source)
                query = "SELECT * FROM table_name"  # Remplace par ta table
                df = pd.read_sql_query(query, conn)
                conn.close()
                print(f"Données SQL chargées depuis {self.source}")

            else:
                raise ValueError(f"Type de source non supporté : {self.source_type}")
            
            if self.size is not None:
                df = df.head(self.size)
                return df
            
            return df
        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")
            return None

    def afficher_info(self):
        """
        Affiche les informations de base du DataFrame.
        """
        if self.data is not None:
            print("Informations sur le DataFrame :")
            print(self.data.info())
            print("\n")
            print("Premières lignes :")
            print(self.data.head().to_string(index=False))
            print("\n")
            print("nombre de valeurs uniques par colonne")
            print(self.data.nunique().to_string())
         
        else:
            print("Aucune donnée à afficher.")

    def fusionner(self, other_df, on, how='inner'):
        """
        Fusionne le DataFrame actuel avec un autre DataFrame.
        
        """
        if  other_df is not None:
            merged_df =  reduce(lambda left, right: left.merge(right, on=on, how=how), other_df)
            print(f"Fusion des DataFrames sur {on} avec une jointure {how}.")
            return merged_df
        else:
            print("Erreur : Un ou plusieurs DataFrames sont vides.")
            return None