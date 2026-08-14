import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/notification_repository.dart';

class NotificationPreferencesScreen extends StatefulWidget {
  final String userId;

  const NotificationPreferencesScreen({
    super.key,
    required this.userId,
  });

  @override
  State<NotificationPreferencesScreen> createState() => _NotificationPreferencesScreenState();
}

class _NotificationPreferencesScreenState extends State<NotificationPreferencesScreen> {
  final NotificationRepository _repository = NotificationRepository();

  bool _maintenanceReminders = true;
  bool _documentExpirations = true;
  bool _quotaAlerts = true;
  bool _systemNews = true;
  bool _isSaving = false;

  Future<void> _savePreferences() async {
    setState(() => _isSaving = true);
    try {
      await _repository.updatePreferences(
        userId: widget.userId,
        maintenanceReminders: _maintenanceReminders,
        documentExpirations: _documentExpirations,
        quotaAlerts: _quotaAlerts,
        systemNews: _systemNews,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Notification preferences saved successfully')),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isSaving = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to save preferences: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notification Preferences', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: VeltricsSpacing.pagePadding,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('SCR-NOTIF-002 • Notification Channels & Alert Preferences', style: VeltricsTextStyles.labelSm),
              const SizedBox(height: 16),

              Card(
                child: Column(
                  children: [
                    SwitchListTile(
                      title: const Text('Maintenance Reminders', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: const Text('Push alerts when vehicle service schedules are upcoming or overdue.'),
                      value: _maintenanceReminders,
                      onChanged: (v) => setState(() => _maintenanceReminders = v),
                      secondary: const Icon(Icons.build, color: VeltricsColors.warningLight),
                    ),
                    const Divider(height: 1),
                    SwitchListTile(
                      title: const Text('Document Expirations', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: const Text('Alerts when insurance or vehicle permits are 7 days from expiring.'),
                      value: _documentExpirations,
                      onChanged: (v) => setState(() => _documentExpirations = v),
                      secondary: const Icon(Icons.description, color: VeltricsColors.infoLight),
                    ),
                    const Divider(height: 1),
                    SwitchListTile(
                      title: const Text('Quota & Billing Alerts', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: const Text('Warnings when reaching vehicle limits or ad quota thresholds.'),
                      value: _quotaAlerts,
                      onChanged: (v) => setState(() => _quotaAlerts = v),
                      secondary: const Icon(Icons.warning_amber, color: VeltricsColors.errorLight),
                    ),
                    const Divider(height: 1),
                    SwitchListTile(
                      title: const Text('System News & Updates', style: TextStyle(fontWeight: FontWeight.bold)),
                      subtitle: const Text('Announcements regarding new features and system updates.'),
                      value: _systemNews,
                      onChanged: (v) => setState(() => _systemNews = v),
                      secondary: const Icon(Icons.campaign, color: VeltricsColors.successLight),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              ElevatedButton(
                onPressed: _isSaving ? null : _savePreferences,
                style: ElevatedButton.styleFrom(
                  minimumSize: const Size.fromHeight(48),
                ),
                child: _isSaving
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Text('Save Preferences'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
