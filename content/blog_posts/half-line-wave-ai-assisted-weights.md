---
title: A Wave Equation Without a Far Wall
slug: half-line-wave-ai-assisted-weights
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: A weight designed for an unbounded domain avoids inventing a boundary where there is none.
kicker: Paper Notes
cover:
  image: /img/blog/half-line-wave-ai-assisted-weights.webp
  alt: A translucent blue wave ribbon starts at a small amber sensor on the left and extends toward an open white
    horizon, without a far wall.
  width: 1600
  height: 900
---

A wave travels along a half-line. There is an accessible endpoint on the left, but no wall on the right.

For a calculation, it is tempting to cut the half-line at some large distance and impose a boundary condition there. The new problem is easier to draw. It may also answer the wrong question: the artificial wall can reflect waves and introduce information that the original system never supplied.

Our paper develops Carleman estimates directly on the half-line, with an AI-assisted search contributing to the choice of weight.[^paper]

## Geometry should choose the weight

For the simple wave equation $u_{tt}-c^2u_{xx}=0$, information travels along characteristic directions $x\pm ct$. A measurement at $x=0$ up to time $T$ cannot reveal an initial disturbance lying beyond the corresponding travel distance without further assumptions.

This suggests two requirements. The estimate should respect wave propagation, and its weighted integrals should remain manageable as $x\to\infty$.

The paper uses a logarithmic phase of the form

$$
\psi(t,x)=-\log(1+ct)-\log(1+x+ct).
$$

A further exponential weighting, with the signs and parameter range chosen in the proof, produces decay at spatial infinity. The combination is not just a convenient cutoff. Its derivatives must also make the integrated wave identity coercive and give the correct boundary terms.

A weight can decay beautifully and still be useless if those signs are wrong.

## What the AI contributed

The search for a weight is a constrained design problem: try functions whose derivatives fit the operator, then test the resulting inequalities. AI assistance helped identify a candidate compatible with those requirements.

The analytical work then establishes the admissible parameter regime and proves the weighted estimate and its consequences. The contribution is not an appeal to an opaque numerical guess, nor a claim that a language model's proposed formula is itself a proof.

What makes the candidate useful is that it survives the exact calculations.

## Recover only what the measurements can reach

One application reconstructs an unknown initial profile from endpoint observations for a semilinear wave equation. The reconstruction targets a finite depth compatible with the observation time, while leaving the more distant initial profile unknown.

Crucially, the target depth is not turned into a new physical boundary. No artificial boundary condition is imposed there. Weighted stability and a regularized iteration provide the reconstruction framework instead.

This keeps the computational question faithful to the unbounded geometry: estimate the part that can be informed by the data, without pretending that the rest of the world ends at the edge of the reconstruction window.

The wider idea is **to design the weight around the domain, rather than alter the domain to suit a familiar weight**. Whether similarly effective constructions exist for other unbounded geometries and propagation patterns is an inviting next question.

[^paper]: C. An, Y. Wang, Q. Ye, Z. Zhang and Q. Zhuang, *Carleman Estimates for Wave Equations on the Half-Line: AI-Assisted Weights and Applications*. [Preprint](https://arxiv.org/abs/2609.06283). See Section 2, including the phase in (2.2), and Section 5 for finite-depth reconstruction. This paper concerns deterministic wave equations.
