# Lacunas e riscos documentais

Este inventário descreve riscos a observar durante a pesquisa. Não é uma especificação normativa nem um gabarito.

## Fontes

- O README da ferramenta é documentação do usuário, preservada em `docs/README.md`.
- A cópia original de requisitos usada como base está em `experimentacao-pesquisa/documentacao-original/`; C1-C4 estão nas subpastas correspondentes.
- O PDF técnico contém uma proposta arquitetural e funcionalidades que podem não corresponder ao snapshot implementado. Não tratá-lo como contrato funcional sem reconciliação documental prévia.
- VM, TIS e NPP são exemplos de entrada da ferramenta, não sistemas de domínio implementados no repositório.

## Lacunas candidatas a registro

- Mensagens de erro, prioridade de opções e comportamento de combinações inválidas podem não estar inteiramente especificados.
- Limites e caminhos que dependem do Z3 podem ser descritos em locais diferentes e requerer verificação de consistência.
- A documentação pode não definir todos os esquemas de entrada/saída, domínios ou estados.
- Uma expectativa pode divergir da implementação observada; a discrepância deve ser registrada sem usar o código para corrigir o texto.
- C1-C4 têm níveis de tratamento pretendidos; a eficácia da manipulação precisa ser caracterizada com evidência, não presumida.

Registrar cada ocorrência por arquivo, seção, trecho literal, interpretação, alternativas, teste afetado e evidência de execução. Nenhuma lista pré-fabricada de lacunas deve ser confundida com verdade comportamental.
