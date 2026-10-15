# Who Speaks, and About What? — Turkish Parliament Speech Analysis (2023–2026)

**STAT 401 Big Data — Final Project · Middle East Technical University · June 2026**

Başak Uğurlu · Zeynep Fenercioğlu · Damla Başarmış

---

## In Plain Words

Every session of the Turkish Grand National Assembly (TBMM) is written down word for word and published online. These transcripts are long blocks of text, so it is hard to answer simple questions from them, such as:

- Which party talks the most?
- Which MPs and provinces are most active?
- What does each party talk about?
- When is parliament busiest?

This project collects those transcripts, splits them into **~196,000 individual speeches**, labels each one with the speaker's party and province, and analyses them. The results are shown in an **interactive dashboard** you can open in your browser.

---

## Key Findings

| Question | Answer |
|---|---|
| Most active party | **CHP** — 36,711 speeches, 2.2M words |
| Shortest speeches | **AKP** — many speeches, but ~42 words on average |
| Most active MPs | Ali Mahir Başarır, Gökhan Günaydın, Gülistan Kılıç Koçyiğit |
| Most active provinces | İstanbul, Ankara, Mersin (Kars ranks high because of one very active MP) |
| Most discussed theme | **Economy** (8,443 speeches), then education, health, agriculture, earthquake |
| Busiest month | **December** every year (budget debates); August–September are almost silent (recess) |
| Busiest single month | December 2025 — 17,652 speeches |

**What parties talk about**

- **CHP:** health, retirees, municipalities, minimum wage, tax, agriculture
- **DEM Party:** identity, democratic rights, peace, women, trustees (kayyum)
- **MHP:** nationalist vocabulary — Turkish, national, nation, movement
- **Provinces:** Hatay → earthquake; Van and Diyarbakır → Kurdish identity; Şanlıurfa → electricity and agriculture

> Full details, charts and discussion are in [`Project Report.pdf`](Project%20Report.pdf).

---

## How It Works

```
TBMM website ──► 1. Scrape ──► 2. Split into speeches ──► 3. Add party & province ──► 4. Clean final table ──► 5. Analyse (PySpark) ──► 6. Dashboard
```

| Step | Notebook / file | What it does | Output |
|---|---|---|---|
| 1 | `tbmm_scraping_23_28.ipynb` | Downloads raw session transcripts (terms 23–28) from the TBMM website | 342 sessions for the 28th term, one row each |
| 2 | `28_donem_konusma_bazli_creation.ipynb` | Splits each session into individual speeches with regex; removes headings and procedural lines | 199,158 speeches |
| 3 | `milletvekili_sehir_parti_lookup_table.ipynb` | Builds an MP → party & province lookup from the TBMM MP directory | 599 MPs |
| 4 | `tbmm_konusma_final_table.ipynb` | Merges speeches with the lookup, fixes encoding, standardises party names, classifies speaker types | 196,442 rows × 18 columns |
| 5 | `tbmm_analiz_son.ipynb` | Runs the analysis with Apache Spark (PySpark) | Statistics, keyword lists, charts |
| 6 | `interactive_tbmm_dashboard.py` | Streamlit + Plotly dashboard of the results | Interactive web app |

---

## Repository Structure

```
├── README.md
├── LICENSE
├── .gitignore
├── Project Report.pdf                  # Full written report
├── interactive_tbmm_dashboard.py        # Step 6 — dashboard
├── requirements.txt                     # Dashboard dependencies
└── Source Codes/
    ├── tbmm_scraping_23_28.ipynb                   # Step 1
    ├── 28_donem_konusma_bazli_creation.ipynb       # Step 2
    ├── milletvekili_sehir_parti_lookup_table.ipynb # Step 3
    ├── tbmm_konusma_final_table.ipynb              # Step 4
    └── tbmm_analiz_son.ipynb                       # Step 5
```

> **Data is not included.** The scraped transcripts and generated CSV / Parquet files are excluded from this repository. They can be recreated by running the notebooks in order (see below). The processed dataset is available on request.

---

## Run the Dashboard

The dashboard is **self-contained**: results from the analysis are built into the script, so no data files are needed.

```bash
pip install -r requirements.txt
streamlit run interactive_tbmm_dashboard.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).

### Dashboard Tabs

1. Dataset Overview
2. Party-Based Speech Statistics
3. Party Speech Trends by Legislative Year
4. Top 20 Most Active MPs
5. Top 20 Most Active Provinces
6. Party-Based Top Keywords
7. Normalized Province-Level Keyword Analysis
8. Topic-Based Speech Analysis
9. Monthly Speech Activity Timeline

All charts support hover, filtering and zooming.

---

## Reproduce the Pipeline

### Environment

- The notebooks were written for **Google Colab** and save files to **Google Drive** (`/content/drive/MyDrive/tbmm_raw_tutanaklar/`).
- To run locally, remove the `drive.mount(...)` cells and change the paths to a local folder.
- Main libraries: `requests`, `beautifulsoup4`, `pandas`, `pyarrow`, `numpy`, `matplotlib`, `seaborn`, `pyspark` (4.0.2)

### Order

Run the notebooks in steps 1 → 5. Each notebook reads the file created by the previous one:

| File | Created by | Used by |
|---|---|---|
| `raw_tutanaklar_28_clean.csv` | Step 1 | Step 2 |
| `tutanaklar_28_konusmaci_bazli.csv` | Step 2 | Steps 3, 4 |
| `milletvekili_party_city_lookup.csv` | Step 3 | Step 4 |
| `donem28_konusmaci_bazli.csv` | Step 4 | Step 5 |

Step 3 also needs `milletvekili_party_info.xlsx`, compiled from the [TBMM MP directory](https://tbmm.gov.tr/milletvekili-arama/form).

### Responsible Scraping

The scraper is single-threaded, identifies itself with a descriptive user agent, waits between requests, retries with backoff, and skips sessions already saved. No proxies, IP rotation or CAPTCHA bypassing were used.

---

## Methods (Technical Summary)

- **Parsing:** regex detection of speaker openings (MP name + province, `BAŞKAN`, group speeches, `(Devamla)` continuations); removal of headers, table-of-contents and procedural lines
- **Enrichment:** normalised name keys, Turkish character handling, city aliases, party standardisation, manual patch for MPs who left office during the term
- **Speaker types:** province left empty for institutional roles (chair, minister, president, committee)
- **Analysis (PySpark):** `groupBy` / `agg` aggregations for speech count, total words and average length by party, MP, province, year and month
- **Text mining:** Turkish-aware cleaning, custom stop-word list (grammar particles, parliamentary protocol words, transcript artefacts)
- **Province keywords:** normalised per 10,000 words, so large provinces don't win automatically
- **Themes:** keyword-based filtering for economy, education, health, agriculture and earthquake

---

## Limitations & Next Steps

- Covers the **28th term only**; the 4th legislative year was incomplete at collection time
- Themes use keyword lists, not learned topics
- Possible extensions: parse terms 23–27, topic modelling (LDA, NMF, BERTopic), sentiment / stance analysis, named-entity recognition

---

## Team

| Member | Main contribution |
|---|---|
| Başak Uğurlu | Data collection & preprocessing — scraper, raw session table, speech-level parsing, MP lookup table, final dataset |
| Zeynep Fenercioğlu | PySpark analysis, interpretation, dashboard design & visualisation |
| Damla Başarmış | PySpark analysis, interpretation, dashboard design & visualisation |

---

## Data Source

- [TBMM Plenary Transcripts (Tutanak Metinleri)](https://tbmm.gov.tr/Tutanaklar/Tutanak-Sorgu-Sonuclari)
- [TBMM MP Directory](https://tbmm.gov.tr/milletvekili-arama/form)

Transcripts are public records published by the Grand National Assembly of Türkiye. This project is for academic purposes.

---

## License

The code in this repository is released under the [MIT License](LICENSE).
