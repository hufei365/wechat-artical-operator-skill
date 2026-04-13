#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境变量检查脚本
- 验证微信公众号配置是否完整
- 在 Skill 执行前调用
"""
import os
import sys
import json


def check_env() -> dict:
    """
    检查环境变量配置

    Returns:
        {
            "ok": bool,
            "missing": ["缺失的变量名"],
            "message": "提示信息"
        }
    """
    required = ["WECHAT_APP_ID", "WECHAT_APP_SECRET"]
    missing = []

    for var in required:
        if not os.environ.get(var):
            missing.append(var)

    if missing:
        return {
            "ok": False,
            "missing": missing,
            "message": (
                f"❌ 缺少环境变量：{missing}\n"
                "\n"
                "配置方法（二选一）：\n"
                "\n"
                "1. 在 ~/.openclaw/openclaw.json 中添加：\n"
                '   {\n'
                '     "env": {\n'
                '       "WECHAT_APP_ID": "你的 AppID",\n'
                '       "WECHAT_APP_SECRET": "你的 AppSecret"\n'
                "     }\n"
                "   }\n"
                "\n"
                "2. 通过 export 设置：\n"
                "   export WECHAT_APP_ID=wx_xxxxxxxx\n"
                "   export WECHAT_APP_SECRET=xxxxxxxxxxxxxxxx\n"
            ),
        }

    # 验证 AppID 格式（微信 AppID 通常是 wx 开头的 18 位字符）
    app_id = os.environ.get("WECHAT_APP_ID", "")
    if not app_id.startswith("wx") or len(app_id) < 10:
        return {
            "ok": False,
            "missing": [],
            "message": f"⚠️ WECHAT_APP_ID 格式可能不正确：{app_id}",
        }

    return {
        "ok": True,
        "missing": [],
        "message": "✅ 环境检查通过",
    }


def main():
    result = check_env()
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result["ok"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
