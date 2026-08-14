# AuthService

> God node · 35 connections · [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\services\auth_service.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/services/auth_service.py#L57)

## Call Trace Diagram

```mermaid
sequenceDiagram
    participant P0 as AuthService
    participant P1 as Organization
    participant P2 as UC-014: Provision commercial or custom organization.
    participant P3 as User
    participant P4 as Vehicle
    participant P5 as MaintenanceSchedule
    participant P6 as AuditLog
    participant P7 as ServiceRecord
    participant P8 as OrganizationInvitation
    participant P9 as Driver
    participant P10 as UserOrganization
    participant P11 as FuelLog
    participant P12 as ExpenseLog
    participant P13 as OrganizationInvitationResponse
    participant P14 as SwitchOrganizationResponse
    participant P15 as OrganizationCreate
    participant P16 as PersonalOrganizationCreate
    participant P17 as OrganizationResponse
    participant P18 as SwitchOrganizationRequest
    participant P19 as OrganizationInvitationCreate
    participant P20 as Trip
    participant P21 as OrganizationUpdate
    participant P22 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P23 as Retrieve organizations list.
    participant P24 as UC-015: Switch active organization context for user.
    participant P25 as UC-015: Get active organization for user.
    participant P26 as Retrieve organization details by ID.
    participant P27 as UC-017: Edit Organization Profile Details.     Enforces ISO 4217 currency valida
    participant P28 as UC-018: Invite Driver / Manager via Email or Phone.     Generates a secure 64-ch
    participant P29 as UC-018: List pending organization invitations.
    participant P30 as UC-021: Remove Member from Organization.     Prevents owner removal. Unassigns u
    participant P31 as UC-022: Cancel Pending Member Invitation.
    participant P32 as UC-023: Soft Delete Organization & Child Entities.     Rejects personal org dele
    participant P33 as UC-011: Account Deletion (GDPR Right to be Forgotten)         Soft-deletes user
    participant P34 as UC-024: Typeahead autocomplete lookup against seeded Vehicle Master Catalogue.
    participant P35 as UC-024: Register New Vehicle with organization quota validation & duplicate VIN
    participant P36 as UC-025: List Organization Vehicles directory with status, search, fuel type, and
    participant P37 as UC-026: View Vehicle Detailed Overview.     Enforces tenant isolation and retur
    participant P38 as UC-026: Update Vehicle Status (ACTIVE, MAINTENANCE, INACTIVE).
    participant P39 as UC-027: Update Vehicle Metadata & Specifications.     Validates organization ow
    participant P40 as UC-007: Fetch current user profile details.
    participant P41 as UC-007: Update current user profile (full name, phone, city, job role, avatar).
    participant P42 as UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio
    participant P43 as UC-007: Multi-tenant authorization boundary verification endpoint.
    participant P44 as UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re
    participant P45 as UC-013: Active Session Management & Device Tracking     Returns list of active
    participant P46 as UC-013: Revoke Specific Device Session     Revokes the specified refresh token
    participant P47 as UC-013 Alternate Flow A1: Revoke All Other Sessions     Revokes all active sess
    participant P48 as UC-053: Get Trip Summary & Tax Deduction Metrics.
    participant P49 as UC-052: Start GPS Trip Tracking session.
    participant P50 as UC-052: Stop active GPS Trip Tracking session and calculate distance.
    participant P51 as UC-052 / UC-053: Create trip entry (Manual or completed GPS trip).
    participant P52 as UC-053: View Trip History.
    participant P53 as UC-054: Edit Trip Entry & Classification.
    participant P54 as UC-055: Soft Delete Trip Entry.
    participant P55 as UC-056: Quick-Log Trip from Dashboard.
    participant P56 as UC-057: View Distance & Mileage Summary Analytics.
    participant P57 as register_or_login()
    participant P58 as UC-014: Provision commercial or custom organization.
    participant P59 as UC-014: Auto-provision personal organization for a user during registration or s
    participant P60 as Retrieve organizations list.
    participant P61 as UC-015: Switch active organization context for user.
    participant P62 as UC-015: Get active organization for user.
    participant P63 as Retrieve organization details by ID.
    participant P64 as UC-016: Invite Team Member to Organization.     Generates a secure 64-character
    participant P65 as UC-016: List pending organization invitations.
    participant P66 as UC-019: Inspect / validate organization invitation token details.     Returns HT
    participant P67 as UC-019: Accept Organization Invitation for existing authenticated user.
    participant P68 as UC-020: Redeem Org Invitation Code for new user during signup/onboard.
    participant P69 as UC-058: Log General Fleet Expense.
    participant P70 as UC-059: Expense Category & Cost Summary Metrics.
    participant P71 as UC-059: View Expense History.
    participant P72 as UC-060: Edit Expense Entry.
    participant P73 as UC-061: Soft Delete Expense Entry.
    participant P74 as UC-062: Quick-Log Expense from Dashboard.
    participant P75 as UC-048: View Fuel Efficiency Trends & Aggregate Metrics.
    participant P76 as UC-050: Detect Fuel Anomaly & Theft Alerts - Fetch anomaly logs.
    participant P77 as UC-050 (A1): Manager clears fuel anomaly flag.
    participant P78 as UC-049: Fuel Receipt OCR Auto-Fill (Pro).
    participant P79 as UC-046: Log Fuel Fill-Up Entry.     Automatically updates vehicle current odome
    participant P80 as UC-047 / UC-048: View Fuel Log History with optional pagination.
    participant P81 as UC-051: Edit Fuel Log Entry.     Updates entry, syncs linked ExpenseLog, and re
    participant P82 as UC-051: Soft Delete Fuel Log Entry.     Soft-deletes entry and linked ExpenseLo
    participant P83 as Test 1: Verify all 7 core data models instantiate clean database tables.
    participant P84 as Test 2: Verify database seeding populates master vehicle catalogue idempotently.
    participant P85 as Test 3: Verify POST /api/v1/admin/seed endpoint.
    participant P86 as complete_profile()
    participant P87 as login()
    participant P88 as test_uc118_schema_instantiation()
    participant P89 as UC-064: GET /api/v1/dashboard/summary calculates total_vehicles, total_drivers,
    participant P90 as UC-064: Requests for Org 2 return only Org 2's metrics.
    participant P91 as UC-064: Empty organization returns 0 stats so client can render onboarding card.
    participant P92 as UC-064: GET /api/v1/dashboard/summary returns 400 if X-Organization-ID is missin
    participant P93 as refresh_token()
    participant P94 as setup_db()
    participant P95 as dashboard_setup()
    participant P96 as AC 1: GIVEN an authenticated user     WHEN DELETE /api/v1/users/me is invoked
    participant P97 as AC 2: GIVEN a user who is the sole owner of an active non-personal organization
    participant P98 as AC 3: GIVEN a soft-deleted user account     WHEN attempting to authenticate, ac
    participant P99 as AC 1: System creates immutable AuditLog entry upon user registration.
    participant P100 as AC 2: System records USER_LOGIN_SUCCESS audit entry with IP & User-Agent metadat
    participant P101 as A1: Unauthenticated attempt records USER_LOGIN_FAILURE with actor_id = None.
    participant P102 as AC 3: System records USER_PASSWORD_RESET_REQUEST and USER_PASSWORD_RESET_SUCCESS
    participant P103 as AC 4: System records USER_LOGOUT audit entry upon session termination.
    participant P104 as Edge Case: Audit log DB write exception is handled safely and does not block use
    participant P105 as UC-046: Test successful fuel log creation & vehicle current odometer update.
    participant P106 as UC-046 Acceptance Criterion: WHEN a fuel log entry is saved     THE SYSTEM SHAL
    participant P107 as UC-046 Edge Case: Odometer entry lower than vehicle's current odometer -> API re
    participant P108 as UC-046 & UC-047: Verify calculated km/L efficiency on 2nd full tank fill-up.
    participant P109 as UC-047: Test retrieving fuel log history via GET /api/v1/fuel.     Should retur
    participant P110 as UC-047 Acceptance Criterion: WHEN two consecutive full-tank fuel logs are create
    participant P111 as UC-047 Alternate Flow A1: Partial fill-up (is_full_tank = False) skips efficienc
    participant P112 as UC-047 Main Flow 5: If efficiency is 30% lower than vehicle baseline average,
    participant P113 as UC-051 Alternate Flow A1: PATCH /api/v1/fuel/{id} updates entry & recalculates e
    participant P114 as UC-051 Main Flow: DELETE /api/v1/fuel/{id} soft-deletes log & linked expense and
    participant P115 as UC-051 Edge Case: Deleting or patching non-existent log returns HTTP 404.
    participant P116 as UC-034: GET /api/v1/maintenance/schedules should auto-populate schedule template
    participant P117 as UC-034: POST /api/v1/maintenance logs record, updates odometer, and resets sched
    participant P118 as UC-034: POST /api/v1/maintenance rejects negative cost with HTTP 422.
    participant P119 as UC-034: Tenant cross-access rejected.
    participant P120 as UC-036: POST /api/v1/maintenance logs service record and updates linked schedule
    participant P121 as UC-036: Odometer reading > current_odometer_km updates vehicle current_odometer_
    participant P122 as UC-036: Omitting maintenance_schedule_id matches schedule item by task name subs
    participant P123 as UC-036: Rejects negative cost, negative odometer, whitespace service_type, or in
    participant P124 as UC-036: Enforces X-Organization-ID header presence and cross-tenant access prote
    participant P125 as UC-037: GET /api/v1/maintenance/records retrieves service records sorted by serv
    participant P126 as UC-037: Pagination limit and offset parameters operate correctly.
    participant P127 as UC-037: Returns 404 when vehicle_id does not exist in active organization.
    participant P128 as UC-037: Header requirements and cross-tenant boundaries are strictly enforced.
    participant P129 as Test 1: Verify GET /api/v1/vehicles/types?q=Toyota returns seeded Toyota models.
    participant P130 as Test 2: Verify POST /api/v1/vehicles registers new vehicle with tenant organizat
    participant P131 as Test 3: Verify duplicate VIN within same organization returns HTTP 409 Conflict.
    participant P132 as Test 4: Verify exceeding max_vehicles quota (max=2 for sample_org) returns HTTP
    participant P133 as Test 5: Verify custom make/model is dynamically indexed into VehicleType catalog
    participant P134 as ensure_organization()
    participant P135 as test_uc011_sole_owner_blocking()
    participant P136 as test_setup()
    participant P137 as UC-048 Acceptance Criterion: System returns fleet aggregate average efficiency a
    participant P138 as UC-048 Efficiency Trends: Monthly fuel cost totals and efficiency trends per veh
    participant P139 as UC-035: POST /api/v1/maintenance/schedules creates custom schedule with default
    participant P140 as UC-035: POST /api/v1/maintenance/schedules uses provided last_performed_km and l
    participant P141 as UC-035: Rejects zero/negative intervals or empty task names with 422.
    participant P142 as UC-035: PATCH /api/v1/maintenance/schedules/{id} updates parameters and recalcul
    participant P143 as UC-035: DELETE /api/v1/maintenance/schedules/{id} soft-deletes schedule task.
    participant P144 as UC-035: Header validation and tenant cross-access isolation.
    participant P145 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with empty schedule_ids a
    participant P146 as UC-038: POST /api/v1/maintenance/schedules/bulk-accept with specific schedule_id
    participant P147 as UC-038: Returns 404 when vehicle_id is not found in active organization.
    participant P148 as UC-038: Returns 404 when one or more schedule_ids do not belong to the vehicle.
    participant P149 as UC-038: Headers and cross-tenant boundaries are strictly enforced.
    participant P150 as UC-016: Owner can create organization invitation, generating a secure 64-char to
    participant P151 as UC-016: Inviting with invalid or blank email yields HTTP 422 Unprocessable Entit
    participant P152 as UC-016: Inviting with unsupported role string yields HTTP 422 Unprocessable Enti
    participant P153 as UC-016: Re-inviting same email updates existing invitation token and TTL without
    participant P154 as UC-016: Non-owner caller attempting to send invitation yields HTTP 403 Forbidden
    participant P155 as UC-016: Owner can list all pending invitations for organization.
    participant P156 as UC-016: Listing invitations for non-existent org yields HTTP 404 Not Found.
    participant P157 as Test 1: Verify PATCH /api/v1/vehicles/{vehicle_id} successfully updates vehicle
    participant P158 as Test 2: Verify updating vehicle under wrong organization_id returns HTTP 403 For
    participant P159 as Test 3: Verify updating non-existent vehicle returns HTTP 404 Not Found.
    participant P160 as Test 4: Verify manual odometer update with discrepancy > 500 km generates an Aud
    participant P161 as Test 5: Verify non-dictionary custom_specs payload returns HTTP 422 Unprocessabl
    participant P162 as create_organization()
    participant P163 as auto_create_personal_organization()
    participant P164 as setup_db()
    participant P165 as test_setup()
    participant P166 as test_setup()
    participant P167 as test_setup()
    participant P168 as AC 1: WHEN a new user authenticates with Google One-Tap THE SYSTEM SHALL     cr
    participant P169 as AC 2: WHEN an existing user authenticates with Google One-Tap THE SYSTEM SHALL
    participant P170 as AC 1: WHEN a user registers via Facebook THE SYSTEM SHALL store \"facebook\" insid
    participant P171 as Alternate Flow A1: Account Linking     If email matches existing account with d
    participant P172 as Edge Case: Facebook permission denied for email -> API returns HTTP 400 Bad Requ
    participant P173 as AC 1: WHEN valid email/password details are submitted THE SYSTEM SHALL return HT
    participant P174 as Alternate Flow A1: Account Linking     If user signed up via Google, submitting
    participant P175 as Edge Case: Weak passwords (less than 8 chars, missing upper, missing digit) retu
    participant P176 as Edge Case: Missing email or missing password for email auth provider returns HTT
    participant P177 as AC 1: WHEN valid login credentials are provided THE SYSTEM SHALL return HTTP 200
    participant P178 as Edge Case: Incorrect password returns HTTP 401 Unauthorized.
    participant P179 as Edge Case: Unregistered email returns HTTP 401 Unauthorized.
    participant P180 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P181 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P182 as AC 1: WHEN an existing Google user signs in,     THE SYSTEM SHALL return HTTP 2
    participant P183 as AC 2: WHEN an existing Facebook user signs in,     THE SYSTEM SHALL return HTTP
    participant P184 as AC 3: WHEN an existing Email/Password user signs in via POST /api/v1/auth/login,
    participant P185 as AC 4 (Account Linking Flow A1): WHEN an existing user registered via email
    participant P186 as Edge Case: Incorrect password on email login returns HTTP 401 Unauthorized.
    participant P187 as Edge Case: Sign in with non-existent email returns HTTP 401 Unauthorized.
    participant P188 as Alternate Flow A1: Disabled user account (is_active == False) returns HTTP 403 F
    participant P189 as Alternate Flow A1: Soft-deleted user account (deleted_at IS NOT NULL) returns HT
    participant P190 as AC 1: GIVEN an authenticated user     WHEN they query GET /api/v1/users/me or u
    participant P191 as AC 2: GIVEN a user completing onboarding on SCR-AUTH-007     WHEN they submit P
    participant P192 as AC 3: GIVEN a profile update request with invalid display name length (< 2 chars
    participant P193 as AC 4: GIVEN tenant-scoped requests     THE SYSTEM SHALL enforce multi-tenant ro
    participant P194 as UC-014: POST /api/v1/organizations creates commercial organization and sets owne
    participant P195 as UC-014: POST /api/v1/organizations/personal auto-creates personal organization f
    participant P196 as UC-014: Blank or whitespace organization name rejected with HTTP 422.
    participant P197 as UC-014: GET /api/v1/organizations?user_id={id} returns list of user organization
    participant P198 as UC-014: GET /api/v1/organizations/{id} returns detail or 404 if not found.
    participant P199 as UC-015: POST /api/v1/organizations/switch switches active context for valid user
    participant P200 as UC-015: Switch attempt to organization owned by another user yields HTTP 403 For
    participant P201 as UC-015: Switch attempt to non-existent organization yields HTTP 404 Not Found.
    participant P202 as UC-015: GET /api/v1/organizations/active returns current primary organization fo
    participant P203 as UC-015: GET /api/v1/organizations/active for user with no org returns HTTP 404 N
    participant P204 as Test 1: Verify GET /api/v1/vehicles?status=MAINTENANCE returns only vehicles in
    participant P205 as Test 2: Verify search query matches license plate, make, or model.
    participant P206 as Test 3: Verify filtering by province (e.g. Sindh).
    participant P207 as Test 1: Verify GET /api/v1/vehicles/{vehicle_id} returns detailed vehicle metada
    participant P208 as Test 2: Verify non-existent vehicle ID returns HTTP 404 Not Found.
    participant P209 as Test 3: Verify requesting another tenant's vehicle returns HTTP 403 Forbidden.
    participant P210 as Test 4: Verify PATCH /api/v1/vehicles/{vehicle_id}/status updates vehicle status
    participant P211 as setup_db()
    participant P212 as setup_db()
    participant P213 as setup_db()
    participant P214 as test_setup()
    participant P215 as test_setup()
    participant P216 as test_setup()
    participant P217 as test_setup()
    participant P218 as test_setup()
    participant P219 as test_setup()
    participant P220 as setup_db()
    participant P221 as test_setup()
    participant P222 as test_setup()
    participant P223 as setup_db()
    participant P224 as setup_db()
    participant P225 as setup_db()
    participant P226 as setup_db()
    participant P227 as setup_db()
    participant P228 as setup_db()
    participant P229 as sample_fleet()
    participant P230 as test_setup()
    participant P231 as test_setup()
    participant P232 as sample_org()
    participant P233 as AuthSessionDTO
    participant P234 as SessionRevokeResponse
    participant P235 as UC-004: User Password Authentication & Session Initiation     Authenticates reg
    participant P236 as UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi
    participant P237 as UC-006: Password Reset Execution     Verifies reset token, validates password p
    participant P238 as UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok
    participant P239 as UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token
    participant P240 as UserDTO
    participant P241 as OrganizationDTO
    participant P242 as UserSessionDTO
    participant P243 as AuditService
    participant P244 as ForgotPasswordResponse
    participant P245 as ResetPasswordResponse
    participant P246 as RefreshTokenResponse
    participant P247 as LogoutResponse
    participant P248 as UserSession
    participant P249 as RegisterRequest
    participant P250 as LoginRequest
    participant P251 as ForgotPasswordRequest
    participant P252 as ResetPasswordRequest
    participant P253 as RefreshTokenRequest
    participant P254 as LogoutRequest
    P0->>+ P1: uses
    P1-->>- P0: return
    P1->>+ P0: uses
    P0-->>- P1: return
    P1->>+ P2: uses
    P2-->>- P1: return
    P2->>+ P1: uses
    P1-->>- P2: return
    P2->>+ P3: uses
    P3-->>- P2: return
    P2->>+ P4: uses
    P4-->>- P2: return
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
    P1->>+ P22: uses
    P22-->>- P1: return
    P1->>+ P23: uses
    P23-->>- P1: return
    P1->>+ P24: uses
    P24-->>- P1: return
    P1->>+ P25: uses
    P25-->>- P1: return
    P1->>+ P26: uses
    P26-->>- P1: return
    P1->>+ P27: uses
    P27-->>- P1: return
    P1->>+ P28: uses
    P28-->>- P1: return
    P1->>+ P29: uses
    P29-->>- P1: return
    P1->>+ P30: uses
    P30-->>- P1: return
    P1->>+ P31: uses
    P31-->>- P1: return
    P1->>+ P32: uses
    P32-->>- P1: return
    P1->>+ P33: uses
    P33-->>- P1: return
    P1->>+ P34: uses
    P34-->>- P1: return
    P1->>+ P35: uses
    P35-->>- P1: return
    P1->>+ P36: uses
    P36-->>- P1: return
    P1->>+ P37: uses
    P37-->>- P1: return
    P1->>+ P38: uses
    P38-->>- P1: return
    P1->>+ P39: uses
    P39-->>- P1: return
    P1->>+ P40: uses
    P40-->>- P1: return
    P1->>+ P41: uses
    P41-->>- P1: return
    P1->>+ P42: uses
    P42-->>- P1: return
    P1->>+ P43: uses
    P43-->>- P1: return
    P1->>+ P44: uses
    P44-->>- P1: return
    P1->>+ P45: uses
    P45-->>- P1: return
    P1->>+ P46: uses
    P46-->>- P1: return
    P1->>+ P47: uses
    P47-->>- P1: return
    P1->>+ P48: uses
    P48-->>- P1: return
    P1->>+ P49: uses
    P49-->>- P1: return
    P1->>+ P50: uses
    P50-->>- P1: return
    P1->>+ P51: uses
    P51-->>- P1: return
    P1->>+ P52: uses
    P52-->>- P1: return
    P1->>+ P53: uses
    P53-->>- P1: return
    P1->>+ P54: uses
    P54-->>- P1: return
    P1->>+ P55: uses
    P55-->>- P1: return
    P1->>+ P56: uses
    P56-->>- P1: return
    P1->>+ P57: calls
    P57-->>- P1: return
    P1->>+ P58: uses
    P58-->>- P1: return
    P1->>+ P59: uses
    P59-->>- P1: return
    P1->>+ P60: uses
    P60-->>- P1: return
    P1->>+ P61: uses
    P61-->>- P1: return
    P1->>+ P62: uses
    P62-->>- P1: return
    P1->>+ P63: uses
    P63-->>- P1: return
    P1->>+ P64: uses
    P64-->>- P1: return
    P1->>+ P65: uses
    P65-->>- P1: return
    P1->>+ P66: uses
    P66-->>- P1: return
    P1->>+ P67: uses
    P67-->>- P1: return
    P1->>+ P68: uses
    P68-->>- P1: return
    P1->>+ P69: uses
    P69-->>- P1: return
    P1->>+ P70: uses
    P70-->>- P1: return
    P1->>+ P71: uses
    P71-->>- P1: return
    P1->>+ P72: uses
    P72-->>- P1: return
    P1->>+ P73: uses
    P73-->>- P1: return
    P1->>+ P74: uses
    P74-->>- P1: return
    P1->>+ P75: uses
    P75-->>- P1: return
    P1->>+ P76: uses
    P76-->>- P1: return
    P1->>+ P77: uses
    P77-->>- P1: return
    P1->>+ P78: uses
    P78-->>- P1: return
    P1->>+ P79: uses
    P79-->>- P1: return
    P1->>+ P80: uses
    P80-->>- P1: return
    P1->>+ P81: uses
    P81-->>- P1: return
    P1->>+ P82: uses
    P82-->>- P1: return
    P1->>+ P83: uses
    P83-->>- P1: return
    P1->>+ P84: uses
    P84-->>- P1: return
    P1->>+ P85: uses
    P85-->>- P1: return
    P1->>+ P86: calls
    P86-->>- P1: return
    P1->>+ P87: calls
    P87-->>- P1: return
    P1->>+ P88: calls
    P88-->>- P1: return
    P1->>+ P89: uses
    P89-->>- P1: return
    P1->>+ P90: uses
    P90-->>- P1: return
    P1->>+ P91: uses
    P91-->>- P1: return
    P1->>+ P92: uses
    P92-->>- P1: return
    P1->>+ P93: calls
    P93-->>- P1: return
    P1->>+ P94: calls
    P94-->>- P1: return
    P1->>+ P95: calls
    P95-->>- P1: return
    P1->>+ P96: uses
    P96-->>- P1: return
    P1->>+ P97: uses
    P97-->>- P1: return
    P1->>+ P98: uses
    P98-->>- P1: return
    P1->>+ P99: uses
    P99-->>- P1: return
    P1->>+ P100: uses
    P100-->>- P1: return
    P1->>+ P101: uses
    P101-->>- P1: return
    P1->>+ P102: uses
    P102-->>- P1: return
    P1->>+ P103: uses
    P103-->>- P1: return
    P1->>+ P104: uses
    P104-->>- P1: return
    P1->>+ P105: uses
    P105-->>- P1: return
    P1->>+ P106: uses
    P106-->>- P1: return
    P1->>+ P107: uses
    P107-->>- P1: return
    P1->>+ P108: uses
    P108-->>- P1: return
    P1->>+ P109: uses
    P109-->>- P1: return
    P1->>+ P110: uses
    P110-->>- P1: return
    P1->>+ P111: uses
    P111-->>- P1: return
    P1->>+ P112: uses
    P112-->>- P1: return
    P1->>+ P113: uses
    P113-->>- P1: return
    P1->>+ P114: uses
    P114-->>- P1: return
    P1->>+ P115: uses
    P115-->>- P1: return
    P1->>+ P116: uses
    P116-->>- P1: return
    P1->>+ P117: uses
    P117-->>- P1: return
    P1->>+ P118: uses
    P118-->>- P1: return
    P1->>+ P119: uses
    P119-->>- P1: return
    P1->>+ P120: uses
    P120-->>- P1: return
    P1->>+ P121: uses
    P121-->>- P1: return
    P1->>+ P122: uses
    P122-->>- P1: return
    P1->>+ P123: uses
    P123-->>- P1: return
    P1->>+ P124: uses
    P124-->>- P1: return
    P1->>+ P125: uses
    P125-->>- P1: return
    P1->>+ P126: uses
    P126-->>- P1: return
    P1->>+ P127: uses
    P127-->>- P1: return
    P1->>+ P128: uses
    P128-->>- P1: return
    P1->>+ P129: uses
    P129-->>- P1: return
    P1->>+ P130: uses
    P130-->>- P1: return
    P1->>+ P131: uses
    P131-->>- P1: return
    P1->>+ P132: uses
    P132-->>- P1: return
    P1->>+ P133: uses
    P133-->>- P1: return
    P1->>+ P134: calls
    P134-->>- P1: return
    P1->>+ P135: calls
    P135-->>- P1: return
    P1->>+ P136: calls
    P136-->>- P1: return
    P1->>+ P137: uses
    P137-->>- P1: return
    P1->>+ P138: uses
    P138-->>- P1: return
    P1->>+ P139: uses
    P139-->>- P1: return
    P1->>+ P140: uses
    P140-->>- P1: return
    P1->>+ P141: uses
    P141-->>- P1: return
    P1->>+ P142: uses
    P142-->>- P1: return
    P1->>+ P143: uses
    P143-->>- P1: return
    P1->>+ P144: uses
    P144-->>- P1: return
    P1->>+ P145: uses
    P145-->>- P1: return
    P1->>+ P146: uses
    P146-->>- P1: return
    P1->>+ P147: uses
    P147-->>- P1: return
    P1->>+ P148: uses
    P148-->>- P1: return
    P1->>+ P149: uses
    P149-->>- P1: return
    P1->>+ P150: uses
    P150-->>- P1: return
    P1->>+ P151: uses
    P151-->>- P1: return
    P1->>+ P152: uses
    P152-->>- P1: return
    P1->>+ P153: uses
    P153-->>- P1: return
    P1->>+ P154: uses
    P154-->>- P1: return
    P1->>+ P155: uses
    P155-->>- P1: return
    P1->>+ P156: uses
    P156-->>- P1: return
    P1->>+ P157: uses
    P157-->>- P1: return
    P1->>+ P158: uses
    P158-->>- P1: return
    P1->>+ P159: uses
    P159-->>- P1: return
    P1->>+ P160: uses
    P160-->>- P1: return
    P1->>+ P161: uses
    P161-->>- P1: return
    P1->>+ P162: calls
    P162-->>- P1: return
    P1->>+ P163: calls
    P163-->>- P1: return
    P1->>+ P164: calls
    P164-->>- P1: return
    P1->>+ P165: calls
    P165-->>- P1: return
    P1->>+ P166: calls
    P166-->>- P1: return
    P1->>+ P167: calls
    P167-->>- P1: return
    P1->>+ P168: uses
    P168-->>- P1: return
    P1->>+ P169: uses
    P169-->>- P1: return
    P1->>+ P170: uses
    P170-->>- P1: return
    P1->>+ P171: uses
    P171-->>- P1: return
    P1->>+ P172: uses
    P172-->>- P1: return
    P1->>+ P173: uses
    P173-->>- P1: return
    P1->>+ P174: uses
    P174-->>- P1: return
    P1->>+ P175: uses
    P175-->>- P1: return
    P1->>+ P176: uses
    P176-->>- P1: return
    P1->>+ P177: uses
    P177-->>- P1: return
    P1->>+ P178: uses
    P178-->>- P1: return
    P1->>+ P179: uses
    P179-->>- P1: return
    P1->>+ P180: uses
    P180-->>- P1: return
    P1->>+ P181: uses
    P181-->>- P1: return
    P1->>+ P182: uses
    P182-->>- P1: return
    P1->>+ P183: uses
    P183-->>- P1: return
    P1->>+ P184: uses
    P184-->>- P1: return
    P1->>+ P185: uses
    P185-->>- P1: return
    P1->>+ P186: uses
    P186-->>- P1: return
    P1->>+ P187: uses
    P187-->>- P1: return
    P1->>+ P188: uses
    P188-->>- P1: return
    P1->>+ P189: uses
    P189-->>- P1: return
    P1->>+ P190: uses
    P190-->>- P1: return
    P1->>+ P191: uses
    P191-->>- P1: return
    P1->>+ P192: uses
    P192-->>- P1: return
    P1->>+ P193: uses
    P193-->>- P1: return
    P1->>+ P194: uses
    P194-->>- P1: return
    P1->>+ P195: uses
    P195-->>- P1: return
    P1->>+ P196: uses
    P196-->>- P1: return
    P1->>+ P197: uses
    P197-->>- P1: return
    P1->>+ P198: uses
    P198-->>- P1: return
    P1->>+ P199: uses
    P199-->>- P1: return
    P1->>+ P200: uses
    P200-->>- P1: return
    P1->>+ P201: uses
    P201-->>- P1: return
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
    P1->>+ P211: calls
    P211-->>- P1: return
    P1->>+ P212: calls
    P212-->>- P1: return
    P1->>+ P213: calls
    P213-->>- P1: return
    P1->>+ P214: calls
    P214-->>- P1: return
    P1->>+ P215: calls
    P215-->>- P1: return
    P1->>+ P216: calls
    P216-->>- P1: return
    P1->>+ P217: calls
    P217-->>- P1: return
    P1->>+ P218: calls
    P218-->>- P1: return
    P1->>+ P219: calls
    P219-->>- P1: return
    P1->>+ P220: calls
    P220-->>- P1: return
    P1->>+ P221: calls
    P221-->>- P1: return
    P1->>+ P222: calls
    P222-->>- P1: return
    P1->>+ P223: calls
    P223-->>- P1: return
    P1->>+ P224: calls
    P224-->>- P1: return
    P1->>+ P225: calls
    P225-->>- P1: return
    P1->>+ P226: calls
    P226-->>- P1: return
    P1->>+ P227: calls
    P227-->>- P1: return
    P1->>+ P228: calls
    P228-->>- P1: return
    P1->>+ P229: calls
    P229-->>- P1: return
    P1->>+ P230: calls
    P230-->>- P1: return
    P1->>+ P231: calls
    P231-->>- P1: return
    P1->>+ P232: calls
    P232-->>- P1: return
    P0->>+ P3: uses
    P3-->>- P0: return
    P0->>+ P6: uses
    P6-->>- P0: return
    P0->>+ P10: uses
    P10-->>- P0: return
    P0->>+ P233: uses
    P233-->>- P0: return
    P0->>+ P234: uses
    P234-->>- P0: return
    P0->>+ P235: uses
    P235-->>- P0: return
    P0->>+ P236: uses
    P236-->>- P0: return
    P0->>+ P237: uses
    P237-->>- P0: return
    P0->>+ P238: uses
    P238-->>- P0: return
    P0->>+ P239: uses
    P239-->>- P0: return
    P0->>+ P240: uses
    P240-->>- P0: return
    P0->>+ P241: uses
    P241-->>- P0: return
    P0->>+ P242: uses
    P242-->>- P0: return
    P0->>+ P40: uses
    P40-->>- P0: return
    P0->>+ P41: uses
    P41-->>- P0: return
    P0->>+ P42: uses
    P42-->>- P0: return
    P0->>+ P43: uses
    P43-->>- P0: return
    P0->>+ P44: uses
    P44-->>- P0: return
    P0->>+ P45: uses
    P45-->>- P0: return
    P0->>+ P46: uses
    P46-->>- P0: return
    P0->>+ P47: uses
    P47-->>- P0: return
    P0->>+ P243: uses
    P243-->>- P0: return
    P0->>+ P244: uses
    P244-->>- P0: return
    P0->>+ P245: uses
    P245-->>- P0: return
    P0->>+ P246: uses
    P246-->>- P0: return
    P0->>+ P247: uses
    P247-->>- P0: return
    P0->>+ P248: uses
    P248-->>- P0: return
    P0->>+ P249: uses
    P249-->>- P0: return
    P0->>+ P250: uses
    P250-->>- P0: return
    P0->>+ P251: uses
    P251-->>- P0: return
    P0->>+ P252: uses
    P252-->>- P0: return
    P0->>+ P253: uses
    P253-->>- P0: return
    P0->>+ P254: uses
    P254-->>- P0: return
```

## Connections by Relation

### contains
- [[auth_service.py]] `EXTRACTED`

### uses
- [[Organization]] `INFERRED`
- [[User]] `INFERRED`
- [[AuditLog]] `INFERRED`
- [[UserOrganization]] `INFERRED`
- [[AuthSessionDTO]] `INFERRED`
- [[SessionRevokeResponse]] `INFERRED`
- [[UC-004: User Password Authentication & Session Initiation     Authenticates reg]] `INFERRED`
- [[UC-006: Forgot Password Request     Issues a password reset JWT token with 5-mi]] `INFERRED`
- [[UC-006: Password Reset Execution     Verifies reset token, validates password p]] `INFERRED`
- [[UC-009: Session Refresh & Access Token Renewal     Validates active refresh tok]] `INFERRED`
- [[UC-010: User Sign Out & Token Revocation     Revokes the provided refresh token]] `INFERRED`
- [[UserDTO]] `INFERRED`
- [[OrganizationDTO]] `INFERRED`
- [[UserSessionDTO]] `INFERRED`
- [[UC-007: Fetch current user profile details.]] `INFERRED`
- [[UC-007: Update current user profile (full name, phone, city, job role, avatar).]] `INFERRED`
- [[UC-007: Complete profile onboarding (SCR-AUTH-007) and return updated AuthSessio]] `INFERRED`
- [[UC-007: Multi-tenant authorization boundary verification endpoint.]] `INFERRED`
- [[UC-011: Account Deletion (GDPR Right to be Forgotten).     Soft-deletes user re]] `INFERRED`
- [[UC-013: Active Session Management & Device Tracking     Returns list of active]] `INFERRED`

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*