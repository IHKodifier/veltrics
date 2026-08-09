import 'package:flutter/material.dart';
import '../../data/auth_repository.dart';
import '../../domain/user_model.dart';

class ProfileSetupScreen extends StatefulWidget {
  final String userId;
  final String? initialFullName;
  final String? initialEmail;
  final AuthRepository authRepository;
  final VoidCallback? onProfileCompleted;

  const ProfileSetupScreen({
    Key? key,
    required this.userId,
    this.initialFullName,
    this.initialEmail,
    required this.authRepository,
    this.onProfileCompleted,
  }) : super(key: key);

  @override
  _ProfileSetupScreenState createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends State<ProfileSetupScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _nameController;
  late TextEditingController _phoneController;
  late TextEditingController _cityController;

  String _selectedRole = 'Fleet Manager';
  bool _isLoading = false;
  String? _errorMessage;

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
    _nameController = TextEditingController(text: widget.initialFullName ?? '');
    _phoneController = TextEditingController();
    _cityController = TextEditingController();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _cityController.dispose();
    super.dispose();
  }

  Future<void> _submitProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      await widget.authRepository.completeProfile(
        userId: widget.userId,
        fullName: _nameController.text.trim(),
        phoneNumber: _phoneController.text.trim().isNotEmpty ? _phoneController.text.trim() : null,
        city: _cityController.text.trim().isNotEmpty ? _cityController.text.trim() : null,
        jobRole: _selectedRole,
      );

      if (mounted) {
        setState(() {
          _isLoading = false;
        });
        if (widget.onProfileCompleted != null) {
          widget.onProfileCompleted!();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Profile setup completed successfully!')),
          );
        }
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('Complete Profile Setup'),
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Personalize Your Profile',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text(
                'Help us customize Veltrics for your fleet management needs.',
                style: TextStyle(color: Colors.grey[600], fontSize: 14),
              ),
              const SizedBox(height: 24),
              if (_errorMessage != null) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.red.shade50,
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.red.shade200),
                  ),
                  child: Text(
                    _errorMessage!,
                    style: TextStyle(color: Colors.red.shade800, fontSize: 13),
                  ),
                ),
                const SizedBox(height: 16),
              ],
              TextFormField(
                key: const Key('name_field'),
                controller: _nameController,
                decoration: const InputDecoration(
                  labelText: 'Full Name *',
                  prefixIcon: Icon(Icons.person),
                  border: OutlineInputBorder(),
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
                key: const Key('phone_field'),
                controller: _phoneController,
                keyboardType: TextInputType.phone,
                decoration: const InputDecoration(
                  labelText: 'Phone Number (Optional)',
                  prefixIcon: Icon(Icons.phone),
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                key: const Key('city_field'),
                controller: _cityController,
                decoration: const InputDecoration(
                  labelText: 'City / Location (Optional)',
                  prefixIcon: Icon(Icons.location_city),
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                key: const Key('role_dropdown'),
                value: _selectedRole,
                decoration: const InputDecoration(
                  labelText: 'Primary Job Role',
                  prefixIcon: Icon(Icons.work),
                  border: OutlineInputBorder(),
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
              const SizedBox(height: 32),
              ElevatedButton(
                key: const Key('complete_profile_btn'),
                onPressed: _isLoading ? null : _submitProfile,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text(
                        'Save & Continue',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
