# 权威依据与检测工具

核查日期：2026-11-15。规则版本 1.0.0。规范、指标、工具与自定义方法需要区分：工具提供证据，不自动决定作品质量。

## 优先推荐给作者的入口

| 入口 | 提供者/性质 | 适合看什么 | 不能证明什么 |
| --- | --- | --- | --- |
| [PageSpeed Insights](https://pagespeed.web.dev/) | Google，在线诊断工具 | 移动/桌面 Lighthouse；有足够数据时的真实用户 CWV | 全部功能、整体安全、真实用户满意、所有页面体验 |
| 浏览器 DevTools 的 Lighthouse | Chrome 内置，本地自动检查 | 性能、部分可访问性、最佳实践、部分 SEO | 分数 100 不能代替人工与业务测试；不同版本和环境不能直接排名 |
| [WAVE](https://wave.webaim.org/) | WebAIM，可访问性评估工具 | 页面错误与可见结构线索，辅助人工检查 | 不能独自证明完整 WCAG AA 符合性 |
| [MDN HTTP Observatory](https://developer.mozilla.org/en-US/observatory) | MDN，HTTP 安全配置扫描 | 响应策略、安全特性与配置建议 | A+ 不代表无漏洞；不覆盖全部 TLS、业务和密码存储安全；历史可能公开 |
| [Qualys SSL Labs](https://www.ssllabs.com/ssltest/) | Qualys，TLS 服务器测试 | 证书链、TLS 协议和配置 | 应用鉴权、数据正确性及整体安全；不擅自提交私有目标 |
| [Nu HTML Checker](https://validator.w3.org/nu/) | W3C HTML 检查服务 | HTML 语法、结构和一致性问题线索 | 不等于可用性/设计质量评分；警告数量不直接作为扣分 |

在线服务可能收到并保存目标 URL/域名；不要替用户上传源码、秘密或私有链接。当前表是工具能力介绍，不意味着已把某站提交给这些服务扫描。免费额度、队列、可用性和输出可能变化，使用时核查官方说明。

## 关键数值与权威来源

### Core Web Vitals

[Web Vitals](https://web.dev/articles/vitals) 与 [PSI 文档](https://developers.google.com/speed/docs/insights/v5/about)：

- LCP 良好 ≤2.5 秒，需改进 >2.5–4 秒，差 >4 秒。
- INP 良好 ≤200 毫秒，需改进 >200–500 毫秒，差 >500 毫秒。
- CLS 良好 ≤0.1，需改进 >0.1–0.25，差 >0.25。
- 看真实用户访问第 75 百分位，移动/桌面分别报告；三项都良好才对应范围通过。
- PSI 的 CrUX field 数据是过去 28 天窗口；URL 数据不足时可能回退 origin，必须注明层级；两者不足时没有真实用户结论。
- TBT 是实验室阻塞诊断指标，不是 INP。用交互 trace 测一个样本也不是完整真实用户 p75。
- Lighthouse 常见档位 90–100、50–89、0–49 只属于相应工具类别，不转换为作品总质量等级。新版本指标/权重会变，记录版本。

### WCAG 2.2

规范：[WCAG 2.2](https://www.w3.org/TR/WCAG22/)。AA 要满足适用的 A 和 AA 全部成功标准及符合性要求，完整流程需要覆盖。

- [文字对比度 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)：普通文字 ≥4.5:1，大字 ≥3:1；大字为 18pt 普通/14pt 粗体。非文本控件按 1.4.11 另判，例外按原文。
- [重排 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)：垂直内容 320 CSS px 宽时保留信息/功能且无需二维滚动，必要二维内容等有例外。
- [文字放大 1.4.4](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html)：200% 无功能/内容损失，有条款例外；浏览器整体缩放不等于已经充分检查所有文本放大场景。
- [目标尺寸 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)：24×24 CSS px 或符合间距/内联/等价控件等例外；不能自动把所有小链接都判失败。
- [可见标签与名称 2.5.3](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name)：可访问名称需包含构成可见标签的文字，复杂卡片要先判断什么是标签。
- 键盘、无陷阱、焦点可见、语义/标签/错误说明，见 rubric 指定条款。

[W3C 评估说明](https://www.w3.org/WAI/test-evaluate/)明确自动工具无法独自确定符合性。axe/WAVE/Lighthouse 都是辅助工具。

### 安全与后端可靠性

- [OWASP ASVS](https://asvs.owasp.org/)：查阅时稳定版为 5.0.0（2025-05-30）；深检选择适用要求，引用需带版本，没逐条执行不说“ASVS 通过”。
- [OWASP API1:2023](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)：对象及操作权限在服务端检验，不能靠隐藏 UI。
- [OWASP HTTP Headers](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)：按保护目的解释；CSP frame-ancestors 与 XFO 有覆盖关系。
- [CSP 指南](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)：适配内联脚本、资源及 nonce/hash；不复制一段策略就承诺安全。新策略可先 Report-Only 观察，但这不等于已强制保护。
- [Google SRE SLO](https://sre.google/workbook/implementing-slos/)：围绕关键用户旅程选择正确性、可用性与延迟目标；没有适用所有网站的固定延迟和 99.9% 要求。

### 理解、交互与视觉

参考 [Nielsen 十条可用性启发式](https://www.nngroup.com/articles/ten-usability-heuristics/)：状态可见、贴近用户、用户控制、一致性、错误预防、识别优先、效率、简洁、错误恢复、帮助。

这是专家评估依据，不是每项都有官方分数阈值。C/V/F 的具体操作规则由本 skill 制定：给场景、截图、影响与验收任务，允许作者依据用途解释有意取舍。实际用户测试是另一种证据。

## 执行工具建议

- 浏览器自动化/已有浏览器工具：公开导航、截图、键盘、状态检查；先盘点能力，不假定某个 MCP/命令存在。
- axe-core / axe DevTools：部分 WCAG 规则；保留 incomplete 项，不能把它们当通过。
- Lighthouse CLI/DevTools：本地报告；独立环境安装、记录版本与参数，不依赖作者框架。
- curl 或等价 HTTP 工具：状态、跳转、响应策略；当前请求协议不能代表所有地区边缘能力。
- Playwright/Puppeteer 或人工真机：实际任务与多尺寸；桌面模拟手机不是真实移动设备测试。
- 仓库测试/集成测试/受控容量工具：只在深检授权范围使用。测试覆盖率不是业务正确性证明。

## 已知误用与版本陷阱

- [Chrome bfcache 更新](https://developer.chrome.com/docs/web-platform/bfcache-ccns)：部分 no-store 页面可进入 bfcache，不能永久硬编码“no-store 必失败”。按本次实际原因报告。
- [Next.js 15 数据安全](https://nextjs.org/docs/15/app/guides/data-security)：Server Actions 可通过 POST 执行；无 app/api 不证明无服务端能力。
- [Lighthouse 可访问性评分](https://developer.chrome.com/docs/lighthouse/accessibility/scoring)：人工审计不纳入分数，100 也不是完整可访问。
- 安全头计数、HTML 警告数、unused JS 估算不能等权扣总分；重复估算不能相加成实际收益。

## 来源获取与维护

本版结合 2026-11-11 的官方资料核查及网站实测；2026-11-15 再次通过官方域名搜索核查 CWV、WCAG 数值、ASVS、PSI 数据窗及 Observatory 边界。部分正文抓取被当前网络限制，不能称逐页完整审阅。WAVE 作为工具入口列出，其完整能力未在本轮实测；SSL Labs 同样未对目标实际提交扫描。

执行时发现版本或工具行为变化，核查官方文档并记录差异；不要自动改规则版本。规则维护者审核后更新版本、日期与变更记录。
