# 代码语法高亮功能说明

## 🎉 功能概述

微信公众号 Skill 现已集成 **Pygments** 语法高亮引擎，采用经典的 **Google Code** 主题风格，为你的技术文章提供专业的代码排版效果。

---

## 📦 安装依赖

```bash
pip3 install pygments --break-system-packages
```

---

## 🎨 高亮效果

### Google Code 主题配色

| 元素类型 | 颜色 | 示例 |
|----------|------|------|
| 关键字 | 紫色 `#008` | `def`, `class`, `import`, `const`, `function` |
| 字符串 | 蓝色 `#00d` | `"Hello, World!"` |
| 注释 | 红色 `#800` | `# 这是注释` |
| 函数名 | 橙色 `#c00` | `print()`, `console.log()` |
| 类名 | 紫红色 `#606` | `class MyClass` |
| 数字 | 深蓝色 `#009` | `42`, `3.14` |
| 操作符 | 黑色 `#000` | `+`, `-`, `=`, `==` |
| 空白字符 | 浅灰 `#ccc` | 空格、换行 |

---

## 💻 支持的语言

支持 **50+** 种编程语言，包括但不限于：

### 常用语言
- Python
- JavaScript / TypeScript
- Java
- C / C++ / C#
- Go
- Rust
- Ruby

### Web 开发
- PHP
- Swift
- Kotlin
- Scala
- HTML
- CSS
- XML
- JSON
- YAML

### 数据与脚本
- SQL
- Bash / Shell
- Lua
- Perl
- R
- MATLAB

### 其他语言
- Objective-C
- Haskell
- Erlang
- Elixir
- 等等...

---

## 📝 使用方法

### 在 Markdown 中使用

使用标准的 fenced code blocks 语法：

````markdown
```python
def hello_world():
    """打印问候语"""
    print("Hello, World!")
    
class Person:
    def __init__(self, name):
        self.name = name
```
````

````markdown
```javascript
// 箭头函数示例
const greet = (name) => {
  console.log(`Hello, ${name}!`);
};

class Calculator {
  constructor(value = 0) {
    this.value = value;
  }
  
  add(n) {
    this.value += n;
    return this;
  }
}
```
````

````markdown
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```
````

````markdown
```go
package main

import "fmt"

func main() {
    messages := make(chan string)
    go func() {
        messages <- "ping"
    }()
    msg := <-messages
    fmt.Println(msg)
}
```
````

````markdown
```rust
fn main() {
    let numbers = vec![1, 2, 3, 4, 5];
    let doubled: Vec<i32> = numbers
        .iter()
        .map(|&x| x * 2)
        .collect();
    println!("{:?}", doubled);
}
```
````

````markdown
```sql
SELECT 
    u.id,
    u.name,
    COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC;
```
````

````markdown
```bash
#!/bin/bash
if [ -f "$1" ]; then
    echo "File exists"
    wc -l "$1"
else
    echo "File not found"
    exit 1
fi
```
````

---

## 🔧 技术实现

### 核心模块

**`scripts/code_highlight.py`**

```python
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def highlight_code(code: str, language: str = "text") -> str:
    """对代码进行语法高亮"""
    lexer = get_lexer_by_name(language)
    formatter = InlineStyleFormatter()  # 自定义内联样式格式化器
    highlighted = highlight(code, lexer, formatter)
    return f'<pre><code>{highlighted}</code></pre>'
```

### 内联样式格式化器

为了让微信公众号兼容，我们自定义了 `InlineStyleFormatter` 类，直接将样式内联到每个 `<span>` 标签，而不是使用 CSS 类：

```html
<!-- 输出示例 -->
<span style="color:#008">def</span>
<span style="color:#ccc"> </span>
<span style="color:#c00">hello_world</span>
<span style="color:#000">(</span>
```

---

## 🎯 代码块样式

### 外层容器

```css
background: #fff;
border: 1px solid #ddd;
border-radius: 4px;
padding: 12px 16px;
margin: 1em 0;
overflow-x: auto;
font-family: Consolas, Monaco, 'Courier New', monospace;
font-size: 14px;
line-height: 1.5;
```

### 特点

- ✅ 白色背景 + 灰色边框
- ✅ 圆角设计
- ✅ 合适的内边距
- ✅ 横向滚动（长代码）
- ✅ 等宽字体
- ✅ 1.5 倍行高

---

## 📊 对比效果

### 无高亮

```
def hello():
    print("Hello")
```

### 有高亮

```python
def hello():
    print("Hello")
```

---

## 🧪 测试示例

项目包含完整的测试文件：

```bash
# 查看测试文件
cat references/code_highlight_test.md

# 转换为 HTML
python3 scripts/md_to_wechat.py \
  --file references/code_highlight_test.md \
  --output /tmp/test_highlight.html
```

---

## 💡 最佳实践

### 1. 始终指定语言

````markdown
<!-- ✅ 推荐 -->
```python
code here
```

<!-- ❌ 不推荐 -->
```
code here
```
````

### 2. 保持代码简洁

- 单段代码不超过 50 行
- 过长代码考虑分段
- 添加必要的注释

### 3. 使用行内代码

对于短代码片段，使用行内代码：

```markdown
使用 `const value = 42` 定义常量
```

---

## 🔗 参考资料

- [Pygments 官方文档](https://pygments.org/)
- [Google Code 主题源码](https://github.com/pygments/pygments/blob/master/pygments/styles/googlecode.py)
- [doocs/md](https://github.com/doocs/md) - 微信 Markdown 编辑器

---

## 📝 更新日志

### v1.3.0 (2024-04-01)
- ✅ 初始版本
- ✅ 集成 Pygments
- ✅ Google Code 主题
- ✅ 支持 50+ 语言

---

## ❓ 常见问题

### Q: 支持自定义主题吗？

A: 目前仅支持 Google Code 风格。如需自定义，可编辑 `scripts/code_highlight.py` 中的 `GOOGLECODE_STYLES` 字典。

### Q: 为什么不用 Prism.js 或 Highlight.js？

A: 微信公众号不支持外部 JavaScript，必须使用服务端渲染的内联样式方案。Pygments 是 Python 生态的标准选择。

### Q: 支持行号吗？

A: 当前版本不支持行号。如需支持，可在 `code_highlight.py` 中添加行号生成逻辑。

### Q: 某些语言识别不准确怎么办？

A: 建议在代码块开头明确指定语言，如 ```python 而不是 ```。
