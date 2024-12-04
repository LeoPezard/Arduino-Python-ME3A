#include <Servo.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
Servo microservo;// Nom du servomoteur utilisé dans le projet

// Les broches
const int thermistancePin = A0;
const int ldrPin = A1;
const int panelPin = A2;
const int servoPin = 9;
const int ventilPin = 7;

// Définir les valeurs constantes
const float desiredVoltage = 2.5;// Tension cible en volts pour le panneau
const int R1 = 4700;// Valeur de la résistance du pont diviseur de la thermistance

// Définition des valeurs pouvant varier par la suite
int servoAngle = 180;
int panelLux;
float volt, resistance, temp, panelVoltage, ldrVoltage;
int lux, ldrValue, panelValue, thermiValue;

// Définition des couleurs pour la led RGB (plutot define que int car je crée 
// des substitutions textuelles, pas de mémoire alouée aux variables)
#define RED 13
#define GRN 8
#define BLUE 10

// Initialisation des entrées/sorties de chaque élément du montage
void setup() {
  Serial.begin(9600);
  microservo.attach(servoPin);
  microservo.write(servoAngle);// angle de départ
  // Pins de la led RGB
  pinMode(RED, OUTPUT);
  pinMode(GRN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  // Pin du ventilateur
  pinMode(ventilPin, OUTPUT);
  // Configuration de l'écran
  lcd.begin(16,2);// 16 colonnes et 2 lignes
}


/// Dans mon code j'ai décidé d'attribuer une fonction par composant
/// Je trouve cela plus facile lorsqu'un problème apparait sur un composant 
/// je sais directement où aller le corriger.

// Fonction pour la led RGB
void colors() { // allume en vert si la température est inférieure à 25 degrés et la luminosité<300 lux
  if(temp<=25 && lux<=300){
    digitalWrite(RED, LOW);
    digitalWrite(GRN, HIGH);
    digitalWrite(BLUE, LOW);}
  else if(temp>25 && lux> 300){ // Si les deux données sont au dessus de valeurs critiques --> allumer la led en rouge
    digitalWrite(RED, HIGH);
    digitalWrite(GRN, LOW);
    digitalWrite(BLUE, LOW);}
  else{ // Sinon en bleu
    digitalWrite(RED, LOW);
    digitalWrite(GRN, LOW);
    digitalWrite(BLUE, HIGH);}
}

//Fonction pour la photorésistance
void luminosite(){
  ldrValue = analogRead(ldrPin); // Lecture de la valeur analogique de la tension
  ldrVoltage = ldrValue * 5.0 / 1023.0; // Conversion en volts
  lux = (int)(ldrVoltage*300/2.5); // Conversion en lux (échelle 300lux<-->2,5V)
  }

// Fonction pour le panneau solaire
void photovolt(){
  panelValue = analogRead(panelPin);
  panelVoltage = panelValue * 5.0 / 1023.0; // conversion de la tension reçue en volt
  panelLux = panelVoltage*300/2,5;// 2,5V <-->300 lux
}

// Fonction pour diriger le servomoteur
void servomoteur(){
  if (panelVoltage < desiredVoltage) {
    servoAngle = constrain(servoAngle + 5, 0, 180); // constrain attribue la valeur servoAngle+5 à servoAngle à condition qu'elle soit comprise entre 0 et 180
  } else if (panelVoltage > desiredVoltage) {
    servoAngle = constrain(servoAngle - 5, 0, 180);
  }
  microservo.write(servoAngle);//Tourner le servomoteur à l'angle donné en paramètre (donc ici on ajoute ou enlève 5 degrès a chaque boucle)
}

// Fonction pour la thermistance (vue en TP)
void thermistance(){
  thermiValue = analogRead(thermistancePin);
  volt = thermiValue*(5.0/1023.0);
  resistance = R1*((5.0/volt)-1); // Valeur de la résistance grâce au pont diviseur de tension 
  temp = 22.3*log(resistance/4700.0)+25; // Conversion de la valeur de la résistance en température
}

// Fonction pour le ventilateur
void vent(){
  if(temp>25){digitalWrite(ventilPin, HIGH);} // Allumer le ventilateur si le température est supérieure à 25 degrés
  else{digitalWrite(ventilPin, LOW);} // Sinon l'éteindre
}


// Création d'un caractère personnalisé pour "θ", pour l'afficher dans l'écran LCD
// J'ai eu du mal à afficher correctement ce caractère, cette méthode marchait corrrectement 
// c'est pourquoi je l'ai utilisée même si je la trouve plutôt brouillon...
byte theta[8] = { 
  B001110,
  B010001,
  B010001,
  B011111,
  B010001,
  B010001,
  B010001,
  B001110
};

//Fonction de l'écran LCD 
void ecranLCD(){// Affichage des valeurs ainsi que de leur légende
  lcd.clear();
  lcd.setCursor(0,0);// Placer le curseur à l'origine (1ere colonne,1ere ligne)
  lcd.print("L: ");
  lcd.print(lux);
  lcd.print("  T: ");
  lcd.print(temp);
  lcd.setCursor(0,1); //Placer le curseur à la 1ere colonne et 2eme ligne 
  lcd.print("V: ");
  lcd.print(panelVoltage);
  lcd.print(" ");
  lcd.createChar(0, theta);
  lcd.write((byte)0); // theta "θ"
  lcd.print(": ");
  lcd.print(servoAngle);
}


void loop() { // Boucle infinie qui va exécuter toutes les fonctions à la suite
  luminosite();
  photovolt();
  servomoteur();
  thermistance();
  colors();
  vent();
  ecranLCD();
  // Envoi des données sur la liaison série pour les récupérer sur python ensuite
  Serial.print(lux);
  Serial.print(",");
  Serial.print(temp);
  Serial.print(",");
  Serial.print(panelVoltage);
  Serial.print(",");
  Serial.println(servoAngle);

  delay(400); // Attente avant la prochaine itération
}


