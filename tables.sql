
CREATE TABLE `customers` (
  `username` varchar(20) NOT NULL,
  `firstname` varchar(15) NOT NULL,
  `lastname` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `phoneNumber` varchar(11) NOT NULL,
  `email` varchar(40) NOT NULL,
  `userType` int(11) NOT NULL,
  `verificationCode` varchar(8) NOT NULL,
  `verifiedUser` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO `customers` (`username`, `firstname`, `lastname`, `password`, `phoneNumber`, `email`, `userType`, `verificationCode`, `verifiedUser`) VALUES
('admin', 'admin', 'admin', '123123', '09999999999', 'admin@gmail.com', 1, '', 0);



CREATE TABLE `inventory` (
  `inventory_id` int(15) NOT NULL,
  `stock` int(10) NOT NULL,
  `prod_id` int(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    totalAmountPayment double(10, 2), 
    username VARCHAR(255)
);


CREATE TABLE `product` (
  `product_id` int(15) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(25) NOT NULL,
  `description` varchar(30) NOT NULL,
  `price` double NOT NULL,
  `inventory_id` int(15) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE `customers`
  ADD PRIMARY KEY (`username`);

  ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

