
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
	install -d $(BINDIR)
	install -s $(TARGET) $(BINDIR)
	install -d $(PREFIX)/share/applications
	install -m 0644 GNUDoku.desktop $(PREFIX)/share/applications
	install -d $(PREFIX)/share/pixmaps
	install -m 0644 GNUDoku.png $(PREFIX)/share/pixmaps

uninstall:
	rm -f $(BINDIR)/$(TARGET)
	rm -f $(PREFIX)/share/applications/GNUDoku.desktop
	rm -f $(PREFIX)/share/pixmaps/GNUDoku.png 

withgtkmm24: CXXFLAGS+= -DGNUDOKU_GTKMMVER=24
withgtkmm24: $(TARGET)
