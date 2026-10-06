const root=document.getElementById(ID);
const tl=gsap.timeline({paused:true});
const q=(s)=>root.querySelector(s);
tl.fromTo(q('.title'),{opacity:0,y:12},{opacity:1,y:0,duration:.48,ease:'power2.out'},0);
tl.fromTo(q('.progress'),{scaleX:0},{scaleX:1,duration:DUR,ease:'none'},0);
root.querySelectorAll('[data-at]').forEach((el)=>{
  const at=Number(el.dataset.at);
  const type=el.dataset.motion||'reveal';
  if(type==='draw'){
    const len=el.getTotalLength();
    tl.fromTo(el,{strokeDasharray:len,strokeDashoffset:len,opacity:1},
      {strokeDashoffset:0,duration:Math.min(2.2,Number(el.dataset.drawDuration||1.15)),ease:'power1.inOut'},at);
  }else if(type==='bar'){
    tl.fromTo(el,{scaleX:0,transformOrigin:'0% 50%',opacity:1},{scaleX:1,duration:1.2,ease:'power2.out'},at);
  }else if(type==='focus'){
    tl.fromTo(el,{opacity:.38},{opacity:1,duration:.45,ease:'power1.out'},at);
  }else{
    tl.fromTo(el,{opacity:0,y:type==='rise'?18:0,x:type==='slide'?24:0},
      {opacity:1,y:0,x:0,duration:.5,ease:type==='slide'?'power3.out':'power1.out'},at);
  }
  if(el.dataset.until){
    tl.to(el,{opacity:0,duration:.22,ease:'power1.in'},Math.max(at+.5,Number(el.dataset.until)-.24));
  }
});
root.querySelectorAll('[data-emphasis-at]').forEach((el)=>{
  const at=Number(el.dataset.emphasisAt);
  tl.fromTo(el,{scale:1},{scale:1.035,duration:.4,transformOrigin:'50% 50%',ease:'power2.out'},at);
  tl.to(el,{scale:1,duration:.7,ease:'power2.inOut'},at+.5);
});
root.querySelectorAll('[data-camera]').forEach((el)=>{
  const move=JSON.parse(el.dataset.camera);
  tl.fromTo(el,{x:0,y:0,scale:1,transformOrigin:'0 0'},
    {x:move.x,y:move.y,scale:move.scale,duration:move.duration||4,ease:'power2.inOut'},move.at||1);
});
root.querySelectorAll('[data-move-at]').forEach((el)=>{
  tl.fromTo(el,{x:0,y:0},{x:Number(el.dataset.moveX||0),y:Number(el.dataset.moveY||0),
    duration:2.1,ease:'power2.inOut'},Number(el.dataset.moveAt));
});
