[app]
title = FruitCounter
package.name = fruitcounter
package.domain = org.fruitcounter
source.dir = app
source.include_exts = py,png,jpg,kv,tflite,txt
version = 1.0.0
orientation = portrait
requirements = python3,kivy,numpy,Pillow,tensorflow
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
