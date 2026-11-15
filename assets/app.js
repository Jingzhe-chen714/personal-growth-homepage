
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
  // 反馈是本地草稿；邮件链接仅打开撰写窗口，不会代替访客发送。
function setupFeedback() {
  const form = document.getElementById('feedback-form');
  if (!form) return;
  const name = document.getElementById('feedback-name');
  const content = document.getElementById('feedback-content');
  const draft = document.getElementById('feedback-draft');
  const status = document.getElementById('feedback-status');
  const copy = document.getElementById('feedback-copy');
  const email = document.getElementById('feedback-email');

  form.addEventListener('submit', event => {
    event.preventDefault();
    const message = content.value.trim();
    if (!message) {
      status.textContent = '请填写建议或问题，不能只输入空格。';
      status.classList.add('error');
      content.focus();
      return;
    }
    draft.value = '称呼：' + (name.value.trim() || '访客') + '\n反馈：' + message;
    document.getElementById('feedback-preview').hidden = false;
    copy.disabled = false;
    email.href = 'mailto:166528786@qq.com?subject=' + encodeURIComponent('个人主页反馈') + '&body=' + encodeURIComponent(draft.value);
    status.classList.remove('error');
    status.textContent = '草稿已生成，尚未发送。请复制反馈，或点击“用邮件发送”后自行确认发送。';
  });

  // 修改输入后清除旧草稿状态，避免误发上一条内容。
  form.addEventListener('input', event => {
    if (event.target === draft) return;
    copy.disabled = true;
    document.getElementById('feedback-preview').hidden = true;
    email.href = 'mailto:166528786@qq.com?subject=' + encodeURIComponent('个人主页反馈');
    status.textContent = '';
  });

  copy.addEventListener('click', async () => {
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(draft.value);
      status.textContent = '已复制反馈，尚未发送。可以粘贴到邮件或其他沟通工具。';
    } catch {
      draft.focus();
      draft.select();
      status.textContent = '请在草稿框中手动复制，再通过邮件发送。';
    }
  });
  // 脚本成功绑定后才允许提交；脚本不可用时不把输入当作GET参数传出。
  form.querySelector('button[type="submit"]').disabled = false;
}
setupFeedback();

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
  form.querySelector('button[type=submit]').disabled = false;
  filterNotes();
})();
