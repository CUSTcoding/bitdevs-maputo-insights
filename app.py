import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

file_path = Path("data/en_translate/bitdevsinquete.csv")

if file_path.exists():
    df = pd.read_csv(file_path)
else:
    st.error("CSV não encontrado. Executa o script de preparação primeiro.")
    st.stop()

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("\n", " ")
)

df = df[[
    "timestamp",
    "1. are you a software developer?",
    "2. what is your current level as a software developer?_en",
    "3. which technologies do you work with? (select all that apply)_en",
    "4. how many years of programming experience do you have?_en",
    "5. do you know bitcoin?",
    "6. if not, are you interested in learning about bitcoin?",
    "7. would you participate in a bitcoin developer community in maputo (bitdevs maputo)?",
    "8. what would most motivate you to participate and stay active in the community? (select all that apply)_en",
    "9. what do you expect to achieve by participating in the community?_en"
]]

df = df.rename(columns={
    "5. do you know bitcoin?": "5. do you know bitcoin?",
    "6. if not, are you interested in learning about bitcoin?": "6. if not, are you interested in learning about bitcoin?",
    "7. would you participate in a bitcoin developer community in maputo (bitdevs maputo)?": "7. would you participate in a bitcoin developer community in maputo (bitdevs maputo)?",

    "1. are you a software developer?": "1. Are you a software developer?",
    "2. what is your current level as a software developer?_en": "2. What is your current level as a software developer?",
    "3. which technologies do you work with? (select all that apply)_en": "3. Which technologies do you work with? (select all that apply)",
    "4. how many years of programming experience do you have?_en": "4. How many years of programming experience do you have?",
    "8. what would most motivate you to participate and stay active in the community? (select all that apply)_en": "8. What would most motivate you to participate and stay active in the community? (select all that apply)",
    "9. what do you expect to achieve by participating in the community?_en": "9. What do you expect to achieve by participating in the community?"
})

st.set_page_config(
    page_title="BitDevs Maputo",
    layout="wide"
)

st.markdown("""
## Project Overview

BitDevs Maputo is a growing developer community focused on Bitcoin education, open-source collaboration, and advanced technical learning in Mozambique.

Mozambique is experiencing a rapid increase in young software developers, but still lacks structured communities dedicated to Bitcoin protocol development, Nostr, and deep technical discussions about decentralization, distributed computing, open-source projects, and collaboration.

This initiative is part of a broader African movement supported by communities such as **Btrust Builders**, **African Bitcoin**, **Bitcoin Dada Dev**, and **Africa Free Routing**, which are actively building Bitcoin education for developers across Africa. This initiative is also part of a broader ecosystem supported by communities such as **Bitcoin Famba**, **Trezor Academy**, and **Bitcoin for Fairness**, which have been developing grassroots Bitcoin education in Mozambique and the region.

After the first BitDevs launch workshop in Maputo, supported by Anita CTO from **Bitcoin For Fairness**, we are now scaling toward a **sustainable and self-sufficient Bitcoin developer ecosystem**.

Currently, the community has 12 active members, all integrated into the Bitcoin Famba community and certified by the Trezor Academy.

- 3 members completed the Orange Craft course  
- 1 member participated in the Africa Free Routing program in Johannesburg  
- 10 members are awaiting confirmation for the Btrust Builders pathway  
- All 12 members are awaiting confirmation for the Bitshala Study Cohorts and the CoreCraft program from Bitcoin Coders  

---

## Data Foundation

To validate demand and guide decision-making, we conducted a structured survey among software developers in Mozambique.

The data was:
- Collected from local developer groups (web, mobile, cybersecurity, data/AI)
- Cleaned, normalized, and standardized for analysis
- Translated from Portuguese to English as the official language of the country, while the original Portuguese data is still preserved as proof of work
- Processed to generate quantitative and qualitative insights

---

## Objectives of This Analysis

- Map the technical profile of developers in Mozambique
- Evaluate interest in joining a Bitcoin-focused developer community
- Identify key motivations (learning, networking, career growth)
- Measure Bitcoin knowledge and readiness for adoption
- Provide data-driven justification for ecosystem funding and sponsorship

---

## Why BitDevs Maputo Matters

Currently, Mozambique still lacks structured environments for:

- Bitcoin protocol development
- Lightning Network systems and Fedi
- Open-source collaboration culture
- Cypherpunk and privacy-focused technologies
- Deep technical discussions (Socratic BitDevs-style meetups)

This initiative bridges that gap by connecting Mozambican developers to the global Bitcoin ecosystem.

---

## Sponsorship Opportunity

We are seeking strategic partners to help us:

- Organize regular BitDevs meetups in Maputo
- Support developer education programs and workshops
- Provide learning resources and technical infrastructure
- Build a sustainable Bitcoin developer ecosystem in Mozambique

This initiative is supported by real survey data and validated community demand, representing a high-impact opportunity to invest in early-stage Bitcoin developer education in Africa. Data may be updated over time.
""")

if st.button("see all data"):
    st.dataframe(df)
else:
    st.dataframe(df.head(6))



st.title("BitDevs Maputo - Core Insight")

df = df.rename(columns={
    "5. do you know bitcoin?": "know_bitcoin",
    "6. if not, are you interested in learning about bitcoin?": "learn_bitcoin",
    "7. would you participate in a bitcoin developer community in maputo (bitdevs maputo)?": "join_bitdevs",

    "1. are you a software developer?": "dev_status",
    "2. what is your current level as a software developer?_en": "level",
    "3. which technologies do you work with? (select all that apply)_en": "3. Which technologies do you work with? (select all that apply)",
    "4. how many years of programming experience do you have?_en": "4. How many years of programming experience do you have?",
    "8. what would most motivate you to participate and stay active in the community? (select all that apply)_en": "8. What would most motivate you to participate and stay active in the community? (select all that apply)",
    "9. what do you expect to achieve by participating in the community?_en": "9. What do you expect to achieve by participating in the community?"
})

know_bitcoin = df["know_bitcoin"].dropna()
learn_bitcoin = df["learn_bitcoin"].fillna("No response")
join_bitdevs = df["join_bitdevs"].fillna("No response")


st.subheader("Bitcoin Awareness")

bitcoin_pct = know_bitcoin.value_counts()
learn_pct = learn_bitcoin.value_counts()
bitdevs_pct = join_bitdevs.value_counts(normalize=True) * 100

col1, col2 = st.columns(2)


with col1:
    fig1 = px.pie(
        values=bitcoin_pct.values,
        names=bitcoin_pct.index,
        title="5. Do you know Bitcoin?"
    )

    # Definir cores manualmente
    colors = []
    for value in bitcoin_pct.values:
        if value == max(bitcoin_pct.values):
            colors.append("#F7931A") 
        else:
            colors.append("#FFFFFF") 

    fig1.update_traces(
        textfont_size=14,
        marker=dict(colors=colors)
    )

    fig1.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig1, width="stretch")

color_map = {
    "Yes": "#00FF5E",   
    "Maybe": "#0099FF",  
    "No": "#EF4444",          
    "No response": "#ABBDDB"  
}

with col2:
    fig2 = px.bar(
        x=learn_pct.index,
        y=learn_pct.values,
        title="6. If not, are you interested in learning about Bitcoin?",
        color=learn_pct.index,
        color_discrete_map=color_map
    )

    fig2.update_traces(
        texttemplate='%{y}',
        textposition='outside'
    )

    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Answers",
        yaxis_title="Count",
        showlegend=False
    )

    st.plotly_chart(fig2, width="stretch")

yes_value = bitdevs_pct.get("yes", 0)

fig3 = go.Figure(go.Indicator(
    mode="gauge+number",
    value=yes_value,
    number={"suffix": "%"},
    title={"text": "People would like to participate in a Bitcoin developer community in Maputo (%)"},
    gauge={
        "axis": {"range": [0, 100]},
        "bar": {"color": "#FFFEFC"},
        "steps": [
            {"range": [0, 30], "color": "#EF4444"},
            {"range": [30, 70], "color": "#FACC15"},
            {"range": [70, 100], "color": "#22C55E"},
        ],
    }
))

fig3.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig3, width="stretch")




df.columns = df.columns.str.strip().str.lower()

df["dev_status"] = df["1. are you a software developer?"].fillna("no").str.strip().str.lower()
df["level"] = df["2. what is your current level as a software developer?"].fillna("unknown").str.strip().str.lower()

df["level"] = df["level"].replace({
    "iniciante": "beginner",
    "intermediário": "intermediate",
    "intermediario": "intermediate",
    "avançado": "advanced",
    "avancado": "advanced",
    "profissional": "professional"
})

yes_data = df[df["dev_status"] == "yes"].groupby("level").size()
no_data = df[df["dev_status"] == "no"].groupby("level").size()

levels = ["beginner", "intermediate", "advanced", "professional"]

yes_data = yes_data.reindex(levels).fillna(0)
no_data = no_data.reindex(levels).fillna(0)

fig = go.Figure()


fig.add_trace(go.Scatter(
    x=levels,
    y=no_data,
    fill='tonexty',
    mode='lines',
    name='No',
    line=dict(color='#EF4444')
))


fig.add_trace(go.Scatter(
    x=levels,
    y=yes_data,
    fill='tonexty',
    mode='lines',
    name='Yes',
    line=dict(color='#F7931A')
))

fig.update_layout(
    title="Developer Status vs Level ",
    xaxis_title="Level",
    yaxis_title="Count",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

fig.update_yaxes(
    range=[0, 15],
    dtick=1
    )

st.plotly_chart(fig, width="stretch")



motivation_col = "8. what would most motivate you to participate and stay active in the community? (select all that apply)"

motivation = (
    df[motivation_col]
    .dropna()
    .str.lower()
    .str.replace("\n", " ") 
    .str.split(",")
    .explode()
    .str.strip()
)

motivation = motivation[motivation != ""]
motivation_top = motivation.value_counts()

goals_col = "9. what do you expect to achieve by participating in the community?"

goals = (
    df[goals_col]
    .dropna()
    .str.lower()
    .str.replace("\n", " ")
    .str.split(",")
    .explode()
    .str.strip()
)

goals = goals[goals != ""]
goals_top = goals.value_counts().head(5)

st.subheader("Motivations")

st.table(
    motivation_top.reset_index().rename(
        columns={"index": "Motivation", 0: "Count"}
    )
)

st.subheader("Top 5 Goals")

st.table(
    goals_top.reset_index().rename(
        columns={"index": "Goal", 0: "Count"}
    )
)