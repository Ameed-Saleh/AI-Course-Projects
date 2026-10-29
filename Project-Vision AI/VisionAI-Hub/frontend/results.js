'use strict';
const words = {
  he: {
    pageTitle:'Vision AI · תוצאות המודלים',skip:'לתוצאות המודלים',nav:'ניווט ראשי',language:'בחירת שפה',projectsNav:'הפרויקטים',aboutNav:'הרעיון',resultsNav:'תוצאות המודלים',eyebrow:'מאחורי התחזית',title:'לראות את התמונה.',accent:'להבין את המספרים.',intro:'תוצאות אמיתיות מתהליכי האימון והבדיקה. מבט על ההתקדמות, ההצלחות והטעויות של המודלים.',projectChoice:'בחירת פרויקט',back:'חזרה לדף הראשי',loading:'טוענים את התוצאות…',loadError:'לא ניתן לטעון את התוצאות כרגע. רעננו את העמוד ונסו שוב.',evaluationKicker:'בדיקה נפרדת · EVALUATION',evaluationTitle:'התוצאה על תמונות הבדיקה',evaluationAccuracy:'דיוק הבדיקה',evaluationLoss:'שגיאת הבדיקה',macroF1:'F1 ממוצע בין המחלקות',images:'תמונות בקבוצת הבדיקה',foodEvaluationNote:'הערכה של המודל הנבחר על קבוצת הבדיקה הנפרדת. הנתונים מיובאים מההרצה שנשלחה; הבדיקה לא הורצה מחדש באתר.',maskEvaluationNote:'מודל עם שתי מחלקות שאומן על 6,674 תמונות ואומת על 1,430. נבחר Epoch 24 לפי הפסד האימות. ההערכה נעשתה על 1,432 תמונות; מסכה לא תקינה הוחרגה. החלוקה אקראית לפי קבצים, ללא בדיקת כפילויות או זהויות. המדדים אינם כוללים את גלאי הפנים או סף Unknown.',trainingKicker:'הדרך לתוצאה',trainingTitle:'איך המודל למד?',model:'מודל',accuracyChart:'דיוק לאורך האימון',lossChart:'שגיאה לאורך האימון',train:'אימון',validation:'ולידציה',accuracyHelp:'גבוה יותר פירושו יותר סיווגים נכונים.',lossHelp:'נמוך יותר עדיף. פער מהוולידציה עשוי להצביע על התאמת יתר.',checkpointNote:'הגרפים מציגים את כל סבבי האימון. קובץ המודל נשמר לפי שגיאת הוולידציה הנמוכה ביותר, ולכן הוא אינו בהכרח מהסבב האחרון.',epochTable:'לצפייה בערכי הגרפים בטבלה',epoch:'סבב',trainAccuracy:'דיוק אימון',valAccuracy:'דיוק ולידציה',trainLoss:'שגיאת אימון',valLoss:'שגיאת ולידציה',comparisonKicker:'בחירת המודל',comparisonTitle:'השוואה על קבוצת הוולידציה',comparisonNote:'המודל נבחר לפי הוולידציה. קבוצת ה־Evaluation שימשה לבדיקה הסופית, ולא לבחירה בין המודלים.',selected:'נבחר',reportKicker:'מבט לכל קטגוריה',reportTitle:'איפה המודל מצליח?',reportNote:'Precision: כמה מהתחזיות לקטגוריה היו נכונות. Recall: כמה מתמונות הקטגוריה זוהו. F1: איזון בין שני המדדים.',category:'קטגוריה',support:'מספר תמונות',matrixKicker:'ללמוד גם מהטעויות',matrixTitle:'מטריצת הבלבול',fullImage:'פתיחה בגודל מלא ↗',matrixNote:'השורות הן הקטגוריות האמיתיות והעמודות הן תחזיות המודל. האלכסון מציג סיווגים נכונים; שאר התאים מראים טעויות.',matrixAlt:'מטריצת הבלבול של {project}: קטגוריות אמיתיות בשורות ותחזיות בעמודות.',downloadsTitle:'הנתונים שמאחורי הגרפים',foodDownloadsNote:'קובצי התוצאות של FoodVision, כפי שיוצאו מהרצת האימון והבדיקה.',maskDownloadsNote:'קובצי הייצוא של אימון MaskVision לשתי מחלקות: דוחות, היסטוריה, חלוקת נתונים וגרפי אימון.',confidenceTitle:'דיוק המודל אינו רמת הביטחון בתמונה.',confidenceNote:'דיוק נמדד על תמונות עם תוויות ידועות. ביטחון הוא הציון שהמודל נותן לתחזית בודדת. כלל Unknown מתחת ל־60% נשאר באתר, אך המדדים כאן חושבו לפני החלתו — ולא מודדים יכולת לזהות תמונות לא רלוונטיות.',footer:'נתונים אמיתיים. מקום ללמוד ולהשתפר.'
  },
  en: {
    pageTitle:'Vision AI · Model Results',skip:'Skip to model results',nav:'Main navigation',language:'Choose language',projectsNav:'The projects',aboutNav:'The idea',resultsNav:'Model Results',eyebrow:'BEHIND THE PREDICTION',title:'See the picture.',accent:'Understand the numbers.',intro:'Real results from training and evaluation. Explore the progress, strengths and mistakes of the models.',projectChoice:'Choose project',back:'Back to Home',loading:'Loading results…',loadError:'Could not load results. Refresh this page to try again.',evaluationKicker:'HELD-OUT EVALUATION',evaluationTitle:'Performance on the test images',evaluationAccuracy:'Evaluation accuracy',evaluationLoss:'Evaluation loss',macroF1:'Macro F1 across classes',images:'Evaluation images',foodEvaluationNote:'The selected model evaluated on a separate test split. Results are imported from the supplied run; evaluation was not repeated on this website.',maskEvaluationNote:'Two-class CNN trained on 6,674 images and validated on 1,430. Epoch 24 was selected by validation loss. Evaluation used 1,432 images; incorrectly worn masks were excluded. Random file split, without duplicate or identity checks. Face detection and the Unknown threshold are excluded.',trainingKicker:'THE PATH TO THE RESULT',trainingTitle:'How did the model learn?',model:'Model',accuracyChart:'Accuracy over training',lossChart:'Loss over training',train:'Training',validation:'Validation',accuracyHelp:'Higher means more correct classifications.',lossHelp:'Lower is better. A widening validation gap may indicate overfitting.',checkpointNote:'Charts show every training epoch. The checkpoint is saved at the lowest validation loss, so it may not come from the final epoch.',epochTable:'View chart values in a table',epoch:'Epoch',trainAccuracy:'Training accuracy',valAccuracy:'Validation accuracy',trainLoss:'Training loss',valLoss:'Validation loss',comparisonKicker:'MODEL SELECTION',comparisonTitle:'Comparison on the validation split',comparisonNote:'Validation was used to select the model. The Evaluation split was used for final testing, not for choosing between models.',selected:'Selected',reportKicker:'A LOOK AT EACH CLASS',reportTitle:'Where does the model succeed?',reportNote:'Precision: how many predictions of a class were correct. Recall: how many actual images of that class were found. F1: a balance of both.',category:'Class',support:'Images',matrixKicker:'LEARNING FROM MISTAKES',matrixTitle:'The confusion matrix',fullImage:'Open full-size image ↗',matrixNote:'Rows are the true classes; columns are the model predictions. The diagonal shows correct classifications; other cells show errors.',matrixAlt:'{project} confusion matrix: true classes in rows and predicted classes in columns.',downloadsTitle:'The data behind the charts',foodDownloadsNote:'FoodVision result files exported from the training and evaluation run.',maskDownloadsNote:'Exports from the two-class MaskVision training run: reports, history, dataset split and training curves.',confidenceTitle:'Accuracy is not the confidence in one photo.',confidenceNote:'Accuracy is measured on labeled images. Confidence is the score for a single prediction. The website still uses Unknown below 60%, but these metrics were computed before that rule and do not measure rejection of unrelated images.',footer:'Real data. Room to learn and improve.'
  }
};
const classHebrew={'Bread':'לחם','Dairy product':'מוצרי חלב','Dessert':'קינוחים','Egg':'ביצים','Fried food':'אוכל מטוגן','Meat':'בשר','Noodles-Pasta':'אטריות ופסטה','Rice':'אורז','Seafood':'מאכלי ים','Soup':'מרק','Vegetable-Fruit':'ירקות ופירות','with_mask':'עם מסכה','without_mask':'בלי מסכה'};
const $=id=>document.getElementById(id);
const query=new URLSearchParams(location.search);
let language=query.get('lang');
if(!['he','en'].includes(language)){try{language=localStorage.getItem('vision-language')}catch{}}
if(!['he','en'].includes(language))language='he';
let project=query.get('project')==='mask'?'mask':'food', modelName=null, results=null, failed=false;
const t=key=>words[language][key];
const num=(value,digits=0)=>new Intl.NumberFormat(language==='he'?'he-IL':'en-US',{minimumFractionDigits:digits,maximumFractionDigits:digits}).format(value);
const percent=value=>num(value*100,2)+'%';
function node(tag,text,className){const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(className)el.className=className;return el}
function updateUrl(){const url=new URL(location.href);url.searchParams.set('lang',language);url.searchParams.set('project',project);history.replaceState(null,'',url)}
function row(cells,header=false){const tr=node('tr');cells.forEach((value,index)=>{const cell=node(header?'th':'td',value);if(header)cell.scope='col';else if(index>0)cell.dir='ltr';tr.append(cell)});return tr}
function setHead(id,labels){$(id).replaceChildren(row(labels,true))}
function drawChart(id,history,key,maxValue){
  const ns='http://www.w3.org/2000/svg',W=620,H=290,L=59,R=20,T=20,B=46;
  function svgNode(tag,attrs,text){const el=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,v));if(text!==undefined)el.textContent=text;return el}
  const title=t(key==='accuracy'?'accuracyChart':'lossChart');
  const svg=svgNode('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':`${modelName}: ${title}`,direction:'ltr'});
  svg.append(svgNode('title',{},`${modelName}: ${title}`));
  const x=index=>L+index*(W-L-R)/Math.max(1,history.length-1), y=value=>T+(1-value/maxValue)*(H-T-B);
  for(let i=0;i<=4;i++){
    const value=maxValue*i/4,yy=y(value);
    svg.append(svgNode('line',{x1:L,x2:W-R,y1:yy,y2:yy,class:'chart-grid'}));
    svg.append(svgNode('text',{x:L-10,y:yy+4,'text-anchor':'end',class:'chart-tick'},key==='accuracy'?num(value*100)+'%':num(value,1)));
  }
  const ticks=[...new Set(Array.from({length:6},(_,i)=>Math.round(i*(history.length-1)/5)))];
  ticks.forEach(i=>svg.append(svgNode('text',{x:x(i),y:H-23,'text-anchor':'middle',class:'chart-tick'},num(history[i].epoch))));
  svg.append(svgNode('text',{x:(L+W-R)/2,y:H-4,'text-anchor':'middle',class:'chart-tick'},t('epoch')));
  for(const [field,label,style] of [[key,t('train'),'training-line'],['val_'+key,t('validation'),'validation-line']]){
    svg.append(svgNode('polyline',{points:history.map((point,i)=>`${x(i)},${y(point[field])}`).join(' '),class:style,fill:'none','stroke-width':2.3,'vector-effect':'non-scaling-stroke'}));
    history.forEach((point,i)=>{const dot=svgNode('circle',{cx:x(i),cy:y(point[field]),r:5,class:`chart-dot ${style}`});dot.append(svgNode('title',{},`${t('epoch')} ${point.epoch} · ${label}: ${key==='accuracy'?percent(point[field]):num(point[field],4)}`));svg.append(dot)});
  }
  $(id).replaceChildren(svg);
}
function render(){
  const d=results[project],ev=d.evaluation;
  document.querySelector('[data-project-download-note]').textContent=t(project==='food'?'foodDownloadsNote':'maskDownloadsNote');
  const current=d.models.find(m=>m.name===modelName)||d.models.find(m=>m.name===ev.selected_model)||d.models[0];modelName=current.name;
  $('evaluation-kicker').textContent=t('evaluationKicker');$('evaluation-title').textContent=t('evaluationTitle');$('selected-model').textContent=ev.selected_model;
  $('evaluation-note').textContent=t(project==='food'?'foodEvaluationNote':'maskEvaluationNote');
  $('metrics').replaceChildren();
  for(const [label,value] of [[t('evaluationAccuracy'),percent(ev.accuracy)],[t('macroF1'),percent(ev.macro_f1)],[t('evaluationLoss'),num(ev.loss,4)],[t('images'),num(ev.images)]]){
    const card=node('article',undefined,'metric-card');const number=node('bdi',value);number.dir='ltr';card.append(node('p',label),number);$('metrics').append(card);
  }
  $('model-select').replaceChildren();d.models.forEach(model=>{const option=node('option',model.name);option.value=model.name;option.selected=model.name===modelName;$('model-select').append(option)});
  $('model-select').disabled=d.models.length===1;
  drawChart('accuracy-chart',current.history,'accuracy',1);
  const maxLoss=Math.max(...d.models.flatMap(model=>model.history.flatMap(point=>[point.loss,point.val_loss])));
  drawChart('loss-chart',current.history,'loss',Math.ceil(maxLoss*2)/2||1);
  setHead('epoch-head',[t('epoch'),t('trainAccuracy'),t('valAccuracy'),t('trainLoss'),t('valLoss')]);$('epoch-body').replaceChildren();
  current.history.forEach(point=>$('epoch-body').append(row([num(point.epoch),percent(point.accuracy),percent(point.val_accuracy),num(point.loss,4),num(point.val_loss,4)])));
  $('comparison-section').hidden=!d.comparison.length;setHead('comparison-head',[t('model'),t('valAccuracy'),t('valLoss')]);$('comparison-body').replaceChildren();
  d.comparison.forEach(item=>{const tr=row([item.name+(item.name===ev.selected_model?' · '+t('selected'):''),percent(item.accuracy),num(item.loss,4)]);if(item.name===ev.selected_model)tr.className='selected-row';$('comparison-body').append(tr)});
  $('report-section').hidden=!d.classes.length;setHead('report-head',[t('category'),'Precision','Recall','F1',t('support')]);$('report-body').replaceChildren();
  d.classes.forEach(item=>{const tr=row([language==='he'?classHebrew[item.name]||item.name:item.name,percent(item.precision),percent(item.recall),percent(item['f1-score']),num(item.support)]);tr.firstChild.title=item.name;$('report-body').append(tr)});
  $('matrix-section').hidden=!d.matrix;
  if(d.matrix){$('matrix-image').src=d.matrix;$('matrix-image').alt=t('matrixAlt').replace('{project}',project==='food'?'FoodVision':'MaskVision');$('matrix-image').width=d.matrix_width||2160;$('matrix-image').height=d.matrix_height||1800;$('matrix-full').href=d.matrix;$('matrix-link').href=d.matrix;$('matrix-link').setAttribute('aria-label',t('fullImage'))}
  $('download-links').replaceChildren();d.downloads.forEach(file=>{const a=node('a',file.split('/').pop());a.href='/hub-static/results-files/'+file;a.download=file.split('/').pop();a.dir='ltr';$('download-links').append(a)});
  $('results-content').hidden=false;$('data-status').hidden=true;
}
function renderLanguage(){
  document.documentElement.lang=language;document.documentElement.dir=language==='he'?'rtl':'ltr';document.title=t('pageTitle');
  document.querySelectorAll('[data-i18n]').forEach(el=>{el.textContent=t(el.dataset.i18n)});
  document.querySelectorAll('[data-label]').forEach(el=>el.setAttribute('aria-label',t(el.dataset.label)));
  document.querySelectorAll('[data-language]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.language===language)));
  document.querySelectorAll('[data-project]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.project===project)));
  document.querySelectorAll('[data-home]').forEach(el=>{el.href='/home?lang='+language});
  document.querySelectorAll('[data-home-section]').forEach(el=>{el.href='/home?lang='+language+'#'+el.dataset.homeSection});
  document.querySelector('[aria-current="page"]').href='/results?lang='+language+'&project='+project;
  try{localStorage.setItem('vision-language',language)}catch{}
  if(results)render();else $('data-status').textContent=t(failed?'loadError':'loading');
}
document.querySelectorAll('[data-language]').forEach(button=>button.addEventListener('click',()=>{language=button.dataset.language;updateUrl();renderLanguage()}));
document.querySelectorAll('[data-project]').forEach(button=>button.addEventListener('click',()=>{project=button.dataset.project;modelName=null;updateUrl();renderLanguage()}));
$('model-select').addEventListener('change',()=>{modelName=$('model-select').value;if(results)render()});
renderLanguage();
fetch('/hub-static/results-data.json').then(response=>{if(!response.ok)throw new Error('resultsUnavailable');return response.json()}).then(data=>{results=data;render()}).catch(()=>{failed=true;$('results-content').hidden=true;$('data-status').hidden=false;$('data-status').textContent=t('loadError')});
