#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <signal.h>

#define TRIG 23   // BCM 23
#define ECHO 24   // BCM 24

void cleanup(int sig)
{
    digitalWrite(TRIG, LOW);
    pinMode(TRIG, INPUT);
    pinMode(ECHO, INPUT);
    printf("\nMeasurement stopped by User\n");
    exit(0);
}

// 현재 시간을 초 단위(double)로 반환
double getTime()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec / 1000000.0;
}

int main(void)
{
    if (wiringPiSetupGpio() == -1) {
        printf("wiringPi 초기화 실패\n");
        return 1;
    }

    signal(SIGINT, cleanup);  // Ctrl+C 처리

    printf("Distance measurement in progress\n");

    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);

    digitalWrite(TRIG, LOW);
    printf("Waiting for sensor to settle\n");
    delay(2000);   // 2초 대기

    while (1) {

        // 10µs Trigger 펄스 생성
        digitalWrite(TRIG, HIGH);
        delayMicroseconds(10);
        digitalWrite(TRIG, LOW);

        // Echo 상승 대기
        while (digitalRead(ECHO) == LOW);
        double start = getTime();

        // Echo 하강 대기
        while (digitalRead(ECHO) == HIGH);
        double stop = getTime();

        double check_time = stop - start;
        double distance = check_time * 34300 / 2;

        printf("Distance : %.1f cm\n", distance);

        delay(400);  // 0.4초 간격
    }

    return 0;
}
