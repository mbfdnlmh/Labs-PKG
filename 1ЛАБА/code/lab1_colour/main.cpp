#include <QApplication>
#include "colorconverterapp.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    ColorConverterApp window;
    window.setWindowTitle("Конвертер цветовых моделей");
    window.show();

    return app.exec();
}
