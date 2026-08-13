import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/expense_repository.dart';

class QuickLogExpenseDialog extends StatefulWidget {
  final String vehicleId;
  final String organizationId;

  const QuickLogExpenseDialog({
    super.key,
    required this.vehicleId,
    required this.organizationId,
  });

  @override
  State<QuickLogExpenseDialog> createState() => _QuickLogExpenseDialogState();
}

class _QuickLogExpenseDialogState extends State<QuickLogExpenseDialog> {
  final _formKey = GlobalKey<FormState>();
  final ExpenseRepository _repository = ExpenseRepository();

  final TextEditingController _amountController = TextEditingController();
  final TextEditingController _notesController = TextEditingController();

  String _category = 'TOLL';
  bool _isSubmitting = false;
  String? _errorMessage;

  final List<Map<String, dynamic>> _quickCategories = [
    {'code': 'TOLL', 'label': 'Toll', 'icon': Icons.toll},
    {'code': 'PARKING', 'label': 'Parking', 'icon': Icons.local_parking},
    {'code': 'WASH', 'label': 'Wash', 'icon': Icons.local_car_wash},
    {'code': 'OTHER', 'label': 'Misc', 'icon': Icons.more_horiz},
  ];

  @override
  void dispose() {
    _amountController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _submitQuickExpense() async {
    if (!_formKey.currentState!.validate()) return;

    final amount = double.parse(_amountController.text.trim());
    setState(() {
      _isSubmitting = true;
      _errorMessage = null;
    });

    try {
      final expense = await _repository.quickLogExpense(
        vehicleId: widget.vehicleId,
        category: _category,
        amount: amount,
        notes: _notesController.text.trim().isNotEmpty ? _notesController.text.trim() : null,
        organizationId: widget.organizationId,
      );

      if (mounted) {
        Navigator.pop(context, expense);
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = e.toString().replaceAll('Exception: ', '');
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
      title: Row(
        children: [
          Icon(Icons.payments, color: theme.colorScheme.primary),
          const SizedBox(width: 8),
          const Text('Quick-Log Expense', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        ],
      ),
      content: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('UC-062 • 1-Tap Dashboard Expense Shortcut', style: VeltricsTextStyles.labelSm),
              const SizedBox(height: 12),

              if (_errorMessage != null) ...[
                Text(_errorMessage!, style: const TextStyle(color: VeltricsColors.errorLight, fontSize: 12)),
                const SizedBox(height: 8),
              ],

              // Category Selection Chips
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: _quickCategories.map((cat) {
                  final isSel = _category == cat['code'];
                  return ChoiceChip(
                    avatar: Icon(cat['icon'] as IconData, size: 14),
                    label: Text(cat['label'] as String),
                    selected: isSel,
                    onSelected: (sel) {
                      if (sel) setState(() => _category = cat['code'] as String);
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 12),

              TextFormField(
                controller: _amountController,
                keyboardType: const TextInputType.numberWithOptions(decimal: true),
                autofocus: true,
                decoration: const InputDecoration(
                  labelText: 'Amount (PKR)',
                  prefixIcon: Icon(Icons.attach_money),
                  prefixText: 'Rs. ',
                ),
                validator: (v) {
                  if (v == null || v.trim().isEmpty) return 'Enter amount';
                  final val = double.tryParse(v.trim());
                  if (val == null || val <= 0) return 'Amount must be > 0';
                  return null;
                },
              ),
              const SizedBox(height: 12),

              TextFormField(
                controller: _notesController,
                decoration: const InputDecoration(
                  labelText: 'Notes (Optional)',
                  prefixIcon: Icon(Icons.notes),
                  hintText: 'e.g. M2 Toll plaza receipt',
                ),
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isSubmitting ? null : _submitQuickExpense,
          child: _isSubmitting
              ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
              : const Text('Save Quick Expense'),
        ),
      ],
    );
  }
}
