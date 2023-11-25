DELIMITER //
CREATE TRIGGER trigger_on_pass_purchase
	BEFORE INSERT ON novapark.park_pass
	FOR EACH ROW
BEGIN
    DECLARE last_pass_credit_date DATE;
	DECLARE total_passes SMALLINT;

    SELECT last_credit_date INTO last_pass_credit_date
    FROM novapark.customer AS cs
    WHERE NEW.cust_email = cs.email;

    IF DATEDIFF(NEW.date_bought, last_pass_credit_date) >= 30 THEN

        SELECT SUM(park.num_passes) INTO total_passes
        FROM novapark.park_pass AS park
        WHERE NEW.cust_email = park.cust_email AND park.date_bought BETWEEN last_pass_credit_date AND NEW.date_bought;

        IF (total_passes + NEW.num_passes) > 10 THEN
            UPDATE novapark.customer AS cs
            SET cs.last_credit_date = NEW.date_bought, cs.pass_credits = cs.pass_credits + 10 
            WHERE NEW.cust_email = cs.email;
        END IF;
    END IF;
END //
DELIMITER ;


#find the number of tickets bought in the last 30 days if > 10 then give pass credit?
#for every purchase over 10 tickets in the past month you gian pass credits?
# small number that gets added ON
# larger number that is reset (10 number of tickets since this date)