#include "pitches.h"
 int button = 4;
int speakerpin = 5; //스피커가 연결된 디지털핀 설정
 
//음계 데이터 (24개)
int melody[] = {NOTE_G7,NOTE_G7,NOTE_A7,NOTE_A7,NOTE_G7,
                NOTE_G7,NOTE_E7,NOTE_G7,NOTE_G7,NOTE_E7,
                NOTE_E7,NOTE_D7,NOTE_G7,NOTE_G7,NOTE_A7,
                NOTE_A7,NOTE_G7,NOTE_G7,NOTE_E7,NOTE_G7,
                NOTE_E7,NOTE_D7,NOTE_E7,NOTE_C7};
//음의길이, 4:4분음표, 2:2분음표
int noteDurations[] = {4,4,4,4,4,4,2,4,4,4,4,1,4,4,4,4,4,4,2,4,4,4,4,1};
int sw=0;
void setup() {
   pinMode(button,INPUT); 
}
 
void loop() {
  sw=digitalRead(button);
  if(sw==1){
    for (int thisNote = 0; thisNote < 24; thisNote++)
  {
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(speakerpin, melody[thisNote], noteDuration); //소리를 낸다.
    int pauseBetweenNotes = noteDuration * 1.00;      //delay 계산식
    delay(pauseBetweenNotes);                         //delay
     noTone(speakerpin);                               //대상핀 출력 중단
  }
  }
  else noTone(5);
}
