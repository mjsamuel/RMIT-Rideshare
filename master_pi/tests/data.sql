INSERT INTO user (username, password)
VALUES
  ('dummy', '$2b$12$xIygz54Gi4G/FROikCKhfej.JmnI8lSzR6RPpqiErQRUvnjSikOjO'),
  ('john', '$2b$12$pUSt0xQDEsdaHmXtNJ7BaOlN8NzqL5.tFucHTwyL6nf7o6KvAl9p');

INSERT INTO car (make, body_type, colour, no_seats, cost_per_hour)
VALUES
    ('Toyota', 'SUV', 'Black', 5, 15),
    ('Tesla', 'Pickup', 'Silver', 6, 25),
    ('Toyota', 'Hatchback', 'Black', 5, 15);

INSERT INTO booking (car_id, username, duration, book_time)
VALUES
    (2, 'dummy', 1, '2020-05-09 02:22:51'),
    (1, 'dummy', 3, '2020-05-09 10:22:51');
