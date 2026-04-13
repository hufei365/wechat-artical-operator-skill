#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码语法高亮模块
使用 Pygments 实现，支持通过主题配置自定义配色方案
向后兼容：不传 code_config 时使用内置 Google Code 默认配色
"""

import re

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatter import Formatter
from pygments.token import Token

GOOGLECODE_STYLES = {
    "comment": "color:#800",
    "keyword": "color:#008",
    "keyword_type": "color:#606",
    "keyword_constant": "color:#606",
    "operator_word": "color:#000",
    "name_builtin": "color:#008",
    "name_function": "color:#c00",
    "name_class": "color:#606",
    "name_namespace": "color:#008",
    "name_exception": "color:#c00",
    "name_variable": "color:#000",
    "name_attribute": "color:#008",
    "name_tag": "color:#008",
    "string": "color:#00d",
    "number": "color:#009",
    "literal": "color:#880",
    "decoration": "color:#880",
    "punctuation": "color:#000",
    "whitespace": "color:#ccc",
    "error": "color:#f00",
}

CODE_CONTAINER_STYLE = (
    "background:#fff; border:1px solid #ddd; border-radius:4px;"
    " padding:12px 16px; margin:1em 0; overflow-x:auto;"
    " font-family:Consolas,Monaco,'Courier New',monospace; font-size:14px;"
    " line-height:1.5; white-space:nowrap;"
)


def highlight_code(code: str, language: str = "text", code_config: dict = None) -> str:
    """
    对代码进行语法高亮

    Args:
        code: 代码文本
        language: 编程语言名称（如 python, javascript, java 等）
        code_config: 主题的代码高亮配置（包含 container, text, token_styles），
                     为 None 时使用内置默认配色

    Returns:
        带内联样式的 HTML 代码块
    """
    try:
        lexer = get_lexer_by_name(language)
    except Exception:
        try:
            lexer = guess_lexer(code)
        except Exception:
            lexer = get_lexer_by_name("text")

    token_styles = None
    if code_config and "token_styles" in code_config:
        token_styles = code_config["token_styles"]

    formatter = InlineStyleFormatter(token_styles=token_styles)
    highlighted = highlight(code, lexer, formatter)

    container_style = CODE_CONTAINER_STYLE
    text_style = ""
    if code_config:
        container_style = code_config.get("container", CODE_CONTAINER_STYLE)
        text_style = code_config.get("text", "")

    if text_style:
        result = (
            f'<pre style="{container_style}">'
            f'<code style="{text_style}">{highlighted}</code>'
            "</pre>"
        )
    else:
        result = f'<pre style="{container_style}"><code>{highlighted}</code></pre>'

    return result


class InlineStyleFormatter(Formatter):
    """
    自定义 Pygments 格式化器
    直接生成带内联样式的 HTML，不使用 CSS 类
    支持通过 token_styles 参数自定义配色
    """

    def __init__(self, token_styles=None, **options):
        super().__init__(**options)
        self.styles = token_styles if token_styles is not None else GOOGLECODE_STYLES
        self._type_map = [
            (Token.Comment.Single, "comment"),
            (Token.Comment.Multiline, "comment"),
            (Token.Comment, "comment"),
            (Token.Keyword.Type, "keyword_type"),
            (Token.Keyword.Constant, "keyword_constant"),
            (Token.Keyword, "keyword"),
            (Token.Operator.Word, "operator_word"),
            (Token.Name.Builtin, "name_builtin"),
            (Token.Name.Function, "name_function"),
            (Token.Name.Class, "name_class"),
            (Token.Name.Namespace, "name_namespace"),
            (Token.Name.Exception, "name_exception"),
            (Token.Name.Variable, "name_variable"),
            (Token.Name.Attribute, "name_attribute"),
            (Token.Name.Tag, "name_tag"),
            (Token.Name, "name_builtin"),
            (Token.Literal.String, "string"),
            (Token.Literal.Number, "number"),
            (Token.Literal, "literal"),
            (Token.String, "string"),
            (Token.Number, "number"),
            (Token.Operator, "punctuation"),
            (Token.Punctuation, "punctuation"),
            (Token.Error, "error"),
        ]

    def format(self, tokensource, outfile):
        result = []

        for token_type, value in tokensource:
            # 先进行 HTML 转义
            value = (
                value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            )

            # 将空格转换为 &nbsp; 以保留代码缩进
            # 只转换行首和连续的空格，避免过度转换
            if " " in value:
                # 使用正则表达式将连续空格转换为 &nbsp;
                import re
                value = re.sub(r' +', lambda m: '&nbsp;' * len(m.group(0)), value)

            style = self._get_style(token_type)

            if style:
                result.append(f'<span style="{style}">{value}</span>')
            else:
                result.append(value)

        # 将换行符替换为 <br> 标签，配合 white-space:nowrap 实现精确换行控制
        final_output = "".join(result).replace("\n", "<br>")
        outfile.write(final_output)

    def _get_style(self, token_type):
        for token_key, style_key in self._type_map:
            if token_type is token_key:
                return self.styles.get(style_key, "")

        for token_key, style_key in self._type_map:
            if token_type in token_key:
                return self.styles.get(style_key, "")

        return ""


def get_supported_languages() -> list:
    """返回支持的语言列表"""
    return [
        "python",
        "javascript",
        "typescript",
        "java",
        "cpp",
        "c",
        "csharp",
        "go",
        "rust",
        "ruby",
        "php",
        "swift",
        "kotlin",
        "scala",
        "bash",
        "shell",
        "sql",
        "html",
        "css",
        "xml",
        "json",
        "yaml",
        "markdown",
        "lua",
        "perl",
        "r",
        "matlab",
        "objective-c",
        "text",
    ]


if __name__ == "__main__":
    test_code = """
def hello_world():
    print("Hello, World!")
    
class Test:
    def __init__(self):
        self.value = 42
"""

    print("默认配色:")
    print(highlight_code(test_code, "python"))

    from themes import get_code_config

    print("\n主题配色 (doocs):")
    config = get_code_config("doocs")
    print(highlight_code(test_code, "python", config))

    print("\n支持的语言:")
    for lang in get_supported_languages()[:10]:
        print(f"  - {lang}")
