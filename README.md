# moomoo OpenAPI

### 简介

[**moomoo OpenAPI**](https://openapi.moomoo.com/moomoo-api-doc/)开源项目可以满足使用[**Futu OpenAPI**](https://www.futunn.com/OpenAPI)进行量化投资的需求, 并提供包括Python、Json/Protobuf协议的行情及交易接口。

- [官方在线文档](https://openapi.moomoo.com/moomoo-api-doc/)

-------------------

### 安装
```
pip install moomoo-api
```

###### 注: 本API支持Python2.7/Python3.x, 推荐安装anaconda2或anaconda3环境，方便快捷。

---

### 快速上手
```

# 导入moomoo-api
import moomoo as ft

# 实例化行情上下文对象
quote_ctx = ft.OpenQuoteContext(host="127.0.0.1", port=11111)

# 上下文控制
quote_ctx.start()              # 开启异步数据接收
quote_ctx.set_handler(ft.TickerHandlerBase())  # 设置用于异步处理数据的回调对象(可派生支持自定义)

# 低频数据接口
market = ft.Market.HK
code = 'HK.00123'
code_list = [code]
plate = 'HK.BK1107'
print(quote_ctx.get_trading_days(market, start=None, end=None))   # 获取交易日
print(quote_ctx.get_stock_basicinfo(market, stock_type=ft.SecurityType.STOCK))   # 获取股票信息
print(quote_ctx.get_autype_list(code_list))                                  # 获取复权因子
print(quote_ctx.get_market_snapshot(code_list))                              # 获取市场快照
print(quote_ctx.get_plate_list(market, ft.Plate.ALL))                         # 获取板块集合下的子板块列表
print(quote_ctx.get_plate_stock(plate))                         # 获取板块下的股票列表

# 高频数据接口
quote_ctx.subscribe(code, [ft.SubType.QUOTE, ft.SubType.TICKER, ft.SubType.K_DAY, ft.SubType.ORDER_BOOK, ft.SubType.RT_DATA, ft.SubType.BROKER])
print(quote_ctx.get_stock_quote(code))  # 获取报价
print(quote_ctx.get_rt_ticker(code))   # 获取逐笔
print(quote_ctx.get_cur_kline(code, num=100, ktype=ft.KLType.K_DAY))   #获取当前K线
print(quote_ctx.get_order_book(code))       # 获取摆盘
print(quote_ctx.get_rt_data(code))          # 获取分时数据
print(quote_ctx.get_broker_queue(code))     # 获取经纪队列

# 停止异步数据接收
quote_ctx.stop()

# 关闭对象
quote_ctx.close()

# 实例化港股交易上下文对象
trade_hk_ctx = ft.OpenHKTradeContext(host="127.0.0.1", port=11111)

# 交易接口列表
print(trade_hk_ctx.unlock_trade(password='123456'))                # 解锁接口
print(trade_hk_ctx.accinfo_query(trd_env=ft.TrdEnv.SIMULATE))      # 查询账户信息
print(trade_hk_ctx.place_order(price=1.1, qty=2000, code=code, trd_side=ft.TrdSide.BUY, order_type=ft.OrderType.NORMAL, trd_env=ft.TrdEnv.SIMULATE))  # 下单接口
print(trade_hk_ctx.order_list_query(trd_env=ft.TrdEnv.SIMULATE))      # 查询订单列表
print(trade_hk_ctx.position_list_query(trd_env=ft.TrdEnv.SIMULATE))    # 查询持仓列表

trade_hk_ctx.close()

```

---

### 示例策略

- 示例策略文件位于目录: (moomoo-api包安装目录)/py-moomoo-api/examples 下，用户可参考实例策略来学习API的使用。

---

### 调试开关和推送记录

- set_futu_debug_model函数可以打开或关闭调试级别的log记录。
- 如果打开记录，则会记录info级别的log并且记录所有逐笔、摆盘、券商经纪的推送记录，以便于后面排查，文件记录在%appdata%(%HOME%)\com.moomoonn.FutuOpenD\Log下面
- examples\analysis下面会有对逐笔、摆盘、券商经纪的推送记录的分析脚本，与我们联系，拿到原始交易所数据后，可以载入比对（beta功能）

---

### 使用须知

- python脚本运行前，需先启动[FutuOpenD](https://www.futunn.com/download/openAPI)网关客户端

### API与FutuOpenD网关客户端的架构

![image](https://futunnopen.github.io/futu-api-doc/_images/API.png)

***


### API及FutuOpenD客户端交流方式

* 富途开放API群(229850364, 108534288) 
* 有一定交易额或特殊需求的用户请在入群后联系群主

***

### 使用说明

* 有任何问题可以到 issues  处提出，我们会及时进行解答。
* 使用新版本时请先仔细阅读接口文档，大部分问题都可以在接口文档中找到你想要的答案。
* 欢迎大家提出建议、也可以提出各种需求，我们一定会尽量满足大家的需求。

---
