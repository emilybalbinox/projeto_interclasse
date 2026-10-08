from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time, tabela_partida, tabela_jogador
from database import *
from database import Time, Jogador, db_session, Partida

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    # Buscar todos os times do banco
    partidas = tabela_partida.select_quantidade_total()
    jogadores = tabela_jogador.select_quantidade_total()
    times = tabela_time.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_jogadores=jogadores,
        total_times=times,
        total_partidas=partidas,

    )


@app.route("/jogadores")
def listar_jogadores():
    # Buscar todos os times do banco
    jogadores = tabela_jogador.select_todos()
    print(jogadores)
    return render_template("jogadores.html", jogadores=jogadores)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    # Quando clicar no botao cadastrar
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        if not nome:
            flash ('Digite o nome do jogador', 'error')
            return redirect(url_for('novo_jogador'))
        if not numero_camisa:
            flash ('Digite o numero da camisa do jogador', 'error')
            return redirect(url_for('novo_jogador'))
        if not posicao:
            flash ('Digite a posição do jogador', 'error')
            return redirect(url_for('novo_jogador'))
        if not time_id:
            flash ('Digite seu time', 'error')
            return redirect(url_for('novo_jogador'))

        tabela_jogador.salvar_jogadores(nome=nome, numero_camisa=numero_camisa, posicao=posicao, time_id=time_id)

    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()


    print(jogadores)
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/times",methods=["GET", "POST"])
def listar_times():
    times = tabela_time.select_todos()
    print(times)
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():

    if request.method == "POST":
        #  1- Pegar os valores digitados no form
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        #2- verificar se foi digitado
        if not nome:
            flash ('Digite o seu nome', 'ERRO!!')
            return render_template("times.html")

        if not turma:
            flash('Digite a sua turma', 'ERRO!!')
            return render_template("times.html")

        if not responsavel:
            flash('Digite o responsavel', 'ERRO!!')
            return render_template("times.html")

        #3- Salvar no banco
        tabela_time.salvar_times(nome=nome,turma=turma,responsavel=responsavel)

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todas_partidas()
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("gols_casa") or 0
        gols_visitante = request.form.get("gols_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()

        if not time_casa_id:
            flash('preencha o campo', 'error')
            return render_template("times.html")

        if not time_visitante_id:
            flash('Preencha o nome do responsável', 'error')
            return render_template("times.html")
        if not gols_casa:
            flash('Preencha os gols marcados', 'error')
            return render_template("times.html")
        if not gols_visitante:
            flash('Preencha os ', 'error')
            return render_template("times.html")
        if not data_partida:
            flash('Digite o responsavel', 'error')
            return render_template("times.html")

        tabela_partida.salvar_partidas(time_casa_id=time_casa_id, time_visitante_id=time_visitante_id, gols_casa=gols_casa, gols_visitante=gols_visitante, data_partida=data_partida)

    partidas = tabela_partida.select_todas_partidas()
    times = tabela_time.select_todos()

    return render_template("partidas.html", partidas=partidas, times=times)

if __name__ == "__main__":
    app.run(debug=True)
