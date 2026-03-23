#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <stdio.h>
#include <unistd.h>
#include <math.h>
#include <string.h>

#define BMP180_ADDR  0x77
#define OLED_ADDR    0x3C

int bmp_fd, oled_fd;

/* ---------------- OLED 기본 함수 ---------------- */

void oled_command(unsigned char cmd)
{
    wiringPiI2CWriteReg8(oled_fd, 0x00, cmd);
}

void oled_data(unsigned char data)
{
    wiringPiI2CWriteReg8(oled_fd, 0x40, data);
}

void oled_init()
{
    oled_command(0xAE); // display off
    oled_command(0x20); oled_command(0x00);
    oled_command(0xB0);
    oled_command(0xC8);
    oled_command(0x00);
    oled_command(0x10);
    oled_command(0x40);
    oled_command(0x81); oled_command(0x7F);
    oled_command(0xA1);
    oled_command(0xA6);
    oled_command(0xA8); oled_command(0x3F);
    oled_command(0xA4);
    oled_command(0xD3); oled_command(0x00);
    oled_command(0xD5); oled_command(0x80);
    oled_command(0xD9); oled_command(0xF1);
    oled_command(0xDA); oled_command(0x12);
    oled_command(0xDB); oled_command(0x40);
    oled_command(0x8D); oled_command(0x14);
    oled_command(0xAF); // display on
}

void oled_clear()
{
    for (int page = 0; page < 8; page++) {
        oled_command(0xB0 + page);
        oled_command(0x00);
        oled_command(0x10);
        for (int col = 0; col < 128; col++) {
            oled_data(0x00);
        }
    }
}

/* -------- BMP180 간단 온도/압력 읽기 (간략화 버전) -------- */

short readS16(int reg)
{
    int msb = wiringPiI2CReadReg8(bmp_fd, reg);
    int lsb = wiringPiI2CReadReg8(bmp_fd, reg+1);
    return (short)((msb << 8) | lsb);
}

double readTemperature()
{
    wiringPiI2CWriteReg8(bmp_fd, 0xF4, 0x2E);
    usleep(5000);
    int msb = wiringPiI2CReadReg8(bmp_fd, 0xF6);
    int lsb = wiringPiI2CReadReg8(bmp_fd, 0xF7);
    int UT = (msb << 8) | lsb;

    return UT / 340.0;   // 간략 계산 (정밀 계산은 이전 코드 참조)
}

/* ------------------ 메인 ------------------ */

int main(void)
{
    if (wiringPiSetup() == -1)
        return 1;

    bmp_fd  = wiringPiI2CSetup(BMP180_ADDR);
    oled_fd = wiringPiI2CSetup(OLED_ADDR);

    oled_init();
    oled_clear();

    while (1)
    {
        double temp = readTemperature();
        double pressure = 101325;  // 예시값
        double altitude = 0;       // 예시값

        printf("Temp = %.2f C\n", temp);
        printf("Pressure = %.2f Pa\n", pressure);
        printf("Altitude = %.2f m\n\n", altitude);

        oled_clear();

        // 간단히 ASCII 텍스트 출력 (폰트 직접 구현 필요)
        // 실제 텍스트 출력은 5x7 폰트 배열 구현 필요
        // 여기서는 구조 예시만 제시

        sleep(2);
    }

    return 0;
}
