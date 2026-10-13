# 相比普通Auto的后端改动

| 模块 | 已落地改动 | 源码 |
| --- | --- | --- |
| Goal API和持久化 | goals/goal_phases/goal_deliveries、活动阶段、真实进度、控制去重与取消；目标长于单次run | main.py、schemas.py、store.py |
| 阶段编排 | PLAN先返回；首阶段先交付；未来阶段预选并合成开场语；推进校验、激活缓存或重选 | goals.py |
| 连续Agent链 | 保存previous_response_id与工具ACK；计划与选歌是同一链；检索可多次往返、工具并行 | agent.py、goals.py |
| 阶段材料合并 | 不走普通Auto独立generate_assessment；submit_selection同时返回音乐、energy、openingText与postReceiptText | run_goal_task、submit_selection_tool_schema |
| 去重和可播验证 | 按canonical carrier/service song去重整首（含九轨/别名）；真实资源校验；未用资源实际耗尽才允许重复；topK 1–5，最多4轮补检索 | agent.py、catalog.py、resource_validation.py、resource_auth.py |
| 回执与语音 | 主候选playing回执复用预生成短句，异常候选/兼容路径再解释；失败/降级无TTS | agent.py、goals.py、tts.py |

## 检索范围

普通Auto有可信Touchpad时偏好内部九轨，但可并行全库比较。普通Refine有Touchpad限定同曲内部，没有则换歌；Explore排除当前整首。

Goal全库可选，各阶段尽量不同歌曲；点击“调整音乐”（goalFeedback）排除当前整首。普通错误重试不自动等于主动换歌。没有真实Touchpad能力时不开放内部工具；内部工具返回完整九轨，不受topK截断。

Goal的去重单位优先使用canonical carrier/service song，覆盖同一首歌的九轨、别名和不同playbackUnit。每阶段模型仍可能看到多个检索工具返回的候选，但最终submit_selection必须选择可信、可播且符合排除范围的ID；只有可用候选耗尽时才允许重复。

## 入口和展示门控

探索页和播放页“+”共用后端目标API，不维护两套计划或选歌逻辑。主页面入口（当前探索页顶部目标条）提交后使用准备开屏，首阶段原生音乐与对应画面就绪后才露出目标播放器；不把开场语播完或全部后续材料就绪作为门控。播放页“+”入口则保留当前音乐，目标面板在提交后立即接管展示，首阶段实际执行确认后才更新歌曲与计时。两种入口都允许开场语与音乐并行，语音不可用不会阻断音乐。

这种差异不改变服务端事实：计划、检索、TTS合成、资源校验和真实playing回执仍走同一套goal/version/phase/run合同。前端不能把SELECTION当成“已经播放”，必须等原生回执来决定实际计时和解释语音。

## 复用与边界

复用推荐Context、本地健康摘要、环境补全、画像检索、TTS、原生回执、资源/Preset。新增编排在PoC侧，资源分发仍走原服务，后端不重算压力。

生产权限/账号合同、客户端跨启动恢复、长期统计、通知与持续监听尚未接入。公开版只为说明流程与提示词，不包含运行数据或音乐资产。
