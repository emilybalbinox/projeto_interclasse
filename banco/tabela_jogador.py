from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Jogador, Time, db_session


def select_todos():
    # 1 mostrar select
    # join (tabela que eu quero juntar, condição = chave estrangeira igual chave primaria)
    jogadores_sql = select(Jogador, Time).join(Time, Jogador.time_id == Time.id)
    # executar o select
    # Usa scalars quando tiver somente uma tabela
    jogadores = db_session.execute(jogadores_sql).all()
    print(jogadores)
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

print(select_quantidade_total())


def salvar_jogadores (nome, numero_camisa, posicao, time_id):
    try:
        jogador = Jogador(nome=nome, numero_camisa=numero_camisa , posicao=posicao, time_id=time_id)
        db_session.add(jogador)
        db_session.commit()
        flash('Time cadastrado com sucesso', 'SUCCESS!')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "ERRO!")
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "ERRO!")
        print(f'Erro: {e}')