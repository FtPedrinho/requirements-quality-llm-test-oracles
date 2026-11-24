"""Oraculo da extensao 1 (C2): casos documentados ainda nao testados no baseline. Congelado antes da execucao."""
import json, pathlib
D = "DETERMINADO"
def c(id, titulo, trecho, esperado, nota=""):
    return dict(id=id, grupo="X-extensao1", titulo=titulo, status=D, trecho_literal=trecho, expectativa=esperado, justificativa=nota)
casos = [
 c("C2-020", "REAVALIACAO do C2-020 (defeito da suite no baseline)", '"20 entradas   tabela-verdade cmpeta"',
   ["codigo 0", "o relatorio declara a tabela-verdade com 2^20 = 1048576 linhas (sem exigir que o formato texto imprima todas)", "cobertura completa, 20 condicoes demonstradas"],
   "A expectativa documental e a mesma do oraculo; a suite baseline assumiu indevidamente que o formato texto lista as linhas. Baseline preservado como FALHOU; esta extensao corrige somente a verificacao."),
 c("C2-E01", "check --format text, suite completa", '"check  verify acetam text e json" / "0: comndo concluido"', ["codigo 0"]),
 c("C2-E02", "check --format text, suite incompleta", '"2: ... condição não demonstrda"', ["codigo 2"]),
 c("C2-E03", "verify --format text com conflito", '"check  verify acetam text e json" / "2: ... um cnfito"', ["codigo 2"]),
 c("C2-E04", "verify --format text sem conflito", '"0: comndo concluido"', ["codigo 0"]),
 c("C2-E05", "analyze VM --z3 --format text", '"text | Tabea verdde, pres, suíte, dmonstração por cond ição, fronteras, mutção e o mtivo   prblema"', ["codigo 0 (todos os requisitos completos)", "saida nao vazia"]),
 c("C2-E06", "analyze (A and B) or C --z3 --boundary --format text", '"--z3 --boundary"', ["codigo 0"]),
 c("C2-E07", "truth-csv do sistema VM: 2^n linhas por decisao e linha 0 tudo verdadeiro", '"truth-csv | A tabela-verdade intea" / "A  linha 0  tudo verdadiro"',
   ["para cada decisao, numero de linhas = 2^(entradas)", "a primeira linha de cada decisao tem todas as entradas verdadeiras"]),
 c("C2-E08", "verify com -o grava arquivo", '"-o <arquivo> | Grava  relatorio  arqivo"', ["arquivo gravado nao vazio e codigo 2 (conflito)"]),
]
pathlib.Path(__file__).with_name("oraculo-extensao1.json").write_text(json.dumps(dict(condicao="C2", extensao=1, casos=casos), ensure_ascii=False, indent=1), encoding="utf-8")
print(len(casos))
