#!/usr/bin/env bash
# Cria o esqueleto Maven multi-módulo da Fase 1 (ver docs/arquitetura-fase1.md).
# Uso: ./setup.sh            (roda na pasta do script)
#      GROUP_ID=com.exemplo.mcdc ./setup.sh
set -euo pipefail

GROUP_ID="${GROUP_ID:-io.github.rvdomingos.mcdc}"
VERSION="0.1.0-SNAPSHOT"
JAVA_RELEASE="21"
JUNIT_VERSION="5.11.4"

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [ -e pom.xml ] || [ -e mcdc-core ] || [ -e mcdc-requirements ]; then
  echo "Já existe pom.xml, mcdc-core ou mcdc-requirements em $ROOT. Nada foi alterado." >&2
  exit 1
fi

PKG_DIR="$(echo "$GROUP_ID" | tr '.' '/')"
CORE_MAIN="mcdc-core/src/main/java/$PKG_DIR/core"
CORE_TEST="mcdc-core/src/test/java/$PKG_DIR/core"
REQ_MAIN="mcdc-requirements/src/main/java/$PKG_DIR/requirements"

mkdir -p "$CORE_MAIN/model" "$CORE_TEST/model" "$REQ_MAIN"

# ---------- pom pai ----------
cat > pom.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>$GROUP_ID</groupId>
  <artifactId>mcdc-parent</artifactId>
  <version>$VERSION</version>
  <packaging>pom</packaging>
  <name>MC/DC Tool</name>

  <modules>
    <module>mcdc-core</module>
    <module>mcdc-requirements</module>
  </modules>

  <properties>
    <maven.compiler.release>$JAVA_RELEASE</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <junit.version>$JUNIT_VERSION</junit.version>
  </properties>

  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>$GROUP_ID</groupId>
        <artifactId>mcdc-core</artifactId>
        <version>\${project.version}</version>
      </dependency>
      <dependency>
        <groupId>org.junit</groupId>
        <artifactId>junit-bom</artifactId>
        <version>\${junit.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  <dependencies>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-compiler-plugin</artifactId>
          <version>3.13.0</version>
        </plugin>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>3.5.2</version>
        </plugin>
      </plugins>
    </pluginManagement>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-enforcer-plugin</artifactId>
        <version>3.5.0</version>
        <executions>
          <execution>
            <id>require-java</id>
            <goals>
              <goal>enforce</goal>
            </goals>
            <configuration>
              <rules>
                <requireJavaVersion>
                  <version>[\${maven.compiler.release},)</version>
                  <message>Este projeto precisa do JDK \${maven.compiler.release}. Ex.: export JAVA_HOME=$(/usr/libexec/java_home -v \${maven.compiler.release})</message>
                </requireJavaVersion>
              </rules>
            </configuration>
          </execution>
        </executions>
      </plugin>
    </plugins>
  </build>
</project>
EOF

# ---------- mcdc-core ----------
cat > mcdc-core/pom.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>$GROUP_ID</groupId>
    <artifactId>mcdc-parent</artifactId>
    <version>$VERSION</version>
  </parent>

  <artifactId>mcdc-core</artifactId>
  <name>MC/DC Core Engine</name>
</project>
EOF

cat > "$CORE_MAIN/model/Expr.java" <<EOF
package $GROUP_ID.core.model;

import java.util.Map;

/** Expressão booleana de uma decisão. As folhas são condições atômicas. */
public sealed interface Expr permits Cond, And, Or, Not {

    /** Avalia a expressão para os valores dados, indexados pelo id da condição. */
    boolean eval(Map<String, Boolean> values);
}
EOF

cat > "$CORE_MAIN/model/Cond.java" <<EOF
package $GROUP_ID.core.model;

import java.util.Map;

public record Cond(String id) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        Boolean value = values.get(id);
        if (value == null) {
            throw new IllegalArgumentException("Condição sem valor: " + id);
        }
        return value;
    }
}
EOF

cat > "$CORE_MAIN/model/And.java" <<EOF
package $GROUP_ID.core.model;

import java.util.Map;

public record And(Expr left, Expr right) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        return left.eval(values) & right.eval(values);
    }
}
EOF

cat > "$CORE_MAIN/model/Or.java" <<EOF
package $GROUP_ID.core.model;

import java.util.Map;

public record Or(Expr left, Expr right) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        return left.eval(values) | right.eval(values);
    }
}
EOF

cat > "$CORE_MAIN/model/Not.java" <<EOF
package $GROUP_ID.core.model;

import java.util.Map;

public record Not(Expr operand) implements Expr {

    @Override
    public boolean eval(Map<String, Boolean> values) {
        return !operand.eval(values);
    }
}
EOF

cat > "$CORE_MAIN/model/Decision.java" <<EOF
package $GROUP_ID.core.model;

import java.util.Map;

/**
 * Decisão extraída de um requisito.
 *
 * @param id             identificador do requisito, ex.: "REQ-001"
 * @param expression     antecedente do requisito
 * @param labels         id da condição para texto legível
 * @param expectedAction consequente do requisito
 */
public record Decision(String id, Expr expression, Map<String, String> labels, String expectedAction) {
}
EOF

cat > "$CORE_MAIN/McdcVariant.java" <<EOF
package $GROUP_ID.core;

public enum McdcVariant {
    UNIQUE_CAUSE,
    MASKING
}
EOF

cat > "$CORE_TEST/model/ExprTest.java" <<EOF
package $GROUP_ID.core.model;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Map;
import org.junit.jupiter.api.Test;

class ExprTest {

    // (A and B) or C
    private final Expr decision = new Or(new And(new Cond("A"), new Cond("B")), new Cond("C"));

    @Test
    void evaluatesAndOr() {
        assertTrue(decision.eval(Map.of("A", true, "B", true, "C", false)));
        assertFalse(decision.eval(Map.of("A", true, "B", false, "C", false)));
        assertTrue(decision.eval(Map.of("A", false, "B", false, "C", true)));
    }

    @Test
    void evaluatesNot() {
        Expr expr = new And(new Cond("A"), new Not(new Cond("B")));
        assertTrue(expr.eval(Map.of("A", true, "B", false)));
        assertFalse(expr.eval(Map.of("A", true, "B", true)));
    }

    @Test
    void rejectsMissingCondition() {
        assertThrows(IllegalArgumentException.class, () -> decision.eval(Map.of("A", true, "B", true)));
    }
}
EOF

# ---------- mcdc-requirements ----------
cat > mcdc-requirements/pom.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <parent>
    <groupId>$GROUP_ID</groupId>
    <artifactId>mcdc-parent</artifactId>
    <version>$VERSION</version>
  </parent>

  <artifactId>mcdc-requirements</artifactId>
  <name>MC/DC Requirements Adapters</name>

  <dependencies>
    <dependency>
      <groupId>$GROUP_ID</groupId>
      <artifactId>mcdc-core</artifactId>
    </dependency>
  </dependencies>
</project>
EOF

cat > "$REQ_MAIN/package-info.java" <<EOF
/** Adaptadores de entrada do modo requisitos: expressão de requisito e DFRS da NAT2TEST. */
package $GROUP_ID.requirements;
EOF

# ---------- .gitignore ----------
if [ ! -e .gitignore ]; then
  cat > .gitignore <<EOF
target/
.idea/
*.iml
.classpath
.project
.settings/
.vscode/
.DS_Store
EOF
fi

echo "Esqueleto criado em $ROOT"
echo "Para validar: mvn -q verify"
