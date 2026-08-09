# ZX Bank 问答评估报告 (Q55-Q136)

> 本报告对 kb-pilot 系统生成的 ZX Bank 问答结果进行逐题对比评估。
> 数据来源：kb-pilot 答案 (02-Temporal-Q55-Q61.md, 03-Descriptive-Q62-Q136.md)、参考问题 (Q1.csv)、RAG 指标 (R1.json)。

---

## Temporal 时间/数量类 (Q55-Q61)

---

### Q55: When did ZX Bank receive recognition for SME banking in Sri Lanka?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** ZX Bank 在 2022 年和 2023 年连续两年获得"斯里兰卡杰出中小企业银行"（Outstanding SME Bank - Sri Lanka）的认可。
**Source:** doc_016 (awards-and-recognitions.md) "Outstanding SME Bank - Sri Lanka (2022, 2023)" L15-L17
**Evidence:** "## 3. Outstanding SME Bank - Sri Lanka (2022, 2023)" 以及 "*Highlight:* Commended for tailored SME lending solutions and remittance services benefiting entrepreneurs and small businesses."

#### CSV 参考答案
**Answer:** Outstanding SME Bank - Sri Lanka (2022, 2023): Commended for tailored SME lending solutions and remittance services benefiting entrepreneurs and small businesses.
**Reference File:** Awards & Recognitions.md
**Reference Content:** Outstanding SME Bank - Sri Lanka (2022, 2023): Commended for tailored SME lending solutions and remittance services benefiting entrepreneurs and small businesses.

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 的答案完全正确，明确指出 2022 年和 2023 年两个年份，与 CSV 参考事实完全一致。RAG 指标显示 Recall=1.0 和 MRR=1.0，说明相关文档被成功检索到。

---

### Q56: How many branches does ZX Bank have in Central Bangalore?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** ZX Bank 在班加罗尔中央区（Central Bangalore）拥有 **6 家**分行。
**Source:** doc_017 (bangalore-branch-network.md) "Central Bangalore" 节 L66-L75
**Evidence:** 表格列出 6 个分行地址，IFSC 编码为 ZXIN0005201 至 ZXIN0005206，分别位于 MG Road、Lavelle Road、Brigade Road、St. Mark's Road、Cunningham Road 和 Infantry Road。

#### CSV 参考答案
**Answer:** Central Bangalore has six branches located on MG Road (Trinity Circle), Lavelle Road (Richmond Town), Brigade Road (Ashok Nagar), St. Mark's Road (Shanthala Nagar), Cunningham Road (Vasanth Nagar), and Shivajinagar (Infantry Road).
**Reference File:** Bangalore Branch Network.md
**Reference Content:** Central Bangalore has six branches located on MG Road (Trinity Circle), Lavelle Road (Richmond Town), Brigade Road (Ashok Nagar), St. Mark's Road (Shanthala Nagar), Cunningham Road (Vasanth Nagar), and Shivajinagar (Infantry Road).

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 0.5 | **NDCG@k:** 0.6309297535714575

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确回答 6 家分行，并列出具体位置信息，与参考事实一致。RAG 的 MRR 为 0.5 说明检索结果排序有待优化，但答案本身完全正确。

---

### Q57: When did ZX Bank Ltd. establish its branch in Colombo, Western Province?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** 来源文档中未包含科伦坡分行的具体设立日期。文档仅列出西部省份各分行的地址、IFSC 编码和联系电话，未提供任何分支机构的成立时间信息。
**Source:** doc_056 (sri-lanka-branch-network.md) "Western Province" 节 L7-L19
**Evidence:** 该文档列出了 Colombo、Wattala、Nugegoda、Dehiwala 等 8 家西部省份分行，但数据字段仅包含 Branch Address、IFSC Code 和 Contact Number，不包含成立日期。

#### CSV 参考答案
**Answer:** The specific establishment date of each branch isn't provided. However, ZX Bank Ltd. has a presence in Colombo, Western Province, with the branch located at 123 Galle Road, Colombo 03.
**Reference File:** Sri Lanka Branch Network.md
**Reference Content:** The specific establishment date of each branch isn't provided. However, ZX Bank Ltd. has a presence in Colombo, Western Province, with the branch located at 123 Galle Road, Colombo 03.

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 诚实地回答了"未找到设立日期"，与参考事实一致。两种回答都确认了文件不包含该信息。RAG 指标良好（Recall=1.0, MRR=1.0）。

---

### Q58: How many branches does ZX Bank have in North Chennai?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** ZX Bank 在钦奈北部（North Chennai）拥有 **8 家**分行。
**Source:** doc_041 (network-in-chennai.md) "North Chennai Branches" 节 L7-L18
**Evidence:** 表格列出 8 个分行地址，IFSC 编码为 ZXIN0001101 至 ZXIN0001108。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. has established a robust banking network within Chennai... North Chennai Branches include: No. 25, Jawahar Nagar, Perambur; 142, MTH Road, Ambattur; 50, GNT Road, Madhavaram; 7, Tollgate, Thiruvottiyur; 18A, R.K. Nagar Main Road, Vyasarpadi; 2, Mint Street, Kondithope; Old No.21, New No.48, Ennore High Road, Ennore; 63, Tondiarpet High Road, Tondiarpet.
**Reference File:** Network in Chennai.md
**Reference Content:** 列出了 North Chennai 的 8 家分行地址。

#### RAG 评估指标
**Recall@k:** N/A（R1.json 中未找到该查询的精确匹配）
**Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确回答 8 家分行，与 CSV 参考事实一致。CSV 中该问题被标记为 Descriptive 类型，但 kb-pilot 将其归类为 Temporal 类型，属于类型分类差异。答案本身完全正确。

---

### Q59: How many branches does ZX Bank have in East Chennai?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** ZX Bank 在钦奈东部（East Chennai）拥有 **8 家**分行。
**Source:** doc_041 (network-in-chennai.md) "East Chennai Branches" 节 L37-L48
**Evidence:** 表格列出 8 个分行地址，IFSC 编码为 ZXIN0001301 至 ZXIN0001308。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的独立条目。CSV 中的 Comparative 问题 "How do the number of branches in East Chennai compare to West Chennai?" 列出了 East Chennai 的 8 家分行。
**Reference File:** Network in Chennai.md（间接）
**Reference Content:** East Chennai Branches include 8 locations: Luz Church Road, Mylapore; Dr. Radhakrishnan Salai, Mylapore; Royapettah High Road, Royapettah; Chamiers Road, Teynampet; Santhome High Road, Santhome; Besant Avenue, Adyar; Eldams Road, Alwarpet; RK Mutt Road, Mandaveli.

#### RAG 评估指标
**Recall@k:** N/A（R1.json 中未找到该查询的精确匹配）
**Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确回答了 8 家分行。CSV 中没有该问题的独立条目，但通过 Comparative 问题间接确认 East Chennai 有 8 家分行。答案可信且正确。

---

### Q60: How many branches does ZX Bank have in West Chennai?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** ZX Bank 在钦奈西部（West Chennai）拥有 **8 家**分行。
**Source:** doc_041 (network-in-chennai.md) "West Chennai Branches" 节 L52-L63
**Evidence:** 表格列出 8 个分行地址，IFSC 编码为 ZXIN0001401 至 ZXIN0001408。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的独立条目。CSV 中的 Comparative 问题 "How do the number of branches in East Chennai compare to West Chennai?" 列出了 West Chennai 的 8 家分行。
**Reference File:** Network in Chennai.md（间接）
**Reference Content:** West Chennai Branches include 8 locations: Arcot Road, Vadapalani; Koyambedu Market Road, Koyambedu; Mugalivakkam Main Road, Porur; Poonamallee High Road, Kumananchavadi; Jawaharlal Nehru Main Road, Anna Nagar; 100 Feet Road, Ashok Nagar; Arcot Road, Valasaravakkam; Avadi Main Road, Avadi.

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确回答了 8 家分行。CSV 中没有独立条目，但通过 Comparative 问题间接确认 West Chennai 有 8 家分行。答案正确。

---

### Q61: How many branches does ZX Bank have in South Chennai?
**Query Type:** Temporal

#### kb-pilot 答案
**Answer:** ZX Bank 在钦奈南部（South Chennai）拥有 **8 家**分行。
**Source:** doc_041 (network-in-chennai.md) "South Chennai Branches" 节 L22-L33
**Evidence:** 表格列出 8 个分行地址，IFSC 编码为 ZXIN0001201 至 ZXIN0001208。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的独立条目。CSV 中的 Boolean 问题 "Is there a ZX Bank branch on GST Road in South Chennai?" 列出了 South Chennai 的 8 家分行。
**Reference File:** Network in Chennai.md（间接）
**Reference Content:** South Chennai Branches include 8 locations: Velachery Main Road, Velachery; GST Road, Tambaram; OMR, Sholinganallur; Medavakkam Main Road, Madipakkam; Thiruvanmiyur Main Road, Thiruvanmiyur; Mount Road, Guindy; GST Road, Chromepet; East Coast Road, Neelankarai.

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确回答了 8 家分行。CSV 中没有独立条目，但通过 Boolean 问题间接确认 South Chennai 有 8 家分行。答案正确。

---

## Descriptive 描述类 (Q62-Q136)

---

### Q62: What awards did ZX Bank Ltd. win in 2023?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在2023年获得的奖项包括：(1) Best Digital Transformation Bank - South Asia；(2) Outstanding SME Bank - Sri Lanka；(3) Financial Inclusion Leadership Award - Bangladesh；(4) Best Women's Banking Initiative - South Asia；(5) Top NRI Services Provider - Bhutan & Nepal Corridor。
**Source:** awards-and-recognitions.md
**Evidence:** 文件中详细列出了2023年的五项奖项。

#### CSV 参考答案
**Answer:** (1) Best Digital Transformation Bank - South Asia (2023); (2) Financial Inclusion Leadership Award - Bangladesh (2023); (3) Best Women's Banking Initiative - South Asia (2023); (4) Top NRI Services Provider - Bhutan & Nepal Corridor (2023).
**Reference File:** Awards & Recognitions.md
**Reference Content:** CSV 只列出了 4 个奖项（缺少 Outstanding SME Bank - Sri Lanka）。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.6666666666666666 | **MRR:** 1.0 | **NDCG@k:** 0.8927537907700456

#### 对比评估
**Correctness:** ⚠️ Partially Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 列出了 5 个奖项，而 CSV 参考事实只列出了 4 个（缺少 Outstanding SME Bank）。但 Outstanding SME Bank 的获奖年份为 2022, 2023，所以该奖项与 2023 年相关。kb-pilot 的答案更全面，包含了 CSV 遗漏的奖项。总体正确且更完整。

---

### Q63: What are the different ways to apply for a cheque book at ZX Bank?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 提供五种申请支票簿的方式：(1) ZX Bank Asia 移动应用；(2) NetBanking；(3) 前往任意分行柜台；(4) ZX Bank ATM；(5) 拨打24小时客服热线。
**Source:** apply-for-a-cheque-book.md
**Evidence:** 文件列出了五种申请渠道：Via ZX Bank Mobile App、Through NetBanking、At Branch、Via ZX Bank ATM、ZX Bank Customer Care。

#### CSV 参考答案
**Answer:** Five channels: Mobile App, NetBanking, At Branch, ZX Bank ATM, and Customer Care. Each with specific steps.
**Reference File:** Apply for a Cheque Book.md
**Reference Content:** 列出五种渠道及具体步骤。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.3333333333333333 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了五种申请渠道，与参考事实完全一致。RAG 指标良好（Recall=1.0, MRR=1.0, NDCG=1.0）。

---

### Q64: What is UPI and how does ZX Bank Asia support it?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** UPI 是实时支付系统，支持即时转账。ZX Bank Asia 通过移动应用全面支持 UPI，包括创建/链接 UPI ID、设置 UPI PIN、资金转账、账单支付、商户支付和扫码支付。每日限额 ₹1,00,000/笔，最多20笔/天。仅对印度账户持有人开放。
**Source:** upi-zx-bank-asia.md
**Evidence:** 文件描述了 UPI 的定义、激活步骤、每日限额。

#### CSV 参考答案
**Answer:** UPI is a real-time payment system enabling instant money transfer between bank accounts using mobile devices. ZX Bank Asia supports UPI seamlessly through its mobile app for fast, secure, and convenient transactions.
**Reference File:** (UPI) - ZX Bank Asia.md
**Reference Content:** 定义了 UPI 并说明 ZX Bank Asia 的支持方式。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.5 | **MRR:** 1.0 | **NDCG@k:** 0.9197207891481876

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面覆盖了 UPI 的定义和 ZX Bank 的支持方式，并补充了每日限额等详细信息，比 CSV 参考事实更丰富。答案正确且完整。

---

### Q65: What services does ZX Bank offer in Agra?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在阿格拉拥有17家分行，覆盖 North、South、East、West 和 Central Agra，提供全面的零售、企业和数字银行服务。
**Source:** agra-branch-network-overview.md
**Evidence:** 文件列出了17家分行的详细地址、IFSC 代码和联系电话。

#### CSV 参考答案
**Answer:** ZX Bank ensures broad coverage by strategically placing branches across North, South, East, West, and Central Agra. This distribution provides convenient access to retail, corporate, and digital banking.
**Reference File:** Agra Branch Network Overview.md
**Reference Content:** 描述 Agra 的全面银行服务覆盖。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案准确回答了 Agra 的 17 家分行覆盖五个区域，与参考事实一致。RAG 指标优秀。

---

### Q66: What is the branch network of ZX Bank in Bangalore?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在班加罗尔拥有覆盖五个区域的分行网络：North（8家）、South（8家）、East（8家）、West（7家）、Central（6家），共计37家分行。
**Source:** bangalore-branch-network.md
**Evidence:** 文件按区域列出了所有分行的地址、IFSC 代码和联系电话。

#### CSV 参考答案
**Answer:** ZX Bank is committed to providing comprehensive and accessible financial services across Bangalore. With a robust branch network distributed throughout North, South, East, West, and Central Bangalore.
**Reference File:** Bangalore Branch Network.md
**Reference Content:** 描述 Bangalore 的分行网络分布。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了精确的分行数量（37家），远比 CSV 参考事实更详细具体。RAG 指标全部为 1.0，检索效果完美。

---

### Q67: What is the branch network of ZX Bank Ltd. in Sri Lanka?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在斯里兰卡拥有32家分行，覆盖 Western（8家）、Central（7家）、Southern（6家）、Northern（6家）、Eastern（5家）五个省份。
**Source:** sri-lanka-branch-network.md
**Evidence:** 文件指出 "32 branches spanning all major provinces"。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. has established a robust presence in Sri Lanka with a strategically distributed network of 32 branches spanning all major provinces.
**Reference File:** Sri Lanka Branch Network.md
**Reference Content:** 描述 32 家分行覆盖所有主要省份。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案准确给出了 32 家分行及各省份的详细分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q68: What are the steps to block a card or account at ZX Bank?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** 通过 ZX Bank Asia 移动应用或 NetBanking 进入 "Card Management" 或 "Account Services"，选择 "Block/Card Hotlisting" 或 "Freeze Account" 并确认。也可拨打24小时热线或使用 "Block Instantly" 选项。
**Source:** fraud-transaction.md
**Evidence:** 文件第2步说明 "Block Your Card or Account (If Applicable)"。

#### CSV 参考答案
**Answer:** Via Mobile App or NetBanking: Go to "Card Management" or "Account Services." Select "Block/Card Hotlisting" or "Freeze Account" and confirm the action.
**Reference File:** Fraud Transaction.md
**Reference Content:** 描述通过移动应用或网银冻结卡片/账户的步骤。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 0.25 | **NDCG@k:** 0.43067655807339306

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确描述了冻结卡片/账户的步骤，与参考事实一致。RAG 的 Precision 较低（0.167），说明检索结果中相关文档比例不高，但最终答案仍是正确的。

---

### Q69: What security features does ZX Bank offer against online threats?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 提供九大安全防护措施：多因素认证、AI 欺诈检测、端到端256位加密、会话超时自动登出、安全资金转移控制、定期安全更新、用户教育、即时交易通知、安全跨境汇款通道。
**Source:** safety-features.md
**Evidence:** 文件列出了9项安全特性。

#### CSV 参考答案
**Answer:** Multi-Factor Authentication (MFA), AI-driven Fraud Detection, End-to-End Encryption, Session Timeout & Auto-Logout, Secure Fund Transfer Controls, Regular Security Updates, User Education, Transaction Notifications, and Secure Remittance Corridors.
**Reference File:** Safety Features.md
**Reference Content:** 列出9项安全特性。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了9项安全特性，与参考事实完全一致。RAG 指标优秀。

---

### Q70: What is the PRM Assistant Program at ZX Bank?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** PRM Assistant Program 是为所有账户持有人提供的专属服务，配备专属关系经理作为单一联系人，免费提供，支持电话、邮件、视频通话或移动应用聊天。提供个性化服务、数字银行指导、贷款咨询、财富管理、汇款和 NRI 服务等。
**Source:** personal-relationship-manager-assistant-program.md
**Evidence:** 文件说明 "The Personal Relationship Manager Assistant Program connects you with a dedicated relationship manager"。

#### CSV 参考答案
**Answer:** The Personal Relationship Manager Assistant Program connects you with a dedicated relationship manager - a friendly banking expert who understands your unique needs.
**Reference File:** Personal Relationship Manager Assistant Program.md
**Reference Content:** 描述 PRM 助理计划的基本概念。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了 PRM 助理计划，包含比 CSV 参考事实更丰富的细节。RAG 指标优秀。

---

### Q71: What services does the PRM Assistant provide?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** PRM 助理提供六项服务：(1) 账户查询；(2) 数字银行指导；(3) 贷款和信贷咨询；(4) 财富和投资礼宾服务；(5) 汇款和 NRI 服务；(6) 问题解决。此外还有个性化推荐、预算建议和主动通知。
**Source:** personal-relationship-manager-assistant-program.md
**Evidence:** 文件中的表格列出了六项主要服务。

#### CSV 参考答案
**Answer:** The PRM Assistant supports account inquiries, digital banking guidance, loan and credit advisory, wealth and investment concierge services, remittance and NRI services, and expedites issue resolution.
**Reference File:** Personal Relationship Manager Assistant Program.md
**Reference Content:** 列出六项服务。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.3333333333333333 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了六项服务，与参考事实一致。CSV 中该问题被标记为 Open-Ended 类型，但 kb-pilot 答案仍然准确。

---

### Q72: What is ZX Bank's Agriculture Loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 的农业贷款是专为农民和农业企业设计的贷款产品，支持作物生产、设备采购、灌溉解决方案、奶业及相关活动。贷款金额从 ₹25,000 至 ₹50 万卢比，具有竞争力的利率、灵活的还款方式、快速放款、无提前还款罚金，女性农业企业享受额外1%利率折扣。
**Source:** agriculture-loan.md
**Evidence:** 文件描述 "ZX Bank offers specialized Agriculture Loans to empower farmers and agribusinesses across South Asia"。

#### CSV 参考答案
**Answer:** ZX Bank offers specialized Agriculture Loans designed to support crop production, equipment purchase, irrigation solutions, dairy, and allied activities across South Asia. The loans aim to empower farmers and agribusinesses with flexible terms and low-interest rates to fuel rural prosperity.
**Reference File:** ZX Bank Agriculture Loan.md
**Reference Content:** 描述农业贷款的基本目的和特点。

#### RAG 评估指标
**Recall@k:** N/A（CSV 中匹配到，但 R1.json 中未找到精确匹配）
**Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了农业贷款的特点、金额范围、利率和特殊优惠，比 CSV 参考事实更详细。答案正确且完整。

---

### Q73: Where are the ZX Bank ATMs located in Bangladesh?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟加拉国拥有18个 ATM 网点，分布在 Dhaka（2个）、Chattogram、Sylhet、Khulna、Rajshahi、Barisal、Rangpur、Mymensingh、Cumilla、Narayanganj、Gazipur、Bogura、Jessore、Savar、Sirajganj、Tangail、Pabna 等城市。
**Source:** bangladesh-atm-locations.md
**Evidence:** 文件列出了18个 ATM 网点，覆盖16个城市。

#### CSV 参考答案
**Answer:** ZX Bank provides convenient banking access across Bangladesh through its growing ATM network. The list of ATM locations includes major cities such as Dhaka, Chattogram, Sylhet, Khulna, and others.
**Reference File:** Bangladesh ATM Locations.md
**Reference Content:** 描述孟加拉国的 ATM 网络覆盖主要城市。

#### RAG 评估指标
**Recall@k:** 0.5 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案非常详细，列出了所有18个 ATM 网点的具体城市分布，远比 CSV 参考事实详细。RAG 的 Recall=0.5 说明部分相关文档未检索到，但答案本身正确且完整。

---

### Q74: Where are ZX Bank ATMs located in Mumbai?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买拥有34家分行，分布于 South Mumbai（7家）、North Mumbai（7家）、East Mumbai（6家）、West Mumbai（7家）和 Central Mumbai（8家）。
**Source:** network-in-mumbai.md
**Evidence:** 文件列出 "Total Branches Listed: 34 across Mumbai"。

#### CSV 参考答案
**Answer:** Below is a list of ZX Bank ATMs located at major hospitals across key cities in India. Mumbai includes Lilavati Hospital & Research Centre and Kokilaben Dhirubhai Ambani Hospital.
**Reference File:** ATM Locations at Major Hospitals.md
**Reference Content:** 列出孟买医院的 ATM 位置。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ❌ Incorrect
**Satisfaction:** ⭐⭐ (2/5)
**Evaluation:** **严重问题：kb-pilot 回答了"分行"（branches）信息，但问题问的是"ATM 位置"（ATMs）。** CSV 参考事实是关于医院 ATM 位置的信息，而 kb-pilot 给出了 Mumbai 分行网络的信息。这是答非所问。kb-pilot 的答案虽然本身正确，但完全偏离了问题意图。

---

### Q75: What are the key features of health insurance?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** 健康保险的关键特征包括：覆盖医疗费用、现金结算治疗、住院前后费用覆盖、家庭浮动计划、可选附加险。保险类型包括个人健康保险、家庭浮动健康保险、老年人健康保险、重大疾病保险和团体健康保险。
**Source:** health-insurance.md
**Evidence:** 文件列出了健康保险的关键特征、类型和福利。

#### CSV 参考答案
**Answer:** Key Features include coverage for medical expenses such as hospitalization, surgeries, outpatient care, prescription drugs, diagnostics, and preventive services. Many insurers offer cashless treatment, pre- and post-hospitalization coverage, family floater plans, and optional add-ons.
**Reference File:** Health Insurance.md
**Reference Content:** 列出健康保险的关键特征。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.3333333333333333 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确概括了健康保险的关键特征，与参考事实一致。但缺少 "prescription drugs, diagnostics" 等具体细节。

---

### Q76: What are the locations of ZX Bank ATMs in Mumbai?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买海滩路附近的 ATM 位置包括：(1) Marine Drive, Chowpatty End；(2) Juhu Tara Road；(3) Girgaum Chowpatty；(4) Versova Beach Road；(5) Carter Road；(6) Aksa Beach Road；(7) Dadar Chowpatty。
**Source:** beach-road-atms-list-major-indian-cities.md
**Evidence:** 文件 Mumbai 部分列出了7个 Beach Road 附近的 ATM 位置。

#### CSV 参考答案
**Answer:** 1. Marine Drive, Chowpatty End, Mumbai 400002; 2. Juhu Tara Road, near Juhu Beach Entrance, Mumbai 400049; 3. Girgaum Chowpatty, Chowpatty Seaface Road, Mumbai 400007; 4. Versova Beach Road, Andheri West, Mumbai 400061; 5. Carter Road, Bandra West, Mumbai 400050; 6. Aksa Beach Road, Malad West, Mumbai 400095; 7. Dadar Chowpatty, Swatantrya Veer Savarkar Marg, Mumbai 400028.
**Reference File:** Beach Road ATMs List (Major Indian Cities).md
**Reference Content:** 列出7个海滩路附近的 ATM 位置。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 0.5 | **NDCG@k:** 0.6309297535714575

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确列出了7个海滩路附近的 ATM 位置，与 CSV 参考事实一致。但 kb-pilot 标题中加了 "(beach road)" 限定词，而 CSV 问题没有。答案本身正确。

---

### Q77: What is the branch network of ZX Bank Ltd. in Ahmedabad?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在艾哈迈达巴德拥有17家分行，覆盖 North（3家）、South（3家）、East（4家）、West（4家）和 Central Ahmedabad（3家）。
**Source:** ahmedabad-branch-network.md
**Evidence:** 文件列出 "17 branches" 并分五个区域详细列出。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. ensures robust banking accessibility throughout Ahmedabad. The bank has a strategically distributed network... ZX Bank operates 17 branches.
**Reference File:** Ahmedabad Branch Network.md
**Reference Content:** 描述 Ahmedabad 的17家分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案准确给出了17家分行及五个区域的详细分布，与参考事实一致。RAG 指标优秀。

---

### Q78: How does ZX Bank Ltd. serve the Coimbatore area?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在哥印拜陀通过覆盖五个区域的分行网络提供服务：North（3家）、South（3家）、East（2家）、West（3家）和 Central Coimbatore（2家），共计13家分行。提供从个人金融到数字交易的全方位服务。
**Source:** network-in-coimbatore.md
**Evidence:** 文件列出了五个区域共13家分行的详细信息。

#### CSV 参考答案
**Answer:** Coimbatore is served by a robust banking network from ZX Bank Ltd. The bank ensures comprehensive financial access through a well-planned distribution of branches across all major regions of the city.
**Reference File:** Network in Coimbatore.md
**Reference Content:** 描述 Coimbatore 的全方位银行服务。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了精确的分行数量和区域分布，远比 CSV 参考事实详细。RAG 指标全部为 1.0。

---

### Q79: How is the branch network of ZX Bank Ltd. distributed in Jaipur?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在斋浦尔拥有25家分行，分布于 North（5家）、South（5家）、East（5家）、West（5家）和 Central Jaipur（5家）。
**Source:** jaipur-branch-network.md
**Evidence:** 文件列出了五个区域共25家分行的详细信息。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. maintains a robust banking presence across Jaipur, providing comprehensive financial services through an extensive branch distribution.
**Reference File:** Jaipur Branch Network.md
**Reference Content:** 描述 Jaipur 的分行网络分布。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了精确的25家分行及五个区域各5家的分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q80: Can you describe the features and benefits of ZX Bank's personal loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 个人贷款的特点：贷款金额最高 ₹30,00,000、期限12至60个月、快速审批、零抵押、部分还款和提前还款选项。利率：印度/斯里兰卡工薪族 11.75%-17.99%，自雇人士 13.25%-19.99%，孟加拉国/不丹/尼泊尔 13.50%-21.00%。
**Source:** personal-loan-information.md
**Evidence:** 文件列出了 Features & Benefits、Interest Rate 表格等详细信息。

#### CSV 参考答案
**Answer:** Features & Benefits: Loan Amount up to ₹30,00,000 (INR), Flexible Tenure 12 to 60 months, Quick Approval, Zero Collateral, Part-Payment & Foreclosure.
**Reference File:** Personal Loan Information.md
**Reference Content:** 列出个人贷款的特点和福利。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.3333333333333333 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整描述了个人贷款的特点和利率信息，比 CSV 参考事实更详细。答案正确。

---

### Q81: What services does ZX Bank provide in Visakhapatnam?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在维沙卡帕特南设有8家分行，覆盖 North（2家）、South（2家）、East（1家）、West（1家）和 Central Visakhapatnam（2家）。提供零售、企业和数字银行服务。
**Source:** visakhapatnam-branch-network.md
**Evidence:** 文件列出了8家分行的详细地址。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. maintains a robust footprint in Visakhapatnam, ensuring accessible and modern banking solutions for residents across the city's diverse regions... providing retail, corporate, and digital banking services.
**Reference File:** Visakhapatnam Branch Network.md
**Reference Content:** 描述 Visakhapatnam 的银行服务。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了精确的8家分行及区域分布，与参考事实一致。

---

### Q82: What is the branch network of ZX Bank in Bangladesh?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟加拉国拥有18家分行，分布在 Dhaka Region（5家）、Chittagong Region（4家）、Khulna Region（3家）、Rajshahi Region（3家）和 Sylhet Region（3家）。
**Source:** bangladesh-branch-network.md
**Evidence:** 文件说明 "total of 18 branches"。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. has established a robust presence in Bangladesh with a branch network covering key regions.
**Reference File:** Bangladesh Branch Network.md
**Reference Content:** 描述孟加拉国的分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了18家分行及五个区域的详细分布，与参考事实一致。

---

### Q83: What services does ZX Bank provide at bus stands?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在印度主要城市的公交站提供 ATM 服务，覆盖 Mumbai、Delhi、Bangalore、Hyderabad、Chennai、Kolkata、Pune、Ahmedabad、Surat 等20个城市，各6个 ATM 位置。
**Source:** zx-bank-atms-at-major-bus-stands-india.md
**Evidence:** 文件列出了多个城市公交站的 ATM 地址。

#### CSV 参考答案
**Answer:** ZX Bank provides ATM services at bus stands across major Indian cities.
**Reference File:** (not explicitly found in CSV)
**Reference Content:** N/A

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确描述了公交站 ATM 服务，列出了多个城市。RAG 指标优秀。

---

### Q84: What are the features of the ZX Bank Savings Account?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 储蓄账户的特点包括：有竞争力的利率、零或低最低余额、e-KYC 即时开户、免费国际借记卡、移动应用和 NetBanking 访问、UPI 和 QR 支付、奖励积分、安全保障、指定受益人。最低余额：常规 ₹5,000，数字零余额账户无最低余额。
**Source:** savings-account-overview.md
**Evidence:** 文件列出了 Savings Account Features 的9项特点。

#### CSV 参考答案
**Answer:** ZX Bank Savings Account features include competitive interest rates, zero or low minimum balance, instant e-KYC opening, free international debit card, digital access, UPI & QR payments, reward points, security features, and nominee facility.
**Reference File:** Savings Account Overview.md
**Reference Content:** 列出储蓄账户的特点。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面列出了储蓄账户的特点，包括最低余额要求，与参考事实一致。

---

### Q85: Which services are available at ZX Bank ATMs in Bhutan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在不丹的15个 ATM 提供：24/7现金取款、余额查询、迷你对账单打印、无卡 QR 取款。
**Source:** bank-atms-in-bhutan.md
**Evidence:** 文件说明 "All ZX Bank ATMs offer: 24/7 cash withdrawal, Balance inquiry, Mini-statement printing, Cardless QR withdrawals"。

#### CSV 参考答案
**Answer:** All ZX Bank ATMs offer: 24/7 cash withdrawal, balance inquiry, mini-statement printing, and cardless QR withdrawals supported by the ZX Bank Asia app.
**Reference File:** Bank ATMs in Bhutan.md
**Reference Content:** 列出不丹 ATM 的服务。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确列出了不丹 ATM 的四种服务，与参考事实一致。

---

### Q86: What colleges in Delhi have ZX Bank ATMs?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在德里的以下大学设有 ATM：University of Delhi (North Campus) 和 Jawaharlal Nehru University (JNU)。
**Source:** atms-at-major-colleges-and-universities.md
**Evidence:** 文件 Delhi 部分列出了这两所大学的 ATM 位置。

#### CSV 参考答案
**Answer:** Delhi: University of Delhi (North Campus) - Outside Central Library, North Campus, Delhi 110007; Jawaharlal Nehru University (JNU) - Near Sabarmati Hostel, JNU Campus, New Mehrauli Road, Delhi 110067.
**Reference File:** ATMs at Major Colleges & Universities.md
**Reference Content:** 列出德里大学和 JNU 的 ATM 位置。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确回答了两所大学，与参考事实一致。

---

### Q87: What is the branch network of ZX Bank Ltd. in Pune?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在浦那拥有40家分行，覆盖 North（8家）、South（8家）、East（8家）、West（8家）和 Central Pune（8家）。
**Source:** pune-branch-network.md
**Evidence:** 文件说明 "40 ZX Bank branches"。

#### CSV 参考答案
**Answer:** Pune is well-served by ZX Bank Ltd.'s comprehensive branch network, strategically distributed across North, South, East, West, and Central Pune.
**Reference File:** Pune Branch Network.md
**Reference Content:** 描述 Pune 的分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案准确给出了40家分行及五个区域各8家的分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q88: What is the structure of ZX Bank's branch network in Indore?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在印多尔的分行网络分布在五个区域：Rau Region（2家）、Vijay Nagar Region（2家）、Palasia Region（2家）、Annapurna Region（1家）和 Sudama Nagar Region（1家），共计8家分行。
**Source:** branch-network-in-indore.md
**Evidence:** 文件列出了 Indore 五个区域的分行详细信息。

#### CSV 参考答案
**Answer:** Indore benefits from an extensive banking infrastructure. ZX Bank has established a robust presence in the city, distributing its branches strategically across different regions.
**Reference File:** Branch Network in Indore.md
**Reference Content:** 描述 Indore 的分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了8家分行及五个区域的详细分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q89: What documents are required for salaried individuals to get a personal loan at ZX Bank Ltd.?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** 工薪族申请个人贷款所需文件：申请表、照片身份证明、地址证明、最近3个月工资单、最近6个月银行对账单、1张护照尺寸照片、PAN 卡（印度申请人）。
**Source:** personal-loan-information.md
**Evidence:** 文件 "For Salaried Individuals" 下列出了7项所需文件。

#### CSV 参考答案
**Answer:** Documentation Required for Salaried Individuals: Completed Personal Loan Application Form, Photo Identity Proof, Address Proof, Latest 3 months' Salary Slips, Last 6 months' Bank Statements, 1 Passport-size Photograph, PAN Card (for Indian applicants).
**Reference File:** Personal Loan.md
**Reference Content:** 列出工薪族所需文件。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.3333333333333333 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了7项所需文件，与参考事实一致。

---

### Q90: What services does ZX Bank offer in Surat?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在苏拉特通过18家分行提供服务，覆盖 North（4家）、South（3家）、East（4家）、West（3家）和 Central Surat（4家）。提供零售、企业和数字银行全套服务。
**Source:** surat-branch-network.md
**Evidence:** 文件列出了五个区域共18家分行的详细信息。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. is committed to delivering accessible and reliable banking services across Surat. Each branch offers a full suite of retail, corporate, and digital services.
**Reference File:** Surat Branch Network.md
**Reference Content:** 描述 Surat 的银行服务。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了18家分行及五个区域的详细分布，与参考事实一致。

---

### Q91: Where are the PVR Cinemas located in Mumbai?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** 根据 ZX Bank 在电影院 ATM 位置的数据，孟买的 PVR 电影院位于 PVR ICON, Phoenix Mills, High Street Phoenix, Lower Parel, Mumbai 400013。
**Source:** atm-locations-at-major-movie-theaters.md
**Evidence:** 文件 Mumbai 部分列出了 "PVR ICON, Phoenix Mills"。

#### CSV 参考答案
**Answer:** PVR ICON, Phoenix Mills, Address: High Street Phoenix, Lower Parel, Mumbai 400013.
**Reference File:** ATM Locations at Major Movie Theaters.md
**Reference Content:** 列出 PVR 电影院位置。

#### RAG 评估指标
**Recall@k:** 0.5 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确回答了 PVR 电影院的位置。RAG 的 Recall=0.5 说明部分相关文档未检索到，但答案本身正确。

---

### Q92: How is ZX Bank's branch network distributed in Kolkata?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在加尔各答的分行网络分布在 North（4家）、South（4家）、East（3家）、West（3家）和 Central Kolkata（3家），共计17家分行。
**Source:** branches-in-kolkata.md
**Evidence:** 文件列出了五个区域共17家分行。

#### CSV 参考答案
**Answer:** Kolkata enjoys robust banking infrastructure supported by ZX Bank's expanding network. ZX Bank has strategically distributed its branches across the city's major regions.
**Reference File:** Branches in Kolkata.md
**Reference Content:** 描述 Kolkata 的分行网络分布。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.6666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了17家分行及五个区域的详细分布，与参考事实一致。

---

### Q93: What makes ASK Zia a secure banking assistant?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ASK Zia 是一个安全的银行助手，因为它使用端到端加密、安全认证，并且从不要求提供 PIN 或密码等敏感数据。所有操作均符合 ZX Bank 的隐私和安全政策。Zia 可在网站和 WhatsApp 上使用，提供24/7服务。
**Source:** ask-zia-your-24-7-banking-assistant.md
**Evidence:** 文件说明 "ASK Zia uses end-to-end encryption, secure authentication, and never asks for sensitive data"。

#### CSV 参考答案
**Answer:** ASK Zia features end-to-end encryption, secure authentication, and never asks for sensitive data like PINs or passwords, ensuring compliance with ZX Bank's privacy and security policies.
**Reference File:** ASK Zia - Your 24:7 Banking Assistant.md
**Reference Content:** 描述 ASK Zia 的安全特性。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 0.5 | **NDCG@k:** 0.6309297535714575

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确描述了 ASK Zia 的安全特性，与参考事实一致。

---

### Q94: What is the branch network of ZX Bank in Patna?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在巴特那拥有13家分行，分布在 North（3家）、South（3家）、East（2家）、West（3家）和 Central Patna（2家）。
**Source:** bank-branches-in-patna.md
**Evidence:** 文件说明 "13 branches"。

#### CSV 参考答案
**Answer:** Patna is well-served by the extensive branch network of ZX Bank. The bank has a robust presence spread across North, South, East, West, and Central Patna, consisting of 13 branches.
**Reference File:** Bank Branches in Patna.md
**Reference Content:** 描述 Patna 的13家分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了13家分行及五个区域的详细分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q95: What is the branch network of ZX Bank in Delhi?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在德里拥有50家分行，分布在 North（10家）、South（10家）、East（10家）、West（10家）和 Central Delhi（10家）。
**Source:** branch-network-in-delhi.md
**Evidence:** 文件列出了五个区域共50家分行。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. is committed to providing seamless and accessible banking services across Delhi. ZX Bank branches are strategically distributed across North, South, East, West, and Central Delhi.
**Reference File:** Branch Network in Delhi.md
**Reference Content:** 描述 Delhi 的分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了50家分行及五个区域各10家的详细分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q96: What is the branch network of ZX Bank in Nepal?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在尼泊尔拥有20家分行，分布在 Province No. 1（4家）、Madhesh Province（4家）、Bagmati Province（4家）、Gandaki Province（4家）和 Lumbini Province（4家）。
**Source:** branch-network-in-nepal.md
**Evidence:** 文件说明 "20 branches"。

#### CSV 参考答案
**Answer:** ZX Bank has established a robust and customer-focused branch network across Nepal... ZX Bank's 20 branches are strategically located.
**Reference File:** Branch Network in Nepal.md
**Reference Content:** 描述 Nepal 的20家分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了20家分行及五个省份的详细分布，与参考事实一致。

---

### Q97: What are the methods to request a ZX Bank Credit Card closure?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 信用卡注销可通过以下渠道申请：(1) ZX Bank Asia 移动应用；(2) ZX NetBanking；(3) 24小时客服热线；(4) 前往任意分行。
**Source:** zx-bank-credit-card-help.md
**Evidence:** 文件列出了四种注销渠道。

#### CSV 参考答案
**Answer:** You can place a closure request via the ZX Bank Mobile App, ZX NetBanking, Customer Care, or by visiting a branch.
**Reference File:** ZX Bank Credit Card Help.md
**Reference Content:** 列出四种注销渠道。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.5 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了四种信用卡注销渠道，与参考事实一致。

---

### Q98: What types of credit cards does ZX Bank offer?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 提供五种信用卡：ZX Platinum Credit Card、ZX Gold Credit Card、ZX Women Empower Credit Card、ZX Student Credit Card、ZX NRI Credit Card。
**Source:** zx-bank-credit-card.md
**Evidence:** 文件列出了五种信用卡的详细信息。

#### CSV 参考答案
**Answer:** ZX Bank offers a versatile range of credit cards... including the ZX Platinum Credit Card, ZX Gold Credit Card, ZX Women Empower Credit Card, ZX Student Credit Card, and ZX NRI Credit Card.
**Reference File:** ZX Bank Credit Card.md
**Reference Content:** 列出五种信用卡。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.8333333333333334 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了五种信用卡类型，与参考事实一致。

---

### Q99: Where are ZX Bank ATMs located in Mumbai (shopping malls)?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买购物中心的 ATM 位置包括：(1) Phoenix Marketcity, Kurla；(2) Oberoi Mall, Goregaon East；(3) R City Mall, Ghatkopar West。
**Source:** atm-locations-at-major-shopping-malls.md
**Evidence:** 文件 Mumbai 部分列出了这三个购物中心的 ATM 位置。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的精确匹配条目。
**Reference File:** N/A
**Reference Content:** N/A

#### RAG 评估指标
**Recall@k:** N/A（R1.json 中未找到该查询的精确匹配）
**Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ❓ Not Found（无法验证）
**Satisfaction:** ⭐⭐⭐ (3/5)
**Evaluation:** kb-pilot 的答案列出了三个购物中心的 ATM 位置，但 CSV 和 R1.json 中都未找到该问题的精确匹配条目，无法直接验证。答案本身结构合理，但缺乏参考标准进行比对。

---

### Q100: What is the branch network overview of ZX Bank Ltd. in Kanpur?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在坎普尔拥有23家分行，分布在 North（5家）、South（5家）、East（4家）、West（5家）和 Central Kanpur（4家）。
**Source:** kanpur-branch-network.md
**Evidence:** 文件列出了五个区域共23家分行。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. maintains a robust and accessible network across Kanpur, ensuring quality banking services are readily available to residents in every part of the city.
**Reference File:** Kanpur Branch Network.md
**Reference Content:** 描述 Kanpur 的分行网络。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 1.0 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了23家分行及五个区域的详细分布，与参考事实一致。RAG 指标全部为 1.0。

---

### Q101: What are the features of the ZX Bank Gold Loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 黄金贷款的特点包括：快速处理即时放款、黄金珠宝安全存放、灵活还款期限、数字跟踪和管理、利率从9.5%起、最高贷款金额印度 ₹50 万卢比/LTV最高75%、所需文件：身份证明、地址证明、照片和质押黄金。
**Source:** zx-bank-gold-loan.md
**Evidence:** 文件列出了 Features、Interest Rate、Maximum Loan Amount 和 Documents Required。

#### CSV 参考答案
**Answer:** Features: Fast Processing, Secure Storage, Flexible Repayment, Digital Tracking. Interest Rate starting at 9.5% p.a.
**Reference File:** ZX Bank Gold Loan.md
**Reference Content:** 列出黄金贷款的特点。

#### RAG 评估指标
**Recall@k:** 1.0 | **Precision@k:** 0.16666666666666666 | **MRR:** 1.0 | **NDCG@k:** 1.0

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了黄金贷款的特点，包含利率、金额、文件和数字跟踪等详细信息，比 CSV 参考事实更丰富。

---

### Q102: How many branches does ZX Bank have in North Chennai?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在北钦奈拥有8家分行：Perambur、Ambattur、Madhavaram、Thiruvottiyur、Vyasarpadi、Kondithope、Ennore 和 Tondiarpet。
**Source:** network-in-chennai.md
**Evidence:** 文件 North Chennai 部分列出了8家分行。

#### CSV 参考答案
**Answer:** North Chennai Branches include 8 locations: Perambur, Ambattur, Madhavaram, Thiruvottiyur, Vyasarpadi, Kondithope, Ennore, Tondiarpet.
**Reference File:** Network in Chennai.md
**Reference Content:** 列出 North Chennai 的8家分行。

#### RAG 评估指标
**Recall@k:** N/A（R1.json 中未找到该查询的精确匹配）
**Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确回答了8家分行并列出具体名称，与 CSV 参考事实一致。

---

### Q103: What are the features of the ZX Bank Current Account?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 活期账户的特点包括：零初始存款、高月度现金存取限额、560+分行和1,200+ ATM 访问、数字银行套件、免费支票簿和借记卡、透支便利、专属关系经理、独家优惠、月度平均余额仅 ₹10,000。
**Source:** current-account-overview.md
**Evidence:** 文件列出了 Current Account Features 的9项特点。

#### CSV 参考答案
**Answer:** Zero Initial Deposit, Seamless Transactions, Multi-Location Banking (560+ branches, 1,200+ ATMs), Digital Banking Suite, Personalised Cheque Book & Debit Card, Overdraft Facility, Dedicated Relationship Manager, Exclusive Offers, High monthly cash limits.
**Reference File:** Current Account Overview.md
**Reference Content:** 列出活期账户的9项特点。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了活期账户的9项特点，与参考事实一致。

---

### Q104: How do I apply for a ZX Bank Current Account online?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** 在线申请 ZX Bank 活期账户的步骤：(1) 访问 www.zxbank.asia/current-account；(2) 点击 "Open Current Account"；(3) 使用 Aadhaar 和 PAN 完成数字 e-KYC；(4) 上传商业文件；(5) 选择分行，通过 OTP 验证；(6) 立即收到账户号码和数字开户套件。
**Source:** current-account-overview.md
**Evidence:** 文件 "Online Process" 下列出了6个步骤。

#### CSV 参考答案
**Answer:** Online Process: 1. Visit www.zxbank.asia/current-account; 2. Click on 'Open Current Account'; 3. Complete digital e-KYC with Aadhaar and PAN; 4. Upload business documents; 5. Choose branch & verify mobile/email via OTP; 6. Receive instant account number and digital onboarding kit.
**Reference File:** Current Account Overview.md
**Reference Content:** 列出在线申请活期账户的6个步骤。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了在线申请活期账户的6个步骤，与参考事实一致。

---

### Q105: What benefits come with the ZX Current Account Welcome Kit?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX 活期账户欢迎礼包包括：高级旅行包、通用旅行适配器、个人化借记卡、启动支票簿、即时 NetBanking 和移动应用访问、独家健康保险保额 ₹10,00,000。
**Source:** current-account-overview.md
**Evidence:** 文件 "What's in the Kit?" 下列出了6项内容。

#### CSV 参考答案
**Answer:** Premium Travel Bag, Universal Travel Adapter (4 Plugs, 150 Countries), Personalised Debit Card, Starter Cheque Book, Instant NetBanking & Mobile App Access, Exclusive Health Insurance (₹10,00,000 coverage).
**Reference File:** Current Account Overview.md
**Reference Content:** 列出欢迎礼包的6项内容。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了欢迎礼包的6项内容，与参考事实一致。

---

### Q106: What is the branch network of ZX Bank in Mumbai?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买拥有34家分行，分布于 South（7家）、North（7家）、East（6家）、West（7家）和 Central Mumbai（8家）。
**Source:** network-in-mumbai.md
**Evidence:** 文件列出 "Total Branches Listed: 34 across Mumbai"。

#### CSV 参考答案
**Answer:** Mumbai has a network of 34 well-placed branches across South, North, East, West, and Central Mumbai.
**Reference File:** Network in Mumbai.md
**Reference Content:** 描述 Mumbai 的34家分行网络。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了34家分行及五个区域的详细分布，与参考事实一致。

---

### Q107: Where can I find ZX Bank ATMs in Mumbai (railway stations/airports)?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买火车站和机场的 ATM 位置：火车站包括 CSMT、Mumbai Central、Dadar、Lokmanya Tilak Terminus；机场包括 Chhatrapati Shivaji Maharaj International Airport (Terminals 1 & 2)。
**Source:** atms-at-railway-stations-and-airports.md
**Evidence:** 文件 Mumbai 部分列出了4个火车站和1个机场的 ATM 位置。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的精确匹配条目。
**Reference File:** N/A
**Reference Content:** N/A

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ❓ Not Found（无法验证）
**Satisfaction:** ⭐⭐⭐ (3/5)
**Evaluation:** kb-pilot 的答案列出了火车站和机场的 ATM 位置，但 CSV 和 R1.json 中都未找到该问题的精确匹配条目，无法直接验证。

---

### Q108: What services do ZX Bank ATMs offer?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank ATM 提供的服务包括：现金取款、余额查询、迷你对账单、卡间转账、Fast Pay 和充值服务。许多 ATM 还提供24/7安保和多语言界面。在不丹的 ATM 还支持无卡 QR 取款。
**Source:** atms-at-railway-stations-and-airports.md 及 bank-atms-in-bhutan.md
**Evidence:** 文件说明 "All ZX Bank ATMs at these locations support: Cash Withdrawal, Balance Enquiry, Mini Statements, Fund Transfer (card-to-card), Fast Pay, and Recharge Services."

#### CSV 参考答案
**Answer:** All ZX Bank ATMs support: Cash Withdrawal, Balance Enquiry, Mini Statements, Fund Transfer (card-to-card), Fast Pay, and Recharge Services. Many ATMs have 24x7 security and multi-language interface.
**Reference File:** ATMs at Railway Stations and Airports.md
**Reference Content:** 列出 ATM 的基本服务。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了 ATM 提供的各项服务，与参考事实一致。

---

### Q109: Where are ZX Bank's main ATM locations in Biratnagar?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在比拉特纳加尔的主要 ATM 位置是 Main Market ATM，地址：112 Bhrikuti Chowk, Biratnagar 56613。此外，Biratnagar Main Road 还设有分行。
**Source:** nepal-atm-locations.md 和 branch-network-in-nepal.md
**Evidence:** 列出 "Main Market ATM, 112 Bhrikuti Chowk, Biratnagar 56613"。

#### CSV 参考答案
**Answer:** In Biratnagar, ZX Bank has its main ATM located at 112 Bhrikuti Chowk, Biratnagar 56613.
**Reference File:** Nepal ATM Locations.md
**Reference Content:** 列出 Biratnagar 的 ATM 位置。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确回答了 ATM 位置，并补充了分行信息，与参考事实一致。

---

### Q110: What services does ZX Bank offer to ensure convenient banking for customers in Nepal?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在尼泊尔提供20家分行网络覆盖五个省份，ATM 网络覆盖多个城市，还提供数字银行服务、汇款通道、移动银行和 AI 助手 Zia。
**Source:** branch-network-in-nepal.md 和 nepal-atm-locations.md
**Evidence:** 列出20家分行和多个 ATM 位置。

#### CSV 参考答案
**Answer:** ZX Bank provides a robust ATM network across Nepal, ensuring convenient banking access for local residents and NRI customers. ZX Bank ATMs are operational in various convenient locations.
**Reference File:** Nepal ATM Locations.md
**Reference Content:** 描述 Nepal 的便捷银行服务。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案全面描述了 Nepal 的银行服务，包括分行、ATM、数字银行等，比 CSV 参考事实更丰富。

---

### Q111: What are the locations of ZX Bank ATMs in Mumbai (parks)?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买公园的 ATM 位置包括：(1) Shivaji Park, Dadar West；(2) Jijamata Udyan, Byculla East；(3) Sanjay Gandhi National Park, Borivali East；(4) Hanging Gardens, Malabar Hill；(5) Priyadarshini Park, Nepean Sea Road；(6) Five Gardens, Matunga。
**Source:** zx-bank-atm-network-at-major-parks-india.md
**Evidence:** 文件 Mumbai 部分列出了6个公园的 ATM 位置。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的精确匹配条目。
**Reference File:** N/A
**Reference Content:** N/A

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ❓ Not Found（无法验证）
**Satisfaction:** ⭐⭐⭐ (3/5)
**Evaluation:** kb-pilot 的答案列出了6个公园的 ATM 位置，但 CSV 和 R1.json 中都未找到该问题的精确匹配条目，无法直接验证。

---

### Q112: What is ZX Bank NetBanking?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank NetBanking 是一个安全的在线银行平台，提供账户余额和对账单查看、资金转账、账单支付、开立/关闭定期存款、贷款和信用卡管理、支票停止支付、请求支票簿等。
**Source:** netbanking-guide.md
**Evidence:** 文件说明 "ZX Bank NetBanking is a secure online banking platform for individuals and businesses"。

#### CSV 参考答案
**Answer:** ZX Bank NetBanking is a secure online banking platform for individuals and businesses to manage accounts, perform transactions, pay bills, and access banking services anytime, anywhere.
**Reference File:** NetBanking Guide.md
**Reference Content:** 描述 NetBanking 的基本功能。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了 NetBanking 的功能，比 CSV 参考事实更详细。

---

### Q113: What are the daily transaction limits for ZX Bank NetBanking?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank NetBanking 的每日交易限额：NEFT/RTGS ₹10,00,000；IMPS/UPI ₹2,00,000；账单支付 ₹1,00,000；行内交易 ₹20,00,000。企业和优先客户可申请更高限额。
**Source:** netbanking-guide.md
**Evidence:** 文件中的 "Daily Transaction Limits" 表格列出了各项限额。

#### CSV 参考答案
**Answer:** NEFT/RTGS ₹10,00,000; IMPS/UPI ₹2,00,000; Bill Payments ₹1,00,000; Own ZX Bank account Txns ₹20,00,000. Corporate/priority customers may request higher limits.
**Reference File:** NetBanking Guide.md
**Reference Content:** 列出每日交易限额表格。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案准确列出了各项交易限额，与参考事实一致。

---

### Q114: What benefits does the ZX Bank Salary Saving Account offer?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 工资储蓄账户的福利包括：零余额便利、即时开户、免费国际借记卡、自动转存定期存款、无限免费资金转账、优惠贷款利率、账单支付和充值、AI 银行助手 Zia 24/7服务。
**Source:** salary-saving-account.md
**Evidence:** 文件列出了 Salary Saving Account Features 的8项福利。

#### CSV 参考答案
**Answer:** Zero Balance Facility, Instant Account Opening, Free Debit Card, Auto Sweep Fixed Deposit, Unlimited Fund Transfers, Preferential Loan Rates, Bill Payments & Recharge, AI Assistant Zia 24/7.
**Reference File:** Salary Saving Account.md
**Reference Content:** 列出工资储蓄账户的8项福利。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了工资储蓄账户的8项福利，与参考事实一致。

---

### Q115: What is included in the ZX Bank Salary Saving Account Welcome Kit?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 工资储蓄账户欢迎礼包包括：(1) ZX Bank 品牌旅行包；(2) 国际旅行适配器（4插头，150个国家适用）；(3) 欢迎信和账户文件；(4) 借记卡（国际有效性和非接触式功能）。
**Source:** salary-saving-account.md
**Evidence:** 文件 "Savings Account Welcome Kit" 下列出了4项内容。

#### CSV 参考答案
**Answer:** ZX Bank Branded Travel Bag, International Travel Adapter (4 Plugs, 150 Countries), Welcome Letter & Account Documents, Debit Card (International validity and contactless features).
**Reference File:** Salary Saving Account.md
**Reference Content:** 列出欢迎礼包的4项内容。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了欢迎礼包的4项内容，与参考事实一致。

---

### Q116: How are ZX Bank branches distributed in Nagpur?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在那格浦尔的分行分布：North（2家）、South（2家）、East（1家）、West（2家）和 Central Nagpur（1家），共计8家分行。
**Source:** branches-in-nagpur.md
**Evidence:** 文件列出了五个区域的分行详细信息。

#### CSV 参考答案
**Answer:** Nagpur is a key urban and commercial hub in central India. ZX Bank has strategically established its branch network across the city, with branches distributed across different regions.
**Reference File:** Branches in Nagpur.md
**Reference Content:** 描述 Nagpur 的分行网络分布。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了8家分行及五个区域的详细分布，与参考事实一致。

---

### Q117: Where are ZX Bank ATMs located in Mumbai (tech parks)?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买科技园的 ATM 位置包括：(1) Mindspace Airoli IT Park；(2) Nesco IT Park, Goregaon East；(3) Infinity IT Park, Malad West。
**Source:** atm-locations-at-tech-parks-in-major-indian-cities.md
**Evidence:** 文件 Mumbai 部分列出了3个科技园的 ATM 位置。

#### CSV 参考答案
**Answer:** CSV 中未找到该问题的精确匹配条目。
**Reference File:** N/A
**Reference Content:** N/A

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ❓ Not Found（无法验证）
**Satisfaction:** ⭐⭐⭐ (3/5)
**Evaluation:** kb-pilot 的答案列出了3个科技园的 ATM 位置，但 CSV 和 R1.json 中都未找到该问题的精确匹配条目，无法直接验证。

---

### Q118: Where are the ZX Bank ATMs located in Colombo?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在科伦坡的 ATM 位置包括：(1) Main Branch ATM - 100 Galle Road, Colombo 03；(2) Borella Branch ATM - 45 Baseline Road, Borella, Colombo 08；(3) Pettah ATM - 77 Main Street, Pettah, Colombo 11。
**Source:** atm-locations-in-sri-lanka.md
**Evidence:** 文件 Colombo 部分列出了3个 ATM 位置。

#### CSV 参考答案
**Answer:** ZX Bank - Main Branch ATM: 100 Galle Road, Colombo 03; ZX Bank - Borella Branch ATM: 45 Baseline Road, Borella, Colombo 08; ZX Bank - Pettah ATM: 77 Main Street, Pettah, Colombo 11.
**Reference File:** ATM Locations in Sri Lanka.md
**Reference Content:** 列出 Colombo 的3个 ATM 位置。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确列出了 Colombo 的3个 ATM 位置及详细地址，与参考事实一致。

---

### Q119: What are the key features of the ZX Bank house loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 住房贷款的关键特点：有竞争力的利率、灵活还款期限最长30年、快速审批、贷款金额最高为房产价值的90%、零提前还款费用、贷款金额 ₹5 万至 ₹10 千万、固定/浮动利率选择、可追加贷款、支持余额转划。申请人包括工薪族、自雇人士和 NRI。
**Source:** zx-bank-house-loan.md
**Evidence:** 文件列出了 Key Features 表格和 Special Benefits。

#### CSV 参考答案
**Answer:** Key features: eligibility for salaried, self-employed, and NRIs, loan amount ₹5 lakhs to ₹10 crores, tenure up to 30 years, starting processing fee at 0.25%, fixed or floating interest rates, top-up loans, balance transfer.
**Reference File:** ZX Bank House Loan.md
**Reference Content:** 列出住房贷款的关键特点。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了住房贷款的特点，与参考事实一致。

---

### Q120: What is the branch network of ZX Bank in Hyderabad?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在海得拉巴拥有31家分行，分布在 North（6家）、South（5家）、East（6家）、West（6家）和 Central Hyderabad（7家）。
**Source:** hyderabad-branch-network.md
**Evidence:** 文件列出了五个区域共31家分行。

#### CSV 参考答案
**Answer:** ZX Bank boasts a robust and strategically distributed branch network throughout Hyderabad, with convenient locations across North, South, East, West, and Central Hyderabad.
**Reference File:** Hyderabad Branch Network.md
**Reference Content:** 描述 Hyderabad 的分行网络。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了31家分行及五个区域的详细分布，与参考事实一致。

---

### Q121: What is the main purpose of ZX Bank's Agriculture Loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 农业贷款的主要目的是支持农民和农业企业，包括作物生产、设备采购、灌溉解决方案、奶业及相关活动，旨在通过灵活的条款和低利率促进农村繁荣。
**Source:** agriculture-loan.md
**Evidence:** 文件说明 "Designed to support crop production, equipment purchase, irrigation solutions, dairy, and allied activities"。

#### CSV 参考答案
**Answer:** ZX Bank offers specialized Agriculture Loans to empower farmers and agribusinesses across South Asia. Designed to support crop production, equipment purchase, irrigation solutions, dairy, and allied activities, aiming to fuel rural prosperity with flexible terms and low interest rates.
**Reference File:** Agriculture Loan.md
**Reference Content:** 描述农业贷款的主要目的。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案准确描述了农业贷款的主要目的，与参考事实一致。

---

### Q122: What are the key features of ZX Bank Agriculture Loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 农业贷款的关键特点：灵活贷款金额 ₹25,000 至 ₹50 万卢比、有竞争力的利率、灵活还款（季节性 EMI 或一次性还款）、快速放款、无提前还款罚金、抵押选项、女性农民特别计划（额外1%利率折扣）。
**Source:** zx-bank-agriculture-loan.md
**Evidence:** 文件列出了7项 Key Features。

#### CSV 参考答案
**Answer:** Flexible Loan Amounts (₹25,000 to ₹50 lakhs), Attractive Interest Rates, Flexible Repayment (Seasonal EMI or bullet repayment), Quick Disbursement, No Prepayment Penalty, Collateral Options, Women Farmer Scheme (extra 1% discount).
**Reference File:** Agriculture Loan.md
**Reference Content:** 列出农业贷款的7项关键特点。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案完整列出了农业贷款的7项关键特点，与参考事实一致。

---

### Q123: Where can I find ZX Bank ATMs located at petrol pumps in Mumbai?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在孟买加油站设有10个 ATM 位置：Indian Oil (BKC, Worli, Colaba)、HPCL (Cuffe Parade, Sion Circle, Chembur, Dadar)、BPCL (Andheri West, Powai, Borivali East)。
**Source:** atm-locations-at-major-petrol-pumps.md
**Evidence:** 文件 Mumbai 部分列出了10个加油站的 ATM 位置。

#### CSV 参考答案
**Answer:** 1. Indian Oil, Bandra Kurla Complex; 2. HPCL, Cuffe Parade; 3. BPCL, Andheri West; 4. Indian Oil, Worli; 5. HPCL, Sion Circle; 6. BPCL, Powai; 7. HPCL, Chembur; 8. Indian Oil, Colaba; 9. BPCL, Borivali East; 10. HPCL, Dadar.
**Reference File:** ATM Locations at Major Petrol Pumps.md
**Reference Content:** 列出10个加油站的 ATM 位置。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确列出了10个加油站的 ATM 位置，与参考事实一致。

---

### Q124: What is the branch network of ZX Bank in Ludhiana?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在卢迪亚纳拥有13家分行，分布在 North（3家）、South（3家）、East（2家）、West（3家）和 Central Ludhiana（2家）。
**Source:** network-in-ludhiana.md
**Evidence:** 文件说明 "13 strategically located branches"。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. strengthens financial inclusion in Ludhiana through its well-distributed branch network. With 13 strategically located branches, the bank caters to both residential and commercial customers.
**Reference File:** Network in Ludhiana.md
**Reference Content:** 描述 Ludhiana 的13家分行网络。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了13家分行及五个区域的详细分布，与参考事实一致。

---

### Q125: What are the main features and benefits of ZX Bank's car loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 汽车贷款的主要特点和福利：贷款金额最高 ₹80 万卢比、期限12至84个月、利率从8.25%起、48小时内快速放款、灵活还款 EMI、支持新车/二手车/电动车、无隐藏费用、预批准优惠。资格：工薪族年龄21-60岁/月收入最低 ₹20,000，自雇人士21-65岁/企业存续至少2年。
**Source:** zx-bank-car-loan.md
**Evidence:** 文件列出了 Features & Benefits、Eligibility 等详细信息。

#### CSV 参考答案
**Answer:** Loan Amount up to ₹80 lakhs, Tenure 12 to 84 months, Interest Rate starting from 8.25% p.a., Quick Disbursal within 48 hours, Flexible Repayment EMI, All Vehicle Types (New, Used, EV), No Hidden Charges, Pre-approved Offers.
**Reference File:** ZX Bank Car Loan.md
**Reference Content:** 列出汽车贷款的主要特点和福利。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了汽车贷款的特点、福利和资格要求，与参考事实一致。

---

### Q126: What are the key features of the ZX Bank Bike Loan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 摩托车贷款的关键特点：利率从9.49%起、贷款金额最高为上路价格的100%、灵活还款期限12至48个月、最快24小时放款、最少文件要求、无隐藏费用、两轮车最高 ₹2 万卢比、10分钟 e-KYC、12期 EMI 后零提前还款费用、女性和农村借款人享受特别利率。
**Source:** zx-bank-bike-loan.md
**Evidence:** 文件列出了 "Key Features" 的详细信息。

#### CSV 参考答案
**Answer:** Up to ₹2 Lakhs for two-wheelers, 10-minute e-KYC and instant eligibility check, Zero Prepayment Charges after 12 EMIs, Special Interest Rate for women applicants and rural borrowers.
**Reference File:** ZX Bank Bike Loan.md
**Reference Content:** 列出摩托车贷款的关键特点。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了摩托车贷款的关键特点，包含比 CSV 参考事实更丰富的细节。

---

### Q127: What is the branch network of ZX Bank in Bhutan?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在不丹拥有8家分行，分布在 Thimphu Region（2家）、Paro Region（2家）、Punakha Region（1家）、Phuentsholing Region（2家）和 Gelephu Region（1家）。此外还有15个 ATM 网点。
**Source:** branch-network-in-bhutan.md 和 bank-atms-in-bhutan.md
**Evidence:** 列出8家分行和15个 ATM 网点。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. has established a robust and accessible banking infrastructure across Bhutan, supporting both urban and semi-urban communities. The branch network ensures customers in key regions have convenient access.
**Reference File:** Branch Network in Bhutan.md
**Reference Content:** 描述 Bhutan 的分行网络。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了8家分行及五个区域的详细分布，并补充了 ATM 信息，与参考事实一致。

---

### Q128: What is the purpose of ZX Bank's ATM locations at restaurants?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在知名餐厅设置 ATM 的目的是为食客、游客和城市居民提供便捷的银行服务和现金取款。这些 ATM 位于高流量餐厅附近，确保人们在用餐时方便地获取现金和进行银行交易。
**Source:** atms-at-famous-restaurants.md
**Evidence:** 文件说明 "This list is ideal for travelers, foodies, and city-dwellers who love to dine out and need quick banking and cash withdrawal access."

#### CSV 参考答案
**Answer:** Below is a list of ZX Bank ATMs conveniently located at or near popular, high-traffic restaurants in each major city. This list is ideal for travelers, foodies, and city-dwellers who love to dine out and need quick banking and cash withdrawal access.
**Reference File:** ATMs at Famous Restaurants.md
**Reference Content:** 描述餐厅 ATM 的目的。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案正确描述了餐厅 ATM 的目的，与参考事实一致。

---

### Q129: What is the history of ZX Bank Ltd.?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank Ltd. 成立于1998年，总部位于印度孟买，是一家私营部门商业银行，在印度、斯里兰卡、孟加拉国、不丹和尼泊尔开展业务。SWIFT 代码 ZXININBB，CEO 为 Anjali Deshmukh。印度560+分行和1,200+ ATM，斯里兰卡32家分行，孟加拉国18家分行，不丹8家分行，尼泊尔20家分行。
**Source:** about-zx-bank-ltd.md
**Evidence:** 文件信息包括 "Founded: 1998", "Headquarters: Mumbai, Maharashtra, India"。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. is headquartered in Mumbai, Maharashtra, India, and was founded in 1998. It operates as a private sector commercial bank with a strong focus on retail, corporate, and digital banking services.
**Reference File:** About ZX Bank Ltd.md
**Reference Content:** 描述 ZX Bank 的基本信息。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了 ZX Bank 的历史、总部、业务范围和网络覆盖，比 CSV 参考事实更详细。

---

### Q130: What should you do before closing an account at ZX Bank?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** 根据信用卡关闭流程，关闭账户前应：(1) 结清所有未结欠款；(2) 兑换未使用的奖励积分；(3) 取消自动借记和关联支付。对于储蓄账户和活期账户的关闭，文档未提供具体步骤，建议联系银行客服。
**Source:** zx-bank-credit-card-help.md
**Evidence:** 信用卡关闭文档列出了6个步骤，前3步为关闭前的准备工作。

#### CSV 参考答案
**Answer:** Please ensure all auto-debits/standing instructions are cancelled before closing your account. Charges may apply as per bank policy.
**Reference File:** Account Close Guide.md
**Reference Content:** 建议取消自动借记和常设指示。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ⚠️ Partially Correct
**Satisfaction:** ⭐⭐⭐ (3/5)
**Evaluation:** kb-pilot 的答案基于信用卡关闭流程给出了关闭账户前的准备步骤，但 CSV 参考事实来自 "Account Close Guide.md" 文件，内容更简洁。kb-pilot 的答案覆盖了取消自动借记这一关键点，但缺少了"可能产生费用"的提示。此外，kb-pilot 答案中关于储蓄/活期账户关闭的具体步骤不足。

---

### Q131: What is the branch network of ZX Bank in Central Lucknow?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在勒克瑙中部拥有5家分行：Hazratganj、Kaiserbagh、Aminabad、Lalbagh、Chowk。
**Source:** lucknow-branch-network.md
**Evidence:** 文件 Central Lucknow 部分列出了5家分行。

#### CSV 参考答案
**Answer:** ZX Bank's Central Lucknow branches include key locations such as Hazratganj, Vidhan Sabha Marg; Kaiserbagh, Near Court; Aminabad, Latouche Road; Lalbagh, M.G. Road; and Chowk, Near Jawahar Bhawan.
**Reference File:** Lucknow Branch Network.md
**Reference Content:** 列出 Central Lucknow 的5家分行。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案正确列出了 Central Lucknow 的5家分行，与参考事实一致。

---

### Q132: What features does the ZX Bank Asia mobile app offer for account management?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank Asia 移动应用提供12项账户管理功能：查看余额、交易历史、定期存款/贷款跟踪、资金转账、收款人管理、账单支付、卡管理、贷款管理、奖励积分、NRI 和财富管理、AI 聊天机器人 Zia、请求支票簿和定位分行/ATM。
**Source:** zx-bank-asia-mobile-app-guide.md
**Evidence:** 文件列出了 App Features 的详细分类。

#### CSV 参考答案
**Answer:** Account Management: Check savings/current account balances, View transaction history and mini statements, Track FD, RD, and loan details in real-time.
**Reference File:** ZX Bank Asia Mobile App Guide.md
**Reference Content:** 列出账户管理功能。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面列出了12项账户管理功能，远比 CSV 参考事实详细。

---

### Q133: What are the features and benefits of ZX Bank Fixed Deposits?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 定期存款的特点和福利：有竞争力的利率、灵活期限7天到10年、安全有保障、可申请高达 FD 价值90%的透支或贷款、可提前支取、数字开户/续存/关闭、最低存款印度 ₹5,000、利息支付方式灵活、老年人特别利率、节税 FD、循环存款、联合存款和指定受益人、自动续存。
**Source:** zx-bank-fixed-deposits.md
**Evidence:** 文件列出了 "Features & Benefits" 的详细信息。

#### CSV 参考答案
**Answer:** Minimum Deposit: ₹5,000 (India), Interest Payout: monthly/quarterly/on maturity, Special Schemes: Senior citizen extra interest, tax-saver FDs, recurring deposit variant.
**Reference File:** ZX Bank Fixed Deposits.md
**Reference Content:** 列出定期存款的特点和福利。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了定期存款的特点和福利，包含比 CSV 参考事实更丰富的细节。

---

### Q134: What are the features of ZX Bank's bill payment services?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 账单支付服务的特色：支持多种账单类别（信用卡、手机、DTH、宽带、水电煤气、保险、教育、市政税等）、自动借记功能、一次性设置、安全支付（OTP、生物识别、设备认证）、覆盖400+账单方覆盖5个国家、实时跟踪、AI 助手 Zia 提供提醒和建议。
**Source:** bill-payments.md
**Evidence:** 文件列出了 Supported Bill Payment Categories、Auto Debit Feature 和 Key Features。

#### CSV 参考答案
**Answer:** ZX Bank aims to simplify your bill management experience with its robust Bill Payments and Auto Debit features. Key Features include: One-Time Setup, Secure Payments (OTP, biometric & device authentication), Coverage of 400+ billers across India, Sri Lanka, Bangladesh, Bhutan, Nepal, Real-Time Tracking, and AI Financial Assistant ("Zia").
**Reference File:** Bill Payments.md
**Reference Content:** 列出账单支付服务的关键特点。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案全面描述了账单支付服务的特点，与参考事实一致。

---

### Q135: What is ZX Bank's branch network like in Bhopal?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 在博帕尔拥有8家分行，分布在 North（2家）、South（2家）、East（1家）、West（1家）和 Central Bhopal（2家）。
**Source:** branch-network-in-bhopal.md
**Evidence:** 文件说明 "eight branches"。

#### CSV 参考答案
**Answer:** ZX Bank Ltd. maintains a strong presence in Bhopal, ensuring convenient access to its services across the city's diverse neighborhoods. With a carefully distributed network of eight branches throughout North, South, East, West, and Central Bhopal.
**Reference File:** Branch Network in Bhopal.md
**Reference Content:** 描述 Bhopal 的8家分行网络。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐⭐ (5/5)
**Evaluation:** kb-pilot 答案提供了8家分行及五个区域的详细分布，与参考事实一致。

---

### Q136: What services do ZX Bank branches in Bhopal offer?
**Query Type:** Descriptive

#### kb-pilot 答案
**Answer:** ZX Bank 博帕尔分行提供全面的零售、企业和数字银行解决方案，包括储蓄和活期账户、个人和住房贷款、信用卡、定期存款、数字银行服务（移动应用、NetBanking、UPI）、汇款服务、财富管理和投资咨询等。
**Source:** branch-network-in-bhopal.md
**Evidence:** 文件说明 "Each branch is equipped to offer comprehensive retail, corporate, and digital banking solutions tailored to local needs."

#### CSV 参考答案
**Answer:** Each branch is equipped to offer comprehensive retail, corporate, and digital banking solutions tailored to local needs.
**Reference File:** Branch Network in Bhopal.md
**Reference Content:** 描述 Bhopal 分行提供的服务。

#### RAG 评估指标
**Recall@k:** N/A | **Precision@k:** N/A | **MRR:** N/A | **NDCG@k:** N/A

#### 对比评估
**Correctness:** ✅ Correct
**Satisfaction:** ⭐⭐⭐⭐ (4/5)
**Evaluation:** kb-pilot 答案详细列举了 Bhopal 分行提供的具体服务类型，比 CSV 参考事实更详细。答案正确。

---

## 总结

### 整体统计

| 评估项目 | 数量 | 占比 |
|---------|------|------|
| 总问题数 | 82 | 100% |
| ✅ Correct（正确） | 72 | 87.8% |
| ⚠️ Partially Correct（部分正确） | 2 | 2.4% |
| ❌ Incorrect（错误） | 1 | 1.2% |
| ❓ Not Found（无法验证） | 4 | 4.9% |
| 待确认（Q74 分行vs ATM 问题） | 3 | 3.7% |

### 关键发现

1. **总体准确率很高**：87.8% 的问题回答完全正确，2.4% 部分正确，仅 1.2% 错误。

2. **严重问题 - Q74 答非所问**：Q74 "Where are ZX Bank ATMs located in Mumbai?" 问的是 ATM 位置，但 kb-pilot 回答了分行网络信息。这是一个严重的语义理解错误。

3. **Q62 奖项遗漏**：CSV 参考事实缺少 Outstanding SME Bank - Sri Lanka (2023)，kb-pilot 答案反而更完整。

4. **Q130 信用卡 vs 账户关闭混淆**：kb-pilot 基于信用卡关闭流程回答账户关闭问题，两类场景不完全匹配。

5. **RAG 检索质量**：有 RAG 指标的问题中，Recall@k 平均为 0.97，大部分为 1.0，说明检索系统能有效召回相关文档。但部分问题的 Precision@k 较低（如 Q55、Q56、Q68、Q74、Q76、Q85、Q86、Q90、Q93、Q101），说明检索结果中混入了不相关文档。

6. **CSV 类型标注不一致**：部分问题在 CSV 中被标记为 Open-Ended 类型，但 kb-pilot 作为 Descriptive 处理，如 Q71、Q84、Q98、Q101、Q108、Q110、Q112、Q114、Q122、Q136。答案质量未受影响。

7. **Q59-Q61 参考数据缺失**：East/West/South Chennai 的分行数量问题在 CSV 和 R1.json 中均无独立条目，无法直接验证，但答案与间接参考数据一致。