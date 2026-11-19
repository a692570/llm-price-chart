#!/usr/bin/env python3
"""Turn research/*.json into the compact lineage data embedded in index.html."""
import json, re, sys
R = 'data/sources/'
N = 23

def load(f):
    return json.load(open(R + f + '.json'))

def tier(f, prefix):
    for t in load(f)['tiers']:
        if (t.get('name') or t.get('tier')).startswith(prefix):
            return t['points']
    raise SystemExit('missing tier %s %s' % (f, prefix))

# ---------- label cleaners ----------
def paren_keep(raw):
    low = raw.lower()
    return ' (preview)' if 'preview' in low and 'qwen3-max' not in low and 'kimi' not in low else ''

def lab_anthropic(raw, i):
    s = raw.replace('Claude ', '')
    return re.sub(r'\s*\(.*\)', '', s)

def lab_openai(raw, i):
    return re.sub(r'\s*\(.*\)', '', raw)

def lab_google(raw, i):
    s = re.sub(r'\s*\(.*\)', '', raw)
    return s

def lab_xai(raw, i):
    s = raw
    m = re.match(r'grok-2-1212', s)
    if m: return 'Grok 2'
    s = re.sub(r'\s*\(.*\)', '', s)
    table = {'grok-3': 'Grok 3', 'grok-4': 'Grok 4', 'grok-4.20': 'Grok 4.20', 'grok-4.3': 'Grok 4.3', 'grok-4.5': 'Grok 4.5',
             'grok-4.6': 'Grok 4.6', 'grok-4.7': 'Grok 4.7', 'grok-3-mini': 'Grok 3 mini', 'grok-4-fast': 'Grok 4 Fast',
             'grok-4.1-fast': 'Grok 4.1 Fast', 'grok-code-fast-1': 'Grok Code Fast 1', 'grok-build-0.1': 'Grok Build 0.1'}
    return table[s]

def lab_mistral(raw, i):
    s = raw.replace('Mistral ', '')
    prev = ' (preview)' if 'public preview' in s else ''
    s = re.sub(r'\s*\(.*\)', '', s)
    s = s.replace('Medium 3 ', 'Medium 3')
    return s + prev

def lab_meta(raw, i):
    if 'Maverick' in raw: return 'Llama 4 Maverick'
    if 'Scout' in raw: return 'Llama 4 Scout'
    if 'Spark' in raw: return 'Muse Spark'
    if 'Wonder' in raw: return 'Muse Wonder'
    return raw

def lab_deepseek(raw, i):
    s = raw.replace('DeepSeek-', '')
    prev = ' (preview)' if 'preview' in s else ''
    s = re.sub(r'\s*\(.*\)', '', s)
    s = re.sub(r'-\d{4}$', '', s)            # V4-Pro-0813 -> V4-Pro ; V4.1-Flash-1017
    s = s.replace('V3-0324', 'V3-0324')
    s = s.replace('-', ' ', 1) if s.startswith('V4') else s
    s = s.replace('V4 Flash', 'V4 Flash').replace('V4.1 Flash', 'V4.1 Flash')
    s = s.replace('V4-Pro', 'V4 Pro').replace(' non-thinking', '')
    return s + prev

def lab_qwen(raw, i):
    s = re.sub(r'\s*\(.*\)', '', raw)
    s = s.split(' / ')[-1]
    s = re.sub(r'-\d{4}-\d{2}-\d{2}$', '', s)
    s = re.sub(r'-\d{4}$', '', s)
    s = s[0].upper() + s[1:]
    return re.sub(r'-(max|plus|turbo|flash)$', lambda m: '-' + m.group(1).capitalize(), s)

def lab_minimax(raw, i):
    s = raw.replace('MiniMax-', '')
    s = s.replace('M2.5-lightning / highspeed', 'M2.5 lightning').replace('M2.7-highspeed', 'M2.7 highspeed')
    return s.replace('M3.1-Flash', 'M3.1 Flash')

def lab_glm(raw, i):
    return raw

def lab_kimi(raw, i):
    t = {'kimi-k2-0711-preview': 'K2', 'kimi-k2-0905-preview': 'K2 0905', 'kimi-k2-thinking': 'K2 Thinking', 'kimi-k2.5': 'K2.5',
         'kimi-k2.6': 'K2.6', 'kimi-k2.7-code': 'K2.7 Code', 'kimi-k3': 'K3', 'kimi-k3.1-pro': 'K3.1 Pro'}
    return t[raw]

def series(points, lab, lo=0, hi=N - 1, price=None, suffix=None):
    d = [None] * N; u = [0] * N; names = [None] * N
    for p in points:
        i = p['index']
        if i < lo or i > hi: continue
        d[i] = p['output_usd_per_mtok']
        u[i] = 1 if p['status'].startswith('U') else 0
        names[i] = lab(p['model'], i) + (suffix(i) if suffix else '')
    return d, u, names

def finish(prov, grp_title, tier_name, d, u, names, **kw):
    m = {}; prev = None
    for i in range(N):
        if d[i] is None: prev = None; continue
        key = (names[i], d[i])
        if prev is None or names[i] != prev[0] or d[i] != prev[1]:
            m[i] = names[i]
        prev = key
    out = {'prov': prov, 'grp': grp_title, 'tier': tier_name, 'd': d, 'u': u, 'm': m}
    out.update(kw)
    return out

L = []  # lineages in display order

# ---------------- Anthropic ----------------
for t in ['Opus', 'Sonnet', 'Haiku', 'Fable']:
    d, u, n = series(tier('anthropic', t), lab_anthropic)
    L.append(finish('Anthropic', 'Anthropic', t, d, u, n))

# ---------------- OpenAI ----------------
for t, key in [('Mini', 'Mini'), ('Nano', 'Nano')]:
    d, u, n = series(tier('openai', key), lab_openai)
    L.append(finish('OpenAI', 'OpenAI Mini and Nano', t, d, u, n))
d, u, n = series(tier('openai', 'Frontier'), lab_openai)
L.append(finish('OpenAI', 'OpenAI Frontier, Sol, Terra and Luna', 'Frontier', d, u, n, hist=1))
for t in ['Sol', 'Terra', 'Luna']:
    d, u, n = series(tier('openai', t), lab_openai)
    L.append(finish('OpenAI', 'OpenAI Frontier, Sol, Terra and Luna', t, d, u, n))

# ---------------- Google ----------------
gp = tier('google', 'Pro')
d, u, n = series(gp, lab_google, hi=20)
L.append(finish('Google', 'Google', 'Pro', d, u, n))
def flash_suffix(i): return ' (intro price)' if i in (19, 20, 21, 22) else ''
gf = [p for p in tier('google', 'Flash') if not p['model'].startswith('Gemini 4')]
# Gemini 3.8 Flash intro price ($3.75) stays in force through Dec 31 2026
last = [p for p in gf if p['index'] == 21][0]
gf = gf + [dict(last, index=22)]
d, u, n = series(gf, lab_google, suffix=flash_suffix)
L.append(finish('Google', 'Google', 'Flash', d, u, n))
tl = [p for p in tier('google', 'Flash-Lite')]
d, u, n = series(tl, lab_google)
L.append(finish('Google', 'Google', 'Flash-Lite', d, u, n))
g4 = [dict(p, model='Gemini 4 Argon') for p in gp if p['index'] in (21, 22)]
d, u, n = series(g4, lab_google, suffix=lambda i: ' (intro price)')
L.append(finish('Google', 'Google', 'Gemini 4', d, u, n))

# ---------------- xAI ----------------
for t, name in [('Flagship', 'Grok'), ('Fast', 'Grok Fast'), ('Code', 'Grok Code')]:
    d, u, n = series(tier('xai', t), lab_xai)
    L.append(finish('xAI', 'xAI', name, d, u, n))

# ---------------- Mistral ----------------
for t in ['Large', 'Medium', 'Small']:
    d, u, n = series(tier('mistral', t), lab_mistral)
    L.append(finish('Mistral', 'Mistral', t, d, u, n))

# ---------------- Meta ----------------
for t, name in [('Llama 4 Maverick', 'Maverick (host list)'), ('Llama 4 Scout', 'Scout (host list)'), ('Muse Spark', 'Muse Spark'), ('Muse Wonder', 'Muse Wonder')]:
    d, u, n = series(tier('meta', t), lab_meta)
    L.append(finish('Meta', 'Meta', name, d, u, n))

# ---------------- DeepSeek ----------------
for t, name in [('Chat', 'Chat / Flash'), ('Reasoner', 'Reasoner'), ('Pro', 'Pro')]:
    d, u, n = series(tier('deepseek', t), lab_deepseek, suffix=(lambda i: ' (peak rate)' if i >= 19 else '') if t != 'Reasoner' else None)
    L.append(finish('DeepSeek', 'DeepSeek', name, d, u, n))

# ---------------- Qwen ----------------
for t, name in [('Max', 'Max'), ('Plus', 'Plus'), ('Turbo', 'Turbo / Flash')]:
    d, u, n = series(tier('qwen', t), lab_qwen)
    L.append(finish('Qwen', 'Qwen', name, d, u, n))

# ---------------- MiniMax ----------------
for t, name in [('Flagship', 'M-series'), ('Highspeed', 'Highspeed'), ('Flash', 'Flash')]:
    d, u, n = series(tier('minimax', t), lab_minimax)
    L.append(finish('MiniMax', 'MiniMax', name, d, u, n))

# ---------------- GLM ----------------
for t, name in [('Flagship', 'GLM'), ('Air', 'Air / Flash')]:
    d, u, n = series(tier('glm', t), lab_glm)
    L.append(finish('GLM', 'GLM', name, d, u, n))

# ---------------- Kimi ----------------
for t, name in [('K2', 'K2'), ('K3', 'K3')]:
    d, u, n = series(tier('kimi', t), lab_kimi)
    L.append(finish('Kimi', 'Kimi', name, d, u, n))

json.dump(L, open(sys.argv[1] if len(sys.argv) > 1 else 'data.json', 'w'), separators=(',', ':'))

# ---------- review print ----------
for l in L:
    idx = [i for i in range(N) if l['d'][i] is not None]
    a, b = idx[0], idx[-1]
    gaps = [i for i in range(a, b + 1) if l['d'][i] is None]
    print('%-9s %-24s %2d-%2d n=%2d %6s -> %-6s unv=%d %s%s' % (l['prov'], l['tier'], a, b, len(idx), l['d'][a], l['d'][b], sum(l['u']),
          'HIST ' if l.get('hist') else '', 'GAPS%s' % gaps if gaps else ''))
    print('     ', ' | '.join('%d:%s' % (k, v) for k, v in sorted(l['m'].items())))
