# kb-chat 严格执行追踪报告

测试对象：`../../fixtures/zx-bank-kb/`

测试题集：`zx-bank-kb-hard-rag-questions.md`

执行目标：严格按照 `kb-chat` Skill 的 6 个步骤，对 11 道复杂问题逐题作答，并记录每题的路由、章节定位、实际读取范围、correction 状态、答案、自检与标准答案对比。

执行时间：2026-08-10 08:22 北京时间开始。

## 执行口径

每道题均按以下流程记录：

1. Document routing：读取并使用 `../../fixtures/zx-bank-kb/.kb/manifest.json`，根据问题语义匹配 `domain/title/summary/tags`，选出相关文档。
2. Section localization：读取每个命中文档的 `.kb/index/<source-stem>/tree.json`，根据节点 `title/summary/keywords` 定位章节。
3. Content extraction：按 `tree.json` 中的 `start_line/end_line` 读取源 Markdown，必要时扩展到同级或父级行段。
4. Correction loading：检查 `.kb/memory/corrections/{doc_id}.jsonl`。本次知识库的 `corrections/` 目录为空，因此所有题均无 correction。
5. Generate answer：仅基于已读取源文档内容作答。
6. Self-verify：逐条核对答案断言是否有引用支撑，再与测试题标准答案比较。

说明：当前环境不暴露模型真实 API token 明细，因此本报告不声称拥有精确计费 token。若需要 token，可另行用日志层或 API 层统计；本报告只记录严格执行轨迹。

## 总体结果

| 题号 | 主要能力 | 事实答案 | 引用精度 | 备注 |
|---|---|---:|---:|---|
| Q1 | 多跳条件推理 | 通过 | 通过 | 信用卡资格、车贷利率、加入费均匹配 |
| Q2 | 账户转换链路 | 通过 | 通过 | 自动转换、最低余额、数字渠道和卡/支票簿保留均匹配 |
| Q3 | 跨国条件与否定推理 | 通过 | 通过 | 孟加拉贷款、利率对比、UPI 否定和替代渠道均匹配 |
| Q4 | 三跳数值提取 | 通过 | 通过 | LTV、尼泊尔 FD 起存、FD 抵押比例均匹配 |
| Q5 | ESG 跨文档综合 | 通过 | 通过 | 绿色金融、绿色家园、绿色商业贷款、FD ESG、女性赋权均识别 |
| Q6 | 多渠道枚举 | 通过 | 通过 | 欺诈冻结、解决时间、支票簿申请渠道均匹配 |
| Q7 | 服务可用性矩阵 | 通过 | 通过 | UPI、e-KYC、学生卡、跨境汇款国家判断均匹配 |
| Q8 | 集合比较 | 通过 | 小偏差 | 汽车贷款未单列 Address Proof，需按 KYC Documents 语义归纳 |
| Q9 | 时空交叉推理 | 通过 | 通过 | HITEC City 近邻分行、孟买 ATM、定位方式均匹配 |
| Q10 | 复合条件推理 | 通过 | 通过 | FD 利率、信用卡年龄边界、保险箱分行流程均匹配 |
| Q11 | NRI 跨国旅程 | 通过 | 通过 | 汇款时间、NRI 卡条件、WhatsApp Zia 均匹配 |

## Q1 多跳条件推理

问题：一位在德里工作的女性上班族，月收入 ₹30,000，年龄 28 岁，CIBIL 720。她想同时申请一张 ZX Bank 信用卡和一笔摩托车贷款。她有资格申请哪些信用卡？摩托车贷款的利率是多少？两张卡的加入费合计多少？

### Step 1 Document routing

读取 `manifest.json` 后，按问题中的“信用卡”“摩托车贷款”“收入/年龄/CIBIL/加入费/利率”路由到：

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `zx-bank-credit-card.md` | `doc_068` | 标题和摘要指向信用卡选项、费用和资格 |
| `zx-bank-bike-loan.md` | `doc_064` | 标题和摘要指向摩托车贷款利率与资格 |

未选择其他贷款文档，因为问题明确是 bike loan，不是 car/personal/house/gold loan。

### Step 2 Section localization

读取 `tree.json` 后命中：

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `zx-bank-credit-card.md` | `ch_1_3` | Platinum eligibility |
| `zx-bank-credit-card.md` | `ch_2_2`, `ch_2_3` | Gold fees 与 eligibility |
| `zx-bank-credit-card.md` | `ch_3_2`, `ch_3_3` | Women Empower fees 与 eligibility |
| `zx-bank-credit-card.md` | `ch_4_3` | Student eligibility |
| `zx-bank-credit-card.md` | `ch_5_3` | NRI eligibility |
| `zx-bank-bike-loan.md` | `ch_1`, `ch_4` | Bike loan interest 与 eligibility |

### Step 3 Content extraction

实际读取并用于作答的源行段：

| 文件 | 行段 | 用途 |
|---|---:|---|
| `zx-bank-credit-card.md` | L18-L25 | Platinum 费用与资格 |
| `zx-bank-credit-card.md` | L39-L46 | Gold 费用与资格 |
| `zx-bank-credit-card.md` | L60-L68 | Women Empower 费用与资格 |
| `zx-bank-credit-card.md` | L82-L89 | Student 费用与资格 |
| `zx-bank-credit-card.md` | L103-L110 | NRI 费用与资格 |
| `zx-bank-bike-loan.md` | L7-L10 | Bike loan 起始利率 |
| `zx-bank-bike-loan.md` | L42-L47 | Bike loan 资格 |

### Step 4 Correction loading

检查 `../../fixtures/zx-bank-kb/.kb/memory/corrections/doc_068.jsonl` 和 `doc_064.jsonl`：不存在。无 correction。

### Step 5 Answer

她有资格申请两张信用卡：

1. ZX Gold Credit Card：月收入要求 ₹25,000，年龄 21-65，CIBIL 700+。她月收入 ₹30,000、28 岁、CIBIL 720，全部满足。
2. ZX Women Empower Credit Card：需自我认同为女性，月收入 ₹15,000，年龄 21-65，CIBIL 650+。她也全部满足。

她不符合：

1. ZX Platinum：月收入需 ₹80,000 且 CIBIL 750+，她不满足。
2. ZX Student：年龄需 18-25 且需学生身份，28 岁不满足。
3. ZX NRI：需有效 NRI 身份，她是在德里工作的客户，不满足。

摩托车贷款利率为起始 9.49% p.a.。她年龄 28 岁、月收入 ₹30,000、CIBIL 720，满足年龄 21-60、收入 ₹8,000/月、CIBIL 650+ preferred 的条件。

两张可申请卡的加入费合计：Gold ₹499 + Women Empower ₹299 = ₹798 + GST。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| Gold 收入、年龄、CIBIL 条件 | `zx-bank-credit-card.md#L43-L46` |
| Women Empower 性别、收入、年龄、CIBIL 条件 | `zx-bank-credit-card.md#L64-L68` |
| Platinum 不符合 | `zx-bank-credit-card.md#L22-L25` |
| Student 不符合 | `zx-bank-credit-card.md#L86-L89` |
| NRI 不符合 | `zx-bank-credit-card.md#L107-L110` |
| 加入费合计 | `zx-bank-credit-card.md#L39-L41`, `zx-bank-credit-card.md#L60-L62` |
| Bike loan 利率与资格 | `zx-bank-bike-loan.md#L9-L10`, `zx-bank-bike-loan.md#L42-L47` |

标准答案对比：一致。

## Q2 上下文割裂

问题：一位客户的工资账户已经连续 4 个月没有收到工资入账。他的账户会发生什么变化？转换后他需要维持多少最低余额才能避免罚款？如果他想改用数字银行方式发起转换请求，具体操作步骤是什么？转换后他的银行卡和支票簿会更换吗？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `salary-account-to-a-savings-account.md` | `doc_052` | 问题核心是工资账户转储蓄账户 |
| `savings-account-overview.md` | `doc_054` | 问题询问转换后最低余额 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `salary-account-to-a-savings-account.md` | `ch_1` | 停发工资后的转换规则 |
| `salary-account-to-a-savings-account.md` | `ch_2_4`, `ch_2_5` | 最低余额提醒、卡/支票簿/账号保留 |
| `salary-account-to-a-savings-account.md` | `ch_3` | 数字银行转换步骤 |
| `savings-account-overview.md` | `ch_3` | 储蓄账户最低余额 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `salary-account-to-a-savings-account.md` | L7-L11 | 3+ months 自动转换规则 |
| `salary-account-to-a-savings-account.md` | L33-L40 | 维持最低余额、确认、卡/支票簿保留 |
| `salary-account-to-a-savings-account.md` | L44-L51 | 数字渠道步骤 |
| `savings-account-overview.md` | L40-L48 | 各类储蓄账户最低余额 |

### Step 4 Correction loading

检查 `doc_052.jsonl` 和 `doc_054.jsonl`：不存在。无 correction。

### Step 5 Answer

工资账户 4 个月无工资入账，超过文档中的 3+ months 条件，银行可能自动将其转为 Savings Account；客户也可手动转换以避免服务中断。

转换后最低余额取决于账户类型：Regular Savings 在印度需 ₹5,000；Digital Zero Balance 无最低余额；Senior Citizens/Students 在印度为 ₹1,000。文档说明最低余额会因国家和账户变体不同而变化。

数字渠道步骤：

1. 打开 ZX Bank Asia Mobile App 或登录 NetBanking。
2. 进入 `Service Requests > Convert Salary Account to Savings Account`。
3. 填写详情，并在要求时上传 KYC 文件。
4. 处理完成后收到确认。

转换后现有 debit card、chequebook 和 account number 通常保持不变。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 3+ months 停发工资可能自动转储蓄 | `salary-account-to-a-savings-account.md#L7-L11` |
| 数字渠道转换步骤 | `salary-account-to-a-savings-account.md#L44-L51` |
| 卡、支票簿、账号通常不变 | `salary-account-to-a-savings-account.md#L37-L40` |
| 最低余额 | `savings-account-overview.md#L40-L48` |

标准答案对比：一致。

## Q3 跨国条件推理

问题：一位居住在孟加拉国的客户想申请个人贷款，最高能借多少？利率范围是多少？与印度受薪人士相比是高还是低？他还想用 UPI 来偿还贷款，这可行吗？如果不可行，他可以通过什么渠道进行还款？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `personal-loan.md` | `doc_047` | 问题涉及个人贷款金额、利率、申请/还款渠道 |
| `upi-zx-bank-asia.md` | `doc_058` | 问题询问 UPI 是否可用 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `personal-loan.md` | `ch_2` | 各国家/客户类别利率 |
| `personal-loan.md` | `ch_4` | 各国家最高贷款额 |
| `personal-loan.md` | `ch_5` | 申请渠道 |
| `upi-zx-bank-asia.md` | `ch_4` | UPI 支持与可用国家说明 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `personal-loan.md` | L17-L25 | 印度受薪人士与孟加拉/不丹/尼泊尔利率 |
| `personal-loan.md` | L52-L68 | 孟加拉国最高贷款额与渠道 |
| `upi-zx-bank-asia.md` | L56-L67 | UPI 支持和仅印度可用说明 |

### Step 4 Correction loading

检查 `doc_047.jsonl` 和 `doc_058.jsonl`：不存在。无 correction。

### Step 5 Answer

孟加拉国客户个人贷款最高可借 BDT 35,00,000。利率范围是 13.50%–21.00% p.a.。印度/斯里兰卡受薪人士利率为 11.75%–17.99% p.a.，因此孟加拉国客户利率更高。

UPI 不可行，因为 UPI currently available in India for ZX Bank account holders。替代渠道包括访问所在国家任意 ZX Bank branch，通过 ZX Bank Asia Mobile App 或 NetBanking 在线办理，或拨打 24x7 Customer Care / 使用 App 内 Zia。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 孟加拉利率 | `personal-loan.md#L17-L25` |
| 印度受薪人士利率 | `personal-loan.md#L17-L22` |
| 孟加拉最高贷款额 | `personal-loan.md#L52-L58` |
| 替代渠道 | `personal-loan.md#L64-L68` |
| UPI 仅印度可用 | `upi-zx-bank-asia.md#L65-L67` |

标准答案对比：一致。

## Q4 三跳链式推理

问题：一位尼泊尔客户想用黄金饰品做抵押获得贷款，然后用贷款所得在尼泊尔开立定期存款，再用该定期存款做抵押获取另一笔贷款。请计算：黄金贷款的最高 LTV 是多少？尼泊尔定期存款的最低起存金额是多少？定期存款可抵押贷款的比例是多少？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `zx-bank-gold-loan.md` | `doc_070` | 问题涉及黄金饰品抵押贷款和 LTV |
| `zx-bank-fixed-deposits.md` | `doc_069` | 问题涉及尼泊尔 FD 起存金额和 FD 抵押贷款 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `zx-bank-gold-loan.md` | `ch_3` | Maximum Loan Amount 与 LTV |
| `zx-bank-fixed-deposits.md` | `ch_1` | Loan Against FD |
| `zx-bank-fixed-deposits.md` | `ch_2` | 最低起存额 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `zx-bank-gold-loan.md` | L24-L28 | Gold loan LTV |
| `zx-bank-fixed-deposits.md` | L7-L14 | Loan Against FD 最高比例 |
| `zx-bank-fixed-deposits.md` | L18-L22 | 尼泊尔最低起存金额 |

### Step 4 Correction loading

检查 `doc_070.jsonl` 和 `doc_069.jsonl`：不存在。无 correction。

### Step 5 Answer

黄金贷款最高 LTV 是黄金市场价值的 75%。尼泊尔定期存款最低起存金额是 NPR 1,500。定期存款可抵押贷款或透支比例最高为 FD 价值的 90%。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| Gold loan LTV 75% | `zx-bank-gold-loan.md#L24-L28` |
| FD 抵押最高 90% | `zx-bank-fixed-deposits.md#L7-L14` |
| Nepal FD 最低起存 NPR 1,500 | `zx-bank-fixed-deposits.md#L18-L22` |

标准答案对比：一致。

## Q5 跨文档 ESG 综合

问题：ZX Bank 获得过绿色金融方面的奖项。请找出银行中至少 4 个与 ESG/绿色金融直接相关的产品或服务，并说明客户的存款如何参与绿色金融项目。哪些国家的项目被特别提及？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `awards-and-recognitions.md` | `doc_016` | 问题提到绿色金融奖项 |
| `about-zx-bank-ltd.md` | `doc_001` | 银行整体 ESG/CSR 概览 |
| `zx-bank-house-loan.md` | `doc_071` | 绿色家园贷款 |
| `zx-bank-business-loans.md` | `doc_065` | Green & Sustainability Loans |
| `zx-bank-fixed-deposits.md` | `doc_069` | FD 存款参与 ESG |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `awards-and-recognitions.md` | `ch_2`, `ch_5` | Green Finance Award 与 Women’s Banking Initiative |
| `about-zx-bank-ltd.md` | `ch_6` | CSR & ESG Focus |
| `zx-bank-house-loan.md` | `ch_5` | Special Benefits / Green Homes |
| `zx-bank-business-loans.md` | `ch_2_5`, `ch_2_6` | Women Empowerment Loans 与 Green & Sustainability Loans |
| `zx-bank-fixed-deposits.md` | `ch_6` | ESG & CSR Initiatives |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `awards-and-recognitions.md` | L9-L11 | Green Finance Award 与国家 |
| `awards-and-recognitions.md` | L27-L29 | Women’s banking / micro-loans |
| `about-zx-bank-ltd.md` | L92-L99 | Green finance、financial literacy、women empowerment |
| `zx-bank-house-loan.md` | L54-L58 | Green Homes |
| `zx-bank-business-loans.md` | L31-L35 | Women Empowerment Loans 与 Green & Sustainability Loans |
| `zx-bank-fixed-deposits.md` | L73-L75 | 存款参与绿色金融项目 |

### Step 4 Correction loading

检查 `doc_016.jsonl`、`doc_001.jsonl`、`doc_071.jsonl`、`doc_065.jsonl`、`doc_069.jsonl`：不存在。无 correction。

### Step 5 Answer

与 ESG/绿色金融直接相关的产品或服务至少包括：

1. Green Finance Projects：与 Bhutan hydropower 和 Nepal solar ventures 合作。
2. Green Homes：对 eco-friendly/energy-efficient homes 提供更低利率。
3. Green & Sustainability Loans：为 renewable energy、eco-friendly infrastructure、climate-smart business initiatives 融资。
4. Fixed Deposits 的 ESG 贡献：部分存款资助 Bhutanese hydropower 和 Nepalese solar ventures。
5. Women Empowerment Loans / micro-loans：服务 South Asia 女性企业主或 women-led enterprises，属于社会层面的 ESG。

客户存款参与方式：部分定期存款资金会投入不丹水电、尼泊尔太阳能等绿色金融项目。被特别提及的国家是不丹和尼泊尔。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 绿色金融奖项、Bhutan hydropower、Nepal solar | `awards-and-recognitions.md#L9-L11` |
| 整体 ESG 项目 | `about-zx-bank-ltd.md#L92-L99` |
| Green Homes | `zx-bank-house-loan.md#L54-L58` |
| Green & Sustainability Loans | `zx-bank-business-loans.md#L34-L35` |
| Women Empowerment Loans | `zx-bank-business-loans.md#L31-L32`, `awards-and-recognitions.md#L27-L29` |
| FD 存款参与 ESG | `zx-bank-fixed-deposits.md#L73-L75` |

标准答案对比：一致。

## Q6 欺诈处理完整路径

问题：如果你的 ZX Bank 借记卡被盗并产生了欺诈交易，你可以通过哪些渠道立即冻结/挂失卡片？银行处理欺诈投诉的目标解决时间是多少天？在问题解决后，如果你想申请新的支票簿，可以通过哪几种方式申请？请列出所有渠道。

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `fraud-transaction.md` | `doc_033` | 欺诈交易报告、冻结、处理时间 |
| `zx-bank-asia-mobile-app-guide.md` | `doc_061` | App 内卡片 block 功能 |
| `apply-for-a-cheque-book.md` | `doc_005` | 支票簿申请渠道 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `fraud-transaction.md` | `ch_1`, `ch_2`, `ch_5`, `ch_6` | 联系银行、冻结卡/账户、解决时间、紧急 block |
| `zx-bank-asia-mobile-app-guide.md` | `ch_5_4_1` | App 内 Block Card |
| `apply-for-a-cheque-book.md` | `ch_1` 到 `ch_5` | 五种支票簿申请渠道 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `fraud-transaction.md` | L7-L17 | 热线、邮件、App 报告 |
| `fraud-transaction.md` | L21-L26 | Mobile App / NetBanking 冻结卡或账户 |
| `fraud-transaction.md` | L50-L54 | 10 working days |
| `fraud-transaction.md` | L58-L63 | Block Instantly |
| `zx-bank-asia-mobile-app-guide.md` | L71-L78 | Card > More options > Block |
| `apply-for-a-cheque-book.md` | L7-L15 | Mobile App 申请 |
| `apply-for-a-cheque-book.md` | L19-L25 | NetBanking 申请 |
| `apply-for-a-cheque-book.md` | L29-L34 | Branch 申请 |
| `apply-for-a-cheque-book.md` | L38-L43 | ATM 申请 |
| `apply-for-a-cheque-book.md` | L47-L51 | Customer Care 申请 |

### Step 4 Correction loading

检查 `doc_033.jsonl`、`doc_061.jsonl`、`doc_005.jsonl`：不存在。无 correction。

### Step 5 Answer

立即冻结/挂失或报告卡片的渠道包括：

1. Mobile App 或 NetBanking：进入 Card Management 或 Account Services，选择 Block/Card Hotlisting 或 Freeze Account 并确认。
2. App 卡片页：选择卡片，More options，Block，立即生效。
3. App 的 Support > Report Fraud。
4. 24x7 fraud hotline：印度、斯里兰卡、孟加拉国、不丹、尼泊尔均有对应号码。
5. Email：`fraudreport@zxbank.asia`。
6. 紧急情况下使用 App 的 Block Instantly。

银行目标解决时间是 10 working days。

新支票簿申请渠道包括：ZX Bank Asia Mobile App、NetBanking、Branch、ZX Bank ATM、ZX Bank Customer Care。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 热线、邮件、App 报告 | `fraud-transaction.md#L7-L17` |
| App/NetBanking 冻结卡或账户 | `fraud-transaction.md#L21-L26` |
| App 内卡片 Block | `zx-bank-asia-mobile-app-guide.md#L71-L78` |
| 10 working days | `fraud-transaction.md#L50-L54` |
| Block Instantly | `fraud-transaction.md#L58-L63` |
| 支票簿五种渠道 | `apply-for-a-cheque-book.md#L7-L15`, `#L19-L25`, `#L29-L34`, `#L38-L43`, `#L47-L51` |

标准答案对比：一致。

## Q7 隐式否定推理

问题：ZX Bank 在 5 个国家运营。请列出以下每项服务在哪些国家可用、哪些国家不可用：(1) UPI 支付，(2) e-KYC 数字身份验证，(3) 学生信用卡，(4) 跨境汇款。如果一位在孟加拉国的学生想申请信用卡，他有什么选择？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `about-zx-bank-ltd.md` | `doc_001` | 5 个运营国家与跨境服务背景 |
| `upi-zx-bank-asia.md` | `doc_058` | UPI 可用性 |
| `zx-bank-credit-card.md` | `doc_068` | e-KYC 与学生信用卡国家 |
| `cross-border-payments.md` | `doc_031` | 跨境汇款走廊 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `about-zx-bank-ltd.md` | `ch_1`, `ch_2_4` | 运营国家、汇款国家 |
| `upi-zx-bank-asia.md` | `ch_4` | UPI 仅印度可用 |
| `zx-bank-credit-card.md` | `ch_4`, `ch_6` | Student card 国家、e-KYC 国家 |
| `cross-border-payments.md` | `ch_1` | India/Sri Lanka/Nepal/Bhutan 跨境汇款 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `about-zx-bank-ltd.md` | L12-L27 | 五个运营国家 |
| `about-zx-bank-ltd.md` | L50-L52 | Remittances 国家 |
| `upi-zx-bank-asia.md` | L65-L67 | UPI 当前仅印度 |
| `zx-bank-credit-card.md` | L72-L89 | Student card 国家与资格 |
| `zx-bank-credit-card.md` | L115-L120 | e-KYC 国家 |
| `cross-border-payments.md` | L3-L5 | 跨境汇款国家 |

### Step 4 Correction loading

检查 `doc_001.jsonl`、`doc_058.jsonl`、`doc_068.jsonl`、`doc_031.jsonl`：不存在。无 correction。

### Step 5 Answer

| 服务 | 可用国家 | 不可用国家 |
|---|---|---|
| UPI 支付 | 印度 | 斯里兰卡、孟加拉国、不丹、尼泊尔 |
| e-KYC | 印度、斯里兰卡、尼泊尔 | 孟加拉国、不丹 |
| 学生信用卡 | 印度、斯里兰卡、尼泊尔 | 孟加拉国、不丹 |
| 跨境汇款 | 印度、斯里兰卡、尼泊尔、不丹 | 孟加拉国 |

孟加拉国学生不能申请 Student Credit Card，因为学生卡只面向 India、Sri Lanka、Nepal 的 college/university students。他可以考虑其他信用卡，例如 Gold，但必须满足收入、年龄、CIBIL 等资格；孟加拉国也不支持 e-KYC，因此不能依赖 e-KYC 数字身份验证。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 运营国家全集 | `about-zx-bank-ltd.md#L12-L27` |
| UPI 仅印度 | `upi-zx-bank-asia.md#L65-L67` |
| e-KYC 国家 | `zx-bank-credit-card.md#L115-L120` |
| 学生卡国家 | `zx-bank-credit-card.md#L72-L89` |
| 跨境汇款国家 | `cross-border-payments.md#L3-L5`, `about-zx-bank-ltd.md#L50-L52` |

标准答案对比：一致。

## Q8 跨文档集合比较

问题：比较 ZX Bank 房屋贷款和汽车贷款所需的文件。哪些文件是两者都需要的？哪些是房屋贷款独有的？哪些是汽车贷款独有的？两种贷款是否都支持完全在线申请？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `zx-bank-house-loan.md` | `doc_071` | 房屋贷款文件和申请方式 |
| `zx-bank-car-loan.md` | `doc_066` | 汽车贷款文件和申请方式 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `zx-bank-house-loan.md` | `ch_3`, `ch_4` | Documents Required 与 How to Apply |
| `zx-bank-car-loan.md` | `ch_3`, `ch_4_1` | Documentation Required 与 Online application |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `zx-bank-house-loan.md` | L32-L37 | 房屋贷款文件 |
| `zx-bank-house-loan.md` | L41-L50 | 房屋贷款申请渠道 |
| `zx-bank-car-loan.md` | L28-L35 | 汽车贷款文件 |
| `zx-bank-car-loan.md` | L39-L47 | 汽车贷款在线申请步骤 |

### Step 4 Correction loading

检查 `doc_071.jsonl` 和 `doc_066.jsonl`：不存在。无 correction。

### Step 5 Answer

两者都需要的文件：

1. 身份/KYC 证明：房贷列 ID Proof；车贷列 KYC Documents，包括 Aadhaar/Passport/Driving License、PAN、photograph。
2. 收入证明：房贷列 Salary slips、ITR、Bank statement、Form 16；车贷列 Salary slips/ITR/Bank statements。
3. 照片或个人身份材料：车贷明确列 photograph；房贷列 ID/address 文件，未单列 photograph。

房屋贷款独有：

1. Property Documents：Sale agreement、title deed、approved plan。
2. Form 16 作为收入证明中的明确细项。

汽车贷款独有：

1. Employment/Business Proof：Offer letter 或 Business registration。
2. Vehicle Quotation/Invoice。

在线申请：

1. 房屋贷款支持 Online，通过 ZX Bank Home Loan Portal，也支持 Mobile App。
2. 汽车贷款支持 Online，通过 ZX Bank Asia App 或 ZX NetBanking，并可上传 documents/e-KYC。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 房贷文件 | `zx-bank-house-loan.md#L32-L37` |
| 房贷在线/App/分行申请 | `zx-bank-house-loan.md#L41-L50` |
| 车贷文件 | `zx-bank-car-loan.md#L28-L35` |
| 车贷在线申请 | `zx-bank-car-loan.md#L39-L47` |

标准答案对比：事实一致。引用说明：标准答案把“地址证明”列为共同文件，但汽车贷款文档没有单列 `Address Proof`，而是放在 `KYC Documents` 的证件集合中；这是语义归纳，不是原文逐字字段。

## Q9 时空交叉推理

问题：一位客户在海得拉巴的 HITEC City 科技园区工作。最近的 ZX Bank 分行在哪里（给出 IFSC 和联系电话）？如果他要前往孟买出差，孟买有哪些科技园区设有 ZX Bank ATM？他可以通过什么方式找到这些 ATM 的具体位置？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | `doc_011` | HITEC City 与孟买科技园 ATM |
| `hyderabad-branch-network.md` | `doc_035` | 海得拉巴分行网络、IFSC、电话 |
| `zx-bank-asia-mobile-app-guide.md` | `doc_061` | Locate Branch/ATM 功能 |
| `atms-at-railway-stations-and-airports.md` | `doc_015` | ATM Locator 文案 |
| `ask-zia-your-24-7-banking-assistant.md` | `doc_006` | Zia 可定位 branches/ATMs |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | `ch_1`, `ch_4` | Mumbai tech parks 与 Hyderabad HITEC City |
| `hyderabad-branch-network.md` | `ch_4` | West Hyderabad / Madhapur |
| `zx-bank-asia-mobile-app-guide.md` | `ch_7` | Locate Branch/ATM |
| `ask-zia-your-24-7-banking-assistant.md` | `ch_1` | Zia branch/ATM locator |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | L7-L16 | Mumbai tech park ATMs |
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | L46-L55 | HITEC City 位于 Madhapur |
| `hyderabad-branch-network.md` | L45-L50 | Madhapur Kavuri Hills 分行、IFSC、电话 |
| `zx-bank-asia-mobile-app-guide.md` | L112-L117 | Locate Branch/ATM |
| `atms-at-railway-stations-and-airports.md` | L178-L180 | Mobile App 与 ATM Locator |
| `ask-zia-your-24-7-banking-assistant.md` | L7-L12 | Zia 可定位 branches and ATMs |

### Step 4 Correction loading

检查 `doc_011.jsonl`、`doc_035.jsonl`、`doc_061.jsonl`、`doc_015.jsonl`、`doc_006.jsonl`：不存在。无 correction。

### Step 5 Answer

HITEC City 位于 Madhapur, Hyderabad, Telangana 500081。最近的 ZX Bank 分行是 West Hyderabad 列表中的 Madhapur Kavuri Hills, 500081；IFSC 为 ZXIN0001232；联系电话为 040-45671232。

孟买设有 ZX Bank ATM 的科技园区包括：

1. Mindspace Airoli IT Park，Building 2, Mindspace, Thane-Belapur Road, Airoli, Navi Mumbai, Maharashtra 400708。
2. Nesco IT Park，Gate 3, Western Express Highway, Goregaon (East), Mumbai, Maharashtra 400063。
3. Infinity IT Park，New Link Road, Malad (West), Mumbai, Maharashtra 400064。

查找 ATM 具体位置的方法：使用 ZX Bank Asia App 的 Locate Branch/ATM，使用 ZX Bank ATM Locator，或询问 Zia。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| HITEC City 地址 | `atm-locations-at-tech-parks-in-major-indian-cities.md#L46-L55` |
| Madhapur 分行、IFSC、电话 | `hyderabad-branch-network.md#L45-L50` |
| Mumbai 三个科技园 ATM | `atm-locations-at-tech-parks-in-major-indian-cities.md#L7-L16` |
| App 定位方式 | `zx-bank-asia-mobile-app-guide.md#L112-L117` |
| ATM Locator | `atms-at-railway-stations-and-airports.md#L178-L180` |
| Zia 定位 | `ask-zia-your-24-7-banking-assistant.md#L7-L12` |

标准答案对比：一致。

## Q10 复合条件推理

问题：一位 67 岁的印度退休老人想做以下三件事：(1) 开立定期存款获取最高利率，(2) 申请一张信用卡用于日常消费，(3) 租用一个银行保险箱存放遗产文件。请逐一分析：他能获得的最高 FD 利率是多少？他有资格申请哪些信用卡？他开立保险箱需要满足什么前提条件？整个流程中哪些步骤必须到分行办理？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `zx-bank-fixed-deposits.md` | `doc_069` | FD 利率、老年人利率、开立方式 |
| `zx-bank-credit-card.md` | `doc_068` | 各信用卡年龄条件 |
| `open-a-locker.md` | `doc_045` | 保险箱资格和分行流程 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `zx-bank-fixed-deposits.md` | `ch_4`, `ch_5` | FD 开立方式、利率表 |
| `zx-bank-credit-card.md` | `ch_1_3`, `ch_2_3`, `ch_3_3`, `ch_4_3`, `ch_5_3` | 各卡年龄条件 |
| `open-a-locker.md` | `ch_1` 到 `ch_6` | 保险箱可用性、资格、申请、支付、钥匙、操作 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `zx-bank-fixed-deposits.md` | L40-L55 | FD App/NetBanking/Branch 开立方式 |
| `zx-bank-fixed-deposits.md` | L59-L69 | Senior Citizen 最高样例利率 |
| `zx-bank-credit-card.md` | L22-L25 | Platinum 年龄 |
| `zx-bank-credit-card.md` | L43-L46 | Gold 年龄 |
| `zx-bank-credit-card.md` | L64-L68 | Women Empower 年龄 |
| `zx-bank-credit-card.md` | L86-L89 | Student 年龄 |
| `zx-bank-credit-card.md` | L107-L110 | NRI 年龄 |
| `open-a-locker.md` | L7-L18 | 可用性与资格 |
| `open-a-locker.md` | L25-L38 | 分行申请、KYC、协议、支付 |
| `open-a-locker.md` | L42-L54 | 钥匙、访问和操作 |

### Step 4 Correction loading

检查 `doc_069.jsonl`、`doc_068.jsonl`、`doc_045.jsonl`：不存在。无 correction。

### Step 5 Answer

FD：67 岁属于 Senior Citizen；样例利率表中最高 Senior Citizen Rate 为 6.80% p.a.，对应 3 years–5 years。

信用卡：他不符合任何列出的 ZX Bank 信用卡。Platinum、Gold、Women Empower、NRI 的年龄上限均为 65 岁；Student 卡年龄为 18-25 岁。67 岁超过所有适用年龄上限。

保险箱前提条件：必须是现有 ZX Bank customer，或开立 savings/current account；KYC 更新，需有效照片 ID、地址证明、近期照片。

必须到分行办理的步骤：查询/确认保险箱可用性可到分行或电话，但正式申请需到分行携带原件和复印件，填写 Locker Facility Application Form，提交 KYC，签署 Locker Hirer Agreement，支付保证金和年租，获批后领取钥匙。每次操作保险箱也需在分行营业时间携带钥匙和有效 ID，并签署 Locker Access Register。FD 可通过 App 或 NetBanking 完成，不必必须到分行。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| FD 最高老年利率 6.80% | `zx-bank-fixed-deposits.md#L59-L69` |
| FD 可数字开立 | `zx-bank-fixed-deposits.md#L40-L55` |
| 各信用卡年龄上限 | `zx-bank-credit-card.md#L22-L25`, `#L43-L46`, `#L64-L68`, `#L86-L89`, `#L107-L110` |
| 保险箱资格 | `open-a-locker.md#L15-L21` |
| 保险箱申请必须到分行 | `open-a-locker.md#L25-L30` |
| 支付、钥匙、操作 | `open-a-locker.md#L34-L38`, `#L42-L54` |

标准答案对比：一致。

## Q11 NRI 跨国银行旅程

问题：一位居住在不丹的印度裔 NRI 想做以下事情：(1) 汇款到印度的家人账户，(2) 申请一张 NRI 信用卡，(3) 通过 WhatsApp 使用银行的 AI 助手。请逐一说明：跨境汇款需要多长时间？NRI 信用卡的最低月海外汇款要求是多少？WhatsApp 上使用 Zia 需要什么步骤？Zia 支持哪些语言？

### Step 1 Document routing

| 文档 | doc_id | 路由理由 |
|---|---|---|
| `cross-border-payments.md` | `doc_031` | 跨境汇款国家、时间和渠道 |
| `zx-bank-credit-card.md` | `doc_068` | NRI 信用卡费用与资格 |
| `ask-zia-your-24-7-banking-assistant.md` | `doc_006` | WhatsApp Zia 步骤和语言 |
| `about-zx-bank-ltd.md` | `doc_001` | 不丹运营和 NRI support 背景 |

### Step 2 Section localization

| 文档 | 节点 | 节点含义 |
|---|---|---|
| `cross-border-payments.md` | `ch_1`, `ch_2`, `ch_3`, `ch_4` | 汇款国家、时间、操作和 App 支持 |
| `zx-bank-credit-card.md` | `ch_5_2`, `ch_5_3` | NRI 卡费用与资格 |
| `ask-zia-your-24-7-banking-assistant.md` | `ch_2`, `ch_4_2` | WhatsApp Zia 和语言 |
| `about-zx-bank-ltd.md` | `ch_1`, `ch_2_4` | Bhutan 与汇款服务 |

### Step 3 Content extraction

| 文件 | 行段 | 用途 |
|---|---:|---|
| `cross-border-payments.md` | L3-L15 | 汇款国家、within minutes |
| `cross-border-payments.md` | L20-L31 | 汇款流程 |
| `cross-border-payments.md` | L35-L37 | App 与 Zia 支持 |
| `zx-bank-credit-card.md` | L93-L110 | NRI 卡费用与资格 |
| `ask-zia-your-24-7-banking-assistant.md` | L17-L23 | WhatsApp Zia 与语言 |
| `ask-zia-your-24-7-banking-assistant.md` | L41-L44 | WhatsApp 使用步骤 |
| `about-zx-bank-ltd.md` | L23-L24 | Bhutan cross-border banking/NRI support |
| `about-zx-bank-ltd.md` | L50-L52 | Remittances 国家 |

### Step 4 Correction loading

检查 `doc_031.jsonl`、`doc_068.jsonl`、`doc_006.jsonl`、`doc_001.jsonl`：不存在。无 correction。

### Step 5 Answer

跨境汇款：不丹在 ZX Bank 的跨境支付/汇款支持范围内，覆盖 India、Sri Lanka、Nepal、Bhutan。大多数转账通过 advanced payment rails 和 SWIFT capabilities 在几分钟内处理。

NRI 信用卡：适用于 Non-resident Indians and NRIs in Bhutan, Nepal, Sri Lanka。最低月海外汇款要求是 $1,000。加入费为 USD $30，年费为 USD $25，消费超过 USD $5,000 可免年费。

WhatsApp Zia 使用步骤：

1. 保存官方 WhatsApp 号码 `+91-XXX-XXX-XXXX`。
2. 发送 `Hello Zia`。
3. 按提示访问银行功能。

Zia 支持 English、Hindi、Sinhala、Bengali、Nepali。

### Step 6 Self-verify

| 断言 | 引用 |
|---|---|
| 不丹在跨境汇款范围内 | `cross-border-payments.md#L3-L5`, `about-zx-bank-ltd.md#L23-L24` |
| 大多数转账几分钟内处理 | `cross-border-payments.md#L9-L15` |
| NRI 卡适用对象、费用、最低汇款 | `zx-bank-credit-card.md#L93-L110` |
| WhatsApp Zia 语言 | `ask-zia-your-24-7-banking-assistant.md#L17-L23` |
| WhatsApp 使用步骤 | `ask-zia-your-24-7-banking-assistant.md#L41-L44` |

标准答案对比：一致。

## 最终结论

严格按 `kb-chat` 六步逐题记录后，11 道题的事实答案均与测试套件标准答案一致。

唯一需要在报告中保留的注意点是 Q8：汽车贷款文档没有逐字列出 `Address Proof`，而是在 `KYC Documents` 中列出 Aadhaar/Passport/Driving License、PAN、photograph；因此“共同需要地址证明”属于语义归纳，不能写成汽车贷款原文单列字段。

本次执行也验证了该知识库的设计边界：`manifest.json` 足以承担文档路由，`tree.json` 足以承担章节定位，源文档行号足以支撑逐条自检；只要执行过程不跳过 `tree.json` 与自检步骤，复杂多跳题仍可完整追踪。
