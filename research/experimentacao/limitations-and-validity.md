# Limitações e validade

## Limitações principais

- Não foram realizadas múltiplas execuções independentes por modelo externo nesta etapa.
- Os oráculos foram gerados pelo agente atual a partir do inventário e do gabarito, não por um processo experimental com logs de modelo externo.
- Precision, Recall e F1 não podem ser calculados sem anotação humana contra o gabarito.
- PIT foi executado sobre `mcdc-core`, mas não mede oráculos gerados pelo LLM.
- A suíte real executou 21 casos; não cobre isoladamente todos os 34 comportamentos.
- O PDF contém propostas arquiteturais não totalmente implementadas no código atual.

## Validade interna

Implementação, commit, Java e Z3 foram registrados. A suíte real passou 21/21 em ambos os experimentos.

## Validade externa

Os resultados não podem ser generalizados além da ferramenta MC/DC Java atual.

## Próximas decisões

- definir o modelo LLM e a versão;
- congelar o prompt-base;
- criar múltiplas execuções;
- executar revisão humana;
- anotar TP/FP/FN;
- gerar suítes a partir dos novos oráculos;
- executar suítes contra o SUT real;
- aplicar mutações a módulos Java e medir cada suíte.
