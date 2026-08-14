# Veltrics Fleet Management — Sprint 04 Manual Testing Guide

> **Document Version:** 1.0.0  
> **Target Release:** Sprint 04 Baseline (Phase 1 MVP)  
> **Master Spec:** [`product-specs/08-master-prd.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/08-master-prd.md)  
> **Sprint Backlog Tracker:** [`trackers/stage-01/sprints/07.01.04-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/stage-01/sprints/07.01.04-tracker.md)

---

## 1. Executive Summary & Environment Setup

This document provides a step-by-step manual testing guide for all **18 Use Cases** implemented in **Sprint 04** (Monetization — Safepay Payments, Ads & Ad-Gate Enforcement).

### 1.1 Local Environment Setup Instructions

1. **Launch Backend Service:**
   ```powershell
   .\scripts\start_backend.ps1
   ```
   *Target API Target:* `http://localhost:8000`  
   *API Docs:* `http://localhost:8000/docs`

2. **Launch Client App:**
   ```powershell
   cd src/frontend
   flutter run -d chrome
   ```

---

## 2. Step-by-Step Manual Test Protocols (UC-080 to UC-122)

---

### Module A: Safepay Payments & Subscriptions

#### UC-080: Initiate Pro Tier Subscription (Safepay Checkout)
* **Target Screen:** Settings -> Billing & Subscription Screen -> Upgrade Modal
* **Pre-conditions:** User in Free tier organization (`max_vehicles=3`, `max_drivers=3`).
* **Execution Steps:**
  1. Open Subscription Screen and click **"Upgrade to Pro ($19/mo)"**.
  2. Select Billing Cycle (`MONTHLY` or `ANNUALLY`).
  3. Click **"Proceed to Safepay Checkout"**.
* **Expected Outcome:**
  * System calls `/api/v1/payments/checkout-session`.
  * Redirects to Safepay payment checkout URL with session ID.
  * Subscription status transitions to `PENDING`.

#### UC-081 & UC-121: Safepay Payment Webhook & Entitlement Activation
* **Target Screen:** Backend Webhook Handler / Interactive Docs (`/docs`)
* **Execution Steps:**
  1. Open `/docs` and locate `POST /api/v1/payments/webhooks/safepay`.
  2. Post `payment.completed` event JSON payload with valid HMAC signature.
* **Expected Outcome:**
  * Webhook returns `{"status": "success", "message": "Subscription activated successfully"}`.
  * Organization upgraded to `tier = "pro"`, `max_vehicles = 25`, `max_drivers = 15`.
  * Duplicate webhook event triggers idempotency response: `"Event already processed"`.

#### UC-082: Payment Failure & 7-Day Grace Period
* **Target Screen:** Subscription Status Screen / Webhook Handler
* **Execution Steps:**
  1. Post `payment.failed` event to `/api/v1/payments/webhooks/safepay`.
* **Expected Outcome:**
  * Subscription status updates to `PAST_DUE`.
  * `grace_period_ends_at` set to +7 days in future.
  * Warning banner displayed in app: `"Payment past due. Grace period active."`

#### UC-083 & UC-084: View Subscription Status & Cancel Subscription
* **Target Screen:** Subscription Management Screen
* **Execution Steps:**
  1. View current active tier, renewal date, and max quotas.
  2. Click **"Cancel Subscription"**.
  3. Confirm cancellation in modal.
* **Expected Outcome:** `cancel_at_period_end` set to `True`. Pro features remain active until current period end date.

#### UC-085 & UC-120: Pro-to-Free Downgrade & Bonus Slot Preservation Protocol
* **Target Screen:** Backend Downgrade Scheduler (`POST /api/v1/payments/process-downgrades`)
* **Execution Steps:**
  1. Trigger downgrade processing after subscription expiry date.
* **Expected Outcome:**
  * Organization tier reset to `free`.
  * Preserved Bonus Slot Formula enforced: `max_vehicles = 3 (base) + ad_bonus_vehicles`.
  * Previously earned rewarded ad bonus slots are preserved!

---

### Module B: Quota Walls & Ad Engine

#### UC-086 & UC-087: Vehicle & Driver Quota Wall Enforcement Screens
* **Target Screen:** Fleet Directory / Drivers Screen
* **Execution Steps:**
  1. In a free organization with 3 vehicles, click **"+ Add Vehicle"** to attempt creating a 4th vehicle.
  2. In a free organization with 3 drivers, attempt creating a 4th driver.
* **Expected Outcome:**
  * Backend returns `HTTP 402 PAYMENT_REQUIRED` (`VEHICLE_QUOTA_EXCEEDED` / `DRIVER_QUOTA_EXCEEDED`).
  * `QuotaWallDialog` modal appears offering:
    * **"Upgrade to Pro (Safepay)"**
    * **"Watch Short Video Ad (+1 Slot)"**
    * **"Contact Enterprise Sales (>25 Fleets)"**

#### UC-088: Pro Upgrade Celebration Modal
* **Target Screen:** Post-Checkout Return Screen
* **Execution Steps:**
  1. Complete Safepay payment checkout.
* **Expected Outcome:** `ProCelebrationModal` pops up displaying celebratory badges and confirmed quotas (25 Vehicles, 15 Drivers, 100% Ad-Free).

#### UC-089: Contact Enterprise Sales Inquiry Form (>25 Fleets)
* **Target Screen:** Quota Wall Modal -> Enterprise Sales Inquiry Modal
* **Execution Steps:**
  1. Click **"Contact Enterprise Sales"** link on quota wall dialog.
  2. Fill in Contact Name, Email, Phone, Estimated Fleet Size (e.g. `150`), and Message.
  3. Click **"Submit Enterprise Inquiry"**.
* **Expected Outcome:** Inquiry submitted successfully, backend returns `inquiry_id`, audit log recorded.

#### UC-098 & UC-101: AdMob Banner Ads & Pro Ad-Free Suppression
* **Target Screen:** Bottom of Dashboard / Fleet Screen
* **Execution Steps:**
  1. View bottom of screen in Free tier organization.
  2. Switch organization context to a Pro tier organization.
* **Expected Outcome:**
  * Free Tier: AdMob Banner widget (`ca-app-pub-3940256099942544/6300978111`) renders at bottom.
  * Pro Tier: AdMob banner is completely hidden (100% ad-free experience).

#### UC-099, UC-100 & UC-122: Play Rewarded Ad & Verify Signature Token
* **Target Screen:** Quota Wall Modal -> Rewarded Ad Player
* **Execution Steps:**
  1. Click **"Watch Short Video Ad (+1 Slot)"** on quota wall.
  2. Complete 30-second rewarded video playback.
  3. Submit AdMob SSV / HMAC token to `/api/v1/ads/verify-reward`.
* **Expected Outcome:**
  * Valid HMAC signature: `ad_bonus_vehicles` / `ad_bonus_drivers` incremented from 0 to 1, max quota updated to 4. User can now add 4th vehicle!
  * Invalid/Forged signature: Returns `HTTP 400 INVALID_AD_SIGNATURE`.
  * Duplicate token reuse: Returns `HTTP 400 AD_TOKEN_ALREADY_USED`.

#### UC-102: Ad Delivery Fallback Grace Handler
* **Target Screen:** Quota Wall Modal
* **Execution Steps:**
  1. Trigger rewarded ad when network is disconnected or no-fill error occurs.
* **Expected Outcome:** Graceful error banner displayed with retry button without freezing UI.

---

## 3. Manual QA Execution Scorecard (Sprint 04)

| Module | Use Case | Description | Target Screen | Status |
|:---|:---|:---|:---|:---:|
| **Payment** | **UC-080** | Initiate Safepay Checkout | Subscription Screen | `[ ] PASS / [ ] FAIL` |
| **Payment** | **UC-081** | Safepay Webhook Entitlements | Backend Webhook | `[ ] PASS / [ ] FAIL` |
| **Payment** | **UC-082** | Payment Failure & Grace Period | Subscription Status | `[ ] PASS / [ ] FAIL` |
| **Payment** | **UC-083** | View Subscription Status | Subscription Screen | `[ ] PASS / [ ] FAIL` |
| **Payment** | **UC-084** | Cancel Active Subscription | Subscription Screen | `[ ] PASS / [ ] FAIL` |
| **Payment** | **UC-085** | Downgrade Bonus Preservation | Downgrade Engine | `[ ] PASS / [ ] FAIL` |
| **Quota** | **UC-086** | Vehicle Quota Wall Dialog | Fleet Directory | `[ ] PASS / [ ] FAIL` |
| **Quota** | **UC-087** | Driver Quota Wall Dialog | Drivers Screen | `[ ] PASS / [ ] FAIL` |
| **Monetization**| **UC-088** | Pro Celebration Modal | Post-Checkout Screen | `[ ] PASS / [ ] FAIL` |
| **Monetization**| **UC-089** | Contact Enterprise Sales | Enterprise Modal | `[ ] PASS / [ ] FAIL` |
| **Ads** | **UC-098** | Free Tier AdMob Banner Ads | Bottom App Bar | `[ ] PASS / [ ] FAIL` |
| **Ads** | **UC-099** | Play Rewarded Video Ad | Quota Wall Modal | `[ ] PASS / [ ] FAIL` |
| **Ads** | **UC-100** | Verify SSV Signature Token | `/api/v1/ads/verify-reward`| `[ ] PASS / [ ] FAIL` |
| **Ads** | **UC-101** | Render Ad-Free Pro Experience | App-wide | `[ ] PASS / [ ] FAIL` |
| **Ads** | **UC-102** | Ad Delivery Fallback Grace | Quota Wall Modal | `[ ] PASS / [ ] FAIL` |
| **Quota** | **UC-120** | Ad-Rewarded Quota Lifecycle | Backend Quota Engine | `[ ] PASS / [ ] FAIL` |
| **Payment** | **UC-121** | Safepay Reconciliation Engine| Webhook Engine | `[ ] PASS / [ ] FAIL` |
| **Security**| **UC-122** | Ad-Gate Signature Protocol | Backend Middleware | `[ ] PASS / [ ] FAIL` |
