#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include <inttypes.h>
#include <stdio.h>
#include "dht22.h"
#include "uart.h"

typedef struct {
        int16_t temperature;
        uint16_t humidity;
} values_t;

int main() {

    DDRD = 0x00;
    PORTD = 0x00;
    UART_init();

    DHT22_DATA_t sensorValues;
    DHT22_ERROR_t error;
    sei();

    values_t values;
    char s[20];
    while (1) {
        values.temperature = 0;
        values.humidity = 0;

        cli();
        error = readDHT22(&sensorValues);
        switch (error) {
            case DHT_ERROR_NONE:
                values.temperature = sensorValues.raw_temperature;
                values.humidity = sensorValues.raw_humidity;
        default:
            break;

        }
        sprintf (s, "Hum:%u\tTemp:%d\n", values.humidity, values.temperature); UART_puts(s);
        sei();
        _delay_ms(1000);
    }

    return 0;
}
