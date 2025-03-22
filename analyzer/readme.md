# API Documentation: Risk Management Endpoints

## Overview
This API provides endpoints for descovering trade direction analysis.

---

## Endpoints


### 1. Get Trade Direction for a Specific Currency Pair
**Endpoint:** `/analyzer/direction/<currency_pair>`  
**Method:** `GET`  
**Description:** Determines a random trade direction (`buy`, `sell`, or `lateral`) for a specific currency pair.

**Parameters:**
- `currency_pair` *(string, required)*: The currency pair for which the trade direction is determined.

**Response:**
```json
{
    "direction": "buy",
    "status": 200
}
```
Possible `direction` values:
- `null`: Lateral (no trade direction)
- `ORDER_TYPE_BUY`: Buy direction
- `ORDER_TYPE_SELL`: Sell direction

**Error Handling:**
- If the direction is not 0, 1, or -1, an error is logged and a `NotImplementedError` is raised.

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
