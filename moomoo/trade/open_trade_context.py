# -*- coding: utf-8 -*-

import pandas as pd
from ..common.open_context_base import OpenContextBase
from .trade_query import *
from ..common.err import *
from ..common.constant import *

class OpenTradeContextBase(OpenContextBase):
    """Class for set context of HK stock trade"""

    def __init__(self, trd_mkt, host="127.0.0.1", port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES, trd_category=TrdCategory.NONE, need_general_sec_acc=False):
        self.__trd_mkt = trd_mkt
        self._ctx_unlock = None
        self.__last_acc_list = []
        self.__is_acc_sub_push = False
        self.__security_firm = security_firm
        self.__trd_category = trd_category
        self.__need_general_sec_acc = need_general_sec_acc

        # if host != "127.0.0.1" and host != "localhost" and is_encrypt is None:
        #     '''非本地连接必须加密，以免远程攻击'''
        #     print("{} is not local connection!".format(host))
        #     raise Exception('Non-local connections must be encrypted')

        super(OpenTradeContextBase, self).__init__(host, port, is_encrypt=is_encrypt)

    def close(self):
        """
        to call close old obj before loop create new, otherwise socket will encounter error 10053 or more!
        """
        super(OpenTradeContextBase, self).close()

    def on_api_socket_reconnected(self):
        """for API socket reconnected"""
        self.__is_acc_sub_push = False
        self.__last_acc_list = []

        ret, msg = RET_OK, ''
        # auto unlock trade
        if self._ctx_unlock is not None:
            password, password_md5 = self._ctx_unlock
            ret, data = self.unlock_trade(password, password_md5)
            logger.debug('auto unlock trade ret={},data={}'.format(ret, data))
            if ret != RET_OK:
                msg = data

        # 定阅交易帐号推送
        if ret == RET_OK:
            self.__check_acc_sub_push()

        return ret, msg

    def is_futures_market_sim(self, trdMkt_list):
        if self.__trd_mkt != TrdMarket.FUTURES:
            return False
        is_futures = False
        futures_list = [TrdMarket.FUTURES_SIMULATE_HK, TrdMarket.FUTURES_SIMULATE_US, TrdMarket.FUTURES_SIMULATE_JP, TrdMarket.FUTURES_SIMULATE_SG]
        for trdMkt in trdMkt_list:
            if trdMkt in futures_list:
                is_futures = True
                break
        return is_futures

    def get_acc_list(self):
        """
        :return: (ret, data)
        """
        query_processor = self._get_sync_query_processor(
            GetAccountList.pack_req, GetAccountList.unpack_rsp)

        kargs = {
            'user_id': self.get_login_user_id(),
            'conn_id': self.get_sync_conn_id(),
            'trd_category': self.__trd_category,
            'need_general_sec_acc': self.__need_general_sec_acc
        }

        ret_code, msg, acc_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        # 记录当前市场的帐号列表
        self.__last_acc_list = []
        for record in acc_list:
            trdMkt_list = record["trdMarket_list"]
            if (self.__trd_mkt == TrdMarket.NONE or
                    self.__trd_mkt in trdMkt_list or
                    self.is_futures_market_sim(trdMkt_list)):
                if record['trd_env'] == TrdEnv.SIMULATE or record['security_firm'] == NoneDataValue or record['security_firm'] == self.__security_firm:
                    trd_marketauth = []
                    for item in record["trdmarket_auth"]:
                        trd_marketauth.append(TrdMarket.to_string2(item))
                    self.__last_acc_list.append({
                        "trd_env": record["trd_env"],
                        "acc_id": record["acc_id"],
                        "acc_type": record["acc_type"],
                        "uni_card_num": record["uni_card_num"],
                        "card_num": record["card_num"],
                        "security_firm": record["security_firm"],
                        "sim_acc_type": record["sim_acc_type"],
                        "trdmarket_auth": trd_marketauth,
                        "acc_status": record["acc_status"]})

        col_list = ["acc_id", "trd_env", "acc_type", "uni_card_num", "card_num", "security_firm", "sim_acc_type", "trdmarket_auth", "acc_status"]

        acc_table = pd.DataFrame(copy(self.__last_acc_list), columns=col_list)

        return RET_OK, acc_table

    def unlock_trade(self, password=None, password_md5=None, is_unlock=True):
        """
        交易解锁，安全考虑，所有的交易api,需成功解锁后才可操作
        :param password: 明文密码字符串 (二选一）
        :param password_md5: 密码的md5字符串（二选一）
        :param is_unlock: 解锁 = True, 锁定 = False
        :return:(ret, data) ret == RET_OK时, data为None，如果之前已经解锁过了，data为提示字符串，指示出已经解锁
                            ret != RET_OK时， data为错误字符串
        """

        # 仅支持真实交易的市场可以解锁，模拟交易不需要解锁
        md5_val = ''
        if is_unlock:
            ret = TRADE.check_mkt_envtype(self.__trd_mkt, TrdEnv.REAL)
            if not ret:
                return RET_OK, Err.NoNeedUnlock.text

            if password is None and password_md5 is None:
                return RET_ERROR, 'Missing necessary parameter. One of the two parameters (password and password_md5) is required.'

            md5_val = str(password_md5) if password_md5 else md5_transform(str(password))

        # 解锁要求先拉一次帐户列表, 目前仅真实环境需要解锁
        ret, msg, acc_id = self._check_acc_id(TrdEnv.REAL, 0)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
                UnlockTrade.pack_req, UnlockTrade.unpack_rsp)

        kargs = {
            'is_unlock': is_unlock,
            'password_md5': md5_val,
            'conn_id': self.get_sync_conn_id(),
            'security_firm': self.__security_firm
        }

        ret_code, msg, _ = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        # reconnected to auto unlock
        if RET_OK == ret_code:
            self._ctx_unlock = (password, password_md5) if is_unlock else None

        # 定阅交易帐号推送
        if is_unlock and ret_code == RET_OK:
            self.__check_acc_sub_push()

        if msg is not None and len(msg) > 0:
            return RET_OK, msg
        return RET_OK, None

    def _async_sub_acc_push(self, acc_id_list):
        """
        异步连接指定要接收送的acc id
        :param acc_id_list:
        :return:
        """
        kargs = {
            'acc_id_list': acc_id_list,
            'conn_id': self.get_async_conn_id(),
        }
        ret_code, msg, push_req_str = SubAccPush.pack_req(**kargs)
        if ret_code == RET_OK:
            self._send_async_req(push_req_str)

        return RET_OK, None

    def on_async_sub_acc_push(self, ret_code, msg):
        self.__is_acc_sub_push = ret_code == RET_OK
        if not self.__is_acc_sub_push:
            logger.error("ret={} msg={}".format(ret_code, msg))

    def _check_trd_env(self, trd_env):
        is_enable = TRADE.check_mkt_envtype(self.__trd_mkt, trd_env)
        if not is_enable:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of environment param is wrong "

        return RET_OK, ""

    def __check_acc_sub_push(self):
        if self.__is_acc_sub_push:
            return

        if len(self.__last_acc_list) == 0:
            ret, _ = self.get_acc_list()
            if ret != RET_OK:
                return

        acc_id_list = [x['acc_id'] for x in self.__last_acc_list]

        if len(acc_id_list):
            self._async_sub_acc_push(acc_id_list)

    def _check_acc_id(self, trd_env, acc_id):
        if acc_id == 0:
            if len(self.__last_acc_list) == 0:
                ret, content = self.get_acc_list()
                if ret != RET_OK:
                    return ret, content, acc_id
            acc_id = self._get_default_acc_id(trd_env)

        msg = "" if acc_id != 0 else ERROR_STR_PREFIX + "No one available account!"
        ret = RET_OK if acc_id != 0 else RET_ERROR

        return ret, msg, acc_id

    def _check_order_status(self, status_filter_list):
        unique_and_normalize_list(status_filter_list)
        for status in status_filter_list:
            if not OrderStatus.if_has_key(status):
                return RET_ERROR, ERROR_STR_PREFIX + "the type of status_filter_list param is wrong "
        return RET_OK, "",

    def _get_default_acc_id(self, trd_env):
        for record in self.__last_acc_list:
            if  record['trd_env'] == trd_env:
                return record['acc_id']
        return 0

    def _get_acc_id_by_acc_index(self, trd_env, acc_index=0):
        ret, msg = self.get_acc_list()
        if ret != RET_OK:
            return ret, msg, None, []
        acc_table = msg
        env_list = [trd_env]
        acc_table = acc_table[acc_table['trd_env'].isin(env_list)]
        acc_table = acc_table.reset_index(drop=True)

        total_acc_num = acc_table.shape[0]
        if total_acc_num == 0:
            if trd_env == TrdEnv.REAL:
                msg = "No available real accounts with {0} market authority in {1}, please check the input parameters 'security_firm' and 'filter_trdmarket' of {2}.".format(self.__trd_mkt, get_string_by_securityFirm(self.__security_firm), self.__class__.__name__)
            else:
                msg = "No available paper accounts with {0} market authority in {1}, please check the input parameters 'security_firm' and 'filter_trdmarket' of {2}.".format(self.__trd_mkt, get_string_by_securityFirm(self.__security_firm), self.__class__.__name__)
            return RET_ERROR, msg, acc_index, []
        elif acc_index >= total_acc_num:
            msg = "The acc_index is out of range"
            return RET_ERROR, msg, acc_index, []
        return RET_OK, "", acc_table['acc_id'][acc_index], acc_table['trdmarket_auth'][acc_index]

    def _check_acc_id_exist(self, trd_env, acc_id):
        ret, msg = self.get_acc_list()
        if ret != RET_OK:
            return ret, msg, acc_id, []
        content = msg

        acc_index = content[(content.acc_id == acc_id) & (content.trd_env == trd_env)].index.tolist()
        if len(acc_index):
            return RET_OK, "", acc_id, content['trdmarket_auth'][acc_index[0]]
        else:
            return RET_ERROR, ERROR_STR_PREFIX + "Nonexisting acc_id {0}!".format(acc_id), acc_id, []

    def _check_acc_id_and_acc_index(self, trd_env, acc_id, acc_index):
        if self.__trd_category == TrdCategory.SECURITY and self.__trd_mkt == TrdMarket.FUTURES:
            return RET_ERROR, 'OpenSecTradeContext can not connect to futures accounts.', None, []
        if acc_id == 0:
            ret, msg, acc_id, auth_list = self._get_acc_id_by_acc_index(trd_env, acc_index)
            if ret != RET_OK:
                return ret, msg, acc_id, []
        else:
            ret, msg, acc_id, auth_list = self._check_acc_id_exist(trd_env, acc_id)
            if ret != RET_OK:
                return ret, msg, acc_id, []
        return RET_OK, "", acc_id, auth_list

    def accinfo_query(self, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False, currency=Currency.HKD):
        """
        :param trd_env:
        :param acc_id:
        :param acc_index:
        :return:
        """
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            AccInfoQuery.pack_req, AccInfoQuery.unpack_rsp)

        kargs = {
            'acc_id': int(acc_id),
            'trd_env': trd_env,
            'trd_market': acc_auth_list[0],
            'conn_id': self.get_sync_conn_id(),
            'refresh_cache': refresh_cache,
            'currency': currency
        }

        ret_code, msg, accinfo_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            'power', 'max_power_short', 'net_cash_power', 'total_assets', 'securities_assets', 'fund_assets',
            'bond_assets', 'cash', 'market_val', 'long_mv', 'short_mv',
            'pending_asset', 'interest_charged_amount', 'frozen_cash', 'avl_withdrawal_cash', 'max_withdrawal', 'currency',
            'available_funds', 'unrealized_pl', 'realized_pl', 'risk_level', 'risk_status', 'initial_margin',
            'margin_call_margin', 'maintenance_margin',
            'hk_cash', 'hk_avl_withdrawal_cash', 'hkd_net_cash_power', 'hkd_assets',
            'us_cash', 'us_avl_withdrawal_cash', 'usd_net_cash_power', 'usd_assets',
            'cn_cash', 'cn_avl_withdrawal_cash', 'cnh_net_cash_power', 'cnh_assets',
            'jp_cash', 'jp_avl_withdrawal_cash', 'jpy_net_cash_power', 'jpy_assets',
            'sg_cash', 'sg_avl_withdrawal_cash', 'sgd_net_cash_power', 'sgd_assets',
            'au_cash', 'au_avl_withdrawal_cash', 'aud_net_cash_power', 'aud_assets',
            'is_pdt', 'pdt_seq', 'beginning_dtbp', 'remaining_dtbp',
            'dt_call_amount', 'dt_status',
        ]
        accinfo_frame_table = pd.DataFrame(accinfo_list, columns=col_list)

        return RET_OK, accinfo_frame_table

    def _get_trd_market_from_market(self, qot_market, trd_env, trd_category):
        # if self.__trd_mkt != TrdMarket.NONE:
        #     return self.__trd_mkt
        trd_market = 'N/A'
        if trd_category == TrdCategory.FUTURE:
            if trd_env == TrdEnv.REAL:
                trd_market = TrdMarket.FUTURES
            else:
                if qot_market == Market.HK:
                    trd_market = TrdMarket.FUTURES_SIMULATE_HK
                elif qot_market == Market.US:
                    trd_market = TrdMarket.FUTURES_SIMULATE_US
                elif qot_market == Market.JP:
                    trd_market = TrdMarket.FUTURES_SIMULATE_JP
                elif qot_market == Market.SG:
                    trd_market = TrdMarket.FUTURES_SIMULATE_SG
        else:
            if qot_market == Market.HK:
                trd_market = TrdMarket.HK
            if qot_market == Market.US:
                trd_market = TrdMarket.US
            if qot_market == Market.SH or qot_market == Market.SZ:
                if trd_env == TrdEnv.REAL:
                    trd_market = TrdMarket.HKCC
                else:
                    trd_market = TrdMarket.CN
            if qot_market == Market.AU:
                trd_market = TrdMarket.AU
            if qot_market == Market.SG:
                trd_market = TrdMarket.SG
            if qot_market == Market.JP:
                trd_market = TrdMarket.JP
            if qot_market == Market.MY:
                trd_market = TrdMarket.MY
            if qot_market == Market.CA:
                trd_market = TrdMarket.CA
        return trd_market

    def _check_stock_code(self, code):
        stock_code = ''
        if code is not None and code != '':
            ret_code, content = split_stock_str(str(code))
            if ret_code == RET_OK:
                _, stock_code = content
            else:
                stock_code = code
        return RET_OK, "", stock_code

    def _split_stock_code(self, code):
        stock_str = str(code)

        split_loc = stock_str.find(".")
        '''do not use the built-in split function in python.
        The built-in function cannot handle some stock strings correctly.
        for instance, US..DJI, where the dot . itself is a part of original code'''
        if 0 <= split_loc < len(stock_str) - 1 and Market.if_has_key(stock_str[0:split_loc]):
            market_str = stock_str[0:split_loc]
            partial_stock_str = stock_str[split_loc + 1:]
            return RET_OK, (market_str, partial_stock_str)

        else:
            error_str = ERROR_STR_PREFIX + "format of %s is wrong. (US.AAPL, HK.00700, SZ.000001)" % stock_str
            return RET_ERROR, error_str

    def position_list_query(self, code='', pl_ratio_min=None,
                            pl_ratio_max=None, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False, position_market = TrdMarket.NONE):
        """for querying the position list"""
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret, msg, stock_code = self._check_stock_code(code)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            PositionListQuery.pack_req, PositionListQuery.unpack_rsp)

        kargs = {
            'code': str(stock_code),
            'pl_ratio_min': pl_ratio_min,
            'pl_ratio_max': pl_ratio_max,
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'refresh_cache': refresh_cache,
            'position_market': position_market
        }
        ret_code, msg, position_list = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "code", "stock_name", "position_market", "qty", "can_sell_qty", "cost_price",
            "cost_price_valid", "average_cost", "diluted_cost", "market_val", "nominal_price", "pl_ratio",
            "pl_ratio_valid", "pl_ratio_avg_cost", "pl_val", "pl_val_valid", "today_buy_qty",
            "today_buy_val", "today_pl_val", "today_trd_val", "today_sell_qty",
            "today_sell_val", "position_side", "unrealized_pl", "realized_pl",
            "currency",
        ]

        position_list_table = pd.DataFrame(position_list, columns=col_list)
        return RET_OK, position_list_table

    def order_list_query(self, order_id="", status_filter_list=[], code='', start='', end='',
                         trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False, order_market= TrdMarket.NONE):

        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret_code, ret_data = self._order_list_query_impl(order_id, status_filter_list,
                                                         code, start, end, trd_env, acc_id,
                                                         refresh_cache, acc_auth_list[0], order_market)
        if ret_code != RET_OK:
            return ret_code, ret_data

        col_list = [
            "code", "stock_name", "order_market", "trd_side", "order_type", "order_status",
            "order_id", "qty", "price", "create_time", "updated_time",
            "dealt_qty", "dealt_avg_price", "last_err_msg", "remark",
            "time_in_force", "fill_outside_rth", "session", "aux_price", "trail_type",
            "trail_value", "trail_spread", "currency",
        ]
        order_list = ret_data
        order_list_table = pd.DataFrame(order_list, columns=col_list)

        return RET_OK, order_list_table

    def _order_list_query_impl(self, order_id, status_filter_list, code, start, end, trd_env, acc_id, refresh_cache, trd_mkt, order_market):
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg
        ret, msg , acc_id = self._check_acc_id(trd_env, acc_id)
        if ret != RET_OK:
            return ret, msg

        ret, msg, stock_code = self._check_stock_code(code)
        if ret != RET_OK:
            return ret, msg

        ret, msg = self._check_order_status(status_filter_list)
        if ret != RET_OK:
            return ret, msg

        if start:
            ret, data = normalize_date_format(start)
            if ret != RET_OK:
                return ret, data
            start = data

        if end:
            ret, data = normalize_date_format(end)
            if ret != RET_OK:
                return ret, data
            end = data

        query_processor = self._get_sync_query_processor(
            OrderListQuery.pack_req, OrderListQuery.unpack_rsp)

        # the keys of kargs should be corresponding to the actual function arguments
        kargs = {
            'order_id': str(order_id),
            'status_filter_list': status_filter_list,
            'code': str(stock_code),
            'start': str(start) if start else "",
            'end': str(end) if end else "",
            'trd_mkt': trd_mkt,
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'refresh_cache': refresh_cache,
            'order_market': order_market
        }
        ret_code, msg, order_list = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR, msg

        return RET_OK, order_list

    def place_order(self, price, qty, code, trd_side, order_type=OrderType.NORMAL,
                    adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, remark=None,
                    time_in_force=TimeInForce.DAY, fill_outside_rth=False, aux_price=None,
                    trail_type=None, trail_value=None, trail_spread=None, session=Session.NONE):
        """
        place order
        use  set_handle(HKTradeOrderHandlerBase) to recv order push !
        """
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret, content = self._split_stock_code(code)
        if ret != RET_OK:
            return ret, content

        if remark is not None:
            if is_str(remark):
                remark_utf8 = remark.encode('utf-8')
                if len(remark_utf8) > 64:
                    return RET_ERROR, make_wrong_value_msg_utf8_len_le('remark', 64)
            else:
                return RET_ERROR, make_wrong_type_msg('remark', 'str')

        fill_outside_rth = True if fill_outside_rth else False

        market_str, stock_code = content

        trd_market = self._get_trd_market_from_market(market_str, trd_env, self.__trd_category)

        query_processor = self._get_sync_query_processor(
            PlaceOrder.pack_req, PlaceOrder.unpack_rsp)

        # the keys of kargs should be corresponding to the actual function arguments
        kargs = {
            'trd_side': trd_side,
            'order_type': order_type,
            'price': float(price),
            'qty': float(qty),
            'code': stock_code,
            'adjust_limit': float(adjust_limit),
            'trd_mkt': trd_market,
            'sec_mkt_str': market_str,
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'remark': remark,
            'time_in_force': time_in_force,
            'fill_outside_rth': fill_outside_rth,
            "session": session,
            'aux_price': aux_price ,
            'trail_type': trail_type ,
            'trail_value': trail_value ,
            'trail_spread': trail_spread ,
        }

        ret_code, msg, order_id = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        order_item = {'trd_env': trd_env, 'order_id': order_id}

        # 保持跟v2.0兼容， 增加必要的订单字段
        for x in range(3):
            ret_code, ret_data = self._order_list_query_impl(order_id=order_id, status_filter_list=[],
                                            code="", start="", end="", trd_env=trd_env, acc_id=acc_id,
                                                             refresh_cache=False, trd_mkt=acc_auth_list[0], order_market=TrdMarket.NONE)
            if ret_code == RET_OK and len(ret_data) > 0:
                order_item = ret_data[0]
                order_item['trd_env'] = trd_env
                break

        col_list = [
            "code", "stock_name", "trd_side", "order_type", "order_status",
            "order_id", "qty", "price", "create_time", "updated_time",
            "dealt_qty", "dealt_avg_price", "last_err_msg", "remark",
            "time_in_force", "fill_outside_rth", "session", 'aux_price',
            'trail_type', 'trail_value', 'trail_spread', "currency",
        ]
        order_list = [order_item]
        order_table = pd.DataFrame(order_list, columns=col_list)

        return RET_OK, order_table

    def modify_order(self, modify_order_op, order_id, qty, price,
                     adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0,
                     aux_price=None, trail_type=None, trail_value=None, trail_spread=None):

        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        if not order_id:
            return RET_ERROR, ERROR_STR_PREFIX + "the type of order_id param is wrong "

        if not ModifyOrderOp.if_has_key(modify_order_op):
            return RET_ERROR, ERROR_STR_PREFIX + "the type of modify_order_op param is wrong "

        if trail_type is not None and not TrailType.if_has_key(trail_type):
            return RET_ERROR, ERROR_STR_PREFIX + "the type of trail_type param is wrong "

        query_processor = self._get_sync_query_processor(
            ModifyOrder.pack_req, ModifyOrder.unpack_rsp)

        kargs = {
            'modify_order_op': modify_order_op,
            'order_id': str(order_id),
            'price': float(price),
            'qty': float(qty),
            'adjust_limit': adjust_limit,
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'aux_price': aux_price,
            'trail_type': trail_type,
            'trail_value': trail_value,
            'trail_spread': trail_spread,
        }

        ret_code, msg, modify_order_list = query_processor(**kargs)

        if ret_code != RET_OK:
            return RET_ERROR,msg

        col_list = ['trd_env', 'order_id']
        modify_order_table = pd.DataFrame(modify_order_list, columns=col_list)

        return RET_OK, modify_order_table

    def cancel_all_order(self, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, trdmarket=TrdMarket.NONE):
        """
        取消所有的订单
        """
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        if trdmarket is not None and not TrdMarket.if_has_key(trdmarket):
            return RET_ERROR, ERROR_STR_PREFIX + "the type of trdmarket param is wrong "

        query_processor = self._get_sync_query_processor(
            CancelOrder.pack_req, CancelOrder.unpack_rsp)

        kargs = {
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'trdmarket': trdmarket,
        }

        ret_code, msg, _ = query_processor(**kargs)
        return ret_code, msg


    def change_order(self, order_id, price, qty, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0):
        return self.modify_order(ModifyOrderOp.NORMAL, order_id=order_id, qty=qty, price=price,
                                 adjust_limit=adjust_limit, trd_env=trd_env, acc_id=acc_id)

    def deal_list_query(self, code="", trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False, deal_market= TrdMarket.NONE):
        """for querying deal list"""
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret, msg, stock_code = self._check_stock_code(code)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            DealListQuery.pack_req, DealListQuery.unpack_rsp)

        kargs = {
            'code': stock_code,
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'refresh_cache': refresh_cache,
            'deal_market': deal_market
            }
        ret_code, msg, deal_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "code", "stock_name", "deal_market", "deal_id", "order_id", "qty", "price",
            "trd_side", "create_time", "counter_broker_id", "counter_broker_name", 'status'
        ]
        deal_list_table = pd.DataFrame(deal_list, columns=col_list)

        return RET_OK, deal_list_table

    def history_order_list_query(self, status_filter_list=[], code='', start='', end='',
                                 trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, order_market= TrdMarket.NONE):

        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret, msg, stock_code = self._check_stock_code(code)
        if ret != RET_OK:
            return ret, msg

        ret, msg = self._check_order_status(status_filter_list)
        if ret != RET_OK:
            return ret, msg

        ret, msg, start, end = normalize_start_end_date(start, end, 90)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            HistoryOrderListQuery.pack_req,
            HistoryOrderListQuery.unpack_rsp)

        kargs = {
            'status_filter_list': status_filter_list,
            'code': str(stock_code),
            'start': str(start) if start else "",
            'end': str(end) if end else "",
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'order_market': order_market
        }
        ret_code, msg, order_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "code", "stock_name", "order_market", "trd_side", "order_type", "order_status",
            "order_id", "qty", "price", "create_time", "updated_time",
            "dealt_qty", "dealt_avg_price", "last_err_msg", "remark",
            "time_in_force", "fill_outside_rth", "session", "aux_price", "trail_type", "trail_value",
            "trail_spread", "currency",
        ]
        order_list_table = pd.DataFrame(order_list, columns=col_list)

        return RET_OK, order_list_table

    def order_fee_query(self, order_id_list=[], trd_env=TrdEnv.REAL, acc_id=0, acc_index=0):
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        if order_id_list is not None and not isinstance(order_id_list, list):
            return RET_ERROR, 'order_id_list type error'

        query_processor = self._get_sync_query_processor(
            OrderFeeQuery.pack_req,
            OrderFeeQuery.unpack_rsp)

        kargs = {
            'order_id_list': order_id_list,
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id()
        }

        ret_code, msg, order_fee_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "order_id", "fee_amount", "fee_details",
        ]
        order_fee_list_table = pd.DataFrame(order_fee_list, columns=col_list)

        return RET_OK, order_fee_list_table

    def history_deal_list_query(self, code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, deal_market= TrdMarket.NONE):

        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret, msg, stock_code = self._check_stock_code(code)
        if ret != RET_OK:
            return ret, msg

        ret, msg, start, end = normalize_start_end_date(start, end, 90)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(
            HistoryDealListQuery.pack_req,
            HistoryDealListQuery.unpack_rsp)

        kargs = {
            'code': str(stock_code),
            'start': str(start) if start else "",
            'end': str(end) if end else "",
            'trd_mkt': acc_auth_list[0],
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id(),
            'deal_market': deal_market
        }
        ret_code, msg, deal_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "code", "stock_name", "deal_market", "deal_id", "order_id", "qty", "price",
            "trd_side", "create_time", "counter_broker_id", "counter_broker_name", 'status'
        ]
        deal_list_table = pd.DataFrame(deal_list, columns=col_list)

        return RET_OK, deal_list_table

    def acctradinginfo_query(self, order_type, code, price, order_id=None, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0):
        """
        查询账户下最大可买卖数量
        :param order_type: 订单类型，参见OrderType
        :param code: 证券代码，例如'HK.00700'
        :param price: 报价，3位精度
        :param order_id: 订单号。如果是新下单，则可以传None。如果是改单则要传单号。
        :param adjust_limit: 调整方向和调整幅度百分比限制，正数代表向上调整，负数代表向下调整，具体值代表调整幅度限制，如：0.015代表向上调整且幅度不超过1.5%；-0.01代表向下调整且幅度不超过1%。默认0表示不调整
        :param trd_env: 交易环境，参见TrdEnv
        :param acc_id: 业务账号，默认0表示第1个
        :param acc_index: int，交易业务子账户ID列表所对应的下标，默认0，表示第1个业务ID
        :return: (ret, data)

                ret == RET_OK, data为pd.DataFrame，数据列如下

                ret != RET_OK, data为错误信息

                =======================   ===========   ======================================================================================
                参数                       类型                        说明
                =======================   ===========   ======================================================================================
                max_cash_buy               float            不使用融资，仅自己的现金最大可买整手股数
                max_cash_and_margin_buy    float            使用融资，自己的现金 + 融资资金总共的最大可买整手股数
                max_position_sell          float            不使用融券(卖空)，仅自己的持仓最大可卖整手股数
                max_sell_short             float            使用融券(卖空)，最大可卖空整手股数，不包括多仓
                max_buy_back               float            卖空后，需要买回的最大整手股数。因为卖空后，必须先买回已卖空的股数，还掉股票，才能再继续买多。
                =======================   ===========   ======================================================================================
        """
        ret, msg = self._check_trd_env(trd_env)
        if ret != RET_OK:
            return ret, msg

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        ret, content = self._split_stock_code(code)
        if ret != RET_OK:
            return ret, content

        market_str, stock_code = content

        trd_market = self._get_trd_market_from_market(market_str, trd_env, self.__trd_category)

        query_processor = self._get_sync_query_processor(
            AccTradingInfoQuery.pack_req,
            AccTradingInfoQuery.unpack_rsp)

        kargs = {
            'order_type': order_type,
            'code': str(stock_code),
            'price': price,
            'order_id': order_id,
            'adjust_limit': adjust_limit,
            'trd_mkt': trd_market,
            'sec_mkt_str': market_str,
            'trd_env': trd_env,
            'acc_id': acc_id,
            'conn_id': self.get_sync_conn_id()
        }

        ret_code, msg, data = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = ['max_cash_buy', 'max_cash_and_margin_buy', 'max_position_sell', 'max_sell_short', 'max_buy_back',
                    'long_required_im', 'short_required_im']
        acctradinginfo_table = pd.DataFrame(data, columns=col_list)
        return RET_OK, acctradinginfo_table

    def get_margin_ratio(self, code_list):
        code_list = unique_and_normalize_list(code_list)
        if not code_list:
            error_str = ERROR_STR_PREFIX + "the type of code param is wrong"
            return RET_ERROR, error_str

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(TrdEnv.REAL, 0, 0)
        if ret != RET_OK:
            return ret, msg

        ret, content = self._split_stock_code(code_list[0])
        if ret != RET_OK:
            return ret, content

        market_str, stock_code = content

        trd_market = self._get_trd_market_from_market(market_str, TrdEnv.REAL, self.__trd_category)

        query_processor = self._get_sync_query_processor(
            MarginRatio.pack_req, MarginRatio.unpack_rsp)
        kargs = {
            "code_list": code_list,
            "conn_id": self.get_sync_conn_id(),
            "acc_id": acc_id,
            'trd_mkt': trd_market,
        }

        ret_code, msg, margin_ratio_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "code", "is_long_permit", "is_short_permit", "short_pool_remain", "short_fee_rate", "alert_long_ratio",
            "alert_short_ratio", "im_long_ratio", "im_short_ratio", "mcm_long_ratio", 'mcm_short_ratio', "mm_long_ratio", 'mm_short_ratio'
        ]
        margin_ratio_table = pd.DataFrame(margin_ratio_list, columns=col_list)

        return RET_OK, margin_ratio_table

    def get_acc_cash_flow(self, clearing_date='', trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, cashflow_direction=CashFlowDirection.NONE):

        ret, msg, acc_id, acc_auth_list = self._check_acc_id_and_acc_index(trd_env, acc_id, acc_index)
        if ret != RET_OK:
            return ret, msg

        query_processor = self._get_sync_query_processor(FlowSummary.pack_req, FlowSummary.unpack_rsp)
        kargs = {
            "conn_id": self.get_sync_conn_id(),
            "acc_id": acc_id,
            "trd_mkt": acc_auth_list[0],
            "clearing_date": clearing_date,
            "direction": cashflow_direction,
            "trd_env" : trd_env,
        }

        ret_code, msg, flow_summary_list = query_processor(**kargs)
        if ret_code != RET_OK:
            return RET_ERROR, msg

        col_list = [
            "cashflow_id", "clearing_date", "settlement_date", "currency", "cashflow_type", "cashflow_direction", "cashflow_amount", "cashflow_remark",
        ]
        flow_summary_table = pd.DataFrame(flow_summary_list, columns=col_list)

        return RET_OK, flow_summary_table

# 港股交易接口
class OpenHKTradeContext(OpenTradeContextBase):
    def __init__(self, host="127.0.0.1", port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES):
        super(OpenHKTradeContext, self).__init__(TrdMarket.HK, host, port, is_encrypt=is_encrypt, security_firm=security_firm, trd_category=TrdCategory.SECURITY)


# 美股交易接口
class OpenUSTradeContext(OpenTradeContextBase):
    def __init__(self, host="127.0.0.1", port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES):
        super(OpenUSTradeContext, self).__init__(TrdMarket.US, host, port, is_encrypt=is_encrypt, security_firm=security_firm, trd_category=TrdCategory.SECURITY)


# A股通交易接口
class OpenHKCCTradeContext(OpenTradeContextBase):
    def __init__(self, host="127.0.0.1", port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES):
        super(OpenHKCCTradeContext, self).__init__(TrdMarket.HKCC, host, port, is_encrypt=is_encrypt, security_firm=security_firm, trd_category=TrdCategory.SECURITY)


# A股交易接口
class OpenCNTradeContext(OpenTradeContextBase):
    def __init__(self, host="127.0.0.1", port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES):
        super(OpenCNTradeContext, self).__init__(TrdMarket.CN, host, port, is_encrypt=is_encrypt, security_firm=security_firm, trd_category=TrdCategory.SECURITY)


# 期货交易接口
class OpenFutureTradeContext(OpenTradeContextBase):
    def __init__(self, host="127.0.0.1", port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES):
        super(OpenFutureTradeContext, self).__init__(TrdMarket.FUTURES, host, port, is_encrypt=is_encrypt, security_firm=security_firm, trd_category=TrdCategory.FUTURE)


# 证券市场交易对象
class OpenSecTradeContext(OpenTradeContextBase):
    def __init__(self, filter_trdmarket=TrdMarket.HK, host='127.0.0.1', port=11111, is_encrypt=None, security_firm=SecurityFirm.FUTUSECURITIES):
        super(OpenSecTradeContext, self).__init__(filter_trdmarket, host, port, is_encrypt=is_encrypt, security_firm=security_firm, trd_category=TrdCategory.SECURITY, need_general_sec_acc=True)
