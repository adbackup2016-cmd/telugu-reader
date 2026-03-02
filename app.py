from flask import Flask, request, Response, render_template_string
from gtts import gTTS
import io

app = Flask(__name__)

HTML = r"""<!DOCTYPE html>
<html lang="te">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>తెలుగు పాఠకుడు</title>
<link href="https://fonts.googleapis.com/css2?family=Tiro+Telugu:ital@0;1&family=Cinzel:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{--gold:#D4A017;--cream:#FDF6E3;--muted:#8B6914;--bg:#0D0500;--card:#1E0E02;--border:#3D2410;--saffron:#FF6B35;--deep:#1A0A00}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--cream);font-family:'Tiro Telugu',serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:40px 20px}
  body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse at 20% 20%,rgba(212,160,23,.08),transparent 60%),radial-gradient(ellipse at 80% 80%,rgba(255,107,53,.06),transparent 60%);pointer-events:none}
  .header{text-align:center;margin-bottom:40px}
  .divider{display:flex;align-items:center;gap:16px;margin-bottom:12px;justify-content:center}
  .divider span{color:var(--gold);font-size:22px}
  .divider::before,.divider::after{content:'';flex:0 0 60px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent)}
  .title-te{font-size:clamp(2rem,5vw,3.2rem);color:var(--gold);letter-spacing:2px;text-shadow:0 0 40px rgba(212,160,23,.4)}
  .title-en{font-family:'Cinzel',serif;font-size:.85rem;color:var(--muted);letter-spacing:6px;text-transform:uppercase;margin-top:6px}
  .card{background:var(--card);border:1px solid var(--border);border-radius:4px;width:100%;max-width:760px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.6),inset 0 1px 0 rgba(212,160,23,.15)}
  .card-header{background:linear-gradient(135deg,#2A1200,#1A0A00);padding:16px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between}
  .card-header-label{font-family:'Cinzel',serif;font-size:.7rem;letter-spacing:4px;color:var(--muted);text-transform:uppercase}
  .char-count{font-size:.75rem;color:var(--muted);font-family:monospace}
  textarea{width:100%;min-height:220px;background:transparent;border:none;outline:none;resize:vertical;padding:24px;font-family:'Tiro Telugu',serif;font-size:1.4rem;line-height:2;color:var(--cream);caret-color:var(--gold)}
  textarea::placeholder{color:#4A2E10;font-size:1.2rem}
  .controls{padding:20px 24px;border-top:1px solid var(--border);background:rgba(0,0,0,.2)}
  .audio-wrap{margin-bottom:16px;display:none}
  .audio-wrap.visible{display:block}
  audio{width:100%;border-radius:2px}
  .btn-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
  .btn{flex:1;min-width:100px;padding:14px 20px;border:none;border-radius:2px;font-family:'Cinzel',serif;font-size:.75rem;letter-spacing:3px;text-transform:uppercase;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:8px}
  .btn-primary{background:linear-gradient(135deg,#C4740A,#D4A017);color:var(--deep);font-weight:600;box-shadow:0 4px 20px rgba(212,160,23,.3)}
  .btn-primary:hover:not(:disabled){background:linear-gradient(135deg,#D4A017,#E8B820);transform:translateY(-1px)}
  .btn-secondary{background:transparent;color:var(--muted);border:1px solid var(--border)}
  .btn-secondary:hover:not(:disabled){border-color:var(--gold);color:var(--gold)}
  .btn-stop{background:rgba(255,107,53,.1);color:var(--saffron);border:1px solid rgba(255,107,53,.3)}
  .btn-stop:hover:not(:disabled){background:rgba(255,107,53,.2)}
  .btn:disabled{opacity:.35;cursor:not-allowed}
  .status-bar{padding:10px 16px;border-radius:2px;font-size:.85rem;display:flex;align-items:center;gap:10px;transition:all .3s}
  .idle{background:rgba(255,255,255,.03);color:#5A3A1A}
  .loading{background:rgba(100,150,255,.08);color:#88aaff;border:1px solid rgba(100,150,255,.2)}
  .playing{background:rgba(212,160,23,.10);color:var(--gold);border:1px solid rgba(212,160,23,.2)}
  .error{background:rgba(255,60,60,.10);color:#ff6060;border:1px solid rgba(255,60,60,.2)}
  .wave{display:none;align-items:flex-end;gap:3px;height:20px}
  .wave.on{display:flex}
  .wave span{display:block;width:3px;background:var(--gold);border-radius:2px;animation:wv .8s ease-in-out infinite}
  .wave span:nth-child(1){animation-delay:0s}.wave span:nth-child(2){animation-delay:.15s}.wave span:nth-child(3){animation-delay:.3s}.wave span:nth-child(4){animation-delay:.15s}.wave span:nth-child(5){animation-delay:0s}
  @keyframes wv{0%,100%{height:4px}50%{height:18px}}
  .note{background:rgba(212,160,23,.05);border:1px solid rgba(212,160,23,.15);border-radius:2px;padding:12px 16px;font-size:.78rem;color:var(--muted);margin-top:14px;line-height:1.8}
  .note strong{color:var(--gold)}
  .samples{width:100%;max-width:760px;margin-top:24px}
  .samples-label{font-family:'Cinzel',serif;font-size:.65rem;letter-spacing:4px;color:var(--muted);text-transform:uppercase;margin-bottom:12px;text-align:center}
  .samples-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
  .sample-btn{background:var(--card);border:1px solid var(--border);color:var(--cream);padding:12px 16px;border-radius:2px;cursor:pointer;text-align:left;transition:all .2s;font-family:'Tiro Telugu',serif;font-size:1rem;line-height:1.5}
  .sample-btn .lbl{display:block;font-family:'Cinzel',serif;font-size:.55rem;letter-spacing:3px;color:var(--muted);margin-bottom:4px;text-transform:uppercase}
  .sample-btn:hover{border-color:var(--gold);background:rgba(212,160,23,.05);transform:translateY(-1px)}
  @media(max-width:500px){.btn-row{flex-direction:column}.btn{flex:none}}
</style>
</head>
<body>
<div class="header">
  <div class="divider"><span>✦</span></div>
  <div class="title-te">తెలుగు పాఠకుడు</div>
  <div class="title-en">Telugu Text Reader</div>
</div>
<div class="card">
  <div class="card-header">
    <span class="card-header-label">Input Text · ప్రవేశపెట్టండి</span>
    <span class="char-count" id="charCount">0 అక్షరాలు</span>
  </div>
  <textarea id="teluguText" placeholder="ఇక్కడ తెలుగు టెక్స్ట్ టైప్ చేయండి లేదా అతికించండి...&#10;Type or paste Telugu text here..." spellcheck="false"></textarea>
  <div class="controls">
    <div class="audio-wrap" id="audioWrap">
      <audio id="audioPlayer" controls></audio>
    </div>
    <div class="btn-row">
      <button class="btn btn-primary" id="btnRead" onclick="readText()">▶ చదవండి · Read</button>
      <button class="btn btn-stop" id="btnStop" onclick="stopAudio()" disabled>■ Stop</button>
      <button class="btn btn-secondary" onclick="clearText()">✕ Clear</button>
    </div>
    <div class="status-bar idle" id="statusBar">
      <div class="wave" id="wave"><span></span><span></span><span></span><span></span><span></span></div>
      <span id="statusMsg">తయారుగా ఉంది · Ready</span>
    </div>
    <div class="note">
      <strong>gTTS · Google Text-to-Speech</strong> · Genuine Telugu voice · Free to use ✓
    </div>
  </div>
</div>
<div class="samples">
  <div class="samples-label">✦ Sample Texts · నమూనా వచనాలు ✦</div>
  <div class="samples-grid">
    <button class="sample-btn" onclick="loadSample(0)"><span class="lbl">Poem · కవిత</span>తెలుగు భాష తేనె లాంటిది</button>
    <button class="sample-btn" onclick="loadSample(1)"><span class="lbl">Greeting · శుభాకాంక్షలు</span>నమస్కారం, మీరు ఎలా ఉన్నారు?</button>
    <button class="sample-btn" onclick="loadSample(2)"><span class="lbl">Proverb · సామెత</span>అన్నదాత సుఖీభవ</button>
    <button class="sample-btn" onclick="loadSample(3)"><span class="lbl">Scripture · వేదము</span>ఓం నమః శివాయ</button>
  </div>
</div>
<script>
const samples=[
  'తెలుగు భాష తేనె లాంటిది, మాటలు మల్లెల వాసన వంటిది. మన సంస్కృతి మహత్తరమైనది, మన భాషే మన గుర్తింపు.',
  'నమస్కారం! మీరు ఎలా ఉన్నారు? తెలుగు పాఠకుడు యాప్ కి స్వాగతం. మీ తెలుగు వచనాన్ని నేను చదువుతాను.',
  'అన్నదాత సుఖీభవ. తప్పు చేస్తే తప్పులేదు, తప్పని తెలుసుకుంటే తప్పులేదు. ఆలస్యం అమృతం విషం.',
  'ఓం నమః శివాయ. హరే రామ హరే రామ, రామ రామ హరే హరే. హరే కృష్ణ హరే కృష్ణ, కృష్ణ కృష్ణ హరే హరే.'
];
const player=document.getElementById('audioPlayer');
function setStatus(type,msg,wave=false){
  document.getElementById('statusBar').className='status-bar '+type;
  document.getElementById('statusMsg').textContent=msg;
  document.getElementById('wave').className='wave'+(wave?' on':'');
}
async function readText(){
  const text=document.getElementById('teluguText').value.trim();
  if(!text){setStatus('error','⚠ దయచేసి టెక్స్ట్ నమోదు చేయండి · Please enter text');return;}
  setStatus('loading','లోడ్ అవుతున్నది · Generating audio...',true);
  document.getElementById('btnRead').disabled=true;
  document.getElementById('btnStop').disabled=false;
  try{
    const resp=await fetch('/tts?text='+encodeURIComponent(text));
    if(!resp.ok){const e=await resp.text();throw new Error(e);}
    const blob=await resp.blob();
    const url=URL.createObjectURL(blob);
    player.src=url;
    document.getElementById('audioWrap').classList.add('visible');
    player.onplay=()=>setStatus('playing','చదువుతున్నాను · Playing...',true);
    player.onpause=()=>{if(!player.ended)setStatus('idle','⏸ నిలిపివేయబడింది · Paused');};
    player.onended=()=>{setStatus('idle','✓ పూర్తయింది · Finished');resetBtns();};
    await player.play();
  }catch(e){
    setStatus('error','⚠ '+e.message);
    resetBtns();
  }
}
function stopAudio(){
  player.pause();player.currentTime=0;
  setStatus('idle','■ ఆపబడింది · Stopped');
  resetBtns();
}
function resetBtns(){
  document.getElementById('btnRead').disabled=false;
  document.getElementById('btnStop').disabled=true;
  document.getElementById('wave').className='wave';
}
function clearText(){
  stopAudio();
  document.getElementById('teluguText').value='';
  document.getElementById('charCount').textContent='0 అక్షరాలు';
  document.getElementById('audioWrap').classList.remove('visible');
  setStatus('idle','తయారుగా ఉంది · Ready');
}
function loadSample(i){
  stopAudio();
  document.getElementById('teluguText').value=samples[i];
  document.getElementById('charCount').textContent=samples[i].length+' అక్షరాలు';
  setStatus('idle','నమూనా లోడ్ చేయబడింది · Sample loaded');
}
document.getElementById('teluguText').addEventListener('input',function(){
  document.getElementById('charCount').textContent=this.value.length+' అక్షరాలు';
});
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/tts')
def tts():
    text = request.args.get('text', '').strip()
    if not text:
        return Response('No text provided', status=400)
    if len(text) > 5000:
        return Response('Text too long (max 5000 chars)', status=400)
    try:
        tts = gTTS(text=text, lang='te', slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return Response(buf.read(), mimetype='audio/mpeg')
    except Exception as e:
        return Response(str(e), status=500)

if __name__ == '__main__':
    app.run(debug=False)
