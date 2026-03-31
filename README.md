# moomoo OpenAPI

### Introduction

The [**moomoo OpenAPI**](https://openapi.moomoo.com/moomoo-api-doc/) open-source project is designed to support quantitative investing using [**Futu OpenAPI**](https://www.moomoo.com/OpenAPI), providing market data and trading interfaces via Python, JSON/Protobuf protocols.

- [Official Online Documentation](https://openapi.moomoo.com/moomoo-api-doc/)

-------------------

### Installation
```
pip install moomoo-api
```

###### Note: This API supports Python 2.7 / Python 3.x.

---

### Quick Start
```

# Import moomoo-api
import moomoo as ft

# Instantiate the quote context object
quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)

# Context control
quote_ctx.start()              # Start async data receiving
quote_ctx.set_handler(ft.TickerHandlerBase())  # Set callback object for async data handling (can be subclassed for customization)

# Low-frequency data interfaces
market = ft.Market.HK
code = 'HK.00123'
code_list = [code]
plate = 'HK.BK1107'
print(quote_ctx.get_trading_days(market, start=None, end=None))   # Get trading days
print(quote_ctx.get_stock_basicinfo(market, stock_type=ft.SecurityType.STOCK))   # Get stock basic info
print(quote_ctx.get_autype_list(code_list))                                  # Get rehab factors
print(quote_ctx.get_market_snapshot(code_list))                              # Get market snapshot
print(quote_ctx.get_plate_list(market, ft.Plate.ALL))                         # Get sub-plate list under a plate set
print(quote_ctx.get_plate_stock(plate))                         # Get stock list under a plate

# High-frequency data interfaces
quote_ctx.subscribe(code, [ft.SubType.QUOTE, ft.SubType.TICKER, ft.SubType.K_DAY, ft.SubType.ORDER_BOOK, ft.SubType.RT_DATA, ft.SubType.BROKER])
print(quote_ctx.get_stock_quote(code))  # Get stock quote
print(quote_ctx.get_rt_ticker(code))   # Get tick-by-tick data
print(quote_ctx.get_cur_kline(code, num=100, ktype=ft.KLType.K_DAY))   # Get current K-line
print(quote_ctx.get_order_book(code))       # Get order book
print(quote_ctx.get_rt_data(code))          # Get intraday data
print(quote_ctx.get_broker_queue(code))     # Get broker queue

# Stop async data receiving
quote_ctx.stop()

# Close the object
quote_ctx.close()

# Instantiate HK stock trading context object
trade_hk_ctx = ft.OpenHKTradeContext(host="127.0.0.1", port=11111)

# Trading interface list
print(trade_hk_ctx.unlock_trade(password='123456'))                # Unlock trading
print(trade_hk_ctx.accinfo_query(trd_env=ft.TrdEnv.SIMULATE))      # Query account info
print(trade_hk_ctx.place_order(price=1.1, qty=2000, code=code, trd_side=ft.TrdSide.BUY, order_type=ft.OrderType.NORMAL, trd_env=ft.TrdEnv.SIMULATE))  # Place order
print(trade_hk_ctx.order_list_query(trd_env=ft.TrdEnv.SIMULATE))      # Query order list
print(trade_hk_ctx.position_list_query(trd_env=ft.TrdEnv.SIMULATE))    # Query position list

trade_hk_ctx.close()

```

---

### Sample Strategies

- Sample strategy files are located in: (moomoo-api package installation directory)/py-moomoo-api/examples. Users can refer to these sample strategies to learn how to use the API.

---

### Debug Switch and Push Records

- The `set_futu_debug_model` function can enable or disable debug-level log recording.
- When enabled, info-level logs are recorded along with all tick-by-tick, order book, and broker push records for later troubleshooting. Log files are stored in `%appdata%(%HOME%)\com.moomoonn.FutuOpenD\Log`.
- Under `examples\analysis`, there are analysis scripts for tick-by-tick, order book, and broker push records. Contact us to obtain raw exchange data for comparison loading (beta feature).

---

### Prerequisites

- Before running any Python scripts, you must first start the [FutuOpenD](https://www.moomoo.com/download/openAPI) gateway client.

### Architecture of API and FutuOpenD Gateway Client

![image](https://futunnopen.github.io/futu-api-doc/_images/API.png)

***


### Community & Support

* Users with significant trading volume or special requirements are welcome to contact the group admin after joining.

***

### Instructions

* For any questions, please submit an issue and we will respond promptly.
* When using a new version, please read the API documentation carefully first — most questions can be answered there.
* Suggestions and feature requests are welcome; we will do our best to accommodate your needs.

---
