const API_URL = 'https://backen-526209179050.europe-west1.run.app/api';

let cart = [];
let productos = [];

const sections = {
    shop: document.getElementById('shop-section'),
    admin: document.getElementById('admin-section'),
    cart: document.getElementById('cart-section')
};

function showSection(sectionName) {
    Object.values(sections).forEach(section => section.classList.add('hidden'));
    sections[sectionName].classList.remove('hidden');
}

function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;     
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');

    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

async function loadProductos() {
    try {
        const response = await fetch(`${API_URL}/productos`);
        productos = await response.json();
        renderProductos();
        renderAdminProductos();
    } catch (error) {
        console.error('Error cargando productos:', error);
        showNotification('Error al cargar los productos', 'error');
    }
}

function renderProductos() {
    const grid = document.getElementById('productos-grid');
    const categoryFilter = document.getElementById('category-filter').value;

    const filteredProductos = categoryFilter
        ? productos.filter(p => p.categoria === categoryFilter)
        : productos;

    if (filteredProductos.length === 0) {
        grid.innerHTML = '<p>No hay productos disponibles</p>';
        return;
    }

    grid.innerHTML = filteredProductos.map(producto => `
        <div class="producto-card">
            <img src="${producto.imagen_url || 'https://picsum.photos/200'}" alt="${producto.nombre}">
            <span class="categoria">${producto.categoria || 'Sin categoría'}</span>
            <h3>${producto.nombre}</h3>
            <p>${producto.descripcion || ''}</p>
            <p class="precio">${producto.precio.toFixed(2)} €</p>
            <p class="stock">Stock: ${producto.stock} unidades</p>
            <div class="producto-actions">
                <input type="number" id="cantidad-${producto.id}" value="1" min="1" max="${producto.stock}">
                <button class="btn btn-primary" onclick="addToCart(${producto.id})" ${producto.stock === 0 ? 'disabled' : ''}>
                    ${producto.stock === 0 ? 'Sin stock' : 'Añadir al carrito'}
                </button>
            </div>
        </div>
    `).join('');
}

function addToCart(productoId) {
    const producto = productos.find(p => p.id === productoId);
    const cantidad = parseInt(document.getElementById(`cantidad-${productoId}`).value);

    if (cantidad > producto.stock) {
        showNotification('No hay suficiente stock', 'error');
        return;
    }

    const existingItem = cart.find(item => item.producto.id === productoId);

    if (existingItem) {
        existingItem.cantidad += cantidad;
    } else {
        cart.push({ producto, cantidad });
    }

    updateCartCount();
    showNotification(`${producto.nombre} añadido al carrito`);
}

function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.cantidad, 0);
    document.getElementById('cart-count').textContent = count;
}

function renderCart() {
    const cartItems = document.getElementById('cart-items');
    const cartSummary = document.getElementById('cart-summary');

    if (cart.length === 0) {
        cartItems.innerHTML = '<p>El carrito está vacío</p>';
        cartSummary.classList.add('hidden');
        return;
    }

    const total = cart.reduce((sum, item) => sum + (item.producto.precio * item.cantidad), 0);

    cartItems.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-info">
                <h4>${item.producto.nombre}</h4>
                <p>${item.producto.precio.toFixed(2)} € x ${item.cantidad} = ${(item.producto.precio * item.cantidad).toFixed(2)} €</p>
            </div>
            <div class="cart-item-actions">
                <input type="number" value="${item.cantidad}" min="1" max="${item.producto.stock}"
                       onchange="updateCartItemQuantity(${index}, this.value)">
                <button class="btn btn-danger" onclick="removeFromCart(${index})">Eliminar</button>
            </div>
        </div>
    `).join('');

    document.getElementById('cart-total').textContent = total.toFixed(2);
    cartSummary.classList.remove('hidden');
}

function updateCartItemQuantity(index, newQuantity) {
    newQuantity = parseInt(newQuantity);
    const item = cart[index];

    if (newQuantity > item.producto.stock) {
        showNotification('No hay suficiente stock', 'error');
        renderCart();
        return;
    }

    if (newQuantity <= 0) {
        removeFromCart(index);
        return;
    }

    cart[index].cantidad = newQuantity;
    updateCartCount();
    renderCart();
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartCount();
    renderCart();
    showNotification('Producto eliminado del carrito');
}

async function checkout(event) {
    event.preventDefault();

    const clienteNombre = document.getElementById('cliente-nombre').value;
    const clienteEmail = document.getElementById('cliente-email').value;

    const total = cart.reduce((sum, item) => sum + (item.producto.precio * item.cantidad), 0);

    const pedido = {
        cliente_nombre: clienteNombre,
        cliente_email: clienteEmail,
        total: total,
        items: cart.map(item => ({
            producto_id: item.producto.id,
            cantidad: item.cantidad,
            precio_unitario: item.producto.precio
        }))
    };

    try {
        const response = await fetch(`${API_URL}/pedidos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(pedido)
        });

        if (response.ok) {
            showNotification('Pedido realizado con éxito');
            cart = [];
            updateCartCount();
            document.getElementById('checkout-form').reset();
            await loadProductos();
            showSection('shop');
        } else {
            showNotification('Error al realizar el pedido', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al realizar el pedido', 'error');
    }
}

function renderAdminProductos() {
    const list = document.getElementById('admin-productos-list');

    if (productos.length === 0) {
        list.innerHTML = '<p>No hay productos</p>';
        return;
    }

    list.innerHTML = productos.map(producto => `
        <div class="admin-producto-item">
            <div class="admin-producto-info">
                <h4>${producto.nombre}</h4>
                <p>${producto.descripcion || ''}</p>
                <p><strong>Precio:</strong> ${producto.precio.toFixed(2)} € | <strong>Stock:</strong> ${producto.stock}</p>
                <p><strong>Categoría:</strong> ${producto.categoria || 'Sin categoría'}</p>
            </div>
            <div class="admin-producto-actions">
                <button class="btn btn-secondary" onclick="editProducto(${producto.id})">Editar</button>
                <button class="btn btn-danger" onclick="deleteProducto(${producto.id})">Eliminar</button>
            </div>
        </div>
    `).join('');
}

function editProducto(id) {
    const producto = productos.find(p => p.id === id);

    document.getElementById('producto-id').value = producto.id;
    document.getElementById('producto-nombre').value = producto.nombre;
    document.getElementById('producto-descripcion').value = producto.descripcion || '';
    document.getElementById('producto-precio').value = producto.precio;
    document.getElementById('producto-stock').value = producto.stock;
    document.getElementById('producto-categoria').value = producto.categoria || '';
    document.getElementById('producto-imagen').value = producto.imagen_url || '';

    document.getElementById('cancel-edit').classList.remove('hidden');
    document.querySelector('#producto-form button[type="submit"]').textContent = 'Actualizar Producto';
}

async function deleteProducto(id) {
    if (!confirm('¿Estás seguro de eliminar este producto?')) return;

    try {
        const response = await fetch(`${API_URL}/productos/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showNotification('Producto eliminado correctamente');
            await loadProductos();
        } else {
            showNotification('Error al eliminar el producto', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al eliminar el producto', 'error');
    }
}

async function saveProducto(event) {
    event.preventDefault();

    const id = document.getElementById('producto-id').value;
    const producto = {
        nombre: document.getElementById('producto-nombre').value,
        descripcion: document.getElementById('producto-descripcion').value,
        precio: parseFloat(document.getElementById('producto-precio').value),
        stock: parseInt(document.getElementById('producto-stock').value),
        categoria: document.getElementById('producto-categoria').value,
        imagen_url: document.getElementById('producto-imagen').value
    };

    try {
        const url = id ? `${API_URL}/productos/${id}` : `${API_URL}/productos`;
        const method = id ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(producto)
        });

        if (response.ok) {
            showNotification(id ? 'Producto actualizado' : 'Producto creado');
            document.getElementById('producto-form').reset();
            document.getElementById('producto-id').value = '';
            document.getElementById('cancel-edit').classList.add('hidden');
            document.querySelector('#producto-form button[type="submit"]').textContent = 'Guardar Producto';
            await loadProductos();
        } else {
            showNotification('Error al guardar el producto', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error al guardar el producto', 'error');
    }
}

async function loadPedidos() {
    try {
        const response = await fetch(`${API_URL}/pedidos`);
        const pedidos = await response.json();
        renderPedidos(pedidos);
    } catch (error) {
        console.error('Error cargando pedidos:', error);
        showNotification('Error al cargar los pedidos', 'error');
    }
}

function renderPedidos(pedidos) {
    const list = document.getElementById('pedidos-list');

    if (pedidos.length === 0) {
        list.innerHTML = '<p>No hay pedidos</p>';
        return;
    }

    list.innerHTML = pedidos.map(pedido => `
        <div class="pedido-item">
            <div class="pedido-header">
                <div>
                    <h4>Pedido #${pedido.id}</h4>
                    <p><strong>Cliente:</strong> ${pedido.cliente_nombre} (${pedido.cliente_email})</p>
                    <p><strong>Total:</strong> ${pedido.total.toFixed(2)} €</p>
                    <p><strong>Fecha:</strong> ${new Date(pedido.fecha_pedido).toLocaleString()}</p>
                </div>
                <span class="pedido-estado ${pedido.estado}">${pedido.estado}</span>
            </div>
            <div class="pedido-items-list">
                <strong>Productos:</strong>
                <ul>
                    ${pedido.items.map(item => `
                        <li>${item.producto_nombre} - ${item.cantidad} x ${item.precio_unitario.toFixed(2)} € = ${item.subtotal.toFixed(2)} €</li>
                    `).join('')}
                </ul>
            </div>
        </div>
    `).join('');
}

async function initData() {
    try {
        const response = await fetch(`${API_URL}/init-data`, {
            method: 'POST'
        });

        if (response.ok) {
            showNotification('Datos iniciales cargados');
            await loadProductos();
        }
    } catch (error) {
        console.error('Error inicializando datos:', error);
    }
}

document.getElementById('admin-btn').addEventListener('click', () => {
    showSection('admin');
    loadPedidos();
});

document.getElementById('cart-btn').addEventListener('click', () => {
    showSection('cart');
    renderCart();
});

document.getElementById('back-to-shop').addEventListener('click', () => {
    showSection('shop');
});

document.getElementById('back-to-shop-from-cart').addEventListener('click', () => {
    showSection('shop');
});

document.getElementById('category-filter').addEventListener('change', renderProductos);

document.getElementById('producto-form').addEventListener('submit', saveProducto);

document.getElementById('cancel-edit').addEventListener('click', () => {
    document.getElementById('producto-form').reset();
    document.getElementById('producto-id').value = '';
    document.getElementById('cancel-edit').classList.add('hidden');
    document.querySelector('#producto-form button[type="submit"]').textContent = 'Guardar Producto';
});

document.getElementById('checkout-form').addEventListener('submit', checkout);

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));

        btn.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');

        if (tabName === 'pedidos') {
            loadPedidos();
        }
    });
});

window.addEventListener('DOMContentLoaded', async () => {
    await loadProductos();

    if (productos.length === 0) {
        await initData();
    }
});
