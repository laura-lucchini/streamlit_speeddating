
#Contexte d'environnement
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .st-bf {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 0px 10px 0px rgba(0,0,0,0.1);
    }
    .st-bt {
        background-color: #FF69B4;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


#En-tête de la page streamlit
col1, col2, col3 = st.columns([1,2,1]) 
with col1:
    st.image("jedha.png", width=100)
with col2:
    st.title("Laura Lucchini")
with col3:
    st.image("tinder.png", width=300)


# Titre de la page
st.title("CDSD-Bloc 2-RNCP35288")
st.markdown("""
### Bonjour, voici mon projet de data-visualisation 
## **💖 _Speed Dating_ 💖 !**""")

if st.button("Cliquez ici pour en savoir plus !"):
    st.markdown("# **Contexte**")
    st.write("")
    st.markdown("""
    - **Client** : Tinder 
    
    - **Dates concernées** : 2002 - 2004  
    
    - **Nombre d'évènements** : 21 vagues aboutissant à 8378 rencontres  
    
    - **Nombre de participants** : 551 participants  
    
    - **Problématique** : Depuis le lancement de l'application de rencontres en 2012, Tinder fait face à une diminution du nombre de matchs et tentent de trouver un moyen de comprendre ce qui fait que les gens s'intéressent les uns aux autres. 
    
    - **Objectif** : A partir de l'analyse des données récoltées dans le cadre de speed-datings physiques et dans le but de concevoir un algorithme affiné correspondant à l'utilisateur, Identifier les facteurs qui influencent la décision d'un premier rendez-vous après le speed-dating """)
   
    st.markdown("# **Etape 1 - Intégration et nettoyage des données**")

    df = pd.read_csv("Speed+Dating+Data.csv", encoding='cp1252')

    pd.set_option('display.max_columns', None, 'display.max_rows', None)
    st.write("### Avant retraitement, voici un aperçu des données")
    st.dataframe(df.head())
    
    st.dataframe(df.describe(include="all"))

    missing_cols = pd.DataFrame({
    'Valeurs manquantes': df.isna().sum(),
    'Pourcentage des valeurs manquantes': round(100 * df.isna().sum() / df.shape[0], 2).astype(str) + '%'
})
 
    st.write("Identification des valeurs manquantes:")

    missing_sorted_desc = missing_cols.sort_values(by='Valeurs manquantes', ascending=False)

    st.write(missing_sorted_desc)
    st.write("Etapes de nettoyage des données:")

    st.write("- Attribution de valeurs textuelles pour la colonnes Gender")
    gender_map = {
    0: "Femme",
    1: "Homme"
}
    df['genre'] = df['gender'].map(gender_map)

    st.write("- Attribution de valeurs textuelles pour la colonne Carreer")
    REGLES_METIERS = {
    1:  ("Droit/Politique publique", ['law', 'attorney', 'legal', 'counsel', 'policy']),
    2:  ("Académique/Recherche", ['professor', 'teach', 'academ', 'research', 'scientist', 'phd', 'student', 'educat']),
    3:  ("Psychologue", ['psychol', 'therapist']),
    4:  ("Médecin/Médecine", ['doctor', 'medic', 'physician', 'health', 'clinic', 'cardio', 'pediat', 'dentist', 'nutrition']),
    5:  ("Ingénieur", ['engin', 'tech', 'software', 'program', 'web']),
    6:  ("Arts créatifs/Divertissement", ['art', 'music', 'film', 'act', 'entertain', 'creat', 'medi', 'produc', 'theat', 'comedi']),
    7:  ("Commerce/Finance/Administration", ['bank', 'consult', 'financ', 'market', 'business', 'ceo', 'manag', 'admin', 'entrepre', 'trad', 'sales', 'mba', 'account', 'economist']),
    8:  ("Immobilier", ['real estate']),
    9:  ("International/Humanitaire", ['international', 'humanitarian', 'develop', 'un ', 'ngo']),
    10: ("Indécis(e)", ['undecided', 'sure', 'know', '?', 'tba', 'idea']),
    11: ("Travail social", ['social']),
    12: ("Orthophonie", ['speech']),
    13: ("Politique", ['politic', 'gov', 'public serv', 'diplomat', 'lobby']),
    14: ("Sports professionnels/Athlétisme", ['sport', 'athlet', 'ball', 'box']),
    15: ("Autre", []),
    16: ("Journalisme", ['journalis', 'editor', 'writ', 'report']),
    17: ("Architecture", ['architect']),
    }


    career_map = {code: info[0] for code, info in REGLES_METIERS.items()}
    career_map[0] = "Non renseigné" 

    def trouver_code_metier(texte):
        if not isinstance(texte, str): return 0
        texte = texte.lower()
        
        for code, (nom, keywords) in REGLES_METIERS.items():
            if any(mot in texte for mot in keywords):
                return code
                
        return 

    # ---------------- APPLICATION ----------------


    df['career_c'] = df['career_c'].fillna(0)

    mask_manquant = (df['career_c'] == 0)

    df.loc[mask_manquant, 'career_c'] = df.loc[mask_manquant, 'career'].apply(trouver_code_metier)

    df['emploi'] = df['career_c'].map(career_map).fillna("Non renseigné")

    
    df_unique = df.drop_duplicates(subset=['iid'])

    emploi = df_unique.groupby(['emploi']).size().reset_index(name='Nombre')

    emploi = emploi.sort_values(by='Nombre', ascending=False)

    st.write("- Regroupement des métiers en grandes catégories")

    st.write("- Renommage des colonnes")

    st.markdown("""
    - Recherche de valeurs dupliquées
    
    - Attribution de valeurs textuelles pour les objectifs de soirée
    
    - Attribution de valeurs textuelles pour la colonne Match
    
    - Création de sous-ensembles selon les besoins d'analyses""")

    st.markdown("# **Etape 2 - Visualisations descriptives: par sexe, par age et par emploi**")

    st.write(f"il y a un total de {len(df['iid'].unique())} participants")

    data_sexe = df_unique['genre'].value_counts()

    col1, col2 = st.columns([1.5,2.5]) 
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.tight_layout()
        ax.pie(
            data_sexe.values,
            labels=data_sexe.index,
            colors=["lightblue", "pink"],
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
        )
        ax.set_title("Sexe des participants aux speeds dating", fontsize=22, pad=30, fontname='Arial')
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.tight_layout()
        sns.boxplot(data=df_unique,  x="age",y="genre", palette=["pink", "lightblue"], ax=ax)
        plt.title("Âge des participants aux speeds dating", fontsize=22, pad=30, fontname='Arial')

        # Afficher le boxplot dans Streamlit
        st.pyplot(fig)

        data_emploi = df_unique['emploi'].value_counts()
        total = data_emploi.sum()

        fig, ax = plt.subplots(figsize=(13, 8))
        plt.tight_layout()
        palette = sns.color_palette("pastel", len(data_emploi.index)) 
        plt.barh(data_emploi.index, data_emploi.values, color=palette)
        plt.gca().invert_yaxis()


    for index, value in enumerate(data_emploi.values):
        percent = (value / total) * 100
        label = f"{value}  ({percent:.1f}%)"
        plt.text(x=value, y=index, s=f" {label}", va='center', fontsize=10, color='black')

    plt.title("Répartition des emplois", fontsize=22, pad=30, fontname='Arial')
    plt.xlabel("Nombre de participants")
    st.pyplot(fig)

    st.markdown(""" 
    **Conclusion sur l'échantillon analysé:**

    - La population analysée s'élève à 551 participants.

    - La parité Hommes / Femmes est respectée.

    - Les âges des participants sont dans la même tranche (moins de 30 ans) mis à part 3 exceptions chez les hommes et 3 chez les femmes (non significatifs)

    - Les métiers représentés sont principalement dans le domaine tertiaire ce qui est probablement lié à la localisation des speed datings """)


    st.markdown("# **Etape 3 - Analyse des données**")
    #Analyse 1
    st.markdown("## Axe d'analyse n°1: est ce que la notation des attributs chez le partenaire évolue au fil du temps?")
    # création d'un dataframe "propre" pour analyse ultérieure
    df2=df
    # retrait des vagues 6 à 9 pour lesquelles la notation des attributs recherchés est différente
    df_attribute = df[~df['wave'].isin([6,7,8,9])]  
    
    # constitution de 4 dataframes correspondants à la notation des attributs recherchés chez les partenaires, suppression des lignes vides

    # avant le Speed dating

    df_attr_1 = df_attribute.iloc[:,[195,69,70,71,72,73,74]]
    df_attr_1 = df_attr_1.dropna()

    # Pendant le speed dating

    df_attr_2 = df_attribute.iloc[:,[195,108,109,110,111,112,113]]
    df_attr_2 = df_attr_2.dropna()


    # le lendemain du speed dating

    df_attr_3 = df_attribute.iloc[:,[195,128,129,130,131,132,133]]
    df_attr_3 = df_attr_3.dropna()


    # 3/4 semaines aprés le speed dating

    df_attr_4 = df_attribute.iloc[:,[195,161,162,163,164,165,166]]
    df_attr_4 = df_attr_4.dropna()


    #renommage des colonnes
    df_attr_1 = df_attr_1.rename(columns= {'attr1_1': 'Attractive',
                'sinc1_1':'Sincere',
                'intel1_1' : 'Intelligent',
                'fun1_1' : 'Funny',
                'amb1_1' : 'Ambitious',
                'shar1_1' : 'shares hobbies'})

    df_attr_2 = df_attr_2.rename(columns= {'attr1_s': 'Attractive',
                'sinc1_s':'Sincere',
                'intel1_s' : 'Intelligent',
                'fun1_s' : 'Funny',
                'amb1_s' : 'Ambitious',
                'shar1_s' : 'shares hobbies'})

    df_attr_3 = df_attr_3.rename(columns= {'attr1_2': 'Attractive',
                'sinc1_2':'Sincere',
                'intel1_2' : 'Intelligent',
                'fun1_2' : 'Funny',
                'amb1_2' : 'Ambitious',
                'shar1_2' : 'shares hobbies'})

    df_attr_4 = df_attr_4.rename(columns= {'attr1_3': 'Attractive',
                'sinc1_3':'Sincere',
                'intel1_3' : 'Intelligent',
                'fun1_3' : 'Funny',
                'amb1_3' : 'Ambitious',
                'shar1_3' : 'shares hobbies'})


    # Séparation par genre et suppression de la colonne 'genre'
    df_attr_1_hom = df_attr_1[df_attr_1['genre'] == 'Homme'].drop(columns=['genre'])
    df_attr_1_fem = df_attr_1[df_attr_1['genre'] == 'Femme'].drop(columns=['genre'])

    df_attr_2_hom = df_attr_2[df_attr_2['genre'] == 'Homme'].drop(columns=['genre'])
    df_attr_2_fem = df_attr_2[df_attr_2['genre'] == 'Femme'].drop(columns=['genre'])

    df_attr_3_hom = df_attr_3[df_attr_3['genre'] == 'Homme'].drop(columns=['genre'])
    df_attr_3_fem = df_attr_3[df_attr_3['genre'] == 'Femme'].drop(columns=['genre'])

    df_attr_4_hom = df_attr_4[df_attr_4['genre'] == 'Homme'].drop(columns=['genre'])
    df_attr_4_fem = df_attr_4[df_attr_4['genre'] == 'Femme'].drop(columns=['genre'])

    # Renommer les colonnes pour plus de clarté
    for df in [df_attr_1_hom, df_attr_1_fem, df_attr_2_hom, df_attr_2_fem,
            df_attr_3_hom, df_attr_3_fem, df_attr_4_hom, df_attr_4_fem]:
        df.columns = ['Beauté', 'Sincérité', 'Intelligence', 'Humour', 'Ambition', 'Intérets communs']

    # Liste des temporalités
    temporalites = ["Avant", "Pendant", "Lendemain", "3/4 semaines après"]

    # DataFrames pour les moyennes
    moyennes_hommes = pd.DataFrame(index=['Beauté', 'Sincérité', 'Intelligence', 'Humour', 'Ambition', 'Intérets communs'], columns=temporalites)
    moyennes_femmes = pd.DataFrame(index=['Beauté', 'Sincérité', 'Intelligence', 'Humour', 'Ambition', 'Intérets communs'], columns=temporalites)

    # Remplir les moyennes pour les hommes
    moyennes_hommes["Avant"] = df_attr_1_hom.mean()
    moyennes_hommes["Pendant"] = df_attr_2_hom.mean()
    moyennes_hommes["Lendemain"] = df_attr_3_hom.mean()
    moyennes_hommes["3/4 semaines après"] = df_attr_4_hom.mean()

    # Remplir les moyennes pour les femmes
    moyennes_femmes["Avant"] = df_attr_1_fem.mean()
    moyennes_femmes["Pendant"] = df_attr_2_fem.mean()
    moyennes_femmes["Lendemain"] = df_attr_3_fem.mean()
    moyennes_femmes["3/4 semaines après"] = df_attr_4_fem.mean()

    def plot_grouped_bars(df, title, palette="pastel"):
        fig, ax = plt.subplots(figsize=(10, 7))
        bar_width = 0.15  
        x = np.arange(len(df.index))  

        for i, temporalite in enumerate(df.columns):
            ax.bar(x + i * bar_width, df[temporalite], width=bar_width, label=temporalite, color=sns.color_palette(palette)[i])

    
        ax.set_xticks(x + bar_width * 1.5)
        ax.set_xticklabels(df.index, rotation=45, ha='right', fontsize=10)
        #ax.set_ylabel("Moyenne", fontsize=12)
        ax.set_title(title, fontsize=16, pad=20)
        ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()
        st.pyplot(fig)
    
   
    plot_grouped_bars(moyennes_hommes, "Moyenne des notations par critère — Hommes", palette="pastel")
    
    plot_grouped_bars(moyennes_femmes, "Moyenne des notations par critère — Femmes", palette="pastel")

    st.markdown("""
    ### **Analyse des critères d’attractivité dans le temps**

    Les notations des participants mettent en évidence des dynamiques différenciées selon le genre :

    **Chez les hommes**

    L’attractivité physique demeure le critère dominant à tous les moments de mesure.

    Le lendemain de l’événement, le critère « drôle » progresse et devance l’intelligence, habituellement citée comme deuxième qualité recherchée.

    Les écarts entre le critère principal et les autres attributs sont nettement marqués, traduisant une hiérarchie claire des préférences.

    **Chez les femmes**

    Avant le speed dating, l’intelligence est déclarée comme le principal facteur d’attractivité.

    À partir du speed dating, l’attractivité physique devient le critère n°1 et le reste dans le temps.

    Les différences entre attributs sont plus modérées que chez les hommes, suggérant des préférences plus équilibrées.

    **➜ À retenir**

    Le speed dating ne modifie pas les préférences exprimées par les hommes.

    Il entraîne en revanche une évolution plus marquée des critères déclarés par les femmes, avec un recentrage sur l’attractivité physique après l’expérience.""")
        
        
    #Analyse 2
    st.markdown("## Axe d'analyse n°2: est ce que la façon dont les participants s'auto évaluent a une incidence sur le fait d'avoir un match?")
    df_eval = df2.loc[:,['genre','match', 'attr3_1', 'sinc3_1', 'fun3_1', 'intel3_1', 'amb3_1', 'attr3_2', 'sinc3_2', 'intel3_2', 'fun3_2', 'amb3_2']]
    #Auto evaluation avant le Speed dating

    df_eval_1 = df2.loc[:,['genre','match', 'attr3_1', 'sinc3_1', 'fun3_1', 'intel3_1', 'amb3_1']]
    df_eval_1 = df_eval_1.dropna()


    # Auto evaluation le lendemain du speed dating

    df_eval_3 = df2.loc[:,['genre','match', 'attr3_2', 'sinc3_2', 'intel3_2', 'fun3_2', 'amb3_2']]
    df_eval_3 = df_eval_3.dropna()



    #renommage des colonnes
    df_eval_1  = df_eval_1 .rename(columns= {'attr3_1': 'Beauté',
                'sinc3_1':'Sincérité',
                'intel3_1' : 'Intelligence',
                'fun3_1' : 'Humour',
                'amb3_1' : 'Ambition'})

    df_eval_3 = df_eval_3.rename(columns= {'attr3_2': 'Beauté',
                'sinc3_2':'Sincérité',
                'intel3_2' : 'Intelligence',
                'fun3_2' : 'Humour',
                'amb3_2' : 'Ambition'})

    # subdivision match / no match 

    df_eval_1_match = df_eval_1[df_eval_1['match']==1]
    df_eval_1_no_match = df_eval_1[df_eval_1['match']==0]
    df_eval_3_match = df_eval_3[df_eval_3['match']==1]
    df_eval_3_no_match = df_eval_3[df_eval_3['match']==0]

    # subdivision Hommes / femmes

    df_eval_1_match_Homme = df_eval_1_match[df_eval_1_match['genre']=='Homme']
    df_eval_1_match_Femme = df_eval_1_match[df_eval_1_match['genre']=='Femme']
    df_eval_1_no_match_Homme = df_eval_1_no_match[df_eval_1['genre']== 'Homme']
    df_eval_1_no_match_Femme = df_eval_1_no_match[df_eval_1['genre']== 'Femme']
    df_eval_3_match_Homme = df_eval_3_match[df_eval_3_match['genre']=='Homme']
    df_eval_3_match_Femme = df_eval_3_match[df_eval_3_match['genre']=='Femme']
    df_eval_3_no_match_Homme = df_eval_3_no_match[df_eval_3['genre']== 'Homme']
    df_eval_3_no_match_Femme = df_eval_3_no_match[df_eval_3['genre']== 'Femme']

    
    # Liste des critères
    criteres =  ['Beauté', 'Sincérité', 'Intelligence', 'Humour', 'Ambition']

    # DataFrame pour les moyennes (hommes)
    moyennes_hommes2 = pd.DataFrame(index=criteres)
    moyennes_hommes2["Avant_Match"] = df_eval_1_match_Homme[criteres].mean()
    moyennes_hommes2["Après_Match"] = df_eval_3_match_Homme[criteres].mean()
    moyennes_hommes2["Avant_NoMatch"] = df_eval_1_no_match_Homme[criteres].mean()
    moyennes_hommes2["Après_NoMatch"] = df_eval_3_no_match_Homme[criteres].mean()

    # DataFrame pour les moyennes (femmes)
    moyennes_femmes2 = pd.DataFrame(index=criteres)
    moyennes_femmes2["Avant_Match"] = df_eval_1_match_Femme[criteres].mean()
    moyennes_femmes2["Après_Match"] = df_eval_3_match_Femme[criteres].mean()
    moyennes_femmes2["Avant_NoMatch"] = df_eval_1_no_match_Femme[criteres].mean()
    moyennes_femmes2["Après_NoMatch"] = df_eval_3_no_match_Femme[criteres].mean()
    
    def plot_grouped_bars(df, title):
        fig, ax = plt.subplots(figsize=(12, 6))
        bar_width = 0.15
        x = np.arange(len(df.index))

        # Définir les couleurs : 2 tons de vert pour les "Match", 2 tons de rose pour les "No Match"
        couleurs = {
            "Avant_Match": "#7FFFD4",  # Vert clair
            "Après_Match": "#33B39B",  # Vert foncé
            "Avant_NoMatch": "#FFC0CB",  # Rose clair
            "Après_NoMatch": "#DB7093"   # Rose foncé
        }

        for i, col in enumerate(df.columns):
            ax.bar(x + i * bar_width, df[col], width=bar_width, label=col, color=couleurs[col])


        ax.set_xticks(x + bar_width * 1.5)
        ax.set_xticklabels(df.index, rotation=45, ha='right', fontsize=10)
        #ax.set_ylabel("Moyenne", fontsize=12)
        ax.set_title(title, fontsize=16, pad=20)
        ax.set_ylim(0, 9)  # Axe des ordonnées jusqu'à 9
        ax.legend(fontsize=10, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        st.pyplot(fig)

    # Tracer pour les hommes
    plot_grouped_bars(moyennes_hommes2, "Auto-évaluation moyenne — Hommes")

    # Tracer pour les femmes
    plot_grouped_bars(moyennes_femmes2, "Auto-évaluation moyenne — Femmes")

    # Construire la matrice de corrélation
    df_eval_1 = df_eval_1.drop(columns=['genre'])
    corr_matrix = df_eval_1.corr()
    # Visualiser la heatmap 
    st.write("Matrice de corrélation (heatmap) :")
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True, ax=ax)
    ax.set_title("Matrice de corrélation")
    st.pyplot(fig)

    #Conclusions analyse 2
    st.markdown("""
    ### **Impact de l’auto-évaluation sur l’obtention d’un match**

L’analyse montre que l’auto-évaluation des participants évolue peu selon qu’ils obtiennent un match ou non.

- **Chez les hommes**

L’auto-évaluation après le speed dating est légèrement inférieure à celle mesurée avant l’événement
(–0,06 point sur l’attribut principal, indépendamment de l’obtention d’un match).

- **Chez les femmes**

En cas de match, l’auto-évaluation du meilleur attribut progresse légèrement (+0,06 point).

En l’absence de match, elle diminue marginalement (–0,02 point).

- **Globalement**

Les écarts d’auto-évaluation entre participants ayant obtenu un match et ceux n’en ayant pas obtenu sont faibles et non significatifs.

**➜ À retenir**

La manière dont les participants s’auto-évaluent n’a pas d’impact notable sur la probabilité d’obtenir un match.""")


    st.markdown("## Axe d'analyse n°3: Est ce que les speed-datings à thèmes conduisent à plus de matchs entre les participants?")

    st.markdown("""
    Lors des vagues 18,19,20 et 21, les participants ont apporté un livre ou un magazine, mettant en évidence un intéret marqué dans le thème de la lecture. 

    Il est intéressant de vérifier si les taux de matchs sont plus significatifs dans ces cas?""")

    df_interest = df2[df2['wave'].isin([18,19,20,21])]  

    col1, col2 = st.columns(2) 
    with col1:
        # Rappel : part des matchs sur la totalité des rencontres
        data_match = df2['match'].value_counts()
        labels = ['Non' if index == 0 else 'Oui' for index in data_match.index]

        # Couleurs personnalisées
        colors = ['#FFC0CB', '#7FFFD4']

        # Créer le graphique en camembert
        fig, ax = plt.subplots()
        ax.pie(
            data_match.values,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            radius=1
        )

        ax.set_title("Répartition des matchs sur la totalité des rencontres", fontsize=14, pad=30)

        # Afficher le graphique dans Streamlit
        st.pyplot(fig)
    with col2:
        # Répartition des matchs suite aux speed-datings "à thèmes"
        data_interest_match = df_interest['match'].value_counts()
        colors = ['#FFC0CB', '#7FFFD4']

        # Corriger les labels pour correspondre à data_interest_match
        labels = ['Non' if index == 0 else 'Oui' for index in data_interest_match.index]

        # Créer le graphique en camembert
        fig, ax = plt.subplots()
        ax.pie(
            data_interest_match.values,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90,
            radius=1
        )

        ax.set_title("Répartition des matchs - Speed-datings à thèmes", fontsize=14, pad=30)

        # Afficher le graphique dans Streamlit
        st.pyplot(fig)
    # conclusion:
    st.markdown("""
    ### **Impact des speed-datings à thèmes sur les matchs:**

    L’analyse des données montre que les rencontres avec un thème commun (ex : participants arrivant avec un livre ou un magazine) ne génèrent pas un taux de matchs plus élevé que les sessions classiques.

    **→ À retenir**
    Un intérêt commun (ex : lecture) ne semble pas augmenter significativement les chances de match entre les participants.

    **Note méthodologique**
    Ces résultats sont à considérer sous réserve d’un échantillon réduit. Une analyse sur un plus grand volume de données serait nécessaire pour confirmer cette tendance""")
    
    
    st.markdown("## Axe d'analyse n°4: Est ce que l'objectif principal incitant les participants à participer au speed-dating a une incidence sur le taux de match?")

    df_goal = df2.dropna(subset=['goal'])
    map_goal = {
    1: 'Pour passer une soirée amusante',
    2: 'Pour rencontrer de nouvelles personnes',
    3: 'Pour obtenir un rendez-vous',
    4: 'Pour trouver une relation sérieuse',
    5: "Pour dire que je l’ai fait",
    6: 'Autre'
    }

    df_goal["objectif"] = df_goal['goal'].map(map_goal)

    df_goal_1 = df_goal[df_goal['goal']==1]
    df_goal_2 = df_goal[df_goal['goal']==2]
    df_goal_3 = df_goal[df_goal['goal']==3]
    df_goal_4 = df_goal[df_goal['goal']==4]
    df_goal_5 = df_goal[df_goal['goal']==5]
    df_goal_6 = df_goal[df_goal['goal']==6]

    data_goal_1_match = df_goal_1['match'].value_counts()
    data_goal_2_match = df_goal_2['match'].value_counts()
    data_goal_3_match = df_goal_3['match'].value_counts()
    data_goal_4_match = df_goal_4['match'].value_counts()
    data_goal_5_match = df_goal_5['match'].value_counts()
    data_goal_6_match = df_goal_6['match'].value_counts()

    dataframes = [data_goal_1_match,data_goal_2_match,data_goal_3_match,data_goal_4_match,data_goal_5_match,data_goal_6_match]
    titres = ['Pour passer une soirée amusante',
        'Pour rencontrer de nouvelles personnes',
        'Pour obtenir un rendez-vous',
        'Pour trouver une relation sérieuse',
        'Pour dire que je l’ai fait',
        'Autre'
    ]  
    colors =['#FFC0CB', '#7FFFD4']

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 11))

    fig.suptitle("Répartition des matches par objectif de speed dating", fontsize=30, y=1.02)

    # Boucle pour créer un pie chart par objectif
    for i, (ax, titre, data) in enumerate(zip(axes.flatten(), titres, dataframes)):
    
        sizes = data.values

        # Créer le pie chart
        ax.pie(sizes, labels=['Non', 'oui'], colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title(titre, fontsize=18)

    # Ajuster l'espacement et afficher
    plt.tight_layout()
    st.pyplot(fig)

    #Conclusion

    st.markdown("""
    ### impact de l'objectif principal sur le taux de match:

    Les taux de matchs sont relativement semblables d'un objectif à l'autre, seul l'objectif "autre" conduit à un taux en dessous de 15%

    **→ À retenir**

    L'objectif avec lequel les participants assistent à un speed dating n'a pas d'impact significatif sur le fait d'obtenir un match ou non""")

    
    st.markdown("## Axe d'analyse n°5: Est ce que le fait d'avoir un match a une incidence sur le fait d'avoir un rendez vous?")

    # Répartition des matchs sur la population totale par date
    data_df_date = df2['date_3'].value_counts()

    # Couleurs personnalisées
    colors = ['#FFC0CB', '#7FFFD4']

    # Créer des labels basés sur les valeurs de data_df_date
    # Si 'date_3' est binaire (0 ou 1), utilise cette ligne :
    labels = ['Non' if str(index) == '0' else 'Oui' for index in data_df_date.index]

    # Créer le graphique en camembert
    fig, ax = plt.subplots()
    ax.pie(
        data_df_date.values,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90,
        radius=1
    )

    ax.set_title("Répartition des personnes ayant eu 1 date (avec ou sans match préalable)", fontsize=14, pad=20)
    st.pyplot(fig)
    df_match=df2[df2['match']==1]
    df_no_match=df2[df2['match']==0]
    col1, col2 = st.columns([1.85,2.15]) 
    with col1:
        #répartition des personnes ayant eu un rdv avec leur match (sur la population ayant eu un match)

        data_date = df_match['date_3'].value_counts()
        colors =[ '#7FFFD4','#FFC0CB']
        labels = ['Non' if index == 0 else 'Oui' for index in data_match.index]

        fig, ax = plt.subplots()
        ax.pie(data_date.values, labels=labels,  
                colors=colors,
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90,
            radius=1
            )
        #plt.legend(bbox_to_anchor=(1.1, 1.05))
        ax.set_title("Répartition personnes ayant eu 1 date aprés leur match", fontsize = 14, pad=30)   
        st.pyplot(fig)    

    with col2:   
        #répartition des personnes ayant eu un rdv sans avoir eu de match (sur la population n'ayant pas eu match)

        data_date_nomatch = df_no_match['date_3'].value_counts()
        colors =['#FFC0CB', '#7FFFD4']
        labels = ['Non' if index == 0 else 'Oui' for index in data_match.index]

        fig, ax = plt.subplots()
        ax.pie(data_date_nomatch.values, labels=labels,  
                colors=colors,
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90,
            radius=1
            )
        
        ax.set_title("Répartition personnes ayant eu 1 date sans avoir eu de match", fontsize = 14, pad=15)   
                                                                                            
        st.pyplot(fig)                                                                         
    st.markdown("""
    ### Impact d'un match sur le fait d'avoir un rendez vous?

    **16,5% des participants (soit 8,25 % des rencontres)** ont obtenu un match.

    Parmi eux, 51,1% ont eu un premier rendez-vous.
    Parmi ceux sans match, 34,8% ont tout de même eu un rendez-vous.

    **→ Constat**
    Bien qu’un match doive théoriquement favoriser les rendez-vous, l’écart observé (51,1 % vs 34,8 %) reste moins marqué qu’attendu.

    **→ Questionnement**
    Incohérence possible : Les participants sans match ne devraient pas pouvoir se rencontrer ultérieurement.
    Hypothèse alternative : Possibilité de "matchs a posteriori" non documentés.

    **→ À retenir**
    L’impact d’un match sur l’obtention d’un rendez-vous est moins net que prévu, soulignant un doute sur la qualité ou la cohérence des données.""")
    
    
    st.markdown("# **Etape 4 - Conclusion & recommandations**")
    st.markdown("**Facteurs influençant l’obtention d’un premier rendez-vous**")

    st.markdown("**→ Conclusion**")
    st.markdown("Les axes analysés ne permettent pas d’identifier les facteurs influençant la décision d’un premier rendez-vous après un speed-dating.")

    st.markdown("**Limites de l’analyse et recommandations**")

    st.markdown("**Objectif initial:**")
    st.markdown("Aider Tinder à identifier les facteurs clés de succès pour qu’un match sur leur application aboutisse à un premier rendez-vous, voire à une relation durable. L’objectif était de construire un modèle prédictif mettant en avant les profils les plus susceptibles de plaire aux utilisateurs.")

    st.markdown("**Limites identifiées**")

    st.markdown("- **Données insuffisantes :**""")

    st.markdown("Volumétrie faible (551 participants seulement).")
    st.markdown("Données obsolètes : Non représentatives des dynamiques actuelles de l’application.")

    st.markdown("- **Contexte inadapté :**")

    st.markdown("Les speed-datings impliquent des rencontres physiques, ce qui introduit des critères inconscients (ex: chimie, langage non verbal) non reproductibles dans un environnement digital comme Tinder.")

    st.markdown("- **Incohérences dans les données :**")

    st.markdown("Certains participants ont eu un rendez-vous sans match préalable, ce qui remet en question la fiabilité des données.")

    st.markdown("**→ Recommandations pour Tinder**")

    st.markdown("- Utiliser des données plus récentes pour refléter les tendances actuelles.")
    st.markdown("- Augmenter la volumétrie des participants pour obtenir des résultats statistiquement significatifs.")
    st.markdown("- Reproduire les conditions réelles d’utilisation de l’application (ex: études basées sur des interactions digitales plutôt que des rencontres physiques).")
    st.markdown(
    """
    - Mener des enquêtes qualitatives auprès des utilisateurs pour identifier :
        - Les critères recherchés chez un partenaire.
        - Les éléments rédhibitoires qui empêchent une rencontre après un match.
            """
    )
