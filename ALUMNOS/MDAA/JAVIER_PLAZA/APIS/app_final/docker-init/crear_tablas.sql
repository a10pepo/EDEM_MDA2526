CREATE TABLE IF NOT EXISTS alimentos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE,
    tipo VARCHAR(50),
    calorias FLOAT,
    grasas FLOAT,
    carbohidratos FLOAT,
    azucar FLOAT,
    proteina FLOAT,
    publicado BOOLEAN
);

CREATE TABLE IF NOT EXISTS credenciales (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL
);