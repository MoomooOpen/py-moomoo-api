# moomoo API

### Introduction

[**moomoo API**](https://openapi.moomoo.com/moomoo-api-doc/) is an open-source project for quantitative investment using [**moomoo API**](https://www.moomoo.com/OpenAPI), providing market data and trading interfaces via Python and Json/Protobuf protocols.

- [Official Documentation](https://openapi.moomoo.com/moomoo-api-doc/)

-------------------

### Installation
```
pip install moomoo-api
```

###### Note: This API supports Python 2.7/Python 3.x.

---

### Quick Start
```

# Import moomoo-api
import moomoo as ft

# Create a quote context object
quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)

# Context control
quote_ctx.start()              # Start asynchronous data reception
quote_ctx.set_handler(ft.TickerHandlerBase())  # Set callback handler for async data processing (subclass to customize)

# Low-frequency data interfaces
market = ft.Market.HK
code = 'HK.00123'
code_list = [code]
plate = 'HK.BK1107'
print(quote_ctx.get_stock_basicinfo(market, stock_type=ft.SecurityType.STOCK))   # Get stock basic info
print(quote_ctx.get_market_snapshot(code_list))                              # Get market snapshot
print(quote_ctx.get_plate_list(market, ft.Plate.ALL))                         # Get sub-plate list
print(quote_ctx.get_plate_stock(plate))                         # Get stocks under a plate

# High-frequency data interfaces
quote_ctx.subscribe(code, [ft.SubType.QUOTE, ft.SubType.TICKER, ft.SubType.K_DAY, ft.SubType.ORDER_BOOK, ft.SubType.RT_DATA, ft.SubType.BROKER])
print(quote_ctx.get_stock_quote(code))  # Get quote
print(quote_ctx.get_rt_ticker(code))   # Get ticker
print(quote_ctx.get_cur_kline(code, num=100, ktype=ft.KLType.K_DAY))   # Get current K-line
print(quote_ctx.get_order_book(code))       # Get order book
print(quote_ctx.get_rt_data(code))          # Get real-time data
print(quote_ctx.get_broker_queue(code))     # Get broker queue

# Stop asynchronous data reception
quote_ctx.stop()

# Close the context
quote_ctx.close()

# Create an HK trade context object
trade_hk_ctx = ft.OpenHKTradeContext(host="127.0.0.1", port=11111)

# Trading interfaces
print(trade_hk_ctx.unlock_trade(password='123456'))                # Unlock trading
print(trade_hk_ctx.accinfo_query(trd_env=ft.TrdEnv.SIMULATE))      # Query account info
print(trade_hk_ctx.place_order(price=1.1, qty=2000, code=code, trd_side=ft.TrdSide.BUY, order_type=ft.OrderType.NORMAL, trd_env=ft.TrdEnv.SIMULATE))  # Place order
print(trade_hk_ctx.order_list_query(trd_env=ft.TrdEnv.SIMULATE))      # Query order list
print(trade_hk_ctx.position_list_query(trd_env=ft.TrdEnv.SIMULATE))    # Query position list

trade_hk_ctx.close()

```

---

### Example Strategies

- Example strategy files are located at: (moomoo-api install directory)/py-moomoo-api/examples. You can refer to these examples to learn how to use the API.

---

### Debug Switch and Push Logs

- The `set_futu_debug_model` function can enable or disable debug-level logging.
- When enabled, it records info-level logs along with all ticker, order book, and broker push records for troubleshooting. Log files are stored in %appdata%(%HOME%)\com.moomoonn.FutuOpenD\Log.
- Analysis scripts for ticker, order book, and broker push records are available in moomoo/tools/analysis. Contact us to obtain raw exchange data for comparison (beta feature).

---

### Project Structure

```
moomoo/
├── common/              # Core module (networking, constants, Protobuf, etc.)
│   └── pb/              # Protobuf definitions and generated files
├── quote/               # Market data module
├── trade/               # Trading module
├── tools/               # Utility tools
│   └── analysis/        # Push log analysis scripts
└── examples/            # Example code
```

---

### Prerequisites

- Before running Python scripts, you must first start the [moomoo OpenD](https://openapi.moomoo.com/moomoo-api-doc/en/quick/opend-base.html) gateway client.

### API and moomoo OpenD Gateway Architecture

- [Architecture Overview](https://openapi.moomoo.com/futu-api-doc/en/intro/intro.html)

***

### Usage

* Feel free to submit questions via Issues and we will respond promptly.
* Please read the API documentation carefully when using a new version. Most questions can be answered there.
* Suggestions and feature requests are welcome. We will do our best to meet your needs.

---
