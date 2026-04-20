# FaultLab API
### Deterministic API Failure Testing & Reliability Scoring System

FaultLab API is a backend reliability intelligence module built to evaluate how APIs behave when they are pushed beyond the happy path.

Instead of only testing whether an endpoint works when everything is correct, FaultLab focuses on what happens when requests are incomplete, malformed, logically invalid, or missing protocol context. The result is a deterministic, explainable, and production-oriented approach to API robustness testing.

---

## 🌍 Project Overview

FaultLab API represents the **Person-2** layer of the broader FaultLab system.

Its role is to act as the reliability analysis engine that:

- generates deterministic failure variants
- validates whether APIs react correctly
- computes a reliability score
- produces structured JSON reports
- exposes metrics for visibility and monitoring

This project is designed like a serious backend engineering portfolio project: modular, testable, CI-ready, and easy to reason about.

---

## ✨ Features

- Deterministic failure injection for repeatable API robustness testing
- Clear validation rules for normal and failure-injected responses
- Reliability Diagnostic Index (RDI) scoring model
- JSON report generation for downstream analysis
- Prometheus-ready observability metrics
- Dockerized verification flow
- GitHub Actions CI pipeline for automated test checks

---

## 🧪 Failure Injection Engine

At the heart of FaultLab API is a deterministic failure testing strategy.

Traditional testing often focuses on valid requests only. FaultLab goes further by intentionally mutating requests in controlled ways to observe whether the target API fails safely and predictably.

### Supported deterministic failure types

- `missing_field`
  Removes one field from the JSON payload to simulate incomplete client input.
- `invalid_type`
  Changes a field value to the wrong type to simulate schema or contract violations.
- `semantic_error`
  Keeps the payload shape intact but injects logically invalid data such as negative numeric values.
- `protocol_error`
  Removes request headers to simulate malformed HTTP usage or missing authentication/content negotiation context.

### Why deterministic failure testing matters

Deterministic failure testing means the same input always produces the same mutated cases.

That matters because it gives teams:

- reproducible failures across local runs and CI
- consistent evaluation of API resilience
- easier debugging and comparison between changes
- confidence that reliability scoring is not influenced by randomness

---

## 🔍 Response Validation

FaultLab API separates validation into two clear modes:

### Normal request validation

If the request is a valid baseline request:

- `status_code < 400` → pass

This confirms the API still handles legitimate traffic correctly.

### Failure-injected request validation

If the request contains an injected fault:

- `status_code >= 400` → pass

This confirms the API correctly rejects malformed or invalid input instead of accepting it silently.

The validation layer is intentionally simple and transparent so the scoring model remains easy to audit.

---

## 📊 Reliability Diagnostic Index (RDI)

FaultLab API computes a reliability score called the **Reliability Diagnostic Index (RDI)**.

It combines multiple signals into one evaluative metric:

- **FCS**: Functional Correctness Score
- **FRS**: Fault Rejection Score
- **FIS**: Flow Integrity Score
- **LSS**: Latency Stability Score

### Formula

```text
RDI =
0.35 * FCS +
0.35 * FRS +
0.20 * FIS +
0.10 * LSS
```

### What the score represents

- A high **FCS** means valid traffic is handled reliably
- A high **FRS** means invalid traffic is rejected correctly
- **FIS** and **LSS** provide additional reliability context

This gives teams a compact but meaningful signal for API robustness instead of relying only on pass/fail counts.

---

## 📄 Structured JSON Reporting

After test execution and scoring, FaultLab API generates a machine-readable report:

```json
{
  "project": "FaultLab",
  "tests_run": 0,
  "tests_passed": 0,
  "tests_failed": 0,
  "reliability_score": 0.0,
  "metrics": {},
  "failure_breakdown": {}
}
```

The report is saved as:

```text
faultlab_report.json
```

This makes the module useful for:

- CI artifacts
- dashboards
- audit trails
- integration with upstream systems like Person-1

---

## 📡 Observability Metrics

Reliability engineering is stronger when it is measurable.

FaultLab API includes Prometheus-style metrics for:

- `tests_total`
- `tests_failed`
- `api_latency_seconds`

These metrics help track:

- how much reliability testing is happening
- how often failures occur
- whether latency behavior changes during fault injection runs

Observability turns test execution into something teams can monitor over time, not just inspect after the fact.

---

## ⚙️ Architecture

FaultLab API is the intelligence layer sitting between generated test cases and final reliability insights.

### System architecture diagram

```text
                ┌──────────────────────┐
                │   User API Endpoint  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Test Case Generator │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Failure Injection    │
                │ Engine               │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ API Execution Layer  │
                │ (Person-1)           │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Response Validator   │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Reliability Scoring  │
                │ Engine               │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Report Generator     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ JSON Reliability     │
                │ Report               │
                └──────────────────────┘
```

### Repository structure

```text
faultlab-api/
├── src/
│   ├── __init__.py
│   ├── failure_injector.py
│   ├── validator.py
│   ├── scoring_engine.py
│   ├── report_generator.py
│   └── observability.py
├── tests/
│   └── test_basic.py
├── requirements.txt
├── Dockerfile
├── README.md
└── .github/
    └── workflows/
        └── ci.yml
```

---

## ☁️ Tech Stack

- **Python 3.11**
- **Pytest**
- **Prometheus Client**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **Requests**
- **Docker**
- **GitHub Actions**

---

## 🚀 Deployment / CI Pipeline

This repository includes a GitHub Actions workflow that:

1. checks out the repository
2. sets up Python 3.11
3. installs dependencies
4. runs `pytest`
5. fails the pipeline if tests fail

This keeps the project ready for GitHub and demonstrates a clean engineering workflow for backend delivery.

The Dockerfile also validates the project by installing dependencies and running tests during build.

---

## 💻 Run Locally

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🧪 Run Tests

```bash
pytest
```

Or:

```bash
python -m pytest
```

---

## 💡 Why This Project Matters

APIs do not become reliable just because they succeed when input is correct.

Real reliability comes from answering harder questions:

- What happens when a required field is missing?
- What happens when a type contract is violated?
- What happens when the payload looks valid structurally but breaks business rules?
- What happens when protocol-level request context is incomplete?

FaultLab API matters because it turns those questions into an engineering system:

- deterministic
- measurable
- explainable
- testable

This makes it a strong example of backend reliability engineering rather than just basic endpoint testing.

---

## 🔮 Future Improvements

- schema-aware mutations using OpenAPI definitions
- richer semantic failure strategies by field meaning
- historical trend analysis for RDI across builds
- API endpoints for internal scoring/report services
- persistent metrics export and dashboard integration
- configurable weighting for different endpoint classes

---

## 👩‍💻 Developer

This project was designed as a backend reliability engineering portfolio piece focused on deterministic failure testing, validation logic, observability, and scoring-driven resilience analysis.

Built by Ananditha ⚡
