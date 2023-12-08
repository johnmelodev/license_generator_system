from flask import Flask, jsonify, request, make_response
from estrutura_banco_de_dados import Usuario, Licenca, app, db
import json
import jwt
from datetime import datetime, timedelta
from functools import wraps


def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Verificar se um token foi enviado
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'mensagem': 'Token não foi incluído!'}, 401)
        # Se temos um token, validar acesso consultando o BD
        try:
            resultado = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Usuario.query.filter_by(
                id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'mensagem': 'Token é inválido'}, 401)
        return f(*args, **kwargs)
    return decorated


@app.route("/")
@token_obrigatorio
def obter_todas_chaves():
    licencas = Licenca.query.all()
    lista_licencas = []

    for licenca in licencas:
        dados = {}
        dados['licenca'] = licenca.licenca
        lista_licencas.append(dados)

    return jsonify({'Licenças': lista_licencas})


@app.route("/chaves/<string:chave>", methods=['GET'])
def validar_chave(chave):
    licenca = Licenca.query.filter_by(licenca=chave).first()
    if licenca:
        return jsonify({'acesso': True})
    return jsonify({'acesso': False})


# Adicionar uma nova chave
@app.route("/chaves", methods=['POST'])
@token_obrigatorio
def adicionar_chave_de_acesso():
    dados = request.get_json()

    nova_licenca = Licenca(licenca=dados['licenca'])
    db.session.add(nova_licenca)
    db.session.commit()

    return jsonify({'mensagem': 'Nova licença registrada com sucesso!'})

# Excluir uma chave existente


@app.route('/chaves/<string:chave>', methods=['DELETE'])
@token_obrigatorio
def excluir_licenca(chave):
    try:
        licenca = Licenca.query.filter_by(licenca=chave).first()
        if licenca:
            db.session.delete(licenca)
            db.session.commit()
        return jsonify({'message': 'Chave excluída com sucesso'})

    except Exception as erro:
        print(erro)
        return jsonify(f'Não foi possível excluir a chave {chave}')


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    usuario = Usuario.query.filter_by(nome=auth.username).first()
    if not usuario:
        return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor': usuario.id_autor, 'exp': datetime.utcnow(
        ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Login inválido', 401, {'WWW-Authenticate': 'Basic realm="Login obrigatório"'})


app.run(port=5000, host='0.0.0.0', debug=False)
