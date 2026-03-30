CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.username, p.phone
    FROM phonebook p
    WHERE p.username ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%'
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.username, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;