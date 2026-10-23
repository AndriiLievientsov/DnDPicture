import fs from 'fs'; import path from 'path';
import { createRequire } from 'module'; const less=createRequire(import.meta.url)('less');
const B='/home/claude/hbr/build';
process.chdir('/home/claude/hb');
for (const dir of ['Blank','5ePHB']){
  const out=await less.render(fs.readFileSync(`./themes/V3/${dir}/style.less`,'utf-8'),{});
  fs.mkdirSync(`${B}/themes/V3/${dir}`,{recursive:true}); fs.writeFileSync(`${B}/themes/V3/${dir}/style.css`,out.css);
}
fs.cpSync('./themes/fonts',`${B}/fonts`,{recursive:true});
fs.cpSync('./themes/assets',`${B}/assets`,{recursive:true});
for (const f of fs.readdirSync('./shared/naturalcrit/styles')) fs.cpSync(`./shared/naturalcrit/styles/${f}`,`${B}/fonts/${f}`,{recursive:true});
console.log('ok');
