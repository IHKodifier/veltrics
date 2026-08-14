import 'package:flutter/material.dart';

class InspectionChecklistDialog extends StatefulWidget {
  final String vehicleId;
  final String vehiclePlate;
  final Function(Map<String, dynamic> inspectionData)? onSubmit;

  const InspectionChecklistDialog({
    Key? key,
    required this.vehicleId,
    required this.vehiclePlate,
    this.onSubmit,
  }) : super(key: key);

  @override
  State<InspectionChecklistDialog> createState() => _InspectionChecklistDialogState();
}

class _InspectionChecklistDialogState extends State<InspectionChecklistDialog> {
  String _inspectionType = 'PRE_TRIP';
  String _overallStatus = 'PASSED';
  final TextEditingController _notesController = TextEditingController();

  final Map<String, bool> _checklistItems = {
    'Tires & Pressure': true,
    'Brakes & Handbrake': true,
    'Headlights & Signals': true,
    'Engine Oil & Coolant': true,
    'Windshield & Wipers': true,
    'Seatbelts & Mirrors': true,
  };

  @override
  void dispose() {
    _notesController.dispose();
    super.dispose();
  }

  void _submitInspection() {
    final bool allPassed = _checklistItems.values.every((val) => val == true);
    final String status = allPassed ? _overallStatus : 'NEEDS_ATTENTION';

    final Map<String, dynamic> payload = {
      'vehicle_id': widget.vehicleId,
      'inspection_type': _inspectionType,
      'overall_status': status,
      'items_json': _checklistItems.map((key, value) => MapEntry(key, value ? 'PASS' : 'FAIL')),
      'notes': _notesController.text,
    };

    if (widget.onSubmit != null) {
      widget.onSubmit!(payload);
    }
    Navigator.of(context).pop(payload);
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.fact_check, color: Colors.indigo, size: 28),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      'Vehicle Inspection Checklist',
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Text(
                'Vehicle: ${widget.vehiclePlate}',
                style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
              ),
              const Divider(height: 24),
              const Text('Inspection Type', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 6),
              DropdownButtonFormField<String>(
                value: _inspectionType,
                decoration: const InputDecoration(border: OutlineInputBorder(), contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8)),
                items: const [
                  DropdownMenuItem(value: 'PRE_TRIP', child: Text('Pre-Trip Inspection')),
                  DropdownMenuItem(value: 'POST_TRIP', child: Text('Post-Trip Inspection')),
                  DropdownMenuItem(value: 'ROUTINE', child: Text('Routine Weekly Safety Check')),
                ],
                onChanged: (val) {
                  if (val != null) setState(() => _inspectionType = val);
                },
              ),
              const SizedBox(height: 16),
              const Text('Safety Checklist Items', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              ..._checklistItems.keys.map((itemKey) {
                final isPassed = _checklistItems[itemKey] ?? true;
                return SwitchListTile(
                  contentPadding: EdgeInsets.zero,
                  title: Text(itemKey, style: const TextStyle(fontSize: 14)),
                  value: isPassed,
                  activeColor: Colors.green,
                  inactiveThumbColor: Colors.red,
                  onChanged: (val) {
                    setState(() => _checklistItems[itemKey] = val);
                  },
                );
              }).toList(),
              const SizedBox(height: 12),
              TextField(
                controller: _notesController,
                maxLines: 2,
                decoration: const InputDecoration(
                  labelText: 'Inspector Notes / Defects Found',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton(
                    onPressed: () => Navigator.of(context).pop(),
                    child: const Text('Cancel'),
                  ),
                  const SizedBox(width: 8),
                  ElevatedButton(
                    onPressed: _submitInspection,
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.indigo),
                    child: const Text('Submit Inspection', style: TextStyle(color: Colors.white)),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
