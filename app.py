import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Analizator Metryk 1812 - Pełna Wersja", layout="wide")

def normalize_father_surname(name):
    if not name or name == "Brak": return name
    if name.endswith('ska'): return name[:-1] + 'i'
    if name.endswith('cka'): return name[:-1] + 'i'
    if name.endswith('dzka'): return name[:-1] + 'i'
    if name.endswith('iey'): return name[:-3] + 'y'
    if name.endswith('ey'): return name[:-2] + 'y'
    return name

def normalize_maiden_name(s):
    if not s or s == "Brak": return s
    s_lower = s.lower().strip()
    s_lower = re.sub(r'iey$|ey$', 'a', s_lower)
    s_lower = re.sub(r'ówny$|owny$|ówna$|owna$', 'ówna', s_lower)
    s_lower = re.sub(r'anki$|anka$', 'anka', s_lower)
    s_lower = re.sub(r'ionki$|ionka$|onki$|onka$', 'a', s_lower)
    s_lower = re.sub(r'ową$|owa$', 'owa', s_lower)
    return s_lower.capitalize()

st.title("🏛️ Cyfrowy Archiwista: Olkusz 1812")
st.markdown("---")


if 'full_text' not in st.session_state:
    try:
        with open('ksiega.txt', 'r', encoding='utf-8') as f:
            st.session_state['full_text'] = f.read()
            st.success("Wczytano plik ksiega.txt automatycznie.")
    except FileNotFoundError:
        uploaded_file = st.file_uploader("Nie znaleziono ksiega.txt. Wgraj go ręcznie:", type=['txt'])
        if uploaded_file:
            st.session_state['full_text'] = uploaded_file.read().decode("utf-8")

if 'full_text' in st.session_state:
    full_text = st.session_state['full_text']
    
    #podział tekstu na poszczególne akty
    acts = re.split(r'Akt nr (\d+)', full_text)
    parsed_records = []
    m_order = ['Stycznia', 'Lutego', 'Marca', 'Kwietnia', 'Maja', 'Czerwca', 'Lipca', 'Sierpnia', 'Września', 'Października', 'Listopada', 'Grudnia']

    for i in range(1, len(acts), 2):
        nr_aktu = acts[i]
        content = acts[i+1].replace('\n', ' ')
        
        #ekstrakcja danych podstawowych
        dziecko_match = re.search(r'\((.*?)\)', content)
        imie_dziecka = dziecko_match.group(1).split()[0] if dziecko_match else "Brak"
        nazwisko_dziecka = dziecko_match.group(1).split()[-1] if dziecko_match else "Brak"
        
        #rozpoznawanie płci
        if "płci Żeń" in content or "płci żeń" in content:
            plec = "Kobieta"
        elif "płci Mę" in content or "płci mę" in content or "płci Męzkiey" in content:
            plec = "Mężczyzna"
        else:
            plec = "Nieznana"

        miesiac_match = re.search(r'Miesiąca (\w+)', content, re.I)
        miesiac = miesiac_match.group(1).capitalize() if miesiac_match else "Nieznany"
        
        m_match = re.search(r'w (?:Wsi|Mieście|Przedmieściu Miasta|Przedmiesciu Miasta)\s+([\w\s]+?)\s+zamieszkał', content, re.I)
        miejscowosc_raw = m_match.group(1).strip() if m_match else "Olkusz"
        
        z_pattern = r'(półrolnik|potrolnik|pulrolnik|zagrodnik|wyrobnik|komornik|mieszczanin|obywatel|leśny|leśniczy|profesor|burmistrz|starozakonny|karczmarz|szewc|kowal|garncarz|sołtys|służący|chałupnik|tkacz|rzeźnik|majster kunsztu [\w]+)'
        zawod_match = re.search(z_pattern, content, re.I)
        zawod = zawod_match.group(1).lower() if zawod_match else "Inny/Brak"

    
        matka_block = re.search(r'(?:z Niego i|z Panny|z Wdowy|z niey|z teyże|z Matki)\s+(.*?)\s+(?:liczą|maią|mają|maiącey|liczącey|iego Małżonki|Żony|zamieszkał)', content, re.I)
        nazwisko_matki_raw = "Brak"
        if matka_block:
            m_text = re.sub(r'\b(Wdowy|Wdową|Panny|Panną|z Pławców|z)\b', '', matka_block.group(1), flags=re.I).strip()
            m_parts = m_text.split()
            if m_parts:
                potencjalne = m_parts[-2] if m_parts[-1].lower() in ['iego', 'jego'] else m_parts[-1]
                if potencjalne[0].isupper(): 
                    nazwisko_matki_raw = potencjalne

        parsed_records.append({
            "Nr": nr_aktu, "Imię": imie_dziecka,
            "Nazwisko Rodziny": normalize_father_surname(nazwisko_dziecka),
            "Płeć": plec, "Miesiąc": miesiac, 
            "Zawód": zawod.replace('potrolnik', 'półrolnik').replace('pulrolnik', 'półrolnik').replace('obywatel', 'mieszczanin'),
            "Nazwisko Matki": normalize_maiden_name(nazwisko_matki_raw),
            "Miejscowość": miejscowosc_raw
        })

    df = pd.DataFrame(parsed_records)
    loc_map = {'Olkuszu': 'Olkusz', 'Żuradzie': 'Żurada', 'Pomorzanach': 'Pomorzany', 'Kluczach': 'Klucze', 'Witeradowie': 'Witeradów', 'Ujkowie': 'Ujków', 'Bogucinie': 'Bogucin', 'Skalskie': 'Skalskie', 'Parczach': 'Parcze', 'Czarney Górze': 'Czarna Góra', 'Sikorce': 'Sikorka'}
    df['Miejscowość_Clean'] = df['Miejscowość'].replace(loc_map)
    df['Miesiąc'] = pd.Categorical(df['Miesiąc'], categories=m_order, ordered=True)

    tab1, tab2, tab3 = st.tabs(["📊 Wykresy i Metryki", "📑 Pełny Raport Liczbowy", "🔍 Przeglądarka Danych"])

    with tab1:
        c1, c2, c3 = st.columns(3)
        c1.metric("Suma aktów", len(df))
        c2.metric("Chłopcy (M)", len(df[df['Płeć'] == 'Mężczyzna']))
        c3.metric("Dziewczynki (K)", len(df[df['Płeć'] == 'Kobieta']))

        st.markdown("---")
        fig1, axes = plt.subplots(3, 2, figsize=(15, 20))
        sns.set_theme(style="whitegrid")

        sns.countplot(data=df, y='Miejscowość_Clean', order=df['Miejscowość_Clean'].value_counts().index, ax=axes[0,0], palette="Blues_r")
        axes[0,0].set_title('Miejscowości')
        axes[0,0].set_xlabel('Liczba')         
        axes[0,0].set_ylabel('Miejscowość')      

        df_z = df[df['Zawód'] != 'inny/brak']
        sns.countplot(data=df_z, y='Zawód', order=df_z['Zawód'].value_counts().index, ax=axes[0,1], palette="Greens_r")
        axes[0,1].set_title('Zawody Ojców')
        axes[0,1].set_xlabel('Liczba')           
        axes[0,1].set_ylabel('Zawód')

        df['Płeć'].value_counts().plot.pie(autopct='%1.1f%%', ax=axes[1,0], colors=['#66b3ff','#ff9999'], startangle=90)
        axes[1,0].set_title('Rozkład płci')
        axes[1,0].set_ylabel('')

        sns.lineplot(x=df['Miesiąc'].value_counts().sort_index().index, y=df['Miesiąc'].value_counts().sort_index().values, marker='o', ax=axes[1,1], color='red')
        axes[1,1].set_title('Dynamika urodzeń')
        axes[1,1].set_xlabel('Miesiąc')         
        axes[1,1].set_ylabel('Liczba urodzeń')
        plt.setp(axes[1,1].get_xticklabels(), rotation=45)

        sns.barplot(x=df['Nazwisko Rodziny'].value_counts().head(10).values, y=df['Nazwisko Rodziny'].value_counts().head(10).index, ax=axes[2,0], palette="rocket")
        axes[2,0].set_title('Top 10 Nazwisk')
        axes[2,0].set_xlabel('Liczba')          
        axes[2,0].set_ylabel('Nazwisko')

        sns.barplot(x=df[df['Nazwisko Matki'] != 'Brak']['Nazwisko Matki'].value_counts().head(10).values, y=df[df['Nazwisko Matki'] != 'Brak']['Nazwisko Matki'].value_counts().head(10).index, ax=axes[2,1], palette="Purples_r")
        axes[2,1].set_title('Top 10 Nazwisk Matek')
        axes[2,1].set_xlabel('Liczba')          
        axes[2,1].set_ylabel('Nazwisko')

        plt.tight_layout()
        st.pyplot(fig1)

    
    with tab2:
        st.header("📋 Kompletne zestawienia (bez skrótów)")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Miejscowości")
            st.write(df['Miejscowość_Clean'].value_counts())
            
            st.subheader("Zawody")
            st.write(df['Zawód'].value_counts())
            
            st.subheader("Dynamika (Miesiące)")
            st.write(df['Miesiąc'].value_counts().sort_index())

        with col_b:
            st.subheader("Wszystkie nazwiska rodzinne")
            st.write(df['Nazwisko Rodziny'].value_counts().sort_index())
            
            st.subheader("Wszystkie nazwiska matek")
            st.write(df[df['Nazwisko Matki'] != 'Brak']['Nazwisko Matki'].value_counts().sort_index())

        st.subheader("Wszystkie imiona dzieci")
        st.write(df['Imię'].value_counts())

    with tab3:
        st.header("🔎 Wyszukiwarka i filtrowanie")
        filter_name = st.text_input("Szukaj nazwiska w bazie:")
        if filter_name:
            res = df[df['Nazwisko Rodziny'].str.contains(filter_name, case=False) | df['Nazwisko Matki'].str.contains(filter_name, case=False)]
            st.dataframe(res, use_container_width=True)
        else:
            st.dataframe(df, use_container_width=True)
else:
    st.warning("Oczekiwanie na dane... Upewnij się, że plik ksiega.txt jest w folderze projektu.")