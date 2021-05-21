#include <Wire.h>
#include <Adafruit_MLX90614.h>
Adafruit_MLX90614 mlx = Adafruit_MLX90614();        //-> mlx declaration

static const int led = 4;                           // Biến khai báo chân đèn LED được nối vào Arduino
static const int buttonPin = 2;                    
int buttonStatePrevious = LOW;                      // previousstate of the switch

unsigned long minButtonLongPressDuration = 2000;    
unsigned long buttonLongPressMillis;                // Thoi gian khi nhan nut
bool buttonStateLongPress = false;                  // Dung neu an lau

const int intervalButton = 50;                      // Thoi gian giua 2 lan do trang thai nut
unsigned long previousButtonMillis;                 // Timestamp cua lan doc gan nhat

unsigned long buttonPressDuration;                  // Thoi gian nut duoc nhan
static boolean ledStatus = 0;                       // tương tự với LOW - mặc định đèn sẽ tắt
//// GENERAL ////

unsigned long currentMillis;          // Gia tri luu tru thoi gian tu khi Arduino bat dau

void setup() {
  Serial.begin(9600);   
  mlx.begin();              
  
  pinMode(led,OUTPUT);   // Đặt chân LED là OUTPUT - hiển nhiên rồi
  pinMode(buttonPin, INPUT);       
    
//  Serial.println("Press button");

}

// Function for reading the button state
// Hàm cho đọc trạng thái chân
void readButtonState() {

  // If the difference in time between the previous reading is larger than intervalButton
  // Nếu có sự khác biệt giữa lần đọc trước lớn hơn khoảng thời gian
  if(currentMillis - previousButtonMillis > intervalButton) {
    
    // Read the digital value of the button (LOW/HIGH)
    // Đọc giá trị của button 
    int buttonState = digitalRead(buttonPin);    

    // If the button has been pushed AND
    // If the button wasn't pressed before AND
    // IF there was not already a measurement running to determine how long the button has been pressed
    
    // Nếu nút được nhấn và nút không được nhấn trước 
    // và chưa có phép đo nào đang chạy để xác định nút đã được nhấn trong bao lâu
    
    if (buttonState == HIGH && buttonStatePrevious == LOW && !buttonStateLongPress) {
      buttonLongPressMillis = currentMillis;
      buttonStatePrevious = HIGH;
      
//      Serial.println("Button pressed");

    }

    // Calculate how long the button has been pressed
    buttonPressDuration = currentMillis - buttonLongPressMillis;

    // If the button is pressed AND
    // If there is no measurement running to determine how long the button is pressed AND
    // If the time the button has been pressed is larger or equal to the time needed for a long press
    if (buttonState == HIGH && !buttonStateLongPress && buttonPressDuration >= minButtonLongPressDuration) {
      buttonStateLongPress = true;

//      Serial.println("Button long pressed");

      ledStatus = 1;
      digitalWrite(led,ledStatus); // Xuất giá trị của đèn LED ra đèn LED

//      Serial.println(ledStatus);

    }
      
    // If the button is released AND
    // If the button was pressed before
    if (buttonState == LOW && buttonStatePrevious == HIGH) {
      buttonStatePrevious = LOW;
      buttonStateLongPress = false;

//      Serial.println("Button released");
      
      // If there is no measurement running to determine how long the button was pressed AND
      // If the time the button has been pressed is smaller than the minimal time needed for a long press
      // Note: The video shows:
      //       if (!buttonStateLongPress && buttonPressDuration < minButtonLongPressDuration) {
      //       since buttonStateLongPress is set to FALSE on line 75, !buttonStateLongPress is always TRUE
      //       and can be removed.
      if (buttonPressDuration < minButtonLongPressDuration) {

//        Serial.println("Button pressed shortly");

      }
      
//      Serial.println("=========");

    }
    
    // store the current timestamp in previousButtonMillis
    previousButtonMillis = currentMillis;
  
  }
  
}

void loop() {
  int count = 1;
  float sum = 0;
  currentMillis = millis();    // store the current time
  readButtonState();           // read the button state
  digitalWrite(led,ledStatus); // Xuất giá trị của đèn LED ra đèn LED
  while(ledStatus){
    if(count == 1){

//      Serial.println("Wait 2 second");

      delay(3000);
    }
    if ((count <=20) && (count>=1)){
      sum += mlx.readObjectTempC();
    
//      Serial.print("Target : ");
//      Serial.println(mlx.readObjectTempC());
//      Serial.println(" C");
//      Serial.println("");
    }
    if(count == 20){
      float result = sum/(count);

//      Serial.print("Result: ");
      
      Serial.println(result);
      
//      Serial.println("=========");
      ledStatus = 0;
    }
    count++;
    delay(200);
  }
}
