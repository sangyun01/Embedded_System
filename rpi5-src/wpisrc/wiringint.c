#include <stdio.h>
#include <wiringPi.h>			// header file for wiringPi library

#define KEY 24

void isr_key()					// interrupt service routine
{
	printf("Key is pressed \r\n");
}

void main(void)
{
	unsigned int sec = 0;

	wiringPiSetupGpio();		// set pin number to BCM mode
	pinMode(KEY,INPUT);
	wiringPiISR(KEY, INT_EDGE_FALLING, isr_key);
								// register ISR for KEY input
	while(1)
	{
		printf("%d sec. \r\n", sec);
		sec = sec + 1;
		delay(1000);			// delay 1 second
	}
}

