'use strict';
const copy = {
  he: {
    title: 'Vision AI · לראות מעבר לתמונה', skip: 'דלגו לבחירת פרויקט', nav: 'ניווט ראשי', language: 'בחירת שפה', projectsNav: 'הפרויקטים', aboutNav: 'הרעיון',
    eyebrow: 'ראייה ממוחשבת. סקרנות אנושית.', heroTitle: 'מבט אחד.', heroAccent: 'עולם של אפשרויות.', intro: 'מתמונה לתובנה, בעזרת בינה מלאכותית. שתי מערכות, שני עולמות — בחרו מה מסקרן אתכם לגלות.', choose: 'בחרו את נקודת המבט שלכם',
    projectsTitle: 'שתי דרכים לראות אחרת.', projectsIndex: '01 — בחרו חוויה', foodEyebrow: 'האוכל שלכם, מזווית חדשה', foodDescription: 'מה יש בצלחת? צלמו מנה או העלו תמונה, וגלו לאיזו מבין 11 קטגוריות המזון היא מתאימה.', foodCta: 'לזיהוי מזון', foodAlt: 'קערת ראמן עם אטריות וביצה',
    maskEyebrow: 'הפרטים שעושים את ההבדל', maskDescription: 'עם מסכה או בלי? העלו תמונת פנים ונסו מודל CNN שאומן לשתי מחלקות.', maskCta: 'לפרויקט המסכות', maskAlt: 'איור של פנים עם מסכה במסגרת סריקה', illustration: 'תמונה להמחשה',
    aboutEyebrow: 'מאחורי התמונה', aboutTitle: 'הסקרנות שלכם.', aboutAccent: 'הלמידה של המכונה.', aboutText: 'פרויקט לימודי המחבר בין אימון רשתות CNN לבין חוויה שאפשר לנסות בעצמכם. המטרה: להפוך מודל לזיהוי תמונות לכלי פשוט ונגיש.',
    stepOne: 'בוחרים עולם', stepOneText: 'מזון או מסכות — מתחילים בפרויקט שמעניין אתכם.', stepTwo: 'מוסיפים תמונה', stepTwoText: 'במערכת הזיהוי מצלמים בטלפון או בוחרים תמונה מהגלריה או מהמחשב.', stepThree: 'מגלים את התוצאה', stepThreeText: 'המודל מנתח את התמונה ומציג את הסיווג ורמת הביטחון שלו.',
    documentEyebrow: 'מהרעיון לפרויקט', documentTitle: 'רוצים להכיר את התמונה המלאה?', documentText: 'מסמך הפרויקט המקורי: המטרה, שלבי העבודה ודרישות המערכת.', download: 'להורדת מסמך הפרויקט', footer: 'נוצר מתוך סקרנות. נבנה כדי ללמוד.'
  },
  en: {
    title: 'Vision AI · Beyond the image', skip: 'Skip to projects', nav: 'Main navigation', language: 'Choose language', projectsNav: 'The projects', aboutNav: 'The idea',
    eyebrow: 'COMPUTER VISION. HUMAN CURIOSITY.', heroTitle: 'One image.', heroAccent: 'A world of possibilities.', intro: 'From images to insights, with artificial intelligence. Two projects, two perspectives. Choose what you’re curious to discover.', choose: 'Choose your perspective',
    projectsTitle: 'Two ways to see differently.', projectsIndex: '01 — CHOOSE AN EXPERIENCE', foodEyebrow: 'A FRESH PERSPECTIVE ON FOOD', foodDescription: 'What’s on your plate? Take a photo or upload an image to explore a model trained on 11 food categories.', foodCta: 'Explore food recognition', foodAlt: 'A bowl of ramen with noodles and an egg',
    maskEyebrow: 'A CLOSER LOOK AT THE DETAILS', maskDescription: 'With a mask or without one? Upload a face photo and try a CNN trained on two classes.', maskCta: 'Explore the mask project', maskAlt: 'Illustration of a masked face inside a scanning frame', illustration: 'Illustrative image',
    aboutEyebrow: 'BEHIND THE IMAGE', aboutTitle: 'Your curiosity.', aboutAccent: 'Machine learning.', aboutText: 'An educational project connecting CNN training with an experience you can try yourself. The goal: turn an image classification model into a simple, accessible tool.',
    stepOne: 'Choose your world', stepOneText: 'Food or masks — start with the project that interests you.', stepTwo: 'Bring a photo', stepTwoText: 'In the classification studio, use your phone camera or choose an image from your gallery or computer.', stepThree: 'Discover the result', stepThreeText: 'The model analyzes your photo and shows its classification and confidence.',
    documentEyebrow: 'FROM IDEA TO PROJECT', documentTitle: 'Curious about the bigger picture?', documentText: 'The original project brief: the goal, the process and the system requirements.', download: 'Download the project brief', footer: 'Made with curiosity. Built for learning.'
  }
};
copy.he.resultsNav = 'תוצאות המודלים';
copy.en.resultsNav = 'Model Results';
copy.he.maskDescription = 'עם מסכה או בלי? העלו תמונת פנים ונסו מודל CNN שאומן לשתי מחלקות.';
Object.assign(copy.he, {"demoNav": "מהטלפון", "demoEyebrow": "מהמודל אל הטלפון", "demoTitle": "כך זה נראה בפועל.", "demoIntro": "שלוש דוגמאות חיזוי מהטלפון ותיעוד השימוש באתר דרך ngrok. צילומי המסך מציגים את השימוש במערכת, כולל מגבלות שנצפו.", "demoNote": "הצילומים הם תיעוד הדגמה מ־29.10.2026, ואינם מדד לדיוק הכולל. כתובת ngrok תלויה בכך שהמחשב, השרת והמנהרה פועלים.", "demoOpen": "פתיחת צילומי ההדגמה בגודל מלא", "demoView": "לצפייה בצילומים ↗", "demoClose": "סגירת הצילום", "demoPrevious": "הקודם", "demoNext": "הבא", "demoOriginal": "פתיחת המקור ↗", "demoCellularBadge": "גישה מהטלפון · NGROK", "demoCellularTitle": "מהמחשב אל הטלפון", "demoCellularDescription": "דף הבית כפי שהוצג בטלפון, עם כתובת ngrok בשורת הכתובת. סוג החיבור בזמן צילום המסך אינו מעיד באיזה חיבור בוצע החיזוי.", "demoCellularAlt": "מהמחשב אל הטלפון", "demoWithoutBadge": "MASKVISION · ללא מסכה", "demoWithoutTitle": "בלי מסכה · 80.6%", "demoWithoutDescription": "תמונת קלט ותוצאת ״בלי מסכה״ בביטחון 80.6% מהטלפון. בצילומי המסך המעודכנים מופיע חיבור 5G ללא סמל Wi‑Fi.", "demoWithoutAlt": "בלי מסכה · 80.6%", "demoFacepaintBadge": "MASKVISION · מקרה כשל", "demoFacepaintTitle": "איפור פנים שמבלבל את המודל", "demoFacepaintDescription": "בדוגמה זו אין מסכה, אך המודל חזה ״עם מסכה״ בביטחון 98.2%. דוגמה למגבלה: ביטחון גבוה אינו מבטיח תשובה נכונה.", "demoFacepaintAlt": "איפור פנים שמבלבל את המודל", "demoFoodBadge": "FOODVISION · זיהוי מזון", "demoFoodTitle": "ביצה · 95.06%", "demoFoodDescription": "תמונה שהועלתה מהטלפון וסווגה כ״ביצה״. הממשק מציג גם את התחזיות החלופיות.", "demoFoodAlt": "ביצה · 95.06%"});
Object.assign(copy.en, {"demoNav": "On mobile", "demoEyebrow": "FROM MODEL TO MOBILE", "demoTitle": "See it in practice.", "demoIntro": "Three phone prediction examples and screenshots of the website accessed through ngrok. They document actual usage, including observed limitations.", "demoNote": "Screenshots document a demonstration on 29 October 2026; they are not an overall accuracy measure. The ngrok address depends on the computer, server and tunnel remaining online.", "demoOpen": "Open full-size demo screenshots", "demoView": "View screenshots ↗", "demoClose": "Close screenshot", "demoPrevious": "Previous", "demoNext": "Next", "demoOriginal": "Open original ↗", "demoCellularBadge": "PHONE ACCESS · NGROK", "demoCellularTitle": "From computer to phone", "demoCellularDescription": "The homepage as displayed on a phone, with the ngrok address visible. The connection shown when the screenshot was taken does not establish which connection was used for inference.", "demoCellularAlt": "From computer to phone", "demoWithoutBadge": "MASKVISION · WITHOUT MASK", "demoWithoutTitle": "Without mask · 80.6%", "demoWithoutDescription": "A phone input image and a Without mask prediction at 80.6% confidence. The updated screenshots show a 5G connection without a Wi-Fi indicator.", "demoWithoutAlt": "Without mask · 80.6%", "demoFacepaintBadge": "MASKVISION · FAILURE CASE", "demoFacepaintTitle": "Face paint that confuses the model", "demoFacepaintDescription": "This image has no mask, but the model predicted With mask at 98.2% confidence. A limitation of the model: high confidence does not guarantee a correct answer.", "demoFacepaintAlt": "Face paint that confuses the model", "demoFoodBadge": "FOODVISION · FOOD RECOGNITION", "demoFoodTitle": "Egg · 95.06%", "demoFoodDescription": "An image uploaded from a phone and classified as Egg. The interface also shows alternative predictions.", "demoFoodAlt": "Egg · 95.06%"});
const config = window.VISION_CONFIG || { foodUrl: '/', maskUrl: '/mask', homeUrl: '/home' };
let language = new URLSearchParams(location.search).get('lang');
if (!['he', 'en'].includes(language)) {
  try { language = localStorage.getItem('vision-language'); } catch { /* Optional persistence. */ }
}
if (!['he', 'en'].includes(language)) language = 'he';

function projectLink(value) {
  const url = new URL(value, location.origin);
  if (!['http:', 'https:'].includes(url.protocol)) throw new Error('Project links must use HTTP or HTTPS');
  url.searchParams.set('lang', language);
  return url.href;
}
function renderLanguage() {
  const t = copy[language];
  document.documentElement.lang = language;
  document.documentElement.dir = language === 'he' ? 'rtl' : 'ltr';
  document.title = t.title;
  document.querySelector('meta[name="description"]').content = t.intro;
  document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t[el.dataset.i18n]; });
  document.querySelectorAll('[data-label]').forEach(el => { el.setAttribute('aria-label', t[el.dataset.label]); });
  document.querySelectorAll('[data-alt]').forEach(el => { el.alt = t[el.dataset.alt]; });
  document.querySelectorAll('[data-language]').forEach(el => { el.setAttribute('aria-pressed', String(el.dataset.language === language)); });
  document.querySelectorAll('[data-project]').forEach(el => { el.href = projectLink(config[el.dataset.project + 'Url']); });
  document.querySelectorAll('[data-home]').forEach(el => { el.href = projectLink(config.homeUrl); });
  document.querySelectorAll('[data-results]').forEach(el => { el.href = '/results?lang=' + language; });
  try { localStorage.setItem('vision-language', language); } catch { /* Storage may be disabled. */ }
  if (demoDialog.open) renderDemo();
}
document.querySelectorAll('[data-language]').forEach(button => button.addEventListener('click', () => {
  language = button.dataset.language;
  const url = new URL(location.href);
  url.searchParams.set('lang', language);
  history.replaceState(null, '', url);
  renderLanguage();
}));

// Screenshots document previous phone runs; this gallery performs no inference.
const demoAlbums = [{"id": "cellular", "cover": "home-cellular.jpg", "badge": ["גישה מהטלפון · NGROK", "PHONE ACCESS · NGROK"], "title": ["מהמחשב אל הטלפון", "From computer to phone"], "description": ["דף הבית כפי שהוצג בטלפון, עם כתובת ngrok בשורת הכתובת. סוג החיבור בזמן צילום המסך אינו מעיד באיזה חיבור בוצע החיזוי.", "The homepage as displayed on a phone, with the ngrok address visible. The connection shown when the screenshot was taken does not establish which connection was used for inference."], "images": [{"file": "home-cellular.jpg", "caption": ["דף הבית בטלפון, עם כתובת HTTPS של ngrok. צילום זה מתעד את תצוגת האתר ולא את חיבור הרשת שבו בוצע החיזוי.", "The homepage on a phone with the ngrok HTTPS address visible. This screenshot records the website display, not the network connection used for inference."]}, {"file": "home-about.jpg", "caption": ["הסבר הפרויקט ושלבי השימוש בתצוגת טלפון.", "Project description and usage steps on a phone."]}]}, {"id": "without", "cover": "mask-without-result.jpg", "badge": ["MASKVISION · ללא מסכה", "MASKVISION · WITHOUT MASK"], "title": ["בלי מסכה · 80.6%", "Without mask · 80.6%"], "description": ["תמונת קלט ותוצאת ״בלי מסכה״ בביטחון 80.6% מהטלפון. בצילומי המסך המעודכנים מופיע חיבור 5G ללא סמל Wi‑Fi.", "A phone input image and a Without mask prediction at 80.6% confidence. The updated screenshots show a 5G connection without a Wi-Fi indicator."], "images": [{"file": "mask-without-input.jpg", "caption": ["תמונת הקלט בממשק הטלפון; בשורת המצב מופיע 5G ללא סמל Wi‑Fi.", "The input image in the phone interface; the status bar shows 5G without a Wi-Fi indicator."], "version": "20261029-2212"}, {"file": "mask-without-result.jpg", "caption": ["״בלי מסכה״ — 80.6%; ״עם מסכה״ — 19.4%. בצילום מופיע סמל 5G.", "Without mask — 80.6%; With mask — 19.4%. The screenshot shows the 5G indicator."], "version": "20261029-2212"}]}, {"id": "facepaint", "cover": "facepaint-result.jpg", "badge": ["MASKVISION · מקרה כשל", "MASKVISION · FAILURE CASE"], "title": ["איפור פנים שמבלבל את המודל", "Face paint that confuses the model"], "description": ["בדוגמה זו אין מסכה, אך המודל חזה ״עם מסכה״ בביטחון 98.2%. דוגמה למגבלה: ביטחון גבוה אינו מבטיח תשובה נכונה.", "This image has no mask, but the model predicted With mask at 98.2% confidence. A limitation of the model: high confidence does not guarantee a correct answer."], "images": [{"file": "facepaint-input.jpg", "caption": ["תמונת פנים עם איפור וללא מסכה בממשק הטלפון. בשורת המצב מופיע 5G.", "A painted face without a mask in the phone interface. The status bar shows 5G."], "version": "20261029-2212"}, {"file": "facepaint-result.jpg", "caption": ["מקרה כשל: ״עם מסכה״ בביטחון 98.2% בתמונה ללא מסכה. בצילום מופיע 5G; שורת הכתובת אינה מוצגת.", "Failure case: With mask at 98.2% confidence for an image without a mask. The screenshot shows 5G; the address bar is not visible."], "version": "20261029-2212"}]}, {"id": "food", "cover": "food-result.jpg", "badge": ["FOODVISION · זיהוי מזון", "FOODVISION · FOOD RECOGNITION"], "title": ["ביצה · 95.06%", "Egg · 95.06%"], "description": ["תמונה שהועלתה מהטלפון וסווגה כ״ביצה״. הממשק מציג גם את התחזיות החלופיות.", "An image uploaded from a phone and classified as Egg. The interface also shows alternative predictions."], "images": [{"file": "food-source.jpg", "caption": ["תמונת המזון שנבחרה לצורך ההדגמה.", "The food image selected for the demonstration."]}, {"file": "food-input.jpg", "caption": ["תמונת המזון כפי שהוצגה לאחר ההעלאה בטלפון.", "The food image displayed after uploading it from the phone."]}, {"file": "food-result.jpg", "caption": ["תחזית ״ביצה״ בביטחון 95.06%, לצד תחזיות לחם ואטריות ופסטה.", "Egg prediction at 95.06% confidence, alongside Bread and Noodles-Pasta alternatives."]}]}];
const demoDialog = document.getElementById('demo-dialog');
let activeDemo = null, activeDemoIndex = 0, demoOpener = null;
function renderDemo() {
  if (!activeDemo) return;
  const index = language === 'he' ? 0 : 1, item = activeDemo.images[activeDemoIndex];
  const path = '/hub-static/assets/mobile-demo/' + item.file + (item.version ? '?v=' + item.version : '');
  document.getElementById('demo-dialog-title').textContent = activeDemo.title[index];
  const image = document.getElementById('demo-full-image');image.src = path;image.alt = item.caption[index];
  document.getElementById('demo-caption').textContent = item.caption[index];
  document.getElementById('demo-counter').textContent = (activeDemoIndex + 1) + ' / ' + activeDemo.images.length;
  document.getElementById('demo-original').href = path;
  document.getElementById('demo-previous').disabled = activeDemoIndex === 0;
  document.getElementById('demo-next').disabled = activeDemoIndex === activeDemo.images.length - 1;
}
document.querySelectorAll('[data-demo]').forEach(button => button.addEventListener('click', () => {
  activeDemo = demoAlbums.find(album => album.id === button.dataset.demo);activeDemoIndex = 0;demoOpener = button;
  renderDemo();demoDialog.showModal();document.getElementById('demo-close').focus();
}));
document.getElementById('demo-close').addEventListener('click', () => demoDialog.close());
demoDialog.addEventListener('click', event => {if (event.target === demoDialog) {const rect=demoDialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)demoDialog.close();}});
demoDialog.addEventListener('close', () => {if(demoOpener)demoOpener.focus();});
document.getElementById('demo-previous').addEventListener('click', () => {if(activeDemoIndex>0){activeDemoIndex--;renderDemo();}});
document.getElementById('demo-next').addEventListener('click', () => {if(activeDemoIndex<activeDemo.images.length-1){activeDemoIndex++;renderDemo();}});

renderLanguage();
