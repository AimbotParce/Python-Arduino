#define PY_GET_BOARD 1
#define PY_GET_PIN 2
#define PY_DIGITAL_WRITE 3
#define PY_ANALOG_READ 4
#define PY_DIGITAL_READ 5
#define PY_ANALOG_WRITE 6
#define PY_PULSE_IN 7
#define PY_TONE 8
#define PY_NO_TONE 9

int firstAnalog = A0;

void setup() {
  Serial.begin(9600);
}

int blocking_Serial_read() {
  while (Serial.available() == 0) {
    //Wait
  }
  return Serial.read();
}

int blocking_Serial_read_string() {
  while (Serial.available() == 0) {
    //Wait
  }
  return Serial.parseInt();
}

void debugging_led_blink(int pin) {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, HIGH);
  delay(100);
  digitalWrite(pin, LOW);
}

int get_pin() {
  int number = blocking_Serial_read();
  int mode = blocking_Serial_read();  // Pin Mode: 0 = OUTPUT, 1 = INPUT
  switch (mode) {
    case 0: {
      pinMode(number, OUTPUT);
      break;
    }
    case 1: {
      pinMode(number, INPUT);
      break;
    }
    default: {
      return 1;  //ERROR
    }
  }
  return 0;
}

int digital_write() {
  int pin = blocking_Serial_read();
  int value = blocking_Serial_read();
  digitalWrite(pin, value);
  return 0;
}

float analog_read() {
  int pin = blocking_Serial_read();
  return analogRead(pin);
}

int digital_read() {
  int pin = blocking_Serial_read();
  int value = digitalRead(pin);
  if (value == HIGH) {
    return 1;
  } else{
    return 0;
  }
}

int analog_write() {
  int pin = blocking_Serial_read();
  int value = blocking_Serial_read();
  analogWrite(pin, value);
  return 0;
}

float pulse_in() {
  int pin = blocking_Serial_read();
  int value = blocking_Serial_read();
  return pulseIn(pin, value);
}

int tone_foo() {
  int pin = blocking_Serial_read();
  int frequency = blocking_Serial_read_string();
  int duration = blocking_Serial_read_string();
  if (duration != 0) {
    tone(pin, frequency, duration);
  }
  else {
    //tone(pin, frequency);
  }
  return 0;
}

int no_tone() {
  int pin = blocking_Serial_read();
  noTone(pin);
  return 0;
}

void loop() {
  if (Serial.available() > 0) {
    byte pyCommand = Serial.read();
    switch (pyCommand) {
      case PY_GET_BOARD:
        Serial.println(A0);
        return;
      case PY_GET_PIN:
        Serial.println(get_pin());
        return;
      case PY_DIGITAL_WRITE:
        Serial.println(digital_write());
        return;
      case PY_ANALOG_READ:
        Serial.println(analog_read());
        return;
      case PY_DIGITAL_READ:
        Serial.println(digital_read());
        return;
      case PY_ANALOG_WRITE:
        Serial.println(analog_write());
        return;
      case PY_PULSE_IN:
        Serial.println(pulse_in());
        return;
      case PY_TONE:
        Serial.println(tone_foo());
        return;
      case PY_NO_TONE:
        Serial.println(no_tone());
        return;
    }
  }
}
