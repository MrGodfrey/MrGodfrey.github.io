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

For a spatial equation, information must also travel. A source heats its neighborhood, diffusion spreads the heat, and measurements are collected somewhere else. A wave carries information differently, with a finite travel time. What can be reconstructed therefore depends on both the randomness and the geometry of observation.

## Turn the question around

The useful starting point is often not “How do we reconstruct the unknown?” but “Could two different unknowns produce almost the same measurements?”

Subtract their equations. The reconstruction problem becomes a question about whether a solution can hide from our sensors.

A Carleman estimate attacks this question by weighting the equation unevenly in space and time. The weight acts like a mathematical spotlight: after the equation has been used, quantities inside the domain can be bounded by observations and controlled remainders. In a stochastic equation, Itô's formula contributes additional terms that must be included rather than discarded.

This is where uniqueness becomes quantitative. Proving that identical data imply identical unknowns is one thing. Estimating how much the unknown can change when the data change a little is considerably more useful.

## From an estimate to a reconstruction

There is still a practical obstacle. An unstable inverse problem can fit measurement noise extremely well. Regularization asks for more than a good fit: it also penalizes implausibly large or irregular reconstructions. The estimates then explain when, and in what sense, the reconstructed quantity approaches the true one as the noise and regularization are reduced.

The book develops this progression for selected stochastic heat and wave problems: identify what the measurements can see, quantify that information, and use it in reconstruction. It is not a claim that every hidden coefficient or source can be recovered from every observation.

The central lesson is simple: **in a random system, deciding what counts as data is already part of solving the inverse problem.**

[^book]: Qi Lü and Yu Wang, *Inverse Problems for Stochastic Partial Differential Equations*, SpringerBriefs on PDEs and Data Science, 2026. [Book](https://doi.org/10.1007/978-981-95-9047-6) · [Author version](https://arxiv.org/abs/2411.05534). Chapters 2–3 develop the parabolic and hyperbolic problems; the scalar model above is an illustration, not a theorem from the book.
