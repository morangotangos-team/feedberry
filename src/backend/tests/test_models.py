"""Testes dos modelos e das regras de negócio garantidas pelo banco (issue #13).

Cada regra é testada de dois jeitos quando faz sentido:
- pelo ORM, como o código da aplicação vai usar;
- por SQL direto, para mostrar que a regra vale mesmo para quem acessa o
  banco sem passar pela aplicação.
"""

from datetime import date, datetime, timedelta, timezone

import pytest
from sqlalchemy import inspect, select, text
from sqlalchemy.exc import IntegrityError

from models import (
    Equipe,
    Feedback,
    Lembrete,
    MetaDesenvolvimento,
    Papel,
    PontoMelhoria,
    StatusLembrete,
    StatusMeta,
    StatusPontoMelhoria,
    TipoFeedback,
    UsuarioNaoPodeSerApagado,
    agora_utc,
)


@pytest.fixture
def lider(criar_usuario):
    return criar_usuario("lider@exemplo.com", Papel.LIDER, "Líder")


@pytest.fixture
def colaborador(criar_usuario):
    return criar_usuario("colaborador@exemplo.com", Papel.COLABORADOR, "Colaborador")


@pytest.fixture
def feedback(sessao, lider, colaborador):
    feedback = Feedback(
        tipo=TipoFeedback.LIDER_PARA_COLABORADOR,
        autor=lider,
        destinatario=colaborador,
        conteudo="Boa apresentação; dá para melhorar a gestão do tempo.",
    )
    sessao.add(feedback)
    sessao.commit()
    return feedback


def gravar_e_esperar_erro(sessao, *objetos):
    sessao.add_all(objetos)
    with pytest.raises(IntegrityError):
        sessao.commit()
    sessao.rollback()


def sql_esperando_erro(sessao, sql, **parametros):
    with pytest.raises(IntegrityError):
        sessao.execute(text(sql), parametros)
        sessao.commit()
    sessao.rollback()


# ---------- Usuário ----------

def test_email_e_salvo_em_minusculas_e_sem_espacos(criar_usuario):
    usuario = criar_usuario("  Maria.Silva@Exemplo.COM ")

    assert usuario.email == "maria.silva@exemplo.com"


def test_email_duplicado_e_rejeitado(criar_usuario, sessao, colaborador):
    with pytest.raises(IntegrityError):
        criar_usuario("COLABORADOR@exemplo.com")
    sessao.rollback()


def test_email_com_maiusculas_por_sql_direto_e_rejeitado(sessao):
    sql_esperando_erro(
        sessao,
        "INSERT INTO usuario (nome, email, senha_hash, papel, ativo, tentativas_login_falhas, criado_em)"
        " VALUES ('X', 'Maiuscula@exemplo.com', 'scrypt:x', 'COLABORADOR', 1, 0, '2026-01-01')",
    )


def test_papel_fora_do_enum_e_rejeitado_pelo_banco(sessao):
    sql_esperando_erro(
        sessao,
        "INSERT INTO usuario (nome, email, senha_hash, papel, ativo, tentativas_login_falhas, criado_em)"
        " VALUES ('X', 'x@exemplo.com', 'scrypt:x', 'ADMIN', 1, 0, '2026-01-01')",
    )


def test_valores_padrao_do_usuario(colaborador):
    assert colaborador.ativo is True
    assert colaborador.tentativas_login_falhas == 0
    assert colaborador.criado_em.tzinfo == timezone.utc


def test_usuario_nao_pode_ser_apagado_so_desativado(sessao, colaborador):
    sessao.delete(colaborador)
    with pytest.raises(UsuarioNaoPodeSerApagado):
        sessao.commit()
    sessao.rollback()

    colaborador.desativar()
    sessao.commit()
    assert colaborador.ativo is False


def test_banco_nao_apaga_usuario_que_tem_feedback(sessao, feedback, colaborador):
    # Mesmo por SQL direto, sem passar pela aplicação (ON DELETE RESTRICT).
    sql_esperando_erro(sessao, "DELETE FROM usuario WHERE id = :id", id=colaborador.id)
    assert sessao.get(Feedback, feedback.id) is not None


# ---------- Equipe ----------

def test_equipe_com_lider_e_membros(sessao, lider, colaborador):
    equipe = Equipe(nome="Produto", lider=lider, membros=[lider, colaborador])
    sessao.add(equipe)
    sessao.commit()

    assert lider.equipe_liderada == equipe
    assert colaborador.equipe == equipe
    assert set(equipe.membros) == {lider, colaborador}


def test_pessoa_lidera_no_maximo_uma_equipe(sessao, lider):
    gravar_e_esperar_erro(sessao, Equipe(nome="A", lider=lider), Equipe(nome="B", lider=lider))


# ---------- Feedback ----------

def test_feedback_valido_com_pontos_de_melhoria(sessao, feedback):
    feedback.pontos_melhoria.append(PontoMelhoria(descricao="Chegar no horário das reuniões"))
    sessao.commit()

    ponto = feedback.pontos_melhoria[0]
    assert ponto.status is StatusPontoMelhoria.ABERTO
    assert ponto.atualizado_em.tzinfo == timezone.utc


def test_feedback_para_si_mesmo_e_rejeitado(sessao, lider):
    gravar_e_esperar_erro(
        sessao,
        Feedback(
            tipo=TipoFeedback.LIDER_PARA_COLABORADOR,
            autor=lider,
            destinatario=lider,
            conteudo="Mandei bem.",
        ),
    )


def test_feedback_anonimo_com_autor_e_rejeitado(sessao, lider, colaborador):
    gravar_e_esperar_erro(
        sessao,
        Feedback(
            tipo=TipoFeedback.COLABORADOR_PARA_LIDER,
            autor=colaborador,
            destinatario=lider,
            conteudo="Reuniões longas demais.",
            anonimo=True,
        ),
    )


def test_feedback_anonimo_do_lider_para_o_colaborador_e_rejeitado(sessao, colaborador):
    gravar_e_esperar_erro(
        sessao,
        Feedback(
            tipo=TipoFeedback.LIDER_PARA_COLABORADOR,
            autor=None,
            destinatario=colaborador,
            conteudo="Feedback sem assinatura.",
            anonimo=True,
        ),
    )


def test_feedback_identificado_sem_autor_e_rejeitado(sessao, colaborador):
    gravar_e_esperar_erro(
        sessao,
        Feedback(
            tipo=TipoFeedback.LIDER_PARA_COLABORADOR,
            autor=None,
            destinatario=colaborador,
            conteudo="Quem escreveu?",
            anonimo=False,
        ),
    )


def test_feedback_anonimo_do_colaborador_para_o_lider_e_aceito_sem_autor(sessao, lider):
    feedback = Feedback(
        tipo=TipoFeedback.COLABORADOR_PARA_LIDER,
        destinatario=lider,
        conteudo="Gostaria de mais retorno sobre as entregas.",
        anonimo=True,
    )
    sessao.add(feedback)
    sessao.commit()

    linha = sessao.execute(
        text("SELECT autor_id FROM feedback WHERE id = :id"), {"id": feedback.id}
    ).one()
    assert linha.autor_id is None


def test_feedback_com_conteudo_vazio_e_rejeitado(sessao, lider, colaborador):
    gravar_e_esperar_erro(
        sessao,
        Feedback(
            tipo=TipoFeedback.LIDER_PARA_COLABORADOR,
            autor=lider,
            destinatario=colaborador,
            conteudo="   ",
        ),
    )


def test_feedback_para_usuario_inexistente_e_rejeitado(sessao, lider):
    # Confere que o SQLite está validando chaves estrangeiras (PRAGMA foreign_keys).
    gravar_e_esperar_erro(
        sessao,
        Feedback(
            tipo=TipoFeedback.LIDER_PARA_COLABORADOR,
            autor_id=lider.id,
            destinatario_id=9999,
            conteudo="Para ninguém.",
        ),
    )


def test_indice_do_historico_existe(sessao):
    indices = inspect(sessao.get_bind()).get_indexes("feedback")

    assert {"name": "ix_feedback_destinatario_id_criado_em", "column_names": ["destinatario_id", "criado_em"]} in [
        {"name": i["name"], "column_names": i["column_names"]} for i in indices
    ]


# ---------- Meta de desenvolvimento ----------

def test_meta_nasce_de_um_ponto_de_melhoria(sessao, feedback, lider, colaborador):
    ponto = PontoMelhoria(feedback=feedback, descricao="Organizar a agenda")
    meta = MetaDesenvolvimento(
        colaborador=colaborador,
        definida_por=lider,
        ponto_melhoria=ponto,
        titulo="Usar bloco de foco diário",
        prazo=date(2026, 12, 31),
    )
    sessao.add(meta)
    sessao.commit()

    assert meta.status is StatusMeta.NAO_INICIADA
    assert ponto.metas == [meta]
    assert colaborador.metas == [meta]


# ---------- Lembrete ----------

def test_lembrete_sem_feedback_e_sem_meta_e_rejeitado(sessao, lider, colaborador):
    gravar_e_esperar_erro(
        sessao,
        Lembrete(
            agendado_por=lider,
            destinatario=colaborador,
            data_agendada=agora_utc() + timedelta(days=7),
            mensagem="Retorno sobre... nada?",
        ),
    )


def test_lembrete_de_retorno_de_um_feedback(sessao, feedback, lider, colaborador):
    lembrete = Lembrete(
        agendado_por=lider,
        destinatario=colaborador,
        feedback=feedback,
        data_agendada=agora_utc() + timedelta(days=7),
    )
    sessao.add(lembrete)
    sessao.commit()

    assert lembrete.status is StatusLembrete.PENDENTE
    assert feedback.lembretes == [lembrete]


def test_lembrete_enviado_sem_data_de_envio_e_rejeitado(sessao, feedback, lider, colaborador):
    gravar_e_esperar_erro(
        sessao,
        Lembrete(
            agendado_por=lider,
            destinatario=colaborador,
            feedback=feedback,
            data_agendada=agora_utc(),
            status=StatusLembrete.ENVIADO,
        ),
    )


# ---------- Datas em UTC ----------

def test_datas_sao_gravadas_e_lidas_em_utc(sessao, feedback, lider, colaborador):
    brasilia = timezone(timedelta(hours=-3))
    lembrete = Lembrete(
        agendado_por=lider,
        destinatario=colaborador,
        feedback=feedback,
        data_agendada=datetime(2026, 12, 1, 9, 0, tzinfo=brasilia),
    )
    sessao.add(lembrete)
    sessao.commit()
    sessao.expire_all()

    lido = sessao.scalar(select(Lembrete).where(Lembrete.id == lembrete.id))
    assert lido.data_agendada == datetime(2026, 12, 1, 12, 0, tzinfo=timezone.utc)
    assert lido.data_agendada.tzinfo == timezone.utc


def test_data_sem_fuso_horario_e_recusada(sessao, feedback, lider, colaborador):
    sessao.add(
        Lembrete(
            agendado_por=lider,
            destinatario=colaborador,
            feedback=feedback,
            data_agendada=datetime(2026, 12, 1, 9, 0),
        )
    )
    with pytest.raises(Exception, match="fuso"):
        sessao.commit()
    sessao.rollback()
