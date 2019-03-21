/*
  AnalogReadSerial

  Reads an analog input on pin 0, prints the result to the Serial Monitor.
  Graphical representation is available using Serial Plotter (Tools > Serial Plotter menu).
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogReadSerial
*/

bool on = false;
unsigned long onTime = 0;
unsigned long offTime = 0;
int startCount = 0;
int endCount = 0;
bool waitMode = true;
bool sending = false;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);

  bool isOff = sensorValue > 700 && sensorValue < 800;
// Entering wait mode.
  if (waitMode) {
    if(!isOff) {
      
          // startCount = 500 means start signaled
          if (startCount >= 130) {
              waitMode = false;
//              Serial.println("START SENDING VAL");
              // save event occure timeframe
              onTime = millis();
          } else if (!isOff) {
              startCount++;
              Serial.println(startCount);
          } else {
              startCount = 0;
          }
      
    }

    
  } else {
    if(isOff) {
      if (endCount >= 130) {
          waitMode = true;
//          Serial.println("ENDING SEND");
          offTime = millis();
      } else if (isOff) {
          endCount++;
          Serial.println(endCount);
      } else {
          endCount = 0;
      }
    }
//  Serial.println("IN ELSE");
  }

  if (offTime - onTime > 490 && offTime - onTime < 510) {
    Serial.println("SENDING START");
    // SEND MSG FROM HERE
    offTime = 0;
    onTime = 0;
    }

  
  // print out the value you read:
//  Serial.println(sensorValue);
  delay(1);        // delay in between reads for stability
}
