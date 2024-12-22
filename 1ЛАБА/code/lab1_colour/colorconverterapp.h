#ifndef COLORCONVERTERAPP_H
#define COLORCONVERTERAPP_H

#include <QWidget>
#include <QLineEdit>
#include <QPushButton>
#include <QColorDialog>
#include <QSlider>
#include <QMessageBox>

class ColorConverterApp : public QWidget
{
    Q_OBJECT

public:
    explicit ColorConverterApp(QWidget *parent = nullptr);

private slots:
    void onRGBChanged();
    void onXYZChanged();
    void onCMYKChanged();
    void onColorPickerClicked();
    void onSliderChanged();

private:
    void updateBackgroundColor(const QColor &color);
    QVector<double> convertRGBToXYZ(int r, int g, int b);
    QVector<int> convertXYZToRGB(double x, double y, double z);
    QVector<double> convertRGBToCMYK(int r, int g, int b);
    QVector<int> convertCMYKToRGB(double c, double m, double yC, double k);
    void checkAndAlertClamping(double value, double min, double max, const QString &componentName);
    void checkAndAlertRGB(int r, int g, int b);
    void checkAndAlertXYZ(double x, double y, double z);
    void checkAndAlertCMYK(double c, double m, double yC, double k);
    void updateSlidersFromRGB(int r, int g, int b);
    void updateSlidersFromXYZ(double x, double y, double z);
    void updateSlidersFromCMYK(double c, double m, double yC, double k);

    QLineEdit *rInput;
    QLineEdit *gInput;
    QLineEdit *bInput;
    QLineEdit *xInput;
    QLineEdit *yInput;
    QLineEdit *zInput;
    QLineEdit *cInput;
    QLineEdit *mInput;
    QLineEdit *yCInput;
    QLineEdit *kInput;
    QPushButton *colorPickerButton;

    QSlider *rSlider;
    QSlider *gSlider;
    QSlider *bSlider;
    QSlider *xSlider;
    QSlider *ySlider;
    QSlider *zSlider;
    QSlider *cSlider;
    QSlider *mSlider;
    QSlider *yCSlider;
    QSlider *kSlider;
};

#endif // COLORCONVERTERAPP_H
