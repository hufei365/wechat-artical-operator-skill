---
name: wechat-publisher
description: "将文章发布到微信公众号草稿箱或正式发布。支持 Markdown 转 HTML、多主题排版、代码语法高亮、封面图上传。触发场景：用户说'发公众号'、'写公众号推文'、'推到草稿箱'、'发布微信文章'、'公众号推文'。不用于发布到其他平台。"
---

# 微信公众号发布技能

## 前置检查

验证环境变量（`WECHAT_APP_ID`、`WECHAT_APP_SECRET`）：

```bash
python3 scripts/check_env.py
```

检查失败时告知用户配置环境变量。

## 依赖安装

```bash
pip3 install requests markdown pygments --break-system-packages
```

## 工作流程

### Step 1：收集信息

| 字段 | 要求 | 默认值 |
|------|------|--------|
| 文章标题 | ≤30 字 | 必填 |
| 文章正文 | Markdown 或 HTML | 必填 |
| 封面图片 | 本地路径或 URL | 可选 |
| 作者名 | 文本 | 可选 |
| 摘要 | ≤120 字 | 可选 |

标题超 30 字时提示精简。

### Step 1.5：Markdown 转 HTML（如需要）

```bash
# 默认主题（doocs 绿），推荐用 --content-file 传内容
python3 scripts/md_to_wechat.py --file <文件路径> --output /tmp/wechat_content.html --theme <主题>
```

**可用主题：** `doocs`（默认，技术文章）、`tech_blue`（企业宣传）、`minimal`（文字创作）、`warm_orange`（生活分享）、`business`（商业报告）

### Step 2：处理封面图

```bash
# 情况 A：用户提供本地图片
python3 scripts/upload_img.py --path <图片路径>

# 情况 B：用户提供 URL，先下载再上传
curl -o /tmp/wechat_cover.jpg "<URL>"
python3 scripts/upload_img.py --path /tmp/wechat_cover.jpg

# 情况 C：用户未提供，获取随机封面图（Picsum Photos）
python3 scripts/upload_img.py --unsplash
```

记录返回的 `media_id`。

### Step 3：创建草稿

**优先使用 `--content-file`**（避免命令行参数截断）：

```bash
python3 scripts/publish.py --action draft \
  --title "<标题>" \
  --content-file /tmp/wechat_content.html \
  --thumb_media_id "<media_id>" \
  --author "<作者>" \
  --digest "<摘要>"
```

也可用 `--content` 直接传 HTML 字符串。记录返回的 `media_id`（草稿 ID）。

### Step 4：发布草稿

询问用户选择：
- 📥 仅保存到草稿箱
- 🚀 立即发布

```bash
python3 scripts/publish.py --action publish --media_id "<草稿 media_id>"
```

### Step 5：查询发布状态

发布是异步操作（1-3 分钟），可查询结果：

```bash
python3 scripts/publish.py --action status --publish_id "<publish_id>"
```

### Step 6：确认结果

**成功：**
```
✅ 文章《{标题}》已{操作类型}

📌 相关信息：
- 草稿 media_id：{id}
- publish_id：{id}（仅发布时）

⏱ 提示：
- 草稿箱内容可随时在公众号后台编辑
- 发布任务为异步操作，预计 1-3 分钟后在公众号可见
- API 发布的文章不会触发系统推荐，需手动群发给粉丝
```

## 错误处理

| 错误码 | 含义 | 处理方案 |
|--------|------|----------|
| 40001 | access_token 无效/过期 | 自动清除缓存后重试 |
| 40164 | IP 不在白名单 | 提示用户在公众号后台添加服务器 IP |
| 45009 | 接口调用超限 | 告知用户每日群发限制（2 次/天） |
| 40003 | 无效 AppID | 检查 WECHAT_APP_ID 配置 |
| 40125 | AppSecret 错误 | 检查 WECHAT_APP_SECRET 配置 |

## 注意事项

- 订阅号每天可群发 1 次，服务号每月 4 次
- API 发布不支持原创声明，需后台手动操作
- 封面图建议 900×383 像素，<2MB
