---
title: When Noise Preserves a Source’s History
slug: stochastic-drift-diffusion-point-sources
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: A stochastic integral can retain temporal information that an ordinary integral allows to cancel.
kicker: Paper Notes
cover:
  image: /img/blog/stochastic-drift-diffusion-point-sources.webp
  alt: Two tiny warm and teal source points inside a pale blue domain send different delicate ripples toward a highlighted
    boundary arc.
  width: 1600
  height: 900
---

Imagine a tiny heater hidden inside a material. One part of its output is a steady input; another fluctuates with Brownian noise. Boundary measurements record their diffused traces.

Which part should be harder to reconstruct?

It is tempting to answer “the random one.” Our point-source paper reveals a more interesting distinction: under its assumptions, the deterministic and stochastic source strengths obey markedly different stability estimates.[^paper]

## Averaging can erase a history

Forget space for a moment. Suppose a sensor records a weighted accumulation

$$
M_f=\int_0^T k(s)f(s)\,ds.
$$

Positive and negative contributions at different times can cancel. Many changes in $f$ may leave this single number unchanged.

Now consider the stochastic accumulation

$$
S_g=\int_0^T k(s)g(s)\,dW_s.
$$

Compare two candidates using the same Brownian motion. Itô's isometry gives

$$
\mathbb E|S_{g_1}-S_{g_2}|^2
=\int_0^T|k(s)|^2|g_1(s)-g_2(s)|^2\,ds.
$$

The temporal difference is squared before it is integrated. It cannot disappear by cancellation between different times.

This does not make every stochastic inverse problem stable: the sensor weight may be small, and spatial diffusion may obscure the source. But it explains why a random time signal can carry information that an averaged signal loses.

## Find the point, then recover what it emitted

In the PDE problem, each point source also has an unknown spatial location. Moving it changes the spatial pattern seen at the boundary; changing its intensity changes the temporal signal.

The proof separates and estimates these effects, using the equation's boundary-to-interior information and the distinct structures of drift and diffusion sources. For a single source of each type, the paper obtains Lipschitz stability for their locations, logarithmic stability for the drift intensity, and Lipschitz stability for the diffusion intensity, under the specified regularity and nondegeneracy conditions.

The multiple-source results require additional care, including separation and dimension-dependent statements. Several nearby sources cannot simply be treated as independent copies of one source.

## What “observing randomness” means here

The comparison uses random boundary trajectories in the paper's observation norm, including late-time information after the sources have stopped. It is not merely a comparison of probability distributions of isolated measurements.

That distinction matters. In the toy example, $S_g$ and $S_{-g}$ have the same distribution for deterministic $g$, so a distribution alone cannot recover the sign. Their trajectories driven by the same Brownian motion are different. The stability statement uses the richer observation framework, not a sign recovery from variance alone.

The central idea is **that temporal cancellation, rather than randomness by itself, can be the enemy of reconstruction**. How much of this advantage survives under weaker, more limited measurements is a natural question for further work.

[^paper]: Qi Lü and Yu Wang, *Stability Estimates for the Inverse Recovery of Drift and Diffusion Point Sources in Stochastic Parabolic Equations*. [Preprint](https://arxiv.org/abs/2609.14009). See Section 1 for the observation norm and the single- and multiple-source results. The two integral formulas above isolate one mechanism; they are not a replacement for the PDE stability proof.
