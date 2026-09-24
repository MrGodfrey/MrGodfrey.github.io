---
title: Seeing the Unseen in a Random World
slug: inverse-problems-stochastic-pdes
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: What can a boundary measurement reveal about a system whose evolution is random?
kicker: Book Notes
cover:
  image: /img/blog/inverse-problems-stochastic-pdes.webp
  alt: A translucent blue region contains a warm hidden source; a small opening in its boundary reveals delicate
    traces of the interior.
  width: 1600
  height: 900
---

A thermometer tells us what is happening where it is placed. An inverse problem asks it to tell us something about somewhere else: an inaccessible part of a material, an unknown initial temperature, or a hidden source.

Now let the temperature fluctuate randomly. Is the randomness merely interference—or does it carry information of its own?

That question runs through our book, *Inverse Problems for Stochastic Partial Differential Equations*.[^book]

## A tiny example: the average is not the whole signal

Consider a single quantity starting at zero:

$$
dX=f\,dt+g\,dW_t,
\qquad X(0)=0.
$$

Here $f$ and $g$ are fixed real numbers. At time $T$,

$$
\mathbb E X(T)=fT,
\qquad
\operatorname{Var}X(T)=g^2T.
$$

The average remembers the steady input $f$. The fluctuations remember the size of the random input $g$. Averaging is useful, but it also throws away part of the story. Even this toy model has a limit: the variance alone cannot distinguish $g$ from $-g$.

For a spatial equation, information must also travel. A source heats its neighborhood, diffusion spreads the heat, and measurements are collected somewhere else. A wave carries information with a finite travel time. The random structure can also change which unknowns these measurements determine.

## A wave source that cannot stay hidden

Consider a membrane fixed along its boundary, with displacement $z$ driven by a random force:

$$
dz_t-\Delta z\,dt=g(t,x)\,dW_t,
\qquad z|_{\partial G}=0.
$$

Here $W_t$ is Brownian motion and $g$ is the unknown force intensity. Under the book's geometric and observation-time assumptions, the boundary slope $\partial_\nu z$ on a suitable part of the boundary, together with the final displacement $z(T)$, uniquely determines $g$ and both initial displacement and velocity.[^wave] The data are the random observations themselves, beyond just their averages.

Compare this with an ordinary wave equation:

$$
u_{tt}-\Delta u=f(t,x).
$$

Choose a nonzero smooth motion $u$ that vanishes near the boundary and near both $t=0$ and $t=T$. Set $f=u_{tt}-\Delta u$. This nonzero force produces motion inside, yet both the boundary slope and final displacement vanish. These measurements cannot determine an arbitrary $f$.

The stochastic equation has extra structure. Itô's formula contributes a positive term involving $g^2$, which the weighted estimate uses to bound the unknown source. This gives a uniqueness result that fails for an unrestricted deterministic force. Randomness itself changes what can be recovered.

## Turn the question around

The useful starting point is often not “How do we reconstruct the unknown?” but “Could two different unknowns produce almost the same measurements?”

Subtract their equations. The reconstruction problem becomes a question about whether a solution can hide from our sensors.

A Carleman estimate attacks this question by weighting the equation unevenly in space and time. The weight acts like a mathematical spotlight: after the equation has been used, quantities inside the domain can be bounded by observations and controlled remainders. In a stochastic equation, Itô's formula contributes additional terms that must be included rather than discarded.

This is where uniqueness becomes quantitative. Proving that identical data imply identical unknowns is one thing. Estimating how much the unknown can change when the data change a little is considerably more useful.

## From an estimate to a reconstruction

There is still a practical obstacle. An unstable inverse problem can fit measurement noise extremely well. Regularization asks for more than a good fit: it also penalizes implausibly large or irregular reconstructions. The estimates then explain when, and in what sense, the reconstructed quantity approaches the true one as the noise and regularization are reduced.

The book develops this progression for selected stochastic heat and wave problems: identify what the measurements can see, quantify that information, and use it in reconstruction. It is not a claim that every hidden coefficient or source can be recovered from every observation.

The central lesson is simple: **randomness can carry information and change what an inverse problem allows us to recover.** Choosing what to measure is part of making that information useful.

[^book]: Qi Lü and Yu Wang, *Inverse Problems for Stochastic Partial Differential Equations*, SpringerBriefs on PDEs and Data Science, 2026. [Book](https://doi.org/10.1007/978-981-95-9047-6) · [Author version](https://arxiv.org/abs/2411.05534). Chapters 2–3 develop the parabolic and hyperbolic problems; the scalar model above is an illustration, not a theorem from the book.

[^wave]: See Section 3.1.2, Theorem 3.4.1 and Remark 3.4.2 in the [author version](https://arxiv.org/html/2411.05534v1#S3.S4). The displayed stochastic equation is a special case with the lower-order coefficients and drift source set to zero. Uniqueness compares solutions driven by the same Brownian motion, with equality of their observations almost surely. The deterministic example follows Remark 3.4.2.
