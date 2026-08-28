# Apify凭证与额度预检

仅在执行Apify渠道时读取。本预检的目标是区分本地凭证发现、Token认证、权限、网络传输和Actor额度问题；不得显示、记录或提交Token本身。

## 凭证来源

按以下优先级读取第一个非空值：

1. 当前进程环境变量`APIFY_TOKEN`；
2. Windows用户环境变量`APIFY_TOKEN`；
3. 仓库根目录、已被`.gitignore`排除的`.env.local`。

若多个来源同时存在，只比较长度和SHA-256短指纹，确认它们是否一致；不要输出Token。仓库、日志、Adapter结果和最终报告均不得包含Token或Authorization header。

## 在线预检

在运行收费或受配额限制的Actor之前，用所选Token请求：

`GET https://api.apify.com/v2/users/me`

- HTTP 200：Token有效，可以继续。
- HTTP 401：Token无效、已撤销或已到期。
- HTTP 403：Token有效但权限不足。
- 没有HTTP状态码：按网络、代理或TLS故障处理，不得表述为Token失效。

Windows PowerShell 5.1不支持`[SHA256]::HashData()`和`[Convert]::ToHexString()`；诊断命令必须使用兼容实现，或只比较存在性、长度与字符串相等性。

## Actor结果判定

Actor运行状态`SUCCEEDED`不等于取得可用商品。读取默认Dataset并分别记录：

- 技术执行状态；
- 原始记录数；
- 相关候选数；
- 错误记录，例如`free_tier_exhausted`；
- 商品详情和SKU是否锁定。

`free_tier_exhausted`表示Actor或套餐额度不足，与API Token认证无关。此时保留已成功取得的候选，整体状态保持`PARTIAL`，列出未完成店铺，不要要求用户无意义地重建Token。

## 退出条件

只有`users/me`返回200、Actor Dataset包含商品级记录且目标SKU已锁定时，才能把价格标为API已验证。搜索展示价、错误记录或未锁SKU不得替代正式可比价。
