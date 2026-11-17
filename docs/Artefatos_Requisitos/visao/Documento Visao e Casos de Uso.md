# Documento Visão e Casos de Uso (critérios Larman)

## 1. Documento Visão (Larman, cap. 7)

- **O problema:** a falta de registros centralizados, a quebra de acompanhamento contínuo e a ausência de canais seguros para feedback anônimo.
- **Afeta:** Líderes (dificuldade de embasar promoções e retenção) e Colaboradores (falta de clareza nas metas de desenvolvimento).
- **O impacto é:** baixo engajamento, falhas de comunicação e desenvolvimento estagnado.
- **Uma boa solução seria:** o FeedBerry, um Sistema de Gestão de Competências web, que centraliza o histórico de avaliações, integra pontos de melhoria a planos de desenvolvimento contínuos, e assegura anonimato total sob conformidade com a LGPD.

## 2. Especificação de casos de uso essenciais (Larman, cap. 6)

### UC03: Registrar e Enviar Feedback (Responsável: Fernando)

- **Ator principal:** Líder.
- **Pré-condições:** usuário autenticado como Líder.
- **Garantia de sucesso:** feedback salvo no banco de dados e colaborador notificado.
- **Fluxo principal:**
  1. O líder seleciona "Enviar Feedback" na Home.
  2. Seleciona o colaborador da equipe.
  3. Preenche as categorias (construtivo/elogio) e descreve os pontos de melhoria.
  4. Confirma o envio.
  5. O sistema grava o registro com a data e atualiza o dashboard do colaborador.
- **Alternativa (3a):** campos obrigatórios vazios; o sistema bloqueia o envio e sinaliza em vermelho.

### UC10: Consultar Histórico de Feedbacks (Responsável: Paula)

- **Ator principal:** Colaborador.
- **Garantia de sucesso:** exibição da timeline cronológica contendo evoluções e metas.
- **Fluxo principal:**
  1. O colaborador acessa a visão "Meu Histórico".
  2. O sistema recupera a lista de avaliações do banco de dados (SQLite/PostgreSQL).
  3. O sistema renderiza os "cards" de feedback ordenados do mais recente ao mais antigo.
  4. O colaborador utiliza filtros para isolar "Elogios" ou "Pontos de Melhoria".

### UC05: Definir Metas de Desenvolvimento (Responsável: Enzo)

- **Ator principal:** Líder.
- **Garantia de sucesso:** plano de melhoria registrado e vinculado ao colaborador.
- **Fluxo principal:**
  1. No perfil do colaborador, o líder clica em "Nova Meta".
  2. Define título, prazo limite e indicadores.
  3. O sistema salva a meta e envia notificação (lembrete) automática aos dois envolvidos.

### UC13: Enviar Feedback Anônimo ao Líder (Responsável: Aimê)

- **Ator principal:** Colaborador.
- **Garantia de sucesso:** mensagem enviada à liderança sem gravação da chave de relacionamento do autor.
- **Fluxo principal:**
  1. Colaborador inicia um envio de feedback ao Líder.
  2. Redige a mensagem e assinala a checkbox "Enviar de forma anônima".
  3. O sistema substitui o ID do usuário por um hash cego ou registro "Anônimo" antes do commit no banco de dados.
  4. O líder recebe a notificação da avaliação construtiva sem identificar o remetente.

### UC07: Gerar Painel de Evolução da Equipe (Responsável: Matheus)

- **Ator principal:** Líder.
- **Garantia de sucesso:** visualização de indicadores consolidados de desempenho.
- **Fluxo principal:**
  1. Líder clica na aba "Visão Geral da Equipe".
  2. O sistema calcula a taxa de alcance de metas e os volumes de feedback das últimas semanas.
  3. Exibe os dados consolidados em formato visual para auxiliar a tomada de decisões de promoção.
