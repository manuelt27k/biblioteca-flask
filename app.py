from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)


# CONEXIÓN A BASE DE DATOS

def get_connection():
    return mysql.connector.connect(
        host="192.168.1.148",
        user="biblioweb",
        password="Web.2026",
        database="adminbiblio"
    )


# HOME

@app.route('/')
def index():
    return render_template("index.html")


#	USUARIOS


# LISTAR

@app.route('/usuarios')
def usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    data = cursor.fetchall()
    conn.close()
    return render_template("usuarios.html", usuarios=data)

# CREATE

@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form['telefono']
        fecha = request.form['fecha']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nombre, apellidos, email, telefono, fecha_registro)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, apellidos, email, telefono, fecha))

        conn.commit()
        conn.close()

        return redirect(url_for('usuarios'))

    return render_template("nuevo_usuario.html")

@app.route('/libros/nuevo', methods=['GET', 'POST'])
def nuevo_libro():
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        isbn = request.form['isbn']
        anio = request.form['anio']
        stock = request.form['stock']
        autor = request.form['autor']
        categoria = request.form['categoria']

        cursor.execute("""
            INSERT INTO libros (titulo, isbn, anio_publicacion, stock, id_autor, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (titulo, isbn, anio, stock, autor, categoria))

        conn.commit()
        conn.close()
        return redirect(url_for('libros'))

    cursor.execute("SELECT id_autor, nombre_autor FROM autores")
    autores = cursor.fetchall()

    cursor.execute("SELECT id_categoria, nombre_categoria FROM categorias")
    categorias = cursor.fetchall()

    conn.close()

    return render_template("nuevo_libro.html", autores=autores, categorias=categorias)

# DELETE

@app.route('/usuarios/borrar/<int:id>')
def borrar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('usuarios'))

# UPDATE

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        telefono = request.form['telefono']

        cursor.execute("""
            UPDATE usuarios
            SET nombre=%s, apellidos=%s, email=%s, telefono=%s
            WHERE id_usuario=%s
        """, (nombre, apellidos, email, telefono, id))

        conn.commit()
        conn.close()
        return redirect(url_for('usuarios'))

    cursor.execute("SELECT * FROM usuarios WHERE id_usuario=%s", (id,))
    usuario = cursor.fetchone()
    conn.close()

    return render_template("editar_usuario.html", usuario=usuario)

@app.route('/libros/editar/<int:id>', methods=['GET', 'POST'])
def editar_libro(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        titulo = request.form['titulo']
        isbn = request.form['isbn']
        anio = request.form['anio']
        stock = request.form['stock']

        cursor.execute("""
            UPDATE libros
            SET titulo=%s, isbn=%s, anio_publicacion=%s, stock=%s
            WHERE id_libro=%s
        """, (titulo, isbn, anio, stock, id))

        conn.commit()
        conn.close()
        return redirect(url_for('libros'))

    cursor.execute("SELECT * FROM libros WHERE id_libro=%s", (id,))
    libro = cursor.fetchone()

    conn.close()

    return render_template("editar_libro.html", libro=libro)


#          LIBROS


@app.route('/libros')
def libros():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT libros.id_libro, libros.titulo, libros.isbn, libros.stock,
               autores.nombre_autor, categorias.nombre_categoria
        FROM libros
        LEFT JOIN autores ON libros.id_autor = autores.id_autor
        LEFT JOIN categorias ON libros.id_categoria = categorias.id_categoria
    """)

    data = cursor.fetchall()
    conn.close()
    return render_template("libros.html", libros=data)



#        PRESTAMOS


@app.route('/prestamos')
def prestamos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT prestamos.id_prestamo, usuarios.nombre, libros.titulo,
               prestamos.fecha_prestamo, prestamos.fecha_devolucion, prestamos.estado
        FROM prestamos
        LEFT JOIN usuarios ON prestamos.id_usuario = usuarios.id_usuario
        LEFT JOIN libros ON prestamos.id_libro = libros.id_libro
    """)

    data = cursor.fetchall()
    conn.close()
    return render_template("prestamos.html", prestamos=data)


# RUN


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
