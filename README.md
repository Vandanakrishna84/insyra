# Insyra — Web Search Intelligence
**Live Demo:**
https://insyra-txyav7gqwfazsypmepyn9i.streamlit.app/

## Overview

Insyra is a web-based research and data analysis application that transforms live web search results into useful insights.

Using SerpApi, Python, and data analysis techniques, Insyra helps users explore search results, identify recurring keywords, compare research topics, and discover relevant sources.

## Features

- Live Google search using SerpApi
- Search results with source links
- Keyword frequency analysis
- Interactive data visualizations
- Text similarity and topic comparison
- CSV export for further analysis

## Technology Stack

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- Scikit-learn
- SerpApi Google Search API

## Installation

Install Python and the dependencies listed in requirements.txt.

Run:

    python -m pip install -r requirements.txt

## API Configuration

Insyra requires a valid SerpApi API key.

Set the SERPAPI_API_KEY environment variable before launching the application.

On Windows Command Prompt, run:

    set SERPAPI_API_KEY=YOUR_API_KEY

Replace YOUR_API_KEY with your own key. Never publish your API key.

## Run the Application

Run the following command in the project directory:

    python -m streamlit run insyra_app.py

Open the local address displayed in the terminal, usually:

    http://localhost:8501

## Security

Never commit API keys, passwords, or private credentials to GitHub.

## Project Purpose

Insyra aims to make web research more structured, interactive, and data-driven by combining search-engine data with text analysis and visualization.
