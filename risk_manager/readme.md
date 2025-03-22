# API Documentation: Risk Management Endpoints

## Overview
This API provides endpoints for calculating Stop Loss (SL) and Take Profit (TP) levels, as well as margin allocation for trading risk management.

---

## Endpoints

### 1. Calculate Stop Loss Price
**Endpoint:** `/risk/stop_loss/<current_price>`  
**Method:** `GET`  
**Description:** Calculates the stop loss price based on the current market price, stop loss pips, and trade direction.

**Parameters:**
- `current_price` *(float, required)*: The current market price.
- `stop_loss_pips` *(float, optional, default=random(5-20))*: The number of pips below the current price.
- `trade_direction` *(string, optional, default='latheral')*: The direction of the trade. Accepted values: `buy`, `short`, `latheral`.

**Response:**
```json
{
    "stop loss": 1.23456
}
```

---

### 2. Calculate Take Profit Price
**Endpoint:** `/risk/take_profit/<current_price>`  
**Method:** `GET`  
**Description:** Calculates the take profit price based on the current market price, take profit pips, and trade direction.

**Parameters:**
- `current_price` *(float, required)*: The current market price.
- `take_profit_pips` *(float, optional, default=random(10-50))*: The number of pips above the current price.
- `direction` *(int, optional, default=0)*: The direction of the trade. Accepted values: `1` (buy), `-1` (short), `0` (lateral).

**Response:**
```json
{
    "take profit": 1.23456
}
```

---

### 3. Margin Allocation
**Endpoint:** `/risk/margin_allocator/`  
**Method:** `GET`  
**Description:** Allocates margin based on open positions, user-intended positions, and available account liquidity.

**Request Body (JSON):**
```json
{
    "open_positions": [
        {"symbol": "EUR/USD", "volume": 1000},
        {"symbol": "GBP/USD", "volume": 500}
    ],
    "number_of_positions": "3",
    "intended_symbols": ["EUR/USD", "GBP/USD", "USD/JPY"],
    "reserved_margin_percentage": 0.1,
    "account_liquidity": 10000
}
```

**Response:**
```json
{
    "USD/JPY": 4000,
    "EUR/USD": 4000,
    "GBP/USD": 2000
}
```

---

## Notes
- The API assumes that `current_price` is a valid floating-point number.
- Trade direction values must be correctly set (`buy`, `short`, `latheral`) for accurate calculations.
- The `margin_allocator` endpoint requires valid JSON input with all necessary fields.
- Logging is used to track calculations and errors.
- The application is designed for trading simulations and should be used with caution in real-world scenarios.

---

## Error Handling
- If `number_of_positions` is not a valid digit, an error is logged.
- If JSON fields are missing in `margin_allocator`, the API may return an empty response.
- Invalid trade directions may cause unexpected results.

       
    