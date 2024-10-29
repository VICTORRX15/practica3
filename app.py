from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

@app.route("/")
def registro_seminarios():
    return render_template('index.html')

@app.route("/listado_inscritos", methods=['GET'])
def listado_inscritos():
    if 'inscritos' not in session:
        session['inscritos'] = []
    return render_template('listado.html', inscritos=session['inscritos'])

@app.route("/agregar_inscripcion", methods=['POST'])
def agregar_inscripcion():
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    turno = request.form['turno']
    seminarios = request.form.getlist('seminarios')

    nueva_inscripcion = {
        'fecha': fecha,
        'nombre': nombre,
        'apellidos': apellidos,
        'turno': turno,
        'seminarios': seminarios
    }

    if 'inscritos' not in session:
        session['inscritos'] = []
    session['inscritos'].append(nueva_inscripcion)
    session.modified = True

    return redirect(url_for('listado_inscritos'))

@app.route("/eliminar_inscripcion/<int:index>", methods=['GET'])
def eliminar_inscripcion(index):
    if 'inscritos' in session:
        del session['inscritos'][index]
        session.modified = True
    return redirect(url_for('listado_inscritos'))

@app.route("/editar_inscripcion/<int:index>", methods=['GET', 'POST'])
def editar_inscripcion(index):
    if 'inscritos' in session:
        if request.method == 'POST':
            fecha = request.form['fecha']
            nombre = request.form['nombre']
            apellidos = request.form['apellidos']
            turno = request.form['turno']
            seminarios = request.form.getlist('seminarios')

            session['inscritos'][index] = {
                'fecha': fecha,
                'nombre': nombre,
                'apellidos': apellidos,
                'turno': turno,
                'seminarios': seminarios
            }
            session.modified = True
            return redirect(url_for('listado_inscritos'))
        else:
            inscrito = session['inscritos'][index]
            return render_template('editar.html', inscrito=inscrito, index=index)
    return redirect(url_for('listado_inscritos'))

@app.route("/vaciar")
def vaciar():
    session.pop('inscritos', None)
    return redirect(url_for('registro_seminarios'))

if __name__ == "__main__":
    app.run(debug=True)