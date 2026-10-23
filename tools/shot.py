import sys,asyncio
from playwright.async_api import async_playwright
async def main(url,out,w=1150,full=True,sel=None):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1243/chrome-linux/chrome' if False else None)
        pg=await b.new_page(viewport={'width':w,'height':900},device_scale_factor=1)
        await pg.goto(url); await pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')"); await pg.wait_for_timeout(2500); await pg.evaluate('document.fonts.ready')
        if sel:
            els=await pg.query_selector_all(sel)
            for i,e in enumerate(els): await e.screenshot(path=out.replace('.png',f'_{i+1:02d}.png'))
        else: await pg.screenshot(path=out,full_page=full)
        await b.close()
a=sys.argv; asyncio.run(main(a[1],a[2],sel=a[3] if len(a)>3 else None))
