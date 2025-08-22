import pandas as pd


class Cleaning:
    def __init__(self, ventes):
        self.ventes = ventes

    def clean_data(self):
        # Nettoyer les noms de colonnes
        self.ventes.columns = self.ventes.columns.str.strip()
        
        # Afficher les premières lignes du DataFrame
        print(self.ventes.head().to_string())
        print("\n")
        # Afficher les dernières lignes du DataFrame
        print(self.ventes.tail().to_string())
        print("\n")
        # Afficher la forme du DataFrame
        print(self.ventes.shape)
        print("\n")
        # Afficher les types de données de chaque colonne
        print(self.ventes.dtypes)
        print("\n")
        # Compter le nombre de lignes dupliquées
        print(self.ventes.duplicated().sum())
        print("\n")
        # Compter le nombre de valeurs uniques par colonne
        print(self.ventes.nunique())
        
    
    def clear_nunique(self):
        constantes = [col for col in self.ventes.columns if self.ventes[col].nunique() == 1]
        print("Colonnes constantes :", constantes)
        self.ventes = self.ventes.drop(columns=constantes, axis=1)


         # Vérifier les colonnes identiques (même valeur sur chaque ligne)
        cols = self.ventes.columns.tolist()
        to_drop = []
        for i in range(len(cols)):
            for j in range(i+1, len(cols)):
                if (self.ventes[cols[i]] == self.ventes[cols[j]]).all():
                    to_drop.append(cols[j])
        # Garder la première, supprimer les suivantes
        self.ventes = self.ventes.drop(columns=list(set(to_drop)), axis=1)

        return self.ventes
   
    def clear_categorical(self):
        constantes = [col for col in self.ventes.columns if self.ventes[col].nunique() == 2]
        print("Colonnes catogirie :", constantes)
        
        # Standardiser en 0/1
        for col in constantes:
            self.ventes[col] = self.ventes[col].astype('category').cat.codes
        
        return self.ventes
    
    def clear_date(self):
        # Convertir uniquement les colonnes qui ressemblent à des dates (pas des heures)
        date_cols = []
        for col in self.ventes.select_dtypes(include=['object']).columns:
            converted = pd.to_datetime(self.ventes[col], format="%Y-%m-%d", errors='coerce')
            # Vérifie que la majorité des valeurs ont l'heure à 00:00:00
            is_date = (converted.notna().mean() > 0.8) and ((converted.dt.hour == 0).mean() > 0.8)
            if is_date:
                date_cols.append(col)
                self.ventes[col] = converted
        print("Colonnes converties en date :", date_cols)
        return self.ventes
    
   
    
    
    def remove_outliers_by_cluster(df, cluster_col, value_col):
        """
        Supprime les outliers pour une colonne numérique dans chaque cluster
        en utilisant la méthode IQR.
        
        df : DataFrame
        cluster_col : nom de la colonne de cluster
        value_col : nom de la colonne numérique à traiter
        """
        def remove_outliers(group):
            Q1 = group[value_col].quantile(0.25)
            Q3 = group[value_col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            return group[(group[value_col] >= lower) & (group[value_col] <= upper)]
        
        return df.groupby(cluster_col).apply(remove_outliers).reset_index(drop=True)