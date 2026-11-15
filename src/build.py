"""Builds ../index.html from content*.txt inside the shared shell in src/shell/.  Run: python3 src/build.py
content format:
# Domain | sigil
## Concept | sigil
### Metaphor name | source key | one-line gloss      (a name already used in this domain reuses that entry)
- an everyday expression
"""
import collections, glob, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
SRC = {
    'MW': 'Lakoff & Johnson, Metaphors We Live By (1980; afterword 2003)',
    'WF': 'Lakoff, Women, Fire, and Dangerous Things (1987)',
    'MT': 'Lakoff & Turner, More Than Cool Reason (1989)',
    'ML': 'Lakoff, Espenson & Schwartz, Master Metaphor List (1991)',
    'MWar': 'Lakoff, “Metaphor and War” (1991)',
    'CT': 'Lakoff, “The Contemporary Theory of Metaphor” (1993)',
    'MP': 'Lakoff, Moral Politics (1996)',
    'PF': 'Lakoff & Johnson, Philosophy in the Flesh (1999)',
    'WM': 'Lakoff & Núñez, Where Mathematics Comes From (2000)',
    'CH': 'Chafetz, Masculine/Feminine or Human? (1978), on the gendering of English',
}
def curl(s):
    s = re.sub(r'(^|[\s(\[])"', r'\1“', s).replace('"', '”')
    return re.sub(r"(^|[\s(\[“])'(?=\w)", r'\1‘', s).replace("'", '’')
def sig(c): return ''.join(ch + ('︎' if 0x2190 <= ord(ch) <= 0x2bff else '') for ch in c)
P = []; D = C = M = None; idx = {}
for f in sorted(glob.glob(os.path.join(here, 'content*.txt'))):
    for ln, line in enumerate(open(f, encoding='utf-8'), 1):
        line = line.strip()
        if not line: continue
        if line.startswith('### '):
            parts = [x.strip() for x in line[4:].split('|')]
            name = parts[0]
            if name in idx:
                assert len(parts) == 1, f'{f}:{ln} duplicate metaphor {name}'
                C['t'].append(idx[name]); M = None; continue
            assert len(parts) == 3 and parts[1] in SRC, f'{f}:{ln}'
            M = {'t': name, 'p': curl(parts[2]) + ' — ' + SRC[parts[1]] + '.', 'k': []}
            idx[name] = len(D['t']); C['t'].append(idx[name]); D['t'].append(M); continue
        if line.startswith('## '):
            n, s = [x.strip() for x in line[3:].split('|')]
            C = {'n': n, 'i': sig(s), 't': []}; D['u'].append(C); continue
        if line.startswith('# '):
            n, s = [x.strip() for x in line[2:].split('|')]
            D = {'n': n, 'i': sig(s), 'u': [], 't': []}; P.append(D); idx = {}; continue
        assert line.startswith('- ') and M is not None, f'{f}:{ln}: {line}'
        e = curl(line[2:].strip())
        M['k'].append({'f': e, 'c': f'{e} ({M["t"].upper()})'})
# checks
allm = [t['t'] for d in P for t in d['t']]
dups = [m for m, c in collections.Counter(allm).items() if c > 1]
exprs = collections.Counter(k['f'] for d in P for t in d['t'] for k in t['k'])
print(len(P), 'domains,', sum(len(d['u']) for d in P), 'concepts,', len(allm), 'metaphors,', sum(exprs.values()), 'expressions')
print('metaphors in two domains:', dups)
print('repeated expressions:', [e for e, c in exprs.items() if c > 1])
print('thin:', [t['t'] for d in P for t in d['t'] if len(t['k']) < 4])
sys.path.insert(0, os.path.join(here, 'shell')); import shell
n = shell.build(P, os.path.join(here, '..', 'index.html'),
    title='Metaphors for…', lead='Metaphors for', key='mx',
    words=['domain', 'concept', 'metaphor', 'expression'],
    steps=['domain', 'concept', 'metaphor', 'expressions'], plurals={},
    foot='', theme='ink')
print(n, 'bytes')
