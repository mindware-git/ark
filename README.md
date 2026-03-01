# ark

**AI-Driven Solver-Aided Design Language**

ark is a hierarchical, solver-validated design language built for AI-driven iterative modeling.

It is designed around a simple idea:

High-level semantic design intent is written as code.  
Precise validation is delegated to a constraint solver.  
Structured errors guide automatic refinement.

ark is not a traditional CAD library.  
It is a design compiler framework optimized for LLM-driven development loops.

---

## Core Principles

ark is built on four foundational layers:

### 1. Hierarchy  
Designs are structured as hierarchical models.  
Each group encapsulates geometry and constraints, enabling scoped reasoning and editability.

### 2. Semantics  
Objects can carry semantic meaning beyond raw geometry.  
This allows AI systems to reason at a higher abstraction level.

### 3. Dependency  
Relationships between elements are explicitly declared.  
Dependencies reference previously defined geometry without requiring manual coordinate reasoning.

### 4. Constraint  
All geometric relationships are validated through explicit constraints.  
The solver ensures determinism and precision while code defines values.

---

## Design Philosophy

- Code defines values.
- The solver validates constraints.
- Errors and warnings include exact file and line references.
- LLMs refine code through structured feedback loops.
- High-level models are progressively lowered into validated geometry.

ark is designed to evolve from 2D fabrication workflows to full 3D and BIM systems.

---

## Vision

Design as code.  
Validate with solvers.  
Iterate with AI.

