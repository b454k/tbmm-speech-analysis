# -*- coding: utf-8 -*-
"""
Interactive Streamlit dashboard for the TBMM 28th Legislative Term speech analysis.

"""

from __future__ import annotations

import calendar
from typing import Iterable

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


COLORS = {
    "page": "#F3F5F7",
    "card": "#FFFFFF",
    "navy": "#132238",
    "blue": "#2457A7",
    "cyan": "#3B82C4",
    "teal": "#2A9D8F",
    "gold": "#E3A72F",
    "coral": "#E76F51",
    "text": "#1B2533",
    "muted": "#6D7785",
    "line": "#DDE3EA",
    "grid": "#E8EDF2",
}

PARTY_COLORS = {
    "CHP": "#D84A4A",
    "AKP": "#E29A24",
    "DEM": "#8B5BB5",
    "MHP": "#C9682A",
    "İYİ PARTİ": "#3E78C5",
    "YENİ YOL": "#35A56A",
    "TİP": "#B83B4B",
    "YENİDEN REFAH": "#697586",
    "EMEP": "#24998D",
    "SAADET": "#278A57",
    "DSP": "#2F6FA3",
    "BAĞIMSIZ": "#8E99A7",
    "HÜDA PAR": "#7450A7",
    "DP": "#B85D25",
    "DBP": "#25887D",
}

THEME_COLORS = {
    "Deprem": "#D95757",
    "Eğitim": "#3E78C5",
    "Ekonomi": "#E0A12A",
    "Sağlık": "#35A56A",
    "Tarım": "#8B5BB5",
}

PLOTLY_CONFIG = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}


@st.cache_data
def load_dashboard_data() -> dict[str, pd.DataFrame]:
    """Create DataFrames from the hardcoded PDF dashboard data."""

    # Page 2: Party-based speech statistics.
    party_order = [
        "CHP",
        "AKP",
        "DEM",
        "İYİ PARTİ",
        "YENİ YOL",
        "MHP",
        "TİP",
        "YENİDEN REFAH",
        "EMEP",
        "SAADET",
        "DSP",
        "BAĞIMSIZ",
        "HÜDA PAR",
        "DP",
        "DBP",
    ]
    party_stats = pd.DataFrame(
        {
            "party": party_order,
            "speech_count": [
                36711,
                34784,
                20111,
                10002,
                7601,
                2560,
                360,
                267,
                229,
                190,
                184,
                171,
                125,
                93,
                15,
            ],
            "total_words": [
                2225464,
                1464891,
                1292541,
                911307,
                819486,
                283640,
                18696,
                37707,
                20844,
                18323,
                28459,
                15324,
                15303,
                21244,
                3301,
            ],
            "average_words": [
                60.6,
                42.1,
                64.3,
                91.1,
                107.8,
                110.8,
                51.9,
                141.2,
                91.0,
                96.4,
                154.7,
                89.6,
                122.4,
                228.4,
                220.1,
            ],
        }
    )

    # Page 3: Party speech and word trends by legislative year.
    years = [1, 2, 3, 4]
    speech_trends = {
        "CHP": [1062, 11745, 12502, 11402],
        "AKP": [926, 14177, 11246, 8435],
        "DEM": [396, 8837, 5983, 4895],
        "İYİ PARTİ": [299, 2797, 3741, 3165],
        "YENİ YOL": [68, 2424, 2778, 2331],
        "MHP": [117, 1199, 682, 562],
    }
    word_trends = {
        "CHP": [70424, 760333, 780028, 614679],
        "AKP": [47493, 584765, 477743, 354890],
        "DEM": [34117, 474766, 437034, 346624],
        "İYİ PARTİ": [26635, 253005, 362530, 269137],
        "YENİ YOL": [10153, 223636, 302886, 282811],
        "MHP": [8530, 95441, 93597, 86072],
    }
    trends_rows = []
    for party, values in speech_trends.items():
        for year, speech_count, total_words in zip(years, values, word_trends[party]):
            trends_rows.append(
                {
                    "party": party,
                    "legislative_year": year,
                    "speech_count": speech_count,
                    "total_words": total_words,
                }
            )
    trends = pd.DataFrame(trends_rows)

    # Page 4: Top 20 most active MPs and party distribution among them.
    top_mps = pd.DataFrame(
        [
            ("ALİ MAHİR BAŞARIR", "CHP", "Mersin", 5260, 179435),
            ("GÖKHAN GÜNAYDIN", "CHP", "İstanbul", 3723, 139943),
            ("GÜLÜSTAN KILIÇ KOÇYİĞİT", "DEM", "Kars", 3629, 200255),
            ("ÖZLEM ZENGİN", "AKP", "İstanbul", 2963, 100560),
            ("LEYLA ŞAHİN USTA", "AKP", "Ankara", 2854, 89393),
            ("M. EMİN AKBAŞOĞLU", "AKP", "Çankırı", 2819, 91986),
            ("MURAT EMİR", "CHP", "Ankara", 2423, 127403),
            ("BÜLENT KAYA", "YENİ YOL", "İstanbul", 2288, 145747),
            ("SEZAİ TEMELLİ", "DEM", "Muş", 2282, 151518),
            ("Y.S. TÜRKOĞLU", "İYİ PARTİ", "Bursa", 2015, 82816),
            ("TURHAN ÇÖMEZ", "İYİ PARTİ", "Balıkesir", 1928, 168675),
            ("SELÇUK ÖZDAĞ", "YENİ YOL", "Muğla", 1608, 179339),
            ("M. DANIŞ BEŞTAŞ", "DEM", "Erzurum", 1509, 62211),
            ("VELİ AĞBABA", "CHP", "Malatya", 1498, 53791),
            ("MAHMUT TANAL", "CHP", "Şanlıurfa", 1376, 30123),
            ("CAVİT ARI", "CHP", "Antalya", 1121, 24900),
            ("Ö.F. GERGERLİOĞLU", "DEM", "Kocaeli", 1094, 52566),
            ("ÖMER FETHİ GÜRER", "CHP", "Niğde", 1075, 49991),
            ("ADEM YILDIRIM", "AKP", "İstanbul", 1074, 16632),
            ("OSMAN GÖKÇEK", "AKP", "Ankara", 1057, 13968),
        ],
        columns=["mp", "party", "province", "speech_count", "total_words"],
    )
    top_mps.insert(0, "rank", range(1, len(top_mps) + 1))

    # Page 5: Top 20 most active provinces.
    provinces = pd.DataFrame(
        {
            "province": [
                "İstanbul",
                "Ankara",
                "Mersin",
                "Kars",
                "Bursa",
                "İzmir",
                "Antalya",
                "Balıkesir",
                "Çankırı",
                "Şanlıurfa",
                "Kocaeli",
                "Manisa",
                "Muş",
                "Muğla",
                "Erzurum",
                "Gaziantep",
                "Hatay",
                "Mardin",
                "Konya",
                "Adana",
            ],
            "speech_count": [
                19183,
                9603,
                7856,
                4316,
                3777,
                3478,
                3065,
                2971,
                2829,
                2667,
                2612,
                2361,
                2295,
                2194,
                2035,
                1973,
                1761,
                1748,
                1691,
                1666,
            ],
            "total_words": [
                1091182,
                439657,
                417340,
                237747,
                193176,
                202250,
                234240,
                231131,
                95247,
                122436,
                180449,
                182012,
                152605,
                222985,
                90038,
                181535,
                171730,
                89026,
                107766,
                152386,
            ],
            "unique_mps": [
                93,
                35,
                12,
                3,
                20,
                27,
                16,
                9,
                2,
                14,
                14,
                11,
                3,
                7,
                6,
                15,
                10,
                7,
                14,
                14,
            ],
        }
    )
    provinces.insert(0, "rank", range(1, len(provinces) + 1))

    # Page 6: Top meaningful words by party after stop-word removal.
    party_words_source = {
        "AKP": [
            ("millî", 1596),
            ("kanun", 1485),
            ("türk", 1463),
            ("dünya", 1348),
            ("sağlık", 1305),
            ("tayyip", 1302),
            ("allah", 1257),
            ("sosyal", 1256),
            ("recep", 1248),
            ("millet", 1216),
        ],
        "CHP": [
            ("kanun", 2774),
            ("halk", 2680),
            ("sağlık", 2454),
            ("emekli", 2378),
            ("belediye", 2044),
            ("bakan", 1979),
            ("millî", 1969),
            ("eğitim", 1969),
            ("asgari", 1879),
            ("adalet", 1843),
        ],
        "DEM": [
            ("kürt", 2590),
            ("demokratik", 1523),
            ("barış", 1487),
            ("adalet", 1462),
            ("kadın", 1354),
            ("siyasi", 1335),
            ("sağlık", 1292),
            ("kayyum", 1195),
            ("eğitim", 1119),
            ("iktidar", 1098),
        ],
        "MHP": [
            ("türk", 1576),
            ("millî", 672),
            ("hareket", 453),
            ("milliyetçi", 402),
            ("millet", 328),
            ("israil", 271),
            ("siyasi", 264),
            ("dünya", 262),
            ("ekonomik", 246),
            ("allah", 245),
        ],
        "İYİ PARTİ": [
            ("iyi", 2762),
            ("türk", 2193),
            ("kanun", 1216),
            ("millet", 966),
            ("millî", 963),
            ("allah", 850),
            ("vergi", 795),
            ("adalet", 755),
            ("cevap", 716),
            ("para", 679),
        ],
        "YENİ YOL": [
            ("kanun", 1547),
            ("adalet", 1186),
            ("yeni", 1146),
            ("iyi", 1015),
            ("iktidar", 926),
            ("millet", 898),
            ("saadet", 865),
            ("yasa", 808),
            ("israil", 776),
            ("meclis", 772),
        ],
    }
    party_words = pd.DataFrame(
        [
            {"party": party, "word": word, "frequency": frequency, "rank": rank}
            for party, words in party_words_source.items()
            for rank, (word, frequency) in enumerate(words, start=1)
        ]
    )

    # Page 7: Province-level normalized keyword frequencies per 10K words.
    province_keywords_source = {
        "İstanbul": [
            ("kanun", 11.14),
            ("adalet", 11.07),
            ("millet", 10.97),
            ("istanbul", 10.05),
            ("millî", 9.47),
            ("siyasi", 9.07),
            ("meclis", 8.76),
            ("israil", 7.55),
            ("türk", 7.42),
            ("iktidar", 7.24),
        ],
        "Ankara": [
            ("kanun", 11.40),
            ("millî", 9.71),
            ("siyasi", 9.71),
            ("belediye", 9.28),
            ("adalet", 9.01),
            ("ankara", 8.30),
            ("türk", 7.76),
            ("üzerinden", 7.64),
            ("allah", 7.32),
            ("sağlık", 7.32),
        ],
        "Hatay": [
            ("hatay", 54.45),
            ("deprem", 30.45),
            ("yasa", 23.35),
            ("iyi", 12.17),
            ("kanun", 11.59),
            ("insanlar", 11.01),
            ("gerekir", 9.84),
            ("yeni", 9.78),
            ("vergi", 9.78),
            ("asla", 9.20),
        ],
        "Van": [
            ("kürt", 45.81),
            ("siyasi", 15.57),
            ("kadın", 15.23),
            ("kayyum", 13.64),
            ("birçok", 12.73),
            ("demokratik", 12.05),
            ("barış", 11.94),
            ("halkı", 11.14),
            ("sosyal", 10.57),
            ("çözüm", 10.12),
        ],
        "Diyarbakır": [
            ("diyarbakır", 31.63),
            ("kürt", 13.08),
            ("allah", 12.01),
            ("adalet", 11.34),
            ("siyasi", 11.26),
            ("hukuk", 9.94),
            ("sağlık", 9.36),
            ("belediye", 9.19),
            ("suriye", 8.78),
            ("barış", 8.69),
        ],
        "Şanlıurfa": [
            ("urfa", 33.08),
            ("şanlıurfa", 28.34),
            ("adalet", 17.23),
            ("elektrik", 12.33),
            ("tarım", 12.01),
            ("barış", 11.11),
            ("halk", 10.94),
            ("sorunu", 10.70),
            ("kadın", 10.13),
            ("eğitim", 10.05),
        ],
    }
    province_keywords = pd.DataFrame(
        [
            {
                "province": province,
                "word": word,
                "normalized_frequency": frequency,
                "rank": rank,
            }
            for province, words in province_keywords_source.items()
            for rank, (word, frequency) in enumerate(words, start=1)
        ]
    )

    # Page 8: Topic-based speech totals, party distributions, and top speakers.
    theme_totals = pd.DataFrame(
        {
            "theme": ["Deprem", "Eğitim", "Ekonomi", "Sağlık", "Tarım"],
            "speech_count": [3504, 7450, 8443, 6031, 4964],
        }
    )
    theme_party_source = {
        "Deprem": {
            "CHP": 1302,
            "AKP": 913,
            "DEM": 432,
            "YENİ YOL": 323,
            "İYİ PARTİ": 297,
            "MHP": 165,
        },
        "Eğitim": {
            "CHP": 2740,
            "AKP": 1599,
            "DEM": 1205,
            "İYİ PARTİ": 899,
            "YENİ YOL": 632,
            "MHP": 219,
        },
        "Ekonomi": {
            "CHP": 3474,
            "DEM": 1206,
            "AKP": 1189,
            "İYİ PARTİ": 1166,
            "YENİ YOL": 905,
            "MHP": 233,
        },
        "Sağlık": {
            "CHP": 2111,
            "AKP": 1265,
            "DEM": 1182,
            "İYİ PARTİ": 667,
            "YENİ YOL": 460,
            "MHP": 227,
        },
        "Tarım": {
            "CHP": 2353,
            "AKP": 798,
            "DEM": 542,
            "İYİ PARTİ": 534,
            "YENİ YOL": 446,
            "MHP": 182,
        },
    }
    theme_party = pd.DataFrame(
        [
            {"theme": theme, "party": party, "speech_count": speech_count}
            for theme, party_values in theme_party_source.items()
            for party, speech_count in party_values.items()
        ]
    )
    theme_top_speakers_source = {
        "Deprem": [
            ("N. ÇALIŞKAN", 138),
            ("M. GÜZELMANSUR", 106),
            ("N. YILDIRIM KARA", 106),
        ],
        "Eğitim": [
            ("A.M. BAŞARIR", 203),
            ("Y.S. TÜRKOĞLU", 158),
            ("T. ÇÖMEZ", 136),
        ],
        "Ekonomi": [
            ("A.M. BAŞARIR", 217),
            ("S. TEMELLİ", 180),
            ("S. ÖZDAĞ", 178),
        ],
        "Sağlık": [
            ("T. ÇÖMEZ", 215),
            ("G.K. KOÇYİĞİT", 135),
            ("S. TEMELLİ", 130),
        ],
        "Tarım": [
            ("T. ÇÖMEZ", 133),
            ("Ö.F. GÜRER", 132),
            ("İ.Ö. AYGUN", 96),
        ],
    }
    theme_top_speakers = pd.DataFrame(
        [
            {
                "theme": theme,
                "rank": rank,
                "speaker": speaker,
                "speech_count": speech_count,
            }
            for theme, speakers in theme_top_speakers_source.items()
            for rank, (speaker, speech_count) in enumerate(speakers, start=1)
        ]
    )

    # Page 9: Monthly speech activity timeline.
    timeline = pd.DataFrame(
        {
            "month": [
                "2023-06",
                "2023-07",
                "2023-08",
                "2023-10",
                "2023-11",
                "2023-12",
                "2024-01",
                "2024-02",
                "2024-03",
                "2024-04",
                "2024-05",
                "2024-06",
                "2024-07",
                "2024-08",
                "2024-10",
                "2024-11",
                "2024-12",
                "2025-01",
                "2025-02",
                "2025-03",
                "2025-04",
                "2025-05",
                "2025-06",
                "2025-07",
                "2025-08",
                "2025-10",
                "2025-11",
                "2025-12",
                "2026-01",
                "2026-02",
                "2026-03",
                "2026-04",
                "2026-05",
            ],
            "speech_count": [
                1392,
                3706,
                181,
                7989,
                8256,
                14772,
                3251,
                6580,
                820,
                3057,
                10024,
                3977,
                13063,
                482,
                5284,
                8355,
                16111,
                5112,
                4601,
                6283,
                3941,
                4863,
                3508,
                7404,
                243,
                5370,
                3879,
                17652,
                5940,
                5541,
                4372,
                6842,
                3591,
            ],
        }
    )
    timeline["date"] = pd.to_datetime(timeline["month"] + "-01")
    timeline["year"] = timeline["date"].dt.year
    timeline["month_number"] = timeline["date"].dt.month
    timeline["month_name"] = timeline["month_number"].map(
        lambda value: calendar.month_abbr[value]
    )

    return {
        "party_stats": party_stats,
        "trends": trends,
        "top_mps": top_mps,
        "provinces": provinces,
        "party_words": party_words,
        "province_keywords": province_keywords,
        "theme_totals": theme_totals,
        "theme_party": theme_party,
        "theme_top_speakers": theme_top_speakers,
        "timeline": timeline,
    }


def apply_page_style() -> None:
    """Apply a compact academic visual style around Streamlit's default layout."""
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background: {COLORS["page"]};
        }}
        .block-container {{
            max-width: 1420px;
            padding-top: 1.35rem;
            padding-bottom: 2.5rem;
        }}
        h1, h2, h3 {{
            color: {COLORS["navy"]};
            letter-spacing: 0;
        }}
        div[data-testid="stMetric"] {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["line"]};
            border-left: 7px solid {COLORS["blue"]};
            border-radius: 8px;
            padding: 0.85rem 1rem;
            box-shadow: 0 1px 2px rgba(19, 34, 56, 0.04);
        }}
        div[data-testid="stMetricValue"] {{
            color: {COLORS["navy"]};
            font-weight: 750;
        }}
        div[data-testid="stMetricLabel"] {{
            color: {COLORS["muted"]};
        }}
        .section-subtitle {{
            color: {COLORS["muted"]};
            font-size: 0.98rem;
            margin-top: -0.6rem;
            margin-bottom: 1.1rem;
        }}
        .insight-box {{
            background: #FFFFFF;
            border: 1px solid {COLORS["line"]};
            border-left: 6px solid {COLORS["gold"]};
            border-radius: 8px;
            padding: 0.82rem 1rem;
            margin: 0.35rem 0 1rem 0;
            color: {COLORS["text"]};
            box-shadow: 0 1px 2px rgba(19, 34, 56, 0.035);
        }}
        .source-note {{
            background: #FFFFFF;
            border: 1px solid {COLORS["line"]};
            border-radius: 8px;
            padding: 0.9rem 1rem;
            color: {COLORS["muted"]};
            font-size: 0.9rem;
        }}
        .small-label {{
            color: {COLORS["muted"]};
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 700;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_int(value: int | float) -> str:
    return f"{value:,.0f}"


def insight(text: str) -> None:
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


def ordered_color_map(parties: Iterable[str]) -> list[str]:
    return [PARTY_COLORS.get(party, COLORS["blue"]) for party in parties]


def style_figure(fig: go.Figure, height: int = 430) -> go.Figure:
    """Give all Plotly charts the same academic dashboard styling."""
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        font={"family": "DejaVu Sans, Arial, sans-serif", "color": COLORS["text"]},
        margin={"l": 20, "r": 20, "t": 54, "b": 35},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
        },
        hoverlabel={"bgcolor": "#FFFFFF", "font_size": 13},
    )
    fig.update_xaxes(
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["line"],
        linecolor=COLORS["line"],
        title_font={"color": COLORS["muted"]},
        tickfont={"color": COLORS["muted"]},
    )
    fig.update_yaxes(
        gridcolor=COLORS["grid"],
        zerolinecolor=COLORS["line"],
        linecolor=COLORS["line"],
        title_font={"color": COLORS["muted"]},
        tickfont={"color": COLORS["muted"]},
    )
    return fig


def empty_filter_warning() -> None:
    st.warning("Please select at least one value to display this analysis.")


def render_overview(data: dict[str, pd.DataFrame]) -> None:
    """Section 1: Dataset Overview, mapped from PDF page 1."""
    st.header("Dataset Overview")
    st.markdown(
        '<p class="section-subtitle">A compact profile of the parliamentary minutes used in the analysis.</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="source-note">
        <span class="small-label">STAT 401 Big Data Final Project Dashboard</span><br>
        Analysis of 28th Plenary Minutes of the Turkish Grand National Assembly (TBMM)<br>
        Basak Ugurlu 2561546 | Zeynep Fenercioglu 2561264 | Damla Basarmis 2510048
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    kpis = [
        ("Total speeches", "196,442"),
        ("Legislative term", "28"),
        ("Legislative years", "1-4"),
        ("Date range", "June 2023 - May 2026"),
        ("Unique parties", "20"),
        ("Speaker types", "16"),
        ("Provinces", "81"),
    ]
    first_row = st.columns(4)
    second_row = st.columns(3)
    for column, (label, value) in zip(first_row + second_row, kpis):
        column.metric(label, value)

    col1, col2 = st.columns([0.58, 0.42])
    with col1:
        party_stats = data["party_stats"].head(6)
        fig = px.bar(
            party_stats.sort_values("speech_count", ascending=True),
            x="speech_count",
            y="party",
            orientation="h",
            color="party",
            color_discrete_map=PARTY_COLORS,
            text="speech_count",
            title="Major Party Speech Volume Snapshot",
            labels={"speech_count": "konuşma_sayısı", "party": "Party"},
            hover_data={"speech_count": ":,", "total_words": ":,", "average_words": ":.1f"},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        style_figure(fig, height=410)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "CHP and AKP account for the largest MP speech volumes in the dashboard, followed by DEM, İYİ PARTİ, YENİ YOL, and MHP."
        )

    with col2:
        timeline = data["timeline"]
        yearly = timeline.groupby("year", as_index=False)["speech_count"].sum()
        fig = px.bar(
            yearly,
            x="year",
            y="speech_count",
            text="speech_count",
            title="Speech Activity by Calendar Year",
            labels={"speech_count": "speech_count", "year": "Year"},
            color="year",
            color_continuous_scale=["#3E78C5", "#D95757", "#E0A12A", "#35A56A"],
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        style_figure(fig, height=410)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "The calendar-year profile reflects the timeline: 2024 and 2025 contain the heaviest cumulative activity in this extracted period."
        )


def render_party_statistics(data: dict[str, pd.DataFrame]) -> None:
    """Section 2: Party-Based Speech Statistics, mapped from PDF page 2."""
    st.header("Party-Based Speech Statistics")
    st.markdown(
        '<p class="section-subtitle">konuşma_sayısı, toplam_kelime, ort_kelime by parti (MPs only).</p>',
        unsafe_allow_html=True,
    )

    party_stats = data["party_stats"]
    selected_parties = st.multiselect(
        "Party filter",
        options=party_stats["party"].tolist(),
        default=party_stats["party"].head(6).tolist(),
        key="party_stats_filter",
    )
    filtered = party_stats[party_stats["party"].isin(selected_parties)]
    if filtered.empty:
        empty_filter_warning()
        return

    col1, col2 = st.columns([0.58, 0.42])
    with col1:
        fig = px.bar(
            filtered.sort_values("speech_count", ascending=True),
            x="speech_count",
            y="party",
            orientation="h",
            color="party",
            color_discrete_map=PARTY_COLORS,
            text="speech_count",
            title="Table 1: Number of Speeches by Major Parties",
            labels={"speech_count": "konuşma_sayısı (Number of Speeches)", "party": "Party"},
            hover_data={"total_words": ":,", "average_words": ":.1f"},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        style_figure(fig, height=max(390, 28 * len(filtered) + 140))
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "The major-party chart shows that speech count is highly concentrated among CHP, AKP, and DEM."
        )

    with col2:
        fig = px.scatter(
            filtered,
            x="total_words",
            y="average_words",
            size="speech_count",
            color="party",
            color_discrete_map=PARTY_COLORS,
            text="party",
            title="Total Words vs. Average Words",
            labels={
                "total_words": "toplam_kelime (Total words)",
                "average_words": "ort_kelime (Avg. words)",
                "speech_count": "Speeches",
            },
            hover_data={"speech_count": ":,", "total_words": ":,", "average_words": ":.1f"},
        )
        fig.update_traces(textposition="top center")
        style_figure(fig, height=430)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "DP and DBP have small speech counts but high average word counts, while the largest parties dominate total word volume."
        )

    st.subheader("All-party detail")
    display_df = party_stats.rename(
        columns={
            "party": "Party",
            "speech_count": "Speeches",
            "total_words": "Total words",
            "average_words": "Avg.",
        }
    )
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def render_yearly_trends(data: dict[str, pd.DataFrame]) -> None:
    """Section 3: Party Speech Trends by Legislative Year, mapped from PDF page 3."""
    st.header("Party Speech Trends by Legislative Year")
    st.markdown(
        '<p class="section-subtitle">konuşma_sayısı by yasama_yılı and parti.</p>',
        unsafe_allow_html=True,
    )

    trends = data["trends"]
    col_filter1, col_filter2 = st.columns([0.55, 0.45])
    with col_filter1:
        selected_parties = st.multiselect(
            "Party filter",
            options=trends["party"].drop_duplicates().tolist(),
            default=trends["party"].drop_duplicates().tolist(),
            key="trend_party_filter",
        )
    with col_filter2:
        selected_years = st.multiselect(
            "Legislative year filter",
            options=sorted(trends["legislative_year"].unique()),
            default=sorted(trends["legislative_year"].unique()),
            key="trend_year_filter",
        )

    filtered = trends[
        trends["party"].isin(selected_parties)
        & trends["legislative_year"].isin(selected_years)
    ]
    if filtered.empty:
        empty_filter_warning()
        return

    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(
            filtered,
            x="legislative_year",
            y="speech_count",
            color="party",
            markers=True,
            color_discrete_map=PARTY_COLORS,
            title="Table 3: Speech Count Trend Across Legislative Years",
            labels={
                "legislative_year": "yasama_yılı (Legislative Year)",
                "speech_count": "konuşma_sayısı (Speech Count)",
                "party": "Party",
            },
            hover_data={"speech_count": ":,"},
        )
        fig.update_xaxes(dtick=1)
        style_figure(fig, height=440)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "Speech counts rise sharply after legislative year 1; CHP peaks in year 3, while AKP peaks in year 2."
        )

    with col2:
        fig = px.line(
            filtered,
            x="legislative_year",
            y="total_words",
            color="party",
            markers=True,
            color_discrete_map=PARTY_COLORS,
            title="Table 4: Total Word Count Trend Across Legislative Years",
            labels={
                "legislative_year": "yasama_yılı (Legislative Year)",
                "total_words": "toplam_kelime (Total Words)",
                "party": "Party",
            },
            hover_data={"total_words": ":,"},
        )
        fig.update_xaxes(dtick=1)
        style_figure(fig, height=440)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "Word-volume trends mirror the speech-count pattern, with CHP remaining the largest contributor across the later years."
        )


def render_top_mps(data: dict[str, pd.DataFrame]) -> None:
    """Section 4: Top 20 Most Active MPs, mapped from PDF page 4."""
    st.header("Top 20 Most Active MPs")
    st.markdown(
        '<p class="section-subtitle">Ranked by konuşma_sayısı (number of speeches).</p>',
        unsafe_allow_html=True,
    )

    top_mps = data["top_mps"]
    selected_parties = st.multiselect(
        "Party filter",
        options=top_mps["party"].drop_duplicates().tolist(),
        default=top_mps["party"].drop_duplicates().tolist(),
        key="top_mps_party_filter",
    )
    filtered = top_mps[top_mps["party"].isin(selected_parties)]
    if filtered.empty:
        empty_filter_warning()
        return

    col1, col2 = st.columns([0.68, 0.32])
    with col1:
        fig = px.bar(
            filtered.sort_values("speech_count", ascending=True),
            x="speech_count",
            y="mp",
            orientation="h",
            color="party",
            color_discrete_map=PARTY_COLORS,
            text="speech_count",
            title="Table 5: Top 20 Most Active Members of Parliament",
            labels={"speech_count": "konuşma_sayısı", "mp": "MP", "party": "Party"},
            hover_data={"province": True, "total_words": ":,", "rank": True},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        style_figure(fig, height=max(520, 25 * len(filtered) + 150))
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "Ali Mahir Başarır leads the top-20 MP list with 5,260 speeches; CHP has the largest presence among the top MPs."
        )

    with col2:
        party_counts = (
            filtered.groupby("party", as_index=False)
            .size()
            .rename(columns={"size": "mp_count"})
            .sort_values("mp_count", ascending=False)
        )
        fig = px.pie(
            party_counts,
            names="party",
            values="mp_count",
            hole=0.52,
            color="party",
            color_discrete_map=PARTY_COLORS,
            title="Table 6: Party Distribution Among Top 20 MPs",
        )
        fig.update_traces(textinfo="label+value", hovertemplate="%{label}<br>MPs: %{value}<extra></extra>")
        style_figure(fig, height=430)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "The distribution chart makes the panel interactive: select or hover parties to inspect their top-MP representation."
        )

    st.dataframe(
        filtered.rename(
            columns={
                "rank": "#",
                "mp": "MP",
                "party": "Party",
                "province": "Province",
                "speech_count": "Speeches",
                "total_words": "Total words",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_top_provinces(data: dict[str, pd.DataFrame]) -> None:
    """Section 5: Top 20 Most Active Provinces, mapped from PDF page 5."""
    st.header("Top 20 Most Active Provinces")
    st.markdown(
        '<p class="section-subtitle">konuşma_sayısı, toplam_kelime, benzersiz_mv by konuşmacı_şehir.</p>',
        unsafe_allow_html=True,
    )

    provinces = data["provinces"]
    metric = st.radio(
        "Metric",
        options=["speech_count", "total_words", "unique_mps"],
        format_func={
            "speech_count": "Speech count",
            "total_words": "Total words",
            "unique_mps": "Unique MPs",
        }.get,
        horizontal=True,
        key="province_metric",
    )
    province_options = provinces["province"].tolist()
    selected_provinces = st.multiselect(
        "Province filter",
        options=province_options,
        default=province_options,
        key="top_province_filter",
    )
    filtered = provinces[provinces["province"].isin(selected_provinces)]
    if filtered.empty:
        empty_filter_warning()
        return

    col1, col2 = st.columns([0.62, 0.38])
    with col1:
        fig = px.bar(
            filtered.sort_values(metric, ascending=True),
            x=metric,
            y="province",
            orientation="h",
            color=metric,
            color_continuous_scale="Blues",
            text=metric,
            title="Table 7: Speech Activity by Province",
            labels={
                "speech_count": "konuşma_sayısı",
                "total_words": "toplam_kelime",
                "unique_mps": "benzersiz_mv",
                "province": "Province",
            },
            hover_data={"speech_count": ":,", "total_words": ":,", "unique_mps": True},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(coloraxis_showscale=False)
        style_figure(fig, height=max(500, 25 * len(filtered) + 150))
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "İstanbul is the dominant province in the table, with 19,183 speeches and 93 unique MPs."
        )

    with col2:
        fig = px.scatter(
            filtered,
            x="unique_mps",
            y="total_words",
            size="speech_count",
            color="speech_count",
            color_continuous_scale="Blues",
            text="province",
            title="Supporting Province Metrics",
            labels={
                "unique_mps": "Unique MPs",
                "total_words": "Total words",
                "speech_count": "Speeches",
            },
            hover_data={"speech_count": ":,", "total_words": ":,"},
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(coloraxis_showscale=False)
        style_figure(fig, height=450)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "Total word volume generally follows speech volume, while provinces such as Kars and Muğla stand out with fewer MPs but high word totals."
        )

    st.dataframe(
        provinces.rename(
            columns={
                "rank": "#",
                "province": "Province",
                "speech_count": "Speeches",
                "total_words": "Total words",
                "unique_mps": "Unique MPs",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_party_keywords(data: dict[str, pd.DataFrame]) -> None:
    """Section 6: Party-Based Top Keywords, mapped from PDF page 6."""
    st.header("Party-Based Top Keywords")
    st.markdown(
        '<p class="section-subtitle">Top meaningful words after stop-word removal, per parti.</p>',
        unsafe_allow_html=True,
    )

    party_words = data["party_words"]
    selected_party = st.selectbox(
        "Party filter",
        options=party_words["party"].drop_duplicates().tolist(),
        key="party_keyword_filter",
    )
    filtered = party_words[party_words["party"] == selected_party]

    col1, col2 = st.columns([0.62, 0.38])
    with col1:
        fig = px.bar(
            filtered.sort_values("frequency", ascending=True),
            x="frequency",
            y="word",
            orientation="h",
            text="frequency",
            title=f"Table: {selected_party}",
            labels={"frequency": "Frequency", "word": "Word"},
            hover_data={"rank": True, "frequency": ":,"},
        )
        fig.update_traces(
            marker_color=PARTY_COLORS.get(selected_party, COLORS["blue"]),
            texttemplate="%{text:,.0f}",
            textposition="outside",
        )
        style_figure(fig, height=470)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        top_word = filtered.iloc[0]
        insight(
            f"For {selected_party}, the top keyword in the table is <strong>{top_word['word']}</strong> with {format_int(top_word['frequency'])} occurrences."
        )

    with col2:
        compare_parties = st.multiselect(
            "Compare parties",
            options=party_words["party"].drop_duplicates().tolist(),
            default=["AKP", "CHP", "DEM"],
            key="party_keyword_compare",
        )
        comparison = party_words[
            party_words["party"].isin(compare_parties) & (party_words["rank"] <= 3)
        ]
        if comparison.empty:
            empty_filter_warning()
        else:
            fig = px.bar(
                comparison,
                x="party",
                y="frequency",
                color="word",
                barmode="group",
                title="Top 3 Keywords by Selected Parties",
                labels={"frequency": "Frequency", "party": "Party", "word": "Word"},
                hover_data={"rank": True},
            )
            style_figure(fig, height=470)
            st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            insight(
                "The party-specific keyword panels show distinct emphasis: CHP centers on kanun/halk/sağlık, DEM on kürt/demokratik/barış, and MHP on türk/millî."
            )


def render_province_keywords(data: dict[str, pd.DataFrame]) -> None:
    """Section 7: Normalized Province-Level Keyword Analysis, mapped from PDF page 7."""
    st.header("Normalized Province-Level Keyword Analysis")
    st.markdown(
        '<p class="section-subtitle">normalize_frekans per 10K words for selected konuşmacı_şehir.</p>',
        unsafe_allow_html=True,
    )

    province_keywords = data["province_keywords"]
    selected_province = st.selectbox(
        "Province selector",
        options=province_keywords["province"].drop_duplicates().tolist(),
        key="province_keyword_selector",
    )
    filtered = province_keywords[province_keywords["province"] == selected_province]

    col1, col2 = st.columns([0.6, 0.4])
    with col1:
        fig = px.bar(
            filtered.sort_values("normalized_frequency", ascending=True),
            x="normalized_frequency",
            y="word",
            orientation="h",
            text="normalized_frequency",
            title=f"Table: {selected_province}",
            labels={
                "normalized_frequency": "normalize_frekans (per 10K words)",
                "word": "Word",
            },
            hover_data={"rank": True, "normalized_frequency": ":.2f"},
        )
        fig.update_traces(
            marker_color=COLORS["teal"],
            texttemplate="%{text:.1f}",
            textposition="outside",
        )
        style_figure(fig, height=480)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        top_word = filtered.iloc[0]
        insight(
            f"In {selected_province}, <strong>{top_word['word']}</strong> has the highest normalized frequency at {top_word['normalized_frequency']:.2f} per 10K words."
        )

    with col2:
        selected_for_compare = st.multiselect(
            "Province comparison",
            options=province_keywords["province"].drop_duplicates().tolist(),
            default=["İstanbul", "Ankara", "Hatay"],
            key="province_keyword_compare",
        )
        comparison = province_keywords[
            province_keywords["province"].isin(selected_for_compare)
            & (province_keywords["rank"] <= 3)
        ]
        if comparison.empty:
            empty_filter_warning()
        else:
            fig = px.bar(
                comparison,
                x="province",
                y="normalized_frequency",
                color="word",
                barmode="group",
                title="Top 3 Normalized Keywords by Province",
                labels={
                    "normalized_frequency": "Frequency per 10K words",
                    "province": "Province",
                    "word": "Word",
                },
                hover_data={"rank": True},
            )
            style_figure(fig, height=480)
            st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
            insight(
                "The province panels reveal local thematic signatures, such as deprem in Hatay, kürt in Van, and electricity/agriculture terms in Şanlıurfa."
            )


def render_topic_analysis(data: dict[str, pd.DataFrame]) -> None:
    """Section 8: Topic-Based Speech Analysis, mapped from PDF page 8."""
    st.header("Topic-Based Speech Analysis")
    st.markdown(
        '<p class="section-subtitle">Speech counts by theme: deprem, eğitim, ekonomi, sağlık, tarım.</p>',
        unsafe_allow_html=True,
    )

    theme_totals = data["theme_totals"]
    theme_party = data["theme_party"]
    theme_top_speakers = data["theme_top_speakers"]

    col_filter1, col_filter2 = st.columns([0.5, 0.5])
    with col_filter1:
        selected_themes = st.multiselect(
            "Theme selector",
            options=theme_totals["theme"].tolist(),
            default=theme_totals["theme"].tolist(),
            key="topic_theme_filter",
        )
    with col_filter2:
        selected_parties = st.multiselect(
            "Party filter",
            options=["CHP", "AKP", "DEM", "İYİ PARTİ", "YENİ YOL", "MHP"],
            default=["CHP", "AKP", "DEM", "İYİ PARTİ", "YENİ YOL", "MHP"],
            key="topic_party_filter",
        )

    filtered_totals = theme_totals[theme_totals["theme"].isin(selected_themes)]
    filtered_party = theme_party[
        theme_party["theme"].isin(selected_themes)
        & theme_party["party"].isin(selected_parties)
    ]
    if filtered_totals.empty or filtered_party.empty:
        empty_filter_warning()
        return

    col1, col2 = st.columns([0.4, 0.6])
    with col1:
        fig = px.bar(
            filtered_totals,
            x="theme",
            y="speech_count",
            color="theme",
            color_discrete_map=THEME_COLORS,
            text="speech_count",
            title="Table 9: Total Topic-Related Speeches",
            labels={"theme": "Theme", "speech_count": "Total Speeches"},
            hover_data={"speech_count": ":,"},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False)
        style_figure(fig, height=430)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "Ekonomi is the largest topic with 8,443 topic-related speeches."
        )

    with col2:
        fig = px.bar(
            filtered_party,
            x="theme",
            y="speech_count",
            color="party",
            barmode="group",
            color_discrete_map=PARTY_COLORS,
            title="Table 10: Party Distribution per Topic",
            labels={"theme": "Theme", "speech_count": "Speech Count", "party": "Party"},
            hover_data={"speech_count": ":,"},
        )
        style_figure(fig, height=430)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
        insight(
            "CHP leads all five selected topic categories in the table."
        )

    filtered_speakers = theme_top_speakers[
        theme_top_speakers["theme"].isin(selected_themes)
    ]
    st.subheader("Table 11: Top 3 Most Active Speakers per Topic")
    st.dataframe(
        filtered_speakers.rename(
            columns={
                "theme": "Theme",
                "rank": "Rank",
                "speaker": "Speaker",
                "speech_count": "Count",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_timeline(data: dict[str, pd.DataFrame]) -> None:
    """Section 9: Monthly Speech Activity Timeline, mapped from PDF page 9."""
    st.header("Monthly Speech Activity Timeline")
    st.markdown(
        '<p class="section-subtitle">speech_count by year-month (all speakers).</p>',
        unsafe_allow_html=True,
    )

    timeline = data["timeline"]
    month_order = [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12]
    month_options = [calendar.month_abbr[value] for value in month_order]
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_years = st.multiselect(
            "Year filter",
            options=sorted(timeline["year"].unique()),
            default=sorted(timeline["year"].unique()),
            key="timeline_year_filter",
        )
    with col_filter2:
        selected_months = st.multiselect(
            "Month filter",
            options=month_options,
            default=month_options,
            key="timeline_month_filter",
        )

    selected_month_numbers = [
        number for number in month_order if calendar.month_abbr[number] in selected_months
    ]
    filtered = timeline[
        timeline["year"].isin(selected_years)
        & timeline["month_number"].isin(selected_month_numbers)
    ]
    if filtered.empty:
        empty_filter_warning()
        return

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=filtered["date"],
            y=filtered["speech_count"],
            mode="lines+markers",
            fill="tozeroy",
            fillcolor="rgba(36, 87, 167, 0.12)",
            line={"color": COLORS["blue"], "width": 2.5},
            marker={"size": 7, "color": COLORS["blue"], "line": {"width": 1, "color": "#FFFFFF"}},
            name="speech_count",
            customdata=filtered["month"],
            hovertemplate="%{customdata}<br>speech_count: %{y:,}<extra></extra>",
        )
    )
    busiest = filtered.loc[filtered["speech_count"].idxmax()]
    fig.add_trace(
        go.Scatter(
            x=[busiest["date"]],
            y=[busiest["speech_count"]],
            mode="markers+text",
            marker={"size": 14, "color": COLORS["coral"], "line": {"width": 2, "color": "#FFFFFF"}},
            text=[f"{format_int(busiest['speech_count'])}<br>{busiest['month']}"],
            textposition="top center",
            name="Selected range peak",
            hovertemplate="%{text}<extra></extra>",
        )
    )
    fig.update_layout(title="Table 12: Monthly Speech Activity Timeline")
    fig.update_xaxes(title="Month")
    fig.update_yaxes(title="speech_count")
    style_figure(fig, height=470)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
    insight(
        "December is consistently the peak month in the timeline; the busiest single month is December 2025 with 17,652 speeches."
    )

    yearly = filtered.groupby("year", as_index=False)["speech_count"].sum()
    month_averages = (
        filtered.groupby("month_number", as_index=False)["speech_count"].mean()
        .sort_values("month_number")
        .assign(month_name=lambda df: df["month_number"].map(lambda value: calendar.month_abbr[value]))
    )

    col1, col2, col3 = st.columns([0.33, 0.33, 0.34])
    with col1:
        fig = px.bar(
            yearly,
            x="year",
            y="speech_count",
            text="speech_count",
            title="Table 13: Total Speeches per Year",
            labels={"year": "Year", "speech_count": "Total Speeches"},
            color="year",
            color_continuous_scale=["#3E78C5", "#D95757", "#E0A12A", "#35A56A"],
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(showlegend=False, coloraxis_showscale=False)
        style_figure(fig, height=390)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    with col2:
        fig = px.bar(
            month_averages,
            x="month_name",
            y="speech_count",
            text="speech_count",
            title="Table 14: Average Monthly Activity",
            labels={"month_name": "Month", "speech_count": "Average speech_count"},
        )
        fig.update_traces(
            marker_color=COLORS["teal"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
        )
        style_figure(fig, height=390)
        st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    with col3:
        st.markdown(
            """
            <div class="insight-box">
            <strong>Key Insights</strong><br><br>
            December is consistently the peak month; budget deliberations drive activity.<br><br>
            August and September recess periods show near-zero activity.<br><br>
            Year 2 (2023-2024) had the highest cumulative activity.
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    st.set_page_config(
        page_title="TBMM 28 Interactive Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_page_style()
    data = load_dashboard_data()

    st.title("TBMM 28th Legislative Term Plenary Speech Analysis")
    

    with st.sidebar:
        st.header("Dashboard")
        st.markdown(
            "All charts use the values from `tbmm_analiz_son.ipynb`."
        )
        st.markdown("Hover charts, filter analyses, and switch tabs to see the analyses.")

    tabs = st.tabs(
        [
            "1. Dataset Overview",
            "2. Party Statistics",
            "3. Yearly Trends",
            "4. Top MPs",
            "5. Top Provinces",
            "6. Party Keywords",
            "7. Province Keywords",
            "8. Topic Analysis",
            "9. Monthly Timeline",
        ]
    )

    with tabs[0]:
        render_overview(data)
    with tabs[1]:
        render_party_statistics(data)
    with tabs[2]:
        render_yearly_trends(data)
    with tabs[3]:
        render_top_mps(data)
    with tabs[4]:
        render_top_provinces(data)
    with tabs[5]:
        render_party_keywords(data)
    with tabs[6]:
        render_province_keywords(data)
    with tabs[7]:
        render_topic_analysis(data)
    with tabs[8]:
        render_timeline(data)


if __name__ == "__main__":
    main()
