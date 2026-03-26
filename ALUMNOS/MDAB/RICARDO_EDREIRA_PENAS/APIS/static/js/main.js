/* JavaScript - Funciones interactivas */

// Actualiza el contador de caracteres
function actualizarContador() {
    const textarea = document.getElementById('texto-post');
    const contadorTexto = document.getElementById('caracteres-actuales');
    const barraRelleno = document.getElementById('barra-relleno');

    if (!textarea) return;

    const caracteres = textarea.value.length;
    contadorTexto.textContent = caracteres;

    const porcentaje = (caracteres / 280) * 100;
    barraRelleno.style.width = porcentaje + '%';

    barraRelleno.classList.remove('advertencia', 'lleno');
    if (caracteres >= 280) {
        barraRelleno.classList.add('lleno');
        contadorTexto.style.color = '#f4212e';
    } else if (caracteres >= 260) {
        barraRelleno.classList.add('advertencia');
        contadorTexto.style.color = '#ffad1f';
    } else {
        contadorTexto.style.color = '#8b98a5';
    }
}

// Muestra modal de confirmación
function confirmarPublicacion() {
    const textarea = document.getElementById('texto-post');
    const texto = textarea.value.trim();

    if (!texto) {
        alert('¡Escribe algo antes de publicar!');
        return;
    }

    if (texto.length > 280) {
        alert('El post es muy largo. Máximo 280 caracteres.');
        return;
    }

    document.getElementById('preview-texto').textContent = texto;
    document.getElementById('modal-confirmacion').style.display = 'flex';
}

// Cierra el modal
function cerrarModal() {
    document.getElementById('modal-confirmacion').style.display = 'none';
}

// Publica el post
function publicarPost() {
    document.getElementById('form-post').submit();
}

// Guarda borrador
function guardarBorrador() {
    const textarea = document.getElementById('texto-post');
    const texto = textarea.value.trim();

    if (!texto) {
        alert('¡Escribe algo antes de guardar!');
        return;
    }

    document.getElementById('texto-borrador').value = texto;
    document.getElementById('form-borrador').submit();
}

// Cerrar modal con Escape
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') cerrarModal();
});

// Inicialización
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('texto-post');

    if (textarea) {
        textarea.addEventListener('input', actualizarContador);
        actualizarContador();
        textarea.focus();
    }

    const modal = document.getElementById('modal-confirmacion');
    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) cerrarModal();
        });
    }
});
