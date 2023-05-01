CREATE TABLE unsecure_protocols (
  id INT NOT NULL AUTO_INCREMENT,
  mac VARCHAR(50),
  protocol VARCHAR(50),
  unsecure BOOLEAN,
  PRIMARY KEY (id)
);
