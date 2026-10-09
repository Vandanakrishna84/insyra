import os
import re
from collections import Counter

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="Insyra | Web Intelligence",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Insyra")
st.subheader("Discover patterns hidden in web search data")
st.write("Turn live web search results into data-driven insights.")

api_key = os.getenv("SERPAPI_API_KEY", "")

with st.sidebar:
    st.header("Research settings")
    topic = st.text_input("Research topic", "Data Science skills")
    location = st.text_input("Location (optional)", "India")
    count = st.slider("Maximum results", 10, 50, 20)
    search_button = st.button("Research topic", type="primary")


def search_web(query, key, location_value, result_count):
    params = {
        "engine": "google",
        "q": query,
        "api_key": key,
        "num": result_count,
    }

    if location_value.strip():
        params["location"] = location_value.strip()

    response = requests.get(
        "https://serpapi.com/search.json",
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("error"):
        raise RuntimeError(data["error"])

    results = []
    for item in data.get("organic_results", []):
        results.append({
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "link": item.get("link", ""),
        })

    return pd.DataFrame(results)


def extract_keywords(texts):
    words = re.findall(
        r"\b[a-z][a-z+#.-]{2,}\b",
        " ".join(texts).lower(),
    )

    stop_words = {
        "the", "and", "for", "with", "that", "this",
        "from", "are", "was", "were", "you", "your",
        "have", "has", "how", "what", "when", "where",
        "which", "their", "will", "can", "about", "also",
        "using", "into", "more", "than", "based",
    }

    return Counter(
        word for word in words if word not in stop_words
    )


if search_button:
    if not topic.strip():
        st.error("Please enter a research topic.")
    elif not api_key:
        st.error(
            "SerpApi key not found. Configure the "
            "SERPAPI_API_KEY environment variable first."
        )
    else:
        try:
            with st.spinner("Collecting live search results..."):
                df = search_web(topic, api_key, location, count)

            if df.empty:
                st.warning("No search results were returned.")
            else:
                df = df.drop_duplicates(subset=["link"])
                df = df[df["title"].str.strip() != ""]
                texts = (
                    df["title"].fillna("")
                    + ". "
                    + df["snippet"].fillna("")
                ).tolist()

                keywords = extract_keywords(texts)

                a, b, c = st.columns(3)
                a.metric("Results analysed", len(df))
                b.metric("Distinct keywords", len(keywords))
                c.metric("Research topic", topic)

                st.header("📊 Keyword analysis")

                if keywords:
                    keyword_df = pd.DataFrame(
                        keywords.most_common(15),
                        columns=["Keyword", "Frequency"],
                    )
                    fig = px.bar(
                        keyword_df,
                        x="Frequency",
                        y="Keyword",
                        orientation="h",
                        title="Most frequent keywords in search results",
                    )
                    fig.update_layout(
                       yaxis={"categoryorder": "total ascending"}
                    )
                    st.plotly_chart(fig, use_container_width=True)

                st.caption(
                    "Keyword frequency describes this dataset, "
                    "not the entire internet."
                )

                st.header("🧠 Compare research topics")
                comparison = st.text_input(
                    "Second topic",
                    "Machine Learning skills",
                )

                if st.button("Compare topics"):
                    other_df = search_web(
                        comparison, api_key, location, count
                    )

                    if not other_df.empty:
                        other_texts = (
                            other_df["title"].fillna("")
                            + ". "
                            + other_df["snippet"].fillna("")
                        ).tolist()

                        vectorizer = TfidfVectorizer(
                            stop_words="english",
                            max_features=1000,
                        )
                        matrix = vectorizer.fit_transform([
                            " ".join(texts),
                            " ".join(other_texts),
                        ])
                        similarity = cosine_similarity(
                            matrix[0:1], matrix[1:2]
                        )[0][0]

                        st.metric(
                            "Text similarity",
                            f"{similarity:.1%}",
                        )
                        st.caption(
                            "Similarity compares word patterns; "
                            "it does not prove factual agreement."
                        )
                    else:
                        st.warning("No comparison results found.")

                st.header("🌐 Original sources")
                for _, row in df.iterrows():
                    with st.expander(row["title"]):
                        st.write(row["snippet"])
                        if row["link"]:
                            st.markdown(f"[Open source]({row['link']})")

                st.download_button(
                    "Download results as CSV",
                    df.to_csv(index=False).encode("utf-8"),
                    file_name="insyra_results.csv",
                    mime="text/csv",
                )

        except requests.RequestException as exc:
            st.error(f"Search request failed: {exc}")
        except (ValueError, RuntimeError) as exc:
            st.error(f"Could not process the search: {exc}")

else:
    st.info("Choose a research topic and click Research topic.")
    st.write("Try: Data Science skills, AI jobs, or Python trends.")