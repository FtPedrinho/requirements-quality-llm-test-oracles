# C3 Test Generation Record

## Suite labels

- **S1**: tests generated from operational claims in the literal C3 documentation. The catalog retains conflicting expectations separately.
- **S2**: candidates for independent-reference behaviors not necessarily stated in C3. These are exploratory checks, not a way to import the reference into C3's oracle.
- **S3**: the Maven test run containing both S1 and S2 classes.

The test mapping is in `test-catalog.csv`; oracle source, classification, and conflicting expectations are in `../oracles/oracle-catalog.csv`. Tests marked `Indeterminado` remain present as disabled JUnit tests, with the reason recorded in `../oracles/indeterminate-cases.csv`.

## Test inputs and external interface

Tests invoke the Java `Main.run` entry point to avoid launching an extra process for every case. The real CLI parser, loaders, analyzers, and report writers still execute. Temporary `.mcdc`, JSON, and report files are used for each test. The actual command-line option spellings and JSON report keys are implementation interfaces, not claims that C3 documents their exact syntax/schema.

S2 candidates are aligned by semantic behavior to the frozen independent reference only after their C3-based expected results were recorded. No C2 CSV format or unsupported empty-source behavior was copied into an executable oracle.

## Conflicts preserved as paired cases

The same input and option combination are used for both sides of these conflicts:

- Multiple `.mcdc` lines: separate decisions vs one decision.
- JSON with absent `temporal`: accepted vs rejected.
- More than two conditions with no variant option: masking vs unique-cause.
- Direct mode: complete table vs no complete table.
- Direct `truth-csv`: accepted vs rejected.
- 21 inputs with `--direct`: accepted vs rejected.
- Uncovered analysis: exit code 2 vs exit code 0 after writing the report.

These are intentionally not normalized to the implementation's behavior. Red test results are expected evidence for the experiment and are not grounds for changing expected results.
