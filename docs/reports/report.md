# ZX Bank 知识库问答评测报告

> 生成时间：2026-08-09
> 数据来源：`docs/reports/A1.txt` + `A2.txt`（kb-pilot 答案，共 192 题）；`Q1.txt`（基准问题与支撑材料）；`R1.txt`（RAG 检索切片）。

---

## 1. 总览

对 192 道已作答问题逐一以基准支撑事实（Q1 `Supporting Facts`）与 RAG 检索原文（R1 `relevant_snippets`）为金标准复核，每道题给出 0–100 评分，并判定 **✅ 通过 / ⚠️ 部分正确 / ❌ 未答**。

| 指标 | 数值 |
|------|------|
| 总题数 | 192 |
| ✅ 通过 | **161**（83.9%） |
| ⚠️ 部分正确 | 28（14.6%） |
| ❌ 未答 | 3（1.6%） |
| 平均分 | **84.6 / 100** |

### 结论

- 整体通过率 **83.9%**，平均 **84.6 分**，绝大多数答案有据可查、来源可追溯（答案均给出 `doc_xxx …… .md#L行号` 形式的可追踪引用）。
- 仅 **3 题**（A18、B15、C23）答成 “文档未提及”但基准材料实际包含该内容，属于漏答；大部分“未提及”回答（P 系 10 题、T 系 5 题）经核对**确为知识库未收录**，属诚实作答、不算错。
- 主要扣分点是**计数误差**（部分列表题把开头统计数字写错）与 **问题改写导致的对不上**（约 30 题因问法改写未匹配到基准题，按引用自行核验，分数略保守）。

---

## 2. 分类汇总

| 分类 | 代码 | 题数 | ✅ | ⚠️ | ❌ | 平均分 | 通过率 |
|------|------|----:|--:|--:|--:|-------:|-------:|
| Analytical（分析型） | A | 30 | 28 | 1 | 1 | 90.7 | 93% |
| Boolean（判断型/是非） | B | 30 | 28 | 1 | 1 | 86.0 | 93% |
| Comparative（比较型） | C | 30 | 28 | 1 | 1 | 86.5 | 93% |
| Descriptive（描述型） | D | 50 | 48 | 2 | 0 | 86.8 | 96% |
| Procedural（流程/步骤型） | P | 38 | 17 | 21 | 0 | 74.2 | 45% |
| Temporal（时间型） | T | 9 | 9 | 0 | 0 | 87.2 | 100% |
| Open-Ended（开放型） | O | 5 | 3 | 2 | 0 | 80.2 | 60% |

**分类分析：**
- **Analytical / 分析型（A）**：推理解释类，答案逻辑清晰、引用精确，仅 A30 出现统计总人数与分行数不一致（7 vs 列表为 8）。
- **Boolean / 判断型（B）**：是非判断准确率高；B15 唯一硬伤——基准 `Account Close Guide.md` 明确“储蓄账户须到行验证”，答案却答“未提及”。
- **Comparative / 比较型（C）**：对比类答案详尽（长答复），字段级核对基本正确；C23 误判传统线下支付“文档未描述”。
- **描述型（D）**：50 题全通过/部分，无硬伤；部分题目简介里的个数与明细条目不一致（如 D11 “18 城”实列 17；D32 “九城”实列 8）。
- **流程型 / 步骤型（P）**：本类最弱——约 10 题基准该有而知识库确实缺失（教育贷、KYC 更新、未成年人/子女开户、第三方开户、柜面存款、支票取现、语音注册等），答案诚实写作“未提及”；多题无基准匹配，按语义核验。
- **时间型（T）**：9 题全过；无日期的都如实指出文档无日期。
- **开放型（O）**：3 题有据可依少扣分；O4/O5 基准未匹配，无法强核。

---

## 3. 逐题明细

### Analytical（分析型）— A

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| A1 | Why was ZX Bank recognized for its digital initiatives in… | 100 | ✅ 通过 | Fully correct and supported: Best Digital Transformation Bank – South Asia (2023) by Asian Banking & Finance Mag, digital onboardi |
| A2 | Why might ZX Bank's 2023 recognition in Bangladesh differ… | 100 | ✅ 通过 | Correct comparison: South Asia award (digital transformation, tech-focused) vs Bangladesh award (financial inclusion in rural area |
| A3 | Why is digital banking important for ZX Bank's Business L… | 95 | ✅ 通过 | Correct: manage loan via ZX Bank Asia app/NetBanking and Zia eligibility/EMI checks match ref_facts. Minor: e-KYC/digital-app deta |
| A4 | Why might someone prefer using the ZX Bank mobile app to … | 95 | ✅ 通过 | Correct: anywhere-without-branch, biometric login, instant confirmation w/ delivery time, in-app tracking all match ref. Minor: ap |
| A5 | Why might ZX Bank Asia impose daily transaction limits on… | 100 | ✅ 通过 | All limits (₹1,00,000/txn, ₹1,00,000/day, 20 txns/day) and NPCI & ZX policy / risk-profile framing match ref_facts exactly. |
| A6 | Why might ZX Bank benefit from having a network in all ar… | 92 | ✅ 通过 | Matches ref (five areas, convenience for retail/corporate/digital). Specific sites (Sanjay Place, MG Road, Tajganj) plausible but  |
| A7 | Why are ZX Bank's branches strategically located in diffe… | 95 | ✅ 通过 | Matches ref_facts (residential/commercial/tech districts); tech-corridor and central-commercial examples plausible from the branch |
| A8 | Why might ZX Bank have chosen to distribute its branches … | 90 | ✅ 通过 | Core reason (financial inclusion/growth across the five regions) matches ref exactly. '18 branches' count is specific and unverifi |
| A9 | Why might women-led agri ventures choose ZX Bank? | 95 | ✅ 通过 | 1% extra discount for women-led ventures and flexible terms match ref; ₹25k–₹50L range confirmed in r1. Correct and well-supported |
| A10 | Why might ZX Bank choose to place an ATM in Gulshan, Dhaka? | 95 | ✅ 通过 | Gulshan strategic accessibility rationale matches ref; ATM address (Plot 12, Gulshan Avenue) consistent. Minor: matching-branch cl |
| A11 | Why might ZX Bank have chosen these specific regions for … | 95 | ✅ 通过 | Indore commercial/educational hub rationale matches ref; district examples (Rau, Vijay Nagar, Palasia) plausible from r1 snippets. |
| A12 | Why does ZX Bank Ltd. offer personal loans without collat… | 90 | ✅ 通过 | Zero-collateral accessibility rationale correct vs ref. Tenor 12–60 months confirmed in r1; the 13.50%–21.00% regional rate spread |
| A13 | Why might ZX Bank have chosen to distribute its branches … | 88 | ✅ 通过 | ref matched the Bangladesh doc (mismatch); answer coherently argues Lucknow five-region coverage with plausible specifics. 22-bran |
| A14 | Why is it important to act quickly when reporting a fraud… | 95 | ✅ 通过 | Follow promptness -> minimise-risk rationale matches ref. Block/freeze, evidence, ref-number details plausible; 'resolution within |
| A15 | Why does ZX Bank employ AI in its security measures? | 95 | ✅ 通过 | Real-time monitoring + immediate alerts match ref. Zia 24/7-assistant facet plausible from Safety Features context though not in r |
| A16 | Why might customers prefer using the PRM Assistant Program? | 88 | ✅ 通过 | ref anchored to ASK Zia (match 0.55) rather than PRM program; answer answers the PRM question coherently with well-cited details.  |
| A17 | Why might ZX Bank consider Phuentsholing an important loc… | 90 | ✅ 通过 | Matches ref (key region designation, strategic for retail/digital/remittance). Two-branch count and Shopping Complex/RSTA location |
| A18 | Why might ZX Bank choose to locate ATMs in major movie th… | 35 | ❌ 未答 | Says 'not mentioned in documents' but ref_facts give the rationale (high foot traffic, cash needs for concessions, brand presence) |
| A19 | Why might ZX Bank focus on Ludhiana for its branch network? | 90 | ✅ 通过 | Ludhiana commercial-hub + financial-inclusion rationale matches ref exactly. 13-branch count unverified. (r1 is misaligned to Visa |
| A20 | Why might ZX Bank have chosen to expand across all major … | 90 | ✅ 通过 | Kolkata cultural/financial hub and five-region distribution match ref. 15-branch count and street examples (Park Street) unverifie |
| A21 | Why might ZX Bank focus on green finance projects in Bhut… | 95 | ✅ 通过 | CSPR/ESG green finance (Bhutan hydropower, Nepal solar) matches ref. Award mention is a bonus consistent with the bank's recogniti |
| A22 | Why might corporate customers get higher NetBanking trans… | 95 | ✅ 通过 | Higher limits for corporate/priority via branch/support subject to approval+enhanced security matches ref exactly. Per-day limit f |
| A23 | Why might customers choose ZX Bank's Fixed Deposits? | 95 | ✅ 通过 | Comprehensive list matches 'Why Choose' ref (rates, tenures 7 days–10 yrs, loan vs FD 90%, premature withdrawal, digital opening). |
| A24 | Why ZX Bank places ATMs at tech parks? | 90 | ✅ 通过 | Honest: doc is a directory and ref_facts likewise give no rationale; answer accurately states absence without fabricating a reason |
| A25 | Why ZX Bank placed ATMs near beach roads? | 95 | ✅ 通过 | Internal logic matches ref (beach-prominence criterion, skipping non-beach cities). Four-city list and per-city counts corroborate |
| A26 | Why ZX Bank chooses major bus stands for ATM placement? | 90 | ✅ 通过 | no-reference-match. Coherent, cites source line, and quotes the doc's stated rationale (commuter cash access at bus stands); plaus |
| A27 | Why ZX Bank evenly distributes branches across Patna? | 90 | ✅ 通过 | Matches ref (even distribution for comprehensive access). Region breakdown sums consistently to 13 (3+3+2+3+2); count itself unver |
| A28 | Why ZX Bank built a strong presence in Mumbai? | 90 | ✅ 通过 | Mumbai economic-powerhouse + all-region coverage matches ref. 34-branch count unverified. |
| A29 | Why ZX Bank distributes branches across all zones of Hyde… | 90 | ✅ 通过 | Matches ref (diverse growing population, financial inclusion in urban hub). Breakdown sums to 30 (6+5+6+6+7); counts internally co |
| A30 | Why ZX Bank spreads branches across all regions of Nagpur? | 78 | ⚠️ 部分 | Count error: claims 'Seven branches' while listing North 2, South 2, East 1, West 2, Central 1 = 8 total; matches ref on five-regi |

---

### Boolean（判断型/是非）— B

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| B1 | Is ZX Bank involved in green financing initiatives? | 90 | ✅ 通过 | Yes correct: ref confirms green financing (Bhutan hydropower/Nepal solar). Extra literacy/women-loan detail is supported by About  |
| B2 | Does ZX Bank offer loans specifically for women entrepren… | 90 | ✅ 通过 | Yes correct: Women Empowerment Loans per ref and retrieval. |
| B3 | Can I convert my savings account to salary account online? | 90 | ✅ 通过 | Yes correct: ref confirms conversion via app/NetBanking if employer registered and KYC current; conditions echoed accurately. |
| B4 | Does ZX Bank use biometric login for security? | 90 | ✅ 通过 | Yes correct: biometric login via fingerprint/facial recognition confirmed by ref. |
| B5 | Can you report fraud through the ZX Bank app? | 90 | ✅ 通过 | Yes correct: ref confirms Support > Report Fraud in app; extra card-blocking detail is accurate. |
| B6 | Does ZX Bank offer a discount for women farmers? | 90 | ✅ 通过 | Yes correct: ref confirms extra 1% interest discount for women-led agri ventures. |
| B7 | Is there a ZX Bank ATM in Jessore? | 90 | ✅ 通过 | Yes correct: ref confirms Jessore ATM at 13 Monihar More, Jessore-7400. (r1 retrieval empty but answer grounded in ref.) |
| B8 | Does ZX Bank have an ATM at AIIMS in Delhi? | 90 | ✅ 通过 | Yes correct: ref confirms AIIMS ATM in Delhi. |
| B9 | Does ZX Bank have a branch in Khulna? | 60 | ⚠️ 部分 | ref_facts/retrieval are about a Howrah branch (---reuses B16 fact), not Khulna; Khulna claim is specific but unverifiable from pro |
| B10 | Does ZX Bank have an ATM in Galle? | 90 | ✅ 通过 | Yes correct: ref confirms Galle Fort ATM at 15 Pedlar Street. |
| B11 | Does ZX Bank require collateral for personal loans? | 90 | ✅ 通过 | No (not required) correct: ref confirms Zero Collateral, no security/guarantor. |
| B12 | Does ZX Bank offer loans to NRIs under house loan scheme? | 90 | ✅ 通过 | Yes correct: ref confirms house loans for NRIs with relationship manager and online app. |
| B13 | Is there a GST Road branch in South Chennai? | 90 | ✅ 通过 | Yes correct: ref confirms two GST Road branches in South Chennai (Tambaram, Chromepet). |
| B14 | Can digital FD be opened via mobile app across all countr… | 80 | ✅ 通过 | no_ref_match; claim plausible and well-cited (FD booking table marks all 5 countries digital, traveling Mobile App flow). |
| B15 | Can I close my ZX Bank savings account online? | 15 | ❌ 未答 | Said 'not mentioned in documents' but ref_facts has Account Close Guide.md stating in-branch verification required for savings-acc |
| B16 | Does ZX Bank have a branch in Howrah? | 90 | ✅ 通过 | Yes correct: ref confirms Howrah branch at 43 Andul Road (IFSC ZXIN0002302). |
| B17 | Does ZX Bank have a branch in Gachibowli area of Hyderabad? | 90 | ✅ 通过 | Yes correct: ref confirms Gachibowli branch, IFSC ZXIN0001231. |
| B18 | Can individual farmers apply for ZX Bank Agriculture Loan? | 90 | ✅ 通过 | Yes correct: ref confirms individual farmers eligible under Who Can Apply. |
| B19 | Is there a ZX Bank ATM at Esplanade Bus Stand in Kolkata? | 90 | ✅ 通过 | Yes correct: ref confirms Esplanade Bus Stand ATM in Kolkata. |
| B20 | Does ZX Bank offer zero initial deposit current account? | 90 | ✅ 通过 | Yes correct: ref confirms Zero Initial Deposit current account, subject to eligibility. |
| B21 | Does ZX Bank have branches in Northern Province of Sri La… | 90 | ✅ 通过 | Yes correct: ref confirms Northern Province branches (Jaffna, Kilinochchi, Vavuniya, etc.). |
| B22 | Does ZX Bank provide digital banking at all branches? | 90 | ✅ 通过 | Yes correct: ref confirms each branch delivers full retail/corporate/digital banking suite. |
| B23 | Does ZX Bank have a branch in South Bhopal? | 90 | ✅ 通过 | Yes correct: ref confirms two South Bhopal branches (Malviya Nagar, Kolar Road). |
| B24 | Does ZX Bank reactivate closed credit cards? | 85 | ✅ 通过 | no_ref_match; confident No with direct quote ('cannot re-activate a closed card; new application required') and citation to closur |
| B25 | Is there an annual fee waiver for first two years on ZX S… | 90 | ✅ 通过 | Yes correct: ref confirms no annual fee for first 2 years; ₹199+GST from year three. Extra fee detail accurate. |
| B26 | Are ZX Bank ATMs available in Hyderabad shopping malls? | 90 | ✅ 通过 | Yes correct: ref confirms Forum Sujana, GVK One, Inorbit malls in Hyderabad. |
| B27 | Does ZX Bank have a branch in Naubasta, West Kanpur? | 90 | ✅ 通过 | Yes correct: ref confirms 19 Naubasta, Naubasta W Kanpur branch (ZXIN0004004). |
| B28 | Do I need to hold a ZX account to open a locker? | 90 | ✅ 通过 | Yes correct: ref confirms locker requires savings/current account and updated KYC. |
| B29 | Is ZX Bank CEO a woman? | 90 | ✅ 通过 | Yes correct: ref confirms CEO Anjali Deshmukh is a woman. |
| B30 | Does ZX Bank offer zero prepayment charges on bike loan a… | 90 | ✅ 通过 | Yes correct: ref confirms Zero Prepayment Charges after 12 EMIs on bike loan. |

---

### Comparative（比较型）— C

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| C1 | How does ZX Bank's 2023 recognition in Bangladesh differ … | 92 | ✅ 通过 | Correctly contrasts Bangladesh Financial Inclusion award (rural/underserved, digital banking/microfinance/literacy) vs South Asia  |
| C2 | How do ZX Bank's Business Loans cater to different custom… | 88 | ✅ 通过 | Six segment-to-product mappings (SME, Working Capital, Term, Trade Finance, Women Empowerment, Green/Sustainability) match r1 snip |
| C3 | How is converting to a salary account different from a re… | 90 | ✅ 通过 | Process (employer tie-up, docs, branch/app) and post-conversion differences (zero balance vs ₹5,000/LKR 3,000, ₹1,000 senior) full |
| C4 | How does ZX Bank's salary account differ from savings acc… | 88 | ✅ 通过 | Compares doc_054 salary account vs doc_055 savings with verified differences (zero-balance, auto-sweep FD, preferential rates vs U |
| C5 | How does ZX Bank's fraud reporting process differ between… | 90 | ✅ 通过 | Distinguishes in-branch written complaint vs online channels (app, NetBanking, email fraudreport@zxbank.asia, hotline, card blocki |
| C6 | How does ZX Bank's approach to phishing protection compar… | 88 | ✅ 通过 | Compares reactive app patching vs proactive phishing detection/education as complementary layers; matches ref_facts wording on vul |
| C7 | How East Agra branches differ from West Agra branches? | 95 | ✅ 通过 | East 3 vs West 4 branches with all addresses, IFSC codes (ZXIN0003041-43 vs 0004041-44), and phone numbers exactly matching ref_fa |
| C8 | How South Bangalore branch locations differ from those in… | 93 | ✅ 通过 | South 8 vs West 7 branches, full IFSC series ZXIN0002201-08 vs 0004201-07; area character (residential/tech vs industrial) matches |
| C9 | How ZX Bank's India presence compares with Sri Lanka netw… | 92 | ✅ 通过 | India 560+ branches/1,200+ ATMs vs Sri Lanka 32/40 matches ref_facts; province breakdown (8+7+6+6+5=32) verified; notes Mumbai HQ  |
| C10 | How East Coimbatore branches differ from West Coimbatore … | 95 | ✅ 通过 | East 2 vs West 3 branches with all addresses and IFSC codes (ZXIN0001441-42 vs 0001451-53) exactly matching ref_facts. |
| C11 | How North Jaipur branches compare with West Jaipur in qua… | 85 | ✅ 通过 | No ground truth (has_ref false); answer states 5 branches each with IFSC series 0001201-05 vs 0001501-05 and location lists, suppo |
| C12 | How bike loan interest rates compare with other ZX loan p… | 85 | ✅ 通过 | Bike loan 9.49% verified vs ref_facts; comparative table (car 8.25%, personal 11.75-19.99%, gold 9.5%, house/ag no numeric) from c |
| C13 | How Chennai beach ATMs compare in number with Visakhapatn… | 90 | ✅ 通过 | Correctly finds 7 ATMs each; both beach lists match ref_facts exactly; concludes no numerical difference. |
| C14 | How North Ahmedabad branches differ from Central Ahmedaba… | 95 | ✅ 通过 | 3 branches each; North (Naranpura/Chandlodia/Ranip, 0001011-13) vs Central (Navrangpura/Lal Darwaza/Ashram Road, 0001051-53) match |
| C15 | How West Surat branches differ from South Surat branches? | 88 | ✅ 通过 | ref_mismatch: ref_query/facts concern North vs South Patna, unrelated to Surat question. Judged on Surat cites: 3 branches each, W |
| C16 | How North Kolkata branches differ from Central Kolkata br… | 95 | ✅ 通过 | North 4 vs Central 3 branches with addresses, IFSC (ZXIN0002001-04 vs 0002401-03), and phones exactly matching ref_facts tables. |
| C17 | How number of ZX ATMs in Colombo compares to Kandy ATMs i… | 95 | ✅ 通过 | Colombo 3 (Main/Borella/Pettah) vs Kandy 2 (City Centre/Peradeniya) matches ref_facts; addresses provided. |
| C18 | How ZX Bank's house loan differs from other banks' house … | 85 | ✅ 通过 | Honestly states KB provides no ZX-vs-other-bank comparison; accurately lists ZX house-loan features (30 yr, 90% LTV, zero prepayme |
| C19 | How salaried personal loan rates differ from self-employe… | 90 | ✅ 通过 | Salaried 11.75-17.99% vs self-employed 13.25-19.99% matches ref_facts; correctly computes 1.50pp/2.00pp gaps; extra BBN band flagg |
| C20 | How Delhi railway station ATMs differ from Bangalore rail… | 85 | ✅ 通过 | No ground truth; Delhi 4 stations (NDLS/NZM/DLI/Anand Vihar) vs Bangalore 2 (SBC/Yeshwanthpur), plus 1 airport ATM each; supported |
| C21 | How ZX ATMs in Kathmandu compare with Pokhara ATMs in Nepal? | 85 | ✅ 通过 | No ground truth; Kathmandu 3 (Thamel/Patan/Baneshwor) vs Pokhara 2 (Lakeside/Mahendrapul) with addresses from cited doc_040; coher |
| C22 | How ZX Fixed Deposit differs from regular savings account? | 88 | ✅ 通过 | FD vs savings contrast correct (7d-10yr, 3.50-6.30%, senior slab, ₹5,000 min, 90% OD vs daily-balance savings, min balance tiers); |
| C23 | How ZX bill payment security differs from traditional off… | 18 | ❌ 未答 | Answer claims traditional offline payments 'are not described in the documents' and no comparison exists, but ref_facts explicitly |
| C24 | How college ATMs in Chennai compare with Bangalore colleg… | 88 | ✅ 通过 | ref_mismatch: ref_query/facts/r1 concern beach ATMs, not college ATMs. Judged on doc_015 cites: 2 each (IIT Madras+Loyola vs IISc+ |
| C25 | How Hyderabad tech park ATMs compare with Coimbatore tech… | 85 | ✅ 通过 | No ground truth; 3 tech-park ATMs each (HITEC/Raheja/Cyber Pearl vs TIDEL/SPC/KCT) with addresses from cited doc_012; location-vs- |
| C26 | How restaurant ATMs in Hyderabad differ from Ludhiana or … | 88 | ✅ 通过 | 12 restaurant ATMs each with full lists; ref_facts confirm first entries (Paradise/Bawarchi; Bistro 226/Barbeque Nation); notes no |
| C27 | How number of branches in Central Pune compares to West P… | 95 | ✅ 通过 | 8 branches each; full Central list (0001601-08, Shivaji Nagar/Deccan/Sadashiv Peth etc.) and West list (0001501-08, Aundh/Baner/Hi |
| C28 | How NetBanking self-registration differs from branch acti… | 85 | ✅ 通过 | No ground truth; contrasts online self-registration (OTP, self-set credentials) vs branch activation (form, welcome kit/activation |
| C29 | How undergraduate tuition differs from graduate tuition a… | 75 | ⚠️ 部分 | No ground truth to verify; answer honestly reports KB has no undergrad vs grad tuition data, citing only cross-border tuition-paym |
| C30 | How North Ludhiana branches compare with West Ludhiana br… | 85 | ✅ 通过 | Partial ref mismatch (ref_query West vs East; question North vs West). West Ludhiana branches (Aggar Nagar/Sukhdev/Atam Park) exac |

---

### Descriptive（描述型）— D

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| D1 | What awards did ZX Bank Ltd. win in 2023? | 90 | ✅ 通过 | All 4 ref-fact awards (Digital Transformation, Financial Inclusion, Women's Banking, NRI Services) correctly named with awarding b |
| D2 | What are the different ways to apply for a cheque book at… | 92 | ✅ 通过 | All 5 application channels (Mobile App, NetBanking, Branch, ATM, Customer Care) match ref facts exactly, plus accurate FAQ details |
| D3 | What is UPI and how does ZX Bank Asia support it? | 90 | ✅ 通过 | Correctly defines UPI (real-time, 24x7, VPA/QR) and cites India-only availability, activation steps, and limits. All verified agai |
| D4 | What services does ZX Bank offer in Agra? | 85 | ✅ 通过 | Enumerates 17 branches across 5 Agra zones consistent with the branch tables; grounded in correct doc. Entries plausible per citat |
| D5 | What is the branch network of ZX Bank in Bangalore? | 85 | ✅ 通过 | Lists 37 Bangalore branches (8/8/8/7/6) with IFSC ranges across N/S/E/W/C zones matching the source structure; lengthy but consist |
| D6 | What is the branch network of ZX Bank Ltd. in Sri Lanka? | 90 | ✅ 通过 | 32 branches confirmed by ref fact; sum of provinces (8+7+6+6+5) = 32 exact with IFSC ranges. Complete and correct. |
| D7 | What steps to block card or account at ZX Bank? | 88 | ✅ 通过 | Card/account blocking steps mirror ref fact (Card Management/Account Services, Block/Freeze, confirm) plus urgent Block Instantly  |
| D8 | What security features does ZX Bank offer against online … | 90 | ✅ 通过 | All 9 security features from ref facts covered (MFA, AI fraud, encryption, session timeout, limits, updates, education, alerts, re |
| D9 | What is the PRM Assistant Program at ZX Bank? | 90 | ✅ 通过 | PRM Assistant described fully: dedicated manager, services, support areas, free for all account holders, reach options. Matches re |
| D10 | What is ZX Bank's Agriculture Loan? | 88 | ✅ 通过 | Agriculture Loan features (₹25k-₹50L, repayment, women's 1% discount) match ref/snippets; who-can-apply, documents, channels also  |
| D11 | Where are the ZX Bank ATMs located in Bangladesh? | 78 | ⚠️ 部分 | 17 city locations with addresses listed, but intro claims '18 cities' (overcount) and addresses not fully verifiable from source;  |
| D12 | Where are ZX Bank ATMs located in Mumbai (hospital locati… | 80 | ✅ 通过 | ref_mismatch: ref facts/r1 are Tech Parks/Mumbai. Graded by the citation (doc ATM Locations at Major Hospitals): 2 Mumbai hospital |
| D13 | Where are ZX Bank ATMs located in Mumbai (beach roads)? | 85 | ✅ 通过 | ref_mismatch: ref facts are Tech Parks. Graded by citation (Beach Road ATMs doc): 7 beach-road Mumbai ATMs with addresses, consist |
| D14 | What are the available ZX Bank ATM locations in Chennai c… | 90 | ✅ 通过 | Both Chennai colleges (IITM, Loyola) match ref facts exactly with correct addresses. Complete. |
| D15 | What features does ZX Bank Savings Account have? | 92 | ✅ 通过 | All 9 savings account features from ref facts listed verbatim (interest, min balance, e-KYC, debit card, digital, UPI/QR, rewards, |
| D16 | What is included in the ZX Bank Savings Account Kit? | 92 | ✅ 通过 | All 5 Savings Account Kit items match ref facts (travel bag, 150-country adapter, EMV debit card, passbook/cheque book, user guide |
| D17 | What is the branch network of ZX Bank in Hyderabad? | 85 | ✅ 通过 | r1 query mismatched (Delhi) but citations point to Hyderabad doc. 30 branches (8/5/6/6/7) with IFSC ranges across 5 zones, consist |
| D18 | What is the branch network of ZX Bank in Bhutan? | 80 | ✅ 通过 | All 5 Bhutan regions covered with addresses/IFSC codes matching source; but intro says '7 branches' while 8 (2+2+1+2+1) are listed |
| D19 | What are the key features and benefits of ZX personal loan? | 88 | ✅ 通过 | Personal loan features (up to ₹30L, 12-60 months, zero collateral, part-payment/foreclosure) match ref facts exactly; rate bands a |
| D20 | What documents required for salaried applicants for ZX pe… | 90 | ✅ 通过 | All 7 salaried-applicant documents match ref facts exactly (form, photo ID, address proof, 3 salary slips, 6-mo statements, photo, |
| D21 | What are the key features of ZX Bank Gold Loan? | 86 | ✅ 通过 | 4 features from ref facts covered; additional figures (9.5% rate, 0.25%/₹250 fee, ₹50L max) supported by cited sections L15-31. Ac |
| D22 | What is the main purpose of ZX Bank Agriculture Loan? | 86 | ✅ 通过 | Main purpose correctly stated (empower farmers/agribusinesses, crop/equipment/irrigation/dairy) matching ref fact; extra features  |
| D23 | What key features are available on ZX Agriculture Loan? | 90 | ✅ 通过 | All 7 key features match ref facts exactly (amounts, repayment, disbursement, no penalty, collateral, women's schemes); categories |
| D24 | Where can I find ZX Bank ATMs at petrol pumps in Mumbai? | 95 | ✅ 通过 | All 10 Mumbai petrol-pump ATM locations match ref facts addresses exactly (IndianOil/HPCL/BPCL). Complete and fully correct. |
| D25 | What services ZX Bank provides at major bus stands across… | 82 | ✅ 通过 | Bus-stand ATM service correctly described; claims 120 ATMs/20 cities/6 per city (plausible from overview); Mumbai examples align w |
| D26 | What ZX ATMs are present at major tech parks across India… | 85 | ✅ 通过 | No ground truth (has_ref=false); graded by citations. 7 verified city park examples with correct addresses; 20 cities/3-per-city c |
| D27 | What ZX ATMs are located at major restaurants across Indi… | 82 | ✅ 通过 | No ground truth; graded by citation. 12 Mumbai restaurant ATMs with addresses from doc section; pattern for other cities inferred  |
| D28 | What is the branch network of ZX Bank in Ludhiana? | 88 | ✅ 通过 | 13 Ludhiana branches confirmed by ref facts; sum (3+3+2+3+2) = 13 with correct zone split and IFSC range for (001-341). Complete. |
| D29 | What is the branch network of ZX Bank in Surat? | 85 | ✅ 通过 | 18 Surat branches distributed as 4/3/4/3/4 (sum 18); West/South match the ref facts exactly, rest plausibly from doc. Solid. |
| D30 | What is the branch network of ZX Bank in Kolkata? | 80 | ✅ 通过 | Kolkata zones described (4+4+3+3+3) but intro says '15 branches' while 17 are listed and IFSC ranges (0002001-0002403) imply 17 -  |
| D31 | What is ASK Zia on ZX website? | 88 | ✅ 通过 | All website ASK Zia features from ref facts (instant answers, smart assistance, secure requests, comparisons, 24/7) plus security  |
| D32 | Where are ZX Bank ATMs located in Nepal? | 78 | ⚠️ 部分 | ref_mismatch (ref facts are Mumbai); graded by citations. Many Nepal ATM addresses listed but intro says 'nine cities' and 8 are g |
| D33 | Where are ZX Bank ATMs located in Colombo? | 88 | ✅ 通过 | ref query mismatch (Mumbai) but 3 Colombo ATMs match the (incidentally relevant) ref facts and Sri Lanka citation exactly. Complet |
| D34 | What undergraduate Mechanical Engineering courses does ZX… | 85 | ✅ 通过 | No ground truth exists (has_ref=false); answer correctly states topic is not mentioned in documents (only ATM-campus listings exis |
| D35 | What is the branch network of ZX Bank in Kanpur? | 88 | ✅ 通过 | 23 Kanpur branches confirmed; sum (5+5+4+5+4) = 23 with zone names and IFSC teachers 1001-5004. Complete and correct. |
| D36 | What features come with ZX Bank Current Account? | 90 | ✅ 通过 | All 8 Current Account features from ref facts (zero deposit, MAB, multi-branch, digital, cheque book, OD, RM, offers) listed exact |
| D37 | What is included in the ZX Current Account Welcome Kit? | 88 | ✅ 通过 | ref mismatched (Salary kit in facts/r1) but graded by citation (Current Account kit doc): all 6 kit items (bag, adapter, debit car |
| D38 | What is the branch network of ZX Bank in Mumbai? | 80 | ✅ 通过 | Mumbai network described (7+7+6+7+8) and headings say 34 branches but 35 listed - one more than claimed (also a typo 'Garden gate' |
| D39 | Where are ZX ATMs located at railway stations and airports? | 85 | ✅ 通过 | No ground truth; graded by citations. 20 Indian cities rail+airport ATM pairs are plausible, code-accurate (NDLS, MAS, CBE), consi |
| D40 | What daily transaction limits apply on ZX NetBanking? | 92 | ✅ 通过 | All four NetBanking daily limits (NEFT/RTGS ₹10L, IMPS/UPI ₹2L, bills ₹1L, self ₹20L) match ref table exactly, including higher-li |
| D41 | What is the branch network of ZX Bank in Bhopal? | 85 | ✅ 通过 | 8 Bhopal branches confirmed by ref fact; sum (2+2+1+1+2) = 8 with IFSC 1201-1208. r1 query mismatched (Nepal) but citations are co |
| D42 | What services are offered at ZX Bhopal branches? | 88 | ✅ 通过 | Bhopal services (retail, corporate, digital banking) match ref fact verbatim; correctly tailored response. Complete for the stated |
| D43 | What features and benefits does ZX Fixed Deposit have? | 85 | ✅ 通过 | FD features match all ref facts (min deposits per country, payout, schemes, joint, auto-renewal); tenure 7d-10yr/90% LTV/₹5,000 pl |
| D44 | What bill payment services does ZX Bank provide? | 86 | ✅ 通过 | Bill payment categories + Auto Debit features match ref facts (400+ billers, secure, OTP, Zia, tracking); category list consistent |
| D45 | What locker sizes are available at ZX Bank? | 90 | ✅ 通过 | Locker sizes (Small/Medium/Large) match ref fact exactly with the location-availability caveat. Simple, complete, correct. |
| D46 | What KYC documents are required to open a ZX locker? | 86 | ✅ 通过 | KYC documents (photo ID, address proof, passport photo) match ref fact; locker context (applications, form, agreement) in correct  |
| D47 | What cross-border payment services does ZX Bank provide? | 85 | ✅ 通过 | ref_mismatch (ref facts are bus stands). Graded by citations (Cross-Border Payments doc): India/SL/Nepal/Bhutan corridors, transfe |
| D48 | What special benefits are available on ZX house loan? | 87 | ✅ 通过 | Special house-loan benefits (women co-applicants, NRI service, green homes) match ref facts exactly; general benefits consistent w |
| D49 | What key features of standard health insurance plans part… | 88 | ✅ 通过 | Health insurance features match ref facts (medical coverage, cashless, pre/post hosp, family floater, add-ons); correctly ties ₹10 |
| D50 | What types of credit cards does ZX Bank issue? | 93 | ✅ 通过 | All 5 credit card variants named in ref facts detailed with features, fees, eligibility, matching per-table cited sections. Compre |

---

### Procedural（流程/步骤型）— P

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| P1 | How to open a ZX Bank savings account? | 90 | ✅ 通过 | All 5 online steps match ref_facts (app/website, Open Savings Account, details/docs, e-KYC, minutes); adds branch channel and bala |
| P2 | How to open a fixed deposit account at ZX Bank? | 85 | ✅ 通过 | 3 channels given (app, NetBanking, branch) with FD booking steps. ref_facts only show country/currency availability (ref_mismatch  |
| P3 | How to apply for a Digital Loan against Fixed Deposits at… | 63 | ⚠️ 部分 | No ref_facts. Correctly notes KB lacks a step-by-step Loan-against-FD procedure but provides related 90% facility info. kb_gap, no |
| P4 | How do I activate my new debit card online? | 65 | ⚠️ 部分 | ref_mismatch (ref is NetBanking activation). Answer states debit-card online activation not separately documented, corrects that m |
| P5 | How do I close my RuPay card? | 68 | ⚠️ 部分 | RuPay genuinely absent from KB (kb_gap); answer gives closest credit-card closure procedure via app/netbanking/care/branch. Ground |
| P6 | How to convert salary account to savings account? | 93 | ✅ 通过 | All 6 ground-truth steps present (branch visit, conversion form, submit, min balance, confirmation) plus digital alternative; matc |
| P7 | How do I add a beneficiary for international transfers? | 80 | ✅ 通过 | No ref_facts. Logically combines documented payee add and cross-border payment steps; disclaims that a dedicated intl-beneficiary  |
| P8 | How do I buy foreign exchange online? | 65 | ⚠️ 部分 | No ref. States online forex purchase not documented; offers related mentions (NRI no-forex-markup, remittance). kb_gap handling; n |
| P9 | How do I transfer money to another bank in India via NetB… | 75 | ⚠️ 部分 | No ref_facts. Correct fund-transfer steps (NEFT/RTGS, add payee, confirm) plus limits and self-registration; grounded but some der |
| P10 | How do I open a deposit account for a minor? | 60 | ⚠️ 部分 | ref_mismatch (ref is account-closing). Correctly reports no minor/guardian procedure exists and gives the standard opening routine |
| P11 | How do I fund the ASK Zia wallet? | 62 | ⚠️ 部分 | ref facts are WhatsApp onboarding (paraphrase mismatch). Correctly states no wallet product/procedure in KB; describes ASK Zia cha |
| P12 | How do I book a branch appointment? | 82 | ✅ 通过 | ref_mismatch (cheque book). Answer correctly gives appointment scheduling via app and PRM Assistant, grounded in cited docs. Minor |
| P13 | How do I deposit cash at an envelope-less ATM? | 62 | ⚠️ 部分 | No ref. Envelope-less cash deposit not documented (ATM services are withdrawal etc). kb_gap; honest answer. |
| P14 | What are the steps for interbank transfer from ZX to othe… | 76 | ⚠️ 部分 | No ref_facts. Gives correct interbank steps (activate NetBanking, Fund Transfer, payee, NEFT/IMPS/UPI, limits) and transparently n |
| P15 | How to open a Current Account at ZX Bank? | 80 | ✅ 通过 | ref_mismatch (ref is closing a current account). Doesn't answer opening with full online/offline steps and MAB/chequebook details; |
| P16 | What documents are required to open a current account at ZX? | 80 | ✅ 通过 | ref_mismatch (car loan docs). Correctly lists Aadhaar/PAN e-KYC, business docs, business KYC, ID/address, registration for current |
| P17 | How do I block and replace my ZX debit card? | 82 | ✅ 通过 | ref_mismatch (credit card closure). Full block/replace/PIN/limits procedure from app guide, plus fraud hotlisting note. Accurate a |
| P18 | What to do if I lose my ZX credit card or unauthorized tr… | 88 | ✅ 通过 | No ref_facts but answer matches doc_034's 5-step report flow exactly (contact/block/gather/complain/follow-up) with country hotlin |
| P19 | How to convert my ZX savings account to a salary account? | 92 | ✅ 通过 | All 6 ground-truth steps present and in order (tie-up, home branch/app, docs, conversion form, verification/processing, salary ben |
| P20 | How to open a ZX locker? | 90 | ✅ 通过 | Full 6-step locker procedure (availability, eligibility, application/agreement, deposit & rent, allotment & keys, operation) plus  |
| P21 | How do I apply for a home loan at ZX Bank? | 88 | ✅ 通过 | All 3 documented channels (online portal, app, branch) covered plus eligibility/docs details; matches ref_facts. |
| P22 | How do I apply for a LAP (Loan against Property) at ZX? | 62 | ⚠️ 部分 | ref_mismatch (car loan). LAP correctly absent from KB; answer notes House Loan as closest product with top-up/balance-transfer ter |
| P23 | How do I apply for a ZX personal loan? | 92 | ✅ 通过 | All 3 channels (branch, online, call/Zia) match ref_facts; tenure/collateral/document details accurate. |
| P24 | How to apply for a gold loan at ZX Bank? | 88 | ✅ 通过 | Matches ref_facts: both routes (branch with gold/docs, app pre-approval+appointment) plus quick disbursal and documents/eligibilit |
| P25 | How do I open an RD account through Mobile Banking? | 68 | ⚠️ 部分 | ref_mismatch (account conversion). Gives correct info that mobile RD-open route not documented, that RD can be handled via NetBank |
| P26 | How to activate online banking with ZX? | 85 | ✅ 通过 | 3 NetBanking activation routes (self-registration, branch, app) with correct step order from doc_041; ref_facts are app-oriented b |
| P27 | How to report and recover from a ZX fraud transaction? | 92 | ✅ 通过 | Matches 5-step fraud ref_facts plus prevention step; hotlines/complaint channels all present. Excellent detail. |
| P28 | How can I block my ZX card or account temporarily in case… | 80 | ✅ 通过 | No ref facts. Correct temporary-block procedure (Card Management/Account Services, Block/Hotlist, Freeze Account, Block Instantly) |
| P29 | How do I update my Know Your Customer (KYC) details at ZX… | 60 | ⚠️ 部分 | No ref. Correctly reports KYC update procedure undocumented; references only indirect mentions and contact-details update. kb_gap. |
| P30 | How do I open a Current Account for someone else (third-p… | 62 | ⚠️ 部分 | No ref. Correctly states 3rd-party/guardian opening not documented; provides standard current-account opening for context. kb_gap. |
| P31 | How to apply for an education loan at ZX Bank? | 55 | ⚠️ 部分 | ref_mismatch (car loan). Education loan absent from KB; claim of 'not mentioned' seems genuine. Fails to add context, so score low |
| P32 | How to apply for a vehicle loan at ZX Bank? | 78 | ⚠️ 部分 | ref_mismatch (house loan). Detailed car/bike loan application steps across app/branch; grounded in cited docs, but extra app-speci |
| P33 | How to open a savings account for a child at ZX Bank? | 60 | ⚠️ 部分 | ref_mismatch (account closing/conversion). Correctly reports no child/minor-specific procedure and gives standard opening; notes S |
| P34 | How do I deposit cash at a ZX Bank branch? | 55 | ⚠️ 部分 | ref_mismatch (cheque book). Cash deposit at branch not a documented procedure; claim of absence plausible. Bare answer, no context |
| P35 | How do I withdraw cash using a cheque at ZX Bank? | 52 | ⚠️ 部分 | No ref. Cheque-based cash withdrawal not in documed KB; bare 'not mentioned' with no explanation or nearest procedure. kb_gap. |
| P36 | How do I transfer money into a ZX savings account myself … | 78 | ⚠️ 部分 | No ref_facts. Reasonable own-account transfer steps with indicative ₹20L limit; well-cited but partially inferred from general tra |
| P37 | How safe is a ZX NetBanking transaction protection? | 78 | ⚠️ 部分 | More descriptive than procedural; accurately summarizes MFA, AI fraud detection, encryption, limits, notifications and user practi |
| P38 | How to register for a ZX Voice Biometrics/phone banking s… | 50 | ⚠️ 部分 | No ref. Voice biometrics/phone-banking registration not documented; correct but bare, no explanation or related information. |

---

### Temporal（时间型）— T

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| T1 | When did ZX Bank receive recognition for SME banking in S… | 95 | ✅ 通过 | Answer states recognition in 2022 and 2023; ref_fact 'Outstanding SME Bank – Sri Lanka (2022, 2023)' matches exactly. Citation ali |
| T2 | When were Bangladesh ATM location records last updated? | 95 | ✅ 通过 | Answer says last updated June 2024; ref_fact 'Last updated: June 2024' matches. Citation to doc_019 correct. |
| T3 | How many branches does ZX Bank have in Central Bangalore? | 90 | ✅ 通过 | Answer says 6 branches in Central Bangalore; ref_fact confirms six branches at the same locations. Verified. |
| T4 | When was ZX Bank Ltd founded? | 80 | ✅ 通过 | ref_facts are mismatched (they describe Bangladesh ATM update page, not founding). Graded by plausibility/citations: founding 1998 |
| T5 | No opening date given for Colombo Sri Lanka branches | 85 | ✅ 通过 | Honest 'no opening date given' answer citing Sri Lanka Branch Network doc; no ref_facts to contradict. Correct handling of absent  |
| T6 | No update date for Pune branch directory | 85 | ✅ 通过 | Honest 'no update date given' answer citing Pune Branch Network Directory; no contradiction. Correct handling of absent date. |
| T7 | No opening dates for Central Surat branches | 85 | ✅ 通过 | Honest 'no opening dates given' answer for Central Surat branches with citations; no contradicting refs. Correct. |
| T8 | No establishment dates for Bhutan ZX branches | 85 | ✅ 通过 | Honest 'no establishment dates given' for Bhutan branches with citations; no contradicting refs. Correct. |
| T9 | No installation dates for Surat park ATMs | 85 | ✅ 通过 | Honest 'no installation dates given' for Surat park ATMs with citations; no contradicting refs. Correct. |

---

### Open-Ended（开放型）— O

| 题号 | 问题 | 得分 | 判定 | 说明 |
|------|------|-----:|------|------|
| O1 | Why should I convert my savings account to a salary accou… | 93 | ✅ 通过 | All five bullet benefits (zero minimum balance, faster salary credit+alerts, preferential loan/card offers, fee waivers, insurance |
| O2 | What services can PRM Assistant provide to ZX customers? | 88 | ✅ 通过 | Covers all six grounded service areas (account inquiries, digital banking guidance, loan/credit advisory, wealth/investment concie |
| O3 | What benefits come with ZX Bank Salary Saving Account? | 90 | ✅ 通过 | All eight ref facts reproduced faithfully (zero balance, instant opening, free intl debit card, auto sweep FD, unlimited transfers |
| O4 | What special benefits ZX house loan offers for NRIs and w… | 65 | ⚠️ 部分 | ref_mismatch: bundle provides no ref_facts for this item (has_ref=false), so traceability to ground truth cannot be verified. The  |
| O5 | What benefits students get from ZX cross-border payment s… | 65 | ⚠️ 部分 | ref_mismatch: no ref_facts supplied (has_ref=false), so the student-focused claim (tuition to Nepal/Bhutan/Sri Lanka/India), curre |

---


## 4. 主要问题与建议

| 类别 | 现象 | 示例 | 建议 |
|------|------|------|------|
| 计数误差 | 开篇统计数字与明细条目不一致 | A30 “七分行”实为 8；D11 “18 城”实为 17；D30 “15”实为 17；D32 “九城”实为 8 | 生成答案时对表格做**逐行进数**核对，并让计数与明细自动一致 |
| 假“未提及” | 知识库其实有内容却判“未提及” | A18 影院 ATM（基准给出 foot traffic/cash 理由）、B15 账户关闭要求到行、C23 传统线下支付对比 | 扩大检索范围/回溯 TOC，避免因“切片未命中”→“未提及” |
| 知识库缺口 | 流程题基准有事而 kb 无相应文档 | P3/P4/P5/P8/P10/P13/P22/P25/P29/P30/P31/P33/P34/P35/P38（15 题） | 补录相关文档（借记卡激活、RuPay、外汇、KYC、子女开户、教育贷/LAP、柜上现金存款、支票取现、语音银行） |
| 改写不匹配 | 问法改写导致与基准题无法对应 | 约 30 题（含 P9/P8/P11/P26…） | 问题侧做改写归一化；报告可加“语义等价”标记 |
| 引用范围 | 引文行号覆盖但略宽/覆盖了多余内容 | 个别题源行号跨多个段 | 引用行号与命中段落做一致性校验 |

---

## 5. 评分口径

- 评分基于：**① Q1 的 Supporting Facts（金标准）**；**② R1 的 relevant_snippets（检索原文）**。
- **PASS ≥ 80**：答案正确且可追溯；**50–79 PARTIAL**：基本正确但有错/漏；**< 50 FAIL**：答错或关键内容缺失/虚构。
- “未提及但是知识库真的没有”按诚实作答处理（PARTIAL 或 PASS），仅当基准实际有内容而答案误判“未提及”才判 FAIL。
- 基准问法与题目无法对应时（ref_mismatch）按 cite/R1 原文核验，分数略保守。