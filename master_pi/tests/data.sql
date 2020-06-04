-- Add dummy users

INSERT INTO user (username, password, f_name, l_name, email, role)
VALUES
  ('dummy', '$2b$12$xIygz54Gi4G/FROikCKhfej.JmnI8lSzR6RPpqiErQRUvnjSikOjO', 'First', 'Last', 'dummyemail@gmail.com', 'default'),
  ('john', '$2b$12$pUSt0xQDEsdaHmXtNJ7BaOlN8NzqL5.tFucHTwyL6nf7o6KvAl9p', 'John', 'Doe', 'john.doe@outlook.com', 'default');

-- Add 10 Demo Cars

INSERT INTO car (make, body_type, colour, no_seats, cost_per_hour, is_locked)
VALUES
    ('Toyota', 'SUV', 'Black', 5, 15, True),
    ('Tesla', 'Pickup', 'Silver', 6, 25, True),
    ('Toyota', 'Hatchback', 'Black', 5, 15, True),
    ('Honda', 'Sedan', 'Green', 5, 25, True),
    ('Mercedes', 'Hatchback', 'Black', 5, 40, True),
    ('Ferrari', 'Supercar', 'Red', 2, 65, True),
    ('Mazda', 'Coupe', 'White', 4, 25, True),
    ('BMW', 'Cabriolet', 'Black', 5, 30, True),
    ('Renault', 'Sedan', 'Yellow', 5, 35, True),
    ('Porsche', 'Truck', 'Black', 2, 65, True);

-- Add dummy bookings

INSERT INTO booking (car_id, username, duration, book_time)
VALUES
    (2, 'dummy', 1, '2020-05-09 02:22:51'),
    (1, 'dummy', 3, '2020-05-09 10:22:51');
