---
title: Guidlines for avoid race conditions
date: 2020-06-10 00:31:32
categories:
 - Unity
tags:
 - Unity
---

- Don't call methods in  `Awake()`

Well we do call some methods in `Awake()`, but we never call any methods that are on `MonoBehaviours` or `ScriptableObjects` . These two types both themselves have `Awake()` methods. We use `Awake()` exclusively for setting up ourselves with data that we already have.

- All state should be safe to access by `Start()`

That means that we would need to be really careful we need to check all uses of variables that are initialized in `Start()`.