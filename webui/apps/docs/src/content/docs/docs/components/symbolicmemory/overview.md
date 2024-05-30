---
title: SymbolicMemory Overview
description: Overview of SymbolicMemory components
---

Abstract base class for a symbolic memory component within an agent.

This class defines the contract for symbolic memory operations such as starting
and stopping the memory service, and CRUD (Create, Read, Update, Delete) operations
on symbolic data. Implementations of this class are expected to manage collections
of symbols, providing a high-level interface to store and retrieve symbolic information.

## Builtins
* [LocalSymbolicMemory](/docs/components/symbolicmemory/localsymbolicmemory/)
* [MongoSymbolicMemory](/docs/components/symbolicmemory/mongosymbolicmemory/)