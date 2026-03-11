from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from models import db, Producto, Pedido, ItemPedido

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/productos', methods=['GET'])
def get_productos():
    productos = Producto.query.all()
    return jsonify([p.to_dict() for p in productos])

@app.route('/api/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(producto.to_dict())

@app.route('/api/productos', methods=['POST'])
def create_producto():
    data = request.get_json()

    nuevo_producto = Producto(
        nombre=data['nombre'],
        descripcion=data.get('descripcion', ''),
        precio=data['precio'],
        stock=data.get('stock', 0),
        imagen_url=data.get('imagen_url', ''),
        categoria=data.get('categoria', '')
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    return jsonify(nuevo_producto.to_dict()), 201

@app.route('/api/productos/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.get_json()

    producto.nombre = data.get('nombre', producto.nombre)
    producto.descripcion = data.get('descripcion', producto.descripcion)
    producto.precio = data.get('precio', producto.precio)
    producto.stock = data.get('stock', producto.stock)
    producto.imagen_url = data.get('imagen_url', producto.imagen_url)
    producto.categoria = data.get('categoria', producto.categoria)

    db.session.commit()

    return jsonify(producto.to_dict())

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    return jsonify({'message': 'Producto eliminado correctamente'}), 200

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([p.to_dict() for p in pedidos])

@app.route('/api/pedidos/<int:id>', methods=['GET'])
def get_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    return jsonify(pedido.to_dict())

@app.route('/api/pedidos', methods=['POST'])
def create_pedido():
    data = request.get_json()

    nuevo_pedido = Pedido(
        cliente_nombre=data['cliente_nombre'],
        cliente_email=data['cliente_email'],
        total=data['total'],
        estado='pendiente'
    )

    db.session.add(nuevo_pedido)
    db.session.flush()

    for item_data in data.get('items', []):
        item = ItemPedido(
            pedido_id=nuevo_pedido.id,
            producto_id=item_data['producto_id'],
            cantidad=item_data['cantidad'],
            precio_unitario=item_data['precio_unitario']
        )
        db.session.add(item)

        producto = Producto.query.get(item_data['producto_id'])
        if producto:
            producto.stock -= item_data['cantidad']

    db.session.commit()

    return jsonify(nuevo_pedido.to_dict()), 201

@app.route('/api/pedidos/<int:id>', methods=['PUT'])
def update_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    data = request.get_json()

    pedido.estado = data.get('estado', pedido.estado)

    db.session.commit()

    return jsonify(pedido.to_dict())

@app.route('/api/init-data', methods=['POST'])
def init_data():
    if Producto.query.count() > 0:
        return jsonify({'message': 'La base de datos ya tiene datos'}), 400

    productos_iniciales = [
        Producto(nombre='Camiseta Universidad', descripcion='Camiseta oficial con logo', precio=19.99, stock=50, categoria='Ropa', imagen_url='https://picsum.photos/200?random=1'),
        Producto(nombre='Sudadera', descripcion='Sudadera con capucha', precio=39.99, stock=30, categoria='Ropa', imagen_url='https://picsum.photos/200?random=2'),
        Producto(nombre='Taza Universidad', descripcion='Taza de cerámica con logo', precio=9.99, stock=100, categoria='Accesorios', imagen_url='https://picsum.photos/200?random=3'),
        Producto(nombre='Bolígrafo', descripcion='Pack de 5 bolígrafos', precio=5.99, stock=200, categoria='Papelería', imagen_url='https://picsum.photos/200?random=4'),
        Producto(nombre='Mochila', descripcion='Mochila deportiva grande', precio=29.99, stock=40, categoria='Accesorios', imagen_url='https://picsum.photos/200?random=5'),
        Producto(nombre='Gorra', descripcion='Gorra con logo bordado', precio=14.99, stock=60, categoria='Accesorios', imagen_url='https://picsum.photos/200?random=6'),
    ]

    for producto in productos_iniciales:
        db.session.add(producto)

    db.session.commit()

    return jsonify({'message': f'{len(productos_iniciales)} productos inicializados correctamente'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
