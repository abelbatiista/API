-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: webfinaldatos
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `consult`
--

DROP TABLE IF EXISTS `consult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consult` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idpatient` int NOT NULL,
  `date` date NOT NULL,
  `consultreason` varchar(200) NOT NULL,
  `securitynumber` varchar(100) NOT NULL,
  `amount` decimal(13,2) NOT NULL,
  `diagnosis` varchar(100) NOT NULL,
  `note` varchar(200) NOT NULL,
  `image` longblob,
  PRIMARY KEY (`id`),
  KEY `idpatient` (`idpatient`),
  CONSTRAINT `consult_ibfk_1` FOREIGN KEY (`idpatient`) REFERENCES `patient` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consult`
--

LOCK TABLES `consult` WRITE;
/*!40000 ALTER TABLE `consult` DISABLE KEYS */;
INSERT INTO `consult` VALUES (1,1,'2020-09-11','Nothingcare','0201454',50021.00,'Niidea','Pontepaeso',_binary 'nothing.jpg'),(2,1,'2020-10-11','Nothingcare','0201454',50021.00,'Niidea','Pontepaeso',_binary 'nothing.jpg'),(4,1,'2019-10-11','Nothingcare','0201454',50021.00,'Niidea','Pontepaeso',_binary 'nothing.jpg'),(5,2,'2019-10-11','Nothingcare','0201454',50021.00,'Niidea','Pontepaeso',_binary 'nothing.jpg'),(6,2,'2019-10-12','Nothingcare','0201454',50021.00,'Niidea','Pontepaeso',_binary 'nothing.jpg'),(7,6,'2020-11-29','ninguno','4564465',450.00,'Nada','si aveces',_binary 'n.jpg'),(8,6,'2020-11-27','saad','fddf',455.00,'asf','daf',_binary 'sdf');
/*!40000 ALTER TABLE `consult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `CONST_UNIQUE_DOCTOR` (`username`,`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (1,'JohnnyBravo','JohnnyBravo@gmail.com','JohnnyBravo123'),(2,'abel','abel@yahoo.com','abel123'),(3,'Juan','Juan@hotmail.com','Juan123');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `iddoctor` int NOT NULL,
  `cedula` varchar(100) NOT NULL,
  `image` longblob NOT NULL,
  `name` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `bloodtype` varchar(100) NOT NULL,
  `email` varchar(200) NOT NULL,
  `sex` varchar(100) NOT NULL,
  `birthdate` date NOT NULL,
  `allergies` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `CONST_UNIQUE_DOCTOR` (`cedula`,`email`),
  KEY `iddoctor` (`iddoctor`),
  CONSTRAINT `patient_ibfk_1` FOREIGN KEY (`iddoctor`) REFERENCES `doctor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,1,'3243434',_binary 'h33.jpg','manuen','lorssa','o-','abel@hot.es','M','2020-08-07','savila'),(2,1,'335434534',_binary 'h33.jpg','majhfgn','lorssa','o-','abel@hot.es','M','2020-08-07','savila'),(3,1,'445588822',_binary 'h33.jpg','mssdahfgn','sad','o-','abel@hot.es','M','2020-08-09','savila'),(5,2,'40208',_binary 'h.jpg','abelitodembow','demboww','hide','si@gmail.com','masculino','2020-08-11','simucha'),(6,3,'40208663944',_binary 'a.jpg','ABel','Batista','O+','Molondronagrio@hotmail.com','Masculino','2020-11-30','Aine'),(7,3,'353544545',_binary 'h.jpg','JULIO','perez','O+','ABelBatiista@outlook.com','Masculino','2020-11-26','Aine');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-11-30 14:01:48
