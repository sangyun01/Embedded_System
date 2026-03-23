#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

#define SERVO_PIN 18   // BCM 18 (PWM0)

void cleanup(int sig)
{
    pwmWrite(SERVO_PIN, 0);   // PWM 출력 정지
    pinMode(SERVO_PIN, INPUT);
    printf("\n서보 종료 및 GPIO 정리\n");
    exit(0);
}

int main(void)
{
    if (wiringPiSetupGpio() == -1) {  // BCM 모드
        printf("wiringPi 초기화 실패\n");
        return 1;
    }

    signal(SIGINT, cleanup);  // Ctrl+C 처리

    pinMode(SERVO_PIN, PWM_OUTPUT);

    // PWM 설정
    pwmSetMode(PWM_MODE_MS);  
    pwmSetRange(2000);        
    pwmSetClock(192);         
    /*
        PWM 주파수 계산:
        19.2MHz / (Clock * Range)
        19.2MHz / (192 * 2000)
        = 50Hz
    */

    while (1) {
        pwmWrite(SERVO_PIN, 150);   // 1.5ms → 90도 (7.5%)
        delay(1000);

        pwmWrite(SERVO_PIN, 250);   // 2.5ms → 180도 (12.5%)
        delay(1000);

        pwmWrite(SERVO_PIN, 50);    // 0.5ms → 0도 (2.5%)
        delay(1000);
    }

    return 0;
}
