const DATA = window.COURSE_DATA;
const appRoot = document.getElementById("app");
const PROGRESS_KEY = "pythonAcademyProgressV1";
let activeQuiz = null;

function readProgress(){
  try{return JSON.parse(localStorage.getItem(PROGRESS_KEY))||{lessons:[],scores:{}}}
  catch{return {lessons:[],scores:{}}}
}
function saveProgress(p){try{localStorage.setItem(PROGRESS_KEY,JSON.stringify(p))}catch{}}
function esc(v){return String(v).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function route(){return (location.hash||"#home").slice(1).split("/")}
function go(path){location.hash=path}
function progressStats(){const p=readProgress();return {lessons:p.lessons.length,scores:Object.keys(p.scores).length}}
function chapterScore(id){return readProgress().scores[id]||null}
function markLesson(id,topic){const p=readProgress();const key=id+"-"+topic;if(!p.lessons.includes(key))p.lessons.push(key);saveProgress(p)}
function header(title,sub,back="#home"){return `<a class="back" href="${back}">← Back</a><div class="section-head"><div><div class="eyebrow">Python Academy course</div><h2>${esc(title)}</h2><p class="muted">${esc(sub)}</p></div></div>`}
function home(){
 const stats=progressStats();
 const learner=readLearner();
 appRoot.innerHTML=`
 <section class="hero"><div class="hero-glow"></div><div class="eyebrow">Your practical Python learning path</div><h1>Learn Python.<br>Build what you imagine.</h1><p>Start with the basics, study clear examples, and check what you know with short chapter tests. Learn at your own pace.</p><a class="btn green" href="#chapter/1">Start learning →</a> <a class="btn secondary" href="#profile">Set learner name</a></section>
 <section class="stats"><div class="stat"><strong>50</strong><span>Python chapters</span></div><div class="stat"><strong>750</strong><span>Learning topics</span></div><div class="stat"><strong>6</strong><span>Questions per test</span></div><div class="stat"><strong>${stats.lessons}</strong><span>Lessons completed here</span></div></section>
 <div id="chapters" class="section-head"><div><div class="eyebrow">Course library</div><h2>Explore all chapters</h2><p class="muted">Choose a chapter to see its 15 learning topics.</p></div><input id="chapterSearch" type="search" placeholder="Search Python chapters…" aria-label="Search chapters"></div>
 <section class="card home-tools"><h3>Keep learning consistently</h3><p class="muted">Track lesson completion and test results on this browser. Your saved progress stays on this device.</p><div class="card-actions"><a class="btn secondary" href="#progress">View progress</a><a class="btn secondary" href="#about">About the Academy</a></div></section><div id="chapterGrid" class="grid">${chapterCards(DATA.chapters.map((name,i)=>({name,id:i+1})))}</div>`;
 const search=document.getElementById("chapterSearch");
 search.addEventListener("input",()=>{const q=search.value.toLowerCase();const items=DATA.chapters.map((name,i)=>({name,id:i+1})).filter(x=>x.name.toLowerCase().includes(q));document.getElementById("chapterGrid").innerHTML=items.length?chapterCards(items):'<div class="empty">No matching chapters.</div>'});
}
function chapterCards(items){return items.map(c=>{const s=chapterScore(c.id);return `<article class="card"><div class="chapter-no">Chapter ${c.id.toString().padStart(2,"0")}</div><h3>${esc(c.name)}</h3><p>15 lessons · 1 chapter test</p>${s?'<span class="pill">Best score: '+s.score+'/6</span>':'<span class="pill">Not tested yet</span>'}<div class="card-actions" style="margin-top:14px"><a class="btn" href="#chapter/${c.id}">Open chapter</a><a class="btn secondary" href="#test/${c.id}">Take test</a></div></article>`}).join("")}
function showChapter(id){
 const name=DATA.chapters[id-1];if(!name){go("home");return}
 const done=readProgress().lessons;
 appRoot.innerHTML=header("Chapter "+id+": "+name,"Choose a topic to study, then take the six-question test.")+`
 <div class="card"><div class="card-actions"><span class="pill">15 topics</span><span class="pill">${done.filter(x=>x.startsWith(id+"-")).length}/15 completed</span></div><div style="margin-top:15px" class="progress-track"><div class="progress-fill" style="width:${done.filter(x=>x.startsWith(id+"-")).length/15*100}%"></div></div><div style="margin-top:18px"><a class="btn green" href="#test/${id}">Take chapter test →</a></div></div>
 <div class="grid">${DATA.topics.map((t,i)=>{const key=id+"-"+(i+1);return `<article class="card"><div class="chapter-no">Topic ${String(i+1).padStart(2,"0")}</div><h3>${esc(t)}</h3><p>${done.includes(key)?"Completed":"Ready to learn"}</p><a class="btn" href="#lesson/${id}/${i+1}">${done.includes(key)?"Review lesson":"Start learning"} →</a></article>`}).join("")}</div>`;
}
function showLesson(id,topic){
 const name=DATA.chapters[id-1],title=DATA.topics[topic-1],example=DATA.examples[(topic-1)%DATA.examples.length];
 if(!name||!title){go("home");return}
 markLesson(id,topic);
 const explanation="This lesson introduces "+title.toLowerCase()+" while studying "+name+". Read the explanation, study the code example and expected output, then try the exercise yourself.";
 const exercise="Write your own Python program related to "+name+" and "+title.toLowerCase()+".";
 appRoot.innerHTML=header("Chapter "+id+": "+name,"Topic "+topic+" of 15 · "+title,"#chapter/"+id)+`
 <div class="lesson-panel"><span class="pill">LESSON ${topic} / 15</span><h2>${esc(title)}</h2><p>${esc(explanation)}</p></div>
 <div class="lesson-panel"><h2>Python code example</h2><pre class="code">${esc(example[0])}</pre><h3>Expected output</h3><div class="output">${esc(example[1])}</div></div>
 <div class="lesson-panel"><h2>Practice exercise</h2><p>${esc(exercise)}</p><p class="muted">Try writing the program in your Python editor, then compare your result with the example above.</p></div>
 <div class="lesson-nav"><a class="btn secondary" href="#chapter/${id}">← All topics</a>${topic<15?`<a class="btn green" href="#lesson/${id}/${topic+1}">Next topic →</a>`:`<a class="btn green" href="#test/${id}">Finish chapter & take test →</a>`}</div>`;
}
function shuffle(a){const x=[...a];for(let i=x.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[x[i],x[j]]=[x[j],x[i]]}return x}
function makeQuestions(id){
 const name=DATA.chapters[id-1],f=DATA.quizFacts[id-1];if(!name||!f)return [];
 const [concept,rule,example,expected,misconception,application]=f;
 const items=[
  {question:"Which statement best describes "+name+"?",correct:concept,wrong:["It is a feature used only to change the colour of the editor.","It is a command that shuts down the Python interpreter.","It is unrelated to writing or running Python programs."],explanation:concept},
  {question:"Which rule or syntax is associated with "+name+"?",correct:rule,wrong:["Python requires every statement to end with two semicolons.","Python uses HTML tags to define all program statements.","Python syntax is written only inside quotation marks."],explanation:rule},
  {question:"What is the output of this "+name+" example?\n"+example,correct:expected,wrong:["The program always prints None.","The program always produces a SyntaxError.","The program produces no output in every case."],explanation:"The example produces: "+expected},
  {question:"Which option is a correct fact about "+name+"?",correct:rule,wrong:["Python code never uses indentation.","Variable names must always contain spaces.","The print function is used to receive keyboard input."],explanation:rule},
  {question:"Which statement is a common misconception about "+name+"?",correct:misconception,wrong:["Python programs can use variables to refer to values.","Python code is executed according to its syntax rules.","Clear code examples can help explain a programming concept."],explanation:"This is incorrect: "+misconception},
  {question:"Which is a practical application of "+name+"?",correct:application,wrong:["Making a computer monitor physically larger.","Changing the electrical power supply of a keyboard.","Replacing the computer's operating system automatically."],explanation:application}
 ];
 return items.map(q=>{const options=shuffle([...q.wrong,q.correct]);return {...q,options,answer:options.indexOf(q.correct)}});
}
function showTest(id){
 const name=DATA.chapters[id-1];if(!name){go("home");return}
 activeQuiz=makeQuestions(id);
 appRoot.innerHTML=header("Chapter "+id+" test",name+" · Six questions · One mark per correct answer.","#chapter/"+id)+`
 <div class="card"><span class="pill">6 QUESTIONS</span><h3>Check your understanding</h3><p class="muted">Choose one answer for every question. Your result and answer explanations will appear after submission.</p><p class="muted">0–2: Learn Again · 3–4: Good · 5–6: Excellent</p></div>
 <form id="quizForm">${activeQuiz.map((q,i)=>`<section class="question"><h3>Question ${i+1} of 6</h3><p>${esc(q.question).replace(/\n/g,"<br>")}</p>${q.options.map((o,j)=>`<label class="option"><input type="radio" name="q${i}" value="${j}" required><span>${esc(o).replace(/\n/g,"<br>")}</span></label>`).join("")}</section>`).join("")}
 <button class="btn green full" type="submit">Submit answers & check my test</button></form>`;
 document.getElementById("quizForm").addEventListener("submit",e=>{e.preventDefault();const fd=new FormData(e.currentTarget);const review=activeQuiz.map((q,i)=>{const selected=Number(fd.get("q"+i));return {question:q.question,selected:q.options[selected],correct:q.options[q.answer],isCorrect:selected===q.answer,explanation:q.explanation}});const score=review.filter(x=>x.isCorrect).length;const p=readProgress();const old=p.scores[id];p.scores[id]={score:Math.max(score,old?.score??0),latest:score,attempts:(old?.attempts??0)+1};saveProgress(p);try{sessionStorage.setItem("pythonAcademyLastResult",JSON.stringify({id,name,score,review}))}catch{}go("result/"+id)});
}
function showResult(id){
 let result=null;try{result=JSON.parse(sessionStorage.getItem("pythonAcademyLastResult"))}catch{}
 if(!result||result.id!==id){appRoot.innerHTML=header("Test result","No recent test result was found.","#chapter/"+id)+'<div class="card"><p>Take the chapter test to see your result.</p><a class="btn" href="#test/'+id+'">Start test</a></div>';return}
 const score=result.score,level=score<=2?["Learn Again","learn","Review the lessons and try the test again."]:score<=4?["Good","good","Review the incorrect answers and strengthen the basics."]:["Excellent","excellent","You answered almost all questions correctly. Keep practising!"];
 appRoot.innerHTML=header("Your test result","Chapter "+id+": "+result.name,"#chapter/"+id)+`
 <div class="card"><div class="result-score">${score} / 6</div><div class="result-label ${level[1]}">${level[0]}</div><p>${level[2]}</p><p class="muted">${Math.round(score/6*100)}% correct · ${6-score} incorrect</p><div class="card-actions"><a class="btn" href="#test/${id}">Try again</a><a class="btn secondary" href="#chapter/${id}">Review chapter</a></div></div>
 <div class="section-head"><div><h2>Answer review</h2><p class="muted">Read the explanation for every question.</p></div></div>
 <div class="card">${result.review.map((r,i)=>`<div class="review-item"><strong>Question ${i+1}: ${esc(r.question).replace(/\n/g,"<br>")}</strong><p class="${r.isCorrect?"correct":"incorrect"}"><b>${r.isCorrect?"Correct":"Incorrect"}</b> · Your answer: ${esc(r.selected)}</p><p>Correct answer: <b>${esc(r.correct)}</b></p><p class="muted">Explanation: ${esc(r.explanation)}</p></div>`).join("")}</div>`;
}
function showProgress(){
 const p=readProgress(),scores=Object.entries(p.scores).sort((a,b)=>Number(a[0])-Number(b[0]));
 appRoot.innerHTML=header("My learning progress","Your completed lessons and best chapter test scores are saved in this browser.")+`
 <div class="stats"><div class="stat"><strong>${p.lessons.length}</strong><span>Lessons completed</span></div><div class="stat"><strong>${scores.length}/50</strong><span>Chapters tested</span></div><div class="stat"><strong>${scores.reduce((n,x)=>n+x[1].attempts,0)}</strong><span>Test attempts</span></div><div class="stat"><strong>${scores.length?Math.round(scores.reduce((n,x)=>n+x[1].score,0)/scores.length*100/6):0}%</strong><span>Average best score</span></div></div>
 <div class="card"><h3>Chapter scores</h3>${scores.length?scores.map(([id,s])=>`<div class="review-item"><div style="display:flex;justify-content:space-between;gap:10px"><b>Chapter ${id}: ${esc(DATA.chapters[Number(id)-1])}</b><strong>${s.score}/6</strong></div><div class="progress-track"><div class="progress-fill" style="width:${s.score/6*100}%"></div></div><small class="muted">Latest: ${s.latest}/6 · Attempts: ${s.attempts}</small></div>`).join(""):'<p class="muted">No tests completed yet. Start with Chapter 1.</p>'}</div>
 <button class="btn secondary" id="resetProgress" type="button">Reset saved progress</button>`;
 document.getElementById("resetProgress").addEventListener("click",()=>{if(confirm("Clear all saved lesson and test progress from this browser?")){localStorage.removeItem(PROGRESS_KEY);showProgress()}});
}
const LEARNER_KEY = "pythonAcademyLearnerV1";
function readLearner(){try{return JSON.parse(localStorage.getItem(LEARNER_KEY))||{name:""}}catch{return {name:""}}}
function showProfile(){
 const learner=readLearner();
 appRoot.innerHTML=header("Student profile","A private nickname stored only in this browser. This is not a secure online account.")+`
 <div class="card profile-card"><span class="pill">LOCAL PROFILE</span><h3>Welcome to your learning space</h3><p class="muted">Choose a nickname to personalize this browser. Do not enter a password, phone number, address, or other private information. Your progress remains on this device and is not synced to other devices.</p>
 <form id="profileForm"><label for="learnerName">Nickname</label><input id="learnerName" maxlength="24" value="${esc(learner.name)}" placeholder="e.g. PythonLearner"><button class="btn green" type="submit">Save nickname</button></form><p id="profileMessage" class="muted" aria-live="polite"></p></div>`;
 document.getElementById("profileForm").addEventListener("submit",e=>{e.preventDefault();const name=document.getElementById("learnerName").value.trim();if(name.length>24)return;try{localStorage.setItem(LEARNER_KEY,JSON.stringify({name}));document.getElementById("profileMessage").textContent=name?"Nickname saved on this device.":"Nickname cleared."; }catch{document.getElementById("profileMessage").textContent="Your browser could not save this nickname."}});
}
function showAbout(){
 appRoot.innerHTML=header("About Python Academy","A free, self-paced introduction to Python programming.")+`
 <section class="hero about-hero"><div class="eyebrow">Our purpose</div><h1>Learn. Practise. Improve.</h1><p>Python Academy is designed to help beginners explore programming through structured chapters, short lessons, code examples, practice tasks, and chapter quizzes.</p><a class="btn green" href="#chapter/1">Begin learning →</a></section>
 <div class="grid about-grid"><article class="card"><h3>Structured learning</h3><p>50 chapters with 15 topics each, covering Python fundamentals.</p></article><article class="card"><h3>Practice and assessment</h3><p>Each chapter includes a six-question test with automatic checking and answer explanations.</p></article><article class="card"><h3>Learn at your pace</h3><p>Lesson completion and test scores are stored locally in your browser.</p></article></div>
 <div class="card"><h3>Important information</h3><p class="muted">This GitHub Pages version is a static website. It does not have secure online accounts or a shared student database. Progress is saved only in the current browser on the current device.</p></div>`;
}
function render(){
 const r=route(),page=r[0];
 if(page==="chapter")showChapter(Number(r[1]));
 else if(page==="lesson")showLesson(Number(r[1]),Number(r[2]));
 else if(page==="test")showTest(Number(r[1]));
 else if(page==="result")showResult(Number(r[1]));
 else if(page==="chapters"){home();document.getElementById("chapters")?.scrollIntoView({behavior:"smooth"})}
 else if(page==="progress")showProgress();
 else if(page==="profile")showProfile();
 else if(page==="about")showAbout();
 else home();
 window.scrollTo(0,0);
}
window.addEventListener("hashchange",render);
document.getElementById("chaptersNav").addEventListener("click",e=>{if(route()[0]==="home"){e.preventDefault();document.getElementById("chapters")?.scrollIntoView({behavior:"smooth"})}});
render();
