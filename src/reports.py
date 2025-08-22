
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd 

def sale_quantity(ventes , groupeby, col) : 
   
    cluster_order = (
        ventes.groupby(groupeby)[col]
        .mean()
        .sort_values()  
        .index
    )

    plt.figure(figsize=(8,6))
    sns.boxplot(
        data=ventes,
        x=groupeby,
        y=col,
        hue=groupeby,
        order=cluster_order, 
        palette="pastel"
    )

    plt.title(f"Distribution des Quantités par segmetation", fontsize=14, fontweight="bold")
    plt.xlabel("segmentation de Quantité", fontsize=12)
    plt.ylabel("Quantité vendue (Kg)", fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks([0,1,2], ["Faible", "Moyenne", "Grande"]) 

    plt.show()
    
  
  
def ratio_marge(ventes): 
    ventes['Date'] = pd.to_datetime(ventes['Date'])

  
    cluster_labels = {0: "Quantité moyenne", 1: "Grande quantité", 2: "Faible quantité"}
    ventes['Cluster_Label'] = ventes['QuantityCluster'].map(cluster_labels)


    plt.figure(figsize=(12,6))
    sns.lineplot(
        data=ventes, 
        x='Date', 
        y='Margin_Loss_Ratio_pct', 
        hue='Cluster_Label', 
        marker='o', 
        palette="Set2"
    )

    plt.title("Ratio Marge / Perte par segment (%)", fontsize=14, fontweight="bold")
    plt.xlabel("Mois", fontsize=12)
    plt.ylabel("Ratio Marge / Perte (%)", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.axhline(100, color='red', linestyle='--', label='Marge = Perte')
    plt.legend(title="Segment de vente vendu pa quantité")
    plt.tight_layout()
    plt.show()



def marge_par_produit(ventes): 
 
    cluster2 = ventes[ventes['QuantityCluster'] == 2]


    marge_par_produit = cluster2.groupby('ItemName')[['Margin', 'NetMargin']].mean().sort_values('NetMargin', ascending=False)

    plt.figure(figsize=(10,6))

    sns.barplot(
        x='NetMargin', 
        y=marge_par_produit.index, 
        data=marge_par_produit.reset_index(),
        color='steelblue'
    )

    plt.title("Top produits par marge nette (Vente 3)")
    plt.xlabel("Marge nette moyenne")
    plt.ylabel("Produit")
    plt.tight_layout()
    plt.show()


def relation_prix(ventes): 

    plt.figure(figsize=(10,6))

   
    sns.scatterplot(
        data=ventes, 
        x='QuantityKg', 
        y='UnitPrice', 
        hue='RelativeLossRate', 
        palette='coolwarm', 
        size='QuantityKg',   
        sizes=(20, 200),
        alpha=0.7
    )

    plt.title("Relation entre Quantité vendue, Prix unitaire et Taux de perte relatif")
    plt.xlabel("Quantité vendue (Kg)")
    plt.ylabel("Prix unitaire")

    plt.show()


def ratio_marge(ventes): 
   
    ventes['Margin_Loss_Ratio_pct'] = (ventes['MarginRate'] / ventes['LossRate']) * 100


    segment_labels = {0: 'Vente 1', 1: 'Vente 2', 2: 'Vente 3'}
    ventes['segmentation_label'] = ventes['segmentation'].map(segment_labels)

    
    plt.figure(figsize=(10,6))
    sns.lineplot(
        data=ventes,
        x='SaleDate',
        y='Margin_Loss_Ratio_pct',
        hue='segmentation_label', 
        marker='o',
        palette="Set2"
    )

    plt.title("Ratio Marge / Perte par segment (%)", fontsize=14, fontweight="bold")
    plt.xlabel("Mois")
    plt.ylabel("Ratio Marge / Perte (%)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)


    plt.axhline(100, color='red', linestyle='--', label='Marge = Perte')

    plt.legend(title='Segmentation')
    plt.show()


