#!python3
import requests
import json
import hmac
import hashlib
import time
from datetime import datetime

from ..common.const import GMOConst
from ..common.exception import GmoCoinException
from ..common.logging import get_logger, log
from ..common.dto import Symbol
from .dto import GetMarginResSchema, GetMarginRes, GetAssetsResSchema, GetAssetsRes,\
    GetActiveOrdersResSchema, GetActiveOrdersRes


logger = get_logger()


class Client:
    '''
    GMOCoinのプライベートAPIクライアントクラスです。
    '''

    @log(logger)
    def __init__(self, api_key: str, secret_key: str):
        """
        コンストラクタです。

        Args:
            api_key:
               APIキーを設定します。

            secret_key:
                APIシークレットを設定します。
        """
        self._api_key = api_key
        self._secret_key = secret_key

    @log(logger)
    def get_margin(self) -> GetMarginRes:
        """
        余力情報を取得します。

        Args:
            なし

        Returns:
            GetMarginRes
        """

        path = '/v1/account/margin'

        headers = self._create_header(method='GET', path=path)

        response = requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers)
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetMarginResSchema().load(response.json())

    @log(logger)
    def get_assets(self) -> GetAssetsRes:
        """
        資産残高を取得します。

        Args:
            なし

        Returns:
            GetAssetsRes
        """

        path = '/v1/account/assets'

        headers = self._create_header(method='GET', path=path)

        response = requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers)
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetAssetsResSchema().load(response.json())

    @log(logger)
    def get_active_orders(self, symbol:Symbol, page:int=1, count:int=100) -> GetActiveOrdersRes:
        """
        有効注文一覧を取得します。
        対象: 現物取引、レバレッジ取引。

        Args:
            symbol:
                BTC ETH BCH LTC XRP BTC_JPY ETH_JPY BCH_JPY LTC_JPY XRP_JPY
            page:
                取得対象ページ: 指定しない場合は1を指定したとして動作する。
            count:
                1ページ当りの取得件数: 指定しない場合は100(最大値)を指定したとして動作する。

        Returns:
            GetActiveOrdersRes
        """

        path = '/v1/activeOrders'

        headers = self._create_header(method='GET', path=path)
        parameters = {
            "symbol": symbol.value,
            "page": page,
            "count": count
        }

        response = requests.get(GMOConst.END_POINT_PRIVATE + path, headers=headers, params=parameters)
        if response.status_code != 200:
            raise GmoCoinException(response.status_code)
        return GetActiveOrdersResSchema().load(response.json())

    @log(logger)
    def _create_header(self, method :str, path :str) -> dict:
        """
        ヘッダーを生成します。

        Args:
            method:
                HTTPメソッドを指定します。
            path:
                url(private以下)を指定します。

        Returns:
            header
        """
        timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))

        text = timestamp + method + path
        sign = hmac.new(bytes(self._secret_key.encode('ascii')), bytes(text.encode('ascii')), hashlib.sha256).hexdigest()
        headers = {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign
        }

        return headers