# 陈小雨的个人主页

个人项目、学习记录和实践笔记。

目前主要做 C 语言与数据结构练习，也参与 FPGA 视觉项目的串口界面开发。

![主页预览](screenshots/首页截图.jpg)

## 这里有什么

| 页面 | 内容 |
| --- | --- |
| [个人主页](index.html) | 关于我、学习方向、技能实践与联系方式 |
| [学习手记](learning.html) | 项目复盘、关键词搜索、分类筛选与记录表单 |
| [项目作品](projects.html) | 项目介绍、个人分工、技术细节与代码片段 |

还有一份[完整单文件版](陈小雨-个人成长主页.html)，将所有页面内容、样式与交互放在一个 HTML 中，方便离线浏览和分享。

## 本地浏览

这是一个使用 HTML、CSS 和原生 JavaScript 的静态网站，不需要安装依赖。

下载后直接打开 `index.html`，或在项目目录启动本地服务：

```sh
python -m http.server 8765 --bind 127.0.0.1
```

然后访问 <http://127.0.0.1:8765/>。页面适配桌面和手机，支持键盘操作。

## 最近的实践

- [Ti60 实时视觉与串口控制](https://github.com/Jingzhe-chen714/fpga)：我负责串口界面，正在复盘设备连接、显示同步与流畅度问题。仓库目前为私有。
- [数据结构练习](https://gitee.com/chen-xiaoyu33/data-structure-course-design)：我负责集合与测试，比较数组和链表实现，并检查重复元素、空集合、容量和删除边界。
- [本地 OCR 图片与文档识别工具](https://github.com/weijiayue19/project6)：参与的团队项目，使用 Python、PaddleOCR、Tkinter 和 SQLite。

## 记录与更新

学习手记页支持新增记录，并将内容保存在当前浏览器中；可以导出 JSON 备份。这些记录不会自动同步到 GitHub，换设备或清除浏览器数据前请先导出。

页面内容与样式在 `templates/` 中维护，学习记录和项目详情位于 `tools/build.py`。修改后运行：

```sh
python tools/build.py
```

脚本会重新生成三个独立页面、共享样式与脚本，以及完整单文件版。也可以直接编辑 HTML；如果使用生成脚本维护，请将改动同步回模板，以免下次生成时被覆盖。

后续会继续补充串口联调记录、集合测试和新的项目实践，也计划探索大模型应用开发。

## 找到我

[GitHub · Jingzhe-chen714](https://github.com/Jingzhe-chen714)
