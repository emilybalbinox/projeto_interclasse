from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import Time,db_session

def select_todos_times():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return times

def salvar_times(nome, responsavel, turma):
    try:
        time = Time(nome=nome, responsavel=responsavel, turma=turma)
        db_session.add(time)
        db_session.commit()
        flash('Time cadastrado com sucesso', 'success')
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f'Erro: {e}')

