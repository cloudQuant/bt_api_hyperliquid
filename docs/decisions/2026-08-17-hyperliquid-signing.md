# 决策：Hyperliquid 签名模式（B-12）

**日期**：2026-08-17
**状态**：已采纳（分支 A）

## 背景

`request_base.py` 当前状态：

- `self.private_key` 通过 `Account.from_key()` 加载为 Ethereum 账户，得到 `self.address` / `self.account`；
- 但请求路径中**没有任何 EIP-712 / sign_message 调用**——私钥仅用于派生 `address`（作为查询账户的 `user` 参数）；
- 实际发出的 HTTP 请求只使用 `X-API-Key` 头（vault/agent 模式，API wallet）；
- `request`/`async_request` 的 `is_sign` 参数被**完全忽略**（spot.py 传 `is_sign=True` 但签名不生效）。

即：私钥签名链路是"半成品/死代码"，下单实际依赖 X-API-Key 头。

## 决策

**分支 A：仅支持 vault/agent 模式（X-API-Key）。**

理由：

1. 当前代码实际只实现了 X-API-Key 头认证（vault/agent 模式），私钥加载未产生任何签名，属于误导性死代码。
2. 实现完整 EIP-712 签名（分支 B）需要 Hyperliquid 官方文档的 action 结构与签名规范；本环境无法访问官方文档，凭空实现错误签名的风险高于收益（错误签名会直接导致下单失败）。
3. 删除死代码 + 显式声明支持模式是诚实且保守的收敛，符合"最小改动"原则。

EIP-712 签名（分支 B）另立 backlog，待能访问官方文档时实现，黄金向量需官方示例私钥 + 期望签名复算。

## 执行内容

- 删除 `Account.from_key` 私钥加载死代码；`address` 改为从构造参数显式传入（默认空串）。
- 删除 `is_sign` 参数（request/async_request 及调用点）。
- 文档/声明：明确当前认证模式为 X-API-Key（vault/agent）。
