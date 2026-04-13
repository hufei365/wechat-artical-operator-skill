#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号 Skill 快速测试脚本
验证所有组件是否正常工作
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)


def test_imports():
    """测试依赖是否齐全"""
    print("📦 检查依赖...")

    try:
        import requests

        print("  ✅ requests")
    except ImportError:
        print("  ❌ requests (pip3 install requests)")
        return False

    try:
        import markdown

        print("  ✅ markdown")
    except ImportError:
        print("  ❌ markdown (pip3 install markdown)")
        return False

    try:
        import pygments

        print("  ✅ pygments")
    except ImportError:
        print("  ❌ pygments (pip3 install pygments)")
        return False

    return True


def test_env():
    """测试环境变量"""
    print("\n🔧 检查环境变量...")

    app_id = os.environ.get("WECHAT_APP_ID")
    app_secret = os.environ.get("WECHAT_APP_SECRET")

    if app_id and app_secret:
        print(f"  ✅ WECHAT_APP_ID={app_id[:8]}...")
        print(f"  ✅ WECHAT_APP_SECRET={app_secret[:8]}...")
        return True
    else:
        print("  ⚠️  未设置环境变量（如需要 API 调用请配置）")
        print("     export WECHAT_APP_ID=wx_xxxxxxxx")
        print("     export WECHAT_APP_SECRET=xxxxx")
        return True  # 不强制要求


def test_md_conversion():
    """测试 Markdown 转换"""
    print("\n📝 测试 Markdown 转换...")

    from md_to_wechat import convert

    md = """
# 测试标题

这是**加粗**和*斜体*。

> 引用内容

```python
print("Hello")
```
"""

    try:
        html = convert(md)
        if "<h1" in html and "<p style=" in html and "<code" in html:
            print("  ✅ Markdown 转换正常")
            return True
        else:
            print("  ❌ 转换结果异常")
            return False
    except Exception as e:
        print(f"  ❌ 转换失败：{e}")
        return False


def test_theme_code_highlight():
    """测试主题代码高亮集成"""
    print("\n🎨 测试主题代码高亮...")

    from themes import get_code_config, list_themes
    from code_highlight import highlight_code

    test_code = 'def hello():\n    print("world")'

    for theme_name, display_name in list_themes():
        config = get_code_config(theme_name)
        if not config:
            print(f"  ❌ {display_name}: 缺少 code 配置")
            return False
        html = highlight_code(test_code, "python", config)
        if '<pre style="' not in html or "<code" not in html:
            print(f"  ❌ {display_name}: 高亮输出异常")
            return False

    print("  ✅ 所有主题代码高亮正常")
    return True


def test_theme_integration():
    """测试主题系统端到端集成"""
    print("\n🔗 测试主题系统集成...")

    from md_to_wechat import convert
    from themes import list_themes

    md = "## 测试\n\n```python\nx = 42\n```\n"

    for theme_name, display_name in list_themes():
        try:
            html = convert(md, theme_name)
            if '<pre style="' not in html:
                print(f"  ❌ {display_name}: 代码块未正确渲染")
                return False
        except Exception as e:
            print(f"  ❌ {display_name}: 转换失败 - {e}")
            return False

    print("  ✅ 所有主题集成转换正常")
    return True


def test_html_entities_in_code():
    """测试代码中的 HTML 实体是否被正确处理，避免双重编码"""
    print("\n🧪 测试 HTML 实体编码...")

    from md_to_wechat import convert
    import re

    # Test 1: &amp; double encoding
    md1 = "```python\nx = 'a & b'\n```"
    html1 = convert(md1, "doocs")
    has_double = "&amp;amp;" in html1
    if has_double:
        print("  ❌ &amp; 被双重编码为 &amp;amp;")
        return False

    # Test 2: < and > encoding
    md2 = "```html\n<div>test</div>\n```"
    html2 = convert(md2, "doocs")
    has_double_lt = "&amp;lt;" in html2
    has_double_gt = "&amp;gt;" in html2
    if has_double_lt or has_double_gt:
        print("  ❌ < > 被双重编码")
        return False

    # Verify entities exist correctly
    code_blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", html1, re.DOTALL)
    if code_blocks:
        if "&amp;" not in code_blocks[0]:
            print("  ❌ &amp; 实体未正确保留")
            return False

    print("  ✅ HTML 实体编码处理正常")
    return True


def test_em_tag_format():
    """测试 <em> 标签格式正确，没有多余空格"""
    print("\n✨ 测试 <em> 标签格式...")

    from md_to_wechat import convert
    import re

    md = "这是 *斜体* 文字"
    html = convert(md, "doocs")

    # Check for space before >
    bad_em = re.search(r"<em[^>]*\s+>", html)
    if bad_em:
        print(f"  ❌ <em> 标签有多余空格: '{bad_em.group()}'")
        return False

    print("  ✅ <em> 标签格式正常")
    return True


def test_code_white_space():
    """测试代码块包含 white-space:pre-wrap"""
    print("\n📄 测试代码块换行保留...")

    from md_to_wechat import convert
    from themes import list_themes

    md = "```python\nline1\nline2\n```"

    for theme_name, _ in list_themes():
        html = convert(md, theme_name)
        if "white-space:pre-wrap" not in html:
            print(f"  ❌ {theme_name}: 缺少 white-space:pre-wrap")
            return False

    print("  ✅ 所有主题代码块包含 white-space:pre-wrap")
    return True


def test_token_module():
    """测试 token 模块导入"""
    print("\n🔑 测试 token 模块...")

    try:
        from wechat_token import get_token, clear_token_cache

        print("  ✅ token 模块导入成功")
        return True
    except Exception as e:
        print(f"  ❌ token 模块导入失败：{e}")
        return False


def main():
    print("=" * 50)
    print("微信公众号 Skill 组件测试")
    print("=" * 50)

    results = []

    results.append(("依赖检查", test_imports()))
    results.append(("环境变量", test_env()))
    results.append(("Markdown 转换", test_md_conversion()))
    results.append(("Token 模块", test_token_module()))
    results.append(("主题代码高亮", test_theme_code_highlight()))
    results.append(("主题系统集成", test_theme_integration()))
    results.append(("HTML 实体编码", test_html_entities_in_code()))
    results.append(("<em> 标签格式", test_em_tag_format()))
    results.append(("代码块换行保留", test_code_white_space()))

    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print(f"\n总计：{passed}/{total} 通过")

    if passed == total:
        print("\n🎉 所有组件正常！")
        return 0
    else:
        print("\n⚠️  部分组件异常，请根据提示修复")
        return 1


if __name__ == "__main__":
    sys.exit(main())
