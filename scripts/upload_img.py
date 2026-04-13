#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号封面图上传脚本
- 从 Unsplash 获取随机封面图
- 上传本地图片到微信素材库
- 返回 media_id 用于后续草稿创建
"""

import sys
import os
import argparse
import json
import tempfile
import requests

# 导入同目录下的 wechat_token 模块
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from wechat_token import get_token

# 随机图片 API（免费，无需 key），按优先级尝试
IMAGE_APIS = [
    {
        "name": "Lorem Picsum",
        "url_random": "https://picsum.photos/900/383",
        "url_keyword": None,
    },
    {
        "name": "Unsplash Source",
        "url_random": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=900&h=383&fit=crop",
        "url_keyword": None,
        "note": "source.unsplash.com 已废弃，使用固定示例图片作为 fallback",
    },
]


def download_random_image(keyword: str = None, output_path: str = None) -> str:
    """
    从随机图片服务下载封面图
    依次尝试 Unsplash → Picsum，任一成功即返回

    Args:
        keyword: 搜索关键词（可选，仅 Unsplash 支持）
        output_path: 保存路径（可选，默认临时文件）

    Returns:
        本地图片路径
    """
    errors = []
    for api in IMAGE_APIS:
        # 构建下载 URL
        if keyword and api.get("url_keyword"):
            url = api["url_keyword"].format(keyword=keyword)
        else:
            url = api["url_random"]

        try:
            resp = requests.get(url, timeout=30, allow_redirects=True)
            resp.raise_for_status()
        except requests.RequestException as e:
            errors.append(f"{api['name']}：{e}")
            continue

        # 检查是否真的是图片
        content_type = resp.headers.get("Content-Type", "")
        if "image" not in content_type:
            errors.append(
                f"{api['name']}：返回内容不是图片（Content-Type: {content_type}）"
            )
            continue

        # 检查大小
        if len(resp.content) > 2 * 1024 * 1024:
            errors.append(f"{api['name']}：图片超过 2MB")
            continue

        if not output_path:
            ext = ".png" if "png" in content_type else ".jpg"
            output_path = os.path.join(
                tempfile.gettempdir(), f"cover_{api['name'].lower()}{ext}"
            )

        with open(output_path, "wb") as f:
            f.write(resp.content)

        return output_path

    raise Exception(f"所有图片服务均失败：{'；'.join(errors)}")


def upload_image(path: str) -> dict:
    """
    上传图片到微信永久素材

    Args:
        path: 本地图片路径

    Returns:
        {"media_id": "xxx", "url": "xxx"}
    """
    token = get_token()
    # 使用永久素材接口（草稿箱需要永久素材的 media_id）
    url = (
        "https://api.weixin.qq.com/cgi-bin/material/add_material"
        f"?access_token={token}&type=image"
    )

    # 检查文件是否存在
    try:
        with open(path, "rb") as f:
            file_content = f.read()
    except FileNotFoundError:
        raise Exception(f"图片文件不存在：{path}")
    except IOError as e:
        raise Exception(f"读取图片失败：{e}")

    # 检查文件大小（微信限制 2MB）
    if len(file_content) > 2 * 1024 * 1024:
        raise Exception("图片大小超过 2MB 限制")

    # 上传
    with open(path, "rb") as f:
        files = {"media": f}
        resp = requests.post(url, files=files, timeout=30)

    try:
        data = resp.json()
    except json.JSONDecodeError:
        raise Exception(f"响应解析失败：{resp.text}")

    if "media_id" not in data:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise Exception(f"上传失败 (errcode={errcode}): {errmsg}")

    result = {
        "media_id": data["media_id"],
        "url": data.get("url", ""),
    }

    # 结构化输出，方便 Skill 解析
    print(json.dumps(result, ensure_ascii=False))
    return result


def main():
    parser = argparse.ArgumentParser(description="上传微信公众号封面图")
    parser.add_argument("--path", help="本地图片路径")
    parser.add_argument(
        "--unsplash",
        nargs="?",
        const="",
        default=None,
        help="从 Unsplash 下载随机封面图，可指定关键词（如 --unsplash technology）",
    )
    parser.add_argument("--output", help="Unsplash 图片保存路径（可选）")
    parser.add_argument(
        "--quiet", action="store_true", help="仅输出 media_id，不输出 JSON"
    )
    args = parser.parse_args()

    try:
        image_path = args.path

        # 如果指定了 --unsplash，先下载图片（自动 fallback 到 Picsum）
        if args.unsplash is not None:
            keyword = args.unsplash.strip() or None
            image_path = download_random_image(keyword=keyword, output_path=args.output)
            if not args.quiet:
                keyword_msg = f"（关键词：{keyword}）" if keyword else ""
                print(
                    f"📷 已下载随机封面图{keyword_msg}：{image_path}", file=sys.stderr
                )

        if not image_path:
            parser.print_help()
            raise ValueError("请提供 --path 或 --unsplash 参数")

        result = upload_image(image_path)
        if args.quiet:
            print(result["media_id"])
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
