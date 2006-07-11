--- setup.py.old	2006-07-11 12:47:57.000000000 +0100
+++ setup.py	2006-07-11 12:48:21.000000000 +0100
@@ -118,6 +118,7 @@
       ext_modules = [Extension('core.plugins._gl1renderer',
                                ['core/plugins/_gl1renderer.c'],
                                include_dirs=find_includes(),
+                               library_dirs=['/usr/X11R6/lib'],
                                libraries=find_libraries()+packages)],
       packages=find_packages(),
       package_data={'core.skins.elisa': ['pictures/*.png']},
