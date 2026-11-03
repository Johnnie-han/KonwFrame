# 数据模型

版本：0.1；日期：2026-11-03。状态：设计契约，非数据库已建表。

## 第一版实体

| 实体 | 主要字段 | 约束 |
| --- | --- | --- |
| Project | id, workspaceId, name, revision, document, createdAt, updatedAt | revision 从 1 开始；document 含 schemaVersion |
| Scene | id, templateId, title, body, narrationText, durationFrames, imageAssetId, voiceover | 位于 document.scenes，数组顺序即播放顺序，ID 不因排序改变 |
| Asset | id, projectId, workspaceId, kind, status, storageKey, originalName, mimeType, byteSize, sha256, metadata, provenance | kind 为 image/audio；status 为 processing/ready/failed；storageKey 由服务端生成 |
| AudioBinding | assetId, sourceStartSample, durationSamples, gainDb | 按源采样率解释；配音挂在分镜，音乐挂在项目 |
| RenderSnapshot | id, projectId, revision, document, assets, templateBuildId, createdAt | 文档、探测元数据和素材存储键不可变 |
| RenderJob | id, projectId, snapshotId, idempotencyKey, status, progress, outputKey, error, leaseUntil, heartbeatAt, retryOf, createdAt, finishedAt | queued → running → succeeded/failed；终态不倒退 |

ID 使用不透明字符串，时间戳为 UTC ISO 8601，界面按用户时区显示。资产名只作显示，不拼接为磁盘路径。媒体内容就绪后不可原位替换；替换上传获得新 assetId。

## ProjectDocument 示例结构

```json
{
  "schemaVersion": 1,
  "settings": {"width": 1080, "height": 1920, "fps": 30},
  "theme": {"background": "#0B1020", "accent": "#67D8FF", "fontId": "bundled-cjk"},
  "scenes": [
    {
      "id": "scene_intro",
      "templateId": "title",
      "title": "为什么天空是蓝色？",
      "body": "从阳光和空气说起",
      "narrationText": "抬头看天空，你有没有想过，它为什么常常是蓝色的？",
      "durationFrames": 180,
      "imageAssetId": null,
      "voiceover": null
    }
  ],
  "music": null
}
```

Project 的名称和 revision 是服务端记录字段，不重复写进 document。运行时媒体 URL 由 resolveAssets 生成，不持久化签名 URL。JSON 不能包含 undefined、函数或任意组件代码。

## 时间规则

- 项目 fps=30，durationFrames = sum(scenes.durationFrames)，不单独保存可失真的总时长。
- Scene 起点为此前分镜帧数之和，局部动画第 0 帧对应其全局起点。
- 第一版分镜无重叠、无额外空隙，边界使用半开区间 [startFrame, endFrame)。
- 音频裁剪记录样本位置；显示/布局时用统一函数换算秒数及 ceil(秒数 × fps)，不累计逐次取整误差。
- 第一版 UI 先不提供源裁剪；配音默认为完整源，sourceStartSample=0。模型保留裁剪字段，避免以后改掉时间含义。
- 音乐从项目第 0 帧开始，播放范围不超过项目；不修改源素材。

## 一致性与删除

- 保存时检查模板枚举、唯一分镜 ID、数量、字符长度、帧数及所有素材所属关系。
- 正在处理/失败/不存在的素材不能写入有效绑定；已有文件意外丢失时预览报警，导出拒绝。
- 减少分镜时长不得使配音被截断；校验失败返回具体分镜和所需帧数。
- 删除分镜不删除素材；首版不暴露素材永久删除入口。
- 清理不得删除被项目或历史导出快照引用的素材；备份恢复保持引用完整。
- 旧 schema 先迁移再校验；遇到未知的更高 schemaVersion 拒绝编辑并提示升级。

## 持久化任务

SQLite 保存项目、素材、快照、任务四类记录，迁移版本独立于文档 schemaVersion。领取任务、写入快照与任务状态更新使用事务；状态更新验证 lease 所有权。幂等键在工作空间内唯一，同键不同请求返回冲突，同键相同请求返回原任务。

## 后续扩展实体（首版不建表）

Track/Clip：多轨时间片；MotionPreset：模板 ID 与经过校验的动画参数；BeatMap：音乐 assetId、分析版本、秒数、置信度、人工修正；AudioCue：sceneId、事件 ID、局部帧偏移及音效绑定。引入重叠转场时必须迁移时间模型并新增边界测试，不能直接改变 sum 规则。
