import 'dart:convert';
import 'package:http/http.dart' as http;
import '../domain/organization_model.dart';
import '../domain/organization_invitation_model.dart';

class OrganizationRepository {
  final String baseUrl;

  OrganizationRepository({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<OrganizationModel> createOrganization({
    required String name,
    required String userId,
    bool isPersonal = false,
    int maxVehicles = 3,
    int maxDrivers = 3,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode({
        'name': name,
        'is_personal': isPersonal,
        'max_vehicles': maxVehicles,
        'max_drivers': maxDrivers,
        'owner_id': userId,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return OrganizationModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error creating organization');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to create organization');
    }
  }

  Future<OrganizationModel> autoCreatePersonalOrg({
    required String userId,
    String? userName,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/personal');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'user_id': userId,
        'user_name': userName,
      }),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return OrganizationModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to auto-create personal organization');
    }
  }

  Future<List<OrganizationModel>> getUserOrganizations({
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations').replace(queryParameters: {
      'user_id': userId,
    });

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list.map((json) => OrganizationModel.fromJson(json as Map<String, dynamic>)).toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch user organizations');
    }
  }

  Future<OrganizationModel> switchOrganization({
    required String targetOrganizationId,
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/switch');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode({
        'target_organization_id': targetOrganizationId,
        'user_id': userId,
      }),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      final activeOrgJson = data['active_organization'] as Map<String, dynamic>;
      return OrganizationModel.fromJson(activeOrgJson);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to switch active organization context');
    }
  }

  Future<OrganizationModel> getActiveOrganization({
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/active').replace(queryParameters: {
      'user_id': userId,
    });

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return OrganizationModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch active organization');
    }
  }

  Future<OrganizationModel> updateOrganizationProfile({
    required String organizationId,
    required String userId,
    String? name,
    String? address,
    String? phone,
    String? taxId,
    String? currency,
    String? website,
    String? logoUrl,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/$organizationId');

    final payload = <String, dynamic>{};
    if (name != null) payload['name'] = name;
    if (address != null) payload['address'] = address;
    if (phone != null) payload['phone'] = phone;
    if (taxId != null) payload['tax_id'] = taxId;
    if (currency != null) payload['currency'] = currency;
    if (website != null) payload['website'] = website;
    if (logoUrl != null) payload['logo_url'] = logoUrl;

    final response = await http.patch(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return OrganizationModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error updating organization profile');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to update organization profile');
    }
  }

  Future<OrganizationInvitationModel> inviteTeamMember({
    required String organizationId,
    String? email,
    String? phone,
    required String role,
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/$organizationId/invitations');

    final payload = <String, dynamic>{
      'role': role,
    };
    if (email != null) payload['email'] = email;
    if (phone != null) payload['phone'] = phone;

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode(payload),
    );

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      return OrganizationInvitationModel.fromJson(data);
    } else {
      final error = jsonDecode(response.body);
      if (error is Map && error.containsKey('detail')) {
        if (error['detail'] is List) {
          final first = error['detail'][0];
          throw Exception(first['msg'] ?? 'Validation error creating invitation');
        }
        throw Exception(error['detail']);
      }
      throw Exception('Failed to send team invitation');
    }
  }

  Future<List<OrganizationInvitationModel>> getPendingInvitations({
    required String organizationId,
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/$organizationId/invitations');

    final response = await http.get(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
    );

    if (response.statusCode == 200) {
      final List<dynamic> list = jsonDecode(response.body);
      return list
          .map((json) => OrganizationInvitationModel.fromJson(json as Map<String, dynamic>))
          .toList();
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to fetch pending invitations');
    }
  }

  Future<Map<String, dynamic>> acceptInvitation({
    required String token,
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/invitations/$token/accept');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId,
      },
      body: jsonEncode({'user_id': userId}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to accept invitation');
    }
  }

  Future<Map<String, dynamic>> redeemInvitationCode({
    required String invitationCode,
    required String userId,
  }) async {
    final uri = Uri.parse('$baseUrl/invitations/redeem');

    final response = await http.post(
      uri,
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'invitation_code': invitationCode,
        'user_id': userId,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } else {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to redeem invitation code');
    }
  }

  Future<void> removeMember({
    required String organizationId,
    required String memberUserId,
    required String actorUserId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/$organizationId/members/$memberUserId');

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': actorUserId,
      },
    );

    if (response.statusCode != 200 && response.statusCode != 204) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to remove member from organization');
    }
  }

  Future<void> cancelInvitation({
    required String organizationId,
    required String invitationId,
    required String actorUserId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/$organizationId/invitations/$invitationId');

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': actorUserId,
      },
    );

    if (response.statusCode != 200 && response.statusCode != 204) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to cancel invitation');
    }
  }

  Future<void> softDeleteOrganization({
    required String organizationId,
    required String actorUserId,
  }) async {
    final uri = Uri.parse('$baseUrl/organizations/$organizationId');

    final response = await http.delete(
      uri,
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': actorUserId,
      },
    );

    if (response.statusCode != 200 && response.statusCode != 204) {
      final error = jsonDecode(response.body);
      throw Exception(error['detail'] ?? 'Failed to soft delete organization');
    }
  }
}
