-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: JobKonnect
-- ------------------------------------------------------
-- Server version	8.0.37-0ubuntu0.22.04.3

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
-- Table structure for table `Applications`
--

DROP TABLE IF EXISTS `Applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `employer_id` int NOT NULL,
  `user_id` int NOT NULL,
  `resume` varchar(255) DEFAULT NULL,
  `cover_letter` varchar(255) DEFAULT NULL,
  `status` enum('submitted','under review','rejected','accepted') DEFAULT 'submitted',
  `submitted_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `years_of_experience` int DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `school_name` varchar(100) NOT NULL,
  `portfolio` varchar(255) NOT NULL,
  `skills` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `job_id` (`job_id`),
  KEY `employer_id` (`employer_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `Applications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `Jobs` (`id`),
  CONSTRAINT `Applications_ibfk_2` FOREIGN KEY (`employer_id`) REFERENCES `Users` (`id`),
  CONSTRAINT `Applications_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Applications`
--

LOCK TABLES `Applications` WRITE;
/*!40000 ALTER TABLE `Applications` DISABLE KEYS */;
INSERT INTO `Applications` VALUES (10,10,4,2,'http://localhost:5000/uploads/Transcript_-_422468_-_Tatenda_TatendaTorerwa_1.pdf','http://localhost:5000/uploads/Transcript_-_422468_-_Tatenda_TatendaTorerwa_1.pdf','submitted','2024-07-18 08:06:13','2024-07-18 08:06:13',6,'Tatenda Torerwa','','https://github.com/Evarmedia/Jobkonnect-frontend','SQL, Python, Data Analysis'),(11,11,1,2,'http://localhost:5000/uploads/New_Uploaded_Resume.pdf','http://localhost:5000/uploads/cv_mishak.8fb98dd1ee459b3090c4_1.pdf','accepted','2024-07-18 08:45:09','2024-07-18 09:07:33',5,'Tatenda Torerwa','','https://github.com/Evarmedia/Jobkonnect-frontend','SQL, Python, Data Analysis'),(13,14,1,2,'http://localhost:5000/uploads/New_Uploaded_Resume.pdf','http://localhost:5000/uploads/cv_mishak.8fb98dd1ee459b3090c4_2.pdf','submitted','2024-07-18 09:09:01','2024-07-18 09:09:01',5,'Tatenda Torerwa','','https://github.com/Evarmedia/Jobkonnect-frontend','SQL, Python, Data Analysis');
/*!40000 ALTER TABLE `Applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Jobs`
--

DROP TABLE IF EXISTS `Jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `requirements` text NOT NULL,
  `employer_id` int NOT NULL,
  `salary` varchar(50) DEFAULT NULL,
  `location` varchar(100) NOT NULL,
  `job_type` enum('full-time','part-time','contract') DEFAULT NULL,
  `application_deadline` date DEFAULT NULL,
  `skills_required` text NOT NULL,
  `preferred_qualifications` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `employer_id` (`employer_id`),
  CONSTRAINT `Jobs_ibfk_1` FOREIGN KEY (`employer_id`) REFERENCES `Users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Jobs`
--

LOCK TABLES `Jobs` WRITE;
/*!40000 ALTER TABLE `Jobs` DISABLE KEYS */;
INSERT INTO `Jobs` VALUES (10,'Data Analyst','Analyze data to help make informed business decisions.','Bachelor\'s degree in Statistics, Mathematics, or related field. Proficiency in SQL and Excel.',4,'Negotiable','Cairo, Egypt','contract','2024-08-20','SQL, Excel','Experience with data visualization tools like Tableau.','2024-07-16 15:35:13','2024-07-16 15:35:13'),(11,'social media manager','social media manager','social media manager',1,'10000','Westlands, Nairobi, Kenya','part-time','2024-07-12','csss, html, javascript','phd','2024-07-18 08:41:12','2024-07-18 08:41:12'),(14,'Backend developer','Backend developer','Backend developer',1,'20000','Westlands, Nairobi, Kenya','part-time','2024-07-31','python, c, node.js','phd','2024-07-18 09:08:19','2024-07-18 09:08:19');
/*!40000 ALTER TABLE `Jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `role` enum('job_seeker','employer') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  `contact_info` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'techsolutions_sa','$2b$12$NAhyQuYD5t4MlHtk0b3AGeVn2mFQvidLZRiFfS1Z2Js23fvVu2aHC','info@techsolutions.co.za','employer','2024-07-14 12:25:56','2024-07-14 12:25:56',NULL,NULL,'+27111234567','789 Pine St, Johannesburg, South Africa','Tech Solutions Ltd','https://www.techsolutions.co.za','info@techsolutions.co.za'),(2,'kwame_gh','$2b$12$JJmDhwgDYedFTVMJzFvtyus83DGFlUPx89ucWxiZZ0J/W3cLsfxtC','kwame.boateng@gmail.com','job_seeker','2024-07-14 12:37:10','2024-07-14 12:37:10','Kwame','Boateng','+233501234567','15 Accra Street, Accra, Ghana',NULL,NULL,NULL),(3,'adebisi_ng','$2b$12$ZXTVMmlQ6hIEusoCOKVWwu9FDuYUeo9O5nnyD1zRFpPhKqVbS4CKi','adebisi.adekunle@yahoo.com','job_seeker','2024-07-14 13:54:24','2024-07-14 13:54:24','Adebisi','Adekunle','+2348012345678','23 Lagos Avenue, Lagos, Nigeria',NULL,NULL,NULL),(4,'innovatech_eg','$2b$12$orUNhkIZDXmiT/is10ulze6jAPOSNHxAi7U9dTGYcIjjkXWDLg0fe','contact@innovatech.com','employer','2024-07-14 13:55:36','2024-07-14 13:55:36',NULL,NULL,'+201234567890','321 Oak St, Cairo, Egypt','Innovatech Inc','https://www.innovatech.com','contact@innovatech.com');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-18 21:36:12
