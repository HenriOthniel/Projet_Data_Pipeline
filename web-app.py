# Importer les modules nécessaires
import streamlit as st
import pandas as pd
import os
import subprocess

# Définir le chemin vers le dossier samples
samples_path = "./samples/"
aggragat = "./"

# Créer le dossier samples s'il n'existe pas
if not os.path.exists(samples_path):
    os.makedirs(samples_path)
    
tab1, tab2, tab3 = st.tabs(["Chargement des fichiers", "Resultats", "Leaderboard"])

# Si l'onglet Upload est sélectionné
with tab1 :
    # Afficher un titre
    st.title("Chargement des fichiers")

    # Afficher un message d'instruction
    st.write("Veuillez télécharger les fichiers messages.csv et users.csv")

    # Créer deux widgets pour télécharger les fichiers CSV
    messages_file = st.file_uploader("Télécharger le fichier messages.csv", type="csv")
    users_file = st.file_uploader("Télécharger le fichier users.csv", type="csv")      
    
    if messages_file and users_file:
        # Enregistrer les fichiers dans le dossier samples
        messages_path = os.path.join(samples_path, "messages.csv")
        users_path = os.path.join(samples_path, "users.csv")
        aggragate_data_path = os.path.join(aggragat, "aggregate_d.py")
        with open(messages_path, "wb") as f:
            f.write(messages_file.getbuffer())
        with open(users_path, "wb") as f:
            f.write(users_file.getbuffer())
            
        
        if messages_file.name == "messages.csv" and users_file.name == "users.csv":
            # Afficher un message de confirmation
            st.success("Les fichiers ont été téléchargés avec succès.")

            # Appeler la fonction aggregate_data.py avec les chemins des fichiers CSV et le chemin du résultat
            output_path = os.path.join(samples_path)
            # aggragation = r"C:/Users/DELL/Documents/Master/API_Docker_Cloud/tp_data_pipeline/aggregate_data.py"
            os.system(f"python {aggragate_data_path} {messages_path} {users_path} {output_path}")

            # # Exécuter le script my_script.py
            # subprocess.run(["python ", "C:/Users/DELL/Documents/Master/API_Docker_Cloud/tp_data_pipeline/aggregate_data.py", messages_path, users_path, output_path])

            # Afficher un message de succès
            st.success("Le fichier pipeline_result.csv a été créé avec succès.")
        
        else:
            st.warning("Les fichiers sont mal chargés ou mal renseignés. REESAYER!!!")
    
    # else:
    #     st.warning("Chargez les fichiers.")
        

# Si l'onglet Classement est sélectionné
with tab2:
    # Afficher un titre
    st.title("Resultats")
    
    # Afficher un message d'instruction
    if messages_file is None and users_file is None:
        st.write("Veuillez vérifier que vous avez téléchargé les fichiers messages.csv et users.csv dans l'onglet Chargement")

    elif messages_file != 'messages.csv' and users_file != 'users.csv':
    # Charger le fichier pipeline_result.csv dans un dataframe
        output_path = os.path.join(samples_path, "pipeline_result.csv")
        try:
            result_df = pd.read_csv(output_path)
        except:
            st.error("Erreur lors du chargement du fichier pipeline_result.csv. Vérifiez que vous avez téléchargé les fichiers messages.csv et users.csv dans l'onglet Upload.")
            result_df = None

        # Si le dataframe n'est pas vide, afficher le tableau sous forme de tableau
        if result_df is not None:
            st.dataframe(result_df)

with tab3:
    st.title('Leaderboard')
    