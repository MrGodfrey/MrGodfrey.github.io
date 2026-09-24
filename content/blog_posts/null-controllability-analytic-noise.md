---
title: Why One Control Can Be Enough for a Stochastic Heat Equation
slug: null-controllability-analytic-noise
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: Two exponentials turn an unobserved stochastic coupling into a closed analytic energy estimate.
kicker: Paper Notes
cover:
  image: /img/blog/null-controllability-analytic-noise.webp
  alt: A cool blue circular heat domain has a short amber control arc, with delicate fluctuations around the ring
    becoming a calm continuous outline.
  width: 1600
  height: 900
---

Can a control acting on a small arc bring an entire noisy temperature profile exactly to zero?

Consider the stochastic heat equation on a circle:

$$
dy=(y_{xx}+\mathbf1_Gu)\,dt+\cos x\,y\,dW_t.
$$

The control acts only in the drift and can use only information already available. Our paper proves that one such control is enough.[^paper] The cosine is a small example with the genuine difficulty: the noise coefficient depends on space.

## An unknown that will not stay in its own frequency

The adjoint equation has two unknowns,

$$
dz=-(z_{xx}+\cos x\,Z)\,dt+Z\,dW_t.
$$

One drift control calls for an estimate observing only $z$ on $G$. Familiar stochastic Carleman arguments generally retain a term involving $Z$. Spectral arguments encounter another obstruction:

$$
\cos x\,e^{ikx}
=\tfrac12e^{i(k-1)x}+\tfrac12e^{i(k+1)x}.
$$

A mode outside a frequency cutoff can feed into the retained modes through the unobserved $Z$. The projected equation no longer closes as it does for spatially constant noise.

## The first exponential: move into complex space

Write $D=-i\partial_x$. Applying $e^{\sigma D}$ multiplies the $k$th Fourier mode by $e^{\sigma k}$—equivalently, it translates $x$ to $x-i\sigma$.

Work first with finite Fourier approximations, leaving their projections implicit. Set $X=e^{\sigma D}z$ and $Y=e^{\sigma D}Z$. The coupling becomes

$$
e^{\sigma D}(bZ)=b_\sigma Y,
\qquad b_\sigma(x)=\cos(x-i\sigma).
$$

For $|\sigma|\le\rho$, the coefficient is bounded by $\cosh\rho$. The weighted unknown $Y$ may be huge; the important point is that it appears with a bounded multiplier.

On an interval $[t,s]$, choose $\sigma(r)=\rho(s-r)/(s-t)$. The translation measures an analytic norm at $t$ but vanishes at $s$. Ordinary square-integrable terminal data are therefore enough.

## The second exponential: pay for what remains

Itô's formula contributes a positive $\|Y\|^2$. Together with the coupling, it gives

$$
\|Y\|^2-2\operatorname{Re}\langle X,b_\sigma Y\rangle
=\|Y-\overline{b_\sigma}X\|^2-\|b_\sigma X\|^2.
$$

Now $Y$ is inside a nonnegative square. The negative remainder involves only $X$. The moving translation creates one more state-only loss, controlled by $|\sigma'|^2\|X\|^2/2$ using the Laplacian.

Both losses are compensated by the time weight $\Gamma(r)=e^{a(r-t)}$, where $a=\cosh^2\rho+\rho^2/[2(s-t)^2]$. Integrating and taking expectations gives

$$
\mathbb E\|e^{\rho D}z(t)\|^2
\le e^{a(s-t)}\mathbb E\|z(s)\|^2.
$$

The opposite translation handles the other Fourier direction. Passing to the limit gives quantitative spatial analyticity of $z$, without assuming analyticity of $Z$.

## From a local arc to the whole circle

View the analytic state as taking values in $L^2(\Omega)$. Propagation of smallness transfers a local observation, together with the analytic bound, to a global estimate. A telescoping argument in time removes the intermediate global norms. Only the observation of $z$ remains; duality supplies the single drift control.

The full result allows higher-dimensional tori and random time-dependent coefficients with a common analytic strip and a pathwise uniform time-integrability bound. General smooth coefficients and domains with boundary require different arguments.

The two exponentials have distinct jobs: **the spatial one keeps the coupling usable; the temporal one compensates for the losses left after the stochastic unknown has been put into a positive square.**

[^paper]: Qi Lü and Yu Wang, *Null Controllability of a Stochastic Parabolic Equation with a Space-Dependent Analytic Noise Coefficient*, manuscript. Section 2 contains the analytic energy estimate; Sections 3–4 establish propagation, observability and duality; Section 6 discusses the method's scope. This post uses its one-dimensional cosine example to explain the mechanism.
