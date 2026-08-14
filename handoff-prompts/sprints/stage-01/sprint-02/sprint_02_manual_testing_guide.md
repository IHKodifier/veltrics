# Veltrics Fleet Management — Sprint 02 Manual Testing Guide

> **Document Version:** 1.0.0  
> **Target Release:** Sprint 02 Baseline (Consumer Data Entry & Notifications Engine)  
> **Master Spec:** [`product-specs/08-master-prd.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/08-master-prd.md)  
> **Sprint Backlog Tracker:** [`trackers/stage-01/sprints/07.01.02-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/stage-01/sprints/07.01.02-tracker.md)

---

## 1. Executive Summary & Test Environment Setup

This document provides a comprehensive, step-by-step manual testing guide for all **24 Use Cases** implemented in **Sprint 02**. Quality Assurance (QA) testers, developers, and product owners can follow this guide to systematically verify front-end screen flows, fuel fill-up logging, trip tracking, expense category breakdowns, receipt photo uploader & OCR auto-fill, fuel anomaly & theft detection rules, and FCM push notifications.

### 1.1 Local Environment Setup Instructions

Before commencing manual testing, ensure the local development environment and backend services are active:

1. **Launch Backend Service (FastAPI + SQLite `dev.db` + Auth Emulator):**
   Open a PowerShell terminal in the repository root and execute:
   ```powershell
   .\scripts\start_backend.ps1
   ```
   *Backend API target address:* `http://localhost:8000`  
   *Interactive API Docs (Swagger UI):* `http://localhost:8000/docs`

2. **Launch Mobile/Web Client App (Flutter):**
   Open a secondary PowerShell terminal and run:
   ```powershell
   cd src/frontend
   flutter run -d chrome  # Or desktop/emulator
   ```

3. **Verify Pre-populated Demo Data:**
   The application initializes with demo vehicles (`veh-demo-001`, `veh-demo-002`), assigned drivers, fuel logs, and trip entries ready for testing.

---

## 2. Global Navigation & Screen Architecture Map (Sprint 02 Additions)

The Veltrics Flutter client includes expanded navigation paths, speed dial floating action buttons (`VeltricsQuickActionsFab`), notification badges, and analytics cards:

```
+-----------------------------------------------------------------------------------+
| Top App Bar: [ Org Selector Dropdown ]   [ 🔔 Notifications (UC-072/075) ]        |
|                                            ├── In-App Inbox (SCR-NOTIF-001)       |
|                                            └── Channel Prefs (SCR-NOTIF-002)     |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Tab 0: Dashboard (UC-064) ]   [ Tab 1: Fleet Directory ]   [ Tab 2: Logs & Hist ] |
|  - Cost Breakdown Card (UC-065)   - Vehicle List (UC-025)     - Fuel Log History    |
|  - Mileage Summary Card (UC-057)  - Tap -> Vehicle Detail        (UC-047/048)       |
|  - Anomaly Banner (UC-050)          (UC-026)                 - Trip History        |
|                                                                (UC-053/054/055)   |
|  [ ⚡ Speed Dial FAB (UC-066) ]                               - Expense History     |
|  ├── ⛽ Quick Fuel (UC-046/056)                                 (UC-058/061)       |
|  ├── 🛣️ Quick Trip (UC-052/056)                                                   |
|  └── 💸 Quick Expense (UC-058/062)                                               |
+-----------------------------------------------------------------------------------+
| Bottom Navigation Bar: [ 📊 Dashboard ]   [ 🚗 Fleet Directory ]   [ 📝 Logs & Hist ] |
+-----------------------------------------------------------------------------------+
```

---

## 3. Step-by-Step Manual Test Protocols (UC-046 to UC-075)

---

### Module A: Fuel Management Core & Intelligence

#### UC-046: Log Fuel Entry
* **Target Screen:** Fuel Log Dialog / Form (`LogFuelScreen` / `SCR-FUEL-001`)
* **Navigation Path:** Tap **Speed Dial FAB (⚡)** -> Select **"Add Fuel Log" (⛽)** OR Navigate to Vehicle Detail -> Tap **"Log Fuel"**.
* **Pre-conditions:** App launched, vehicle selected (`veh-demo-001`).
* **Execution Steps:**
  1. Open the Fuel Log form.
  2. Select vehicle `veh-demo-001` (Current Odometer: 15,000 km).
  3. Enter **Odometer:** `15,450` km.
  4. Enter **Liters Filled:** `35.0` L.
  5. Enter **Total Cost ($):** `52.50`.
  6. Check **"Is Full Tank"** checkbox.
  7. Tap **"Save Fuel Log"**.
* **Expected Outcome:**
  * Fuel log entry is successfully saved to SQLite backend (`POST /api/v1/fuel/logs`).
  * Vehicle odometer updates automatically from `15,000` to `15,450` km.
  * A linked expense entry of `$52.50` under category `"FUEL"` is auto-generated (UC-058 link).
  * Calculated fuel efficiency (`450 km / 35.0 L = 12.85 km/L`) is calculated and displayed.
* **Automated Test Ref:** `pytest src/tests/unit/test_fuel_uc046.py`

---

#### UC-047: View Fuel Log History
* **Target Screen:** Fuel History List Screen (`FuelHistoryScreen` / `SCR-FUEL-002`)
* **Navigation Path:** Tap **Logs & History Tab** -> Select **"Fuel Logs"** tab.
* **Pre-conditions:** At least 2 fuel entries exist for the vehicle.
* **Execution Steps:**
  1. Open the Fuel History tab.
  2. Filter by Vehicle `veh-demo-001`.
  3. Scroll down through fuel history cards.
* **Expected Outcome:**
  * Chronological list of fuel entries displayed with date, liters, total cost, price per liter, and calculated `km/L` efficiency.
  * Partial fill-up logs are clearly tagged with a "Partial" badge.
* **Automated Test Ref:** `pytest src/tests/unit/test_fuel_uc047.py`

---

#### UC-048: View Fuel History & Efficiency Trends
* **Target Screen:** Fuel Trends Card / Analytics Section (`FuelTrendsCard`)
* **Navigation Path:** Open Vehicle Detail Screen (`veh-demo-001`) -> Scroll to **Fuel Analytics**.
* **Pre-conditions:** At least 2 full-tank fill-ups recorded.
* **Execution Steps:**
  1. Navigate to Vehicle Detail.
  2. Inspect the **Fuel Efficiency Trend Chart**.
  3. Observe average fuel cost per km and monthly fuel spending summary.
* **Expected Outcome:**
  * Interactive line/bar chart shows fuel consumption efficiency over time (`km/L`).
  * Average consumption rate (e.g., `12.5 km/L`) and total fuel spend summary are accurate.
* **Automated Test Ref:** `pytest src/tests/unit/test_fuel_uc048.py`

---

#### UC-051: Soft Delete & Edit Fuel Log Entry
* **Target Screen:** Fuel Log Edit Dialog / Detail View (`EditFuelDialog`)
* **Navigation Path:** Fuel History Screen -> Tap target Fuel Log entry -> Tap **Edit (✏️)** or **Delete (🗑️)**.
* **Pre-conditions:** Target fuel log entry exists.
* **Execution Steps:**
  1. Tap Edit on a fuel entry, change Total Cost to `$55.00`, and tap **"Update"**.
  2. Tap Delete on another fuel entry and confirm the prompt **"Delete Fuel Log?"**.
* **Expected Outcome:**
  * Edit updates the fuel record (`PATCH /api/v1/fuel/{id}`) and recalculates price per liter.
  * Soft delete marks `is_deleted = True` (`DELETE /api/v1/fuel/{id}`). Entry disappears from fuel history list.
* **Automated Test Ref:** `pytest src/tests/unit/test_fuel_uc051.py`

---

#### UC-049: Fuel Receipt OCR Auto-Fill (Pro)
* **Target Screen:** Fuel Entry Form with OCR Scanner (`ReceiptOcrButton`)
* **Navigation Path:** Open **Log Fuel Form** -> Tap **"Scan Receipt with OCR" (📸)**.
* **Pre-conditions:** Camera/file picker active.
* **Execution Steps:**
  1. Tap **"Scan Receipt"**.
  2. Select/upload a fuel receipt image sample.
  3. Wait for OCR parsing (`POST /api/v1/fuel/ocr-scan`).
* **Expected Outcome:**
  * Form fields (**Liters**, **Total Cost**, **Price per Liter**, **Date**, **Fuel Type**) auto-fill with parsed OCR data.
  * User can manually edit or confirm auto-filled values before saving.
* **Automated Test Ref:** `pytest src/tests/unit/test_fuel_ocr_uc049.py`

---

#### UC-050: Detect Fuel Anomaly & Theft Alerts
* **Target Screen:** Fuel Anomaly Warning Card / Notification Center (`FuelAnomalyCard`)
* **Navigation Path:** Log Fuel Form OR In-App Notification Center.
* **Pre-conditions:** Vehicle fuel tank capacity set to `50.0` L (`fuel_tank_capacity`).
* **Execution Steps:**
  1. Log a fuel entry for `veh-demo-001` with **Liters Filled:** `65.0` L (Breaches 50.0 L capacity).
  2. Submit the fuel entry.
  3. Observe dashboard notification banner & alert inbox.
  4. As Fleet Manager, tap **"Verify Anomaly"** action on the alert card.
* **Expected Outcome:**
  * System detects tank capacity overflow breach (`> 50 L`).
  * Entry is saved with `anomaly_detected = True` and `anomaly_reason = "Liters filled (65.0L) exceeds tank capacity (50.0L)"`.
  * An automated manager notification alert is triggered.
  * Tapping **"Verify Anomaly"** marks `is_verified = True` (`PATCH /api/v1/fuel/{id}/verify-anomaly`).
* **Automated Test Ref:** `pytest src/tests/unit/test_fuel_anomaly_uc050.py`

---

### Module B: Trip & Mileage Tracking

#### UC-052: Log Manual Trip Entry & Start/Stop Trip
* **Target Screen:** Log Trip Screen (`LogTripScreen` / `SCR-TRIP-001`)
* **Navigation Path:** Tap **Speed Dial FAB (⚡)** -> Select **"Log Trip" (🛣️)**.
* **Pre-conditions:** Vehicle `veh-demo-001` selected.
* **Execution Steps:**
  1. Open Log Trip form.
  2. Set **Start Odometer:** `15,450` km, **End Odometer:** `15,580` km (Distance: 130 km).
  3. Enter **Origin:** `Lahore Depot`, **Destination:** `Faisalabad Warehouse`.
  4. Select **Classification:** `BUSINESS`.
  5. Tap **"Save Trip"**.
* **Expected Outcome:**
  * Trip record saved with `distance_km = 130.0` (`POST /api/v1/trips`).
  * Vehicle odometer updates to `15,580` km.
* **Automated Test Ref:** `pytest src/tests/unit/test_trip_uc052.py`

---

#### UC-053: View Trip History
* **Target Screen:** Trip History Screen (`TripHistoryScreen` / `SCR-TRIP-002`)
* **Navigation Path:** Tap **Logs & History Tab** -> Select **"Trips"** tab.
* **Pre-conditions:** At least 2 trip entries logged.
* **Execution Steps:**
  1. Navigate to Trip History tab.
  2. Filter by classification (**All**, **Business**, **Personal**).
* **Expected Outcome:**
  * List displays trip cards showing route (`Origin -> Destination`), distance (km), date, and classification badge (Blue for Business, Green for Personal).
* **Automated Test Ref:** `pytest src/tests/unit/test_trip_uc053.py`

---

#### UC-054: Edit Trip Entry & Classification
* **Target Screen:** Edit Trip Dialog (`EditTripDialog`)
* **Navigation Path:** Trip History -> Tap trip entry -> Tap **Edit (✏️)**.
* **Pre-conditions:** Existing trip entry available.
* **Execution Steps:**
  1. Change classification from `PERSONAL` to `BUSINESS`.
  2. Update notes to `"Client delivery round 2"`.
  3. Tap **"Save Changes"**.
* **Expected Outcome:**
  * Trip updated (`PATCH /api/v1/trips/{id}`).
  * Classification badge updates immediately to Business.
* **Automated Test Ref:** `pytest src/tests/unit/test_trip_uc054_055.py`

---

#### UC-055: Soft Delete Trip Entry
* **Target Screen:** Trip History List Item Action
* **Navigation Path:** Trip History -> Swipe left or tap Delete icon on trip card.
* **Pre-conditions:** Target trip entry exists.
* **Execution Steps:**
  1. Click Delete icon on trip entry.
  2. Confirm **"Delete Trip Entry?"** modal.
* **Expected Outcome:**
  * Soft delete executed (`DELETE /api/v1/trips/{id}`). Entry removed from history view.
* **Automated Test Ref:** `pytest src/tests/unit/test_trip_uc054_055.py`

---

#### UC-056: Quick-Log Trip from Dashboard
* **Target Screen:** Quick Trip Dialog (`VeltricsQuickActionsFab`)
* **Navigation Path:** Dashboard Tab -> Tap **⚡ Speed Dial FAB** -> Tap **Quick Trip (🛣️)**.
* **Pre-conditions:** User on Dashboard screen.
* **Execution Steps:**
  1. Tap Quick Trip action.
  2. Enter **Distance:** `45` km, **Purpose:** `"Parts Pickup"`.
  3. Tap **"Quick Log"**.
* **Expected Outcome:**
  * Modal saves trip entry quickly without requiring full route details.
  * Distance summary card updates immediately.
* **Automated Test Ref:** `pytest src/tests/unit/test_quick_actions_uc056_062.py`

---

#### UC-057: View Distance & Mileage Summary
* **Target Screen:** Mileage Summary Card / Screen (`MileageSummaryCard`)
* **Navigation Path:** Dashboard Tab OR Trip History Top Summary.
* **Pre-conditions:** Business & Personal trips logged.
* **Execution Steps:**
  1. Open Mileage Summary view.
  2. Observe total distance, business distance %, and estimated tax deduction ($0.65/km rate).
* **Expected Outcome:**
  * Total distance (e.g., `450 km`), Business split (`300 km / 66.7%`), and Tax Deduction Estimate (`300 km * $0.65 = $195.00`) calculated accurately.
* **Automated Test Ref:** `pytest src/tests/unit/test_trip_uc057.py`

---

### Module C: Expense Management & Attachments

#### UC-058: Log Vehicle Expense
* **Target Screen:** Log Expense Screen (`LogExpenseScreen` / `SCR-EXPENSE-001`)
* **Navigation Path:** Tap **Speed Dial FAB (⚡)** -> Select **"Add Expense" (💸)**.
* **Pre-conditions:** Vehicle selected.
* **Execution Steps:**
  1. Open Log Expense form.
  2. Select Category: `TOLL`, `PARKING`, `REPAIR`, or `INSURANCE`.
  3. Enter **Amount ($):** `120.00`.
  4. Enter **Vendor / Notes:** `"City Parking Garage"`.
  5. Tap **"Save Expense"**.
* **Expected Outcome:**
  * Expense entry created (`POST /api/v1/expenses`).
  * Total vehicle spending summary updates.
* **Automated Test Ref:** `pytest src/tests/unit/test_expense_uc058.py`

---

#### UC-059: View Expense History
* **Target Screen:** Expense History List Screen (`ExpenseHistoryScreen` / `SCR-EXPENSE-002`)
* **Navigation Path:** Logs & History Tab -> Select **"Expenses"** tab.
* **Pre-conditions:** Multiple expense records logged.
* **Execution Steps:**
  1. Navigate to Expense History tab.
  2. Filter list by Category or Date Range.
* **Expected Outcome:**
  * List shows expense cards with category icon, vendor, date, amount ($), and attached receipt preview thumbnail if present.
* **Automated Test Ref:** `pytest src/tests/unit/test_expense_uc059.py`

---

#### UC-060: Edit Expense Entry
* **Target Screen:** Edit Expense Dialog (`EditExpenseDialog`)
* **Navigation Path:** Expense History -> Tap Expense Card -> Tap Edit icon.
* **Pre-conditions:** Target expense record exists.
* **Execution Steps:**
  1. Edit amount from `$120.00` to `$135.00`.
  2. Tap **"Save"**.
* **Expected Outcome:**
  * Expense record updated (`PATCH /api/v1/expenses/{id}`). Amount updates in cost breakdown.
* **Automated Test Ref:** `pytest src/tests/unit/test_expense_uc060_061.py`

---

#### UC-061: Delete Expense Entry
* **Target Screen:** Expense History Action
* **Navigation Path:** Expense History -> Tap Delete icon on expense card.
* **Pre-conditions:** Expense record exists.
* **Execution Steps:**
  1. Click Delete. Confirm confirmation prompt.
* **Expected Outcome:**
  * Expense soft deleted (`DELETE /api/v1/expenses/{id}`). Record removed from history.
* **Automated Test Ref:** `pytest src/tests/unit/test_expense_uc060_061.py`

---

#### UC-062: Quick-Log Expense from Dashboard
* **Target Screen:** Quick Expense Dialog (`VeltricsQuickActionsFab`)
* **Navigation Path:** Dashboard Tab -> Tap **⚡ Speed Dial FAB** -> Tap **Quick Expense (💸)**.
* **Pre-conditions:** User on Dashboard.
* **Execution Steps:**
  1. Tap Quick Expense.
  2. Select Category `PARKING`, enter `$15.00`.
  3. Tap **"Save"**.
* **Expected Outcome:**
  * Fast-log dialog saves entry without requiring full form modal.
* **Automated Test Ref:** `pytest src/tests/unit/test_quick_actions_uc056_062.py`

---

#### UC-063: Attach Receipt Photo to Expense/Fuel Log
* **Target Screen:** Receipt Uploader Component (`ReceiptPickerWidget`)
* **Navigation Path:** Expense Form or Fuel Log Form -> Tap **"Attach Receipt Photo" (📎)**.
* **Pre-conditions:** Device image gallery/camera available.
* **Execution Steps:**
  1. Tap **"Attach Receipt Photo"**.
  2. Select an image file (`receipt_test.jpg`).
  3. Save the Expense/Fuel entry.
* **Expected Outcome:**
  * Image file uploaded via `POST /api/v1/uploads/receipt` (multipart form).
  * Backend saves file in `uploads/receipts/` and returns `photo_url`.
  * Thumbnail preview renders on Expense card.
* **Automated Test Ref:** `pytest src/tests/unit/test_receipt_uc063.py`

---

#### UC-065: Cost Breakdown Charts per Vehicle
* **Target Screen:** Cost Breakdown Card (`CostBreakdownCard`)
* **Navigation Path:** Dashboard Tab -> Scroll to **Cost Breakdown per Vehicle**.
* **Pre-conditions:** Expenses across categories (Fuel, Maintenance, Toll, Parking) logged.
* **Execution Steps:**
  1. Navigate to Dashboard.
  2. Inspect the **Cost Breakdown Donut/Bar Chart**.
  3. Filter by Monthly / YTD time period.
* **Expected Outcome:**
  * Visual chart displays category percentage breakdown (e.g., Fuel: 65%, Maintenance: 25%, Toll: 10%).
  * Total spending matches aggregate sum of logged expenses.
* **Automated Test Ref:** `pytest src/tests/unit/test_cost_breakdown_uc065.py`

---

#### UC-066: Quick Actions Floating Button
* **Target Screen:** Speed Dial FAB Component (`VeltricsQuickActionsFab`)
* **Navigation Path:** Dashboard or Fleet Directory -> Bottom right floating button.
* **Pre-conditions:** App launched.
* **Execution Steps:**
  1. Tap the primary **⚡ Speed Dial FAB**.
  2. Observe expanded menu items: **Fuel (⛽)**, **Trip (🛣️)**, **Expense (💸)**.
  3. Tap backdrop area to collapse menu.
* **Expected Outcome:**
  * FAB smoothly expands with animated child action buttons.
  * Backdrop darkens. Tapping backdrop or an action collapses the speed dial cleanly.
* **Automated Test Ref:** `pytest src/tests/unit/test_quick_actions_uc056_062.py`

---

### Module D: Push Notifications Engine

#### UC-072: Request FCM Push Notification Permission
* **Target Screen:** Notification Permission Banner / Dialog
* **Navigation Path:** App startup or Top App Bar -> Tap **Notifications Bell (🔔)**.
* **Pre-conditions:** First time opening notification feature.
* **Execution Steps:**
  1. Tap Notification Bell icon.
  2. Click **"Enable Notifications"** on permission prompt.
* **Expected Outcome:**
  * System FCM permission request dialog triggers.
  * On grant, device token is registered via `POST /api/v1/notifications/devices` (`UserDevice` model created).
* **Automated Test Ref:** `pytest src/tests/unit/test_notifications_uc072_075.py`

---

#### UC-073: Send Maintenance Overdue Push Notification
* **Target Screen:** In-App Notification Center (`NotificationInboxScreen` / `SCR-NOTIF-001`)
* **Navigation Path:** Top App Bar -> Tap **Notifications Bell (🔔)**.
* **Pre-conditions:** Vehicle has an overdue maintenance schedule (e.g., Oil Change due 500 km ago).
* **Execution Steps:**
  1. Trigger maintenance check background task or backend worker.
  2. Open Notification Inbox.
* **Expected Outcome:**
  * High-priority overdue alert notification appears: `"OVERDUE: Oil Change for veh-demo-001 is overdue by 500 km!"`.
  * Top App Bar bell badge shows red unread counter `(1)`.
* **Automated Test Ref:** `pytest src/tests/unit/test_notifications_uc072_075.py`

---

#### UC-074: Send Maintenance Upcoming Push Notification
* **Target Screen:** In-App Notification Center (`NotificationInboxScreen` / `SCR-NOTIF-001`)
* **Navigation Path:** Top App Bar -> Tap **Notifications Bell (🔔)**.
* **Pre-conditions:** Maintenance schedule due within 7 days or 200 km.
* **Execution Steps:**
  1. Open Notification Inbox.
  2. Tap upcoming notification item.
* **Expected Outcome:**
  * Notification displays `"UPCOMING: Tire Rotation due in 150 km"`.
  * Tapping notification navigates directly to the target Vehicle Maintenance Detail screen.
  * Notification is marked as read (`PATCH /api/v1/notifications/{id}/read`). Unread badge updates.
* **Automated Test Ref:** `pytest src/tests/unit/test_notifications_uc072_075.py`

---

#### UC-075: Background FCM Push Notification Handler & Preferences
* **Target Screen:** Notification Preferences Screen (`NotificationPreferencesScreen` / `SCR-NOTIF-002`)
* **Navigation Path:** Notification Inbox -> Tap **Settings (⚙️)** in top right.
* **Pre-conditions:** User logged in.
* **Execution Steps:**
  1. Open Notification Preferences.
  2. Toggle OFF **"Fuel Anomaly Alerts"**.
  3. Toggle ON **"Maintenance Overdue Alerts"**.
  4. Tap **"Save Preferences"**.
* **Expected Outcome:**
  * Preferences updated via `PATCH /api/v1/notifications/preferences`.
  * Disabled alert channels suppress background push alerts accordingly.
* **Automated Test Ref:** `pytest src/tests/unit/test_notifications_uc072_075.py`

---

## 4. Verification Checklist & QA Sign-Off Matrix

| Ticket ID | Category | Primary Feature | Verified By (Manual) | Test Suite Status | Sign-off |
|:---|:---|:---|:---|:---|:---|
| **UC-046** | Fuel | Log Fuel Entry | [ ] Pass | `test_fuel_uc046.py` (PASS) | [ ] |
| **UC-047** | Fuel | View Fuel Log History | [ ] Pass | `test_fuel_uc047.py` (PASS) | [ ] |
| **UC-048** | Fuel | Fuel Trends & km/L Chart | [ ] Pass | `test_fuel_uc048.py` (PASS) | [ ] |
| **UC-051** | Fuel | Edit/Delete Fuel Log | [ ] Pass | `test_fuel_uc051.py` (PASS) | [ ] |
| **UC-049** | Fuel | Fuel Receipt OCR Auto-Fill | [ ] Pass | `test_fuel_ocr_uc049.py` (PASS) | [ ] |
| **UC-050** | Fuel | Fuel Anomaly & Theft Alerts | [ ] Pass | `test_fuel_anomaly_uc050.py` (PASS) | [ ] |
| **UC-052** | Trip | Log Trip & Odometer Update | [ ] Pass | `test_trip_uc052.py` (PASS) | [ ] |
| **UC-053** | Trip | View Trip History | [ ] Pass | `test_trip_uc053.py` (PASS) | [ ] |
| **UC-054** | Trip | Edit Trip Classification | [ ] Pass | `test_trip_uc054_055.py` (PASS) | [ ] |
| **UC-055** | Trip | Soft Delete Trip Entry | [ ] Pass | `test_trip_uc054_055.py` (PASS) | [ ] |
| **UC-056** | Trip | Quick-Log Trip Dialog | [ ] Pass | `test_quick_actions_uc056_062.py` (PASS) | [ ] |
| **UC-057** | Trip | Mileage & Tax Deduction Summary | [ ] Pass | `test_trip_uc057.py` (PASS) | [ ] |
| **UC-058** | Expense | Log Vehicle Expense | [ ] Pass | `test_expense_uc058.py` (PASS) | [ ] |
| **UC-059** | Expense | View Expense History | [ ] Pass | `test_expense_uc059.py` (PASS) | [ ] |
| **UC-060** | Expense | Edit Expense Record | [ ] Pass | `test_expense_uc060_061.py` (PASS) | [ ] |
| **UC-061** | Expense | Delete Expense Record | [ ] Pass | `test_expense_uc060_061.py` (PASS) | [ ] |
| **UC-062** | Expense | Quick-Log Expense Dialog | [ ] Pass | `test_quick_actions_uc056_062.py` (PASS) | [ ] |
| **UC-063** | Expense | Attach Receipt Photo | [ ] Pass | `test_receipt_uc063.py` (PASS) | [ ] |
| **UC-065** | Expense | Cost Breakdown Donut Chart | [ ] Pass | `test_cost_breakdown_uc065.py` (PASS) | [ ] |
| **UC-066** | UI | Speed Dial Quick Actions FAB | [ ] Pass | `test_quick_actions_uc056_062.py` (PASS) | [ ] |
| **UC-072** | Push | Request FCM Permission & Token | [ ] Pass | `test_notifications_uc072_075.py` (PASS) | [ ] |
| **UC-073** | Push | Maintenance Overdue Alert | [ ] Pass | `test_notifications_uc072_075.py` (PASS) | [ ] |
| **UC-074** | Push | Maintenance Upcoming Alert | [ ] Pass | `test_notifications_uc072_075.py` (PASS) | [ ] |
| **UC-075** | Push | Notification Inbox & Prefs | [ ] Pass | `test_notifications_uc072_075.py` (PASS) | [ ] |
