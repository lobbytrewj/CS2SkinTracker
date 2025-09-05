# CS2 Skin Investment Advisor 📈
A full-stack application that leverages machine learning and real-time market data to provide investment advice for the Counter-Strike 2 (CS2) skin market. This tool helps users track their portfolio, analyze market trends, and make data-driven decisions to maximize their return on investment.

# Core Features
📊 Market Data Collection: Scrapes and aggregates data from the Steam Community Market and third-party sites like CSFloat and Buff163, tracking price history, volume, and item metadata.

🤖 Price Prediction Engine: Utilizes Random Forest/XGBoost and LSTM models with technical and fundamental analysis to forecast future skin prices.

💡 Investment Recommendation System: Generates "Buy/Hold/Sell" signals using portfolio optimization techniques (Modern Portfolio Theory) and custom risk scoring.

💼 Portfolio Tracker & Analytics: Allows users to import their Steam inventory to monitor real-time Profit & Loss, analyze portfolio health, and set up custom price alerts.

# Technologies Used
Frontend: React, TypeScript, Chart.js / D3.js

Backend: Python (FastAPI), PostgreSQL, Redis

Machine Learning: scikit-learn, pandas, NumPy, XGBoost

APIs & Scraping: Steam API, aiohttp, BeautifulSoup

Deployment: Docker, AWS / Heroku

# Prerequisites
Python 3.8+

Node.js and npm

Docker and Docker Compose

A Steam API Key (get one here)

# Installation & Setup

1. Clone the Repository
```
git clone https://github.com/your-username/cs2-skin-investment-advisor.git
cd cs2-skin-investment-advisor
```
2. Backend Setup
* Create a virtual environment:
```
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
* Install dependencies:
```
pip install -r requirements.txt
```
* Set up environment variables: Create a .env file in the backend directory and add your Steam API key:
```
STEAM_API_KEY="YOUR_API_KEY_HERE"
DATABASE_URL="postgresql://postgres:yourpassword@localhost/cs2_db"
```
* Launch the database with Docker:
```
docker-compose up -d
```
This will start a PostgreSQL container.
* Run the backend server:
```
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.
```
3. Frontend Setup
* Navigate to the frontend directory and install dependencies:
```
cd frontend
npm install
```
* Start the development server:
```
npm start
```
The application will be running at http://localhost:3000.

4. Run Initial Data Collection
* Execute the collection script to populate the database with initial skin data.
```
python scripts/collect_data.py
```

# Implementation Roadmap

The project is being developed in three main phases:

Phase 1 (Complete): Data Foundation & Basic UI

✅ Data collection pipeline for popular skins from the Steam Market.

✅ PostgreSQL database schema for items and price history.

✅ Basic web interface to browse skins and view historical price charts.

Phase 2 (In Progress): ML Predictions & Portfolio Tracking

⏳ Implementation of ML prediction models (Random Forest, LSTM).

⏳ User portfolio tracking by importing a Steam inventory.

⏳ Development of an initial investment scoring algorithm.

Phase 3 (Upcoming): Recommendation Engine & Advanced Analytics

planned: Build a full recommendation engine with "Buy/Hold/Sell" signals.

planned: Implement a notification system for price alerts.

planned: Polish UI/UX and add advanced portfolio analytics dashboards.
