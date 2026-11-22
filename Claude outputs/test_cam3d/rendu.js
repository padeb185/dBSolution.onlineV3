// Mini-DOM pour sérialiser le SVG produit par camembert3d.js
function Node(tag){this.tag=tag;this.attrs={};this.children=[];this.style={};this.textContent="";this.innerHTML="";}
Node.prototype.setAttribute=function(k,v){this.attrs[k]=v};
Node.prototype.appendChild=function(c){this.children.push(c);return c};
Node.prototype.addEventListener=function(){};
Node.prototype.getBoundingClientRect=function(){return{left:0,top:0}};
Node.prototype.ser=function(){
  if(!this.tag.startsWith("svg:"))return this.children.map(c=>c.ser?c.ser():"").join("");
  const t=this.tag.slice(4);let st=Object.keys(this.style).length?` style="${Object.entries(this.style).map(([k,v])=>k.replace(/[A-Z]/g,m=>'-'+m.toLowerCase())+':'+v).join(';')}"`:"";
  return `<${t}${t==="svg"?' xmlns="http://www.w3.org/2000/svg"':''} ${Object.entries(this.attrs).map(([k,v])=>`${k}="${v}"`).join(" ")}${st}>${this.textContent}${this.children.map(c=>c.ser()).join("")}</${t}>`;};
const document={documentElement:{lang:"fr-BE"},createElementNS:(ns,t)=>new Node("svg:"+t),createElement:t=>new Node(t)};
const window={};
eval(require("fs").readFileSync(process.argv[2],"utf8"));
const out=[];
for(const parts of [[{label:"Acquisition",valeur:42000},{label:"Énergie",valeur:9800},{label:"Maintenances",valeur:6100},{label:"Coûts annuels",valeur:3900}],
                    [{label:"Pièces",valeur:18500},{label:"Main-d'œuvre",valeur:22100},{label:"Autres",valeur:900}]]){
  const c=new Node("div");window.Camembert3D.dessiner(c,parts,{});
  const svg=c.children[0].children[0]; out.push(svg.ser());
}
require("fs").writeFileSync("a.svg",out[0]);require("fs").writeFileSync("b.svg",out[1]);console.log("ok");
