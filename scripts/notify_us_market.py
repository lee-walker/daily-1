#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import traceback

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.scraper import MarketDataScraper
    from src.bark_notifier import BarkNotifier
    from src.config import Config

    def main():
        bark_url = os.environ.get('BARK_URL')
        if not bark_url:
            print('❌ BARK_URL环境变量未设置')
            sys.exit(1)
        
        # 检查是否为交易日
        if not MarketDataScraper.is_trading_day():
            print('ℹ️ 今天不是交易日，跳过推送')
            sys.exit(0)
        
        # 获取美股数据
        print('📥 正在获取美股数据...')
        us_data = MarketDataScraper.get_us_market_data(Config.US_INDICES)
        
        if not us_data:
            print('❌ 未能获取到美股数据')
            sys.exit(1)
        
        # 格式化数据
        content = MarketDataScraper.format_market_data(us_data, 'us')
        print('📄 格式化后的数据:')
        print(content)
        
        # 发送推送
        notifier = BarkNotifier(bark_url)
        success = notifier.send_stock_notification(content, 'us')
        
        if success:
            print('✅ 美股数据推送成功')
            sys.exit(0)
        else:
            print('❌ 美股数据推送失败')
            sys.exit(1)
            
except Exception as e:
    print(f'❌ 执行过程中出现错误: {e}')
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    main()
