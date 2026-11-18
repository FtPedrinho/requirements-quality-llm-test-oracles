# Metadata da Experimentação 0

| Campo | Valor |
|---|---|
| Data | 18/11/2026 |
| Commit | `b3e9cd01ad6082882bc21ce1ae91e7fc51ca5c52` |
| Sistema | Windows |
| Python | 3.13.5 |
| Z3 Python | 5.4.1.0 |
| Modelo efetivamente utilizado | GitHub Copilot, modo agente |
| Versão do modelo | Não disponível no ambiente |
| Modo de execução | GitHub Copilot SDK in VS Code |
| Arquivos normativos consultados | Arquivos `.mcdc` e JSON NAT2TEST |
| Arquivos excluídos nesta etapa | Código-fonte, testes JUnit, CSV de testes, relatórios e implementação |

Z3 não estava instalado no início da tarefa nem como pacote Python nem como executável no `PATH`. O pacote `z3-solver` foi instalado via `pip` em ambiente de usuário para permitir a execução dos scripts.
