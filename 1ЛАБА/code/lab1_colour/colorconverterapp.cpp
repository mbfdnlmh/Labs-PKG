#include "colorconverterapp.h"
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QColorDialog>
#include <QMessageBox>

ColorConverterApp::ColorConverterApp(QWidget *parent)
    : QWidget(parent)
{
    rInput = new QLineEdit(this);
    gInput = new QLineEdit(this);
    bInput = new QLineEdit(this);
    xInput = new QLineEdit(this);
    yInput = new QLineEdit(this);
    zInput = new QLineEdit(this);
    cInput = new QLineEdit(this);
    mInput = new QLineEdit(this);
    yCInput = new QLineEdit(this);
    kInput = new QLineEdit(this);
    colorPickerButton = new QPushButton("Выбрать цвет", this);

    rSlider = new QSlider(Qt::Horizontal, this);
    gSlider = new QSlider(Qt::Horizontal, this);
    bSlider = new QSlider(Qt::Horizontal, this);
    xSlider = new QSlider(Qt::Horizontal, this);
    ySlider = new QSlider(Qt::Horizontal, this);
    zSlider = new QSlider(Qt::Horizontal, this);
    cSlider = new QSlider(Qt::Horizontal, this);
    mSlider = new QSlider(Qt::Horizontal, this);
    yCSlider = new QSlider(Qt::Horizontal, this);
    kSlider = new QSlider(Qt::Horizontal, this);

    rSlider->setRange(0, 255);
    gSlider->setRange(0, 255);
    bSlider->setRange(0, 255);
    xSlider->setRange(0, 100);
    ySlider->setRange(0, 100);
    zSlider->setRange(0, 100);
    cSlider->setRange(0, 100);
    mSlider->setRange(0, 100);
    yCSlider->setRange(0, 100);
    kSlider->setRange(0, 100);

    QVBoxLayout *mainLayout = new QVBoxLayout(this);

    QHBoxLayout *rgbLayout = new QHBoxLayout();
    rgbLayout->addWidget(new QLabel("R:", this));
    rgbLayout->addWidget(rInput);
    rgbLayout->addWidget(rSlider);
    rgbLayout->addWidget(new QLabel("G:", this));
    rgbLayout->addWidget(gInput);
    rgbLayout->addWidget(gSlider);
    rgbLayout->addWidget(new QLabel("B:", this));
    rgbLayout->addWidget(bInput);
    rgbLayout->addWidget(bSlider);

    QHBoxLayout *xyzLayout = new QHBoxLayout();
    xyzLayout->addWidget(new QLabel("X:", this));
    xyzLayout->addWidget(xInput);
    xyzLayout->addWidget(xSlider);
    xyzLayout->addWidget(new QLabel("Y:", this));
    xyzLayout->addWidget(yInput);
    xyzLayout->addWidget(ySlider);
    xyzLayout->addWidget(new QLabel("Z:", this));
    xyzLayout->addWidget(zInput);
    xyzLayout->addWidget(zSlider);

    QHBoxLayout *cmykLayout = new QHBoxLayout();
    cmykLayout->addWidget(new QLabel("C:", this));
    cmykLayout->addWidget(cInput);
    cmykLayout->addWidget(cSlider);
    cmykLayout->addWidget(new QLabel("M:", this));
    cmykLayout->addWidget(mInput);
    cmykLayout->addWidget(mSlider);
    cmykLayout->addWidget(new QLabel("Y:", this));
    cmykLayout->addWidget(yCInput);
    cmykLayout->addWidget(yCSlider);
    cmykLayout->addWidget(new QLabel("K:", this));
    cmykLayout->addWidget(kInput);
    cmykLayout->addWidget(kSlider);

    mainLayout->addLayout(rgbLayout);
    mainLayout->addLayout(xyzLayout);
    mainLayout->addLayout(cmykLayout);
    mainLayout->addWidget(colorPickerButton);

    setLayout(mainLayout);

    connect(rInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onRGBChanged);
    connect(gInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onRGBChanged);
    connect(bInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onRGBChanged);
    connect(xInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onXYZChanged);
    connect(yInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onXYZChanged);
    connect(zInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onXYZChanged);
    connect(cInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onCMYKChanged);
    connect(mInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onCMYKChanged);
    connect(yCInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onCMYKChanged);
    connect(kInput, &QLineEdit::editingFinished, this, &ColorConverterApp::onCMYKChanged);
    connect(colorPickerButton, &QPushButton::clicked, this, &ColorConverterApp::onColorPickerClicked);
    connect(rSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(gSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(bSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(xSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(ySlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(zSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(cSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(mSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(yCSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
    connect(kSlider, &QSlider::valueChanged, this, &ColorConverterApp::onSliderChanged);
}

void ColorConverterApp::onRGBChanged() {
    int r = rInput->text().toInt();
    int g = gInput->text().toInt();
    int b = bInput->text().toInt();
    checkAndAlertRGB(r, g, b);
    auto xyz = convertRGBToXYZ(r, g, b);
    auto cmyk = convertRGBToCMYK(r, g, b);
    xInput->setText(QString::number(xyz[0]));
    yInput->setText(QString::number(xyz[1]));
    zInput->setText(QString::number(xyz[2]));
    cInput->setText(QString::number(cmyk[0]));
    mInput->setText(QString::number(cmyk[1]));
    yCInput->setText(QString::number(cmyk[2]));
    kInput->setText(QString::number(cmyk[3]));
    updateSlidersFromRGB(r, g, b);
    updateBackgroundColor(QColor(r, g, b));
}

void ColorConverterApp::onXYZChanged() {
    double x = xInput->text().toDouble();
    double y = yInput->text().toDouble();
    double z = zInput->text().toDouble();
    checkAndAlertXYZ(x, y, z);
    auto rgb = convertXYZToRGB(x, y, z);
    auto cmyk = convertRGBToCMYK(rgb[0], rgb[1], rgb[2]);
    rInput->setText(QString::number(rgb[0]));
    gInput->setText(QString::number(rgb[1]));
    bInput->setText(QString::number(rgb[2]));
    cInput->setText(QString::number(cmyk[0]));
    mInput->setText(QString::number(cmyk[1]));
    yCInput->setText(QString::number(cmyk[2]));
    kInput->setText(QString::number(cmyk[3]));
    updateSlidersFromXYZ(x, y, z);
    updateBackgroundColor(QColor(rgb[0], rgb[1], rgb[2]));
}

void ColorConverterApp::onCMYKChanged() {
    double c = cInput->text().toDouble();
    double m = mInput->text().toDouble();
    double yC = yCInput->text().toDouble();
    double k = kInput->text().toDouble();
    checkAndAlertCMYK(c, m, yC, k);
    auto rgb = convertCMYKToRGB(c, m, yC, k);
    auto xyz = convertRGBToXYZ(rgb[0], rgb[1], rgb[2]);
    rInput->setText(QString::number(rgb[0]));
    gInput->setText(QString::number(rgb[1]));
    bInput->setText(QString::number(rgb[2]));
    xInput->setText(QString::number(xyz[0]));
    yInput->setText(QString::number(xyz[1]));
    zInput->setText(QString::number(xyz[2]));
    updateSlidersFromCMYK(c, m, yC, k);
    updateBackgroundColor(QColor(rgb[0], rgb[1], rgb[2]));
}

void ColorConverterApp::onSliderChanged() {
    int r = rSlider->value();
    int g = gSlider->value();
    int b = bSlider->value();
    int x = xSlider->value();
    int y = ySlider->value();
    int z = zSlider->value();
    int c = cSlider->value();
    int m = mSlider->value();
    int yC = yCSlider->value();
    int k = kSlider->value();

    rInput->setText(QString::number(r));
    gInput->setText(QString::number(g));
    bInput->setText(QString::number(b));
    xInput->setText(QString::number(x));
    yInput->setText(QString::number(y));
    zInput->setText(QString::number(z));
    cInput->setText(QString::number(c));
    mInput->setText(QString::number(m));
    yCInput->setText(QString::number(yC));
    kInput->setText(QString::number(k));

    onRGBChanged();
    onXYZChanged();
    onCMYKChanged();
}

void ColorConverterApp::onColorPickerClicked() {
    QColor color = QColorDialog::getColor();
    if (color.isValid()) {
        rInput->setText(QString::number(color.red()));
        gInput->setText(QString::number(color.green()));
        bInput->setText(QString::number(color.blue()));
        onRGBChanged();
    }
}

QVector<double> ColorConverterApp::convertRGBToXYZ(int r, int g, int b) {
    double xr = r / 255.0;
    double xg = g / 255.0;
    double xb = b / 255.0;
    return {xr * 100, xg * 100, xb * 100};
}

QVector<int> ColorConverterApp::convertXYZToRGB(double x, double y, double z) {
    return {static_cast<int>(x * 2.55), static_cast<int>(y * 2.55), static_cast<int>(z * 2.55)};
}

QVector<double> ColorConverterApp::convertRGBToCMYK(int r, int g, int b) {
    double c = 1 - r / 255.0;
    double m = 1 - g / 255.0;
    double yC = 1 - b / 255.0;
    double k = qMin(c, qMin(m, yC));
    c = (c - k) / (1 - k);
    m = (m - k) / (1 - k);
    yC = (yC - k) / (1 - k);
    return {c * 100, m * 100, yC * 100, k * 100};
}

QVector<int> ColorConverterApp::convertCMYKToRGB(double c, double m, double yC, double k) {
    int r = static_cast<int>(255 * (1 - c / 100) * (1 - k / 100));
    int g = static_cast<int>(255 * (1 - m / 100) * (1 - k / 100));
    int b = static_cast<int>(255 * (1 - yC / 100) * (1 - k / 100));
    return {r, g, b};
}

void ColorConverterApp::checkAndAlertRGB(int r, int g, int b) {
    if (r < 0 || r > 255 || g < 0 || g > 255 || b < 0 || b > 255) {
        QMessageBox::warning(this, "Ошибка", "Значения RGB должны быть в диапазоне 0-255.");
    }
}

void ColorConverterApp::checkAndAlertXYZ(double x, double y, double z) {
    if (x < 0 || x > 100 || y < 0 || y > 100 || z < 0 || z > 100) {
        QMessageBox::warning(this, "Ошибка", "Значения XYZ должны быть в диапазоне 0-100.");
    }
}

void ColorConverterApp::checkAndAlertCMYK(double c, double m, double yC, double k) {
    if (c < 0 || c > 100 || m < 0 || m > 100 || yC < 0 || yC > 100 || k < 0 || k > 100) {
        QMessageBox::warning(this, "Ошибка", "Значения CMYK должны быть в диапазоне 0-100.");
    }
}

void ColorConverterApp::updateSlidersFromRGB(int r, int g, int b) {
    rSlider->setValue(r);
    gSlider->setValue(g);
    bSlider->setValue(b);
}

void ColorConverterApp::updateSlidersFromXYZ(double x, double y, double z) {
    xSlider->setValue(static_cast<int>(x));
    ySlider->setValue(static_cast<int>(y));
    zSlider->setValue(static_cast<int>(z));
}

void ColorConverterApp::updateSlidersFromCMYK(double c, double m, double yC, double k) {
    cSlider->setValue(static_cast<int>(c));
    mSlider->setValue(static_cast<int>(m));
    yCSlider->setValue(static_cast<int>(yC));
    kSlider->setValue(static_cast<int>(k));
}

void ColorConverterApp::updateBackgroundColor(const QColor &color) {
    QPalette palette = this->palette();
    palette.setColor(QPalette::Window, color);
    this->setPalette(palette);
}
