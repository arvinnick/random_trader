//+------------------------------------------------------------------+
//|                      API-Based Expert Advisor                   |
//|   This EA fetches trade directions, SL, and TP from an API      |
//+------------------------------------------------------------------+

#include <Trade/Trade.mqh>
CTrade trade;

// API Endpoint Base URLs
#define ANALYZER_API "http://localhost:5003/analyzer/direction/"
#define RISK_API "http://localhost:5001/risk/"

// Function to fetch trade direction
int GetTradeDirection(string currencyPair) {
   string url = ANALYZER_API + currencyPair;
   char result[];
   int timeout = 5000;
   ResetLastError();
   int request = WebRequest("GET", url, "", timeout, result, 1024);

   if(request != 200) {
      Print("Error fetching trade direction: ", GetLastError());
      return 0; // Default to no trade
   }

   string response = CharArrayToString(result);
   Print("Trade Direction Response: ", response);
   if(StringFind(response, "ORDER_TYPE_BUY") >= 0) return 1;
   if(StringFind(response, "ORDER_TYPE_SELL") >= 0) return -1;
   return 0;
}

// Function to get Stop Loss or Take Profit
double GetRiskParameter(string type, double price) {
   string url = RISK_API + type + "/" + DoubleToString(price, 5);
   char result[];
   int timeout = 5000;
   ResetLastError();
   int request = WebRequest("GET", url, "", timeout, result, 1024);

   if(request != 200) {
      Print("Error fetching ", type, ": ", GetLastError());
      return 0;
   }

   string response = CharArrayToString(result);
   Print(type, " Response: ", response);
   double level = StringToDouble(response);
   return level;
}

// Main trading logic
void OnTick() {
   string currencyPair = "EURUSD";
   double price = SymbolInfoDouble(currencyPair, SYMBOL_BID);
   int direction = GetTradeDirection(currencyPair);

   if(direction == 0) return;

   double stopLoss = GetRiskParameter("stop_loss", price);
   double takeProfit = GetRiskParameter("take_profit", price);

   if(stopLoss == 0 || takeProfit == 0) {
      Print("Skipping trade due to invalid SL/TP values.");
      return;
   }

   if(direction == 1) {
      trade.Buy(0.1, currencyPair, price, stopLoss, takeProfit);
   } else if(direction == -1) {
      trade.Sell(0.1, currencyPair, price, stopLoss, takeProfit);
   }
   Print("Trade placed: ", direction == 1 ? "BUY" : "SELL", " @ ", price);
}
