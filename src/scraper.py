import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple
from .config import Config

class MarketDataScraper:
    """市场数据抓取器"""
    
    @staticmethod
    def get_us_market_data(symbols: List[str]) -> List[Dict]:
        """
        获取美股市场数据
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            包含股票数据的字典列表
        """
        try:
            data = []
            stocks = yf.download(symbols, period="2d", group_by='ticker')
            
            if len(symbols) == 1:
                # 单个符号的情况
                symbol = symbols[0]
                stock_data = stocks
                if not stock_data.empty and len(stock_data) >= 1:
                    latest_data = stock_data.iloc[-1]
                    prev_data = stock_data.iloc[-2] if len(stock_data) >= 2 else latest_data
                    
                    close_price = latest_data['Close']
                    open_price = latest_data['Open']
                    prev_close = prev_data['Close']
                    
                    change = close_price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                    
                    data.append({
                        'symbol': symbol,
                        'name': Config.get_index_name(symbol),
                        'close': round(close_price, 2),
                        'open': round(open_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': int(latest_data['Volume']) if 'Volume' in latest_data else 0
                    })
            else:
                # 多个符号的情况
                for symbol in symbols:
                    if symbol in stocks.columns.levels[0]:
                        stock_data = stocks[symbol]
                        if not stock_data.empty and len(stock_data) >= 1:
                            latest_data = stock_data.iloc[-1]
                            prev_data = stock_data.iloc[-2] if len(stock_data) >= 2 else latest_data
                            
                            close_price = latest_data['Close']
                            open_price = latest_data['Open']
                            prev_close = prev_data['Close']
                            
                            change = close_price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                            
                            data.append({
                                'symbol': symbol,
                                'name': Config.get_index_name(symbol),
                                'close': round(close_price, 2),
                                'open': round(open_price, 2),
                                'change': round(change, 2),
                                'change_percent': round(change_percent, 2),
                                'volume': int(latest_data['Volume']) if 'Volume' in latest_data else 0
                            })
            
            return data
        except Exception as e:
            print(f"获取美股数据时出错: {e}")
            return []
    
    @staticmethod
    def get_cn_market_data(symbols: List[str]) -> List[Dict]:
        """
        获取国内股市数据
        
        Args:
            symbols: 股票代码列表
            
        Returns:
            包含股票数据的字典列表
        """
        try:
            data = []
            stocks = yf.download(symbols, period="2d", group_by='ticker')
            
            if len(symbols) == 1:
                # 单个符号的情况
                symbol = symbols[0]
                stock_data = stocks
                if not stock_data.empty and len(stock_data) >= 1:
                    latest_data = stock_data.iloc[-1]
                    prev_data = stock_data.iloc[-2] if len(stock_data) >= 2 else latest_data
                    
                    close_price = latest_data['Close']
                    open_price = latest_data['Open']
                    prev_close = prev_data['Close']
                    
                    change = close_price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                    
                    data.append({
                        'symbol': symbol,
                        'name': Config.get_index_name(symbol),
                        'close': round(close_price, 2),
                        'open': round(open_price, 2),
                        'change': round(change, 2),
                        'change_percent': round(change_percent, 2),
                        'volume': int(latest_data['Volume']) if 'Volume' in latest_data else 0
                    })
            else:
                # 多个符号的情况
                for symbol in symbols:
                    if symbol in stocks.columns.levels[0]:
                        stock_data = stocks[symbol]
                        if not stock_data.empty and len(stock_data) >= 1:
                            latest_data = stock_data.iloc[-1]
                            prev_data = stock_data.iloc[-2] if len(stock_data) >= 2 else latest_data
                            
                            close_price = latest_data['Close']
                            open_price = latest_data['Open']
                            prev_close = prev_data['Close']
                            
                            change = close_price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close != 0 else 0
                            
                            data.append({
                                'symbol': symbol,
                                'name': Config.get_index_name(symbol),
                                'close': round(close_price, 2),
                                'open': round(open_price, 2),
                                'change': round(change, 2),
                                'change_percent': round(change_percent, 2),
                                'volume': int(latest_data['Volume']) if 'Volume' in latest_data else 0
                            })
            
            return data
        except Exception as e:
            print(f"获取国内股市数据时出错: {e}")
            return []
    
    @staticmethod
    def is_trading_day() -> bool:
        """
        判断是否为交易日（简单判断，实际应用中可能需要更精确的逻辑）
        这里简化处理，假设周一到周五都是交易日
        """
        today = datetime.now()
        weekday = today.weekday()  # 0=Monday, 6=Sunday
        return 0 <= weekday <= 4  # 周一到周五
    
    @staticmethod
    def format_market_data(data: List[Dict], market_type: str) -> str:
        """
        格式化市场数据为推送文本
        
        Args:
            data: 市场数据列表
            market_type: 市场类型 ('us' 或 'cn')
            
        Returns:
            格式化的文本字符串
        """
        if not data:
            return f"{market_type.upper()}市场数据获取失败"
        
        title = "美股收盘数据" if market_type == 'us' else "A股收盘数据"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        result = f"📊 {title}\n📈 更新时间: {current_time}\n\n"
        
        for item in data:
            name = item['name']
            close = item['close']
            change = item['change']
            change_percent = item['change_percent']
            
            # 判断涨跌颜色emoji
            emoji = "🔴" if change > 0 else "🟢" if change < 0 else "⚪"
            sign = "+" if change > 0 else "" if change < 0 else ""
            
            result += f"{emoji} {name}\n"
            result += f"  收盘: {close:,}\n"
            result += f"  涨跌: {sign}{change:.2f} ({sign}{change_percent:.2f}%)\n\n"
        
        return result.strip()
