import streamlit as st
import pandas as pd
from datetime import date
import datetime
import time


def maj_db(df):
   for index,row in df.iterrows():
        
        str_heure = row["heure"].split(":")
        
        
        if row["date"].day<=date.today().day and row["date"].month<=date.today().month and row["date"].year<=date.today().year and int(str_heure[0])<=datetime.datetime.now().hour and int(str_heure[1])<datetime.datetime.now().minute:
            df.at[index,"status"] = "fini"
        else:
            df.at[index,"nombre de place restante"] = row["nombre de place total"] - len(row["personnes"].split(";"))+1
            if row["nombre de place restante"] <= 0:
                df.at[index,"status"] = "complet"
            else:
                df.at[index,"status"] = "en cours"
        df.to_excel("autre.xlsx",index=False)

def html(body):
    st.markdown(body, unsafe_allow_html=True)

def card_begin_str(header):
    return (
        "<style>div.card{padding: 5px 20px 5px 10px;background-color:white;border-radius: 5px;box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);transition: 0.3s;}</style>"
        '<div class="card">'
        '<div class="container">'
        f"<h3><b>{header}</b></h3>"
    )

def card_end_str():
    return "</div></div>"

def br(n):
    html(n * "<br>")

def card(header, body):
    lines = [card_begin_str(header), f"<p>{body}</p>", card_end_str()]
    html("".join(lines))

def main():
    
    id_ref = 0
    df = pd.read_excel("autre.xlsx")
    
    maj_db(df)
    
    st.write("<h1>Takwira toulouse ⚽<h1/>",unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Amel talla al takwirat elli mawjoudin","Nathem takwira jdida"])
    with tab2:
        with st.form("ajouter_match_form"):
            st.write("Bellehi hot les détails mta takwira")
            adresse = st.text_input("Win?")
            date = st.date_input("Ana nhar?")
            heure = st.time_input("M3a ana wakt?")
            nombre_de_place = st.number_input("Kadeh men wehed bech tkawrou?",min_value=1, max_value=24)
            nom = st.text_input("Esmek haboub")
            
            submitted = st.form_submit_button("Enzel bch tconfirmi bro")

        if submitted:
            if (len(nom) == 0 or len(adresse) == 0 ):
                st.error("Kamel hot les détails el kol w yezi mel bleda")
            else:
                st.success("Tbarkallah alik araft tamer formulaire, koul l shabek yjiw yzidou asamihom taw")
                time.sleep(2)

                liste_adresse = df["adresse"].to_list()
                liste_date = df["date"].to_list()
                liste_heure = df["heure"].to_list()
                liste_nombre_de_place_total = df["nombre de place total"].to_list()
                liste_nombre_de_place_restante = df["nombre de place restante"].to_list()
                liste_status = df["status"].to_list()
                liste_id = df["id"].to_list()
                liste_presonne = df["personnes"].to_list()
                
                
                liste_presonne.append(nom+";")
                liste_adresse.append(adresse)
                liste_date.append(date)
                liste_heure.append(heure)
                liste_nombre_de_place_total.append(nombre_de_place)
                liste_nombre_de_place_restante.append(nombre_de_place-1)
                liste_status.append("en cours")

                if len(liste_id) == 0:
                    liste_id.append(id_ref)
                else:
                    liste_id.append(liste_id[-1]+1)
                new_df = pd.DataFrame({
                                        "adresse":liste_adresse,
                                        "date":liste_date,
                                        "heure":liste_heure,
                                        "nombre de place total":liste_nombre_de_place_total,
                                        "nombre de place restante":liste_nombre_de_place_restante,
                                        "status":liste_status,
                                        "id":liste_id,
                                        "personnes":liste_presonne,
                                        
                                    })
                
                new_df.to_excel("autre.xlsx",index=False)
                
    with tab1:
        st.write("<h2>Liste takwirat en cours ⏳</h2>",unsafe_allow_html=True)
        st.markdown("""---""") 
        df = pd.read_excel("autre.xlsx")
        flag = True
        for index,row in df.iterrows():
            if row["status"] == "en cours":
                flag = False
                with st.form("Nheb nkawer"+str(row["id"])):
                    str_personnes = ""
                    for personne in row["personnes"].split(";"):
                        str_personnes = str_personnes + personne + "    "
                    st.write("Takwira nathamha si "+ row["personnes"].split(";")[0])
                    st.write("Date : " + str(row["date"]))
                    st.write("El wakt : "  + str(row["heure"]))
                    st.write("El blasa : " + str(row["adresse"]))
                    st.write("Laabed elli bch tkawer : " + str_personnes)
                    st.write("Mezelou " + str(row["nombre de place restante"]) + " blayes")
                    nom = st.text_input("Ekteb esmek ken theb tkawer",disabled=(row["nombre de place restante"]<=0))
                    ajouter = st.form_submit_button("Enzel houni ken theb tzid esmek fel lista",disabled=(row["nombre de place restante"]<=0))
                    if ajouter:
                        df.at[index,"personnes"] = row["personnes"] + nom + ";"
                        df.to_excel("autre.xlsx",index=False)
                        st.experimental_rerun()
                
                st.markdown("""---""")    
        if flag:
            st.error("Mafama hata match en cours pour le moment")    
            st.markdown("""---""")        
                    


        st.write("<h2>Liste takwirat eli complet ✔️</h2>",unsafe_allow_html=True)
        st.markdown("""---""") 
        flag2 = True
        for index,row in df.iterrows():
            if row["status"] == "complet":
                flag2 = False
                str_personnes = ""
                for personne in row["personnes"].split(";"):
                    str_personnes = str_personnes + personne + "    "
                    
                
                body = "Date : " + str(row["date"]) + " <br />El wakt : "  + str(row["heure"] + "<br /> El blasa : " + str(row["adresse"]) + "<br /> Laabed elli bch talaab : " + str_personnes)
                
                card("Takwira nathamha si "+ row["personnes"].split(";")[0],body)
                
                st.markdown("""---""")  
        if flag2:
            st.error("Mafama hata match complet pour le moment") 
            st.markdown("""---""")    
                
                
        

             
        

main()



