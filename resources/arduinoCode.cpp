#include <Adafruit_NeoPixel.h>
#include <stdint.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

//Global variables
#define SIG1                38          // using pin 38 for signal 1 (mux array 1)
#define SIG2                51          // using pin 51 for data signal 2 (mux array 2)
#define BRIGHTNESS          128         // level of brightness of all LEDs (8 bit value --> [0, 255])const int rings = 17;
const uint8_t rings = 17;
const uint8_t crystals = 22;
const uint8_t pixel = 24;

const uint8_t muxX = 16;
const uint8_t muxY = 16;


//-------------------------INSTANTIATE LED RING OBJECT-------------------------//
// Parameter 1 = number of pixels in ring
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
Adafruit_NeoPixel muxA = Adafruit_NeoPixel(24, SIG1, NEO_KHZ800 + NEO_GRB);
Adafruit_NeoPixel muxB = Adafruit_NeoPixel(24, SIG2, NEO_KHZ800 + NEO_GRB);


uint32_t oldValuesA[muxX][muxY];
uint32_t oldValuesB[muxX][muxY];


// Define and instantiate demux select switch pin arrays (Colored wires that are the output of Arduino to control board)
uint8_t innerMux1[4] = {22, 23, 24, 25};
uint8_t outerMux1[4] = {26, 27, 28, 29};
uint8_t innerMux2[4] = {30, 31, 32, 33};
uint8_t outerMux2[4] = {34, 35, 36, 37};

const int buffer_len = muxX * muxY * 2 * 3;
//const int buffer_len = 15;
uint8_t inBuffer[buffer_len];

// Display Functions
void displayBuffer();

//----------------------------------------------SETUP-----------------------------------------------//
void setup(){
    // Configure digital pins for mux selector switches as outputs
    for(int i = 3; i >= 0; i--){
        pinMode(innerMux1[i], OUTPUT);
        pinMode(outerMux1[i], OUTPUT);
        pinMode(innerMux2[i], OUTPUT);
        pinMode(outerMux2[i], OUTPUT);

        digitalWrite(innerMux1[i], LOW);
        digitalWrite(outerMux1[i], LOW);
        digitalWrite(innerMux2[i], LOW);
        digitalWrite(outerMux2[i], LOW);
    }

    muxA.begin();                      // Start higher LED rings
    muxB.begin();                      // Start lower LED rings
    muxA.setBrightness(BRIGHTNESS);    // Set higher LEDs brightness
    muxB.setBrightness(BRIGHTNESS);    // Set higher LEDs brightness
    muxA.show();                       // Initialize all pixels to 'off'
    muxB.show();                       // Initialize all pixels to 'off'


    // Sets up serial connection
    Serial.begin(115200);
    Serial.setTimeout(1);

    for(int i = 0; i < buffer_len; i++){
        inBuffer[i] = 0;
    }
    //displayBuffer(innerMux1, outerMux1, oldValuesA, muxA, 0, true);
    //displayBuffer(innerMux2, outerMux2, oldValuesB, muxB, buffer_len / 2, true);
}


//----------------------------------------------LOOP-----------------------------------------------//

int index = 0;
bool upd = false;
bool ran = false;
void loop(){
    while(Serial.available() > 0){
        ran = true;
        int in = Serial.read();
        if(in != -1){
            inBuffer[index] = in;
            index++;
            if(index >= buffer_len){
                index = 0;
                upd = true;
            }
        } else{
            break;
        }
    }
    if(ran){
        //Serial.write(buffer, buffer_len);
        ran = false;
    }
    if(upd){
        Serial.write(inBuffer, buffer_len);
        displayBuffer('a', 0, true);
        displayBuffer('b', buffer_len / 2, true);
        upd = false;
    }
}

// --------------------------------------------- FUNCTIONS -----------------------------------------//

//Display Functions
void displayBuffer(char muxSelect, int offset, bool over){
    //void displayBuffer(uint8_t innerMux[4], uint8_t outerMux[4], uint32_t oldValues[muxX][muxY], Adafruit_NeoPixel mux, int offset, bool over){
    uint8_t* innerMux;
    uint8_t* outerMux;
    Adafruit_NeoPixel* mux;
    if(muxSelect == 'a'){
        innerMux = innerMux1;
        outerMux = outerMux1;
        mux = &muxA;
    } else{
        innerMux = innerMux2;
        outerMux = outerMux2;
        mux = &muxB;
    }

    uint32_t color;
    int index;
    for(int i = 0; i < muxX; i++){
        digitalWrite(innerMux[0], bitRead(i, 0));
        digitalWrite(innerMux[1], bitRead(i, 1));
        digitalWrite(innerMux[2], bitRead(i, 2));
        digitalWrite(innerMux[3], bitRead(i, 3));

        for(int j = 0; j < muxY; j++){
            index = 3 * (i * muxX + j) + offset;
            color = muxA.Color(inBuffer[index], inBuffer[index + 1], inBuffer[index + 2]);

            if((muxSelect == 'a' && oldValuesA[i][j] != color) || (muxSelect == 'b' && color != oldValuesB[i][j]) || over || true){
                digitalWrite(outerMux[0], bitRead(j, 0));
                digitalWrite(outerMux[1], bitRead(j, 1));
                digitalWrite(outerMux[2], bitRead(j, 2));
                digitalWrite(outerMux[3], bitRead(j, 3));

                (*mux).fill(color);
                if(muxSelect == 'a'){
                    oldValuesA[i][j] = color;
                } else{
                    oldValuesB[i][j] = color;
                }

                (*mux).show();
            }
        }
    }
}