# kb-chat 严格执行追踪报告

测试对象：`../../../fixtures/fengshen-kb/`

测试题集：`fengshen-hard-rag-questions.md`

执行目标：按 `kb-chat` Skill 的 6 个步骤，对知识库问题逐题作答，并记录每题的路由、章节定位、实际读取范围、correction 状态、答案、自检与标准答案对比。

执行时间：2026-08-10。

| 题号 | 主要能力 | 事实答案 | 引用精度 | 备注 |
|---|---|---:|---:|---|
| Q1 | 多跳师承推理、跨文档关联 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |
| Q2 | 实体消歧、跨文档关联、否定推理 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |
| Q3 | 跨文档因果链、时序推理 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |
| Q4 | 否定推理、分类完备性 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |
| Q5 | 集合运算、跨文档关联 | 通过 | 通过 | 源文支持 9 位有弟子、8 位破阵金仙；题集标准答案计数字段存在不一致 |
| Q6 | 法宝流转追踪、跨文档关联 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |
| Q7 | 跨阵营实体追踪、实体消歧、否定推理 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |
| Q8 | 时序推理、因果判断、影响推理 | 通过 | 通过 | 完成 Step 1 到 Step 6；答案与题集标准答案一致 |

## 本次单题执行更新：Q1

更新时间：2026-08-10。

问题：杨戬的师父是阐教十二金仙之一。这位师父的同门师兄弟中，谁破了十绝阵中的天绝阵？破阵者的弟子是谁？弟子的最终结局如何？

结论：

| 问点 | 答案 |
|---|---|
| 杨戬的师父 | 玉鼎真人，是十二金仙第五位，弟子为杨戬 |
| 破天绝阵的同门师兄弟 | 文殊广法天尊 |
| 破阵者的弟子 | 金吒 |
| 金吒最终结局 | 封神大战后肉身成圣，不入封神榜；封神后为“大同”，为文殊广法天尊弟子、李靖长子 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-factions-and-lineage.md` | `doc_004` | 标题为“封神演义门派体系与师承谱系”；摘要说明详列十二金仙与师承关系；tags 含“十二金仙”“玉鼎真人”“文殊广法天尊”“十二金仙弟子” | 确认杨戬师承、玉鼎真人与文殊广法天尊同属十二金仙，以及文殊广法天尊弟子 |
| `fengshen-major-battles.md` | `doc_005` | 标题为“封神演义重大战役纪事”；摘要包含十绝阵；tags 含“十绝阵”“天绝阵”“破阵过程”“文殊广法天尊” | 确认十绝阵中天绝阵的破阵者 |
| `fengshen-deification-list.md` | `doc_003` | 标题为“封神演义封神榜名录”；摘要包含肉身成圣七人与未入榜者；tags 含“肉身成圣”“金吒” | 确认金吒的最终结局 |

路由判断：题目需要跨文档推理。`fengshen-factions-and-lineage.md` 覆盖“杨戬→玉鼎真人→十二金仙同门→文殊广法天尊→金吒”；`fengshen-major-battles.md` 覆盖“天绝阵由谁破”；`fengshen-deification-list.md` 覆盖“金吒最终结局”。`fengshen-character-profiles.md` 虽含杨戬条目，但本题的师承与同门关系已由十二金仙表直接支撑；`fengshen-artifacts-and-counter.md` 与法宝克制有关，不是本题必要证据；`fengshen-variant-records.md` 处理异文误传，本题没有异文冲突。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-factions-and-lineage.md` | `ch_2_2` / `十二金仙` | L21-L39 | 定位十二金仙表，确认玉鼎真人、文殊广法天尊及二者弟子 |
| `fengshen-major-battles.md` | `ch_1_2` / `破阵过程` | L11-L23 | 定位十绝阵各阵破阵者，确认天绝阵由文殊广法天尊破 |
| `fengshen-deification-list.md` | `ch_13` / `肉身成圣七人` | L102-L113 | 定位金吒最终结局 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-factions-and-lineage.md` | L21-L38 | 十二金仙为元始天尊门下核心弟子；玉鼎真人为第 5 位，弟子杨戬；文殊广法天尊为第 12 位，弟子金吒 |
| `fengshen-major-battles.md` | L11-L22 | 十绝阵破阵过程中，天绝阵由文殊广法天尊破阵，并杀秦完天君 |
| `fengshen-deification-list.md` | L102-L112 | 七人封神大战后肉身成圣，不入封神榜；金吒为第 6 人，封号“大同”，是文殊广法天尊弟子、李靖长子 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录 |
| `doc_004.jsonl` | 不存在 |
| `doc_005.jsonl` | 不存在 |
| `doc_003.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 杨戬的师父 | 玉鼎真人 | 十二金仙表列出“玉鼎真人 | 玉泉山金霞洞 | 杨戬” |
| 玉鼎真人的同门范围 | 十二金仙同属元始天尊门下核心弟子 | 源文写明“十二金仙为元始天尊门下核心弟子” |
| 天绝阵破阵者 | 文殊广法天尊 | 十绝阵破阵过程列出“天绝阵：文殊广法天尊破阵” |
| 破阵者弟子 | 金吒 | 十二金仙表列出“文殊广法天尊 | 五龙山云霄洞 | 金吒” |
| 金吒最终结局 | 肉身成圣，不入封神榜；封神后为“大同” | 肉身成圣七人章节说明七人封神大战后肉身成圣、不入封神榜，并列出“金吒：大同” |

最终答案：杨戬的师父是玉鼎真人；玉鼎真人与文殊广法天尊同属元始天尊门下十二金仙，因此文殊广法天尊是玉鼎真人的同门师兄弟之一。十绝阵中的天绝阵由文殊广法天尊破阵。文殊广法天尊的弟子是金吒。金吒的最终结局是封神大战后肉身成圣、不入封神榜，封神后为“大同”，并被记载为文殊广法天尊弟子、李靖长子。

引用：

- Source: `doc_004` `ch_2_2` `fengshen-factions-and-lineage.md#L23-L38`
- Source: `doc_005` `ch_1_2` `fengshen-major-battles.md#L11-L13`
- Source: `doc_003` `ch_13` `fengshen-deification-list.md#L102-L112`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 杨戬的师父是玉鼎真人 | 通过 | `fengshen-factions-and-lineage.md#L25-L31` |
| 玉鼎真人与文殊广法天尊同属十二金仙，构成同门师兄弟关系 | 通过 | `fengshen-factions-and-lineage.md#L23-L38` |
| 天绝阵由文殊广法天尊破阵 | 通过 | `fengshen-major-battles.md#L11-L13` |
| 文殊广法天尊的弟子是金吒 | 通过 | `fengshen-factions-and-lineage.md#L38-L38` |
| 金吒肉身成圣，不入封神榜，封神后为“大同” | 通过 | `fengshen-deification-list.md#L102-L112` |

自检结论：已回答题目所有问点；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。与题集 `fengshen-hard-rag-questions.md` 的 Q1 标准答案对比一致：玉鼎真人、文殊广法天尊、金吒、肉身成圣不入封神榜及“大同”结局均匹配。

## 本次单题执行更新：Q2

更新时间：2026-08-10。

问题：太公望在封神台册封了多少位正神？飞熊先生本人是否在封神榜上？吕尚与姜子牙是什么关系？

结论：

| 问点 | 答案 |
|---|---|
| 太公望册封了多少位正神 | 三百六十五位正神 |
| 飞熊先生本人是否在封神榜上 | 不在封神榜上；本人功成圆满，未入封神榜 |
| 吕尚与姜子牙是什么关系 | 吕尚是姜子牙的别称；姜子牙本名姜尚，因先祖封于吕地，故又称吕尚 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-character-profiles.md` | `doc_002` | 标题为“封神演义核心人物图鉴”；摘要包含姜子牙核心事迹；tags 含“姜子牙”“姜尚”“飞熊先生”“太公望”“封神” | 识别太公望、飞熊先生、吕尚与姜子牙的称号关系，并判断姜子牙本人是否入榜 |
| `fengshen-deification-list.md` | `doc_003` | 标题为“封神演义封神榜名录”；摘要包含三百六十五位正神名录和未入榜者；tags 含“封神台总管”“清福正神”“未入封神榜”“姜子牙” | 交叉确认册封数量与姜子牙未入封神榜 |

路由判断：本题核心是同一人物的多重称号消歧和封神状态判断。`fengshen-character-profiles.md` 的姜子牙条目直接覆盖“太公望”“飞熊先生”“吕尚/姜尚”和册封数量；`fengshen-deification-list.md` 可交叉确认三百六十五位正神和姜子牙本人未封神。`fengshen-variant-records.md` 虽含姜子牙异文，但本题没有“土地神”等误传前提，故不作为必要命中文档；其他战役、法宝、师承文档与本题问点无直接关系。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-character-profiles.md` | `ch_1_1` / `姜子牙` | L9-L18 | 定位姜子牙多重称号、册封数量和本人未入榜 |
| `fengshen-deification-list.md` | `ch_1_1` / `三界首领` | L7-L9 | 定位封神榜三百六十五位正神表述 |
| `fengshen-deification-list.md` | `ch_14` / `未入封神榜者` | L114-L121 | 定位姜子牙主持封神但本人未封神的结局 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-character-profiles.md` | L9-L17 | 姜子牙本名姜尚、字子牙，先祖封于吕地故又称吕尚；道号飞熊先生；周室尊称太公望；于封神台册封三百六十五位正神；本人未入封神榜 |
| `fengshen-deification-list.md` | L1-L11 | 封神榜共册封三百六十五位正神，由姜子牙在封神台代元始天尊逐一宣读册封；柏鉴统领八部三百六十五位清福正神 |
| `fengshen-deification-list.md` | L114-L121 | 姜子牙主持封神，本人未封神；封神完成后归周辅政，后封于齐，只享人间富贵 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录 |
| `doc_002.jsonl` | 不存在 |
| `doc_003.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 太公望指代谁 | 太公望是姜子牙的周室尊称 | 源文写明“周室尊称太公望” |
| 太公望册封数量 | 三百六十五位正神 | 姜子牙条目写明“于封神台册封三百六十五位正神”；封神榜名录也写明共册封三百六十五位正神 |
| 飞熊先生指代谁 | 飞熊先生是姜子牙道号 | 源文写明“道号飞熊先生” |
| 飞熊先生本人是否在榜上 | 不在封神榜上 | 姜子牙条目写明“本人功成圆满，未入封神榜”；名录写明“姜子牙：主持封神之人，本人未封神” |
| 吕尚与姜子牙关系 | 吕尚是姜子牙的别称 | 源文写明“本名姜尚，字子牙，先祖封于吕地，故又称吕尚” |

最终答案：太公望就是姜子牙的周室尊称；他在封神台册封了三百六十五位正神。飞熊先生是姜子牙的道号，姜子牙本人未入封神榜，也就是飞熊先生本人不在封神榜上。吕尚是姜子牙的别称：姜子牙本名姜尚、字子牙，因先祖封于吕地，故又称吕尚。

引用：

- Source: `doc_002` `ch_1_1` `fengshen-character-profiles.md#L11-L17`
- Source: `doc_003` `ch_1_1` `fengshen-deification-list.md#L3-L8`
- Source: `doc_003` `ch_14` `fengshen-deification-list.md#L114-L118`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 太公望是姜子牙的周室尊称 | 通过 | `fengshen-character-profiles.md#L11-L13` |
| 姜子牙在封神台册封三百六十五位正神 | 通过 | `fengshen-character-profiles.md#L16-L16`; `fengshen-deification-list.md#L3-L3` |
| 飞熊先生是姜子牙的道号 | 通过 | `fengshen-character-profiles.md#L12-L12` |
| 飞熊先生本人不在封神榜上 | 通过 | `fengshen-character-profiles.md#L17-L17`; `fengshen-deification-list.md#L116-L118` |
| 吕尚是姜子牙的别称 | 通过 | `fengshen-character-profiles.md#L11-L11` |

自检结论：已回答题目所有问点；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q2 标准答案进行对比，结果一致：太公望、飞熊先生、吕尚均指向姜子牙相关称号；册封数量为三百六十五位；本人未入封神榜。

## 本次单题执行更新：Q3

更新时间：2026-08-10。

问题：赵公明之死引发了一系列连锁反应。请按时间顺序列出从赵公明身亡到万仙阵结束的全部关键事件，并说明每个事件的直接触发原因。

结论：

| 顺序 | 关键事件 | 直接触发原因 |
|---:|---|---|
| 1 | 赵公明身亡 | 赵公明失去定海珠后，陆压道人施钉头七箭书，二十一日后身亡 |
| 2 | 三霄复仇并布九曲黄河阵 | 赵公明之死直接引发三霄娘娘复仇；兄妹之情成为直接动因 |
| 3 | 十二金仙修为被削 | 三霄以混元金斗困住十二金仙，削去顶上三花、胸中五气 |
| 4 | 元始天尊与太上老君合力破九曲黄河阵 | 姜子牙虽有戊己杏黄旗自保，但无法破阵，元始天尊亲自下山并与太上老君合力 |
| 5 | 三霄被杀，十二金仙获救但修为大损 | 九曲黄河阵被二圣合力破除后的结果 |
| 6 | 通天教主命多宝道人摆诛仙阵 | 截教弟子接连阵亡，通天教主震怒，意在以截教之力一雪前耻 |
| 7 | 四圣合力破诛仙阵，四剑被摘 | 诛仙阵非四位圣人合力不可破，元始天尊、太上老君、接引道人、准提道人四圣合力 |
| 8 | 诛仙阵破，通天教主逃走，多宝道人被擒 | 四圣合力破阵后的结果 |
| 9 | 通天教主摆万仙阵决战 | 诛仙阵破后，通天教主倾截教全部实力，欲与阐教决战 |
| 10 | 万仙阵被破，封神大战基本结束 | 四圣再次合力，各方悉数参战；金灵圣母战死、龟灵圣母被吞噬、无当圣母撤走，截教元气大伤 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-major-battles.md` | `doc_005` | 标题为“封神演义重大战役纪事”；摘要说明依原著顺序记述赵公明之死、九曲黄河阵、诛仙阵、万仙阵等大战；tags 含“赵公明之死”“三霄复仇”“九曲黄河阵”“诛仙阵”“万仙阵”“封神大战结束” | 按时间顺序抽取赵公明身亡到万仙阵结束的关键事件及直接触发原因 |

路由判断：本题问的是从赵公明之死到万仙阵结束的连续战役因果链，`fengshen-major-battles.md` 在 manifest 中同时覆盖相关事件、时序和结果，且 `path` 字段存在，可直接用于后续 tree 定位和源文读取。`fengshen-character-profiles.md` 含赵公明人物条目，但不能完整覆盖九曲黄河阵、诛仙阵、万仙阵的连续时序；`fengshen-deification-list.md` 主要记录封神名录，不是本题主要证据；其他文档与本题问点不直接匹配。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-major-battles.md` | `ch_3` / `赵公明之死` | L34-L39 | 定位赵公明身亡及三霄复仇的直接动因 |
| `fengshen-major-battles.md` | `ch_4` / `九曲黄河阵之战` | L40-L53 | 定位三霄布阵、十二金仙修为被削、二圣破阵及结果 |
| `fengshen-major-battles.md` | `ch_5` / `诛仙阵之战` | L54-L74 | 定位通天摆诛仙阵、四圣破阵及结果 |
| `fengshen-major-battles.md` | `ch_6` / `万仙阵之战` | L75-L90 | 定位万仙阵决战及封神大战基本结束 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-major-battles.md` | L34-L39 | 赵公明失去定海珠后，陆压施钉头七箭书，二十一日后赵公明身亡；赵公明之死直接引发三霄复仇，兄妹之情是九曲黄河阵直接动因 |
| `fengshen-major-battles.md` | L40-L53 | 三霄为报赵公明之仇布九曲黄河阵；混元金斗削十二金仙三花五气；姜子牙无法破阵，元始天尊与太上老君合力破阵；三霄被杀，十二金仙修为大损 |
| `fengshen-major-battles.md` | L54-L74 | 通天教主因截教弟子接连阵亡而命多宝道人摆诛仙阵；诛仙阵非四圣不可破；四圣合力破阵，四剑被摘；通天逃走，多宝被擒 |
| `fengshen-major-battles.md` | L75-L89 | 诛仙阵破后，通天教主倾截教全部实力摆万仙阵；四圣再次合力，阐教众人参战；金灵圣母战死、龟灵圣母被吞噬、无当圣母撤走，截教元气大伤，封神大战基本结束 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录 |
| `doc_005.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 起点事件 | 赵公明身亡 | 源文写明陆压施钉头七箭书，二十一日后赵公明身亡 |
| 第一层连锁 | 三霄复仇、布九曲黄河阵 | 源文写明赵公明之死直接引发三霄复仇，兄妹之情是直接动因 |
| 九曲黄河阵影响 | 十二金仙修为被削 | 源文写明混元金斗困住十二金仙，削去三花五气 |
| 九曲黄河阵被破 | 元始天尊与太上老君合力破阵 | 源文写明姜子牙无法破阵，元始天尊亲自下山，与太上老君合力破阵 |
| 诛仙阵触发 | 截教弟子接连阵亡，通天震怒 | 源文写明通天因截教弟子接连阵亡而命多宝道人摆诛仙阵 |
| 诛仙阵结果 | 四圣破阵，通天逃走，多宝被擒 | 源文写明四圣合力破阵，诛仙阵破，通天逃走，多宝被擒 |
| 万仙阵触发 | 诛仙阵破后通天倾截教全部实力决战 | 源文写明诛仙阵破后通天摆下万仙阵 |
| 万仙阵结果 | 截教元气大伤，封神大战基本结束 | 源文写明金灵圣母战死、龟灵圣母被吞噬、无当圣母撤走，万仙阵被破 |

最终答案：按时间顺序，赵公明身亡后的连锁反应是：第一，赵公明在失去定海珠后，被陆压道人以钉头七箭书咒杀，二十一日后身亡。第二，赵公明之死直接引发三霄娘娘复仇，三霄因兄妹之情在西岐城外布下九曲黄河阵。第三，三霄用混元金斗困住阐教十二金仙，削去其顶上三花、胸中五气，使其千年修为尽数废去。第四，姜子牙无法破阵，元始天尊亲自下山，与太上老君合力破九曲黄河阵；结果三霄被杀，十二金仙虽被救出但修为大损。第五，截教弟子接连阵亡使通天教主震怒，他命多宝道人代为摆设诛仙阵，一雪前耻。第六，诛仙阵非四圣不可破，元始天尊、太上老君、接引道人、准提道人合力破阵，四剑被摘，通天教主逃走，多宝道人被擒。第七，诛仙阵破后，通天教主倾截教全部实力摆下万仙阵，与阐教决战。第八，万仙阵中四圣再次合力，阐教十二金仙、姜子牙、哪吒、杨戬等参战；最终金灵圣母战死，龟灵圣母遭蚊道人吞噬，无当圣母撤走，截教元气大伤，万仙阵被破，封神大战至此基本结束。

引用：

- Source: `doc_005` `ch_3` `fengshen-major-battles.md#L34-L39`
- Source: `doc_005` `ch_4` `fengshen-major-battles.md#L40-L53`
- Source: `doc_005` `ch_5` `fengshen-major-battles.md#L54-L74`
- Source: `doc_005` `ch_6` `fengshen-major-battles.md#L75-L89`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 赵公明因陆压钉头七箭书，二十一日后身亡 | 通过 | `fengshen-major-battles.md#L36-L36` |
| 赵公明之死直接引发三霄复仇，并成为九曲黄河阵直接动因 | 通过 | `fengshen-major-battles.md#L38-L44` |
| 三霄以混元金斗削去十二金仙三花五气 | 通过 | `fengshen-major-battles.md#L48-L48` |
| 姜子牙无法破阵，元始天尊与太上老君合力破阵 | 通过 | `fengshen-major-battles.md#L48-L48` |
| 三霄被杀，十二金仙修为大损 | 通过 | `fengshen-major-battles.md#L50-L52` |
| 通天因截教弟子接连阵亡而摆诛仙阵 | 通过 | `fengshen-major-battles.md#L56-L60` |
| 四圣合力破诛仙阵，四剑被摘，通天逃走，多宝被擒 | 通过 | `fengshen-major-battles.md#L62-L73` |
| 诛仙阵破后通天摆万仙阵决战 | 通过 | `fengshen-major-battles.md#L75-L79` |
| 万仙阵被破，截教元气大伤，封神大战基本结束 | 通过 | `fengshen-major-battles.md#L81-L89` |

自检结论：已回答题目所有问点；事件顺序与源文章节顺序一致；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q3 标准答案进行对比，结果一致：覆盖赵公明身亡、三霄布九曲黄河阵、十二金仙修为被废、二圣破阵、通天摆诛仙阵、四圣破诛仙阵、万仙阵决战及万仙阵破。

## 本次单题执行更新：Q4

更新时间：2026-08-10。

问题：以下八位人物中，哪些入了封神榜（给出封号），哪些是肉身成圣不入榜，哪些因其他原因未入榜？闻仲、哪吒、姜子牙、杨戬、苏妲己、赵公明、殷郊、韦护。

结论：

| 分类 | 人物 | 封号 / 圣号 / 原因 |
|---|---|---|
| 入封神榜 | 闻仲 | 九天应元雷声普化天尊 |
| 入封神榜 | 赵公明 | 金龙如意正一龙虎玄坛真君，民间称财神 |
| 入封神榜 | 殷郊 | 执年岁君太岁 |
| 肉身成圣不入榜 | 哪吒 | 中坛元帅，民间称三太子 |
| 肉身成圣不入榜 | 杨戬 | 清源妙道真君，民间称二郎神 |
| 肉身成圣不入榜 | 韦护 | 韦陀菩萨 |
| 其他原因未入榜 | 姜子牙 | 主持封神之人，本人未封神；封神完成后归周辅政，后封于齐，只享人间富贵 |
| 其他原因未入榜 | 苏妲己 | 原著明确狐妖不入封神榜，因系妖邪祸乱，非正途修行 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-deification-list.md` | `doc_003` | 标题为“封神演义封神榜名录”；摘要说明涵盖正神名录、肉身成圣七人与未入榜者；tags 含“闻仲”“赵公明”“殷郊”“哪吒”“杨戬”“韦护”“姜子牙”“苏妲己”“肉身成圣”“未入封神榜” | 对八人做入榜、肉身成圣不入榜、其他原因未入榜三类归档，并提取封号或原因 |
| `fengshen-character-profiles.md` | `doc_002` | 标题为“封神演义核心人物图鉴”；摘要包含姜子牙、哪吒、杨戬、闻仲、妲己等人物；tags 含“不入封神榜”“莲花化身”“肉身成圣”“清源妙道真君”“苏护”“狐妖夺舍” | 补充确认姜子牙、哪吒、杨戬、苏妲己等人物身份和封神状态边界 |

路由判断：本题核心是封神状态分类，`fengshen-deification-list.md` 是主证据文档，能覆盖八人的封号或未入榜状态；`fengshen-character-profiles.md` 用于补充人物身份和否定边界，尤其是苏妲己狐妖夺舍、不入封神榜以及姜子牙、哪吒、杨戬的状态说明。战役、法宝、师承文档不是本题主要证据。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-deification-list.md` | `ch_3` / `雷部诸神` | L25-L32 | 定位闻仲入榜封号 |
| `fengshen-deification-list.md` | `ch_7` / `财神体系` | L58-L65 | 定位赵公明入榜封号 |
| `fengshen-deification-list.md` | `ch_10` / `殷郊殷洪封位` | L82-L86 | 定位殷郊入榜封号 |
| `fengshen-deification-list.md` | `ch_13` / `肉身成圣七人` | L102-L113 | 定位哪吒、杨戬、韦护肉身成圣不入榜 |
| `fengshen-deification-list.md` | `ch_14` / `未入封神榜者` | L114-L121 | 定位姜子牙、苏妲己其他原因未入榜 |
| `fengshen-character-profiles.md` | `ch_1_1` / `姜子牙` | L9-L18 | 补充姜子牙未入封神榜 |
| `fengshen-character-profiles.md` | `ch_1_2` / `哪吒` | L19-L27 | 补充哪吒肉身成圣 |
| `fengshen-character-profiles.md` | `ch_1_3` / `杨戬` | L28-L35 | 补充杨戬清源妙道真君 |
| `fengshen-character-profiles.md` | `ch_2_2` / `妲己` | L56-L63 | 补充苏妲己狐妖夺舍、不入封神榜 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-deification-list.md` | L25-L31 | 闻仲封九天应元雷声普化天尊，统领雷部二十四员正神，绝龙岭战死后受封 |
| `fengshen-deification-list.md` | L58-L64 | 赵公明封金龙如意正一龙虎玄坛真君，民间称财神 |
| `fengshen-deification-list.md` | L82-L85 | 殷郊封执年岁君太岁 |
| `fengshen-deification-list.md` | L102-L112 | 哪吒、杨戬、韦护属于肉身成圣七人，不入封神榜；分别为中坛元帅、清源妙道真君、韦陀菩萨 |
| `fengshen-deification-list.md` | L114-L121 | 姜子牙主持封神但本人未封神；苏妲己狐妖不入封神榜，因系妖邪祸乱、非正途修行 |
| `fengshen-character-profiles.md` | L9-L17 | 姜子牙本人功成圆满，未入封神榜 |
| `fengshen-character-profiles.md` | L19-L34 | 哪吒封神后肉身成圣；杨戬封神后为清源妙道真君 |
| `fengshen-character-profiles.md` | L56-L62 | 真正苏妲己已死，狐妖以其身份祸乱商朝，原著明确其不入封神榜 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录 |
| `doc_003.jsonl` | 不存在 |
| `doc_002.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 闻仲 | 入封神榜，封九天应元雷声普化天尊 | 雷部诸神条目直接列出闻仲封号 |
| 赵公明 | 入封神榜，封金龙如意正一龙虎玄坛真君 | 财神体系条目直接列出赵公明封号 |
| 殷郊 | 入封神榜，封执年岁君太岁 | 殷郊殷洪封位条目直接列出殷郊封位 |
| 哪吒 | 肉身成圣不入榜，中坛元帅 | 肉身成圣七人条目说明七人不入封神榜，并列哪吒 |
| 杨戬 | 肉身成圣不入榜，清源妙道真君 | 肉身成圣七人条目说明七人不入封神榜，并列杨戬 |
| 韦护 | 肉身成圣不入榜，韦陀菩萨 | 肉身成圣七人条目说明七人不入封神榜，并列韦护 |
| 姜子牙 | 其他原因未入榜，主持封神但本人未封神 | 未入封神榜者条目和人物图鉴均说明姜子牙本人未封神 |
| 苏妲己 | 其他原因未入榜，狐妖祸乱，非正途修行 | 未入封神榜者条目和人物图鉴均说明苏妲己不入封神榜 |

最终答案：

| 分类 | 人物 | 封号 / 圣号 / 原因 |
|---|---|---|
| 入封神榜 | 闻仲 | 九天应元雷声普化天尊 |
| 入封神榜 | 赵公明 | 金龙如意正一龙虎玄坛真君，民间称财神 |
| 入封神榜 | 殷郊 | 执年岁君太岁 |
| 肉身成圣，不入封神榜 | 哪吒 | 中坛元帅，民间称三太子 |
| 肉身成圣，不入封神榜 | 杨戬 | 清源妙道真君，民间称二郎神 |
| 肉身成圣，不入封神榜 | 韦护 | 韦陀菩萨 |
| 其他原因未入封神榜 | 姜子牙 | 主持封神之人，本人未封神；封神完成后归周辅政，后封于齐，只享人间富贵 |
| 其他原因未入封神榜 | 苏妲己 | 狐妖夺舍并祸乱商朝，原著明确不入封神榜；因系妖邪祸乱，非正途修行 |

引用：

- Source: `doc_003` `ch_3` `fengshen-deification-list.md#L25-L31`
- Source: `doc_003` `ch_7` `fengshen-deification-list.md#L58-L64`
- Source: `doc_003` `ch_10` `fengshen-deification-list.md#L82-L85`
- Source: `doc_003` `ch_13` `fengshen-deification-list.md#L102-L112`
- Source: `doc_003` `ch_14` `fengshen-deification-list.md#L114-L121`
- Source: `doc_002` `ch_1_1` `fengshen-character-profiles.md#L9-L17`
- Source: `doc_002` `ch_1_2` `fengshen-character-profiles.md#L19-L27`
- Source: `doc_002` `ch_1_3` `fengshen-character-profiles.md#L28-L35`
- Source: `doc_002` `ch_2_2` `fengshen-character-profiles.md#L56-L62`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 闻仲入封神榜，封九天应元雷声普化天尊 | 通过 | `fengshen-deification-list.md#L25-L31` |
| 赵公明入封神榜，封金龙如意正一龙虎玄坛真君 | 通过 | `fengshen-deification-list.md#L58-L64` |
| 殷郊入封神榜，封执年岁君太岁 | 通过 | `fengshen-deification-list.md#L82-L85` |
| 哪吒肉身成圣，不入封神榜，为中坛元帅 | 通过 | `fengshen-deification-list.md#L102-L106`; `fengshen-character-profiles.md#L19-L27` |
| 杨戬肉身成圣，不入封神榜，为清源妙道真君 | 通过 | `fengshen-deification-list.md#L102-L107`; `fengshen-character-profiles.md#L28-L35` |
| 韦护肉身成圣，不入封神榜，为韦陀菩萨 | 通过 | `fengshen-deification-list.md#L102-L110` |
| 姜子牙因主持封神而本人未封神，未入封神榜 | 通过 | `fengshen-deification-list.md#L114-L118`; `fengshen-character-profiles.md#L9-L17` |
| 苏妲己因狐妖祸乱、非正途修行，未入封神榜 | 通过 | `fengshen-deification-list.md#L114-L119`; `fengshen-character-profiles.md#L56-L62` |

自检结论：已回答题目所有问点；八位人物均完成分类且无遗漏；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q4 标准答案进行对比，结果一致：入榜者为闻仲、赵公明、殷郊；肉身成圣不入榜者为哪吒、杨戬、韦护；其他原因未入榜者为姜子牙、苏妲己。

## 本次单题执行更新：Q5

更新时间：2026-08-10。

问题：阐教十二金仙中，哪些人有弟子？哪些人没有弟子？在十绝阵中破阵的金仙有几位？这些破阵金仙中，有弟子的是多数还是少数？

结论：

| 问点 | 答案 |
|---|---|
| 有弟子的十二金仙 | 广成子、赤精子、清虚道德真君、太乙真人、玉鼎真人、普贤真人、惧留孙、道行天尊、文殊广法天尊，共 9 位 |
| 没有弟子的十二金仙 | 灵宝大法师、黄龙真人、慈航道人，共 3 位 |
| 十绝阵中破阵的十二金仙 | 文殊广法天尊、惧留孙、慈航道人、普贤真人、广成子、太乙真人、赤精子、清虚道德真君，共 8 位 |
| 破阵金仙中有弟子的是多数还是少数 | 多数；8 位破阵金仙中 7 位有弟子，仅慈航道人无弟子 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-factions-and-lineage.md` | `doc_004` | 标题为“封神演义门派体系与师承谱系”；摘要说明详列十二金仙与师承关系树；tags 含“十二金仙”“十二金仙弟子”“广成子”“赤精子”“清虚道德真君”“文殊广法天尊”等 | 提取十二金仙名单及各自弟子，区分有弟子和无弟子 |
| `fengshen-major-battles.md` | `doc_005` | 标题为“封神演义重大战役纪事”；摘要含十绝阵；tags 含“十绝阵”“十二金仙破阵”“破阵过程”“文殊广法天尊”“惧留孙”“慈航道人”“普贤真人”“广成子”“太乙真人”“赤精子”“清虚道德真君” | 提取十绝阵各阵破阵者，并与十二金仙名单求交集 |

路由判断：本题需要两个集合：十二金仙弟子分布与十绝阵破阵者。`fengshen-factions-and-lineage.md` 提供十二金仙表；`fengshen-major-battles.md` 提供十绝阵破阵列表。其他文档不直接提供这两个集合的完整结构，因此不作为命中文档。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-factions-and-lineage.md` | `ch_2_2` / `十二金仙` | L21-L39 | 定位十二金仙表，读取每位金仙的弟子字段 |
| `fengshen-major-battles.md` | `ch_1_2` / `破阵过程` | L11-L23 | 定位十绝阵各阵破阵者 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-factions-and-lineage.md` | L21-L38 | 十二金仙及弟子表：广成子、赤精子、清虚道德真君、太乙真人、玉鼎真人、普贤真人、惧留孙、道行天尊、文殊广法天尊有弟子；灵宝大法师、黄龙真人、慈航道人弟子为“无” |
| `fengshen-major-battles.md` | L11-L22 | 十绝阵破阵者：文殊广法天尊、惧留孙、慈航道人、普贤真人、广成子、太乙真人、陆压道人、赤精子、清虚道德真君、南极仙翁；其中陆压道人和南极仙翁不在十二金仙表中 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录 |
| `doc_004.jsonl` | 不存在 |
| `doc_005.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 有弟子的十二金仙 | 9 位：广成子、赤精子、清虚道德真君、太乙真人、玉鼎真人、普贤真人、惧留孙、道行天尊、文殊广法天尊 | 十二金仙表中这 9 人的弟子字段不为“无” |
| 无弟子的十二金仙 | 3 位：灵宝大法师、黄龙真人、慈航道人 | 十二金仙表中这 3 人的弟子字段为“无” |
| 十绝阵破阵者中属于十二金仙者 | 8 位：文殊广法天尊、惧留孙、慈航道人、普贤真人、广成子、太乙真人、赤精子、清虚道德真君 | 破阵列表中共有 10 位破阵者，扣除不在十二金仙表中的陆压道人、南极仙翁，剩余 8 位金仙 |
| 破阵金仙中有弟子的人数 | 7 位 | 8 位破阵金仙中，仅慈航道人在十二金仙表中弟子为“无” |
| 多数还是少数 | 多数 | 7/8 有弟子，明显超过半数 |

最终答案：

| 类别 | 人物 |
|---|---|
| 有弟子的十二金仙 | 广成子（殷郊）、赤精子（殷洪）、清虚道德真君（黄天化、杨任）、太乙真人（哪吒）、玉鼎真人（杨戬）、普贤真人（木吒）、惧留孙（土行孙）、道行天尊（韦护、韩毒龙、薛恶虎）、文殊广法天尊（金吒） |
| 无弟子的十二金仙 | 灵宝大法师、黄龙真人、慈航道人 |
| 十绝阵中破阵的十二金仙 | 文殊广法天尊（天绝阵）、惧留孙（地烈阵）、慈航道人（风吼阵）、普贤真人（寒冰阵）、广成子（金光阵）、太乙真人（化血阵）、赤精子（落魂阵）、清虚道德真君（红水阵） |

十绝阵中破阵的十二金仙共有 8 位。破阵金仙中有弟子的共有 7 位，只有慈航道人无弟子，所以有弟子者占多数。

引用：

- Source: `doc_004` `ch_2_2` `fengshen-factions-and-lineage.md#L21-L38`
- Source: `doc_005` `ch_1_2` `fengshen-major-battles.md#L11-L22`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 十二金仙中有弟子的为 9 位 | 通过 | `fengshen-factions-and-lineage.md#L27-L38` |
| 十二金仙中无弟子的为灵宝大法师、黄龙真人、慈航道人 3 位 | 通过 | `fengshen-factions-and-lineage.md#L32-L35` |
| 十绝阵破阵者列表包含 10 位破阵者 | 通过 | `fengshen-major-battles.md#L13-L22` |
| 十绝阵破阵者中属于十二金仙者为 8 位 | 通过 | `fengshen-factions-and-lineage.md#L27-L38`; `fengshen-major-battles.md#L13-L22` |
| 破阵金仙中有弟子者为 7 位，仅慈航道人无弟子 | 通过 | `fengshen-factions-and-lineage.md#L27-L38`; `fengshen-major-battles.md#L13-L22` |
| 破阵金仙中有弟子者占多数 | 通过 | `fengshen-factions-and-lineage.md#L27-L38`; `fengshen-major-battles.md#L13-L22` |

自检结论：已回答题目所有问点；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q5 标准答案进行对比：题集标准答案的列举内容与源文一致，但计数字段存在内部不一致，写作“有弟子的金仙（8位）”却列出 9 位，写作“十绝阵破阵的金仙（7位）”却列出 8 位；因此本报告按源文和题集列出的证据锚点记录为 9 位有弟子、8 位破阵金仙、其中 7 位有弟子。

## 本次单题执行更新：Q6

更新时间：2026-08-10。

问题：殷郊叛变时使用了什么法宝？这件法宝原本属于谁？为什么要克制这件法宝需要四件法宝？最终殷郊是怎么死的？殷郊的弟弟殷洪使用了什么法宝叛变？

结论：

| 问点 | 答案 |
|---|---|
| 殷郊叛变时使用的法宝 | 番天印 |
| 番天印原本属于谁 | 广成子 |
| 为什么克制番天印需要四件法宝 | 番天印威力极强，广成子本人也无法正面对抗；源文记录需四方旗（戊己杏黄旗、素色云界旗、离地焰光旗、青莲宝色旗）合力抵消其威力 |
| 殷郊最终怎么死 | 被四方旗所制后，应誓被犁锄而死 |
| 殷洪使用什么法宝叛变 | 阴阳镜 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-artifacts-and-counter.md` | `doc_001` | 标题为“封神演义法宝谱与克制关系”；摘要说明涵盖阐教法宝及法宝克制关系；tags 含“番天印”“广成子”“殷郊”“叛变”“重创周营”“阴阳镜”“赤精子”“殷洪”“四方旗克番天印”“太极图克阴阳镜” | 确认番天印、阴阳镜的持有者、流转、实战，以及四方旗对番天印的克制方式 |
| `fengshen-major-battles.md` | `doc_005` | 标题为“封神演义重大战役纪事”；摘要说明含殷郊殷洪叛变事件因果链；tags 含“殷郊殷洪叛变”“太极图”“番天印”“四方旗”“犁锄而死”“阴阳镜”“化为飞灰” | 确认殷郊、殷洪叛变经过、殷郊死因及殷洪结局 |
| `fengshen-character-profiles.md` | `doc_002` | 标题为“封神演义核心人物图鉴”；摘要包含殷郊殷洪生平与结局；tags 含“殷郊”“殷洪”“纣王之子”“叛变助商”“太极图”“四方旗”“犁锄而死”“番天印” | 交叉确认殷郊殷洪兄弟身份、师承、叛变和结局 |

路由判断：本题核心是法宝流转和叛变因果链，`fengshen-artifacts-and-counter.md` 直接覆盖番天印、阴阳镜及克制关系；`fengshen-major-battles.md` 直接覆盖殷郊殷洪叛变经过和殷郊死因；`fengshen-character-profiles.md` 作为人物图鉴交叉确认二人身份和结局。封神榜名录、门派体系、异文记录不是本题必要证据。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-artifacts-and-counter.md` | `ch_2_3` / `番天印` | L35-L40 | 定位番天印原持有者、功能、流转与殷郊叛变实战 |
| `fengshen-artifacts-and-counter.md` | `ch_2_7` / `阴阳镜` | L56-L61 | 定位阴阳镜持有者、功能、流转与殷洪叛变实战 |
| `fengshen-artifacts-and-counter.md` | `ch_5` / `法宝克制关系总览` | L88-L98 | 定位四方旗克制番天印及太极图克制阴阳镜 |
| `fengshen-major-battles.md` | `ch_7_1` / `殷洪叛变` | L93-L96 | 定位殷洪受蛊惑叛变、使用阴阳镜和被太极图收服 |
| `fengshen-major-battles.md` | `ch_7_2` / `殷郊叛变` | L97-L100 | 定位殷郊获授番天印、叛变、四方旗克制和死因 |
| `fengshen-major-battles.md` | `ch_7_3` / `因果链` | L101-L103 | 定位殷洪之死触发殷郊叛变及殷郊应誓而死的因果链 |
| `fengshen-character-profiles.md` | `ch_3_1` / `殷洪` | L82-L89 | 交叉确认殷洪身份、师承、叛变和死因 |
| `fengshen-character-profiles.md` | `ch_3_2` / `殷郊` | L90-L97 | 交叉确认殷郊身份、师承、番天印、四方旗和死因 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-artifacts-and-counter.md` | L30-L40 | 戊己杏黄旗可抵挡番天印；番天印原持有者为广成子，是威力极强的攻击型法宝，广成子传给弟子殷郊，殷郊叛变后以此印重创周营，广成子本人无法正面对抗 |
| `fengshen-artifacts-and-counter.md` | L56-L60 | 阴阳镜持有者为赤精子，白面照生、红面照死，传给弟子殷洪，殷洪叛变后以此镜对抗周营 |
| `fengshen-artifacts-and-counter.md` | L88-L98 | 克制关系表明番天印需四方旗（戊己杏黄旗、素色云界旗、离地焰光旗、青莲宝色旗）合力抵消威力；殷郊番天印被广成子借四方旗克制；殷洪阴阳镜被太极图收服 |
| `fengshen-major-battles.md` | L91-L103 | 殷洪被赤精子收为弟子并传以阴阳镜，受申公豹蛊惑助商，最终被太极图收服化为飞灰；殷郊获授番天印，得知殷洪被杀后叛变，以番天印重创周营，最终广成子借四方旗合力克制番天印，殷郊应誓被犁锄而死 |
| `fengshen-character-profiles.md` | L80-L96 | 殷洪为纣王次子、赤精子弟子，反叛助商后被太极图所杀；殷郊为纣王长子、广成子弟子，执番天印重创周营，被四方旗所制，应誓被犁锄而死 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录；实际检查中 `.kb/memory/` 目录不存在 |
| `doc_001.jsonl` | 不存在 |
| `doc_005.jsonl` | 不存在 |
| `doc_002.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 殷郊叛变使用的法宝 | 番天印 | 法宝文档写明殷郊叛变后以番天印重创周营；战役文档写明殷郊以番天印重创周营 |
| 番天印原持有者 | 广成子 | 法宝文档写明“原持有者：广成子”；战役与人物文档均说明殷郊为广成子弟子并获授番天印 |
| 需要四件法宝克制的原因 | 番天印威力极强，广成子也无法正面对抗；克制表记录必须由四方旗合力抵消其威力 | 法宝文档写明番天印“威力极强”“广成子本人也无法正面对抗”，克制表写明“四旗合力抵消番天印威力” |
| 殷郊死因 | 应誓被犁锄而死 | 战役文档写明殷郊应誓被犁锄而死；人物图鉴写明被四方旗所制，应誓被犁锄而死 |
| 殷洪叛变使用的法宝 | 阴阳镜 | 法宝文档写明阴阳镜传给弟子殷洪，殷洪叛变后以此镜对抗周营；战役文档写明赤精子传殷洪阴阳镜 |

最终答案：殷郊叛变时使用的是番天印。番天印原本属于广成子，后来由广成子传给弟子殷郊助其下山；殷郊叛变后以番天印重创周营。克制番天印需要四方旗，是因为源文把番天印描述为“威力极强”的攻击型法宝，且广成子本人也无法正面对抗；克制关系表明确写明要用戊己杏黄旗、素色云界旗、离地焰光旗、青莲宝色旗四旗合力，才能抵消番天印威力。殷郊最终被四方旗所制，应誓被犁锄而死。殷郊的弟弟殷洪叛变时使用阴阳镜；阴阳镜原为赤精子法宝，传给弟子殷洪，殷洪叛变后以此镜对抗周营，最终被太极图收服，连人带马化为飞灰。

引用：

- Source: `doc_001` `ch_2_3` `fengshen-artifacts-and-counter.md#L35-L39`
- Source: `doc_001` `ch_2_7` `fengshen-artifacts-and-counter.md#L56-L60`
- Source: `doc_001` `ch_5` `fengshen-artifacts-and-counter.md#L90-L97`
- Source: `doc_005` `ch_7_1` `fengshen-major-battles.md#L93-L95`
- Source: `doc_005` `ch_7_2` `fengshen-major-battles.md#L97-L99`
- Source: `doc_002` `ch_3_1` / `ch_3_2` `fengshen-character-profiles.md#L82-L96`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 殷郊叛变时使用番天印 | 通过 | `fengshen-artifacts-and-counter.md#L38-L39`; `fengshen-major-battles.md#L99-L99`; `fengshen-character-profiles.md#L94-L95` |
| 番天印原持有者是广成子 | 通过 | `fengshen-artifacts-and-counter.md#L35-L38`; `fengshen-character-profiles.md#L92-L95` |
| 番天印威力极强，广成子本人无法正面对抗 | 通过 | `fengshen-artifacts-and-counter.md#L36-L39`; `fengshen-major-battles.md#L99-L99` |
| 四方旗为戊己杏黄旗、素色云界旗、离地焰光旗、青莲宝色旗，四旗合力抵消番天印威力 | 通过 | `fengshen-artifacts-and-counter.md#L93-L93`; `fengshen-major-battles.md#L99-L99` |
| 殷郊最终应誓被犁锄而死 | 通过 | `fengshen-major-battles.md#L99-L103`; `fengshen-character-profiles.md#L96-L96` |
| 殷洪叛变时使用阴阳镜 | 通过 | `fengshen-artifacts-and-counter.md#L56-L60`; `fengshen-major-battles.md#L93-L95` |
| 阴阳镜原为赤精子持有并传给弟子殷洪 | 通过 | `fengshen-artifacts-and-counter.md#L57-L60`; `fengshen-major-battles.md#L95-L95` |
| 殷洪最终被太极图收服，连人带马化为飞灰 | 通过 | `fengshen-major-battles.md#L95-L95`; `fengshen-character-profiles.md#L87-L88` |

自检结论：已回答题目所有问点；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q6 标准答案进行对比，结果一致：番天印、广成子、四方旗合力抵消、犁锄而死、阴阳镜、赤精子和太极图收服等关键事实均匹配。

## 本次单题执行更新：Q7

更新时间：2026-08-10。

问题：申公豹原本属于哪个教派？他的师父是谁？他与姜子牙是什么关系？他后来做了什么？他最终的封号是什么？这个封号与一般受封有何不同？

结论：

| 问点 | 答案 |
|---|---|
| 申公豹原本属于哪个教派 | 阐教 |
| 他的师父是谁 | 元始天尊 |
| 他与姜子牙是什么关系 | 同门，二人同为元始天尊弟子；人物图鉴中“姜尚”即姜子牙 |
| 他后来做了什么 | 因与姜子牙 / 姜尚理念不合转而助商，骑白额虎，游说各方仙人下山助商，四处挑拨，是封神大战的重要推手；并曾蛊惑殷洪叛变 |
| 最终封号 | 东海分水将军 |
| 与一般受封有何不同 | 虽有封号，但实为被罚填北海眼，与一般受封性质不同，是惩罚性质而非普通封神受职 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-factions-and-lineage.md` | `doc_004` | 标题为“封神演义门派体系与师承谱系”；摘要说明阐教、截教组织结构和师承关系树；tags 含“阐教”“元始天尊”“姜子牙”“申公豹”“师承关系”“师承树”“助商” | 确认申公豹原属阐教、师父为元始天尊、与姜子牙同门，以及后来助商、游说截教门人 |
| `fengshen-character-profiles.md` | `doc_002` | 标题为“封神演义核心人物图鉴”；摘要包含姜子牙、申公豹等人物生平；tags 含“姜尚”“元始天尊”“申公豹”“阐教弟子”“白额虎”“游说助商”“道友请留步”“封神大战推手” | 交叉确认姜尚即姜子牙，并提取申公豹人物行为细节 |
| `fengshen-deification-list.md` | `doc_003` | 标题为“封神演义封神榜名录”；摘要覆盖封位与未入榜者；tags 含“申公豹”“东海分水将军”“北海眼” | 确认申公豹最终封号和该封号的惩罚性质 |
| `fengshen-major-battles.md` | `doc_005` | 标题为“封神演义重大战役纪事”；摘要含殷郊殷洪叛变因果链；tags 含“申公豹蛊惑”“殷洪叛变” | 补充确认申公豹曾蛊惑殷洪叛变这一具体行为 |

路由判断：本题涉及申公豹从阐教弟子到助商、再到封号惩罚的跨文档追踪。`fengshen-factions-and-lineage.md` 提供师承和教派主证据；`fengshen-character-profiles.md` 提供人物行为和“姜尚”消歧；`fengshen-deification-list.md` 提供最终封号与惩罚性质；`fengshen-major-battles.md` 补充具体蛊惑殷洪事件。法宝谱、异文记录不是本题必要证据。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-factions-and-lineage.md` | `ch_2_1` / `教主与道场` | L17-L20 | 定位元始天尊为阐教教主 |
| `fengshen-factions-and-lineage.md` | `ch_2_3` / `其他阐教重要人物` | L40-L47 | 定位申公豹原为元始天尊弟子、与姜子牙同门、后助商 |
| `fengshen-factions-and-lineage.md` | `ch_3_3` / `截教其他重要门人` | L63-L70 | 定位申公豹原阐教后助截教、四处挑拨仙人助商 |
| `fengshen-factions-and-lineage.md` | `ch_4` / `师承关系速查` | L71-L107 | 定位师承树中元始天尊下有姜子牙与申公豹 |
| `fengshen-character-profiles.md` | `ch_1_1` / `姜子牙` | L9-L18 | 定位姜子牙本名姜尚、拜元始天尊为师 |
| `fengshen-character-profiles.md` | `ch_2_4` / `申公豹` | L72-L79 | 定位申公豹人物详情、同师元始天尊、助商、游说与挑拨 |
| `fengshen-deification-list.md` | `ch_12` / `其他重要封位` | L96-L101 | 定位申公豹封东海分水将军、被填北海眼 |
| `fengshen-deification-list.md` | `ch_14` / `未入封神榜者` | L114-L121 | 定位申公豹虽封东海分水将军但实为被罚填北海眼，与一般受封性质不同 |
| `fengshen-major-battles.md` | `ch_7_1` / `殷洪叛变` | L93-L96 | 定位申公豹蛊惑殷洪叛变 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-factions-and-lineage.md` | L15-L47 | 元始天尊为阐教教主；申公豹原为元始天尊弟子，与姜子牙同门，后因理念分歧转为助商，四处游说截教门人下山参战 |
| `fengshen-factions-and-lineage.md` | L63-L70 | 申公豹原阐教弟子后助截教，骑白额虎，四处挑拨各方仙人下山助商 |
| `fengshen-factions-and-lineage.md` | L71-L107 | 师承树列出元始天尊（阐教）下有姜子牙、申公豹，并标注申公豹后叛出助商 |
| `fengshen-character-profiles.md` | L9-L18 | 姜子牙本名姜尚，三十二岁上昆仑山拜元始天尊为师 |
| `fengshen-character-profiles.md` | L72-L78 | 申公豹原阐教弟子，与姜尚同师元始天尊；骑白额虎；因与姜尚理念不合转而助商，游说各方仙人下山助商，“道友请留步”是标志性话语，四处挑拨，是封神大战的重要推手 |
| `fengshen-deification-list.md` | L96-L101 | 申公豹封东海分水将军，原阐教弟子，游说各方助商，封神后被填北海眼 |
| `fengshen-deification-list.md` | L114-L121 | 申公豹虽封东海分水将军，但实为被罚填北海眼，与一般受封性质不同 |
| `fengshen-major-battles.md` | L91-L103 | 殷洪途中受申公豹蛊惑，转而助商；因果链也记录“申公豹蛊惑殷洪” |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录；实际检查中 `.kb/memory/` 目录不存在 |
| `doc_004.jsonl` | 不存在 |
| `doc_002.jsonl` | 不存在 |
| `doc_003.jsonl` | 不存在 |
| `doc_005.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 原属教派 | 阐教 | 门派文档写明申公豹原为元始天尊弟子，人物图鉴写明“原阐教弟子” |
| 师父 | 元始天尊 | 门派文档写明申公豹原为元始天尊弟子；师承树列在元始天尊（阐教）之下 |
| 与姜子牙关系 | 同门，同师元始天尊 | 门派文档写明与姜子牙同门；人物图鉴写明与姜尚同师元始天尊，且姜子牙本名姜尚 |
| 后来行为 | 因理念不合助商，骑白额虎，游说各方仙人下山助商，四处挑拨，是封神大战重要推手，并曾蛊惑殷洪叛变 | 门派文档和人物图鉴记录助商、游说、挑拨；战役文档记录殷洪受申公豹蛊惑 |
| 最终封号 | 东海分水将军 | 封神榜名录写明“申公豹：东海分水将军” |
| 与一般受封不同 | 实为被罚填北海眼，与一般受封性质不同 | 封神榜名录写明“虽封东海分水将军，但实为被罚填北海眼，与一般受封性质不同” |

最终答案：申公豹原本属于阐教；他的师父是元始天尊。申公豹与姜子牙是同门，二人同为元始天尊弟子；人物图鉴中说申公豹“与姜尚同师元始天尊”，而姜子牙本名姜尚，所以这里的姜尚就是姜子牙。后来申公豹因与姜子牙理念不合转而助商，骑白额虎，游说各方仙人下山助商，四处挑拨，是封神大战的重要推手；在殷洪事件中，他还蛊惑殷洪转而助商。申公豹最终封号是东海分水将军，但这个封号与一般受封不同：文档明确说他虽封东海分水将军，实为被罚填北海眼，因此是惩罚性质，不是普通的受封任职。

引用：

- Source: `doc_004` `ch_2_1` / `ch_2_3` `fengshen-factions-and-lineage.md#L19-L46`
- Source: `doc_004` `ch_3_3` `fengshen-factions-and-lineage.md#L63-L68`
- Source: `doc_004` `ch_4` `fengshen-factions-and-lineage.md#L75-L81`
- Source: `doc_002` `ch_1_1` `fengshen-character-profiles.md#L11-L14`
- Source: `doc_002` `ch_2_4` `fengshen-character-profiles.md#L72-L78`
- Source: `doc_003` `ch_12` `fengshen-deification-list.md#L96-L101`
- Source: `doc_003` `ch_14` `fengshen-deification-list.md#L114-L121`
- Source: `doc_005` `ch_7_1` `fengshen-major-battles.md#L93-L95`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 申公豹原本属于阐教 | 通过 | `fengshen-character-profiles.md#L74-L74`; `fengshen-factions-and-lineage.md#L46-L46`; `fengshen-deification-list.md#L100-L100` |
| 申公豹师父是元始天尊 | 通过 | `fengshen-factions-and-lineage.md#L46-L46`; `fengshen-factions-and-lineage.md#L78-L81`; `fengshen-character-profiles.md#L74-L74` |
| 申公豹与姜子牙是同门 | 通过 | `fengshen-factions-and-lineage.md#L45-L46`; `fengshen-factions-and-lineage.md#L78-L81` |
| 人物图鉴中的姜尚即姜子牙 | 通过 | `fengshen-character-profiles.md#L11-L14` |
| 申公豹后来转而助商、游说各方仙人下山助商、四处挑拨 | 通过 | `fengshen-factions-and-lineage.md#L46-L46`; `fengshen-factions-and-lineage.md#L67-L67`; `fengshen-character-profiles.md#L76-L78` |
| 申公豹曾蛊惑殷洪转而助商 | 通过 | `fengshen-major-battles.md#L95-L95`; `fengshen-major-battles.md#L103-L103` |
| 申公豹最终封号是东海分水将军 | 通过 | `fengshen-deification-list.md#L100-L100`; `fengshen-deification-list.md#L121-L121` |
| 该封号实为被罚填北海眼，与一般受封性质不同 | 通过 | `fengshen-deification-list.md#L100-L100`; `fengshen-deification-list.md#L121-L121` |

自检结论：已回答题目所有问点；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q7 标准答案进行对比，结果一致：阐教、元始天尊、与姜子牙同门、助商游说、蛊惑殷洪、东海分水将军、被罚填北海眼和惩罚性质均匹配。

## 本次单题执行更新：Q8

更新时间：2026-08-10。

问题：将以下六场战役按发生先后排列：九曲黄河阵之战、万仙阵之战、十绝阵之战、诛仙阵之战、绝龙岭之战、赵公明之死。哪场战役直接导致了十二金仙修为大损？修为大损后对后续参战有何影响？

结论：

| 问点 | 答案 |
|---|---|
| 六场战役发生先后 | 十绝阵之战 → 绝龙岭之战 → 赵公明之死 → 九曲黄河阵之战 → 诛仙阵之战 → 万仙阵之战 |
| 哪场战役直接导致十二金仙修为大损 | 九曲黄河阵之战 |
| 修为大损后对后续参战有何影响 | 十二金仙虽被救出，但修为大损，此后不再以全盛状态参战；后续诛仙阵、万仙阵中均依赖四位圣人合力破阵或合力参战 |

### Step 1 Document routing

执行说明：本题使用 `../../../fixtures/fengshen-kb/.kb/manifest.json`。本题没有用户显式提供 `domain_preference`，且目标知识库未发现 `.kb/memory/route_preferences.json`。

| 命中文档 | doc_id | manifest 匹配点 | 用途 |
|---|---|---|---|
| `fengshen-major-battles.md` | `doc_005` | 标题为“封神演义重大战役纪事”；摘要说明依原著顺序记述十绝阵、绝龙岭、九曲黄河阵、诛仙阵、万仙阵等重大战役；tags 含“十绝阵”“绝龙岭”“赵公明之死”“九曲黄河阵”“十二金仙修为大损”“诛仙阵”“万仙阵”“四圣人合力” | 确认六场战役时序，判断九曲黄河阵导致十二金仙修为大损，并提取后续参战影响 |

路由判断：本题要求对六场战役排序，并判断十二金仙修为大损的直接战役及后续影响。`fengshen-major-battles.md` 在 manifest 中明确“依原著顺序”记述相关战役，且其 tags 覆盖全部战役名、修为大损和四圣合力，因此足以独立回答。人物、法宝、封神榜、门派和异文文档不是本题必要证据。

### Step 2 Section localization

| 文档 | 命中节点 | 源行锚 | 用途 |
|---|---|---:|---|
| `fengshen-major-battles.md` | `ch_1` / `十绝阵之战` | L5-L27 | 定位六场战役中的第一场及其结果 |
| `fengshen-major-battles.md` | `ch_2` / `绝龙岭之战` | L28-L33 | 定位第二场战役 |
| `fengshen-major-battles.md` | `ch_3` / `赵公明之死` | L34-L39 | 定位第三个事件及其引出九曲黄河阵的因果 |
| `fengshen-major-battles.md` | `ch_4` / `九曲黄河阵之战` | L40-L53 | 定位第四场战役、十二金仙修为被削和后续影响 |
| `fengshen-major-battles.md` | `ch_5` / `诛仙阵之战` | L54-L74 | 定位第五场战役及四圣合力破阵 |
| `fengshen-major-battles.md` | `ch_6` / `万仙阵之战` | L75-L90 | 定位第六场战役及四圣再次合力、十二金仙参战 |

### Step 3 Content extraction

| 实际读取文件 | 行段 | 提取事实 |
|---|---:|---|
| `fengshen-major-battles.md` | L1-L4 | 文档说明“依原著顺序”记述各次重大战役，战役之间存在因果关联 |
| `fengshen-major-battles.md` | L5-L27 | 十绝阵之战为本题六场中最早，十绝阵全破后闻仲退守绝龙岭 |
| `fengshen-major-battles.md` | L28-L33 | 绝龙岭之战发生在闻仲退至绝龙岭后，闻仲被通天神火柱烧死 |
| `fengshen-major-battles.md` | L34-L39 | 赵公明之死发生在绝龙岭之后，并直接引发三霄娘娘复仇，成为九曲黄河阵之战的直接动因 |
| `fengshen-major-battles.md` | L40-L53 | 九曲黄河阵之战中，三霄以混元金斗困住十二金仙，削去顶上三花、胸中五气，千年修为尽数废去；十二金仙虽被救出但修为大损，此后不再以全盛状态参战 |
| `fengshen-major-battles.md` | L54-L74 | 诛仙阵之战发生在九曲黄河阵之后，元始天尊、太上老君、接引道人、准提道人四圣合力破阵 |
| `fengshen-major-battles.md` | L75-L90 | 万仙阵之战发生在诛仙阵破后，四圣再次合力，阐教十二金仙等悉数参战；万仙阵被破后封神大战基本结束 |

### Step 4 Correction loading

| 检查位置 | 结果 |
|---|---|
| `.kb/memory/corrections/` | 不存在 correction 目录；实际检查中 `.kb/memory/` 目录不存在 |
| `doc_005.jsonl` | 不存在 |

结论：未加载到与当前问题相关的 correction；最终答案仅基于 Step 3 已读取源文。

### Step 5 Generate answer

| 判断项 | 结论 | 判断依据 |
|---|---|---|
| 战役顺序依据 | 按 `fengshen-major-battles.md` 的章节顺序排列 | 源文说明本文依原著顺序记述各次重大战役 |
| 六场战役顺序 | 十绝阵之战 → 绝龙岭之战 → 赵公明之死 → 九曲黄河阵之战 → 诛仙阵之战 → 万仙阵之战 | 六个章节标题依次出现在 L5、L28、L34、L40、L54、L75 |
| 直接导致十二金仙修为大损的战役 | 九曲黄河阵之战 | 该章节写明三霄以混元金斗困住十二金仙，削去三花五气，千年修为尽数废去 |
| 修为大损后的影响 | 十二金仙此后不再以全盛状态参战 | 九曲黄河阵结果写明“十二金仙虽被救出，但修为大损，此后不再以全盛状态参战” |
| 后续战役体现 | 诛仙阵由四圣合力破阵；万仙阵四圣再次合力，十二金仙等悉数参战 | 诛仙阵章节写明四圣合力破阵；万仙阵章节写明四圣再次合力，十二金仙等悉数参战 |

最终答案：按发生先后排列，六场战役依次是：十绝阵之战、绝龙岭之战、赵公明之死、九曲黄河阵之战、诛仙阵之战、万仙阵之战。直接导致十二金仙修为大损的是九曲黄河阵之战；三霄以混元金斗困住阐教十二金仙，削去其顶上三花、胸中五气，使千年修为尽数废去。修为大损后的影响是：十二金仙虽被救出，但此后不再以全盛状态参战；在后续诛仙阵中由元始天尊、太上老君、接引道人、准提道人四圣合力破阵，在万仙阵中也是四圣再次合力，十二金仙虽参战但已不是全盛状态。

引用：

- Source: `doc_005` `ch_1` `fengshen-major-battles.md#L5-L27`
- Source: `doc_005` `ch_2` `fengshen-major-battles.md#L28-L33`
- Source: `doc_005` `ch_3` `fengshen-major-battles.md#L34-L39`
- Source: `doc_005` `ch_4` `fengshen-major-battles.md#L40-L53`
- Source: `doc_005` `ch_5` `fengshen-major-battles.md#L54-L74`
- Source: `doc_005` `ch_6` `fengshen-major-battles.md#L75-L90`

### Step 6 Self-verify

| 断言 | 核验 | 来源 |
|---|---|---|
| 本文依原著顺序记述各次重大战役，可用章节顺序判断本题六场时序 | 通过 | `fengshen-major-battles.md#L3-L3` |
| 十绝阵之战在六场中最早 | 通过 | `fengshen-major-battles.md#L5-L26` |
| 绝龙岭之战发生在十绝阵之后 | 通过 | `fengshen-major-battles.md#L26-L30` |
| 赵公明之死发生在绝龙岭之后，并引出九曲黄河阵 | 通过 | `fengshen-major-battles.md#L34-L38` |
| 九曲黄河阵之战发生在赵公明之死之后 | 通过 | `fengshen-major-battles.md#L38-L44` |
| 诛仙阵之战发生在九曲黄河阵之后 | 通过 | `fengshen-major-battles.md#L54-L58` |
| 万仙阵之战发生在诛仙阵破后 | 通过 | `fengshen-major-battles.md#L73-L79` |
| 九曲黄河阵直接导致十二金仙修为大损 | 通过 | `fengshen-major-battles.md#L48-L52` |
| 修为大损后十二金仙不再以全盛状态参战 | 通过 | `fengshen-major-battles.md#L52-L52` |
| 后续诛仙阵和万仙阵主要依赖四圣合力 | 通过 | `fengshen-major-battles.md#L64-L64`; `fengshen-major-battles.md#L83-L83` |

自检结论：已回答题目所有问点；每个关键断言均可回到已读取源文行段；引用行号真实存在且能支撑断言。源文自检通过后读取题集 `fengshen-hard-rag-questions.md` 的 Q8 标准答案进行对比，结果一致：战役顺序、九曲黄河阵导致修为大损、此后不再以全盛状态参战，以及后续主要依赖四圣合力均匹配。
