"""Read-only runtime probes injected into a page by the browser helper (only when a capture requests them)."""
from __future__ import annotations

# Optional read-only probe of running animations, expensive effects and layout shift (runs after the screenshot).
PROBE_JS = r'''async(waitMs)=>{let cls=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)cls+=e.value}).observe({type:'layout-shift',buffered:true})}catch(_){}
 await new Promise(r=>setTimeout(r,waitMs));const h=document.documentElement.scrollHeight;window.scrollTo(0,h/2);await new Promise(r=>setTimeout(r,Math.max(100,waitMs/2)));window.scrollTo(0,0);await new Promise(r=>setTimeout(r,100));
 const an=(document.getAnimations?document.getAnimations():[]).map(a=>{const t=a.effect&&a.effect.getTiming?a.effect.getTiming():{};return{type:a.constructor.name,name:a.animationName||a.transitionProperty||null,duration:typeof t.duration==='number'?Math.round(t.duration):null,iterations:t.iterations===Infinity?'infinite':t.iterations,easing:t.easing||null}});
 let backdrop=0,blur=0,willChange=0,transitionAll=0,n=0;for(const el of document.querySelectorAll('body *')){if(++n>5000)break;const s=getComputedStyle(el);if(s.backdropFilter&&s.backdropFilter!=='none')backdrop++;if(s.filter&&s.filter.includes('blur'))blur++;if(s.willChange&&s.willChange!=='auto')willChange++;if(s.transitionProperty.split(',').map(x=>x.trim()).includes('all')&&parseFloat(s.transitionDuration)>0)transitionAll++}
 return{schema_version:1,animations:{total:an.length,infinite:an.filter(a=>a.iterations==='infinite').length,items:an.slice(0,50)},effects:{backdrop_filter:backdrop,filter_blur:blur,will_change:willChange},transition_all_elements:transitionAll,elements_scanned:Math.min(n,5000),cumulative_layout_shift:Math.round(cls*1000)/1000,reduced_motion_active:matchMedia('(prefers-reduced-motion: reduce)').matches}}'''

__all__ = ["PROBE_JS"]
