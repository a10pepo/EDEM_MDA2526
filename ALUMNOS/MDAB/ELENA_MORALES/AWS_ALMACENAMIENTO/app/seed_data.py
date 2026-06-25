# Datos de ejemplo de la tienda Sephora (equivalente a los cuadernos del padre de Jacinto)
# Estructura paralela al ejercicio del aeródromo:
#   aviones    -> products  (productos en el almacén / estantería)
#   vuelos     -> orders     (pedidos / ventas)
#   pasajeros  -> customers  (clientes)

# ---------------------------------------------------------------------------
# PRODUCTOS (en almacén)  ~ aviones en el hangar
#   expiryDate  -> fecha de caducidad   (~ nextMaintenanceDate)
#   maxStock    -> stock máximo          (~ capacity, para la alerta del 10%)
# ---------------------------------------------------------------------------
products = [
    {
        "productCode": "SEP-001",
        "name": "Soft Pinch Liquid Blush",
        "brand": "Rare Beauty",
        "category": "Colorete",
        "manufactureDate": "2025-01-10",
        "expiryDate": "2026-07-15",        # caduca pronto -> dispara alerta
        "maxStock": 200,
        "supplierId": "S-12345",
        "supplierName": "Rare Beauty Inc.",
        "shelfId": "A-01",
        "price": 23.00,
    },
    {
        "productCode": "SEP-002",
        "name": "Pro Filt'r Soft Matte Foundation",
        "brand": "Fenty Beauty",
        "category": "Base de maquillaje",
        "manufactureDate": "2025-03-01",
        "expiryDate": "2027-03-01",
        "maxStock": 150,
        "supplierId": "S-23456",
        "supplierName": "Fenty Beauty LLC",
        "shelfId": "A-02",
        "price": 39.00,
    },
    {
        "productCode": "SEP-003",
        "name": "Matte Revolution Lipstick (Pillow Talk)",
        "brand": "Charlotte Tilbury",
        "category": "Labial",
        "manufactureDate": "2024-11-20",
        "expiryDate": "2026-08-20",        # caduca pronto -> dispara alerta
        "maxStock": 120,
        "supplierId": "S-34567",
        "supplierName": "Charlotte Tilbury Beauty Ltd.",
        "shelfId": "B-01",
        "price": 35.00,
    },
    {
        "productCode": "SEP-004",
        "name": "Eyeshadow Palette Nude",
        "brand": "Sephora Collection",
        "category": "Sombra de ojos",
        "manufactureDate": "2025-06-01",
        "expiryDate": "2028-06-01",
        "maxStock": 300,
        "supplierId": "S-45678",
        "supplierName": "Sephora Collection",
        "shelfId": "B-02",
        "price": 28.00,
    },
    {
        "productCode": "SEP-005",
        "name": "Radiant Creamy Concealer",
        "brand": "NARS",
        "category": "Corrector",
        "manufactureDate": "2025-02-15",
        "expiryDate": "2027-02-15",
        "maxStock": 100,
        "supplierId": "S-56789",
        "supplierName": "NARS Cosmetics",
        "shelfId": "A-03",
        "price": 31.00,
    },
]


# ---------------------------------------------------------------------------
# PEDIDOS (ventas)  ~ vuelos que aterrizan
#   unitsSold   -> unidades vendidas       (~ occupiedSeats / fuelConsumption)
#   customerIds -> clientes y su estado     (~ passengerIds con boarding status)
#   Estados de cliente: 'Confirmed' / 'Cancelled' / 'Returned'
# ---------------------------------------------------------------------------
orders = [
    {
        "orderId": "ORD-2026-001",
        "productCode": "SEP-001",
        "orderDate": "2026-05-01T10:30:00",
        "shipDate": "2026-05-03T09:00:00",
        "unitsSold": 30,                   # 30 > 10% de 200 (=20) -> alerta de pedido grande
        "channel": "Online",
        "store": "Sephora Gran Vía Madrid",
        "customerIds": [("C-1001", "Confirmed"), ("C-1002", "Confirmed"),
                        ("C-1003", "Cancelled"), ("C-1004", "Confirmed")],
    },
    {
        "orderId": "ORD-2026-002",
        "productCode": "SEP-005",
        "orderDate": "2026-05-10T16:15:00",
        "shipDate": "2026-05-12T11:00:00",
        "unitsSold": 95,                   # deja 5 unidades disponibles -> alerta de stock bajo
        "channel": "Tienda física",
        "store": "Sephora Barcelona Paseo de Gracia",
        "customerIds": [("C-1005", "Confirmed"), ("C-1006", "Returned"),
                        ("C-1007", "Confirmed")],
    },
    {
        "orderId": "ORD-2026-003",
        "productCode": "SEP-002",
        "orderDate": "2026-05-20T12:00:00",
        "shipDate": "2026-05-21T10:00:00",
        "unitsSold": 12,
        "channel": "Online",
        "store": "Sephora Valencia Colón",
        "customerIds": [("C-1008", "Confirmed"), ("C-1009", "Confirmed"),
                        ("C-1010", "Cancelled")],
    },
]


# ---------------------------------------------------------------------------
# CLIENTES  ~ pasajeros
# ---------------------------------------------------------------------------
customers = [
    {"customerId": "C-1001", "name": "Ana García Martínez",     "nationalId": "12345678A", "dateOfBirth": "1991-05-15"},
    {"customerId": "C-1002", "name": "Carlos Rodríguez López",  "nationalId": "87654321B", "dateOfBirth": "1973-11-30"},
    {"customerId": "C-1003", "name": "Elena Sánchez García",    "nationalId": "11223344C", "dateOfBirth": "1988-03-25"},
    {"customerId": "C-1004", "name": "Javier Martínez Pérez",   "nationalId": "44332211D", "dateOfBirth": "1995-07-10"},
    {"customerId": "C-1005", "name": "María López Rodríguez",   "nationalId": "33441122E", "dateOfBirth": "1985-09-05"},
    {"customerId": "C-1006", "name": "Pedro García Sánchez",    "nationalId": "22114433F", "dateOfBirth": "1979-01-20"},
    {"customerId": "C-1007", "name": "Sara Pérez Martínez",     "nationalId": "55443322G", "dateOfBirth": "1999-12-15"},
    {"customerId": "C-1008", "name": "Juan Sánchez López",      "nationalId": "66554433H", "dateOfBirth": "1977-08-25"},
    {"customerId": "C-1009", "name": "Lucía Martínez García",   "nationalId": "77665544I", "dateOfBirth": "1990-02-10"},
    {"customerId": "C-1010", "name": "Antonio García López",    "nationalId": "88776655J", "dateOfBirth": "1980-06-05"},
]
