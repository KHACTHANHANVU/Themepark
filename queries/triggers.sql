DELIMITER //

CREATE TRIGGER trigger_on_pass_purchase
    BEFORE INSERT ON novapark.park_pass
    FOR EACH ROW
BEGIN
    DECLARE last_credit_date DATE;
    DECLARE total_passes SMALLINT;

    SELECT cs.last_pass_credit_date INTO last_credit_date
    FROM novapark.customer AS cs
    WHERE NEW.cust_email = cs.email;

    IF (DATEDIFF(NEW.date_bought, last_credit_date) >= 30 OR last_credit_date IS NULL) THEN

        SELECT COALESCE(SUM(park.num_passes), 0) INTO total_passes
        FROM novapark.park_pass AS park
        WHERE NEW.cust_email = park.cust_email AND park.date_bought BETWEEN last_credit_date AND NEW.date_bought;

        IF (total_passes + NEW.num_passes) > 10 THEN
            UPDATE novapark.customer AS cs
            SET cs.last_pass_credit_date = NEW.date_bought, cs.pass_credits = cs.pass_credits + 10 
            WHERE NEW.cust_email = cs.email;
        END IF;
    END IF;
END //

DELIMITER ;




# If ride is marked for repair, update last repair date and marks it as not working
DELIMITER //

CREATE TRIGGER trigger_on_ride_repiar_log
    BEFORE INSERT ON novapark.ride_repair
    FOR EACH ROW
BEGIN
    UPDATE novapark.amusement_ride AS ar
    SET ar.date_of_last_repair = NEW.repair_date, ar.is_working = 0
    WHERE new.ride_no = ar.ride_no;
END //
DELIMITER ;