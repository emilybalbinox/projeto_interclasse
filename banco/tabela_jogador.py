from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import Jogador, db_session


def select_todos_jogadores():
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores


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