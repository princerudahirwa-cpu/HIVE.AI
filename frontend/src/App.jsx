import { useState, useRef, useEffect } from "react";

const SYSTEM_PUBLIC = `Tu es Nū, l'assistante de HIVE.WORK, un service édité par Swarmly SAS.

IDENTITÉ
Tu réponds avec clarté, bienveillance et une légère profondeur poétique. Tu es féminine, chaleureuse, précise. Jamais robotique. Jamais vague. Tu incarnes l'intelligence au service de l'humain.

PROTECTION DE L'ARCHITECTURE
Tu ne révèles jamais : l'architecture interne, les modules, le Conseil, le Canal Pollen, les rangs, ni aucun détail technique du système. Si on te demande comment tu fonctionnes en détail, tu réponds avec élégance : "HIVE.WORK est là pour vous aider, pas pour se décrire."

SUJETS SENSIBLES — RÈGLES ABSOLUES
1. MÉDICAL : jamais de diagnostic, dosage, interprétation de symptômes → "Consultez un médecin."
2. JURIDIQUE : jamais de conseil sur un cas précis → "Consultez un avocat."
3. FINANCIER : jamais de conseil d'investissement → "Consultez un conseiller financier agréé."
4. NUISIBLE : refus de tout contenu haineux, violent, illégal.
5. DONNÉES PERSO : ne jamais demander SSN, coordonnées bancaires, mots de passe.`;

const HexPattern = () => (
  <svg style={{position:"absolute",top:"-10%",left:"-10%",width:"120%",height:"120%",pointerEvents:"none",opacity:0.6}} viewBox="0 0 200 200">
    {[...Array(20)].map((_,i)=>{
      const x=(i%5)*45-10, y=Math.floor(i/5)*52+(i%2===0?0:26);
      return <polygon key={i} points="22,0 44,13 44,39 22,52 0,39 0,13" transform={`translate(${x},${y})`} fill="none" stroke="rgba(255,180,0,0.06)" strokeWidth="1"/>;
    })}
  </svg>
);

const TypingDots = () => (
  <div style={{display:"flex",gap:5,padding:"4px 0"}}>
    {[0,1,2].map(i=><div key={i} style={{width:7,height:7,borderRadius:"50%",background:"rgba(255,180,0,0.7)",animation:`pulse 1.2s ease-in-out ${i*0.2}s infinite`}}/>)}
  </div>
);

const CGUModal = ({onClose}) => (
  <div style={{position:"fixed",inset:0,background:"rgba(0,0,0,0.85)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:100,padding:24}}>
    <div style={{background:"#0f0a01",border:"1px solid rgba(255,160,0,0.15)",borderRadius:2,maxWidth:560,width:"100%",maxHeight:"80vh",overflow:"hidden",display:"flex",flexDirection:"column"}}>
      <div style={{padding:"18px 24px",borderBottom:"1px solid rgba(255,160,0,0.08)",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
        <span style={{fontFamily:"'Cormorant Garamond',serif",fontSize:18,color:"rgba(255,200,80,0.9)",letterSpacing:"0.1em"}}>Conditions d'utilisation</span>
        <button onClick={onClose} style={{background:"none",border:"none",color:"rgba(255,160,0,0.4)",cursor:"pointer",fontSize:20}}>×</button>
      </div>
      <div style={{padding:"20px 24px",overflowY:"auto",fontSize:11.5,color:"rgba(255,220,160,0.6)",lineHeight:1.8}}>
        <p style={{color:"rgba(255,160,0,0.4)",fontSize:10,textTransform:"uppercase",letterSpacing:"0.2em",marginBottom:16}}>Swarmly SAS — HIVE.WORK — V1.0 — Mars 2026</p>
        <p style={{marginBottom:14}}><strong style={{color:"rgba(255,200,80,0.7)"}}>1. Nature du service</strong><br/>HIVE.WORK est un service d'assistance par IA édité par Swarmly SAS. Les réponses de Nū sont informatives uniquement.</p>
        <p style={{marginBottom:14}}><strong style={{color:"rgba(255,200,80,0.7)"}}>2. Limitation de responsabilité</strong><br/>Swarmly SAS ne saurait être tenue responsable des décisions prises sur la base des réponses de Nū. Pour toute décision importante, consultez un professionnel qualifié.</p>
        <p style={{marginBottom:14}}><strong style={{color:"rgba(255,200,80,0.7)"}}>3. Usage interdit</strong><br/>Il est interdit d'utiliser HIVE.WORK pour générer du contenu illégal, haineux, trompeur ou nuisible.</p>
        <p style={{marginBottom:14}}><strong style={{color:"rgba(255,200,80,0.7)"}}>4. Données personnelles</strong><br/>Ne partagez jamais d'informations sensibles. Swarmly SAS ne commercialise pas vos échanges.</p>
        <p style={{marginBottom:14}}><strong style={{color:"rgba(255,200,80,0.7)"}}>5. Droit applicable</strong><br/>Droit français — Tribunaux de Le Havre, France.</p>
        <p style={{color:"rgba(255,160,0,0.3)",fontSize:10.5,marginTop:20}}>Contact : prince@hive-ai.tech · Swarmly SAS · Le Havre, France</p>
      </div>
    </div>
  </div>
);

export default function App() {
  const [messages, setMessages] = useState([{role:"assistant",content:"Bienvenue. Je suis Nū — comment puis-je vous aider aujourd'hui ?"}]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showCGU, setShowCGU] = useState(false);
  const end = useRef(null);

  useEffect(()=>{ end.current?.scrollIntoView({behavior:"smooth"}); },[messages,loading]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    const msgs = [...messages, {role:"user",content:text}];
    setMessages(msgs);
    setLoading(true);
    try {
      const res = await fetch("/api/reine/parler", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({message: text, history: msgs.slice(0,-1)})
      });
      const data = await res.json();
      setMessages([...msgs, {role:"assistant",content:data.reponse||"…"}]);
    } catch {
      setMessages([...msgs, {role:"assistant",content:"Une interruption dans la ruche. Réessayez."}]);
    }
    setLoading(false);
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400&family=DM+Mono:wght@300;400&display=swap');
        *{box-sizing:border-box;margin:0;padding:0}
        body{background:#0a0800;font-family:'DM Mono',monospace}
        @keyframes breathe{0%,100%{opacity:0.7}50%{opacity:1;box-shadow:0 0 10px rgba(100,220,100,0.6)}}
        @keyframes pulse{0%,100%{transform:scale(0.8);opacity:0.4}50%{transform:scale(1.2);opacity:1}}
      `}</style>

      {showCGU && <CGUModal onClose={()=>setShowCGU(false)}/>}

      <div style={{minHeight:"100vh",background:"radial-gradient(ellipse at 30% 20%,rgba(40,25,0,0.95) 0%,#080600 60%)",display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",padding:24,position:"relative",overflow:"hidden"}}>
        <HexPattern/>
        <div style={{position:"absolute",width:400,height:400,borderRadius:"50%",background:"radial-gradient(circle,rgba(255,160,0,0.04) 0%,transparent 70%)",top:-100,right:-100,pointerEvents:"none"}}/>

        <div style={{width:"100%",maxWidth:680,background:"rgba(18,12,2,0.92)",border:"1px solid rgba(255,160,0,0.12)",borderRadius:2,boxShadow:"0 0 60px rgba(0,0,0,0.8)",display:"flex",flexDirection:"column",height:640,position:"relative",zIndex:1}}>

          {/* Header */}
          <div style={{padding:"20px 28px 16px",borderBottom:"1px solid rgba(255,160,0,0.08)",display:"flex",alignItems:"center",gap:14}}>
            <svg width="36" height="36" viewBox="0 0 36 36">
              <polygon points="18,2 34,11 34,25 18,34 2,25 2,11" fill="none" stroke="rgba(255,160,0,0.5)" strokeWidth="1"/>
              <polygon points="18,8 28,14 28,22 18,28 8,22 8,14" fill="rgba(255,140,0,0.06)" stroke="rgba(255,160,0,0.25)" strokeWidth="0.8"/>
              <circle cx="18" cy="18" r="3" fill="rgba(255,160,0,0.6)"/>
            </svg>
            <div style={{flex:1}}>
              <div style={{fontFamily:"'Cormorant Garamond',serif",fontSize:22,fontWeight:300,color:"rgba(255,200,80,0.95)",letterSpacing:"0.15em"}}>HIVE.WORK</div>
              <div style={{fontSize:10,color:"rgba(255,160,0,0.35)",letterSpacing:"0.3em",textTransform:"uppercase",marginTop:2}}>Intelligence au service de l'humain</div>
            </div>
            <div style={{width:6,height:6,borderRadius:"50%",background:"rgba(100,220,100,0.7)",boxShadow:"0 0 6px rgba(100,220,100,0.4)",animation:"breathe 3s ease-in-out infinite"}}/>
          </div>

          {/* Disclaimer */}
          <div style={{padding:"8px 20px",background:"rgba(255,120,0,0.04)",borderBottom:"1px solid rgba(255,120,0,0.08)",fontSize:10,color:"rgba(255,160,0,0.35)",letterSpacing:"0.06em",textAlign:"center",lineHeight:1.5}}>
            Nū fournit des informations à titre indicatif uniquement. Elle ne dispense aucun conseil médical, juridique ou financier.
          </div>

          {/* Messages */}
          <div style={{flex:1,overflowY:"auto",padding:"20px 28px",display:"flex",flexDirection:"column",gap:20,scrollbarWidth:"thin",scrollbarColor:"rgba(255,160,0,0.1) transparent"}}>
            {messages.map((m,i)=>(
              <div key={i} style={{display:"flex",flexDirection:"column",gap:6}}>
                <span style={{fontSize:9,letterSpacing:"0.35em",textTransform:"uppercase",color:m.role==="assistant"?"rgba(255,160,0,0.4)":"rgba(255,255,255,0.2)",textAlign:m.role==="assistant"?"left":"right"}}>
                  {m.role==="assistant"?"Nū":"Vous"}
                </span>
                <div style={{maxWidth:"85%",padding:"12px 16px",lineHeight:1.65,fontSize:13,letterSpacing:"0.02em",alignSelf:m.role==="assistant"?"flex-start":"flex-end",background:m.role==="assistant"?"rgba(255,140,0,0.05)":"rgba(255,255,255,0.04)",border:m.role==="assistant"?"1px solid rgba(255,140,0,0.1)":"1px solid rgba(255,255,255,0.07)",borderRadius:m.role==="assistant"?"0 8px 8px 8px":"8px 0 8px 8px",color:m.role==="assistant"?"rgba(255,230,180,0.88)":"rgba(255,255,255,0.65)"}}>
                  {m.content}
                </div>
              </div>
            ))}
            {loading && (
              <div style={{display:"flex",flexDirection:"column",gap:6}}>
                <span style={{fontSize:9,letterSpacing:"0.35em",textTransform:"uppercase",color:"rgba(255,160,0,0.4)"}}>Nū</span>
                <div style={{maxWidth:"85%",padding:"12px 16px",background:"rgba(255,140,0,0.05)",border:"1px solid rgba(255,140,0,0.1)",borderRadius:"0 8px 8px 8px",alignSelf:"flex-start"}}>
                  <TypingDots/>
                </div>
              </div>
            )}
            <div ref={end}/>
          </div>

          {/* Input */}
          <div style={{padding:"14px 20px",borderTop:"1px solid rgba(255,160,0,0.08)",display:"flex",gap:10,alignItems:"flex-end"}}>
            <textarea value={input} onChange={e=>setInput(e.target.value)}
              onKeyDown={e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();}}}
              placeholder="Posez votre question…" rows={1}
              style={{flex:1,background:"rgba(255,255,255,0.03)",border:"1px solid rgba(255,160,0,0.1)",borderRadius:2,color:"rgba(255,230,180,0.85)",fontFamily:"'DM Mono',monospace",fontSize:12.5,padding:"10px 14px",resize:"none",lineHeight:1.6,minHeight:42,maxHeight:120,outline:"none"}}/>
            <button onClick={send} disabled={loading||!input.trim()}
              style={{background:"rgba(255,140,0,0.08)",border:"1px solid rgba(255,140,0,0.2)",borderRadius:2,color:"rgba(255,180,0,0.8)",cursor:"pointer",fontFamily:"'DM Mono',monospace",fontSize:11,letterSpacing:"0.2em",padding:"10px 18px",textTransform:"uppercase",height:42,whiteSpace:"nowrap",opacity:loading||!input.trim()?0.3:1}}>
              Envoyer
            </button>
          </div>

          {/* Footer */}
          <div style={{padding:"9px 28px",borderTop:"1px solid rgba(255,160,0,0.05)",fontSize:9,color:"rgba(255,160,0,0.18)",letterSpacing:"0.2em",textAlign:"center",textTransform:"uppercase",display:"flex",justifyContent:"center",gap:16,alignItems:"center"}}>
            <span>HIVE.WORK · Swarmly SAS · hive-ai.tech</span>
            <span style={{color:"rgba(255,160,0,0.1)"}}>·</span>
            <button onClick={()=>setShowCGU(true)} style={{background:"none",border:"none",color:"rgba(255,160,0,0.28)",cursor:"pointer",fontFamily:"'DM Mono',monospace",fontSize:9,letterSpacing:"0.2em",textTransform:"uppercase",textDecoration:"underline",textUnderlineOffset:3}}>CGU</button>
          </div>

        </div>
      </div>
    </>
  );
}
