#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define SPI_CHANNEL 0        // SPI0 CE0
#define SPI_SPEED   100000   // 100kHz
#define LDR_CHANNEL 0        // MCP3008 CH0

int readadc(int adcnum)
{
    if (adcnum < 0 || adcnum > 7)
        return -1;

    unsigned char buffer[3];

    buffer[0] = 1;                           // Start bit
    buffer[1] = (8 + adcnum) << 4;            // Single-ended + 채널 선택
    buffer[2] = 0;

    wiringPiSPIDataRW(SPI_CHANNEL, buffer, 3);

    int data = ((buffer[1] & 3) << 8) | buffer[2];
    return data;   // 0 ~ 1023 (10bit)
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
        int ldr_value = readadc(LDR_CHANNEL);

        printf("---------------------------------------\n");
        printf("LDR Value: %d\n", ldr_value);

        usleep(500000);   // 0.5초 대기 (500ms)
    }

    return 0;
}
