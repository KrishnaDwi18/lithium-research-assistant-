
import re
from collections import Counter

import streamlit as st

st.set_page_config(
    page_title="Lithium Research Assistant",
    page_icon="🔋",
    layout="wide"
)

st.title("🔋 Lithium Research Assistant")
st.write(
    "A simple research tool for studying lithium mining, "
    "critical minerals, and climate justice, with a focus on Zimbabwe."
)

st.info(
    "Paste text from a research paper or policy report below "
    "to generate a basic extractive summary."
)

text = st.text_area(
    "Paste your research text here",
    height=250,
    placeholder="Paste an abstract, research paper excerpt, or policy report..."
)

def summarise(text, sentence_count=5):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s for s in sentences if len(s.split()) > 4]

    if len(sentences) <= sentence_count:
        return "\n\n".join(sentences)

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    common_words = {
        "the", "and", "for", "that", "this", "with", "from",
        "are", "was", "were", "has", "have", "had", "not",
        "but", "its", "their", "they", "which", "into",
        "also", "can", "may", "will", "than", "these",
        "those", "been", "being", "such", "our", "more"
    }

    words = [word for word in words if word not in common_words]
    frequencies = Counter(words)

    scored_sentences = []
    for index, sentence in enumerate(sentences):
        sentence_words = re.findall(
            r"\b[a-zA-Z]{3,}\b", sentence.lower()
        )
        score = sum(
            frequencies[word]
            for word in sentence_words
            if word not in common_words
        )
        score = score / max(len(sentence_words), 1)
        scored_sentences.append((index, score, sentence))

    top_sentences = sorted(
        scored_sentences,
        key=lambda item: item[1],
        reverse=True
    )[:sentence_count]

    top_sentences.sort(key=lambda item: item[0])
    return "\n\n".join(item[2] for item in top_sentences)


if st.button("Summarise Research Text"):
    if not text.strip():
        st.warning("Please paste some research text first.")
    else:
        summary = summarise(text)
        st.subheader("Research Summary")
        st.write(summary)

        st.download_button(
            "Download Summary",
            data=summary,
            file_name="research_summary.txt",
            mime="text/plain"
        )

st.divider()
st.caption(
    "Early prototype. This version selects important sentences "
    "using word frequency; it does not generate AI analysis "
    "or verify research claims."
)
