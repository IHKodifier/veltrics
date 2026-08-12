import 'package:flutter/material.dart';
import '../../domain/organization_model.dart';
import '../../data/organization_repository.dart';

class OrganizationSwitcherWidget extends StatefulWidget {
  final OrganizationModel activeOrganization;
  final List<OrganizationModel> availableOrganizations;
  final String userId;
  final OrganizationRepository repository;
  final ValueChanged<OrganizationModel> onOrganizationChanged;

  const OrganizationSwitcherWidget({
    Key? key,
    required this.activeOrganization,
    required this.availableOrganizations,
    required this.userId,
    required this.repository,
    required this.onOrganizationChanged,
  }) : super(key: key);

  @override
  State<OrganizationSwitcherWidget> createState() => _OrganizationSwitcherWidgetState();
}

class _OrganizationSwitcherWidgetState extends State<OrganizationSwitcherWidget> {
  bool _isSwitching = false;

  Future<void> _handleSwitch(OrganizationModel targetOrg) async {
    if (targetOrg.id == widget.activeOrganization.id) {
      Navigator.of(context).pop();
      return;
    }

    setState(() {
      _isSwitching = true;
    });

    try {
      final updatedOrg = await widget.repository.switchOrganization(
        targetOrganizationId: targetOrg.id,
        userId: widget.userId,
      );

      if (mounted) {
        Navigator.of(context).pop();
        widget.onOrganizationChanged(updatedOrg);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Switched to ${updatedOrg.name}'),
            backgroundColor: Colors.teal.shade700,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to switch organization: $e'),
            backgroundColor: Colors.red.shade700,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSwitching = false;
        });
      }
    }
  }

  void _showSwitcherModal() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) {
        return Container(
          padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Select Organization Context',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close),
                    onPressed: () => Navigator.of(ctx).pop(),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Flexible(
                child: ListView.separated(
                  shrinkWrap: true,
                  itemCount: widget.availableOrganizations.length,
                  separatorBuilder: (_, __) => const Divider(),
                  itemBuilder: (context, index) {
                    final org = widget.availableOrganizations[index];
                    final isSelected = org.id == widget.activeOrganization.id;

                    return ListTile(
                      leading: CircleAvatar(
                        backgroundColor: isSelected
                            ? Theme.of(context).primaryColor
                            : Colors.grey.shade300,
                        child: Icon(
                          org.isPersonal ? Icons.person : Icons.business,
                          color: isSelected ? Colors.white : Colors.black87,
                        ),
                      ),
                      title: Text(
                        org.name,
                        style: TextStyle(
                          fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                        ),
                      ),
                      subtitle: Text(
                        org.isPersonal ? 'Personal Workspace' : 'Commercial Fleet',
                      ),
                      trailing: isSelected
                          ? const Icon(Icons.check_circle, color: Colors.teal)
                          : null,
                      onTap: _isSwitching ? null : () => _handleSwitch(org),
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: _showSwitcherModal,
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          border: Border.all(color: Colors.grey.shade300),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              widget.activeOrganization.isPersonal ? Icons.person : Icons.business,
              size: 18,
              color: Theme.of(context).primaryColor,
            ),
            const SizedBox(width: 8),
            Text(
              widget.activeOrganization.name,
              style: const TextStyle(
                fontWeight: FontWeight.w600,
                fontSize: 14,
              ),
            ),
            const SizedBox(width: 4),
            const Icon(
              Icons.arrow_drop_down,
              size: 20,
            ),
          ],
        ),
      ),
    );
  }
}
