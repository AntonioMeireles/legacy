
PREFIX=/usr
BINDIR=$(PREFIX)/bin

VERSION=\"0.92\"

CXX=g++
SOURCES=GNUDoku.C sudoku.C sudoku-solve.C
TARGET=GNUDoku
CXXFLAGS=`pkg-config gtkmm-2.4 --cflags` "-DVERSION=$(VERSION)"
LIBS=`pkg-config gtkmm-2.4 --libs`


all: $(TARGET)

clean:
	rm -f $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(SOURCES) -o $(TARGET) $(CXXFLAGS) $(LIBS)

install:
	install -d $(DESTDIR)$(BINDIR)
	install -s $(TARGET) $(DESTDIR)$(BINDIR)
	install -d $(DESTDIR)$(PREFIX)/share/applications
	install -m 0644 GNUDoku.desktop $(DESTDIR)$(PREFIX)/share/applications
	install -d $(DESTDIR)$(PREFIX)/share/pixmaps
	install -m 0644 GNUDoku.png $(DESTDIR)$(PREFIX)/share/pixmaps

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/$(TARGET)
	rm -f $(DESTDIR)$(PREFIX)/share/applications/GNUDoku.desktop
	rm -f $(DESTDIR)$(PREFIX)/share/pixmaps/GNUDoku.png 

withgtkmm24: CXXFLAGS+= -DGNUDOKU_GTKMMVER=24
withgtkmm24: $(TARGET)
