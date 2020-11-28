#!python3
from enum import Enum
from marshmallow import Schema, fields, post_load
# from datetime import datetime


class Status(Enum):
    """
    GMOサーバの状態を示します。
    """
    MAINTENANCE = 'MAINTENANCE'
    PREOPEN = 'PREOPEN'
    OPEN = 'OPEN'


class Symbol(Enum):
    """
    銘柄種別を示します。
    """
    BTC = 'BTC'
    ETH = 'ETH'
    BCH = 'BCH'
    LTC = 'LTC'
    XRP = 'XRP'
    BTC_JPY = 'BTC_JPY'
    ETH_JPY = 'ETH_JPY'
    BCH_JPY = 'BCH_JPY'
    LTC_JPY = 'LTC_JPY'
    XRP_JPY = 'XRP_JPY'


class AssetSymbol(Enum):
    """
    資産銘柄種別を示します。
    """
    BTC = 'BTC'
    ETH = 'ETH'
    BCH = 'BCH'
    LTC = 'LTC'
    XRP = 'XRP'
    JPY = 'JPY'
    XEM = 'XEM'
    XLM = 'XLM'
    BAT = 'BAT'
    OMG = 'OMG'


class SalesSide(Enum):
    """
    売買種別を示します。
    """
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(Enum):
    """
    取引区分を示します。
    """
    NORMAL = 'NORMAL'
    LOSSCUT = 'LOSSCUT'


class ExecutionType(Enum):
    """
    注文タイプを示します。
    """
    MARKET = 'MARKET'
    LIMIT = 'LIMIT'
    STOP = 'STOP'


class SettleType(Enum):
    """
    決済区分を示します。
    """
    OPEN = 'OPEN'
    CLOSE = 'CLOSE'

class OrderStatus(Enum):
    """
    注文ステータスを示します。
    """
    WAITING = 'WAITING'
    ORDERED = 'ORDERED'
    MODIFYING = 'MODIFYING'
    CANCELLING = 'CANCELLING'
    CANCELED = 'CANCELED'
    EXECUTED = 'EXECUTED'
    EXPIRED = 'EXPIRED'


class TimeInForce(Enum):
    """
    執行数量条件を示します。
    """
    FAK = 'FAK'
    FAS = 'FAS'
    FOK = 'FOK'
    SOK = 'SOK'


class BaseSchema(Schema):
    """
    ベーススキーマクラスです。
    """
    __model__ = None

    @post_load
    def to_dto(self, data, **_):
        """
        dto変換関数です。

        Args:
            data
            **_

        """
        return self.__model__(**data)

    class Meta:
        """
        ベーススキーマメタクラスです。
        """
        ordered = True


class BaseResponse:
    """
    ベースレスポンスクラスです。
    """
    def __init__(self, status: int, responsetime: str) -> None:
        """
        コンストラクタです。

        Args:
            status:
                ステータスコードを設定します。
            responsetime :
                レスポンスタイムを設定します。
        """
        self.status = status
        self.responsetime = responsetime


class BaseResponseSchema(BaseSchema):
    """
    ベースレスポンススキーマクラスです。
    """
    __model__ = BaseResponse
    status = fields.Int(data_key='status')
    # responsetime = fields.DateTime(format='%Y-%m-%dT%H:%M:%S.%fZ', data_key='responsetime')
    responsetime = fields.Str(data_key='responsetime')
