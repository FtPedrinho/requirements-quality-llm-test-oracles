# Repetição técnica F03

O baseline e seu resultado permanecem imutáveis. O processo Java F03 produziu arquivo de relatório e dados de cobertura, mas o harness tentou decodificar stdout como UTF-8. O runtime informa `file.encoding=UTF-8` e `stdout.encoding=Cp1252`; a mensagem de confirmação contém byte não UTF-8. A execução baseline permanece classificada como erro técnico.

A repetição usa a mesma entrada, a mesma expectativa F03 e a mesma função de asserção já congelada. Apenas a decodificação do stdout/stderr é ajustada para Cp1252 e os caminhos de evidência/cobertura são novos. Nenhuma expectativa, fórmula ou regra de comportamento foi acrescentada. A repetição é uma rodada técnica separada, não uma substituição do baseline.
