#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>

#define BMP180_ADDR 0x77

// 보정계수 구조체
short AC1, AC2, AC3, B1, B2, MB, MC, MD;
unsigned short AC4, AC5, AC6;

int fd;
long B5;

// 16비트 읽기
short readS16(int reg)
{
    int msb = wiringPiI2CReadReg8(fd, reg);
    int lsb = wiringPiI2CReadReg8(fd, reg + 1);
    return (short)((msb << 8) | lsb);
}

unsigned short readU16(int reg)
{
    int msb = wiringPiI2CReadReg8(fd, reg);
    int lsb = wiringPiI2CReadReg8(fd, reg + 1);
    return (unsigned short)((msb << 8) | lsb);
}

void readCalibration()
{
    AC1 = readS16(0xAA);
    AC2 = readS16(0xAC);
    AC3 = readS16(0xAE);
    AC4 = readU16(0xB0);
    AC5 = readU16(0xB2);
    AC6 = readU16(0xB4);
    B1  = readS16(0xB6);
    B2  = readS16(0xB8);
    MB  = readS16(0xBA);
    MC  = readS16(0xBC);
    MD  = readS16(0xBE);
}

long readRawTemp()
{
    wiringPiI2CWriteReg8(fd, 0xF4, 0x2E);
    usleep(5000);
    return readU16(0xF6);
}

long readRawPressure()
{
    wiringPiI2CWriteReg8(fd, 0xF4, 0x34);
    usleep(8000);
    long msb = wiringPiI2CReadReg8(fd, 0xF6);
    long lsb = wiringPiI2CReadReg8(fd, 0xF7);
    long xlsb = wiringPiI2CReadReg8(fd, 0xF8);
    return ((msb << 16) + (lsb << 8) + xlsb) >> 8;
}

double readTemperature()
{
    long UT = readRawTemp();
    long X1 = ((UT - AC6) * AC5) >> 15;
    long X2 = (MC << 11) / (X1 + MD);
    B5 = X1 + X2;
    return ((B5 + 8) >> 4) / 10.0;
}

double readPressure()
{
    long UP = readRawPressure();
    long B6 = B5 - 4000;
    long X1 = (B2 * (B6 * B6 >> 12)) >> 11;
    long X2 = (AC2 * B6) >> 11;
    long X3 = X1 + X2;
    long B3 = (((long)AC1 * 4 + X3) + 2) >> 2;
    X1 = (AC3 * B6) >> 13;
    X2 = (B1 * (B6 * B6 >> 12)) >> 16;
    X3 = ((X1 + X2) + 2) >> 2;
    unsigned long B4 = (AC4 * (unsigned long)(X3 + 32768)) >> 15;
    unsigned long B7 = ((unsigned long)UP - B3) * 50000;

    long p;
    if (B7 < 0x80000000)
        p = (B7 << 1) / B4;
    else
        p = (B7 / B4) << 1;

    X1 = (p >> 8) * (p >> 8);
    X1 = (X1 * 3038) >> 16;
    X2 = (-7357 * p) >> 16;
    p = p + ((X1 + X2 + 3791) >> 4);

    return (double)p;
}

double calculateAltitude(double pressure)
{
    return 44330.0 * (1.0 - pow(pressure / 101325.0, 0.1903));
}

int main(void)
{
    if (wiringPiSetup() == -1) {
        printf("wiringPi 초기화 실패\n");
        return 1;
    }

    fd = wiringPiI2CSetup(BMP180_ADDR);
    if (fd < 0) {
        printf("BMP180 연결 실패\n");
        return 1;
    }

    readCalibration();

    while (1)
    {
        double temp = readTemperature();
        double pressure = readPressure();
        double altitude = calculateAltitude(pressure);

        printf("Temp = %.2f *C\n", temp);
        printf("Pressure = %.2f Pa\n", pressure);
        printf("Altitude = %.2f m\n\n", altitude);

        sleep(2);
    }

    return 0;
}
