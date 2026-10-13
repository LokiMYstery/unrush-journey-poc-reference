# Unrush 旅程内化：后端流程与提示词参考

2026-10-13 当前PoC源码快照，供UI、iOS和后端对照目标编排、阶段准备、检索工具、提示词与原生回执；不包含部署凭据和业务资产。

对应iOS：[旅程分支固定版本](https://github.com/Qiyin-Tech/unrush-ios/tree/a2db0695e4e50280d9ce5da4a5020fe7de4d83a6)，基于Auto PoC。源文件摘要及公开版调整见[source-snapshot.json](source-snapshot.json)。

| 要了解什么 | 入口 |
| --- | --- |
| 前后端流转、缓存与激活 | [docs/data-flow.md](docs/data-flow.md) |
| 后端新增与复用 | [docs/backend-changes.md](docs/backend-changes.md) |
| 提示词策略与原文模板 | [docs/prompts.md](docs/prompts.md)、[docs/prompt-templates.md](docs/prompt-templates.md) |
| 工具schema、调用和范围 | [examples/tool-schemas.json](examples/tool-schemas.json)、[app/agent.py](app/agent.py)、[app/catalog.py](app/catalog.py) |
| 目标API、状态与持久化 | [app/main.py](app/main.py)、[app/schemas.py](app/schemas.py)、[app/goals.py](app/goals.py)、[app/store.py](app/store.py) |

## 当前原型

播放页“+”和探索页顶部进入目标输入。不拆解为一个阶段，拆解为2–8阶段；Agent决定标题、时长和图标。目标是主体，能量只有上升boost/下降lower，可逐阶段变化。情绪关怀和陪伴也是目标。

探索提交经过准备页，首阶段声画就绪后进入播放；播放页提交保留音乐。阶段条横向浏览，以实际播放倒计时，通过下一阶段或到时推进。Touchpad独立顶层覆层，关闭不取消适配；拖动和手动换歌让手动声音优先，再选择继续适配。

## 资产、配置与验证

源码不带密钥、专属部署地址、请求日志、健康记录、数据库、音乐画像、映射、向量和媒体。公开版移除了部署专属英文音色默认值，需设置自己的VOLCENGINE_TTS_VOICE_ID_EN，其余链路保留原实现。

`.env.example`仅列环境变量。完整运行需兼容Profile、PlaybackUnitCatalog、`app/assets/music/v1/FastSceneSongTiers.json`、POI规则和描述召回模型/向量。缺必需资产不能启动；描述召回缺依赖返回结构化错误，不伪造召回。

无需业务资产/SDK的六项合同校验：

```sh
python3 -m unittest discover -s tests -v
```

测试直接提取本快照的纯schema/计划校验函数，验证阶段数量、时长/图标、两类能量、阶段语音字段、工具可用性和topK；不替代运行态或真机测试。Python源码另经语法编译检查。

完整服务：Python 3.11+，安装requirements.txt，提供上述资产并注入环境变量，再运行`uvicorn app.main:app`。本地CLAP额外依赖见requirements-retrieval.txt。

这是实现参考，不是生产发布。客户端跨启动/跨设备目标恢复、长期统计、通知和持续主动感知仍未接入；后端部分编排恢复不代表客户端已支持跨启动恢复。
