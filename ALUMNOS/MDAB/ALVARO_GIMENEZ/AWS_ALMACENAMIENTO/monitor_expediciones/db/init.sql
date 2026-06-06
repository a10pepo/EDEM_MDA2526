CREATE TABLE IF NOT EXISTS maestro_productos (
    id               SERIAL PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    categoria        VARCHAR(50)  NOT NULL,
    precio_unitario  NUMERIC(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS maestro_clientes (
    id      SERIAL PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL,
    empresa VARCHAR(100) NOT NULL,
    ciudad  VARCHAR(50)  NOT NULL
);

CREATE TABLE IF NOT EXISTS transacciones (
    id               SERIAL PRIMARY KEY,
    producto_id      INT NOT NULL REFERENCES maestro_productos(id),
    cliente_id       INT NOT NULL REFERENCES maestro_clientes(id),
    cantidad         INT NOT NULL,
    fecha_expedicion TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO maestro_productos (nombre, categoria, precio_unitario) VALUES
    ('Laptop ProX 15',        'Electrónica',    1299.99),
    ('Teclado Mecánico RGB',  'Periféricos',      89.95),
    ('Monitor UltraWide 34"', 'Electrónica',     599.00),
    ('Silla Ergonómica',      'Mobiliario',      349.50),
    ('Auriculares BT Pro',    'Audio',           129.00),
    ('Ratón Inalámbrico',     'Periféricos',      49.99),
    ('Webcam HD 1080p',       'Periféricos',      79.00),
    ('Disco SSD 1TB',         'Almacenamiento',   99.90),
    ('Hub USB-C 7 puertos',   'Accesorios',       35.00),
    ('Lámpara LED Escritorio','Mobiliario',        29.95);

INSERT INTO maestro_clientes (nombre, empresa, ciudad) VALUES
    ('Ana García',     'Soluciones Tech S.L.',    'Madrid'),
    ('Carlos López',   'InnovaData S.A.',          'Barcelona'),
    ('María Fernández','Grupo Digital Plus',        'Valencia'),
    ('Pedro Martínez', 'NextStep Consulting',       'Sevilla'),
    ('Laura Sánchez',  'DataFlow Systems',          'Bilbao'),
    ('Javier Torres',  'Kirotech S.A.',             'Zaragoza'),
    ('Elena Ruiz',     'CloudBase Corp.',           'Málaga'),
    ('Sergio Mora',    'Impulso Digital',           'Valladolid');
