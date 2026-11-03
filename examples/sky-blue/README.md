# 贯穿开发的天空科普样例

用途：需求讨论、布局、时间轴与后续真实视频制作验收。当前是素材和设计数据，尚未制作成片。

## 内容

- [script.md](script.md)：5 镜讲解文稿，计划 6 + 12 + 18 + 16 + 8 = 60 秒。
- [project.fixture.json](project.fixture.json)：schemaVersion=1 的项目文档与本地素材清单。
- `assets/sunlight.png`、`scattering.png`、`sunset.png`：原创示意图，可作为首版 PNG 上传样本，不是物理模拟。
- `assets/test-music-120bpm-60s.wav`：24kHz、单声道、16 位 PCM 合成测试配乐。
- `assets/test-cue-0.25s.wav`：用于后续动作音效绑定验证的测试提示音。
- `assets/voice-calibration-tone-6s.wav`：非语音校准音，只用于文件探测、配音时长边界和混音测试。
- [beat-reference.json](beat-reference.json)：合成器事件的参考时刻；不是已经实现的节拍分析结果。
- [sources.md](sources.md)：科学依据、适用范围和素材来源说明。

没有真实讲解录音。project.fixture.json 的 voiceover 保持 null；阶段 1 必须另行录制或上传真实中文讲解，不得把校准音当成完成配音。现有 60 秒是分镜设计时长，不保证未录制文稿恰好讲满每镜。

## 使用与导入约定

本地 fixture 不是公开 API 请求，也不是已经存在的数据库记录。素材清单中的 sourceFile 是相对于本目录的路径，id 是样例 ID。

实现阶段先上传真实文件，取得服务端 assetId，再替换文档中的样例引用并保存。服务器存储键、签名 URL、项目 ID 和 revision 由运行中的服务产生。不要将本地文件路径直接作为远程渲染输入。

## 重新生成

素材由 [generate-assets.py](generate-assets.py) 原创程序绘制或合成。开发辅助脚本使用 Python 与 Pillow；无需调用外部生成服务，不是应用运行依赖。

```shell
python generate-assets.py --font /path/to/a/CJK-font.ttc
```

脚本会重写本目录中的生成素材、JSON、script.md 及 docs/design/editor-wireframe.png，手工修改前先复制。字体只用于本机设计图栅格化；不复制操作系统字体到交付包，应用字体另行选型并核对授权。
