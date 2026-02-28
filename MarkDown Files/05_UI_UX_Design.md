# UI/UX & Interaction System Architecture

## 1. UI/UX from Stitch
The foundation of the UI incorporates designs exported from Stitch (Account token: `AQ.Ab8RN6IXBCAmZ39D46xnFi9pUVfajyTCqT5Gb1zPkxOQm1aEfw`).
*   **Mapping:** The Stitch design system components (buttons, cards, data tables) map strictly to raw Tailwind CSS and reusable React functional components in `apps/frontend/src/components`.
*   **Frontend to Backend Label Mapping:**
    *   Stitch Design Label: *Action Required* -> Backend Status: `REQUIRE_HITL_INTERVENTION`
    *   Stitch Design Label: *Active Processing* -> Backend Status: `SPINE_ROUTING_IN_PROGRESS`
    *   Stitch Design Label: *Task Complete* -> Backend Status: `EXECUTION_SEALED`
    *   Labels are hard-coded in TypeScript `enum` models mapping strictly to the Prisma schema to avoid drift.

## 2. Interaction System Architecture & Visual Design
*   **The "Apple" Ethos:** Interfaces must communicate calmness and meaning. Clutter is aggressively deleted. Font hierarchies are structured using clear size, standard spacing, and high-contrast color balances.
*   **Motion & Feedback:** The application is never "frozen".
    *   If a request takes > 200ms, skeleton loaders instantiate immediately.
    *   Hover effects gently lift components via drop-shadows and subtle CSS transforms (e.g., `hover:-translate-y-0.5`).
    *   Action completion triggers fluid micro-animations (e.g., a checkmark drawing itself via SVG morphing).
*   **Responsive layouts:** Flex and Grid systems scale flawlessly. A data-heavy table on desktop degrades gracefully into stacked summary cards on mobile.

## 3. Conversion Copy Architecture
Text within the application is carefully crafted to mimic native, premium software.
*   **Headlines** are declarative and concise. (e.g., "Pending Approvals", not "Here are the things you need to approve").
*   **Substitutions & Context:** Sentences use contextual AI injection seamlessly so the user feels they are working with an intelligent peer. 
*   **Status indicators** use explicit, unambiguous language (e.g., "System Paused - Awaiting Operator Verification" instead of "Error").

## 4. Visual Execution Checklist
*   [ ] Screen is fundamentally reactive down to 320px mobile viewports.
*   [ ] Fonts are adjusted fluidly based on viewport size (clamp metrics).
*   [ ] Light/Dark mode transitions are fully supported utilizing centralized CSS/Tailwind variables.
*   [ ] Accessibility mapping (ARIA labels, keyboard navigation) is guaranteed for all interactive DOM elements.
