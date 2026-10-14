# 提示词策略

实际提示词均在后端app/agent.py；iOS仅输入、展示和执行。

1. **generate_goal_plan → submit_goal_plan**：保留用户原意；支持任务、情绪照顾与陪伴。不拆解1阶段，拆解2–8阶段；时长有效且总和一致，iconId来自69个允许图标。
2. **model_select_with_retrieval_tools**：沿计划Responses链带工具ACK与完整Context，调用所有可用检索工具，可并行。使用结构化画像、模型撰写的英文描述召回，以及真实Touchpad能力满足时的内部九轨工具。
3. **submit_selection**：只选真实召回且可播、符合去重范围的ID；同时提交boost/lower、openingText、postReceiptText。[实际工具schema](../examples/tool-schemas.json)。
4. **continue_after_receipt**：实际playing且主候选匹配时复用短句，不匹配等兼容路径使用generate_explanation；失败或降级无TTS。

Goal计划、阶段检索和阶段选择沿同一条Responses链继续，但会包含计划请求、工具调用、工具ACK、选择提交等多次模型和工具往返。文档中的“同一条链”只表示上下文连续和previous_response_id继承，不表示一条HTTP请求完成全部阶段。

阶段开场语自然简短，最多一句能量；回执短句不重复能量，以音乐和一个可选轻建议为主。表达情绪先理解陪伴，不强迫积极/任务化，不作诊疗或持续聆听承诺。

仅基于可用事实首次简提天气、地点与定性压力；历史参考不称实时，同样环境不反复说，未来阶段主要讲音乐和目标。继承开场语和建议历史，减少话术重复。

不说成功、失败、准备好、成功切换或轨道编号，不说keep the same song。用可信画像变化乐器、音色、节奏和律动，不总是更轻柔/更留白。

[完整实际模板](prompt-templates.md)从本次源码自动提取。generate_assessment是普通Auto路径，不是Goal主路径；同一工具链不等于一次模型HTTP请求。

共用场景来源合同更新：systemRecommendation 弱参考；currentScene 只来自明确选择；Goal 的目标/阶段优先；potentialIntent 仅 Auto 预留。见 [场景合同](scene-intent-contract.md)。

潜在意图语义修订：非空 Auto 通知输入是本次调节需求，音乐与具体轻建议要主动承接，如压力舒缓／放慢呼吸、日照／出去走走；不是泛化背景。见源码 NOTIFICATION_NEED_RULE。
