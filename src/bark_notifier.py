import requests
import json
from typing import Optional
from .config import Config

class BarkNotifier:
    """Bark推送通知器"""
    
    def __init__(self, bark_url: str = None):
        """
        初始化Bark通知器
        
        Args:
            bark_url: Bark服务器URL，如果未提供则从环境变量获取
        """
        self.bark_url = bark_url or Config.BARK_URL
        if not self.bark_url:
            raise ValueError("BARK_URL不能为空，请设置环境变量或传入参数")
    
    def send_notification(self, title: str, body: str, 
                         group: str = "Stock", 
                         icon: str = None,
                         sound: str = "default",
                         badge: int = None) -> bool:
        """
        发送Bark通知
        
        Args:
            title: 通知标题
            body: 通知内容
            group: 分组名称
            icon: 图标URL
            sound: 提示音
            badge: 角标数字
            
        Returns:
            发送成功返回True，否则返回False
        """
        try:
            payload = {
                "title": title,
                "body": body,
                "group": group,
                "sound": sound
            }
            
            if icon:
                payload["icon"] = icon
            if badge is not None:
                payload["badge"] = badge
            
            # 构建完整的URL
            url = f"{self.bark_url}/{title}/{body}"
            
            response = requests.post(
                self.bark_url,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    print(f"Bark通知发送成功: {title}")
                    return True
                else:
                    print(f"Bark通知发送失败: {result.get('message', '未知错误')}")
                    return False
            else:
                print(f"Bark请求失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"Bark通知发送异常: {e}")
            return False
    
    def send_stock_notification(self, content: str, market_type: str) -> bool:
        """
        发送股票数据通知
        
        Args:
            content: 通知内容
            market_type: 市场类型 ('us' 或 'cn')
            
        Returns:
            发送成功返回True，否则返回False
        """
        title = "美股数据推送" if market_type == 'us' else "A股数据推送"
        group = "美股监控" if market_type == 'us' else "A股监控"
        
        # 添加一些视觉效果的图标
        icon = "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f4c8.png"
        
        return self.send_notification(
            title=title,
            body=content,
            group=group,
            icon=icon
        )
