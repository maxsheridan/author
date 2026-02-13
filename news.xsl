<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0" 
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:atom="http://www.w3.org/2005/Atom">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <meta charset="utf-8"/>
        <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, interactive-widget=resizes-content"/>
        <meta name="color-scheme" content="light dark"/>
        <link rel="preload" href="/assets/type/hexfranklin_variable.woff2" as="font" type="font/woff2" crossorigin="anonymous"/>
        <link rel="preload" href="/assets/type/bigshoulders_variable.woff2" as="font" type="font/woff2" crossorigin="anonymous"/>
        <style>html,body{background-color:rgb(251, 250, 247)}@media(prefers-color-scheme:dark){html,body{background-color:rgb(22, 23, 24);}}.subscribe{width:max-content;max-width:100%; text-transform:lowercase;text-decoration:underline;text-decoration-thickness:2px;text-decoration-color:rgb(var(--accent));text-underline-offset:2px;text-decoration-skip-ink:all;;word-break:break-all;cursor:pointer;transition:background .2s ease;}@media(hover:hover) and (pointer:fine){.subscribe:hover{opacity:.6};}.flex .rss-item>*+*{margin-block-start:var(--space--2);}hr.rss-feed{margin-block-start:var(--space-2);margin-block-end:var(--space-2);}p.pub-date{color:rgb(var(--accent));}</style>
        <link rel="stylesheet" href="/assets/css/shared.min.css?v=2"/>
        <link rel="icon" href="/favicon.ico?v=2" type="image/x-icon" sizes="48x48"/>
        <link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml" sizes="any"/>
        <title>RSS Updates - Max Sheridan</title>
      </head>
      <body>
        <a href="#main-content" class="skip-link">Skip to content</a>
        <header class="linkstyling-off">
          <hr aria-hidden="true"/>
          <a href="/" aria-label="Max Sheridan home">Max Sheridan</a>
          <hr aria-hidden="true"/>
        </header>
        
        <main id="main-content" class="flex rss-feed" tabindex="-1">
          <div>
            <h1>RSS Feed</h1>
            <p>
              This is an old-school RSS feed. Copy the URL below and paste it into your feed reader and you’re set. Or click on a link to read my latest updates.
            </p>
            <button class="subscribe" 
                    onclick="copyToClipboard(this)" 
                    type="button"
                    aria-label="Copy RSS feed URL to clipboard">
              <xsl:value-of select="/rss/channel/atom:link/@href"/>
            </button>
            <hr class="rss-feed"/>
            <xsl:for-each select="/*[local-name()='rss']/*[local-name()='channel']/*[local-name()='item']">
            <div class="rss-item">
              <span class="rss-title">
                <a href="{link}">
                  <xsl:value-of select="title"/>
                </a>
              </span>
              <p class="pub-date">
                Published on:
                <xsl:value-of select="substring(pubDate, 6, 11)"/>
              </p>
            </div>
            </xsl:for-each>
          </div>
        </main>
        
        <footer class="linkstyling-off" aria-label="Footer">
          <ul>
            <li class="inline-hr big-screen" aria-hidden="true"></li>
            <li><a href="/short-fiction" aria-current="page">Short Fiction</a></li>
            <li class="inline-hr" aria-hidden="true"></li>
            <li><a href="/news">News</a></li>
            <li class="inline-hr" aria-hidden="true"></li>
            <li><button id="copyLink" aria-label="Copy email address" type="button" onclick="copyEmail()">Email</button></li>
            <li class="inline-hr big-screen" aria-hidden="true"></li>
          </ul>
        </footer>
        <script src="/assets/js/copy_email" defer="defer"></script>
        <script>function copyToClipboard(element){const text=element.textContent;navigator.clipboard.writeText(text).then(()=>{const originalText=element.textContent;const originalColor=element.style.color;const originalDecoration=element.style.textDecoration;element.textContent="Copied!";element.style.color="rgb(var(--primary))";element.style.textDecoration="none";setTimeout(()=>{element.textContent=originalText;element.style.color=originalColor;element.style.textDecoration=originalDecoration},2000)}).catch(err=>{console.error('Failed to copy:',err)})}</script>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>