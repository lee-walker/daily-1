import os
from typing import Dict, List

class Config:
    # Bark推送配置
    BARK_URL = os.getenv('BARK_URL', '')
    
    # 美股主要指数
    US_INDICES = [
        '^DJI',      # 道琼斯工业平均指数
        '^IXIC',     # 纳斯达克综合指数
        '^GSPC',     # 标普500指数
    ]
    
    # 国内主要指数
    CN_INDICES = [
        '000001.SS',  # 上证指数
        '000300.SS',  # 沪深300
        '510050.SS',  # 上证50
    ]
    
    # 指数名称映射
    INDEX_NAMES = {
        '^DJI': '道琼斯工业平均指数',
        '^IXIC': '纳斯达克综合指数',
        '^GSPC': '标普500指数',
        '000001.SS': '上证指数',
        '000300.SS': '沪深300',
        '510050.SS': '上证50',
    }
    
    @classmethod
    def get_index_name(cls, symbol: str) -> str:
        return cls.INDEX_NAMES.get(symbol, symbol)
