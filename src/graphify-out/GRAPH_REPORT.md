# Graph Report - E:\Non_Office\Dev_Space\vibe_skool\veltrics\src  (2026-08-14)

## Corpus Check
- 153 files · ~71,070 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1405 nodes · 2679 edges · 61 communities detected
- Extraction: 56% EXTRACTED · 44% INFERRED · 0% AMBIGUOUS · INFERRED: 1187 edges (avg confidence: 0.54)
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

## God Nodes (most connected - your core abstractions)
1. `Organization` - 199 edges
2. `User` - 115 edges
3. `Vehicle` - 102 edges
4. `MaintenanceSchedule` - 53 edges
5. `ServiceRecord` - 40 edges
6. `AuthService` - 35 edges
7. `AuditLog` - 32 edges
8. `package:flutter/material.dart` - 32 edges
9. `../../../../theme/app_theme.dart` - 28 edges
10. `seed_database()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `setup_db()` --calls--> `seed_database()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_fuel_uc048.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py
- `setup_db()` --calls--> `seed_database()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_organizations_uc014.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py
- `setup_db()` --calls--> `seed_database()`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_organizations_uc015.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\db\seed.py
- `UC-064: Get high-level KPI dashboard metrics summary for active organization.` --uses--> `CostBreakdownResponse`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\api\v1\dashboard.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\schemas\cost_breakdown.py
- `UC-065: Cost Breakdown Charts per Vehicle (Fuel vs Maintenance vs Expenses).` --uses--> `CostBreakdownResponse`  [INFERRED]
  E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\api\v1\dashboard.py → E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\schemas\cost_breakdown.py

## Communities

### Community 0 - "Community 0"

Cohesion: 0.02
Nodes (200): AuditLog, UC-012: Audit Log Recording for Authentication Events.         Extracts event m, Base, DashboardSummaryResponse, get_cost_breakdown(), get_dashboard_summary(), UC-065: Cost Breakdown Charts per Vehicle (Fuel vs Maintenance vs Expenses)., UC-064: Get high-level KPI dashboard metrics summary for active organization. (+192 more)

### Community 1 - "Community 1"

Cohesion: 0.02
Nodes (120): OrganizationInvitation, OrganizationInvitationCreate, OrganizationInvitationResponse, OrganizationCreate, OrganizationResponse, PersonalOrganizationCreate, SwitchOrganizationRequest, SwitchOrganizationResponse (+112 more)

### Community 2 - "Community 2"

Cohesion: 0.02
Nodes (121): add_vehicle_screen.dart, ../../data/expense_repository.dart, ../../data/notification_repository.dart, ../../data/vehicle_repository.dart, ../../domain/vehicle_model.dart, build, CounterScreen, _CounterScreenState (+113 more)

### Community 3 - "Community 3"

Cohesion: 0.03
Nodes (69): dart:convert, ../../data/auth_repository.dart, ../../data/fuel_repository.dart, ../../domain/expense_model.dart, ../../domain/fuel_log_model.dart, ../../domain/notification_model.dart, ../../domain/user_model.dart, AuthRepository (+61 more)

### Community 4 - "Community 4"

Cohesion: 0.1
Nodes (69): log_event(), AuthSessionDTO, forgot_password(), ForgotPasswordRequest, ForgotPasswordResponse, login(), LoginRequest, logout() (+61 more)

### Community 5 - "Community 5"

Cohesion: 0.04
Nodes (43): ../../data/trip_repository.dart, ../../domain/trip_model.dart, Exception, TripRepository, build, _buildDetailRow, _buildStatItem, Center (+35 more)

### Community 6 - "Community 6"

Cohesion: 0.05
Nodes (42): ../../data/maintenance_repository.dart, ../../domain/maintenance_model.dart, Exception, MaintenanceRepository, build, dispose, initState, LogMaintenanceScreen (+34 more)

### Community 7 - "Community 7"

Cohesion: 0.14
Nodes (34): Config, MileageSummaryResponse, QuickTripCreate, create_trip(), get_trips(), quick_log_trip(), start_trip(), Trip (+26 more)

### Community 8 - "Community 8"

Cohesion: 0.11
Nodes (33): create_fuel_log(), delete_fuel_log(), get_fuel_trends(), list_fuel_anomalies(), list_fuel_logs(), Config, FuelLogCreate, FuelLogResponse (+25 more)

### Community 9 - "Community 9"

Cohesion: 0.05
Nodes (41): build, _buildActionButton, Column, dispose, initState, ScaleTransition, SizedBox, _toggle (+33 more)

### Community 10 - "Community 10"

Cohesion: 0.06
Nodes (30): ../../data/dashboard_repository.dart, ../../domain/cost_breakdown_model.dart, ../../domain/dashboard_model.dart, DashboardRepository, Exception, build, _buildKpiCard, _buildOnboardingCard (+22 more)

### Community 11 - "Community 11"

Cohesion: 0.06
Nodes (33): adBg, adFg, build, buildTextTheme, _buildTheme, Container, dark, _darkColorScheme (+25 more)

### Community 12 - "Community 12"

Cohesion: 0.17
Nodes (23): Config, ExpenseLogCreate, ExpenseLogResponse, ExpenseLogUpdate, ExpensePaginatedResponse, ExpenseSummaryResponse, QuickExpenseCreate, get_expenses() (+15 more)

### Community 13 - "Community 13"

Cohesion: 0.07
Nodes (25): ../../data/organization_repository.dart, ../../domain/organization_invitation_model.dart, ../../domain/organization_model.dart, Exception, OrganizationRepository, AlertDialog, build, Center (+17 more)

### Community 14 - "Community 14"

Cohesion: 0.17
Nodes (21): DeviceTokenCreate, DeviceTokenResponse, NotificationPaginatedResponse, NotificationPreferencesUpdate, NotificationResponse, mark_all_as_read(), mark_as_read(), register_device_token() (+13 more)

### Community 15 - "Community 15"

Cohesion: 0.23
Nodes (19): bulk_accept_maintenance_schedules(), BulkAcceptSchedulesRequest, create_maintenance_schedule(), delete_maintenance_schedule(), get_maintenance_schedules(), get_service_history(), log_maintenance_task(), MaintenanceScheduleCreate (+11 more)

### Community 16 - "Community 16"

Cohesion: 0.09
Nodes (21): build, _buildDetailRow, _buildEditForm, _buildHeaderCard, _buildViewDetailsCard, _cancelEdit, Card, dispose (+13 more)

### Community 17 - "Community 17"

Cohesion: 0.09
Nodes (20): AlertDialog, build, _buildDetailRow, Card, Center, Chip, Divider, ExpenseHistoryScreen (+12 more)

### Community 18 - "Community 18"

Cohesion: 0.13
Nodes (14): AuditService, Exception, AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS, AC 4: System records USER_LOGOUT audit entry upon session termination., Edge Case: Audit log DB write exception is handled safely and does not block use, AC 1: System creates immutable AuditLog entry upon user registration., AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat, A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None. (+6 more)

### Community 19 - "Community 19"

Cohesion: 0.14
Nodes (10): Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F, Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT, AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200, Edge Case: Incorrect password returns HTTP 401 Unauthorized., Edge Case: Unregistered email returns HTTP 401 Unauthorized., test_uc004_disabled_user(), test_uc004_incorrect_password(), test_uc004_login_success() (+2 more)

### Community 20 - "Community 20"

Cohesion: 0.18
Nodes (9): A1: User can revoke all other active sessions., AC 1: WHEN GET /api/v1/users/me/sessions is called THE SYSTEM SHALL return activ, AC 2: User can revoke a specific session., Acceptance Criterion: WHEN a session is revoked via API THE SYSTEM SHALL block a, test_uc013_list_active_sessions(), test_uc013_revoke_all_other_sessions(), test_uc013_revoke_session(), test_uc013_revoked_session_blocked_on_refresh() (+1 more)

### Community 21 - "Community 21"

Cohesion: 0.17
Nodes (8): Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu, Edge Case: Missing email or missing password for email auth provider returns HTT, AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT, Alternate Flow A1: Account Linking     If user signed up via Google, submitting, test_uc003_account_linking_email(), test_uc003_email_registration_success(), test_uc003_missing_email_or_password(), test_uc003_weak_password_validation()

### Community 22 - "Community 22"

Cohesion: 0.17
Nodes (8): AC 3: GIVEN a profile update request with invalid display name length (< 2 chars, AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro, AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u, AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P, test_uc007_display_name_validation(), test_uc007_get_and_patch_user_profile(), test_uc007_multi_tenant_role_authorization(), test_uc007_profile_completion_endpoint()

### Community 23 - "Community 23"

Cohesion: 0.21
Nodes (7): AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac, AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked, AC 2: GIVEN a user who is the sole owner of an active non-personal organization, test_uc011_post_deletion_auth_rejection(), test_uc011_sole_owner_blocking(), test_uc011_successful_account_deletion_and_anonymization(), UserOrganization

### Community 24 - "Community 24"

Cohesion: 0.2
Nodes (1): setup_db()

### Community 25 - "Community 25"

Cohesion: 0.25
Nodes (4): AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr, AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL, test_uc001_existing_user_google_one_tap_returns_existing_data(), test_uc001_new_user_google_one_tap_creates_user_and_personal_org()

### Community 26 - "Community 26"

Cohesion: 0.25
Nodes (5): UC-048 Main Flow: App queries GET /api/v1/fuel with pagination (page=1, limit=2), setup_db(), test_fleet_aggregate_average_efficiency(), test_fuel_efficiency_trends_monthly_aggregation(), test_get_fuel_logs_paginated()

### Community 27 - "Community 27"
_Unable to determine domain due to missing code entities._
Cohesion: 0.25
Nodes (0): 

### Community 28 - "Community 28"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 29 - "Community 29"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 30 - "Community 30"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 31 - "Community 31"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 32 - "Community 32"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 33 - "Community 33"
_Unable to determine domain due to missing code entities._
Cohesion: 0.29
Nodes (0): 

### Community 34 - "Community 34"
_Unable to determine domain due to missing code entities._
Cohesion: 0.33
Nodes (0): 

### Community 35 - "Community 35"
_Unable to determine domain due to missing code entities._
Cohesion: 0.33
Nodes (0): 

### Community 36 - "Community 36"
_Unable to determine domain due to missing code entities._
Cohesion: 0.33
Nodes (0): 

### Community 37 - "Community 37"
_Unable to determine domain due to missing code entities._
Cohesion: 0.33
Nodes (0): 

### Community 38 - "Community 38"

Cohesion: 0.4
Nodes (4): AuthSession, OrganizationModel, RefreshTokenTokens, UserModel

### Community 39 - "Community 39"

Cohesion: 0.5
Nodes (3): FuelLogModel, FuelMonthlyTrendModel, FuelTrendsModel

### Community 40 - "Community 40"

Cohesion: 0.5
Nodes (3): MileageSummaryModel, TripModel, TripSummaryModel

### Community 41 - "Community 41"

Cohesion: 0.5
Nodes (3): VehicleDetailModel, VehicleModel, VehicleTypeModel

### Community 42 - "Community 42"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (0): 

### Community 43 - "Community 43"

Cohesion: 0.67
Nodes (2): UC-063: Upload receipt image file., upload_receipt()

### Community 44 - "Community 44"

Cohesion: 0.67
Nodes (2): BaseSettings, Settings

### Community 45 - "Community 45"
_Automatically registers Flutter plugins with the platform activity so Dart code can access native plugin functionalities._
Cohesion: 0.67
Nodes (1): GeneratedPluginRegistrant

### Community 46 - "Community 46"

Cohesion: 0.67
Nodes (2): CostBreakdownItemModel, CostBreakdownModel

### Community 47 - "Community 47"

Cohesion: 0.67
Nodes (2): ExpenseModel, ExpenseSummaryModel

### Community 48 - "Community 48"

Cohesion: 0.67
Nodes (2): MaintenanceScheduleModel, ServiceRecordModel

### Community 49 - "Community 49"

Cohesion: 0.67
Nodes (2): NotificationModel, NotificationPaginatedModel

### Community 50 - "Community 50"
_Unable to determine domain due to missing code entities._
Cohesion: 0.67
Nodes (0): 

### Community 51 - "Community 51"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 52 - "Community 52"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 53 - "Community 53"
_Handles the primary screen and user interactions at app launch._
Cohesion: 1.0
Nodes (1): MainActivity

### Community 54 - "Community 54"

Cohesion: 1.0
Nodes (1): DashboardSummaryModel

### Community 55 - "Community 55"

Cohesion: 1.0
Nodes (1): OrganizationInvitationModel

### Community 56 - "Community 56"

Cohesion: 1.0
Nodes (1): OrganizationModel

### Community 57 - "Community 57"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 58 - "Community 58"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 59 - "Community 59"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

### Community 60 - "Community 60"
_Unable to determine domain due to missing code entities._
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **452 isolated node(s):** `UC-001 & UC-002: Register or Log In with OAuth Providers (Google, Facebook)`, `UC-118: Trigger Database Migration & Master Seeding Infrastructure.     Pre-pop`, `UC-063: Upload receipt image file.`, `Config`, `Config` (+447 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 51`** (2 nodes): `session.py`, `get_db()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (2 nodes): `get_cost_breakdown()`, `dashboard_service.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (2 nodes): `MainActivity.kt`, `MainActivity`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (2 nodes): `dashboard_model.dart`, `DashboardSummaryModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (2 nodes): `organization_invitation_model.dart`, `OrganizationInvitationModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 56`** (2 nodes): `organization_model.dart`, `OrganizationModel`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 59`** (1 nodes): `run_and_report.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 60`** (1 nodes): `run_tests.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.