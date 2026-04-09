CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone)
        VALUES(p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR phone = p_value;
END;
$$;



CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names  VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i            INT;
    bad_names    VARCHAR[] := '{}';
    bad_phones   VARCHAR[] := '{}';
BEGIN
    FOR i IN 1 .. array_length(p_names, 1) LOOP

        IF p_phones[i] !~ '^\+?[0-9\s\-]{7,15}$' THEN
            bad_names  := array_append(bad_names,  p_names[i]);
            bad_phones := array_append(bad_phones, p_phones[i]);
            CONTINUE;  
        END IF;

        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_names[i]) THEN
            UPDATE phonebook
            SET phone = p_phones[i]
            WHERE first_name = p_names[i];
        ELSE
            INSERT INTO phonebook(first_name, phone)
            VALUES (p_names[i], p_phones[i]);
        END IF;

    END LOOP;


    IF array_length(bad_names, 1) > 0 THEN
        RAISE NOTICE 'uncorrect wtf:';
        FOR i IN 1 .. array_length(bad_names, 1) LOOP
            RAISE NOTICE 'name: %, number: %', bad_names[i], bad_phones[i];
        END LOOP;
    END IF;
END;
$$;
