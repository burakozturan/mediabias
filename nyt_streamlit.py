import json
import streamlit as st
import pandas as pd

st.set_page_config(page_title="News Entity & Word Analysis", layout="wide")

st.title("📰 Media Analysis: Top Entities & Words in May 2025")

# --- Choose outlet ---
media_files = {
    "NYTimes": "daily_nytimes_stats.json",
    "Fox News": "daily_fox_stats.json"
}

media_choice = st.sidebar.selectbox("📺 Choose Media Outlet", list(media_files.keys()))
json_file = media_files[media_choice]

# --- Load daily data ---
with open(json_file, "r", encoding="utf-8") as f:
    daily_data = json.load(f)

# --- Aggregate monthly totals ---
entity_counter = {}
word_counter = {}

for day_data in daily_data.values():
    for entity, count in day_data["top_entities"]:
        entity_counter[entity] = entity_counter.get(entity, 0) + count
    for word, count in day_data["top_words"]:
        word_counter[word] = word_counter.get(word, 0) + count

# Convert to DataFrames
monthly_entities_df = pd.DataFrame(
    sorted(entity_counter.items(), key=lambda x: x[1], reverse=True)[:20],
    columns=["Entity", "Count"]
)

monthly_words_df = pd.DataFrame(
    sorted(word_counter.items(), key=lambda x: x[1], reverse=True)[:20],
    columns=["Word", "Count"]
)

# --- Daily Exploration ---
st.sidebar.markdown("### 📅 Pick a day in May")
day = st.sidebar.selectbox("Day", sorted(daily_data.keys()))
day_data = daily_data[day]

st.subheader(f"📌 Top Entities – {media_choice}, May {day}")
daily_entity_df = pd.DataFrame(day_data["top_entities"], columns=["Entity", "Count"]).head(20)
st.bar_chart(daily_entity_df.set_index("Entity"))

st.subheader(f"📌 Top Words – {media_choice}, May {day}")
daily_word_df = pd.DataFrame(day_data["top_words"], columns=["Word", "Count"]).head(20)
st.bar_chart(daily_word_df.set_index("Word"))

# --- Monthly Summary ---
st.subheader(f"📈 Monthly Top 20 Entities – {media_choice}")
st.dataframe(monthly_entities_df)

st.subheader(f"📈 Monthly Top 20 Words – {media_choice}")
st.dataframe(monthly_words_df)
