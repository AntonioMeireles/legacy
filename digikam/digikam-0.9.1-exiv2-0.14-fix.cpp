Index: extragear/graphics/digikam/libs/widgets/metadata/makernotewidget.h
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/makernotewidget.h	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/makernotewidget.h	(revision 642723)
@@ -1,10 +1,10 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-20
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-20
  * Description : a widget to display non standard Exif metadata
  *               used by camera makers
  * 
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
Index: extragear/graphics/digikam/libs/widgets/metadata/exifwidget.cpp
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/exifwidget.cpp	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/exifwidget.cpp	(revision 642723)
@@ -1,9 +1,9 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-20
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-20
  * Description : a widget to display Standard Exif metadata
  * 
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
@@ -46,6 +46,7 @@
 #include "dmetadata.h"
 #include "metadatalistview.h"
 #include "exifwidget.h"
+#include "exifwidget.moc"
 
 namespace Digikam
 {
@@ -180,11 +181,10 @@
     }
     catch (Exiv2::Error& e)
     {
-        DDebug() << "Cannot parse EXIF metadata using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return false;
+        DMetadata::printExiv2ExceptionError("Cannot parse EXIF metadata using Exiv2 ", e);
     }
+
+    return false;
 }
 
 void ExifWidget::buildView(void)
@@ -210,11 +210,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag title using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("Unknown");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag title using Exiv2 ", e);
     }
+
+    return i18n("Unknown");
 }
 
 QString ExifWidget::getTagDescription(const QString& key)
@@ -227,11 +226,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag description using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("No description available");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag description using Exiv2 ", e);
     }
+
+    return i18n("No description available");
 }
 
 void ExifWidget::slotSaveMetadataToFile(void)
@@ -243,4 +241,3 @@
 
 }  // namespace Digikam
 
-#include "exifwidget.moc"
Index: extragear/graphics/digikam/libs/widgets/metadata/gpswidget.h
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/gpswidget.h	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/gpswidget.h	(revision 642723)
@@ -1,9 +1,9 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-22
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-22
  * Description : a tab widget to display GPS info
  * 
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
@@ -84,7 +84,6 @@
 private:
 
     GPSWidgetPriv *d;
-
 };
 
 }  // namespace Digikam
Index: extragear/graphics/digikam/libs/widgets/metadata/iptcwidget.cpp
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/iptcwidget.cpp	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/iptcwidget.cpp	(revision 642723)
@@ -1,9 +1,9 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-20
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-20
  * Description : A widget to display IPTC metadata
  * 
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
@@ -44,6 +44,7 @@
 #include "ddebug.h"
 #include "dmetadata.h"
 #include "iptcwidget.h"
+#include "iptcwidget.moc"
 
 namespace Digikam
 {
@@ -155,11 +156,10 @@
     }
     catch (Exiv2::Error& e)
     {
-        DDebug() << "Cannot parse IPTC metadata using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return false;
+        DMetadata::printExiv2ExceptionError("Cannot parse IPTC metadata using Exiv2 ", e);
     }
+
+    return false;
 }
 
 void IptcWidget::buildView(void)
@@ -184,11 +184,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag title using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("Unknow");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag title using Exiv2 ", e);
     }
+
+    return i18n("Unknow");
 }
 
 QString IptcWidget::getTagDescription(const QString& key)
@@ -201,11 +200,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag description using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("No description available");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag description using Exiv2 ", e);
     }
+
+    return i18n("No description available");
 }
 
 void IptcWidget::slotSaveMetadataToFile(void)
@@ -217,4 +215,3 @@
 
 }  // namespace Digikam
 
-#include "iptcwidget.moc"
Index: extragear/graphics/digikam/libs/widgets/metadata/exifwidget.h
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/exifwidget.h	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/exifwidget.h	(revision 642723)
@@ -1,9 +1,9 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-20
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-20
  * Description : a widget to display Standard Exif metadata
  * 
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
Index: extragear/graphics/digikam/libs/widgets/metadata/iptcwidget.h
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/iptcwidget.h	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/iptcwidget.h	(revision 642723)
@@ -1,9 +1,9 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-20
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-20
  * Description : A widget to display IPTC metadata
  * 
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
Index: extragear/graphics/digikam/libs/widgets/metadata/makernotewidget.cpp
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/makernotewidget.cpp	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/makernotewidget.cpp	(revision 642723)
@@ -1,10 +1,10 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-20
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-20
  * Description : a widget to display non standard Exif metadata
  *               used by camera makers
  *
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
@@ -46,6 +46,7 @@
 #include "ddebug.h"
 #include "dmetadata.h"
 #include "makernotewidget.h"
+#include "makernotewidget.moc"
 
 namespace Digikam
 {
@@ -197,11 +198,10 @@
     }
     catch (Exiv2::Error& e)
     {
-        DDebug() << "Cannot parse MAKERNOTE metadata using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return false;
+        DMetadata::printExiv2ExceptionError("Cannot parse MAKERNOTE metadata using Exiv2 ", e);
     }
+
+    return false;
 }
 
 void MakerNoteWidget::buildView(void)
@@ -226,11 +226,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag title using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("Unknown");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag title using Exiv2 ", e);
     }
+
+    return i18n("Unknown");
 }
 
 QString MakerNoteWidget::getTagDescription(const QString& key)
@@ -243,11 +242,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag description using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("No description available");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag description using Exiv2 ", e);
     }
+
+    return i18n("No description available");
 }
 
 void MakerNoteWidget::slotSaveMetadataToFile(void)
@@ -259,4 +257,3 @@
 
 }  // namespace Digikam
 
-#include "makernotewidget.moc"
Index: extragear/graphics/digikam/libs/widgets/metadata/gpswidget.cpp
===================================================================
--- extragear/graphics/digikam/libs/widgets/metadata/gpswidget.cpp	(revision 642722)
+++ extragear/graphics/digikam/libs/widgets/metadata/gpswidget.cpp	(revision 642723)
@@ -1,9 +1,9 @@
 /* ============================================================
- * Author: Gilles Caulier <caulier dot gilles at gmail dot com>
- * Date  : 2006-02-22
+ * Authors: Gilles Caulier <caulier dot gilles at gmail dot com>
+ * Date   : 2006-02-22
  * Description : a tab widget to display GPS info
  *
- * Copyright 2006 by Gilles Caulier
+ * Copyright 2006-2007 by Gilles Caulier
  *
  * This program is free software; you can redistribute it
  * and/or modify it under the terms of the GNU General
@@ -62,6 +62,7 @@
 
 namespace Digikam
 {
+
 static const char* ExifGPSHumanList[] =
 {
      "GPSLatitude",
@@ -304,11 +305,10 @@
     catch (Exiv2::Error& e)
     {
         setMetadataEmpty();
-        DDebug() << "Cannot parse EXIF metadata using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return false;
+        DMetadata::printExiv2ExceptionError("Cannot parse EXIF metadata using Exiv2 ", e);        
     }
+
+    return false;
 }
 
 void GPSWidget::setMetadataEmpty()
@@ -342,11 +342,10 @@
     }
     catch (Exiv2::Error& e) 
     {
-        DDebug() << "Cannot get metadata tag title using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("Unknown");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag title using Exiv2 ", e);
     }
+
+    return i18n("Unknown");
 }
 
 QString GPSWidget::getTagDescription(const QString& key)
@@ -359,11 +358,10 @@
     }
     catch (Exiv2::Error& e) 
     {   
-        DDebug() << "Cannot get metadata tag description using Exiv2 ("
-                  << QString::fromAscii(e.what().c_str())
-                  << ")" << endl;
-        return i18n("No description available");
+        DMetadata::printExiv2ExceptionError("Cannot get metadata tag description using Exiv2 ", e);
     }
+
+    return i18n("No description available");
 }
 
 bool GPSWidget::decodeGPSPosition(void)
