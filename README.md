# 数据推送系统

一个基于GitHub Actions的自动化股市数据推送系统，支持美股和A股市场数据获取并通过Bark进行推送通知。

## 功能特性

- 📈 **美股数据获取**：自动获取主要美股指数数据（道琼斯、纳斯达克、标普500）
- 🇨🇳 **A股数据获取**：自动获取主要A股指数数据（上证指数、深证成指、创业板指）
- ⏰ **定时推送**：根据设定的时间自动执行数据获取和推送
- 🔔 **Bark推送**：通过Bark应用接收推送通知
- 📅 **交易日判断**：自动识别并跳过非交易日
- ☁️ **云端运行**：基于GitHub Actions，无需本地服务器

## 项目结构

```
project/
├── src/                    # 核心源码
│   ├── __init__.py
│   ├── scraper.py         # 数据抓取模块
│   ├── bark_notifier.py   # Bark推送模块
│   └── config.py          # 配置文件
├── scripts/               # 执行脚本
│   ├── __init__.py
│   ├── notify_us_market.py # 美股推送脚本
│   └── notify_cn_market.py # A股推送脚本
├── requirements.txt       # Python依赖
└── .github/workflows/     # GitHub Actions工作流
    ├── us_market.yml      # 美股推送工作流
    └── cn_market.yml      # A股推送工作流
```

## 安装配置

### 1. Fork本项目

点击右上角的"Fork"按钮，将项目复制到你的GitHub账户下。

### 2. 配置Bark URL密钥

1. 在你的Fork项目中，进入 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 添加以下密钥：
   - **Name**: `BARK_URL`
   - **Value**: 你的Bark推送URL（格式：`https://api.day.app/你的密钥`）

### 3. 启用GitHub Actions

默认情况下，Fork的项目会自动启用GitHub Actions。如果没有，请手动启用：
1. 进入 **Actions** 选项卡
2. 点击 **I understand my workflows, go ahead and enable them**

## 使用说明

### 推送时间安排

- **美股推送**：周一至周五 UTC时间 22:00（北京时间次日 6:00）
- **A股推送**：周一至周五 UTC时间 07:10（北京时间 15:10）

> 注意：系统会自动跳过法定节假日和周末等非交易日。

### 手动触发推送

你可以随时手动触发推送：
1. 进入 **Actions** 选项卡
2. 选择对应的工作流（US Market Data Notification 或 CN Market Data Notification）
3. 点击 **Run workflow** → **Run workflow**

## 技术细节

### 依赖库

- `yfinance`: Yahoo Finance数据获取
- `requests`: HTTP请求处理
- `numpy`: 数值计算
- `pandas`: 数据处理

### 数据来源

- 美股数据：Yahoo Finance
- A股数据：Yahoo Finance

### 推送格式

推送消息包含以下信息：
- 指数名称
- 当前点位
- 涨跌幅
- 涨跌点数

示例：
```
📈 道琼斯工业平均指数
📊 点位: 35,000.00
📊 涨幅: +1.20%
📊 涨跌: +420.00
```

## 自定义配置

### 修改推送时间

编辑 `.github/workflows/` 中的YAML文件，修改 `cron` 表达式：

```yaml
# cron格式: 分 时 日 月 周
schedule:
  - cron: '0 22 * * 0-4'  # UTC时间 22:00，周日至周四
```

### 添加自定义指数

编辑 `src/config.py` 文件中的指数列表：

```python
US_INDICES = ['^DJI', '^IXIC', '^GSPC']  # 可添加更多美股指数
CN_INDICES = ['000001.SS', '399001.SZ', '399006.SZ']  # 可添加更多A股指数
```

常见指数代码：
- 美股：
  - `^DJI`: 道琼斯工业平均指数
  - `^IXIC`: 纳斯达克综合指数
  - `^GSPC`: 标普500指数
  - `^RUT`: 罗素2000指数

- A股：
  - `000001.SS`: 上证指数
  - `399001.SZ`: 深证成指
  - `399006.SZ`: 创业板指
  - `000300.SS`: 沪深300

## 故障排除

### 推送失败

1. 检查Bark URL是否正确配置
2. 查看GitHub Actions日志了解具体错误
3. 确认网络连接正常

### 数据获取失败

1. 检查Yahoo Finance服务是否正常
2. 确认指数代码是否正确
3. 查看是否触发了API限制

### 非交易日推送

系统内置交易日判断逻辑，会自动跳过：
- 周末（周六、周日）
- 法定节假日
- 特殊休市日

**注意**：本项目仅供学习交流使用，投资有风险，入市需谨慎！
