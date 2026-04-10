CREATE OR REPLACE FUNCTION search_pattern(p text)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.name, phonebook.phone
    FROM phonebook
    WHERE phonebook.name ILIKE '%' || p || '%'
       OR phonebook.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(lim INT, off INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT phonebook.id, phonebook.name, phonebook.phone
    FROM phonebook
    LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;
