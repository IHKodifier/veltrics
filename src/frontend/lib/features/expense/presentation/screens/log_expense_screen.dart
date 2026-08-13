import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/expense_repository.dart';
import '../widgets/receipt_picker_widget.dart';

class LogExpenseScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;

  const LogExpenseScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
  });

  @override
  State<LogExpenseScreen> createState() => _LogExpenseScreenState();
}

class _LogExpenseScreenState extends State<LogExpenseScreen> {
  final _formKey = GlobalKey<FormState>();
  final ExpenseRepository _repository = ExpenseRepository();

  final TextEditingController _amountController = TextEditingController();
  final TextEditingController _notesController = TextEditingController();
  final TextEditingController _receiptUrlController = TextEditingController();

  String _selectedCategory = 'TOLL';
  DateTime _selectedDate = DateTime.now();
  String? _receiptPhotoUrl;
  bool _isSubmitting = false;
  String? _errorMessage;

  final List<Map<String, dynamic>> _categories = [
    {'code': 'TOLL', 'label': 'Toll Tax', 'icon': Icons.toll},
    {'code': 'PARKING', 'label': 'Parking Fee', 'icon': Icons.local_parking},
    {'code': 'INSURANCE', 'label': 'Vehicle Insurance', 'icon': Icons.security},
    {'code': 'PERMIT', 'label': 'Permit & Registration', 'icon': Icons.card_membership},
    {'code': 'WASH', 'label': 'Car Wash & Detailing', 'icon': Icons.local_car_wash},
    {'code': 'MAINTENANCE', 'label': 'Maintenance', 'icon': Icons.build_circle},
    {'code': 'FINE', 'label': 'Traffic Fine / Challan', 'icon': Icons.gavel},
    {'code': 'OTHER', 'label': 'Other / Misc', 'icon': Icons.more_horiz},
  ];

  @override
  void dispose() {
    _amountController.dispose();
    _notesController.dispose();
    _receiptUrlController.dispose();
    super.dispose();
  }

  Future<void> _submitExpense() async {
    if (!_formKey.currentState!.validate()) return;

    final amount = double.parse(_amountController.text.trim());
    if (amount <= 0) {
      setState(() {
        _errorMessage = 'Expense amount must be greater than 0.';
      });
      return;
    }

    setState(() {
      _isSubmitting = true;
      _errorMessage = null;
    });

    try {
      final expense = await _repository.logExpense(
        vehicleId: widget.vehicleId,
        category: _selectedCategory,
        amount: amount,
        expenseDate: _selectedDate,
        receiptPhotoUrl: _receiptPhotoUrl,
        notes: _notesController.text.trim().isNotEmpty ? _notesController.text.trim() : null,
        organizationId: widget.organizationId,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Expense logged successfully (Rs. ${expense.amount.toStringAsFixed(0)})'),
            backgroundColor: VeltricsColors.successLight,
          ),
        );
        Navigator.pop(context, expense);
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isSubmitting = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Log Fleet Expense', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: VeltricsSpacing.pagePadding,
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('SCR-EXP-002 • Vehicle Expense Recording', style: VeltricsTextStyles.labelSm),
                const SizedBox(height: VeltricsSpacing.xs2),

                if (_errorMessage != null) ...[
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: VeltricsColors.errorLight.withValues(alpha: 0.15),
                      borderRadius: VeltricsRadius.smAll,
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline, color: VeltricsColors.errorLight),
                        const SizedBox(width: 8),
                        Expanded(child: Text(_errorMessage!, style: const TextStyle(color: VeltricsColors.errorLight))),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),
                ],

                // 1. Category Selection Chips Grid
                Card(
                  child: Padding(
                    padding: VeltricsSpacing.cardPaddingMobile,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('EXPENSE CATEGORY', style: VeltricsTextStyles.labelSm),
                        const SizedBox(height: 12),
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: _categories.map((cat) {
                            final isSel = _selectedCategory == cat['code'];
                            return ChoiceChip(
                              avatar: Icon(cat['icon'] as IconData, size: 16, color: isSel ? Colors.white : theme.colorScheme.primary),
                              label: Text(cat['label'] as String),
                              selected: isSel,
                              onSelected: (sel) {
                                if (sel) setState(() => _selectedCategory = cat['code'] as String);
                              },
                            );
                          }).toList(),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 2. Amount & Date Inputs
                Card(
                  child: Padding(
                    padding: VeltricsSpacing.cardPaddingMobile,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('AMOUNT & DATE', style: VeltricsTextStyles.labelSm),
                        const SizedBox(height: 12),
                        TextFormField(
                          controller: _amountController,
                          keyboardType: const TextInputType.numberWithOptions(decimal: true),
                          decoration: const InputDecoration(
                            labelText: 'Expense Amount (PKR)',
                            prefixIcon: Icon(Icons.payments),
                            prefixText: 'Rs. ',
                          ),
                          validator: (v) {
                            if (v == null || v.trim().isEmpty) return 'Please enter expense amount';
                            final val = double.tryParse(v.trim());
                            if (val == null || val <= 0) return 'Amount must be greater than 0';
                            return null;
                          },
                        ),
                        const SizedBox(height: 12),
                        InkWell(
                          onTap: () async {
                            final picked = await showDatePicker(
                              context: context,
                              initialDate: _selectedDate,
                              firstDate: DateTime(2020),
                              lastDate: DateTime.now(),
                            );
                            if (picked != null) {
                              setState(() => _selectedDate = picked);
                            }
                          },
                          child: InputDecorator(
                            decoration: const InputDecoration(
                              labelText: 'Expense Date',
                              prefixIcon: Icon(Icons.calendar_today),
                            ),
                            child: Text(
                              '${_selectedDate.day}/${_selectedDate.month}/${_selectedDate.year}',
                              style: const TextStyle(fontSize: 14),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                // 3. Optional Attachment & Notes
                TextFormField(
                  controller: _receiptUrlController,
                  decoration: const InputDecoration(
                    labelText: 'Receipt Image URL (Optional)',
                    prefixIcon: Icon(Icons.receipt_long),
                    hintText: 'https://...',
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _notesController,
                  maxLines: 2,
                  decoration: const InputDecoration(
                    labelText: 'Notes / Details (Optional)',
                    prefixIcon: Icon(Icons.notes),
                    hintText: 'e.g. Purchased oil filter and 4L synthetic motor oil',
                  ),
                ),
                const SizedBox(height: 16),

                ReceiptPickerWidget(
                  initialReceiptUrl: _receiptPhotoUrl,
                  onReceiptChanged: (url) {
                    setState(() => _receiptPhotoUrl = url);
                  },
                ),
                const SizedBox(height: 24),

                // Submit Button
                SizedBox(
                  width: double.infinity,
                  height: 48,
                  child: ElevatedButton(
                    onPressed: _isSubmitting ? null : _submitExpense,
                    child: _isSubmitting
                        ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Text('Save Expense Record', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                  ),
                ),
                const SizedBox(height: 24),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
