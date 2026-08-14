# ServiceRecord

> God node · 40 connections · [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\maintenance.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/maintenance.py#L28)

## Call Trace Diagram

```mermaid
sequenceDiagram
    participant P0 as ServiceRecord
    participant P1 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P2 as Organization
    participant P3 as AuthService
    participant P4 as UC-011: Account Deletion (GDPR Right to be Forgotten)         Soft-deletes user
    participant P5 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P6 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P7 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P8 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P9 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P10 as UC-007: Fetch current user profile details.
    participant P11 as UC-007: Update current user profile (full name, phone, city, job role, avatar).
    participant P12 as UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio
    participant P13 as UC-007: Multi-tenant authorization boundary verification endpoint.
    participant P14 as UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re
    participant P15 as UC-013: Active Session Management & Device Tracking     Returns list of active
    participant P16 as UC-013: Revoke Specific Device Session     Revokes the specified refresh token
    participant P17 as UC-013 Alternate Flow A1: Revoke All Other Sessions     Revokes all active sess
    participant P18 as UC-014: Provision commercial or custom organization.
    participant P19 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P20 as Retrieve organizations list.
    participant P21 as UC-015: Switch active organization context for user.
    participant P22 as UC-015: Get active organization for user.
    participant P23 as Retrieve organization details by ID.
    participant P24 as UC-016: Invite Team Member to Organization.     Generates a secure 64-character
    participant P25 as UC-016: List pending organization invitations.
    participant P26 as UC-053: Get Trip Summary & Tax Deduction Metrics.
    participant P27 as UC-052: Start GPS Trip Tracking session.
    participant P28 as UC-052: Stop active GPS Trip Tracking session and calculate distance.
    participant P29 as UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    participant P30 as UC-053: View Trip History.
    participant P31 as UC-054: Edit Trip Entry & Classification.
    participant P32 as UC-055: Soft Delete Trip Entry.
    participant P33 as UC-056: Quick-Log Trip from Dashboard.
    participant P34 as UC-057: View Distance & Mileage Summary Analytics.
    participant P35 as register_or_login()
    participant P36 as UC-058: Log General Fleet Expense.
    participant P37 as UC-059: Expense Category & Cost Summary Metrics.
    participant P38 as UC-059: View Expense History.
    participant P39 as UC-060: Edit Expense Entry.
    participant P40 as UC-061: Soft Delete Expense Entry.
    participant P41 as UC-062: Quick-Log Expense from Dashboard.
    participant P42 as UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    participant P43 as UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    participant P44 as UC-050 (A1): Manager clears fuel anomaly flag.
    participant P45 as UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    participant P46 as UC-046: Log Fuel Fill-Up Entry.     Automatically updates vehicle current odome
    participant P47 as UC-047 / UC-048: View Fuel Log History with optional pagination.
    participant P48 as UC-051: Edit Fuel Log Entry.     Updates entry, syncs linked ExpenseLog, and re
    participant P49 as UC-051: Soft Delete Fuel Log Entry.     Soft-deletes entry and linked ExpenseLo
    participant P50 as Test 1: Verify all 7 core data models instantiate clean database tables.
    participant P51 as Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    participant P52 as Test 3: Verify POST /api/v1/admin/seed endpoint.
    participant P53 as complete_profile()
    participant P54 as login()
    participant P55 as test_uc118_schema_instantiation()
    participant P56 as UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    participant P57 as UC-064: Requests for Org 2 return only Org 2's metrics.
    participant P58 as UC-064: Empty organization returns 0 stats so client can render onboarding card.
    participant P59 as UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin
    participant P60 as refresh_token()
    participant P61 as setup_db()
    participant P62 as dashboard_setup()
    participant P63 as AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked
    participant P64 as AC 2: GIVEN a user who is the sole owner of an active non-personal organization
    participant P65 as AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac
    participant P66 as AC 1: System creates immutable AuditLog entry upon user registration.
    participant P67 as AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat
    participant P68 as A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    participant P69 as AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS
    participant P70 as AC 4: System records USER_LOGOUT audit entry upon session termination.
    participant P71 as Edge Case: Audit log DB write exception is handled safely and does not block use
    participant P72 as UC-046: Test successful fuel log creation & vehicle current odometer update.
    participant P73 as UC-046 Acceptance Criterion: WHEN a fuel log entry is saved     THE SYSTEM SHAL
    participant P74 as UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API re
    participant P75 as UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    participant P76 as UC-047: Test retrieving fuel log history via GET /api/v1/fuel.     Should retur
    participant P77 as UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are create
    participant P78 as UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficienc
    participant P79 as UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    participant P80 as UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates e
    participant P81 as UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and
    participant P82 as UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    participant P83 as UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule template
    participant P84 as UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets sched
    participant P85 as UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422.
    participant P86 as UC-034: Tenant cross-access rejected.
    participant P87 as UC-036: POST /api/v1/maintenance logs service record and updates linked schedule
    participant P88 as UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_
    participant P89 as UC-036: Omitting maintenance_schedule_id matches schedule item by task name subs
    participant P90 as UC-036: Rejects negative cost, negative odometer, whitespace service_type, or in
    participant P91 as UC-036: Enforces X-Organization-ID header presence and cross-tenant access prote
    participant P92 as UC-037: GET /api/v1/maintenance/records retrieves service records sorted by serv
    participant P93 as UC-037: Pagination limit and offset parameters operate correctly.
    participant P94 as UC-037: Returns 404 when vehicle_id does not exist in active organization.
    participant P95 as UC-037: Header requirements and cross-tenant boundaries are strictly enforced.
    participant P96 as Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    participant P97 as Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organizat
    participant P98 as Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    participant P99 as Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP
    participant P100 as Test 5: Verify custom make/model is dynamically indexed into VehicleType catalog
    participant P101 as ensure_organization()
    participant P102 as test_uc011_sole_owner_blocking()
    participant P103 as UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a
    participant P104 as UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh
    participant P105 as UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default
    participant P106 as UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and l
    participant P107 as UC-035: Rejects zero/negative intervals or empty task names with 422.
    participant P108 as UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalcul
    participant P109 as UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task.
    participant P110 as UC-035: Header validation and tenant cross-access isolation.
    participant P111 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids a
    participant P112 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_id
    participant P113 as UC-038: Returns 404 when vehicle_id is not found in active organization.
    participant P114 as UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle.
    participant P115 as UC-038: Headers and cross-tenant boundaries are strictly enforced.
    participant P116 as UC-016: Owner can create organization invitation, generating a secure 64-char to
    participant P117 as UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entit
    participant P118 as UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Enti
    participant P119 as UC-016: Re-inviting same email updates existing invitation token and TTL without
    participant P120 as UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden
    participant P121 as UC-016: Owner can list all pending invitations for organization.
    participant P122 as UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found.
    participant P123 as Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle
    participant P124 as Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 For
    participant P125 as Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    participant P126 as Test 4: Verify manual odometer update with discrepancy > 500 km generates an Aud
    participant P127 as Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessabl
    participant P128 as setup_db()
    participant P129 as test_setup()
    participant P130 as test_setup()
    participant P131 as test_setup()
    participant P132 as AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr
    participant P133 as AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    participant P134 as AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store \"facebook\" insid
    participant P135 as Alternate Flow A1: Account Linking     If email matches existing account with d
    participant P136 as Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ
    participant P137 as AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT
    participant P138 as Alternate Flow A1: Account Linking     If user signed up via Google, submitting
    participant P139 as Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu
    participant P140 as Edge Case: Missing email or missing password for email auth provider returns HTT
    participant P141 as AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200
    participant P142 as Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    participant P143 as Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    participant P144 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P145 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P146 as AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2
    participant P147 as AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP
    participant P148 as AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    participant P149 as AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    participant P150 as Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    participant P151 as Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    participant P152 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P153 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P154 as AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u
    participant P155 as AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P
    participant P156 as AC 3: GIVEN a profile update request with invalid display name length (< 2 chars
    participant P157 as AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro
    participant P158 as UC-014: POST /api/v1/organizations creates commercial organization and sets owne
    participant P159 as UC-014: POST /api/v1/organizations/personal auto-creates personal organization f
    participant P160 as UC-014: Blank or whitespace organization name rejected with HTTP 422.
    participant P161 as UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization
    participant P162 as UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found.
    participant P163 as UC-015: POST /api/v1/organizations/switch switches active context for valid user
    participant P164 as UC-015: Switch attempt to organization owned by another user yields HTTP 403 For
    participant P165 as UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found.
    participant P166 as UC-015: GET /api/v1/organizations/active returns current primary organization fo
    participant P167 as UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N
    participant P168 as Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in
    participant P169 as Test 2: Verify search query matches license plate, make, or model.
    participant P170 as Test 3: Verify filtering by province (e.g. Sindh).
    participant P171 as Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metada
    participant P172 as Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    participant P173 as Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    participant P174 as Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status
    participant P175 as create_organization()
    participant P176 as auto_create_personal_organization()
    participant P177 as setup_db()
    participant P178 as setup_db()
    participant P179 as setup_db()
    participant P180 as test_setup()
    participant P181 as test_setup()
    participant P182 as test_setup()
    participant P183 as test_setup()
    participant P184 as test_setup()
    participant P185 as test_setup()
    participant P186 as setup_db()
    participant P187 as test_setup()
    participant P188 as test_setup()
    participant P189 as setup_db()
    participant P190 as setup_db()
    participant P191 as setup_db()
    participant P192 as setup_db()
    participant P193 as setup_db()
    participant P194 as setup_db()
    participant P195 as sample_fleet()
    participant P196 as test_setup()
    participant P197 as test_setup()
    participant P198 as sample_org()
    participant P199 as User
    participant P200 as Vehicle
    participant P201 as MaintenanceSchedule
    participant P202 as AuditLog
    participant P203 as VehicleType
    participant P204 as Driver
    participant P205 as VehicleResponse
    participant P206 as VehicleDetailResponse
    participant P207 as VehicleCreateRequest
    participant P208 as VehicleTypeResponse
    participant P209 as VehicleStatusUpdateRequest
    participant P210 as VehicleUpdateRequest
    participant P211 as UC-035: Create custom maintenance schedule task item for a vehicle.
    participant P212 as UC-035: Update schedule parameters (intervals, task name, active status) and rec
    participant P213 as UC-035: Soft-delete schedule item.
    participant P214 as UC-037: Retrieve chronological service records for a vehicle within the active o
    participant P215 as UC-038: Bulk accept/acknowledge default maintenance schedules for a vehicle.
    participant P216 as UC-064: Get high-level KPI dashboard metrics summary for active organization.
    participant P217 as UC-065: Cost Breakdown Charts per Vehicle (Fuel vs Maintenance vs Expenses).
    participant P218 as log_maintenance_task()
    P0->>+ P1: uses
    P1-->>- P0: return
    P1->>+ P2: uses
    P2-->>- P1: return
    P2->>+ P3: uses
    P3-->>- P2: return
    P2->>+ P4: uses
    P4-->>- P2: return
    P2->>+ P1: uses
    P1-->>- P2: return
    P2->>+ P5: uses
    P5-->>- P2: return
    P2->>+ P6: uses
    P6-->>- P2: return
    P2->>+ P7: uses
    P7-->>- P2: return
    P2->>+ P8: uses
    P8-->>- P2: return
    P2->>+ P9: uses
    P9-->>- P2: return
    P2->>+ P10: uses
    P10-->>- P2: return
    P2->>+ P11: uses
    P11-->>- P2: return
    P2->>+ P12: uses
    P12-->>- P2: return
    P2->>+ P13: uses
    P13-->>- P2: return
    P2->>+ P14: uses
    P14-->>- P2: return
    P2->>+ P15: uses
    P15-->>- P2: return
    P2->>+ P16: uses
    P16-->>- P2: return
    P2->>+ P17: uses
    P17-->>- P2: return
    P2->>+ P18: uses
    P18-->>- P2: return
    P2->>+ P19: uses
    P19-->>- P2: return
    P2->>+ P20: uses
    P20-->>- P2: return
    P2->>+ P21: uses
    P21-->>- P2: return
    P2->>+ P22: uses
    P22-->>- P2: return
    P2->>+ P23: uses
    P23-->>- P2: return
    P2->>+ P24: uses
    P24-->>- P2: return
    P2->>+ P25: uses
    P25-->>- P2: return
    P2->>+ P26: uses
    P26-->>- P2: return
    P2->>+ P27: uses
    P27-->>- P2: return
    P2->>+ P28: uses
    P28-->>- P2: return
    P2->>+ P29: uses
    P29-->>- P2: return
    P2->>+ P30: uses
    P30-->>- P2: return
    P2->>+ P31: uses
    P31-->>- P2: return
    P2->>+ P32: uses
    P32-->>- P2: return
    P2->>+ P33: uses
    P33-->>- P2: return
    P2->>+ P34: uses
    P34-->>- P2: return
    P2->>+ P35: calls
    P35-->>- P2: return
    P2->>+ P36: uses
    P36-->>- P2: return
    P2->>+ P37: uses
    P37-->>- P2: return
    P2->>+ P38: uses
    P38-->>- P2: return
    P2->>+ P39: uses
    P39-->>- P2: return
    P2->>+ P40: uses
    P40-->>- P2: return
    P2->>+ P41: uses
    P41-->>- P2: return
    P2->>+ P42: uses
    P42-->>- P2: return
    P2->>+ P43: uses
    P43-->>- P2: return
    P2->>+ P44: uses
    P44-->>- P2: return
    P2->>+ P45: uses
    P45-->>- P2: return
    P2->>+ P46: uses
    P46-->>- P2: return
    P2->>+ P47: uses
    P47-->>- P2: return
    P2->>+ P48: uses
    P48-->>- P2: return
    P2->>+ P49: uses
    P49-->>- P2: return
    P2->>+ P50: uses
    P50-->>- P2: return
    P2->>+ P51: uses
    P51-->>- P2: return
    P2->>+ P52: uses
    P52-->>- P2: return
    P2->>+ P53: calls
    P53-->>- P2: return
    P2->>+ P54: calls
    P54-->>- P2: return
    P2->>+ P55: calls
    P55-->>- P2: return
    P2->>+ P56: uses
    P56-->>- P2: return
    P2->>+ P57: uses
    P57-->>- P2: return
    P2->>+ P58: uses
    P58-->>- P2: return
    P2->>+ P59: uses
    P59-->>- P2: return
    P2->>+ P60: calls
    P60-->>- P2: return
    P2->>+ P61: calls
    P61-->>- P2: return
    P2->>+ P62: calls
    P62-->>- P2: return
    P2->>+ P63: uses
    P63-->>- P2: return
    P2->>+ P64: uses
    P64-->>- P2: return
    P2->>+ P65: uses
    P65-->>- P2: return
    P2->>+ P66: uses
    P66-->>- P2: return
    P2->>+ P67: uses
    P67-->>- P2: return
    P2->>+ P68: uses
    P68-->>- P2: return
    P2->>+ P69: uses
    P69-->>- P2: return
    P2->>+ P70: uses
    P70-->>- P2: return
    P2->>+ P71: uses
    P71-->>- P2: return
    P2->>+ P72: uses
    P72-->>- P2: return
    P2->>+ P73: uses
    P73-->>- P2: return
    P2->>+ P74: uses
    P74-->>- P2: return
    P2->>+ P75: uses
    P75-->>- P2: return
    P2->>+ P76: uses
    P76-->>- P2: return
    P2->>+ P77: uses
    P77-->>- P2: return
    P2->>+ P78: uses
    P78-->>- P2: return
    P2->>+ P79: uses
    P79-->>- P2: return
    P2->>+ P80: uses
    P80-->>- P2: return
    P2->>+ P81: uses
    P81-->>- P2: return
    P2->>+ P82: uses
    P82-->>- P2: return
    P2->>+ P83: uses
    P83-->>- P2: return
    P2->>+ P84: uses
    P84-->>- P2: return
    P2->>+ P85: uses
    P85-->>- P2: return
    P2->>+ P86: uses
    P86-->>- P2: return
    P2->>+ P87: uses
    P87-->>- P2: return
    P2->>+ P88: uses
    P88-->>- P2: return
    P2->>+ P89: uses
    P89-->>- P2: return
    P2->>+ P90: uses
    P90-->>- P2: return
    P2->>+ P91: uses
    P91-->>- P2: return
    P2->>+ P92: uses
    P92-->>- P2: return
    P2->>+ P93: uses
    P93-->>- P2: return
    P2->>+ P94: uses
    P94-->>- P2: return
    P2->>+ P95: uses
    P95-->>- P2: return
    P2->>+ P96: uses
    P96-->>- P2: return
    P2->>+ P97: uses
    P97-->>- P2: return
    P2->>+ P98: uses
    P98-->>- P2: return
    P2->>+ P99: uses
    P99-->>- P2: return
    P2->>+ P100: uses
    P100-->>- P2: return
    P2->>+ P101: calls
    P101-->>- P2: return
    P2->>+ P102: calls
    P102-->>- P2: return
    P2->>+ P103: uses
    P103-->>- P2: return
    P2->>+ P104: uses
    P104-->>- P2: return
    P2->>+ P105: uses
    P105-->>- P2: return
    P2->>+ P106: uses
    P106-->>- P2: return
    P2->>+ P107: uses
    P107-->>- P2: return
    P2->>+ P108: uses
    P108-->>- P2: return
    P2->>+ P109: uses
    P109-->>- P2: return
    P2->>+ P110: uses
    P110-->>- P2: return
    P2->>+ P111: uses
    P111-->>- P2: return
    P2->>+ P112: uses
    P112-->>- P2: return
    P2->>+ P113: uses
    P113-->>- P2: return
    P2->>+ P114: uses
    P114-->>- P2: return
    P2->>+ P115: uses
    P115-->>- P2: return
    P2->>+ P116: uses
    P116-->>- P2: return
    P2->>+ P117: uses
    P117-->>- P2: return
    P2->>+ P118: uses
    P118-->>- P2: return
    P2->>+ P119: uses
    P119-->>- P2: return
    P2->>+ P120: uses
    P120-->>- P2: return
    P2->>+ P121: uses
    P121-->>- P2: return
    P2->>+ P122: uses
    P122-->>- P2: return
    P2->>+ P123: uses
    P123-->>- P2: return
    P2->>+ P124: uses
    P124-->>- P2: return
    P2->>+ P125: uses
    P125-->>- P2: return
    P2->>+ P126: uses
    P126-->>- P2: return
    P2->>+ P127: uses
    P127-->>- P2: return
    P2->>+ P128: calls
    P128-->>- P2: return
    P2->>+ P129: calls
    P129-->>- P2: return
    P2->>+ P130: calls
    P130-->>- P2: return
    P2->>+ P131: calls
    P131-->>- P2: return
    P2->>+ P132: uses
    P132-->>- P2: return
    P2->>+ P133: uses
    P133-->>- P2: return
    P2->>+ P134: uses
    P134-->>- P2: return
    P2->>+ P135: uses
    P135-->>- P2: return
    P2->>+ P136: uses
    P136-->>- P2: return
    P2->>+ P137: uses
    P137-->>- P2: return
    P2->>+ P138: uses
    P138-->>- P2: return
    P2->>+ P139: uses
    P139-->>- P2: return
    P2->>+ P140: uses
    P140-->>- P2: return
    P2->>+ P141: uses
    P141-->>- P2: return
    P2->>+ P142: uses
    P142-->>- P2: return
    P2->>+ P143: uses
    P143-->>- P2: return
    P2->>+ P144: uses
    P144-->>- P2: return
    P2->>+ P145: uses
    P145-->>- P2: return
    P2->>+ P146: uses
    P146-->>- P2: return
    P2->>+ P147: uses
    P147-->>- P2: return
    P2->>+ P148: uses
    P148-->>- P2: return
    P2->>+ P149: uses
    P149-->>- P2: return
    P2->>+ P150: uses
    P150-->>- P2: return
    P2->>+ P151: uses
    P151-->>- P2: return
    P2->>+ P152: uses
    P152-->>- P2: return
    P2->>+ P153: uses
    P153-->>- P2: return
    P2->>+ P154: uses
    P154-->>- P2: return
    P2->>+ P155: uses
    P155-->>- P2: return
    P2->>+ P156: uses
    P156-->>- P2: return
    P2->>+ P157: uses
    P157-->>- P2: return
    P2->>+ P158: uses
    P158-->>- P2: return
    P2->>+ P159: uses
    P159-->>- P2: return
    P2->>+ P160: uses
    P160-->>- P2: return
    P2->>+ P161: uses
    P161-->>- P2: return
    P2->>+ P162: uses
    P162-->>- P2: return
    P2->>+ P163: uses
    P163-->>- P2: return
    P2->>+ P164: uses
    P164-->>- P2: return
    P2->>+ P165: uses
    P165-->>- P2: return
    P2->>+ P166: uses
    P166-->>- P2: return
    P2->>+ P167: uses
    P167-->>- P2: return
    P2->>+ P168: uses
    P168-->>- P2: return
    P2->>+ P169: uses
    P169-->>- P2: return
    P2->>+ P170: uses
    P170-->>- P2: return
    P2->>+ P171: uses
    P171-->>- P2: return
    P2->>+ P172: uses
    P172-->>- P2: return
    P2->>+ P173: uses
    P173-->>- P2: return
    P2->>+ P174: uses
    P174-->>- P2: return
    P2->>+ P175: calls
    P175-->>- P2: return
    P2->>+ P176: calls
    P176-->>- P2: return
    P2->>+ P177: calls
    P177-->>- P2: return
    P2->>+ P178: calls
    P178-->>- P2: return
    P2->>+ P179: calls
    P179-->>- P2: return
    P2->>+ P180: calls
    P180-->>- P2: return
    P2->>+ P181: calls
    P181-->>- P2: return
    P2->>+ P182: calls
    P182-->>- P2: return
    P2->>+ P183: calls
    P183-->>- P2: return
    P2->>+ P184: calls
    P184-->>- P2: return
    P2->>+ P185: calls
    P185-->>- P2: return
    P2->>+ P186: calls
    P186-->>- P2: return
    P2->>+ P187: calls
    P187-->>- P2: return
    P2->>+ P188: calls
    P188-->>- P2: return
    P2->>+ P189: calls
    P189-->>- P2: return
    P2->>+ P190: calls
    P190-->>- P2: return
    P2->>+ P191: calls
    P191-->>- P2: return
    P2->>+ P192: calls
    P192-->>- P2: return
    P2->>+ P193: calls
    P193-->>- P2: return
    P2->>+ P194: calls
    P194-->>- P2: return
    P2->>+ P195: calls
    P195-->>- P2: return
    P2->>+ P196: calls
    P196-->>- P2: return
    P2->>+ P197: calls
    P197-->>- P2: return
    P2->>+ P198: calls
    P198-->>- P2: return
    P1->>+ P199: uses
    P199-->>- P1: return
    P1->>+ P200: uses
    P200-->>- P1: return
    P1->>+ P201: uses
    P201-->>- P1: return
    P1->>+ P0: uses
    P0-->>- P1: return
    P1->>+ P202: uses
    P202-->>- P1: return
    P1->>+ P203: uses
    P203-->>- P1: return
    P1->>+ P204: uses
    P204-->>- P1: return
    P1->>+ P205: uses
    P205-->>- P1: return
    P1->>+ P206: uses
    P206-->>- P1: return
    P1->>+ P207: uses
    P207-->>- P1: return
    P1->>+ P208: uses
    P208-->>- P1: return
    P1->>+ P209: uses
    P209-->>- P1: return
    P1->>+ P210: uses
    P210-->>- P1: return
    P0->>+ P5: uses
    P5-->>- P0: return
    P0->>+ P6: uses
    P6-->>- P0: return
    P0->>+ P7: uses
    P7-->>- P0: return
    P0->>+ P8: uses
    P8-->>- P0: return
    P0->>+ P9: uses
    P9-->>- P0: return
    P0->>+ P211: uses
    P211-->>- P0: return
    P0->>+ P212: uses
    P212-->>- P0: return
    P0->>+ P213: uses
    P213-->>- P0: return
    P0->>+ P214: uses
    P214-->>- P0: return
    P0->>+ P215: uses
    P215-->>- P0: return
    P0->>+ P50: uses
    P50-->>- P0: return
    P0->>+ P51: uses
    P51-->>- P0: return
    P0->>+ P52: uses
    P52-->>- P0: return
    P0->>+ P216: uses
    P216-->>- P0: return
    P0->>+ P217: uses
    P217-->>- P0: return
    P0->>+ P55: calls
    P55-->>- P0: return
    P0->>+ P56: uses
    P56-->>- P0: return
    P0->>+ P57: uses
    P57-->>- P0: return
    P0->>+ P58: uses
    P58-->>- P0: return
    P0->>+ P59: uses
    P59-->>- P0: return
    P0->>+ P61: calls
    P61-->>- P0: return
    P0->>+ P62: calls
    P62-->>- P0: return
    P0->>+ P83: uses
    P83-->>- P0: return
    P0->>+ P84: uses
    P84-->>- P0: return
    P0->>+ P85: uses
    P85-->>- P0: return
    P0->>+ P86: uses
    P86-->>- P0: return
    P0->>+ P87: uses
    P87-->>- P0: return
    P0->>+ P88: uses
    P88-->>- P0: return
    P0->>+ P89: uses
    P89-->>- P0: return
    P0->>+ P90: uses
    P90-->>- P0: return
    P0->>+ P91: uses
    P91-->>- P0: return
    P0->>+ P92: uses
    P92-->>- P0: return
    P0->>+ P93: uses
    P93-->>- P0: return
    P0->>+ P94: uses
    P94-->>- P0: return
    P0->>+ P95: uses
    P95-->>- P0: return
    P0->>+ P130: calls
    P130-->>- P0: return
    P0->>+ P218: calls
    P218-->>- P0: return
```

## Connections by Relation

### calls
- [[test_uc118_schema_instantiation()]] `INFERRED`
- [[setup_db()]] `INFERRED`
- [[dashboard_setup()]] `INFERRED`
- [[test_setup()]] `INFERRED`
- [[log_maintenance_task()]] `INFERRED`

### contains
- [[maintenance.py]] `EXTRACTED`

### inherits
- [[Base]] `EXTRACTED`

### uses
- [[UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.]] `INFERRED`
- [[UC-024: Register New Vehicle with organization quota validation & duplicate VIN]] `INFERRED`
- [[UC-025: List Organization Vehicles directory with status, search, fuel type, and]] `INFERRED`
- [[UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur]] `INFERRED`
- [[UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).]] `INFERRED`
- [[UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow]] `INFERRED`
- [[UC-035: Create custom maintenance schedule task item for a vehicle.]] `INFERRED`
- [[UC-035: Update schedule parameters (intervals, task name, active status) and rec]] `INFERRED`
- [[UC-035: Soft-delete schedule item.]] `INFERRED`
- [[UC-037: Retrieve chronological service records for a vehicle within the active o]] `INFERRED`
- [[UC-038: Bulk accept/acknowledge default maintenance schedules for a vehicle.]] `INFERRED`
- [[Test 1: Verify all 7 core data models instantiate clean database tables.]] `INFERRED`
- [[Test 2: Verify database seeding populates master vehicle catalogue idempotently.]] `INFERRED`
- [[Test 3: Verify POST /api/v1/admin/seed endpoint.]] `INFERRED`
- [[UC-064: Get high-level KPI dashboard metrics summary for active organization.]] `INFERRED`
- [[UC-065: Cost Breakdown Charts per Vehicle (Fuel vs Maintenance vs Expenses).]] `INFERRED`
- [[UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,]] `INFERRED`
- [[UC-064: Requests for Org 2 return only Org 2's metrics.]] `INFERRED`
- [[UC-064: Empty organization returns 0 stats so client can render onboarding card.]] `INFERRED`
- [[UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*