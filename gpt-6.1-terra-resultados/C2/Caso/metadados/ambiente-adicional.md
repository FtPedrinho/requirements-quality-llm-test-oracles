# Ferramenta externa e exame da documentação

O executável Z3 não estava no PATH. Após essa verificação, foi baixada para diretório isolado a distribuição oficial `https://github.com/Z3Prover/z3/releases/download/z3-4.13.4/z3-4.13.4-x64-win.zip`; nenhuma instalação global foi feita. SHA-256 do arquivo ZIP: `0A36DD5654FE423D23A727C4570C9DB9A315926A4301189B868B6EB9BFD5979D`. Extraídos somente `z3.exe` e `libz3.dll`. O executável informa `Z3 version 4.13.4 - 64 bit`; hashes: executável `AE8C008BD675C0626CF3891E9ADBC6CF172AA1D70ADA44980055D234A99C77AE`, biblioteca `07B3DDF9CD347786441E4DA11983A0EEC3787A594F670F9FA7F198564AD4CE61`. A origem é a URL oficial; assinatura ou hash publicado independente não foram verificados.

A fonte C2 foi examinada integralmente, em complementação à leitura anterior dos trechos selecionados, e seu hash voltou a corresponder ao protocolo. Contém exemplos, descrições de testes e resultados históricos. Esses dados foram vistos porque integram a documentação completa e não serão copiados para os registros do novo resultado, nem usados como gabarito ou critério de sucesso. A possibilidade de influência residual permanece.

Como autorizado pelo usuário, foram examinados tipos de arquivos e títulos/estruturas das visualizações de C0 e C1, sem expor valores de resultados dessas rodadas. As estruturas encontradas incluem relatório em Markdown e registros CSV e JSON. A nova rodada manterá relatório legível, dados por caso em CSV/JSON e relatórios brutos JaCoCo. Não se afirma que os experimentos anteriores sejam equivalentes ou comparáveis.

Verificação do estado local dos quatro diretórios de produção e POMs: nenhuma modificação ou arquivo não rastreado foi indicado. As demais áreas do workspace não foram inspecionadas.
