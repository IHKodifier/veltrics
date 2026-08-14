import 'package:flutter/material.dart';

class DriverLeaderboardItem {
  final int rank;
  final String driverId;
  final String driverName;
  final String badgeTier; // PLATINUM, GOLD, SILVER, BRONZE
  final int safetyScore;
  final int completedTrips;
  final double totalDistanceKm;

  const DriverLeaderboardItem({
    required this.rank,
    required this.driverId,
    required this.driverName,
    required this.badgeTier,
    required this.safetyScore,
    required this.completedTrips,
    required this.totalDistanceKm,
  });
}

class DriverLeaderboardWidget extends StatelessWidget {
  final List<DriverLeaderboardItem> leaderboard;
  final Function(String driverId)? onDriverSelected;

  const DriverLeaderboardWidget({
    Key? key,
    required this.leaderboard,
    this.onDriverSelected,
  }) : super(key: key);

  Color _getBadgeColor(String tier) {
    switch (tier.toUpperCase()) {
      case 'PLATINUM':
        return Colors.purple.shade700;
      case 'GOLD':
        return Colors.amber.shade700;
      case 'SILVER':
        return Colors.blueGrey.shade600;
      case 'BRONZE':
      default:
        return Colors.brown.shade600;
    }
  }

  IconData _getRankIcon(int rank) {
    if (rank == 1) return Icons.emoji_events;
    if (rank == 2) return Icons.workspace_premium;
    if (rank == 3) return Icons.military_tech;
    return Icons.person;
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Row(
                  children: const [
                    Icon(Icons.leaderboard, color: Colors.indigo),
                    SizedBox(width: 8),
                    Text(
                      'Driver Safety Leaderboard',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
                Text(
                  '${leaderboard.length} Drivers',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey.shade600,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (leaderboard.isEmpty)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 24.0),
                child: Center(
                  child: Text('No driver safety scores calculated yet.'),
                ),
              )
            else
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: leaderboard.length,
                separatorBuilder: (context, index) => const Divider(),
                itemBuilder: (context, index) {
                  final item = leaderboard[index];
                  final badgeColor = _getBadgeColor(item.badgeTier);

                  return ListTile(
                    contentPadding: EdgeInsets.zero,
                    onTap: onDriverSelected != null ? () => onDriverSelected!(item.driverId) : null,
                    leading: CircleAvatar(
                      backgroundColor: item.rank <= 3 ? badgeColor.withOpacity(0.15) : Colors.grey.shade200,
                      child: Icon(
                        _getRankIcon(item.rank),
                        color: item.rank <= 3 ? badgeColor : Colors.grey.shade700,
                      ),
                    ),
                    title: Row(
                      children: [
                        Text(
                          '#${item.rank} ${item.driverName}',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 15,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                          decoration: BoxDecoration(
                            color: badgeColor,
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            item.badgeTier,
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                    subtitle: Text(
                      '${item.completedTrips} trips · ${item.totalDistanceKm.toStringAsFixed(0)} km',
                      style: TextStyle(fontSize: 12, color: Colors.grey.shade600),
                    ),
                    trailing: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          '${item.safetyScore}',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.extrabold,
                            color: badgeColor,
                          ),
                        ),
                        const Text(
                          'pts',
                          style: TextStyle(fontSize: 10, color: Colors.grey),
                        ),
                      ],
                    ),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }
}
