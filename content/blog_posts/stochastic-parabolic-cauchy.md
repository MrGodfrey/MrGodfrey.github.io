---
title: Reconstructing Heat Through a Narrow Window
slug: stochastic-parabolic-cauchy
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: Small boundary errors can hide large interior changes. A conditional estimate makes reconstruction meaningful.
kicker: Paper Notes
cover:
  image: /img/blog/stochastic-parabolic-cauchy.webp
  alt: A warm interior glow is seen through a narrow opening in the edge of a translucent cool-blue material.
  width: 1600
  height: 900
---

Suppose you can measure temperature and heat flux on an accessible part of a material's boundary, but you do not know the temperature inside. Can you reconstruct it?

For a forward heat problem, initial and boundary data drive the solution. Here the direction of reasoning is different: incomplete boundary observations must reveal an unknown interior state. This is a Cauchy inverse problem—and its instability is already visible without randomness.[^paper]

## Tiny at the boundary, large inside

Consider the exact heat-equation solution

$$
u_k(t,x)=e^{k(x-a)}\cos(kx+2k^2t),\qquad a>0.
$$

It satisfies $u_t=u_{xx}$. At the observed boundary $x=0$, both the temperature and its spatial derivative become exponentially small as $k$ grows. At the interior location $x=a$, the oscillation still has amplitude one.

Thus very small boundary signals can conceal an appreciable interior state. No reconstruction method can remove this instability simply by fitting the measured data more accurately.

The example has increasingly large gradients. An a priori bound on the solution is therefore not an incidental technical assumption: it restricts the very behavior that makes the problem unstable.

## Ask for conditional stability

Our paper studies a stochastic parabolic Cauchy problem. Its estimate controls the solution in an interior subdomain and away from the initial and final times, using the observation error together with an a priori bound.

A Carleman weight supplies the bridge between those boundary and interior quantities. The stochastic terms are retained in the weighted calculation, so the estimate concerns the random solution rather than only its expectation.

The resulting stability is conditional and of Hölder type. It is not a claim that arbitrarily small, noisy boundary data determine the entire space–time solution with a uniform Lipschitz constant.

## Do not let the reconstruction chase every fluctuation

The numerical counterpart is regularization. A candidate solution should match the observations and the equation, but it should also pay a penalty for being excessively irregular.

Tikhonov regularization balances these requirements. The paper establishes a well-defined minimization problem and convergence estimates, then develops a numerical reconstruction using suitable kernel representations.

The regularization parameter is not merely a knob for making a plot look smoother. It encodes the compromise between trusting the measurements and preventing the hidden amplification illustrated by $u_k$.

The central idea is **to quantify instability before trying to compute through it**. Once an estimate says which interior quantities remain recoverable under which bounds, an algorithm can be designed around a meaningful target.

Reconstructing closer to inaccessible boundaries or time endpoints, or under weaker prior information, asks more of the data. Those are extensions to investigate, not consequences that should be inferred from an interior conditional estimate.

[^paper]: Fangfang Dou, Peimin Lü and Yu Wang, *Stability and regularization for ill-posed Cauchy problem of a stochastic parabolic differential equation*, Inverse Problems 40 (2024), 115005. [Paper](https://doi.org/10.1088/1361-6420/ad7f80) · [Author version](https://arxiv.org/abs/2308.15741). See Theorem 2.1, Section 3 on regularization and Section 4 on reconstruction. The oscillatory heat solution is an explanatory example.
