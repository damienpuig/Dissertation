#include <CmdMessenger.h>
#include <redisClient.h>
#include <SPI.h>
#include <Ethernet.h>

// Mustnt conflict / collide with our message payload data. Fine if we use base64 library ^^ above
char field_separator = '-';
char command_separator = ';';

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger cmdMessenger = CmdMessenger(Serial, field_separator, command_separator);

int led = 13;
int intervalCoordinatorCheck = 5000;

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress server(192, 168, 1, 20); // Redis Server
RedisClient client(server);
 
enum
{
  kACK              = 1,
  kDATAREQUEST      = 2,
  kDATAANSWER       = 3,
  kNOTIFYAWAKE      = 5,
  kSEND_CMDS_END,
};


 // ------------------ C A L L B A C K  M E T H O D S -------------------------
 void DataCallback()
{
  alert();
  cmdMessenger.sendCmd(kACK, "Data received on coordinator");
  delay(100);
   while ( cmdMessenger.available() )
  {
    char buf[350] = { '\0' };
    cmdMessenger.copyString(buf, 350);
    if(buf[0])
    {
        Serial.println("Publishing to pub/sub channel... ");
    client.startPUBLISH("Arduino1");
    client.sendArg(buf);
    delay(500);
     Serial.println("Published!");
      delay(100);
    }
  }
}

 void AwakeRequestCallback()
{
  cmdMessenger.sendCmd(kACK, "Nodes awaked");
  cmdMessenger.sendCmd(kDATAREQUEST,"Ask for data");
}

// ------------------ D E F A U L T  C A L L B A C K S -----------------------
 
void Ack_root()
{
  // In response to ping. We just send a throw-away Acknowledgement to say "im alive"
  while ( cmdMessenger.available() )
  {
    char buf[350] = { '\0' };
    cmdMessenger.copyString(buf, 350);
    if(buf[0])
    {
       Serial.println(buf);
       delay(100);
    }
  }
}
 
void unknownCmd()
{ 
  //discard potential wrong messages ( logs? )
}
 
// ------------------ E N D  C A L L B A C K  M E T H O D S ------------------

 void hello_coordinator_device()
{
  cmdMessenger.sendCmd(kACK, "Hello from coordinator");
  delay(100);
}
 
 
void setup() {
pinMode(led, OUTPUT);
Serial.begin(9600);

  cmdMessenger.attach(kACK, Ack_root);
  cmdMessenger.attach(unknownCmd);
  cmdMessenger.attach(kDATAANSWER, DataCallback);
  cmdMessenger.attach(kNOTIFYAWAKE, AwakeRequestCallback);
  
  hello_coordinator_device();
  
  Ethernet.begin(mac);
  connection();
}

void connection()
{
  RedisClient tempClient(server);
  client = tempClient;
  client.connect();
  Serial.println("connecting...");
  delay(500);
  
  if(client.connected())
  {
    Serial.println("connected!");
  }
  else
  {
     Serial.println("connection failed!");
  }
}
 
void loop() {
  
  if(!client.connected())
  {
    Serial.println("client unavailable! retrying connection now..");
    delay(500);
    connection();
  }
  
cmdMessenger.feedinSerialData();
delay(intervalCoordinatorCheck);
}

 
 
void alert()
{
  digitalWrite(led, HIGH);
delay(100);
digitalWrite(led, LOW);    
delay(100);     
digitalWrite(led, HIGH);
delay(100);
digitalWrite(led, LOW);    
delay(100);     
}
