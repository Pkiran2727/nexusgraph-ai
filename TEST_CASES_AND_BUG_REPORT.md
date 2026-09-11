# NexusGraph AI: QA Execution, Test Cases, & Bug Report

## Executive Summary
A comprehensive Quality Assurance (QA) testing cycle was performed on the local deployment of NexusGraph AI (`http://localhost:8095`). This included backend Unit Testing (Pytest), frontend Automated E2E Testing (Selenium), and Manual Browser UI Verification. 

The application architecture and graph logic proved extremely robust, with all backend tests passing successfully. However, one race condition was identified during the Selenium E2E automated test suite related to asynchronous AI API latency.

---

## 1. Test Cases & Execution Matrix

### A. Backend Unit Testing (`test_backend.py`)
Executed via `pytest`. **Pass Rate: 100% (6/6)**

| Test Case ID | Description | Execution Result |
| :--- | :--- | :---: |
| `TC_B_01` | Verify SQLite database persistence and schema loading | ✅ **PASSED** |
| `TC_B_02` | Verify NetworkX compiles nodes and edges correctly for Cytoscape payload | ✅ **PASSED** |
| `TC_B_03` | Verify Assignment 4: Role AI exposure scoring and reasoning chains | ✅ **PASSED** |
| `TC_B_04` | Verify Assignment 11: Cascading impact simulation math algorithms | ✅ **PASSED** |
| `TC_B_05` | Verify API Key security (Zero hardcoded secrets in source code) | ✅ **PASSED** |
| `TC_B_06` | Verify FastAPI REST endpoints return HTTP 200 via `TestClient` | ✅ **PASSED** |

### B. Automated Browser E2E Testing (`test_selenium_e2e.py`)
Executed via `pytest` (Headless Chrome). **Pass Rate: 66% (2/3)**

| Test Case ID | Description | Execution Result |
| :--- | :--- | :---: |
| `TC_E_01` | Verify Homepage layout, DOM, and metric statistical cards render correctly | ✅ **PASSED** |
| `TC_E_02` | Verify tab switching navigation and Role Analytics drawer display | ✅ **PASSED** |
| `TC_E_03` | Verify live "Surprise Record" ingestion form parsing & graph updating | ❌ **FAILED** (See Bug Report) |

### C. Manual UI Browser Verification
Executed via local UI interaction (`http://localhost:8095`). **Pass Rate: 100%**

| Test Case ID | Description | Execution Result |
| :--- | :--- | :---: |
| `TC_M_01` | Verify Custom Pastel Theme rendering and styling | ✅ **PASSED** |
| `TC_M_02` | Verify Cytoscape interactive graph canvas (Node/Edge visibility & controls) | ✅ **PASSED** |
| `TC_M_03` | JavaScript Console Audit (Check for severe application errors) | ✅ **PASSED** (0 Errors) |

---

## 2. Bug Report 

> [!WARNING]
> **Bug ID:** `BUG-001`
> **Title:** Automation Test Failure due to Asynchronous API Race Condition in `test_03_surprise_record_ingestion_form`
> **Severity:** Low (Test Script Issue, NOT an Application Logic Issue)
> **Component:** `tests/test_selenium_e2e.py`

### Description
The Selenium automation test suite failed on `test_03_surprise_record_ingestion_form`. The test asserts that the UI will update to `"Ingestion Successful"` within a hardcoded 3-second window (`time.sleep(3)`). However, because the backend relies on the external `gemini-3.1-flash-lite` API to parse unstructured inputs, the API call latency frequently exceeds 3 seconds, causing the assertion to fail prematurely.

### Traceback Log
```python
E       AssertionError: 'Ingestion Successful' not found in 'Gemini AI Agent decomposing and persisting record...'
tests/test_selenium_e2e.py:91: AssertionError
========================= 1 failed, 2 passed in 22.08s =========================
```

### Root Cause Analysis
The backend FastAPI server successfully processed the request (Terminal log verified: `[GeminiAgent] Successfully persisted surprise record...`), but the Selenium test script timed out before the UI could render the result. 

### Recommended Fix
Update `tests/test_selenium_e2e.py` to use **WebDriverWait (Explicit Waits)** instead of hardcoded `time.sleep()`. 
```python
# Recommended Selenium Fix:
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Wait up to 15 seconds for the success message to appear in the DOM
WebDriverWait(self.driver, 15).until(
    EC.text_to_be_present_in_element((By.ID, "surprise-results"), "Ingestion Successful")
)
```

---

## 3. Manual Browser Verification Evidence

Below is the automated recording of the manual browser subagent successfully loading the UI, verifying the pastel theme, and testing the navigation tabs on `http://localhost:8095`.

![Manual UI Testing Recording](/home/ostilio/.gemini/antigravity/brain/87ba0b07-2115-4549-b5aa-557667fec19d/nexusgraph_ui_manual_test_1789105124416.webp)
