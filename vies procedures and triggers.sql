CREATE VIEW customer_info_view AS
SELECT
    username,
    firstname,
    lastname,
    phoneNumber,
    email,
    CASE
        WHEN verifiedUser = 0 THEN 'Verified'
        ELSE 'Not Verified'
    END AS verificationStatus,
    verificationCode
FROM customers;


CREATE VIEW product_availability_view AS
SELECT
    p.product_id,
    p.product_name,
    p.description,
    p.price,
    i.stock,
    CASE
        WHEN i.stock > 0 THEN 'Available'
        ELSE 'Not Available'
    END AS availability
FROM
    product p
JOIN
    inventory i ON p.product_id = i.prod_id;


CREATE VIEW `product_details` AS
SELECT
    `p`.`product_id` AS `product_id`,
    `p`.`product_name` AS `product_name`,
    `p`.`description` AS `description`,
    `p`.`price` AS `price`,
    `i`.`stock` AS `stock`
FROM
    `product` `p`
JOIN
    `inventory` `i` ON (`p`.`product_id` = `i`.`prod_id`);







DELIMITER $$
CREATE PROCEDURE AddProduct(
    IN p_product_name VARCHAR(25),
    IN p_description VARCHAR(30),
    IN p_price DOUBLE,
    IN p_stock INT
)
BEGIN
    DECLARE product_id INT;
    
    SELECT product_id INTO product_id FROM product WHERE product_name = p_product_name LIMIT 1;
    
    IF product_id IS NULL THEN
        INSERT INTO product (product_name, description, price, inventory_id) 
        VALUES (p_product_name, p_description, p_price, 1);
        
        SET product_id = LAST_INSERT_ID();
        
        -- Insert into inventory
        INSERT INTO inventory (inventory_id, stock, prod_id) VALUES (1, p_stock, product_id);
    ELSE
        -- Update existing product stock
        UPDATE inventory SET stock = stock + p_stock WHERE prod_id = product_id;
    END IF;
END $$
DELIMITER ;





DELIMITER $$
CREATE PROCEDURE DeleteProduct(IN p_product_id INT)
BEGIN
    DELETE FROM inventory WHERE prod_id = p_product_id;
    DELETE FROM product WHERE product_id = p_product_id;
END $$
DELIMITER ;






DELIMITER $$

CREATE PROCEDURE UpdateProduct(
    IN p_product_id INT,
    IN p_new_name VARCHAR(255),
    IN p_new_description VARCHAR(255),  -- Add this parameter for the new description
    IN p_new_price DECIMAL(10, 2)
)
BEGIN
    UPDATE product
    SET product_name = p_new_name, description = p_new_description, price = p_new_price
    WHERE product_id = p_product_id;
END $$

DELIMITER ;






DELIMITER $$

CREATE PROCEDURE UpdateInventory(
    IN p_product_id INT,
    IN p_new_quantity INT
)
BEGIN
    UPDATE inventory
    SET stock = p_new_quantity
    WHERE prod_id = p_product_id;
END $$

DELIMITER ;







DELIMITER $$

CREATE TRIGGER productInsert
AFTER INSERT ON product
FOR EACH ROW
BEGIN
    DECLARE new_inventory_id INT;

    -- Retrieve the newly inserted product's inventory_id
    SELECT NEW.inventory_id INTO new_inventory_id;

    -- Update the inventory stock count for the related product
    UPDATE inventory SET stock = stock + 1 WHERE inventory_id = new_inventory_id;
END $$
DELIMITER ;




DELIMITER $$

CREATE TRIGGER orderplaced
AFTER INSERT ON payment
FOR EACH ROW
BEGIN
    DECLARE new_total_amount DOUBLE;

    SELECT NEW.totalAmountPayment INTO new_total_amount;

    UPDATE customers SET totalAmountPayment = totalAmountPayment + new_total_amount WHERE username = NEW.username;
END $$

DELIMITER ;





DELIMITER $$

CREATE TRIGGER productdeletion
BEFORE DELETE ON product
FOR EACH ROW
BEGIN
    DECLARE deleted_inventory_id INT;

    -- Retrieve the inventory_id of the product being deleted
    SELECT OLD.inventory_id INTO deleted_inventory_id;

    -- Update the inventory stock count for the related product
    UPDATE inventory SET stock = stock - 1 WHERE inventory_id = deleted_inventory_id;
END $$

DELIMITER ;