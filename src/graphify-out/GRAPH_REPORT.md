# Graph Report - E:\Non_Office\Dev_Space\vibe_skool\veltrics\src  (2026-08-14)

## Corpus Check
- 198 files · ~379,514 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1862 nodes · 4273 edges · 75 communities detected
- Extraction: 46% EXTRACTED · 54% INFERRED · 0% AMBIGUOUS · INFERRED: 2290 edges (avg confidence: 0.54)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]

## God Nodes (most connected - your core abstractions)
1. `Organization` - 274 edges
2. `User` - 214 edges
3. `Vehicle` - 178 edges
4. `MaintenanceSchedule` - 103 edges
5. `ServiceRecord` - 101 edges
6. `AuditLog` - 93 edges
7. `UserOrganization` - 85 edges
8. `Driver` - 65 edges
9. `FuelLog` - 45 edges
10. `package:flutter/material.dart` - 40 edges

## Surprising Connections (you probably didn't know these)
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_dashboard_uc064.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_maintenance_uc034.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_maintenance_uc035.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_maintenance_uc036.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_maintenance_uc037.py

## Communities

### Community 0 - "Community 0"

Cohesion: 0.02
Nodes (196): ExpenseLog, FuelLog, log_fuel_entry(), accept_organization_invitation(), get_invitation_by_token(), is_expired(), UC-020: Redeem Org Invitation Code for new user during signup/onboard., UC-019: Inspect / validate organization invitation token details.     Returns HT (+188 more)

### Community 1 - "Community 1"

Cohesion: 0.01
Nodes (182): ../../data/expense_repository.dart, ../../data/notification_repository.dart, ../../data/trip_repository.dart, build, CounterScreen, _CounterScreenState, _incrementCounter, _resetCounter (+174 more)

### Community 2 - "Community 2"

Cohesion: 0.04
Nodes (159): AuditLog, UC-012: Audit Log Recording for Authentication Events.         Extracts event m, Base, UC-065: Cost Breakdown Charts per Vehicle (Fuel vs Maintenance vs Expenses)., UC-064: Get high-level KPI dashboard metrics summary for active organization., Driver, MaintenanceSchedule, ServiceRecord (+151 more)

### Community 3 - "Community 3"

Cohesion: 0.05
Nodes (93): AuditService, log_event(), AuthSessionDTO, forgot_password(), ForgotPasswordRequest, ForgotPasswordResponse, login(), LoginRequest (+85 more)

### Community 4 - "Community 4"

Cohesion: 0.02
Nodes (68): UC-118: Trigger Database Migration & Master Seeding Infrastructure.     Pre-pop, Idempotent seeding script for Vehicle Master Catalogue and Default Maintenance T, seed_database(), trigger_seed_database(), test_uc118_idempotent_database_seeding(), test_uc118_seed_api_endpoint(), setup_db(), test_create_fuel_log_success() (+60 more)

### Community 5 - "Community 5"

Cohesion: 0.02
Nodes (83): dart:convert, ../../data/fuel_repository.dart, ../../data/organization_repository.dart, ../../domain/expense_model.dart, ../../domain/fuel_log_model.dart, ../../domain/notification_model.dart, ../../domain/organization_invitation_model.dart, ../../domain/organization_model.dart (+75 more)

### Community 6 - "Community 6"

Cohesion: 0.02
Nodes (80): add_vehicle_screen.dart, ../../data/vehicle_repository.dart, ../domain/vehicle_document_model.dart, ../../domain/vehicle_model.dart, build, _buildActionButton, Column, dispose (+72 more)

### Community 7 - "Community 7"

Cohesion: 0.03
Nodes (61): build, _buildAvailabilityWidget, _buildCostRankingCard, _buildKpiCard, _buildKpiHeaderGrid, Card, DataRow, Divider (+53 more)

### Community 8 - "Community 8"

Cohesion: 0.04
Nodes (46): ../../data/auth_repository.dart, ../../domain/user_model.dart, AuthRepository, Exception, jsonDecode, _register, AlertDialog, build (+38 more)

### Community 9 - "Community 9"

Cohesion: 0.12
Nodes (42): add_custom_maintenance_schedule(), bulk_accept_maintenance_schedules(), BulkAcceptSchedulesRequest, create_maintenance_schedule(), delete_maintenance_schedule(), delete_service_record(), get_maintenance_schedules(), get_service_history() (+34 more)

### Community 10 - "Community 10"

Cohesion: 0.1
Nodes (40): cancel_subscription(), create_checkout_session(), execute_downgrade_protocol(), get_subscription_status(), PaymentService, reconcile_safepay_webhook(), verify_safepay_signature(), cancel_subscription() (+32 more)

### Community 11 - "Community 11"

Cohesion: 0.05
Nodes (42): ../../data/maintenance_repository.dart, ../../domain/maintenance_model.dart, Exception, MaintenanceRepository, build, dispose, initState, LogMaintenanceScreen (+34 more)

### Community 12 - "Community 12"

Cohesion: 0.11
Nodes (33): create_fuel_log(), delete_fuel_log(), get_fuel_trends(), list_fuel_anomalies(), list_fuel_logs(), Config, FuelLogCreate, FuelLogResponse (+25 more)

### Community 13 - "Community 13"

Cohesion: 0.16
Nodes (33): Config, MileageSummaryResponse, QuickTripCreate, create_trip(), get_trips(), quick_log_trip(), start_trip(), TripCreate (+25 more)

### Community 14 - "Community 14"

Cohesion: 0.06
Nodes (30): ../../data/dashboard_repository.dart, ../../domain/cost_breakdown_model.dart, ../../domain/dashboard_model.dart, DashboardRepository, Exception, build, _buildKpiCard, _buildOnboardingCard (+22 more)

### Community 15 - "Community 15"

Cohesion: 0.15
Nodes (27): CostBreakdownItem, CostBreakdownResponse, DashboardSummaryResponse, get_cost_ranking_table(), get_dashboard_layout(), get_dashboard_summary(), get_manager_kpi_dashboard(), get_vehicle_availability_widget() (+19 more)

### Community 16 - "Community 16"

Cohesion: 0.17
Nodes (23): Config, ExpenseLogCreate, ExpenseLogResponse, ExpenseLogUpdate, ExpensePaginatedResponse, ExpenseSummaryResponse, QuickExpenseCreate, get_expenses() (+15 more)

### Community 17 - "Community 17"

Cohesion: 0.16
Nodes (21): AppNotification, BillingAlertCreateRequest, BillingAlertResponse, NotificationItemResponse, NotificationPreferenceDTO, PurgeTokenResponse, mark_as_read(), register_device_token() (+13 more)

### Community 18 - "Community 18"

Cohesion: 0.18
Nodes (17): detect_anomalies(), DriverAnomalyItem, DriverAnomalyScanResponse, DriverLeaderboardEntry, DriverLeaderboardResponse, DriverPerformanceDetailResponse, DriverSafetyCertificateResponse, DriverSafetyScoreResponse (+9 more)

### Community 19 - "Community 19"

Cohesion: 0.11
Nodes (1): test_uc019_accept_invitation_expired()

### Community 20 - "Community 20"

Cohesion: 0.26
Nodes (12): AdService, submit_enterprise_inquiry(), verify_and_claim_ad_reward(), AdRewardVerifyRequest, AdRewardVerifyResponse, EnterpriseInquiryRequest, EnterpriseInquiryResponse, UC-100 & UC-120 & UC-122: Verify Rewarded Ad Completion Signature Token & Claim (+4 more)

### Community 21 - "Community 21"

Cohesion: 0.12
Nodes (1): test_uc031_restore_vehicle_quota_exceeded()

### Community 22 - "Community 22"

Cohesion: 0.13
Nodes (4): lifespan(), test_uc094_sync_conflict_server_wins(), test_uc096_delta_sync_full_snapshot(), test_uc096_delta_sync_with_since_timestamp()

### Community 23 - "Community 23"

Cohesion: 0.2
Nodes (11): ExportEmailRequest, ExportEmailResponse, email_monthly_summary(), generate_fuel_expenses_csv(), generate_maintenance_pdf(), email_monthly_summary(), export_fuel_expenses_csv(), export_maintenance_pdf() (+3 more)

### Community 24 - "Community 24"

Cohesion: 0.14
Nodes (10): AC 4: WHEN an invalid token or token of wrong type (e.g. access token) is submit, AC 5: WHEN a new password does not satisfy password policy (min 8 chars, 1 upper, AC 1: WHEN a registered user requests a password reset link/token for their emai, AC 2: WHEN a reset request is submitted for a non-existent email     THE SYSTEM, AC 3: WHEN a user submits a valid reset token and strong new password     THE S, test_uc006_forgot_password_success(), test_uc006_forgot_password_user_not_found(), test_uc006_reset_password_invalid_or_wrong_token() (+2 more)

### Community 25 - "Community 25"

Cohesion: 0.29
Nodes (9): create_access_token(), create_test_user_and_org(), generate_admob_ssv_signature(), UC-089: Contact Enterprise Sales Inquiry Submission (>25 Fleets), test_uc086_087_vehicle_and_driver_quota_wall_enforcement(), test_uc089_enterprise_sales_inquiry_submission(), test_uc100_120_verify_ad_reward_signature_and_slot_increment(), test_uc101_pro_tier_ad_suppression_logic() (+1 more)

### Community 26 - "Community 26"

Cohesion: 0.17
Nodes (8): AC 3: GIVEN a profile update request with invalid full name length (< 2 characte, AC 4: GIVEN an unauthenticated request to profile endpoints without user identit, AC 1: GIVEN an authenticated registered user     WHEN they request GET /api/v1/, AC 2: GIVEN an authenticated user updating their profile details     WHEN they, test_uc008_get_user_profile(), test_uc008_patch_user_profile(), test_uc008_profile_field_validation(), test_uc008_unauthenticated_access()

### Community 27 - "Community 27"
_Unable to determine domain due to missing code entities._
Cohesion: 0.17
Nodes (8): AC 4: GIVEN a newly issued access token from POST /api/v1/auth/refresh     WHEN, AC 1: GIVEN a valid active refresh token     WHEN submitted to POST /api/v1/aut, AC 2: GIVEN an invalid, expired, or non-refresh token (e.g. access or reset toke, AC 3: GIVEN a refresh token for a disabled or soft-deleted user account     WHE, test_uc009_access_token_authorization(), test_uc009_disabled_user_refresh_rejection(), test_uc009_invalid_or_expired_refresh_token(), test_uc009_valid_token_refresh()

### Community 28 - "Community 28"
_Unable to determine domain due to missing code entities._
Cohesion: 0.17
Nodes (8): AC 3: GIVEN a malformed or invalid refresh token     WHEN submitted to POST /ap, AC 4: GIVEN a refresh token that has already been revoked     WHEN logout is ca, AC 1: GIVEN an authenticated user session with a valid refresh token     WHEN s, AC 2: GIVEN a revoked refresh token     WHEN submitted to POST /api/v1/auth/ref, test_uc010_invalid_or_malformed_logout_token(), test_uc010_repeat_logout_idempotency(), test_uc010_revoked_token_refresh_rejection(), test_uc010_successful_logout_and_revocation()

### Community 29 - "Community 29"
_Unable to determine domain due to missing code entities._
Cohesion: 0.36
Nodes (8): InspectionCreateRequest, InspectionResponse, create_inspection(), get_user_org_id(), get_vehicle_inspections(), UC-044: Log Vehicle Safety Inspection Checklist., UC-044: Fetch Vehicle Safety Inspections., VehicleInspection

### Community 30 - "Community 30"
_Unable to determine domain due to missing code entities._
Cohesion: 0.36
Nodes (8): Vendor, VendorCreateRequest, VendorResponse, create_vendor(), get_user_org_id(), get_vendors(), UC-043: Create Maintenance Vendor., UC-043: List Maintenance Vendors.

### Community 31 - "Community 31"
_Unable to determine domain due to missing code entities._
Cohesion: 0.22
Nodes (0): 

### Community 32 - "Community 32"
_Unable to determine domain due to missing code entities._
Cohesion: 0.22
Nodes (1): setup_db()

### Community 33 - "Community 33"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (1): setup_db()

### Community 34 - "Community 34"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (1): setup_db()

### Community 35 - "Community 35"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (1): setup_db()

### Community 36 - "Community 36"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (1): setup_db()

### Community 37 - "Community 37"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (1): setup_db()

### Community 38 - "Community 38"

Cohesion: 0.29
Nodes (3): test_uc002_account_linking_facebook(), test_uc002_facebook_missing_email_returns_400(), test_uc002_new_user_facebook_registration()

### Community 39 - "Community 39"

Cohesion: 0.29
Nodes (1): setup_db()

### Community 40 - "Community 40"

Cohesion: 0.29
Nodes (0): 

### Community 41 - "Community 41"

Cohesion: 0.29
Nodes (1): setup_db()

### Community 42 - "Community 42"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (1): setup_db()

### Community 43 - "Community 43"

Cohesion: 0.33
Nodes (2): test_uc001_existing_user_google_one_tap_returns_existing_data(), test_uc001_new_user_google_one_tap_creates_user_and_personal_org()

### Community 44 - "Community 44"

Cohesion: 0.33
Nodes (0): 

### Community 45 - "Community 45"
_Automatically registers Flutter plugins with the platform activity so Dart code can access native plugin functionalities._
Cohesion: 0.4
Nodes (4): AuthSession, OrganizationModel, RefreshTokenTokens, UserModel

### Community 46 - "Community 46"

Cohesion: 0.4
Nodes (4): DeltaSyncResponseModel, SyncBatchResponseModel, SyncOperationEnvelopeModel, SyncOperationResultModel

### Community 47 - "Community 47"

Cohesion: 0.5
Nodes (3): FuelLogModel, FuelMonthlyTrendModel, FuelTrendsModel

### Community 48 - "Community 48"

Cohesion: 0.5
Nodes (3): MileageSummaryModel, TripModel, TripSummaryModel

### Community 49 - "Community 49"

Cohesion: 0.5
Nodes (3): VehicleDetailModel, VehicleModel, VehicleTypeModel

### Community 50 - "Community 50"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (0): 

### Community 51 - "Community 51"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (2): UC-063: Upload receipt image file., upload_receipt()

### Community 52 - "Community 52"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (2): BaseSettings, Settings

### Community 53 - "Community 53"
_Handles the primary screen and user interactions at app launch._
Cohesion: 0.67
Nodes (1): GeneratedPluginRegistrant

### Community 54 - "Community 54"

Cohesion: 0.67
Nodes (2): CostBreakdownItemModel, CostBreakdownModel

### Community 55 - "Community 55"

Cohesion: 0.67
Nodes (2): ExpenseModel, ExpenseSummaryModel

### Community 56 - "Community 56"

Cohesion: 0.67
Nodes (2): MaintenanceScheduleModel, ServiceRecordModel

### Community 57 - "Community 57"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (2): NotificationModel, NotificationPaginatedModel

### Community 58 - "Community 58"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (0): 

### Community 59 - "Community 59"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 60 - "Community 60"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 61 - "Community 61"

Cohesion: 1.0
Nodes (1): MainActivity

### Community 62 - "Community 62"

Cohesion: 1.0
Nodes (1): DashboardSummaryModel

### Community 63 - "Community 63"

Cohesion: 1.0
Nodes (1): OrganizationInvitationModel

### Community 64 - "Community 64"

Cohesion: 1.0
Nodes (1): OrganizationModel

### Community 65 - "Community 65"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (1): VehicleDocumentModel

### Community 66 - "Community 66"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 67 - "Community 67"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 68 - "Community 68"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 69 - "Community 69"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 70 - "Community 70"

Cohesion: 1.0
Nodes (1): UC-072: Register FCM Device Push Token.

### Community 71 - "Community 71"

Cohesion: 1.0
Nodes (1): UC-073: In-App Notification Center Directory & Unread Counter.

### Community 72 - "Community 72"

Cohesion: 1.0
Nodes (1): UC-074: Mark Notification as Read / Deep Link Routing.

### Community 73 - "Community 73"

Cohesion: 1.0
Nodes (1): UC-073 (A1): Mark All Notifications as Read.

### Community 74 - "Community 74"

Cohesion: 1.0
Nodes (1): UC-075: Configure Notification Channel Preferences.

## Knowledge Gaps
- **545 isolated node(s):** `UC-001 & UC-002: Register or Log In with OAuth Providers (Google, Facebook)`, `UC-080: Initiate Pro Subscription Checkout (Safepay)`, `UC-118: Trigger Database Migration & Master Seeding Infrastructure.     Pre-pop`, `UC-063: Upload receipt image file.`, `Config` (+540 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 59`** (2 nodes): `session.py`, `get_db()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (2 nodes): `get_cost_breakdown()`, `dashboard_service.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 61`** (2 nodes): `MainActivity.kt`, `MainActivity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (2 nodes): `dashboard_model.dart`, `DashboardSummaryModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `organization_invitation_model.dart`, `OrganizationInvitationModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (2 nodes): `organization_model.dart`, `OrganizationModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (2 nodes): `vehicle_document_model.dart`, `VehicleDocumentModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (1 nodes): `run_and_report.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (1 nodes): `run_tests.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (1 nodes): `UC-072: Register FCM Device Push Token.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (1 nodes): `UC-073: In-App Notification Center Directory & Unread Counter.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 72`** (1 nodes): `UC-074: Mark Notification as Read / Deep Link Routing.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (1 nodes): `UC-073 (A1): Mark All Notifications as Read.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (1 nodes): `UC-075: Configure Notification Channel Preferences.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.