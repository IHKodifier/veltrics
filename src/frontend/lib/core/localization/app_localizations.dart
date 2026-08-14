import 'package:flutter/material.dart';

class AppLocalizations {
  final Locale locale;

  AppLocalizations(this.locale);

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations) ??
        AppLocalizations(const Locale('en'));
  }

  static bool isRtl(Locale locale) {
    return locale.languageCode == 'ur' || locale.languageCode == 'ar';
  }

  TextDirection get textDirection {
    return isRtl(locale) ? TextDirection.rtl : TextDirection.ltr;
  }

  static const _localizedValues = <String, Map<String, String>>{
    'en': {
      'app_title': 'Veltrics Fleet & Vehicle Management',
      'dashboard': 'Dashboard',
      'fleet': 'Fleet',
      'auth': 'Auth',
      'settings': 'Settings',
      'appearance': 'Appearance & Preferences',
      'theme': 'Theme Mode',
      'light_mode': 'Light',
      'dark_mode': 'Slate Teal Dark',
      'system_mode': 'System Default',
      'accent_color': 'Brand Accent Palette',
      'slate_teal': 'Slate Teal',
      'amber_gold': 'Amber Gold',
      'forest_green': 'Forest Green',
      'high_contrast': 'High-Contrast Accessibility Mode',
      'unit_system': 'Measurement Units',
      'metric': 'Metric (km, L, km/L)',
      'imperial': 'Imperial (miles, gal, MPG)',
      'language': 'App Language',
      'english': 'English',
      'urdu': 'Urdu (اردو)',
      'arabic': 'Arabic (العربية)',
      'save': 'Save Preferences',
      'saved_toast': 'Preferences updated successfully!',
      'kpi_total_vehicles': 'Total Fleet Vehicles',
      'kpi_active_drivers': 'Active Drivers',
      'kpi_monthly_fuel': 'Monthly Fuel Consumption',
      'recent_vehicles': 'Recent Vehicles',
      'odometer': 'Odometer Reading',
    },
    'ur': {
      'app_title': 'ویلٹرکس فلیٹ اور گاڑیوں کا انتظام',
      'dashboard': 'ڈیش بورڈ',
      'fleet': 'گاڑیاں',
      'auth': 'لاگ ان',
      'settings': 'ترتیبات',
      'appearance': 'ظاہری شکل و ترجیحات',
      'theme': 'تھیم کا موڈ',
      'light_mode': 'روشن تھیم',
      'dark_mode': 'سلیٹ ٹیل ڈارک تھیم',
      'system_mode': 'سسٹم سسٹم ڈیفالٹ',
      'accent_color': 'برانڈ کا رنگ',
      'slate_teal': 'سلیٹ ٹیل',
      'amber_gold': 'عنبر گولڈ',
      'forest_green': 'سیب کا سبز',
      'high_contrast': 'اعلی کنٹراسٹ متبادل موڈ',
      'unit_system': 'پیمائش کی اکائیاں',
      'metric': 'میٹرک (کلومیٹر، لیٹر)',
      'imperial': 'امپیریل (میل، گیلن)',
      'language': 'ایپ کی زبان',
      'english': 'English',
      'urdu': 'اردو',
      'arabic': 'العربية',
      'save': 'ترجیحات محفوظ کریں',
      'saved_toast': 'ترجیحات کامیابی کے ساتھ اپ ڈیٹ ہوگئیں!',
      'kpi_total_vehicles': 'کل فلیٹ گاڑیاں',
      'kpi_active_drivers': 'فعال ڈرائیور',
      'kpi_monthly_fuel': 'ماہانہ ایندھن کا استعمال',
      'recent_vehicles': 'حالیہ گاڑیاں',
      'odometer': 'اوڈومیٹر ریڈنگ',
    },
    'ar': {
      'app_title': 'فيلتركس لإدارة أسطول المركبات',
      'dashboard': 'لوحة القيادة',
      'fleet': 'الأسطول',
      'auth': 'تسجيل الدخول',
      'settings': 'الإعدادات',
      'appearance': 'المظهر والتفضيلات',
      'theme': 'وضع المظهر',
      'light_mode': 'فاتح',
      'dark_mode': 'داكن',
      'system_mode': 'افتراضي النظام',
      'accent_color': 'لون العرض الأساسي',
      'slate_teal': 'أزرق طاووسي',
      'amber_gold': 'ذهبي عنبري',
      'forest_green': 'أخضر غابي',
      'high_contrast': 'وضع التباين العالي accessibility',
      'unit_system': 'وحدات القياس',
      'metric': 'متري (كم، لتر)',
      'imperial': 'إمبراطوري (ميل، جالون)',
      'language': 'لغة التطبيق',
      'english': 'English',
      'urdu': 'Urdu (اردو)',
      'arabic': 'العربية',
      'save': 'حفظ التفضيلات',
      'saved_toast': 'تم تحديث التفضيلات بنجاح!',
      'kpi_total_vehicles': 'إجمالي مركبات الأسطول',
      'kpi_active_drivers': 'السائقين النشطين',
      'kpi_monthly_fuel': 'استهلاك الوقود الشهري',
      'recent_vehicles': 'المركبات الأخيرة',
      'odometer': 'قراءة العداد',
    },
  };

  String translate(String key) {
    final langMap = _localizedValues[locale.languageCode] ?? _localizedValues['en']!;
    return langMap[key] ?? _localizedValues['en']![key] ?? key;
  }
}

class AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) {
    return ['en', 'ur', 'ar'].contains(locale.languageCode);
  }

  @override
  Future<AppLocalizations> load(Locale locale) async {
    return AppLocalizations(locale);
  }

  @override
  bool shouldReload(AppLocalizationsDelegate old) => false;
}
