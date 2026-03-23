#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#define LED_R 20   // BCM 20 (빨간 LED)
#define LED_Y 21   // BCM 21 (노란 LED)
#define SENSOR 17  // BCM 17 (PIR 센서)

void cleanup(int sig)
{
    digitalWrite(LED_R, LOW);
    digitalWrite(LED_Y, LOW);
    pinMode(LED_R, INPUT);
    pinMode(LED_Y, INPUT);
    printf("\nStopped by User\n");
    exit(0);
}

int main(void)
{
    if (wiringPiSetupGpio() == -1) {   // BCM 모드
        printf("wiringPi 초기화 실패\n");
        return 1;
    }

    signal(SIGINT, cleanup);  // Ctrl+C 처리

    pinMode(LED_R, OUTPUT);
    pinMode(LED_Y, OUTPUT);
    pinMode(SENSOR, INPUT);

    printf("PIR Ready . . . . \n");
    delay(5000);   // PIR 안정화 시간 5초

    while (1)
    {
        if (digitalRead(SENSOR) == HIGH)
        {
            digitalWrite(LED_Y, HIGH);
            digitalWrite(LED_R, LOW);
            printf("Motion Detected !\n");
            delay(200);
        }
        else
        {
            digitalWrite(LED_R, HIGH);
            digitalWrite(LED_Y, LOW);
            printf("NO Motion !\n");
            delay(200);
        }
    }

    return 0;
}
