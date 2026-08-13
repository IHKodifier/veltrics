import 'package:flutter/material.dart';
import '../../../../theme/app_theme.dart';
import '../../data/expense_repository.dart';
import '../../domain/expense_model.dart';
import 'log_expense_screen.dart';

class ExpenseHistoryScreen extends StatefulWidget {
  final String? vehicleId;
  final String organizationId;

  const ExpenseHistoryScreen({
    super.key,
    this.vehicleId,
    required this.organizationId,
  });

  @override
  State<ExpenseHistoryScreen> createState() => _ExpenseHistoryScreenState();
}

class _ExpenseHistoryScreenState extends State<ExpenseHistoryScreen> {
  final ExpenseRepository _repository = ExpenseRepository();

  List<ExpenseModel> _expenses = [];
  ExpenseSummaryModel? _summary;
  bool _isLoading = true;
  String? _errorMessage;
  String _selectedCategoryFilter = 'ALL';

  final List<Map<String, String>> _filterCategories = [
    {'code': 'ALL', 'label': 'All Categories'},
    {'code': 'TOLL', 'label': 'Tolls'},
    {'code': 'PARKING', 'label': 'Parking'},
    {'code': 'INSURANCE', 'label': 'Insurance'},
    {'code': 'PERMIT', 'label': 'Permit'},
    {'code': 'WASH', 'label': 'Car Wash'},
    {'code': 'MAINTENANCE', 'label': 'Maintenance'},
    {'code': 'FINE', 'label': 'Fine / Penalty'},
    {'code': 'OTHER', 'label': 'Misc / Other'},
  ];

  @override
  void initState() {
    super.initState();
    _fetchExpenseData();
  }

  Future<void> _fetchExpenseData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final results = await Future.wait([
        _repository.getExpenses(
          vehicleId: widget.vehicleId,
          category: _selectedCategoryFilter == 'ALL' ? null : _selectedCategoryFilter,
          organizationId: widget.organizationId,
        ),
        _repository.getExpenseSummary(
          vehicleId: widget.vehicleId,
          organizationId: widget.organizationId,
        ),
      ]);

      if (mounted) {
        setState(() {
          _expenses = results[0] as List<ExpenseModel>;
          _summary = results[1] as ExpenseSummaryModel;
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

  IconData _getCategoryIcon(String category) {
    switch (category.toUpperCase()) {
      case 'TOLL':
        return Icons.toll;
      case 'PARKING':
        return Icons.local_parking;
      case 'INSURANCE':
        return Icons.security;
      case 'PERMIT':
        return Icons.card_membership;
      case 'WASH':
        return Icons.local_car_wash;
      case 'MAINTENANCE':
        return Icons.build_circle;
      case 'FINE':
        return Icons.gavel;
      default:
        return Icons.payments;
    }
  }

  String _formatDate(DateTime dt) {
    final months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return '${dt.day} ${months[dt.month - 1]} ${dt.year}';
  }

  Future<void> _confirmDeleteExpense(ExpenseModel expense) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Expense Record'),
        content: Text(
          'Are you sure you want to delete this ${expense.category} expense record (Rs. ${expense.amount.toStringAsFixed(0)})?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: VeltricsColors.errorLight),
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (confirm == true) {
      try {
        await _repository.deleteExpense(
          expenseId: expense.id,
          organizationId: widget.organizationId,
        );
        if (mounted) {
          Navigator.pop(context);
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Expense record deleted successfully')),
          );
          _fetchExpenseData();
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Failed to delete expense: $e')),
          );
        }
      }
    }
  }

  void _showExpenseDetailDialog(ExpenseModel expense, ThemeData theme) {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: VeltricsRadius.mdAll),
          title: Row(
            children: [
              Icon(_getCategoryIcon(expense.category), color: theme.colorScheme.primary),
              const SizedBox(width: 8),
              Text('${expense.category} Expense', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            ],
          ),
          content: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildDetailRow('Amount:', 'Rs. ${expense.amount.toStringAsFixed(0)}'),
                _buildDetailRow('Category:', expense.category),
                _buildDetailRow('Expense Date:', _formatDate(expense.expenseDate)),
                _buildDetailRow('Currency:', expense.currency),
                if (expense.receiptPhotoUrl != null && expense.receiptPhotoUrl!.isNotEmpty)
                  _buildDetailRow('Receipt Attached:', 'Yes'),
                if (expense.notes != null && expense.notes!.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  const Text('Notes:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
                  const SizedBox(height: 2),
                  Text(expense.notes!, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                ],
              ],
            ),
          ),
          actions: [
            TextButton.icon(
              icon: const Icon(Icons.delete_outline, color: VeltricsColors.errorLight, size: 18),
              label: const Text('Delete', style: TextStyle(color: VeltricsColors.errorLight)),
              onPressed: () => _confirmDeleteExpense(expense),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Close'),
            ),
          ],
        );
      },
    );
  }

  Widget _buildDetailRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 3),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
          Text(value, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Expense History', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchExpenseData,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          if (widget.vehicleId != null) {
            final res = await Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => LogExpenseScreen(
                  vehicleId: widget.vehicleId!,
                  organizationId: widget.organizationId,
                ),
              ),
            );
            if (res != null && mounted) _fetchExpenseData();
          }
        },
        icon: const Icon(Icons.add),
        label: const Text('Log Expense'),
      ),
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _fetchExpenseData,
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: VeltricsSpacing.pagePadding,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('SCR-EXP-001 • Vehicle Expense Ledger & Metrics', style: VeltricsTextStyles.labelSm),
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

                // 1. Summary Header Card
                if (_summary != null)
                  Card(
                    elevation: 2,
                    child: Padding(
                      padding: VeltricsSpacing.cardPaddingMobile,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text('TOTAL EXPENSE SPEND', style: VeltricsTextStyles.labelSm),
                              Icon(Icons.account_balance_wallet, color: theme.colorScheme.primary, size: 20),
                            ],
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Rs. ${_summary!.totalExpenseAmount.toStringAsFixed(0)}',
                            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: theme.colorScheme.primary),
                          ),
                          const SizedBox(height: 4),
                          Text('${_summary!.totalExpensesCount} total expense records logged', style: const TextStyle(fontSize: 12, color: Colors.grey)),
                          if (_summary!.categoryBreakdown.isNotEmpty) ...[
                            const Divider(height: 20),
                            Text('CATEGORY BREAKDOWN', style: VeltricsTextStyles.labelSm),
                            const SizedBox(height: 8),
                            Wrap(
                              spacing: 8,
                              runSpacing: 4,
                              children: _summary!.categoryBreakdown.entries.map((e) {
                                return Chip(
                                  visualDensity: VisualDensity.compact,
                                  backgroundColor: theme.colorScheme.primary.withValues(alpha: 0.1),
                                  avatar: Icon(_getCategoryIcon(e.key), size: 14, color: theme.colorScheme.primary),
                                  label: Text('${e.key}: Rs. ${e.value.toStringAsFixed(0)}', style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
                                );
                              }).toList(),
                            ),
                          ],
                        ],
                      ),
                    ),
                  ),
                const SizedBox(height: 16),

                // 2. Category Filter Chips
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: _filterCategories.map((cat) {
                      final isSel = _selectedCategoryFilter == cat['code'];
                      return Padding(
                        padding: const EdgeInsets.only(right: 6),
                        child: ChoiceChip(
                          label: Text(cat['label']!),
                          selected: isSel,
                          onSelected: (sel) {
                            if (sel) {
                              setState(() => _selectedCategoryFilter = cat['code']!);
                              _fetchExpenseData();
                            }
                          },
                        ),
                      );
                    }).toList(),
                  ),
                ),
                const SizedBox(height: 16),

                // 3. Expense Ledger List
                if (_isLoading)
                  const Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
                else if (_expenses.isEmpty)
                  Center(
                    child: Padding(
                      padding: const EdgeInsets.all(32),
                      child: Column(
                        children: [
                          const Icon(Icons.receipt_long, size: 48, color: Colors.grey),
                          const SizedBox(height: 8),
                          const Text('No expense records found', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                          const SizedBox(height: 4),
                          const Text('Logged vehicle expenses will appear in this history timeline.', style: TextStyle(color: Colors.grey, fontSize: 12)),
                        ],
                      ),
                    ),
                  )
                else
                  ListView.separated(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: _expenses.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 8),
                    itemBuilder: (context, index) {
                      final item = _expenses[index];
                      return Card(
                        child: ListTile(
                          onTap: () => _showExpenseDetailDialog(item, theme),
                          leading: CircleAvatar(
                            backgroundColor: theme.colorScheme.primary.withValues(alpha: 0.15),
                            child: Icon(_getCategoryIcon(item.category), color: theme.colorScheme.primary, size: 20),
                          ),
                          title: Text(item.category, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                          subtitle: Text(
                            '${_formatDate(item.expenseDate)}${item.notes != null && item.notes!.isNotEmpty ? ' • ${item.notes}' : ''}',
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(fontSize: 12, color: Colors.grey),
                          ),
                          trailing: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            crossAxisAlignment: CrossAxisAlignment.end,
                            children: [
                              Text(
                                'Rs. ${item.amount.toStringAsFixed(0)}',
                                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: theme.colorScheme.primary),
                              ),
                              if (item.receiptPhotoUrl != null)
                                const Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    Icon(Icons.attachment, size: 12, color: Colors.grey),
                                    Text(' Receipt', style: TextStyle(fontSize: 10, color: Colors.grey)),
                                  ],
                                ),
                            ],
                          ),
                        ),
                      );
                    },
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
