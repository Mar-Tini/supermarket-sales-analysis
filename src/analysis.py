from matplotlib import pyplot as plt
import seaborn as sns
import sys
from sklearn.ensemble import IsolationForest   
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
             
class Analisis: 
    def __init__(self, ventes):
        self.ventes = ventes
    
    
    # Analyse des données pour détecter les outliers
    
    # Méthodes pour détecter les outliers
    # IQR (Interquartile Range) est une méthode robuste pour détecter les outliers
    # Elle est basée sur la dispersion des données et est moins sensible aux valeurs extrêmes que le Z-score
    # L'IQR est calculé comme la différence entre le troisième quartile (Q3) et le premier quartile (Q1)
    # Les valeurs en dehors de l'intervalle [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR] sont considérées comme des outliers
    # Cette méthode est efficace pour les données qui ne suivent pas une distribution normale   
    def iqr(self, col):
        q1 = self.ventes[col].quantile(0.25)
        q3 = self.ventes[col].quantile(0.75)
        iqr = q3 - q1
        
        outliers_iqr = self.ventes[(self.ventes[col] < (q1 - 1.5 * iqr)) | (self.ventes[col] > (q3 + 1.5 * iqr))]
    
        return outliers_iqr 
    
    # Winsorisation pour limiter l'impact des valeurs extrêmes
    # La méthode winsorize remplace les valeurs extrêmes par les valeurs aux limites de l'intervalle interquartile
    # Elle est utilisée pour réduire l'influence des valeurs extrêmes sur les statistiques descriptives
    # l'intervalle interquartile (IQR) multiplié par un facteur (généralement 1.5)
    # Cela permet de réduire l'influence des valeurs extrêmes sur les statistiques descriptives
    
    def winsorize_column(self, column, method='iqr', factor=1.5, lower_percentile=0.05, upper_percentile=0.95):
        """
        Winsorize a column of the dataframe.
        
        method: 'iqr' -> classic IQR method
                'percentile' -> percentile-based method
        factor: multiplier for IQR (used only if method='iqr')
        lower_percentile / upper_percentile: used if method='percentile'
        """
        if method == 'iqr':
            Q1 = self.ventes[column].quantile(0.25)
            Q3 = self.ventes[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - factor * IQR
            upper_bound = Q3 + factor * IQR
        elif method == 'percentile':
            lower_bound = self.ventes[column].quantile(lower_percentile)
            upper_bound = self.ventes[column].quantile(upper_percentile)
        else:
            raise ValueError("Method must be 'iqr' or 'percentile'")
        
        self.ventes[column] = self.ventes[column].clip(lower=lower_bound, upper=upper_bound)
        return self.ventes

    # Méthode pour tracer la distribution d'une colonne
    # Cette méthode utilise matplotlib pour tracer la série temporelle d'une colonne spécifique
    # Elle permet de visualiser l'évolution des données au fil du temps
    # Les paramètres title et ylable permettent de personnaliser le titre et l'étiquette de l'axe des ordonnées
    def plot_distibution(self, col, title=None, ylable=None):
        self.ventes[col].plot(figsize=(12, 6))
        if title:
            plt.title(title)
        plt.xlabel('Date')
        if ylable:
            plt.ylabel(ylable)
        plt.grid(True)
        plt.show()
        
        
    
    def min_maxscaling(self, colonnes_numeriques): 
        min_max_scaler = MinMaxScaler()
        ventes_scaled = self.ventes.copy()
        ventes_scaled[colonnes_numeriques] = min_max_scaler.fit_transform(
            ventes_scaled[colonnes_numeriques]
        )
        return ventes_scaled
    
    def standardisation(self, colonnes_numeriques):
        standard_scaler = StandardScaler()
        ventes_scaled = self.ventes.copy()
        ventes_scaled[colonnes_numeriques] = standard_scaler.fit_transform(
            ventes_scaled[colonnes_numeriques]
        )
        return ventes_scaled
    
    def robust_scaling(self, colonnes_numeriques): 
        robust_scaler = RobustScaler()
        ventes_scaled = self.ventes.copy()
        ventes_scaled[colonnes_numeriques] = robust_scaler.fit_transform(
            ventes_scaled[colonnes_numeriques]
        )
        return ventes_scaled
    
    