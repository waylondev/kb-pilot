# KB-Pilot 硬核 RAG 测试题集

> 基于 `../../../fixtures/zx-bank-kb/` 目录下的文档设计，专门针对传统 RAG 系统的薄弱环节：多跳推理、跨文档关联、上下文割裂、条件推理、否定推理。
> 每道题包含：问题、RAG 难度分析、标准答案、原文引用（文件名 + 行号）。

---

## Q1: 多跳条件推理 — 跨三文档的资格判断

**问题：** 一位在德里工作的女性上班族，月收入 ₹30,000，年龄 28 岁，CIBIL 720。她想同时申请一张 ZX Bank 信用卡和一笔摩托车贷款。她有资格申请哪些信用卡？摩托车贷款的利率是多少？两张卡的加入费合计多少？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 多跳推理 | 需要逐一比对 5 种信用卡的资格条件 × 个人条件，再跳到摩托车贷款文档查利率 |
| 跨文档关联 | 信用卡和摩托车贷款是两个完全独立的文档，问题把它们绑定在同一个人物场景中 |
| 上下文割裂 | "月收入 ₹30,000" 这个条件需要分别与 5 张卡的收入门槛比较，RAG 很难一次性提取所有门槛 |
| 条件推理 | 需要同时满足年龄、收入、CIBIL 三个维度才能判断资格 |

### 标准答案

**有资格的信用卡：**

1. **ZX Gold Credit Card** — 月收入要求 ₹25,000（✅ ₹30,000 满足），年龄 21-65（✅ 28 满足），CIBIL 700+（✅ 720 满足）
2. **ZX Women Empower Credit Card** — 申请人需自我认同为女性（✅），月收入要求 ₹15,000（✅），年龄 21-65（✅），CIBIL 650+（✅）

**不符合的信用卡：**
- ZX Platinum：月收入要求 ₹80,000（❌ 不满足）
- ZX Student：年龄限制 18-25（❌ 28 岁超出），且需学生身份证明
- ZX NRI：需 NRI 身份（❌ 在德里工作，非 NRI）

**摩托车贷款利率：** 起始 9.49% p.a.。她符合条件（年龄 21-60 ✅，月收入 ≥₹8,000 ✅，CIBIL >650 ✅）

**加入费合计：** Gold ₹499 + Women Empower ₹299 = **₹798 + GST**

### 原文引用

**信用卡资格条件** — `../../../fixtures/zx-bank-kb/zx-bank-credit-card.md`:
- L23: `- Minimum monthly income: ₹80,000`（Platinum）
- L25: `- Good credit history (CIBIL 750+)`
- L43-44: `- Minimum monthly income: ₹25,000` / `- CIBIL 700+`（Gold）
- L64-66: `- Applicant must self-identify as female` / `- Minimum monthly income: ₹15,000` / `- CIBIL 650+`（Women Empower）
- L86: `- Age: 18 to 25 years`（Student）
- L108: `- Valid NRI status (passport copy and visa/residence permit)`（NRI）

**摩托车贷款** — `../../../fixtures/zx-bank-kb/zx-bank-bike-loan.md`:
- L9: `- **Attractive Interest Rates** – Starting from *9.49% p.a.*`
- L43-46: `- **Age:** 21–60 years` / `- **Minimum Income:** ₹8,000/month` / `- **CIBIL Score:** Above 650 preferred`

---

## Q2: 上下文割裂 — 账户类型转换的连锁影响

**问题：** 一位客户的工资账户已经连续 4 个月没有收到工资入账。他的账户会发生什么变化？转换后他需要维持多少最低余额才能避免罚款？如果他想改用数字银行方式发起转换请求，具体操作步骤是什么？转换后他的银行卡和支票簿会更换吗？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 上下文割裂 | "4 个月没收到工资" → 需要跳到 `salary-account-to-a-savings-account.md` 查自动转换规则 → 再跳到 `savings-account-overview.md` 查最低余额 → 再回到转换文档查数字渠道操作步骤 |
| 隐式关联 | 问题没有提到任何文档名，"工资账户"和"储蓄账户最低余额"之间的关联是隐式的 |
| 多层推理 | 自动转换规则 → 最低余额变化 → 数字渠道操作 → 卡/支票簿是否保留，四层连锁 |

### 标准答案

1. **账户变化：** 工资账户 3 个月以上未收到工资入账，银行可能自动将其转为储蓄账户。客户也可以主动发起转换以避免服务中断。
2. **最低余额：** 转为 regular Savings Account 后，若客户在印度，需按 Regular Savings 要求维持 **₹5,000**；若在斯里兰卡则为 LKR 3,000。不维持最低余额可能产生罚款。Digital Zero Balance、Senior Citizens/Students 是其他储蓄账户类型，不能直接当作该工资账户转换后的默认结果。
3. **数字渠道转换步骤：**
   - 打开 ZX Bank Asia 手机 App 或登录 NetBanking
   - 进入 "Service Requests" > "Convert Salary Account to Savings Account"
   - 填写详情并上传必要的 KYC 文件（如有要求）
   - 处理完成后收到确认
4. **卡和支票簿：** 现有借记卡、支票簿和账号通常**保持不变**。

### 原文引用

**自动转换规则** — `../../../fixtures/zx-bank-kb/salary-account-to-a-savings-account.md`:
- L10: `- If salary credits stop (for 3+ months), your account may be automatically converted to a Savings Account by the bank, but manual conversion avoids service interruptions.`

**最低余额** — `../../../fixtures/zx-bank-kb/savings-account-overview.md`:
- L42-46: `| Regular Savings       | ₹5,000 (India) / LKR 3,000 (Sri Lanka) |` / `| Digital Zero Balance  | Nil (No minimum balance)  |` / `| Senior Citizens/Students | ₹1,000 (India)         |`

**数字渠道转换** — `../../../fixtures/zx-bank-kb/salary-account-to-a-savings-account.md`:
- L46-51: `1. **Open the ZX Bank Asia Mobile App** or log into NetBanking.` / `2. Go to "Service Requests" > "Convert Salary Account to Savings Account."` / `3. Fill in details and upload necessary KYC docs, if asked.` / `4. Receive confirmation after processing.`

**卡/支票簿保留** — `../../../fixtures/zx-bank-kb/salary-account-to-a-savings-account.md`:
- L40: `- Existing debit card, chequebook, and account number typically remain unchanged.`

---

## Q3: 跨国条件推理 — 不同国家的产品可用性矩阵

**问题：** 一位居住在孟加拉国的客户想申请个人贷款，最高能借多少？利率范围是多少？与印度受薪人士相比是高还是低？他还想用 UPI 来偿还贷款，这可行吗？如果不可行，他可以通过什么渠道进行还款？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 跨文档否定推理 | 需要 `personal-loan.md` 查孟加拉国贷款条件，再跳到 `upi-zx-bank-asia.md` 查 UPI 可用国家，发现 UPI 仅限印度 → 否定推理 |
| 隐式比较 | "与印度相比" 需要从同一文档的不同行提取两个国家的数据并比较 |
| 来源边界判断 | UPI 不可用后，需要区分“源文明确说明的替代跨境汇款方式”和“源文没有直接列明的个人贷款还款渠道” |

### 标准答案

1. **最高贷款额：** 孟加拉国 — 最高 **BDT 35,00,000**
2. **利率范围：** 孟加拉国 — **13.50% – 21.00% p.a.**
3. **与印度比较：** 印度受薪人士利率为 11.75% – 17.99%，孟加拉国利率**更高**（下限高 1.75 个百分点，上限高 3.01 个百分点）
4. **UPI 不可行：** UPI 服务目前仅限印度用户。孟加拉国客户无法使用 UPI。
5. **替代渠道：** 源文没有明确列出孟加拉国个人贷款的还款渠道。可以确定的是：UPI 不可用；UPI 文档提示跨境付款/汇款应使用 App 内 dedicated remittance options。`personal-loan.md` 中的分行、App/NetBanking、Customer Care/Zia 是个人贷款申请/服务渠道，不能直接写成已明示的还款渠道。

### 原文引用

**个人贷款条件** — `../../../fixtures/zx-bank-kb/personal-loan.md`:
- L22: `| Bangladesh, Bhutan, Nepal        | 13.50% – 21.00%*                         |`
- L20: `| Salaried (India, Sri Lanka)      | 11.75% – 17.99%                          |`
- L56: `- **Bangladesh:** Up to BDT 35,00,000`

**UPI 可用性** — `../../../fixtures/zx-bank-kb/upi-zx-bank-asia.md`:
- L66: `- UPI services currently available in India for ZX Bank account holders`

**UPI 限制与替代提示** — `../../../fixtures/zx-bank-kb/upi-zx-bank-asia.md`:
- L66-67: `- UPI services currently available in India for ZX Bank account holders` / `- For cross-border payments/remittances, use the dedicated remittance options in the app.`

**个人贷款申请/服务渠道（不是还款渠道的直接证据）** — `../../../fixtures/zx-bank-kb/personal-loan.md`:
- L65-68: `1. **Visit:** Any ZX Bank branch in your country` / `2. **Online:** Through [ZX Bank Asia Mobile App] or [NetBanking]` / `3. **Call:** 24x7 Customer Care or use AI Assistant "Zia" on the app`

---

## Q4: 三跳链式推理 — 抵押品 → 存款 → 再贷款

**问题：** 一位尼泊尔客户想用黄金饰品做抵押获得贷款，然后用贷款所得在尼泊尔开立定期存款，再用该定期存款做抵押获取另一笔贷款。请计算：黄金贷款的最高 LTV 是多少？尼泊尔定期存款的最低起存金额是多少？定期存款可抵押贷款的比例是多少？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 三跳链式推理 | 黄金贷款(LTV) → 定期存款(最低金额) → FD 抵押贷款(比例)，三个文档形成一条链 |
| 隐式场景构建 | 问题构造了一个现实中罕见但逻辑自洽的场景，RAG 需要理解"贷款所得 → 开FD → FD再抵押"的因果链 |
| 跨文档数值提取 | 三个数值分散在三个不同文档中，且没有关键词重叠 |

### 标准答案

1. **黄金贷款最高 LTV：** 源文给出的黄金贷款 LTV 为最高 **75%**（按黄金市场价值计算）。需要注意：该行写有 `as per RBI regulations`，源文没有为尼泊尔单独列出不同 LTV，因此这里按产品文档的统一 LTV 回答，不额外推断尼泊尔监管细则。
2. **尼泊尔定期存款最低起存额：** **NPR 1,500**
3. **定期存款可抵押贷款比例：** 最高 **90%**（可获得的透支或贷款占 FD 价值的比例）

### 原文引用

**黄金贷款 LTV** — `../../../fixtures/zx-bank-kb/zx-bank-gold-loan.md`:
- L28: `- **Loan-to-Value (LTV):** Up to 75% of the gold's market value, as per RBI regulations`

**尼泊尔 FD 最低起存** — `../../../fixtures/zx-bank-kb/zx-bank-fixed-deposits.md`:
- L20: `- Minimum Deposit: ₹5,000 (India), LKR 10,000 (Sri Lanka), BDT 10,000 (Bangladesh), BTN 1,000 (Bhutan), NPR 1,500 (Nepal)`

**FD 抵押贷款比例** — `../../../fixtures/zx-bank-kb/zx-bank-fixed-deposits.md`:
- L12: `- **Loan Against FD:** Avail instant overdraft or loans up to 90% of your FD value.`

---

## Q5: 跨文档综合 — ESG/绿色金融全景图

**问题：** ZX Bank 获得过绿色金融方面的奖项。请找出银行中至少 4 个与 ESG/绿色金融直接相关的产品或服务，并说明客户的存款如何参与绿色金融项目。哪些国家的项目被特别提及？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 跨文档综合 | 答案分散在至少 5 个文档中：`awards-and-recognitions.md`、`about-zx-bank-ltd.md`、`zx-bank-fixed-deposits.md`、`zx-bank-house-loan.md`、`zx-bank-business-loans.md` |
| 隐式语义关联 | "ESG/绿色金融" 这个概念在不同文档中有不同表述："Green Finance"、"Green Homes"、"Green & Sustainability Loans"、"ESG & CSR" — 关键词不完全匹配 |
| 归纳推理 | 需要从多个文档中归纳出银行整体的 ESG 战略，而非单一事实查询 |

### 标准答案

**与 ESG/绿色金融直接相关的产品/服务：**

1. **绿色金融项目（企业级）：** 与不丹水电和尼泊尔太阳能项目合作
2. **绿色家园贷款优惠：** 对环保/节能住宅提供更低利率
3. **绿色与可持续商业贷款：** 为可再生能源、环保基础设施和气候智慧型商业项目提供融资
4. **定期存款 ESG 贡献：** 客户的部分存款用于资助不丹水电和尼泊尔太阳能项目
5. **妇女赋权贷款：** 面向南亚女性主导企业的微型贷款（社会层面 ESG）

**特别提及的国家：** **不丹**（水电项目）和 **尼泊尔**（太阳能项目）

**客户存款参与方式：** 定期存款的一部分用于资助绿色金融项目，确保客户储蓄为可持续未来做出贡献。

### 原文引用

**绿色金融奖项** — `../../../fixtures/zx-bank-kb/awards-and-recognitions.md`:
- L9-11: `## 2. Excellence in Green Finance Award (2022)` / `*Highlight:* Honored for innovative green financing projects supporting Bhutan's hydropower and Nepal's solar ventures, advancing ESG goals in banking.`

**绿色金融项目** — `../../../fixtures/zx-bank-kb/about-zx-bank-ltd.md`:
- L93-94: `- **Green Finance Projects**` / `  - Partnering with Bhutan hydropower & Nepal solar ventures`

**绿色家园贷款** — `../../../fixtures/zx-bank-kb/zx-bank-house-loan.md`:
- L58: `- **Green Homes:** Lower rates for eco-friendly/energy-efficient homes`

**绿色商业贷款** — `../../../fixtures/zx-bank-kb/zx-bank-business-loans.md`:
- L34-35: `### 6. **Green & Sustainability Loans**` / `> Financing for renewable energy, eco-friendly infrastructure, and climate-smart business initiatives.`

**存款参与 ESG** — `../../../fixtures/zx-bank-kb/zx-bank-fixed-deposits.md`:
- L74-75: `Part of your deposits fuel green finance projects such as Bhutanese hydropower and Nepalese solar ventures, ensuring your savings contribute to a sustainable future.`

---

## Q6: 逆向推理 + 多渠道枚举 — 欺诈处理的完整路径

**问题：** 如果你的 ZX Bank 借记卡被盗并产生了欺诈交易，你可以通过哪些渠道立即冻结/挂失卡片？银行处理欺诈投诉的目标解决时间是多少天？在问题解决后，如果你想申请新的支票簿，可以通过哪几种方式申请？请列出所有渠道。

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 多文档渠道枚举 | 冻结卡片渠道在 `fraud-transaction.md` 和 `zx-bank-asia-mobile-app-guide.md` 中；支票簿申请渠道在 `apply-for-a-cheque-book.md` 中 |
| 逆向推理 | 问题不是"如何报告欺诈"，而是"冻结卡片的所有渠道" — 需要逆向思考，从多个文档中提取所有可能的冻结途径 |
| 完整性要求 | "所有渠道" 要求不遗漏，RAG 通常只返回最相关的片段而非穷举 |

### 标准答案

**明确可用于冻结/挂失卡片的渠道：**

1. **手机 App：** ZX Bank Asia App → Card Management → "Block/Card Hotlisting" → 确认操作
   - 或 App → 选择卡片 → More options → Block（立即生效）
   - 或 App 内使用 "Block Instantly" 进行紧急冻结
2. **NetBanking：** 登录 → Account Services → "Freeze Account" 或 Card Management → Block

**欺诈报告/联系银行渠道（源文未明确说这些渠道都能立即冻结卡片）：**

1. **欺诈热线电话（24x7）：**
   - 印度：1800 123 9876
   - 斯里兰卡：+94 11 2345678
   - 孟加拉国：+880 9612 345678
   - 不丹：+975 2 345678
   - 尼泊尔：+977 1 2345678
2. **邮件：** fraudreport@zxbank.asia
3. **App 内举报：** ZX Bank Asia App → Support → Report Fraud

**欺诈处理目标解决时间：** **10 个工作日**内

**申请新支票簿的所有渠道（5种）：**

1. **手机 App：** ZX Bank Asia → Services → Cheque Book Request → 选择账户 → 确认
2. **NetBanking：** 登录 → Services > Cheque Book Request → 选择账户和页数 → 提交
3. **分行：** 到访最近的 ZX Bank 分行 → 填写 Cheque Book Request Form → 提交
4. **ATM：** 插入借记卡并输入 PIN → Services > Cheque Book Request → 选择账户和页数 → 确认
5. **客户服务热线：** 拨打 24x7 热线 → 验证身份 → 提出申请 → 记录参考编号

### 原文引用

**欺诈冻结渠道** — `../../../fixtures/zx-bank-kb/fraud-transaction.md`:
- L22-24: `- Go to "Card Management" or "Account Services"` / `- Select "Block/Card Hotlisting" or "Freeze Account"`
- L63: `For urgent blocking, use the “Block Instantly” option in the app.`

**欺诈报告/联系银行渠道** — `../../../fixtures/zx-bank-kb/fraud-transaction.md`:
- L9-14: 热线电话（印度/斯里兰卡/孟加拉国/不丹/尼泊尔）
- L16: `- **Email:** fraudreport@zxbank.asia`
- L17: `- **Mobile App:** Go to **ZX Bank Asia** app → Support → Report Fraud`

**App 内冻结卡片** — `../../../fixtures/zx-bank-kb/zx-bank-asia-mobile-app-guide.md`:
- L75: `- **Block Card**: Select card → More options → Block (immediate effect).`

**解决时间** — `../../../fixtures/zx-bank-kb/fraud-transaction.md`:
- L54: `- ZX Bank targets resolution within 10 working days.`

**支票簿申请渠道** — `../../../fixtures/zx-bank-kb/apply-for-a-cheque-book.md`:
- L1-15: Via ZX Bank Mobile App（渠道1）
- L19-26: Through NetBanking（渠道2）
- L29-34: At Branch（渠道3）
- L38-43: Via ZX Bank ATM（渠道4）
- L47-51: ZX Bank Customer Care（渠道5）

---

## Q7: 隐式否定推理 — 哪些服务在哪些国家不可用

**问题：** ZX Bank 在 5 个国家运营。请列出以下每项服务在哪些国家可用、在哪些国家不可用：(1) UPI 支付，(2) e-KYC 数字身份验证，(3) 学生信用卡，(4) 跨境汇款。如果一位在孟加拉国的学生想申请信用卡，他有什么选择？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 否定推理 | 需要 RAG 不仅找出"在哪里可用"，还要推断"在哪里不可用" — 传统 RAG 极不擅长否定推理 |
| 多文档交叉 | 4 项服务的可用性分散在 4 个不同文档中，且有些文档只正面提及可用国家，不提及不可用国家 |
| 隐式推断 | "孟加拉国学生" 需要交叉比对：学生卡仅限印度/斯里兰卡/尼泊尔 → 孟加拉国不可用 → 该学生只能选其他卡 |

### 标准答案

| 服务 | 可用国家 | 不可用国家 |
|------|---------|-----------|
| UPI 支付 | 仅印度 | 斯里兰卡、孟加拉国、不丹、尼泊尔 |
| e-KYC（信用卡申请） | 印度、斯里兰卡、尼泊尔 | 孟加拉国、不丹 |
| 学生信用卡 | 印度、斯里兰卡、尼泊尔 | 孟加拉国、不丹 |
| 跨境汇款 | 印度、斯里兰卡、尼泊尔、不丹 | 孟加拉国（汇款走廊不包含孟加拉国） |

**孟加拉国学生的信用卡选择：** 学生信用卡仅在印度、斯里兰卡、尼泊尔提供，孟加拉国学生**无法申请学生信用卡**。他可以考虑其他信用卡（如 Gold Card，需月收入 ₹25,000 且 CIBIL 700+），但需满足相应的收入和信用要求。就信用卡申请文档而言，e-KYC 不覆盖孟加拉国；是否存在其他产品线的数字开户能力，需要另看对应文档，不能由本题直接推断。

### 原文引用

**UPI 可用性** — `../../../fixtures/zx-bank-kb/upi-zx-bank-asia.md`:
- L66: `- UPI services currently available in India for ZX Bank account holders`

**信用卡申请 e-KYC 可用性** — `../../../fixtures/zx-bank-kb/zx-bank-credit-card.md`:
- L119: `- e-KYC available for India, Sri Lanka, and Nepal residents`

**学生信用卡可用性** — `../../../fixtures/zx-bank-kb/zx-bank-credit-card.md`:
- L74: `**Best For:** College & university students (India, Sri Lanka, Nepal only)`

**跨境汇款走廊** — `../../../fixtures/zx-bank-kb/cross-border-payments.md`:
- L5: `ZX Bank provides **fast, secure cross-border payment services** between **India, Sri Lanka, Nepal, and Bhutan**.`

---

## Q8: 跨文档比较 + 集合运算 — 贷款文件差异分析

**问题：** 比较 ZX Bank 房屋贷款和汽车贷款所需的文件。哪些文件是两者都需要的？哪些是房屋贷款独有的？哪些是汽车贷款独有的？两种贷款是否都支持完全在线申请？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 集合运算 | 需要从两个文档分别提取文件清单，然后做交集和差集 — RAG 无法做集合运算 |
| 跨文档比较 | 两种贷款在不同文档中，文档结构和表述方式不同（一个用列表，一个用分类标题） |
| 语义匹配 | "Income Proof" 在两个文档中表述不同：房屋贷款写 "Salary slips, ITR, Bank statement, Form 16"，汽车贷款写 "Salary slips/ITR/Bank statements" — 需要语义等价判断 |

### 标准答案

**共同需要的文件（交集）：**
- 身份/KYC 类文件：房屋贷款列 ID Proof；汽车贷款列 KYC Documents
- 收入证明（工资单/ITR/银行流水）

**房屋贷款独有：**
- 地址证明：Utility Bill、Passport、Aadhaar（房屋贷款单独列为 Address Proof）
- 物业文件：销售协议、地契、批准平面图
- Form 16（作为收入证明的一部分）

**汽车贷款独有：**
- 雇佣/商业证明：录用通知书或商业注册证
- 车辆报价单/发票
- photograph（汽车贷款 KYC 中明确列出，房屋贷款文件清单未列照片）

**在线申请：** 两种贷款都支持在线/移动端发起申请。
- 房屋贷款：通过 ZX Bank Home Loan Portal 或 ZX Bank Asia App 发起申请；源文没有说明所有文件都能数字上传，因此不能直接确认“完全在线”。
- 汽车贷款：通过 ZX Bank Asia App 或 NetBanking；源文明确说明所有文件可通过 App/NetBanking 数字上传，因此可以确认完整线上申请与文件上传流程。

### 原文引用

**房屋贷款文件** — `../../../fixtures/zx-bank-kb/zx-bank-house-loan.md`:
- L34-37: `- **ID Proof:** Aadhaar, PAN, Passport, Voter ID` / `- **Address Proof:** Utility Bill, Passport, Aadhaar` / `- **Income Proof:** Salary slips, ITR, Bank statement, Form 16` / `- **Property Documents:** Sale agreement, title deed, approved plan`
- L43-47: `1. **Online:**` / `Visit [ZX Bank Home Loan Portal]` / `2. **Mobile App:**`

**汽车贷款文件** — `../../../fixtures/zx-bank-kb/zx-bank-car-loan.md`:
- L31-34: `- **KYC Documents:** Aadhaar/Passport/Driving License, PAN, photograph` / `- **Income Proof:** Salary slips/ITR/Bank statements (Past 6 months)` / `- **Employment/Business Proof:** Offer letter/Business registration` / `- **Vehicle Quotation/Invoice**`
- L35: `_All documents can be uploaded digitally via the ZX Bank Asia app/NetBanking_`
- L41-47: `1. **Download** the [ZX Bank Asia App] or log in to [ZX NetBanking]` / `4. **Upload documents** using e-KYC ...` / `6. **Submit application**`

---

## Q9: 时空交叉推理 — 城市级 ATM + 分行网络

**问题：** 一位客户在海得拉巴的 HITEC City 科技园区工作。最近的 ZX Bank 分行在哪里（给出 IFSC 和联系电话）？如果他要前往孟买出差，孟买有哪些科技园区设有 ZX Bank ATM？他可以通过什么方式找到这些 ATM 的具体位置？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 跨文档地理推理 | 海得拉巴分行在 `hyderabad-branch-network.md`，科技园区 ATM 在 `atm-locations-at-tech-parks-in-major-indian-cities.md` — 两个文档无直接关联 |
| 近邻推理 | "HITEC City 最近的分行" 需要理解 HITEC City 在 Madhapur 地区，然后从分行列表中找最近的 — 需要 LLM 的地理理解能力，RAG 的关键词匹配无法做到 |
| 多层问题 | 分行查找 → ATM 查找 → 查找方式，三层独立查询 |

### 标准答案

**海得拉巴 HITEC City 最近的分行：**

HITEC City 位于 Madhapur 地区。从源文中的地区和邮编可推断，最匹配、可视为最近的 ZX Bank 分行是：

| 分行地址 | IFSC | 联系电话 |
|---------|------|---------|
| Madhapur Kavuri Hills, 500081 | ZXIN0001232 | 040-45671232 |

（注：HITEC City 地址为 Madhapur, Hyderabad, Telangana 500081，与 Madhapur Kavuri Hills 分行在同一区域 500081）

**孟买科技园区 ATM（3 个）：**

1. **Mindspace Airoli IT Park** — Building 2, Mindspace, Thane-Belapur Road, Airoli, Navi Mumbai, Maharashtra 400708
2. **Nesco IT Park** — Gate 3, Western Express Highway, Goregaon (East), Mumbai, Maharashtra 400063
3. **Infinity IT Park** — New Link Road, Malad (West), Mumbai, Maharashtra 400064

**查找 ATM 位置的方式：**
- 使用 ZX Bank Asia 手机 App 中的 "Locate Branch/ATM" 功能
- 使用官网的 ZX Bank ATM Locator（www.zxbank.asia/atm-locator）
- 询问 AI 助手 "Zia"

### 原文引用

**海得拉巴西区分行** — `../../../fixtures/zx-bank-kb/hyderabad-branch-network.md`:
- L49-50: `| Madhapur Kavuri Hills, 500081                   | ZXIN0001232   | 040-45671232    |`

**HITEC City 位置** — `../../../fixtures/zx-bank-kb/atm-locations-at-tech-parks-in-major-indian-cities.md`:
- L48-49: `1. **HITEC City**` / `   Madhapur, Hyderabad, Telangana 500081`

**孟买科技园区 ATM** — `../../../fixtures/zx-bank-kb/atm-locations-at-tech-parks-in-major-indian-cities.md`:
- L9-16: Mindspace Airoli IT Park / Nesco IT Park / Infinity IT Park

**ATM 定位方式** — `../../../fixtures/zx-bank-kb/zx-bank-asia-mobile-app-guide.md`:
- L117: `- **Locate Branch/ATM**: Find ZX Bank locations in all supported countries`

**ATM 定位方式** — `../../../fixtures/zx-bank-kb/atms-at-railway-stations-and-airports.md`:
- L180: `Find the nearest ZX Bank ATM using the [ZX Bank Asia Mobile App] or [ZX Bank ATM Locator].`

**Zia 定位分行/ATM** — `../../../fixtures/zx-bank-kb/ask-zia-your-24-7-banking-assistant.md`:
- L9-10: `From locating branches and ATMs to product information`

---

## Q10: 复合条件 + 跨产品推理 — 老年客户的综合银行方案

**问题：** 一位 67 岁的印度退休老人想做以下三件事：(1) 开立定期存款获取最高利率，(2) 申请一张信用卡用于日常消费，(3) 租用一个银行保险箱存放遗产文件。请逐一分析：他能获得的最高 FD 利率是多少？他有资格申请哪些信用卡？他开立保险箱需要满足什么前提条件？整个流程中哪些步骤必须到分行办理？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 复合条件推理 | 单一问题包含 3 个子任务，每个子任务需要不同文档，且条件互相影响（年龄 67 影响 FD 利率和信用卡资格） |
| 跨产品关联 | FD、信用卡、保险箱是三个完全独立的产品文档，RAG 很难一次性检索全部 |
| 流程推理 | "哪些步骤必须到分行" 需要从三个产品的流程中提取"必须到分行"的步骤并汇总 |
| 边界条件 | 67 岁是否超过信用卡年龄上限（65 岁）？这是一个关键的边界判断 |

### 标准答案

**(1) 最高 FD 利率：**

作为老年人，他可获得的最高利率为 **6.80% p.a.**（3-5 年期老年人优惠利率）。相比常规利率 6.30%，享受额外 0.5% 的老年人优惠。

**(2) 信用卡资格：**

**他不符合任何 ZX Bank 信用卡的资格条件。** 所有信用卡的年龄上限均为 65 岁，而他 67 岁，超出了年龄限制：
- Platinum：21-65 岁 ❌
- Gold：21-65 岁 ❌
- Women Empower：21-65 岁 ❌（且需女性身份）
- Student：18-25 岁 ❌
- NRI：21-65 岁 ❌（且需 NRI 身份）

**(3) 保险箱前提条件：**

- 必须是现有的 ZX Bank 客户：需持有（或开立）储蓄账户或往来账户
- KYC 合规：确保 KYC 详情已更新（有效带照片身份证、地址证明、近期护照照片）
- 签署保险箱租赁协议
- 支付可退还保证金和年租金

**(4) 必须到分行办理的步骤：**

- **FD 开立：** 可完全在线（App/NetBanking），无需到分行
- **信用卡：** 不适用（不符合资格）
- **保险箱：** 以下步骤**必须到分行**：
  - 正式申请保险箱并携带原件和复印件
  - 填写申请表并提交 KYC 文件原件
  - 签署保险箱租赁协议
  - 领取保险箱钥匙
  - 每次操作保险箱（在分行营业时间到访，携带钥匙和身份证，签署访问登记簿）

查询保险箱可用性可到分行或电话完成，不应写成必须到分行；支付保证金和租金属于申请流程的一部分，但源文允许 cash、cheque 或 direct bank transfer，因此不能把“支付”本身写成必须到分行。

### 原文引用

**FD 老年人利率** — `../../../fixtures/zx-bank-kb/zx-bank-fixed-deposits.md`:
- L67: `| 3 years–5 years  | 6.30%        | 6.80%               |`
- L22: `- Special Schemes: Senior citizen extra interest, tax-saver FDs, recurring deposit variants`

**信用卡年龄限制** — `../../../fixtures/zx-bank-kb/zx-bank-credit-card.md`:
- L24: `- Age: 21 to 65 years`（Platinum）
- L45: `- Age: 21 to 65 years`（Gold）
- L67: `- Age: 21 to 65 years`（Women Empower）
- L87: `- Age: 18 to 25 years`（Student）
- L110: `- Age: 21 to 65 years`（NRI）

**保险箱前提条件** — `../../../fixtures/zx-bank-kb/open-a-locker.md`:
- L17-18: `- **Existing ZX Bank customer:** You must have (or open) a savings or current account.` / `- **KYC Compliance:** Ensure your KYC (Know Your Customer) details are updated.`
- L9-10: `Visit your nearest branch or call the branch directly to check locker availability.`
- L27-30: `1. **Visit the Branch:** Bring original documents and photocopies.` / `2. **Fill Application Form:**` / `3. **Submit KYC Documents:**` / `4. **Locker Agreement:** Read and sign the Locker Hirer Agreement`
- L35-38: `- Pay the **refundable security deposit**` / `- Locker rent is typically paid **annually**.` / `Payment can be made via cash, cheque, or direct bank transfer.`
- L44: `- Upon approval, a locker number will be allotted.`
- L45: `- Receive the **locker keys**`

**保险箱操作** — `../../../fixtures/zx-bank-kb/open-a-locker.md`:
- L51-54: `- Locker can be operated **during branch working hours**.` / `- Visit the branch with your locker keys and valid ID proof.` / `- Sign the **Locker Access Register** each time you access the locker.`

**FD 在线开立** — `../../../fixtures/zx-bank-kb/zx-bank-fixed-deposits.md`:
- L14: `- **Digital Opening:** Open, renew, or close FDs instantly through ZX Bank Asia mobile app or NetBanking.`
- L42-47: Via Mobile App 步骤（完全在线）

---

## Q11: 隐式推理 — NRI 跨国银行完整旅程

**问题：** 一位居住在不丹的印度裔 NRI 想做以下事情：(1) 汇款到印度的家人账户，(2) 申请一张 NRI 信用卡，(3) 通过 WhatsApp 使用银行的 AI 助手。请逐一说明：跨境汇款需要多长时间？NRI 信用卡的最低月海外汇款要求是多少？WhatsApp 上使用 Zia 需要什么步骤？Zia 支持哪些语言？

### RAG 难度分析

| 难度维度 | 说明 |
|---------|------|
| 多文档 NRI 场景 | 汇款在 `cross-border-payments.md`，NRI 信用卡在 `zx-bank-credit-card.md`，Zia 在 `ask-zia-your-24-7-banking-assistant.md` — 三个文档无关键词重叠 |
| 隐式关联 | "NRI 在不丹" 需要从不丹运营信息（`about-zx-bank-ltd.md`）+ NRI 信用卡资格 + 跨境汇款走廊三个维度交叉验证 |
| 细节提取 | "最低月海外汇款"、"WhatsApp 步骤"、"支持语言" 都是细节信息，分散在不同文档的不同位置 |

### 标准答案

**(1) 跨境汇款时间：** 大多数转账在**几分钟内**完成处理。不丹在 ZX Bank 的跨境汇款走廊范围内（印度、斯里兰卡、尼泊尔、不丹）。

**(2) NRI 信用卡最低月海外汇款要求：** 每月最低 **$1,000**。加入费为 USD $30，年费为 USD $25（年消费超过 USD $5,000 可免年费）。

**(3) WhatsApp 使用 Zia 的步骤：**
1. 保存 ZX Bank 官方 WhatsApp 号码：+91-XXX-XXX-XXXX
2. 发送消息："Hello Zia"
3. 按照提示操作即可访问银行功能

**(4) Zia 支持的语言：** 英语、印地语、僧伽罗语、孟加拉语、尼泊尔语

### 原文引用

**跨境汇款时间** — `../../../fixtures/zx-bank-kb/cross-border-payments.md`:
- L11: `- **Instant Transfers:** Most transfers are processed within minutes using ZX Bank's advanced payment rails and SWIFT capabilities.`
- L5: `ZX Bank provides **fast, secure cross-border payment services** between **India, Sri Lanka, Nepal, and Bhutan**.`

**NRI 信用卡条件** — `../../../fixtures/zx-bank-kb/zx-bank-credit-card.md`:
- L95: `**Best For:** Non-resident Indians and NRIs in Bhutan, Nepal, Sri Lanka`
- L104-105: `- Joining Fee: USD $30 (or equivalent)` / `- Annual Fee: USD $25 (waived on spends above USD $5,000)`
- L109: `- Minimum monthly overseas remittance: $1,000`

**WhatsApp Zia** — `../../../fixtures/zx-bank-kb/ask-zia-your-24-7-banking-assistant.md`:
- L19: `- **Easy Onboarding**: Start a chat by saving our official number and saying "Hello Zia!"`
- L24: `- **Language Support**: Interact in English, Hindi, Sinhala, Bengali, and Nepali.`
- L42-44: `1. Save our official WhatsApp number: **+91-XXX-XXX-XXXX**` / `2. Send a message: \`Hello Zia\`` / `3. Follow prompts to access banking features.`

**不丹运营** — `../../../fixtures/zx-bank-kb/about-zx-bank-ltd.md`:
- L23-24: `- **Bhutan**` / `  - Cross-border banking, digital onboarding, and NRI support.`

---

## 使用说明

### 测试方法

1. 使用 kb-chat SKILL 逐一输入上述问题
2. 对比 kb-pilot 的回答与标准答案
3. 检查引用的文件名和行号是否准确
4. 评估维度：
   - **事实准确性**：数值、条件、资格判断是否正确
   - **完整性**：是否遗漏了跨文档的关键信息
   - **引用精度**：原文引用是否可追溯到正确文件和行号
   - **推理质量**：多跳推理的逻辑链是否完整

### 难度分级

| 等级 | 题号 | 特征 |
|------|------|------|
| 极难 | Q1, Q5, Q10 | 3+ 文档交叉，复合条件，需集合运算或边界判断 |
| 困难 | Q4, Q6, Q7, Q11 | 2-3 文档关联，隐式推理或否定推理 |
| 中等偏难 | Q2, Q3, Q8, Q9 | 2 文档关联，条件链或跨文档比较 |
