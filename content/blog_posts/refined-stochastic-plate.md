---
title: Why a Stochastic Plate Needs a Different Model
slug: refined-stochastic-plate
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: Late random fluctuations expose a difference between controlling momentum and controlling displacement.
kicker: Paper Notes
cover:
  image: /img/blog/refined-stochastic-plate.webp
  alt: A delicate translucent blue plate bends above a faint flat outline, with small warm accents at its boundary
    and interior.
  width: 1600
  height: 900
---

A plate has both a displacement and a momentum-like variable. In a deterministic model, these are tied together by a time derivative. Adding randomness only to the momentum equation may seem like the most natural extension.

But exact controllability asks a sharp question: can we produce an arbitrary admissible random terminal displacement as well as a terminal momentum?

A two-variable example shows why the placement of noise matters.[^paper]

## A random target can arrive too late

Consider

$$
dq=p\,dt,\qquad dp=g\,dW_t,\qquad q(0)=p(0)=0.
$$

Integrating gives

$$
q(T)=\int_0^T(T-s)g(s)\,dW_s.
$$

A noise increment arriving at time $s$ has only $T-s$ units of time to influence the displacement. To achieve the target $q(T)=W_T$, uniqueness of the stochastic-integral representation would require

$$
g(s)=\frac1{T-s},
$$

which is not square integrable.

This is not a small-control problem. It is a mismatch between where randomness enters and what the terminal target asks us to create.

## Give displacement its own stochastic channel

Now refine the first equation to

$$
dq=p\,dt+f\,dW_t.
$$

The particular displacement target $W_T$ is no longer obstructed: take $f=1$, $p=0$. This scalar example does not prove a plate theorem, but it reveals the modeling issue.

In the refined stochastic plate equation, the displacement and momentum-like equations both contain stochastic terms. Consequently the momentum-like variable should not be interpreted as an ordinary pathwise time derivative of the displacement.

The paper combines this refined model with two interior diffusion controls and two boundary controls, and proves exact controllability in the stated state spaces. It also analyzes limitations of the classical model and the roles of the control channels.

This is a four-control result. It would be misleading to describe it as a theorem saying that one local actuator can prescribe every random plate motion.

## The proof must see bending and randomness together

Plate dynamics involve fourth-order spatial derivatives. Their boundary information is more elaborate than that of a string, and the stochastic adjoint carries additional martingale components.

The proof develops a weighted identity suited to this structure and derives the observability estimate needed for duality. The refined stochastic channels are not decorative additions: they make the adjoint information required by the estimate correspond to available controls.

The broader lesson is that **controllability can test a stochastic model, not merely solve a problem inside it**. If the model puts all fresh randomness in the wrong channel, no clever boundary maneuver can automatically repair the mismatch.

Finding weaker or more localized control configurations is a further question. The first task is to give the model enough structure to make the desired random terminal states reachable at all.

[^paper]: Qi Lü and Yu Wang, *Exact controllability for a refined stochastic plate equation*, Chinese Annals of Mathematics, Series B 46 (2025), 415–442. [Paper](https://doi.org/10.1007/s11401-025-0023-2) · [Author version](https://arxiv.org/abs/2211.16730). See system (1.1) and the controllability and non-controllability results in Section 1. The two-variable calculation is an illustrative model.
