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
