import 'package:flutter/material.dart';

class NotificationInboxScreen extends StatefulWidget {
  const NotificationInboxScreen({Key? key}) : super(key: key);

  @override
  State<NotificationInboxScreen> createState() => _NotificationInboxScreenState();
}

class _NotificationInboxScreenState extends State<NotificationInboxScreen> {
  bool _pushEnabled = true;
  bool _emailEnabled = true;
  bool _maintenanceAlerts = true;

  final List<Map<String, dynamic>> _notifications = [
    {
      'id': 'notif-01',
      'title': 'Maintenance Alert: Oil Change Due',
      'message': 'Vehicle V-108 is due for routine engine oil replacement.',
      'category': 'MAINTENANCE',
      'is_read': false,
      'time': '10 mins ago',
    },
    {
      'id': 'notif-02',
      'title': 'Subscription Renewal Reminder',
      'message': 'Your Safepay Pro plan renews in 3 days.',
      'category': 'BILLING',
      'is_read': false,
      'time': '2 hours ago',
    },
    {
      'id': 'notif-03',
      'title': 'Driver Anomaly Detected',
      'message': 'Driver John Doe has been inactive for more than 14 days.',
      'category': 'SAFETY',
      'is_read': true,
      'time': '1 day ago',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications & Inbox'),
        backgroundColor: Colors.indigo,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: 'Channel Preferences',
            onPressed: _showPreferencesModal,
          ),
        ],
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(16.0),
        itemCount: _notifications.length,
        separatorBuilder: (_, __) => const Divider(height: 16),
        itemBuilder: (context, index) {
          final item = _notifications[index];
          final isRead = item['is_read'] as bool;

          return Card(
            elevation: isRead ? 1 : 3,
            color: isRead ? Colors.grey.shade50 : Colors.white,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: _getCategoryColor(item['category'] as String).withOpacity(0.15),
                child: Icon(_getCategoryIcon(item['category'] as String), color: _getCategoryColor(item['category'] as String)),
              ),
              title: Text(
                item['title'] as String,
                style: TextStyle(
                  fontWeight: isRead ? FontWeight.normal : FontWeight.bold,
                  fontSize: 15,
                ),
              ),
              subtitle: Padding(
                padding: const EdgeInsets.only(top: 4.0),
                child: Text(item['message'] as String, style: const TextStyle(fontSize: 13)),
              ),
              trailing: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.end,
                children: [
                  Text(item['time'] as String, style: TextStyle(fontSize: 11, color: Colors.grey.shade500)),
                  const SizedBox(height: 4),
                  if (!isRead)
                    const CircleAvatar(radius: 4, backgroundColor: Colors.indigo),
                ],
              ),
              onTap: () {
                setState(() {
                  _notifications[index]['is_read'] = true;
                });
              },
            ),
          );
        },
      ),
    );
  }

  Color _getCategoryColor(String cat) {
    switch (cat) {
      case 'MAINTENANCE':
        return Colors.orange;
      case 'BILLING':
        return Colors.green;
      case 'SAFETY':
        return Colors.red;
      default:
        return Colors.blue;
    }
  }

  IconData _getCategoryIcon(String cat) {
    switch (cat) {
      case 'MAINTENANCE':
        return Icons.build;
      case 'BILLING':
        return Icons.payment;
      case 'SAFETY':
        return Icons.warning_amber;
      default:
        return Icons.notifications;
    }
  }

  void _showPreferencesModal() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(16))),
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Notification Preferences', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const Divider(height: 24),
                  SwitchListTile(
                    title: const Text('Push Notifications'),
                    subtitle: const Text('Receive push alerts on your mobile device'),
                    value: _pushEnabled,
                    onChanged: (val) {
                      setModalState(() => _pushEnabled = val);
                      setState(() => _pushEnabled = val);
                    },
                  ),
                  SwitchListTile(
                    title: const Text('Email Summaries & Reports'),
                    subtitle: const Text('Receive monthly fleet reports via email'),
                    value: _emailEnabled,
                    onChanged: (val) {
                      setModalState(() => _emailEnabled = val);
                      setState(() => _emailEnabled = val);
                    },
                  ),
                  SwitchListTile(
                    title: const Text('Vehicle Maintenance Alerts'),
                    subtitle: const Text('Overdue and upcoming service notifications'),
                    value: _maintenanceAlerts,
                    onChanged: (val) {
                      setModalState(() => _maintenanceAlerts = val);
                      setState(() => _maintenanceAlerts = val);
                    },
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () => Navigator.pop(context),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo),
                      child: const Text('Save Preferences', style: TextStyle(color: Colors.white)),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}
