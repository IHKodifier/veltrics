import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../domain/fuel_log_model.dart';

class FuelAnomalyCard extends StatelessWidget {
  final FuelLogModel fuelLog;
  final VoidCallback? onVerify;

  const FuelAnomalyCard({
    super.key,
    required this.fuelLog,
    this.onVerify,
  });

  @override
  Widget build(BuildContext context) {
    if (!fuelLog.anomalyDetected) {
      return const SizedBox.shrink();
    }

    final isVerified = fuelLog.isVerified;

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isVerified
            ? VeltricsColors.successLight.withValues(alpha: 0.1)
            : VeltricsColors.errorLight.withValues(alpha: 0.1),
        borderRadius: VeltricsRadius.smAll,
        border: Border.all(
          color: isVerified ? VeltricsColors.successLight : VeltricsColors.errorLight,
          width: 1.5,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(
            isVerified ? Icons.check_circle : Icons.warning,
            color: isVerified ? VeltricsColors.successLight : VeltricsColors.errorLight,
            size: 24,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  isVerified ? 'Verified Fuel Anomaly' : 'Fuel Anomaly / Theft Alert',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: isVerified ? VeltricsColors.successLight : VeltricsColors.errorLight,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  fuelLog.anomalyReason ?? 'Abnormal fuel fill parameters detected.',
                  style: const TextStyle(fontSize: 12, color: Colors.black87),
                ),
                if (!isVerified && onVerify != null) ...[
                  const SizedBox(height: 8),
                  OutlinedButton.icon(
                    onPressed: onVerify,
                    icon: const Icon(Icons.check, size: 14),
                    label: const Text('Mark Verified', style: TextStyle(fontSize: 12)),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: VeltricsColors.errorLight,
                      side: const BorderSide(color: VeltricsColors.errorLight),
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      minimumSize: Size.zero,
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}
