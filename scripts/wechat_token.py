#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号 access_token 管理模块
- 自动缓存 token，避免频繁请求
- token 有效期 7200 秒，提前 5 分钟刷新
"""
import os
import json
import time
import requests

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".token_cache.json")


def get_token() -> str:
    """获取微信公众号 access_token"""
    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")

    if not app_id or not app_secret:
        raise Exception("缺少环境变量：WECHAT_APP_ID 或 WECHAT_APP_SECRET")

    # 读取缓存
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                cache = json.load(f)
            # token 有效期 7200 秒，提前 300 秒（5 分钟）刷新
            if time.time() - cache.get("timestamp", 0) < 6900:
                return cache["access_token"]
        except (json.JSONDecodeError, KeyError):
            # 缓存文件损坏，重新获取
            pass

    # 重新获取 token
    url = (
        "https://api.weixin.qq.com/cgi-bin/token"
        f"?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    )

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        raise Exception(f"请求 access_token 失败：{e}")

    if "access_token" not in data:
        errcode = data.get("errcode", "unknown")
        errmsg = data.get("errmsg", "unknown error")
        raise Exception(f"获取 token 失败 (errcode={errcode}): {errmsg}")

    # 写入缓存
    cache_dir = os.path.dirname(CACHE_FILE)
    os.makedirs(cache_dir, exist_ok=True)

    with open(CACHE_FILE, "w") as f:
        json.dump(
            {"access_token": data["access_token"], "timestamp": time.time()},
            f,
            indent=2,
        )

    return data["access_token"]


def clear_token_cache():
    """清除 token 缓存（用于 token 失效时）"""
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)


if __name__ == "__main__":
    try:
        token = get_token()
        print(token)
    except Exception as e:
        print(f"ERROR: {e}", file=__import__("sys").stderr)
        exit(1)
