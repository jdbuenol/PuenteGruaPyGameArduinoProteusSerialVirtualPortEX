#include <LiquidCrystal.h>

int STRETCH = 13;
int COLLAPSE = 12;
int RIGHT = 11;
int LEFT = 10;
int PICK_DROP = 9;
int EXIT = 21;

int D4 = A4;
int D5 = A5;
int D6 = A6;
int D7 = A7;
int E = A0;
int RS = A1;

bool stretch_pressed = false;
bool collapse_pressed = false;
bool right_pressed = false;
bool left_pressed = false;
bool exit_pressed = false;
bool pick_drop_pressed = false;

float timer = millis();
String output = "";
int coords_x = 0;
int coords_y = 0;

LiquidCrystal lcd(RS, E, D4, D5, D6, D7);

void setup() {
  lcd.begin(16, 2);
  lcd.setCursor(8,0);
  lcd.println("LOL");
  Serial.begin(9600);
  pinMode(STRETCH, INPUT);
  pinMode(LEFT, INPUT);
  pinMode(RIGHT, INPUT);
  pinMode(COLLAPSE, INPUT);
  pinMode(EXIT, INPUT);
  pinMode(PICK_DROP, INPUT);
}

void loop() {
  if(millis() - timer > 50 and output.length() != 0){
    Serial.println(output);
    output = "";
    timer = millis();
  }
  if(digitalRead(STRETCH) and ! stretch_pressed){
    output = "STRETCH";
    stretch_pressed = true;
  }
  if(digitalRead(LEFT) and ! left_pressed){
    output = "LEFT";
    left_pressed = true;
  }
  if(digitalRead(RIGHT) and ! right_pressed){
    output = "RIGHT";
    right_pressed = true;
  }
  if(digitalRead(COLLAPSE) and ! collapse_pressed){
    output = "COLLAPSE";
    collapse_pressed = true;
  }
  if(digitalRead(EXIT) and ! exit_pressed){
    output = "EXIT";
    exit_pressed = true;
  }
  if(digitalRead(PICK_DROP) and ! pick_drop_pressed){
    output = "PICK";
    pick_drop_pressed = true;
  }
  if(! digitalRead(STRETCH)) stretch_pressed = false;
  if(! digitalRead(LEFT)) left_pressed = false;
  if(! digitalRead(RIGHT)) right_pressed = false;
  if(! digitalRead(COLLAPSE)) collapse_pressed = false;
  if(! digitalRead(EXIT)) exit_pressed = false;
  if(! digitalRead(PICK_DROP)) pick_drop_pressed = false;
}

void serialEvent(){
  while(Serial.available()){
    lcd.clear();
    lcd.setCursor(8, 0);
    String adrian_es_gei = Serial.readString();
    lcd.print(adrian_es_gei);
  }
}
