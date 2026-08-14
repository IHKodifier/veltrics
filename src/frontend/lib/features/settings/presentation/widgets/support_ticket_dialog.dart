import 'package:flutter/material.dart';

class SupportTicketDialog extends StatefulWidget {
  const SupportTicketDialog({super.key});

  @override
  State<SupportTicketDialog> createState() => _SupportTicketDialogState();
}

class _SupportTicketDialogState extends State<SupportTicketDialog> {
  String _category = 'BUG';
  final TextEditingController _descriptionController = TextEditingController();
  bool _isSubmitting = false;

  @override
  void dispose() {
    _descriptionController.dispose();
    super.dispose();
  }

  void _submitTicket() async {
    if (_descriptionController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter a description for your ticket.')),
      );
      return;
    }

    setState(() => _isSubmitting = true);

    await Future.delayed(const Duration(milliseconds: 600));

    if (mounted) {
      Navigator.of(context).pop();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Support ticket submitted successfully! Ticket ID: TCK-84920'),
          backgroundColor: Color(0xFF0F766E),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Row(
        children: [
          Icon(Icons.headset_mic_outlined, color: Color(0xFF0F766E)),
          SizedBox(width: 8),
          Text('Submit Support Ticket'),
        ],
      ),
      content: SingleChildScrollView(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Category', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
            const SizedBox(height: 6),
            DropdownButtonFormField<String>(
              value: _category,
              items: const [
                DropdownMenuItem(value: 'BUG', child: Text('Bug Report')),
                DropdownMenuItem(value: 'FEATURE_REQUEST', child: Text('Feature Request')),
                DropdownMenuItem(value: 'BILLING', child: Text('Billing & Subscriptions')),
                DropdownMenuItem(value: 'OTHER', child: Text('Other Question')),
              ],
              onChanged: (val) {
                if (val != null) setState(() => _category = val);
              },
              decoration: const InputDecoration(
                contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            const Text('Description', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
            const SizedBox(height: 6),
            TextField(
              controller: _descriptionController,
              maxLines: 4,
              decoration: const InputDecoration(
                hintText: 'Describe the issue or feedback in detail...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.grey.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(6),
              ),
              child: const Row(
                children: [
                  Icon(Icons.info_outline, size: 16, color: Colors.grey),
                  SizedBox(width: 6),
                  Expanded(
                    child: Text(
                      'App version & device specs will be automatically attached to this ticket.',
                      style: TextStyle(fontSize: 11, color: Colors.grey),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: _isSubmitting ? null : () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isSubmitting ? null : _submitTicket,
          child: _isSubmitting
              ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
              : const Text('Submit Ticket'),
        ),
      ],
    );
  }
}
