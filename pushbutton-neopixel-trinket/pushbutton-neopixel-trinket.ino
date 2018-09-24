#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define LED_PIN 0
#define PI_SIG_PIN 4
#define BUTTON_PIN 2

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
//   NEO_RGBW    Pixels are wired for RGBW bitstream (NeoPixel RGBW products)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(25, LED_PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.
int buttonState=0 ;
int signalState=0;
int buttonToggle=0;

void setup() {
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
  #if defined (__AVR_ATtiny85__)
    if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code

  pinMode(PI_SIG_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT);
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

void loop() {
  signalState = digitalRead(PI_SIG_PIN);
  buttonState = digitalRead(BUTTON_PIN);
  //on button press, toggle the button state
  if (buttonState == HIGH) {
    if (buttonToggle == 0){
      buttonToggle = 1;
    } else {
      buttonToggle = 0;
    }
    delay(1000);
  }
  // if PI signal or button, turn lights on
  if (buttonToggle == 1 || signalState == HIGH) {
    // turn LED on:
    colorWipe(strip.Color(255, 255, 255, 255), 50); // White RGBW
  } else {
    // turn LED off:
    colorWipe(strip.Color(0, 0, 0, 255), 50); // off RGBW
  } 

}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    
  }
  strip.show();
    delay(wait);
}


