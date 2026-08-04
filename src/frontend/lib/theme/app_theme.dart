// =============================================================================
// app_theme.dart
// Veltrics Design System & Theme Engine
// Source: product-specs/05b-flutter-theme.dart
// =============================================================================

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

enum VeltricsPalette { teal, amber, green }

class VeltricsPaletteSet {
  const VeltricsPaletteSet({
    required this.shade50,
    required this.shade100,
    required this.shade200,
    required this.shade300,
    required this.shade400,
    required this.shade500,
    required this.shade600,
    required this.shade700,
    required this.shade800,
    required this.shade900,
    required this.secondary500,
    required this.secondary600,
    required this.darkPrimary,
    required this.darkPrimaryHover,
    required this.onPrimary,
    required this.darkSurface1,
    required this.darkSurface2,
    required this.darkSurface3,
    required this.onSurfaceDark,
    required this.onSurfaceMutedDark,
  });

  final Color shade50;
  final Color shade100;
  final Color shade200;
  final Color shade300;
  final Color shade400;
  final Color shade500;
  final Color shade600;
  final Color shade700;
  final Color shade800;
  final Color shade900;
  final Color secondary500;
  final Color secondary600;

  final Color darkPrimary;
  final Color darkPrimaryHover;
  final Color onPrimary;

  final Color darkSurface1;
  final Color darkSurface2;
  final Color darkSurface3;
  final Color onSurfaceDark;
  final Color onSurfaceMutedDark;
}

class VeltricsColors {
  VeltricsColors._();

  static const VeltricsPaletteSet _teal = VeltricsPaletteSet(
    shade50: Color(0xFFF0FDFA),
    shade100: Color(0xFFCCFBF1),
    shade200: Color(0xFF99F6E4),
    shade300: Color(0xFF5EEAD4),
    shade400: Color(0xFF2DD4BF),
    shade500: Color(0xFF14B8A6),
    shade600: Color(0xFF0D9488),
    shade700: Color(0xFF0F766E),
    shade800: Color(0xFF115E59),
    shade900: Color(0xFF134E4A),
    secondary500: Color(0xFF06B6D4),
    secondary600: Color(0xFF0891B2),
    darkPrimary: Color(0xFF2DD4BF),
    darkPrimaryHover: Color(0xFF14B8A6),
    onPrimary: Color(0xFF042F2E),
    darkSurface1: Color(0xFF1E1E1E),
    darkSurface2: Color(0xFF2A2A2A),
    darkSurface3: Color(0xFF333333),
    onSurfaceDark: Color(0xFFE2E8F0),
    onSurfaceMutedDark: Color(0xFF94A3B8),
  );

  static const VeltricsPaletteSet _amber = VeltricsPaletteSet(
    shade50: Color(0xFFFFFBEB),
    shade100: Color(0xFFFEF3C7),
    shade200: Color(0xFFFDE68A),
    shade300: Color(0xFFFCD34D),
    shade400: Color(0xFFFBBF24),
    shade500: Color(0xFFF59E0B),
    shade600: Color(0xFFD97706),
    shade700: Color(0xFFB45309),
    shade800: Color(0xFF92400E),
    shade900: Color(0xFF78350F),
    secondary500: Color(0xFFF97316),
    secondary600: Color(0xFFEA580C),
    darkPrimary: Color(0xFFFBBF24),
    darkPrimaryHover: Color(0xFFF59E0B),
    onPrimary: Color(0xFF1C0A00),
    darkSurface1: Color(0xFF1C1A16),
    darkSurface2: Color(0xFF27231C),
    darkSurface3: Color(0xFF38321F),
    onSurfaceDark: Color(0xFFF1EDE5),
    onSurfaceMutedDark: Color(0xFFA8A097),
  );

  static const VeltricsPaletteSet _green = VeltricsPaletteSet(
    shade50: Color(0xFFF0FDF4),
    shade100: Color(0xFFDCFCE7),
    shade200: Color(0xFFBBF7D0),
    shade300: Color(0xFF86EFAC),
    shade400: Color(0xFF4ADE80),
    shade500: Color(0xFF22C55E),
    shade600: Color(0xFF16A34A),
    shade700: Color(0xFF15803D),
    shade800: Color(0xFF166534),
    shade900: Color(0xFF14532D),
    secondary500: Color(0xFF059669),
    secondary600: Color(0xFF047857),
    darkPrimary: Color(0xFF4ADE80),
    darkPrimaryHover: Color(0xFF22C55E),
    onPrimary: Color(0xFF052E16),
    darkSurface1: Color(0xFF151A17),
    darkSurface2: Color(0xFF1E2720),
    darkSurface3: Color(0xFF2D3A31),
    onSurfaceDark: Color(0xFFE8F5EC),
    onSurfaceMutedDark: Color(0xFF8FA897),
  );

  static VeltricsPaletteSet of(VeltricsPalette palette) {
    switch (palette) {
      case VeltricsPalette.teal:
        return _teal;
      case VeltricsPalette.amber:
        return _amber;
      case VeltricsPalette.green:
        return _green;
    }
  }

  static const Color successLight = Color(0xFF16A34A);
  static const Color successBgLight = Color(0xFFDCFCE7);
  static const Color warningLight = Color(0xFFCA8A04);
  static const Color warningBgLight = Color(0xFFFEF9C3);
  static const Color errorLight = Color(0xFFDC2626);
  static const Color errorBgLight = Color(0xFFFEE2E2);
  static const Color infoLight = Color(0xFF2563EB);
  static const Color infoBgLight = Color(0xFFDBEAFE);

  static const Color successDark = Color(0xFF4ADE80);
  static const Color successBgDark = Color(0xFF14532D);
  static const Color warningDark = Color(0xFFFACC15);
  static const Color warningBgDark = Color(0xFF3F2E00);
  static const Color errorDark = Color(0xFFF87171);
  static const Color errorBgDark = Color(0xFF3F0000);
  static const Color infoDark = Color(0xFF60A5FA);
  static const Color infoBgDark = Color(0xFF1E3A8A);

  static const Color proBadgeLight = Color(0xFF7C3AED);
  static const Color proBadgeDark = Color(0xFFA78BFA);
  static const Color adBadgeLight = Color(0xFFB45309);
  static const Color adBadgeDark = Color(0xFFFBBF24);

  static const Color neutral50 = Color(0xFFF8FAFC);
  static const Color neutral100 = Color(0xFFF1F5F9);
  static const Color neutral200 = Color(0xFFE2E8F0);
  static const Color neutral300 = Color(0xFFCBD5E1);
  static const Color neutral400 = Color(0xFF94A3B8);
  static const Color neutral500 = Color(0xFF64748B);
  static const Color neutral600 = Color(0xFF475569);
  static const Color neutral700 = Color(0xFF334155);
  static const Color neutral800 = Color(0xFF1E293B);
  static const Color neutral900 = Color(0xFF0F172A);

  static const Color neutralD50 = Color(0xFF1E1E1E);
  static const Color neutralD100 = Color(0xFF27272A);
  static const Color neutralD200 = Color(0xFF3F3F46);
  static const Color neutralD300 = Color(0xFF52525B);
  static const Color neutralD400 = Color(0xFF71717A);
  static const Color neutralD500 = Color(0xFFA1A1AA);
  static const Color neutralD600 = Color(0xFFD4D4D8);
  static const Color neutralD700 = Color(0xFFE4E4E7);
  static const Color neutralD800 = Color(0xFFF4F4F5);
  static const Color neutralD900 = Color(0xFFFAFAFA);

  static const Color surfaceBgLight = Color(0xFFF8FAFC);
  static const Color surfaceCardLight = Color(0xFFFFFFFF);
  static const Color surfaceBgDark = Color(0xFF121212);
}

class VeltricsTextStyles {
  VeltricsTextStyles._();

  static TextStyle _inter({
    required double fontSize,
    required FontWeight fontWeight,
    required double height,
    Color? color,
    double? letterSpacing,
  }) =>
      GoogleFonts.inter(
        fontSize: fontSize,
        fontWeight: fontWeight,
        height: height,
        color: color,
        letterSpacing: letterSpacing,
      );

  static TextStyle get displayXl => _inter(fontSize: 36, fontWeight: FontWeight.w800, height: 1.2);
  static TextStyle get displayLg => _inter(fontSize: 30, fontWeight: FontWeight.w700, height: 1.25);
  static TextStyle get displayMd => _inter(fontSize: 24, fontWeight: FontWeight.w700, height: 1.3);
  static TextStyle get titleLg => _inter(fontSize: 20, fontWeight: FontWeight.w600, height: 1.35);
  static TextStyle get titleMd => _inter(fontSize: 18, fontWeight: FontWeight.w600, height: 1.4);
  static TextStyle get titleSm => _inter(fontSize: 16, fontWeight: FontWeight.w600, height: 1.4);
  static TextStyle get bodyLg => _inter(fontSize: 16, fontWeight: FontWeight.w400, height: 1.6);
  static TextStyle get bodyMd => _inter(fontSize: 14, fontWeight: FontWeight.w400, height: 1.6);
  static TextStyle get bodySm => _inter(fontSize: 12, fontWeight: FontWeight.w400, height: 1.5);
  static TextStyle get labelLg => _inter(fontSize: 14, fontWeight: FontWeight.w500, height: 1.2);
  static TextStyle get labelMd => _inter(fontSize: 12, fontWeight: FontWeight.w500, height: 1.2);
  static TextStyle get labelSm => _inter(fontSize: 10, fontWeight: FontWeight.w600, height: 1.2, letterSpacing: 0.08);

  static const TextStyle mono = TextStyle(
    fontFamily: 'RobotoMono',
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.5,
    fontFeatures: [FontFeature.tabularFigures()],
  );

  static TextStyle get dashboardMetric => displayXl.copyWith(
        fontFeatures: const [FontFeature.tabularFigures()],
      );

  static TextTheme buildTextTheme({Color? bodyColor, Color? displayColor}) {
    return GoogleFonts.interTextTheme(TextTheme(
      displayLarge: displayXl.copyWith(color: displayColor),
      displayMedium: displayLg.copyWith(color: displayColor),
      displaySmall: displayMd.copyWith(color: displayColor),
      headlineLarge: titleLg.copyWith(color: displayColor),
      headlineMedium: titleMd.copyWith(color: displayColor),
      headlineSmall: titleSm.copyWith(color: displayColor),
      titleLarge: titleLg.copyWith(color: bodyColor),
      titleMedium: titleMd.copyWith(color: bodyColor),
      titleSmall: titleSm.copyWith(color: bodyColor),
      bodyLarge: bodyLg.copyWith(color: bodyColor),
      bodyMedium: bodyMd.copyWith(color: bodyColor),
      bodySmall: bodySm.copyWith(color: bodyColor),
      labelLarge: labelLg.copyWith(color: bodyColor),
      labelMedium: labelMd.copyWith(color: bodyColor),
      labelSmall: labelSm.copyWith(color: bodyColor),
    ));
  }
}

class VeltricsSpacing {
  VeltricsSpacing._();

  static const double xs1 = 4.0;
  static const double xs2 = 8.0;
  static const double xs3 = 12.0;
  static const double sm = 16.0;
  static const double sm5 = 20.0;
  static const double md = 24.0;
  static const double lg = 32.0;
  static const double xl = 40.0;
  static const double xl2 = 48.0;
  static const double xxl = 64.0;

  static const EdgeInsets cardPaddingMobile = EdgeInsets.all(sm);
  static const EdgeInsets cardPaddingWeb = EdgeInsets.all(md);
  static const EdgeInsets pagePadding = EdgeInsets.symmetric(horizontal: sm);
  static const EdgeInsets listItemPadding = EdgeInsets.symmetric(horizontal: sm, vertical: xs3);
}

class VeltricsRadius {
  VeltricsRadius._();

  static const double sm = 6.0;
  static const double md = 10.0;
  static const double lg = 16.0;
  static const double xl = 24.0;
  static const double full = 999.0;

  static BorderRadius get smAll => BorderRadius.circular(sm);
  static BorderRadius get mdAll => BorderRadius.circular(md);
  static BorderRadius get lgAll => BorderRadius.circular(lg);
  static BorderRadius get xlAll => BorderRadius.circular(xl);
  static BorderRadius get pillAll => BorderRadius.circular(full);
}

class VeltricsMotion {
  VeltricsMotion._();

  static const Duration fast = Duration(milliseconds: 100);
  static const Duration normal = Duration(milliseconds: 200);
  static const Duration slow = Duration(milliseconds: 350);
  static const Duration deliberate = Duration(milliseconds: 500);

  static const Curve standard = Curves.easeInOut;
  static const Curve emphasized = Cubic(0.4, 0.0, 0.2, 1.0);
  static const Curve spring = Cubic(0.34, 1.56, 0.64, 1.0);
  static const Curve decelerate = Curves.decelerate;
}

class VeltricsStatusColors {
  VeltricsStatusColors._();

  static Color successBg(bool isDark) => isDark ? const Color(0xFF14532D) : const Color(0xFFDCFCE7);
  static Color successFg(bool isDark) => isDark ? const Color(0xFF4ADE80) : const Color(0xFF166534);
  static Color warningBg(bool isDark) => isDark ? const Color(0xFF3F2E00) : const Color(0xFFFEF9C3);
  static Color warningFg(bool isDark) => isDark ? const Color(0xFFFACC15) : const Color(0xFFCA8A04);
  static Color errorBg(bool isDark) => isDark ? const Color(0xFF3F0000) : const Color(0xFFFEE2E2);
  static Color errorFg(bool isDark) => isDark ? const Color(0xFFF87171) : const Color(0xFFDC2626);
  static Color infoBg(bool isDark) => isDark ? const Color(0xFF1E3A8A) : const Color(0xFFDBEAFE);
  static Color infoFg(bool isDark) => isDark ? const Color(0xFF60A5FA) : const Color(0xFF2563EB);
  static Color proBg(bool isDark) => isDark ? const Color(0xFF2E1065) : const Color(0xFFEDE9FE);
  static Color proFg(bool isDark) => isDark ? const Color(0xFFA78BFA) : const Color(0xFF7C3AED);
  static Color adBg(bool isDark) => isDark ? const Color(0xFF3F2000) : const Color(0xFFFEF3C7);
  static Color adFg(bool isDark) => isDark ? const Color(0xFFFBBF24) : const Color(0xFFB45309);
}

class VeltricsTheme {
  VeltricsTheme._();

  static ThemeData light(VeltricsPalette palette) {
    final p = VeltricsColors.of(palette);
    final cs = _lightColorScheme(p);
    return _buildTheme(colorScheme: cs, palette: p, isDark: false);
  }

  static ThemeData dark(VeltricsPalette palette) {
    final p = VeltricsColors.of(palette);
    final cs = _darkColorScheme(p);
    return _buildTheme(colorScheme: cs, palette: p, isDark: true);
  }

  static ColorScheme _lightColorScheme(VeltricsPaletteSet p) => ColorScheme(
        brightness: Brightness.light,
        primary: p.shade500,
        onPrimary: p.onPrimary,
        primaryContainer: p.shade100,
        onPrimaryContainer: p.shade800,
        secondary: p.secondary500,
        onSecondary: Colors.white,
        secondaryContainer: p.shade100,
        onSecondaryContainer: p.shade700,
        tertiary: VeltricsColors.proBadgeLight,
        onTertiary: Colors.white,
        tertiaryContainer: const Color(0xFFEDE9FE),
        onTertiaryContainer: const Color(0xFF4C1D95),
        error: VeltricsColors.errorLight,
        onError: Colors.white,
        errorContainer: VeltricsColors.errorBgLight,
        onErrorContainer: const Color(0xFF7F1D1D),
        surface: VeltricsColors.surfaceCardLight,
        onSurface: VeltricsColors.neutral800,
        surfaceContainerHighest: VeltricsColors.neutral100,
        surfaceContainerHigh: VeltricsColors.neutral50,
        surfaceContainer: VeltricsColors.neutral50,
        surfaceContainerLow: Colors.white,
        surfaceContainerLowest: Colors.white,
        onSurfaceVariant: VeltricsColors.neutral500,
        outline: VeltricsColors.neutral300,
        outlineVariant: VeltricsColors.neutral200,
        inverseSurface: VeltricsColors.neutral900,
        onInverseSurface: VeltricsColors.neutral50,
        inversePrimary: p.shade300,
        scrim: Colors.black,
        shadow: Colors.black,
      );

  static ColorScheme _darkColorScheme(VeltricsPaletteSet p) => ColorScheme(
        brightness: Brightness.dark,
        primary: p.darkPrimary,
        onPrimary: p.onPrimary,
        primaryContainer: p.shade800,
        onPrimaryContainer: p.shade200,
        secondary: p.secondary500,
        onSecondary: p.onPrimary,
        secondaryContainer: p.shade800,
        onSecondaryContainer: p.shade100,
        tertiary: VeltricsColors.proBadgeDark,
        onTertiary: const Color(0xFF1A0050),
        tertiaryContainer: const Color(0xFF2E1065),
        onTertiaryContainer: const Color(0xFFEDE9FE),
        error: VeltricsColors.errorDark,
        onError: const Color(0xFF450A0A),
        errorContainer: VeltricsColors.errorBgDark,
        onErrorContainer: const Color(0xFFFECACA),
        surface: p.darkSurface1,
        onSurface: p.onSurfaceDark,
        surfaceContainerHighest: p.darkSurface3,
        surfaceContainerHigh: p.darkSurface2,
        surfaceContainer: p.darkSurface1,
        surfaceContainerLow: VeltricsColors.surfaceBgDark,
        surfaceContainerLowest: VeltricsColors.surfaceBgDark,
        onSurfaceVariant: p.onSurfaceMutedDark,
        outline: VeltricsColors.neutralD300,
        outlineVariant: VeltricsColors.neutralD200,
        inverseSurface: VeltricsColors.neutral100,
        onInverseSurface: VeltricsColors.neutral900,
        inversePrimary: p.shade600,
        scrim: Colors.black,
        shadow: Colors.black,
      );

  static ThemeData _buildTheme({
    required ColorScheme colorScheme,
    required VeltricsPaletteSet palette,
    required bool isDark,
  }) {
    final primary = colorScheme.primary;
    final onPrimary = colorScheme.onPrimary;
    final onSurface = colorScheme.onSurface;

    final bodyColor = isDark ? palette.onSurfaceDark : VeltricsColors.neutral700;
    final displayColor = isDark ? palette.onSurfaceDark : VeltricsColors.neutral800;
    final textTheme = VeltricsTextStyles.buildTextTheme(bodyColor: bodyColor, displayColor: displayColor);

    return ThemeData(
      useMaterial3: true,
      brightness: isDark ? Brightness.dark : Brightness.light,
      colorScheme: colorScheme,
      textTheme: textTheme,
      primaryTextTheme: textTheme,
      scaffoldBackgroundColor: isDark ? VeltricsColors.surfaceBgDark : VeltricsColors.surfaceBgLight,
      appBarTheme: AppBarTheme(
        backgroundColor: isDark ? palette.darkSurface1 : VeltricsColors.surfaceCardLight,
        foregroundColor: onSurface,
        elevation: 0,
        scrolledUnderElevation: 1,
        shadowColor: Colors.black12,
        titleTextStyle: VeltricsTextStyles.titleLg.copyWith(color: onSurface),
        iconTheme: IconThemeData(color: onSurface, size: 24),
        actionsIconTheme: IconThemeData(color: onSurface, size: 24),
        centerTitle: false,
        toolbarHeight: 56,
        surfaceTintColor: Colors.transparent,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ButtonStyle(
          backgroundColor: WidgetStateProperty.resolveWith((s) {
            if (s.contains(WidgetState.disabled)) return isDark ? VeltricsColors.neutralD200 : VeltricsColors.neutral200;
            if (s.contains(WidgetState.pressed)) return palette.shade700;
            if (s.contains(WidgetState.hovered)) return palette.shade600;
            return primary;
          }),
          foregroundColor: WidgetStateProperty.resolveWith((s) {
            if (s.contains(WidgetState.disabled)) return isDark ? VeltricsColors.neutralD400 : VeltricsColors.neutral400;
            return onPrimary;
          }),
          elevation: WidgetStateProperty.resolveWith((s) => s.contains(WidgetState.pressed) ? 0 : 2),
          minimumSize: WidgetStateProperty.all(const Size(64, 48)),
          padding: WidgetStateProperty.all(const EdgeInsets.symmetric(horizontal: 24, vertical: 14)),
          shape: WidgetStateProperty.all(RoundedRectangleBorder(borderRadius: VeltricsRadius.pillAll)),
          textStyle: WidgetStateProperty.all(VeltricsTextStyles.labelLg),
          animationDuration: VeltricsMotion.fast,
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: ButtonStyle(
          foregroundColor: WidgetStateProperty.resolveWith((s) {
            if (s.contains(WidgetState.disabled)) return isDark ? VeltricsColors.neutralD400 : VeltricsColors.neutral400;
            return primary;
          }),
          backgroundColor: WidgetStateProperty.resolveWith((s) {
            if (s.contains(WidgetState.pressed)) return palette.shade100;
            if (s.contains(WidgetState.hovered)) return palette.shade50;
            return Colors.transparent;
          }),
          side: WidgetStateProperty.resolveWith((s) => BorderSide(
                color: s.contains(WidgetState.disabled) ? (isDark ? VeltricsColors.neutralD300 : VeltricsColors.neutral300) : primary,
                width: 1.5,
              )),
          minimumSize: WidgetStateProperty.all(const Size(64, 48)),
          padding: WidgetStateProperty.all(const EdgeInsets.symmetric(horizontal: 24, vertical: 14)),
          shape: WidgetStateProperty.all(RoundedRectangleBorder(borderRadius: VeltricsRadius.pillAll)),
          textStyle: WidgetStateProperty.all(VeltricsTextStyles.labelLg),
          animationDuration: VeltricsMotion.fast,
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: isDark ? palette.darkSurface2 : Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: VeltricsRadius.smAll,
          borderSide: BorderSide(color: isDark ? VeltricsColors.neutralD300 : VeltricsColors.neutral300, width: 1.5),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: VeltricsRadius.smAll,
          borderSide: BorderSide(color: isDark ? VeltricsColors.neutralD300 : VeltricsColors.neutral300, width: 1.5),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: VeltricsRadius.smAll,
          borderSide: BorderSide(color: primary, width: 2),
        ),
      ),
    );
  }
}

class VeltricsStatusPill extends StatelessWidget {
  const VeltricsStatusPill._({
    required this.text,
    required this.backgroundColor,
    required this.textColor,
    this.icon,
  });

  factory VeltricsStatusPill.healthy({bool isDark = false}) =>
      VeltricsStatusPill._(text: 'HEALTHY', backgroundColor: VeltricsStatusColors.successBg(isDark), textColor: VeltricsStatusColors.successFg(isDark), icon: Icons.check_circle_outline);
  factory VeltricsStatusPill.proBadge({bool isDark = false}) =>
      VeltricsStatusPill._(text: 'PRO', backgroundColor: VeltricsStatusColors.proBg(isDark), textColor: VeltricsStatusColors.proFg(isDark), icon: Icons.star_outline);

  final String text;
  final Color backgroundColor, textColor;
  final IconData? icon;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(color: backgroundColor, borderRadius: VeltricsRadius.pillAll),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        if (icon != null) ...[Icon(icon, size: 12, color: textColor), const SizedBox(width: 4)],
        Text(text.toUpperCase(), style: VeltricsTextStyles.labelSm.copyWith(color: textColor)),
      ]),
    );
  }
}
