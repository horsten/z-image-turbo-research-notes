#!/usr/bin/env python3
# Z-Image-Turbo (NextDiT) architecture diagram -> standalone SVG.
# Modular: main flow panel + 4 inset panels + legend, wrapped in one container.

W, H = 1704, 1880
S = []

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rect(x, y, w, h, cls, rx=8, extra=""):
    S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}" {extra}/>')

def txt(x, y, s, cls="t", anchor="middle"):
    S.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{esc(s)}</text>')

def box(x, y, w, h, cls, title=None, sub=None, dim=None, rx=8):
    rect(x, y, w, h, cls, rx=rx)
    cx = x + w / 2
    lines = [(title, "t"), (sub, "t2"), (dim, "d")]
    lines = [l for l in lines if l[0]]
    n = len(lines)
    cy = y + h / 2
    if n == 1:
        ys = [cy + 5]
    elif n == 2:
        ys = [cy - 8, cy + 11]
    else:
        ys = [cy - 15, cy + 4, cy + 22]
    for (s, c), yy in zip(lines, ys):
        txt(cx, yy, s, c)
    return {"cx": cx, "cy": cy, "top": (cx, y), "bot": (cx, y + h),
            "l": (x, cy), "r": (x + w, cy), "x": x, "y": y, "w": w, "h": h}

def arrow(x1, y1, x2, y2, cls="flow"):
    S.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#ah)"/>')

def vconn(a, b):  # vertical arrow between stacked boxes
    arrow(a["bot"][0], a["bot"][1], b["top"][0], b["top"][1])

def line(x1, y1, x2, y2, cls="flow", marker=True):
    m = ' marker-end="url(#ah)"' if marker else ""
    S.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{m}/>')

def poly(pts, cls="flow", marker=True):
    d = " ".join(f"{x},{y}" for x, y in pts)
    m = ' marker-end="url(#ah)"' if marker else ""
    S.append(f'<polyline points="{d}" fill="none" class="{cls}"{m}/>')

def dot(x, y, r=6, cls="amberdot"):
    S.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>')

def sdot(x, y, r=7):  # struck (no-modulation) dot
    S.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="sdot"/>')
    S.append(f'<line x1="{x-r}" y1="{y+r}" x2="{x+r}" y2="{y-r}" class="sdotslash"/>')

# ---- header / defs ----
S.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Inter, \'Segoe UI\', system-ui, sans-serif">')
S.append('''<defs>
<marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
  <path d="M0,0 L9,4.5 L0,9 Z" fill="#4a5568"/>
</marker>
<marker id="aha" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
  <path d="M0,0 L9,4.5 L0,9 Z" fill="#c07d1e"/>
</marker>
<marker id="aht" markerWidth="8" markerHeight="8" refX="6.5" refY="4" orient="auto">
  <path d="M0,0 L8,4 L0,8 Z" fill="#2c7a6b"/>
</marker>
<style>
  rect { stroke-width:1.5; }
  .flow { stroke:#4a5568; stroke-width:1.7; fill:none; }
  .amber { stroke:#c07d1e; stroke-width:2.6; fill:none; }
  .amberconn { stroke:#c07d1e; stroke-width:1.6; fill:none; stroke-dasharray:5 3; }
  .ropeconn { stroke:#2c7a6b; stroke-width:1.5; fill:none; stroke-dasharray:5 3; }
  .resid { stroke:#8a94a2; stroke-width:1.5; fill:none; }
  .lin  { fill:#e7ebf0; stroke:#51678a; }
  .norm { fill:#eceef1; stroke:#737d8a; }
  .attn { fill:#e7e2f2; stroke:#5c4a97; }
  .ffn  { fill:#f4e2dd; stroke:#a85445; }
  .rope { fill:#dcefe9; stroke:#2c7a6b; }
  .mod  { fill:#f9e7c5; stroke:#c07d1e; }
  .top  { fill:#ffffff; stroke:#9aa4b2; stroke-dasharray:5 3; }
  .imgb { fill:#e3edf8; stroke:#35618e; }
  .promptb { fill:#e2f1ec; stroke:#2c7a6b; }
  .cont { fill:#f6f8fb; stroke:#51678a; stroke-width:2; }
  .contghost { fill:#eef2f7; stroke:#9fb0c4; }
  .inset { fill:#fcfcfd; stroke:#c7cfd8; stroke-width:1.5; }
  .node { fill:#f4f6f8; stroke:#9aa4b2; }
  .amberdot { fill:#c07d1e; stroke:#8a5a12; stroke-width:1; }
  .sdot { fill:#fbeed0; stroke:#c07d1e; stroke-width:1.4; }
  .sdotslash { stroke:#a85445; stroke-width:1.8; }
  .title { font-size:27px; font-weight:700; fill:#17202a; }
  .subtitle { font-size:14.5px; font-weight:400; fill:#55606c; }
  .t   { font-size:14px; font-weight:600; fill:#17202a; }
  .t2  { font-size:12.5px; font-weight:400; fill:#33404d; }
  .d   { font-size:12px; font-weight:500; fill:#2c3e50; font-family:'SF Mono',ui-monospace,Menlo,Consolas,monospace; }
  .cap { font-size:12px; font-weight:400; fill:#5a6672; }
  .hd  { font-size:15.5px; font-weight:700; fill:#17202a; }
  .tb  { font-size:18px; font-weight:700; fill:#17202a; }
  .sm  { font-size:11px; font-weight:500; fill:#5a6672; }
  .amb { font-size:11.5px; font-weight:600; fill:#9a6410; font-family:'SF Mono',ui-monospace,Menlo,Consolas,monospace; }
  .eyebrow { font-size:12px; font-weight:700; fill:#8a94a2; letter-spacing:2px; }
</style>
</defs>''')

rect(0, 0, W, H, "top", rx=0, extra='fill="#ffffff" stroke="none"')

# ---- title ----
txt(48, 62, "Z-Image-Turbo \u00b7 Single-Stream Diffusion Transformer (NextDiT)", "title", "start")
txt(48, 90, "Latent path \u00b7 dim 3840 \u00b7 30 heads (head_dim 128) \u00b7 parameters reconciled with a live model dump", "subtitle", "start")
line(48, 104, 1656, 104, "resid", marker=False)

# divider between flow and insets
line(918, 130, 918, 1388, "resid", marker=False)
txt(120, 128, "MAIN FLOW", "eyebrow", "start")
txt(940, 128, "COMPONENT DETAIL", "eyebrow", "start")

# =========================================================================
#  CONDITIONING ORIGIN + RAIL  (far left)
# =========================================================================
railx = 118
t1 = box(42, 150, 152, 40, "mod", title="t = 1 \u2212 timestep")
t2 = box(42, 214, 152, 54, "mod", title="t_embedder", dim="\u2192 adaln_input [256]")
vconn(t1, t2)
# amber rail down
line(railx, 268, railx, 1108, "amber", marker=False)
S.append('<text x="102" y="392" class="amb" text-anchor="middle" transform="rotate(-90 102 392)">timestep conditioning</text>')

# =========================================================================
#  IMAGE BRANCH (left column)
# =========================================================================
icx = 340; iw = 236; ix = icx - iw / 2
I1 = box(ix, 210, iw, 58, "top", title="Latent image  z_t", dim="[16 \u00d7 H \u00d7 W]")
I2 = box(ix, 300, iw, 58, "top", title="Patchify \u00b7 reshape", dim="2\u00d72 block \u2192 [N, 64]")
I3 = box(ix, 390, iw, 58, "lin", title="x_embedder \u00b7 Linear", dim="64 \u2192 3840   \u2192 [N, 3840]")
rect(ix, 480, iw, 96, "imgb")
I4 = {"cx": icx, "top": (icx, 480), "bot": (icx, 576), "l": (ix, 528), "cy": 528}
txt(icx, 508, "Noise Refiner", "t")
txt(icx, 529, "2 \u00d7 JointTransformerBlock", "t2")
txt(icx, 550, "modulated \u00b7 image tokens only", "cap")
vconn(I1, I2); vconn(I2, I3); vconn(I3, I4)
dot(ix, 528)  # modulated tap marker on refiner

# =========================================================================
#  PROMPT BRANCH (right column)
# =========================================================================
pcx = 650; pw = 236; px = pcx - pw / 2
P1 = box(px, 210, pw, 58, "top", title="Qwen3-4B text encoder", dim="[L, 2560]")
P2 = box(px, 300, pw, 72, "lin", title="cap_embedder", sub="RMSNorm 2560 \u00b7 Linear 2560\u21923840", dim="\u2192 [L, 3840]")
rect(px, 480, pw, 96, "promptb")
P3 = {"cx": pcx, "top": (pcx, 480), "bot": (pcx, 576), "cy": 528}
sdot(px + 18, 500)  # unmodulated marker, inside the block
txt(pcx, 504, "Context Refiner", "t")
txt(pcx, 524, "2 \u00d7 JointTransformerBlock", "t2")
txt(pcx, 545, "prompt tokens only", "cap")
txt(pcx, 563, "unmodulated \u2014 no timestep", "cap")
vconn(P1, P2); vconn(P2, P3)

# =========================================================================
#  SHARED RoPE cluster
# =========================================================================
rect(350, 592, 290, 92, "rope")
txt(495, 616, "rope_embedder (EmbedND) \u00b7 shared", "t")
txt(495, 636, "head_dim 128 = 16+56+56  over (t, y, x)", "d")
txt(495, 658, "computed at embed \u00b7 used by every attention", "cap")
txt(495, 675, "(both refiners and all main layers)", "cap")
RP = {"cx": 495, "l": (350, 638), "r": (640, 638), "top": (495, 592), "bot": (495, 684)}
ci = box(232, 615, 104, 46, "top", title="pos-ids img", dim="(t\u2093, y, x)")
cp = box(654, 615, 104, 46, "top", title="pos-ids txt", dim="(1..L, 0, 0)")
line(ci["r"][0], ci["r"][1], RP["l"][0], RP["l"][1], "ropeconn")
line(cp["l"][0], cp["l"][1], RP["r"][0], RP["r"][1], "ropeconn")

# =========================================================================
#  MERGE + TRUNK
# =========================================================================
CC = box(325, 720, 340, 58, "top", title="Concat  [ prompt ; image ]", dim="\u2192 [L+N, 3840]")
# merge arrows from refiners -> concat (elbow to clear rope box)
poly([(icx, 576), (icx, 700), (CC["cx"] - 60, 720)])
poly([(pcx, 576), (pcx, 700), (CC["cx"] + 60, 720)])
# rope feed into trunk (dashed)
poly([(495, 684), (495, 714)], "ropeconn")

# DiT container with stacked-card ghost
dc_x, dc_y, dc_w, dc_h = 315, 838, 360, 168
rect(dc_x + 12, dc_y - 12, dc_w, dc_h, "contghost")
rect(dc_x + 6, dc_y - 6, dc_w, dc_h, "contghost")
rect(dc_x, dc_y, dc_w, dc_h, "cont")
txt(dc_x + dc_w / 2, dc_y + 42, "Unified DiT", "tb")
txt(dc_x + dc_w / 2, dc_y + 66, "30 \u00d7 JointTransformerBlock", "t2")
# badge
rect(dc_x + dc_w - 66, dc_y + 14, 52, 26, "mod", rx=13)
txt(dc_x + dc_w - 40, dc_y + 31, "\u00d730", "t")
txt(dc_x + dc_w / 2, dc_y + 98, "sandwich RMSNorm \u00b7 scale-only AdaLN (no shift)", "cap")
txt(dc_x + dc_w / 2, dc_y + 118, "tanh-bounded gates \u00b7 SwiGLU feed-forward", "cap")
txt(dc_x + dc_w / 2, dc_y + 146, "residual stream \u2192 [L+N, 3840]", "d")
dc = {"cx": dc_x + dc_w / 2, "top": (dc_x + dc_w / 2, dc_y), "bot": (dc_x + dc_w / 2, dc_y + dc_h),
      "l": (dc_x, dc_y + dc_h / 2)}
arrow(CC["bot"][0], CC["bot"][1], dc["top"][0], dc["top"][1])
dot(dc_x, dc_y + dc_h / 2)  # modulated tap
# link to hero inset
line(dc_x + dc_w, dc_y + 30, 956, dc_y + 30, "amberconn")
txt(dc_x + dc_w + 96, dc_y + 24, "\u2192 block inset", "sm", "middle")

FL = box(325, 1058, 340, 78, "lin", title="Final Layer",
         sub="LayerNorm(affine=False) \u00b7 AdaLN scale \u00b7 Linear 3840\u219264", dim="\u2192 [\u00b7, 64]")
arrow(dc["bot"][0], dc["bot"][1], FL["top"][0], FL["top"][1])
dot(FL["x"], FL["cy"])  # modulated tap

UP = box(345, 1178, 300, 58, "top", title="Unpatchify \u00b7 reshape", dim="[N, 64] \u2192 [16, H, W]")
OUT = box(345, 1268, 300, 58, "imgb", title="Latent output", dim="\u2212v\u03b8   \u00b7   [16 \u00d7 H \u00d7 W]")
vconn(FL, UP); vconn(UP, OUT)

# rail taps (amber)
line(railx, 528, ix, 528, "amber")
S[-1] = S[-1].replace('class="amber"', 'class="amber" marker-end="url(#aha)"').replace(' marker-end="url(#ah)"', '')
line(railx, dc_y + dc_h / 2, dc_x, dc_y + dc_h / 2, "amber")
S[-1] = S[-1].replace(' marker-end="url(#ah)"', ' marker-end="url(#aha)"')
line(railx, FL["cy"], FL["x"], FL["cy"], "amber")
S[-1] = S[-1].replace(' marker-end="url(#ah)"', ' marker-end="url(#aha)"')

# =========================================================================
#  INSET 1 : JointTransformerBlock (hero)
# =========================================================================
IX = 956
rect(IX, 150, 700, 896, "inset")
txt(IX + 20, 180, "JointTransformerBlock", "hd", "start")
txt(IX + 20, 200, "used by all 30 main DiT layers, as well as the 2 + 2 noise/context refiner layers", "sm", "start")

dcx = IX + 200          # dataflow column center
dw = 220
dxx = dcx - dw / 2
acx = IX + 540          # adaLN column center
aw = 200
axx = acx - aw / 2

def dnode(y, cls, title, sub=None, h=40):
    return box(dxx, y, dw, h, cls, title=title, sub=sub)

y = 228
n_xin = dnode(y, "node", "x", None, 32); y += 54
n_an1 = dnode(y, "norm", "attention_norm1", "RMSNorm 3840"); y += 62
n_sm1 = box(dxx, y, dw, 30, "mod", title="\u2297  1 + scale_msa"); y += 52
n_att = dnode(y, "attn", "Attention", "\u2192 inset A", 46); y += 68
n_an2 = dnode(y, "norm", "attention_norm2", "RMSNorm 3840"); y += 62
n_gm1 = box(dxx, y, dw, 30, "mod", title="\u2299  tanh(gate_msa)"); y += 52
n_ad1 = box(dxx, y, dw, 30, "node", title="\u2295  residual add"); y += 52
n_fn1 = dnode(y, "norm", "ffn_norm1", "RMSNorm 3840"); y += 62
n_sm2 = box(dxx, y, dw, 30, "mod", title="\u2297  1 + scale_mlp"); y += 52
n_ffn = dnode(y, "ffn", "Feed-Forward \u00b7 SwiGLU", "\u2192 inset B", 46); y += 68
n_fn2 = dnode(y, "norm", "ffn_norm2", "RMSNorm 3840"); y += 62
n_gm2 = box(dxx, y, dw, 30, "mod", title="\u2299  tanh(gate_mlp)"); y += 52
n_ad2 = box(dxx, y, dw, 30, "node", title="\u2295  residual add"); y += 52
n_out = dnode(y, "node", "x", None, 32)

chain = [n_xin, n_an1, n_sm1, n_att, n_an2, n_gm1, n_ad1, n_fn1, n_sm2, n_ffn, n_fn2, n_gm2, n_ad2, n_out]
for a, b in zip(chain, chain[1:]):
    vconn(a, b)

# residual bypass lines (left side)
rlx = dxx - 26
poly([(n_xin["bot"][0], n_xin["bot"][1]), (rlx, n_xin["bot"][1] + 6),
      (rlx, n_ad1["cy"]), (n_ad1["l"][0], n_ad1["cy"])], "resid")
poly([(n_ad1["bot"][0], n_ad1["bot"][1]), (rlx, n_ad1["bot"][1] + 6),
      (rlx, n_ad2["cy"]), (n_ad2["l"][0], n_ad2["cy"])], "resid")
txt(rlx - 6, (n_xin["bot"][1] + n_ad1["cy"]) / 2, "residual", "sm", "end")

# adaLN column
a_in = box(axx, 470, aw, 40, "mod", title="adaln_input [256]")
a_mod = box(axx, 542, aw, 52, "mod", title="adaLN_modulation", dim="Linear 256 \u2192 15360")
a_chk = box(axx, 624, aw, 34, "mod", title="chunk \u00d7 4")
vconn(a_in, a_mod); vconn(a_mod, a_chk)
# four modulation signals routed via a shared vertical bus -> inject nodes
busx = 1300
tgts = [n_sm1, n_gm1, n_sm2, n_gm2]
ys = [t["cy"] for t in tgts]
poly([(a_chk["cx"], a_chk["bot"][1]), (a_chk["cx"], a_chk["bot"][1] + 12), (busx, a_chk["bot"][1] + 12)], "amberconn", marker=False)
line(busx, min(ys), busx, max(ys), "amberconn", marker=False)
for t in tgts:
    line(busx, t["cy"], t["r"][0], t["cy"], "amberconn", marker=False)
txt(acx, 702, "4 chunks \u00d7 3840", "amb", "middle")
txt(acx, 732, "scale-only \u2014 no shift term", "cap", "middle")
txt(acx, 750, "(cf. Flux, which also shifts)", "cap", "middle")
txt(acx, 768, "gates are tanh-bounded", "cap", "middle")

# =========================================================================
#  INSET 2 : Attention
# =========================================================================
rect(IX, 1078, 700, 648, "inset")
txt(IX + 20, 1108, "Inset A \u2014 Attention (JointAttention)", "hd", "start")
txt(IX + 20, 1128, "no GQA: n_kv_heads = n_heads = 30  \u00b7  bias-free projections", "sm", "start")
acx2 = IX + 300; aw2 = 320; ax2 = acx2 - aw2 / 2
yy = 1152
A1 = box(ax2, yy, aw2, 34, "node", title="x   [\u00b7, 3840]"); yy += 80
A2 = box(ax2, yy, aw2, 40, "lin", title="qkv \u00b7 Linear 3840 \u2192 11520"); yy += 84
A3 = box(ax2, yy, aw2, 40, "top", title="split \u2192 Q, K, V", dim="30 \u00d7 128 each"); yy += 84
A4 = box(ax2, yy, aw2, 40, "norm", title="q_norm / k_norm \u00b7 RMSNorm(128)", sub="on Q, K"); yy += 84
A5 = box(ax2, yy, aw2, 40, "rope", title="RoPE  \u2192  Q, K"); yy += 84
A6 = box(ax2, yy, aw2, 40, "attn", title="Scaled Dot-Product Attention"); yy += 84
A7 = box(ax2, yy, aw2, 40, "lin", title="out \u00b7 Linear 3840 \u2192 3840")
for a, b in zip([A1, A2, A3, A4, A5, A6, A7], [A2, A3, A4, A5, A6, A7]):
    vconn(a, b)
# rope freqs feed (kept inside the inset margin)
fs = A5["r"][0] + 96
line(fs, A5["cy"], A5["r"][0], A5["cy"], "ropeconn")
txt(fs + 2, A5["cy"] - 22, "freqs_cis", "sm", "start")
txt(fs + 2, A5["cy"] - 8, "(rope_embedder)", "sm", "start")

# =========================================================================
#  INSET 3 : SwiGLU FFN
# =========================================================================
rect(48, 1380, 430, 372, "inset")
txt(68, 1410, "Inset B \u2014 Feed-Forward \u00b7 SwiGLU", "hd", "start")
txt(68, 1430, "gated MLP, not a plain 2-layer MLP", "sm", "start")
fcx = 263
F0 = box(fcx - 110, 1448, 220, 34, "node", title="x   [\u00b7, 3840]")
Fw1 = box(fcx - 176, 1504, 168, 46, "lin", title="w1 \u00b7 Linear", dim="3840 \u2192 10240")
Fw3 = box(fcx + 8, 1504, 168, 46, "lin", title="w3 \u00b7 Linear", dim="3840 \u2192 10240")
Fsl = box(fcx - 176, 1574, 168, 38, "ffn", title="SiLU")
Fml = box(fcx - 30, 1630, 60, 38, "node", title="\u2299")
Fw2 = box(fcx - 126, 1682, 252, 56, "lin", title="w2 \u00b7 Linear 10240 \u2192 3840", dim="w2( SiLU(w1\u00b7x) \u2299 w3\u00b7x )")
poly([(F0["bot"][0], F0["bot"][1]), (Fw1["top"][0], F0["bot"][1] + 8), (Fw1["top"][0], Fw1["top"][1])])
poly([(F0["bot"][0], F0["bot"][1]), (Fw3["top"][0], F0["bot"][1] + 8), (Fw3["top"][0], Fw3["top"][1])])
vconn(Fw1, Fsl)
poly([(Fsl["bot"][0], Fsl["bot"][1]), (Fsl["bot"][0], Fml["cy"]), (Fml["l"][0], Fml["cy"])])
poly([(Fw3["bot"][0], Fw3["bot"][1]), (Fw3["bot"][0], Fml["cy"]), (Fml["r"][0], Fml["cy"])])
poly([(Fml["bot"][0], Fml["bot"][1]), (Fml["bot"][0], Fw2["top"][1] - 8), (Fw2["top"][0], Fw2["top"][1] - 8), (Fw2["top"][0], Fw2["top"][1])])

# =========================================================================
#  INSET 4 : Timestep embedder + legend
# =========================================================================
rect(498, 1380, 402, 372, "inset")
txt(518, 1410, "Timestep conditioning", "hd", "start")
tcx = 636; tw = 264; tx = tcx - tw / 2
T1 = box(tx, 1444, tw, 34, "mod", title="t = 1 \u2212 timestep")
T2 = box(tx, 1494, tw, 40, "mod", title="sinusoidal embedding", dim="\u2192 256")
T3 = box(tx, 1550, tw, 56, "mod", title="t_embedder MLP", sub="Linear 256\u21921024 \u00b7 SiLU \u00b7 Linear 1024\u2192256")
T4 = box(tx, 1622, tw, 34, "mod", title="adaln_input  [256]")
for a, b in zip([T1, T2, T3], [T2, T3, T4]):
    vconn(a, b)
txt(636, 1690, "the same 256-d vector drives AdaLN in the noise", "cap", "middle")
txt(636, 1708, "refiner, all 30 main blocks and the final layer \u2014", "cap", "middle")
txt(636, 1726, "but never the context refiner.", "cap", "middle")

# =========================================================================
#  LEGEND (bottom strip)
# =========================================================================
ly = 1772
rect(48, ly, 1608, 76, "top", rx=10, extra='stroke="#c7cfd8" stroke-dasharray="0"')
txt(64, ly + 24, "LEGEND", "eyebrow", "start")
items = [
    ("lin", "Linear / projection"), ("norm", "Norm (RMS / Layer)"),
    ("attn", "Attention"), ("ffn", "SwiGLU FFN"), ("rope", "RoPE"),
    ("mod", "Modulation / conditioning"), ("top", "Tensor op (reshape / concat)"),
]
xk = 180
for cls, lab in items:
    rect(xk, ly + 14, 22, 16, cls, rx=4)
    txt(xk + 30, ly + 27, lab, "cap", "start")
    xk += 205
# second row
def key_line(x, ycol, cls, lab, amber=False, rope=False):
    if amber:
        S.append(f'<line x1="{x}" y1="{ycol}" x2="{x+26}" y2="{ycol}" class="amber"/>')
    elif rope:
        S.append(f'<line x1="{x}" y1="{ycol}" x2="{x+26}" y2="{ycol}" class="ropeconn"/>')
    else:
        S.append(f'<line x1="{x}" y1="{ycol}" x2="{x+26}" y2="{ycol}" class="{cls}"/>')
    txt(x + 34, ycol + 4, lab, "cap", "start")

yl2 = ly + 54
key_line(180, yl2, "flow", "data flow"); 
key_line(320, yl2, None, "timestep conditioning", amber=True)
key_line(560, yl2, None, "RoPE / modulation routing", rope=True)
dot(830, yl2); txt(846, yl2 + 4, "modulated", "cap", "start")
sdot(950, yl2); txt(966, yl2 + 4, "unmodulated", "cap", "start")
txt(1120, yl2 + 4, "dims shown per token unless noted; N = image patches, L = prompt tokens", "sm", "start")

S.append("</svg>")

open("z-image-turbo-architecture.svg", "w").write("\n".join(S))
print("written", len("\n".join(S)), "bytes")
