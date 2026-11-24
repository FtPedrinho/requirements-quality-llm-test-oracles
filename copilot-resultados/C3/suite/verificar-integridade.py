import hashlib
from pathlib import Path


SUITE = Path(__file__).resolve().parent
ROOT = SUITE.parent
DETAILS = ROOT / "detalhes-C3"
OLD_DETAILS = ROOT / "2026-11-23-experimento-1158"
MANIFESTS = (
    "manifesto-oraculos.sha256",
    "manifesto-suite.sha256",
    "manifesto-repeticao-f03.sha256",
    "manifesto-extensao.sha256",
    "manifesto-fontes-sut.sha256",
)
COPIES = (
    "executar-suite.py",
    "executar-extensao.py",
    "repetir-f03.py",
    "oraculos.json",
    "oraculos-integracao.json",
    "entradas/requisitos.mcdc",
    "entradas/decisoes.json",
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def resolve_recorded_path(name):
    path = Path(name)
    if not path.is_absolute():
        return DETAILS / path
    try:
        relative = path.relative_to(OLD_DETAILS)
    except ValueError:
        return path
    return DETAILS / relative


def main():
    for manifest in MANIFESTS:
        lines = (DETAILS / manifest).read_text(encoding="utf-8-sig").splitlines()
        for line in lines:
            expected, name = line.split("  ", 1)
            path = resolve_recorded_path(name)
            actual = digest(path)
            if actual != expected:
                raise RuntimeError(f"Hash divergente: {path}")
        print(f"{manifest}: {len(lines)} arquivos OK")
    for name in COPIES:
        if digest(SUITE / name) != digest(DETAILS / name):
            raise RuntimeError(f"Copia da suite divergente: {name}")
    print(f"Suite: {len(COPIES)} copias identicas aos originais")


if __name__ == "__main__":
    main()
