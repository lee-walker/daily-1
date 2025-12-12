#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import traceback

def main():
    try:
        # 添加项目根目录到Python路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        
        # 尝试导入模块
        from src.scraper import MarketDataScraper
        from src.bark_notifier import BarkNotifier
        from src.config import Config

        bark_url = os.environ.get('BARK_URL')
        if not bark_url:
            print('❌ BARK_URL环境变量未设置')
            sys.exit(1)
        
        # 检查是否为交易日
        if not MarketDataScraper.is_trading_day():
            print('ℹ️ 今天不是交易日，跳过推送')
            sys.exit(0)
        
        # 获取国内股市数据
        print('📥 正在获取A股数据...')
        cn_data = MarketDataScraper.get_cn_market_data(Config.CN_INDICES)
        
        if not cn_data:
            print('❌ 未能获取到A股数据')
            sys.exit(1)
        
        # 格式化数据
        content = MarketDataScraper.format_market_data(cn_data, 'cn')
        print('📄 格式化后的数据:')
        print(content)
        
        # 发送推送
        notifier = BarkNotifier(bark_url)
        success = notifier.send_stock_notification(content, 'cn')
        
        if success:
            print('✅ A股数据推送成功')
            sys.exit(0)
        else:
            print('❌ A股数据推送失败')
            sys.exit(1)
            
    except ImportError as e:
        print(f'❌ 导入模块失败: {e}')
        print("请确保所有依赖已正确安装")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f'❌ 执行过程中出现错误: {e}')
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
