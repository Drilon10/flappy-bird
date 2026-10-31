from pathlib import Path
from io import BytesIO
from html import escape
import subprocess, shutil, zipfile, json
from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, Preformatted)

BASE=Path(__file__).resolve().parents[2]
TMP=BASE/'tmp'/'pdfs'
OUT=BASE/'output'/'pdf'
DOWNLOADS=Path(r'C:\Users\DELL\Downloads')
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Mono','consola.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
NAVY=colors.HexColor('#17324D');TEAL=colors.HexColor('#007D80')
INK=colors.HexColor('#213549');LIGHT=colors.HexColor('#EAF4F5')
styles={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=23,leading=27,textColor=NAVY,spaceAfter=13),
 'h':ParagraphStyle('h',fontName='Bold',fontSize=12,leading=16,textColor=TEAL,spaceBefore=8,spaceAfter=7),
 'p':ParagraphStyle('p',fontName='Body',fontSize=10.2,leading=14.5,textColor=INK,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.6,leading=11.7,textColor=INK,spaceAfter=6),
 'code':ParagraphStyle('code',fontName='Mono',fontSize=9,leading=12.5,textColor=NAVY,spaceAfter=10),
 'cell':ParagraphStyle('cell',fontName='Body',fontSize=9.1,leading=12.7,textColor=INK),
 'head':ParagraphStyle('head',fontName='Bold',fontSize=9.1,leading=12.7,textColor=colors.white),
}
TITLES={26:'Projekti dhe komponenti Bird',27:'Komponenti Obstacles',
        28:'Kërcimi, përplasjet dhe pikët',29:'Përfundimi i lojës'}

class Notes:
 def __init__(self,n):self.n=n;self.story=[];self.page_count=0
 def page(self,title):
  if self.story:self.story.append(PageBreak())
  self.page_count+=1
  self.p(f'MËSIMI {self.n} / SHËNIME PËR INSTRUKTORIN','small')
  self.p(title,'title')
 def p(self,text,style='p'):self.story.append(Paragraph(text,styles[style]))
 def h(self,text):self.p(text,'h')
 def code(self,text):self.story.append(Preformatted(text,styles['code']))
 def table(self,heads,rows,widths=None):
  data=[[Paragraph(escape(h),styles['head']) for h in heads]]
  data.extend([[Paragraph(str(x),styles['cell']) for x in row] for row in rows])
  t=Table(data,colWidths=widths or [260,260],hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),NAVY),
   ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F0F5F8')]),
   ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
   ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
   ('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),0.4,colors.HexColor('#DAE4EB'))]))
  self.story.extend([t,Spacer(1,9)])
 def note(self,label,text):
  t=Table([[Paragraph(f'<b>{label}</b><br/>{text}',styles['p'])]],colWidths=[520])
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),LIGHT),('LEFTPADDING',(0,0),(-1,-1),11),
   ('RIGHTPADDING',(0,0),(-1,-1),11),('TOPPADDING',(0,0),(-1,-1),9),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
  self.story.extend([t,Spacer(1,10)])
 def sources(self,extra=None):
  self.h('Burimi dhe komandat e verifikuara')
  self.p(f'Materiali bazë: Lesson {self.n}, Digital School, PDF-ja e furnizuar. Pas këtyre 3 faqeve vijon materiali origjinal me numërtimin e vet. Kodi dhe rendi i hapave ruhen; në modulin 26 janë përditësuar vetëm komandat e krijimit dhe nisjes.','small')
  links=[('Template blank: JavaScript me strukturë minimale','https://docs.expo.dev/more/create-expo/'),
         ('Nisja e projektit me Expo CLI','https://docs.expo.dev/more/expo-cli/')]
  if extra:links.append(extra)
  for label,url in links:self.p(f'<link href="{url}" color="#007D80">{escape(label)}</link><br/>{escape(url)}','small')
  self.p('Verifikuar më 31.10.2026. Provoje hapjen në pajisjen e klasës para orës; përputhshmëria e Expo Go varet nga SDK-ja e projektit.','small')
 def render(self):
  path=TMP/f'notes{self.n}.pdf'
  d=SimpleDocTemplate(str(path),pagesize=letter,leftMargin=46,rightMargin=46,topMargin=62,bottomMargin=42)
  def chrome(c,doc):
   c.setFillColor(NAVY);c.rect(0,756,612,36,fill=1,stroke=0)
   c.setFillColor(colors.white);c.setFont('Bold',9)
   c.drawString(46,770,'FLAPPY BIRD / JAVASCRIPT');c.drawRightString(566,770,f'MODULI {self.n}')
   c.setFillColor(INK);c.setFont('Body',8)
   c.drawString(46,24,'Shënime për instruktorin | 31.10.2026')
   c.drawRightString(566,24,f'{doc.page} / 3')
  d.build(self.story,onFirstPage=chrome,onLaterPages=chrome)
  assert len(PdfReader(path).pages)==3,(self.n,len(PdfReader(path).pages))
  return path

def opening(n,result,plan):
 g=Notes(n);g.page(TITLES[n])
 g.p('<b>75 minuta • App.js, Bird.js dhe Obstacles.js</b>')
 g.note('Rezultati i pritshëm',result)
 g.h('Rrjedha e orës')
 g.table(['Koha','Çfarë bën instruktori'],plan,[75,445])
 g.h('Si ta përdorësh këtë PDF')
 g.p('Tre faqet e para janë shënime në shqip për drejtimin e orës. Më pas përdor materialin origjinal dhe kodin e tij në JavaScript. Jep një hap, provo rezultatin dhe vetëm pastaj vazhdo me hapin tjetër.')
 g.p('Ruaj të njëjtët emra variablash dhe të njëjtat props si në fotografitë e kodit. Shënimet shpjegojnë shembullin ekzistues; nuk shtojnë funksione të reja në lojë.','small')
 return g

def notes26():
 g=opening(26,'Nxënësi krijon projektin bosh, ndërton Bird.js dhe e lidh me App.js. Në fund zogu katror bie poshtë, si në modulin origjinal.',[
  ('0-5','Rikujtim: komponenti, props dhe useState.'),('5-15','Shpjego lojën dhe krijo/hap projektin.'),
  ('15-30','Ndërto Bird.js si View statik dhe shfaqe në App.js.'),('30-45','Shpjego screenWidth, screenHeight, birdLeft dhe birdBottom.'),
  ('45-60','Shto useEffect dhe setInterval për rënien.'),('60-70','Lidh props dhe zgjidh gabimet me nxënësit.'),
  ('70-75','Pyetje kontrolli dhe ruajtja e punës.')])
 g.page('Komandat: ndryshimet e vetme teknike')
 g.table(['Në materialin e vjetër','Përdor tani'],[
  ('expo init flappy-bird-rn --template blank','npx create-expo-app@latest flappy-bird-rn --template blank'),
  ('npm run, për ta nisur projektin','npm start ose npx expo start')],[235,285])
 g.h('Rendi i komandave')
 g.code('npx create-expo-app@latest flappy-bird-rn --template blank\ncd flappy-bird-rn\nnpm start')
 g.p('blank është template minimal në JavaScript. Mos zgjidh default ose blank-typescript për këtë seri. Për një projekt që ekziston, mos e krijo përsëri: hyr në dosjen e tij dhe ekzekuto vetëm npm start.')
 g.h('Struktura mbetet ajo e mësimit')
 g.code('flappy-bird-rn/\n  App.js\n  assets/\n  src/\n    components/\n      Bird.js\n      Obstacles.js  // krijohet ne modulin 27')
 g.note('Përgatitja para orës','Provoje nisjen dhe telefonin përpara klasës. Instalimet dhe rrjeti nuk duhet të të marrin pjesën e demonstrimit. Nëse Expo Go nuk e hap projektin, kontrollo SDK-në e mbështetur; ky është problem mjedisi, jo arsye për të ndryshuar kodin e mësimit.')
 g.h('Shpjegimi që mund t’u thuash nxënësve')
 g.p('"App.js mban vlerën e pozicionit. Bird.js e merr atë përmes props dhe vizaton katrorin. Kur ndryshon state, ndryshon edhe vendi ku shfaqet zogu."')
 g.page('Rënia: çfarë duhet të kuptojnë')
 g.table(['Pjesa e kodit','Shpjegimi i thjeshtë'],[
  ('birdLeft','Pozicioni horizontal i zogut; vendoset në mes të ekranit.'),
  ('birdBottom','Pozicioni vertikal i përdorur nga mësimi. Kur zvogëlohet, zogu zbret.'),
  ('gravity = 3','Në këtë shembull zbriten 3 njësi në çdo hap; është vlerë e thjeshtë mësimore.'),
  ('setInterval(..., 30)','Përsërit përditësimin afërsisht çdo 30 milisekonda.'),
  ('clearInterval(gameTimerId)','Pastron intervalin që të mos mbetet aktiv pas cleanup-it.'),
  ('Props te Bird','birdBottom dhe birdLeft duhet të kalojnë nga App.js te Bird.js.')],[185,335])
 g.h('Kontroll pas çdo hapi')
 g.p('<b>1.</b> Para intervalit: katrori shfaqet dhe nuk lëviz.<br/><b>2.</b> Pas intervalit: state ndryshon.<br/><b>3.</b> Pas lidhjes së props: katrori bie. Nëse state ndryshon por zogu jo, kontrollo props dhe emrat e tyre.')
 g.h('Pyetje për vlerësim')
 g.p('<b>Pse përdorim state?</b> Sepse ndryshimi duhet të shfaqet në ekran.<br/><b>A duhet ta shkruajmë intervalin te Bird.js?</b> Në këtë mësim ai mbetet në App.js.<br/><b>Çfarë ndryshon kur gravity bëhet 1?</b> Zogu zbret më ngadalë.')
 g.sources(('setInterval dhe clearInterval','https://reactnative.dev/docs/timers'))
 return g

def notes27():
 g=opening(27,'Nxënësi krijon Obstacles.js dhe shfaq dy çifte pengesash. Secili çift lëviz majtas sipas intervalit të vet, si në materialin origjinal.',[
  ('0-5','Rikujtim i Bird.js dhe props.'),('5-15','Vizato dy pengesat dhe hapësirën mes tyre.'),
  ('15-30','Krijo Obstacles.js dhe shpjego props.'),('30-45','Shto gjendjen dhe intervalin për çiftin e parë.'),
  ('45-60','Përsërit hapat për çiftin e dytë.'),('60-70','Provo lëvizjen dhe rikthimin në anën e djathtë.'),
  ('70-75','Pyetje kontrolli dhe ruajtja e punës.')])
 g.page('Obstacles.js: shpjego një çift fillimisht')
 g.p('Vazhdo mbi projektin e modulit 26. Krijo src/components/Obstacles.js, pastaj importoje në App.js. Përdor emrin <b>Obstacles</b> njësoj në emrin e skedarit, import dhe JSX.')
 g.table(['Prop','Roli në shembullin origjinal'],[
  ('color','Ngjyra e dy View-ve që formojnë çiftin.'),('obstacleWidth','Gjerësia e pengesës.'),
  ('obstacleHeight','Lartësia e pengesës së poshtme.'),('randomBottom','Zhvendosja vertikale e çiftit.'),
  ('gap','Hapësira e lirë mes dy pengesave.'),('obstaclesLeft','Pozicioni horizontal i përbashkët.')],[160,360])
 g.h('Si ta vizatosh në tabelë')
 g.p('Vizato pengesën e poshtme, pastaj hapësirën gap. Pengesa e sipërme fillon mbi atë hapësirë. Formula që shfaqet te kodi është:')
 g.code('bottom: randomBottom + obstacleHeight + gap')
 g.p('Të dyja View-t marrin të njëjtin obstaclesLeft. Prandaj lëvizin së bashku si një çift. Trego një çift statik përpara se të shtosh intervalin.')
 g.note('Për të mos i ngatërruar','Së pari ndërto dhe provo çiftin e parë. Vetëm pasi funksionon, shto variantet Two për çiftin e dytë. Mbaj emrat e materialit; mos prezanto një strukturë tjetër për listën e pengesave.')
 g.page('Lëvizja dhe kontrolli në klasë')
 g.h('Lexoje intervalin me fjali të thjeshta')
 g.p('"Për sa kohë pengesa nuk ka dalë në të majtë, çdo 30 ms ia zvogëlojmë pozicionin me 5. Kur del, e kthejmë në anën e djathtë." Pastaj trego të njëjtin hap për obstaclesLeftTwo.')
 g.h('Çfarë të kontrollosh')
 g.table(['Simptoma','Kontrollo'],[
  ('Nuk shfaqet pengesa','Importin, export default dhe thirrjen e komponentit.'),
  ('Të dy çiftet janë njëri mbi tjetrin','Pozicionin fillestar të obstaclesLeft dhe obstaclesLeftTwo.'),
  ('Lëviz vetëm çifti i parë','Intervalin e dytë dhe props-in obstaclesLeft të çiftit të dytë.'),
  ('Pengesa nuk rikthehet','Kushtin që kontrollon daljen nga ekrani dhe degën else.'),
  ('Hapësira duket e gabuar','Vlerat e gap, obstacleHeight dhe randomBottom.')],[205,315])
 g.h('Pyetje me përgjigje orientuese')
 g.p('<b>Pse dy View?</b> Një pengesë sipër dhe një poshtë.<br/><b>Pse një pozicion horizontal për të dyja?</b> Që të formojnë një çift.<br/><b>Çfarë e lëviz pengesën majtas?</b> Zbritja e 5 nga pozicioni horizontal.')
 g.note('Komandat','Ky modul nuk ka komandë të re për t’u zëvendësuar. Hape projektin ekzistues me npm start. Ruaj kodin dhe vazhdo me të njëjtën mënyrë pune si në modulin 26.')
 g.sources(('Intervalet mbeten të mbështetura','https://reactnative.dev/docs/timers'))
 return g

def notes28():
 g=opening(28,'Nxënësi shton kontrollin e përplasjes, funksionin jump dhe rezultatin score. Prekja rrit birdBottom me 50, si te kodi i mësimit.',[
  ('0-5','Rikujtim: birdBottom, obstaclesLeft dhe gap.'),('5-20','Shpjego kushtin e përplasjes për një çift.'),
  ('20-35','Shto gameOver dhe kontrollin për çiftin e dytë.'),('35-50','Mbështill View me TouchableWithoutFeedback dhe lidh jump.'),
  ('50-62','Shto score në degët e rikthimit të pengesave.'),('62-70','Provo prekjen, përplasjen dhe numërimin.'),
  ('70-75','Pyetje kontrolli dhe ruajtja e punës.')])
 g.page('Përplasja dhe kërcimi në stilin origjinal')
 g.h('1. Shpjego kushtin për një çift')
 g.p('Ndaje kushtin e gjatë në dy pyetje: <b>A është pengesa afër zogut horizontalisht?</b> dhe <b>A është zogu jashtë hapësirës së lirë vertikalisht?</b> Vetëm kur plotësohen të dyja, kërkohet ndalimi i lojës. Pastaj përsërite për çiftin Two.')
 g.h('2. Lexo funksionin gameOver')
 g.p('Në burim ai ndalon intervalin e zogut dhe dy intervalet e pengesave me clearInterval. Kërko nga nxënësi të tregojë cilit interval i përket secili emër. Mos e paraqit si buton rinisjeje: moduli origjinal nuk ndërton një të tillë.')
 g.h('3. Mbaj TouchableWithoutFeedback')
 g.p('Ai mbështjell një View që përmban zogun, pengesat dhe tekstin. onPress={jump} thërret funksionin kur preket ekrani. Kjo API ende ekziston; nuk kërkohet ndryshim vetëm për të ndjekur këtë mësim.')
 g.h('4. Jump mbetet ndryshim i pozicionit')
 g.code('setBirdBottom(birdBottom => birdBottom + 50)')
 g.p('Meqë përdoret bottom, shtimi i vlerës e ngre zogun. Intervali i rënies vazhdon ta ulë atë. Këtu mësohet një kërcim i thjeshtë me zhvendosje, njësoj si në materialin origjinal.')
 g.note('Demonstrimi','Bëj një prekje dhe pyet çfarë ndryshoi. Pastaj mos prek për pak kohë: zogu duhet të vazhdojë rënien. Mbaj të njëjtat vlera dhe të njëjtët emra si te fotografitë e kodit.')
 g.page('Pikët dhe prova e nxënësve')
 g.h('Kur shtohet score sipas materialit')
 g.p('Në këtë version, +1 vendoset te dega else ku pengesa rikthehet në të djathtë. Pra rezultati ndryshon kur çifti del nga ekrani dhe riciklohet, jo saktësisht në çastin kur kalon pranë zogut. Shpjego atë që bën kodi i dhënë.')
 g.code('setScore(score => score + 1)')
 g.p('Shto rreshtin te të dy çiftet, sipas hapit të mësimit. Text shfaq vlerën e score. Mos vendos shtimin te intervali që ekzekutohet çdo 30 ms, sepse rezultati do të rritet vazhdimisht.')
 g.table(['Prova','Çfarë të vëzhgosh'],[
  ('Prek ekranin','jump thirret dhe birdBottom rritet.'),
  ('Kalo në hapësirën mes pengesave','Zogu nuk duhet të trajtohet si jashtë hapësirës.'),
  ('Përplasu me pengesën','Kontrollo thirrjen gameOver dhe ndalimin e intervaleve.'),
  ('Lër një çift të dalë jashtë ekranit','score rritet një herë te rikthimi.'),
  ('Lër edhe çiftin e dytë të dalë','Edhe dega e tij duhet të shtojë score.')],[225,295])
 g.h('Pyetje për vlerësim')
 g.p('<b>Çfarë thërret prekja?</b> jump.<br/><b>Çfarë ndalon gameOver?</b> Tre intervalet.<br/><b>Ku shtohet pikë në këtë material?</b> Te else i rikthimit të pengesës.')
 g.sources(('TouchableWithoutFeedback','https://reactnative.dev/docs/touchablewithoutfeedback'))
 return g

def notes29():
 g=opening(29,'Nxënësi zëvendëson View me Image për zogun dhe pengesat dhe shton figurën e sfondit. Logjika mbetet ajo e moduleve të mëparshme.',[
  ('0-5','Rikujtim i përplasjes dhe pikëve.'),('5-15','Kontrollo bird.png, pipe.png dhe background.png.'),
  ('15-30','Ndrysho vetëm pjesën vizuale te Bird.js.'),('30-45','Shto sfondin dhe kontrollo rendin e elementeve.'),
  ('45-60','Zëvendëso dy View-t e pengesave me Image.'),('60-70','Provo pamjen, prekjen dhe lojën e plotë.'),
  ('70-75','Vlerësimi dhe ruajtja e projektit.')])
 g.page('Figurat dhe rrugët: i njëjti projekt JS')
 g.p('Figurat duhet të jenë gati përpara orës. PDF-ja burimore i tregon në pamje, por nuk i jep si skedarë PNG të veçantë. Përdor figurat e kursit që i ke në dispozicion ose figura të tua me këta emra:')
 g.code('assets/\n  bird.png\n  pipe.png\n  background.png\nsrc/\n  components/\n    Bird.js\n    Obstacles.js\nApp.js')
 g.table(['Nga cili skedar?','Rruga që përdor materiali'],[
  ('src/components/Bird.js',"require('../../assets/bird.png')"),
  ('src/components/Obstacles.js',"require('../../assets/pipe.png')"),
  ('App.js',"require('./assets/background.png')")],[225,295])
 g.h('Rendi i demonstrimit')
 g.p('<b>1.</b> Te Bird.js importo Image dhe zëvendëso View, duke mbajtur props e pozicionit.<br/><b>2.</b> Te App.js shto figurën e sfondit sipas materialit.<br/><b>3.</b> Te Obstacles.js zëvendëso të dyja View-t me Image dhe ruaj vlerat e pozicionit.')
 g.note('Mos e lidh pamjen me një strukturë tjetër','App.js mbetet App.js dhe komponentët mbeten skedarë .js. Nuk nevojitet paketë e re për Image, sepse importohet nga react-native. Source dhe resizeMode shkruhen si në mësimin origjinal.')
 g.page('Kontrolli përfundimtar për instruktorin')
 g.table(['Problemi','Kontrollo së pari'],[
  ('Nuk gjendet figura','Emrin, prapashtesën .png dhe rrugën relative nga skedari që e thërret.'),
  ('Figura nuk shfaqet siç pritet','width, height dhe resizeMode të dhëna në shembull.'),
  ('Sfondi mbulon elementet e lojës','Rendin e elementeve dhe stilin backgroundImage.'),
  ('Zogu shihet, por nuk lëviz','Props birdBottom dhe birdLeft duhet të ruhen pas zëvendësimit.'),
  ('Pengesat kanë ndryshuar pozicion','Vlerat e stilit duhet të mbeten ato që ishin te View.')],[215,305])
 g.h('Lista e dorëzimit')
 g.p('• Zogu shfaqet si figurë dhe lëviz.<br/>• Dy çiftet e pengesave shfaqen dhe lëvizin.<br/>• Prekja thërret jump.<br/>• Përplasja dhe score provohen si në modulin 28.<br/>• Të tri figurat ruhen bashkë me projektin.<br/>• Nxënësi e nis projektin me npm start dhe shpjegon një prop të Bird ose Obstacles.')
 g.h('Vlerësimi')
 g.p('Vlerëso funksionimin dhe shpjegimin e nxënësit. Kërko të tregojë ndryshimin mes View dhe Image dhe të shpjegojë nga vjen pozicioni i zogut. Ndryshimet e pamjes nuk duhet të përdoren si arsye për të rishkruar logjikën e lojës.')
 g.note('Komandat','Në këtë modul nuk ka komandë të re për t’u përditësuar. Image, source dhe resizeMode janë pjesë e kodit; ndiqi në të njëjtin stil si materiali origjinal.')
 g.sources(('Image dhe resizeMode','https://reactnative.dev/docs/image'))
 return g

def changed_source26(source):
 """Flatten only the two pages with command edits; retain all code pages."""
 paths=[]
 for page in [1,2]:
  subprocess.run([shutil.which('pdftoppm'),'-f',str(page),'-l',str(page),'-r','180','-png',str(source),str(TMP/f'command26p{page}')],check=True,capture_output=True)
  image_path=next(TMP.glob(f'command26p{page}-*.png'))
  im=Image.open(image_path).convert('RGB');draw=ImageDraw.Draw(im)
  sx,sy=im.width/612,im.height/792
  if page==1:rect=(88,734,556,751)
  else:rect=(493,55.5,548,70)
  draw.rectangle((int(rect[0]*sx),int(rect[1]*sy),int(rect[2]*sx+1),int(rect[3]*sy+1)),fill='white')
  im.save(image_path)
  stream=BytesIO();c=canvas.Canvas(stream,pagesize=letter)
  c.drawImage(str(image_path),0,0,width=612,height=792)
  c.setFillColor(colors.black)
  if page==1:
   c.setFont('Mono',9);c.drawString(90,46,'npx create-expo-app@latest flappy-bird-rn --template blank')
  else:
   c.setFont('Body',10.3);c.drawString(494.6,725,'npm start.')
  c.save();stream.seek(0);paths.append(stream)
 return paths

def build():
 files=[];manifest=[]
 for n,make in [(26,notes26),(27,notes27),(28,notes28),(29,notes29)]:
  source=next(DOWNLOADS.glob(f'Lesson {n} *DS.pdf'))
  notes=make().render();writer=PdfWriter()
  writer.append(str(notes))
  original=PdfReader(source)
  if n==26:
   changed=changed_source26(source)
   for stream in changed:writer.add_page(PdfReader(stream).pages[0])
   for pg in original.pages[2:]:writer.add_page(pg)
  else:
   for pg in original.pages:writer.add_page(pg)
  writer.add_metadata({'/Title':f'Moduli {n} - {TITLES[n]} - JavaScript',
      '/Subject':'Kodi dhe stili origjinal JS; komanda te perditesuara; shenime per instruktorin',
      '/Author':'Udhëzues për instruktorin'})
  out=OUT/f'Moduli_{n}_Flappy_Bird_Udhezues_Instruktori.pdf'
  with out.open('wb') as f:writer.write(f)
  r=PdfReader(out)
  assert len(r.pages)==len(original.pages)+3
  text='\n'.join(p.extract_text() or '' for p in r.pages)
  for forbidden in ['.tsx','.ts\n','useGame','requestAnimationFrame','expo-router','TypeScript']:
   assert forbidden not in text,(n,forbidden)
  assert 'JavaScript' in text
  files.append(out)
  manifest.append({'module':n,'path':str(out),'pages':len(r.pages),'source_pages':len(original.pages)})
 zpath=OUT/'Flappy_Bird_Modulet_26-29_Per_Instruktorin.zip'
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in files:z.write(p,p.name)
 with zipfile.ZipFile(zpath) as z:
  assert len(z.namelist())==4 and z.testzip() is None
  for p in files:assert z.read(p.name)==p.read_bytes()
 (TMP/'manifest_js.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'files':manifest,'zip':str(zpath)},ensure_ascii=False,indent=2))

if __name__=='__main__':build()
