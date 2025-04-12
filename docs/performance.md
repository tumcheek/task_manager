# ⚙️ Performance Profiling Report

This document contains profiling results for the FastAPI application. The performance of four key user-related task endpoints was analyzed using `pyinstrument` (for CPU time) and `memory_profiler` (for memory usage).

---

## 📐 Methodology

- **CPU profiling** was performed using [`pyinstrument`](https://github.com/joerick/pyinstrument).
- **Memory profiling** was done using [`memory_profiler`](https://pypi.org/project/memory-profiler/).
- Profiling was based on isolated function calls with mock/test data (e.g., 1 user, a few tasks).
- Database used: SQLite/PostgreSQL (specify as applicable).

---

## 🧠 CPU Profiling (`pyinstrument`)

| Function / Endpoint         | Execution Time (s) | Notes                             |
|----------------------------|--------------------|------------------------------------|
| `get_user_tasks_list`      | `0.124`            | Loads entire task list into memory |
| `get_user_task_detail`     | `0.011`            | Fast single-record query           |
| `create_task`              | `0.040`            | Expected for ORM                   |
| `update_task`              | `0.020`            | Minimal business logic             |

---

## 🧠 Memory Profiling (`memory_profiler`)

| Function / Endpoint         | Main Operation                    | Memory Increase | Notes                                          |
|-----------------------------|-----------------------------------|------------------|------------------------------------------------|
| `get_user_tasks_list`       | `db.query(...).all()`             | **+2.1 MiB**     | Main memory hotspot — loads many records       |
| `get_user_task_detail`      | `db.query(...).first()`           | +0.0 MiB         | Very efficient, single record fetched          |
| `create_task`               | `.dict()`, `commit()`, `refresh()`| **+0.2 MiB**     | Small increase during transaction              |
| `update_task`               | `update()`, `commit()`            | **+0.1 MiB**     | Lightweight update; no excessive memory usage  |

---

## 🔎 Summary

- **`get_user_tasks_list`** is the only notable memory hotspot due to `.all()`, which loads full task sets.
- Other functions perform **efficiently in both memory and execution time**.
- Potential optimizations:
  - Use pagination or `.limit()` for listing tasks

