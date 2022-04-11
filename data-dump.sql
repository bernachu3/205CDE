-- MariaDB dump 10.19  Distrib 10.7.3-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: gym
-- ------------------------------------------------------
-- Server version	10.4.24-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE utf8_bin NOT NULL,
  `password` varchar(256) COLLATE utf8_bin NOT NULL,
  `email` varchar(100) COLLATE utf8_bin NOT NULL,
  `newsletter` tinyint(1) NOT NULL,
  `plan` tinyint(4) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES
(2,'test','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4','john@example.com',0,1);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catalog`
--

DROP TABLE IF EXISTS `catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catalog` (
  `id` smallint(4) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8_bin NOT NULL,
  `price` int(11) NOT NULL,
  `desc` varchar(500) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catalog`
--

LOCK TABLES `catalog` WRITE;
/*!40000 ALTER TABLE `catalog` DISABLE KEYS */;
INSERT INTO `catalog` VALUES
(1,'T-Shirt',40,'A T-Shirt for you to lounge about in and delay having to do the laundry for another week.'),
(2,'Mug',80,'It\'s a mug. Or maybe it\'s a cup. Honestly, no clue on what the difference between the two are. One\'s square, and one\'s round? Does that really need distinguishing? English is weird.'),
(3,'Calendar',20,'A calendar to tell you the current date, in case you don\'t have your phone with you. Do you know calenders are actually a massive pain because of the very complex history of time zones?'),
(4,'Water Bottle',50,'A water bottle. Look, there\'s not really much to say about a bottle. It holds liquids. What else does a bottle need to do? Sing?'),
(5,'Sticker',10,'A sticker, the cheapest novelty souvenir item produced in some random shed in the back and sold for a ludicrous price.'),
(6,'Towel',100,'A stack of towels. Not made from Egyptian cotton.');
/*!40000 ALTER TABLE `catalog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coach`
--

DROP TABLE IF EXISTS `coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `coach` (
  `coachID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE utf8_bin NOT NULL,
  `day` smallint(4) NOT NULL,
  PRIMARY KEY (`coachID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coach`
--

LOCK TABLES `coach` WRITE;
/*!40000 ALTER TABLE `coach` DISABLE KEYS */;
/*!40000 ALTER TABLE `coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `headline` varchar(100) COLLATE utf8_bin NOT NULL,
  `contents` varchar(1000) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES
(1,'We are now hiring!','Praesent aliquam ipsum eget mollis dignissim. Sed gravida arcu vitae tempus molestie. Curabitur auctor auctor egestas. Pellentesque tincidunt elementum lacus, sed mollis justo rutrum accumsan. In condimentum, neque ut laoreet pulvinar, est orci dictum tellus, non finibus quam massa eu dui. Mauris ornare quam erat, non molestie diam hendrerit feugiat. Maecenas eu dui dolor. Aliquam felis diam, dapibus id sapien ac, congue dignissim arcu. In hac habitasse platea dictumst. Maecenas rhoncus orci vel leo commodo, sed mollis velit pretium.'),
(2,'Congratulations to the winner of our contest','Maecenas in massa fermentum, gravida tellus sit amet, volutpat lacus. Morbi laoreet, mauris id vehicula molestie, nisl enim faucibus ex, vitae pretium elit urna in eros. Quisque lacinia mollis risus sed luctus. Etiam condimentum mauris massa, id fermentum odio ullamcorper sed. Duis mi diam, pulvinar et sagittis quis, consectetur et nisi. Etiam sit amet gravida purus, sed sagittis lorem. Proin vestibulum ultricies dolor eget tempor. Pellentesque cursus, mauris eget scelerisque commodo, nunc ipsum vehicula magna, a luctus lectus tortor in risus. Suspendisse potenti. Ut faucibus vitae libero id ultrices. Suspendisse in pulvinar eros. Cras lacinia fringilla sapien hendrerit congue.'),
(3,'Voted best gym in the city','In eu lobortis nisl. Nullam feugiat cursus dapibus. Mauris ultrices metus a risus luctus commodo. Phasellus vel risus vitae urna suscipit iaculis a ac leo. Fusce consequat non felis at gravida. Vivamus venenatis sed purus eget auctor. Praesent et justo sapien. Aliquam viverra nec felis at molestie. Cras vitae lobortis leo, nec ullamcorper massa. Etiam sodales, felis vel ultrices porttitor, magna mauris pellentesque lorem, at venenatis orci augue at velit. Donec facilisis neque nec ullamcorper vulputate. Proin vitae pulvinar enim. Integer lectus sem, vestibulum id dictum ut, vestibulum et magna. Quisque eu suscipit purus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut risus mi, faucibus sit amet tristique vitae, porta nec justo.');
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `room` (
  `roomID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) COLLATE utf8_bin NOT NULL,
  `day` smallint(4) NOT NULL,
  PRIMARY KEY (`roomID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-05 12:12:01
