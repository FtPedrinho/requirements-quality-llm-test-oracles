# Metodologia da pesquisa com LLMs

Esta pesquisa investiga a geração de oráculos e testes para a ferramenta Java
MC/DC a partir de documentações com diferentes níveis de clareza e
consistência. A documentação da condição é a única autoridade para os
resultados esperados; o sistema é o objeto avaliado, não o gabarito.

## Condições independentes

Cada experimento C0–C4 segue o mesmo procedimento e pode ser realizado
independentemente dos demais. A única variável documental é a fonte da
condição, identificada no [protocolo](protocolo/metodologia.md). C0 usa a
documentação original; C1–C4 representam combinações pretendidas de clareza
e consistência. Não se presume que esses níveis tenham sido atingidos.

## Procedimento

1. Ler integralmente somente a documentação técnica e de requisitos de Cx.
2. Derivar o oráculo exclusivamente do texto, tratando-o como verdade absoluta
   para o experimento; registrar trechos, regras e indeterminações.
3. Usar obrigatoriamente Z3 independente para formalizar e verificar as
   restrições do oráculo. Congelar o oráculo antes de consultar o sistema.
4. Criar uma suíte nova contra o MC/DC real, buscando a maior Branch Coverage
   possível sem inventar expectativas nem modificar o sistema ou a
   documentação.
5. Executar os testes e registrar Branch Coverage e quantidades de testes
   que passaram, falharam e ficaram indeterminados.

Falhas com expectativas documentais determinadas são preservadas;
ambiguidades, omissões e conflitos sem resultado único são indeterminados.
O Z3 não prova que a tradução do texto para fórmulas seja fiel.

## Documentos metodológicos

- [Protocolo comum e fontes C0–C4](protocolo/metodologia.md).
- [Prompt de geração](prompts/geracao-de-oraculos-v3.md).
- [Avaliação qualitativa](avaliacao-qualitativa/README.md).
- [Modelo de relatório](protocolo/modelo-relatorio.md).
- [Documentação original](documentacao-original/README.md).

Esta pasta contém metodologia e documentos de entrada, não resultados de
execuções. Suítes, oráculos concretos, logs e relatórios de cada coleta devem
ser guardados fora dela, sem depender de coletas de outras condições.
