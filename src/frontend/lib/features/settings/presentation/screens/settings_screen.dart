import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../../../theme/app_theme.dart';
import '../../../../core/localization/app_localizations.dart';
import '../../../../core/utils/unit_converter.dart';
import '../../../../core/services/cache_service.dart';
import '../controllers/settings_controller.dart';
import '../widgets/support_ticket_dialog.dart';
import '../widgets/account_deletion_dialog.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final settings = Provider.of<SettingsController>(context);
    final loc = AppLocalizations.of(context);
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Directionality(
      textDirection: loc.textDirection,
      child: Scaffold(
        appBar: AppBar(
          title: Text(loc.translate('settings')),
        ),
        body: ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            // =================================================================
            // 1. APPEARANCE & THEME (UC-107, UC-108, UC-109)
            // =================================================================
            _buildSectionHeader(context, loc.translate('appearance'), Icons.palette_outlined),
            const SizedBox(height: 12),
            Card(
              elevation: 0,
              color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(
                  color: settings.highContrastMode
                      ? (isDark ? Colors.white : Colors.black)
                      : (isDark ? const Color(0xFF333333) : const Color(0xFFE2E8F0)),
                  width: settings.highContrastMode ? 2.5 : 1.0,
                ),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      loc.translate('theme'),
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: settings.highContrastMode ? FontWeight.w700 : FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 8),
                    SegmentedButton<ThemeMode>(
                      segments: [
                        ButtonSegment(
                          value: ThemeMode.light,
                          label: Text(loc.translate('light_mode')),
                          icon: const Icon(Icons.wb_sunny_outlined),
                        ),
                        ButtonSegment(
                          value: ThemeMode.dark,
                          label: Text(loc.translate('dark_mode')),
                          icon: const Icon(Icons.nightlight_round_outlined),
                        ),
                        ButtonSegment(
                          value: ThemeMode.system,
                          label: Text(loc.translate('system_mode')),
                          icon: const Icon(Icons.settings_suggest_outlined),
                        ),
                      ],
                      selected: {settings.themeMode},
                      onSelectionChanged: (Set<ThemeMode> selection) {
                        settings.updatePreferences(themeMode: selection.first);
                      },
                    ),
                    const Divider(height: 24),

                    // ACCENT COLOR PICKER (UC-108)
                    Text(
                      loc.translate('accent_color'),
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: settings.highContrastMode ? FontWeight.w700 : FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        _buildColorChip(
                          context,
                          label: loc.translate('slate_teal'),
                          color: const Color(0xFF0F766E),
                          selected: settings.palette == VeltricsPalette.teal,
                          onTap: () => settings.updatePreferences(palette: VeltricsPalette.teal),
                        ),
                        const SizedBox(width: 8),
                        _buildColorChip(
                          context,
                          label: loc.translate('amber_gold'),
                          color: const Color(0xFFD97706),
                          selected: settings.palette == VeltricsPalette.amber,
                          onTap: () => settings.updatePreferences(palette: VeltricsPalette.amber),
                        ),
                        const SizedBox(width: 8),
                        _buildColorChip(
                          context,
                          label: loc.translate('forest_green'),
                          color: const Color(0xFF15803D),
                          selected: settings.palette == VeltricsPalette.green,
                          onTap: () => settings.updatePreferences(palette: VeltricsPalette.green),
                        ),
                      ],
                    ),
                    const Divider(height: 24),

                    // HIGH CONTRAST (UC-109)
                    SwitchListTile(
                      contentPadding: EdgeInsets.zero,
                      title: Text(
                        loc.translate('high_contrast'),
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight: settings.highContrastMode ? FontWeight.w700 : FontWeight.w500,
                        ),
                      ),
                      value: settings.highContrastMode,
                      onChanged: (bool val) {
                        settings.updatePreferences(highContrastMode: val);
                      },
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // =================================================================
            // 2. REGIONAL MEASUREMENT UNITS (UC-114)
            // =================================================================
            _buildSectionHeader(context, loc.translate('unit_system'), Icons.straighten_outlined),
            const SizedBox(height: 12),
            Card(
              elevation: 0,
              color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(
                  color: settings.highContrastMode
                      ? (isDark ? Colors.white : Colors.black)
                      : (isDark ? const Color(0xFF333333) : const Color(0xFFE2E8F0)),
                  width: settings.highContrastMode ? 2.5 : 1.0,
                ),
              ),
              child: Column(
                children: [
                  RadioListTile<UnitSystem>(
                    title: Text(loc.translate('metric')),
                    subtitle: const Text('Odometer: km | Fuel: L | Efficiency: km/L'),
                    value: UnitSystem.metric,
                    groupValue: settings.unitSystem,
                    onChanged: (val) {
                      if (val != null) settings.updatePreferences(unitSystem: val);
                    },
                  ),
                  const Divider(height: 1),
                  RadioListTile<UnitSystem>(
                    title: Text(loc.translate('imperial')),
                    subtitle: const Text('Odometer: miles | Fuel: gallons | Efficiency: MPG'),
                    value: UnitSystem.imperial,
                    groupValue: settings.unitSystem,
                    onChanged: (val) {
                      if (val != null) settings.updatePreferences(unitSystem: val);
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // =================================================================
            // 3. APP LANGUAGE & LOCALIZATION (UC-115)
            // =================================================================
            _buildSectionHeader(context, loc.translate('language'), Icons.language_outlined),
            const SizedBox(height: 12),
            Card(
              elevation: 0,
              color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(
                  color: settings.highContrastMode
                      ? (isDark ? Colors.white : Colors.black)
                      : (isDark ? const Color(0xFF333333) : const Color(0xFFE2E8F0)),
                  width: settings.highContrastMode ? 2.5 : 1.0,
                ),
              ),
              child: Column(
                children: [
                  RadioListTile<String>(
                    title: Text(loc.translate('english')),
                    value: 'en',
                    groupValue: settings.locale.languageCode,
                    onChanged: (code) {
                      if (code != null) settings.updatePreferences(locale: Locale(code));
                    },
                  ),
                  const Divider(height: 1),
                  RadioListTile<String>(
                    title: Text(loc.translate('urdu')),
                    subtitle: const Text('Right-to-Left (RTL) Layout'),
                    value: 'ur',
                    groupValue: settings.locale.languageCode,
                    onChanged: (code) {
                      if (code != null) settings.updatePreferences(locale: Locale(code));
                    },
                  ),
                  const Divider(height: 1),
                  RadioListTile<String>(
                    title: Text(loc.translate('arabic')),
                    subtitle: const Text('Right-to-Left (RTL) Layout'),
                    value: 'ar',
                    groupValue: settings.locale.languageCode,
                    onChanged: (code) {
                      if (code != null) settings.updatePreferences(locale: Locale(code));
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // =================================================================
            // 4. DATA PRIVACY & STORAGE CACHE (UC-116)
            // =================================================================
            _buildSectionHeader(context, 'Data Privacy & Storage', Icons.security_outlined),
            const SizedBox(height: 12),
            Card(
              elevation: 0,
              color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(
                  color: settings.highContrastMode
                      ? (isDark ? Colors.white : Colors.black)
                      : (isDark ? const Color(0xFF333333) : const Color(0xFFE2E8F0)),
                  width: settings.highContrastMode ? 2.5 : 1.0,
                ),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.cleaning_services_outlined, color: Color(0xFF0F766E)),
                    title: const Text('Clear Temporary Cache'),
                    subtitle: const Text('Purges temporary image & network caches (preserves offline logs)'),
                    onTap: () async {
                      final size = await CacheService.clearCache();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('Cleared $size MB of temporary cache.'),
                            backgroundColor: const Color(0xFF0F766E),
                          ),
                        );
                      }
                    },
                  ),
                  const Divider(height: 1),
                  ListTile(
                    leading: const Icon(Icons.delete_forever_outlined, color: Colors.red),
                    title: const Text('Request Account & Data Deletion', style: TextStyle(color: Colors.red)),
                    subtitle: const Text('GDPR Right to be Forgotten — Anonymizes all account PII'),
                    onTap: () {
                      showDialog(
                        context: context,
                        builder: (_) => const AccountDeletionDialog(),
                      );
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // =================================================================
            // 5. HELP & SUPPORT (UC-117)
            // =================================================================
            _buildSectionHeader(context, 'Help & Support', Icons.help_outline),
            const SizedBox(height: 12),
            Card(
              elevation: 0,
              color: isDark ? const Color(0xFF1E1E1E) : Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(
                  color: settings.highContrastMode
                      ? (isDark ? Colors.white : Colors.black)
                      : (isDark ? const Color(0xFF333333) : const Color(0xFFE2E8F0)),
                  width: settings.highContrastMode ? 2.5 : 1.0,
                ),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.headset_mic_outlined, color: Color(0xFF0F766E)),
                    title: const Text('Submit Support Ticket'),
                    subtitle: const Text('Contact Veltrics Helpdesk or submit feedback'),
                    onTap: () {
                      showDialog(
                        context: context,
                        builder: (_) => const SupportTicketDialog(),
                      );
                    },
                  ),
                  const Divider(height: 1),
                  const ListTile(
                    leading: Icon(Icons.info_outline, color: Color(0xFF0F766E)),
                    title: Text('Veltrics Platform Version'),
                    subtitle: Text('v1.0.0+1 (Sprint 06 Release) • Terms of Service & Privacy Policy'),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Theme.of(context).colorScheme.primary),
        const SizedBox(width: 8),
        Text(
          title,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Theme.of(context).colorScheme.primary,
          ),
        ),
      ],
    );
  }

  Widget _buildColorChip(
    BuildContext context, {
    required String label,
    required Color color,
    required bool selected,
    required VoidCallback onTap,
  }) {
    return Expanded(
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(8),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: color.withValues(alpha: selected ? 0.15 : 0.05),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: selected ? color : Colors.transparent,
              width: 2,
            ),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Container(
                width: 12,
                height: 12,
                decoration: BoxDecoration(color: color, shape: BoxShape.circle),
              ),
              const SizedBox(width: 6),
              Flexible(
                child: Text(
                  label,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: selected ? FontWeight.bold : FontWeight.normal,
                    color: selected ? color : Theme.of(context).colorScheme.onSurface,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
