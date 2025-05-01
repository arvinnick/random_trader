# Microservices-Based Trading System

## Overview
This project is a microservices-based automated trading system designed to operate with MetaTrader 5 (MT5). The system consists of multiple containerized services that communicate via APIs. The Expert Advisor (EA) in MT5 interacts with these services to make trading decisions, set risk parameters, and analyze market conditions.

![containers and their API interactions.jpg](containers and their API interactions.jpg)

## Microservices Architecture

### 1. **Trader (Expert Advisor on MT5)**
- Runs on MetaTrader 5 (MT5) as an Expert Advisor (EA).
- Calls the various microservices to determine trading actions.
- Places buy/sell orders and sets Stop Loss (SL) and Take Profit (TP) levels based on API responses.

### 2. **Risk Manager (Port: 5001)**
- Evaluates the market price and other parameters.
- Determines the appropriate SL and TP levels as well as the allocated margine to the trade action.
- Returns these levels to the Trader for execution.

### 3. **Analyzer (Port: 5003)**
- Receives requests from the Trader to analyze market conditions.
- Returns a categorical market situation: `bull`, `bear`, or `lateral`.
- Helps the Trader decide whether to buy, sell, or hold.


### 4. **Data Parser/Retriever**
- Fetches market data from designated sources (APIs, crawlers, etc.).
- Provides structured data to the Analyzer for computation.
- Ensures data consistency and accuracy.

### 5. **ORM (Database Binding)**
- Stores trade records for future analysis.
- Maintains historical market data.
- Facilitates backtesting and performance evaluation.

## API Communication
- **Trader → Analyzer** (`GET http://localhost:5003/analyzer/direction/`)
    - Returns the trading direction: `ORDER_TYPE_BUY`, `ORDER_TYPE_SELL`, or `None` (for lateral market conditions).

- **Trader → Risk Manager** (`GET http://localhost:5001/risk/`)
    - `type` can be `stop_loss` or `take_profit`.
    - Returns appropriate SL or TP levels based on the current market price.

## Deployment
- **Analyzer, Risk Manager, Data Parser, and ORM** are containerized and communicate via REST APIs.
- The **Expert Advisor** is manually installed on MetaTrader 5 and interacts with the APIs.

## Future Enhancements
- Implement more advanced risk assessment in the Risk Manager.
- Expand the Analyzer with AI-based prediction models.
- Improve data retrieval with more efficient API integration.

## Notes
- Ensure that all microservices are running before launching the Expert Advisor in MT5.
- The public repository provides a simplified version of SL/TP calculation for demonstration purposes.

This document serves as a high-level guide to the system's architecture and functionality. For implementation details, refer to individual service documentation.

## how to run:
1. run the docker compose file
sample request payload:
  ```json
   {
     "request_identifier": 12345,
     "current_price": 1.2345,
     "currency_pair":"EURUSD",
     "open_positions": 
       [
         {"symbol": "EURUSD", "volume": 400},
         {"symbol": "USDCHF", "volume": 400},
         {"symbol": "GBPUSD", "volume": 400},
         {"symbol": "AUDUSD", "volume": 400}
       ],
     "account_liquidity": 2800,
     "available_margin": 800
   }
```