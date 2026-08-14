# Graph Report - E:\Non_Office\Dev_Space\vibe_skool\veltrics\src  (2026-08-14)

## Corpus Check
- 178 files · ~319,495 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1650 nodes · 3702 edges · 70 communities detected
- Extraction: 48% EXTRACTED · 52% INFERRED · 0% AMBIGUOUS · INFERRED: 1939 edges (avg confidence: 0.54)
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

## God Nodes (most connected - your core abstractions)
1. `Organization` - 248 edges
2. `User` - 169 edges
3. `Vehicle` - 140 edges
4. `AuditLog` - 93 edges
5. `MaintenanceSchedule` - 82 edges
6. `ServiceRecord` - 68 edges
7. `UserOrganization` - 55 edges
8. `Driver` - 54 edges
9. `package:flutter/material.dart` - 36 edges
10. `AuthService` - 35 edges

## Surprising Connections (you probably didn't know these)
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_fuel_uc048.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_organizations_uc014.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_organizations_uc015.py
- `seed_database()` --calls--> `setup_db()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_organizations_uc016.py
- `OrganizationInvitation` --calls--> `test_uc019_accept_invitation_expired()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\organization_invitation.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_org_uc017_023.py

## Communities

### Community 0 - "Community 0"

Cohesion: 0.02
Nodes (208): DashboardSummaryResponse, get_cost_breakdown(), get_dashboard_summary(), UC-065: Cost Breakdown Charts per Vehicle (Fuel vs Maintenance vs Expenses)., UC-064: Get high-level KPI dashboard metrics summary for active organization., Driver, MaintenanceSchedule, ServiceRecord (+200 more)

### Community 1 - "Community 1"

Cohesion: 0.01
Nodes (224): dart:convert, ../../data/expense_repository.dart, ../../data/maintenance_repository.dart, ../../data/notification_repository.dart, ../../data/trip_repository.dart, ../../domain/expense_model.dart, ../../domain/maintenance_model.dart, ../../domain/notification_model.dart (+216 more)

### Community 2 - "Community 2"

Cohesion: 0.04
Nodes (119): AuditLog, AuditService, UC-012: Audit Log Recording for Authentication Events.         Extracts event m, Base, Exception, ExpenseLog, FuelLog, log_fuel_entry() (+111 more)

### Community 3 - "Community 3"

Cohesion: 0.07
Nodes (81): log_event(), AuthSessionDTO, forgot_password(), ForgotPasswordRequest, ForgotPasswordResponse, login(), LoginRequest, logout() (+73 more)

### Community 4 - "Community 4"

Cohesion: 0.02
Nodes (80): add_vehicle_screen.dart, ../../data/vehicle_repository.dart, ../domain/vehicle_document_model.dart, ../../domain/vehicle_model.dart, build, _buildActionButton, Column, dispose (+72 more)

### Community 5 - "Community 5"

Cohesion: 0.04
Nodes (46): ../../data/auth_repository.dart, ../../domain/user_model.dart, AuthRepository, Exception, jsonDecode, _register, AlertDialog, build (+38 more)

### Community 6 - "Community 6"

Cohesion: 0.1
Nodes (40): cancel_subscription(), create_checkout_session(), execute_downgrade_protocol(), get_subscription_status(), PaymentService, reconcile_safepay_webhook(), verify_safepay_signature(), cancel_subscription() (+32 more)

### Community 7 - "Community 7"

Cohesion: 0.11
Nodes (33): create_fuel_log(), delete_fuel_log(), get_fuel_trends(), list_fuel_anomalies(), list_fuel_logs(), Config, FuelLogCreate, FuelLogResponse (+25 more)

### Community 8 - "Community 8"

Cohesion: 0.16
Nodes (33): Config, MileageSummaryResponse, QuickTripCreate, create_trip(), get_trips(), quick_log_trip(), start_trip(), TripCreate (+25 more)

### Community 9 - "Community 9"

Cohesion: 0.05
Nodes (36): ../../data/fuel_repository.dart, ../../domain/fuel_log_model.dart, Exception, FuelRepository, AlertDialog, build, _buildDetailRow, _buildFuelLogCard (+28 more)

### Community 10 - "Community 10"

Cohesion: 0.06
Nodes (30): ../../data/dashboard_repository.dart, ../../domain/cost_breakdown_model.dart, ../../domain/dashboard_model.dart, DashboardRepository, Exception, build, _buildKpiCard, _buildOnboardingCard (+22 more)

### Community 11 - "Community 11"

Cohesion: 0.06
Nodes (33): adBg, adFg, build, buildTextTheme, _buildTheme, Container, dark, _darkColorScheme (+25 more)

### Community 12 - "Community 12"

Cohesion: 0.14
Nodes (25): AdService, submit_enterprise_inquiry(), verify_and_claim_ad_reward(), AdRewardVerifyRequest, AdRewardVerifyResponse, EnterpriseInquiryRequest, EnterpriseInquiryResponse, UC-100 & UC-120 & UC-122: Verify Rewarded Ad Completion Signature Token & Claim (+17 more)

### Community 13 - "Community 13"

Cohesion: 0.07
Nodes (26): ../../data/organization_repository.dart, ../../domain/organization_invitation_model.dart, ../../domain/organization_model.dart, Exception, jsonDecode, OrganizationRepository, AlertDialog, build (+18 more)

### Community 14 - "Community 14"

Cohesion: 0.17
Nodes (23): Config, ExpenseLogCreate, ExpenseLogResponse, ExpenseLogUpdate, ExpensePaginatedResponse, ExpenseSummaryResponse, QuickExpenseCreate, get_expenses() (+15 more)

### Community 15 - "Community 15"

Cohesion: 0.19
Nodes (20): DeviceTokenCreate, DeviceTokenResponse, NotificationPaginatedResponse, NotificationPreferencesUpdate, NotificationResponse, mark_all_as_read(), mark_as_read(), register_device_token() (+12 more)

### Community 16 - "Community 16"

Cohesion: 0.23
Nodes (19): bulk_accept_maintenance_schedules(), BulkAcceptSchedulesRequest, create_maintenance_schedule(), delete_maintenance_schedule(), get_maintenance_schedules(), get_service_history(), log_maintenance_task(), MaintenanceScheduleCreate (+11 more)

### Community 17 - "Community 17"

Cohesion: 0.1
Nodes (16): AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,, AC 4 (Account Linking Flow A1): WHEN an existing user registered via email, Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized., Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized., Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F, Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT, AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2, AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP (+8 more)

### Community 18 - "Community 18"

Cohesion: 0.11
Nodes (1): test_uc019_accept_invitation_expired()

### Community 19 - "Community 19"

Cohesion: 0.12
Nodes (5): lifespan(), test_data(), test_uc094_sync_conflict_server_wins(), test_uc096_delta_sync_full_snapshot(), test_uc096_delta_sync_with_since_timestamp()

### Community 20 - "Community 20"

Cohesion: 0.12
Nodes (1): test_uc031_restore_vehicle_quota_exceeded()

### Community 21 - "Community 21"

Cohesion: 0.13
Nodes (12): UC-014: Blank or whitespace organization name rejected with HTTP 422., UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization, UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found., UC-014: POST /api/v1/organizations creates commercial organization and sets owne, UC-014: POST /api/v1/organizations/personal auto-creates personal organization f, setup_db(), test_auto_create_personal_organization(), test_create_commercial_organization_success() (+4 more)

### Community 22 - "Community 22"

Cohesion: 0.13
Nodes (12): UC-015: POST /api/v1/organizations/switch switches active context for valid user, UC-015: Switch attempt to organization owned by another user yields HTTP 403 For, UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found., UC-015: GET /api/v1/organizations/active returns current primary organization fo, UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N, setup_db(), test_get_active_organization_not_found(), test_get_active_organization_success() (+4 more)

### Community 23 - "Community 23"

Cohesion: 0.14
Nodes (10): Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F, Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT, AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200, Edge Case: Incorrect password returns HTTP 401 Unauthorized., Edge Case: Unregistered email returns HTTP 401 Unauthorized., test_uc004_disabled_user(), test_uc004_incorrect_password(), test_uc004_login_success() (+2 more)

### Community 24 - "Community 24"

Cohesion: 0.14
Nodes (10): AC 4: WHEN an invalid token or token of wrong type (e.g. access token) is submit, AC 5: WHEN a new password does not satisfy password policy (min 8 chars, 1 upper, AC 1: WHEN a registered user requests a password reset link/token for their emai, AC 2: WHEN a reset request is submitted for a non-existent email     THE SYSTEM, AC 3: WHEN a user submits a valid reset token and strong new password     THE S, test_uc006_forgot_password_success(), test_uc006_forgot_password_user_not_found(), test_uc006_reset_password_invalid_or_wrong_token() (+2 more)

### Community 25 - "Community 25"

Cohesion: 0.29
Nodes (9): create_access_token(), create_test_user_and_org(), generate_admob_ssv_signature(), UC-089: Contact Enterprise Sales Inquiry Submission (>25 Fleets), test_uc086_087_vehicle_and_driver_quota_wall_enforcement(), test_uc089_enterprise_sales_inquiry_submission(), test_uc100_120_verify_ad_reward_signature_and_slot_increment(), test_uc101_pro_tier_ad_suppression_logic() (+1 more)

### Community 26 - "Community 26"

Cohesion: 0.17
Nodes (8): Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu, Edge Case: Missing email or missing password for email auth provider returns HTT, AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT, Alternate Flow A1: Account Linking     If user signed up via Google, submitting, test_uc003_account_linking_email(), test_uc003_email_registration_success(), test_uc003_missing_email_or_password(), test_uc003_weak_password_validation()

### Community 27 - "Community 27"
_Unable to determine domain due to missing code entities._
Cohesion: 0.17
Nodes (8): AC 3: GIVEN a profile update request with invalid display name length (< 2 chars, AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro, AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u, AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P, test_uc007_display_name_validation(), test_uc007_get_and_patch_user_profile(), test_uc007_multi_tenant_role_authorization(), test_uc007_profile_completion_endpoint()

### Community 28 - "Community 28"
_Unable to determine domain due to missing code entities._
Cohesion: 0.17
Nodes (8): AC 3: GIVEN a profile update request with invalid full name length (< 2 characte, AC 4: GIVEN an unauthenticated request to profile endpoints without user identit, AC 1: GIVEN an authenticated registered user     WHEN they request GET /api/v1/, AC 2: GIVEN an authenticated user updating their profile details     WHEN they, test_uc008_get_user_profile(), test_uc008_patch_user_profile(), test_uc008_profile_field_validation(), test_uc008_unauthenticated_access()

### Community 29 - "Community 29"
_Unable to determine domain due to missing code entities._
Cohesion: 0.17
Nodes (8): AC 4: GIVEN a newly issued access token from POST /api/v1/auth/refresh     WHEN, AC 1: GIVEN a valid active refresh token     WHEN submitted to POST /api/v1/aut, AC 2: GIVEN an invalid, expired, or non-refresh token (e.g. access or reset toke, AC 3: GIVEN a refresh token for a disabled or soft-deleted user account     WHE, test_uc009_access_token_authorization(), test_uc009_disabled_user_refresh_rejection(), test_uc009_invalid_or_expired_refresh_token(), test_uc009_valid_token_refresh()

### Community 30 - "Community 30"
_Unable to determine domain due to missing code entities._
Cohesion: 0.2
Nodes (6): Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ, AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store "facebook" insid, Alternate Flow A1: Account Linking     If email matches existing account with d, test_uc002_account_linking_facebook(), test_uc002_facebook_missing_email_returns_400(), test_uc002_new_user_facebook_registration()

### Community 31 - "Community 31"
_Unable to determine domain due to missing code entities._
Cohesion: 0.2
Nodes (7): UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a, UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh, UC-048 Main Flow: App queries GET /api/v1/fuel with pagination (page=1, limit=2), setup_db(), test_fleet_aggregate_average_efficiency(), test_fuel_efficiency_trends_monthly_aggregation(), test_get_fuel_logs_paginated()

### Community 32 - "Community 32"
_Unable to determine domain due to missing code entities._
Cohesion: 0.2
Nodes (1): setup_db()

### Community 33 - "Community 33"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (4): AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr, AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL, test_uc001_existing_user_google_one_tap_returns_existing_data(), test_uc001_new_user_google_one_tap_creates_user_and_personal_org()

### Community 34 - "Community 34"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (0): 

### Community 35 - "Community 35"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 36 - "Community 36"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 37 - "Community 37"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 38 - "Community 38"

Cohesion: 0.29
Nodes (0): 

### Community 39 - "Community 39"

Cohesion: 0.29
Nodes (0): 

### Community 40 - "Community 40"

Cohesion: 0.29
Nodes (0): 

### Community 41 - "Community 41"

Cohesion: 0.33
Nodes (0): 

### Community 42 - "Community 42"
_Unable to determine domain due to missing code entities._
Cohesion: 0.33
Nodes (0): 

### Community 43 - "Community 43"

Cohesion: 0.33
Nodes (0): 

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

## Knowledge Gaps
- **491 isolated node(s):** `UC-001 & UC-002: Register or Log In with OAuth Providers (Google, Facebook)`, `UC-080: Initiate Pro Subscription Checkout (Safepay)`, `UC-118: Trigger Database Migration & Master Seeding Infrastructure.     Pre-pop`, `UC-063: Upload receipt image file.`, `Config` (+486 more)
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