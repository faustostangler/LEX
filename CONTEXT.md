# LEX — Ingestion, Treatment & Consolidation Bounded Contexts

LEX (Legislação, Extração e Estruturação) ingests, digests, classifies, and exposes Brazilian legislation across Federal, State, and Municipal tiers as clean structured data.

## Ubiquitous Language

**OfficialGazette**:
The periodic official publication of a federative entity containing administrative and normative acts.
_Avoid_: Newspaper, journal, bulletin, periodical.

**GazetteEdition**:
A distinct published issue of an **OfficialGazette** identified by date, territory, and optional edition number or section.
_Avoid_: Edition, issue, paper, document.

**Territory**:
A formal political-administrative jurisdiction in Brazil, uniquely identified by its official IBGE code (e.g., `BR` for Federal, 2-digit for State, 7-digit for Municipality).
_Avoid_: City, place, location, region.

**FederativeTier**:
The administrative jurisdiction level of an **OfficialGazette** or legislative act: Federal (`federal`), State (`state`), or Municipal (`municipal`).
_Avoid_: Level, scope, hierarchy tier.

**EphemeralTextExtraction**:
The streaming transformation of binary payload streams (PDF) into plain structured text in memory (with ephemeral disk spooling fallback for oversized payloads) without saving binary files to persistent storage.
_Avoid_: File caching, binary downloading, local storage.

**SingleSourceOfTruthUrl (SSOT URL)**:
The canonical, external HTTP/HTTPS link to the original publication source of a **GazetteEdition** or **NormativeAct**.
_Avoid_: Link, web address, download link.

**DomainCircuitBreaker**:
An adaptive stability mechanism that temporarily suspends HTTP requests to a failing **Territory** portal when error thresholds are breached, preventing socket exhaustion without halting the whole crawl.
_Avoid_: Error handler, rate limit trip, crash blocker.

**CrawlSession**:
A single bounded execution of an ingestion run for a specific date range or set of **Territory** spiders.
_Avoid_: Batch run, crawl job, task execution.

**RawGazettePayload**:
An untyped, transient Data Transfer Object (DTO) yielded by a spider containing raw web strings, headers, and in-memory byte streams before domain validation.
_Avoid_: Raw item, scrapy item, raw data.

**RawNormativeActPayload**:
An untyped DTO representing an individual discrete legislative/administrative act yielded by a spider before domain normalization.
_Avoid_: Article payload, raw item.

**GazetteMapper**:
An Anti-Corruption Layer (ACL) translator that transforms a **RawGazettePayload** or **RawNormativeActPayload** into strictly validated **GazetteEdition** and **NormativeAct** domain entities with $O(1)$ fast prefix hierarchy resolution.
_Avoid_: Parser, converter, transformer.

**NormativeAct**:
An individual, segmented legislative or administrative rule (e.g., Lei, Decreto, Portaria, Resolução, Extrato) published within a parent **GazetteEdition**.
_Avoid_: Law, rule, item, document, text snippet.

**HierarchicalGroup (Estrato Kelseniano)**:
The eight empirical publication strata grounded in Hans Kelsen's pyramid of norms and Brazilian positive law:
- `Grupo 1`: Atos Primários Constitucionais e Legislativos (CF, EC, LC, Lei Ordinária, MP, Decreto Legislativo).
- `Grupo 2`: Decretos do Chefe do Executivo.
- `Grupo 3`: Atos Normativos Secundários Colegiados e Regulatórios (Resoluções, Deliberações, INs, Provimentos).
- `Grupo 4`: Atos Ordinatórios Ministeriais e Internos (Portarias, Atos Declaratórios).
- `Grupo 5`: Atos Administrativos Decisórios e Regulatórios Concretos (Acórdãos, Decisões, Despachos, Alvarás).
- `Grupo 6`: Instrumentos Editalícios e Convocatórios (Editais, Atos Convocatórios, Atas).
- `Grupo 7`: Instrumentos Contratuais e Convênios (Contratos, Termos Aditivos, Convênios).
- `Grupo 8`: Instrumentos de Publicidade e Operacionais (Extratos, Avisos de Licitação, Resultados, Retificações, Pautas).
_Avoid_: Category, group number, tier enum.

**HierarchicalRank (Peso de Autoridade Normativa)**:
A bounded integer weight $[10, 100]$ enforcing constitutional and LINDB validity rules (*Lex Superior Derogat Inferiori*).
_Avoid_: Level score, rank number.

**PublicationNature**:
The operational classification determining the processing track:
- `normativa_abstrata` / `regulatoria_setorial` $\to$ Dispatches to **Trilha A (Deep AST & Consolidation)**.
- `concreta_individual` / `publicidade_operacional` $\to$ Dispatches to **Trilha B (Fast-Path Entity Extraction / NER)**.
_Avoid_: Category type, tag.

**DualTrackPipeline**:
The architectural separation of processing paths where true general norms undergo full AST parsing and mutation ledgering while high-volume operational/contractual notices undergo fast-path structured NER.
_Avoid_: Parallel processing, dual runners.

**CanonicalUrn**:
The unique, immutable LexML/FRBR uniform resource identifier for a statute (e.g., `urn:lex:br:federal:lei:1993-06-21;8666`).
_Avoid_: System ID, law link, string key.

**CanonicalNodePath**:
The dot-separated hierarchical address of a legislative provision (e.g., `art_3.par_2.inc_14.ali_a`).
_Avoid_: Article path, xpath, css selector.

**NormativeActMutation**:
An atomic, immutable event delta recording a statutory amendment (e.g., `ALTERACAO_NR`, `ACRESCIMO`, `REVOGACAO_EXPRESSA`) targeting a specific **CanonicalNodePath**.
_Avoid_: Law patch, diff item, update row.

**CompiledNormativeAct**:
The materialized read-model projection containing the consolidated AST (JSONB) and pre-rendered LZ4 TOAST HTML/Markdown with strike-through tags and historical notes.
_Avoid_: Final law, merged text, output file.

**StubEntity (Skeleton Entity)**:
A lightweight placeholder record in `normative_acts` (`is_stub = True`) created when an amendment references an older historical statute that has not yet been ingested, preserving relational foreign keys and enqueuing the missing act into the **LegislationBackfillQueue**.
_Avoid_: Phantom record, dummy row, temp law.

**LegislationBackfillQueue**:
A priority-ranked discovery queue tracking uningested historical base statutes, where priority dynamically increments with every citation in modern gazettes.
_Avoid_: Task list, scrape queue.

**DeterministicClassifier**:
A fast, rule-based parsing engine that extracts and categorizes **NormativeAct** attributes via structural regexes, ementa boundaries, and canonical ontology maps.
_Avoid_: Regular expression parser, rule engine, text matcher.

**LexSuperiorValidation**:
A domain invariant enforcing the principle that an act of inferior **HierarchicalRank** cannot modify, suspend, or revoke an act of superior rank, raising a `LexSuperiorViolationError` if violated.
_Avoid_: Rank check, permission validator.

---

## Example Architectural Dialogue

**Architect**: "When the scraper encounters a `PORTARIA` in `secao_1` that modifies a previous regulation, how is it processed?"  
**Engineer**: "The **GazetteMapper** classifies it as `Grupo 4` (Rank 40, `normativa_abstrata`), routing it to **Trilha A**. The **MutationExtractor** identifies the target **CanonicalNodePath** (e.g., `art_2.inc_1`), validates **LexSuperiorValidation** against the target's **HierarchicalRank**, and appends the delta to **NormativeActMutation**."

**Architect**: "And what happens if a modern 2024 gazette amends a 1966 statute not yet in PostgreSQL?"  
**Engineer**: "The repository creates a **StubEntity** with `is_stub = True` under its **CanonicalUrn**, links the mutation via foreign key, and enqueues a priority task in the **LegislationBackfillQueue**. When the historical crawler ingests the 1966 base text, it fires `NormativeActHydrated`, and the **Pure AST Reducer** compiles the entire 58-year mutation history into **CompiledNormativeAct** in under 10 milliseconds."

**Architect**: "And how does the system handle the 70,000 monthly `EXTRATO DE CONTRATO` and `AVISO DE LICITAÇÃO` items?"  
**Engineer**: "The **GazetteMapper** resolves them to `Grupo 8` (Rank 10, `publicidade_operacional`), routing them directly to **Trilha B** for fast regex entity extraction (CNPJ, values, bidding numbers) into `metadata_json` without wasting CPU on AST recursion."
