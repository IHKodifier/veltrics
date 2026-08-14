import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/notification_repository.dart';
import '../../domain/notification_model.dart';
import 'notification_preferences_screen.dart';

class NotificationInboxScreen extends StatefulWidget {
  final String userId;
  final String organizationId;

  const NotificationInboxScreen({
    super.key,
    required this.userId,
    required this.organizationId,
  });

  @override
  State<NotificationInboxScreen> createState() => _NotificationInboxScreenState();
}

class _NotificationInboxScreenState extends State<NotificationInboxScreen> {
  final NotificationRepository _repository = NotificationRepository();

  NotificationPaginatedModel? _data;
  bool _isLoading = true;
  String? _errorMessage;
  bool _unreadOnly = false;

  @override
  void initState() {
    super.initState();
    _fetchNotifications();
  }

  Future<void> _fetchNotifications() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final res = await _repository.getNotifications(
        userId: widget.userId,
        organizationId: widget.organizationId,
        unreadOnly: _unreadOnly,
      );

      if (mounted) {
        setState(() {
          _data = res;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString().replaceAll('Exception: ', '');
          _isLoading = false;
        });
      }
    }
  }

  Future<void> _markAllRead() async {
    try {
      await _repository.markAllAsRead(
        userId: widget.userId,
        organizationId: widget.organizationId,
      );
      if (!mounted) return;
      _fetchNotifications();
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to mark all as read: $e')),
        );
      }
    }
  }

  Future<void> _onNotificationTap(NotificationModel item) async {
    if (!item.isRead) {
      await _repository.markAsRead(userId: widget.userId, notificationId: item.id);
      _fetchNotifications();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            const Text('Notifications', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            if (_data != null && _data!.unreadCount > 0) ...[
              const SizedBox(width: 8),
              Badge(
                label: Text('${_data!.unreadCount}'),
                backgroundColor: VeltricsColors.errorLight,
              ),
            ],
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.done_all),
            tooltip: 'Mark All Read',
            onPressed: _data != null && _data!.unreadCount > 0 ? _markAllRead : null,
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: 'Notification Preferences',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => NotificationPreferencesScreen(userId: widget.userId),
                ),
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text('SCR-NOTIF-001 • In-App Notification Center', style: VeltricsTextStyles.labelSm),
                  FilterChip(
                    label: const Text('Unread Only'),
                    selected: _unreadOnly,
                    onSelected: (sel) {
                      setState(() => _unreadOnly = sel);
                      _fetchNotifications();
                    },
                  ),
                ],
              ),
            ),
            const Divider(height: 1),

            if (_errorMessage != null)
              Padding(
                padding: const EdgeInsets.all(16),
                child: Text(_errorMessage!, style: const TextStyle(color: VeltricsColors.errorLight)),
              ),

            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _data == null || _data!.items.isEmpty
                      ? _buildEmptyState()
                      : RefreshIndicator(
                          onRefresh: _fetchNotifications,
                          child: ListView.separated(
                            padding: const EdgeInsets.all(16),
                            itemCount: _data!.items.length,
                            separatorBuilder: (_, __) => const SizedBox(height: 8),
                            itemBuilder: (context, index) {
                              final item = _data!.items[index];
                              return _buildNotificationTile(item, theme);
                            },
                          ),
                        ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.notifications_none, size: 64, color: Colors.grey.withValues(alpha: 0.5)),
          const SizedBox(height: 12),
          const Text('No notifications found', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.grey)),
          const SizedBox(height: 4),
          const Text('You are all caught up!', style: TextStyle(fontSize: 12, color: Colors.grey)),
        ],
      ),
    );
  }

  Widget _buildNotificationTile(NotificationModel item, ThemeData theme) {
    final categoryIcon = _getCategoryIcon(item.category);
    final categoryColor = _getCategoryColor(item.category);

    return InkWell(
      onTap: () => _onNotificationTap(item),
      borderRadius: VeltricsRadius.smAll,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: item.isRead ? Colors.transparent : theme.colorScheme.primary.withValues(alpha: 0.05),
          borderRadius: VeltricsRadius.smAll,
          border: Border.all(
            color: item.isRead ? Colors.grey.withValues(alpha: 0.2) : theme.colorScheme.primary.withValues(alpha: 0.3),
          ),
        ),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            CircleAvatar(
              radius: 18,
              backgroundColor: categoryColor.withValues(alpha: 0.15),
              child: Icon(categoryIcon, color: categoryColor, size: 18),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Text(
                          item.title,
                          style: TextStyle(
                            fontSize: 14,
                            fontWeight: item.isRead ? FontWeight.normal : FontWeight.bold,
                          ),
                        ),
                      ),
                      if (!item.isRead)
                        Container(
                          width: 8,
                          height: 8,
                          decoration: BoxDecoration(
                            color: theme.colorScheme.primary,
                            shape: BoxShape.circle,
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(item.body, style: const TextStyle(fontSize: 12, color: Colors.black87)),
                  const SizedBox(height: 6),
                  Text(item.createdAt.split('T')[0], style: const TextStyle(fontSize: 10, color: Colors.grey)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData _getCategoryIcon(String category) {
    switch (category.toUpperCase()) {
      case 'MAINTENANCE':
        return Icons.build;
      case 'DOCUMENT':
        return Icons.description;
      case 'QUOTA':
        return Icons.warning_amber;
      default:
        return Icons.info;
    }
  }

  Color _getCategoryColor(String category) {
    switch (category.toUpperCase()) {
      case 'MAINTENANCE':
        return VeltricsColors.warningLight;
      case 'DOCUMENT':
        return VeltricsColors.infoLight;
      case 'QUOTA':
        return VeltricsColors.errorLight;
      default:
        return VeltricsColors.successLight;
    }
  }
}
