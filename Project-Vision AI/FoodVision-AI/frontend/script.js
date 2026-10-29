// כל הטקסטים של הממשק מרוכזים כאן, כולל הודעות שנוצרות אחרי פעולה.
const translations = {
  en: {
    backToHome: 'Back to Home',
    languageHebrew: '🇮🇱 עברית', languageEnglish: '🇺🇸 English',
    pageTitle: 'FoodVision AI · A fresh perspective on food', home: 'FoodVision AI home', navigation: 'Main navigation', language: 'Choose language',
    navStudio: 'Explore the studio', eyebrow: 'A NEW PERSPECTIVE ON FOOD', heroTitle: 'See food differently.', heroAccent: 'Powered by AI.',
    intro: 'Every dish has a story. Discover the intersection of great food and computer vision — a new way to explore what’s on your plate.', heroCta: 'Explore the vision studio', heroNote: 'Start with a photo. Stay for the possibilities.',
    tagVision: 'Computer vision', tagFood: 'Food, in focus', tagCuriosity: 'Made for discovery', artLabel: 'A black ceramic bowl of ramen with golden noodles, rich amber broth, soft-boiled eggs and red chili, lit by warm cinematic light.',
    visualTitle: 'THE FOODVISION EDIT', chipTitle: 'A feast for your curiosity', chipSubtitle: 'Food. Detail. Discovery.', chipStatus: 'Model in development', chipStatusSub: 'No inference is running', visualCaption: 'EDITORIAL VISUAL · NOT A PREDICTION',
    stripLabel: 'FROM CURIOSITY TO DISCOVERY', stripOne: 'A university project', stripTwo: 'Powered by ideas', stripThree: 'Designed for exploration',
    studioEyebrow: 'YOUR FOOD, IN FOCUS', studioTitle: 'The vision studio', studioDescription: 'One photo. A whole new perspective.', modelStatus: 'Model not connected',
    uploadTitle: 'Add your photo', localOnly: 'Stays on your device', uploadPrompt: 'Bring something delicious.', uploadInstructions: 'Drop a food photo here, or choose an image below.', fileHint: 'JPEG, PNG or WebP · up to 15 MB', previewAlt: 'Preview of your selected food photo',
    chooseImage: 'Choose image', camera: 'Use camera', cameraHelp: 'Choose from your computer or phone gallery. Camera capture is available on supported mobile devices.', remove: 'Remove', classify: 'Classify Food', save: 'Save Image',
    resultsTitle: 'Your results', resultKicker: 'THE NEXT CHAPTER', defaultHeading: 'A little patience. A smarter plate.', defaultMessage: 'Your photos are welcome. Food classification will be available once our trained CNN model is connected.',
    predictedFood: 'Predicted food', confidence: 'Confidence', unavailable: 'Not available', unknownFood: 'Unrecognized food class', honesty: 'A university project in progress. No predictions or confidence scores are generated while the model is unavailable.',
    workflow: 'How the studio works', stepOneTitle: 'Bring your own plate.', stepOneText: 'Start with a clear, well-lit food photo. Curiosity is the only other ingredient.', stepTwoTitle: 'Find your best angle.', stepTwoText: 'Preview your image, switch it out, or save a copy to your device.', stepThreeTitle: 'Watch this space.', stepThreeText: 'Coming next: food recognition with a trained convolutional neural network.',
    footer: 'Made for curious minds. A university computer vision project.', footerNote: 'A fresh perspective, one plate at a time.',
    switchLight: 'Switch to light mode', switchDark: 'Switch to dark mode', invalidImage: 'Please choose an image file.', tooLarge: 'This image is too large. Please choose one up to 15 MB.',
    loading: 'Preparing your image…', ready: 'Photo ready. Your image stays in this browser; it is not uploaded to a server.', decodeError: 'Your browser could not preview this image. Please try a JPEG, PNG or WebP photo.', saved: 'Image download requested. Your browser may ask where to save it.',
    modelHeading: 'New model not available yet.', modelMessage: 'Your image is ready. Food classification will be available after the new model is trained.', predictionHeading: 'A new perspective on your plate.', predictionMessage: 'Classification result from the connected model.', downloadName: 'foodvision-image'
  },
  he: {
    backToHome: 'חזרה לדף הראשי',
    languageHebrew: '🇮🇱 עברית', languageEnglish: '🇺🇸 English',
    pageTitle: 'FoodVision AI · מבט חדש על אוכל', home: 'דף הבית של FoodVision AI', navigation: 'ניווט ראשי', language: 'בחירת שפה',
    navStudio: 'לסטודיו התמונות', eyebrow: 'נקודת מבט חדשה על אוכל', heroTitle: 'לגלות אוכל מזווית חדשה.', heroAccent: 'בעזרת בינה מלאכותית.',
    intro: 'לכל מנה יש סיפור. גלו את המפגש בין אוכל משובח לראייה ממוחשבת — דרך חדשה לחקור את מה שיש בצלחת שלכם.', heroCta: 'לגלות את סטודיו התמונות', heroNote: 'מתחילים בתמונה. ממשיכים באפשרויות.',
    tagVision: 'ראייה ממוחשבת', tagFood: 'אוכל במרכז', tagCuriosity: 'נוצר כדי לגלות', artLabel: 'קערת ראמן מקרמיקה שחורה עם אטריות זהובות, ציר עשיר בגוון ענבר, ביצים רכות וצ׳ילי אדום, בתאורה קולנועית חמימה.',
    visualTitle: 'המבט של FoodVision', chipTitle: 'חגיגה של סקרנות', chipSubtitle: 'אוכל. פרטים. גילוי.', chipStatus: 'המודל בפיתוח', chipStatusSub: 'לא מתבצע חיזוי', visualCaption: 'תמונה להמחשה · אינה תוצאת חיזוי',
    stripLabel: 'מסקרנות לגילוי', stripOne: 'פרויקט אוניברסיטאי', stripTwo: 'מונע ברעיונות', stripThree: 'נועד לחקירה ולגילוי',
    studioEyebrow: 'האוכל שלכם במרכז', studioTitle: 'סטודיו התמונות', studioDescription: 'תמונה אחת. נקודת מבט חדשה לגמרי.', modelStatus: 'המודל טרם חובר',
    uploadTitle: 'הוספת תמונה', localOnly: 'נשארת במכשיר שלכם', uploadPrompt: 'בואו נתחיל במשהו טעים.', uploadInstructions: 'גררו לכאן תמונת אוכל, או בחרו תמונה למטה.', fileHint: 'תמונות JPEG, PNG או WebP · עד 15 מגה־בייט', previewAlt: 'תצוגה מקדימה של תמונת האוכל שנבחרה',
    chooseImage: 'בחירת תמונה', camera: 'צילום במצלמה', cameraHelp: 'בחרו תמונה מהמחשב או מהגלריה בטלפון. צילום ישיר זמין במכשירים ניידים תומכים.', remove: 'הסרה', classify: 'זיהוי האוכל', save: 'שמירת תמונה',
    resultsTitle: 'התוצאות שלכם', resultKicker: 'השלב הבא', defaultHeading: 'קצת סבלנות. צלחת חכמה יותר.', defaultMessage: 'אפשר כבר להוסיף תמונות. זיהוי האוכל יהיה זמין לאחר חיבור המודל המאומן של הרשת העצבית הקונבולוציונית.',
    predictedFood: 'האוכל שזוהה', confidence: 'רמת ביטחון', unavailable: 'לא זמין', unknownFood: 'קטגוריית אוכל לא מוכרת', honesty: 'פרויקט אוניברסיטאי בתהליך פיתוח. כל עוד המודל אינו זמין, לא מוצגות תחזיות או רמות ביטחון.',
    workflow: 'איך הסטודיו עובד', stepOneTitle: 'הצלחת שלכם, הסקרנות שלכם.', stepOneText: 'התחילו בתמונת אוכל ברורה ומוארת. סקרנות היא המרכיב הנוסף היחיד שצריך.', stepTwoTitle: 'מוצאים את הזווית הנכונה.', stepTwoText: 'צפו בתמונה, החליפו אותה או שמרו עותק במכשיר שלכם.', stepThreeTitle: 'יש למה לצפות.', stepThreeText: 'בשלב הבא: זיהוי אוכל באמצעות רשת עצבית קונבולוציונית מאומנת.',
    footer: 'נוצר לאנשים סקרנים. פרויקט אוניברסיטאי בראייה ממוחשבת.', footerNote: 'מבט רענן, צלחת אחת בכל פעם.',
    switchLight: 'מעבר למצב בהיר', switchDark: 'מעבר למצב כהה', invalidImage: 'יש לבחור קובץ תמונה.', tooLarge: 'התמונה גדולה מדי. יש לבחור תמונה בגודל של עד 15 מגה־בייט.',
    loading: 'מכינים את התמונה לתצוגה…', ready: 'התמונה מוכנה. היא נשארת בדפדפן ואינה נשלחת לשרת.', decodeError: 'הדפדפן לא הצליח להציג את התמונה. נסו תמונה בפורמט JPEG, PNG או WebP.', saved: 'הורדת התמונה התבקשה. ייתכן שהדפדפן יבקש לבחור היכן לשמור אותה.',
    modelHeading: 'המודל החדש עדיין אינו זמין.', modelMessage: 'התמונה מוכנה. זיהוי אוכל יהיה זמין לאחר אימון המודל החדש.', predictionHeading: 'מבט חדש על הצלחת שלכם.', predictionMessage: 'תוצאת זיהוי מהמודל המחובר.', downloadName: 'foodvision-image'
  }
};

Object.assign(translations.en, {"chipStatus":"Food-11 CNN","chipStatusSub":"11 food categories","modelStatus":"Model available on server","localOnly":"Upload on classification","ready":"Photo ready. Classify Food sends it to the server.","defaultHeading":"What’s on your plate?","defaultMessage":"Choose a photo and classify it with Food-11.","honesty":"Confidence below 60% is displayed as Unknown. The model recognizes 11 food categories.","stepThreeTitle":"Discover your food.","stepThreeText":"Classify your photo with the trained Food-11 CNN.","modelHeading":"Model unavailable.","modelMessage":"The model could not be loaded. Please try again after the server is ready.","predicting":"Classifying your photo…","inferenceError":"Classification failed. Please try again.","networkError":"Could not reach the server. Please try again.","unknownFood":"Unknown","rawPrediction":"Best match","lowConfidence":"Confidence below 60%.","modelUnavailable":"Model unavailable"});
Object.assign(translations.he, {"chipStatus":"מודל Food-11 CNN","chipStatusSub":"11 קטגוריות מזון","modelStatus":"המודל זמין בשרת","localOnly":"שליחה בעת הזיהוי","ready":"התמונה מוכנה. זיהוי האוכל שולח אותה לשרת.","defaultHeading":"מה יש בצלחת?","defaultMessage":"בחרו תמונה וזהו אותה באמצעות Food-11.","honesty":"רמת ביטחון נמוכה מ־60% מוצגת כלא ידוע. המודל מזהה 11 קטגוריות מזון.","stepThreeTitle":"מגלים את האוכל.","stepThreeText":"זהו את התמונה באמצעות מודל Food-11 CNN המאומן.","modelHeading":"המודל אינו זמין.","modelMessage":"טעינת המודל נכשלה. נסו שוב לאחר שהשרת יהיה מוכן.","predicting":"מזהים את האוכל…","inferenceError":"הזיהוי נכשל. נסו שוב.","networkError":"לא ניתן להתחבר לשרת. נסו שוב.","unknownFood":"לא ידוע","rawPrediction":"ההתאמה המובילה","lowConfidence":"רמת הביטחון נמוכה מ־60%.","modelUnavailable":"המודל אינו זמין"});

Object.assign(translations.en, {
  "analysisLabel": "VISION INTELLIGENCE",
  "idleStatus": "Awaiting a photo",
  "workingStatus": "Analyzing image",
  "matchedStatus": "✅ High Confidence",
  "finalResult": "Final result",
  "uncertainStatus": "⚠️ Low Confidence",
  "errorStatus": "Analysis unavailable",
  "topThree": "Top predictions",
  "probabilityLabel": "Model probability",
  "modelScore": "Model confidence",
  "thresholdLabel": "Threshold · 60%",
  "highInterpretation": "The model assigns high confidence to this result. This does not guarantee a correct classification.",
  "unknownInterpretation": "Confidence is below the 60% threshold, so the system marks this image as Unknown.",
  "analysisHeading": "Looking closer…",
  "analysisMessage": "Comparing your photo across the 11 food categories.",
  "errorHeading": "Let’s try that again.",
  "modelChecking": "Checking model…"
});
Object.assign(translations.he, {
  "analysisLabel": "ניתוח תמונה חכם",
  "idleStatus": "ממתינים לתמונה",
  "workingStatus": "מנתחים את התמונה",
  "matchedStatus": "✅ רמת ביטחון גבוהה",
  "finalResult": "תוצאה סופית",
  "uncertainStatus": "⚠️ רמת ביטחון נמוכה",
  "errorStatus": "הניתוח אינו זמין",
  "topThree": "התחזיות המובילות",
  "probabilityLabel": "הסתברות המודל",
  "modelScore": "רמת הביטחון של המודל",
  "thresholdLabel": "סף · 60%",
  "highInterpretation": "המודל מייחס רמת ביטחון גבוהה לתוצאה זו. הדבר אינו מבטיח שהזיהוי נכון.",
  "unknownInterpretation": "רמת הביטחון נמוכה מסף של 60%, ולכן המערכת מסמנת את התמונה כלא ידועה.",
  "analysisHeading": "מבט מקרוב…",
  "analysisMessage": "משווים את התמונה ל־11 קטגוריות המזון.",
  "errorHeading": "ננסה שוב.",
  "modelChecking": "בודקים את המודל…"
});

Object.assign(translations.en, {
  "categoryEyebrow": "THE FOOD-11 COLLECTION",
  "categoryTitle": "What’s on the menu?",
  "categoryIntro": "Explore the 11 food categories our model is trained to recognize.",
  "categoryCount": "food categories",
  "categoryNote": "The model predicts a category, rather than the exact dish. A clear photo of a single dish helps it make a better match."
});
Object.assign(translations.he, {
  "categoryEyebrow": "אוסף הקטגוריות של FOOD-11",
  "categoryTitle": "מה בתפריט של המודל?",
  "categoryIntro": "הכירו את 11 קטגוריות המזון שהמודל שלנו אומן לזהות.",
  "categoryCount": "קטגוריות מזון",
  "categoryNote": "המודל מזהה קטגוריית מזון, ולא את שם המנה המדויק. תמונה ברורה של מנה אחת עוזרת לו למצוא התאמה טובה יותר."
});

Object.assign(translations.en, {"exampleFruit": "Fruit", "examplesTitle": "Try an example", "examplesHint": "One click loads a sample and runs a real prediction.", "exampleRamen": "Ramen bowl", "exampleFace": "Face photo", "exampleNoFace": "No-face check", "exampleError": "Could not load the sample. Try again."});
Object.assign(translations.he, {"examplesTitle":"נסו דוגמה","examplesHint":"לחיצה טוענת תמונה לדוגמה ומפעילה זיהוי אמיתי.","exampleFruit": "פירות","exampleRamen":"קערת ראמן","exampleFace":"תמונת פנים","exampleNoFace":"בדיקה ללא פנים","exampleError":"טעינת הדוגמה נכשלה. נסו שוב."});

function readPreference(key, fallback) {
  try { return localStorage.getItem(key) || fallback; }
  catch { return fallback; }
}
function savePreference(key, value) {
  // חסימת אחסון בדפדפן לא צריכה למנוע החלפת שפה או ערכת צבעים.
  try { localStorage.setItem(key, value); } catch { /* ההעדפה נשמרת בעמוד הנוכחי בלבד. */ }
}
const incomingLanguage = new URLSearchParams(location.search).get('lang');
let language = (['he', 'en'].includes(incomingLanguage) ? incomingLanguage : readPreference('vision-language', readPreference('foodvision-language', 'he'))) === 'he' ? 'he' : 'en';
let theme = readPreference('foodvision-theme', 'dark') === 'light' ? 'light' : 'dark';
let selectedFile = null;
let previewUrl = null;
let imageVersion = 0;
let messageKey = '';
let resultState = 'empty';
let prediction = null;
let requestController = null;
let modelReady = null;
const hebrewClasses = {"Bread":"לחם","Dairy product":"מוצרי חלב","Dessert":"קינוח","Egg":"ביצה","Fried food":"אוכל מטוגן","Meat":"בשר","Noodles-Pasta":"אטריות ופסטה","Rice":"אורז","Seafood":"מאכלי ים","Soup":"מרק","Vegetable-Fruit":"ירקות ופירות"};
const classLabel = name => name === 'Unknown' ? t('unknownFood') : language === 'he' ? (hebrewClasses[name] || name) : name;
const fileInput = document.getElementById('file-input');
const cameraInput = document.getElementById('camera-input');
const preview = document.getElementById('preview');
const dropZone = document.getElementById('drop-zone');
const classifyButton = document.getElementById('classify-button');
const saveButton = document.getElementById('save-button');
const t = key => translations[language][key];

const categoryIcons = {
  Bread: '🍞', 'Dairy product': '🥛', Dessert: '🍰', Egg: '🥚', 'Fried food': '🍟',
  Meat: '🥩', 'Noodles-Pasta': '🍝', Rice: '🍚', Seafood: '🦐', Soup: '🍲', 'Vegetable-Fruit': '🥦'
};
let resultAnimationFrame = 0;
let animatedPrediction = null;
const percentText = value => value.toFixed(2) + '%';

// האחוז הראשי כבר מגיע באחוזים; הסתברויות המחלקות מוכפלות פעם אחת בלבד.
function topPredictions(data) {
  return [...data.probabilities].sort((a, b) => b.probability - a.probability).slice(0, 3)
    .map(item => ({ category: item.category, percent: item.probability * 100 }));
}
function validatePrediction(data) {
  if (!data || typeof data.prediction !== 'string' || !Object.hasOwn(hebrewClasses, data.raw_prediction)
    || !Number.isFinite(data.confidence) || data.confidence < 0 || data.confidence > 100
    || !Array.isArray(data.probabilities) || data.probabilities.length !== 11) return false;
  const names = new Set();
  for (const item of data.probabilities) {
    if (!item || !Object.hasOwn(hebrewClasses, item.category) || names.has(item.category)
      || !Number.isFinite(item.probability) || item.probability < 0 || item.probability > 1) return false;
    names.add(item.category);
  }
  const best = topPredictions(data)[0];
  return Math.abs(data.probabilities.reduce((sum, item) => sum + item.probability, 0) - 1) < 0.001
    && Math.abs(best.percent - data.confidence) < 0.001
    && Math.abs(data.probabilities.find(item => item.category === data.raw_prediction).probability * 100 - data.confidence) < 0.001
    && data.prediction === (data.confidence < 60 ? 'Unknown' : data.raw_prediction);
}

// יצירת טקסט דינמי באמצעות DOM בלבד שומרת על תוכן בטוח.
function renderResults() {
  cancelAnimationFrame(resultAnimationFrame);
  const success = resultState === 'success' && prediction;
  const low = success && prediction.prediction === 'Unknown';
  const loading = resultState === 'loading';
  const failed = ['error', 'unavailable'].includes(resultState);
  const card = document.querySelector('.results-card');
  const surface = document.getElementById('prediction-surface');
  const fresh = success && animatedPrediction !== prediction;
  card.dataset.state = loading ? 'loading' : success ? (low ? 'uncertain' : 'matched') : failed ? 'error' : 'empty';
  card.setAttribute('aria-busy', String(loading));
  surface.classList.remove('result-reveal');
  document.getElementById('prediction-status').textContent = t(loading ? 'workingStatus' : success ? (low ? 'uncertainStatus' : 'matchedStatus') : failed ? 'errorStatus' : 'idleStatus');
  document.getElementById('category-icon').textContent = success ? (low ? '◇' : categoryIcons[prediction.prediction] || '◎') : loading ? '◌' : failed ? '↻' : '◎';
  document.getElementById('result-heading').textContent = success ? classLabel(prediction.prediction) : t(loading ? 'analysisHeading' : resultState === 'unavailable' ? 'modelHeading' : failed ? 'errorHeading' : 'defaultHeading');
  document.getElementById('prediction-label').textContent = t(low ? 'finalResult' : 'predictedFood');
  const bestMatch = document.getElementById('best-match');
  bestMatch.hidden = !low;
  bestMatch.textContent = low ? t('rawPrediction') + ': ' + classLabel(prediction.raw_prediction) : '';
  document.getElementById('result-message').textContent = success
    ? (low ? t('unknownInterpretation') : t('highInterpretation').replace('{category}', classLabel(prediction.raw_prediction)))
    : t(loading ? 'analysisMessage' : resultState === 'unavailable' ? 'modelMessage' : failed ? 'inferenceError' : 'defaultMessage');
  document.getElementById('confidence-section').hidden = !success;
  document.getElementById('top-predictions').hidden = !success;
  document.getElementById('confidence-result').textContent = success ? percentText(prediction.confidence) : '';
  const meter = document.getElementById('confidence-meter');
  if (success) meter.setAttribute('aria-valuenow', prediction.confidence);
  else meter.removeAttribute('aria-valuenow');
  const fill = document.getElementById('confidence-fill');
  fill.style.width = success && !fresh ? prediction.confidence + '%' : '0%';
  const list = document.getElementById('probability-list');
  list.replaceChildren();
  const fills = [];
  if (success) {
    topPredictions(prediction).forEach((item, index) => {
      const row = document.createElement('li');
      row.className = 'probability-row';
      const rank = document.createElement('span');
      rank.className = 'probability-rank';
      rank.textContent = String(index + 1) + '.';
      rank.setAttribute('aria-hidden', 'true');
      const body = document.createElement('div');
      body.className = 'probability-body';
      const head = document.createElement('div');
      head.className = 'probability-head';
      const name = document.createElement('span');
      name.textContent = classLabel(item.category);
      const value = document.createElement('bdi');
      value.dir = 'ltr';
      value.textContent = percentText(item.percent);
      head.append(name, value);
      const track = document.createElement('div');
      track.className = 'probability-track';
      track.setAttribute('aria-hidden', 'true');
      const bar = document.createElement('span');
      bar.className = 'meter-fill';
      bar.style.width = fresh ? '0%' : item.percent + '%';
      bar.style.transitionDelay = index * 70 + 'ms';
      track.append(bar);
      body.append(head, track);
      row.append(rank, body);
      list.append(row);
      fills.push([bar, item.percent]);
    });
    if (fresh) {
      // ציור מצב האפס לפני הפעלת המעבר, גם בחיזוי חוזר.
      void surface.offsetWidth;
      surface.classList.add('result-reveal');
    }
    resultAnimationFrame = requestAnimationFrame(() => {
      fill.style.width = prediction.confidence + '%';
      fills.forEach(([bar, value]) => { bar.style.width = value + '%'; });
    });
    animatedPrediction = prediction;
  } else {
    animatedPrediction = null;
  }
  document.querySelector('[data-i18n="modelStatus"]').textContent = t(modelReady === null ? 'modelChecking' : modelReady ? 'modelStatus' : 'modelUnavailable');
}

function showMessage(key) {
  messageKey = key;
  const message = document.getElementById('upload-message');
  message.textContent = key ? t(key) : '';
  // מצב ההודעה משמש גם לעיצוב, בלי להסתמך על השפה של הטקסט.
  message.dataset.state = ['invalidImage', 'tooLarge', 'decodeError', 'inferenceError', 'networkError', 'modelUnavailable'].includes(key) ? 'error' : ['loading', 'predicting'].includes(key) ? 'loading' : key ? 'success' : '';
}
function renderTheme() {
  document.documentElement.dataset.theme = theme;
  const label = t(theme === 'dark' ? 'switchLight' : 'switchDark');
  const toggle = document.getElementById('theme-toggle');
  toggle.setAttribute('aria-label', label);
  toggle.title = label;
  document.getElementById('theme-label').textContent = label;
  document.getElementById('theme-icon').textContent = theme === 'dark' ? '☀' : '☾';
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#101114' : '#faf8f3';
}
function applyLanguage() {
  document.documentElement.lang = language;
  document.documentElement.dir = language === 'he' ? 'rtl' : 'ltr';
  document.getElementById('hub-home-link').href = '/home?lang=' + language;
  savePreference('vision-language', language);
  document.title = t('pageTitle');
  // שמות הקטגוריות מתעדכנים יחד עם שפת האתר.
  document.querySelectorAll('[data-food-category]').forEach(item => {
    item.querySelector('.food-category-name').textContent = classLabel(item.dataset.foodCategory);
    item.querySelector('.food-category-original').hidden = language !== 'he';
  });
  document.querySelectorAll('[data-i18n]').forEach(element => { element.textContent = t(element.dataset.i18n); });
  document.querySelectorAll('[data-label]').forEach(element => { element.setAttribute('aria-label', t(element.dataset.label)); });
  document.querySelectorAll('[data-alt]').forEach(element => { element.alt = t(element.dataset.alt); });
  document.querySelectorAll('[data-language]').forEach(button => { button.setAttribute('aria-pressed', String(button.dataset.language === language)); });
  showMessage(messageKey);
  renderResults();
  renderTheme();
}
document.querySelectorAll('[data-language]').forEach(button => button.addEventListener('click', () => {
  language = button.dataset.language;
  savePreference('foodvision-language', language);
  applyLanguage();
}));
document.getElementById('theme-toggle').addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  savePreference('foodvision-theme', theme);
  renderTheme();
});

function clearImage() {
  // מספר הגרסה מונע מתמונה קודמת לדרוס בחירה חדשה בזמן טעינה.
  imageVersion += 1;
  requestController?.abort();
  requestController = null;
  prediction = null;
  classifyButton.setAttribute('aria-busy', 'false');
  preview.onload = null;
  preview.onerror = null;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  selectedFile = null;
  preview.removeAttribute('src');
  preview.hidden = true;
  document.getElementById('empty-preview').hidden = false;
  document.getElementById('file-details').hidden = true;
  document.getElementById('file-name').textContent = '';
  dropZone.setAttribute('aria-busy', 'false');
  fileInput.value = '';
  cameraInput.value = '';
  classifyButton.disabled = true;
  saveButton.disabled = true;
  resultState = 'empty';
  showMessage('');
  renderResults();
}
function selectImage(file, autoClassify = false) {
  if (!file) return;
  if (!file.type.startsWith('image/')) { showMessage('invalidImage'); return; }
  if (file.size > 15 * 1024 * 1024) { showMessage('tooLarge'); return; }
  clearImage();
  const version = imageVersion;
  selectedFile = file;
  previewUrl = URL.createObjectURL(file);
  showMessage('loading');
  dropZone.setAttribute('aria-busy', 'true');
  // הפעולות זמינות רק אחרי שהדפדפן הצליח לפענח את התמונה.
  preview.onload = () => {
    if (version !== imageVersion) return;
    preview.hidden = false;
    document.getElementById('empty-preview').hidden = true;
    document.getElementById('file-details').hidden = false;
    document.getElementById('file-name').textContent = file.name;
    dropZone.setAttribute('aria-busy', 'false');
    classifyButton.disabled = false;
    saveButton.disabled = false;
    showMessage('ready');
    if (autoClassify) classifyButton.click();
  };
  preview.onerror = () => {
    if (version !== imageVersion) return;
    clearImage();
    showMessage('decodeError');
  };
  preview.src = previewUrl;
}
document.getElementById('choose-button').addEventListener('click', () => fileInput.click());
document.getElementById('camera-button').addEventListener('click', () => cameraInput.click());
fileInput.addEventListener('change', () => selectImage(fileInput.files[0]));
cameraInput.addEventListener('change', () => selectImage(cameraInput.files[0]));
document.getElementById('remove-button').addEventListener('click', clearImage);
['dragenter', 'dragover'].forEach(name => dropZone.addEventListener(name, event => {
  event.preventDefault(); dropZone.classList.add('drag-over');
}));
['dragleave', 'drop'].forEach(name => dropZone.addEventListener(name, event => {
  event.preventDefault(); dropZone.classList.remove('drag-over');
}));
dropZone.addEventListener('drop', event => selectImage(event.dataTransfer.files[0]));
// גרסת התמונה מונעת הצגת תוצאה של תמונה קודמת.
classifyButton.addEventListener('click', async () => {
  if (!selectedFile || classifyButton.disabled) return;
  const version = imageVersion;
  const controller = new AbortController();
  requestController = controller;
  const timeout = setTimeout(() => controller.abort(), 60000);
  const form = new FormData();
  form.append('file', selectedFile);
  classifyButton.disabled = true;
  classifyButton.setAttribute('aria-busy', 'true');
  prediction = null;
  resultState = 'loading';
  showMessage('predicting');
  renderResults();
  try {
    const response = await fetch('/predict', { method: 'POST', body: form, signal: controller.signal });
    const data = await response.json();
    if (version !== imageVersion) return;
    if (!response.ok) {
      const key = ['modelUnavailable', 'invalidImage', 'tooLarge', 'inferenceError'].includes(data.detail) ? data.detail : 'inferenceError';
      if (response.status === 503) modelReady = false;
      resultState = response.status === 503 ? 'unavailable' : 'error';
      showMessage(key);
    } else {
      if (!validatePrediction(data)) {
        resultState = 'error';
        showMessage('inferenceError');
        return;
      }
      prediction = data;
      modelReady = true;
      resultState = 'success';
      showMessage('');
    }
  } catch {
    if (version !== imageVersion) return;
    resultState = 'error';
    showMessage('networkError');
  } finally {
    clearTimeout(timeout);
    if (version === imageVersion) {
      requestController = null;
      classifyButton.disabled = false;
      classifyButton.setAttribute('aria-busy', 'false');
      renderResults();
    }
  }
});
saveButton.addEventListener('click', () => {
  if (!selectedFile || !previewUrl || saveButton.disabled) return;
  const link = document.createElement('a');
  link.href = previewUrl;
  link.download = selectedFile.name || t('downloadName');
  document.body.appendChild(link);
  link.click();
  link.remove();
  showMessage('saved');
});
applyLanguage();

fetch('/health').then(r => { if (!r.ok) throw new Error(); return r.json(); }).then(data => { modelReady = data.model_ready === true; renderResults(); }).catch(() => { modelReady = false; renderResults(); });

// Ignore a downloaded example if the user has selected or removed another photo.
document.querySelectorAll('[data-example]').forEach(button => {
  button.addEventListener('click', async () => {
    const current = imageVersion;
    const buttons = [...document.querySelectorAll('[data-example]')];
    buttons.forEach(item => item.disabled = true);
    button.setAttribute('aria-busy', 'true');
    const request = new AbortController();
    const timeout = setTimeout(() => request.abort(), 15000);
    try {
      const response = await fetch(button.dataset.example, {signal: request.signal});
      if (!response.ok) throw new Error('Example unavailable');
      const blob = await response.blob();
      if (current !== imageVersion) return;
      selectImage(new File([blob], button.dataset.example.split('/').pop(), {type: blob.type}), true);
    } catch {
      if (current === imageVersion) showMessage('exampleError');
    } finally {
      clearTimeout(timeout);
      buttons.forEach(item => item.disabled = false);
      button.removeAttribute('aria-busy');
    }
  });
});
