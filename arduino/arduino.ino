// the time that a bit is transmitted in (ms)
int TIME_PER_BIT = 58;
// the time that one of the pieces in a start or end pattern is transmitted in (ms)
int TIME_PER_PATTERN_PIECE = TIME_PER_BIT / 2;
// the time that the Arduino should be reading in sensor values at (ms)
int POLLING_RATE = TIME_PER_PATTERN_PIECE / 2;
// the maximum size of any particular message is 34 bytes (2-byte header + 32-byte max payload)
const int MAX_MSG_SIZE = 34;

int START_PATTERN_TIME = 550;

bool inWaitMode = true;
unsigned long previousMillis = 0; //
unsigned long elapsedTime = 0;
bool LEDisOn = false;
unsigned long timeThatLEDHasBeenOn = 0;
unsigned long timeThatLEDHasBeenOff = 0;

unsigned long timeThatLEDHasBeenOnForABit = 0;
unsigned long timeThatLEDHasBeenOffForABit = 0;

// used to store the message
byte message[MAX_MSG_SIZE + 6] ;
int curIdxInMessage = 0;
byte currentByte = 0;
int curBitInByte = 0;
bool currentBit = 0;

void setup() {
  // put your setup code here, to run once:
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

void loop()
{
  // get the elapsed time
  unsigned long currentMillis = millis();
  elapsedTime = currentMillis - previousMillis;
  previousMillis = currentMillis;

  // read the input on analog pin 0
  int sensorValue = analogRead(A0);
  LEDisOn = sensorValue > 600;
//  Serial.println(sensorValue);
//  Serial.print("time on: ");
//  Serial.println(timeThatLEDHasBeenOn);
//  Serial.print("time off: ");
//  Serial.println(timeThatLEDHasBeenOff);
//  Serial.print("elapsed time: ");
//  Serial.println(elapsedTime);

  if (LEDisOn) {
    timeThatLEDHasBeenOn += elapsedTime;
    timeThatLEDHasBeenOff = 0;
    timeThatLEDHasBeenOnForABit += elapsedTime;
    timeThatLEDHasBeenOffForABit = 0;
  } else {
    timeThatLEDHasBeenOff += elapsedTime;
    timeThatLEDHasBeenOn = 0;
    timeThatLEDHasBeenOffForABit += elapsedTime;
    timeThatLEDHasBeenOnForABit = 0;
  }

  // if in wait mode
  if (inWaitMode) {
    waitModeOperations();
  } else {
    receiveMessageOperations();
  }
}

void waitModeOperations() {
  // check for start pattern
  if (timeThatLEDHasBeenOn >= START_PATTERN_TIME) {
    switchModes();
  }

  
}

void receiveMessageOperations() {
  // check for end pattern
  if (timeThatLEDHasBeenOff >= START_PATTERN_TIME) {
    // finalize all message-related stuff and write to the Serial

    // assume that all bits have been correctly written into the final byte

    switchModes();

    // REMOVE THIS AND CHANGE THE SERIAL BACK TO .write
    message[curIdxInMessage] = 0;
    String blah = String((char *) message);
    Serial.println(blah);

//    Serial.println(curIdxInMessage);
//    for (int i = 0; i < curIdxInMessage; i++) {
//      Serial.print(message[i], BIN);
//      Serial.print(" ");
//    }
//    Serial.println();
    curIdxInMessage = 0;
    curBitInByte = 0;
  }

  // check if the LED has been on long enough to count as a 1-bit or off long enough to count as a 0-bit
  if (timeThatLEDHasBeenOnForABit >= TIME_PER_BIT || timeThatLEDHasBeenOffForABit >= TIME_PER_BIT) {
    performBitOperations();
  }

  
}

void performBitOperations() {
  currentBit = 0;
  if (timeThatLEDHasBeenOnForABit >= TIME_PER_BIT) {
    // do we need to reset timeThatLEDHasBeenOn so that is less than TIME_PER_BIT, and therefore has to go through 4 more cycles until it registers again?
    currentBit = 1;
  }
  timeThatLEDHasBeenOnForABit = 0;
  timeThatLEDHasBeenOffForABit = 0;
  
  // left shift the bits in currentByte to make room for the new bit coming in
  currentByte = currentByte << 1;
  currentByte += currentBit;
  curBitInByte++;

  if (curBitInByte == 8) {
    message[curIdxInMessage] = currentByte;
    curIdxInMessage++;
    // reset byte and bit-in-byte index
    currentByte = 0;
    curBitInByte = 0;
  }
}

void switchModes() {
//  Serial.println("Switching Modes");
  inWaitMode = !inWaitMode;
  timeThatLEDHasBeenOff = 0;
  timeThatLEDHasBeenOn = 0;

  timeThatLEDHasBeenOffForABit = 0;
  timeThatLEDHasBeenOnForABit = 0;
}
