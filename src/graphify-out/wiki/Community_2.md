# Community 2

> 153 nodes · cohesion 0.04

## Key Concepts

- [User](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/user.py#L13) (169 connections)
- [AuditLog](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/audit_log.py#L5) (93 connections)
- [UserOrganization](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/user_organization.py#L8) (55 connections)
- [OrganizationInvitation](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/organization_invitation.py#L6) (34 connections)
- [ExpenseLog](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/expense_log.py#L6) (32 connections)
- [FuelLog](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/fuel_log.py#L6) (32 connections)
- [OrganizationInvitationResponse](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization_invitation.py#L45) (25 connections)
- [SwitchOrganizationResponse](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization.py#L67) (23 connections)
- [OrganizationInvitationCreate](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization_invitation.py#L8) (22 connections)
- [OrganizationCreate](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization.py#L7) (22 connections)
- [OrganizationResponse](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization.py#L45) (22 connections)
- [PersonalOrganizationCreate](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization.py#L41) (22 connections)
- [SwitchOrganizationRequest](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization.py#L63) (22 connections)
- [Retrieve organizations list.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L146) (21 connections)
- [UC-015: Switch active organization context for user.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L163) (21 connections)
- [UC-015: Get active organization for user.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L209) (21 connections)
- [Retrieve organization details by ID.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L249) (21 connections)
- [UC-017: Edit Organization Profile Details.     Enforces ISO 4217 currency valida](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L272) (21 connections)
- [UC-018: Invite Driver / Manager via Email or Phone.     Generates a secure 64-ch](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L319) (21 connections)
- [UC-018: List pending organization invitations.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L401) (21 connections)
- [UC-021: Remove Member from Organization.     Prevents owner removal. Unassigns u](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L434) (21 connections)
- [UC-022: Cancel Pending Member Invitation.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L507) (21 connections)
- [UC-014: Provision commercial or custom organization.](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L55) (21 connections)
- [UC-023: Soft Delete Organization & Child Entities.     Rejects personal org dele](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L558) (21 connections)
- [UC-014: Auto-provision personal organization for a user during registration or s](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py#L96) (21 connections)
- *... and 128 more nodes in this community*

## Class Diagram

```mermaid
classDiagram
    class AuditLog {
        +audit_log.py()
    }
    class AuditService {
        +audit_service.py()
    }
    class ExpenseLog {
        +expense_log.py()
    }
    class FuelLog {
        +fuel_log.py()
    }
    class AppNotification {
        +notification.py()
    }
    class UserDevice {
        +notification.py()
    }
    class OrganizationInvitation {
        +organization_invitation.py()
    }
    class OrganizationInvitationCreate {
        +organization_invitation.py()
    }
    class OrganizationInvitationRedeem {
        +organization_invitation.py()
    }
    class OrganizationInvitationResponse {
        +organization_invitation.py()
    }
    class RedeemInvitationResponse {
        +organization_invitation.py()
    }
    class OrganizationCreate {
        +organization.py()
    }
    class OrganizationResponse {
        +organization.py()
    }
    class OrganizationUpdate {
        +organization.py()
    }
    class PersonalOrganizationCreate {
        +organization.py()
    }
    class SwitchOrganizationRequest {
        +organization.py()
    }
    class SwitchOrganizationResponse {
        +organization.py()
    }
    class Trip {
        +trip.py()
    }
    class UserOrganization {
        +user_organization.py()
    }
    class User {
        +user.py()
    }
    AuditLog --> AuditService
    AuditService --> AuditLog
```

## Relationships

- [[Community 1]] (65 shared connections)
- [[Community 3]] (40 shared connections)
- [[unknown]] (25 shared connections)
- [[Community 18]] (15 shared connections)
- [[Community 16]] (8 shared connections)
- [[Community 23]] (5 shared connections)
- [[Community 24]] (5 shared connections)
- [[Community 21]] (5 shared connections)
- [[Community 22]] (5 shared connections)
- [[Community 25]] (4 shared connections)
- [[Community 26]] (4 shared connections)
- [[Community 5]] (2 shared connections)

## Source Files

- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\api\v1\invitations.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/invitations.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\api\v1\organizations.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/api/v1/organizations.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\audit_log.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/audit_log.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\expense_log.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/expense_log.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\fuel_log.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/fuel_log.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\notification.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/notification.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\organization_invitation.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/organization_invitation.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\trip.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/trip.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\user.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/user.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\models\user_organization.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/models/user_organization.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\schemas\organization.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\schemas\organization_invitation.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/schemas/organization_invitation.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\services\audit_service.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/services/audit_service.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\backend\app\services\fuel_service.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/backend/app/services/fuel_service.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\frontend\lib\features\vehicle\data\vehicle_repository.dart](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/frontend/lib/features/vehicle/data/vehicle_repository.dart)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_ads_uc086_122.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/tests/unit/test_ads_uc086_122.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_auth_uc010.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/tests/unit/test_auth_uc010.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_auth_uc011.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/tests/unit/test_auth_uc011.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_auth_uc012.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/tests/unit/test_auth_uc012.py)
- [E:\Non_Office\Dev_Space\vibe_skool\veltrics\src\tests\unit\test_fuel_uc047.py](file:///E:/Non_Office/Dev_Space/vibe_skool/veltrics/src/tests/unit/test_fuel_uc047.py)

## Audit Trail

- EXTRACTED: 300 (22%)
- INFERRED: 1080 (78%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [[index]] to navigate.*