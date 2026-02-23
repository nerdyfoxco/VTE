# VTE Per Page Content Structure

## Page: VTE Operator Dashboard (`/`)

### 1. Header Component
*   **Left Section:**
    *   **Icon:** `ShieldAlert` (Blue)
    *   **Title (`<h1>`):** "VTE Operator Dashboard"
    *   **Subtitle (`<p>`):** "E2E Deterministic Runtime Trace Viewer"
*   **Right Section:**
    *   **Button:** "Simulate Gmail Ingestion"
        *   **Icon:** `RefreshCw` (Spinning on Active)
        *   **Action:** Triggers `/sync-gmail` and fetches updated queues.

### 2. Workqueue Component (Pending Approval)
*   **Title Area:**
    *   **Icon:** `Clock` (Yellow)
    *   **Title (`<h2>`):** "Workqueue (Pending Approval)"
*   **Content Area:**
    *   **Empty State:** "No items pending approval." (Italic, gray).
    *   **Populated State (List Item):**
        *   `work_item_id` (Monospace, Blue)
        *   `timestamp` (Formatted Date/Time)
        *   `policy_outcome` (Yellow, Bold)
        *   `status` (Gray text)

### 3. Complete Execution Traces Component
*   **Title Area:**
    *   **Icon:** `CheckCircle` (Green)
    *   **Title (`<h2>`):** "Complete Execution Traces"
*   **Content Area:**
    *   **Empty State:** "No execution traces recorded." (Italic, gray).
    *   **Populated State (Card):**
        *   `work_item_id` (Monospace, Blue)
        *   **Action Badge:** Red for `TERMINATE`, Green for `PROCEED`.
        *   **Decision Badge:** Gray badge for `final_decision`.
        *   **Trace Log Details:**
            *   "Primary Reason:" string.
            *   Bulleted list of `reasons` strings providing deep deterministic traces.
