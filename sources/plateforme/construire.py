import sys
import os, base64
ICI=os.path.dirname(os.path.abspath(__file__))
RACINE=os.path.dirname(os.path.dirname(ICI))
# le GIF est intégré au tutoriel : une image servie ailleurs ne s'affiche pas toujours dans l'éditeur
gif = 'data:image/gif;base64,' + base64.b64encode(open(os.path.join(ICI, 'plateforme.gif'), 'rb').read()).decode()
s=open(os.path.join(ICI,'tuto-source.md')).read()
s=s.replace('@@JRES@@',open(os.path.join(ICI,'niveau.jres')).read()).replace('@@HEROS@@',open(os.path.join(ICI,'heros.txt')).read().rstrip('\n')).replace('@@GIF@@',gif)
open(os.path.join(RACINE,'plateforme.md'),'w').write(s)
print('ok', s.count('## '))
