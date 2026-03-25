# 🏛️ Cyfrowy Archiwista: Olkusz 1812 (Text Data Exploration)

Celem projektu było przeprowadzenie pełnego procesu eksploracji danych tekstowych (EDT) na podstawie historycznych aktów urodzenia z Parafii Olkusz z roku 1812[cite: 3]. [cite_start]Projekt przetwarza surowe skany dokumentów z Archiwów Państwowych, wykorzystując techniki rozpoznawania tekstu (OCR), zaawansowane przetwarzanie języka naturalnego (NLP) oraz wizualizację statystyczną[cite: 3, 4].

[cite_start]Projekt został zrealizowany przez Aleksandrę Orzech oraz Milanę Lukasiuk w ramach przedmiotu Eksploracja Danych Tekstowych na kierunku Data Science[cite: 1].

## 🛠️ Technologie i Narzędzia
* **Język:** Python
* **Frontend / Interfejs:** Streamlit [cite: 326]
* **Przetwarzanie Danych:** Pandas, Regex (Wyrażenia regularne) [cite: 119, 339]
* **NLP:** spaCy (`pl_core_news_sm`) [cite: 108]
* **Wizualizacja:** Seaborn, Matplotlib [cite: 147]
* **OCR:** Transkribus (Model: *Transkribus Polish M2*) [cite: 59, 63]

## 🚀 Główne funkcjonalności i etapy projektu

### 1. Rozpoznawanie tekstu (OCR)
Surowe skany poddano automatycznej transkrypcji na platformie Transkribus. [cite_start]Zastosowano dedykowany model *Transkribus Polish M2*, specjalizujący się w polskim piśmie ręcznym z okresu XVII-XXI wieku. Model ten osiągnął bardzo wysoką dokładność (CER na poziomie 4.10%).

### 2. Zaawansowany Preprocessing i Ekstrakcja Danych (Regex)
Kluczowym etapem przetwarzania dokumentów było wyodrębnienie poszczególnych rekordów za pomocą wyrażeń regularnych (Regex). 
* Zaimplementowano skomplikowane reguły do normalizacji archaicznych nazwisk żeńskich (np. usuwanie końcówek *-iey*, *-ówny*, *-ową*).
* Ujednolicono nazwiska ojców i dzieci do formy męskiej/rodzinnej.
* Wprowadzono słownik mapujący archaiczne i odmienione formy miejscowości (toponimów) do mianownika.

### 3. Przetwarzanie Języka Naturalnego (NLP)
Do analizy struktury zawodowej wykorzystano bibliotekę spaCy[cite: 108]. [cite_start]Zawody występujące w aktach w formie narzędnika (np. "mieszczaninem") poddano procesowi lematyzacji, sprowadzając je automatycznie do formy podstawowej ("mieszczanin").

### 4. Interaktywny Dashboard (Streamlit)
W celu prezentacji wyników analizy stworzono aplikację webową z wykorzystaniem frameworka Streamlit[cite: 326]. Aplikacja dzieli się na trzy zakładki:
1. **Wykresy i Metryki:** Prezentuje kluczowe wskaźniki (np. podział na płeć) oraz generuje wykresy struktury zawodowej, terytorialnej i dynamiki urodzeń.
2. **Pełny Raport Liczbowy:** Wyświetla surowe dane statystyczne i zestawienia Pandas.
3. **Przeglądarka Danych:** Umożliwia dynamiczne filtrowanie bazy po nazwiskach.

## 💻 Jak uruchomić projekt lokalnie?

1. Sklonuj to repozytorium na swój dysk.
2. Zainstaluj wymagane biblioteki poleceniem:
   ```bash
   pip install -r requirements.txt
