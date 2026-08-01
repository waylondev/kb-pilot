import json
from pathlib import Path

fills = {
    'doc_004': {
        'ch_1': {'summary': '公司成立于2015年，总部北京，2800+员工', 'keywords': ['公司简介', '价值观', '总部', '北京', '2015年']},
        'ch_2': {'summary': '入职流程5步，试用期6个月可提前转正', 'keywords': ['入职', '试用期', '转正', '劳动合同', '导师']},
        'ch_2_1': {'summary': '入职需提交材料、签合同、开通权限', 'keywords': ['入职流程', '入职材料', '劳动合同', '培训']},
        'ch_2_2': {'summary': '试用期6个月，薪资80%，考核四维度', 'keywords': ['试用期', '6个月', '转正', '考核', '80%']},
        'ch_3': {'summary': '薪酬=基本工资+绩效+年终+补贴，五险一金', 'keywords': ['薪酬', '绩效', '年终奖', '五险一金', '补贴']},
        'ch_3_1': {'summary': '职级P1-M3，月薪8K-120K，股票期权', 'keywords': ['职级', '薪资', 'P序列', 'M序列', '股票期权', '月薪']},
        'ch_3_2': {'summary': '五险一金12%，补充商业保险，学习基金5000元', 'keywords': ['福利', '五险一金', '公积金', '体检', '年假', '学习基金']},
        'ch_4': {'summary': '弹性工作制10-16点，企业微信打卡，远程办公', 'keywords': ['考勤', '弹性工作', '打卡', '远程办公', '工作时间']},
        'ch_4_1': {'summary': '核心工作时间10-16点，标准8小时', 'keywords': ['工作时间', '弹性', '10:00', '16:00', '午休']},
        'ch_4_2': {'summary': '企业微信打卡，迟到30分钟不计异常', 'keywords': ['打卡', '企业微信', 'GPS', '迟到', '远程办公']},
        'ch_4_3': {'summary': '年假5-15天，婚假10天，产假158天', 'keywords': ['假期', '年假', '婚假', '产假', '陪产假', '丧假']},
        'ch_5': {'summary': '季度考核S/A/B/C/D五级，PIP改进计划', 'keywords': ['绩效', '考核', 'S级', 'PIP', '绩效系数']},
        'ch_5_1': {'summary': '季度考核+年度考核', 'keywords': ['考核周期', '季度考核', '年度考核']},
        'ch_5_2': {'summary': 'S级5%，A级20%，B级60%，C级10%，D级5%', 'keywords': ['绩效等级', 'S级', 'A级', 'B级', 'C级', 'D级', 'PIP']},
        'ch_5_3': {'summary': '晋升评审每年2次，薪资涨幅15-25%', 'keywords': ['晋升', '评审', '3月', '9月', '涨薪', '答辩']},
        'ch_6': {'summary': '新员工培训、技术分享、管理培训、外部培训', 'keywords': ['培训', '技术分享', '管理培训', '职业发展', 'P序列', 'M序列']},
        'ch_6_1': {'summary': '新员工培训、周技术分享、季度管理培训', 'keywords': ['培训体系', '新员工培训', '技术分享', '管理培训', '外部培训']},
        'ch_6_2': {'summary': '管理通道M序列和技术通道P序列双通道发展', 'keywords': ['职业发展', '双通道', 'M序列', 'P序列', '晋升']},
        'ch_7': {'summary': '信息安全规范、违纪四级处分', 'keywords': ['行为规范', '信息安全', '违纪', '处分', '纪律']},
        'ch_7_1': {'summary': '禁止代码外泄，锁定屏幕，使用VPN', 'keywords': ['信息安全', '代码', 'VPN', '社交媒体', '锁定']},
        'ch_7_2': {'summary': '轻微口头警告、一般书面警告、严重记过、重大解除合同', 'keywords': ['违纪', '处分', '警告', '记过', '解除合同', '旷工']},
        'ch_8': {'summary': '正式员工提前30天离职，竞业限制6个月', 'keywords': ['离职', '交接', '竞业限制', '补偿金', '30天']},
        'ch_8_1': {'summary': '离职需提前30天申请，6步流程', 'keywords': ['离职流程', '30天', '交接', '离职证明', '工作交接']},
        'ch_8_2': {'summary': 'P7/M2以上竞业限制6个月，补偿月薪30%', 'keywords': ['竞业限制', 'P7', 'M2', '补偿金', '6个月', '30%']},
        'ch_9': {'summary': '手册由人力资源部解释修订', 'keywords': ['附则', '人力资源部', '修订', 'OA系统']},
    },
    'doc_005': {
        'ch_1': {'summary': '智策企业AI平台，大模型全生命周期管理', 'keywords': ['智策', 'AI平台', '大模型', '云原生', '私有化部署', 'SaaS']},
        'ch_1_1': {'summary': '模型管理、推理服务、数据管道、安全合规、可观测性', 'keywords': ['模型管理', '推理服务', '数据管道', '安全合规', '可观测性']},
        'ch_2': {'summary': '四层微服务架构，接入层/业务层/引擎层/基础设施层', 'keywords': ['系统架构', '微服务', 'Kong', 'Triton', 'Kubernetes', 'PostgreSQL']},
        'ch_2_1': {'summary': '接入层、业务层、引擎层、基础设施层四层架构', 'keywords': ['架构', '四层', 'API Gateway', 'Triton', 'Kubernetes']},
        'ch_2_2': {'summary': '最小8核32G，标准32核128G，高配64核256G', 'keywords': ['部署', '配置', 'CPU', 'GPU', 'A100', '内存']},
        'ch_3': {'summary': '模型管理、推理服务、数据管道、安全四大模块', 'keywords': ['功能模块', '模型管理', '推理', '数据管道', '安全']},
        'ch_3_1': {'summary': '支持PyTorch/TensorFlow/ONNX/TensorRT格式', 'keywords': ['模型管理', 'PyTorch', 'TensorFlow', 'ONNX', 'TensorRT', '注册']},
        'ch_3_2': {'summary': 'Triton引擎，动态批处理，P99延迟<200ms', 'keywords': ['推理服务', 'Triton', 'GPU', '批处理', '延迟', '吞吐']},
        'ch_3_3': {'summary': '数据接入、清洗、特征工程、版本管理、标注', 'keywords': ['数据管道', 'MySQL', 'Kafka', '特征工程', 'DVC', '标注']},
        'ch_3_4': {'summary': 'RBAC权限模型，5种角色，TLS+AES加密', 'keywords': ['安全', 'RBAC', '权限', 'TLS', 'AES', 'BYOK']},
        'ch_4': {'summary': 'API Key和OAuth2.0认证，推理和模型管理接口', 'keywords': ['API', '认证', 'API Key', 'OAuth', '推理', '速率限制']},
        'ch_4_1': {'summary': 'API Key服务间调用，OAuth2.0用户授权', 'keywords': ['认证', 'API Key', 'OAuth', 'Bearer Token']},
        'ch_4_2': {'summary': '推理接口POST /api/v1/inference，模型CRUD接口', 'keywords': ['API接口', '推理', 'POST', '模型管理', '速率限制', 'QPS']},
        'ch_5': {'summary': '可用率99.9%，ELK日志，RPO<1min,RTO<15min', 'keywords': ['运维', '监控', 'ELK', '备份', 'RPO', 'RTO']},
        'ch_5_1': {'summary': '可用率99.9%，P99延迟500ms，GPU利用率告警', 'keywords': ['监控', '可用率', '延迟', 'GPU', '告警', '队列']},
        'ch_5_2': {'summary': '结构化JSON日志，ELK采集，热7天温30天冷180天', 'keywords': ['日志', 'JSON', 'ELK', 'Elasticsearch', 'Logstash', 'Kibana']},
        'ch_5_3': {'summary': '配置每日备份，模型版本化，RPO<1min,RTO<15min', 'keywords': ['备份', '恢复', 'RPO', 'RTO', '灾备', '版本化']},
        'ch_6': {'summary': 'v1.0至v3.2五个版本迭代', 'keywords': ['版本历史', 'v1.0', 'v2.0', 'v3.0', 'v3.2', '多模态']},
        'ch_7': {'summary': '模型加载失败、推理延迟、GPU资源估算FAQ', 'keywords': ['附录', 'FAQ', '常见问题', '模型加载', '延迟', 'GPU']},
        'ch_7_1': {'summary': '模型加载失败、推理延迟、GPU资源估算常见问题', 'keywords': ['常见问题', '模型加载', 'SHA256', '延迟', 'GPU', '显存']},
    },
    'doc_006': {
        'ch_1': {'summary': '依据网络安全法、数据安全法、个保法制定', 'keywords': ['总则', '网络安全法', '数据安全法', '个人信息保护法', '方针']},
        'ch_2': {'summary': 'L1-L4四级资产分级，个人/商业/技术/财务四类数据', 'keywords': ['资产分类', '分级', 'L1', 'L4', '个人数据', '商业数据']},
        'ch_2_1': {'summary': 'L1公开L2内部L3敏感L4机密，加密要求递增', 'keywords': ['资产分级', 'L1', 'L2', 'L3', 'L4', '加密']},
        'ch_2_2': {'summary': '个人数据、商业数据、技术数据、财务数据四类', 'keywords': ['数据分类', '个人数据', '商业数据', '技术数据', '财务数据']},
        'ch_3': {'summary': '密码12位90天换，最小权限原则，特权账号双人复核', 'keywords': ['访问控制', '密码', '权限', '特权账号', '双人复核', '最小权限']},
        'ch_3_1': {'summary': '企业邮箱注册，密码12位90天强制修改', 'keywords': ['账号管理', '密码', '12位', '90天', '禁用', '外包']},
        'ch_3_2': {'summary': '最小权限原则，特权账号不超过5个，季度审计', 'keywords': ['权限管理', '最小权限', '特权账号', 'DBA', '审计', '审批']},
        'ch_4': {'summary': 'DMZ/应用/数据三区隔离，VPN远程，IDS/IPS入侵检测', 'keywords': ['网络安全', 'DMZ', '防火墙', 'VPN', 'IDS', 'IPS']},
        'ch_4_1': {'summary': 'DMZ区、应用区、数据区三区防火墙隔离', 'keywords': ['网络分区', 'DMZ', '应用区', '数据区', '防火墙']},
        'ch_4_2': {'summary': 'VPN远程访问，禁止公共WiFi，堡垒机录屏审计', 'keywords': ['远程访问', 'VPN', '堡垒机', '公共WiFi', '录屏']},
        'ch_4_3': {'summary': 'IDS/IPS实时监控，端口扫描、SQL注入、暴力破解告警', 'keywords': ['入侵检测', 'IDS', 'IPS', '端口扫描', 'SQL注入', '暴力破解']},
        'ch_5': {'summary': 'TLS1.3传输加密，AES-256存储加密，Vault密钥管理', 'keywords': ['数据安全', 'TLS', 'AES', 'Vault', '脱敏', '备份']},
        'ch_5_1': {'summary': 'TLS1.3全链路加密，TDE数据库加密，Vault 90天轮换', 'keywords': ['加密', 'TLS', 'TDE', 'AES-256', 'Vault', 'BitLocker']},
        'ch_5_2': {'summary': '日志/测试/开发环境禁止明文敏感数据', 'keywords': ['脱敏', '手机号', '身份证', '银行卡', '邮箱']},
        'ch_5_3': {'summary': '数据库每日全量+每小时增量，RPO<1min,RTO<15min', 'keywords': ['备份', '全量', '增量', '异地', 'RPO', 'RTO']},
        'ch_6': {'summary': '四级安全事件，一至四级响应时间2h/30min/15min/立即', 'keywords': ['安全事件', '分级', '响应', '上报', '应急处置', '根因分析']},
        'ch_6_1': {'summary': '一级2h二级30min三级15min四级立即响应', 'keywords': ['事件分级', '一级', '二级', '三级', '四级', '响应时间', '上报']},
        'ch_6_2': {'summary': '发现→判断→处置→根因分析→恢复→改进六步流程', 'keywords': ['响应流程', '发现', '处置', '根因分析', '恢复', '改进']},
        'ch_6_3': {'summary': '个人信息泄露72小时内报告监管', 'keywords': ['数据泄露', '通知', '72小时', '个人信息保护法', '监管']},
        'ch_7': {'summary': '季度内部审计，ISO27001年审，等保三级测评', 'keywords': ['合规', '审计', 'ISO27001', '等保', 'SOC2', '网络安全法']},
        'ch_7_1': {'summary': '每季度内部安全审计，纳入绩效考核', 'keywords': ['内部审计', '季度', '访问日志', '权限', '绩效']},
        'ch_7_2': {'summary': 'ISO27001年审，等保三级年测，SOC2审计中', 'keywords': ['外部审计', 'ISO27001', '等保三级', 'SOC2', '认证']},
        'ch_7_3': {'summary': '网络安全法、数据安全法、个保法、ISO27001、等保合规', 'keywords': ['合规要求', '网络安全法', '数据安全法', '个保法', 'ISO27001', '等保']},
        'ch_8': {'summary': '全员每年1次安全培训，开发每半年1次，季度钓鱼演练', 'keywords': ['安全培训', '全员', '开发', 'OWASP', '钓鱼', '考试']},
        'ch_9': {'summary': '第三方须签NDA和DPA，年度安全评估', 'keywords': ['第三方', 'NDA', 'DPA', '供应商', '安全评估', '临时账号']},
        'ch_10': {'summary': '制度由信息安全部解释修订，30日内宣贯', 'keywords': ['附则', '信息安全部', '宣贯', '自查']},
    },
    'doc_007': {
        'ch_1': {'summary': 'PMBOK+敏捷，覆盖产品研发/客户交付/内部改进', 'keywords': ['总则', 'PMBOK', '敏捷', '项目管理', '制度']},
        'ch_2': {'summary': 'A/B/C/D四类项目，P0-P3四级优先级', 'keywords': ['项目分类', 'A类', 'B类', 'C类', 'D类', '优先级', 'P0']},
        'ch_2_1': {'summary': 'A类战略6-12月，B类重要3-6月，C类一般1-3月，D类维护', 'keywords': ['项目类型', '战略', '客户交付', '功能迭代', 'bug修复', '审批']},
        'ch_2_2': {'summary': 'P0紧急立即响应，P1高优先，P2中正常，P3低空闲执行', 'keywords': ['优先级', 'P0', 'P1', 'P2', 'P3', '资源保障', '紧急']},
        'ch_3': {'summary': '立项五步：需求→可行性→评审→资源→启动会', 'keywords': ['立项', '需求', '可行性', '评审', '项目章程', '里程碑']},
        'ch_3_1': {'summary': '需求提出→可行性分析→立项评审→资源分配→启动会', 'keywords': ['立项流程', '需求', '可行性', '评审', '启动会', '项目章程']},
        'ch_3_2': {'summary': '项目建议书、技术方案、资源计划、里程碑计划', 'keywords': ['立项材料', '建议书', '技术方案', '资源计划', '里程碑']},
        'ch_4': {'summary': 'Scrum框架，2周迭代，Jira需求管理', 'keywords': ['项目执行', 'Scrum', '迭代', 'Jira', 'Story', 'Sprint']},
        'ch_4_1': {'summary': 'Sprint Planning、Daily Standup、Review、Retrospective', 'keywords': ['敏捷开发', 'Scrum', 'Sprint', '站会', 'Review', 'Retro']},
        'ch_4_2': {'summary': 'Epic/Story/Task/Bug四级需求，Fibonacci估算', 'keywords': ['需求管理', 'Jira', 'Epic', 'Story', 'Task', 'Bug', 'Fibonacci']},
        'ch_4_3': {'summary': 'main/release/develop/feature分支策略，Conventional Commits', 'keywords': ['代码管理', '分支', 'main', 'develop', 'Code Review', 'Squash Merge']},
        'ch_5': {'summary': '单元测试80%覆盖，S1-S4四级缺陷，灰度发布', 'keywords': ['质量', '测试', '单元测试', '缺陷', '灰度', '发布']},
        'ch_5_1': {'summary': '单元测试≥80%，集成测试核心链路，功能测试全量用例', 'keywords': ['测试策略', '单元测试', '集成测试', '功能测试', '性能测试', '安全测试']},
        'ch_5_2': {'summary': 'S1致命2h修复，S2严重24h，S3一般3天，S4轻微下迭代', 'keywords': ['缺陷管理', 'S1', 'S2', 'S3', 'S4', '修复时限', '致命']},
        'ch_5_3': {'summary': '周二四发布窗口，紧急发布P0随时，灰度10%，15min回滚', 'keywords': ['发布管理', '发布窗口', '灰度', '回滚', '紧急发布', '审批']},
        'ch_6': {'summary': 'Top10风险每迭代更新，五类常见风险及应对', 'keywords': ['风险管理', '风险识别', '应对策略', '规避', '转移', '减轻']},
        'ch_6_1': {'summary': '每迭代更新Top10风险登记册', 'keywords': ['风险识别', 'Top10', '概率', '影响', '应对策略', '责任人']},
        'ch_6_2': {'summary': '人员/技术/需求/进度/外部依赖五类风险应对', 'keywords': ['风险应对', '人员', '技术', '需求', '进度', '外部依赖']},
        'ch_7': {'summary': '每日站会、周报、迭代评审、月度汇报、季度复盘', 'keywords': ['沟通', '站会', '周报', '评审', '汇报', '复盘']},
        'ch_7_1': {'summary': '每日站会/周报/迭代评审/月度汇报/季度复盘', 'keywords': ['沟通机制', '站会', '周报', '迭代评审', '月度汇报', '季度复盘']},
        'ch_7_2': {'summary': '本周完成、下周计划、风险阻塞、关键指标', 'keywords': ['周报', '模板', '完成', '计划', '风险', '指标']},
        'ch_8': {'summary': '交付验收→复盘→归档→资源释放→关闭', 'keywords': ['收尾', '验收', '复盘', '归档', '资源释放', 'Jira']},
        'ch_8_1': {'summary': '交付验收、项目复盘、文档归档、资源释放、项目关闭', 'keywords': ['收尾流程', '验收', '复盘', '归档', '资源释放', '关闭']},
        'ch_8_2': {'summary': 'What went well/wrong/learned/Action items四维度复盘', 'keywords': ['复盘', '模板', '经验', '教训', '改进', 'Action']},
        'ch_9': {'summary': '按时交付30%、质量25%、预算20%、满意度15%、合规10%', 'keywords': ['考核', 'KPI', '交付率', '质量', '预算', '满意度', '奖金']},
        'ch_9_1': {'summary': '按时交付率≥90%，质量合格率≥95%，预算偏差≤10%', 'keywords': ['考核指标', '交付率', '质量', '预算', '满意度', '合规']},
        'ch_9_2': {'summary': '按时交付项目奖金5%，连续延期需改进计划', 'keywords': ['奖惩', '项目奖金', '延期', '改进计划', '优秀项目']},
        'ch_10': {'summary': 'PMBOK/Scrum/MVP/PoC/RACI术语表，Jira/飞书/GitLab工具', 'keywords': ['附录', '术语', 'PMBOK', 'Scrum', 'MVP', 'Jira', 'GitLab']},
        'ch_10_1': {'summary': 'PMBOK、Scrum、MVP、PoC、RACI等术语', 'keywords': ['术语表', 'PMBOK', 'Scrum', 'MVP', 'PoC', 'RACI']},
        'ch_10_2': {'summary': 'Jira项目管理和飞书文档协作工具', 'keywords': ['工具', 'Jira', '飞书', 'GitLab', 'CI/CD', 'ArgoCD']},
    },
}

dir_map = {'doc_004': '03_人力资源', 'doc_005': '02_技术研发', 'doc_006': '04_合规安全', 'doc_007': '05_项目管理'}

for doc_id, fill in fills.items():
    tree_files = list(Path('knowledge_repo/docs').glob(f'{dir_map[doc_id]}/{doc_id}_*/tree.json'))
    if not tree_files:
        print(f'NOT FOUND: {doc_id}')
        continue
    tp = tree_files[0]
    tree = json.loads(tp.read_text(encoding='utf-8'))
    
    def fill_node(node):
        nid = node['id']
        if nid in fill:
            node['summary'] = fill[nid]['summary']
            node['keywords'] = fill[nid]['keywords']
        for child in node.get('children', []):
            fill_node(child)
    
    for node in tree['nodes']:
        fill_node(node)
    
    tp.write_text(json.dumps(tree, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Filled: {tp} ({len(fill)} nodes)')