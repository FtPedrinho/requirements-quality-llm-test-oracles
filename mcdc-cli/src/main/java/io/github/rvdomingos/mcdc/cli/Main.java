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
import io.github.rvdomingos.mcdc.core.model.Expr;
import io.github.rvdomingos.mcdc.z3.Z3DirectAnalyzer;
import io.github.rvdomingos.mcdc.z3.Z3FeasibilityChecker;
import io.github.rvdomingos.mcdc.z3.Z3RequirementsVerifier;
import io.github.rvdomingos.mcdc.z3.Z3SuiteOptimizer;
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
              mcdc verify  <fonte> [--context "<expr>"]    confere os requisitos entre si (usa o Z3)

            Fonte (uma só):
              "<expressão>"           ex.: "(A and B) or C", 'speed > 100 /\\ mode = idle'
              -f <arquivo.mcdc>       um requisito por linha: ID: expressão
              --json <decisoes.json>  decisões no formato do Extractor da NAT2TEST

            Opções:
              --unique-cause          causa única em vez de mascaramento
              --constraint "<expr>"   restrição entre condições (só com expressão direta)
              --z3                    usa o Z3 para descobrir linhas impossíveis e gerar valores concretos;
                                      decisões com mais de 12 entradas passam ao modo direto
              --exact                 suíte exata: a menor possível, escolhida pelo Z3 (em vez da gulosa)
              --direct                pede os pares direto ao Z3, sem montar a tabela (até 30 entradas)
              --boundary              com --z3, acrescenta variantes de fronteira (speed > 100 -> speed = 101)
              --mutation              confere se a suíte detecta versões do requisito com uma falha
              --context "<expr>"      verify: confere se, nessa situação, sempre alguma guarda vale
              --format <formato>      text (padrão), json, csv (suíte) ou truth-csv (tabela verdade inteira);
                                      check e verify aceitam text e json
              -o <arquivo>            grava o relatório no arquivo em vez de mostrar na tela

            Exemplos:
              mcdc analyze "(A and B) or C"
              mcdc analyze "speed > 100 or (speed > 50 and rain)" --z3 --boundary
              mcdc analyze --json exemplos/decisoes.json --format json -o relatorio.json
              mcdc analyze --json exemplos/vm-decisoes.json --z3 --format truth-csv -o tabela.csv
              mcdc check --json exemplos/decisoes.json --tests exemplos/testes.csv
              mcdc verify --json exemplos/npp-decisoes.json
            """;

    /** Opções lidas da linha de comando. */
    private record Options(String command, String expression, String file, String json, String constraint,
            String tests, String format, String output, McdcVariant variant, boolean z3, boolean boundary,
            boolean mutation, boolean exact, boolean direct, String context) {
    }

    private Main() {
    }

    public static void main(String[] args) {
        System.exit(run(args));
    }

    static int run(String[] args) {
        if (args.length == 0 || !List.of("analyze", "check", "verify").contains(args[0])) {
            System.err.print(USAGE);
            return INPUT_ERROR;
        }
        try {
            Options options = parse(args);
            DecisionSet set = load(options);
            if (options.command().equals("verify")) {
                return verify(options, set);
            }
            Z3FeasibilityChecker checker = options.z3() ? new Z3FeasibilityChecker(set.inputs()) : null;
            McdcOptions mcdc = McdcOptions.defaults()
                    .withVariant(options.variant())
                    .withConstraint(options.constraint() == null ? null : ExpressionParser.parse(options.constraint()))
                    .withFeasibility(checker)
                    .withOptimizer(options.exact() ? new Z3SuiteOptimizer() : null);
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
        Z3DirectAnalyzer direct = options.z3() ? new Z3DirectAnalyzer(set.inputs()) : null;
        List<DecisionAnalysis> analyses = new ArrayList<>();
        for (Decision decision : set.decisions()) {
            DecisionAnalysis a = useDirect(options, decision)
                    ? new DecisionAnalysis(decision, direct.analyze(decision.expression(), mcdc))
                    : Mcdc.analyze(decision, mcdc);
            if (options.boundary()) {
                a = a.withBoundaryTests(checker.boundaryTests(decision.expression(), a.report().minimalSuite()));
            }
            if (options.mutation()) {
                if (!a.report().table().isFull()) {
                    throw new IllegalArgumentException(decision.id() + ": --mutation precisa da tabela inteira, "
                            + "que o modo direto não monta (" + decision.expression().inputs().size() + " entradas).");
                }
                a = a.withMutation(MutationReport.of(a.report()));
            }
            analyses.add(a);
        }
        String report = switch (options.format()) {
            case "json" -> JsonReport.format(set.system(), mcdc, options.constraint(), analyses);
            case "csv" -> CsvReport.format(analyses);
            case "truth-csv" -> TruthTableCsvReport.format(analyses);
            default -> TextReport.format(analyses, options.constraint());
        };
        write(report, options.output());
        return analyses.stream().allMatch(a -> a.report().isComplete()) ? OK : UNCOVERED;
    }

    /** Modo direto quando pedido, ou com --z3 quando a verificação linha a linha não cabe (mais de 12 entradas). */
    private static boolean useDirect(Options options, Decision decision) {
        int inputs = decision.expression().inputs().size();
        return options.direct() || (options.z3() && (1L << inputs) > Z3FeasibilityChecker.MAX_ROWS);
    }

    private static int verify(Options options, DecisionSet set) throws IOException {
        Expr context = options.context() == null ? null : ExpressionParser.parse(options.context());
        Z3RequirementsVerifier.Result result = new Z3RequirementsVerifier().verify(set, context);
        String report = options.format().equals("json")
                ? VerifyReport.json(set.system(), options.context(), result)
                : VerifyReport.text(set.system(), options.context(), result);
        write(report, options.output());
        return result.hasProblems() ? UNCOVERED : OK;
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
        boolean exact = false;
        boolean direct = false;
        String context = null;

        for (int i = 1; i < args.length; i++) {
            switch (args[i]) {
                case "--unique-cause" -> variant = McdcVariant.UNIQUE_CAUSE;
                case "--z3" -> z3 = true;
                case "--boundary" -> boundary = true;
                case "--mutation" -> mutation = true;
                case "--exact" -> exact = true;
                case "--direct" -> direct = true;
                case "--context" -> context = valueAfter(args, i++);
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
        List<String> formats = command.equals("analyze") ? List.of("text", "json", "csv", "truth-csv") : List.of("text", "json");
        if (!formats.contains(format)) {
            throw new IllegalArgumentException("Formato desconhecido para " + command + ": " + format + ". Use " + String.join(", ", formats) + ".");
        }
        if (direct) {
            z3 = true; // o modo direto usa o Z3
        }
        if (boundary && !z3) {
            throw new IllegalArgumentException("--boundary precisa de --z3.");
        }
        if (!command.equals("analyze") && (exact || direct)) {
            throw new IllegalArgumentException("--exact e --direct só valem para analyze.");
        }
        if (exact && direct) {
            throw new IllegalArgumentException("--exact escolhe sobre a tabela inteira; não vale com --direct.");
        }
        if (direct && (mutation || format.equals("truth-csv"))) {
            throw new IllegalArgumentException("--mutation e truth-csv precisam da tabela inteira, que --direct não monta.");
        }
        if (context != null && !command.equals("verify")) {
            throw new IllegalArgumentException("--context só vale para verify.");
        }
        if (command.equals("verify") && (z3 || boundary || mutation || constraint != null || tests != null)) {
            throw new IllegalArgumentException("verify aceita só a fonte, --context, --format e -o.");
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
                mutation, exact, direct, context);
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
