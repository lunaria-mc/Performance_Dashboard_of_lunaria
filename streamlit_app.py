import streamlit as st
import time

# DB CONNEXION
conn = st.connection('mysql', type='sql')

# Titre de la page principale
st.title("Performance Dashboard de Lunaria")

# Placeholder pour l'écran de chargement
loading_placeholder = st.empty()

# Utiliser un conteneur pour afficher l'écran de chargement
with loading_placeholder.container():
    with st.spinner('Chargement en cours...'):
        progress_bar = st.progress(0)

        # Définir les étapes du chargement
        steps = [
            {"name": "Étape 1 : Connexion à la base de données", "duration": 2},
            {"name": "Étape 2 : Analyse des données", "duration": 3},
            {"name": "Étape 3 : Initialisation des graphiques", "duration": 2},
            {"name": "Étape 4 : Finalisation", "duration": 1}
        ]

        total_steps = len(steps)
        progress_per_step = 100 // total_steps

        # Boucle sur chaque étape
        for i, step in enumerate(steps):
            st.write(step["name"])  # Afficher le nom de l'étape
            for percent_complete in range(progress_per_step):
                time.sleep(step["duration"] / progress_per_step)  # Simuler la durée de l'étape
                progress_bar.progress(i * progress_per_step + percent_complete + 1)

# Une fois le chargement terminé, effacer l'écran de chargement
loading_placeholder.empty()

# Afficher un message de succès à la fin du chargement
st.success('Chargement terminé !')

# Afficher le contenu principal de la page après le chargement
st.header("Bienvenue sur les dashboards de performance de Lunaria")

# Ajouter la barre latérale une fois le chargement terminé
st.sidebar.header("Gerer les paramètres")
with st.sidebar:
    dure = st.sidebar.selectbox(
        "Choisissez une durée",
        ["1 jour","2 jours","3 jours","4 jours","5 jours","6 jours","1 semaine","1 mois","1 ans"],
    )

