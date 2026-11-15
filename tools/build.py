"""Build three independent pages and a self-contained HTML edition."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'templates/style.css').read_text(encoding='utf-8')
HOME = (ROOT / 'templates/home.html').read_text(encoding='utf-8')

def note(title, what, problem, solution, source, source_title, category, status):
    return f'''<article class="entry" data-category="{category}"><div class="entry-meta"><time datetime="2026-11-14">2026.11.14 · 项目复盘</time><span class="tag">{category}</span><span>{status}</span></div><h2>{title}</h2><div class="entry-grid"><b>学到什么</b><p>{what}</p><b>遇到问题</b><p>{problem}</p><b>处理 / 下一步</b><p>{solution}</p></div><div class="entry-source">相关项目：<a href="{source}" target="_blank" rel="noopener noreferrer">{source_title}</a></div></article>'''

NOTES = ''.join([
note('串口连接排查', '参与 FPGA 项目的电脑串口界面，把界面操作与板端控制联系起来。先确认通信路径，再排查具体功能，是这次实践中需要坚持的顺序。', '项目最开始，电脑串口与板子难以建立连接。', '保留这一问题作为联调复盘。下一轮按端口识别、端口占用、通信参数和命令响应逐项记录，并为界面补充连接状态与错误提示。接下来重点补全连接日志，确认具体根因。', 'https://github.com/Jingzhe-chen714/fpga', 'FPGA 项目与串口控制说明', 'FPGA', '待补充根因'),
note('串口界面与显示同步', '串口控制界面、板端处理和显示屏刷新之间存在多个环节；观察到同一画面，并不等于已经验证严格同步。', '串口界面与显示屏难以做到百分之百同步，整体流畅度还不够。', '目前仍是待改进事项。计划分别记录命令发送、板端响应和显示变化的时间；再检查界面刷新是否受阻、是否重复发送命令。仓库的仿真与编译记录可以辅助分析，不能替代真实设备测试。', 'https://github.com/Jingzhe-chen714/fpga/blob/main/README.md', 'README：已有验证结果与适用范围', 'FPGA', '持续改进'),
note('集合边界测试', '在数据结构项目中负责集合与测试。数组集合需要处理固定容量，链表集合需要管理节点与字符串的生命周期。', '测试需要确认重复添加是否改变大小、空集合运算是否正确，以及删除首节点、中间节点和末节点后结构是否仍然有效。我把这些情况作为边界测试的重点。', '仓库已覆盖基本集合运算、重复元素、删除边界、清空后复用和结果写回等场景。现有测试记录通过；链表分配失败模拟与内存检测仍是后续补充方向。', 'https://gitee.com/chen-xiaoyu33/data-structure-course-design', '集合源码、测试程序与设计说明', 'C 语言', '已有测试记录'),
])

JOURNAL = '''<header class="page-title"><div class="title-line"><h1>学习记录</h1></div><p>按整理日期记录项目中遇到的问题、尝试和后续计划。</p></header><div class="searchbar"><div class="search-field"><label for="note-search">搜索学习记录</label><input id="note-search" type="search" placeholder="试试：串口、同步、集合" maxlength="100"></div><div class="filters" aria-label="学习记录分类"><button class="filter" data-note-filter="全部" aria-pressed="true" type="button">全部</button><button class="filter" data-note-filter="FPGA" aria-pressed="false" type="button">FPGA</button><button class="filter" data-note-filter="C 语言" aria-pressed="false" type="button">C 语言</button></div></div><p class="result-info" id="note-count" aria-live="polite">共 3 条学习记录</p><div class="journal-layout"><div><div id="notes">''' + NOTES + '''</div><p id="note-empty" class="empty" hidden>没有找到匹配的记录，试试其他关键词或分类。</p></div></div><details class="write-box" aria-labelledby="write-title"><summary id="write-title">添加学习记录</summary><p class="hint">记录保存在当前浏览器，可以导出 JSON 备份；换设备或清除浏览器数据前，记得先导出。</p><form id="note-form"><div class="form-grid"><div><label for="new-title">标题 *</label><input id="new-title" name="title" required maxlength="80" placeholder="这一次，我弄懂了什么？"></div><div><label for="new-date">整理日期 *</label><input id="new-date" name="date" type="date" value="2026-11-15" required min="2000-01-01" max="2100-12-31"></div><div class="full"><label for="new-what">学了什么 *</label><textarea id="new-what" name="what" required maxlength="1200" placeholder="具体任务、知识点或作品"></textarea></div><div class="full"><label for="new-problem">遇到什么问题 *</label><textarea id="new-problem" name="problem" required maxlength="1200" placeholder="描述现象，也可以记录还没理解的地方"></textarea></div><div class="full"><label for="new-solution">如何处理 / 下一步 *</label><textarea id="new-solution" name="solution" required maxlength="1200" placeholder="写清已做的尝试和仍需验证的部分"></textarea></div></div><div class="form-actions"><button type="submit" class="button">保存到当前浏览器</button><button id="export-notes" type="button" class="button secondary">导出我的记录</button></div><p id="form-status" class="status" role="status"></p></form></details>'''

snippet = escape('''int set_contains(const LinkedSet *set, const char *text)
{
    const Node *current = set->head;
    while (current != NULL) {
        if (strcmp(current->text, text) == 0) return 1;
        current = current->next;
    }
    return 0;
}''')

PROJECTS = '''<header class="page-title"><div class="title-line"><h1>项目</h1></div><p>整理目前参与的项目、具体分工和遇到的问题。</p></header><div class="filters" aria-label="项目分类"><button class="filter" data-project-filter="全部" aria-pressed="true" type="button">全部作品</button><button class="filter" data-project-filter="FPGA" aria-pressed="false" type="button">FPGA / 交互</button><button class="filter" data-project-filter="C 语言" aria-pressed="false" type="button">C / 数据结构</button></div><p class="result-info" id="project-count" aria-live="polite">共 2 个项目</p>
<article class="project" data-category="FPGA"><div><div class="tags"><span class="tag">FPGA</span><span class="tag">串口界面</span><span class="tag">团队项目</span></div><h2>Ti60 实时视觉与串口控制</h2><p class="summary">面向摄像头图像处理和电脑端控制的系统。仓库包括 Sobel / Canny 边缘处理、几何识别、板端工程、电脑控制台与验证资料。</p><dl><dt>解决问题</dt><dd>通过电脑端串口界面控制视觉处理功能，连接板端处理与显示输出。</dd><dt>我的分工</dt><dd>负责电脑端串口界面。具体视觉算法、硬件与系统整体成果属于团队项目范围。</dd><dt>使用技术</dt><dd>串口交互、电脑控制台；系统整体基于 Ti60 FPGA 与 Verilog / SystemVerilog 工程。</dd><dt>主要困难</dt><dd>初始串口连接困难；界面与显示屏同步不足，流畅度仍有提升空间。</dd><dt>当前进展</dt><dd>已有编译与仿真记录，后续继续完成实板联调，检查设备响应与显示效果。</dd></dl><div class="project-links"><a href="https://github.com/Jingzhe-chen714/fpga" target="_blank" rel="noopener noreferrer">查看项目仓库</a><a data-page="journal" href="learning.html">阅读联调复盘</a></div><details><summary>查看项目结构与后续验证计划</summary><pre>FPGA_engin/        板端工程入口与 RTL
开发源码/pc_v11/   电脑控制台源码
开发源码/tb/       测试台
说明文档/          使用与交付说明
验证记录/          已有仿真与报告</pre><p>下一步：记录连接失败的具体日志；为命令与显示变化添加时间标记；分别测试串口响应和界面刷新。</p></details><p class="tiny">项目仓库目前为私有，页面保留主要结构与实践记录。</p></div></article>
<article class="project" data-category="C 语言"><div><div class="tags"><span class="tag">C 语言</span><span class="tag">集合</span><span class="tag">测试</span></div><h2>字符串集合与数据结构实践</h2><p class="summary">这个仓库包含集合、英文文本排版、外部排序等练习。我参与的部分是集合实现与测试，用两种结构理解相同操作的实现差异。</p><dl><dt>解决问题</dt><dd>用数组和链表表示字符串集合，实现添加、删除、并集、交集、差集、子集判断等操作。</dd><dt>我的分工</dt><dd>负责集合与测试；针对重复元素、空集合、删除边界、容量限制和结果写回检查程序行为。</dd><dt>使用技术</dt><dd>C11、数组、链表、动态内存管理、assert 断言测试、Git。</dd><dt>关键挑战</dt><dd>需要兼顾容量和字符串边界，并正确释放链表节点与字符串；这是实现及测试的关注点。</dd><dt>当前证据</dt><dd>仓库保留数组与链表源码、测试程序和测试记录。分配失败模拟与内存检测可继续补充。</dd></dl><div class="project-links"><a href="https://gitee.com/chen-xiaoyu33/data-structure-course-design" target="_blank" rel="noopener noreferrer">查看 Gitee 仓库</a><a href="https://gitee.com/chen-xiaoyu33/data-structure-course-design/tree/master/task1_set" target="_blank" rel="noopener noreferrer">查看集合源码与测试</a></div><details open><summary>代码证据：遍历链表判断成员是否存在</summary><pre><code>''' + snippet + '''</code></pre><p>摘编自 task1_set/linked_set.c 的 set_contains，压缩了部分排版。逐个比较字符串，命中返回 1，遍历结束返回 0；若忽略字符串比较长度因素，时间复杂度为 O(n)。</p></details></div></article>
<section class="section"><div class="section-heading"><div><h2>其他协作记录</h2></div></div><h3>本地 OCR 图片与文档识别工具</h3><p class="about-copy">我参与的另一个团队项目是 <a href="https://github.com/weijiayue19/project6" target="_blank" rel="noopener noreferrer">project6</a>。项目采用 Python、PaddleOCR、Tkinter 与 SQLite，提供图片 / PDF 识别、识别结果编辑和历史检索。后续继续补充这个项目的实践笔记。</p></section><p class="project-end"><a data-page="journal" href="learning.html">查看相关学习记录</a></p>'''

JS = r'''
'use strict';
(() => {
  const single = document.body.dataset.single === 'true';
  const views = [...document.querySelectorAll('.view')];
  function route() {
    if (!single) return;
    const page = ['home','journal','projects'].includes(location.hash.slice(1)) ? location.hash.slice(1) : 'home';
    for (const view of views) view.hidden = view.dataset.view !== page;
    for (const link of document.querySelectorAll('.nav [data-page]')) {
      if (link.dataset.page === page) link.setAttribute('aria-current','page');
      else link.removeAttribute('aria-current');
    }
    document.title = ({home:'首页',journal:'学习记录',projects:'项目'})[page] + ' · 陈小雨';
  }
  if (single) {
    for (const link of document.querySelectorAll('[data-page]')) link.href = '#' + link.dataset.page;
    document.querySelector('.skip').addEventListener('click', event => {
      event.preventDefault();
      const main = document.querySelector('main');
      main.tabIndex = -1;
      main.focus();
    });
    window.addEventListener('hashchange', () => {route(); window.scrollTo(0,0);});
    route();
  }
  const notes = document.getElementById('notes');
  const search = document.getElementById('note-search');
  let category = '全部';
  function filterNotes(){
    if (!notes) return;
    const keyword = search.value.trim().toLocaleLowerCase();
    let count=0;
    for (const entry of notes.querySelectorAll('.entry')) {
      const match = (!keyword || entry.textContent.toLocaleLowerCase().includes(keyword)) && (category==='全部'||entry.dataset.category===category);
      entry.hidden=!match; if(match)count++;
    }
    document.getElementById('note-count').textContent='共 '+count+' 条学习记录';
    document.getElementById('note-empty').hidden=count!==0;
  }
  search?.addEventListener('input',filterNotes);
  for (const btn of document.querySelectorAll('[data-note-filter]')) btn.addEventListener('click',()=>{
    category=btn.dataset.noteFilter;
    for(const b of document.querySelectorAll('[data-note-filter]'))b.setAttribute('aria-pressed',String(b===btn));
    filterNotes();
  });
  for (const btn of document.querySelectorAll('[data-project-filter]'))btn.addEventListener('click',()=>{
    let count=0;
    for(const b of document.querySelectorAll('[data-project-filter]'))b.setAttribute('aria-pressed',String(b===btn));
    for(const project of document.querySelectorAll('.project')){
      project.hidden=btn.dataset.projectFilter!=='全部'&&project.dataset.category!==btn.dataset.projectFilter;
      if(!project.hidden)count++;
    }
    document.getElementById('project-count').textContent='共 '+count+' 个项目';
  });
  const form=document.getElementById('note-form');
  if(!form)return;
  const status=document.getElementById('form-status');
  const key='cxy_growth_notes_v1';
  let localNotes=[];
  let writable=true;
  const maxLengths={title:80,date:10,what:1200,problem:1200,solution:1200};
  function valid(item){return item&&Object.entries(maxLengths).every(([key,max])=>typeof item[key]==='string'&&item[key].trim()&&item[key].length<=max)&&/^\d{4}-\d{2}-\d{2}$/.test(item.date)&&item.date>='2000-01-01'&&item.date<='2100-12-31';}
  function message(text,error=false){status.textContent=text;status.classList.toggle('error',error);}
  function addLocal(item){
    const article=document.createElement('article');article.className='entry local-entry';article.dataset.category='个人记录';
    const meta=document.createElement('div');meta.className='entry-meta';
    const time=document.createElement('time');time.dateTime=item.date;time.textContent=item.date.replaceAll('-','.');
    const tag=document.createElement('span');tag.className='tag';tag.textContent='浏览器本地记录';meta.append(time,tag);
    const title=document.createElement('h2');title.textContent=item.title;
    const grid=document.createElement('div');grid.className='entry-grid';
    for(const [label,field] of [['学到什么','what'],['遇到问题','problem'],['处理 / 下一步','solution']]){
      const b=document.createElement('b');b.textContent=label;const p=document.createElement('p');p.textContent=item[field];grid.append(b,p);
    }
    article.append(meta,title,grid);notes.prepend(article);
  }
  try{
    const raw=localStorage.getItem(key);
    if(raw!==null){const loaded=JSON.parse(raw);if(!Array.isArray(loaded)||loaded.length>300||!loaded.every(valid))throw Error('invalid');localNotes=loaded;localNotes.forEach(addLocal);}
  }catch{writable=false;message('无法读取本地存储，或已有记录格式异常。原数据未改动；新记录仍可临时添加，请及时导出。',true);}
  form.addEventListener('submit',event=>{
    event.preventDefault();
    if(!form.reportValidity())return;
    const item=Object.fromEntries(Object.keys(maxLengths).map(key=>[key,form.elements.namedItem(key).value.trim()]));
    if(!valid(item)){message('请填写所有内容，不能只输入空格，并检查日期。',true);return;}
    if(localNotes.length>=300){message('本地记录已达 300 条，请先导出留存，公开更新可整理到网页源码中。',true);return;}
    localNotes.push(item);addLocal(item);
    let saved=false;
    if(writable){try{localStorage.setItem(key,JSON.stringify(localNotes));saved=true;}catch{writable=false;}}
    category='全部';search.value='';for(const btn of document.querySelectorAll('[data-note-filter]'))btn.setAttribute('aria-pressed',String(btn.dataset.noteFilter==='全部'));
    filterNotes();form.reset();
    message(saved?'已保存到当前浏览器。公开网页内容不会自动更新，请导出留存。':'已临时添加，但本地存储不可用；刷新会丢失本次新增内容，请立即导出。',!saved);
  });
  document.getElementById('export-notes').addEventListener('click',()=>{
    if(!localNotes.length){message('还没有新增记录。填写表单后即可导出。');return;}
    const blob=new Blob([JSON.stringify({version:1,notes:localNotes},null,2)],{type:'application/json;charset=utf-8'});
    const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='陈小雨-学习记录.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);
    message('已生成 JSON 下载文件，请妥善留存。');
  });
  filterNotes();
})();
'''

def document(page, standalone=False):
    labels={'home':('首页','index.html'),'journal':('学习记录','learning.html'),'projects':('项目','projects.html')}
    nav=''.join(f'<a data-page="{k}" href="{v[1]}"'+(' aria-current="page"' if page==k else '')+f'>{v[0]}</a>' for k,v in labels.items())
    style=f'<style>{CSS}</style>' if standalone else '<link rel="stylesheet" href="assets/style.css">'
    script=f'<script>{JS}</script>' if standalone else '<script src="assets/app.js" defer></script>'
    content=''.join(f'<div class="view" data-view="{k}">{v}</div>' for k,v in [('home',HOME),('journal',JOURNAL),('projects',PROJECTS)] if standalone or page==k)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="陈小雨的个人主页：项目、学习记录与编程实践。"><meta name="color-scheme" content="light"><title>{labels[page][0]} · 陈小雨</title>{style}</head>
<body data-single="{str(standalone).lower()}"><a class="skip" href="#main">跳到主要内容</a><header class="site-header"><div class="wrap header-inner"><a class="brand" data-page="home" href="index.html">陈小雨</a><nav class="nav" aria-label="主导航">{nav}</nav><a class="github-link" href="https://github.com/Jingzhe-chen714" target="_blank" rel="noopener noreferrer">GitHub</a></div></header><main class="wrap" id="main"><noscript><p class="noscript">JavaScript 未启用，静态内容仍可阅读；筛选与记录表单需要启用 JavaScript。</p></noscript>{content}</main><footer class="wrap footer"><span>© 2026 陈小雨</span><span>更新于 2026-11-15</span></footer>{script}</body></html>'''

if __name__=='__main__':
    (ROOT/'assets').mkdir(exist_ok=True)
    (ROOT/'assets/style.css').write_text(CSS,encoding='utf-8')
    (ROOT/'assets/app.js').write_text(JS,encoding='utf-8')
    for page,name in [('home','index.html'),('journal','learning.html'),('projects','projects.html')]:
        (ROOT/name).write_text(document(page),encoding='utf-8')
    (ROOT/'陈小雨-个人成长主页.html').write_text(document('home',True),encoding='utf-8')
    print('Built 3 pages and 1 self-contained HTML edition.')
