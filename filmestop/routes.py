from flask import jsonify, request, render_template, url_for, redirect, abort, session
from filmestop import app, db
from filmestop.models import Filme, Usuario, Aluguel
from datetime import datetime

@app.route('/')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtém o nome do usuário do formulário
        usuario_nome = request.form['usuario_nome']
        # Busca o usuário no banco de dados
        usuario = Usuario.query.filter_by(nome=usuario_nome).first()
        if not usuario:
            # Cria um novo usuário se não existir
            usuario = Usuario(nome=usuario_nome)
            db.session.add(usuario)
            db.session.commit()
        # Armazena o ID do usuário na sessão
        session['usuario_id'] = usuario.id
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/listar-filmes')
def listar_filmes():
    return render_template('listar_filme.html')

@app.route('/adicionar-filme', methods=['GET', 'POST'])
def adicionar_filme():
    if request.method == 'POST':
        # Obtém os dados do filme do formulário
        nome = request.form['nome']
        ano = request.form['ano']
        genero = request.form['genero']
        sinopse = request.form['sinopse']
        diretor = request.form['diretor']

        # Cria uma nova instância de Filme
        novo_filme = Filme(nome=nome, ano=ano, genero=genero, sinopse=sinopse, diretor=diretor)
        try:
            db.session.add(novo_filme)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)})

        return redirect(url_for('listar_filmes'))

    return render_template('adicionar_filme.html')

@app.route('/filmes/<string:genero>', methods=['GET'])
def listar_filmes_por_genero(genero):
    # Busca filmes no banco de dados
    filmes = Filme.query.filter_by(genero=genero).all()
    # Cria uma lista de dicionários com informações dos filmes
    filmes_lista = [{
        'id': filme.id,
        'nome': filme.nome,
        'ano': filme.ano,
        'diretor': filme.diretor
    } for filme in filmes]
    return jsonify(filmes_lista)

@app.route('/filme/<string:nome>', methods=['GET'])
def info_filme(nome):
    # Busca o filme no banco de dados
    filme = Filme.query.filter_by(nome=nome).first()
    if filme:
        return jsonify({
            'nome': filme.nome,
            'ano': filme.ano,
            'genero': filme.genero,
            'sinopse': filme.sinopse,
            'diretor': filme.diretor
        })
    else:
        return jsonify({'Filme não encontrado'})

@app.route('/alugar', methods=['POST'])
def alugar_filme():
    if 'usuario_id' not in session:
        return jsonify({"error": "Usuário não está logado"})

    # Obtém os dados do pedido de aluguel
    data = request.get_json()
    usuario_id = session['usuario_id']
    filme_id = data['filme_id']
    
    # Verifica se o filme já foi alugado por este usuário
    aluguel_existente = Aluguel.query.filter_by(usuario_id=usuario_id, filme_id=filme_id).first()
    if aluguel_existente:
        return jsonify({"Filme já alugado por este usuário"})

    # Cria uma nova instância de aluguel
    novo_aluguel = Aluguel(usuario_id=usuario_id, filme_id=filme_id, data_aluguel=datetime.utcnow())
    try:
        db.session.add(novo_aluguel)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"Filme alugado com sucesso!"})

@app.route('/usuario/<int:usuario_id>/alugueis', methods=['GET'])
def listar_alugueis(usuario_id):
    # Busca todos os aluguéis do usuário no banco de dados
    alugueis = Aluguel.query.filter_by(usuario_id=usuario_id).all()
    alugueis_lista = []
    
    for aluguel in alugueis:
        # Obtém as informações do filme associado ao aluguel
        filme = Filme.query.get(aluguel.filme_id)
        alugueis_lista.append({
            "filme": filme.nome,
            "data_locacao": aluguel.data_locacao,
            "nota": aluguel.nota if aluguel.nota is not None else "Sem avaliação"
        })
    
    return jsonify(alugueis_lista)

@app.route('/avaliar', methods=['POST'])
def avaliar_filme():
    if 'usuario_id' not in session:
        return jsonify({"Usuário não está logado"})

    # Obtém os dados da avaliação
    data = request.get_json()
    filme_id = data['filme_id']
    nota_valor = data['nota']
    usuario_id = session['usuario_id']
    
    # Verifica se o usuário alugou o filme
    aluguel = Aluguel.query.filter_by(usuario_id=usuario_id, filme_id=filme_id).first()
    
    if not aluguel:
        return jsonify({"Usuário não alugou este filme, portanto não pode avaliar"})

    if aluguel.nota is not None:
        return jsonify({"Este filme já foi avaliado por este usuário"})

    # Atualiza a nota do filme
    aluguel.nota = nota_valor
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})

    return jsonify({"Nota atribuída com sucesso!"})

@app.route('/meus-alugueis', methods=['GET'])
def meus_alugueis():
    if 'usuario_id' not in session:
        # Redireciona para a página de login se o usuário não estiver autenticado
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    # Busca todos os aluguéis do usuário no banco de dados
    alugueis = Aluguel.query.filter_by(usuario_id=usuario_id).all()
    filmes_alugados = []

    for aluguel in alugueis:
        # Obtém as informações do filme associado ao aluguel
        filme = Filme.query.get(aluguel.filme_id)
        filmes_alugados.append({
            "id": filme.id,
            "nome": filme.nome,
            "data_aluguel": aluguel.data_aluguel,
            "nota": aluguel.nota
        })

    # Renderiza a página com os filmes alugados
    return render_template('meus_alugueis.html', filmes=filmes_alugados)
