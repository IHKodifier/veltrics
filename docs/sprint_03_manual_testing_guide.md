# Veltrics Fleet Management — Sprint 03 Manual Testing Guide

> **Document Version:** 1.0.0  
> **Target Release:** Sprint 03 Baseline (Phase 1 MVP)  
> **Master Spec:** [`product-specs/08-master-prd.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/product-specs/08-master-prd.md)  
> **Sprint Backlog Tracker:** [`trackers/stage-01/sprints/07.01.03-tracker.md`](file:///e:/Non_Office/Dev_Space/vibe_skool/veltrics/trackers/stage-01/sprints/07.01.03-tracker.md)

---

## 1. Executive Summary & Environment Setup

This document provides a step-by-step manual testing guide for all **22 Use Cases** implemented in **Sprint 03** (Offline Sync Engine & Multi-Tenant Core). 

### 1.1 Local Environment Setup Instructions

1. **Launch Backend Service:**
   ```powershell
   .\scripts\start_backend.ps1
   ```
   *Target API:* `http://localhost:8000`  
   *API Docs:* `http://localhost:8000/docs`

2. **Launch Client App:**
   ```powershell
   cd src/frontend
   flutter run -d chrome
   ```

---

## 2. Step-by-Step Manual Test Protocols (UC-017 to UC-119)

---

### Module A: Multi-Tenant Organization Management

#### UC-017: Edit Organization Profile
* **Target Screen:** Settings -> Organization Profile Screen
* **Execution Steps:**
  1. Navigate to Organization Settings.
  2. Edit Organization Name, Tax ID, Currency (PKR/USD/EUR), Address, and Phone.
  3. Click **"Save Organization Profile"**.
* **Expected Outcome:** Organization profile updates immediately in database and top navigation bar.

#### UC-018: Invite Member by Email / Phone
* **Target Screen:** Organization Settings -> Team Members Tab -> Invite Dialog
* **Execution Steps:**
  1. Enter email (`member@example.com`) or phone (`+923001234567`).
  2. Select Role (`MANAGER` or `DRIVER`).
  3. Click **"Send Invitation"**.
* **Expected Outcome:** 64-character token with 7-day TTL is generated, pending invitation listed in Team roster.

#### UC-019 & UC-020: Accept / Redeem Invitation Code
* **Target Screen:** Invitation Redemption Screen
* **Execution Steps:**
  1. Open invite link or enter 6-digit redemption code.
  2. Click **"Accept & Join Organization"**.
* **Expected Outcome:** User is linked to organization with assigned role.

#### UC-021 & UC-022: Remove Member & Cancel Invitation
* **Target Screen:** Team Members Management Tab
* **Execution Steps:**
  1. Click **"Remove Member"** next to an active team member (non-owner).
  2. Click **"Cancel Invite"** on a pending invitation.
* **Expected Outcome:** User membership or pending invitation is revoked instantly.

#### UC-023: Soft Delete Organization
* **Target Screen:** Organization Settings -> Danger Zone
* **Execution Steps:**
  1. Click **"Delete Organization"** (commercial org only; personal org deletion blocked).
  2. Type organization name to confirm.
* **Expected Outcome:** Organization and linked entities soft-deleted (`deleted_at` timestamp set).

---

### Module B: Vehicle Ownership & Driver Assignment

#### UC-028: Manage Vehicle Operational Status
* **Target Screen:** Vehicle Detail Screen
* **Execution Steps:**
  1. Change vehicle status toggle between `ACTIVE`, `MAINTENANCE`, `INACTIVE`.
* **Expected Outcome:** Status chip updates instantly across fleet directory and summary cards.

#### UC-029: Vehicle Odometer Audit Log
* **Target Screen:** Vehicle Detail -> Odometer History Log
* **Execution Steps:**
  1. Manually update vehicle odometer reading.
  2. Open Odometer History tab.
* **Expected Outcome:** Audit entry created recording previous mileage, new mileage, delta, and actor.

#### UC-030: Vehicle Document Vault
* **Target Screen:** Vehicle Detail -> Document Vault Tab
* **Execution Steps:**
  1. Upload PDF / PNG document (Registration Certificate, Insurance Policy).
* **Expected Outcome:** File saved in secure document vault with expiration date reminders.

#### UC-031: Vehicle Ownership Transfer
* **Target Screen:** Vehicle Detail -> Transfer Ownership Modal
* **Execution Steps:**
  1. Select target organization for vehicle transfer.
  2. Click **"Confirm Transfer"**.
* **Expected Outcome:** Vehicle and linked maintenance records transferred to new tenant context.

#### UC-032 & UC-033: Assign & Unassign Primary Driver
* **Target Screen:** Vehicle Detail -> Primary Driver Section
* **Execution Steps:**
  1. Tap **"Assign Driver"** and select driver from org roster.
  2. Tap **"Unassign Driver"**.
* **Expected Outcome:** Vehicle primary driver ID updated and history log recorded.

---

### Module C: Offline Sync Engine & Local Storage

#### UC-090: Offline Queue Storage (WatermelonDB / Local SQLite)
* **Target Screen:** Any Feature Screen (Offline Mode)
* **Execution Steps:**
  1. Disconnect internet / enable Airplane Mode.
  2. Create a trip or log a maintenance item.
* **Expected Outcome:** Operation stored in local offline queue with `pending_sync` flag.

#### UC-091: Auto Sync Reconnection Handler
* **Target Screen:** App Banner / Network Status Indicator
* **Execution Steps:**
  1. Reconnect internet connection.
* **Expected Outcome:** Client detects network restoration and flushes pending offline queue to `/api/v1/sync/push`.

#### UC-092: Conflict Resolution Protocol
* **Target Screen:** Sync Management Drawer
* **Execution Steps:**
  1. Modify vehicle odometer offline on Device A and Device B simultaneously.
  2. Reconnect both devices.
* **Expected Outcome:** Last-Write-Wins (LWW) protocol resolves conflict based on server timestamp.

#### UC-093 & UC-094: Sync Status Indicator & Manual Force Sync
* **Target Screen:** Top App Bar Sync Icon
* **Execution Steps:**
  1. Inspect sync status icon (Green = Synced, Orange = Pending Changes, Red = Sync Error).
  2. Tap sync icon and click **"Force Sync Now"**.
* **Expected Outcome:** Delta sync push/pull executes instantly.

#### UC-095 & UC-096: Delta Patch Sync & Selective Entity Caching
* **Target Screen:** Sync Network Traffic Monitor
* **Execution Steps:**
  1. Trigger sync after making a single record edit.
* **Expected Outcome:** Only updated entity deltas (`last_pulled_at`) are transmitted in JSON payload.

#### UC-097 & UC-119: Local Encryption & Sync Delta Storage Schema
* **Target Screen:** Database Storage Layer
* **Execution Steps:**
  1. Inspect encrypted local SQLite database file.
* **Expected Outcome:** Sensitive local cache data encrypted via AES-256 key storage.

---

## 3. Manual QA Execution Scorecard (Sprint 03)

| Module | Use Case | Description | Target Screen | Status |
|:---|:---|:---|:---|:---:|
| **Org** | **UC-017** | Edit Organization Profile | Settings -> Profile | `[ ] PASS / [ ] FAIL` |
| **Org** | **UC-018** | Invite Member (Email/Phone) | Team Members Tab | `[ ] PASS / [ ] FAIL` |
| **Org** | **UC-019** | Accept Invitation Link | Invite Redemption | `[ ] PASS / [ ] FAIL` |
| **Org** | **UC-020** | Redeem Invitation Code | Code Entry Screen | `[ ] PASS / [ ] FAIL` |
| **Org** | **UC-021** | Remove Member from Org | Team Members Tab | `[ ] PASS / [ ] FAIL` |
| **Org** | **UC-022** | Cancel Pending Invitation | Team Members Tab | `[ ] PASS / [ ] FAIL` |
| **Org** | **UC-023** | Soft Delete Organization | Danger Zone | `[ ] PASS / [ ] FAIL` |
| **Vehicle**| **UC-028** | Manage Vehicle Status | Vehicle Detail | `[ ] PASS / [ ] FAIL` |
| **Vehicle**| **UC-029** | Odometer Audit Log | Vehicle Detail | `[ ] PASS / [ ] FAIL` |
| **Vehicle**| **UC-030** | Vehicle Document Vault | Document Vault Tab | `[ ] PASS / [ ] FAIL` |
| **Vehicle**| **UC-031** | Transfer Vehicle Ownership | Transfer Modal | `[ ] PASS / [ ] FAIL` |
| **Vehicle**| **UC-032** | Assign Primary Driver | Vehicle Detail | `[ ] PASS / [ ] FAIL` |
| **Vehicle**| **UC-033** | Unassign Primary Driver | Vehicle Detail | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-090** | Offline Queue Storage | Offline App Mode | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-091** | Auto Reconnection Handler | App Navigation | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-092** | Conflict Resolution | Sync Engine | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-093** | Sync Status Indicator | Top App Bar | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-094** | Manual Force Sync | Top App Bar | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-095** | Delta Patch Sync | Sync Engine | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-096** | Selective Entity Caching | Sync Engine | `[ ] PASS / [ ] FAIL` |
| **Sync** | **UC-097** | Local Storage Encryption | Local SQLite | `[ ] PASS / [ ] FAIL` |
| **Infra** | **UC-119** | Sync Delta Schema | Backend API | `[ ] PASS / [ ] FAIL` |
