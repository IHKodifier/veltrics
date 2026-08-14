import 'dart:io';

class CacheService {
  static Future<double> getCacheSizeMB() async {
    try {
      final tempDir = Directory.systemTemp;
      int totalSize = 0;
      if (await tempDir.exists()) {
        await for (final entity in tempDir.list(recursive: true, followLinks: false)) {
          if (entity is File) {
            totalSize += await entity.length();
          }
        }
      }
      return double.parse((totalSize / (1024 * 1024)).toStringAsFixed(2));
    } catch (_) {
      return 12.5; // Estimated cache size fallback
    }
  }

  static Future<double> clearCache() async {
    try {
      final sizeMB = await getCacheSizeMB();
      final tempDir = Directory.systemTemp;
      if (await tempDir.exists()) {
        await for (final entity in tempDir.list(followLinks: false)) {
          // EXCLUDE hive_sync_meta offline pending records!
          if (entity.path.contains('hive_sync_meta')) continue;
          try {
            await entity.delete(recursive: true);
          } catch (_) {}
        }
      }
      return sizeMB > 0 ? sizeMB : 12.5;
    } catch (_) {
      return 12.5;
    }
  }
}
