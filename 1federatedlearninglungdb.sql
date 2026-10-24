-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 08, 2025 at 05:34 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `1federatedlearninglungdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `apptb`
--

CREATE TABLE `apptb` (
  `id` bigint(250) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `DoctorName` varchar(250) NOT NULL,
  `Date` date NOT NULL,
  `Specialist` varchar(250) NOT NULL,
  `Disease` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `apptb`
--

INSERT INTO `apptb` (`id`, `UserName`, `Mobile`, `Email`, `DoctorName`, `Date`, `Specialist`, `Disease`) VALUES
(1, 'jack', '9087259509', 'fantasypythonprojects@gmail.com', 'mark', '2025-11-08', 'mark', 'Pneumonia');

-- --------------------------------------------------------

--
-- Table structure for table `doctb`
--

CREATE TABLE `doctb` (
  `id` bigint(20) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `doctb`
--

INSERT INTO `doctb` (`id`, `Name`, `Mobile`, `Email`, `Address`, `UserName`, `Password`) VALUES
(1, 'mark', '9087259509', 'fantasypythonprojects@gmail.com', 'Trichy', 'mark', 'mark');

-- --------------------------------------------------------

--
-- Table structure for table `drugtb`
--

CREATE TABLE `drugtb` (
  `id` bigint(250) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `EmailId` varchar(250) NOT NULL,
  `DoctorName` varchar(250) NOT NULL,
  `Medicine` varchar(250) NOT NULL,
  `OtherInfo` varchar(500) NOT NULL,
  `Report` varchar(500) NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `drugtb`
--

INSERT INTO `drugtb` (`id`, `UserName`, `Mobile`, `EmailId`, `DoctorName`, `Medicine`, `OtherInfo`, `Report`, `Date`) VALUES
(1, 'jack', '9087259509', 'fantasypythonprojects@gmail.com', 'Admin', 'Dolo 650', 'nil', '000009 (3).png', '2025-11-08');

-- --------------------------------------------------------

--
-- Table structure for table `modeltb`
--

CREATE TABLE `modeltb` (
  `id` bigint(10) NOT NULL auto_increment,
  `ownerName` varchar(250) NOT NULL,
  `info` varchar(250) NOT NULL,
  `ModelName` varchar(250) NOT NULL,
  `PuplicKey` varchar(250) NOT NULL,
  `PrivateKey` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `modeltb`
--

INSERT INTO `modeltb` (`id`, `ownerName`, `info`, `ModelName`, `PuplicKey`, `PrivateKey`) VALUES
(1, 'Admin', 'Lung', 'lungmodel.h5', '021d6ff0858f199aa57bd330c63cdc111a73903f4cfea4671d78015b5a37cf5524', 'ab72784ebeb5be7b9317de8db9dc4235e37d62f44204f334b2c097e8fe116427');

-- --------------------------------------------------------

--
-- Table structure for table `regtb`
--

CREATE TABLE `regtb` (
  `id` bigint(20) NOT NULL auto_increment,
  `Name` varchar(250) NOT NULL,
  `Mobile` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Address` varchar(500) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `regtb`
--

INSERT INTO `regtb` (`id`, `Name`, `Mobile`, `Email`, `Address`, `UserName`, `Password`) VALUES
(1, 'jack', '9087259509', 'fantasypythonprojects@gmail.com', 'Trichy', 'jack', 'jack');

-- --------------------------------------------------------

--
-- Table structure for table `requesttb`
--

CREATE TABLE `requesttb` (
  `id` int(10) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `OwnerName` varchar(250) NOT NULL,
  `Type` varchar(250) NOT NULL,
  `ModelName` varchar(250) NOT NULL,
  `PriKey` varchar(250) NOT NULL,
  `Status` varchar(250) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `requesttb`
--

INSERT INTO `requesttb` (`id`, `UserName`, `OwnerName`, `Type`, `ModelName`, `PriKey`, `Status`) VALUES
(1, 'jack', 'Admin', 'Lung', 'lungmodel.h5', 'ab72784ebeb5be7b9317de8db9dc4235e37d62f44204f334b2c097e8fe116427', 'Accept'),
(2, 'jack', 'Admin', 'Lung', 'lungmodel.h5', 'ab72784ebeb5be7b9317de8db9dc4235e37d62f44204f334b2c097e8fe116427', 'Accept');
