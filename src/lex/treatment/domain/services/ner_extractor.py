"""Trilha B Fast-Path Deterministic Named Entity Recognition (NER) Extractor.

Extracts structured operational entities (CPFs, CNPJs, Process Numbers, Bidding Modalities,
Monetary Values, and Validity Dates) directly for Groups 4 to 8 publications.
"""

import re
from datetime import datetime
from typing import Any

# Hoisted compiled regex constants
RE_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
RE_CPF = re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")
RE_PROCESSO = re.compile(
    r"(?:[Pp]rocesso|[Nn]º\s+[Pp]rocesso|[Pp][Aa]\s+n[ºo°\.]?)\s*[:\s]*([\d\.\/\-]+)",
    re.IGNORECASE,
)
RE_LICITACAO = re.compile(
    r"\b(Preg[ãa]o\s+Eletr[ôo]nico|Preg[ãa]o\s+Presencial|Concorr[êe]ncia|Dispensa\s+de\s+Licita[çc][ãa]o|"
    r"Inexigibilidade\s+de\s+Licita[çc][ãa]o|Tomada\s+de\s+Pre[çc]os|Convite|Leil[ãa]o)\s*"
    r"(?:N[ºo°\.]?\s*)?([\d\.\/\-]+)",
    re.IGNORECASE,
)
RE_VALOR = re.compile(
    r"Valor\s*(?:Total|Global|Estimado|do\s+Contrato)?[\s:]*(R\$\s*[\d\.\,]+)",
    re.IGNORECASE,
)
RE_VIGENCIA = re.compile(
    r"Vigência[\s:]*(\d{2}/\d{2}/\d{4})\s*(?:a|até|-)\s*(\d{2}/\d{2}/\d{4})",
    re.IGNORECASE,
)
RE_OBJETO = re.compile(
    r"Objeto[\s:]*([^\n\r]+)",
    re.IGNORECASE,
)

# Section 2: Personnel Acts Regex Constants
RE_PESSOAL_ACAO = re.compile(
    r"\b(DESIGNAR|NOMEAR|EXONERAR|DISPENSAR|DECLARAR\s+APOSENTAD[OA]|REMOVER|SUBSTITUIR|"
    r"CONCEDER\s+APOSENTADORIA|CONCEDER\s+PENS[AÃ]O|DECLARAR\s+VAC[AÂ]NCIA)\b",
    re.IGNORECASE,
)
RE_SERVIDOR_NOME = re.compile(
    r"(?:servidor(?:a)?|bacharel(?:a)?)\s+([A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]{4,60}?)"
    r"(?:\s*[\(,–\-]|\s+para\b|\s+ocupante\b|\s+matrícula\b|\s+siape\b)",
    re.IGNORECASE,
)
RE_MATRICULA = re.compile(
    r"(?:(?:matrícula|siape|registro\s+funcional)[\s:nº°]*|\()(\d{4,10})\)?",
    re.IGNORECASE,
)
RE_CARGO_ORIGEM = re.compile(
    r"(?:ocupante\s+do\s+cargo\s+de|titular\s+do\s+cargo\s+de)\s+"
    r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ\w\s\-_\/]{3,60}?)(?:,|\s+Área|\s+para\b)",
    re.IGNORECASE,
)
RE_CARGO_DESTINO = re.compile(
    r"(?:cargo\s+em\s+comissão\s+de|função\s+comissionada\s+de|função\s+de|"
    r"para\s+exercer[,\s\w]*?\s+o\s+cargo\s+(?:em\s+comissão\s+)?de)\s+"
    r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9\-_/\s]{3,60}?)"
    r"(?:,|\s+do\s+GABINETE|\s+do\s+DEPARTAMENTO|\s+da\s+SECRETARIA|\s+no\b|\s+na\b|\s+nos\b|\s+nas\b|$)",
    re.IGNORECASE,
)

PESSOAL_ACTION_MAP: dict[str, str] = {
    "designar": "DESIGNACAO",
    "nomear": "NOMEACAO",
    "exonerar": "EXONERACAO",
    "dispensar": "DISPENSA",
    "remover": "REMOCAO",
    "substituir": "SUBSTITUICAO",
}


def _mask_cpf(cpf: str) -> str:
    """Masks first 3 and last 2 digits of a CPF for LGPD compliance."""
    parts = cpf.split("-")
    if len(parts) == 2:
        num_parts = parts[0].split(".")
        if len(num_parts) == 3:
            return f"***.{num_parts[1]}.{num_parts[2]}-**"
    return "***.***.***-**"


def _parse_currency(val_str: str) -> float | None:
    """Parses a Brazilian currency string (e.g. 'R$ 1.450.000,00') into a float."""
    try:
        clean = val_str.replace("R$", "").strip()
        clean = clean.replace(".", "").replace(",", ".")
        return float(clean)
    except (ValueError, AttributeError):
        return None


def _parse_date(date_str: str) -> str | None:
    """Parses DD/MM/YYYY into ISO YYYY-MM-DD."""
    try:
        dt = datetime.strptime(date_str.strip(), "%d/%m/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None


class DeterministicNerExtractor:
    """High-throughput regex NER entity extractor for Trilha B operational acts."""

    @classmethod
    def extract_entities(cls, text: str) -> dict[str, Any]:
        """Extracts structured entities from operational/contractual text.

        Args:
            text: Plain text of the notice or operational act.

        Returns:
            A dictionary containing identified structured fields.
        """
        entities: dict[str, Any] = {}

        # 1. CNPJ extraction
        cnpjs = list(dict.fromkeys(RE_CNPJ.findall(text)))
        if cnpjs:
            entities["cnpjs"] = cnpjs

        # 2. CPF extraction with LGPD masking
        cpfs = list(dict.fromkeys(RE_CPF.findall(text)))
        if cpfs:
            entities["cpfs_masked"] = [_mask_cpf(c) for c in cpfs]
            entities["total_cpfs_found"] = len(cpfs)

        # 3. Process Number extraction
        proc_matches = RE_PROCESSO.findall(text)
        if proc_matches:
            clean_procs = [p.strip(" .;") for p in proc_matches if len(p.strip(" .;")) >= 5]
            if clean_procs:
                entities["processos"] = list(dict.fromkeys(clean_procs))

        # 4. Bidding modality and number
        m_lic = RE_LICITACAO.search(text)
        if m_lic:
            raw_mod = m_lic.group(1).strip()
            # Canonical normalization
            mod_lower = raw_mod.lower()
            if "pregão eletrônico" in mod_lower or "pregao eletronico" in mod_lower:
                modality = "Pregão Eletrônico"
            elif "pregão presencial" in mod_lower or "pregao presencial" in mod_lower:
                modality = "Pregão Presencial"
            elif "dispensa" in mod_lower:
                modality = "Dispensa de Licitação"
            elif "inexigibilidade" in mod_lower:
                modality = "Inexigibilidade de Licitação"
            elif "concorrência" in mod_lower or "concorrencia" in mod_lower:
                modality = "Concorrência"
            elif "tomada de preços" in mod_lower or "tomada de precos" in mod_lower:
                modality = "Tomada de Preços"
            elif "leilão" in mod_lower or "leilao" in mod_lower:
                modality = "Leilão"
            elif "convite" in mod_lower:
                modality = "Convite"
            else:
                modality = raw_mod.title()

            entities["licitacao_modalidade"] = modality
            entities["licitacao_numero"] = m_lic.group(2).strip(" .;")

        # 5. Monetary values
        m_val = RE_VALOR.search(text)
        if m_val:
            raw_val = m_val.group(1).strip(" .;")
            num_val = _parse_currency(raw_val)
            if num_val is not None:
                entities["valor_total"] = num_val
                entities["valor_formatado"] = raw_val

        # 6. Validity period
        m_vig = RE_VIGENCIA.search(text)
        if m_vig:
            start_d = _parse_date(m_vig.group(1))
            end_d = _parse_date(m_vig.group(2))
            if start_d and end_d:
                entities["vigencia_inicio"] = start_d
                entities["vigencia_fim"] = end_d

        # 7. Object
        m_obj = RE_OBJETO.search(text)
        if m_obj:
            obj_text = m_obj.group(1).strip(" .;")
            if obj_text:
                entities["objeto"] = obj_text

        # 8. Section 2 Personnel Acts Extraction
        m_acao = RE_PESSOAL_ACAO.search(text)
        if m_acao:
            raw_act = m_acao.group(1).lower().strip()
            if "aposentad" in raw_act:
                act_norm = "APOSENTADORIA"
            elif "dispens" in raw_act:
                act_norm = "DISPENSA"
            elif "pens" in raw_act:
                act_norm = "PENSAO"
            elif "vac" in raw_act:
                act_norm = "VACANCIA"
            else:
                act_norm = PESSOAL_ACTION_MAP.get(raw_act, raw_act.upper())
            entities["tipo_ato_pessoal"] = act_norm

        m_serv = RE_SERVIDOR_NOME.search(text)
        if m_serv:
            clean_serv = m_serv.group(1).strip()
            if clean_serv:
                entities["servidor_nome"] = clean_serv

        m_mat = RE_MATRICULA.search(text)
        if m_mat:
            entities["servidor_matricula"] = m_mat.group(1).strip()

        m_cg_orig = RE_CARGO_ORIGEM.search(text)
        if m_cg_orig:
            entities["cargo_origem"] = m_cg_orig.group(1).strip()

        m_cg_dest = RE_CARGO_DESTINO.search(text)
        if m_cg_dest:
            entities["cargo_destino"] = m_cg_dest.group(1).strip()

        # 9. Batch Discovery & Manual Triage Classification
        has_business_entities = bool(
            entities.get("cnpjs")
            or entities.get("cpfs_masked")
            or entities.get("processos")
            or entities.get("licitacao_modalidade")
            or entities.get("valor_total")
            or entities.get("vigencia_inicio")
            or entities.get("objeto")
            or entities.get("tipo_ato_pessoal")
            or entities.get("servidor_nome")
            or entities.get("cargo_destino")
        )

        if has_business_entities:
            entities["triage_status"] = "EXTRACTED"
            entities["needs_manual_review"] = False
        else:
            entities["triage_status"] = "UNCLASSIFIED_TRILHA_B"
            entities["needs_manual_review"] = True
            entities["triage_sample"] = text[:300].strip()

        return entities
