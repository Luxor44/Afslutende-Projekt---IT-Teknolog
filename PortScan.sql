CREATE DATABASE port_scanning;

USE port_scanning;

CREATE TABLE scanned_ports (
    id INT NOT NULL AUTO_INCREMENT,
    ports VARCHAR(255) NOT NULL,
    open VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
