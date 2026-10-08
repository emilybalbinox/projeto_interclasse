from datetime import date

from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import aliased
from sqlalchemy.sql.elements import or_

from database import Partida, db_session, Time


def select_todas():
    partidas_sql = (
        select(Partida, Time)
        .join(Time, or_(Partida.time_casa_id == Time.id, Partida.time_visitante_id == Time.id))

    )
    TimeCasa= aliased(Time)
    TimeVisitante = aliased

    partidas_sql = (
        select(Partida, TimeCasa, TimeVisitante)
        .join(TimeCasa, Partida.Time_Casa_id == TimeCasa.id)
        .join(TimeVisitante, Partida.time_visitante_id == TimeVisitante.id)

    )

    partidas_casa= db_session.execute(partidas_sql).all()
    return partidas_casa

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total

print(select_quantidade_total())

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

