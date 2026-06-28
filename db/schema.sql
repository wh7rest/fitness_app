-- =========================
-- DROP (чтобы пересоздавалось чисто при init)
-- =========================
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS users;
-- =========================
-- USERS (авторизация)
-- =========================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'client'
);
-- =========================
-- CLIENTS
-- =========================
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    membership_start TEXT,
    membership_end TEXT
);
-- =========================
-- TRAINERS
-- =========================
CREATE TABLE trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    specialization TEXT,
    phone TEXT
);
-- =========================
-- SERVICES
-- =========================
CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL,
    duration INTEGER
);
-- =========================
-- SESSIONS (связующая таблица)
-- =========================
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    trainer_id INTEGER,
    service_id INTEGER,
    session_date TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (trainer_id) REFERENCES trainers(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);
-- =========================
-- TEST DATA: USERS
-- =========================
INSERT INTO users (username, password, role)
VALUES
    ('admin', '123', 'admin'),
    ('user1', '111', 'client');
-- =========================
-- TEST DATA: CLIENTS
-- =========================
INSERT INTO clients (
        full_name,
        phone,
        email,
        membership_start,
        membership_end
    )
VALUES (
        'Иван Петров',
        '900-101',
        'ivan@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Мария Соколова',
        '900-102',
        'maria@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Алексей Смирнов',
        '900-103',
        'alexey@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Ольга Кузнецова',
        '900-104',
        'olga@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Дмитрий Волков',
        '900-105',
        'dmitry@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Екатерина Морозова',
        '900-106',
        'ekaterina@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Сергей Орлов',
        '900-107',
        'sergey@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Анна Лебедева',
        '900-108',
        'anna@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Николай Фёдоров',
        '900-109',
        'nikolay@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    ),
    (
        'Татьяна Павлова',
        '900-110',
        'tatyana@mail.com',
        DATE('now'),
        DATE('now', '+1 year')
    );
-- =========================
-- TEST DATA: TRAINERS
-- =========================
INSERT INTO trainers (full_name, specialization, phone)
VALUES ('Андрей Васильев', 'Фитнес', '800-201'),
    ('Ирина Новикова', 'Йога', '800-202'),
    ('Павел Зайцев', 'Кроссфит', '800-203'),
    ('Наталья Романова', 'Пилатес', '800-204'),
    ('Виктор Беляев', 'Кардио', '800-205'),
    ('Елена Тихонова', 'Стретчинг', '800-206'),
    (
        'Максим Борисов',
        'Силовые тренировки',
        '800-207'
    ),
    ('Юлия Григорьева', 'Аэробика', '800-208'),
    ('Артём Крылов', 'Бокс', '800-209'),
    (
        'Светлана Медведева',
        'Реабилитационный фитнес',
        '800-210'
    );
-- =========================
-- TEST DATA: SERVICES
-- =========================
INSERT INTO services (name, price, duration)
VALUES ('Персональная тренировка', 2500, 60),
    ('Групповая йога', 1200, 45),
    ('Кроссфит тренировка', 1800, 50),
    ('Консультация по питанию', 2000, 30),
    ('Пилатес', 1500, 50),
    ('Кардио тренировка', 1400, 40),
    ('Стретчинг', 1300, 45),
    ('Силовая тренировка', 2200, 60),
    ('Бокс тренировка', 2100, 55),
    ('Функциональный тренинг', 1900, 50);
-- =========================
-- TEST DATA: SESSIONS
-- =========================
INSERT INTO sessions (client_id, trainer_id, service_id, session_date)
VALUES (1, 1, 1, '2026-04-20'),
    (2, 2, 2, '2026-04-21'),
    (3, 3, 3, '2026-04-22'),
    (4, 4, 5, '2026-04-23'),
    (5, 5, 6, '2026-04-24'),
    (6, 6, 7, '2026-04-25'),
    (7, 7, 8, '2026-04-26'),
    (8, 8, 2, '2026-04-27'),
    (9, 9, 9, '2026-04-28'),
    (10, 10, 10, '2026-04-29');
