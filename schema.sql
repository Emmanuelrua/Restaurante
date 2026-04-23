-- ============================================================
-- Restaurante CLI — Esquema PostgreSQL para Supabase
-- Tablas: meseros, platillos, mesas, pedidos, detalle_pedido
-- ============================================================


-- ── Tabla: meseros ──────────────────────────────────────────
-- SERIAL: el sistema genera el ID automáticamente al insertar
CREATE TABLE IF NOT EXISTS meseros (
    mesero_id  SERIAL       PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    pin        CHAR(4)      NOT NULL,
    CONSTRAINT chk_pin_numerico CHECK (pin ~ '^\d{4}$')
);

-- ── Tabla: platillos ────────────────────────────────────────
-- SERIAL: el sistema genera el ID automáticamente; precio en COP
CREATE TABLE IF NOT EXISTS platillos (
    platillo_id SERIAL        PRIMARY KEY,
    nombre      VARCHAR(100)  NOT NULL,
    precio      NUMERIC(10,2) NOT NULL,
    categoria   VARCHAR(20)   NOT NULL,
    disponible  BOOLEAN       NOT NULL DEFAULT TRUE,
    CONSTRAINT chk_precio_positivo CHECK (precio > 0),
    CONSTRAINT chk_categoria_valida
        CHECK (categoria IN ('entrada', 'plato_fuerte', 'postre', 'bebida'))
);

-- ── Tabla: mesas ────────────────────────────────────────────
-- SERIAL porque el sistema asigna IDs automáticamente
CREATE TABLE IF NOT EXISTS mesas (
    mesa_id   SERIAL      PRIMARY KEY,
    numero    INTEGER     NOT NULL UNIQUE,
    capacidad INTEGER     NOT NULL,
    estado    VARCHAR(20) NOT NULL DEFAULT 'disponible',
    CONSTRAINT chk_numero_positivo    CHECK (numero > 0),
    CONSTRAINT chk_capacidad_positiva CHECK (capacidad > 0),
    CONSTRAINT chk_estado_mesa
        CHECK (estado IN ('disponible', 'ocupada', 'reservada'))
);

-- ── Tabla: pedidos ──────────────────────────────────────────
-- Relaciona una mesa con un mesero; SERIAL para ID autogenerado
CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id  SERIAL        PRIMARY KEY,
    mesa_id    INTEGER       NOT NULL,
    mesero_id  INTEGER       NOT NULL,
    fecha_hora TIMESTAMP     NOT NULL DEFAULT NOW(),
    estado     VARCHAR(20)   NOT NULL DEFAULT 'abierto',
    total      NUMERIC(10,2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_pedido_mesa    FOREIGN KEY (mesa_id)   REFERENCES mesas(mesa_id)    ON DELETE RESTRICT,
    CONSTRAINT fk_pedido_mesero  FOREIGN KEY (mesero_id) REFERENCES meseros(mesero_id) ON DELETE RESTRICT,
    CONSTRAINT chk_total_no_negativo CHECK (total >= 0),
    CONSTRAINT chk_estado_pedido
        CHECK (estado IN ('abierto', 'cerrado', 'cancelado'))
);

-- ── Tabla: detalle_pedido ───────────────────────────────────
-- Líneas de un pedido; CASCADE para que al borrar un pedido se borren sus ítems
CREATE TABLE IF NOT EXISTS detalle_pedido (
    detalle_id      SERIAL        PRIMARY KEY,
    pedido_id       INTEGER       NOT NULL,
    platillo_id     INTEGER       NOT NULL,
    cantidad        INTEGER       NOT NULL DEFAULT 1,
    precio_unitario NUMERIC(10,2) NOT NULL,
    subtotal        NUMERIC(10,2) NOT NULL,
    CONSTRAINT fk_detalle_pedido   FOREIGN KEY (pedido_id)   REFERENCES pedidos(pedido_id)    ON DELETE CASCADE,
    CONSTRAINT fk_detalle_platillo FOREIGN KEY (platillo_id) REFERENCES platillos(platillo_id) ON DELETE RESTRICT,
    CONSTRAINT chk_cantidad_positiva        CHECK (cantidad > 0),
    CONSTRAINT chk_precio_unitario_positivo CHECK (precio_unitario > 0),
    CONSTRAINT chk_subtotal_positivo        CHECK (subtotal > 0)
);


-- ============================================================
-- DATOS DE PRUEBA
-- ============================================================

-- ── Meseros ──────────────────────────────────────────────────
-- mesero_id es SERIAL: PostgreSQL lo genera automáticamente
INSERT INTO meseros (nombre, pin) VALUES
('Carlos Pérez',    '1234'),
('Laura Gómez',     '5678'),
('Andrés Torres',   '9012'),
('Valentina Ríos',  '3456'),
('Santiago Mora',   '7890'),
('Camila Herrera',  '2468'),
('Julián Castillo', '1357'),
('Natalia Vargas',  '8642'),
('Diego Salcedo',   '9753'),
('Paola Mendoza',   '4321');

-- ── Platillos ────────────────────────────────────────────────
-- platillo_id es SERIAL: PostgreSQL lo genera automáticamente
INSERT INTO platillos (nombre, precio, categoria, disponible) VALUES
('Sopa de tomate',      12000.00, 'entrada',      TRUE),
('Ensalada César',      15000.00, 'entrada',      TRUE),
('Bandeja paisa',       35000.00, 'plato_fuerte', TRUE),
('Churrasco',           42000.00, 'plato_fuerte', TRUE),
('Brownie con helado',  14000.00, 'postre',       TRUE),
('Jugo de maracuyá',     8000.00, 'bebida',       TRUE),
('Arepas con hogao',     9000.00, 'entrada',      TRUE),
('Pollo a la plancha',  28000.00, 'plato_fuerte', TRUE),
('Flan de caramelo',    11000.00, 'postre',       TRUE),
('Limonada de coco',     9500.00, 'bebida',       TRUE),
('Caldo de costilla',   13000.00, 'entrada',      TRUE),
('Lomo al trapo',       45000.00, 'plato_fuerte', FALSE),
('Arroz con leche',     10000.00, 'postre',       TRUE),
('Agua de panela',       5000.00, 'bebida',       TRUE);

-- ── Mesas ────────────────────────────────────────────────────
INSERT INTO mesas (numero, capacidad, estado) VALUES
(1,   2, 'disponible'),
(2,   4, 'ocupada'),
(3,   4, 'disponible'),
(4,   6, 'reservada'),
(5,   2, 'disponible'),
(6,   8, 'disponible'),
(7,   4, 'ocupada'),
(8,   4, 'disponible'),
(9,   6, 'disponible'),
(10,  2, 'disponible'),
(11, 10, 'reservada'),
(12,  4, 'disponible');

-- ── Pedidos ───────────────────────────────────────────────────
INSERT INTO pedidos (mesa_id, mesero_id, fecha_hora, estado, total) VALUES
(2,  1,  '2026-04-23 12:00:00', 'abierto',    65000.00),
(7,  2,  '2026-04-23 12:15:00', 'abierto',    61000.00),
(4,  3,  '2026-04-23 11:30:00', 'cerrado',   110000.00),
(1,  4,  '2026-04-23 13:00:00', 'cerrado',    42000.00),
(3,  5,  '2026-04-23 12:45:00', 'abierto',    35000.00),
(5,  6,  '2026-04-23 11:00:00', 'cancelado',      0.00),
(6,  7,  '2026-04-23 13:30:00', 'abierto',    86000.00),
(8,  8,  '2026-04-23 14:00:00', 'cerrado',    60000.00),
(9,  9,  '2026-04-23 14:15:00', 'abierto',    51500.00),
(10, 10, '2026-04-23 14:30:00', 'cerrado',    20000.00);

-- ── Detalle de pedido ────────────────────────────────────────
-- Pedido 1 (mesa 2, mesero Carlos): Bandeja + 2 Jugos + Brownie = 65 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(1, 3, 1, 35000.00, 35000.00),
(1, 6, 2,  8000.00, 16000.00),
(1, 5, 1, 14000.00, 14000.00);

-- Pedido 2 (mesa 7, mesero Laura): Churrasco + 2 Limonadas = 61 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(2, 4,  1, 42000.00, 42000.00),
(2, 10, 2,  9500.00, 19000.00);

-- Pedido 3 (mesa 4, mesero Andrés): 2 Bandejas + 2 Sopas + 2 Jugos = 110 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(3, 3, 2, 35000.00, 70000.00),
(3, 1, 2, 12000.00, 24000.00),
(3, 6, 2,  8000.00, 16000.00);

-- Pedido 4 (mesa 1, mesero Valentina): Churrasco = 42 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(4, 4, 1, 42000.00, 42000.00);

-- Pedido 5 (mesa 3, mesero Santiago): Bandeja paisa = 35 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(5, 3, 1, 35000.00, 35000.00);

-- Pedido 6 fue cancelado — sin ítems

-- Pedido 7 (mesa 6, mesero Julián): 2 Pollos + 2 Ensaladas = 86 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(7, 8, 2, 28000.00, 56000.00),
(7, 2, 2, 15000.00, 30000.00);

-- Pedido 8 (mesa 8, mesero Natalia): Pollo + 2 Flanes + 2 Aguas = 60 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(8, 8,  1, 28000.00, 28000.00),
(8, 9,  2, 11000.00, 22000.00),
(8, 14, 2,  5000.00, 10000.00);

-- Pedido 9 (mesa 9, mesero Diego): Churrasco + Limonada = 51 500
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(9, 4,  1, 42000.00, 42000.00),
(9, 10, 1,  9500.00,  9500.00);

-- Pedido 10 (mesa 10, mesero Paola): Ensalada + Agua = 20 000
INSERT INTO detalle_pedido (pedido_id, platillo_id, cantidad, precio_unitario, subtotal) VALUES
(10, 2,  1, 15000.00, 15000.00),
(10, 14, 1,  5000.00,  5000.00);
