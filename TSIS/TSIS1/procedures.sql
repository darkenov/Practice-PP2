CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id
    FROM contacts
    WHERE name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact not found';
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    IF v_group_id IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE name = p_contact_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    created_at TIMESTAMP
)
LANGUAGE sql
AS $$
    SELECT DISTINCT c.id, c.name, c.email, c.birthday, g.name, c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
$$;


CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    created_at TIMESTAMP
)
LANGUAGE sql
AS $$
    SELECT c.id, c.name, c.email, c.birthday, g.name, c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
$$;