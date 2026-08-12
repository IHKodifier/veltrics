import 'package:flutter/material.dart';

import '../../../../theme/app_theme.dart';
import '../../data/maintenance_repository.dart';
import '../../domain/maintenance_model.dart';
import 'log_maintenance_screen.dart';
import 'service_history_screen.dart';

class MaintenanceScheduleScreen extends StatefulWidget {
  final String vehicleId;
  final String organizationId;
  final double currentOdometer;

  const MaintenanceScheduleScreen({
    super.key,
    required this.vehicleId,
    required this.organizationId,
    this.currentOdometer = 0.0,
  });

  @override
  State<MaintenanceScheduleScreen> createState() => _MaintenanceScheduleScreenState();
}

class _MaintenanceScheduleScreenState extends State<MaintenanceScheduleScreen> {
  final MaintenanceRepository _repository = MaintenanceRepository();

  List<MaintenanceScheduleModel> _schedules = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchSchedules();
  }

  Future<void> _fetchSchedules() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      final list = await _repository.getSchedules(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      );
      if (!mounted) return;
      setState(() {
        _schedules = list;
        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
        _isLoading = false;
      });
    }
  }

  Widget _buildDueStatusPill(MaintenanceScheduleModel sched, bool isDark) {
    if (!sched.isActive) {
      return VeltricsStatusPill.warning(text: 'INACTIVE', isDark: isDark);
    }

    final kmRemaining = sched.nextDueKm - widget.currentOdometer;
    if (kmRemaining <= 0) {
      return VeltricsStatusPill.error(text: 'OVERDUE', isDark: isDark);
    } else if (kmRemaining <= 1000) {
      return VeltricsStatusPill.warning(text: 'DUE SOON', isDark: isDark);
    } else {
      return VeltricsStatusPill.healthy(text: 'OK', isDark: isDark);
    }
  }

  Future<void> _bulkAcceptAll() async {
    try {
      final updated = await _repository.bulkAcceptSchedules(
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
      );
      if (!mounted) return;
      setState(() {
        _schedules = updated;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Successfully accepted all ${updated.length} default maintenance schedules')),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to bulk accept schedules: ${e.toString().replaceAll("Exception: ", "")}')),
      );
    }
  }

  Widget _buildBulkAcceptBanner() {
    final hasInactive = _schedules.any((s) => !s.isActive);
    if (!hasInactive && _schedules.isNotEmpty) return const SizedBox.shrink();

    return Container(
      margin: const EdgeInsets.only(bottom: VeltricsSpacing.sm),
      padding: const EdgeInsets.all(VeltricsSpacing.sm),
      decoration: BoxDecoration(
        color: VeltricsColors.infoBgLight,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: VeltricsColors.neutral300),
      ),
      child: Row(
        children: [
          const Icon(Icons.playlist_add_check, color: VeltricsColors.infoLight),
          const SizedBox(width: VeltricsSpacing.xs2),
          Expanded(
            child: Text(
              'Default schedules available for activation.',
              style: VeltricsTextStyles.bodySm.copyWith(color: VeltricsColors.neutral800),
            ),
          ),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            ),
            onPressed: _bulkAcceptAll,
            icon: const Icon(Icons.check_circle_outline, size: 16),
            label: const Text('Accept All'),
          ),
        ],
      ),
    );
  }

  Future<void> _toggleActive(MaintenanceScheduleModel sched) async {
    try {
      await _repository.updateSchedule(
        scheduleId: sched.id,
        payload: {'is_active': !sched.isActive},
        organizationId: widget.organizationId,
      );
      if (!mounted) return;
      _fetchSchedules();
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to update task: ${e.toString().replaceAll("Exception: ", "")}')),
      );
    }
  }

  Future<void> _showAddOrEditDialog({MaintenanceScheduleModel? schedule}) async {
    final success = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => _ScheduleEditDialog(
        schedule: schedule,
        vehicleId: widget.vehicleId,
        organizationId: widget.organizationId,
        repository: _repository,
      ),
    );

    if (!mounted) return;
    if (success == true) {
      _fetchSchedules();
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(schedule != null ? 'Schedule task updated' : 'Custom task added successfully')),
      );
    }
  }

  Future<void> _showDeleteDialog(MaintenanceScheduleModel schedule) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Delete Maintenance Task'),
        content: Text('Are you sure you want to remove "${schedule.taskName}" from maintenance schedules?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: VeltricsColors.errorLight),
            onPressed: () => Navigator.pop(dialogContext, true),
            child: const Text('Delete'),
          ),
        ],
      ),
    );

    if (!mounted) return;
    if (confirmed == true) {
      try {
        await _repository.deleteSchedule(
          scheduleId: schedule.id,
          organizationId: widget.organizationId,
        );
        if (!mounted) return;
        _fetchSchedules();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Schedule task deleted')),
        );
      } catch (e) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to delete schedule: ${e.toString().replaceAll("Exception: ", "")}')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Maintenance Schedules'),
        actions: [
          IconButton(
            icon: const Icon(Icons.done_all),
            tooltip: 'Accept All Default Schedules',
            onPressed: _bulkAcceptAll,
          ),
          IconButton(
            icon: const Icon(Icons.history),
            tooltip: 'View Service History',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => ServiceHistoryScreen(
                    vehicleId: widget.vehicleId,
                    organizationId: widget.organizationId,
                    currentOdometer: widget.currentOdometer,
                  ),
                ),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.add),
            tooltip: 'Add Custom Task',
            onPressed: () => _showAddOrEditDialog(),
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchSchedules,
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () async {
          final logged = await Navigator.push<bool>(
            context,
            MaterialPageRoute(
              builder: (_) => LogMaintenanceScreen(
                vehicleId: widget.vehicleId,
                organizationId: widget.organizationId,
                currentOdometer: widget.currentOdometer,
              ),
            ),
          );
          if (!mounted) return;
          if (logged == true) {
            _fetchSchedules();
          }
        },
        icon: const Icon(Icons.add_task),
        label: const Text('Log Service'),
      ),
      body: SafeArea(
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : _errorMessage != null
                ? Center(
                    child: Padding(
                      padding: VeltricsSpacing.pagePadding,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(Icons.error_outline, size: 48, color: VeltricsColors.errorLight),
                          const SizedBox(height: VeltricsSpacing.xs2),
                          Text('Error Loading Schedules', style: VeltricsTextStyles.titleLg),
                          const SizedBox(height: VeltricsSpacing.xs3),
                          Text(_errorMessage!, style: VeltricsTextStyles.bodyMd, textAlign: TextAlign.center),
                          const SizedBox(height: VeltricsSpacing.md),
                          ElevatedButton(
                            onPressed: _fetchSchedules,
                            child: const Text('Retry'),
                          ),
                        ],
                      ),
                    ),
                  )
                : _schedules.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.build_circle_outlined, size: 48, color: VeltricsColors.neutral400),
                            const SizedBox(height: VeltricsSpacing.sm),
                            Text('No maintenance schedules found.', style: VeltricsTextStyles.titleSm),
                            const SizedBox(height: VeltricsSpacing.xs2),
                            ElevatedButton.icon(
                              onPressed: () => _showAddOrEditDialog(),
                              icon: const Icon(Icons.add),
                              label: const Text('Add Custom Task'),
                            ),
                          ],
                        ),
                      )
                    : RefreshIndicator(
                        onRefresh: _fetchSchedules,
                        child: ListView.separated(
                          padding: VeltricsSpacing.pagePadding,
                          itemCount: _schedules.length + 1,
                          separatorBuilder: (_, __) => const SizedBox(height: VeltricsSpacing.sm),
                          itemBuilder: (context, index) {
                            if (index == 0) {
                              return _buildBulkAcceptBanner();
                            }
                            final sched = _schedules[index - 1];

                            final lastDateStr = sched.lastPerformedDate != null
                                ? '${sched.lastPerformedDate!.year}-${sched.lastPerformedDate!.month.toString().padLeft(2, '0')}-${sched.lastPerformedDate!.day.toString().padLeft(2, '0')}'
                                : 'N/A';
                            final nextDateStr = sched.nextDueDate != null
                                ? '${sched.nextDueDate!.year}-${sched.nextDueDate!.month.toString().padLeft(2, '0')}-${sched.nextDueDate!.day.toString().padLeft(2, '0')}'
                                : 'N/A';

                            return Card(
                              child: Padding(
                                padding: VeltricsSpacing.cardPaddingMobile,
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      children: [
                                        Expanded(
                                          child: Text(
                                            sched.taskName,
                                            style: VeltricsTextStyles.titleSm.copyWith(
                                              decoration: sched.isActive ? TextDecoration.none : TextDecoration.lineThrough,
                                              color: sched.isActive ? null : VeltricsColors.neutral400,
                                            ),
                                          ),
                                        ),
                                        _buildDueStatusPill(sched, isDark),
                                        PopupMenuButton<String>(
                                          icon: const Icon(Icons.more_vert, size: 20),
                                          onSelected: (val) {
                                            if (val == 'toggle') {
                                              _toggleActive(sched);
                                            } else if (val == 'edit') {
                                              _showAddOrEditDialog(schedule: sched);
                                            } else if (val == 'delete') {
                                              _showDeleteDialog(sched);
                                            }
                                          },
                                          itemBuilder: (ctx) => [
                                            PopupMenuItem<String>(
                                              value: 'toggle',
                                              child: Row(
                                                children: [
                                                  Icon(
                                                    sched.isActive ? Icons.pause_circle_outline : Icons.play_circle_outline,
                                                    size: 18,
                                                  ),
                                                  const SizedBox(width: 8),
                                                  Text(sched.isActive ? 'Disable Task' : 'Enable Task'),
                                                ],
                                              ),
                                            ),
                                            const PopupMenuItem<String>(
                                              value: 'edit',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.edit_outlined, size: 18),
                                                  SizedBox(width: 8),
                                                  Text('Edit Interval'),
                                                ],
                                              ),
                                            ),
                                            const PopupMenuItem<String>(
                                              value: 'delete',
                                              child: Row(
                                                children: [
                                                  Icon(Icons.delete_outline, size: 18, color: VeltricsColors.errorLight),
                                                  SizedBox(width: 8),
                                                  Text('Delete Task', style: TextStyle(color: VeltricsColors.errorLight)),
                                                ],
                                              ),
                                            ),
                                          ],
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: VeltricsSpacing.xs3),
                                    Wrap(
                                      spacing: 8,
                                      children: [
                                        Chip(
                                          avatar: const Icon(Icons.loop, size: 14),
                                          label: Text('Every ${sched.intervalKm} km / ${sched.intervalDays} days'),
                                          labelStyle: VeltricsTextStyles.labelSm,
                                          visualDensity: VisualDensity.compact,
                                        ),
                                      ],
                                    ),
                                    const Divider(height: 20),
                                    Row(
                                      children: [
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Text('LAST PERFORMED', style: VeltricsTextStyles.labelSm),
                                              const SizedBox(height: 2),
                                              Text(
                                                '${sched.lastPerformedKm.toStringAsFixed(0)} km',
                                                style: VeltricsTextStyles.bodyMd.copyWith(fontWeight: FontWeight.bold),
                                              ),
                                              Text(lastDateStr, style: VeltricsTextStyles.labelSm),
                                            ],
                                          ),
                                        ),
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment: CrossAxisAlignment.start,
                                            children: [
                                              Text('NEXT DUE', style: VeltricsTextStyles.labelSm),
                                              const SizedBox(height: 2),
                                              Text(
                                                '${sched.nextDueKm.toStringAsFixed(0)} km',
                                                style: VeltricsTextStyles.bodyMd.copyWith(
                                                  fontWeight: FontWeight.bold,
                                                  color: theme.colorScheme.primary,
                                                ),
                                              ),
                                              Text(nextDateStr, style: VeltricsTextStyles.labelSm),
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: VeltricsSpacing.sm),
                                    Align(
                                      alignment: Alignment.centerRight,
                                      child: OutlinedButton.icon(
                                        onPressed: () async {
                                          final logged = await Navigator.push<bool>(
                                            context,
                                            MaterialPageRoute(
                                              builder: (_) => LogMaintenanceScreen(
                                                vehicleId: widget.vehicleId,
                                                organizationId: widget.organizationId,
                                                currentOdometer: widget.currentOdometer,
                                                schedule: sched,
                                              ),
                                            ),
                                          );
                                          if (!mounted) return;
                                          if (logged == true) {
                                            _fetchSchedules();
                                          }
                                        },
                                        icon: const Icon(Icons.add_task, size: 16),
                                        label: const Text('Log Service'),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                      ),
      ),
    );
  }
}

class _ScheduleEditDialog extends StatefulWidget {
  final MaintenanceScheduleModel? schedule;
  final String vehicleId;
  final String organizationId;
  final MaintenanceRepository repository;

  const _ScheduleEditDialog({
    required this.schedule,
    required this.vehicleId,
    required this.organizationId,
    required this.repository,
  });

  @override
  State<_ScheduleEditDialog> createState() => _ScheduleEditDialogState();
}

class _ScheduleEditDialogState extends State<_ScheduleEditDialog> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _taskNameController;
  late final TextEditingController _intervalKmController;
  late final TextEditingController _intervalDaysController;
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    final isEdit = widget.schedule != null;
    _taskNameController = TextEditingController(text: isEdit ? widget.schedule!.taskName : '');
    _intervalKmController = TextEditingController(text: isEdit ? widget.schedule!.intervalKm.toString() : '5000');
    _intervalDaysController = TextEditingController(text: isEdit ? widget.schedule!.intervalDays.toString() : '180');
  }

  @override
  void dispose() {
    _taskNameController.dispose();
    _intervalKmController.dispose();
    _intervalDaysController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isSubmitting = true);

    try {
      if (widget.schedule != null) {
        await widget.repository.updateSchedule(
          scheduleId: widget.schedule!.id,
          payload: {
            'task_name': _taskNameController.text.trim(),
            'interval_km': int.parse(_intervalKmController.text.trim()),
            'interval_days': int.parse(_intervalDaysController.text.trim()),
          },
          organizationId: widget.organizationId,
        );
      } else {
        await widget.repository.createSchedule(
          payload: {
            'vehicle_id': widget.vehicleId,
            'task_name': _taskNameController.text.trim(),
            'interval_km': int.parse(_intervalKmController.text.trim()),
            'interval_days': int.parse(_intervalDaysController.text.trim()),
          },
          organizationId: widget.organizationId,
        );
      }
      if (!mounted) return;
      Navigator.pop(context, true);
    } catch (e) {
      if (!mounted) return;
      setState(() => _isSubmitting = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString().replaceAll('Exception: ', ''))),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final isEdit = widget.schedule != null;
    return AlertDialog(
      title: Text(isEdit ? 'Edit Schedule Item' : 'Add Custom Task'),
      content: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(
                controller: _taskNameController,
                decoration: const InputDecoration(
                  labelText: 'Task Name *',
                  hintText: 'e.g. Brake Fluid Flush',
                ),
                validator: (val) {
                  if (val == null || val.trim().isEmpty) {
                    return 'Please enter a task name';
                  }
                  return null;
                },
              ),
              const SizedBox(height: VeltricsSpacing.sm),
              TextFormField(
                controller: _intervalKmController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Interval (km) *',
                  hintText: 'e.g. 10000',
                ),
                validator: (val) {
                  if (val == null || val.trim().isEmpty) {
                    return 'Please enter kilometer interval';
                  }
                  final parsed = int.tryParse(val.trim());
                  if (parsed == null || parsed <= 0) {
                    return 'Must be a positive integer';
                  }
                  return null;
                },
              ),
              const SizedBox(height: VeltricsSpacing.sm),
              TextFormField(
                controller: _intervalDaysController,
                keyboardType: TextInputType.number,
                decoration: const InputDecoration(
                  labelText: 'Interval (Days) *',
                  hintText: 'e.g. 180',
                ),
                validator: (val) {
                  if (val == null || val.trim().isEmpty) {
                    return 'Please enter day interval';
                  }
                  final parsed = int.tryParse(val.trim());
                  if (parsed == null || parsed <= 0) {
                    return 'Must be a positive integer';
                  }
                  return null;
                },
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: _isSubmitting ? null : () => Navigator.pop(context, false),
          child: const Text('Cancel'),
        ),
        ElevatedButton(
          onPressed: _isSubmitting ? null : _submit,
          child: _isSubmitting
              ? const SizedBox(
                  width: 18,
                  height: 18,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
              : Text(isEdit ? 'Save Changes' : 'Add Task'),
        ),
      ],
    );
  }
}
