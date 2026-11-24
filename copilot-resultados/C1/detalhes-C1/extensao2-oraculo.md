# Extensão coverage-informed E2 — formato texto

E02 do executor E1 impôs que o relatório contivesse literalmente a palavra
“tabela”, embora a documentação exija o conteúdo e não essa palavra. Essa
asserção adicional é `INCORRETO/SEM SUPORTE` e sua falha não é divergência do
SUT. O resultado bruto permanece preservado.

E20 reavalia separadamente o conteúdo documental, sem exigir o título
“tabela”. Fonte, O que a ferramenta faz: “Tabela verdade, pares de
independência, suíte de testes e o par que demonstra cada condição”; Como
funciona: “para as entradas distintas da expressão, são consideradas as 2ⁿ
combinações e calculado o resultado da guarda em cada uma”; Uso: “`text`
(padrão)”. Entrada `analyze "A and B"`; expectativas conformes: código 0,
quatro vetores distintos com resultado `A∧B`, pares para A e B cujos dois
vetores mudam a condição e o resultado, e os vetores desses pares presentes
na suíte. As fórmulas e testemunhas são as de B03, já congeladas.

O formato de linhas é adaptador de leitura, não um requisito normativo; se a
leitura falhar, isso não prova ausência de um componente em outro formato.
O alvo de cobertura é `TextReport`, observado sem cobertura no baseline. A
suíte E20 e esta explicação serão congeladas antes de executar a extensão E2.
