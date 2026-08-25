# MD 阅读器

![GitHub Release](https://img.shields.io/github/v/release/LittlePenhu/md-reader)
![Downloads](https://img.shields.io/github/downloads/LittlePenhu/md-reader/total)
![Language](https://img.shields.io/github/languages/top/LittlePenhu/md-reader)

本地 Markdown 阅读器：美观、双击即用、纯本地运行（不上传任何数据）。
默认界面风格：黛绿 · 新中式（可在应用内随时切换 5 种风格 × 深浅色）。

## 功能

- **主页**：启动后默认打开主页——最近文件卡片列表（含相对时间）、一键打开、支持把 .md 文件直接拖进窗口
- **设置页**（工具栏 ⚙）：默认界面风格（5 种主题卡片：黛绿 / 书卷 / 极简 / 紫夜 / OLED 纯黑）、深浅色（含"跟随系统"）、字号滑块、页面宽度、启动行为（默认主页 / 恢复上次文件）、清除阅读记录
- 目录侧边栏：自动提取 h1-h3，点击跳转，滚动时高亮当前章节（可按 ☰ 隐藏）
- 全文搜索：`Ctrl+F`，高亮全部匹配，↑/↓ 或 Enter 跳转上/下一个，Esc 关闭（输入防抖，大文档不卡）
- 5 种界面风格：黛绿 / 书卷 / 极简 / 紫夜 / OLED 纯黑（纯黑背景省电配色，深色模式下生效），每种含深浅两套配色；主题在 设置 → 外观 中修改，工具栏只保留深浅色快捷切换
- 代码高亮：marked.js + highlight.js（本地 `web/libs/` 优先，离线可用；CDN 仅作后备：unpkg → jsdelivr → cdnjs → bootcdn）；代码块 hover 显示语言标签与一键复制
- 安全渲染：DOMPurify 清洗 HTML，md 内嵌的危险标签/属性不会执行
- 本地图片：md 中的相对路径图片自动基于文件所在目录加载（file:// 直载，失败时 base64 兜底）
- 阅读进度：按文件记忆滚动位置，重新打开自动恢复
- 自动刷新：文件被外部编辑后自动重载（窗口聚焦时检测 + 3 秒轮询，保持阅读位置）；F5 / Ctrl+R 手动刷新
- 字号调节：`Ctrl+=` / `Ctrl+-` 放大缩小，`Ctrl+0` 复原（工具栏 A+ / A− 按钮），设置持久化
- 链接安全：外部链接由系统浏览器打开，不会把应用窗口导航走；文档内 `#锚点` 平滑跳转（GFM 风格标题 slug）
- 记忆：最近 10 个文件列表（带打开时间，失效路径自动清理）
- 编码自适应：UTF-8（含 BOM）/ GB18030 / UTF-16（含 BOM）自动识别
- 其他：YAML front matter 自动剥离、大文件保护（>10MB 拒绝打开）、`Ctrl+O` 打开文件、⌂ 回主页
- 快捷键：`Ctrl+F` 搜索 · `Ctrl+O` 打开 · `Ctrl+=/-/0` 字号 · `F5`/`Ctrl+R` 刷新 · `Esc` 关闭搜索

## 使用

**下载最新版**：[GitHub Releases](https://github.com/LittlePenhu/md-reader/releases) 下载 `MDReader-vX.X.X.exe`（双击即用，无终端窗口）。
命令行方式：`MDReader-vX.X.X.exe 文件.md` 可直接打开指定文件。

## 从源码运行

```powershell
# 1. 安装 Python（Miniconda 推荐：https://www.anaconda.com/download）
# 2. 安装依赖
pip install pywebview

# 3. 运行（两种方式任选）
python app.py                 # 打开窗口，自动恢复上次文件与阅读进度
python app.py 文件.md         # 直接打开指定文件
```

## 重新打包 exe

```powershell
pip install pyinstaller
pyinstaller --onefile --noconsole --name "MD阅读器" --add-data "web;web" app.py
# 产物：dist\MD阅读器.exe（--noconsole = 启动时不弹终端；web\libs\ 一并打入，离线可用）
```

## 右键"打开方式"注册（可选）

保存为 `注册打开方式.reg` 双击导入（把路径改成你的实际路径），之后在任意 .md 文件上
右键 → 打开方式 → MD 阅读器：

```
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.md\Shell\OpenWithMDReader]
@="用 MD 阅读器打开"

[HKEY_CLASSES_ROOT\.md\Shell\OpenWithMDReader\command]
@="\"C:\\Users\\你的用户名\\Desktop\\MD阅读器\\MD阅读器.exe\" \"%1\""
```

> 注意：`pip install pywebview` 后第一次启动会自动使用系统自带的 Edge WebView2
> （Windows 10/11 内置）。若你的系统没有 WebView2 Runtime，会提示安装，装一次即可。

## 图标与署名

应用图标来自 [Flaticon](https://www.flaticon.com)（双马尾女孩，作者 Freepik），
按 Flaticon 免费许可要求在此署名致谢。原图保留在 `icons/候选6_双马尾女孩_Flaticon.png`。
想换图标：把新图放到 `icons/`，用 Pillow 转成 `app.ico`（参考 `icons/gen_icons.py`），
再按上方命令重新打包。

## 目录结构

```
MD阅读器/
├── app.py          # 主程序（窗口 + 文件读写 + 图片/进度/状态）
├── web/
│   ├── index.html  # 界面（主页 + 设置页 + 阅读视图 + 目录 + 搜索，单文件）
│   └── libs/       # marked / highlight.js / DOMPurify 本地副本（离线渲染用）
└── README.md
```
