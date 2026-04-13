#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号草稿管理脚本
- 创建草稿 (draft/add)
- 发布草稿 (freepublish/submit)
- 查询发布状态 (freepublish/get)
"""

import argparse
import json
import re
import requests
import sys
import time

# 导入同目录下的 wechat_token 模块
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from wechat_token import get_token, clear_token_cache

WX_BASE = "https://api.weixin.qq.com/cgi-bin"

MAX_RETRIES = 2
RETRY_DELAY = 1  # 秒
MAX_CONTENT_SIZE = 20000  # 微信正文字数限制


def _decode_unicode_escapes(text: str) -> str:
    """将字符串中的 \\uXXXX 转义序列还原为实际字符。

    AI agent 生成内容时可能将中文编码为 \\uXXXX 形式，
    导致微信公众号显示原始转义序列而非中文。
    使用 regex 精准替换，避免 codecs.decode 损坏已有的真实中文字符。
    """
    if not text or "\\u" not in text:
        return text
    result = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    try:
        result = result.encode("utf-16", "surrogatepass").decode("utf-16")
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    return result


def _request_with_retry(method, url, **kwargs):
    """带重试的 HTTP 请求（处理网络超时和 5xx 错误）"""
    kwargs.setdefault("timeout", 30)
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.request(method, url, **kwargs)
            data = resp.json()
            # token 过期自动重试
            if data.get("errcode") == 40001:
                clear_token_cache()
                token = get_token()
                url = url.split("?")[0] + f"?access_token={token}"
                resp = requests.request(method, url, **kwargs)
                data = resp.json()
            return data
        except requests.RequestException as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except json.JSONDecodeError:
            raise Exception(f"响应解析失败：{resp.text}")
    raise Exception(f"请求失败（重试 {MAX_RETRIES} 次后）：{last_error}")


def add_draft(
    title: str,
    content: str,
    thumb_media_id: str,
    author: str = "",
    digest: str = "",
    show_cover_pic: int = 1,
    dry_run: bool = False,
) -> dict:
    """
    创建草稿

    Args:
        title: 文章标题（≤30 字）
        content: 文章正文（HTML 格式）
        thumb_media_id: 封面图 media_id
        author: 作者名（可选）
        digest: 摘要（≤120 字，可选）
        show_cover_pic: 是否显示封面 (0/1)

    Returns:
        {"status": "draft_created", "media_id": "xxx"}
    """
    title = _decode_unicode_escapes(title)
    content = _decode_unicode_escapes(content)
    author = _decode_unicode_escapes(author)
    digest = _decode_unicode_escapes(digest)

    if len(title) > 30:
        raise Exception(f"标题超过 30 字限制（当前{len(title)}字）")
    if len(content) > MAX_CONTENT_SIZE:
        raise Exception(f"正文超过 {MAX_CONTENT_SIZE} 字限制（当前{len(content)}字）")
    if digest and len(digest) > 120:
        raise Exception(f"摘要超过 120 字限制（当前{len(digest)}字）")
    if not thumb_media_id:
        raise Exception("缺少封面图 media_id")

    token = get_token()
    url = f"{WX_BASE}/draft/add?access_token={token}"

    article = {
        "title": title,
        "thumb_media_id": thumb_media_id,
        "content": content,
        "show_cover_pic": show_cover_pic,
    }

    if author:
        article["author"] = author
    if digest:
        article["digest"] = digest

    payload = {"articles": [article]}

    if dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return {"status": "dry_run", "media_id": ""}

    data = _request_with_retry(
        "POST",
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    if "media_id" not in data:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise Exception(f"草稿创建失败 (errcode={errcode}): {errmsg}")

    result = {"status": "draft_created", "media_id": data["media_id"]}
    print(json.dumps(result, ensure_ascii=False))
    return result


def publish_draft(media_id: str) -> dict:
    """
    发布草稿

    Args:
        media_id: 草稿的 media_id

    Returns:
        {"status": "published", "publish_id": "xxx"}
    """
    if not media_id:
        raise Exception("缺少草稿 media_id")

    token = get_token()
    url = f"{WX_BASE}/freepublish/submit?access_token={token}"

    payload = {"media_id": media_id}

    data = _request_with_retry(
        "POST",
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    # errcode=0 表示发布任务提交成功
    if data.get("errcode", -1) != 0:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise Exception(f"发布失败 (errcode={errcode}): {errmsg}")

    result = {
        "status": "published",
        "publish_id": data.get("publish_id", ""),
        "media_id": media_id,
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def query_publish_status(publish_id: str) -> dict:
    """
    查询发布状态

    Args:
        publish_id: 发布任务 ID

    Returns:
        {"status": "xxx", "article_url": "xxx", ...}
    """
    if not publish_id:
        raise Exception("缺少 publish_id")

    token = get_token()
    url = f"{WX_BASE}/freepublish/get?access_token={token}"

    payload = {"publish_id": publish_id}

    data = _request_with_retry(
        "POST",
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    if data.get("errcode", -1) != 0:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise Exception(f"查询失败 (errcode={errcode}): {errmsg}")

    publish_status = data.get("publish_status", -1)
    status_map = {
        0: "成功",
        1: "发布中",
        2: "原创失败",
        3: "常规失败",
        4: "平台拒绝",
        5: "成功但审核不通过",
    }

    result = {
        "status": "query_success",
        "publish_status": publish_status,
        "publish_status_desc": status_map.get(
            publish_status, f"未知({publish_status})"
        ),
        "article_url": data.get("article_url", ""),
        "article_detail": data.get("article_detail", {}),
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="微信公众号草稿管理")
    parser.add_argument(
        "--action",
        choices=["draft", "publish", "status"],
        required=True,
        help="操作类型：draft=创建草稿，publish=发布草稿，status=查询发布状态",
    )
    parser.add_argument("--title", default="", help="文章标题")
    parser.add_argument("--content", default="", help="文章正文 (HTML)")
    parser.add_argument("--content-file", default="", help="文章正文文件路径 (HTML)")
    parser.add_argument("--thumb_media_id", default="", help="封面图 media_id")
    parser.add_argument("--media_id", default="", help="草稿 media_id（发布时使用）")
    parser.add_argument(
        "--publish_id", default="", help="发布任务 ID（查询状态时使用）"
    )
    parser.add_argument("--author", default="", help="作者名")
    parser.add_argument("--digest", default="", help="摘要")
    parser.add_argument(
        "--show-cover", type=int, default=1, choices=[0, 1], help="是否显示封面"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅打印发给微信的 payload，不实际发送（用于调试）",
    )

    args = parser.parse_args()

    try:
        if args.action == "draft":
            # 优先从文件读取内容（避免命令行参数过长）
            content = args.content
            if args.content_file:
                with open(args.content_file, "r", encoding="utf-8") as f:
                    content = f.read()
            add_draft(
                title=args.title,
                content=content,
                thumb_media_id=args.thumb_media_id,
                author=args.author,
                digest=args.digest,
                show_cover_pic=args.show_cover,
                dry_run=args.dry_run,
            )
        elif args.action == "publish":
            publish_draft(media_id=args.media_id)
        elif args.action == "status":
            query_publish_status(publish_id=args.publish_id)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
