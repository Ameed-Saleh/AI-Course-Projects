'use strict';
const text = {
  he: {
    pageTitle:'MaskVision AI · זיהוי מסכות',skip:'לסטודיו הזיהוי',back:'חזרה לדף הראשי',eyebrow:'הפרטים שעושים את ההבדל',title:'מבט מקרוב.',accent:'זיהוי חכם.',description:'תמונה אחת, שתי אפשרויות: עם מסכה או בלי מסכה. העלו תמונת פנים ברורה ותנו למודל לנתח אותה.',start:'לסטודיו הזיהוי',studio:'סטודיו זיהוי המסכות',processingNote:'הכנת הזיהוי אינה זמינה כרגע. נסו שוב לאחר טעינת המודל.',upload:'מוסיפים תמונה',uploadPrompt:'מתחילים בתמונת פנים.',drop:'גררו לכאן תמונה או בחרו קובץ למטה',formats:'JPEG, PNG, WebP · עד 15 מגה־בייט',choose:'בחירת תמונה',camera:'צילום במצלמה',cameraNote:'צילום ישיר זמין בטלפונים תומכים. התמונה נשלחת לשרת רק בלחיצה על זיהוי.',remove:'הסרה',classify:'בצע זיהוי',save:'שמור תמונה',results:'התוצאה שלכם',confidence:'רמת ביטחון',probabilities:'ההסתברויות לכל מחלקה',honesty:'רמת ביטחון נמוכה מ־60% מוצגת כ״לא ידוע״. זהו פרויקט לימודי; רמת הביטחון אינה מבטיחה שהזיהוי נכון.',categories:'מה המודל מזהה?',with_mask:'עם מסכה',without_mask:'בלי מסכה',Unknown:'לא ידוע',singleFace:'מומלץ להשתמש בתמונה של אדם אחד. המערכת מסווגת את התמונה כולה ואינה מסמנת פנים נפרדות.',footer:'פרויקט לימודי בראייה ממוחשבת',alt:'איור פנים עם מסכה',preview:'תצוגה מקדימה של התמונה שנבחרה',language:'בחירת שפה',nav:'ניווט ראשי',checking:'בודקים את המודל…',available:'המודל נטען',modelUnavailable:'המודל אינו זמין כרגע.',awaiting:'ממתינים לתמונה',defaultHeading:'מה התמונה שלכם מספרת?',defaultDescription:'בחרו תמונה ולחצו על זיהוי כדי לקבל תוצאה.',loading:'מכינים את התמונה…',ready:'התמונה מוכנה לזיהוי.',invalidImage:'בחרו קובץ תמונה תקין.',tooLarge:'התמונה גדולה מדי. המגבלה היא 15 מגה־בייט.',decodeError:'לא ניתן להציג את התמונה. נסו JPEG, PNG או WebP.',saved:'הורדת התמונה התבקשה.',predicting:'מנתחים את התמונה…',inferenceError:'הזיהוי נכשל. נסו שוב.',networkError:'לא ניתן להתחבר לשרת. נסו שוב.',matched:'רמת ביטחון גבוהה',uncertain:'רמת ביטחון נמוכה',uncertainDescription:'רמת הביטחון נמוכה מ־60%, לכן התוצאה היא לא ידוע.',matchedDescription:'זהו הסיווג שקיבל את ההסתברות הגבוהה ביותר מהמודל.',errorHeading:'הניתוח אינו זמין',workingHeading:'מבט מקרוב…',workingDescription:'המודל משווה בין שתי מחלקות: עם מסכה ובלי מסכה.'
  },
  en: {
    pageTitle:'MaskVision AI · Mask recognition',skip:'Skip to the studio',back:'Back to Home',eyebrow:'A CLOSER LOOK AT THE DETAILS',title:'Look closer.',accent:'See smarter.',description:'One photo, two possibilities: with a mask or without a mask. Upload a clear face photo for the model to analyze.',start:'Explore the studio',studio:'The mask recognition studio',processingNote:'Image preparation is currently unavailable. Try again after the model has loaded.',upload:'Add your photo',uploadPrompt:'Start with a face photo.',drop:'Drop an image here or choose a file below',formats:'JPEG, PNG, WebP · up to 15 MB',choose:'Choose image',camera:'Use camera',cameraNote:'Direct camera capture is available on supported phones. Your image is sent to the server only when you classify it.',remove:'Remove',classify:'Classify image',save:'Save image',results:'Your results',confidence:'Confidence',probabilities:'Class probabilities',honesty:'Confidence below 60% is displayed as Unknown. This is an educational project; confidence does not guarantee a correct classification.',categories:'What does the model recognize?',with_mask:'With mask',without_mask:'Without mask',Unknown:'Unknown',singleFace:'Use a photo of one person for best results. The system classifies the whole image and does not locate individual faces.',footer:'An educational computer vision project',alt:'Illustration of a masked face',preview:'Preview of your selected image',language:'Choose language',nav:'Main navigation',checking:'Checking model…',available:'Model loaded',preprocessingPending:'Classification setup is pending.',modelUnavailable:'The model is currently unavailable.',awaiting:'Awaiting a photo',defaultHeading:'What does your photo say?',defaultDescription:'Choose an image and classify it to see the result.',loading:'Preparing your image…',ready:'Photo ready to classify.',invalidImage:'Please choose a valid image file.',tooLarge:'This image is too large. The limit is 15 MB.',decodeError:'Could not preview this image. Try JPEG, PNG or WebP.',saved:'Image download requested.',predicting:'Analyzing your image…',inferenceError:'Classification failed. Please try again.',networkError:'Could not reach the server. Please try again.',matched:'High confidence',uncertain:'Low confidence',uncertainDescription:'Confidence is below 60%, so the result is Unknown.',matchedDescription:'This class received the highest probability from the model.',errorHeading:'Analysis unavailable',workingHeading:'Looking closer…',workingDescription:'The model is comparing two classes: with mask and without mask.'
  }
};
Object.assign(text.he, {
  artCaption: 'דיוקן להמחשה · אינו תוצאת זיהוי', artSignature: 'מבט על הפרטים.',
  switchLight: 'מעבר למצב בהיר', switchDark: 'מעבר למצב כהה',
  preprocessingPending: 'הזיהוי ממתין להשלמת החיבור.',
  noFace: 'לא זוהו פנים בתמונה.',
  noFaceHint: 'נסו תמונה ברורה ומוארת של אדם אחד, כשהפנים פונות למצלמה.',
  multipleFaces: 'זוהו כמה פנים בתמונה.',
  multipleFacesHint: 'בחרו תמונה של אדם אחד כדי לקבל סיווג מסכה יחיד.',
  faceDetectorUnavailable: 'בדיקת הפנים אינה זמינה כרגע. נסו שוב מאוחר יותר.',
  photoCheck: 'בדיקת התמונה',
  invalidResponse: 'תשובת הזיהוי אינה תואמת לגרסת הדף. סגרו את הטאב ופתחו את הקישור מחדש.',
  workingDescription: 'בודקים שמופיעות פנים של אדם אחד, ואז מנתחים את מצב המסכה.',
  singleFace: 'המערכת בודקת שיש פנים של אדם אחד לפני הסיווג. תמונה ללא פנים או עם כמה פנים לא תסווג.'
});
Object.assign(text.en, {
  artCaption: 'ILLUSTRATED PORTRAIT · NOT A PREDICTION', artSignature: 'A closer look.',
  switchLight: 'Switch to light mode', switchDark: 'Switch to dark mode',
  noFace: 'No face detected in this image.',
  noFaceHint: 'Try a clear, well-lit photo of one person facing the camera.',
  multipleFaces: 'Multiple faces detected.',
  multipleFacesHint: 'Choose a photo of one person to get a single mask classification.',
  faceDetectorUnavailable: 'Face detection is currently unavailable. Please try again later.',
  photoCheck: 'Photo check',
  invalidResponse: 'The prediction does not match this page version. Close this tab and reopen the link.',
  workingDescription: 'Checking for one face, then analyzing the mask class.',
  singleFace: 'The system checks for one face before classification. Photos with no detected face or multiple detected faces are not classified.'
});
Object.assign(text.en, {"examplesTitle": "Try an example", "examplesHint": "One click loads a sample and runs a real prediction.", "exampleRamen": "Ramen bowl", "exampleMask": "Mask worn correctly", "exampleNoFace": "No-face check", "exampleError": "Could not load the sample. Try again."});
Object.assign(text.he, {"examplesTitle":"נסו דוגמה","examplesHint":"לחיצה טוענת תמונה לדוגמה ומפעילה זיהוי אמיתי.","exampleBread":"לחם","exampleRamen":"קערת ראמן","exampleMask": "עם מסכה","exampleNoFace":"בדיקה ללא פנים","exampleError":"טעינת הדוגמה נכשלה. נסו שוב."});

Object.assign(text.he, {exampleMultipleFaces: 'כמה פנים בתמונה'});
Object.assign(text.en, {exampleMultipleFaces: 'Multiple faces'});

const $ = id => document.getElementById(id);
let theme = document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
function renderTheme() {
  document.documentElement.dataset.theme = theme;
  const label = t(theme === 'dark' ? 'switchLight' : 'switchDark');
  $('theme-toggle').setAttribute('aria-label', label);
  $('theme-toggle').setAttribute('aria-pressed', String(theme === 'dark'));
  $('theme-toggle').title = label;
  $('theme-label').textContent = label;
  if (theme === 'dark') { $('theme-moon').setAttribute('hidden', ''); $('theme-sun').removeAttribute('hidden'); }
  else { $('theme-sun').setAttribute('hidden', ''); $('theme-moon').removeAttribute('hidden'); }
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#1a1719' : '#f7f4ee';
}
$('theme-toggle').addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem('maskvision-theme', theme); } catch { /* Optional preference. */ }
  renderTheme();
});
let detectorReady=false;
let language = new URLSearchParams(location.search).get('lang');
if (!['he','en'].includes(language)) { try { language = localStorage.getItem('vision-language'); } catch {} }
if (!['he','en'].includes(language)) language = 'he';
const t = key => text[language][key];
let selectedFile=null, imageUrl=null, version=0, controller=null, result=null, state='empty', message='', modelReady=null, preprocessingReady=false;
const classes=['with_mask','without_mask'];
function feedback(key) { message=key; $('upload-message').textContent=key?t(key):''; $('upload-message').dataset.state=['invalidImage','tooLarge','decodeError','inferenceError','networkError','modelUnavailable','preprocessingPending','noFace','multipleFaces','faceDetectorUnavailable','exampleError'].includes(key)?'error':''; }
function percentage(value) { return new Intl.NumberFormat(language==='he'?'he-IL':'en-US',{maximumFractionDigits:1}).format(value)+'%'; }
function renderResult() {
  const ok=state==='success'&&result, low=ok&&result.prediction==='Unknown', busy=state==='loading', error=state==='error', rejected=state==='rejected';
  $('results').dataset.state = busy ? 'loading' : rejected ? 'rejected' : error ? 'error' : ok ? (low ? 'uncertain' : 'matched') : 'empty';
  $('results').setAttribute('aria-busy',String(busy));
  $('result-state').textContent=t(rejected?'photoCheck':busy?'predicting':ok?(low?'uncertain':'matched'):error?'errorHeading':'awaiting');
  $('result-heading').textContent=rejected?t(message):ok?t(result.prediction):t(busy?'workingHeading':error?'errorHeading':'defaultHeading');
  $('result-description').textContent=rejected?t(message+'Hint'):ok?t(low?'uncertainDescription':'matchedDescription'):t(busy?'workingDescription':error?(message||'inferenceError'):'defaultDescription');
  $('scores').hidden=!ok;
  $('confidence-meter').setAttribute('aria-label',t('confidence'));
  if (ok) {
    $('confidence-value').textContent=percentage(result.confidence);
    $('confidence-meter').setAttribute('aria-valuenow',result.confidence);
    $('confidence-fill').style.width=result.confidence+'%';
  } else { $('confidence-meter').removeAttribute('aria-valuenow'); $('confidence-fill').style.width='0%'; $('confidence-value').textContent=''; }
  $('probabilities').replaceChildren();
  if (ok) [...result.probabilities].sort((a,b)=>b.probability-a.probability).forEach(item=>{
    const row=document.createElement('li'), head=document.createElement('div'), name=document.createElement('span'), value=document.createElement('bdi'), track=document.createElement('div'), bar=document.createElement('span');
    name.textContent=t(item.category);value.textContent=percentage(item.probability*100);head.append(name,value);track.className='score-track';track.setAttribute('aria-hidden','true');bar.style.width=(item.probability*100)+'%';track.append(bar);row.append(head,track);$('probabilities').append(row);
  });
  $('model-status').textContent=t(modelReady===null?'checking':!modelReady?'modelUnavailable':!preprocessingReady?'preprocessingPending':!detectorReady?'faceDetectorUnavailable':'available');
  $('model-status').dataset.state=modelReady===false?'error':'';
}
function renderLanguage() {
  document.documentElement.lang=language;document.documentElement.dir=language==='he'?'rtl':'ltr';document.title=t('pageTitle');
  document.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=t(el.dataset.i18n)});
  document.querySelectorAll('[data-language]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.language===language)));
  const home=new URL(window.VISION_CONFIG?.homeUrl||'/home',location.origin);home.searchParams.set('lang',language);
  document.querySelectorAll('[data-return]').forEach(el=>{el.href=home.href});
  document.querySelector('.language-switch').setAttribute('aria-label',t('language'));document.querySelector('nav').setAttribute('aria-label',t('nav'));
  $('mask-art').alt=t('alt');$('preview').alt=t('preview');$('file-input').setAttribute('aria-label',t('choose'));$('camera-input').setAttribute('aria-label',t('camera'));
  try {localStorage.setItem('vision-language',language)} catch {}
  feedback(message);renderResult();renderTheme();
}
document.querySelectorAll('[data-language]').forEach(button=>button.addEventListener('click',()=>{language=button.dataset.language;const url=new URL(location.href);url.searchParams.set('lang',language);history.replaceState(null,'',url);renderLanguage()}));
function clearImage() {
  version++;controller?.abort();controller=null;selectedFile=null;result=null;state='empty';
  $('preview').onload=null;$('preview').onerror=null;
  if(imageUrl)URL.revokeObjectURL(imageUrl);imageUrl=null;
  $('preview').removeAttribute('src');$('preview').hidden=true;$('empty-preview').hidden=false;$('file-details').hidden=true;$('file-name').textContent='';
  $('classify').disabled=true;$('classify').setAttribute('aria-busy','false');$('save').disabled=true;$('file-input').value='';$('camera-input').value='';$('drop-zone').setAttribute('aria-busy','false');feedback('');renderResult();
}
function selectImage(file, autoClassify = false) {
  if(!file)return;
  if(!file.type.startsWith('image/')){feedback('invalidImage');return}
  if(file.size>15*1024*1024){feedback('tooLarge');return}
  clearImage();const current=version;selectedFile=file;imageUrl=URL.createObjectURL(file);feedback('loading');$('drop-zone').setAttribute('aria-busy','true');
  $('preview').onload=()=>{if(current!==version)return;$('preview').hidden=false;$('empty-preview').hidden=true;$('file-details').hidden=false;$('file-name').textContent=file.name;$('classify').disabled=!(modelReady&&preprocessingReady&&detectorReady);$('save').disabled=false;$('drop-zone').setAttribute('aria-busy','false');feedback('ready');if(autoClassify)$('classify').click()};
  $('preview').onerror=()=>{if(current!==version)return;clearImage();feedback('decodeError')};$('preview').src=imageUrl;
}
$('choose').addEventListener('click',()=>$('file-input').click());$('camera').addEventListener('click',()=>$('camera-input').click());
$('file-input').addEventListener('change',()=>selectImage($('file-input').files[0]));$('camera-input').addEventListener('change',()=>selectImage($('camera-input').files[0]));$('remove').addEventListener('click',clearImage);
['dragenter','dragover'].forEach(name=>$('drop-zone').addEventListener(name,event=>{event.preventDefault();$('drop-zone').classList.add('drag-over')}));
['dragleave','drop'].forEach(name=>$('drop-zone').addEventListener(name,event=>{event.preventDefault();$('drop-zone').classList.remove('drag-over')}));$('drop-zone').addEventListener('drop',event=>selectImage(event.dataTransfer.files[0]));
function validResult(data) {
  if(!data||!classes.includes(data.raw_prediction)||!Number.isFinite(data.confidence)||data.confidence<0||data.confidence>100||!Array.isArray(data.probabilities)||data.probabilities.length!==classes.length)return false;
  const seen=new Set();let sum=0,best=0,raw;
  for(const item of data.probabilities){if(!item||!classes.includes(item.category)||seen.has(item.category)||!Number.isFinite(item.probability)||item.probability<0||item.probability>1)return false;seen.add(item.category);sum+=item.probability;best=Math.max(best,item.probability);if(item.category===data.raw_prediction)raw=item.probability}
  return Math.abs(sum-1)<.001&&Math.abs(raw*100-data.confidence)<.001&&Math.abs(raw-best)<.00001&&data.prediction===(data.confidence>=60?data.raw_prediction:'Unknown');
}
$('classify').addEventListener('click',async()=>{
  if(!selectedFile||$('classify').disabled)return;
  const current=version,request=new AbortController();controller=request;const timeout=setTimeout(()=>request.abort(),60000),form=new FormData();form.append('file',selectedFile);
  $('classify').disabled=true;$('classify').setAttribute('aria-busy','true');result=null;state='loading';feedback('predicting');renderResult();
  try {
    const response=await fetch('/mask/predict',{method:'POST',body:form,signal:request.signal}),data=await response.json();if(current!==version)return;
    if(!response.ok){state=['noFace','multipleFaces'].includes(data.detail)?'rejected':'error';if(data.detail==='modelUnavailable')modelReady=false;if(data.detail==='preprocessingPending')preprocessingReady=false;if(data.detail==='faceDetectorUnavailable')detectorReady=false;feedback(['noFace','multipleFaces','faceDetectorUnavailable','modelUnavailable','preprocessingPending','invalidImage','tooLarge','inferenceError'].includes(data.detail)?data.detail:'inferenceError')}
    else if(!validResult(data)){state='error';feedback('invalidResponse')}
    else{result=data;state='success';modelReady=true;feedback('')}
  } catch {if(current===version){state='error';feedback('networkError')}}
  finally{clearTimeout(timeout);if(current===version){controller=null;$('classify').disabled=!(modelReady&&preprocessingReady&&detectorReady);$('classify').setAttribute('aria-busy','false');renderResult()}}
});
$('save').addEventListener('click',()=>{if(!selectedFile||!imageUrl)return;const a=document.createElement('a');a.href=imageUrl;a.download=selectedFile.name||'maskvision-image';document.body.append(a);a.click();a.remove();feedback('saved')});
window.addEventListener('pagehide',()=>{controller?.abort();if(imageUrl)URL.revokeObjectURL(imageUrl)});
renderLanguage();
fetch('/mask/health').then(response=>{if(!response.ok)throw new Error();return response.json()}).then(data=>{modelReady=data.model_ready===true;preprocessingReady=data.preprocessing_ready===true;detectorReady=data.face_detector_ready===true;$('classify').disabled=!(selectedFile&&!$('preview').hidden&&modelReady&&preprocessingReady&&detectorReady);document.querySelector('.processing-note').hidden=preprocessingReady;renderResult()}).catch(()=>{modelReady=false;renderResult()});

// Ignore a downloaded example if the user has selected or removed another photo.
document.querySelectorAll('[data-example]').forEach(button => {
  button.addEventListener('click', async () => {
    const current = version;
    const buttons = [...document.querySelectorAll('[data-example]')];
    buttons.forEach(item => item.disabled = true);
    button.setAttribute('aria-busy', 'true');
    const request = new AbortController();
    const timeout = setTimeout(() => request.abort(), 15000);
    try {
      const response = await fetch(button.dataset.example, {signal: request.signal});
      if (!response.ok) throw new Error('Example unavailable');
      const blob = await response.blob();
      if (current !== version) return;
      selectImage(new File([blob], button.dataset.example.split('/').pop(), {type: blob.type}), true);
    } catch {
      if (current === version) feedback('exampleError');
    } finally {
      clearTimeout(timeout);
      buttons.forEach(item => item.disabled = false);
      button.removeAttribute('aria-busy');
    }
  });
});
