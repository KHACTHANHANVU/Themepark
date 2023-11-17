



DELIMITER //

CREATE TRIGGER trigger_on_pass_purchase BEFORE INSERT ON novapark.park_pass
BEGIN
    DECLARE last_pass_credit_date DATE;

    SELECT last_credit_date INTO last_pass_credit_date 
    FROM novapark.customer AS cs
    WHERE new.cust_email = cs.email;

    IF DATEDIFF(month, new.date_bought, last_pass_credit_date) >= 30 THEN
        DECLARE total_passes SMALLINT;

        SELECT COUNT(num_passes) INTO total_passes;
        FROM novapark.park_pass AS park 
        WHERE new.cust_email = park.cust_email AND park.date_bought BETWEEN last_pass_credit_date AND new.date_bought;

        IF (total_passes + new.num_passes) > 10 THEN
            UPDATE cs.last_credit_date, cs.pass_credits
            SET cs.last_credit_date = new.date_bought, cs.pass_credits = cs.pass_credits + 10;
            FROM novapark.customer AS cs
            WHERE new.cust_email = cs.email;
            END IF;
    END IF;

        

END



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
