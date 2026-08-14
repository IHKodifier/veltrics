import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';

class ReceiptPickerWidget extends StatefulWidget {
  final String? initialReceiptUrl;
  final ValueChanged<String?> onReceiptChanged;

  const ReceiptPickerWidget({
    super.key,
    this.initialReceiptUrl,
    required this.onReceiptChanged,
  });

  @override
  State<ReceiptPickerWidget> createState() => _ReceiptPickerWidgetState();
}

class _ReceiptPickerWidgetState extends State<ReceiptPickerWidget> {
  String? _receiptUrl;
  bool _isUploading = false;

  @override
  void initState() {
    super.initState();
    _receiptUrl = widget.initialReceiptUrl;
  }

  Future<void> _simulateUploadReceipt() async {
    setState(() => _isUploading = true);

    // Simulate network upload delay
    await Future.delayed(const Duration(milliseconds: 600));

    final mockUrl = '/uploads/receipts/rec_${DateTime.now().millisecondsSinceEpoch}.jpg';
    setState(() {
      _receiptUrl = mockUrl;
      _isUploading = false;
    });

    widget.onReceiptChanged(_receiptUrl);
  }

  void _removeReceipt() {
    setState(() => _receiptUrl = null);
    widget.onReceiptChanged(null);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Receipt Photo Attachment', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey)),
        const SizedBox(height: 6),

        if (_isUploading)
          Container(
            height: 70,
            decoration: BoxDecoration(
              color: Colors.grey.withValues(alpha: 0.1),
              borderRadius: VeltricsRadius.smAll,
              border: Border.all(color: Colors.grey.withValues(alpha: 0.3)),
            ),
            child: const Center(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2)),
                  SizedBox(width: 8),
                  Text('Uploading receipt...', style: TextStyle(fontSize: 12)),
                ],
              ),
            ),
          )
        else if (_receiptUrl != null && _receiptUrl!.isNotEmpty)
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: VeltricsColors.successLight.withValues(alpha: 0.1),
              borderRadius: VeltricsRadius.smAll,
              border: Border.all(color: VeltricsColors.successLight.withValues(alpha: 0.4)),
            ),
            child: Row(
              children: [
                const Icon(Icons.receipt_long, color: VeltricsColors.successLight, size: 24),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Receipt Attached', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: VeltricsColors.successLight)),
                      Text(_receiptUrl!, style: const TextStyle(fontSize: 11, color: Colors.grey), overflow: TextOverflow.ellipsis),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close, size: 18, color: VeltricsColors.errorLight),
                  onPressed: _removeReceipt,
                  tooltip: 'Remove Receipt',
                ),
              ],
            ),
          )
        else
          OutlinedButton.icon(
            onPressed: _simulateUploadReceipt,
            icon: const Icon(Icons.camera_alt, size: 18),
            label: const Text('Attach Receipt Photo'),
            style: OutlinedButton.styleFrom(
              minimumSize: const Size.fromHeight(42),
              shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.smAll),
            ),
          ),
      ],
    );
  }
}
