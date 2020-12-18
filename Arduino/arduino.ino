// 2 Bytes - Magic (0xabcd)
// 1 Byte - Pin
// 1 Byte - Mode (1 - Digital, 2 - Analog)
// 1 Byte - Request (1 - Write, 2 - Read)
// 1 Byte (Opt) - Value to set to - 0 when not used.

// returned messages:
// 0xab 0xcd 0x1 - ERROR
// 0xab 0xcd 0x0 - SUCCESS
// 0xab 0xcd 0x0 VALUE - Returning answer to read

const unsigned int MAGIC_BYTE1_OFFSET = 0;
const unsigned int MAGIC_BYTE2_OFFSET = 1;
const unsigned int PIN_OFFSET = 2;
const unsigned int MODE_OFFSET = 3;
const unsigned int REQUEST_OFFSET = 4;
const unsigned int VALUE_OFFSET = 5;

const unsigned int PIN_MODE_DI = 1;
const unsigned int PIN_MODE_AN = 2;

const unsigned int REQUEST_TYPE_SET = 1;
const unsigned int REQUEST_TYPE_READ  = 2;

const unsigned char MAGIC_BYTE1 = 0xab;
const unsigned char MAGIC_BYTE2 = 0xcd;

const char ERROR_MESSAGE[] = {MAGIC_BYTE1, MAGIC_BYTE2, 1};
const char SUCCESS_MESSAGE[] = {MAGIC_BYTE1, MAGIC_BYTE2, 3};

const unsigned int MESSAGE_SIZE = 6;
char message[MESSAGE_SIZE];

const int DIGITAL_INPUT_PINS[] = {};
const int DIGITAL_OUTPUT_PINS[] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}; // 3, 8, 9, 11, 12, 13 are used by motors
const int ANALOG_INPUT_PINS[] = {0, 1, 2, 3, 4, 5, 6, 7};
const int ANALOG_OUTPUT_PINS[] = {};

void setup() {
  Serial.begin(9600);              //Starting serial communication
  for (int i = 0; i < sizeof(DIGITAL_INPUT_PINS); i++) {
    pinMode(i, INPUT);
  }
  for (int i = 0; i < sizeof(ANALOG_INPUT_PINS); i++) {
    pinMode(i, INPUT); 
  }
  
  for (int i = 0; i < sizeof(DIGITAL_OUTPUT_PINS); i++) {
    pinMode(i, OUTPUT); 
    digitalWrite(i, LOW); 
  }
  for (int i = 0; i < sizeof(ANALOG_OUTPUT_PINS); i++) {
    pinMode(i, OUTPUT); 
  }
}

bool is_in_array(int value, int arr[], unsigned int arr_size) 
{
  for (int i = 0; i < arr_size; i++) {
    if (arr[i] == value) {
      return true;
    }
  }
  return false;
}

void update_buffer(int recevied_byte) {
  for (int i = 1; i < MESSAGE_SIZE; i++) {
    message[i - 1] = message[i];
  }
  message[MESSAGE_SIZE - 1] = recevied_byte;
}

void send_error_message() {
  Serial.write(ERROR_MESSAGE, sizeof(ERROR_MESSAGE));
}

void send_success_message() {
  Serial.write(SUCCESS_MESSAGE, sizeof(SUCCESS_MESSAGE));
}

void handle_set_command() {
  int pin = message[PIN_OFFSET];
  
  switch (message[MODE_OFFSET]) {
    case PIN_MODE_DI:
      if (!is_in_array(pin, DIGITAL_OUTPUT_PINS, sizeof(DIGITAL_OUTPUT_PINS))) {
        send_error_message();
        return;
      }
      digitalWrite(pin, message[VALUE_OFFSET]);
      break;
    case PIN_MODE_AN:
      if (!is_in_array(pin, ANALOG_OUTPUT_PINS, sizeof(ANALOG_OUTPUT_PINS))) {
        send_error_message();
        return;
      }
      analogWrite(pin, message[VALUE_OFFSET]);
      break;
    default:
      send_error_message();
      return;
  }
  send_success_message();
}

void handle_read_command() {
  int pin = message[PIN_OFFSET];
  pinMode(pin, INPUT);

  unsigned char value = 0;
  switch (message[MODE_OFFSET]) {
    case PIN_MODE_DI:
      if (!is_in_array(pin, DIGITAL_INPUT_PINS, sizeof(DIGITAL_INPUT_PINS))) {
        send_error_message();
        return;
      }
      value = digitalRead(pin);
      break;
    case PIN_MODE_AN:
      if (!is_in_array(pin, ANALOG_INPUT_PINS, sizeof(ANALOG_INPUT_PINS))) {
        send_error_message();
        return;
      }
      value = analogRead(pin);
      break;
    default:
      send_error_message();
      break;
  }
  char reply[] = {MAGIC_BYTE1, MAGIC_BYTE2, 2, value};
  Serial.write(reply);
}

void handle_command() {
  switch (message[REQUEST_OFFSET]) {
    case REQUEST_TYPE_SET:
      handle_set_command();
      break;
    case REQUEST_TYPE_READ:
      handle_read_command();
      break;
    default:
      send_error_message();
  }
}

void loop() 
{
  int new_byte = 0;  
   if (Serial.available() > 0) {
     new_byte = Serial.read();
     //Serial.write(new_byte);
     update_buffer(new_byte);
     if (MAGIC_BYTE1 == (unsigned char)message[MAGIC_BYTE1_OFFSET] && MAGIC_BYTE2 == (unsigned char)message[MAGIC_BYTE2_OFFSET]) {
      handle_command();
     }
  }
}
