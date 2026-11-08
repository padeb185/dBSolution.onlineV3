"""Régénère carscosts_app/lib/l10n/traductions.dart à partir des textes t('…') du code et de trad_app.py."""
import json, re, glob, sys, os
ici=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(ici,'_trad_app.py'),encoding='utf-8').read())
lib=sys.argv[1]
lit = r"'((?:[^'\\]|\\.)*)'"
pat = re.compile(r"\bt\(\s*(" + lit + r"(?:\s*" + lit + r")*)")
cles=[]
for f in sorted(glob.glob(lib+'/**/*.dart', recursive=True)):
    if 'traductions.dart' in f: continue
    for m in pat.finditer(open(f,encoding='utf-8').read()):
        k=''.join(re.findall(lit, m.group(1))).replace("\\'","'").replace('\\$','$')
        if k not in cles: cles.append(k)
manq=[k for k in cles if k not in T]
if manq: sys.exit('Sans traduction : %r' % manq)
for k in cles:
    ph=set(re.findall(r'\{\w+\}',k))
    for x in T[k]:
        assert set(re.findall(r'\{\w+\}',x))==ph,(k,x)
langs=['nl','en','de','es','it','el']
esc=lambda s: s.replace('\\','\\\\').replace("'","\\'").replace('$','\\$')
out=["// Traductions de l'interface (clé = texte français). Fichier généré : modifier la table de traduction,",
     "// pas ce fichier à la main. Le français est la langue source (pas de table).",
     "const traductions = <String, Map<String, String>>{"]
for i,l in enumerate(langs):
    out.append(f"  '{l}': {{")
    out += [f"    '{esc(k)}': '{esc(T[k][i])}'," for k in cles]
    out.append("  },")
out.append("};")
open(os.path.join(lib,'l10n','traductions.dart'),'w',encoding='utf-8').write("\n".join(out)+"\n")
print(len(cles), 'textes traduits')
