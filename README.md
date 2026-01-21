# hotel-analytics
# 🏨 Dubai Hotel Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-success)
![Status](https://img.shields.io/badge/Status-Live-green)

A professional data analytics application designed to provide real-time market insights for the Dubai hospitality sector. This dashboard integrates with **SerpAPI (Google Hotels)** to fetch live pricing data and uses statistical modeling to generate "Value Scores" and demand forecasts.

## 🚀 Live Demo
**[Click here to view the Live App](https://your-app-url.streamlit.app)** *(Replace this link after you deploy on Streamlit Cloud)*

---

## 📊 Project Overview

This project solves the problem of "stale data" in market analysis. Instead of relying on static CSV files, this application offers two modes:

1.  **🔴 Live Mode:** Connects to the **Google Hotels API** via SerpAPI to fetch real-time pricing, ratings, and availability for detailed competitor analysis.
2.  **📊 Demo Mode:** Uses a sophisticated **Synthetic Data Engine** (built with NumPy) to generate realistic datasets using Gamma and Poisson distributions, ensuring the dashboard works even without an API key.

### Key Features
* **📈 Real-Time ETL Pipeline:** Fetches, cleans, and normalizes unstructured JSON data from search engines.
* **🧠 Value Scoring Engine:** Custom algorithm (`Rating / Price`) to identify "Hidden Gem" properties.
* **🌍 Geospatial Intelligence:** Interactive maps clustering hotels by price and location (e.g., Jumeirah vs. Downtown).
* **🔐 Secure Authentication:** Built-in login system with session management.
* **📱 Responsive UI:** Dark-mode enabled interface built with Streamlit and custom CSS.

---

## 🛠️ Technology Stack

* **Core Logic:** Python 3.9+
* **Web Framework:** Streamlit
* **Data Processing:** Pandas, NumPy
* **Visualization:** Plotly Express, Plotly Graph Objects
* **API Integration:** SerpAPI (Google Search Results)
* **Statistical Analysis:** SciPy (Distribution modeling)

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/dubai-hotel-analytics.git](https://github.com/your-username/dubai-hotel-analytics.git)
cd dubai-hotel-analytics
