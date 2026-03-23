#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define SPI_CHANNEL 0     // SPI0 CE0
#define SPI_SPEED   100000  // 100kHz
#define POT_CHANNEL 0     // MCP3008 CH0

int readadc(int adcnum)
{
    if (adcnum < 0 || adcnum > 7)
        return -1;

    unsigned char buffer[3];

    buffer[0] = 1;                                  // Start bit
    buffer[1] = (8 + adcnum) << 4;                   // Single-ended + channel
    buffer[2] = 0;

    wiringPiSPIDataRW(SPI_CHANNEL, buffer, 3);

    int data = ((buffer[1] & 3) << 8) | buffer[2];
    return data;   // 0~1023 (10-bit)
}

int main(void)
{
    if (wiringPiSetupGpio() == -1) {
        printf("wiringPi 초기화 실패\n");
        return 1;
    }

    if (wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) < 0) {
        printf("SPI 설정 실패\n");
        return 1;
    }

    while (1)
    {
        int pot_value = readadc(POT_CHANNEL);

        printf("---------------------------------------\n");
        printf("POT Value: %d\n", pot_value);

        sleep(0.5);  // 0.5초 대기 (주의: sleep은 정수초용)
        usleep(500000);  // 0.5초 (마이크로초 단위)
    }

    return 0;
}
