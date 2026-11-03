# 接口契约

版本：0.1；日期：2026-11-03。状态：第一版接口设计，尚无可调用服务。

## 通用约定

前缀 `/api/v1`；成功返回 JSON（媒体和下载除外）；ID 是不透明字符串。除存活检查外，接口在部署时均经过工作空间访问控制。浏览器使用同源身份；渲染媒体访问使用受限任务凭证。

错误结构：`{"error":{"code":"REVISION_CONFLICT","message":"项目已在其他页面更新","details":{"currentRevision":3},"requestId":"req_..."}}`。

状态码：400 格式错误；401/403 无身份或无权；404 不存在；409 版本/幂等冲突；413 文件过大；415 类型不支持；422 文档或媒体不合法；429 配额/速率限制；500 内部错误（不返回磁盘路径、堆栈或密钥）。

## 接口表

| 方法与路径 | 输入 | 成功输出 | 特殊规则 |
| --- | --- | --- | --- |
| GET `/projects?cursor=…&limit=20` | 可选分页 | 200 `{items:[{id,name,revision,updatedAt}],nextCursor}` | 限工作空间，limit 上限 100 |
| POST `/projects` | `{name}` | 201 `{project}` | document.scenes=[]，revision=1 |
| GET `/projects/:id` | 项目 ID | 200 `{project}` | project 含 document 和 revision |
| PUT `/projects/:id` | `{baseRevision,name,document}` | 200 `{project}` | 原子版本检查，成功 revision+1；409 时不修改记录 |
| GET `/projects/:id/assets` | 项目 ID | 200 `{items:[asset]}` | 仅本项目素材 |
| POST `/projects/:id/assets` | multipart `file` | 202 `{asset}` | 持久化文件及 processing 记录，异步探测；超限尽早 413 |
| GET `/assets/:id` | 素材 ID | 200 `{asset}` | 轮询 processing → ready/failed，失败含安全原因 |
| GET `/assets/:id/content` | 素材 ID，Range 可选 | 200/206 文件内容 | 先验权，支持音频 Range；不公开 storageKey |
| POST `/projects/:id/renders` | `{expectedRevision}` + `Idempotency-Key` | 202 `{job}` | 服务端冻结该 revision；空项目/配音越界/缺失素材 422，版本变化 409 |
| GET `/projects/:id/renders` | 项目 ID | 200 `{items:[job]}` | 最近任务，包含 revision，不含快照内部文件路径 |
| GET `/renders/:id` | 任务 ID | 200 `{job}` | 持久化状态，不依赖浏览器持续连接 |
| POST `/renders/:id/retry` | 新 `Idempotency-Key` | 202 `{job}` | 仅失败任务可重试，复用原 snapshotId，retryOf 指向原任务 |
| GET `/renders/:id/download` | 成功任务 ID | 200 附件或授权重定向 | 未完成返回 409；下载前重新鉴权 |
| GET `/health/live` | 无 | 200 `{status:"ok"}` | 仅表明进程存活，不披露环境 |
| GET `/health/ready` | 受控运维身份 | 200 或 503 | 检查数据库、数据目录及 worker 心跳；细节仅内部可见 |

## 最小字段示例

```json
{
  "job": {
    "id": "render_01",
    "projectId": "project_01",
    "revision": 2,
    "status": "queued",
    "progress": 0,
    "retryOf": null,
    "error": null,
    "downloadUrl": null
  }
}
```

progress 为 0—1；queued=0，running <1，只有文件发布完毕才 succeeded=1。失败保留最后进度。错误使用 `RENDER_FAILED`、`RENDER_INTERRUPTED`、`ASSET_MISSING`、`BUILD_UNAVAILABLE` 等代码；消息可供用户理解。

Asset 对外字段：id、projectId、kind、status、originalName、mimeType、byteSize、metadata、contentUrl、error。metadata 对图片含 width/height，对音频含 sampleRate/channels/durationSamples。ready 前不保证这些字段存在。provenance 为服务端可选来源记录，接口不接受客户端任意覆盖存储信息。

## 请求流程与并发

上传返回 202 不代表素材就绪；浏览器轮询素材状态，ready 后才能应用。第一版网页服务内执行有上限的媒体探测，超时或重启遗留的 processing 记录转 failed，可重新上传；不允许无限悬挂。

导出流程为“完成上传 → 保存 → 获得 revision → 提交导出 → 查询任务 → 下载”。轮询默认 2 秒，可退避到 10 秒；离开页面不取消任务。网络重试复用同一幂等键，用户显式重试失败任务用新键。重复提交的匹配依据包括项目、revision 或 retryOf。

音频超过分镜返回 422，details 包含 sceneId、requiredDurationFrames。请求 revision 与数据库不符返回 409；前端不能自动以最新 revision 重新提交旧文档。

取消、永久删除、AI、节拍和音效接口属于后续范围，在各自功能规格完成后增加。
