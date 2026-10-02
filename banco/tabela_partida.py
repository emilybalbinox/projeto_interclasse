from datetime import date

from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import Partida, db_session


def select_todas_partidas():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas

def salvar_partidas(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida):
    try:
        partida_nova = Partida(time_casa_id=int(time_casa_id),time_visitante_id=int(time_visitante_id), gols_casa=int(gols_casa),gols_visitante=int(gols_visitante), data_partida=data_partida)
        db_session.add(partida_nova)
        db_session.commit()
        flash('Partida salva com sucesso')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash('Ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash('Ocorreu um erro, tente novamente', 'error')
        print(f"Erro: {e}")

