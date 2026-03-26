DROP TABLE IF EXISTS Stocker;
DROP TABLE IF EXISTS Partager;
DROP TABLE IF EXISTS Comporter;
DROP TABLE IF EXISTS Certif;
DROP TABLE IF EXISTS Type;
DROP TABLE IF EXISTS Machine;
DROP TABLE IF EXISTS Modele;
DROP TABLE IF EXISTS Extra;
DROP TABLE IF EXISTS Composer;
DROP TABLE IF EXISTS Assembler;
DROP TABLE IF EXISTS Plats;
DROP TABLE IF EXISTS Repas;
DROP TABLE IF EXISTS Club;
DROP TABLE IF EXISTS Adresses;
DROP TABLE IF EXISTS Ordre;
DROP TABLE IF EXISTS Tenrac;
DROP TABLE IF EXISTS Historique;
DROP TABLE IF EXISTS Rang;
DROP TABLE IF EXISTS Dignite;
DROP TABLE IF EXISTS Titre;
DROP TABLE IF EXISTS Grade;
DROP TABLE IF EXISTS Organisation;
DROP TABLE IF EXISTS Ingredient;
DROP TABLE IF EXISTS Legume;
DROP TABLE IF EXISTS Sauce;
DROP TABLE IF EXISTS Composant;
DROP TABLE IF EXISTS Organisme;

CREATE TABLE Machine(
   id_Machine INTEGER PRIMARY KEY,
   nom VARCHAR(50) NOT NULL
);

CREATE TABLE Modele(
   id_Modele INTEGER PRIMARY KEY,
   Entretien VARCHAR(50) NOT NULL,
   Periodicite VARCHAR(50) NOT NULL
);

CREATE TABLE Organisme(
   nom_O VARCHAR(50) PRIMARY KEY,
   Numero_SIRET VARCHAR(14) UNIQUE
);

CREATE TABLE Composant(
   id_Composant INTEGER PRIMARY KEY,
   nom_ingredient VARCHAR(50) NOT NULL,
   type_ingredient VARCHAR(50) NOT NULL,
   legume INTEGER NOT NULL, 
   alergene VARCHAR(50)
);

CREATE TABLE Sauce(
   Nom VARCHAR(50) PRIMARY KEY
);

CREATE TABLE Legume(
   id_Composant INTEGER PRIMARY KEY,
   verifier INTEGER NOT NULL,
   FOREIGN KEY(id_Composant) REFERENCES Composant(id_Composant)
);

CREATE TABLE Ingredient(
   id_I INTEGER PRIMARY KEY,
   id_Composant INTEGER NOT NULL UNIQUE,
   FOREIGN KEY(id_Composant) REFERENCES Composant(id_Composant)
);

CREATE TABLE Organisation(
   id_Organisation INTEGER PRIMARY KEY
);

CREATE TABLE Grade(
   nom_G VARCHAR(50) PRIMARY KEY,
   nom_G_1 VARCHAR(50),
   FOREIGN KEY(nom_G_1) REFERENCES Grade(nom_G)
);

CREATE TABLE Titre(
   nom_T VARCHAR(50) PRIMARY KEY,
   nom_T_1 VARCHAR(50),
   FOREIGN KEY(nom_T_1) REFERENCES Titre(nom_T)
);

CREATE TABLE Dignite(
   nom_D VARCHAR(50) PRIMARY KEY,
   nom_D_1 VARCHAR(50),
   FOREIGN KEY(nom_D_1) REFERENCES Dignite(nom_D)
);

CREATE TABLE Rang(
   nom_R VARCHAR(50) PRIMARY KEY,
   nom_R_1 VARCHAR(50),
   FOREIGN KEY(nom_R_1) REFERENCES Rang(nom_R)
);

CREATE TABLE Historique(
   id_H INTEGER PRIMARY KEY,
   date_ DATE NOT NULL,
   id_Machine INTEGER NOT NULL UNIQUE,
   FOREIGN KEY(id_Machine) REFERENCES Machine(id_Machine)
);

CREATE TABLE Tenrac(
   id_T INTEGER PRIMARY KEY,
   nom VARCHAR(50) NOT NULL,
   courriel VARCHAR(100) UNIQUE NOT NULL,
   num_tel VARCHAR(20) NOT NULL,
   adr VARCHAR(100) NOT NULL,
   RFID VARCHAR(50) UNIQUE,
   id_Organisation INTEGER NOT NULL,
   nom_O VARCHAR(50) NOT NULL,
   nom_R VARCHAR(50),
   nom_G VARCHAR(50) NOT NULL,
   nom_T VARCHAR(50),
   nom_D VARCHAR(50),
   FOREIGN KEY(id_Organisation) REFERENCES Organisation(id_Organisation),
   FOREIGN KEY(nom_O) REFERENCES Organisme(nom_O),
   FOREIGN KEY(nom_R) REFERENCES Rang(nom_R),
   FOREIGN KEY(nom_G) REFERENCES Grade(nom_G),
   FOREIGN KEY(nom_T) REFERENCES Titre(nom_T),
   FOREIGN KEY(nom_D) REFERENCES Dignite(nom_D)
);

CREATE TABLE Ordre(
   nom_Ordre VARCHAR(50) PRIMARY KEY,
   id_Organisation INTEGER NOT NULL UNIQUE,
   FOREIGN KEY(id_Organisation) REFERENCES Organisation(id_Organisation)
);

CREATE TABLE Adresses(
   Nom_A VARCHAR(100) PRIMARY KEY,
   nom_Ordre VARCHAR(50) NOT NULL,
   FOREIGN KEY(nom_Ordre) REFERENCES Ordre(nom_Ordre)
);

CREATE TABLE Plats(
   id_P INTEGER PRIMARY KEY,
   Raclette VARCHAR(50) NOT NULL,
   id_Composant INTEGER,
   FOREIGN KEY(id_Composant) REFERENCES Legume(id_Composant)
);

CREATE TABLE Club(
   nom_Club VARCHAR(50) PRIMARY KEY,
   nom_Ordre VARCHAR(50),
   id_Organisation INTEGER NOT NULL UNIQUE,
   FOREIGN KEY(nom_Ordre) REFERENCES Ordre(nom_Ordre),
   FOREIGN KEY(id_Organisation) REFERENCES Organisation(id_Organisation)
);

CREATE TABLE Repas(
   Id_R INTEGER PRIMARY KEY,
   Nom VARCHAR(50) NOT NULL,
   Date_ DATETIME NOT NULL,
   Nom_A VARCHAR(100) NOT NULL,
   FOREIGN KEY(Nom_A) REFERENCES Adresses(Nom_A)
);

CREATE TABLE Partager(
   id_T INTEGER,
   Id_R INTEGER,
   PRIMARY KEY(id_T, Id_R),
   FOREIGN KEY(id_T) REFERENCES Tenrac(id_T),
   FOREIGN KEY(Id_R) REFERENCES Repas(Id_R)
);

CREATE TABLE Comporter(
   Id_R INTEGER,
   id_P INTEGER,
   PRIMARY KEY(Id_R, id_P),
   FOREIGN KEY(Id_R) REFERENCES Repas(Id_R),
   FOREIGN KEY(id_P) REFERENCES Plats(id_P)
);

CREATE TABLE Certif(
   id_T INTEGER,
   id_Machine INTEGER,
   PRIMARY KEY(id_T, id_Machine),
   FOREIGN KEY(id_T) REFERENCES Tenrac(id_T),
   FOREIGN KEY(id_Machine) REFERENCES Machine(id_Machine)
);

CREATE TABLE Type(
   id_Machine INTEGER,
   id_Modele INTEGER,
   PRIMARY KEY(id_Machine, id_Modele),
   FOREIGN KEY(id_Machine) REFERENCES Machine(id_Machine),
   FOREIGN KEY(id_Modele) REFERENCES Modele(id_Modele)
);

CREATE TABLE Assembler(
   id_Composant INTEGER,
   Nom VARCHAR(50),
   PRIMARY KEY(id_Composant, Nom),
   FOREIGN KEY(id_Composant) REFERENCES Composant(id_Composant),
   FOREIGN KEY(Nom) REFERENCES Sauce(Nom)
);

CREATE TABLE Composer(
   id_P INTEGER,
   id_I INTEGER,
   PRIMARY KEY(id_P, id_I),
   FOREIGN KEY(id_P) REFERENCES Plats(id_P),
   FOREIGN KEY(id_I) REFERENCES Ingredient(id_I)
);

CREATE TABLE Extra(
   id_P INTEGER,
   Nom VARCHAR(50),
   PRIMARY KEY(id_P, Nom),
   FOREIGN KEY(id_P) REFERENCES Plats(id_P),
   FOREIGN KEY(Nom) REFERENCES Sauce(Nom)
);

CREATE TABLE Stocker(
   id_Organisation INTEGER,
   id_H INTEGER,
   PRIMARY KEY(id_Organisation, id_H),
   FOREIGN KEY(id_Organisation) REFERENCES Organisation(id_Organisation),
   FOREIGN KEY(id_H) REFERENCES Historique(id_H)
);