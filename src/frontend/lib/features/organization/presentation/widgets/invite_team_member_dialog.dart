import 'package:flutter/material.dart';
import '../../data/organization_repository.dart';
import '../../domain/organization_invitation_model.dart';

class InviteTeamMemberDialog extends StatefulWidget {
  final String organizationId;
  final String currentUserId;
  final OrganizationRepository repository;

  const InviteTeamMemberDialog({
    super.key,
    required this.organizationId,
    required this.currentUserId,
    required this.repository,
  });

  @override
  State<InviteTeamMemberDialog> createState() => _InviteTeamMemberDialogState();
}

class _InviteTeamMemberDialogState extends State<InviteTeamMemberDialog> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  String _selectedRole = 'manager';
  bool _isLoading = false;
  bool _isFetchingInvitations = true;
  String? _errorMessage;
  String? _successMessage;
  List<OrganizationInvitationModel> _pendingInvitations = [];

  final List<String> _roles = ['admin', 'manager', 'driver', 'viewer'];

  @override
  void initState() {
    super.initState();
    _loadPendingInvitations();
  }

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  Future<void> _loadPendingInvitations() async {
    setState(() {
      _isFetchingInvitations = true;
    });

    try {
      final invitations = await widget.repository.getPendingInvitations(
        organizationId: widget.organizationId,
        userId: widget.currentUserId,
      );
      if (mounted) {
        setState(() {
          _pendingInvitations = invitations;
          _isFetchingInvitations = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isFetchingInvitations = false;
        });
      }
    }
  }

  Future<void> _handleSendInvite() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _successMessage = null;
    });

    try {
      final invitation = await widget.repository.inviteTeamMember(
        organizationId: widget.organizationId,
        email: _emailController.text.trim(),
        role: _selectedRole,
        userId: widget.currentUserId,
      );

      if (mounted) {
        setState(() {
          _isLoading = false;
          _successMessage = 'Invitation sent successfully to ${invitation.email}!';
          _emailController.clear();
        });
        _loadPendingInvitations();
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isLoading = false;
          _errorMessage = e.toString().replaceAll('Exception: ', '');
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return AlertDialog(
      backgroundColor: const Color(0xFF1E293B),
      title: Row(
        children: [
          const Icon(Icons.person_add_alt_1_rounded, color: Color(0xFF38BDF8)),
          const SizedBox(width: 10),
          Text(
            'Invite Team Member',
            style: theme.textTheme.titleMedium?.copyWith(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
      content: SizedBox(
        width: 440,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Recipient Email',
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: const Color(0xFF94A3B8),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 6),
                    TextFormField(
                      controller: _emailController,
                      keyboardType: TextInputType.emailAddress,
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        hintText: 'colleague@company.com',
                        hintStyle: const TextStyle(color: Color(0xFF94A3B8)),
                        filled: true,
                        fillColor: const Color(0xFF0F172A),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: const BorderSide(color: Color(0xFF334155)),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                      ),
                      validator: (value) {
                        if (value == null || value.trim().isEmpty) {
                          return 'Email is required';
                        }
                        if (!value.contains('@') || !value.contains('.')) {
                          return 'Enter a valid email address';
                        }
                        return null;
                      },
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Assigned Role',
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: const Color(0xFF94A3B8),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    const SizedBox(height: 6),
                    DropdownButtonFormField<String>(
                      value: _selectedRole,
                      dropdownColor: const Color(0xFF0F172A),
                      style: const TextStyle(color: Colors.white),
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: const Color(0xFF0F172A),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(8),
                          borderSide: const BorderSide(color: Color(0xFF334155)),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                      ),
                      items: _roles.map((role) {
                        return DropdownMenuItem<String>(
                          value: role,
                          child: Text(role.toUpperCase()),
                        );
                      }).toList(),
                      onChanged: (val) {
                        if (val != null) {
                          setState(() {
                            _selectedRole = val;
                          });
                        }
                      },
                    ),
                  ],
                ),
              ),

              if (_errorMessage != null) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.red.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: Colors.red.shade400),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.error_outline, color: Colors.redAccent, size: 20),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _errorMessage!,
                          style: const TextStyle(color: Colors.redAccent, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ],

              if (_successMessage != null) ...[
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: Colors.green.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(6),
                    border: Border.all(color: Colors.green.shade400),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.check_circle_outline, color: Colors.greenAccent, size: 20),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          _successMessage!,
                          style: const TextStyle(color: Colors.greenAccent, fontSize: 13),
                        ),
                      ),
                    ],
                  ),
                ),
              ],

              const SizedBox(height: 24),
              const Divider(color: Color(0xFF334155)),
              const SizedBox(height: 12),
              Text(
                'Pending Invitations',
                style: theme.textTheme.titleSmall?.copyWith(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 8),

              if (_isFetchingInvitations)
                const Center(
                  child: Padding(
                    padding: EdgeInsets.all(16.0),
                    child: CircularProgressIndicator(strokeWidth: 2),
                  ),
                )
              else if (_pendingInvitations.isEmpty)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 12.0),
                  child: Text(
                    'No pending invitations found.',
                    style: TextStyle(color: Colors.grey.shade400, fontSize: 13),
                  ),
                )
              else
                Container(
                  constraints: const BoxConstraints(maxHeight: 160),
                  child: ListView.separated(
                    shrinkWrap: true,
                    itemCount: _pendingInvitations.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 6),
                    itemBuilder: (context, index) {
                      final item = _pendingInvitations[index];
                      return Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                        decoration: BoxDecoration(
                          color: const Color(0xFF0F172A),
                          borderRadius: BorderRadius.circular(6),
                          border: Border.all(color: const Color(0xFF334155)),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    item.email,
                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w500, fontSize: 13),
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                  Text(
                                    'Role: ${item.role.toUpperCase()} · Status: ${item.status}',
                                    style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 11),
                                  ),
                                ],
                              ),
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                              decoration: BoxDecoration(
                                color: Colors.amber.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                item.status,
                                style: const TextStyle(color: Colors.amber, fontSize: 11, fontWeight: FontWeight.bold),
                              ),
                            ),
                          ],
                        ),
                      );
                    },
                  ),
                ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Close', style: TextStyle(color: Color(0xFF94A3B8))),
        ),
        ElevatedButton(
          onPressed: _isLoading ? null : _handleSendInvite,
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF0284C7),
            foregroundColor: Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
          ),
          child: _isLoading
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
              : const Text('Send Invitation'),
        ),
      ],
    );
  }
}
