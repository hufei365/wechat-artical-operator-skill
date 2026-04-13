#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号主题样式库
参考 doocs/md 等主流微信编辑器设计

每个主题包含：
- styles: HTML 标签内联样式
- code: 代码块容器样式 + 语法高亮配色方案
"""

# ─── 主题 1：默认主题（doocs 绿）────────────────────────────────────
# 特点：简洁清新，适合技术文章、干货分享
THEME_DOOCS = {
    "name": "doocs",
    "display_name": "Doocs 绿",
    "primary_color": "#07C160",  # 微信绿
    "text_color": "#1a1a1a",
    "styles": {
        "p": (
            "font-size:16px; line-height:1.75em; color:#333;"
            " margin:0 0 1.2em 0; letter-spacing:0.05em;"
        ),
        "h1": (
            "font-size:22px; font-weight:bold; color:#1a1a1a;"
            " margin:1.5em 0 0.8em; border-bottom:2px solid #07C160;"
            " padding-bottom:6px; text-align:center;"
        ),
        "h2": (
            "font-size:19px; font-weight:bold; color:#1a1a1a;"
            " margin:1.4em 0 0.7em; padding-left:10px;"
            " border-left:4px solid #07C160;"
        ),
        "h3": (
            "font-size:17px; font-weight:bold; color:#1a1a1a; margin:1.2em 0 0.6em;"
        ),
        "blockquote": (
            "border-left:4px solid #07C160; margin:1em 0;"
            " padding:8px 16px; background:#f6fff9; color:#555;"
            " font-style:italic;"
        ),
        "code_inline": (
            "font-family:Consolas,Monaco,monospace; font-size:14px;"
            " background:#f0f0f0; padding:2px 6px; border-radius:3px;"
            " color:#e83e8c;"
        ),
        "ul": "margin:0.5em 0 1em 1.5em; padding:0;",
        "ol": "margin:0.5em 0 1em 1.5em; padding:0;",
        "li": "font-size:16px; line-height:1.75em; color:#333; margin:0.3em 0;",
        "strong": "font-weight:bold; color:#1a1a1a;",
        "em": "font-style:italic; color:#555;",
        "a": "color:#07C160; text-decoration:none;",
        "hr": "border:none; border-top:1px solid #e5e5e5; margin:1.5em 0;",
        "table": (
            "border-collapse:collapse; width:100%; font-size:15px; margin:1em 0;"
        ),
        "th": (
            "background:#07C160; color:#fff; font-weight:bold;"
            " padding:8px 12px; text-align:left; border:1px solid #07C160;"
        ),
        "td": "padding:8px 12px; border:1px solid #ddd; color:#333;",
        "img": "max-width:100%; display:block; margin:1em auto;",
    },
    "code": {
        "container": (
            "background:#282c34; border-radius:8px; padding:16px;"
            " overflow-x:auto; margin:1em 0;"
            " font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; line-height:1.6; white-space:nowrap;"
        ),
        "text": (
            "font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; color:#abb2bf;"
        ),
        "token_styles": {
            "comment": "color:#5c6370; font-style:italic",
            "keyword": "color:#07C160; font-weight:bold",
            "keyword_type": "color:#e5c07b",
            "keyword_constant": "color:#d19a66",
            "operator_word": "color:#56b6c2",
            "name_builtin": "color:#e5c07b",
            "name_function": "color:#61afef",
            "name_class": "color:#e5c07b",
            "name_namespace": "color:#e5c07b",
            "name_exception": "color:#e06c75",
            "name_variable": "color:#e06c75",
            "name_attribute": "color:#d19a66",
            "name_tag": "color:#e06c75",
            "string": "color:#98c379",
            "number": "color:#d19a66",
            "literal": "color:#56b6c2",
            "punctuation": "color:#abb2bf",
        },
    },
}

# ─── 主题 2：科技蓝 ──────────────────────────────────────────────
# 特点：专业稳重，适合企业宣传、产品介绍
THEME_TECH_BLUE = {
    "name": "tech_blue",
    "display_name": "科技蓝",
    "primary_color": "#1a73e8",  # Google 蓝
    "text_color": "#1a1a1a",
    "styles": {
        "p": (
            "font-size:16px; line-height:1.8; color:#333;"
            " margin:0 0 1.2em 0; text-align:justify;"
        ),
        "h1": (
            "font-size:24px; font-weight:bold; color:#1a73e8;"
            " margin:1.5em 0 0.8em; text-align:center;"
            " padding:10px 0; border-bottom:3px solid #1a73e8;"
        ),
        "h2": (
            "font-size:20px; font-weight:bold; color:#1a73e8;"
            " margin:1.4em 0 0.7em; padding:8px 12px;"
            " background:#e8f0fe;"
            " border-radius:4px;"
        ),
        "h3": (
            "font-size:18px; font-weight:bold; color:#1a73e8; margin:1.2em 0 0.6em;"
        ),
        "blockquote": (
            "border-left:4px solid #1a73e8; margin:1em 0;"
            " padding:10px 16px; background:#e8f0fe; color:#555;"
        ),
        "code_inline": (
            "font-family:Consolas,Monaco,monospace; font-size:14px;"
            " background:#e8f0fe; padding:2px 6px; border-radius:3px;"
            " color:#1a73e8;"
        ),
        "ul": "margin:0.5em 0 1em 1.5em; padding:0;",
        "ol": "margin:0.5em 0 1em 1.5em; padding:0;",
        "li": "font-size:16px; line-height:1.8; color:#333; margin:0.3em 0;",
        "strong": "font-weight:bold; color:#1a73e8;",
        "em": "font-style:italic; color:#555;",
        "a": "color:#1a73e8; text-decoration:none; border-bottom:1px solid #1a73e8;",
        "hr": "border:none; border-top:2px solid #e8f0fe; margin:1.5em 0;",
        "table": (
            "border-collapse:collapse; width:100%; font-size:15px; margin:1em 0;"
        ),
        "th": (
            "background:#1a73e8; color:#fff; font-weight:bold;"
            " padding:10px 12px; text-align:left; border:1px solid #1a73e8;"
        ),
        "td": "padding:8px 12px; border:1px solid #e8f0fe; color:#333;",
        "img": "max-width:100%; display:block; margin:1em auto; border-radius:6px;",
    },
    "code": {
        "container": (
            "background:#263238; border-radius:6px; padding:16px;"
            " overflow-x:auto; margin:1em 0; border:1px solid #37474f;"
            " font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; line-height:1.6; white-space:nowrap;"
        ),
        "text": (
            "font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; color:#eceff1;"
        ),
        "token_styles": {
            "comment": "color:#546e7a; font-style:italic",
            "keyword": "color:#82aaff; font-weight:bold",
            "keyword_type": "color:#ffcb6b",
            "keyword_constant": "color:#f78c6c",
            "operator_word": "color:#89ddff",
            "name_builtin": "color:#ffcb6b",
            "name_function": "color:#82aaff",
            "name_class": "color:#ffcb6b",
            "name_namespace": "color:#ffcb6b",
            "name_exception": "color:#f07178",
            "name_variable": "color:#eeffff",
            "name_attribute": "color:#c792ea",
            "name_tag": "color:#f07178",
            "string": "color:#c3e88d",
            "number": "color:#f78c6c",
            "literal": "color:#89ddff",
            "punctuation": "color:#89ddff",
        },
    },
}

# ─── 主题 3：简约黑 ──────────────────────────────────────────────
# 特点：极简主义，适合文字类、观点类文章
# 代码块使用浅色背景，与黑白灰主题保持一致
THEME_MINIMAL = {
    "name": "minimal",
    "display_name": "简约黑",
    "primary_color": "#000000",
    "text_color": "#000000",
    "styles": {
        "p": (
            "font-size:16px; line-height:1.9; color:#000;"
            " margin:0 0 1.5em 0; text-align:justify;"
        ),
        "h1": (
            "font-size:26px; font-weight:bold; color:#000;"
            " margin:2em 0 1em; text-align:center; letter-spacing:2px;"
        ),
        "h2": (
            "font-size:20px; font-weight:bold; color:#000;"
            " margin:1.5em 0 0.8em; padding-bottom:6px;"
            " border-bottom:1px solid #000;"
        ),
        "h3": ("font-size:17px; font-weight:bold; color:#333; margin:1.2em 0 0.6em;"),
        "blockquote": (
            "border-left:2px solid #000; margin:1em 0;"
            " padding:8px 16px; color:#666;"
            " font-style:italic;"
        ),
        "code_inline": (
            "font-family:Consolas,Monaco,monospace; font-size:14px;"
            " background:#f5f5f5; padding:2px 6px; border-radius:2px;"
            " color:#333;"
        ),
        "ul": "margin:0.5em 0 1em 1.5em; padding:0;",
        "ol": "margin:0.5em 0 1em 1.5em; padding:0;",
        "li": "font-size:16px; line-height:1.9; color:#000; margin:0.3em 0;",
        "strong": "font-weight:bold; color:#000;",
        "em": "font-style:italic; color:#666;",
        "a": "color:#000; text-decoration:underline;",
        "hr": "border:none; border-top:1px solid #000; margin:1.5em 0;",
        "table": (
            "border-collapse:collapse; width:100%; font-size:15px; margin:1em 0;"
        ),
        "th": (
            "background:#000; color:#fff; font-weight:bold;"
            " padding:8px 12px; text-align:left; border:1px solid #000;"
        ),
        "td": "padding:8px 12px; border:1px solid #ddd; color:#333;",
        "img": "max-width:100%; display:block; margin:1em auto;",
    },
    "code": {
        "container": (
            "background:#f8f8f8; border-radius:4px; padding:16px;"
            " overflow-x:auto; margin:1em 0; border:1px solid #e0e0e0;"
            " font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; line-height:1.6; white-space:nowrap;"
        ),
        "text": (
            "font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; color:#333;"
        ),
        "token_styles": {
            "comment": "color:#999; font-style:italic",
            "keyword": "color:#000; font-weight:bold",
            "keyword_type": "color:#458",
            "keyword_constant": "color:#008080",
            "operator_word": "color:#000",
            "name_builtin": "color:#008",
            "name_function": "color:#900",
            "name_class": "color:#458; font-weight:bold",
            "name_namespace": "color:#008",
            "name_exception": "color:#900",
            "name_variable": "color:#333",
            "name_attribute": "color:#458",
            "name_tag": "color:#008",
            "string": "color:#d14",
            "number": "color:#009",
            "literal": "color:#008080",
            "punctuation": "color:#333",
        },
    },
}

# ─── 主题 4：文艺橙 ──────────────────────────────────────────────
# 特点：温暖活泼，适合生活类、情感类文章
THEME_WARM_ORANGE = {
    "name": "warm_orange",
    "display_name": "文艺橙",
    "primary_color": "#ff6b35",
    "text_color": "#2c2c2c",
    "styles": {
        "p": ("font-size:16px; line-height:1.8; color:#2c2c2c; margin:0 0 1.2em 0;"),
        "h1": (
            "font-size:24px; font-weight:bold; color:#ff6b35;"
            " margin:1.5em 0 0.8em; text-align:center;"
        ),
        "h2": (
            "font-size:19px; font-weight:bold; color:#ff6b35;"
            " margin:1.4em 0 0.7em;"
            " padding:8px 12px; background:#fff5f0; border-radius:6px;"
        ),
        "h3": (
            "font-size:17px; font-weight:bold; color:#ff8c42; margin:1.2em 0 0.6em;"
        ),
        "blockquote": (
            "border-left:4px solid #ff6b35; margin:1em 0;"
            " padding:10px 16px; background:#fff5f0; color:#666;"
            " border-radius:0 6px 6px 0;"
        ),
        "code_inline": (
            "font-family:Consolas,Monaco,monospace; font-size:14px;"
            " background:#fff5f0; padding:2px 6px; border-radius:3px;"
            " color:#ff6b35;"
        ),
        "ul": "margin:0.5em 0 1em 1.5em; padding:0;",
        "ol": "margin:0.5em 0 1em 1.5em; padding:0;",
        "li": "font-size:16px; line-height:1.8; color:#2c2c2c; margin:0.3em 0;",
        "strong": "font-weight:bold; color:#ff6b35;",
        "em": "font-style:italic; color:#666;",
        "a": "color:#ff6b35; text-decoration:none;",
        "hr": "border:none; border-top:2px dashed #ffd8b8; margin:1.5em 0;",
        "table": (
            "border-collapse:collapse; width:100%; font-size:15px; margin:1em 0;"
        ),
        "th": (
            "background:#ff6b35; color:#fff; font-weight:bold;"
            " padding:8px 12px; text-align:left; border:1px solid #ff6b35;"
        ),
        "td": "padding:8px 12px; border:1px solid #ffd8b8; color:#2c2c2c;",
        "img": "max-width:100%; display:block; margin:1em auto; border-radius:8px;",
    },
    "code": {
        "container": (
            "background:#2d2d2d; border-radius:8px; padding:16px;"
            " overflow-x:auto; margin:1em 0;"
            " font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; line-height:1.6; white-space:nowrap;"
        ),
        "text": (
            "font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:14px; color:#f8f8f2;"
        ),
        "token_styles": {
            "comment": "color:#75715e; font-style:italic",
            "keyword": "color:#ff6b35; font-weight:bold",
            "keyword_type": "color:#66d9ef",
            "keyword_constant": "color:#ae81ff",
            "operator_word": "color:#f92672",
            "name_builtin": "color:#66d9ef",
            "name_function": "color:#a6e22e",
            "name_class": "color:#66d9ef; font-weight:bold",
            "name_namespace": "color:#66d9ef",
            "name_exception": "color:#a6e22e",
            "name_variable": "color:#f8f8f2",
            "name_attribute": "color:#a6e22e",
            "name_tag": "color:#f92672",
            "string": "color:#ffd866",
            "number": "color:#ae81ff",
            "literal": "color:#ae81ff",
            "punctuation": "color:#f8f8f2",
        },
    },
}

# ─── 主题 5：商务灰 ──────────────────────────────────────────────
# 特点：专业正式，适合商业报告、行业资讯
THEME_BUSINESS = {
    "name": "business",
    "display_name": "商务灰",
    "primary_color": "#4a5568",
    "text_color": "#1a202c",
    "styles": {
        "p": (
            "font-size:15px; line-height:1.8; color:#2d3748;"
            " margin:0 0 1.2em 0; text-align:justify;"
        ),
        "h1": (
            "font-size:22px; font-weight:bold; color:#1a202c;"
            " margin:1.5em 0 0.8em; padding:12px 0;"
            " border-bottom:2px solid #4a5568;"
        ),
        "h2": (
            "font-size:18px; font-weight:bold; color:#4a5568;"
            " margin:1.4em 0 0.7em; padding-left:12px;"
            " border-left:3px solid #4a5568;"
        ),
        "h3": (
            "font-size:16px; font-weight:bold; color:#718096; margin:1.2em 0 0.6em;"
        ),
        "blockquote": (
            "border-left:4px solid #cbd5e0; margin:1em 0;"
            " padding:10px 16px; background:#f7fafc; color:#718096;"
        ),
        "code_inline": (
            "font-family:Consolas,Monaco,monospace; font-size:13px;"
            " background:#edf2f7; padding:2px 6px; border-radius:3px;"
            " color:#4a5568;"
        ),
        "ul": "margin:0.5em 0 1em 1.5em; padding:0;",
        "ol": "margin:0.5em 0 1em 1.5em; padding:0;",
        "li": "font-size:15px; line-height:1.8; color:#2d3748; margin:0.3em 0;",
        "strong": "font-weight:bold; color:#1a202c;",
        "em": "font-style:italic; color:#718096;",
        "a": "color:#4a5568; text-decoration:none; border-bottom:1px dotted #4a5568;",
        "hr": "border:none; border-top:1px solid #e2e8f0; margin:1.5em 0;",
        "table": (
            "border-collapse:collapse; width:100%; font-size:14px; margin:1em 0;"
        ),
        "th": (
            "background:#4a5568; color:#fff; font-weight:bold;"
            " padding:10px 12px; text-align:left; border:1px solid #cbd5e0;"
        ),
        "td": "padding:8px 12px; border:1px solid #e2e8f0; color:#2d3748;",
        "img": "max-width:100%; display:block; margin:1em auto;",
    },
    "code": {
        "container": (
            "background:#1a202c; border-radius:6px; padding:16px;"
            " overflow-x:auto; margin:1em 0;"
            " font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:13px; line-height:1.6; white-space:nowrap;"
        ),
        "text": (
            "font-family:Consolas,Monaco,'Courier New',monospace;"
            " font-size:13px; color:#e2e8f0;"
        ),
        "token_styles": {
            "comment": "color:#718096; font-style:italic",
            "keyword": "color:#90cdf4; font-weight:bold",
            "keyword_type": "color:#fbd38d",
            "keyword_constant": "color:#fc8181",
            "operator_word": "color:#63b3ed",
            "name_builtin": "color:#fbd38d",
            "name_function": "color:#63b3ed",
            "name_class": "color:#fbd38d; font-weight:bold",
            "name_namespace": "color:#fbd38d",
            "name_exception": "color:#fc8181",
            "name_variable": "color:#e2e8f0",
            "name_attribute": "color:#b794f4",
            "name_tag": "color:#fc8181",
            "string": "color:#68d391",
            "number": "color:#fbd38d",
            "literal": "color:#63b3ed",
            "punctuation": "color:#a0aec0",
        },
    },
}

# ─── 主题列表 ───────────────────────────────────────────────────
THEMES = {
    "doocs": THEME_DOOCS,
    "tech_blue": THEME_TECH_BLUE,
    "minimal": THEME_MINIMAL,
    "warm_orange": THEME_WARM_ORANGE,
    "business": THEME_BUSINESS,
}


def get_theme(theme_name: str = "doocs") -> dict:
    """
    获取指定主题

    Args:
        theme_name: 主题名称 (doocs/tech_blue/minimal/warm_orange/business)

    Returns:
        主题配置字典
    """
    return THEMES.get(theme_name, THEME_DOOCS)


def get_code_config(theme_name: str = "doocs") -> dict:
    """获取指定主题的代码高亮配置"""
    theme = get_theme(theme_name)
    return theme.get("code", {})


def list_themes() -> list:
    """
    列出所有可用主题

    Returns:
        [(theme_name, display_name), ...]
    """
    return [(k, v["display_name"]) for k, v in THEMES.items()]


if __name__ == "__main__":
    print("可用主题：")
    for name, display in list_themes():
        print(f"  - {name}: {display}")
