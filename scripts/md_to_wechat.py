#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 Markdown 转换成微信公众号可用的内联样式 HTML
用例：
  python3 md_to_wechat.py --file article.md --output out.html
  python3 md_to_wechat.py --text "## 标题\n正文内容"
"""

import argparse
import re
import markdown
from markdown.extensions import tables, fenced_code

from themes import get_theme, list_themes

from code_highlight import highlight_code

DEFAULT_THEME = "doocs"


def _decode_html_entities(text: str) -> str:
    """将 Markdown 库输出的 HTML 实体还原为原始字符

    Markdown 库会把代码块内的 & < > 转义为 &amp; &lt; &gt;，
    但 Pygments 的 InlineStyleFormatter 会再次转义这些字符。
    必须先还原，避免双重编码（如 &amp;amp;）。
    &amp; 必须最先处理，否则还原出的 & 会干扰后续替换。
    """
    return (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )


def apply_inline_styles(html: str, styles: dict, code_config: dict = None) -> str:
    """把 HTML 标签逐一替换为带内联样式的版本

    Args:
        html: 原始 HTML
        styles: 样式表字典
        code_config: 主题的代码高亮配置，传给 highlight_code()
    """

    html = re.sub(r"<p>", f'<p style="{styles["p"]}">', html)

    for level in [1, 2, 3]:
        key = f"h{level}"
        html = re.sub(rf"<{key}>", f'<{key} style="{styles[key]}">', html)

    html = re.sub(
        r"<blockquote>",
        f'<blockquote style="{styles["blockquote"]}">',
        html,
    )

    # 代码块 <pre><code class="language-xxx"> —— 带语法高亮
    def replace_pre_code_highlight(m):
        lang_match = re.search(r'class="language-(\w+)"', m.group(0))
        language = lang_match.group(1) if lang_match else "text"
        inner = m.group(1)
        inner = _decode_html_entities(inner)
        return highlight_code(inner, language, code_config=code_config)

    html = re.sub(
        r"<pre><code[^>]*>(.*?)</code></pre>",
        replace_pre_code_highlight,
        html,
        flags=re.DOTALL,
    )

    # 行内 code（未被 pre 包裹的）
    html = re.sub(
        r"(?<!pre>)<code>",
        f'<code style="{styles["code_inline"]}">',
        html,
    )

    # 列表
    html = re.sub(r"<ul>", f'<ul style="{styles["ul"]}">', html)
    html = re.sub(r"<ol>", f'<ol style="{styles["ol"]}">', html)
    html = re.sub(r"<li>", f'<li style="{styles["li"]}">', html)

    # 强调
    html = re.sub(r"<strong>", f'<strong style="{styles["strong"]}">', html)
    html = re.sub(r"<em>", f'<em style="{styles["em"]}">', html)

    # 链接
    html = re.sub(r"<a ", f'<a style="{styles["a"]}" ', html)

    # 分割线
    html = re.sub(r"<hr />|<hr>", f'<hr style="{styles["hr"]}" />', html)

    # 图片
    html = re.sub(r"<img ", f'<img style="{styles["img"]}" ', html)

    # 表格
    html = re.sub(r"<table>", f'<table style="{styles["table"]}">', html)
    html = re.sub(r"<th>", f'<th style="{styles["th"]}">', html)
    html = re.sub(r"<td>", f'<td style="{styles["td"]}">', html)

    return html


def convert(md_text: str, theme: str = DEFAULT_THEME) -> str:
    """
    将 Markdown 转换为微信公众号可用的 HTML

    Args:
        md_text: Markdown 格式文本
        theme: 主题名称 (doocs/tech_blue/minimal/warm_orange/business)

    Returns:
        带内联样式的 HTML 字符串
    """
    theme_config = get_theme(theme)
    styles = theme_config["styles"]
    code_config = theme_config.get("code", {})

    raw_html = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )

    styled = apply_inline_styles(raw_html, styles, code_config=code_config)

    wrapper = (
        '<section style="font-family:-apple-system,BlinkMacSystemFont,'
        "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;"
        f' max-width:100%; word-wrap:break-word; color:{theme_config.get("text_color", "#333")};">'
        + styled
        + "</section>"
    )
    return wrapper


def convert_file(
    input_path: str, output_path: str = None, theme: str = DEFAULT_THEME
) -> str:
    """
    转换 Markdown 文件

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（可选）
        theme: 主题名称

    Returns:
        转换后的 HTML 字符串
    """
    with open(input_path, encoding="utf-8") as f:
        md_content = f.read()

    result = convert(md_content, theme)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="将 Markdown 转换为微信公众号可用的 HTML"
    )
    parser.add_argument("--file", help="Markdown 文件路径")
    parser.add_argument("--text", help="直接传入 Markdown 文本")
    parser.add_argument("--output", help="输出 HTML 文件路径（可选）")
    parser.add_argument(
        "--theme",
        choices=["doocs", "tech_blue", "minimal", "warm_orange", "business"],
        default="doocs",
        help="主题样式（默认：doocs）",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="列出所有可用主题",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="仅输出 HTML，不输出提示信息",
    )
    args = parser.parse_args()

    if args.list_themes:
        print("可用主题：")
        for name, display in list_themes():
            print(f"  - {name}: {display}")
        return 0

    try:
        if args.file:
            with open(args.file, encoding="utf-8") as f:
                md_content = f.read()
        elif args.text:
            md_content = args.text
        else:
            parser.print_help()
            raise ValueError("请提供 --file 或 --text 参数")

        result = convert(md_content, args.theme)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result)
            if not args.quiet:
                print(f"✅ 已输出到 {args.output} (主题：{args.theme})")
        else:
            print(result)

    except FileNotFoundError as e:
        print(f"ERROR: 文件不存在 - {e}", file=__import__("sys").stderr)
        __import__("sys").exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=__import__("sys").stderr)
        __import__("sys").exit(1)


if __name__ == "__main__":
    main()
