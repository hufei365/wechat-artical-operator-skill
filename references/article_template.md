# 微信公众号文章排版规范

## 基础样式

### 标题层级

```html
<!-- 主标题 -->
<h1 style="text-align: center; font-size: 20px; color: #333; margin: 20px 0;">
  文章主标题
</h1>

<!-- 一级小节 -->
<h2 style="font-size: 18px; color: #1a73e8; border-left: 4px solid #1a73e8; 
          padding-left: 12px; margin: 30px 0 15px;">
  01 小标题
</h2>

<!-- 二级小节 -->
<h3 style="font-size: 16px; color: #555; margin: 25px 0 10px;">
  1.1 子标题
</h3>
```

### 正文段落

```html
<p style="font-size: 16px; line-height: 1.8; color: #333; 
         text-align: justify; margin: 15px 0;">
  正文内容...
</p>
```

### 引用块

```html
<blockquote style="border-left: 4px solid #ddd; padding: 15px 20px; 
                   background: #f9f9f9; margin: 20px 0; 
                   color: #666; font-style: italic;">
  引用内容...
</blockquote>
```

### 代码块

```html
<pre style="background: #282c34; color: #abb2bf; padding: 15px; 
            border-radius: 6px; overflow-x: auto; margin: 20px 0;">
  <code style="font-family: 'Fira Code', monospace; font-size: 14px;">
    const hello = "world";
  </code>
</pre>
```

### 强调文本

```html
<!-- 加粗 -->
<strong style="color: #1a73e8; font-weight: 600;">重点内容</strong>

<!-- 高亮 -->
<mark style="background: #fff3cd; padding: 2px 6px; border-radius: 3px;">
  高亮内容
</mark>
```

### 列表

```html
<!-- 无序列表 -->
<ul style="padding-left: 20px; margin: 15px 0;">
  <li style="margin: 8px 0; line-height: 1.8;">列表项一</li>
  <li style="margin: 8px 0; line-height: 1.8;">列表项二</li>
</ul>

<!-- 有序列表 -->
<ol style="padding-left: 20px; margin: 15px 0;">
  <li style="margin: 8px 0; line-height: 1.8;">第一步</li>
  <li style="margin: 8px 0; line-height: 1.8;">第二步</li>
</ol>
```

### 图片

```html
<figure style="margin: 25px 0; text-align: center;">
  <img src="图片 URL" alt="图片说明" 
       style="max-width: 100%; height: auto; border-radius: 8px; 
              box-shadow: 0 2px 12px rgba(0,0,0,0.1);">
  <figcaption style="font-size: 14px; color: #999; margin-top: 10px;">
    图片说明文字
  </figcaption>
</figure>
```

### 分割线

```html
<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
```

### 文末引导

```html
<div style="text-align: center; margin: 40px 0; padding: 20px; 
            background: #f5f5f5; border-radius: 8px;">
  <p style="font-size: 16px; color: #666; margin: 0;">
    喜欢这篇文章吗？欢迎关注公众号获取更多干货
  </p>
</div>
```

---

## 封面图规范

| 项目 | 要求 |
|------|------|
| 尺寸 | 900×383 像素（2.35:1） |
| 大小 | ≤ 2MB |
| 格式 | JPG / PNG |
| 建议 | 文字居中，留足边距 |

---

## 常用配色方案

### 科技蓝
- 主色：`#1a73e8`
- 辅色：`#4285f4`
- 背景：`#f8f9fa`

### 商务灰
- 主色：`#333333`
- 辅色：`#666666`
- 背景：`#f5f5f5`

### 活力橙
- 主色：`#ff6b35`
- 辅色：`#ff8c42`
- 背景：`#fff5f0`

---

## 注意事项

1. **字体大小**：正文 15-16px，注释 13-14px
2. **行间距**：1.7-1.8 倍行距最佳
3. **字间距**：保持默认即可
4. **两端对齐**：提升阅读体验
5. **段间距**：15-20px，避免过密
6. **颜色数量**：全文主色不超过 3 种
