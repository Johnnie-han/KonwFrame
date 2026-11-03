# 知帧 · KnowFrame

让知识按节奏成片。面向知识科普视频制作的网页编辑器，计划采用剪映式布局和 Remotion。

GitHub 仓库：[Johnnie-han/KonwFrame](https://github.com/Johnnie-han/KonwFrame)。产品英文名为 KnowFrame，仓库路径保留创建时的 KonwFrame 拼写。本地目录保留 `vibe知识大赏`。

当前状态：阶段 0 需求与设计已完成，文档与样例验收已记录。应用尚未初始化，尚不能启动编辑器、渲染视频或部署。下一步为阶段 1：视频制作闭环。

## 开发入口

- 开发规范：[AGENTS.md](AGENTS.md)。
- 项目概述与文档导航：[docs/00-project-overview.md](docs/00-project-overview.md)。
- 阶段计划与完成状态：`docs/08-roadmap.md`。
- 开发日志：`docs/09-development-log.md`。
- 第一版功能规格：[docs/features/mvp-editor.md](docs/features/mvp-editor.md)。
- 阶段 0 验收：[docs/acceptance/stage-0.md](docs/acceptance/stage-0.md)。
- 服务器交付约束：[docs/10-deployment.md](docs/10-deployment.md)。

项目需要通过真实、持续的小步提交展示开发过程。完成并验证一个独立小任务后及时提交；配置并授权 GitHub 远程后及时推送，保留过程历史。详细规则见项目根目录的 `AGENTS.md`。

## 目录

- `docs/`：需求、设计、接口、验收和阶段计划。
- `docs/features/`：单个功能规格。
- `docs/decisions/`：架构决策。
- `docs/design/`：设计线框，不是运行中的网页截图。
- `docs/acceptance/`：各阶段验收证据。
- `src/components/`：通用界面组件。
- `src/editor/`：编辑器功能。
- `src/remotion/`：视频组件与模板。
- `src/lib/`：公共逻辑。
- `src/types/`：类型定义。
- `public/`：公开静态资源。
- `assets/`：本地素材，按图片、音乐、配音、音效和参考案例分类。
- `examples/`：样例内容。
- `renders/`：本地视频导出结果。
- `scripts/`：开发辅助检查，不是应用运行代码。

上述目录是初始约定，应用初始化时按实际框架调整。
不要将私密素材直接放入公开静态资源目录。

## 查看本阶段交付

阅读 [产品需求](docs/01-product-requirements.md) 和 [界面设计](docs/02-user-flows-and-ui.md)，查看 [60 秒样例](examples/sky-blue/README.md)。

文档和样例完整性检查：

```shell
python scripts/verify-stage0.py
```

该脚本需要 Python 与 Pillow，仅检查文档链接和样例数据；不代表应用功能已通过测试。应用安装、启动、构建及导出命令待阶段 1 实现后补充。

## 提交历史

[在 GitHub 查看逐步提交记录](https://github.com/Johnnie-han/KonwFrame/commits/main)。

本次首次上传按开发规范、需求设计、样例素材和验收记录分组建立真实基线，不代表这些工作发生在不同日期。后续功能在实现和验证过程中持续小步提交。
