# 🏛️ Cyfrowy Archiwista: Olkusz 1812 (Text Data Exploration)

[cite_start]Celem projektu było przeprowadzenie pełnego procesu eksploracji danych tekstowych (EDT) na podstawie historycznych aktów urodzenia z Parafii Olkusz z roku 1812[cite: 3]. [cite_start]Projekt przetwarza surowe skany dokumentów z Archiwów Państwowych, wykorzystując techniki rozpoznawania tekstu (OCR), zaawansowane przetwarzanie języka naturalnego (NLP) oraz wizualizację statystyczną[cite: 3, 4].

[cite_start]Projekt został zrealizowany przez Aleksandrę Orzech oraz Milanę Lukasiuk w ramach przedmiotu Eksploracja Danych Tekstowych na kierunku Data Science[cite: 1].

## 🛠️ Technologie i Narzędzia
* **Język:** Python
* [cite_start]**Frontend / Interfejs:** Streamlit [cite: 326]
* [cite_start]**Przetwarzanie Danych:** Pandas, Regex (Wyrażenia regularne) [cite: 119, 339]
* [cite_start]**NLP:** spaCy (`pl_core_news_sm`) [cite: 108]
* [cite_start]**Wizualizacja:** Seaborn, Matplotlib [cite: 147]
* [cite_start]**OCR:** Transkribus (Model: *Transkribus Polish M2*) [cite: 59, 63]

## 🚀 Główne funkcjonalności i etapy projektu

### 1. Rozpoznawanie tekstu (OCR)
[cite_start]Surowe skany poddano automatycznej transkrypcji na platformie Transkribus[cite: 59]. [cite_start]Zastosowano dedykowany model *Transkribus Polish M2*, specjalizujący się w polskim piśmie ręcznym z okresu XVII-XXI wieku[cite: 63, 64]. [cite_start]Model ten osiągnął bardzo wysoką dokładność (CER na poziomie 4.10%)[cite: 65].

### 2. Zaawansowany Preprocessing i Ekstrakcja Danych (Regex)
[cite_start]Kluczowym etapem przetwarzania dokumentów było wyodrębnienie poszczególnych rekordów za pomocą wyrażeń regularnych (Regex)[cite: 118, 119]. 
* [cite_start]Zaimplementowano skomplikowane reguły do normalizacji archaicznych nazwisk żeńskich (np. usuwanie końcówek *-iey*, *-ówny*, *-ową*)[cite: 78, 81, 83, 85].
* [cite_start]Ujednolicono nazwiska ojców i dzieci do formy męskiej/rodzinnej[cite: 98].
* [cite_start]Wprowadzono słownik mapujący archaiczne i odmienione formy miejscowości (toponimów) do mianownika[cite: 142, 143].

### 3. Przetwarzanie Języka Naturalnego (NLP)
[cite_start]Do analizy struktury zawodowej wykorzystano bibliotekę spaCy[cite: 108]. [cite_start]Zawody występujące w aktach w formie narzędnika (np. "mieszczaninem") poddano procesowi lematyzacji, sprowadzając je automatycznie do formy podstawowej ("mieszczanin")[cite: 111, 112, 113].

### 4. Interaktywny Dashboard (Streamlit)
[cite_start]W celu prezentacji wyników analizy stworzono aplikację webową z wykorzystaniem frameworka Streamlit[cite: 326]. Aplikacja dzieli się na trzy zakładki:
1. [cite_start]**Wykresy i Metryki:** Prezentuje kluczowe wskaźniki (np. podział na płeć) oraz generuje wykresy struktury zawodowej, terytorialnej i dynamiki urodzeń[cite: 335, 337].
2. [cite_start]**Pełny Raport Liczbowy:** Wyświetla surowe dane statystyczne i zestawienia Pandas[cite: 338, 339].
3. [cite_start]**Przeglądarka Danych:** Umożliwia dynamiczne filtrowanie bazy po nazwiskach[cite: 341].

## 💻 Jak uruchomić projekt lokalnie?

1. Sklonuj to repozytorium na swój dysk.
2. Zainstaluj wymagane biblioteki poleceniem:
   ```bash
   pip install -r requirements.txt
