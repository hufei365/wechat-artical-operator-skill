#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 Markdown 转换成微信公众号可用的内联样式 HTML
"""

import argparse
import re
import markdown
from markdown.extensions import tables, fenced_code

from themes import get_theme, list_themes

from code_highlight import highlight_code

DEFAULT_THEME = "doocs"


def _decode_html_entities(text: str) -> str:
    """将 Markdown 库输出的 HTML 实体还原为原始字符"""
    return (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
    )


def preprocess_nested_code_in_blockquotes(md_text: str) -> str:
    """
    预处理引用块中的代码块
    
    将包含代码块的引用块转换为 HTML div 结构，保持视觉连贯性。
    """
    lines = md_text.split('\n')
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检查是否进入引用块
        if line.startswith('>'):
            blockquote_lines = []
            
            # 收集引用块内容
            while i < len(lines) and (lines[i].startswith('>') or (lines[i].strip() == '' and i + 1 < len(lines) and lines[i + 1].startswith('>'))):
                if lines[i].startswith('>'):
                    blockquote_lines.append(lines[i])
                i += 1
            
            # 检查是否包含代码块
            has_code_block = any(re.match(r'^>\s*```', bq_line) for bq_line in blockquote_lines)
            
            if has_code_block:
                # 转换为 HTML div 结构
                from themes import get_theme
                theme_config = get_theme(DEFAULT_THEME)
                
                # 解析引用块内容，保持顺序
                in_code = False
                code_lang = ''
                code_lines = []
                text_paragraphs = []
                current_text = []
                
                for bq_line in blockquote_lines:
                    content = bq_line[1:].lstrip() if bq_line.startswith('> ') else bq_line[1:]
                    
                    code_start = re.match(r'^```(\w*)\s*$', content)
                    if code_start:
                        if in_code:
                            # 代码块结束，保存代码
                            text_paragraphs.append(('code', code_lang, '\n'.join(code_lines)))
                            code_lines = []
                            in_code = False
                        else:
                            # 代码块开始
                            if current_text:
                                text_paragraphs.append(('text', ' '.join(current_text)))
                                current_text = []
                            in_code = True
                            code_lang = code_start.group(1)
                    elif in_code:
                        code_lines.append(content)
                    else:
                        current_text.append(content)
                
                # 处理剩余内容
                if in_code and code_lines:
                    text_paragraphs.append(('code', code_lang, '\n'.join(code_lines)))
                if current_text:
                    text_paragraphs.append(('text', ' '.join(current_text)))
                
                # 生成 HTML
                container_style = (
                    "border-left:4px solid #07C160; margin:1em 0; padding:0 16px; "
                    "background:#f6fff9; border-radius:4px; overflow:hidden;"
                )
                
                html = f'<div class="blockquote-container" style="{container_style}">'
                
                for item in text_paragraphs:
                    if item[0] == 'text':
                        text = item[1]
                        if text.strip():
                            p_style = theme_config["styles"]["p"]
                            html += f'<p style="{p_style}">{text}</p>'
                    elif item[0] == 'code':
                        code_lang = item[1]
                        code_content = item[2]
                        
                        # 使用 doocs 主题的原始代码块配置（深色背景）
                        from themes import THEME_DOOCS
                        dark_code_config = THEME_DOOCS["code"].copy()
                        # 调整背景色为深色，与外部代码块一致
                        dark_code_config["container"] = dark_code_config["container"].replace(
                            "background:#282c34",
                            "background:#282c34"
                        )
                        # 确保在引用块内正确显示
                        dark_code_config["container"] = (
                            "background:#282c34; border-radius:4px; "
                            "padding:12px 16px; margin:0.8em 0; "
                            "overflow-x:auto; font-family:Consolas,Monaco,'Courier New',monospace; "
                            "font-size:14px; line-height:1.6; white-space:pre-wrap; word-wrap:break-word;"
                        )
                        light_code_config = {
                            "container": dark_code_config["container"],
                            "text": dark_code_config.get("text", ""),
                            "token_styles": dark_code_config["token_styles"],
                        }
                        
                        highlighted_html = highlight_code(code_content, code_lang, light_code_config)
                        html += highlighted_html
                
                html += '</div>'
                result.append(html)
            else:
                # 普通引用块，保持 Markdown 格式
                for bq_line in blockquote_lines:
                    result.append(bq_line)
        else:
            result.append(line)
            i += 1
    
    return '\n'.join(result)


def apply_inline_styles(html: str, styles: dict, code_config: dict = None) -> str:
    """把 HTML 标签逐一替换为带内联样式的版本"""
    html = re.sub(r"<p>", f'<p style="{styles["p"]}">', html)

    for level in [1, 2, 3]:
        key = f"h{level}"
        html = re.sub(rf"<{key}>", f'<{key} style="{styles[key]}">', html)

    html = re.sub(r"<blockquote>", f'<blockquote style="{styles["blockquote"]}">', html)

    def replace_pre_code_highlight(m):
        lang_match = re.search(r'class="language-(\w+)"', m.group(0))
        language = lang_match.group(1) if lang_match else "text"
        inner = m.group(1)
        inner = _decode_html_entities(inner)
        return highlight_code(inner, language, code_config=code_config)

    html = re.sub(r"<pre><code[^>]*>(.*?)</code></pre>", replace_pre_code_highlight, html, flags=re.DOTALL)
    html = re.sub(r"(?<!pre)<code>", f'<code style="{styles["code_inline"]}">', html)

    html = re.sub(r"<ul>", f'<ul style="{styles["ul"]}">', html)
    html = re.sub(r"<ol>", f'<ol style="{styles["ol"]}">', html)
    html = re.sub(r"<li>", f'<li style="{styles["li"]}">', html)
    html = re.sub(r"<strong>", f'<strong style="{styles["strong"]}">', html)
    html = re.sub(r"<em>", f'<em style="{styles["em"]}">', html)
    html = re.sub(r"<a ", f'<a style="{styles["a"]}" ', html)
    html = re.sub(r"<hr />|<hr>", f'<hr style="{styles["hr"]}" />', html)
    html = re.sub(r"<img ", f'<img style="{styles["img"]}" ', html)
    html = re.sub(r"<table>", f'<table style="{styles["table"]}">', html)
    html = re.sub(r"<th>", f'<th style="{styles["th"]}">', html)
    html = re.sub(r"<td>", f'<td style="{styles["td"]}">', html)

    return html


def convert(md_text: str, theme: str = DEFAULT_THEME) -> str:
    """将 Markdown 转换为微信公众号可用的 HTML"""
    theme_config = get_theme(theme)
    styles = theme_config["styles"]
    code_config = theme_config.get("code", {})
    
    md_text = preprocess_nested_code_in_blockquotes(md_text)

    raw_html = markdown.markdown(md_text, extensions=["tables", "fenced_code", "nl2br", "sane_lists"])
    styled = apply_inline_styles(raw_html, styles, code_config=code_config)

    wrapper = (
        '<section style="font-family:-apple-system,BlinkMacSystemFont,'
        "'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;"
        f' max-width:100%; word-wrap:break-word; color:{theme_config.get("text_color", "#333")};">'
        + styled
        + "</section>"
    )
    return wrapper


def convert_file(input_path: str, output_path: str = None, theme: str = DEFAULT_THEME) -> str:
    """转换 Markdown 文件"""
    with open(input_path, encoding="utf-8") as f:
        md_content = f.read()
    result = convert(md_content, theme)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)
    return result


def main():
    parser = argparse.ArgumentParser(description="将 Markdown 转换为微信公众号可用的 HTML")
    parser.add_argument("--file", help="Markdown 文件路径")
    parser.add_argument("--text", help="直接传入 Markdown 文本")
    parser.add_argument("--output", help="输出 HTML 文件路径（可选）")
    parser.add_argument("--theme", choices=["doocs", "tech_blue", "minimal", "warm_orange", "business"], default="doocs")
    parser.add_argument("--list-themes", action="store_true")
    parser.add_argument("--quiet", action="store_true")
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
