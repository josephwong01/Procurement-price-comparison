# Apify 连接常见问题

## 现象

采购比价 Skill 已成功下载，`APIFY_TOKEN` 也存在，但当前会话找不到 Apify、Actor 或 Dataset 工具，或误报 Chrome Native Host 缺失。

## 根因判断

`APIFY_TOKEN`、采购 Skill、Apify 工具通道是三个独立层次：

1. `APIFY_TOKEN` 只是 Apify 凭证；
2. Skill 只包含采购流程、Schema、评分和输出规则；
3. Apify 工具通道决定 Codex 是否能直接调用 Actor/Dataset。

缺少 Chrome Native Host 不等于 Apify 或 MCP 故障。只要 Codex 内置浏览器能够打开并登录 Apify Console，就可以通过网页运行 Actor、查看 Runs 和 Dataset；这条路径不依赖本机 Chrome 扩展的 Native Host。

## 推荐排查顺序

1. 先检查当前会话工具列表是否实际出现 Apify、Actor 或 Dataset 工具。
2. 若没有，检查 Codex 内置浏览器是否能访问 `https://console.apify.com/` 并显示已登录。
3. 若已登录，可在 Console 中运行授权的 Actor，并记录运行 ID、Dataset、状态、费用和采集时间。
4. 若未登录，提示用户在内置浏览器中手动登录；不要索取或显示密码、Token、Cookie。
5. 只有在 Token 本身返回 401/撤销/过期时，才排查 Token；不要因为工具未加载而反复重配 Token。

## 防止死循环

- 不要把“Skill 已下载”当成“Apify 已连接”。
- 不要把“Chrome Native Host 缺失”当成“Apify Token 失效”。
- 不要为访问 Apify Console 申请 Google 权限。
- 工具通道不存在时，不要重复运行 Actor、重复配置 Token 或修改采购文件。
- 报告必须区分：工具未加载、Console 未登录、Actor/API 受限、Actor 运行成功但结果为空。

## 记录要求

每次 Apify 运行保留 Actor 名称、运行 ID、Dataset ID、运行状态、费用、结果数量和采集时间；禁止保存 Token、Cookie 或授权请求头。
