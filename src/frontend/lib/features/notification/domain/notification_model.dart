class NotificationModel {
  final String id;
  final String userId;
  final String? organizationId;
  final String title;
  final String body;
  final String category;
  final bool isRead;
  final String? readAt;
  final String? actionUrl;
  final String createdAt;

  NotificationModel({
    required this.id,
    required this.userId,
    this.organizationId,
    required this.title,
    required this.body,
    required this.category,
    required this.isRead,
    this.readAt,
    this.actionUrl,
    required this.createdAt,
  });

  factory NotificationModel.fromJson(Map<String, dynamic> json) {
    return NotificationModel(
      id: json['id'] as String,
      userId: json['user_id'] as String,
      organizationId: json['organization_id'] as String?,
      title: json['title'] as String,
      body: json['body'] as String,
      category: json['category'] as String,
      isRead: json['is_read'] as bool,
      readAt: json['read_at'] as String?,
      actionUrl: json['action_url'] as String?,
      createdAt: json['created_at'] as String,
    );
  }
}

class NotificationPaginatedModel {
  final int unreadCount;
  final int total;
  final List<NotificationModel> items;

  NotificationPaginatedModel({
    required this.unreadCount,
    required this.total,
    required this.items,
  });

  factory NotificationPaginatedModel.fromJson(Map<String, dynamic> json) {
    final list = json['items'] as List? ?? [];
    return NotificationPaginatedModel(
      unreadCount: json['unread_count'] as int,
      total: json['total'] as int,
      items: list.map((i) => NotificationModel.fromJson(i as Map<String, dynamic>)).toList(),
    );
  }
}
