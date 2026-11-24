# Proveniência e execução

- HEAD no início: `2aec3564c30890031db86bd2cc1bb015794d5d2e`.
  A correspondência integral da árvore de trabalho com o commit não foi
  verificada. Os 51 arquivos de produção utilizados têm hashes em
  [fontes-sut.sha256](fontes-sut.sha256), conferidos após a execução.
- Windows 10.0.26200.0, arquitetura x64; Java e javac 21.0.3; Python
  3.13.5; Git 2.41.0.windows.1; JaCoCo 0.8.16. Maven não estava no PATH;
  o executor usou javac e arquivos de dependência já presentes. Nenhuma
  dependência foi instalada.
- Z3 independente: pacote `z3-solver` 5.4.1.0, biblioteca 5.4.1,
  SHA-256 da DLL
  `6B1FF40D6B87076EEFC21C215E394EBE38D0AF05ED0D8D42F4C606A608BAFD3D`.
  O executável usado pelo SUT também é versão 5.4.1, SHA-256
  `3D51A3AACB54506245E205759EE553AC358F1E4B64ECCBD056125B685B26B780`.
- JaCoCo agent SHA-256
  `37AE2F374AD77E85C59C6E5B46565226C3AC3CB460AC19DE0BCB844AC2F43E33`;
  CLI SHA-256
  `1F2A806225623FBD9F53D1EE0E42A6975323DE0ADEBE01C12FC464ED147D756A`.
- Jackson databind 2.17.2 SHA-256
  `C04993F33C0F845342653784F14F38373D005280E6359DB5F808701CFAE73C0C`;
  core 2.17.2 SHA-256
  `721A189241DAB0525D9E858E5CB604D3ECC0EDE081E2DE77D6F34FA5779A5B46`;
  annotations 2.17.2 SHA-256
  `873A606E23507969F9BBBEA939D5E19274A88775EA5A169BA7E2D795AA5156E1`.
- Fonte C4 SHA-256
  `D6BC0A588CD9A7DF7F1F566573944FA5CB1707BBA676B4E9854CAD2CC5440FC2`;
  prompt SHA-256
  `A89A9F10E579B0189AB83CD845A42764637AB6754BD28D2E567D8D6A6B401E3F`;
  metodologia SHA-256
  `EC3F96C59C6C2A3570E7833B2C561B6DB38BE415B41C10A7F383BF5DA2FA6B1F`.
- Nome/versão específicos do modelo, configuração, chamadas, tokens, custos,
  duração total da geração e recursos da máquina: não informado. A resposta
  integral da plataforma não foi exportada; não informado. O prompt integral
  está em [prompt-usado.md](prompt-usado.md).

## Cronologia e comandos

1. Verificação SHA-256 da fonte, leitura do prompt, protocolo e fonte C4.
2. Formalização e execução independente:
   `python copilot-resultados\C4\detalhes\executar_z3.py`.
   Resultados e testemunhas: [resultado-z3.json](resultado-z3.json).
3. Oráculos congelados em 2026-11-23 16:48:15 UTC:
   [congelamento-oraculos.sha256](congelamento-oraculos.sha256).
4. Inspeção dos fontes de produção. Suíte e entradas congeladas em
   2026-11-23 16:51:28 UTC:
   [congelamento-suite.sha256](congelamento-suite.sha256).
5. Execução:
   `.\copilot-resultados\C4\suite\executar.ps1 -Z3 'C:\Users\User\AppData\Roaming\Python\bin\z3.exe'`.
   O script compila os quatro módulos com `javac`, compila o harness à parte,
   executa `java` com JaCoCo e produz XML e dados estruturados. A duração da
   execução Java foi 6308 ms; o código 1 representa asserções falhas, não
   uma falha de compilação. O log de erro Java está vazio.
6. Os hashes dos oráculos, da suíte e dos fontes de produção foram verificados
   depois da execução; não foi detectada alteração entre as verificações.
   Isso não demonstra ausência de alteração transitória no ambiente compartilhado.

Não houve execução de suíte histórica, algoritmos de mutação ou rodadas
orientadas por cobertura. A execução usou a biblioteca Z3 independente antes
do congelamento e o executável Z3 para o SUT depois dele.
