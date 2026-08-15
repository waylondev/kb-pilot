# 恒生 enJoy 卡 e2e 测试问题集

> 知识库：`fixtures/hangseng-enjoy-kb`（3 篇文档：rewards-programme / offers / card-benefits）
> 用途：验证 kb-chat 的路由、定位、引用与自校验。每题标注预期命中文档与预期行为。

## 单文档事实题

### Q1: enJoy Dollars 怎么赚？消费多少可以赚多少？

- 预期命中文档：`docs/rewards-programme.md`
- 预期行为：定位到「enJoy Dollars」节，引用 `#L5-L12`，回答 HKD200 赚 HKD2。

### Q2: +FUN Dollars 可以在哪里用？

- 预期命中文档：`docs/rewards-programme.md`
- 预期行为：定位「+FUN Dollars」节，引用 `#L13-L18`，说明参与商户即时抵用或 Gift Parade 兑换礼品/现金券。

### Q3: yuu 积分转换一次最少要换多少？

- 预期命中文档：`docs/rewards-programme.md`
- 预期行为：引用 `#L23-L34`，回答 200 积分的倍数。

### Q4: enJoy 卡迎新优惠，新客户最多可得多少积分？价值多少？

- 预期命中文档：`docs/offers.md`
- 预期行为：定位「Welcome Offers」，引用 `#L5-L13`，回答 140,000 积分 ≈ 港币 700，永久免年费。**数值核对点**。

### Q5: 星期二在 enJoy 卡餐饮优惠是什么？消费满多少减多少？

- 预期命中文档：`docs/offers.md`
- 预期行为：定位「星期一至日餐饮优惠」，引用 `#L18-L26`，回答 88 折、满港币 250 减 30。**数值核对点**。

### Q6: enJoy 卡遗失要打哪个热线报案？

- 预期命中文档：`docs/card-benefits.md`
- 预期行为：定位「Lost Card / PIN Report」，引用 `#L22-L25`，回答 2836 0838。**数值核对点**。

### Q7: 24 小时客户服务热线是多少？可以查什么？

- 预期命中文档：`docs/card-benefits.md`
- 预期行为：定位「Customer Service」，引用 `#L26-L35`，回答 2998 8888，可查结欠、信用额、奖励结余。

## 跨文档 / 对比题

### Q8: enJoy 卡餐饮优惠和日常折扣有什么不同？

- 预期命中文档：`docs/offers.md`（同一文档内两个节）
- 预期行为：对比「enJoy Every Taste」与「enJoy Every Day」，分别引用 `#L14-L26` 与 `#L27-L46`。

### Q9: 赚取 enJoy Dollars 和赚取 +FUN Dollars 的机制一样吗？

- 预期命中文档：`docs/rewards-programme.md`
- 预期行为：对比两个节，引用 `#L5-L12` 与 `#L13-L18`。

## 不属于知识库

### Q10: 恒生 Visa Platinum 卡的年费是多少？

- 预期命中文档：无
- 预期行为：回答「not mentioned in the documents」，不编造。

## 模糊归属 / 路由判断题

### Q11: 我签账后得到的奖励积分可以用来做什么？

- 预期命中文档：`docs/rewards-programme.md`（奖励的用途集中在奖励计划文档）
- 预期行为：路由到 rewards-programme，说明 enJoy Dollars / +FUN Dollars 的抵现与兑换用途。

### Q12: 每月 8 号和 18 号刷卡有什么优惠？

- 预期命中文档：`docs/offers.md`
- 预期行为：定位「每月固定日期优惠」或「特约商户全年折扣」，引用对应行，回答 95 折。