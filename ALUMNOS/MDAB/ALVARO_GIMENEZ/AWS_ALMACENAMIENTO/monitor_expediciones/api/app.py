import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

load_dotenv()

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "almacen_db")
DB_USER = os.getenv("DB_USER", "almacen_user")
DB_PASS = os.getenv("DB_PASS", "almacen_pass")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class MaestroProducto(db.Model):
    __tablename__ = "maestro_productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    precio_unitario = db.Column(db.Numeric(10, 2))


class MaestroCliente(db.Model):
    __tablename__ = "maestro_clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    empresa = db.Column(db.String(100))
    ciudad = db.Column(db.String(50))


class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("maestro_productos.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("maestro_clientes.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_expedicion = db.Column(db.DateTime, default=datetime.utcnow)

    producto = db.relationship("MaestroProducto")
    cliente = db.relationship("MaestroCliente")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/metrics")
def metrics():
    since = datetime.utcnow() - timedelta(hours=24)

    base_q = db.session.query(Transaccion).filter(Transaccion.fecha_expedicion >= since)

    total_transacciones = base_q.count()
    total_unidades = db.session.query(func.sum(Transaccion.cantidad)).filter(
        Transaccion.fecha_expedicion >= since
    ).scalar() or 0
    clientes_unicos = db.session.query(func.count(func.distinct(Transaccion.cliente_id))).filter(
        Transaccion.fecha_expedicion >= since
    ).scalar() or 0

    top_productos = (
        db.session.query(MaestroProducto.nombre, func.sum(Transaccion.cantidad).label("total"))
        .join(Transaccion, MaestroProducto.id == Transaccion.producto_id)
        .filter(Transaccion.fecha_expedicion >= since)
        .group_by(MaestroProducto.nombre)
        .order_by(func.sum(Transaccion.cantidad).desc())
        .limit(5)
        .all()
    )

    top_clientes = (
        db.session.query(MaestroCliente.nombre, func.sum(Transaccion.cantidad).label("total"))
        .join(Transaccion, MaestroCliente.id == Transaccion.cliente_id)
        .filter(Transaccion.fecha_expedicion >= since)
        .group_by(MaestroCliente.nombre)
        .order_by(func.sum(Transaccion.cantidad).desc())
        .limit(5)
        .all()
    )

    return jsonify({
        "total_transacciones": total_transacciones,
        "total_unidades": int(total_unidades),
        "clientes_unicos": clientes_unicos,
        "top_productos": [{"nombre": r.nombre, "total": int(r.total)} for r in top_productos],
        "top_clientes": [{"nombre": r.nombre, "total": int(r.total)} for r in top_clientes],
    })


@app.route("/api/transactions")
def transactions():
    rows = (
        db.session.query(Transaccion)
        .order_by(Transaccion.fecha_expedicion.desc())
        .limit(20)
        .all()
    )
    return jsonify([
        {
            "id": r.id,
            "producto": r.producto.nombre,
            "categoria": r.producto.categoria,
            "cliente": r.cliente.nombre,
            "empresa": r.cliente.empresa,
            "cantidad": r.cantidad,
            "fecha_expedicion": r.fecha_expedicion.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for r in rows
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
