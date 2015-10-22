-- phpMyAdmin SQL Dump
-- version 4.1.6
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Lug 29, 2015 alle 23:10
-- Versione del server: 5.6.16
-- PHP Version: 5.5.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `imagerecognize`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `clusttable`
--

CREATE TABLE IF NOT EXISTS `clusttable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Search` varchar(128) NOT NULL,
  `ImageName` varchar(128) NOT NULL,
  `Rank` double(3,2) NOT NULL DEFAULT '0.00',
  `Class` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ImageName` (`ImageName`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=808 ;

--
-- Dump dei dati per la tabella `clusttable`
--

INSERT INTO `clusttable` (`ID`, `Search`, `ImageName`, `Rank`, `Class`) VALUES
(788, 'topo', 'topo000.jpg', 0.00, 2),
(789, 'topo', 'topo001.jpg', 0.00, 2),
(790, 'topo', 'topo002.jpg', 0.00, 2),
(791, 'topo', 'topo003.jpg', 0.00, 1),
(792, 'topo', 'topo004.jpg', 0.00, 1),
(793, 'topo', 'topo005.jpg', 0.00, 2),
(794, 'topo', 'topo006.jpg', 0.00, 1),
(795, 'topo', 'topo007.jpg', 0.00, 3),
(796, 'topo', 'topo008.jpg', 0.00, 3),
(797, 'topo', 'topo009.jpg', 0.00, 1),
(798, 'topo', 'topo010.jpg', 0.00, 2),
(799, 'topo', 'topo011.jpg', 0.00, 2),
(800, 'topo', 'topo012.jpg', 0.00, 3),
(801, 'topo', 'topo013.jpg', 0.00, 1),
(802, 'topo', 'topo014.jpg', 0.00, 3),
(803, 'topo', 'topo015.jpg', 0.00, 1),
(804, 'topo', 'topo016.jpg', 0.00, 3),
(805, 'topo', 'topo017.jpg', 0.00, 1),
(806, 'topo', 'topo018.jpg', 0.00, 3),
(807, 'topo', 'topo019.jpg', 0.00, 3);

-- --------------------------------------------------------

--
-- Struttura della tabella `dbtable`
--

CREATE TABLE IF NOT EXISTS `dbtable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `classe` varchar(128) NOT NULL,
  `nome` varchar(128) NOT NULL,
  `path` varchar(258) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=169 ;

--
-- Dump dei dati per la tabella `dbtable`
--

INSERT INTO `dbtable` (`ID`, `classe`, `nome`, `path`) VALUES
(146, 'casa', 'casa000.jpg', './ClustImm/'),
(147, 'casa', 'casa001.jpg', './ClustImm/'),
(148, 'casa', 'casa002.jpg', './ClustImm/'),
(149, 'casa', 'casa003.jpg', './ClustImm/'),
(150, 'casa', 'casa004.jpg', './ClustImm/'),
(151, 'casa', 'casa005.jpg', './ClustImm/'),
(152, 'casa', 'casa006.jpg', './ClustImm/'),
(153, 'casa', 'casa009.jpg', './ClustImm/'),
(154, 'casa', 'casa010.jpg', './ClustImm/'),
(155, 'casa', 'casa011.jpg', './ClustImm/'),
(156, 'casa', 'casa012.jpg', './ClustImm/'),
(157, 'casa', 'casa013.jpg', './ClustImm/'),
(158, 'casa', 'casa014.jpg', './ClustImm/'),
(159, 'casa', 'casa016.jpg', './ClustImm/'),
(160, 'casa', 'casa017.jpg', './ClustImm/'),
(161, 'casa', 'casa019.jpg', './ClustImm/'),
(162, 'topo', 'topo007.jpg', './ClustImm/'),
(163, 'topo', 'topo008.jpg', './ClustImm/'),
(164, 'topo', 'topo012.jpg', './ClustImm/'),
(165, 'topo', 'topo014.jpg', './ClustImm/'),
(166, 'topo', 'topo016.jpg', './ClustImm/'),
(167, 'topo', 'topo018.jpg', './ClustImm/'),
(168, 'topo', 'topo019.jpg', './ClustImm/');

-- --------------------------------------------------------

--
-- Struttura della tabella `inputtable`
--

CREATE TABLE IF NOT EXISTS `inputtable` (
  `ID` int(1) NOT NULL DEFAULT '0',
  `toSearch` varchar(128) NOT NULL,
  `numImages` int(3) NOT NULL DEFAULT '10',
  `deleteSearch` int(1) NOT NULL DEFAULT '0',
  `deleteAll` int(1) NOT NULL DEFAULT '0',
  `selectCluster` int(1) NOT NULL DEFAULT '0',
  `algoritmo1` int(1) NOT NULL DEFAULT '1',
  `algoritmo2` int(1) NOT NULL DEFAULT '1',
  `algoritmo3` int(1) NOT NULL DEFAULT '1',
  `numClassi` int(1) NOT NULL DEFAULT '8',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `inputtable`
--

INSERT INTO `inputtable` (`ID`, `toSearch`, `numImages`, `deleteSearch`, `deleteAll`, `selectCluster`, `algoritmo1`, `algoritmo2`, `algoritmo3`, `numClassi`) VALUES
(0, 'topo', 20, 0, 0, 2, 1, 1, 1, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `maintable`
--

CREATE TABLE IF NOT EXISTS `maintable` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Object` varchar(128) NOT NULL,
  `numeroImm` int(3) NOT NULL,
  `googleIndex` int(3) NOT NULL DEFAULT '0',
  `Path` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Object` (`Object`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=57 ;

--
-- Dump dei dati per la tabella `maintable`
--

INSERT INTO `maintable` (`ID`, `Object`, `numeroImm`, `googleIndex`, `Path`) VALUES
(55, 'casa', 20, 28, 'C:\\xampp\\htdocs\\dipp\\imm\\casa'),
(56, 'topo', 20, 22, 'C:\\xampp\\htdocs\\dipp\\imm\\topo');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
