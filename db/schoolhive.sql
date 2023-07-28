-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 28, 2023 at 09:59 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `schoolhive`
--
CREATE DATABASE IF NOT EXISTS `schoolhive` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `schoolhive`;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `cedula` int(9) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`cedula`, `nombre`, `apellido`, `email`, `password`) VALUES
(1234567, 'Admin', '1', 'admin@gmail.com', '3496b72c9b710a62dd14a3c63adaa4011b6441ba'),
(7654321, 'admin', '2', 'admin2@gmail.com', '3496b72c9b710a62dd14a3c63adaa4011b6441ba');

-- --------------------------------------------------------

--
-- Table structure for table `carrera`
--

CREATE TABLE `carrera` (
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `carrera`
--

INSERT INTO `carrera` (`nombre`) VALUES
('Contaduría'),
('Ingeniería en Computación'),
('Ingeniería en Informática');

-- --------------------------------------------------------

--
-- Table structure for table `estudiante`
--

CREATE TABLE `estudiante` (
  `cedula` int(9) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `carrera` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `estudiante`
--

INSERT INTO `estudiante` (`cedula`, `nombre`, `apellido`, `email`, `password`, `carrera`) VALUES
(0, '陈杨', 'el chino', 'elchino@gmail.com', '778edf016cea2c7b0bdb3f70bfe1893f42bf7604', 'Ingeniería en Informática'),
(111222, 'Alba', 'Bala', 'Alba@gmail.com', '778edf016cea2c7b0bdb3f70bfe1893f42bf7604', 'Contaduría'),
(7898775, 'Roberto', 'Alcabala', 'estudiante3@gmail.com', 'f024df9c710cd05b20b525272fefb4feb518571d', 'Contaduría'),
(7898777, 'Pedro', 'Rodríguez', 'estudiante1@gmail.com', 'f024df9c710cd05b20b525272fefb4feb518571d', 'Ingeniería en Informática'),
(33333333, 'Carla', 'ɐןᴙɐↄ', 'Carla@gmail.com', '778edf016cea2c7b0bdb3f70bfe1893f42bf7604', 'Ingeniería en Computación'),
(55555555, 'Ramón', 'Rodríguez', 'estudiante@gmail.com', 'f024df9c710cd05b20b525272fefb4feb518571d', 'Ingeniería en Computación');

-- --------------------------------------------------------

--
-- Table structure for table `materia`
--

CREATE TABLE `materia` (
  `id` int(9) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `periodo` varchar(45) NOT NULL,
  `seccion` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `materia`
--

INSERT INTO `materia` (`id`, `nombre`, `periodo`, `seccion`) VALUES
(1, 'Bases de Datos I', '2-2023', 'N-613'),
(2, 'Gestión de Proyectos informático', '2-2023', 'N-613'),
(3, 'Matemática I', '1-2023', 'P-613'),
(4, 'Contabilidad', '2-2023', 'P-613');

-- --------------------------------------------------------

--
-- Table structure for table `materia_estudiante`
--

CREATE TABLE `materia_estudiante` (
  `materia` int(9) NOT NULL,
  `estudiante` int(9) NOT NULL,
  `nota` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `materia_estudiante`
--

INSERT INTO `materia_estudiante` (`materia`, `estudiante`, `nota`) VALUES
(3, 0, 20),
(1, 111222, 0),
(1, 7898775, 0),
(2, 7898775, 0),
(3, 7898777, 15),
(4, 7898777, 0),
(1, 33333333, 0),
(2, 33333333, 0),
(3, 55555555, 15),
(4, 55555555, 0);

-- --------------------------------------------------------

--
-- Table structure for table `materia_profesor`
--

CREATE TABLE `materia_profesor` (
  `materia` int(9) NOT NULL,
  `profesor` int(9) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `materia_profesor`
--

INSERT INTO `materia_profesor` (`materia`, `profesor`) VALUES
(2, 5555555),
(1, 3333333),
(3, 1111111),
(4, 1111111);

-- --------------------------------------------------------

--
-- Table structure for table `periodo`
--

CREATE TABLE `periodo` (
  `nombre` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `periodo`
--

INSERT INTO `periodo` (`nombre`) VALUES
('1-2023'),
('2-2023'),
('3-2023'),
('4-2023');

-- --------------------------------------------------------

--
-- Table structure for table `profesor`
--

CREATE TABLE `profesor` (
  `cedula` int(9) NOT NULL,
  `nombre` varchar(45) NOT NULL,
  `apellido` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profesor`
--

INSERT INTO `profesor` (`cedula`, `nombre`, `apellido`, `email`, `password`) VALUES
(1111111, 'Profe', '3', 'profe3@gmail.com', '12e76b0a96da6af17dab0b8539d6733ab2d5fb31'),
(3333333, 'Profesor', '2', 'profesor2@gmail.com', '12e76b0a96da6af17dab0b8539d6733ab2d5fb31'),
(5555555, 'profesor', '1', 'profesor1@gmail.com', '12e76b0a96da6af17dab0b8539d6733ab2d5fb31');

-- --------------------------------------------------------

--
-- Table structure for table `seccion`
--

CREATE TABLE `seccion` (
  `nombre` varchar(45) NOT NULL,
  `carrera` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `seccion`
--

INSERT INTO `seccion` (`nombre`, `carrera`) VALUES
('P-113', 'Contaduría'),
('P-613', 'Contaduría'),
('C-413', 'Ingeniería en Computación'),
('C-613', 'Ingeniería en Computación'),
('N-513', 'Ingeniería en Informática'),
('N-613', 'Ingeniería en Informática');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`cedula`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `carrera`
--
ALTER TABLE `carrera`
  ADD PRIMARY KEY (`nombre`);

--
-- Indexes for table `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`cedula`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `carrera` (`carrera`);

--
-- Indexes for table `materia`
--
ALTER TABLE `materia`
  ADD PRIMARY KEY (`id`),
  ADD KEY `periodo` (`periodo`),
  ADD KEY `seccion` (`seccion`);

--
-- Indexes for table `materia_estudiante`
--
ALTER TABLE `materia_estudiante`
  ADD KEY `materia` (`materia`),
  ADD KEY `estudiante` (`estudiante`);

--
-- Indexes for table `materia_profesor`
--
ALTER TABLE `materia_profesor`
  ADD KEY `materia` (`materia`),
  ADD KEY `profesor` (`profesor`);

--
-- Indexes for table `periodo`
--
ALTER TABLE `periodo`
  ADD PRIMARY KEY (`nombre`);

--
-- Indexes for table `profesor`
--
ALTER TABLE `profesor`
  ADD PRIMARY KEY (`cedula`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `seccion`
--
ALTER TABLE `seccion`
  ADD PRIMARY KEY (`nombre`),
  ADD KEY `carrera` (`carrera`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `materia`
--
ALTER TABLE `materia`
  MODIFY `id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `estudiante`
--
ALTER TABLE `estudiante`
  ADD CONSTRAINT `estudiante_ibfk_1` FOREIGN KEY (`carrera`) REFERENCES `carrera` (`nombre`) ON UPDATE CASCADE;

--
-- Constraints for table `materia`
--
ALTER TABLE `materia`
  ADD CONSTRAINT `materia_ibfk_1` FOREIGN KEY (`periodo`) REFERENCES `periodo` (`nombre`),
  ADD CONSTRAINT `materia_ibfk_2` FOREIGN KEY (`seccion`) REFERENCES `seccion` (`nombre`);

--
-- Constraints for table `materia_estudiante`
--
ALTER TABLE `materia_estudiante`
  ADD CONSTRAINT `materia_estudiante_ibfk_1` FOREIGN KEY (`materia`) REFERENCES `materia` (`id`),
  ADD CONSTRAINT `materia_estudiante_ibfk_2` FOREIGN KEY (`estudiante`) REFERENCES `estudiante` (`cedula`) ON DELETE CASCADE;

--
-- Constraints for table `materia_profesor`
--
ALTER TABLE `materia_profesor`
  ADD CONSTRAINT `materia_profesor_ibfk_1` FOREIGN KEY (`materia`) REFERENCES `materia` (`id`),
  ADD CONSTRAINT `materia_profesor_ibfk_2` FOREIGN KEY (`profesor`) REFERENCES `profesor` (`cedula`);

--
-- Constraints for table `seccion`
--
ALTER TABLE `seccion`
  ADD CONSTRAINT `seccion_ibfk_1` FOREIGN KEY (`carrera`) REFERENCES `carrera` (`nombre`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
