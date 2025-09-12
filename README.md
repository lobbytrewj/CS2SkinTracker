# CS2 Skin Investment Advisor 📈
A full-stack application that leverages machine learning and real-time market data to provide investment advice for the Counter-Strike 2 (CS2) skin market. This tool helps users track their portfolio, analyze market trends, and make data-driven decisions to maximize their return on investment.

# Core Features
📊 Market Data CollectionScrapes and aggregates data from the Steam Community Market and third-party sites like Buff163 to track price history, volume, and item metadata.

🤖 Price Prediction Engine: Utilizes Random Forest/XGBoost and LSTM models with technical and fundamental analysis to forecast future skin prices.

💡 Investment Recommendation System: Generates "Buy/Hold/Sell" signals using portfolio optimization techniques (Modern Portfolio Theory) and custom risk scoring.

💼 Portfolio Tracker & Analytics: Allows users to import their Steam inventory to monitor real-time Profit & Loss, analyze portfolio health, and set up custom price alerts.

# Technologies Used
Frontend: React, TypeScript, Chart.js / D3.js

Backend: Python (FastAPI), PostgreSQL

Machine Learning: scikit-learn, pandas, NumPy, XGBoost

APIs & Scraping: Buff163 API, aiohttp, BeautifulSoup

Deployment: Local System (AWS coming soon)

# Prerequisites
Python 3.8+

Node.js and npm

PostgreSQL

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
DB_HOST=localhost
DB_NAME=cs2skins
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
```
* Initialize your database:
'''
python init_db.py
'''
* Run the backend server:
```
uvicorn app.main:app --reload
The API will be available at http://localhost:8000.
```
3. Frontend Setup (Coming Soon)
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

# Implementation Progress Checks

Phase 1 (Current): Data Foundation & Basic UI

✅ Data collection pipeline for popular skins from Buff163.

✅ PostgreSQL database schema for items and price history.

⏳ Basic web interface to browse skins and view historical price charts.

Phase 2 (Upcoming): ML Predictions & Portfolio Tracking

⏳ Implementation of ML prediction models (Random Forest, LSTM).

⏳ User portfolio tracking by importing a Steam inventory.

⏳ Development of an initial investment scoring algorithm.

Phase 3 (Future): Recommendation Engine & Advanced Analytics

planned: Build a full recommendation engine with "Buy/Hold/Sell" signals.

planned: Implement a notification system for price alerts.

planned: Polish UI/UX and add advanced portfolio analytics dashboards.

planned: Utilize AWS CLI to obtain data from the cloud
