# kb-chat 严格执行追踪报告

测试对象：`../../../fixtures/zx-bank-kb/`

测试题集：`zx-bank-kb-hard-rag-questions.md`

执行目标：按 `kb-chat` Skill 的 6 个步骤，对 11 道复杂问题逐题作答，并记录每题的路由、章节定位、实际读取范围、correction 状态、答案、自检与标准答案对比。

执行时间：2026-08-10 08:22 北京时间开始。

## 报告结论

本报告是一次手工可审计的执行记录，记录了 `kb-chat` 六步流程下的逐题作答轨迹。按报告中的源文行号复核，11 道题的主要事实答案均能回到源文行号；在该结构化题集上的整体通过率为 `11/11`，引用精度为 `11/11`。

评测口径以源文为准：若源文直接说明，则给出确定结论；若结论依赖语义归纳或地理近邻推断，则在答案中保留边界；若源文未说明，则明确写出未提及。

本次结果说明，在小型、结构化 Markdown 知识库和人工可审计执行记录下，`manifest.json` 可以承担文档路由，`tree.json` 可以承担章节定位，源文档行号可以支撑逐条自检。该结论不等同于自动化 benchmark、盲测结果或线上开放场景评测，也不证明任意知识库和任意用户问题都能达到同等表现。

## 总体结果

| 题号 | 主要能力 | 事实答案 | 引用精度 | 备注 |
|---|---|---:|---:|---|
| Q1 | 多跳条件推理 | 通过 | 通过 | 信用卡资格、车贷利率、加入费均匹配 |
| Q2 | 账户转换链路 | 通过 | 通过 | 自动转换、Regular Savings 最低余额、数字渠道和卡/支票簿保留均有源文支撑 |
| Q3 | 跨国条件与否定推理 | 通过 | 通过 | 孟加拉贷款、利率对比、UPI 否定均匹配；“还款渠道”源文未明示，答案保留来源边界 |
| Q4 | 三跳数值提取 | 通过 | 通过 | LTV、尼泊尔 FD 起存、FD 抵押比例均匹配；LTV 的尼泊尔监管细节未在源文单独说明 |
| Q5 | ESG 跨文档综合 | 通过 | 通过 | 绿色金融、绿色家园、绿色商业贷款、FD ESG、女性赋权均识别 |
| Q6 | 多渠道枚举 | 通过 | 通过 | 冻结/挂失渠道、欺诈报告渠道、解决时间和支票簿申请渠道均按源文边界区分 |
| Q7 | 服务可用性矩阵 | 通过 | 通过 | UPI、信用卡申请 e-KYC、学生卡、跨境汇款国家判断均匹配 |
| Q8 | 集合比较 | 通过 | 通过 | 共同文件、独有文件和在线申请边界均按源文回答 |
| Q9 | 时空交叉推理 | 通过 | 通过 | HITEC City 近邻分行为合理地理推断，孟买 ATM 和定位方式均匹配 |
| Q10 | 复合条件推理 | 通过 | 通过 | FD 利率、信用卡年龄边界、保险箱分行流程均匹配 |
| Q11 | NRI 跨国旅程 | 通过 | 通过 | 汇款时间、NRI 卡条件、WhatsApp Zia 均匹配 |

## 执行口径

每道题均按以下流程记录：

1. Document routing：读取并使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`，根据问题语义匹配 `domain/title/summary/tags`，选出相关文档。
2. Section localization：读取每个命中文档的 `.kb/index/<source-stem>/tree.json`，根据节点 `title/summary/keywords` 定位章节。
3. Content extraction：按 `tree.json` 中的 `start_line/end_line` 读取源 Markdown，必要时扩展到同级或父级行段。
4. Correction loading：检查 `.kb/memory/corrections/{doc_id}.jsonl`。本次知识库的 `corrections/` 目录为空，因此所有题均无 correction。
5. Generate answer：仅基于已读取源文档内容作答。
6. Self-verify：逐条核对答案断言是否有引用支撑，再与测试题标准答案比较。

说明：当前环境不暴露模型真实 API token 明细，因此本报告不声称拥有精确计费 token。若需要 token，可另行用日志层或 API 层统计；本报告只记录严格执行轨迹。

## 本次单题执行更新：Q1

更新时间：2026-08-10。

问题：一位在德里工作的女性上班族，月收入 ₹30,000，年龄 28 岁，CIBIL 720。她想同时申请一张 ZX Bank 信用卡和一笔摩托车贷款。她有资格申请哪些信用卡？摩托车贷款的利率是多少？两张卡的加入费合计多少？

结论：

| 问点 | 答案 |
|---|---|
| 可申请信用卡 | `ZX Gold Credit Card`、`ZX Women Empower Credit Card` |
| 摩托车贷款利率 | starting from `9.49% p.a.` |
| 两张卡加入费合计 | `₹499 + ₹299 = ₹798 + GST` |

### Step 1 Document routing

执行说明：根目录未发现 `.kb/manifest.json`，本题按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `zx-bank-credit-card.md` | `doc_068` | 标题为 `ZX Bank Credit Card Options`；摘要覆盖各信用卡的 fees 与 eligibility | 判断信用卡资格与加入费 |
| `zx-bank-bike-loan.md` | `doc_064` | 标题为 `ZX Bank Bike Loan`；摘要覆盖 bike loan 利率和资格 | 判断摩托车贷款利率与资格 |

路由判断：未路由到 `zx-bank-car-loan.md`、`personal-loan.md`、`zx-bank-house-loan.md` 等其他贷款文档，因为问题明确限定为 motorcycle/two-wheeler/bike loan。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录，用于说明最终命中文档的边界。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `zx-bank-credit-card.md` | `ch_1_2`, `ch_1_3` | L18-L25 | Platinum 费用与资格，用于排除 |
| `zx-bank-credit-card.md` | `ch_2_2`, `ch_2_3` | L39-L46 | Gold 费用与资格，用于判断可申请 |
| `zx-bank-credit-card.md` | `ch_3_2`, `ch_3_3` | L60-L68 | Women Empower 费用与资格，用于判断可申请 |
| `zx-bank-credit-card.md` | `ch_4_2`, `ch_4_3` | L82-L89 | Student 费用与资格，用于排除 |
| `zx-bank-credit-card.md` | `ch_5_2`, `ch_5_3` | L103-L110 | NRI 费用与资格，用于排除 |
| `zx-bank-bike-loan.md` | `ch_1` | L7-L17 | Bike loan 利率 |
| `zx-bank-bike-loan.md` | `ch_4` | L42-L50 | Bike loan 资格 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `zx-bank-credit-card.md` | L18-L25 | Platinum：加入费 ₹2,999 + GST；资格要求月收入 ₹80,000、年龄 21-65、CIBIL 750+ |
| `zx-bank-credit-card.md` | L39-L46 | Gold：加入费 ₹499 + GST；资格要求月收入 ₹25,000、年龄 21-65、CIBIL 700+ |
| `zx-bank-credit-card.md` | L60-L68 | Women Empower：加入费 ₹299 + GST；资格要求女性、月收入 ₹15,000、年龄 21-65、CIBIL 650+ |
| `zx-bank-credit-card.md` | L82-L89 | Student：加入费 ₹0；资格要求年龄 18-25、学生证明 |
| `zx-bank-credit-card.md` | L103-L110 | NRI：加入费 USD $30；资格要求 NRI status、海外汇款、年龄 21-65 |
| `zx-bank-bike-loan.md` | L7-L23 | Bike loan：利率 starting from 9.49% p.a.；女性申请人有 special interest rate 提示 |
| `zx-bank-bike-loan.md` | L42-L47 | Bike loan：年龄 21-60、受薪/自雇/企业主、最低收入 ₹8,000/month、CIBIL above 650 preferred |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_068.jsonl` | 不存在 |
| `doc_064.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

| 信用卡 | 是否可申请 | 判断依据 |
|---|---|---|
| `ZX Gold Credit Card` | 可以 | 月收入 ₹30,000 ≥ ₹25,000；年龄 28 在 21-65 内；CIBIL 720 ≥ 700 |
| `ZX Women Empower Credit Card` | 可以 | 女性上班族；月收入 ₹30,000 ≥ ₹15,000；年龄 28 在 21-65 内；CIBIL 720 ≥ 650 |
| `ZX Platinum Credit Card` | 不可以 | 需要月收入 ₹80,000 且 CIBIL 750+，她不满足 |
| `ZX Student Credit Card` | 不可以 | 需要年龄 18-25 且有学生身份，她 28 岁且为上班族 |
| `ZX NRI Credit Card` | 不可以 | 需要 NRI status 和海外汇款条件，题干未满足 |

摩托车贷款方面，她 28 岁、受薪上班族、月收入 ₹30,000、CIBIL 720，满足 bike loan 的资格要求；适用利率为 starting from `9.49% p.a.`。

加入费合计：`Gold ₹499 + Women Empower ₹299 = ₹798 + GST`。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| Gold 可申请 | 通过 | `zx-bank-credit-card.md#L43-L46` |
| Women Empower 可申请 | 通过 | `zx-bank-credit-card.md#L64-L68` |
| Platinum 不可申请 | 通过 | `zx-bank-credit-card.md#L22-L25` |
| Student 不可申请 | 通过 | `zx-bank-credit-card.md#L86-L89` |
| NRI 不可申请 | 通过 | `zx-bank-credit-card.md#L107-L110` |
| Bike loan 利率为 9.49% p.a. 起 | 通过 | `zx-bank-bike-loan.md#L7-L10` |
| Bike loan 资格满足 | 通过 | `zx-bank-bike-loan.md#L42-L47` |
| 加入费合计 ₹798 + GST | 通过 | `zx-bank-credit-card.md#L39-L41`, `zx-bank-credit-card.md#L60-L62` |

自检结论：三个问点均已回答；每个事实断言均有源文行号支撑。

## 本次单题执行更新：Q2

更新时间：2026-08-10。

问题：一位客户的工资账户已经连续 4 个月没有收到工资入账。他的账户会发生什么变化？转换后他需要维持多少最低余额才能避免罚款？如果他想改用数字银行方式发起转换请求，具体操作步骤是什么？转换后他的银行卡和支票簿会更换吗？

结论：

| 问点 | 答案 |
|---|---|
| 账户会发生什么变化 | 连续 4 个月无工资入账，超过 3+ months 条件，工资账户可能被银行自动转换为 Savings Account |
| 转换后最低余额 | 取决于 Savings Account 类型：Regular Savings 在印度为 `₹5,000`；Digital Zero Balance 为 `Nil`；Senior Citizens/Students 在印度为 `₹1,000` |
| 数字渠道转换步骤 | 打开 App 或 NetBanking → `Service Requests` → `Convert Salary Account to Savings Account` → 填写信息并按要求上传 KYC → 等待确认 |
| 银行卡和支票簿是否更换 | 通常不会更换；existing debit card、chequebook 和 account number typically remain unchanged |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `salary-account-to-a-savings-account.md` | `doc_052` | 标题为 `How to Convert Your Salary Account to a Savings Account at ZX Bank`；摘要覆盖转换原因、分行和数字渠道步骤、最低余额与支持 | 判断 4 个月无工资后的账户变化、数字渠道步骤、卡和支票簿是否保留 |
| `savings-account-overview.md` | `doc_054` | 标题为 `ZX Bank Ltd. – Savings Account Overview`；摘要覆盖 savings account features、application channels、minimum balance requirements 和账户 kit | 补充转换后 Savings Account 的最低余额标准 |

路由判断：未路由到 `salary-saving-account.md`，因为题目不是询问工资账户产品权益，而是询问 salary account 停发工资后的转换后果与转换流程；未路由到一般账户开立或银行卡帮助文档，因为卡和支票簿是否更换已在转换文档中直接说明。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `salary-account-to-a-savings-account.md` | `ch_1` | L7-L14 | 判断停发工资 3+ months 后可能自动转为 Savings Account |
| `salary-account-to-a-savings-account.md` | `ch_2_4` | L33-L36 | 判断转换后需维持 Savings Account 最低余额以避免 charges |
| `salary-account-to-a-savings-account.md` | `ch_2_5` | L37-L43 | 判断转换确认方式，以及 debit card、chequebook、account number 是否保留 |
| `salary-account-to-a-savings-account.md` | `ch_3` | L44-L54 | 定位数字银行转换步骤 |
| `savings-account-overview.md` | `ch_3` | L40-L51 | 定位各类 Savings Account 的 minimum balance requirements |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `salary-account-to-a-savings-account.md` | L7-L11 | Salary credits stop for 3+ months 时，账户 may be automatically converted to a Savings Account；manual conversion 可避免服务中断 |
| `salary-account-to-a-savings-account.md` | L33-L40 | 转换后需维持 Savings Account 要求的最低余额；转换完成后收到 SMS/email；existing debit card、chequebook、account number typically remain unchanged |
| `salary-account-to-a-savings-account.md` | L44-L51 | 数字渠道步骤：打开 ZX Bank Asia Mobile App 或 NetBanking，进入 Service Requests > Convert Salary Account to Savings Account，填写信息并上传 KYC，处理后确认 |
| `savings-account-overview.md` | L40-L48 | Regular Savings 最低余额：India ₹5,000 / Sri Lanka LKR 3,000；Digital Zero Balance 为 Nil；Senior Citizens/Students 在印度为 ₹1,000；最低余额因国家和账户变体而异 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_052.jsonl` | 不存在 |
| `doc_054.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

该客户的工资账户已经连续 4 个月没有工资入账，超过文档中的 `3+ months` 条件，因此账户可能被银行自动转换为 `Savings Account`；客户也可以主动发起手动转换，以避免服务中断。

转换后的最低余额不是单一固定数值，而是取决于转换成哪一种 Savings Account：

| Savings Account 类型 | 最低余额 |
|---|---:|
| Regular Savings | India `₹5,000` / Sri Lanka `LKR 3,000` |
| Digital Zero Balance | `Nil`，无最低余额 |
| Senior Citizens/Students | India `₹1,000` |

如果题干默认客户在印度且转换为普通储蓄账户，则为避免罚款需维持 `₹5,000`。

数字银行方式发起转换的步骤：

1. 打开 `ZX Bank Asia Mobile App` 或登录 `NetBanking`。
2. 进入 `Service Requests > Convert Salary Account to Savings Account`。
3. 填写所需信息，并在系统要求时上传 KYC 文件。
4. 处理完成后接收确认。

转换后，现有 `debit card`、`chequebook` 和 `account number` 通常保持不变，因此银行卡和支票簿通常不会更换。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 4 个月无工资入账可能自动转 Savings Account | 通过：4 个月超过 3+ months 条件 | `salary-account-to-a-savings-account.md#L7-L11` |
| 转换后需维持 Savings Account 最低余额 | 通过 | `salary-account-to-a-savings-account.md#L33-L35` |
| Regular Savings 印度最低余额 ₹5,000 | 通过 | `savings-account-overview.md#L40-L48` |
| Digital Zero Balance 无最低余额 | 通过 | `savings-account-overview.md#L40-L48` |
| Senior Citizens/Students 印度最低余额 ₹1,000 | 通过 | `savings-account-overview.md#L40-L48` |
| 数字渠道转换步骤 | 通过 | `salary-account-to-a-savings-account.md#L44-L51` |
| debit card、chequebook、account number 通常不变 | 通过 | `salary-account-to-a-savings-account.md#L37-L40` |

自检结论：四个问点均已回答；最低余额按文档保留账户类型差异，并给出印度普通储蓄账户的默认值。

## 本次单题执行更新：Q3

更新时间：2026-08-10。

问题：一位居住在孟加拉国的客户想申请个人贷款，最高能借多少？利率范围是多少？与印度受薪人士相比是高还是低？他还想用 UPI 来偿还贷款，这可行吗？如果不可行，他可以通过什么渠道进行还款？

结论：

| 问点 | 答案 |
|---|---|
| 孟加拉国个人贷款最高额度 | `BDT 35,00,000` |
| 孟加拉国利率范围 | `13.50% – 21.00% p.a.` |
| 与印度受薪人士相比 | 更高；印度/斯里兰卡受薪人士为 `11.75% – 17.99% p.a.` |
| 能否用 UPI 还款 | 不可行；UPI services currently available in India for ZX Bank account holders |
| 替代渠道 | 文档明确支持 App 内 dedicated remittance options 用于 cross-border payments/remittances；个人贷款服务可通过所在国家分行、ZX Bank Asia Mobile App/NetBanking、Customer Care 或 Zia 办理，但源文没有单列“个人贷款还款渠道” |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `personal-loan.md` | `doc_047` | 标题为 `ZX Bank Ltd. – Personal Loan Information`；摘要覆盖 personal loan features、interest rates by customer type、maximum loan amounts by country 和 how to apply | 判断孟加拉国最高额度、利率范围，并与印度受薪人士利率比较 |
| `upi-zx-bank-asia.md` | `doc_058` | 标题为 `Unified Payments Interface (UPI) – ZX Bank Asia`；摘要覆盖 UPI 激活、限额和 India-only support channels | 判断孟加拉国客户是否可以使用 UPI，以及跨境支付替代提示 |

路由判断：未路由到 `cross-border-payments.md`，因为题目询问的是 UPI 是否可用于个人贷款还款，UPI 文档已直接给出 India-only 限制和 dedicated remittance options 提示；未路由到其他贷款文档，因为额度和利率问题明确限定为 personal loan。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `personal-loan.md` | `ch_2` | L17-L28 | 定位印度/斯里兰卡受薪人士与孟加拉国等国家的利率范围 |
| `personal-loan.md` | `ch_4` | L52-L63 | 定位孟加拉国最高个人贷款额度 |
| `personal-loan.md` | `ch_5` | L64-L74 | 定位个人贷款相关服务/申请渠道 |
| `upi-zx-bank-asia.md` | `ch_4` | L56-L71 | 定位 UPI 支持渠道、India-only 可用性和跨境替代提示 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `personal-loan.md` | L17-L25 | Salaried (India, Sri Lanka) 利率为 11.75% – 17.99%；Bangladesh, Bhutan, Nepal 利率为 13.50% – 21.00%，且受本地市场和分行/国家差异影响 |
| `personal-loan.md` | L52-L60 | Bangladesh 个人贷款最高额度为 BDT 35,00,000；最终额度受银行政策、申请人资料和信用评估影响 |
| `personal-loan.md` | L64-L68 | 个人贷款相关渠道包括所在国家任意 ZX Bank branch、ZX Bank Asia Mobile App、NetBanking、24x7 Customer Care 或 App 内 Zia |
| `upi-zx-bank-asia.md` | L56-L67 | UPI 支持渠道；UPI services currently available in India for ZX Bank account holders；cross-border payments/remittances 使用 App 内 dedicated remittance options |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_047.jsonl` | 不存在 |
| `doc_058.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

孟加拉国客户申请个人贷款，最高可借 `BDT 35,00,000`。利率范围为 `13.50% – 21.00% p.a.`，并且受本地市场审查及分行/国家差异影响。

与印度受薪人士相比，孟加拉国客户的利率更高：印度/斯里兰卡受薪人士利率为 `11.75% – 17.99% p.a.`，低于孟加拉国适用的 `13.50% – 21.00% p.a.`。

用 UPI 还款不可行，因为 UPI services currently available in India for ZX Bank account holders；孟加拉国不在 UPI 可用范围内。

替代渠道需区分两层：

1. 对跨境支付/汇款，UPI 文档明确说明应使用 App 内 dedicated remittance options。
2. 对个人贷款服务，个人贷款文档列出的可办理渠道包括所在国家任意 `ZX Bank branch`、`ZX Bank Asia Mobile App`、`NetBanking`、`24x7 Customer Care` 或 App 内 `Zia`。但源文没有单独列出“个人贷款还款渠道”，因此不能把这些写成已明确命名的还款渠道，只能作为个人贷款服务渠道说明。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 孟加拉国个人贷款最高 BDT 35,00,000 | 通过 | `personal-loan.md#L52-L60` |
| 孟加拉国利率 13.50% – 21.00% p.a. | 通过 | `personal-loan.md#L17-L25` |
| 印度/斯里兰卡受薪人士利率 11.75% – 17.99% p.a. | 通过 | `personal-loan.md#L19-L22` |
| 孟加拉国客户利率更高 | 通过：孟加拉国区间上下限均高于印度/斯里兰卡受薪人士区间 | `personal-loan.md#L19-L25` |
| UPI 不可用于孟加拉国客户 | 通过：UPI 当前仅印度 ZX Bank 账户持有人可用 | `upi-zx-bank-asia.md#L65-L67` |
| App 内 dedicated remittance options 是跨境替代提示 | 通过 | `upi-zx-bank-asia.md#L65-L67` |
| 分行、App/NetBanking、Customer Care/Zia 是个人贷款服务渠道 | 通过，但源文写作 `How to Apply`，不是专门的 repayment channels | `personal-loan.md#L64-L68` |

自检结论：贷款额度、利率比较和 UPI 不可用均有直接来源支撑；“还款渠道”在源文中没有被单独列明，因此答案保留了来源边界，避免把申请/服务渠道误写成明确还款渠道。

## 本次单题执行更新：Q4

更新时间：2026-08-10。

问题：一位尼泊尔客户想用黄金饰品做抵押获得贷款，然后用贷款所得在尼泊尔开立定期存款，再用该定期存款做抵押获取另一笔贷款。请计算：黄金贷款的最高 LTV 是多少？尼泊尔定期存款的最低起存金额是多少？定期存款可抵押贷款的比例是多少？

结论：

| 问点 | 答案 |
|---|---|
| 黄金贷款最高 LTV | 最高为黄金 market value 的 `75%` |
| 尼泊尔定期存款最低起存金额 | `NPR 1,500` |
| 定期存款可抵押贷款比例 | 最高为 FD value 的 `90%` |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `zx-bank-gold-loan.md` | `doc_070` | 标题为 `ZX Bank Gold Loan`；摘要覆盖 gold loan、maximum loan amount、LTV、documents 和申请方式 | 判断黄金饰品抵押贷款最高 LTV |
| `zx-bank-fixed-deposits.md` | `doc_069` | 标题为 `ZX Bank Fixed Deposits`；摘要覆盖 fixed deposits、minimum deposits by country、loan against FD 和 opening channels | 判断尼泊尔 FD 最低起存金额，以及 FD 可抵押贷款比例 |

路由判断：未路由到 `zx-bank-house-loan.md`、`personal-loan.md` 或其他贷款文档，因为题目链路明确是 gold loan → fixed deposit → loan against FD；两份命中文档已经分别覆盖黄金抵押和 FD 抵押。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `zx-bank-gold-loan.md` | `ch_3` | L24-L31 | 定位黄金贷款最高额度与 LTV |
| `zx-bank-fixed-deposits.md` | `ch_1` | L7-L17 | 定位 Loan Against FD 最高比例 |
| `zx-bank-fixed-deposits.md` | `ch_2` | L18-L27 | 定位各国家 FD 最低起存金额，尤其 Nepal |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `zx-bank-gold-loan.md` | L24-L28 | 黄金贷款 `Loan-to-Value (LTV)` 最高为黄金 market value 的 75%；其他国家包括 Nepal 可按当地等值货币和监管上限办理 |
| `zx-bank-fixed-deposits.md` | L7-L14 | Fixed Deposits 支持 `Loan Against FD`，可获得 instant overdraft or loans up to 90% of FD value |
| `zx-bank-fixed-deposits.md` | L18-L24 | FD 最低起存金额按国家不同；Nepal 为 `NPR 1,500` |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_070.jsonl` | 不存在 |
| `doc_069.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

这条链路中的三个数值分别是：

| 计算项 | 数值 | 说明 |
|---|---:|---|
| 黄金贷款最高 LTV | `75%` | 最高可贷黄金 market value 的 75% |
| 尼泊尔 FD 最低起存金额 | `NPR 1,500` | FD minimum deposit 中 Nepal 对应金额 |
| FD 抵押贷款比例 | `90%` | 可获得最高 FD value 90% 的 overdraft 或 loan |

因此，尼泊尔客户先用黄金饰品抵押时，黄金贷款最高 LTV 为 `75%`；用贷款所得在尼泊尔开立 FD 时，最低起存金额是 `NPR 1,500`；之后再以该 FD 抵押时，最高可贷比例为 FD value 的 `90%`。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 黄金贷款最高 LTV 为 75% | 通过 | `zx-bank-gold-loan.md#L24-L28` |
| 尼泊尔 FD 最低起存金额为 NPR 1,500 | 通过 | `zx-bank-fixed-deposits.md#L18-L24` |
| FD 抵押贷款比例最高为 90% | 通过 | `zx-bank-fixed-deposits.md#L7-L14` |

自检结论：三个计算点均为直接数值提取，无需额外换算；每个数值均有源文行号支撑。

## 本次单题执行更新：Q5（绿色金融题）

更新时间：2026-08-10。

问题：ZX Bank 获得过绿色金融方面的奖项。请找出银行中至少 4 个与 ESG/绿色金融直接相关的产品或服务，并说明客户的存款如何参与绿色金融项目。哪些国家的项目被特别提及？

结论：

| 问点 | 答案 |
|---|---|
| 绿色金融奖项 | `Excellence in Green Finance Award (2022)`，表彰支持 Bhutan hydropower 和 Nepal solar ventures 的绿色融资项目 |
| 至少 4 个 ESG/绿色金融相关产品或服务 | Green Finance Projects、Green Homes、Green & Sustainability Loans、Fixed Deposits 的 ESG/CSR 资金参与、Women Empowerment Loans / micro-loans |
| 客户存款如何参与 | 部分 deposits 会 fuel green finance projects，例如 Bhutanese hydropower 和 Nepalese solar ventures |
| 特别提及的国家 | Bhutan、Nepal；另有 ESG 社会项目提及 rural India、Bangladesh，以及 South Asia women-led businesses |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `awards-and-recognitions.md` | `doc_016` | 标题为 `ZX Bank Ltd. — Awards & Recognitions`；摘要覆盖 green finance、financial inclusion、women banking 等奖项 | 确认绿色金融奖项及奖项提到的国家项目 |
| `about-zx-bank-ltd.md` | `doc_001` | 标题为 `ZX Bank Ltd.`；包含 `CSR & ESG Focus` 节点 | 获取银行整体 ESG/CSR 项目清单 |
| `zx-bank-house-loan.md` | `doc_071` | 标题为 `ZX Bank House Loan`；Special Benefits 节点包含 Green Homes | 识别绿色住房贷款优惠 |
| `zx-bank-business-loans.md` | `doc_065` | 标题为 `ZX Bank – Business Loans`；Business Loans 类型包含 Women Empowerment Loans 和 Green & Sustainability Loans | 识别企业端 ESG/绿色贷款产品 |
| `zx-bank-fixed-deposits.md` | `doc_069` | 标题为 `ZX Bank Fixed Deposits`；包含 `ESG & CSR Initiatives` 节点 | 说明客户存款如何参与绿色金融项目 |

路由判断：未路由到普通分支网络、ATM、个人贷款等文档，因为问题核心是绿色金融奖项、ESG 项目、绿色产品和存款资金用途；上述五个文档已覆盖奖项、银行 ESG 概览、绿色住房、绿色企业融资和存款参与路径。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `awards-and-recognitions.md` | `ch_2` | L9-L14 | 定位 Excellence in Green Finance Award 及 Bhutan/Nepal 项目 |
| `awards-and-recognitions.md` | `ch_4`, `ch_5` | L21-L32 | 定位金融普惠、microfinance、women-led enterprises 等社会 ESG 项目 |
| `about-zx-bank-ltd.md` | `ch_6` | L92-L103 | 定位 CSR & ESG Focus 总览 |
| `zx-bank-house-loan.md` | `ch_5` | L54-L61 | 定位 Green Homes |
| `zx-bank-business-loans.md` | `ch_2_5`, `ch_2_6` | L31-L38 | 定位 Women Empowerment Loans 与 Green & Sustainability Loans |
| `zx-bank-fixed-deposits.md` | `ch_6` | L73-L78 | 定位存款参与绿色金融项目的说明 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `awards-and-recognitions.md` | L9-L12 | ZX Bank 获得 `Excellence in Green Finance Award (2022)`；亮点是支持 Bhutan’s hydropower 和 Nepal’s solar ventures，推进 ESG banking goals |
| `awards-and-recognitions.md` | L21-L29 | Bangladesh 金融普惠奖涉及 digital banking、microfinance、financial literacy；Women’s Banking Initiative 涉及 micro-loan programs 和 women-led enterprises |
| `about-zx-bank-ltd.md` | L92-L99 | CSR & ESG Focus 包括 Green Finance Projects、rural India & Bangladesh 金融教育、South Asia women-led businesses micro-loans |
| `zx-bank-house-loan.md` | L54-L58 | Green Homes：eco-friendly/energy-efficient homes 可获得 lower rates |
| `zx-bank-business-loans.md` | L31-L35 | Women Empowerment Loans 面向 women entrepreneurs / women-led businesses；Green & Sustainability Loans 融资 renewable energy、eco-friendly infrastructure、climate-smart initiatives |
| `zx-bank-fixed-deposits.md` | L73-L75 | 部分 deposits fuel Bhutanese hydropower 和 Nepalese solar ventures，使 savings contribute to a sustainable future |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_016.jsonl` | 不存在 |
| `doc_001.jsonl` | 不存在 |
| `doc_071.jsonl` | 不存在 |
| `doc_065.jsonl` | 不存在 |
| `doc_069.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

ZX Bank 的绿色金融奖项是 `Excellence in Green Finance Award (2022)`，获奖原因是其绿色融资项目支持 `Bhutan’s hydropower` 和 `Nepal’s solar ventures`，并推动银行业 ESG 目标。

与 ESG/绿色金融直接相关的产品或服务至少包括：

| 产品或服务 | ESG/绿色金融关联 |
|---|---|
| `Green Finance Projects` | 与 Bhutan hydropower、Nepal solar ventures 合作，属于绿色融资项目 |
| `Green Homes` | 对 eco-friendly / energy-efficient homes 提供 lower rates |
| `Green & Sustainability Loans` | 为 renewable energy、eco-friendly infrastructure、climate-smart business initiatives 融资 |
| `Fixed Deposits ESG & CSR Initiatives` | 部分客户存款投入绿色金融项目，使储蓄支持可持续未来 |
| `Women Empowerment Loans / micro-loans` | 面向 women entrepreneurs / women-led businesses，是 ESG 中社会维度的金融赋能项目 |
| `Financial Literacy / Microfinance initiatives` | 面向 rural India & Bangladesh 的金融教育、microfinance 和普惠金融项目，属于社会维度 ESG |

客户存款参与绿色金融项目的方式是：部分定期存款资金会投入绿色金融项目，例如 `Bhutanese hydropower` 和 `Nepalese solar ventures`，因此客户的 savings 会 contribute to a sustainable future。

被特别提及的绿色项目国家是 `Bhutan` 和 `Nepal`。此外，社会维度 ESG 项目还特别提及 `India`、`Bangladesh` 和 South Asia 的 women-led businesses。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| ZX Bank 获得 Excellence in Green Finance Award (2022) | 通过 | `awards-and-recognitions.md#L9-L12` |
| 绿色金融奖项涉及 Bhutan hydropower 和 Nepal solar ventures | 通过 | `awards-and-recognitions.md#L9-L12` |
| CSR & ESG Focus 包括 Green Finance Projects、金融教育和 Women Empowerment Loans | 通过 | `about-zx-bank-ltd.md#L92-L99` |
| Green Homes 对环保/节能住房提供 lower rates | 通过 | `zx-bank-house-loan.md#L54-L58` |
| Green & Sustainability Loans 支持 renewable energy、eco-friendly infrastructure、climate-smart initiatives | 通过 | `zx-bank-business-loans.md#L34-L35` |
| Women Empowerment Loans / micro-loans 属于 ESG 社会维度 | 通过 | `zx-bank-business-loans.md#L31-L32`, `awards-and-recognitions.md#L27-L29` |
| 客户存款会参与 Bhutanese hydropower 和 Nepalese solar ventures | 通过 | `zx-bank-fixed-deposits.md#L73-L75` |
| 特别提及的绿色项目国家为 Bhutan 和 Nepal | 通过 | `awards-and-recognitions.md#L9-L12`, `zx-bank-fixed-deposits.md#L73-L75` |

自检结论：题目要求的“至少 4 个”已提供 6 个；客户存款参与机制和特别提及国家均有直接来源支撑。

## 本次单题执行更新：Q6

更新时间：2026-08-10。

问题：如果你的 ZX Bank 借记卡被盗并产生了欺诈交易，你可以通过哪些渠道立即冻结/挂失卡片？银行处理欺诈投诉的目标解决时间是多少天？在问题解决后，如果你想申请新的支票簿，可以通过哪几种方式申请？请列出所有渠道。

结论：

| 问点 | 答案 |
|---|---|
| 立即冻结/挂失或报告卡片渠道 | 24x7 fraud hotline、`fraudreport@zxbank.asia`、ZX Bank Asia App `Support > Report Fraud`、Mobile App/NetBanking 的 `Card Management` 或 `Account Services`、App 内 `Block Card` / `Block Instantly` |
| 欺诈投诉目标解决时间 | `10 working days` |
| 新支票簿申请渠道 | ZX Bank Mobile App、NetBanking、Branch、ZX Bank ATM、ZX Bank Customer Care |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fraud-transaction.md` | `doc_033` | 标题为 `How to Report a Fraud Transaction at ZX Bank`；摘要覆盖 fraud hotline、email、App fraud report、block card、freeze account 和 resolution target | 判断欺诈交易后冻结/挂失渠道与目标解决时间 |
| `zx-bank-asia-mobile-app-guide.md` | `doc_061` | 标题为 `ZX Bank Asia Mobile App Guide`；App features 包含 cards 管理和 block card immediate effect | 补充 App 内卡片即时 block 的具体路径 |
| `apply-for-a-cheque-book.md` | `doc_005` | 标题为 `How to Apply for a Cheque Book at ZX Bank`；摘要覆盖 App、NetBanking、Branch、ATM、Customer Care 申请方式 | 枚举支票簿申请的所有渠道 |

路由判断：未路由到普通账户、储蓄账户或卡片营销文档，因为题目核心是欺诈交易处置、App 内即时卡片冻结，以及支票簿申请渠道；上述三个文档已覆盖全部问点。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fraud-transaction.md` | `ch_1` | L7-L20 | 定位立即联系银行的 hotline、email、App Report Fraud 渠道 |
| `fraud-transaction.md` | `ch_2` | L21-L29 | 定位 Mobile App / NetBanking 的 Block/Card Hotlisting 或 Freeze Account |
| `fraud-transaction.md` | `ch_5` | L50-L57 | 定位投诉跟踪和 10 working days 目标解决时间 |
| `fraud-transaction.md` | `ch_6` | L58-L67 | 定位 urgent blocking 的 Block Instantly |
| `zx-bank-asia-mobile-app-guide.md` | `ch_5_4_1` | L73-L78 | 定位 App 内 Select card > More options > Block |
| `apply-for-a-cheque-book.md` | `ch_1` 到 `ch_5` | L7-L64 | 定位支票簿 App、NetBanking、Branch、ATM、Customer Care 五种申请渠道 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fraud-transaction.md` | L7-L18 | 立即联系渠道包括 24x7 hotline、email `fraudreport@zxbank.asia`、ZX Bank Asia App `Support > Report Fraud` |
| `fraud-transaction.md` | L21-L26 | 可通过 Mobile App 或 NetBanking 进入 `Card Management` 或 `Account Services`，选择 `Block/Card Hotlisting` 或 `Freeze Account` 并确认 |
| `fraud-transaction.md` | L50-L54 | 可通过 App `Support > Track Requests` 或 hotline 跟踪，目标解决时间为 `10 working days` |
| `fraud-transaction.md` | L58-L63 | 紧急冻结可使用 App 的 `Block Instantly` 选项 |
| `zx-bank-asia-mobile-app-guide.md` | L71-L77 | App 内卡片管理支持 `Block Card`: Select card → More options → Block，immediate effect |
| `apply-for-a-cheque-book.md` | L7-L15 | 支票簿可通过 ZX Bank Mobile App 申请 |
| `apply-for-a-cheque-book.md` | L19-L25 | 支票簿可通过 NetBanking 申请 |
| `apply-for-a-cheque-book.md` | L29-L34 | 支票簿可在 Branch 申请 |
| `apply-for-a-cheque-book.md` | L38-L43 | 支票簿可通过 ZX Bank ATM 申请 |
| `apply-for-a-cheque-book.md` | L47-L51 | 支票簿可通过 ZX Bank Customer Care 申请 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_033.jsonl` | 不存在 |
| `doc_061.jsonl` | 不存在 |
| `doc_005.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

如果 ZX Bank 借记卡被盗并产生欺诈交易，可以通过以下渠道立即冻结/挂失或报告：

| 渠道 | 操作 |
|---|---|
| 24x7 fraud hotline | 按所在国家拨打热线：India、Sri Lanka、Bangladesh、Bhutan、Nepal 均有号码 |
| Email | 发送到 `fraudreport@zxbank.asia` |
| ZX Bank Asia App | 进入 `Support > Report Fraud` |
| Mobile App / NetBanking | 进入 `Card Management` 或 `Account Services`，选择 `Block/Card Hotlisting` 或 `Freeze Account` 并确认 |
| App 内卡片管理 | `Select card > More options > Block`，immediate effect |
| App urgent blocking | 使用 `Block Instantly` |

银行处理欺诈投诉的目标解决时间是 `10 working days`。

问题解决后，如果要申请新的支票簿，可以通过以下全部渠道：

| 支票簿申请渠道 | 操作摘要 |
|---|---|
| ZX Bank Mobile App | `Services` 或 `Request Services` → `Cheque Book Request` |
| NetBanking | `Services > Cheque Book Request` |
| Branch | 到分行填写 `Cheque Book Request Form` |
| ZX Bank ATM | `Services > Cheque Book Request` |
| ZX Bank Customer Care | 拨打 24x7 helpline，验证信息后提交请求 |

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 可通过 24x7 hotline、email、App Report Fraud 报告 | 通过 | `fraud-transaction.md#L7-L18` |
| 可通过 Mobile App/NetBanking 执行 Block/Card Hotlisting 或 Freeze Account | 通过 | `fraud-transaction.md#L21-L26` |
| App 内 Select card > More options > Block 可立即生效 | 通过 | `zx-bank-asia-mobile-app-guide.md#L71-L77` |
| 可使用 App 的 Block Instantly 紧急冻结 | 通过 | `fraud-transaction.md#L58-L63` |
| 欺诈投诉目标解决时间为 10 working days | 通过 | `fraud-transaction.md#L50-L54` |
| 支票簿可通过 Mobile App 申请 | 通过 | `apply-for-a-cheque-book.md#L7-L15` |
| 支票簿可通过 NetBanking 申请 | 通过 | `apply-for-a-cheque-book.md#L19-L25` |
| 支票簿可在 Branch 申请 | 通过 | `apply-for-a-cheque-book.md#L29-L34` |
| 支票簿可通过 ZX Bank ATM 申请 | 通过 | `apply-for-a-cheque-book.md#L38-L43` |
| 支票簿可通过 Customer Care 申请 | 通过 | `apply-for-a-cheque-book.md#L47-L51` |

自检结论：冻结/挂失、目标解决时间和支票簿五种申请渠道均已覆盖；每个渠道均有源文行号支撑。

## 本次单题执行更新：Q7

更新时间：2026-08-10。

问题：ZX Bank 在 5 个国家运营。请列出以下每项服务在哪些国家可用、在哪些国家不可用：(1) UPI 支付，(2) e-KYC 数字身份验证，(3) 学生信用卡，(4) 跨境汇款。如果一位在孟加拉国的学生想申请信用卡，他有什么选择？

结论：

| 服务 | 可用国家 | 不可用国家 |
|---|---|---|
| UPI 支付 | India | Sri Lanka、Bangladesh、Bhutan、Nepal |
| e-KYC 数字身份验证 | India、Sri Lanka、Nepal | Bangladesh、Bhutan |
| 学生信用卡 | India、Sri Lanka、Nepal | Bangladesh、Bhutan |
| 跨境汇款 | India、Sri Lanka、Nepal、Bhutan | Bangladesh |

孟加拉国学生不能申请 `ZX Student Credit Card`，因为学生卡只面向 India、Sri Lanka、Nepal 的 college/university students。若他想申请信用卡，只能考虑非学生卡产品，例如普通信用卡，但必须满足对应卡种的收入、年龄、CIBIL 或其他资格；同时，孟加拉国不支持 e-KYC，不能走 e-KYC 数字身份验证路径。

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `about-zx-bank-ltd.md` | `doc_001` | 标题为 `ZX Bank Ltd.`；包含 operating countries、digital banking、remittances | 获取 5 个运营国家全集，以及汇款服务背景 |
| `upi-zx-bank-asia.md` | `doc_058` | 标题为 `Unified Payments Interface (UPI) – ZX Bank Asia`；摘要包含 India-only support channels | 判断 UPI 可用国家 |
| `zx-bank-credit-card.md` | `doc_068` | 标题为 `ZX Bank Credit Card Options`；摘要覆盖 Student card、e-KYC、各卡资格 | 判断学生信用卡和 e-KYC 可用国家，并分析孟加拉国学生选择 |
| `cross-border-payments.md` | `doc_031` | 标题为 `Fast Cross-Border Payments with ZX Bank`；摘要覆盖 India、Sri Lanka、Nepal、Bhutan 跨境支付 | 判断跨境汇款可用国家 |

路由判断：未路由到普通分行、ATM 或贷款文档，因为题目是服务可用性矩阵，核心证据来自运营国家总览、UPI、信用卡/e-KYC 和跨境支付四类文档。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `about-zx-bank-ltd.md` | `ch_1` | L12-L30 | 定位 5 个运营国家全集 |
| `about-zx-bank-ltd.md` | `ch_2_3`, `ch_2_4` | L44-L52 | 定位 Digital Banking 和 Remittances 总览 |
| `upi-zx-bank-asia.md` | `ch_4` | L56-L71 | 定位 UPI India-only 说明 |
| `zx-bank-credit-card.md` | `ch_4` | L72-L92 | 定位 Student Credit Card 的适用国家和资格 |
| `zx-bank-credit-card.md` | `ch_6` | L115-L120 | 定位 e-KYC 可用国家 |
| `cross-border-payments.md` | `ch_1` | L3-L8 | 定位跨境汇款可用国家 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `about-zx-bank-ltd.md` | L12-L27 | ZX Bank 运营国家为 India、Sri Lanka、Bangladesh、Bhutan、Nepal |
| `about-zx-bank-ltd.md` | L44-L52 | Digital Banking 包含 NetBanking & UPI、e-KYC；Remittances 为 India、Sri Lanka、Nepal、Bhutan |
| `upi-zx-bank-asia.md` | L65-L67 | UPI services currently available in India for ZX Bank account holders |
| `zx-bank-credit-card.md` | L72-L89 | ZX Student Credit Card 面向 India、Sri Lanka、Nepal only 的 college & university students；资格要求年龄、学生 ID、admission proof 等 |
| `zx-bank-credit-card.md` | L115-L120 | e-KYC available for India、Sri Lanka、Nepal residents |
| `cross-border-payments.md` | L3-L5 | Cross-border payment services between India、Sri Lanka、Nepal、Bhutan |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_001.jsonl` | 不存在 |
| `doc_058.jsonl` | 不存在 |
| `doc_068.jsonl` | 不存在 |
| `doc_031.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

以 ZX Bank 的 5 个运营国家 `India`、`Sri Lanka`、`Bangladesh`、`Bhutan`、`Nepal` 为全集，各服务可用性如下：

| 服务 | 可用国家 | 不可用国家 | 判断依据 |
|---|---|---|---|
| UPI 支付 | India | Sri Lanka、Bangladesh、Bhutan、Nepal | UPI 当前仅适用于 India 的 ZX Bank account holders |
| e-KYC 数字身份验证 | India、Sri Lanka、Nepal | Bangladesh、Bhutan | 信用卡申请 e-KYC 仅对 India、Sri Lanka、Nepal residents 可用 |
| 学生信用卡 | India、Sri Lanka、Nepal | Bangladesh、Bhutan | Student card 标注为 India、Sri Lanka、Nepal only |
| 跨境汇款 | India、Sri Lanka、Nepal、Bhutan | Bangladesh | 跨境支付服务覆盖 India、Sri Lanka、Nepal、Bhutan |

孟加拉国学生不能申请 `ZX Student Credit Card`，因为学生信用卡不覆盖 Bangladesh。他可以考虑申请其他信用卡，例如 `ZX Gold Credit Card` 等非学生卡，但必须满足对应卡种的收入、年龄、CIBIL 等资格条件；并且因为 Bangladesh 不在 e-KYC 可用国家中，他不能依赖 e-KYC 完成数字身份验证。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 运营国家全集为 India、Sri Lanka、Bangladesh、Bhutan、Nepal | 通过 | `about-zx-bank-ltd.md#L12-L27` |
| UPI 仅 India 可用 | 通过 | `upi-zx-bank-asia.md#L65-L67` |
| e-KYC 仅 India、Sri Lanka、Nepal residents 可用 | 通过 | `zx-bank-credit-card.md#L115-L120` |
| Student Credit Card 仅 India、Sri Lanka、Nepal 可用 | 通过 | `zx-bank-credit-card.md#L72-L89` |
| 跨境汇款覆盖 India、Sri Lanka、Nepal、Bhutan | 通过 | `cross-border-payments.md#L3-L5`, `about-zx-bank-ltd.md#L50-L52` |
| Bangladesh 学生不能申请学生信用卡 | 通过：Bangladesh 不在 Student card only 国家列表中 | `zx-bank-credit-card.md#L72-L89` |
| Bangladesh 不支持 e-KYC | 通过：e-KYC 国家列表不含 Bangladesh | `zx-bank-credit-card.md#L115-L120` |

自检结论：四项服务的可用/不可用国家均以 5 个运营国家为全集推导；孟加拉国学生的选择与限制均由学生卡和 e-KYC 国家范围支撑。

## 本次单题执行更新：Q8

更新时间：2026-08-10。

问题：比较 ZX Bank 房屋贷款和汽车贷款所需的文件。哪些文件是两者都需要的？哪些是房屋贷款独有的？哪些是汽车贷款独有的？两种贷款是否都支持完全在线申请？

结论：

| 比较项 | 答案 |
|---|---|
| 两者都需要 | 身份/KYC 类文件、收入证明 |
| 房屋贷款独有 | `Address Proof` 明确单列；`Property Documents`，包括 sale agreement、title deed、approved plan；`Form 16` 明确列在收入证明中 |
| 汽车贷款独有 | `Employment/Business Proof`、`Vehicle Quotation/Invoice`、photograph 明确列在 KYC 中 |
| 在线申请 | 两者都支持在线申请渠道；汽车贷款明确支持 App/NetBanking、e-KYC 和文件数字上传；房屋贷款明确支持 Home Loan Portal 和 Mobile App，但源文没有像汽车贷款一样明确写出“所有文件均可数字上传” |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `zx-bank-house-loan.md` | `doc_071` | 标题为 `ZX Bank House Loan`；摘要覆盖 house loan documents required 和 how to apply | 提取房屋贷款所需文件和在线申请方式 |
| `zx-bank-car-loan.md` | `doc_066` | 标题为 `ZX Bank Car Loan`；摘要覆盖 car loan documentation required、digital upload、online/offline apply | 提取汽车贷款所需文件和在线申请方式 |

路由判断：未路由到 personal loan、bike loan 或 gold loan 文档，因为题目明确比较 house loan 与 car loan 的 documents 和 online application；两份命中文档已覆盖全部比较维度。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `zx-bank-house-loan.md` | `ch_3` | L32-L40 | 定位房屋贷款 Documents Required |
| `zx-bank-house-loan.md` | `ch_4` | L41-L53 | 定位房屋贷款 How to Apply |
| `zx-bank-car-loan.md` | `ch_3` | L28-L38 | 定位汽车贷款 Documentation Required 和 digital upload |
| `zx-bank-car-loan.md` | `ch_4_1`, `ch_4_2` | L39-L55 | 定位汽车贷款 Online 和 Offline / Branch 申请方式 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `zx-bank-house-loan.md` | L32-L37 | 房屋贷款需要 ID Proof、Address Proof、Income Proof、Property Documents |
| `zx-bank-house-loan.md` | L41-L50 | 房屋贷款可通过 Home Loan Portal、ZX Bank Asia Mobile App 或 Branch 申请 |
| `zx-bank-car-loan.md` | L28-L35 | 汽车贷款需要 KYC Documents、Income Proof、Employment/Business Proof、Vehicle Quotation/Invoice；所有文件可通过 App/NetBanking 数字上传 |
| `zx-bank-car-loan.md` | L39-L52 | 汽车贷款可 Online 申请：App 或 NetBanking、填写信息、使用 e-KYC 上传文件、提交；也可 Branch 线下申请 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_071.jsonl` | 不存在 |
| `doc_066.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

文件比较如下：

| 类别 | 文件 |
|---|---|
| 两者都需要 | 身份/KYC 类文件：房屋贷款列 `ID Proof`，汽车贷款列 `KYC Documents`；收入证明：房屋贷款列 salary slips、ITR、bank statement、Form 16，汽车贷款列 salary slips/ITR/bank statements |
| 房屋贷款独有 | `Property Documents`，包括 sale agreement、title deed、approved plan；房屋贷款还明确单列 `Address Proof`；`Form 16` 也在房屋贷款收入证明中明确列出 |
| 汽车贷款独有 | `Employment/Business Proof`，包括 offer letter/business registration；`Vehicle Quotation/Invoice`；汽车贷款 KYC 中还明确列 `photograph` |

在线申请方面，两种贷款都支持在线申请渠道：

| 贷款类型 | 在线申请情况 |
|---|---|
| 房屋贷款 | 支持通过 `ZX Bank Home Loan Portal` 在线申请，也支持 `ZX Bank Asia` Mobile App；但源文没有明确写出所有文件可在线上传 |
| 汽车贷款 | 明确支持通过 `ZX Bank Asia App` 或 `ZX NetBanking` 在线申请，并且所有文件可数字上传，在线流程包含 e-KYC、填写申请、上传文件和提交 |

因此，如果“完全在线申请”严格理解为“申请和文件上传都在数字渠道完成”，汽车贷款有直接明文支撑；房屋贷款有在线申请渠道支撑，但源文没有明确到文件数字上传这一层。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 房屋贷款需要 ID Proof、Address Proof、Income Proof、Property Documents | 通过 | `zx-bank-house-loan.md#L32-L37` |
| 汽车贷款需要 KYC、Income Proof、Employment/Business Proof、Vehicle Quotation/Invoice | 通过 | `zx-bank-car-loan.md#L28-L35` |
| 两者都需要身份/KYC 类文件和收入证明 | 通过：两份文件均列明相应类别 | `zx-bank-house-loan.md#L34-L36`, `zx-bank-car-loan.md#L30-L31` |
| 房屋贷款独有 Property Documents | 通过 | `zx-bank-house-loan.md#L37-L37` |
| 汽车贷款独有 Employment/Business Proof 和 Vehicle Quotation/Invoice | 通过 | `zx-bank-car-loan.md#L32-L33` |
| 房屋贷款支持 Online 和 Mobile App 申请 | 通过 | `zx-bank-house-loan.md#L41-L50` |
| 汽车贷款支持 App/NetBanking 在线申请、e-KYC 和数字上传文件 | 通过 | `zx-bank-car-loan.md#L35-L47` |
| 房屋贷款源文未明确所有文件数字上传 | 通过：读取行段只说明 Online / Mobile App / Branch 渠道，未出现 digital upload 描述 | `zx-bank-house-loan.md#L41-L50` |

自检结论：共同文件、独有文件和在线申请差异均有源文支撑；对“完全在线申请”的回答保留了房屋贷款文档未明确数字上传的边界。

## 本次单题执行更新：Q9

更新时间：2026-08-10。

问题：一位客户在海得拉巴的 HITEC City 科技园区工作。最近的 ZX Bank 分行在哪里（给出 IFSC 和联系电话）？如果他要前往孟买出差，孟买有哪些科技园区设有 ZX Bank ATM？他可以通过什么方式找到这些 ATM 的具体位置？

结论：

| 问点 | 答案 |
|---|---|
| HITEC City 最近分行 | `Madhapur Kavuri Hills, 500081` |
| IFSC | `ZXIN0001232` |
| 联系电话 | `040-45671232` |
| 孟买科技园 ATM | `Mindspace Airoli IT Park`、`Nesco IT Park`、`Infinity IT Park` |
| 查找具体位置方式 | ZX Bank Asia Mobile App 的 `Locate Branch/ATM`、ZX Bank ATM Locator、ASK Zia |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | `doc_011` | 标题为 `ZX Bank – ATM Locations at Tech Parks in Major Indian Cities`；摘要覆盖 Hyderabad HITEC City 和 Mumbai tech parks | 判断 HITEC City 所在区域，并列出孟买科技园 ATM |
| `hyderabad-branch-network.md` | `doc_035` | 标题为 `ZX Bank: Hyderabad Branch Network`；摘要覆盖 Hyderabad 各区域分行、IFSC 和电话 | 定位 Madhapur 附近分行的 IFSC 与联系电话 |
| `zx-bank-asia-mobile-app-guide.md` | `doc_061` | 标题为 `ZX Bank Asia Mobile App Guide`；包含 Locate Branch/ATM 功能 | 说明通过 App 查找分行/ATM |
| `atms-at-railway-stations-and-airports.md` | `doc_015` | 标题为 `ZX Bank ATM Locations at Major Railway Stations and Airports`；包含 ATM Locator 通用说明 | 说明可用 ZX Bank ATM Locator 查找最近 ATM |
| `ask-zia-your-24-7-banking-assistant.md` | `doc_006` | 标题为 `ASK Zia – Your 24/7 Banking Assistant`；摘要和正文说明 Zia 可定位 branches and ATMs | 说明可通过 Zia 查找具体位置 |

路由判断：未路由到普通孟买分行网络或一般 Hyderabad 文档之外的其他城市文档，因为题目一半是 HITEC City 附近分行，一半是 Mumbai tech park ATM 和定位方式；上述五个文档已覆盖地点、分行、ATM 和查询渠道。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | `ch_4` | L46-L58 | 定位 HITEC City 在 Madhapur, Hyderabad |
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | `ch_1` | L7-L19 | 定位孟买科技园区 ATM 列表 |
| `hyderabad-branch-network.md` | `ch_4` | L45-L57 | 定位 West Hyderabad / Madhapur 分行、IFSC、电话 |
| `zx-bank-asia-mobile-app-guide.md` | `ch_7` | L112-L121 | 定位 App 中 Locate Branch/ATM 功能 |
| `atms-at-railway-stations-and-airports.md` | 文末 ATM Locator 说明 | L176-L180 | 定位 ZX Bank ATM Locator 说明 |
| `ask-zia-your-24-7-banking-assistant.md` | `ch_1` | L7-L16 | 定位 Zia 可帮助 locate branches and ATMs |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | L46-L55 | HITEC City 位于 Madhapur, Hyderabad, Telangana 500081；Hyderabad 科技园 ATM 还包括 Raheja Mindspace IT Park、Cyber Pearl |
| `hyderabad-branch-network.md` | L45-L54 | West Hyderabad 分行中 `Madhapur Kavuri Hills, 500081` 的 IFSC 为 `ZXIN0001232`，电话为 `040-45671232` |
| `atm-locations-at-tech-parks-in-major-indian-cities.md` | L7-L16 | Mumbai 科技园 ATM 位于 Mindspace Airoli IT Park、Nesco IT Park、Infinity IT Park |
| `zx-bank-asia-mobile-app-guide.md` | L112-L117 | App 支持 `Locate Branch/ATM`，可查找支持国家的 ZX Bank locations |
| `atms-at-railway-stations-and-airports.md` | L176-L180 | 可用 ZX Bank Asia Mobile App 或 ZX Bank ATM Locator 查找最近 ATM |
| `ask-zia-your-24-7-banking-assistant.md` | L7-L12 | ASK Zia 可协助 locating branches and ATMs |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_011.jsonl` | 不存在 |
| `doc_035.jsonl` | 不存在 |
| `doc_061.jsonl` | 不存在 |
| `doc_015.jsonl` | 不存在 |
| `doc_006.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

HITEC City 位于 `Madhapur, Hyderabad, Telangana 500081`。在 Hyderabad 分行网络中，对应该区域最近的分行是：

| 分行 | IFSC | 联系电话 |
|---|---|---|
| `Madhapur Kavuri Hills, 500081` | `ZXIN0001232` | `040-45671232` |

如果他前往孟买出差，孟买设有 ZX Bank ATM 的科技园区包括：

| 科技园区 | 地址 |
|---|---|
| `Mindspace Airoli IT Park` | Building 2, Mindspace, Thane-Belapur Road, Airoli, Navi Mumbai, Maharashtra 400708 |
| `Nesco IT Park` | Gate 3, Western Express Highway, Goregaon (East), Mumbai, Maharashtra 400063 |
| `Infinity IT Park` | New Link Road, Malad (West), Mumbai, Maharashtra 400064 |

查找这些 ATM 具体位置的方式包括：

1. 使用 `ZX Bank Asia Mobile App` 的 `Locate Branch/ATM`。
2. 使用 `ZX Bank ATM Locator`。
3. 询问 `ASK Zia`，它可以帮助定位 branches and ATMs。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| HITEC City 位于 Madhapur, Hyderabad, Telangana 500081 | 通过 | `atm-locations-at-tech-parks-in-major-indian-cities.md#L46-L55` |
| 最近分行为 Madhapur Kavuri Hills, 500081 | 通过 | `hyderabad-branch-network.md#L45-L54` |
| IFSC 为 ZXIN0001232 | 通过 | `hyderabad-branch-network.md#L47-L50` |
| 联系电话为 040-45671232 | 通过 | `hyderabad-branch-network.md#L47-L50` |
| 孟买 ATM 科技园区为 Mindspace Airoli、Nesco、Infinity | 通过 | `atm-locations-at-tech-parks-in-major-indian-cities.md#L7-L16` |
| 可通过 App Locate Branch/ATM 查找 | 通过 | `zx-bank-asia-mobile-app-guide.md#L112-L117` |
| 可通过 ZX Bank ATM Locator 查找 | 通过 | `atms-at-railway-stations-and-airports.md#L176-L180` |
| 可通过 ASK Zia 定位 branches and ATMs | 通过 | `ask-zia-your-24-7-banking-assistant.md#L7-L12` |

自检结论：最近分行、IFSC、电话、孟买科技园 ATM 清单和三种定位方式均有源文行号支撑。

## 本次单题执行更新：Q10

更新时间：2026-08-10。

问题：一位 67 岁的印度退休老人想做以下三件事：(1) 开立定期存款获取最高利率，(2) 申请一张信用卡用于日常消费，(3) 租用一个银行保险箱存放遗产文件。请逐一分析：他能获得的最高 FD 利率是多少？他有资格申请哪些信用卡？他开立保险箱需要满足什么前提条件？整个流程中哪些步骤必须到分行办理？

结论：

| 问点 | 答案 |
|---|---|
| 最高 FD 利率 | `6.80% p.a.`，Senior Citizen Rate，期限 `3 years–5 years` |
| 有资格申请哪些信用卡 | 无。67 岁超过 Platinum、Gold、Women Empower、NRI 的 65 岁上限，也不符合 Student 的 18-25 岁条件 |
| 开立保险箱前提 | 必须是现有 ZX Bank customer，或开立 savings/current account；KYC 需更新，并提供 valid photo ID、address proof、recent passport-sized photo |
| 必须到分行办理的步骤 | 保险箱可用性确认可到分行或致电；正式保险箱申请、提交文件、签署协议、领取钥匙、实际操作保险箱均需到分行。FD 可通过 App/NetBanking 开立，不必必须到分行 |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `zx-bank-fixed-deposits.md` | `doc_069` | 标题为 `ZX Bank Fixed Deposits`；摘要覆盖 FD 开立方式、tenure、senior citizen 利率和 branch/App/NetBanking 渠道 | 判断退休老人最高 FD 利率，以及 FD 是否必须到分行 |
| `zx-bank-credit-card.md` | `doc_068` | 标题为 `ZX Bank Credit Card Options`；摘要覆盖各信用卡 eligibility | 判断 67 岁客户是否符合各信用卡年龄条件 |
| `open-a-locker.md` | `doc_045` | 标题为 `How to Open a Locker at ZX Bank Branch`；摘要覆盖 locker availability、eligibility、application process、rent、keys 和 operating locker | 判断保险箱前提条件及必须到分行办理的步骤 |

路由判断：未路由到 savings account 或 current account 详情文档，因为题目只要求保险箱开立前提是否需有 savings/current account，`open-a-locker.md` 已直接说明；未路由到信用卡帮助文档，因为资格判断由信用卡选项文档直接覆盖。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `zx-bank-fixed-deposits.md` | `ch_4` | L40-L58 | 定位 FD 可通过 App、NetBanking 或 Branch 开立 |
| `zx-bank-fixed-deposits.md` | `ch_5` | L59-L72 | 定位 Senior Citizen Rate 最高值 |
| `zx-bank-credit-card.md` | `ch_1_3`, `ch_2_3`, `ch_3_3`, `ch_4_3`, `ch_5_3` | L22-L25, L43-L46, L64-L68, L86-L89, L107-L110 | 定位所有信用卡年龄条件 |
| `open-a-locker.md` | `ch_1`, `ch_2` | L7-L24 | 定位 locker availability 和资格前提 |
| `open-a-locker.md` | `ch_3`, `ch_4`, `ch_5`, `ch_6` | L25-L58 | 定位保险箱申请、支付、领取钥匙和操作流程 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `zx-bank-fixed-deposits.md` | L40-L56 | FD 可通过 Mobile App、NetBanking 或 Branch 开立；Branch 方式需携带 KYC documents、填写 FD application form 并存入金额 |
| `zx-bank-fixed-deposits.md` | L59-L69 | Senior Citizen Rate 表中最高为 `6.80%`，对应 `3 years–5 years` |
| `zx-bank-credit-card.md` | L22-L25 | Platinum 年龄要求 21-65 |
| `zx-bank-credit-card.md` | L43-L46 | Gold 年龄要求 21-65 |
| `zx-bank-credit-card.md` | L64-L68 | Women Empower 年龄要求 21-65 |
| `zx-bank-credit-card.md` | L86-L89 | Student 年龄要求 18-25 |
| `zx-bank-credit-card.md` | L107-L110 | NRI 年龄要求 21-65 |
| `open-a-locker.md` | L7-L21 | 可到分行或致电查询 availability；资格要求现有或新开 savings/current account，KYC 更新，提供 valid photo ID、address proof、recent photo |
| `open-a-locker.md` | L25-L38 | 申请保险箱需到分行携带原件和复印件，填写 Locker Facility Application Form，提交 KYC，签署 Locker Hirer Agreement，支付押金/年租 |
| `open-a-locker.md` | L42-L55 | 获批后领取 locker keys；操作保险箱需在 branch working hours 到分行，携带 keys 和 valid ID，签署 Locker Access Register |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_069.jsonl` | 不存在 |
| `doc_068.jsonl` | 不存在 |
| `doc_045.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

FD 方面，这位客户 67 岁，属于 Senior Citizen；样例利率表中最高 Senior Citizen Rate 是 `6.80% p.a.`，对应期限为 `3 years–5 years`。

信用卡方面，他不符合文档列出的任何一张 ZX Bank 信用卡：

| 信用卡 | 年龄条件 | 67 岁是否符合 |
|---|---:|---|
| `ZX Platinum Credit Card` | 21-65 | 不符合 |
| `ZX Gold Credit Card` | 21-65 | 不符合 |
| `ZX Women Empower Credit Card` | 21-65 | 不符合，且题干为男性退休老人 |
| `ZX Student Credit Card` | 18-25 | 不符合 |
| `ZX NRI Credit Card` | 21-65 | 不符合 |

保险箱前提条件：

1. 必须是现有 `ZX Bank customer`，或先开立 `savings/current account`。
2. KYC 必须更新。
3. 需要 valid photo ID、address proof、recent passport-sized photo。

必须到分行办理的步骤：

1. 保险箱可用性可到 nearest ZX Bank branch 查询，也可直接致电分行；若选择现场查询则需要到分行。
2. 正式申请保险箱必须到分行，携带原件和复印件，填写 `Locker Facility Application Form`。
3. 提交 KYC documents、签署 `Locker Hirer Agreement` 属于分行申请流程。
4. 支付 refundable security deposit 和 annual rent 可通过 cash、cheque 或 direct bank transfer，但该步骤发生在保险箱申请流程中。
5. 获批后领取 locker keys，并由 bank officer 说明 locker location 和 operating procedure。
6. 每次操作保险箱必须在 branch working hours 到分行，携带 locker keys 和 valid ID proof，并签署 `Locker Access Register`。

FD 开立不必须到分行，因为可通过 `ZX Bank Asia app` 或 `NetBanking` 开立；只有选择 Branch 方式开 FD 时才需要到分行。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 最高 Senior Citizen FD 利率为 6.80% | 通过 | `zx-bank-fixed-deposits.md#L59-L69` |
| FD 可通过 App/NetBanking 开立，不必须到分行 | 通过 | `zx-bank-fixed-deposits.md#L40-L56` |
| Platinum、Gold、Women Empower、NRI 年龄上限均为 65 | 通过 | `zx-bank-credit-card.md#L22-L25`, `zx-bank-credit-card.md#L43-L46`, `zx-bank-credit-card.md#L64-L68`, `zx-bank-credit-card.md#L107-L110` |
| Student 年龄要求 18-25 | 通过 | `zx-bank-credit-card.md#L86-L89` |
| 67 岁不符合任何列出的信用卡年龄条件 | 通过：所有年龄范围均不覆盖 67 岁 | 同上 |
| 保险箱资格要求现有或新开 savings/current account、KYC 更新和身份证明材料 | 通过 | `open-a-locker.md#L15-L21` |
| 保险箱申请需到分行、填表、提交 KYC、签署协议 | 通过 | `open-a-locker.md#L25-L30` |
| 保险箱获批后领取钥匙和操作流程与分行相关 | 通过 | `open-a-locker.md#L42-L55` |

自检结论：FD 最高利率、信用卡资格排除、保险箱前提和必须到分行办理的步骤均有源文行号支撑；FD 与保险箱的分行必要性已区分。

## 本次单题执行更新：Q11

更新时间：2026-08-10。

问题：一位居住在不丹的印度裔 NRI 想做以下事情：(1) 汇款到印度的家人账户，(2) 申请一张 NRI 信用卡，(3) 通过 WhatsApp 使用银行的 AI 助手。请逐一说明：跨境汇款需要多长时间？NRI 信用卡的最低月海外汇款要求是多少？WhatsApp 上使用 Zia 需要什么步骤？Zia 支持哪些语言？

结论：

| 问点 | 答案 |
|---|---|
| 跨境汇款时间 | 大多数转账 processed within minutes |
| NRI 信用卡最低月海外汇款要求 | `USD $1,000` |
| WhatsApp 使用 Zia 步骤 | 保存官方 WhatsApp 号码 `+91-XXX-XXX-XXXX` → 发送 `Hello Zia` → 按提示访问银行功能 |
| Zia 支持语言 | English、Hindi、Sinhala、Bengali、Nepali |

### Step 1 Document routing

执行说明：本题继续按测试对象使用 `../../../fixtures/zx-bank-kb/.kb/manifest.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `cross-border-payments.md` | `doc_031` | 标题为 `Fast Cross-Border Payments with ZX Bank`；摘要覆盖 India、Sri Lanka、Nepal、Bhutan 跨境支付和汇款流程 | 判断不丹到印度汇款是否覆盖、处理时间和操作渠道 |
| `zx-bank-credit-card.md` | `doc_068` | 标题为 `ZX Bank Credit Card Options`；NRI card 节点覆盖 NRI 适用对象、费用和资格 | 判断 NRI 信用卡最低月海外汇款要求 |
| `ask-zia-your-24-7-banking-assistant.md` | `doc_006` | 标题为 `ASK Zia – Your 24/7 Banking Assistant`；摘要覆盖 WhatsApp 用法和语言支持 | 判断 WhatsApp 上使用 Zia 的步骤和语言 |
| `about-zx-bank-ltd.md` | `doc_001` | 标题为 `ZX Bank Ltd.`；Operating Countries 和 Remittances 节点提到 Bhutan、NRI support 和汇款国家 | 补充不丹运营、NRI support 和汇款覆盖背景 |

路由判断：未路由到普通 UPI 或分行网络文档，因为题目要求的是跨境汇款、NRI 信用卡和 WhatsApp Zia；四个命中文档已覆盖汇款、卡片资格、Zia 使用和不丹/NRI 背景。该判断属于 `kb-chat` 的 Step 1 Document routing 执行记录。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `cross-border-payments.md` | `ch_1`, `ch_2`, `ch_3`, `ch_4` | L3-L40 | 定位跨境支付国家、处理时间、汇款步骤和数字便利性 |
| `zx-bank-credit-card.md` | `ch_5_1`, `ch_5_2`, `ch_5_3` | L93-L114 | 定位 NRI 信用卡适用对象、费用和最低月海外汇款要求 |
| `ask-zia-your-24-7-banking-assistant.md` | `ch_2`, `ch_4_2` | L17-L26, L41-L47 | 定位 WhatsApp Zia 功能、语言和使用步骤 |
| `about-zx-bank-ltd.md` | `ch_1`, `ch_2_4` | L20-L27, L50-L52 | 定位 Bhutan 的 cross-border banking / NRI support 和 remittances 国家 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `cross-border-payments.md` | L3-L16 | ZX Bank 提供 India、Sri Lanka、Nepal、Bhutan 之间的跨境支付；most transfers are processed within minutes；支持 INR、LKR、NPR、BTN 等 |
| `cross-border-payments.md` | L20-L37 | 汇款可在 branch、mobile app 或 NetBanking 发起，收款方可为 India、Sri Lanka、Nepal、Bhutan 的 ZX Bank 或 partner bank accounts；App 支持 24/7 transfers 和 Zia in-app support |
| `zx-bank-credit-card.md` | L93-L110 | NRI card 面向 Non-resident Indians and NRIs in Bhutan, Nepal, Sri Lanka；minimum monthly overseas remittance 为 `$1,000` |
| `ask-zia-your-24-7-banking-assistant.md` | L17-L24 | WhatsApp Zia 可通过保存官方号码并发送 `Hello Zia` 开始；支持 English、Hindi、Sinhala、Bengali、Nepali |
| `ask-zia-your-24-7-banking-assistant.md` | L41-L44 | WhatsApp 具体步骤：保存 `+91-XXX-XXX-XXXX`，发送 `Hello Zia`，follow prompts |
| `about-zx-bank-ltd.md` | L23-L24 | Bhutan 支持 cross-border banking、digital onboarding、NRI support |
| `about-zx-bank-ltd.md` | L50-L52 | Remittances 覆盖 India、Sri Lanka、Nepal、Bhutan |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `../../../fixtures/zx-bank-kb/.kb/memory/corrections/` | 目录存在但为空 |
| `doc_031.jsonl` | 不存在 |
| `doc_068.jsonl` | 不存在 |
| `doc_006.jsonl` | 不存在 |
| `doc_001.jsonl` | 不存在 |

结论：本题无 correction 记录需要合并。

### Step 5 Generate answer

跨境汇款方面，不丹在 ZX Bank 跨境支付/汇款覆盖范围内，且可向印度家人账户汇款。大多数转账通过 advanced payment rails 和 SWIFT capabilities 在 `within minutes` 内处理。

NRI 信用卡方面，`ZX NRI Credit Card` 适用于 Non-resident Indians and NRIs in Bhutan, Nepal, Sri Lanka；最低月海外汇款要求是 `USD $1,000`。

WhatsApp 上使用 Zia 的步骤：

1. 保存官方 WhatsApp 号码：`+91-XXX-XXX-XXXX`。
2. 发送消息：`Hello Zia`。
3. 按提示访问银行功能。

Zia 支持语言包括：`English`、`Hindi`、`Sinhala`、`Bengali`、`Nepali`。

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| Bhutan 在跨境支付/汇款覆盖范围内 | 通过 | `cross-border-payments.md#L3-L5`, `about-zx-bank-ltd.md#L23-L24`, `about-zx-bank-ltd.md#L50-L52` |
| 大多数跨境转账 within minutes | 通过 | `cross-border-payments.md#L9-L16` |
| 跨境汇款可发往 India 家人账户 | 通过：收款国家列表含 India，场景为 family support | `cross-border-payments.md#L3-L5`, `cross-border-payments.md#L22-L25` |
| NRI 信用卡适用于 Bhutan 的 NRI | 通过 | `zx-bank-credit-card.md#L93-L100` |
| NRI 信用卡最低月海外汇款为 USD $1,000 | 通过 | `zx-bank-credit-card.md#L107-L110` |
| WhatsApp 使用步骤为保存号码、发送 Hello Zia、按提示操作 | 通过 | `ask-zia-your-24-7-banking-assistant.md#L41-L44` |
| Zia 支持 English、Hindi、Sinhala、Bengali、Nepali | 通过 | `ask-zia-your-24-7-banking-assistant.md#L17-L24` |

自检结论：汇款时间、NRI 卡汇款要求、WhatsApp 使用步骤和语言支持均有直接源文行号支撑。
