"""Testes complementares do login (issue #9).

Cobrem login válido e inválido, validação de entrada e a garantia de que
nenhuma senha aparece em texto puro (código, usuarios.json, respostas, logs).

Usam um arquivo de usuários temporário, criado com senhas conhecidas só aqui
dentro, então não dependem das senhas do data/usuarios.json do repositório.

Rodar a partir de src/backend: python -m pytest
(também funcionam com: python -m unittest discover -s tests -t .)
"""

import io
import json
import logging
import re
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from app import create_app
from auth.security import gerar_hash_senha, verificar_senha

PASTA_BACKEND = Path(__file__).resolve().parent.parent
USUARIOS_REPOSITORIO = PASTA_BACKEND / "data" / "usuarios.json"

SENHA_PUBLICADOR = "Senha-Publicador-123"
SENHA_RECEPTOR = "Senha-Receptor-456"
MENSAGEM_GENERICA = "E-mail ou senha inválidos."


class _CapturaLogs(logging.Handler):
    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.mensagens = []

    def emit(self, record):
        self.mensagens.append(record.getMessage())


class BaseLogin(unittest.TestCase):
    def setUp(self):
        self._pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self._pasta.cleanup)
        self.arquivo = Path(self._pasta.name) / "usuarios.json"
        self.arquivo.write_text(
            json.dumps(
                [
                    {
                        "nome": "Pessoa Publicadora",
                        "email": "publicador@exemplo.com",
                        "perfil": "publicador",
                        "senha_hash": gerar_hash_senha(SENHA_PUBLICADOR),
                    },
                    {
                        "nome": "Pessoa Receptora",
                        "email": "receptor@exemplo.com",
                        "perfil": "receptor",
                        "senha_hash": gerar_hash_senha(SENHA_RECEPTOR),
                    },
                ]
            ),
            encoding="utf-8",
        )
        self.app = create_app({"USUARIOS_ARQUIVO": self.arquivo})
        self.client = self.app.test_client()

    def login(self, email="publicador@exemplo.com", senha=SENHA_PUBLICADOR, perfil="publicador", **extra):
        corpo = {"email": email, "senha": senha, "perfil": perfil}
        corpo.update(extra)
        return self.client.post("/auth/login", json=corpo)


class TestLoginValido(BaseLogin):
    def test_publicador_entra_com_perfil_correto(self):
        resposta = self.login()
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.get_json(),
            {
                "sucesso": True,
                "usuario": {
                    "nome": "Pessoa Publicadora",
                    "email": "publicador@exemplo.com",
                    "perfil": "publicador",
                },
            },
        )

    def test_receptor_entra_com_perfil_correto(self):
        resposta = self.login("receptor@exemplo.com", SENHA_RECEPTOR, "receptor")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["usuario"]["perfil"], "receptor")

    def test_email_ignora_maiusculas_e_espacos_nas_pontas(self):
        resposta = self.login("  PUBLICADOR@Exemplo.COM  ")
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.get_json()["usuario"]["email"], "publicador@exemplo.com")

    def test_resposta_de_sucesso_nao_expoe_hash_nem_senha(self):
        resposta = self.login()
        usuario = resposta.get_json()["usuario"]
        self.assertEqual(set(usuario), {"nome", "email", "perfil"})
        texto = resposta.get_data(as_text=True)
        self.assertNotIn("senha_hash", texto)
        self.assertNotIn("scrypt:", texto)
        self.assertNotIn(SENHA_PUBLICADOR, texto)

    def test_senha_com_acentos_e_simbolos(self):
        senha = "sênha-çãO-✓-#42"
        dados = json.loads(self.arquivo.read_text(encoding="utf-8"))
        dados[0]["senha_hash"] = gerar_hash_senha(senha)
        self.arquivo.write_text(json.dumps(dados), encoding="utf-8")
        self.assertEqual(self.login(senha=senha).status_code, 200)

    def test_senha_com_espacos_nas_pontas_e_considerada_como_digitada(self):
        # A senha não é "aparada": com espaço a mais, não confere.
        self.assertEqual(self.login(senha=f" {SENHA_PUBLICADOR}").status_code, 401)


class TestLoginInvalido(BaseLogin):
    def test_senha_errada(self):
        resposta = self.login(senha="senha-errada")
        self.assertEqual(resposta.status_code, 401)
        self.assertEqual(resposta.get_json(), {"sucesso": False, "mensagem": MENSAGEM_GENERICA})

    def test_senha_diferencia_maiusculas(self):
        self.assertEqual(self.login(senha=SENHA_PUBLICADOR.upper()).status_code, 401)

    def test_email_inexistente(self):
        resposta = self.login("ninguem@exemplo.com")
        self.assertEqual(resposta.status_code, 401)
        self.assertEqual(resposta.get_json(), {"sucesso": False, "mensagem": MENSAGEM_GENERICA})

    def test_perfil_diferente_do_cadastrado_mesmo_com_senha_certa(self):
        resposta = self.login(perfil="receptor")
        self.assertEqual(resposta.status_code, 401)
        self.assertEqual(resposta.get_json(), {"sucesso": False, "mensagem": MENSAGEM_GENERICA})

    def test_senha_de_outro_usuario_nao_serve(self):
        self.assertEqual(self.login(senha=SENHA_RECEPTOR).status_code, 401)

    def test_os_tres_motivos_de_401_devolvem_exatamente_a_mesma_resposta(self):
        respostas = [
            self.login(senha="errada"),
            self.login("ninguem@exemplo.com"),
            self.login(perfil="receptor"),
        ]
        self.assertEqual({r.status_code for r in respostas}, {401})
        self.assertEqual(len({r.get_data() for r in respostas}), 1)

    def test_email_inexistente_confere_senha_contra_hash_ficticio(self):
        with mock.patch("auth.service.simular_verificacao") as simular:
            self.login("ninguem@exemplo.com", senha="qualquer")
        simular.assert_called_once_with("qualquer")

    def test_email_existente_nao_usa_o_hash_ficticio(self):
        with mock.patch("auth.service.simular_verificacao") as simular:
            self.login(senha="errada")
        simular.assert_not_called()


class TestValidacaoDeEntrada(BaseLogin):
    def assertErro400(self, resposta, mensagem):
        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.get_json(), {"sucesso": False, "mensagem": mensagem})

    def test_campos_vazios_ou_ausentes(self):
        for email, senha in [("", SENHA_PUBLICADOR), ("publicador@exemplo.com", ""), ("", ""), ("   ", "   ")]:
            with self.subTest(email=email, senha=senha):
                self.assertErro400(self.login(email, senha), "Preencha e-mail e senha.")
        resposta = self.client.post("/auth/login", json={"perfil": "publicador"})
        self.assertErro400(resposta, "Preencha e-mail e senha.")

    def test_senha_so_com_espacos(self):
        self.assertErro400(self.login(senha="     "), "Preencha e-mail e senha.")

    def test_email_mal_formatado(self):
        for email in ["maria.com", "maria@", "@exemplo.com", "maria@exemplo", "ma ria@exemplo.com", "a@@b.com"]:
            with self.subTest(email=email):
                self.assertErro400(self.login(email), "E-mail inválido.")

    def test_perfil_ausente_ou_invalido(self):
        mensagem = "Perfil inválido. Use 'publicador' ou 'receptor'."
        for perfil in [None, "", "admin", "PUBLICADOR", " publicador", 1, ["publicador"], {"a": 1}]:
            with self.subTest(perfil=perfil):
                self.assertErro400(self.login(perfil=perfil), mensagem)
        resposta = self.client.post(
            "/auth/login", json={"email": "publicador@exemplo.com", "senha": SENHA_PUBLICADOR}
        )
        self.assertErro400(resposta, mensagem)

    def test_tipos_errados_nos_campos(self):
        for email, senha in [(123, SENHA_PUBLICADOR), (None, SENHA_PUBLICADOR), ("publicador@exemplo.com", 123),
                             ("publicador@exemplo.com", None), (["a@b.com"], SENHA_PUBLICADOR)]:
            with self.subTest(email=email, senha=senha):
                self.assertErro400(self.login(email, senha), "Preencha e-mail e senha.")

    def test_corpo_que_nao_e_json(self):
        mensagem = "Envie e-mail, senha e perfil em JSON."
        casos = [
            self.client.post("/auth/login", data="email=a@b.com&senha=x", content_type="application/x-www-form-urlencoded"),
            self.client.post("/auth/login", data="texto qualquer", content_type="text/plain"),
            self.client.post("/auth/login", data="{quebrado", content_type="application/json"),
            self.client.post("/auth/login", data="", content_type="application/json"),
            self.client.post("/auth/login"),
        ]
        for resposta in casos:
            self.assertErro400(resposta, mensagem)

    def test_json_que_nao_e_objeto(self):
        mensagem = "Envie e-mail, senha e perfil em JSON."
        for corpo in (["a", "b"], "texto", 42, None):
            with self.subTest(corpo=corpo):
                self.assertErro400(self.client.post("/auth/login", json=corpo), mensagem)

    def test_campos_extras_sao_ignorados(self):
        self.assertEqual(self.login(admin=True, perfil_real="receptor").status_code, 200)

    def test_corpo_acima_de_16kb_e_recusado(self):
        grande = {"email": "publicador@exemplo.com", "senha": "x" * (17 * 1024), "perfil": "publicador"}
        self.assertEqual(self.client.post("/auth/login", json=grande).status_code, 413)

    def test_outros_metodos_nao_sao_aceitos(self):
        for metodo in ("get", "put", "delete", "patch"):
            with self.subTest(metodo=metodo):
                self.assertEqual(getattr(self.client, metodo)("/auth/login").status_code, 405)


class TestSenhaNuncaEmTextoPuro(BaseLogin):
    def test_hashes_sao_diferentes_para_a_mesma_senha_e_verificaveis(self):
        h1, h2 = gerar_hash_senha("mesma-senha"), gerar_hash_senha("mesma-senha")
        self.assertNotEqual(h1, h2)  # salt por senha
        for h in (h1, h2):
            self.assertTrue(h.startswith("scrypt:"))
            self.assertNotIn("mesma-senha", h)
            self.assertTrue(verificar_senha(h, "mesma-senha"))
            self.assertFalse(verificar_senha(h, "outra-senha"))

    def test_usuarios_json_do_repositorio_so_tem_hash_scrypt(self):
        usuarios = json.loads(USUARIOS_REPOSITORIO.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(usuarios), 1)
        formato = re.compile(r"^scrypt:\d+:\d+:\d+\$[^$]+\$[0-9a-f]+$")
        for usuario in usuarios:
            self.assertEqual(set(usuario), {"nome", "email", "perfil", "senha_hash"})
            self.assertRegex(usuario["senha_hash"], formato)
        self.assertEqual(len({u["senha_hash"] for u in usuarios}), len(usuarios))

    def test_codigo_nao_tem_senha_literal(self):
        # Procura atribuições como senha = "abc123" ou password: "abc" fora dos testes.
        padrao = re.compile(r"""(senha|password|passwd|secret)\w*\s*[:=]\s*["'][^"']+["']""", re.IGNORECASE)
        achados = []
        for arquivo in PASTA_BACKEND.rglob("*.py"):
            if "tests" in arquivo.parts or ".venv" in arquivo.parts:
                continue
            for numero, linha in enumerate(arquivo.read_text(encoding="utf-8").splitlines(), 1):
                if padrao.search(linha) and not linha.lstrip().startswith("#"):
                    achados.append(f"{arquivo.relative_to(PASTA_BACKEND)}:{numero}: {linha.strip()}")
        self.assertEqual(achados, [])

    def test_senha_nao_aparece_em_respostas_nem_em_logs_nem_na_saida(self):
        captura = _CapturaLogs()
        raiz = logging.getLogger()
        nivel_anterior = raiz.level
        raiz.addHandler(captura)
        raiz.setLevel(logging.DEBUG)
        self.app.logger.addHandler(captura)
        saida, erro = io.StringIO(), io.StringIO()
        senha_secreta = "SenhaMuitoSecreta-XYZ-987"
        try:
            with redirect_stdout(saida), redirect_stderr(erro):
                respostas = [
                    self.login(senha=senha_secreta),
                    self.login("ninguem@exemplo.com", senha_secreta),
                    self.login(senha=SENHA_PUBLICADOR),
                    self.login(email="x", senha=senha_secreta),
                ]
        finally:
            raiz.removeHandler(captura)
            raiz.setLevel(nivel_anterior)
            self.app.logger.removeHandler(captura)
        for resposta in respostas:
            texto = resposta.get_data(as_text=True)
            self.assertNotIn(senha_secreta, texto)
            self.assertNotIn(SENHA_PUBLICADOR, texto)
        tudo = "\n".join(captura.mensagens) + saida.getvalue() + erro.getvalue()
        self.assertNotIn(senha_secreta, tudo)
        self.assertNotIn(SENHA_PUBLICADOR, tudo)

    def test_falha_interna_nao_vaza_a_senha(self):
        # Hoje a falha vira 500 (ver "Limitações conhecidas" no login.md).
        self.arquivo.unlink()
        app = create_app({"USUARIOS_ARQUIVO": self.arquivo, "TESTING": False})
        app.logger.disabled = True  # o traceback esperado só polui a saída dos testes
        resposta = app.test_client().post(
            "/auth/login",
            json={"email": "publicador@exemplo.com", "senha": SENHA_PUBLICADOR, "perfil": "publicador"},
        )
        self.assertEqual(resposta.status_code, 500)
        self.assertNotIn(SENHA_PUBLICADOR, resposta.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
