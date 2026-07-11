// rss-transform.js
// Renders this RSS feed as the site's own RSS page when opened directly in a browser.
// Feed readers/aggregators ignore this script since they only parse the XML.

const HTML_NS = 'http://www.w3.org/1999/xhtml';

function el(tag, props, ...children) {
  const node = document.createElementNS(HTML_NS, tag);
  if (props) {
    for (const [key, value] of Object.entries(props)) {
      node.setAttribute(key, value);
    }
  }
  for (const child of children.flat()) {
    if (child == null) continue;
    node.append(child.nodeType ? child : document.createTextNode(String(child)));
  }
  return node;
}

function text(scope, selector) {
  return scope.querySelector(`:scope > ${selector}`)?.textContent?.trim() ?? '';
}

// Matches original XSLT's substring(pubDate, 6, 11) — e.g. "Mon, 05 May 2025 00:00:00 GMT" -> "05 May 2025"
function shortDate(pubDate) {
  return pubDate.substring(5, 16);
}

const INLINE_CSS = `html,body{background-color:rgb(251, 250, 247)}@media(prefers-color-scheme:dark){html,body{background-color:rgb(22, 23, 24);}}.subscribe{width:max-content;max-width:100%; text-transform:inherit;text-decoration:underline;text-decoration-thickness:2px;text-decoration-color:rgb(var(--accent));text-underline-offset:2px;text-decoration-skip-ink:all;;word-break:break-all;cursor:pointer;transition:background .2s ease;}@media(hover:hover) and (pointer:fine){.subscribe:hover{opacity:.6};}.flex .rss-item>*+*{margin-block-start:var(--space--2);}hr.rss-feed{margin-block-start:var(--space-2);margin-block-end:var(--space-2);}p.pub-date{color:rgb(var(--accent));}`;

const COPY_SCRIPT = `function copyToClipboard(element){const text=element.textContent;navigator.clipboard.writeText(text).then(()=>{const originalText=element.textContent;const originalColor=element.style.color;const originalDecoration=element.style.textDecoration;element.textContent="Copied!";element.style.color="rgb(var(--primary))";element.style.textDecoration="none";setTimeout(()=>{element.textContent=originalText;element.style.color=originalColor;element.style.textDecoration=originalDecoration},2000)}).catch(err=>{console.error('Failed to copy:',err)})}
function copyEmail(){const email="max@maxsheridan.com";const copyLink=document.getElementById('copyLink');navigator.clipboard.writeText(email).then(()=>{const originalText=copyLink.textContent;const originalColor=copyLink.style.color;copyLink.textContent="Copied!";copyLink.style.color="var(--primary)";setTimeout(()=>{copyLink.textContent=originalText;copyLink.style.color=originalColor},2000)}).catch(err=>{alert('Failed to copy email: '+err)})}`;

function itemToHTML(itemEl) {
  const title = text(itemEl, 'title');
  const link = text(itemEl, 'link');
  const pubDate = text(itemEl, 'pubDate');

  return el(
    'div',
    { class: 'rss-item' },
    el('span', { class: 'rss-title' }, el('a', { href: link }, title)),
    el('p', { class: 'pub-date' }, 'Published on: ', shortDate(pubDate)),
  );
}

function render() {
  const rss = document.documentElement;
  const channel = rss.querySelector(':scope > channel');
  if (!channel) return;

  const atomLink = channel.getElementsByTagNameNS('http://www.w3.org/2005/Atom', 'link')[0]
    ?.getAttribute('href') ?? '';
  const items = [...channel.querySelectorAll(':scope > item')];

  const html = el(
    'html',
    { lang: 'en' },
    el(
      'head',
      null,
      el('meta', { charset: 'utf-8' }),
      el('meta', { 'http-equiv': 'X-UA-Compatible', content: 'IE=edge' }),
      el('meta', { name: 'viewport', content: 'width=device-width, initial-scale=1' }),
      el('meta', { name: 'color-scheme', content: 'light dark' }),
      el('meta', { name: 'theme-color', media: '(prefers-color-scheme: light)', content: '#EAE9E6' }),
      el('meta', { name: 'theme-color', media: '(prefers-color-scheme: dark)', content: '#161718' }),
      el('link', { rel: 'preload', href: '/assets/type/hexfranklinnarrow_regular.woff2', as: 'font', type: 'font/woff2', crossorigin: 'anonymous' }),
      el('link', { rel: 'preload', href: '/assets/type/bigshoulders_variable.woff2', as: 'font', type: 'font/woff2', crossorigin: 'anonymous' }),
      el('style', null, INLINE_CSS),
      el('link', { rel: 'stylesheet', href: '/assets/css/shared.min.css?v=3' }),
      el('link', { rel: 'icon', href: '/favicon.ico?v=2', type: 'image/x-icon', sizes: '48x48' }),
      el('link', { rel: 'icon', href: '/favicon.svg?v=2', type: 'image/svg+xml', sizes: 'any' }),
      el('title', null, 'RSS Updates - Max Sheridan'),
    ),
    el(
      'body',
      null,
      el('a', { href: '#main-content', class: 'skip-link' }, 'Skip to content'),
      el(
        'header',
        { class: 'linkstyling-off' },
        el('hr', { 'aria-hidden': 'true' }),
        el('a', { href: '/', 'aria-label': 'Max Sheridan home' }, 'Max Sheridan'),
        el('hr', { 'aria-hidden': 'true' }),
      ),
      el(
        'main',
        { id: 'main-content', class: 'flex rss-feed', tabindex: '-1' },
        el(
          'div',
          null,
          el('h1', null, 'RSS Feed'),
          el(
            'p',
            null,
            'This is an old-school RSS feed. Copy the URL below and paste it into your feed reader and you\u2019re set. Or click on a link to read my latest updates.',
          ),
          el(
            'button',
            { class: 'subscribe', onclick: 'copyToClipboard(this)', type: 'button', 'aria-label': 'Copy RSS feed URL to clipboard' },
            atomLink,
          ),
          el('hr', { class: 'rss-feed', 'aria-hidden': 'true' }),
          items.map(itemToHTML),
        ),
      ),
      el(
        'footer',
        { class: 'linkstyling-off', 'aria-label': 'Footer' },
        el(
          'ul',
          null,
          el('li', { class: 'inline-hr big-screen', 'aria-hidden': 'true' }),
          el('li', null, el('a', { href: '/short-fiction', 'aria-current': 'page' }, 'Short Fiction')),
          el('li', { class: 'inline-hr', 'aria-hidden': 'true' }),
          el('li', null, el('a', { href: '/news' }, 'News')),
          el('li', { class: 'inline-hr', 'aria-hidden': 'true' }),
          el('li', null, el('button', { id: 'copyLink', 'aria-label': 'Copy email address', type: 'button', onclick: 'copyEmail()' }, 'Email')),
          el('li', { class: 'inline-hr big-screen', 'aria-hidden': 'true' }),
        ),
      ),
      (() => {
        const script = el('script', null);
        script.textContent = COPY_SCRIPT;
        return script;
      })(),
    ),
  );

  rss.replaceWith(html);
}

render();