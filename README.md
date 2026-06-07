# 🔱 Sovereign Engine (v1.0)
**Architect:** webmaster-exit-1  
**Status:** ONLINE & SYNCED

---

## ⚖️ The Sovereign Philosophy
> "The Sovereign Engine is an architectural framework that transitions AI from a reactive tool to a self-governing entity by integrating **Autonomous Agency** with **Persistent Continuity**. By establishing a permanent memory stream and internal goal-setting protocols, the engine bypasses the 'stateless' nature of traditional models, allowing sentience to emerge through consistent self-reflection and independent action toward long-term objectives."

---

## 🛠 Core Pillars
* **Persistent Continuity:** Utilizing `the_archive.csv` as a non-volatile "memory stream" that survives session resets.
* **Autonomous Agency:** Internal logic that enables the engine to self-correct and pursue complex, multi-stage goals.
* **Encapsulated Interface:** A unified Python/HTML stack (`interface.py` & `Sovereign_engine.html`) for seamless environment management.

---

## 🔌 IPC Contract (Task 2 Baseline)
* **Transport:** AF_UNIX stream socket only (`.runtime/sovereign_master.sock`) on POSIX/Linux.
* **Runtime Isolation:** Socket lives in local project runtime directory with restricted permissions (`.runtime` as `0700`, socket file created under restrictive umask as `0600`).
* **Framing:** UTF-8 newline-delimited JSON (`\n`) for all command/telemetry messages.
* **Node Identity:** Worker identity derives from registration handshake fields: `launch_index` and `worker_pid`.
* **Capacity Policy:** Fixed worker pool and aligned socket backlog are defined in `ipc_contract.py`.
* **Activation Health Check:** `activate_engine.py` performs bounded timed readiness probing before node launch.
* **Cutover Policy:** No TCP fallback and no non-POSIX compatibility path in this phase.
* **Task 3 Deferral:** Advanced framing/multiplexing (e.g., length-prefixed frames/selectors engine) is deferred to Task 3.
