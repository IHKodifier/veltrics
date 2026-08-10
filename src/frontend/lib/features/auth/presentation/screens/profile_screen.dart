import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/auth_repository.dart';

class ProfileScreen extends StatefulWidget {
  final String userId;
  final String? refreshToken;
  final AuthRepository authRepository;
  final VoidCallback? onProfileUpdated;
  final VoidCallback? onBackPressed;
  final VoidCallback? onSignOut;

  const ProfileScreen({
    Key? key,
    required this.userId,
    this.refreshToken,
    required this.authRepository,
    this.onProfileUpdated,
    this.onBackPressed,
    this.onSignOut,
  }) : super(key: key);

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _formKey = GlobalKey<FormState>();

  bool _isEditing = false;
  bool _isLoading = true;
  bool _isSaving = false;
  String? _errorMessage;
  String? _successMessage;

  Map<String, dynamic>? _profileData;

  late TextEditingController _nameController;
  late TextEditingController _phoneController;
  late TextEditingController _cityController;
  late TextEditingController _avatarUrlController;
  String _selectedRole = 'Fleet Manager';

  final List<String> _jobRoles = [
    'Fleet Owner',
    'Fleet Manager',
    'Driver',
    'Dispatcher',
    'Individual Vehicle Owner',
    'Viewer'
  ];

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
    _phoneController = TextEditingController();
    _cityController = TextEditingController();
    _avatarUrlController = TextEditingController();
    _fetchProfile();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _cityController.dispose();
    _avatarUrlController.dispose();
    super.dispose();
  }

  Future<void> _fetchProfile() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final profile = await widget.authRepository.getProfile(userId: widget.userId);
      if (mounted) {
        setState(() {
          _profileData = profile;
          _isLoading = false;
          _populateControllers(profile);
        });
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

  void _populateControllers(Map<String, dynamic> profile) {
    _nameController.text = profile['full_name'] ?? '';
    _phoneController.text = profile['phone_number'] ?? '';
    _cityController.text = profile['city'] ?? '';
    _avatarUrlController.text = profile['avatar_url'] ?? profile['photo_url'] ?? '';
    
    final role = profile['job_role'];
    if (role != null && _jobRoles.contains(role)) {
      _selectedRole = role;
    }
  }

  Future<void> _saveProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isSaving = true;
      _errorMessage = null;
      _successMessage = null;
    });

    try {
      final updatedProfile = await widget.authRepository.updateProfile(
        userId: widget.userId,
        fullName: _nameController.text.trim(),
        phoneNumber: _phoneController.text.trim().isNotEmpty ? _phoneController.text.trim() : null,
        city: _cityController.text.trim().isNotEmpty ? _cityController.text.trim() : null,
        jobRole: _selectedRole,
        avatarUrl: _avatarUrlController.text.trim().isNotEmpty ? _avatarUrlController.text.trim() : null,
      );

      if (mounted) {
        setState(() {
          _profileData = updatedProfile;
          _isSaving = false;
          _isEditing = false;
          _successMessage = 'Profile updated successfully!';
        });

        if (widget.onProfileUpdated != null) {
          widget.onProfileUpdated!();
        }

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Profile updated successfully!'),
            backgroundColor: VeltricsColors.successLight,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _isSaving = false;
          _errorMessage = e.toString().replaceAll('Exception: ', '');
        });
      }
    }
  }

  void _cancelEdit() {
    setState(() {
      _isEditing = false;
      _errorMessage = null;
      if (_profileData != null) {
        _populateControllers(_profileData!);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('User Profile & Settings'),
        leading: widget.onBackPressed != null
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: widget.onBackPressed,
              )
            : null,
        actions: [
          if (!_isLoading && !_isEditing)
            IconButton(
              key: const Key('edit_profile_icon_button'),
              icon: const Icon(Icons.edit),
              tooltip: 'Edit Profile',
              onPressed: () {
                setState(() {
                  _isEditing = true;
                  _successMessage = null;
                });
              },
            ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _fetchProfile,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    _buildHeaderCard(isDark),
                    const SizedBox(height: 24),
                    if (_errorMessage != null) ...[
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: VeltricsColors.errorBgLight,
                          borderRadius: VeltricsRadius.smAll,
                          border: Border.all(color: VeltricsColors.errorLight.withOpacity(0.5)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.error_outline, color: VeltricsColors.errorLight, size: 20),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                _errorMessage!,
                                style: const TextStyle(color: VeltricsColors.errorLight, fontSize: 13),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),
                    ],
                    if (_successMessage != null && !_isEditing) ...[
                      Container(
                        padding: const EdgeInsets.all(12),
                        decoration: BoxDecoration(
                          color: VeltricsColors.successBgLight,
                          borderRadius: VeltricsRadius.smAll,
                          border: Border.all(color: VeltricsColors.successLight.withOpacity(0.5)),
                        ),
                        child: Row(
                          children: [
                            const Icon(Icons.check_circle_outline, color: VeltricsColors.successLight, size: 20),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                _successMessage!,
                                style: const TextStyle(color: VeltricsColors.successLight, fontSize: 13),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 16),
                    ],
                    _isEditing ? _buildEditForm(isDark) : _buildViewDetailsCard(isDark),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildHeaderCard(bool isDark) {
    final fullName = _profileData?['full_name'] ?? 'Veltrics User';
    final jobRole = _profileData?['job_role'] ?? 'Fleet Member';
    final email = _profileData?['email'] ?? '';
    final avatarUrl = _profileData?['avatar_url'] ?? _profileData?['photo_url'];
    final provider = (_profileData?['auth_provider'] ?? 'email').toUpperCase();

    final initials = fullName.isNotEmpty
        ? fullName.trim().split(' ').map((e) => e.isNotEmpty ? e[0] : '').take(2).join()
        : 'VU';

    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.lgAll),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            CircleAvatar(
              radius: 44,
              backgroundColor: VeltricsColors.of(VeltricsPalette.teal).shade500,
              backgroundImage: (avatarUrl != null && avatarUrl.toString().startsWith('http'))
                  ? NetworkImage(avatarUrl)
                  : null,
              child: (avatarUrl == null || !avatarUrl.toString().startsWith('http'))
                  ? Text(
                      initials.toUpperCase(),
                      style: VeltricsTextStyles.displayLg.copyWith(color: Colors.white),
                    )
                  : null,
            ),
            const SizedBox(height: 16),
            Text(
              fullName,
              style: VeltricsTextStyles.titleLg.copyWith(fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 4),
            Text(
              jobRole,
              style: VeltricsTextStyles.bodyMd.copyWith(color: VeltricsColors.neutral500),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.email_outlined, size: 14, color: VeltricsColors.neutral400),
                const SizedBox(width: 4),
                Text(
                  email,
                  style: VeltricsTextStyles.bodySm.copyWith(color: VeltricsColors.neutral500),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: VeltricsColors.neutral100,
                borderRadius: VeltricsRadius.pillAll,
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    provider == 'GOOGLE'
                        ? Icons.g_mobiledata
                        : provider == 'FACEBOOK'
                            ? Icons.facebook
                            : Icons.lock_outline,
                    size: 14,
                    color: VeltricsColors.neutral700,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    'AUTH: $provider',
                    style: VeltricsTextStyles.labelSm.copyWith(color: VeltricsColors.neutral700),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showSignOutConfirmation() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Sign Out'),
        content: const Text('Are you sure you want to sign out of Veltrics?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            key: const Key('confirm_logout_btn'),
            style: ElevatedButton.styleFrom(backgroundColor: VeltricsColors.errorLight),
            onPressed: () async {
              Navigator.of(ctx).pop();
              if (widget.refreshToken != null) {
                await widget.authRepository.logout(refreshToken: widget.refreshToken!);
              }
              if (widget.onSignOut != null) {
                widget.onSignOut!();
              }
            },
            child: const Text('Sign Out', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  void _showDeleteAccountConfirmation() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete Account'),
        content: const Text(
          'Are you sure you want to permanently delete your account? '
          'This action is IRREVERSIBLE. Your personal identifying data will be anonymized per GDPR standards.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            key: const Key('confirm_delete_account_btn'),
            style: ElevatedButton.styleFrom(backgroundColor: VeltricsColors.errorLight),
            onPressed: () async {
              Navigator.of(ctx).pop();
              try {
                await widget.authRepository.deleteAccount(userId: widget.userId);
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Account successfully deleted and anonymized.'),
                      backgroundColor: VeltricsColors.successLight,
                    ),
                  );
                  if (widget.onSignOut != null) {
                    widget.onSignOut!();
                  }
                }
              } catch (e) {
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(e.toString().replaceAll('Exception: ', '')),
                      backgroundColor: VeltricsColors.errorLight,
                    ),
                  );
                }
              }
            },
            child: const Text('Delete Account', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  Widget _buildViewDetailsCard(bool isDark) {
    final phone = _profileData?['phone_number'] ?? 'Not provided';
    final city = _profileData?['city'] ?? 'Not specified';
    final isSuperAdmin = _profileData?['is_super_admin'] == true;

    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Profile Information',
                  style: VeltricsTextStyles.titleMd.copyWith(fontWeight: FontWeight.bold),
                ),
                ElevatedButton.icon(
                  key: const Key('edit_profile_btn'),
                  onPressed: () {
                    setState(() {
                      _isEditing = true;
                      _successMessage = null;
                    });
                  },
                  icon: const Icon(Icons.edit, size: 16),
                  label: const Text('Edit'),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    minimumSize: const Size(0, 36),
                  ),
                ),
              ],
            ),
            const Divider(height: 24),
            _buildDetailRow(Icons.person_outline, 'Full Name', _profileData?['full_name'] ?? 'N/A'),
            const SizedBox(height: 14),
            _buildDetailRow(Icons.phone_outlined, 'Phone Number', phone),
            const SizedBox(height: 14),
            _buildDetailRow(Icons.location_city_outlined, 'City / Location', city),
            const SizedBox(height: 14),
            _buildDetailRow(Icons.work_outline, 'Job Role', _profileData?['job_role'] ?? 'Fleet Member'),
            if (isSuperAdmin) ...[
              const SizedBox(height: 14),
              _buildDetailRow(Icons.admin_panel_settings_outlined, 'System Role', 'Super Administrator'),
            ],
            const Divider(height: 32),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                key: const Key('sign_out_btn'),
                onPressed: _showSignOutConfirmation,
                icon: const Icon(Icons.logout, color: VeltricsColors.errorLight),
                label: const Text('Sign Out', style: TextStyle(color: VeltricsColors.errorLight)),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: VeltricsColors.errorLight),
                  padding: const EdgeInsets.symmetric(vertical: 12),
                ),
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: TextButton.icon(
                key: const Key('delete_account_btn'),
                onPressed: _showDeleteAccountConfirmation,
                icon: const Icon(Icons.delete_forever, color: VeltricsColors.errorLight),
                label: const Text('Delete Account (GDPR)', style: TextStyle(color: VeltricsColors.errorLight, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }


  Widget _buildDetailRow(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, size: 20, color: VeltricsColors.neutral500),
        const SizedBox(width: 12),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              label,
              style: VeltricsTextStyles.labelSm.copyWith(color: VeltricsColors.neutral400),
            ),
            const SizedBox(height: 2),
            Text(
              value,
              style: VeltricsTextStyles.bodyMd.copyWith(fontWeight: FontWeight.w500),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildEditForm(bool isDark) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Edit Profile Details',
                style: VeltricsTextStyles.titleMd.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('edit_name_field'),
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Full Name *',
                  prefixIcon: Icon(Icons.person),
                ),
                validator: (val) {
                  if (val == null || val.trim().length < 2) {
                    return 'Full name must be at least 2 characters.';
                  }
                  if (val.trim().length > 50) {
                    return 'Full name cannot exceed 50 characters.';
                  }
                  return null;
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('edit_phone_field'),
                controller: _phoneController,
                keyboardType: TextInputType.phone,
                decoration: const InputDecoration(
                  labelText: 'Phone Number (Optional)',
                  prefixIcon: Icon(Icons.phone),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('edit_city_field'),
                controller: _cityController,
                decoration: const InputDecoration(
                  labelText: 'City / Location (Optional)',
                  prefixIcon: Icon(Icons.location_city),
                ),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                key: const Key('edit_role_dropdown'),
                value: _selectedRole,
                decoration: const InputDecoration(
                  labelText: 'Job Role',
                  prefixIcon: Icon(Icons.work),
                ),
                items: _jobRoles.map((role) {
                  return DropdownMenuItem(
                    value: role,
                    child: Text(role),
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
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('edit_avatar_field'),
                controller: _avatarUrlController,
                decoration: const InputDecoration(
                  labelText: 'Avatar Image URL (Optional)',
                  prefixIcon: Icon(Icons.image_outlined),
                ),
              ),
              const SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      key: const Key('cancel_edit_btn'),
                      onPressed: _isSaving ? null : _cancelEdit,
                      child: const Text('Cancel'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: ElevatedButton(
                      key: const Key('save_profile_btn'),
                      onPressed: _isSaving ? null : _saveProfile,
                      child: _isSaving
                          ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                            )
                          : const Text('Save Changes'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
