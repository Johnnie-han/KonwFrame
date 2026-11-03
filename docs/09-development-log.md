# 开发日志

## 2026-11-03

- 已创建项目目录和文档骨架。
- 阶段计划由 docs/08-roadmap.md 单独维护，具体内容待用户填写。
- 尚未安装依赖、初始化应用或实现功能。
- 本记录仅表示骨架准备完成，不表示任何开发阶段已完成。

- 新增最终服务器部署要求，补充项目规范、架构约束及 docs/10-deployment.md；尚未执行部署。

### 阶段 0：需求与设计完成

- 用户授权开始阶段 0；读取用户补充的阶段计划，未改动阶段 1—6 的范围。
- 完成产品概述、需求表 F01—F10、后续能力清单、界面流程与线框。
- 完成架构、数据、接口、音视频规则、测试矩阵与单服务器架构决策。
- 明确 Next.js/React/TypeScript + Remotion、SQLite、独立 Node.js worker 的起步设计；具体依赖版本尚未安装和锁定。
- 扩充服务器部署设计，覆盖配置、持久化、任务恢复、发布、备份和回滚。
- 创建 60 秒天空科普样例：5 镜文稿与 JSON、3 张原创 PNG、3 个合成 WAV、节拍参考时刻及来源说明。
- 查看设计图和图解，修正字体符号及图注交叠。
- 执行 scripts/verify-stage0.py，通过文档与样例完整性检查，证据保存在 docs/acceptance/。
- 在阶段计划中将阶段 0 勾选为已完成，阶段 1—6 保持未开始。
- 尚未初始化应用、录制真实讲解、执行 Remotion 渲染或部署服务器。

### 项目命名与 GitHub 过程要求

- 项目命名为“知帧 · KnowFrame”，建议 GitHub 仓库名为 knowframe；本地目录保持不变。
- 在上级 AGENTS.md 增加小步提交、验证、远程同步、提交说明和历史保留规则，要求评委可查看真实开发过程。
- 命名规范编写时，上级工作区仓库尚无提交、未配置远程地址；当时只更新规范、命名及设计图。后续首次上传按真实现状建立基线，不伪造历史。

### GitHub 远端配置与首次分批上传

- 用户授权远端：https://github.com/Johnnie-han/KonwFrame 。保留仓库创建时的 KonwFrame 拼写。
- 在项目目录建立独立 Git 仓库，main 跟踪 origin/main；不向远端提交上级工作区或“动效库”。
- 保留远端初始提交 7b62c71；之后按规范、设计、样例和验收四个目的建立当前阶段的真实基线，未修改日期或改写共享历史。
- 项目根目录新增随仓库分发的 AGENTS.md 和 .gitignore，修正从项目根读取规范的路径。
- 当前环境代理无法连接，单次 Git 请求使用 `-c http.proxy=` 直连；未修改系统或全局代理。
- 已完成并推送的前三批提交：
- [0a21a80](https://github.com/Johnnie-han/KonwFrame/commit/0a21a80a57dbf366a16e08ca7c953a7addc6018e)：chore(repo): 建立知帧项目规范与独立仓库基线（已推送）。
- [dfbd3a0](https://github.com/Johnnie-han/KonwFrame/commit/dfbd3a088351e1ad2e4bb18d502b5821a9bee95e)：docs(design): 明确首版编辑器需求与服务器架构（已推送）。
- [45cc65f](https://github.com/Johnnie-han/KonwFrame/commit/45cc65f247dd05bb8626b70051ae6d6ea9ed2697)：docs(examples): 添加可复现的科普分镜与原创测试素材（已推送）。
- 本条日志、阶段进度、验收报告和完整性检查工具作为第四批验收提交提交并同步；该提交自身哈希见 Git 历史。
- 尚未开始阶段 1，未部署服务器。
