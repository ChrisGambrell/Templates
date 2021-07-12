INSERT INTO user (name, username, password)
VALUES
    ('user', 'username', 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155'),
    ('John Doe', 'other', 'pbkdf2:sha256:260000$PMLqezAg2LqvlI9c$e3bb259297561bac7418481fd46b78590dc15e5e836d520535085f0966ac9155');

INSERT INTO task (user_id, body)
VALUES
    ('test title', 1);
