import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import '../../../../theme/app_theme.dart';
import '../../../../core/utils/unit_converter.dart';

class SettingsController extends ChangeNotifier {
  ThemeMode _themeMode = ThemeMode.system;
  VeltricsPalette _palette = VeltricsPalette.teal;
  bool _highContrastMode = false;
  UnitSystem _unitSystem = UnitSystem.metric;
  Locale _locale = const Locale('en');

  ThemeMode get themeMode => _themeMode;
  VeltricsPalette get palette => _palette;
  bool get highContrastMode => _highContrastMode;
  UnitSystem get unitSystem => _unitSystem;
  Locale get locale => _locale;

  static const String _prefThemeKey = 'veltrics_pref_theme';
  static const String _prefPaletteKey = 'veltrics_pref_palette';
  static const String _prefContrastKey = 'veltrics_pref_contrast';
  static const String _prefUnitsKey = 'veltrics_pref_units';
  static const String _prefLocaleKey = 'veltrics_pref_locale';

  SettingsController() {
    loadPreferences();
  }

  Future<void> loadPreferences() async {
    final prefs = await SharedPreferences.getInstance();

    final themeStr = prefs.getString(_prefThemeKey) ?? 'SYSTEM';
    if (themeStr == 'LIGHT') {
      _themeMode = ThemeMode.light;
    } else if (themeStr == 'DARK') {
      _themeMode = ThemeMode.dark;
    } else {
      _themeMode = ThemeMode.system;
    }

    final paletteStr = prefs.getString(_prefPaletteKey) ?? 'teal';
    if (paletteStr == 'amber') {
      _palette = VeltricsPalette.amber;
    } else if (paletteStr == 'green') {
      _palette = VeltricsPalette.green;
    } else {
      _palette = VeltricsPalette.teal;
    }

    _highContrastMode = prefs.getBool(_prefContrastKey) ?? false;

    final unitsStr = prefs.getString(_prefUnitsKey) ?? 'METRIC';
    _unitSystem = unitsStr == 'IMPERIAL' ? UnitSystem.imperial : UnitSystem.metric;

    final localeStr = prefs.getString(_prefLocaleKey) ?? 'en';
    _locale = Locale(localeStr);

    notifyListeners();
  }

  Future<void> updatePreferences({
    ThemeMode? themeMode,
    VeltricsPalette? palette,
    bool? highContrastMode,
    UnitSystem? unitSystem,
    Locale? locale,
    String? baseUrl,
    String? token,
    String? userId,
  }) async {
    final prefs = await SharedPreferences.getInstance();

    if (themeMode != null) {
      _themeMode = themeMode;
      final val = themeMode == ThemeMode.light ? 'LIGHT' : (themeMode == ThemeMode.dark ? 'DARK' : 'SYSTEM');
      await prefs.setString(_prefThemeKey, val);
    }

    if (palette != null) {
      _palette = palette;
      final val = palette == VeltricsPalette.amber ? 'amber' : (palette == VeltricsPalette.green ? 'green' : 'teal');
      await prefs.setString(_prefPaletteKey, val);
    }

    if (highContrastMode != null) {
      _highContrastMode = highContrastMode;
      await prefs.setBool(_prefContrastKey, highContrastMode);
    }

    if (unitSystem != null) {
      _unitSystem = unitSystem;
      await prefs.setString(_prefUnitsKey, unitSystem == UnitSystem.imperial ? 'IMPERIAL' : 'METRIC');
    }

    if (locale != null) {
      _locale = locale;
      await prefs.setString(_prefLocaleKey, locale.languageCode);
    }

    notifyListeners();

    // Async sync with FastAPI backend if authenticated
    if (baseUrl != null && token != null && userId != null) {
      try {
        final themeStr = _themeMode == ThemeMode.light ? 'LIGHT' : (_themeMode == ThemeMode.dark ? 'DARK' : 'SYSTEM');
        final paletteStr = _palette == VeltricsPalette.amber ? 'amber_gold' : (_palette == VeltricsPalette.green ? 'forest_green' : 'slate_teal');
        final unitsStr = _unitSystem == UnitSystem.imperial ? 'IMPERIAL' : 'METRIC';

        await http.patch(
          Uri.parse('$baseUrl/api/v1/users/me/preferences'),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer $token',
            'X-User-ID': userId,
          },
          body: jsonEncode({
            'theme': themeStr,
            'accent_color': paletteStr,
            'high_contrast': _highContrastMode,
            'units': unitsStr,
            'locale': _locale.languageCode,
          }),
        );
      } catch (_) {
        // Fallback silently if offline; preference write failed -> client updates runtime theme state regardless
      }
    }
  }
}
