-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 11, 2020 at 05:45 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.1.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `e_commerce`
--

-- --------------------------------------------------------

--
-- Table structure for table `buyer`
--

CREATE TABLE `buyer` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phoneNumber` varchar(11) NOT NULL,
  `address` varchar(50) NOT NULL,
  `securityQuestion` varchar(500) NOT NULL,
  `answer` varchar(250) NOT NULL,
  `wish_list` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `buyer`
--

INSERT INTO `buyer` (`id`, `name`, `password`, `email`, `phoneNumber`, `address`, `securityQuestion`, `answer`, `wish_list`) VALUES
(28, 'mahdeed', 'abc', 'mahdeed@gmail.com', ' ', ' ', 'Childhood nickname?', 'abc', NULL),
(29, 'sample', 'abc', 'abc@gmail.com', '', '', '', '', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cartNo` int(11) NOT NULL,
  `buyerId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cartNo`, `buyerId`) VALUES
(50, 28),
(76, 29);

-- --------------------------------------------------------

--
-- Table structure for table `cartitems`
--

CREATE TABLE `cartitems` (
  `cartNo` int(11) NOT NULL,
  `productId` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cartitems`
--

INSERT INTO `cartitems` (`cartNo`, `productId`, `quantity`) VALUES
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 3, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 2, 1),
(29, 3, 1),
(50, 3, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 3, 1),
(50, 3, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 2, 1),
(50, 1, 1),
(50, 8, 1),
(50, 1, 1),
(50, 1, 1),
(50, 10, 1),
(50, 10, 1),
(50, 10, 1),
(50, 14, 1);

-- --------------------------------------------------------

--
-- Table structure for table `invoice`
--

CREATE TABLE `invoice` (
  `invoiceNumber` int(11) NOT NULL,
  `name` varchar(250) NOT NULL,
  `customerId` int(11) NOT NULL,
  `totalCost` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `invoice`
--

INSERT INTO `invoice` (`invoiceNumber`, `name`, `customerId`, `totalCost`) VALUES
(1, 'mahdeed', 28, 9600),
(2, 'mahdeed', 28, 9600),
(3, 'mahdeed', 28, 9600),
(4, 'mahdeed', 28, 9600),
(5, 'mahdeed', 28, 9600),
(6, 'mahdeed', 28, 9800),
(7, 'mahdeed', 28, 9800),
(8, 'mahdeed', 28, 9800),
(9, 'mahdeed', 28, 11000),
(10, 'mahdeed', 28, 11000),
(11, 'mahdeed', 28, 12200),
(12, 'mahdeed', 28, 13400),
(13, 'mahdeed', 28, 15800),
(14, 'mahdeed', 28, 4200),
(15, 'mahdeed', 28, 4200),
(16, 'mahdeed', 28, 29670),
(17, 'mahdeed', 28, 396880),
(18, 'mahdeed', 28, 410100),
(19, 'mahdeed', 28, 422220),
(20, 'mahdeed', 28, 431140);

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `orderNo` int(11) NOT NULL,
  `cartNo` int(11) NOT NULL,
  `shipmentFee` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(255) NOT NULL,
  `rating` int(11) NOT NULL,
  `warranty` date DEFAULT NULL,
  `type` varchar(25) NOT NULL,
  `deliveryCharges` int(11) DEFAULT NULL,
  `seller` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `price`, `quantity`, `rating`, `warranty`, `type`, `deliveryCharges`, `seller`) VALUES
(1, 'Bagpack', 12000, 20, 5, '2020-05-05', 'bag', 120, 1),
(2, 'bag', 16000, 20, 2, '2020-05-05', 'bag', 1200, 2),
(3, 'Denim Jacket', 2000, 20, 2, NULL, 'clothing', 120, 2),
(5, 'watch', 1300, 20, 2, NULL, 'accessory', 100, 2),
(6, 'jeans', 5000, 30, 4, NULL, 'clothing', 400, 1),
(7, 'Denim shorts', 800, 20, 2, NULL, 'clothing', 120, 2),
(8, 'watch(brown)', 800, 10, 2, NULL, 'accessory', 300, 3),
(10, 'Grey shirt', 2000, 10, 3, NULL, 'clothing', 300, 2),
(11, 'Trouser', 400, 200, 3, '2020-05-04', 'clothing', 35, 3),
(12, 'White T-shirt', 1000, 10, 2, NULL, 'clothing', 200, 3),
(14, 'Grey T-Shirt', 2000, 20, 4, NULL, 'clothing', 20, 1),
(15, 'Basic T-shirt', 5000, 40, 4, NULL, 'clothing', 300, 3),
(16, 'Shirt', 4000, 4, 5, NULL, 'clothing', 400, 1),
(17, 'Sneakers', 3000, 30, 4, NULL, 'shoes', 200, 2);

-- --------------------------------------------------------

--
-- Table structure for table `seller`
--

CREATE TABLE `seller` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phoneNumber` varchar(11) NOT NULL,
  `password` varchar(50) NOT NULL,
  `ranking` int(11) NOT NULL,
  `securityQuestion` varchar(500) NOT NULL,
  `answer` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `seller`
--

INSERT INTO `seller` (`id`, `name`, `address`, `email`, `phoneNumber`, `password`, `ranking`, `securityQuestion`, `answer`) VALUES
(1, 'MAHAD', 'LAHORE', 'mahad@gmail.com', '123', '123', 5, '', ''),
(2, 'Haziq', '', 'haziq@gmail.com', '', 'abc', 4, 'Sibling\'s middle name?', 'Taz'),
(3, 'mahdeed', '', 'mahdeed@gmail.com', '1234567', 'abc', 5, '', '');

-- --------------------------------------------------------

--
-- Table structure for table `wish_list`
--

CREATE TABLE `wish_list` (
  `id` int(11) NOT NULL,
  `product1` int(11) NOT NULL,
  `product2` int(11) NOT NULL,
  `product3` int(11) NOT NULL,
  `product4` int(11) NOT NULL,
  `product5` int(11) NOT NULL,
  `product6` int(11) NOT NULL,
  `product7` int(11) NOT NULL,
  `product8` int(11) NOT NULL,
  `product9` int(11) NOT NULL,
  `product10` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `buyer`
--
ALTER TABLE `buyer`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `wish_list` (`wish_list`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cartNo`),
  ADD UNIQUE KEY `buyerId` (`buyerId`);

--
-- Indexes for table `invoice`
--
ALTER TABLE `invoice`
  ADD PRIMARY KEY (`invoiceNumber`),
  ADD KEY `customerId` (`customerId`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`orderNo`),
  ADD KEY `cartNo` (`cartNo`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `seller` (`seller`);

--
-- Indexes for table `seller`
--
ALTER TABLE `seller`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `wish_list`
--
ALTER TABLE `wish_list`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `buyer`
--
ALTER TABLE `buyer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cartNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT for table `invoice`
--
ALTER TABLE `invoice`
  MODIFY `invoiceNumber` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `orderNo` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `seller`
--
ALTER TABLE `seller`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `wish_list`
--
ALTER TABLE `wish_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `buyer`
--
ALTER TABLE `buyer`
  ADD CONSTRAINT `buyer_ibfk_1` FOREIGN KEY (`wish_list`) REFERENCES `product` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Constraints for table `invoice`
--
ALTER TABLE `invoice`
  ADD CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`customerId`) REFERENCES `buyer` (`id`);

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_ibfk_1` FOREIGN KEY (`cartNo`) REFERENCES `cart` (`cartNo`);

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`seller`) REFERENCES `seller` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
