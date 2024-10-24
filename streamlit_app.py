import streamlit as st
import time
import mysql.connector
import pandas as pd
import plotly.express as px
from mysql.connector import Error
from datetime import datetime, timedelta

st.title("Performance Dashboard de Lunaria")

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host="193.34.79.27",
            port="3306",
            user="u17876_kLxmOC09WT",  
            password="Ri=liN0b@bh0W0CW=DkuM6YN",  
            database="s17876_DTB"  
        )
        if connection.is_connected():
            st.success("Connexion à la base de données réussie")
            return connection
    except Error as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")
        return None

if 'loading_done' not in st.session_state:
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        with st.spinner('Chargement en cours...'):
            progress_bar = st.progress(0)
            steps = [{"name": "Étape 1 : Connexion à la base de données", "duration": 3},
                     {"name": "Étape 2 : Analyse des données", "duration": 2},
                     {"name": "Étape 3 : Initialisation des graphiques", "duration": 2},
                     {"name": "Étape 4 : Finalisation", "duration": 1}]
            for i, step in enumerate(steps):
                st.write(step["name"])
                for percent_complete in range(100 // len(steps)):
                    time.sleep(step["duration"] / (100 // len(steps)))
                    progress_bar.progress(i * (100 // len(steps)) + percent_complete + 1)
            db_connection = create_db_connection()
        loading_placeholder.empty()
        st.session_state['loading_done'] = True
else:
    db_connection = create_db_connection()

st.success('Chargement terminé !')

st.sidebar.header("Gérer les paramètres")
with st.sidebar:
    data_type = st.selectbox("Sélectionnez le type de données à afficher", options=["CPU", "RAM"])
    heures = st.sidebar.number_input("Heures", min_value=0, max_value=23, value=0)
    jours = st.sidebar.number_input("Jours", min_value=0, max_value=30, value=0)
    mois = st.sidebar.number_input("Mois", min_value=0, max_value=12, value=0)
    annees = st.sidebar.number_input("Années", min_value=0, value=0)
    apply_button = st.sidebar.button("Appliquer")
    average_button = st.sidebar.button("Afficher l'utilisation moyenne")

def get_time_filter(hours, days, months, years):
    return datetime.now() - timedelta(hours=hours, days=days) - timedelta(days=months*30) - timedelta(days=years*365)

if db_connection is not None and apply_button:
    st.header(f"Données {data_type}")
    try:
        start_time = get_time_filter(heures, jours, mois, annees)
        query = f"SELECT time, {'charge' if data_type == 'CPU' else 'usage'} FROM {data_type.lower()} WHERE time >= '{start_time}' ORDER BY time ASC;"
        data = pd.read_sql(query, db_connection)
        if not data.empty:
            fig = px.line(data, x='time', y=('charge' if data_type == "CPU" else 'usage'), title=f"Utilisation du {data_type} pour les {heures} heures, {jours} jours, {mois} mois, {annees} années")
            st.plotly_chart(fig)
        else:
            st.write(f"Aucune donnée disponible pour la période sélectionnée concernant {data_type}.")
    except Error as e:
        st.error(f"Erreur lors de l'exécution de la requête : {e}")

# Function to calculate and display average usage
if db_connection is not None and average_button:
    st.header(f"Utilisation moyenne de {data_type}")
    try:
        query_avg = f"SELECT AVG({'charge' if data_type == 'CPU' else 'usage'}) AS average_usage FROM {data_type.lower()};"
        avg_data = pd.read_sql(query_avg, db_connection)
        if not avg_data.empty:
            average_value = avg_data['average_usage'].values[0]
            avg_fig = px.pie(names=[f"Utilisation Moyenne {data_type}"], values=[average_value], title=f"Utilisation Moyenne de {data_type}")
            st.plotly_chart(avg_fig)
        else:
            st.write(f"Aucune donnée disponible pour le calcul de l'utilisation moyenne concernant {data_type}.")
    except Error as e:
        st.error(f"Erreur lors de l'exécution de la requête pour la moyenne : {e}")
    finally:
        db_connection.close()
