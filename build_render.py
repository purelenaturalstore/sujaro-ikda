from pathlib import Path
import os,re,shutil,html
base=os.environ["RENDER_EXTERNAL_URL"].rstrip("/")
assert base.startswith("https://")
out=Path("dist");out.mkdir(exist_ok=True)
urls=[]
for f in Path(".").glob("*.html"):
 s=f.read_text(encoding="utf-8").replace('content="noindex,nofollow"','content="index,follow"')
 url=base+"/"+("" if f.name=="index.html" else f.name)
 s=s.replace("</head>",'<link rel="canonical" href="'+html.escape(url)+'"/></head>')
 (out/f.name).write_text(s,encoding="utf-8");urls.append(url)
shutil.copy2("style.css",out/"style.css")
(out/"robots.txt").write_text(Path("robots.txt").read_text(encoding="utf-8")+"Sitemap: "+base+"/sitemap.xml\n",encoding="utf-8")
(out/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+html.escape(u)+'</loc></url>' for u in urls)+'</urlset>',encoding="utf-8")
print("Built",len(urls),"pages for",base)
