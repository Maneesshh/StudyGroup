-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 03, 2023 at 10:27 AM
-- Server version: 8.0.32-0ubuntu0.20.04.2
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `manojcrystalerp`
--

-- --------------------------------------------------------

--
-- Table structure for table `setting`
--

CREATE TABLE `setting` (
  `setting_id` bigint NOT NULL,
  `setting_key` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_group` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `setting`
--

INSERT INTO `setting` (`setting_id`, `setting_key`, `setting_group`, `setting_value`) VALUES
(1, 'SHOW_EVENT_IN_HOMEPAGE', 'CMS', 'true'),
(2, 'Account_Opening_Date', 'Account_Ledger_SetUp', '2077-4-1'),
(8, 'SHOW_COMPANY_INFO_IN_RECEIPT', 'COMPANY_DETAILS', 'true'),
(9, 'COMPANY_SLOGAN', 'COMPANY_DETAILS', NULL),
(10, 'GOOGLE_MAP', 'COMPANY_DETAILS', NULL),
(11, 'COMPANY_WEBSITE', 'COMPANY_DETAILS', NULL),
(12, 'COMPANY_NAME', 'COMPANY_DETAILS', 'Dev Manoj'),
(13, 'COMPANY_Email', 'COMPANY_DETAILS', 'test@gmail.com'),
(14, 'COMPANY_ADDRESS', 'COMPANY_DETAILS', 'Birtamode'),
(15, 'PHONE_NUMBER', 'COMPANY_DETAILS', '9875674323'),
(16, 'PAN_NUMBER', 'COMPANY_DETAILS', '2345678');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `setting`
--
ALTER TABLE `setting`
  ADD PRIMARY KEY (`setting_id`),
  ADD UNIQUE KEY `setting_key` (`setting_key`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `setting`
--
ALTER TABLE `setting`
  MODIFY `setting_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
