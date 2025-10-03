<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="3.0" 
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  
  <xsl:template match="/">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1, interactive-widget=resizes-content"/>
        <meta name="color-scheme" content="light dark"/>
        <title>RSS Updates - Max Sheridan</title>
        <link rel="icon" href="/favicon.ico?v=2" type="image/x-icon" sizes="48x48"/>
        <link rel="icon" href="/favicon.svg?v=2" type="image/svg+xml" sizes="any"/>
        <link rel="stylesheet" href="/style.min.css"/>
        <style>p.pub-date{color:rgb(var(--accent))}hr.rss{margin-block-start:1.75rem;margin-block-end:1.75rem}</style>
      </head>
      <body>
        <a href="#main-content" class="skip-link">Skip to content</a>
        <div class="acme-all-purpose-wrapper flex">
          <header class="linkstyling-off">
            <hr aria-hidden="true"/>
            <a href="/" class="site-title" aria-label="Max Sheridan home">
              Max Sheridan
            </a>
            <hr aria-hidden="true"/>
          </header>
          
          <main id="main-content" tabindex="-1">
            <div class="acme-content-wrapper">
              <h1>RSS Feed</h1>
              <p>
                  This is an old-school RSS feed. Copy the URL in your browser and paste it into your feed reader and you’re set. Or click on a link to read my latest updates.
              </p>
              <hr class="rss"/>
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
          
          <footer class="linkstyling-off" aria-label="footer links">
            <hr class="big-screen" aria-hidden="true"/>
            <a href="/short-fiction">Short Fiction</a>
            <hr aria-hidden="true"/>
            <a href="/news">News</a>
            <hr aria-hidden="true"/>
            <a id="copyLink" onclick="copyEmail()">Email</a>
            <hr class="big-screen" aria-hidden="true"/>
          </footer>
        </div>
        <script>function copyEmail(){const email="max@maxsheridan.com";const copyLink=document.getElementById('copyLink');navigator.clipboard.writeText(email).then(()=>{const originalText=copyLink.textContent;const originalColor=copyLink.style.color;copyLink.textContent="Copied!";copyLink.style.color="var(--accent-color)";setTimeout(()=>{copyLink.textContent=originalText;copyLink.style.color=originalColor},2000)}).catch(err=>{alert('Failed to copy email: '+err)})}</script>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>