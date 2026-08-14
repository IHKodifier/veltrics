import 'package:flutter/material.dart';

enum QuotaType { vehicle, driver }

class QuotaWallDialog extends StatelessWidget {
  final QuotaType quotaType;
  final int currentCount;
  final int maxLimit;
  final VoidCallback onUpgradePressed;
  final VoidCallback onWatchAdPressed;
  final VoidCallback onContactSalesPressed;

  const QuotaWallDialog({
    Key? key,
    required this.quotaType,
    required this.currentCount,
    required this.maxLimit,
    required this.onUpgradePressed,
    required this.onWatchAdPressed,
    required this.onContactSalesPressed,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final title = quotaType == QuotaType.vehicle
        ? 'Vehicle Limit Reached ($currentCount/$maxLimit)'
        : 'Driver Limit Reached ($currentCount/$maxLimit)';
    final message = quotaType == QuotaType.vehicle
        ? 'You have reached the maximum allowed vehicles for your free workspace tier. Upgrade to Pro for up to 25 vehicles or watch a short video ad for +1 free bonus vehicle slot.'
        : 'You have reached the maximum allowed drivers for your free workspace tier. Upgrade to Pro for up to 15 drivers or watch a short video ad for +1 free bonus driver slot.';

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.amber.shade100,
                shape: BoxShape.circle,
              ),
              child: Icon(
                quotaType == QuotaType.vehicle ? Icons.directions_car : Icons.badge,
                size: 40,
                color: Colors.amber.shade900,
              ),
            ),
            const SizedBox(height: 16),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 12),
            Text(
              message,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey.shade700,
                height: 1.4,
              ),
            ),
            const SizedBox(height: 24),
            // Primary Option: Safepay Pro Upgrade
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.of(context).pop();
                  onUpgradePressed();
                },
                icon: const Icon(Icons.star, color: Colors.white),
                label: const Text(
                  'Upgrade to Pro (Safepay)',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF1E3A8A),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 12),
            // Secondary Option: Watch Rewarded Ad for +1 Bonus Slot
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.of(context).pop();
                  onWatchAdPressed();
                },
                icon: const Icon(Icons.ondemand_video, color: Color(0xFF059669)),
                label: const Text(
                  'Watch Short Video Ad (+1 Slot)',
                  style: TextStyle(
                    color: Color(0xFF059669),
                    fontWeight: FontWeight.w600,
                  ),
                ),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  side: const BorderSide(color: Color(0xFF059669), width: 1.5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 16),
            // Enterprise Sales Inquiry Link
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                onContactSalesPressed();
              },
              child: const Text(
                'Managing >25 Vehicles? Contact Enterprise Sales',
                style: TextStyle(
                  fontSize: 12,
                  color: Color(0xFF4B5563),
                  decoration: TextDecoration.underline,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
