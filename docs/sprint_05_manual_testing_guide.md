# Sprint 05 Manual Testing Guide & Verification Matrix

**Sprint:** Sprint 05 — Fleet Intelligence, Driver Behavior Scoring, Analytics & Data Export  
**Branch:** `sprint/sprint-05`  
**Completion Status:** 23 / 23 Use Cases (100% Complete)

---

## 1. Automated Test Suite Execution

Run all Sprint 05 automated unit test suites locally:
```powershell
src/backend/venv/Scripts/python.exe -m pytest src/tests/unit/test_driver_analytics_uc103_106_070.py src/tests/unit/test_maintenance_uc039_045.py src/tests/unit/test_dashboard_manager_uc067_071.py src/tests/unit/test_exports_and_notifications_uc076_079_110_112.py -v
```

---

## 2. Feature Test Matrix (23 Use Cases)

| Batch | Use Case | Title | Endpoint / Trigger | Expected Verification Result |
|:---|:---|:---|:---|:---|
| **Batch 1** | **UC-103** | Calculate Driver Consistency Score | `GET /api/v1/driver-analytics/drivers/{id}/performance` | Score computed (0–100) with harsh event and idle penalties. |
| **Batch 1** | **UC-104** | View Individual Driver Performance Detail | `GET /api/v1/driver-analytics/drivers/{id}/performance` | Returns detailed breakdown of safety events and trip stats. |
| **Batch 1** | **UC-105** | Driver Inactivity & Anomaly Alert | `GET /api/v1/driver-analytics/detect-anomalies` | Detects drivers idle >14 days or licenses expiring <30 days. |
| **Batch 1** | **UC-106** | Driver Safety Certificate Badge | `GET /api/v1/driver-analytics/drivers/{id}/certificate` | Generates SHA-256 verified safety badge certificate. |
| **Batch 1** | **UC-070** | Driver Safety Score Leaderboard | `GET /api/v1/driver-analytics/leaderboard` | Returns ranked driver leaderboard sorted by safety score. |
| **Batch 2** | **UC-039** | Add Custom Maintenance Service Item | `POST /api/v1/maintenance/schedules/custom` | Creates custom recurring schedule item (`is_custom=True`). |
| **Batch 2** | **UC-040** | Edit Existing Service Record | `PUT /api/v1/maintenance/records/{id}` | Updates cost, provider name, notes, and odometer. |
| **Batch 2** | **UC-041** | Delete Service Record (Soft Delete) | `DELETE /api/v1/maintenance/records/{id}` | Soft deletes service record setting `deleted_at`. |
| **Batch 2** | **UC-042** | Filter & Search Service History | `GET /api/v1/maintenance/records` | Filters records by search query, vehicle ID, and org ID. |
| **Batch 2** | **UC-043** | Maintenance Vendor Management | `POST /api/v1/vendors` | Saves vendor contacts, address, and ratings directory. |
| **Batch 2** | **UC-044** | Vehicle Safety Inspection Checklist | `POST /api/v1/inspections` | Logs pre-trip/post-trip safety checks and defects. |
| **Batch 2** | **UC-045** | Snooze / Defer Maintenance Alert | `POST /api/v1/maintenance/schedules/{id}/snooze` | Defers alert by custom days and kilometers. |
| **Batch 3** | **UC-067** | Fleet Manager Web Dashboard Layout | `GET /api/v1/dashboard/manager` | Aggregates KPI cards, total costs, and active trips. |
| **Batch 3** | **UC-068** | Fleet Cost Ranking Table & Heatmap | `GET /api/v1/dashboard/cost-ranking` | Returns vehicle TCO and cost-per-km rankings. |
| **Batch 3** | **UC-069** | Fleet Vehicle Availability Widget | `GET /api/v1/dashboard/vehicle-availability` | Displays available vs maintenance vs in-use counts. |
| **Batch 3** | **UC-071** | Customize Fleet Dashboard Layout | `PUT /api/v1/dashboard/layout` | Saves user widget grid order and visibility. |
| **Batch 4** | **UC-110** | Export Maintenance History to PDF | `GET /api/v1/exports/maintenance/pdf` | Downloads valid PDF file of maintenance history. |
| **Batch 4** | **UC-111** | Export Fuel & Expense Logs to CSV | `GET /api/v1/exports/fuel-expenses/csv` | Downloads CSV formatted log data. |
| **Batch 4** | **UC-112** | Email Monthly Fleet Summary PDF | `POST /api/v1/exports/monthly-summary/email` | Generates summary report and sends to target email. |
| **Batch 4** | **UC-076** | Notification Inbox Screen | `GET /api/v1/notifications/inbox` | Displays list of in-app notification alerts with read state. |
| **Batch 4** | **UC-077** | Notification Preferences | `PUT /api/v1/notifications/preferences` | Configures push vs email notification channels. |
| **Batch 4** | **UC-078** | Billing & Payment Alert Notifications | `POST /api/v1/notifications/billing-alerts` | Triggers automated alerts for renewals & payment failures. |
| **Batch 4** | **UC-079** | Purge Stale FCM Tokens | `POST /api/v1/notifications/purge-stale-tokens` | Cleans up push tokens inactive for >90 days. |
