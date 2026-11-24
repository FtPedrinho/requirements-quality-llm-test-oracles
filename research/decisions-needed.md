# Decisões pendentes antes da nova coleta

As escolhas abaixo não estão especificadas com evidência suficiente e não foram inventadas nesta revisão. Registrar as decisões antes de gerar qualquer resultado:

1. Modelo, versão, parâmetros e número de repetições por condição.
2. Commit do SUT e ambiente exato (SO, arquitetura, Java, Maven, Z3 e dependências).
3. Ferramenta e versão para medir Branch Coverage, fixadas para comparações.
4. Harness para os testes gerados e comando de execução por condição, mantendo a independência das coletas.
5. Procedimento de caracterização de clareza/consistência, incluindo avaliadores e forma de registrar divergências.
6. Revisor independente e procedimento para conferir a correspondência texto–SMT; na ausência, registrar a autorrevisão.

Não são decisões pendentes: C0-C4 seguem o mesmo protocolo de forma independente; a documentação congelada é a referência absoluta para o oráculo; o Z3 independente é obrigatório; as métricas são Branch Coverage e quantidades de testes aprovados, falhos e indeterminados. O escopo de cobertura já inclui todas as classes de produção dos quatro módulos, inclusive classes não carregadas e de mutação, e exclui harness e bibliotecas externas.
