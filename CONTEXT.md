# LEX — Ingestion Bounded Context

LEX (Legislação, Extração e Estruturação) ingests, digests, and exposes Brazilian legislation across Federal, State, and Municipal tiers as clean structured data.

## Language

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
The canonical, external HTTP/HTTPS link to the original publication source of a **GazetteEdition**.
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

**GazetteMapper**:
An Anti-Corruption Layer (ACL) translator that transforms a **RawGazettePayload** into a strictly validated **GazetteEdition** domain entity.
_Avoid_: Parser, converter, transformer.

**NormativeAct**:
An individual, segmented legislative or administrative rule (e.g., Lei, Decreto, Portaria, Resolução) published within a parent **GazetteEdition**.
_Avoid_: Law, rule, item, document, text snippet.

**NormativeLevel**:
The constitutional and administrative rank of a **NormativeAct** (e.g., `constituicao`, `lei_complementar`, `lei_ordinaria`, `decreto`, `portaria`, `resolucao`).
_Avoid_: Law type, legal rank, hierarchy type.

**ThematicDomain**:
The standardized subject matter classification of a **NormativeAct** (e.g., `health`, `taxation`, `labor`, `transport`, `environment`).
_Avoid_: Category, topic, subject, tag.

**IssuingAuthority**:
The government ministry, regulatory agency, or administrative body that promulgated a **NormativeAct** (e.g., `Presidência da República`, `ANVISA`, `Banco Central`).
_Avoid_: Author, department, issuer, body.

**TemporalStatus**:
The operational legal efficacy state of a **NormativeAct**: `active` (vigente) or `historical` (revogada, exaurida, ou com vigência encerrada).
_Avoid_: Status, legal state, validity condition.

**DeterministicClassifier**:
A fast, rule-based parsing engine that extracts and categorizes **NormativeAct** attributes via structural regexes, ementa boundaries, and canonical ontology maps.
_Avoid_: Regular expression parser, rule engine, text matcher.

**HeuristicFeedbackFlywheel**:
An active learning mechanism where ambiguous cases resolved by the LLM fallback are logged as golden dataset samples to continuously expand and harden the **DeterministicClassifier** in subsequent code revisions.
_Avoid_: Feedback loop, training pipeline, active learning script.

**AmbiguityScore**:
A bounded numeric confidence value $[0.0, 1.0]$ determining whether a segmented act is definitively resolved by the **DeterministicClassifier** or requires LLM fallback.
_Avoid_: Uncertainty level, accuracy, probability score.

## Example Dialogue

**Architect**: "When the spider fetches a new **OfficialGazette**, does it persist the PDF?"
**Engineer**: "No, it performs **EphemeralTextExtraction** to extract raw text and metadata, records the **SingleSourceOfTruthUrl**, and stores the resulting **GazetteEdition** in PostgreSQL."
**Architect**: "And how does the Treatment context digest that container?"
**Engineer**: "The **DeterministicClassifier** segments and classifies standard acts. If an act has a high **AmbiguityScore**, it triggers an LLM fallback, which feeds the **HeuristicFeedbackFlywheel** to improve our deterministic rules in the next release."
**Architect**: "And what happens if a state portal goes down during a **CrawlSession**?"
**Engineer**: "The **DomainCircuitBreaker** opens for that specific domain after consecutive failures, allowing other state spiders to proceed uninterrupted."
**Architect**: "And how do we identify whether it belongs to a city or a state?"
**Engineer**: "Through the **Territory** IBGE code and its **FederativeTier**."
