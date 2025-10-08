[app]
title = Parking Register
package.name = parking_register
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
icon.filename = %(source.dir)s/my_ico.png
presplash.filename = %(source.dir)s/my_ico.png
version = 0.1.1
requirements = python3,kivy,sqlite3,pyjnius,kivymd,pillow
orientation = landscape
fullscreen = 0
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Android API levels
android.api = 35
android.minapi = 21
android.ndk_api = 21

# Skip these for now
# android.gradle_dependencies =

# Force Gradle versions
android.gradle_version = 8.7
android.gradle_plugin_version = 8.5.2
android.gradle_distribution_url = https://services.gradle.org/distributions/gradle-8.7-bin.zip

[buildozer]

# Force Gradle versions
android.gradle_version = 8.7
android.gradle_plugin_version = 8.5.2
android.gradle_distribution_url = https://services.gradle.org/distributions/gradle-8.7-bin.zip

log_level = 2
warn_on_root = 1

# This tells buildozer where to store cache
# buildozer_dir = /home/user/.buildozer  # REMOVE THIS LINE - it causes issues



# SDK settings
android.skip_update = False
android.accept_sdk_license = True