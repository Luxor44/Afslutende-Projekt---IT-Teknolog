CREATE DATABASE MasterDatabase;

USE MasterDatabase;

CREATE TABLE login (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    phonenumber VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
)

CREATE TABLE PortScan (
   id INT NOT NULL AUTO_INCREMENT,
   IpAdress VARCHAR(50) NOT NULL,
   MacAdress VARCHAR(50) NOT NULL,
   Ports json NOT NULL,
   PRIMARY KEY (id)
)
 
 CREATE TABLE ProtocolScan (
  id INT NOT NULL AUTO_INCREMENT,
  IpAdress VARCHAR(50) NOT NULL,
  MacAdress VARCHAR(50) NOT NULL,
  SSLTSL json NOT NULL,
  HeartBleedVulnability json NOT NULL,
  Protocols json NOT NULL,
  PRIMARY KEY (id)
  
);
 
