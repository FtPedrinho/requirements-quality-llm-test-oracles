package io.github.rvdomingos.mcdc.cli;

import io.github.rvdomingos.mcdc.core.DecisionAnalysis;
import io.github.rvdomingos.mcdc.core.Mcdc;
import io.github.rvdomingos.mcdc.core.McdcOptions;
import io.github.rvdomingos.mcdc.core.McdcVariant;
import io.github.rvdomingos.mcdc.core.TestCase;
import io.github.rvdomingos.mcdc.core.TestSetEvaluation;
import io.github.rvdomingos.mcdc.core.model.Decision;
import io.github.rvdomingos.mcdc.core.model.DecisionSet;
import io.github.rvdomingos.mcdc.core.mutation.MutationReport;
import io.github.rvdomingos.mcdc.requirements.ExpressionParser;
import io.github.rvdomingos.mcdc.requirements.Nat2TestJsonReader;
import io.github.rvdomingos.mcdc.requirements.RequirementsFile;
import io.github.rvdomingos.mcdc.requirements.TestCasesFile;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Comando {@code mcdc}. */
public final class Main {

    static final int OK = 0;
    static final int INPUT_ERROR = 1;
    static final int UNCOVERED = 2;

    private static final String USAGE = """
            Uso:
              mcdc analyze <fonte> [opções]                gera a suíte mínima de testes MC/DC
              mcdc check   <fonte> --tests <testes.csv>    mede o MC/DC de testes já existentes

            Fonte (uma só):
              "<expressão>"           ex.: "(A and B) or C", 'speed > 100 /\\ mode = idle'
              -f <arquivo.mcdc>       um requisito por linha: ID: expressão
              --json <decisoes.json>  decisões no formato do Extractor da NAT2TEST

            Opções:
              --unique-cause          causa única em vez de mascaramento
              --constraint "<expr>"   restrição entre condições (só com expressão direta)
              --z3                    usa o Z3 para descobrir linhas impossíveis e gerar valores concretos
              --boundary              com --z3, acrescenta variantes de fronteira (speed > 100 -> speed = 101)
              --mutation              confere se a suíte detecta versões do requisito com uma falha
              --format <formato>      text (padrão), json, csv (suíte), truth-csv (tabela verdade inteira)
                                      ou gherkin; check aceita text e json
              -o <arquivo>            grava o relatório no arquivo em vez de mostrar na tela

            Exemplos:
              mcdc analyze "(A and B) or C"
              mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary
              mcdc analyze --json exemplos/decisoes.json --format json -o relatorio.json
              mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv -o tabela.csv
              mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv
            """;

    /** Opções lidas da linha de comando. */
    private record Options(String command, String expression, String file, String json, String constraint,
            String tests, String format, String output, McdcVariant variant, boolean z3, boolean boundary,
            boolean mutation) {
    }

    private Main() {
    }

    public static void main(String[] args) {
        System.exit(run(args));
    }

    static int run(String[] args) {
        if (args.length == 0 || !List.of("analyze", "check").contains(args[0])) {
            System.err.print(USAGE);
            return INPUT_ERROR;
        }
        try {
            Options options = parse(args);
            DecisionSet set = load(options);
            Z3FeasibilityChecker checker = options.z3() ? new Z3FeasibilityChecker(set.inputs()) : null;
            McdcOptions mcdc = McdcOptions.defaults()
                    .withVariant(options.variant())
                    .withConstraint(options.constraint() == null ? null : ExpressionParser.parse(options.constraint()))
                    .withFeasibility(checker);
            return options.command().equals("check")
                    ? check(options, set, mcdc)
                    : analyze(options, set, mcdc, checker);
        } catch (IllegalArgumentException | IllegalStateException e) {
            System.err.println("Erro: " + e.getMessage());
            return INPUT_ERROR;
        } catch (IOException e) {
            System.err.println("Erro de arquivo: " + e.getMessage());
            return INPUT_ERROR;
        }
    }

    private static int analyze(Options options, DecisionSet set, McdcOptions mcdc, Z3FeasibilityChecker checker)
            throws IOException {
        List<DecisionAnalysis> analyses = set.decisions().stream()
                .map(decision -> Mcdc.analyze(decision, mcdc))
                .map(a -> options.boundary()
                        ? a.withBoundaryTests(checker.boundaryTests(a.decision().expression(), a.report().minimalSuite()))
                        : a)
                .map(a -> options.mutation() ? a.withMutation(MutationReport.of(a.report())) : a)
                .toList();
        String report = switch (options.format()) {
            case "json" -> JsonReport.format(set.system(), mcdc, options.constraint(), analyses);
            case "csv" -> CsvReport.format(analyses);
            case "truth-csv" -> TruthTableCsvReport.format(analyses);
            case "gherkin" -> GherkinReport.format(set.system(), analyses);
            default -> TextReport.format(analyses, options.constraint());
        };
        write(report, options.output());
        return analyses.stream().allMatch(a -> a.report().isComplete()) ? OK : UNCOVERED;
    }

    private static int check(Options options, DecisionSet set, McdcOptions mcdc) throws IOException {
        TestCasesFile.Contents contents = TestCasesFile.read(Path.of(options.tests()));
        if (!contents.hasDecisionColumn() && set.decisions().size() > 1) {
            throw new IllegalArgumentException("O arquivo de testes precisa da coluna \"decision\" quando há mais de uma decisão.");
        }
        List<CheckReport.Entry> entries = new ArrayList<>();
        for (Decision decision : set.decisions()) {
            Map<String, TestCasesFile.RawTest> raw = contents.hasDecisionColumn()
                    ? contents.byDecision().getOrDefault(decision.id(), Map.of())
                    : contents.byDecision().get("");
            List<TestCase> tests = new ArrayList<>();
            raw.forEach((name, test) ->
                    tests.add(TestCase.resolve(decision.expression(), name, test.values(), test.expected())));
            TestSetEvaluation evaluation = Mcdc.evaluate(decision.expression(), mcdc, tests);
            entries.add(new CheckReport.Entry(decision, evaluation));
        }
        String report = options.format().equals("json")
                ? CheckReport.json(set.system(), mcdc, entries)
                : CheckReport.text(entries);
        write(report, options.output());
        return entries.stream().allMatch(e -> e.evaluation().isComplete()) ? OK : UNCOVERED;
    }

    private static Options parse(String[] args) {
        String command = args[0];
        String expression = null;
        String file = null;
        String json = null;
        String constraint = null;
        String tests = null;
        String format = "text";
        String output = null;
        McdcVariant variant = McdcVariant.MASKING;
        boolean z3 = false;
        boolean boundary = false;
        boolean mutation = false;

        for (int i = 1; i < args.length; i++) {
            switch (args[i]) {
                case "--unique-cause" -> variant = McdcVariant.UNIQUE_CAUSE;
                case "--z3" -> z3 = true;
                case "--boundary" -> boundary = true;
                case "--mutation" -> mutation = true;
                case "--constraint" -> constraint = valueAfter(args, i++);
                case "-f" -> file = valueAfter(args, i++);
                case "--json" -> json = valueAfter(args, i++);
                case "--tests" -> tests = valueAfter(args, i++);
                case "--format" -> format = valueAfter(args, i++);
                case "-o" -> output = valueAfter(args, i++);
                default -> {
                    if (args[i].startsWith("-")) {
                        throw new IllegalArgumentException("Opção desconhecida: " + args[i]);
                    }
                    expression = args[i];
                }
            }
        }

        int sources = (expression != null ? 1 : 0) + (file != null ? 1 : 0) + (json != null ? 1 : 0);
        if (sources != 1) {
            throw new IllegalArgumentException("Informe uma única fonte: uma expressão, -f <arquivo> ou --json <arquivo>.");
        }
        List<String> formats = command.equals("check") ? List.of("text", "json") : List.of("text", "json", "csv", "truth-csv", "gherkin");
        if (!formats.contains(format)) {
            throw new IllegalArgumentException("Formato desconhecido para " + command + ": " + format + ". Use " + String.join(", ", formats) + ".");
        }
        if (boundary && !z3) {
            throw new IllegalArgumentException("--boundary precisa de --z3.");
        }
        if ((boundary || mutation) && command.equals("check")) {
            throw new IllegalArgumentException("--boundary e --mutation só valem para analyze.");
        }
        if (expression == null && constraint != null) {
            throw new IllegalArgumentException("--constraint só vale com uma expressão direta.");
        }
        if (command.equals("check") && tests == null) {
            throw new IllegalArgumentException("check precisa de --tests <arquivo.csv>.");
        }
        return new Options(command, expression, file, json, constraint, tests, format, output, variant, z3, boundary,
                mutation);
    }

    private static DecisionSet load(Options options) throws IOException {
        if (options.file() != null) {
            return RequirementsFile.read(Path.of(options.file()));
        }
        if (options.json() != null) {
            return Nat2TestJsonReader.read(Path.of(options.json()));
        }
        return new DecisionSet(null, List.of(), List.of(RequirementsFile.expression("REQ", null, options.expression())));
    }

    private static void write(String report, String output) throws IOException {
        if (output == null) {
            System.out.print(report);
        } else {
            Files.writeString(Path.of(output), report);
            System.out.println("Relatório gravado em " + output);
        }
    }

    /** Valor da opção em args[i + 1]. Quem chama avança o índice com i++. */
    private static String valueAfter(String[] args, int i) {
        if (i + 1 >= args.length) {
            throw new IllegalArgumentException("Faltou o valor de " + args[i]);
        }
        return args[i + 1];
    }
}
