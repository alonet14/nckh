#include <Wire.h>
#include <Adafruit_MLX90614.h>

Adafruit_MLX90614 mlx = Adafruit_MLX90614(); //-> mlx declaration
int count = -2;
float sum;
//==========================================================================================setup()
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
 
  mlx.begin();
  
}
//==========================================================================================
void loop() {
  // put your main code here, to run repeatedly:

  //------------------------------------------making the temperature in Celsius
  if ((count <=20) && (count>=0)){
    sum += mlx.readObjectTempC();
    
    Serial.print("Target : ");
    Serial.print(mlx.readObjectTempC());
    Serial.println(" C");
    Serial.println("");

    if(count == 20){
      float result = sum/(count+1);
      Serial.print("Result: ");
      Serial.println(result);
      Serial.println("=========");
    }
    
  } else{
    Serial.println("Done");  
  }
  //------------------------------------------
  count++;
  delay(500);
}
