"""
==============================================
RUTAS DE LA APLICACIÓN WEB
==============================================
Este módulo define las páginas web y acciones
de la aplicación Flask.

Rutas disponibles:
- /             → Página principal (escribir post)
- /publicar     → Publicar un post
- /historial    → Ver historial de posts
- /borradores   → Ver borradores guardados

Autor: Ricardo Edreira
Fecha: Enero 2026
==============================================
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.cliente_x import ClienteX
from app.almacenamiento import (
    obtener_historial,
    obtener_borradores,
    guardar_borrador,
    eliminar_borrador,
    contar_posts_hoy
)
from app.config import es_modo_desarrollo

# Crear el Blueprint (grupo de rutas)
rutas = Blueprint('rutas', __name__)


# ==============================================
# PÁGINA PRINCIPAL - ESCRIBIR POST
# ==============================================

@rutas.route('/')
def inicio():
    """
    Página principal donde se escribe el post.
    """
    # Obtener información para mostrar
    posts_hoy = contar_posts_hoy()
    modo_desarrollo = es_modo_desarrollo()
    
    return render_template(
        'inicio.html',
        posts_hoy=posts_hoy,
        modo_desarrollo=modo_desarrollo
    )


# ==============================================
# PUBLICAR POST
# ==============================================

@rutas.route('/publicar', methods=['POST'])
def publicar():
    """
    Publica un post en X.
    
    Lee el texto del formulario y lo publica
    usando el cliente de X.
    """
    # Obtener el texto del formulario
    texto = request.form.get('texto', '')
    
    # Crear cliente y publicar
    cliente = ClienteX()
    resultado = cliente.publicar(texto)
    
    # Mostrar mensaje al usuario
    if resultado['exito']:
        flash(resultado['mensaje'], 'exito')
    else:
        flash(resultado['mensaje'], 'error')
    
    return redirect(url_for('rutas.inicio'))


# ==============================================
# HISTORIAL DE POSTS
# ==============================================

@rutas.route('/historial')
def historial():
    """
    Muestra el historial de posts publicados.
    """
    posts = obtener_historial()
    modo_desarrollo = es_modo_desarrollo()
    
    return render_template(
        'historial.html',
        posts=posts,
        modo_desarrollo=modo_desarrollo
    )


# ==============================================
# BORRADORES
# ==============================================

@rutas.route('/borradores')
def borradores():
    """
    Muestra los borradores guardados.
    """
    lista_borradores = obtener_borradores()
    modo_desarrollo = es_modo_desarrollo()
    
    return render_template(
        'borradores.html',
        borradores=lista_borradores,
        modo_desarrollo=modo_desarrollo
    )


@rutas.route('/borradores/guardar', methods=['POST'])
def guardar_nuevo_borrador():
    """
    Guarda un nuevo borrador.
    """
    texto = request.form.get('texto', '')
    
    if texto.strip():
        guardar_borrador(texto.strip())
        flash('Borrador guardado correctamente', 'exito')
    else:
        flash('El borrador no puede estar vacío', 'error')
    
    return redirect(url_for('rutas.inicio'))


@rutas.route('/borradores/eliminar/<id_borrador>', methods=['POST'])
def eliminar_un_borrador(id_borrador):
    """
    Elimina un borrador.
    """
    if eliminar_borrador(id_borrador):
        flash('Borrador eliminado', 'exito')
    else:
        flash('No se encontró el borrador', 'error')
    
    return redirect(url_for('rutas.borradores'))


@rutas.route('/borradores/publicar/<id_borrador>', methods=['POST'])
def publicar_borrador(id_borrador):
    """
    Publica un borrador directamente.
    """
    from app.almacenamiento import obtener_borrador
    
    borrador = obtener_borrador(id_borrador)
    
    if borrador:
        # Publicar el texto del borrador
        cliente = ClienteX()
        resultado = cliente.publicar(borrador['texto'])
        
        if resultado['exito']:
            # Eliminar el borrador después de publicar
            eliminar_borrador(id_borrador)
            flash(resultado['mensaje'], 'exito')
        else:
            flash(resultado['mensaje'], 'error')
    else:
        flash('No se encontró el borrador', 'error')
    
    return redirect(url_for('rutas.borradores'))
