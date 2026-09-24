---
title: Finding Cell Families from Incomplete Portraits
slug: scdcl-cell-families
template: paper_post
date: '2026-09-24'
lang: en
math: true
listed: true
excerpt: Denoise first, then let individual cell profiles and the geometry between cells inform each other.
kicker: Paper Notes
cover:
  image: /img/blog/scdcl-cell-families.webp
  alt: Small translucent cells form three loose blue, teal and amber families, with a few fine connections suggesting
    shared structure.
  width: 1600
  height: 900
---

Suppose you are asked to sort portraits into families, but many of their features are missing. Looking at each portrait alone wastes the resemblance between relatives. Looking only at who resembles whom can make an early mistake spread through the whole collection.

This is a useful way to think about clustering single-cell RNA sequencing data. Each cell comes with a long vector of gene counts, and many entries are zero. A zero can be biologically meaningful; it can also reflect limitations of measurement. The clustering method has to work with that ambiguity.[^paper]

## Do not build the neighborhood too soon

As a toy example, compare the count vectors $(5,5,0)$ and $(5,0,0)$. Their difference might separate two cell types—or it might be an incomplete observation of otherwise similar cells. Three numbers cannot decide. The point is that a graph built immediately from noisy counts may turn an uncertain comparison into a firm neighborhood connection.

Once a graph neural network starts sharing information along that connection, the initial mistake can influence other representations.

The first choice in scDCL is therefore **denoise, then build the graph**. A masked autoencoder learns a representation using a count model designed to accommodate sparsity and overdispersion. It tries to extract a useful cell portrait before deciding which portraits belong near each other.

## A portrait and a map tell different stories

Even a better portrait is not the whole answer. Imagine cells arranged along a curved developmental trajectory. Nearby cells reveal local similarity, but the shape of the trajectory contains information that isolated pairwise distances may miss.

scDCL constructs two kinds of graph from the learned representations: a nearest-neighbor graph and a diffusion-map graph. The first emphasizes local neighborhoods; the second contributes a broader view of connectivity. Graph-based filtering and graph neural networks then produce several representations of the same cells.

These are constructed views of one dataset, not four independently measured biological modalities.

## Make the views agree without making everything identical

A useful representation needs two properties at once. Different views of the same underlying structure should remain consistent. At the same time, meaningful differences between cells and clusters should not disappear.

The dual contrastive objective combines these aims: it improves discrimination within representations while encouraging consistency between them. The refined views are combined, and clustering is performed on the resulting embedding.

The interesting part is the order and interaction of the steps. Denoising protects graph construction; graphs supply relationships missing from isolated portraits; the learning objectives prevent those relationships from erasing individuality.

The paper evaluates this combination on benchmark datasets. Such experiments test a clustering method, not the biological truth of every inferred group. Robustness to new tissues, measurement protocols and rare cell populations remains an important question.

The central idea is modest but powerful: **understand a cell both by its own features and by where it sits among other cells—and do not let the noisiest measurements decide the map too early.**

[^paper]: Lin Gan, Hua Meng, Yuxu Chen and Yu Wang, *scDCL: A multi-view single-cell RNA sequencing clustering method based on dual contrastive learning*, Computational Biology and Chemistry 123 (2026), 108998. [Paper](https://doi.org/10.1016/j.compbiolchem.2026.108998). See Section 2 for the denoise-then-graph pipeline and dual contrastive learning. The portrait analogy and three-gene example are explanatory illustrations.
