#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int gpio_pin;

void cleanup(int sig)
{
    pwmWrite(gpio_pin, 0);   // PWM 출력 0
    pinMode(gpio_pin, INPUT);
    printf("\nPWM 종료 및 GPIO 정리\n");
    exit(0);
}

int main(int argc, char *argv[])
{
    if (argc < 2) {
        printf("Usage: %s GPIO_NO(BCM)\n", argv[0]);
        return 1;
    }

    gpio_pin = atoi(argv[1]);

    if (wiringPiSetupGpio() == -1) {  // BCM 모드
        printf("wiringPi 초기화 실패\n");
        return 1;
    }

    signal(SIGINT, cleanup);  // Ctrl+C 처리

    pinMode(gpio_pin, PWM_OUTPUT);

    // PWM 설정
    pwmSetMode(PWM_MODE_MS);      // Mark-Space 모드
    pwmSetRange(255);             // 0~255 범위
    pwmSetClock(75);              
    /*
       PWM 주파수 계산:
       19.2MHz / (Clock * Range)
       19.2MHz / (75 * 255) ≈ 1003Hz (약 1kHz)
    */

    for (int i = 0; i < 10000; i++) {
        int duty = i % 256;   // 0~255 반복
        pwmWrite(gpio_pin, duty);
        delay(5);             // 5ms
    }

    cleanup(0);
    return 0;
}
