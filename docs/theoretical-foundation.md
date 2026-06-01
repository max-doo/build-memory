# Lightweight Externalized Memory Architecture for LLM Agents: A Comparative Study and Evaluation Plan

**Abstract**  
As Large Language Models (LLMs) transition from single-turn assistants to autonomous agents executing multi-session software engineering tasks, the need for persistent memory mechanisms has become paramount. While mainstream frameworks (e.g., Hermes, Claude Code, Codex) employ complex tiered memory systems, full-text search, and automated background summarization, these architectures can introduce opacity and non-determinism into the development workflow. This paper presents `build-memory`, a lightweight, file-based external memory architecture. We review the theoretical foundations of LLM memory, conduct a comparative analysis of mainstream agent memory systems, and articulate the rationale for a transparent, version-controlled approach. Finally, we propose a systematic evaluation plan to benchmark the effectiveness of this lightweight architecture based on recent agentic memory metrics.

---

## 1. Introduction
The inherent statelessness of current LLMs poses a significant bottleneck for agents engaged in long-horizon tasks. In multi-agent software engineering, this "AI amnesia" manifests as a loss of project context, repetitive debugging of known issues, and "context rot" within the active session window. 

Recent literature demonstrates that simply expanding the theoretical Maximum Context Window (MCW) is insufficient. Studies on "attentional dilution" and the "Lost in the Middle" phenomenon reveal that as context grows, retrieval accuracy for information in the middle of the prompt degrades significantly [4], [7]. To bridge this gap, Context Engineering and Harness Engineering have emerged as crucial disciplines for orchestrating LLM memory. 

The `build-memory` project introduces a highly deterministic, file-based memory layer (`AGENTS.md`, `SESSION_LOG.md`, `KNOWLEDGE.md`). This paper contextualizes this architecture within current academic literature and industry practices, explaining why a lightweight system is often preferable for project-level orchestration.

## 2. Comprehensive Literature Review on Agent Memory
Recent research has formalized the categorization and mechanics of LLM memory.

**2.1 Virtual Context Management and Semantic Memory**  
Packer et al. [1] introduced **MemGPT**, advocating for "virtual context management." By treating the LLM like an operating system, MemGPT pages information between a limited context window (RAM) and external storage (Disk). This ensures the context window only contains high-signal information. Similarly, **MemoryBank** [2] demonstrated how LLMs can mimic the Ebbinghaus Forgetting Curve to synthesize interactions into long-term semantic knowledge, evolving the agent's understanding over time.

**2.2 Taxonomies of Memory Modules**  
A comprehensive survey by Zhang et al. [3] categorizes LLM memory into *parametric* (model weights), *contextual* (the active prompt window), and *external* (persistent outside the model). External memory is further divided by its structure (vector databases vs. knowledge graphs vs. raw text). Another 2025 survey by D. Zhang et al. [5] proposes a "memory quadruple" framework (storage location, persistence, write/access path, and controllability), emphasizing that the "write/access path" must be highly controllable for reliable agentic performance.

**2.3 Memory in Software Engineering Agents**  
In software engineering, memory is often formalized as a "write–manage–read" loop [3], [5]. Rather than passively recalling facts, agents must structure knowledge. Tools like **StructMemEval** [9] evaluate an agent's ability to maintain structured memories (e.g., trees, ledgers, to-do lists), which aligns precisely with the goal of maintaining a `TODO.md` and chronological `SESSION_LOG.md`.

## 3. Comparative Analysis of Mainstream Agent Memory Systems
To situate `build-memory`, we must analyze how leading industry tools handle persistent state.

**3.1 Hermes (Nous Research)**  
Hermes implements a heavily engineered, multi-tier memory system [10]. Its "Brain" layer relies on frozen snapshot files (`MEMORY.md`, `USER.md`) that are injected into every prompt. For deep history, it utilizes a SQLite database with FTS5 (Full-Text Search) to query past decisions. While powerful, this dual-layer approach obscures memory from the user, as the SQLite database is not easily version-controllable or human-readable. Furthermore, its automated skill generation loop requires complex orchestration to prevent hallucinated rules from permanently polluting the agent's memory [10].

**3.2 Claude Code (Anthropic)**  
Claude Code employs active in-session context compaction to prevent "context rot" [11]. For persistence, it heavily relies on user-provided static files (e.g., `CLAUDE.md`) and a background "Auto Memory" system that logs preferences to a local directory. While the static `CLAUDE.md` provides excellent deterministic grounding, the automated background notes can sometimes lead to redundant or conflicting rules if not actively curated by the developer [11].

**3.3 OpenAI Codex (CLI/IDE)**  
Codex blends static instructions with contextual observation [12]. It performs a repository walk to find `AGENTS.md` files, ensuring base rules are loaded. It supplements this with an automated "Memories" feature that summarizes past threads into hidden local files (`~/.codex/memories/`), and a "Chronicle" extension that reads screen context. The reliance on opaque background summarization means developers often lack immediate visibility into *why* Codex made a specific architectural assumption [12].

## 4. The `build-memory` Architecture: A Rationale for Lightweight Design
In contrast to the complex, database-backed, or opaque background-summarization approaches, `build-memory` adopts a **lightweight, transparent, file-based architecture**. 

### 4.1 Rationale Against Complex Architectures
For project-level software engineering, relying on local SQLite databases or complex vector stores introduces significant friction:
1. **Opacity:** Developers cannot easily review, edit, or pull-request a vector embedding or a hidden SQLite row. 
2. **Version Control:** Project memory should live and branch with the code. A shared `SESSION_LOG.md` tracked via Git ensures that any developer (or agent) checking out a branch immediately possesses the historical context of *that specific branch*.
3. **Determinism (Harness Engineering):** Automated background summarization is non-deterministic. `build-memory` enforces a strict harness via `.memory/session_log.py`, requiring explicit logging of decisions. This ensures that memory updates are deliberate, high-signal, and auditable.

### 4.2 Mapping to Cognitive Architecture
*   **Semantic / Baseline Memory:** `AGENTS.md` and `CLAUDE.md` serve as the frozen snapshot (similar to Hermes' Brain layer), providing single-source-of-truth project rules [1], [10].
*   **Episodic Memory:** `SESSION_LOG.md` acts as the chronological trace of debugging efforts, acting as the explicit structured ledger evaluated by frameworks like StructMemEval [9].
*   **Working Memory / Executive Function:** `TODO.md` dictates immediate task focus, aligning the agent with human intent.
*   **Long-Term Condensed Knowledge:** `.memory/KNOWLEDGE.md` acts as the analog to MemoryBank's evolved understanding, storing abstracted, durable lessons [2].

## 5. Limitations and Research Plan for Systematic Evaluation
While the architecture ensures transparency and Git compatibility, its lightweight nature introduces limitations that must be rigorously tested.

**5.1 Limitations and Vulnerabilities**  
1. **Manual Triggering:** Unlike systems that automatically update memory, `build-memory` relies on the agent proactively calling the `session_log.py` script. If the agent crashes or fails to execute the script before session termination, episodic memory is lost.
2. **Context Window Limitations and Retrieval Degradation:** As `SESSION_LOG.md` and `KNOWLEDGE.md` grow, loading them entirely into the context window will eventually trigger the "Lost in the Middle" degradation [4]. Without a dynamic retrieval mechanism, a monolithic text file scales poorly.
3. **Lack of Automated Condensation:** The architecture currently lacks a formalized mechanism to periodically condense sprawling episodic memory (`SESSION_LOG.md`) into refined semantic rules (`KNOWLEDGE.md`). This places the burden of memory maintenance entirely on the agent's unstructured reasoning.
4. **Concurrency in Multi-Agent Environments:** A pure file-based approach introduces race conditions. If multiple agents operate concurrently on different branches or threads, simultaneous writes to `SESSION_LOG.md` or `KNOWLEDGE.md` without file-locking mechanisms will lead to data corruption or overwrites.

**5.2 Proposed Evaluation Plan**  
To validate the efficacy of the `build-memory` system, we propose a systematic evaluation benchmark derived from recent literature, specifically **MemoryAgentBench** [8] and **MemBench** [6]. The evaluation will assess the system across four core competencies:

1.  **Effectiveness (Accurate Retrieval):**  
    *Metrics:* Task Success Rate in a simulated debugging environment [6].  
    *Method:* Introduce a bug that was previously encountered and documented in `SESSION_LOG.md`. Measure the agent's time-to-resolution and whether it successfully bypasses known "gotchas" referenced in the log.
2.  **Long-Range Understanding & Test-Time Learning:**  
    *Metrics:* Causal Accuracy and Dialogue Consistency [8].  
    *Method:* Execute a 10-session refactoring task. Measure the agent's ability to maintain architectural consistency across sessions solely by reading the generated `TODO.md` and `SESSION_LOG.md`.
3.  **Selective Forgetting and Conflict Resolution:**  
    *Metrics:* Rule Adherence Rate under contradictory conditions [8].  
    *Method:* Intentionally inject an outdated architectural rule into `KNOWLEDGE.md`, while providing an updated, overriding rule in `AGENTS.md`. Evaluate if the agent correctly prioritizes the static instruction file over the legacy memory.
4.  **Harness Efficiency:**  
    *Metrics:* Temporal Efficiency and Token Overhead [6].  
    *Method:* Measure the token consumption and script latency of loading the 5-file architecture versus a dynamic vector-search approach, evaluating the "signal-to-token" ratio.

## 6. Conclusion
The `build-memory` architecture demonstrates that effective Context Engineering does not strictly require complex databases or opaque background summarization. By externalizing the agent's semantic, episodic, and working memory into plain-text, version-controlled files, the system transforms stateless LLMs into reliable engineering partners. Future systematic evaluations will quantify the boundary where this lightweight approach necessitates integration with dynamic compaction techniques.

---

## References

[1] C. Packer, V. Fang, S. G. Patil, K. Lin, S. Wooders, and J. E. Gonzalez, "MemGPT: Towards LLMs as Operating Systems," *arXiv preprint arXiv:2310.08560*, 2023. Available: [https://arxiv.org/abs/2310.08560](https://arxiv.org/abs/2310.08560)

[2] W. Zhong, L. Guo, Q. Gao, H. Ye, and Y. Wang, "MemoryBank: Enhancing Large Language Models with Long-Term Memory," *arXiv preprint arXiv:2305.10250*, 2023. Available: [https://arxiv.org/abs/2305.10250](https://arxiv.org/abs/2305.10250)

[3] Z. Zhang *et al.*, "A Survey on the Memory Mechanism of Large Language Model based Agents," *arXiv preprint arXiv:2404.13501*, 2024. Available: [https://arxiv.org/abs/2404.13501](https://arxiv.org/abs/2404.13501)

[4] N. F. Liu *et al.*, "Lost in the Middle: How Language Models Use Long Contexts," *arXiv preprint arXiv:2307.03172*, 2023. Available: [https://arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

[5] D. Zhang *et al.*, "Memory in Large Language Models: Mechanisms, Evaluation and Evolution," *arXiv preprint arXiv:2509.18868*, 2025. Available: [https://arxiv.org/abs/2509.18868](https://arxiv.org/abs/2509.18868)

[6] H. Tan *et al.*, "MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents," *arXiv preprint arXiv:2506.21605*, 2025. Available: [https://arxiv.org/abs/2506.21605](https://arxiv.org/abs/2506.21605)

[7] Y. Wu *et al.*, "From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs," *arXiv preprint arXiv:2504.15965*, 2025. Available: [https://arxiv.org/abs/2504.15965](https://arxiv.org/abs/2504.15965)

[8] Y. Hu *et al.*, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions," (MemoryAgentBench), *arXiv preprint arXiv:2507.05257*, 2025. Available: [https://arxiv.org/abs/2507.05257](https://arxiv.org/abs/2507.05257)

[9] A. Shutova *et al.*, "Evaluating Memory Structure in LLM Agents," (StructMemEval). [Online]. Available: [https://github.com/yandex-research/StructMemEval](https://github.com/yandex-research/StructMemEval)

[10] Nous Research, "Hermes Agent Framework Documentation and Architecture," 2024. [Online]. Available: [https://github.com/NousResearch/Hermes](https://github.com/NousResearch/Hermes)

[11] Anthropic, "Claude Code Context Management and Persistent Memory," Anthropic Documentation, 2025. [Online]. Available: [https://docs.anthropic.com/en/docs/agents-and-tools/claude-code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code)

[12] OpenAI, "Codex Agent Memory and Workspace Configuration," OpenAI Developer Guides, 2025. [Online]. Available: [https://platform.openai.com/docs/guides/codex](https://platform.openai.com/docs/guides/codex)
