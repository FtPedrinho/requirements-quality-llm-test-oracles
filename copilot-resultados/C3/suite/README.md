# Suíte C3

Esta pasta contém cópias byte a byte dos executores, dos oráculos e das entradas congelados. Os originais e as evidências permanecem em [detalhes-C3](../detalhes-C3/). O arquivo [oraculos.json](oraculos.json) contém as tabelas documentais; [oraculos-integracao.json](oraculos-integracao.json), as propriedades de integração.

| Arquivo | Finalidade |
|---|---|
| [executar-suite.py](executar-suite.py) | 14 casos do baseline |
| [repetir-f03.py](repetir-f03.py) | repetição técnica do caso F03 |
| [executar-extensao.py](executar-extensao.py) | 16 casos que reutilizam expectativas congeladas |
| [entradas](entradas/) | arquivo de requisitos e decisão JSON |
| [verificar-integridade.py](verificar-integridade.py) | confere manifestos originais e cópias desta pasta |

Para executar, siga o [passo a passo](../metodologia.md). Os executores exigem classes Java de produção compiladas, Jackson e agente JaCoCo; eles não compilam o SUT automaticamente. Eles se recusam a sobrescrever resultados existentes. A repetição e a extensão não criam expectativas semânticas novas.
