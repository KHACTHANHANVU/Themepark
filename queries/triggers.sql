
DELIMETER //
CREATE TRIGGER trigger_on_purchase BEFORE INSERT ON novapark.pass_park
BEGIN
    SET @time_of_purchase
    SELECT COUNT(*) INTO 
END;

DELIMITER //
CREATE TRIGGER trigger_Employee_inserthour BEFORE UPDATE ON novapark.staff
FOR EACH ROW
BEGIN
    DECLARE rowCount INT;
    
    SELECT COUNT(*) INTO rowCount FROM novapark.staff;
    
    IF rowCount = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table Staff does not have any data';
    END IF;

    IF NEW.hours_work > 40 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table staff cannot be updated';
    END IF;
    
    IF NEW.hours_work > 40 THEN
        UPDATE week_wage
        SET week_wage = week_wage * 1.5 * NEW.hours_work
        WHERE staff_no = NEW.staff_no;
    END IF;
END;
//
DELIMITER ;


DELIMITER //
CREATE TRIGGER trigger_visitor_ispresent BEFORE UPDATE ON novapark.visitor
FOR EACH ROW
BEGIN
    DECLARE rowCount INT;
    
    SELECT COUNT(*) INTO rowCount FROM novapark.visitor;
    
    IF rowCount = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Table Visitor does not have any data';
    END IF;

    IF NEW.ticket_no IS NOT NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You are qualified for coupons';
    END IF;
    
    IF NEW.is_present = TRUE THEN
        UPDATE novapark.price
        SET price = price * 0.75;
    END IF;
END;
//
DELIMITER ;
