#include <LiquidCrystal.h>
String cmdData = NULL;				 // a string to hold incoming data
boolean stringComplete = false;
LiquidCrystal lcd(2, 3, 4, 5, 6, 7); 
void setup()	
{
	Serial.begin(9600);				// open connection to ID-12LA
	cmdData.reserve(200);
	pinMode(13, OUTPUT);
	digitalWrite(13, HIGH);			// reserve some data for the serialEvent read
	pinMode(10, OUTPUT);
	pinMode(8, OUTPUT);
	digitalWrite(8, HIGH);
	lcd.begin(16, 2);
	lcd.print("Initializing...");
	tone(10, 1600, 200);
}

void loop() 
{
if (stringComplete) {
	if (cmdData.startsWith("BEEP")) {
		tone(10, 900, 300);
		cmdData = NULL;
		stringComplete = false;
	}
	if (cmdData.startsWith("SADBEEP")) {
        tone(10, 400, 300);
        cmdData = NULL;
        stringComplete = false;
    }
	if (cmdData.startsWith("ROW0")) {
		lcd.setCursor(0, 0);
		stringComplete = false;
		cmdData = NULL;
	}
	if (cmdData.startsWith("ROW1")) {
		lcd.setCursor(0, 1);
		stringComplete = false;
		cmdData = NULL;
	}
	 if (cmdData.startsWith("CLEAR")) {
		lcd.clear();
		stringComplete = false;
		cmdData = NULL;
	}
	if (cmdData.startsWith("BL1")) {
	 digitalWrite(8, HIGH);
	}
	if (cmdData.startsWith("BL0")) {
	 digitalWrite(8, LOW);
	}
	if (cmdData.startsWith("W")) {
		char bytes[16];
		cmdData = cmdData.substring(1);
		cmdData.toCharArray(bytes, 17); // lcd.write needs data in the form of a char array
		lcd.write(bytes);
		stringComplete = false;
		cmdData = NULL;
	}
	else {
		stringComplete = false;
		cmdData = NULL;
	}
}
}

void serialEvent() {
	while (Serial.available()) {
		char inChar = (char)Serial.read();
		if (inChar == '\n') {
			stringComplete = true;
		}
		else cmdData += inChar;
	}
}

