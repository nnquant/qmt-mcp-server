# QMT-MCP-Server

赋予大模型执行股票交易的能力！

QMT-MCP-Server 是一个基于 MCP (Model Control Protocol) 的服务器应用，用于对接迅投 QMT 交易系统，提供股票交易相关的功能接口。

**本项目仅供交流学习使用，请谨慎用于实盘环境**

## 已实现功能

- 账户资产查询
- 持仓信息查询
- 下单
- 撤单

## 系统要求

- Python >= 3.10
- 开通QMT交易权限，且本地已启动miniqmt

## 安装说明
**使用前请先安装python包管理工具 uv**

安装方法请参考
https://docs.astral.sh/uv/getting-started/installation/#github-releases
1. 克隆项目到本地
```bash
git clone https://github.com/nnquant/qmt-mcp-server
```
2. 安装依赖：

```bash
uv sync
```
3. 运行项目
```bash
uv run main.py
```

## 配置说明

首次运行时，系统会提示输入必要的配置信息：
- MiniQMT 所在路径
- 资金账户

配置信息将自动保存在 `xttrader.yaml` 文件中。

## MCP使用技巧
1. 选择合适的MCP客户端，配置好MCP服务器，例如在Cursor中，配置如下：

```json
{
  "mcpServers": {
    "qmt-mcp-server": {
      "url": "http://localhost:8001/sse"
    }
  }
}
```

2. 指令案例
- 请帮我查询我的账户持仓
- 以10元的价格购买100股600000.SH股票
- 以11元的价格购买100股平安银行股票
  - **（由于不同大模型的差异，部分情况下可能无法正确转换股票名称到股票代码，使用股票名称下单请谨慎）**
- 以XX的价格为我购买20%可用仓位的XXXX股票
- 配合其他MCP服务完成选股交易的一条龙

## 注意事项

- 使用前请确保 MiniQMT 系统正常运行
- 交易前请仔细核对账户信息
- 所有股票代码需要包含交易所后缀（.SH 或 .SZ）
- 本程序仅用于交流和学习，请谨慎用于实盘，本人不承担任何使用者使用本程序所造成的损失