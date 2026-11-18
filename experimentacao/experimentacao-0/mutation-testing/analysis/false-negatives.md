# Falsos negativos

Foram registrados 42 mutantes não equivalentes sobreviventes.

Isso significa que a suíte não encontrou, entre os casos concretos associados, uma diferença observável entre o comportamento original e o mutante.

Causas potenciais:

- casos MC/DC abstratos que não foram concretizados;
- pares que não exercitam exatamente o limite alterado;
- domínios reais ou inteiros não suficientemente cobertos pelos valores concretos;
- mutações em limites que exigem valores adjacentes não presentes na formalização;
- insuficiência de casos associados a determinados oráculos.
