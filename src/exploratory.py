from matplotlib import pyplot as plt
import seaborn as sns
import sys
from sklearn.ensemble import IsolationForest   
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
             
class Exploratory: 
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
    def winsorize_column(self, column):
        Q1 = self.ventes[column].quantile(0.25)
        Q3 = self.ventes[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        self.ventes[column] = self.ventes[column].clip(lower=lower_bound, upper=upper_bound)
        return self.ventes

    
    # si le donnee est normalement distribué, on peut utiliser le Z-score pour détecter les outliers
    # si la distribution n'est pas normale, on peut utiliser l'IQR ou Isolation Forest
    # Le Z-score mesure combien d'écarts-types une valeur est éloignée de la moyenne
    # Les valeurs avec un Z-score supérieur à 3 ou inférieur à -3 sont généralement considérées comme des outliers
    # Cette méthode est efficace pour les données qui suivent une distribution normale
    # Cependant, elle peut être sensible aux valeurs extrêmes et ne fonctionne pas bien pour les données non normales
    # Il est donc recommandé de vérifier la distribution des données avant d'appliquer cette méthode    
    def z_score(self, col):
        mean = self.ventes[col].mean()
        std_dev = self.ventes[col].std()
        
        z_scores = (self.ventes[col] - mean) / std_dev
        outliers_z = self.ventes[abs(z_scores) > 3]
        
        return outliers_z
    
    # Isolation Forest est une méthode d'apprentissage automatique pour détecter les anomalies
    # Elle est efficace pour les données de grande dimension et peut être utilisée même si la distribution des données n'est pas normale
    # L'algorithme construit des arbres de décision pour isoler les points de données
    # Les points qui sont isolés plus rapidement sont considérés comme des anomalies
    # Cette méthode est robuste aux valeurs extrêmes et peut gérer des données avec des formes de distribution complexes
    # Elle est particulièrement utile pour les données avec des dimensions élevées et des distributions non normales    
    def isolation_forest(self, col):
       
        model = IsolationForest(contamination=0.05)
        self.ventes['anomaly'] = model.fit_predict(self.ventes[[col]])
        
        outliers_if = self.ventes[self.ventes['anomaly'] == -1]
        
        return outliers_if
    
    
    # DBSCAN (Density-Based Spatial Clustering of Applications with Noise) est une méthode de clustering qui peut être utilisée pour détecter les outliers
    # Elle est basée sur la densité des points de données et peut identifier des clusters de points denses tout en considérant les points isolés comme des outliers
    # Elle est particulièrement utile pour les données avec des formes de clusters non sphériques et pour les données avec du bruit
    # DBSCAN nécessite de normaliser les données avant de l'appliquer   
    def dbscan(self, col):
     
        # Normalisation des données
        data_scaled = StandardScaler().fit_transform(self.ventes[[col]])
        
        # Application de DBSCAN
        db = DBSCAN(eps=0.5, min_samples=5).fit(data_scaled)
        
        # Ajout des labels de cluster à la DataFrame
        self.ventes['cluster'] = db.labels_
        
        # Détection des outliers (label -1)
        outliers_dbscan = self.ventes[self.ventes['cluster'] == -1]
        
        return outliers_dbscan
    
    # Méthode pour visualiser les outliers détectés
    # Cette méthode utilise seaborn pour créer un graphique de dispersion des données
    # Les points normaux sont affichés en bleu et les outliers en rouge
    # Elle permet de visualiser les outliers détectés par les différentes méthodes  
    def plot_outliers(self, outliers, colx, col, title=None):
        plt.figure(figsize=(8,5))
        sns.scatterplot(data=self.ventes, x=colx, y=col, color="blue", label="Normal")
        sns.scatterplot(data=outliers, x=colx, y=col, color="red", label="Outliers")
        plt.legend()
        if title:
            plt.title(title)
        plt.show()
        
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