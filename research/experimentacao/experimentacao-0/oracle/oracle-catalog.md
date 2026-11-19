# Catálogo de oráculos - Experimento 0 reconstruído

| Oracle ID | Behavior ID | Comportamento | Resultado esperado | Fonte |
|---|---|---|---|---|
| E0-ORACLE-B001 | B001 | analyze expression | MC/DC report complete | README; PDF sections; Main.analyze |
| E0-ORACLE-B002 | B002 | check tests | coverage report and problems | README; CheckReport; Main.check |
| E0-ORACLE-B003 | B003 | verify decisions | conflicts/overlaps/gaps | README; Z3 verifier docs |
| E0-ORACLE-B004 | B004 | missing/invalid command | usage and exit 1 | Main USAGE |
| E0-ORACLE-B005 | B005 | exactly one source | exit 1 | README; Main.parse |
| E0-ORACLE-B006 | B006 | unknown option | exit 1 | Main USAGE |
| E0-ORACLE-B007 | B007 | and syntax | AST And | README; ExpressionParser docs |
| E0-ORACLE-B008 | B008 | or syntax | AST Or | README; ExpressionParser docs |
| E0-ORACLE-B009 | B009 | not syntax | AST Not | README; ExpressionParser docs |
| E0-ORACLE-B010 | B010 | comparisons | Predicate AST | README; ExpressionParser docs |
| E0-ORACLE-B011 | B011 | invalid expression | error with requirement ID and exit 1 | Requirements docs |
| E0-ORACLE-B012 | B012 | .mcdc parsing | DecisionSet | RequirementsFile docs |
| E0-ORACLE-B013 | B013 | empty .mcdc | exit 1 | RequirementsFile docs |
| E0-ORACLE-B014 | B014 | NAT2TEST JSON valid | DecisionSet | README; Nat2TestJsonReader |
| E0-ORACLE-B015 | B015 | NAT2TEST JSON invalid | exit 1 | README; Nat2TestJsonReader |
| E0-ORACLE-B016 | B016 | CSV valid | TestCasesContents | TestCasesFile docs |
| E0-ORACLE-B017 | B017 | CSV invalid | exit 1 | TestCasesFile docs |
| E0-ORACLE-B018 | B018 | truth table | 2^n rows | TruthTable docs |
| E0-ORACLE-B019 | B019 | repeated conditions | conditions A#1 A#2 | README; Condition docs |
| E0-ORACLE-B020 | B020 | masking | result pairs | README; IndependencePairs docs |
| E0-ORACLE-B021 | B021 | unique cause | only condition changes | README; IndependencePairs docs |
| E0-ORACLE-B022 | B022 | infeasible lines | impossible rows removed | README; Z3 docs |
| E0-ORACLE-B023 | B023 | greedy suite | greedy suite | MinimalSuite docs |
| E0-ORACLE-B024 | B024 | exact suite | Z3 minimum rows | README; Z3SuiteOptimizer |
| E0-ORACLE-B025 | B025 | direct analyzer | pairs without truth table | README; Z3DirectAnalyzer |
| E0-ORACLE-B026 | B026 | boundary tests | adjacent boundaries | README; Z3FeasibilityChecker |
| E0-ORACLE-B027 | B027 | internal mutation | mutation score/survivors | README; MutationReport |
| E0-ORACLE-B028 | B028 | requirement conflict | conflict with witness | Z3 verifier docs |
| E0-ORACLE-B029 | B029 | requirement gap | gap witness | Z3 verifier docs |
| E0-ORACLE-B030 | B030 | JSON report | JSON report | README; JsonReport docs |
| E0-ORACLE-B031 | B031 | CSV report | CSV suite | README; CsvReport docs |
| E0-ORACLE-B032 | B032 | truth-csv | full truth table | README; TruthTableCsvReport |
| E0-ORACLE-B033 | B033 | exit 2 | exit 2 | README; Main |
| E0-ORACLE-B034 | B034 | Z3 unavailable | exit 1 with clear error | README; Z3Process |
