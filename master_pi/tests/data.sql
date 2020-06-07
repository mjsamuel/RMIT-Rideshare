-- Add dummy users

INSERT INTO user (username, password, f_name, l_name, email, role, mac_address)
VALUES
  ('dummy', '$2b$12$xIygz54Gi4G/FROikCKhfej.JmnI8lSzR6RPpqiErQRUvnjSikOjO', 'First', 'Last', 'dummyemail@gmail.com', 'default', '18:F1:D8:E2:E9:6B'),
  ('john', '$2b$12$pUSt0xQDEsdaHmXtNJ7BaOlN8NzqL5.tFucHTwyL6nf7o6KvAl9p', 'John', 'Doe', 'john.doe@outlook.com', 'default', null),
  ('admin', '$2b$12$xIygz54Gi4G/FROikCKhfej.JmnI8lSzR6RPpqiErQRUvnjSikOjO', 'First', 'Last', 'admin@gmail.com', 'admin', null),
  ('engineer', '$2b$12$xIygz54Gi4G/FROikCKhfej.JmnI8lSzR6RPpqiErQRUvnjSikOjO', 'First', 'Last', 'engineer@gmail.com', 'engineer', null);

-- Add 10 Demo Cars

INSERT INTO car (make, body_type, colour, no_seats, cost_per_hour, location, is_locked)
VALUES
    ('Toyota', 'SUV', 'Black', 5, 15, "-37.808880,144.965179", True),
    ('Tesla', 'Pickup', 'Silver', 6, 25, "-37.810219,144.961395", True),
    ('Toyota', 'Hatchback', 'Black', 5, 15, NULL, True),
    ('Honda', 'Sedan', 'Green', 5, 25, NULL, True),
    ('Mercedes', 'Hatchback', 'Black', 5, 40, NULL, True),
    ('Ferrari', 'Supercar', 'Red', 2, 65, NULL, True),
    ('Mazda', 'Coupe', 'White', 4, 25, NULL, True),
    ('BMW', 'Cabriolet', 'Black', 5, 30, NULL, True),
    ('Renault', 'Sedan', 'Yellow', 5, 35, NULL, True),
    ('Porsche', 'Truck', 'Black', 2, 65, NULL, True);

-- Add dummy bookings

INSERT INTO booking (car_id, username, duration, book_time)
VALUES
    (2, 'dummy', 1, '2020-05-09 02:22:51'),
    (1, 'dummy', 3, '2020-05-09 10:22:51');

-- Add dummy issues

INSERT INTO issue (car_id, time, details, resolved)
VALUES
    (1, '2020-05-09 02:22:51', "Broken tail light", True),
    (2, '2020-05-07 02:22:51', "Battery is dead", True),
    (1, '2020-06-01 02:22:51', "Flat tire", False);
