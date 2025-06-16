import json
import streamlit as st
import pandas as pd

# --- Load daily data ---
with open("daily_nytimes_stats.json") as f:
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

# --- Streamlit UI ---
st.title("NYTimes Article Analysis – May 2025")

# Daily exploration
day = st.selectbox("📅 Select a Day (May)", sorted(daily_data.keys()))
day_data = daily_data[day]

st.subheader(f"Top Entities – May {day}")
daily_entity_df = pd.DataFrame(day_data["top_entities"], columns=["Entity", "Count"]).head(20)
st.bar_chart(daily_entity_df.set_index("Entity"))

st.subheader(f"Top Words – May {day}")
daily_word_df = pd.DataFrame(day_data["top_words"], columns=["Word", "Count"]).head(20)
st.bar_chart(daily_word_df.set_index("Word"))

# Monthly summary
st.subheader("📈 Monthly Top 20 Entities (May 2025)")
st.dataframe(monthly_entities_df)

st.subheader("📈 Monthly Top 20 Words (May 2025)")
st.dataframe(monthly_words_df)
