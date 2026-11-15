"""Build three independent pages and a self-contained HTML edition."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / 'templates/style.css').read_text(encoding='utf-8')
FEEDBACK = (ROOT / 'templates/feedback.html').read_text(encoding='utf-8')
FEEDBACK_JS = (ROOT / 'templates/feedback.js').read_text(encoding='utf-8')
ASSET_VERSION = '20261115-r6'
HOME = (ROOT / 'templates/home.html').read_text(encoding='utf-8')

def note(title, what, problem, solution, source, source_title, category, status, date="2026-11-14"):
    return f'''<article class="entry" data-category="{category}"><div class="entry-meta"><time datetime="{date}">{date} · 项目复盘</time><span class="tag">{category}</span><span>{status}</span></div><h2>{title}</h2><div class="entry-grid"><b>学到什么</b><p>{what}</p><b>遇到问题</b><p>{problem}</p><b>处理 / 下一步</b><p>{solution}</p></div><div class="entry-source">相关项目：<a href="{source}" target="_blank" rel="noopener noreferrer">{source_title}</a></div></article>'''

NOTES = ''.join([
note('FPGA联调与显示同步', '负责电脑端串口界面，并参与软硬件联调，理解板端资源、视频输出和电脑显示之间的关系。', '现场显示器输出正常，但电脑端在接入分配器和采集卡前严重卡顿，长时间工作后会黑屏。原有板卡资源与硬件配置无法支撑预期的同步显示。', '已购买并加入分配器和采集卡，补充硬件配置，解决电脑端卡顿、长时间工作后黑屏的同步显示问题。项目于2026年9—10月完成；后续继续记录设备型号、连接步骤与长时间运行情况。', 'https://github.com/Jingzhe-chen714/fpga', 'FPGA项目源码与说明', 'FPGA', '项目已完成', '2026-10'),
note('集合实现与边界测试', '从2026年9月开始，负责数据结构项目中的集合实现与测试，比较数组和链表的存储方式。', '例如，重复添加apple后集合大小应保持3；99字节字符串应允许添加，100字节字符串应被拒绝；满容量并集失败时，原结果应保留。链表还需要覆盖首尾节点删除、释放与复用。', '集合源码与测试记录已整理到仓库；项目仍在进行，后续继续补充异常分配、内存检查和设计报告。', 'https://gitee.com/chen-xiaoyu33/data-structure-course-design', '集合源码与测试', 'C 语言', '项目进行中', '2026-09'),
note('本地OCR工具项目复盘', '2026年7月参与团队OCR项目，围绕图片与文档识别，了解识别结果编辑、SQLite历史记录和桌面界面的组合。', '需要把文件导入、识别、结果编辑与历史检索组织成完整流程。这里记录项目实践目标，具体个人模块将继续补充。', '团队项目已完成，仓库包含Python、PaddleOCR、Tkinter与SQLite相关源码和使用说明，可继续复盘代码结构与运行方式。', 'https://github.com/weijiayue19/project6', 'OCR团队项目', 'Python', '项目已完成', '2026-07'),
])

JOURNAL = '''<header class="page-title"><div class="title-line"><h1>学习记录</h1></div><p>以下按实际参与月份记录，更新截至2026年11月15日；2026年7—10月的项目实践均已发生。</p></header><div class="searchbar js-only"><div class="search-field"><label for="note-search">搜索学习记录</label><input id="note-search" type="search" placeholder="试试：串口、同步、集合" maxlength="100"></div><div class="filters" aria-label="学习记录分类"><button class="filter" data-note-filter="全部" aria-pressed="true" type="button">全部</button><button class="filter" data-note-filter="FPGA" aria-pressed="false" type="button">FPGA</button><button class="filter" data-note-filter="C 语言" aria-pressed="false" type="button">C 语言</button></div></div><p class="result-info" id="note-count" aria-live="polite">共 3 条学习记录</p><div class="journal-layout"><div><div id="notes">''' + NOTES + '''</div><p id="note-empty" class="empty" hidden>没有找到匹配的记录，试试其他关键词或分类。</p></div></div><details class="write-box" aria-labelledby="write-title"><summary id="write-title">添加学习记录</summary><p class="hint">启用脚本时，记录仅保存到当前浏览器并可导出；无脚本时，使用邮件客户端撰写记录，不会自动发送。</p><form id="note-form" action="mailto:166528786@qq.com?subject=学习记录分享" method="post" enctype="text/plain"><div class="form-grid"><div><label for="new-title">标题 *</label><input id="new-title" name="title" required maxlength="80" placeholder="这一次，我弄懂了什么？"></div><div><label for="new-date">整理日期 *</label><input id="new-date" name="date" type="date" value="2026-11-15" required min="2000-01-01" max="2100-12-31"></div><div class="full"><label for="new-what">学了什么 *</label><textarea id="new-what" name="what" required maxlength="1200" placeholder="具体任务、知识点或作品"></textarea></div><div class="full"><label for="new-problem">遇到什么问题 *</label><textarea id="new-problem" name="problem" required maxlength="1200" placeholder="描述现象，也可以记录还没理解的地方"></textarea></div><div class="full"><label for="new-solution">如何处理 / 下一步 *</label><textarea id="new-solution" name="solution" required maxlength="1200" placeholder="写清已做的尝试和仍需验证的部分"></textarea></div></div><div class="form-actions"><button type="submit" class="button">打开记录邮件</button><button id="export-notes" type="button" class="button secondary js-only">导出我的记录</button></div><p id="form-status" class="status" role="status"></p></form></details>'''

JOURNAL += FEEDBACK

PROJECTS = (ROOT / 'templates/projects.html').read_text(encoding='utf-8')

JS = r'''
'use strict';
(() => {
  // 渐进增强：无脚本时保留原生导航、阅读与邮件表单。
  document.body.classList.add('js-ready');
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
  ''' + FEEDBACK_JS + r'''
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
  form.querySelector('button[type=submit]').textContent = '保存到当前浏览器';
  filterNotes();
})();
'''

def document(page, standalone=False):
    labels={'home':('首页','index.html'),'journal':('学习记录','learning.html'),'projects':('项目','projects.html')}
    nav=''.join(f'<a data-page="{k}" href="{v[1]}"'+(' aria-current="page"' if page==k else '')+f'>{v[0]}</a>' for k,v in labels.items())
    style=f'<style>{CSS}</style>' if standalone else f'<link rel="stylesheet" href="assets/style.css?v={ASSET_VERSION}">'
    script=f'<script>{JS}</script>' if standalone else f'<script src="assets/app.js?v={ASSET_VERSION}" defer></script>'
    content=''.join(f'<div class="view" data-view="{k}">{v}</div>' for k,v in [('home',HOME),('journal',JOURNAL),('projects',PROJECTS)] if standalone or page==k)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="陈小雨的个人主页：项目、学习记录与编程实践。"><meta name="color-scheme" content="light"><title>{labels[page][0]} · 陈小雨</title>{style}</head>
<body data-single="{str(standalone).lower()}"><a class="skip" href="#main">跳到主要内容</a><header class="site-header"><div class="wrap header-inner"><a class="brand" data-page="home" href="index.html">陈小雨</a><nav class="nav" aria-label="主导航">{nav}</nav><a class="github-link" href="https://github.com/Jingzhe-chen714" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></header><main class="wrap" id="main"><noscript><p class="noscript">JavaScript 未启用：仍可访问三个页面、阅读全部内容并使用邮件表单。搜索可用浏览器的页面查找功能；本地保存、导出和筛选需要启用脚本。</p></noscript>{content}</main><footer class="wrap footer"><span>© 2026 陈小雨</span><span>更新于 2026.11.15</span><span class="footer-links"><a href="https://github.com/Jingzhe-chen714" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="mailto:166528786@qq.com">邮箱 ↗</a></span></footer>{script}</body></html>'''

if __name__=='__main__':
    (ROOT/'assets').mkdir(exist_ok=True)
    (ROOT/'assets/style.css').write_text(CSS,encoding='utf-8')
    (ROOT/'assets/app.js').write_text(JS,encoding='utf-8')
    for page,name in [('home','index.html'),('journal','learning.html'),('projects','projects.html')]:
        (ROOT/name).write_text(document(page),encoding='utf-8')
    (ROOT/'陈小雨-个人成长主页.html').write_text(document('home',True),encoding='utf-8')
    print('Built 3 pages and 1 self-contained HTML edition.')
