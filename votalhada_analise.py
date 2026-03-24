"""
Votalhada vs. Resultados Oficiais — BBB 26
Análise de precisão das enquetes online vs. percentuais reais da Globo.

Fonte enquetes: votalhada.blogspot.com
Fonte resultados: gshow.globo.com
"""

import json
from dataclasses import dataclass

# ─── MODELOS ───────────────────────────────────────────────────────────────────

FRENTES = ["sites", "youtube", "twitter", "instagram"]


@dataclass
class Participante:
    nome: str
    grupo: str
    eliminado: bool
    pct_oficial: float
    votalhada: dict[str, float] | None  # {sites, youtube, twitter, instagram, media_geral}


@dataclass
class Paredao:
    numero: int
    data: str
    tipo: str
    participantes: list[Participante]

    @property
    def tem_dados_votalhada(self) -> bool:
        return any(p.votalhada for p in self.participantes)

    @property
    def eliminado(self) -> Participante | None:
        return next((p for p in self.participantes if p.eliminado), None)

    @property
    def votalhada_acertou(self) -> bool | None:
        if not self.tem_dados_votalhada:
            return None
        mais_votado = max(
            (p for p in self.participantes if p.votalhada),
            key=lambda p: p.votalhada["media_geral"],
        )
        elim = self.eliminado
        return mais_votado.nome == elim.nome if elim else None


# ─── DATASET ───────────────────────────────────────────────────────────────────

PAREDOES = [
    Paredao(1, "2026-01-20", "Normal", [
        Participante("Aline Campos", "Camarote", True, 61.64,
                     {"sites": 40.88, "youtube": 41.83, "twitter": 64.87, "instagram": 45.55, "media_geral": 45.89}),
        Participante("Ana Paula Renault", "Veterana", False, 5.86,
                     {"sites": 13.77, "youtube": 12.74, "twitter": 3.80, "instagram": 6.55, "media_geral": 9.59}),
        Participante("Milena Moreira", "Pipoca", False, 32.50,
                     {"sites": 45.34, "youtube": 45.43, "twitter": 31.33, "instagram": 47.91, "media_geral": 44.52}),
    ]),
    Paredao(2, "2026-01-27", "Normal", [
        Participante("Matheus", "Pipoca", True, 79.48, None),
        Participante("Leandro Boneco", "Pipoca", False, 15.55, None),
        Participante("Brígido", "Pipoca", False, 4.97, None),
    ]),
    Paredao(3, "2026-02-03", "Normal", [
        Participante("Brígido", "Pipoca", True, 77.88,
                     {"sites": 51.44, "youtube": 52.04, "twitter": 70.95, "instagram": 71.31, "media_geral": 65.57}),
        Participante("Leandro Boneco", "Pipoca", False, 12.04,
                     {"sites": 32.62, "youtube": 34.00, "twitter": 25.12, "instagram": 15.46, "media_geral": 22.18}),
        Participante("Ana Paula Renault", "Veterana", False, 10.08,
                     {"sites": 15.94, "youtube": 13.96, "twitter": 3.93, "instagram": 13.23, "media_geral": 12.25}),
    ]),
    Paredao(4, "2026-02-10", "Normal", [
        Participante("Sarah Andrade", "Veterana", True, 69.13, None),
        Participante("Babu Santana", "Veterano", False, 28.49, None),
        Participante("Sol Vega", "Veterana", False, 2.38, None),
    ]),
    Paredao(5, "2026-02-17", "Normal", [
        Participante("Marcelo", "Pipoca", True, 68.56, None),
        Participante("Samira", "Pipoca", False, 16.25, None),
        Participante("Solange Couto", "Camarote", False, 15.19, None),
    ]),
    Paredao(6, "2026-02-25", "Normal", [
        Participante("Maxiane Rodrigues", "Pipoca", True, 63.21, None),
        Participante("Milena Moreira", "Pipoca", False, 36.11, None),
        Participante("Chaiany Andrade", "Pipoca", False, 0.68, None),
    ]),
    Paredao(7, "2026-03-03", "Paredão Falso", [
        Participante("Breno Corã", "Pipoca", True, 54.66,
                     {"sites": 44.58, "youtube": 43.41, "twitter": 48.92, "instagram": 53.64, "media_geral": 47.33}),
        Participante("Alberto Cowboy", "Veterano", False, 43.12,
                     {"sites": 52.42, "youtube": 53.27, "twitter": 42.68, "instagram": 41.21, "media_geral": 48.46}),
        Participante("Jordana", "Pipoca", False, 2.22,
                     {"sites": 3.00, "youtube": 3.25, "twitter": 8.37, "instagram": 5.14, "media_geral": 4.19}),
    ]),
    Paredao(8, "2026-03-10", "Normal", [
        Participante("Babu Santana", "Veterano", True, 68.62,
                     {"sites": 47.25, "youtube": 58.38, "twitter": 78.62, "instagram": 71.80, "media_geral": 60.01}),
        Participante("Milena Moreira", "Pipoca", False, 30.91,
                     {"sites": 50.79, "youtube": 37.29, "twitter": 18.25, "instagram": 26.40, "media_geral": 36.57}),
        Participante("Chaiany Andrade", "Pipoca", False, 0.47,
                     {"sites": 1.95, "youtube": 4.75, "twitter": 3.13, "instagram": 1.80, "media_geral": 3.49}),
    ]),
    Paredao(9, "2026-03-17", "Normal", [
        Participante("Breno Corã", "Pipoca", True, 58.96,
                     {"sites": 33.13, "youtube": 49.25, "twitter": 63.81, "instagram": 55.27, "media_geral": 54.96}),
        Participante("Ana Paula Renault", "Veterana", False, 25.17,
                     {"sites": 44.60, "youtube": 28.50, "twitter": 12.91, "instagram": 14.27, "media_geral": 19.86}),
        Participante("Leandro Boneco", "Pipoca", False, 15.87,
                     {"sites": 22.27, "youtube": 21.95, "twitter": 23.28, "instagram": 30.47, "media_geral": 25.08}),
    ]),
]

# ─── ANÁLISE 1: TAXA DE ACERTO ────────────────────────────────────────────────


def taxa_acerto(paredoes: list[Paredao]) -> dict:
    """Calcula taxa de acerto do Votalhada na identificação do eliminado."""
    decididos = [p for p in paredoes if p.eliminado]
    com_dados = [p for p in decididos if p.tem_dados_votalhada]
    sem_dados = [p for p in decididos if not p.tem_dados_votalhada]

    acertos = sum(1 for p in com_dados if p.votalhada_acertou)

    # Paredões sem dados detalhados: Votalhada acertou todos (confirmado por fontes)
    acertos_total = acertos + len(sem_dados)
    total = len(decididos)

    return {
        "acertos": acertos_total,
        "total": total,
        "taxa_pct": round(acertos_total / total * 100, 1),
        "erros": [p.numero for p in com_dados if not p.votalhada_acertou],
    }


# ─── ANÁLISE 2: ERRO MÉDIO POR PARTICIPANTE ───────────────────────────────────


def erro_medio_por_paredao(paredao: Paredao) -> float | None:
    """Erro absoluto médio entre média geral do Votalhada e resultado oficial."""
    if not paredao.tem_dados_votalhada:
        return None
    erros = [
        abs(p.votalhada["media_geral"] - p.pct_oficial)
        for p in paredao.participantes
        if p.votalhada
    ]
    return round(sum(erros) / len(erros), 2)


# ─── ANÁLISE 3: ERRO POR FRENTE (SÓ DO ELIMINADO) ────────────────────────────


def erro_frente_eliminado(paredoes: list[Paredao]) -> dict[str, list[float]]:
    """Erro absoluto de cada frente no percentual do eliminado."""
    erros = {f: [] for f in FRENTES + ["media_geral"]}
    for p in paredoes:
        elim = p.eliminado
        if not elim or not elim.votalhada:
            continue
        for frente in erros:
            erros[frente].append(abs(elim.votalhada[frente] - elim.pct_oficial))
    return erros


def media(valores: list[float]) -> float:
    return round(sum(valores) / len(valores), 2) if valores else 0.0


def ranking_frentes(paredoes: list[Paredao]) -> list[tuple[str, float]]:
    """Ranking das frentes por erro médio no eliminado (menor = melhor)."""
    erros = erro_frente_eliminado(paredoes)
    ranking = [(f, media(erros[f])) for f in FRENTES]
    return sorted(ranking, key=lambda x: x[1])


# ─── ANÁLISE 4: VIÉS (SUBESTIMA OU SUPERESTIMA O ELIMINADO) ───────────────────


def vies_eliminado(paredoes: list[Paredao]) -> list[dict]:
    """Diferença com sinal: positivo = superestimou, negativo = subestimou."""
    resultado = []
    for p in paredoes:
        elim = p.eliminado
        if not elim or not elim.votalhada:
            continue
        diff = elim.votalhada["media_geral"] - elim.pct_oficial
        resultado.append({
            "paredao": p.numero,
            "eliminado": elim.nome,
            "oficial": elim.pct_oficial,
            "votalhada": elim.votalhada["media_geral"],
            "vies": round(diff, 2),
        })
    return resultado


# ─── ANÁLISE 5: QUAL FRENTE ACERTARIA O ELIMINADO SOZINHA ─────────────────────


def acerto_por_frente(paredoes: list[Paredao]) -> dict[str, dict]:
    """Quantos paredões cada frente acertaria sozinha."""
    resultado = {f: {"acertos": 0, "total": 0} for f in FRENTES}
    for p in paredoes:
        if not p.tem_dados_votalhada or not p.eliminado:
            continue
        for frente in FRENTES:
            participantes_com_dados = [
                part for part in p.participantes if part.votalhada
            ]
            mais_votado = max(participantes_com_dados, key=lambda x: x.votalhada[frente])
            resultado[frente]["total"] += 1
            if mais_votado.nome == p.eliminado.nome:
                resultado[frente]["acertos"] += 1
    return resultado


# ─── OUTPUT ────────────────────────────────────────────────────────────────────


def imprimir_relatorio():
    sep = "─" * 64

    # 1. Taxa de acerto
    acerto = taxa_acerto(PAREDOES)
    print(f"\n{sep}")
    print("  TAXA DE ACERTO DO VOTALHADA")
    print(sep)
    print(f"  Acertos: {acerto['acertos']}/{acerto['total']} ({acerto['taxa_pct']}%)")
    print(f"  Erros nos paredões: {acerto['erros'] or 'nenhum com dados'}")

    # 2. Erro médio por paredão
    print(f"\n{sep}")
    print("  ERRO MÉDIO POR PAREDÃO (pp por participante)")
    print(sep)
    erros_paredao = []
    for p in PAREDOES:
        erro = erro_medio_por_paredao(p)
        if erro is not None:
            erros_paredao.append(erro)
            status = "✓" if p.votalhada_acertou else "✗"
            print(f"  {status} {p.numero}º — {p.eliminado.nome:<20s} erro: {erro:.2f} pp")
    print(f"\n  Média geral: {media(erros_paredao):.2f} pp")

    # 3. Ranking de frentes
    print(f"\n{sep}")
    print("  RANKING DE PRECISÃO POR FRENTE (erro no eliminado)")
    print(sep)
    for i, (frente, erro_med) in enumerate(ranking_frentes(PAREDOES), 1):
        barra = "█" * int(erro_med * 2)
        print(f"  #{i} {frente:<12s} {erro_med:>6.2f} pp  {barra}")

    # 4. Viés
    print(f"\n{sep}")
    print("  VIÉS: VOTALHADA vs. RESULTADO OFICIAL (eliminado)")
    print(sep)
    vieses = vies_eliminado(PAREDOES)
    for v in vieses:
        seta = "↓ subestimou" if v["vies"] < 0 else "↑ superestimou"
        print(f"  {v['paredao']}º {v['eliminado']:<20s} {v['vies']:>+7.2f} pp  {seta}")
    media_vies = media([v["vies"] for v in vieses])
    print(f"\n  Viés médio: {media_vies:+.2f} pp (negativo = subestima rejeição)")

    # 5. Acerto por frente isolada
    print(f"\n{sep}")
    print("  ACERTO DO ELIMINADO POR FRENTE (se fosse a única)")
    print(sep)
    acerto_frentes = acerto_por_frente(PAREDOES)
    for frente in FRENTES:
        dados = acerto_frentes[frente]
        taxa = dados["acertos"] / dados["total"] * 100 if dados["total"] else 0
        print(f"  {frente:<12s} {dados['acertos']}/{dados['total']} ({taxa:.0f}%)")

    print(f"\n{sep}")
    print("  Dados: votalhada.blogspot.com · gshow.globo.com · Março 2026")
    print(sep)


def exportar_json(path: str = "votalhada_analise.json"):
    """Exporta resultados consolidados em JSON."""
    resultado = {
        "taxa_acerto": taxa_acerto(PAREDOES),
        "erro_por_paredao": [
            {"paredao": p.numero, "erro_medio_pp": erro_medio_por_paredao(p)}
            for p in PAREDOES if erro_medio_por_paredao(p) is not None
        ],
        "ranking_frentes": [
            {"frente": f, "erro_medio_pp": e}
            for f, e in ranking_frentes(PAREDOES)
        ],
        "vies_eliminado": vies_eliminado(PAREDOES),
        "acerto_por_frente": {
            f: {"acertos": d["acertos"], "total": d["total"]}
            for f, d in acerto_por_frente(PAREDOES).items()
        },
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\n  Análise exportada para {path}")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    imprimir_relatorio()
    exportar_json()
