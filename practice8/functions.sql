CREATE OR REPLACE FUNCTION search_pattern(p text)
RETURNS TABLE(first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT first_name, phone
    FROM phonebook
    WHERE first_name ILIKE '%' || p || '%'
       OR phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, first_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;