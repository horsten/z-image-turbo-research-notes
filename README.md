# Research notes for Z-Image-Turbo

This repository currently contains a generator for an architectural diagram of Z-Image-Turbo.

It was created in collaboration between Thomas Horsten and Claude Opus 4.8 based on the architectural overview below, and a detailed code review of the ComfyUI implementation, reconciled with a live parameter dump from a debugging session with the actual model loaded.

## Files

- `z-image-turbo-architecture.svg` — the diagram (standalone, vector; opens in any browser).
- `gen.py` — the layout script that produces the SVG. This is the source of truth; edit and re-run to regenerate the figure.

## Usage

```sh
python3 gen.py
```

`gen.py` uses only the Python standard library and writes the SVG directly, so it regenerates the diagram anywhere with no dependencies. The output path near the end of the script currently points at the working directory it was authored in — change that `open(...)` line to wherever you keep the repo.

`cairosvg` is optional and only needed if you want to rasterize the SVG to PNG (e.g. for an inline README preview, since GitHub sanitizes inline SVG in Markdown and renders `![](…svg)` as a link rather than an image).

## Architectural overview

### Z-Image-Turbo — single-stream diffusion transformer (NextDiT), latent path

Global constants from the dump: `dim = 3840`, `head_dim = 128` → **30 attention heads**, no GQA (Q/K/V all 30 heads, since `qkv = 3840 → 11520 = 3·30·128`), FFN hidden = 10240, conditioning vector `adaln_input` = 256-dim.

### Image branch — patchify + embed

- **Patchifier** (pure tensor reshape, no parameters): groups each 2×2 spatial block of the 16-channel latent into one patch of 2·2·16 = 64 values.
- **Image embedder** (`x_embedder`): single `Linear(64 → 3840, bias=True)` projecting each patch to a 3840-dim token.
- **Position IDs (image):** each patch is assigned a 3-axis coordinate `(t, y, x)` where `t` is a *constant* offset placing the image after the prompt, and `y, x` are the patch's row/column. So image tokens vary only along the two spatial axes.
- **Noise Refiner:** 2 × `JointTransformerBlock`, image tokens only, **timestep-modulated** (same modulated block as the main DiT).

### Prompt branch — embed

- **Prompt embedder** (`cap_embedder`): `RMSNorm(2560)` → `Linear(2560 → 3840, bias=True)`, projecting Qwen3-4B encoder tokens (hidden 2560) to 3840-dim.
- **Position IDs (prompt):** each token gets coordinate `(t, 0, 0)` with `t = 1, 2, 3, …` — i.e. the prompt varies along a single linear axis, with both spatial axes zeroed.
- **Context Refiner:** 2 × `JointTransformerBlock`, prompt tokens only, **unmodulated** — it never sees the timestep. It keeps the sandwich norms but drops all scale/gate modulation.

### Shared RoPE embedder

- A single `rope_embedder` (`EmbedND`) turns the 3-axis position IDs into rotary frequencies. `head_dim = 128` is split across the three axes (default 16/56/56, config-set). Both branches use the *same* module; they differ only in how their position IDs are computed (linear-`t` for prompt vs. spatial-`y,x` for image, above).

### Concatenation

`[prompt tokens, image tokens]` along the sequence axis into one unified stream.

### Unified DiT — 30 × `JointTransformerBlock`

Each block receives the stream `x` and the 256-dim conditioning `c`. Modulation is produced by `adaLN_modulation = Linear(256 → 15360)`, chunked into four 3840-vectors: `scale_msa, gate_msa, scale_mlp, gate_mlp`. Note this is **scale-only** (`x·(1+scale)`, no shift — unlike Flux, which also shifts here), and the gates are **tanh-bounded**.

- Attention sublayer (sandwich-normed, scale before / gate after):
  - `attention_norm1` (RMSNorm) → **scale by `(1+scale_msa)`** →
  - Attention: fused `qkv = Linear(3840 → 11520, bias=False)`, split to Q/K/V (30×128 each) → per-head `RMSNorm(128)` on **Q and K** → RoPE applied to **Q and K** → scaled dot-product attention → `out = Linear(3840 → 3840, bias=False)` →
  - `attention_norm2` (RMSNorm) → **gate by `tanh(gate_msa)`** →
  - residual add to the stream.
- Feed-forward sublayer (sandwich-normed, scale before / gate after):
  - `ffn_norm1` (RMSNorm) → **scale by `(1+scale_mlp)`** →
  - FFN is **SwiGLU**, not a plain MLP: `w2( SiLU(w1·h) ⊙ (w3·h) )`, with `w1, w3: 3840 → 10240` and `w2: 10240 → 3840` (all bias-free) →
  - `ffn_norm2` (RMSNorm) → **gate by `tanh(gate_mlp)`** →
  - residual add to the stream.

### Timestep conditioning rail

- `t = 1 − timestep` (flow-matching convention) → `TimestepEmbedder` (sinusoidal 256 → MLP `256 → 1024 → 256`) → the 256-dim `adaln_input`.
- This single vector feeds the AdaLN of **every modulated block**: the 2 noise-refiner blocks, all 30 main blocks, and the final layer — but **not** the context refiner.

### Final layer + unpatchify

- `FinalLayer`: `LayerNorm(3840, affine=False, eps=1e-6)` → **scale-only AdaLN** (`SiLU → Linear(256 → 3840)`, applied as `x·(1+scale)`) → `Linear(3840 → 64, bias=True)` down-projecting each token to a 64-value patch.
- **Unpatchifier** (reshape): splits each 64-value patch back into a 2×2 block of the 16-channel latent, reassembling the latent image. (The model's raw output is a negated velocity/`−x0`; the sampler reconstructs `x0` from it — worth a footnote but outside the forward graph.)
