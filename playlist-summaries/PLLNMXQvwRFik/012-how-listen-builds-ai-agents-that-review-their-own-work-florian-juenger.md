# How Listen builds AI Agents that review their own work | Florian Juengermann, CTO

- **Video:** https://www.youtube.com/watch?v=YTTH-0XXEBE
- **Generated:** 2026-08-31 21:22 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The transcript describes Listen’s agentic research platform and the operating practices behind it. Its central architectural pattern is **LLM-directed orchestration with deterministic execution for scale, governance, and cost control**:

- A primary agent plans analysis and calls high-level tools.
- Deterministic backend workflows handle filtering, fan-out, aggregation, charting, and artifact generation.
- Smaller/cheaper models perform constrained, per-record classification; larger models perform planning, synthesis, and complex reasoning.
- Research data is modeled as a **table of rows and AI-derived columns**, enabling LLM-assisted feature engineering over unstructured interviews, transcripts, and notes.
- Common analytics should use built-in tools; sandboxed Python is a controlled fallback for advanced or unsupported analysis.
- Long-running analysis is separated from low-latency interactive exploration, with different model/reasoning settings and quality/cost trade-offs.
- Outputs can include narrative reports, charts, editable PowerPoint decks, and—in the speaker’s product—video highlight reels.

The strongest enterprise lessons for Superior Propane are:

1. **Use an agent for intent interpretation and workflow selection, not unrestricted execution.**
2. **Keep governed filtering, large-scale classification, aggregation, and metrics in deterministic Databricks/Azure services.**
3. **Use LLMs for qualitative synthesis and constrained extraction, but calculate reported figures through versioned, auditable code or governed semantic metrics.**
4. **Treat prompts, retrieval, models, tools, runtime images, and agent workflows as production software configuration requiring evaluation, telemetry, release controls, and rollback.**
5. **Avoid autonomous write actions, unrestricted Python, static credentials in sandboxes, and ungoverned “agent memory” in early implementations.**

Many implementation statements in the transcript are **speaker/company claims**. The speakers do not provide independent benchmarks, model/provider details, measured accuracy, security attestations, cost figures, or formal evaluation results.

---

# Technical details

## 1. Platform and workflow architecture

Listen describes a multi-agent qualitative research platform with three broad product functions:

- **Composer agent:** assists a human in creating interview/discussion guides.
- **Interview agent:** conducts multimodal interviews, reportedly supporting voice, image, and screen sharing at potentially large parallel scale.
- **Research/analysis agent:** analyzes transcripts and media, producing summaries, charts, clips, and report/deck artifacts.

### Core orchestration model

The most significant design pattern is:

```text
User request
  ↓
Primary/orchestrator LLM
  ↓
One high-level, typed tool call
  ↓
Deterministic backend workflow
  ├─ authorization and filtering
  ├─ parallel worker/model jobs
  ├─ aggregation
  ├─ quality checks
  └─ evidence/provenance capture
  ↓
Results returned to primary agent
  ↓
Narrative response or generated artifact
```

**Speaker claim:** Rather than allowing an LLM to call hundreds of sub-agents directly, one tool call can invoke a hard-coded workflow that fans out to approximately **500 worker agents/jobs**, then aggregates them in a predefined pattern.

This separation is important:

- The LLM handles intent and selects an approved workflow.
- Backend services manage concurrency, retries, rate limits, data access, aggregation, and cost controls.
- High-volume work is not left to unconstrained agent loops.

For Superior Propane, this pattern is preferable to an agent that freely generates SQL/Python, scans broad datasets, or repeatedly invokes models without limits.

---

## 2. Data model: transcripts as analytical tables

Listen’s analysis layer conceptualizes research data primarily as a **table**, rather than as a collection of files:

| Logical concept | Representation |
|---|---|
| Interview, response, transcript | Row |
| Question, source field, extracted attribute | Column |
| AI-generated classification/summary | Derived column |
| Per-record inference result | Cell value |

Example:

```text
Source transcript row
  → classifier / constrained LLM call
  → derived fields:
      - topic
      - sentiment
      - escalation indicator
      - resolution status
      - summary
      - safety/theme category
```

The agent can create new derived columns and populate them over the corpus. This is effectively **LLM-assisted feature engineering** for unstructured data.

### Map/reduce-style classification

For questions such as “How many interviews mention X?”, the platform reportedly uses smaller models—examples named include “GPT mini” and “Haiku”—to perform constrained work across each record.

```text
Map:
  classify each transcript / note / response

Reduce:
  aggregate classifications, counts, trends, and evidence
```

The speaker characterizes these calls as “sub-agents,” but clarifies that many are simply constrained LLM inference calls rather than autonomous planning agents.

**Speaker claim:** This can produce robust quantitative insights from open-ended conversations.

That is plausible only when classification taxonomy, prompt design, model selection, data quality, and validation are strong. It is not an inherent guarantee of LLM-based classification.

### Superior Propane implication

This pattern is highly relevant to:

- Contact-centre transcripts and customer feedback
- Technician and field-service notes
- Delivery exception narratives
- Safety observations, incidents, and near misses
- Dispatch comments and work-order notes
- Employee surveys and operational retrospectives

A suitable Databricks implementation would store source records and derived features in Delta tables, preserving:

- Source record ID and version
- Prompt/template and taxonomy version
- Model deployment/version
- Run ID and timestamp
- Output value and evidence excerpt
- Confidence/validation status
- Error/retry state

---

## 3. Live versus asynchronous processing

The platform reportedly uses broadly the same architecture for both interactive exploration and long-running report generation, with different model settings and execution choices.

| Workload | Described behavior | Trade-off |
|---|---|---|
| Live / interactive | Smaller/faster models; low reasoning settings; may subsample | Lower latency, but potentially incomplete or less rigorous results |
| Asynchronous / long-running | More capable models; medium-to-higher reasoning; can inspect more/all records | Better quality/completeness, but higher latency and cost |
| Final analysis | Full rerun at study completion or after inactivity | More coherent final insight, but expensive and slow |

**Speaker claim:** Long-running research analysis can take roughly **30 minutes**. Full analysis is reportedly triggered at thresholds such as 10, 20, and 100 responses rather than after every new response. A final rerun may occur when collection finishes or after approximately two days without new responses.

### Important design lesson: narrative versus metrics

The transcript describes a useful separation:

```text
LLM:
  qualitative interpretation, themes, narrative, metric placeholders

Deterministic code/classification:
  counts, percentages, charts, supporting records
```

Rather than allowing an LLM to state a percentage directly, the LLM should generate a placeholder that resolves to a governed metric.

Example:

```text
Narrative:
"Delivery scheduling was a frequent concern, affecting {{delivery_scheduling_complaint_pct}} of analyzed contacts."

Metric:
Calculated from a governed, versioned classification and aggregation pipeline.
```

Benefits:

- Prevents free-form numeric hallucination.
- Supports drill-through from metrics to source records.
- Enables fast metric refresh without rerunning expensive reasoning.
- Makes executive reporting more auditable.

Limitation acknowledged by the speaker: if metrics materially change, simply refreshing a number is insufficient. The narrative, recommendation, and conclusion may need a full regeneration or human review.

### Superior Propane implication

For dashboards, executive reporting, service insight, safety review, or commercial analysis:

- Use Databricks/semantic-layer calculations for all reported KPIs and percentages.
- Permit an LLM to explain metrics and produce narrative only with citations to those metrics.
- Label reports clearly as:
  - **Provisional / directional**
  - **Metrics refreshed; narrative pending review**
  - **Finalized**

---

## 4. Tool design and server-side filtering

The speakers describe an evolution from broad analysis followed by code-based filtering to explicit filter parameters in tool contracts.

### Earlier approach

1. Analyze the entire dataset.
2. Return results.
3. Generate Python to filter afterward.

### Revised approach

Pass approved parameters into a tool, such as:

- `filter_column`
- equality value
- likely date/segment-related constraints

**Speaker claim:** Simple `column = value` filtering handles roughly **90%** of their cases; complex combinations may still require Python.

This is a strong enterprise design principle. Filtering should happen before retrieval, classification, or fan-out.

### Recommended Superior Propane tool pattern

Avoid open-ended data access. Use typed, parameterized tools such as:

- `get_delivery_exception_summary(region, date_range, exception_type)`
- `classify_service_notes(region, date_range, work_order_type)`
- `summarize_contact_centre_themes(queue, date_range, issue_category)`
- `analyze_safety_observations(branch, inspection_period, severity_band)`

Tool contracts should enforce:

- Approved dataset and metric scope
- Required filters and maximum date ranges
- User and application entitlement checks
- Row-count and cost limits
- Allowed dimensions and operators
- Read-only access by default
- Evidence/provenance output requirements

For complex filtering, prefer an approved query DSL or governed semantic layer over arbitrary model-generated Python.

---

## 5. Retrieval, chunking, and scalable corpus analysis

The speakers do not position retrieval as universally necessary. Their described evolution is:

1. Conventional RAG using semantic retrieval plus metadata filtering.
2. A period of processing all available material directly with smaller models.
3. A current hybrid approach retaining retrieval for scale, speed, and cross-study knowledge search.

### Semi-structured document strategy

For interview data, the platform reportedly uses known interview sections and annotations to limit processing to relevant sections. It also uses:

- Chunking
- Semantic retrieval
- Hierarchical summarization
- Targeted extraction over selected chunks

Example scale challenge cited:

- ~1,000 interviews
- ~200-token summary per interview
- ~200,000 tokens before final synthesis

The response is hierarchical summarization:

```text
Raw transcripts
  ↓
Per-interview summaries
  ↓
Thematic/aggregate summaries
  ↓
Final synthesis
```

### Benefits and limitations

| Pattern | Benefit | Risk |
|---|---|---|
| Section filtering | Lower cost and faster analysis | Relevant evidence may exist outside expected section |
| Semantic retrieval | Scales better than full-corpus model scans | Missed evidence / recall failures |
| Hierarchical summaries | Reduces context and synthesis cost | Minority themes, nuance, and uncertainty can disappear |
| Full-corpus analysis | Better completeness | Expensive and slower at scale |

The speaker acknowledges that filtering may miss cases where a participant later contradicts or expands on an earlier response.

### Superior Propane implication

For operational documents, use **hybrid retrieval**:

- Lexical retrieval for exact terms: account IDs, product names, equipment types, safety language, policy numbers.
- Semantic retrieval for themes and paraphrases: dissatisfaction, delivery friction, safety concerns.
- Metadata filtering for region, business unit, date, source type, record classification, and permissions.
- Source-level ACL enforcement before content reaches the model.

For high-stakes questions—safety, regulatory, pricing, customer commitments—provide a full-corpus or escalated-review fallback rather than relying solely on retrieved chunks.

---

## 6. Python, sandboxing, and custom analytics

The platform uses deterministic built-in tools for frequent analytics and visualization requests, with Python as a fallback for the “long tail.”

### Built-in tools first

Examples described:

- Counts of positive/negative responses
- Standard aggregations
- Column charts
- Segmented charts
- Common metrics and visualizations

### Python fallback

For specialized analysis, the agent can invoke a sandboxed Python environment to:

- Perform advanced statistical analysis
- Create custom charts with tools such as Matplotlib
- Calculate derived values
- Generate output artifacts

**Speaker claim:** Python is used in approximately **20%** of long-running default reports. This is product-specific and not independently benchmarked.

### Execution design

The speaker describes:

- Agent runs in application backend.
- Python runs as a tool in a sandbox, reportedly using **E2B** in one implementation.
- A table-like data representation is materialized as a Pandas DataFrame in the sandbox.
- Sandboxes may be pre-warmed to reduce interactive latency.

The speaker also says the logical table is backed by PostgreSQL in their platform, and is effectively a virtual-table abstraction. This does not imply a scalable architecture for large datasets: Pandas materialization can become a bottleneck.

### Superior Propane implementation principle

Keep large-scale joins, filtering, aggregations, and transformations in **Databricks**, not in a Pandas sandbox.

Use Python only for:

- Bounded, curated result sets
- Advanced statistical post-processing
- Custom visual rendering
- Experimentation in isolated, read-only environments

A recommended routing policy:

| Request type | Execution path |
|---|---|
| Standard operational KPI / aggregation | Governed Databricks SQL or semantic metric tool |
| Standard chart | Deterministic chart renderer from validated specification |
| High-volume text classification | Databricks batch job / workflow with controlled model endpoint |
| Advanced but bounded analysis | Restricted Python sandbox |
| Executive report/deck | Template-based artifact renderer with approval workflow |

### Sandbox controls required

A sandbox is not sufficient by itself. Require:

- No static provider or business-system credentials in the runtime
- Restricted or no unrestricted outbound internet access
- Read-only data access by default
- Per-session and per-tenant isolation
- Allowlisted packages and blocked arbitrary installation
- CPU, memory, runtime, file-size, concurrency, and spend limits
- Malware scanning for file inputs/outputs
- Short-lived, scoped identity credentials
- Full execution logging and artifact retention rules
- Explicit deletion of temporary data

---

## 7. Secret brokering and tool gateway pattern

The transcript contains a concrete sandbox credential issue.

**Speaker claim:** A Claude Agent SDK running in an E2B sandbox expected an Anthropic API key in the environment. To avoid exposing the real key, the team used a proxy:

1. Give sandbox a fake key.
2. Sandbox sends a request to a proxy.
3. Proxy validates request legitimacy.
4. Proxy replaces the fake key with the real key server-side.
5. Proxy forwards the request to the model provider.

The speaker calls this workaround “hacky” and reports deployment friction with Render. This is not evidence of a general weakness in any named vendor; it is a specific implementation experience.

### Superior Propane implication

The underlying pattern is sound: **agent runtimes should not receive broadly reusable static secrets.**

Use a managed tool gateway:

```text
Agent / sandbox
  ↓ authenticated request
Tool gateway
  ├─ identity verification
  ├─ authorization
  ├─ schema validation
  ├─ policy/DLP checks
  ├─ rate and spend limits
  ├─ short-lived credential acquisition
  └─ audit logging
  ↓
Approved model endpoint / business API / data service
```

Relevant Azure services to assess:

- Microsoft Entra ID managed identities/workload identity federation
- Azure Key Vault
- Azure API Management
- Private Link and restricted egress networking
- Azure Container Apps, AKS, or Functions for controlled tool execution
- Azure AI Foundry/Azure OpenAI for approved model access

---

## 8. Artifact generation and specialized sub-agents

The platform uses a main agent plus specialized agents/tools to generate artifacts.

### Artifact model

**Speaker claim:** Artifacts may begin as structured tool outputs—such as JSON chart specifications—then be rendered by the application.

Examples described:

- Charts
- Written reports/memos
- Editable PowerPoint decks
- Video highlight reels from interview recordings

This separation is useful:

```text
LLM:
  chooses intent and structured parameters

Tool/service:
  executes approved rendering or generation

Application:
  displays/stores final artifact
```

### PowerPoint generation

The speaker describes a specialized PowerPoint sub-agent:

- Delegated from the main research agent.
- Uses a cloud code-agent SDK.
- Writes and iteratively modifies Python code to create editable PowerPoint files.
- Runs in a separate sandbox.
- Has task-specific instructions/skills.

The original hard-coded PowerPoint workflow reportedly used templates and text/image replacement. The transcript does not fully describe the replacement architecture.

### Recommended Superior Propane approach

For executive or operational reporting:

- Use a structured report/chart specification.
- Generate editable PowerPoint only from approved corporate templates.
- Keep calculations and chart data deterministic.
- Require human approval for leadership, customer-facing, safety, financial, commercial, or regulated outputs.
- Store source-data version, metric definitions, filters, chart spec, template version, and generation timestamp with each deck.

Video highlight reels have **low immediate relevance** to Superior Propane’s core operations. They may be applicable to internal training, employee research, or customer-research programs, but introduce elevated consent, privacy, retention, and selective-quotation risks.

---

## 9. Document co-editing and structured edit operations

The transcript describes a useful design for long-document AI editing.

Rather than rewriting an entire document, the system applies targeted updates using stable element IDs or replacement operations. Human and AI changes share one edit history.

### Described pattern

```text
Document state
  ↓
Human or AI generates structured edit operation
  ↓
Application validates and applies operation
  ↓
Version/history log updated
  ↓
Relevant recent edits included in future AI context
```

Conceptual edit fields:

- operation ID
- actor type: human or AI
- actor ID
- target element ID
- insert/replace/delete/move/format operation
- prior state reference
- new value
- parent document version
- timestamp
- validation/approval status

The schema above is an implementation interpretation; the speaker did not provide a formal data model.

### Benefits

- Avoids rewriting unaffected content.
- Supports undo and comparison.
- Makes human versus AI edits auditable.
- Helps prevent subsequent AI actions from overwriting recent user changes.
- Better suited to long documents than sending full old/new versions to a model.

### Superior Propane relevance

Applicable to internal content such as:

- Training guides
- Customer-service scripts
- SOPs
- Field-service guidance
- Internal policy drafts
- Safety and incident-review templates

For safety, legal, pricing, regulatory, or customer-policy documents, AI should propose edits only. Deterministic application controls and human publishing approval should remain mandatory.

---

## 10. Voice architecture and domain-aware transcription

The speakers prefer a modular voice stack rather than an end-to-end real-time voice model:

```text
Audio
  → speech-to-text
  → high-capability text LLM
  → text-to-speech
  → audio response
```

**Speaker claim:** At the time of their evaluation, real-time voice models were faster but “one or two tiers” less capable than leading text models for nuanced interview reasoning. The speaker acknowledges that real-time models are improving, so this should be benchmarked rather than assumed.

### Voice UX design

For research interviews, the system reportedly:

- Shows a live transcript.
- Prioritizes listening over frequent interruption.
- Avoids treating short pauses as answer completion.
- Allows tangents and long answers because they may contain useful context.

### Transcription correction

The speaker says general transcription can fail on new or domain-specific terms. Their pattern is:

```text
Raw STT transcript
  + interview context
  + expected terminology
  ↓
LLM-based contextual correction/enrichment
```

This could improve recognition of product names, technical terms, and internal vocabulary, but creates a serious risk: an LLM may replace uncertainty with a plausible but incorrect term.

### Superior Propane implication

Voice is most suitable initially for:

- Contact-centre agent assist
- Field-service knowledge retrieval
- Transcription, summarization, and post-call documentation
- Human-led customer interviews
- Internal safety debriefs, with strict escalation controls

Do not begin with an autonomous customer-facing voice agent for emergency, safety, billing, pricing, dispatch, or account-change workflows.

If voice is pursued:

- Preserve raw audio where permitted.
- Preserve raw STT and corrected transcript separately.
- Capture correction confidence and review flags.
- Maintain a governed terminology list for products, assets, locations, and operational/safety terms.
- Define deterministic escalation procedures for gas-leak, odour, fire, or carbon-monoxide statements.
- Benchmark latency, device reliability, word-error rate, entity accuracy, barge-in behavior, and cost.

---

## 11. Evaluation, reviewer agents, and change management

The transcript emphasizes that agent evaluation remains difficult, particularly for long-form answers.

### Reviewer-agent pattern

Listen uses a dedicated reviewer/evaluator agent with constrained context and explicit criteria.

Example criterion:

- Flag report claims that lack supporting citations or data.

The reviewer can be used in two modes:

| Mode | Role |
|---|---|
| Long-running workflow | Review output before delivery; potentially trigger revision |
| Interactive workflow | Evaluate asynchronously after response; capture production quality signals |

This is a useful pattern, but an LLM evaluator is also probabilistic. Fewer evaluator findings do not prove improved quality.

### Current evaluation limitations

**Speaker claim:** The team uses gradual rollout and small manually reviewed test sets—around **20 products/examples**—to catch obvious regressions. They explicitly say they do not believe they have a complete evaluation solution.

This is a smoke-test approach, not sufficient for material enterprise decisions.

### Recommended Superior Propane evaluation stack

Use layered controls:

1. **Deterministic synchronous checks**
   - Authorization and ACL enforcement
   - Required citations/source links
   - Schema/tool-call validation
   - Metric-definition validation
   - Data classification/DLP controls
   - Policy checks for high-risk actions

2. **Model-based asynchronous evaluation**
   - Groundedness
   - Citation support
   - Completeness
   - Tone and policy adherence
   - Failure categorization

3. **Human review**
   - Safety, legal, financial, pricing, customer-impacting, and executive outputs
   - Low-confidence or contradictory results
   - New/unseen failure patterns

4. **Versioned golden datasets**
   - Representative tasks
   - Expected source evidence
   - Known failure cases
   - Prompt-injection examples
   - Regional/seasonal/business-domain edge cases

5. **Production telemetry**
   - User corrections
   - Escalations
   - Tool failures
   - Cost/latency anomalies
   - Grounding incidents
   - Quality by prompt/model/tool version

### Treat all changes as software releases

Changes requiring controlled evaluation include:

- Prompts and organization-level instructions
- Models/model deployments
- Retrieval indexes, chunking, embeddings, and ranking
- Tool schemas and tool behavior
- Taxonomies and classifier prompts
- Sandbox images/packages
- Orchestration logic
- Evaluator prompts and criteria

Use versioning, release rings, regression testing, rollback thresholds, and production monitoring.

---

## 12. Observability, traces, and governed “memory”

### Trace collection

**Speaker claim:** Listen retains all traces but manually reviews approximately **0.01% or less**, focusing on deep inspection of unusual, expensive, failing, or representative runs. Some traces may last ~30 minutes.

This supports a useful operational principle: deep review of selected high-value traces can reveal issues that aggregate dashboards miss.

However, raw trace retention creates cost and privacy risk because traces may contain:

- Prompts
- Retrieved documents
- Tool inputs/outputs
- Customer or employee information
- Generated code
- Agent responses
- Data references and business context

### Recommended trace record

For Superior Propane, log structured operational evidence rather than hidden chain-of-thought:

- Correlation/run ID
- User/application identity and authorization context
- Prompt/configuration version
- Model/deployment version
- Retrieval source IDs and index version
- Tool name, version, parameters, and authorization decision
- Dataset/table identifiers and data watermark
- Token usage, latency, retries, errors, and cost
- Output/artifact references
- Policy decisions
- Human feedback, corrections, escalation outcome

Avoid capturing or exposing hidden reasoning traces unless there is a clear policy-approved reason. Protect raw prompts, tool payloads, and retrieved content as sensitive telemetry.

### “Memory” as governed configuration

The speaker describes organization-level memory as human-defined instructions, such as:

- How projects should be set up
- Analysis conventions
- Report formatting preferences
- Organization-specific context

This is better understood as **versioned, curated configuration**, not autonomous learning.

A key insight from the speakers: the existence of a report or historical insight does not mean it is authoritative, current, relevant, or appropriate for another business unit.

### Superior Propane implication

Start with curated, scoped knowledge:

- Approved business definitions
- Safety and compliance instructions
- Product/service terminology
- Operating procedures
- Escalation criteria
- Business-unit-specific rules
- Authorized knowledge sources

Each memory/instruction item should have:

- Owner
- Scope
- Effective and review/expiry dates
- Version
- Source/reference
- Approval status
- Classification
- Access policy

Do not permit self-writing persistent agent memory until ownership, provenance, access boundaries, review, and lifecycle controls are established.

---

# Potential applications for Superior Propane

## 1. Contact-centre and voice-of-customer intelligence

Use the table-plus-derived-feature model to analyze service calls, surveys, complaints, chats, and retention interactions.

Potential AI-derived fields:

- Reason for contact
- Delivery, billing, scheduling, portal, or service issue
- Resolution status / first-contact resolution
- Sentiment and dissatisfaction theme
- Escalation or churn signal
- Competitor mention
- Account-access or payment-plan issue
- Customer effort indicator
- Safety-related mention requiring review

**Recommended architecture:**

- Curated transcripts and metadata in Databricks Delta tables.
- PII-aware preprocessing and access controls.
- Constrained batch classification jobs for approved taxonomies.
- Governed metrics and dashboards by region, queue, segment, product, and time period.
- LLM-generated qualitative summaries that cite governed metrics and source evidence.

## 2. Technician, delivery, and field-service narrative mining

Apply the same pattern to work-order notes, inspection notes, delivery exceptions, route comments, and maintenance narratives.

Potential use cases:

- Repeat-visit root-cause analysis
- Equipment/part issue categorization
- Customer-access constraints
- Weather/route impacts
- Service follow-up requirements
- Recurring operational friction
- Safety observation detection
- Dispatch-to-field handoff quality

Use classifications for triage and trend detection, not as the sole basis for safety, disciplinary, regulatory, or customer-impacting decisions.

## 3. Safety and incident-review support

AI can assist with organizing and summarizing incident and near-miss narratives:

- Hazard category
- Severity indicator
- Equipment or location type
- Contributing factor
- Corrective-action theme
- Required follow-up
- PII/sensitive-content detection

This should remain **decision support**, with mandatory human validation. It should not autonomously determine incident severity, regulatory reporting, disciplinary action, or safety procedures.

## 4. Governed operational analytics agent

A natural-language agent could support questions such as:

- “What drove delivery exceptions in Ontario this week?”
- “Which service centres have the highest repeat-contact rate?”
- “What complaint themes increased after a process change?”
- “Summarize technician notes associated with repeat visits last month.”

The agent should call approved Databricks-backed tools and return:

- Data range and filters
- Metric definitions
- Record counts
- Source tables/data versions
- Evidence examples
- Confidence or coverage statements
- Report finality/freshness status

## 5. Management reporting and artifact generation

A controlled workflow could create weekly or monthly internal reports covering:

- Delivery volume and service-level trends
- Route or fleet exceptions
- Contact-centre performance
- Customer feedback themes
- Safety or maintenance observations
- Customer retention and service experience

Use deterministic metric services and approved visualization/rendering tools. Generate PowerPoint from corporate templates, with human approval before broad distribution.

## 6. Internal knowledge and procedure assistant

A lower-risk initial use case is an internal assistant over approved operational documentation:

- SOPs
- Customer-service guidance
- Field-service procedures
- IT and data-platform runbooks
- Product/service reference material
- Approved safety and compliance content

Use hybrid search, document ACL enforcement, citations, source status, and escalation for insufficient evidence.

---

# Risks/validation questions

## 1. Data privacy, security, and residency

Superior Propane data may include:

- Customer PII, addresses, and account/service details
- Payment or billing information
- Call recordings and transcript data
- Employee information
- Commercial pricing and contract data
- Safety and operationally sensitive information

Validate:

- Are Azure OpenAI/model endpoints approved for required geography and contractual data handling?
- Is private networking enforced through private endpoints/Private Link where required?
- Are Entra ID, managed identities, Key Vault, RBAC, and least privilege implemented?
- Are raw recordings, raw transcripts, corrected transcripts, source documents, prompts, traces, generated code, and artifacts separately classified?
- Is PII redacted, minimized, tokenized, or access-restricted before model inference?
- Are row-, column-, and document-level controls preserved through retrieval, tools, prompts, and generated outputs?
- What retention, deletion, legal-hold, and incident-response rules apply?

## 2. Prompt injection and tool misuse

Retrieved documents, transcripts, uploaded files, and user requests are potential injection channels.

Required controls:

- Treat retrieved content as data, not instructions.
- Use typed tool schemas and server-side validation.
- Restrict tools by user role and task.
- Apply least-privilege identities per tool/sub-agent.
- Prevent generated code from accessing arbitrary network, filesystem, secrets, or APIs.
- Validate chart/report/artifact specifications before rendering.
- Require approval for external sharing and high-impact outputs.

## 3. Quantitative validity and classification quality

LLM-generated labels can be wrong, inconsistent, or biased.

Validate:

- What taxonomy and label definitions apply?
- What gold-standard human labeling process exists?
- What precision, recall, calibration, and agreement thresholds are required by use case?
- How are ambiguous, multi-topic, multilingual, or low-confidence records represented?
- Are outputs stable across repeated runs and model version changes?
- How are seasonal, regional, and customer-segment differences tested?
- Are counts labeled as model-classified estimates where appropriate?

Deterministic aggregation does not compensate for incorrect upstream classification.

## 4. Generated-code trust and reproducibility

An LLM-generated explanation of Python is not an independent audit mechanism.

For any generated computation, retain:

- Code and code hash
- Input dataset/table IDs and versions
- Query plan or data-access record
- Execution environment identity and image version
- Prompt/model/tool versions
- Parameters and assumptions
- Output values and artifacts
- Validation results
- Reviewer/approver actions

Business users can receive a readable explanation, but technical evidence must remain available under RBAC.

## 5. Retrieval completeness and summarization loss

Filtering, semantic retrieval, and hierarchical summarization can miss evidence or suppress minority views.

Validate:

- What retrieval-recall target is acceptable for each use case?
- Is there a full-corpus fallback for high-stakes questions?
- Are results labeled as based on full population, selected sections, or retrieved evidence?
- Do safety, complaint, and minority themes survive hierarchical compression?
- Are retrieval quality, citation correctness, and missed-evidence rates measured on labeled test sets?

## 6. Cost, scale, and latency

The transcript does not provide cost figures. Likely drivers include:

- Tokens per transcript and report
- Number of derived columns/classifications
- Record volume and reprocessing cadence
- Model routing
- Fan-out/concurrency
- Retrieval and embedding storage
- Python sandbox startup/warm capacity
- Databricks compute and query cost
- Artifact/media generation and storage
- Trace and evaluation retention

Validate:

- Cost per completed interaction, report, classification run, and artifact.
- Maximum permitted fan-out, row count, token count, runtime, and spend per request.
- Whether filters are applied before model calls.
- Caching and incremental processing for unchanged records.
- Queue, retry, dead-letter, timeout, cancellation, and backpressure behavior.
- Cold versus warm sandbox latency and standing cost.
- Whether recurring Python workloads should become deterministic tools.

## 7. Evaluation and release management

A small manually reviewed set is insufficient for business-critical workflows.

Validate:

- What release-blocking quality thresholds exist?
- Who owns sign-off: Product, engineering, SME, data owner, security, safety, or operations?
- Are prompts, models, tools, retrieval configuration, taxonomies, and runtime images versioned?
- Are production metrics segmented by configuration release?
- Are canary, rollback, and emergency-disable processes defined?
- How is evaluator-agent accuracy calibrated against humans?

## 8. Voice-specific risks

Validate:

- Recording consent and legal/privacy requirements.
- Domain terminology accuracy for equipment, locations, names, and safety terms.
- Preservation of raw versus corrected transcripts.
- Escalation for gas leak, odour, fire, carbon-monoxide, or emergency statements.
- Device, microphone, browser, telephony, and network support.
- Accessibility and fallback modes.
- End-to-end latency and unit cost under expected contact-centre/field volume.

---

# Action items

1. **Choose one bounded, low-risk pilot**
   - Preferred candidates:
     - Contact-centre theme classification
     - Technician-note categorization
     - Delivery-exception narrative analysis
     - Internal approved-procedure knowledge assistant
   - Avoid autonomous customer actions, safety decisions, unrestricted Python, video workflows, and external artifact distribution in the first release.

2. **Define a reference architecture**
   - Azure AI Foundry/Azure OpenAI for model access and orchestration.
   - Databricks for governed Delta tables, scalable batch processing, data quality, and analytics.
   - Unity Catalog for data access, lineage, and governed sharing.
   - API-backed tools for approved retrieval, metrics, classification, charts, and document generation.
   - Azure Monitor/Application Insights/OpenTelemetry-compatible instrumentation for operations.
   - Controlled enterprise storage for outputs, reports, and artifacts.

3. **Adopt “governed tools first, code fallback second”**
   - Build deterministic services for common KPIs, filters, classifications, and visualizations.
   - Use typed tool schemas and server-side filtering.
   - Keep large-scale computation in Databricks.
   - Permit sandboxed Python only for bounded, approved advanced analysis.

4. **Implement a governed Delta-table feature schema**
   - Include source record/version, derived value, evidence excerpt, taxonomy/prompt version, model deployment/version, run ID, timestamp, validation status, and error state.
   - Store source, extracted metadata, chunks, embeddings, summaries, and lineage as separate governed artifacts.

5. **Implement the “LLM narrative, deterministic metrics” rule**
   - Prohibit unsourced LLM-generated figures in executive or operational reporting.
   - Require chart/report specifications to reference approved metric IDs and source data versions.
   - Provide drill-through from every material metric to supporting records and calculation definition.

6. **Build evaluation and release controls before production**
   - Create a representative golden set with normal, edge, privacy-sensitive, and prompt-injection cases.
   - Measure tool selection, filter correctness, retrieval recall, classification quality, groundedness, latency, and cost.
   - Require regression evaluation for prompt, model, tool, retrieval, taxonomy, and runtime changes.
   - Define rollback thresholds.

7. **Establish sandbox and tool-gateway security baseline**
   - No standing static credentials in agent runtimes.
   - Managed identity/short-lived credential pattern.
   - Tool gateway with authorization, validation, DLP checks, rate/spend limits, and audit logs.
   - Restricted egress, read-only data access, resource quotas, package allowlists, and secure artifact deletion.

8. **Define trace governance**
   - Establish a minimum trace schema, redaction standards, access controls, and risk-based retention tiers.
   - Retain detailed traces only as long as operationally necessary.
   - Create a regular review cadence for failures, escalations, high-cost sessions, abnormal latency, and policy blocks.
   - Convert findings into regression tests and backlog items.

9. **Create an enterprise knowledge/memory governance model**
   - Treat organization-level “memory” as curated, approved, versioned configuration.
   - Assign owners, scope, review dates, classifications, and access policies.
   - Do not enable self-writing persistent memory without governance and lifecycle controls.

10. **Benchmark voice only if a validated business case exists**
    - Compare modular STT → LLM → TTS against real-time voice options.
    - Evaluate domain accuracy, latency, reliability, consent/privacy, escalation handling, and unit cost.
    - Start with transcription and human-assist workflows rather than autonomous voice agents.

## Full transcript

[00:01] We've been struggling with this for a
[00:01] We've been struggling with this for a bit where we used to have our own
[00:02] bit where we used to have our own
[00:02] bit where we used to have our own hard-coded pipeline. Now we completely
[00:04] hard-coded pipeline. Now we completely
[00:04] hard-coded pipeline. Now we completely rethought it.
[00:04] rethought it.
[00:04] rethought it. &gt;&gt; Today, I'm talking to Florian Ungermann,
[00:06] &gt;&gt; Today, I'm talking to Florian Ungermann,
[00:06] &gt;&gt; Today, I'm talking to Florian Ungermann, co-founder and CTO of Listen. They're
[00:08] co-founder and CTO of Listen. They're
[00:09] co-founder and CTO of Listen. They're known for their agents that can analyze
[00:10] known for their agents that can analyze
[00:10] known for their agents that can analyze hundreds of interviews, surveys, and
[00:12] hundreds of interviews, surveys, and
[00:13] hundreds of interviews, surveys, and focus group feedback to pull out the
[00:14] focus group feedback to pull out the
[00:14] focus group feedback to pull out the signal from the noise. Right now, in the
[00:17] signal from the noise. Right now, in the
[00:17] signal from the noise. Right now, in the main agent, it's not directly file
[00:18] main agent, it's not directly file
[00:18] main agent, it's not directly file structure. We think of it more as a
[00:20] structure. We think of it more as a
[00:20] structure. We think of it more as a table. So, the table is every row is a
[00:22] table. So, the table is every row is a
[00:22] table. So, the table is every row is a response, and every column is kind of
[00:24] response, and every column is kind of
[00:24] response, and every column is kind of like a question or a feature that we
[00:26] like a question or a feature that we
[00:26] like a question or a feature that we extract. And then, the agent can
[00:27] extract. And then, the agent can
[00:28] extract. And then, the agent can basically create new columns.
[00:29] basically create new columns.
[00:29] basically create new columns. &gt;&gt; Florian describes how their agent works
[00:30] &gt;&gt; Florian describes how their agent works
[00:30] &gt;&gt; Florian describes how their agent works to put structure to interview responses
[00:33] to put structure to interview responses
[00:33] to put structure to interview responses and gather implicit signal from
[00:34] and gather implicit signal from
[00:34] and gather implicit signal from media-rich user conversations.
[00:36] media-rich user conversations.
[00:36] media-rich user conversations. &gt;&gt; We have been relying more on contextual
[00:39] &gt;&gt; We have been relying more on contextual
[00:39] &gt;&gt; We have been relying more on contextual prompt engineering. There's one feature
[00:41] prompt engineering. There's one feature
[00:41] prompt engineering. There's one feature we have which is emotional understanding
[00:42] we have which is emotional understanding
[00:42] we have which is emotional understanding based on the video and the audio, not
[00:44] based on the video and the audio, not
[00:44] based on the video and the audio, not just the text.
[00:45] just the text.
[00:45] just the text. &gt;&gt; We also go deep into their approach on
[00:47] &gt;&gt; We also go deep into their approach on
[00:47] &gt;&gt; We also go deep into their approach on quality control for the end report the
[00:49] quality control for the end report the
[00:49] quality control for the end report the agent writes and their eval system to
[00:51] agent writes and their eval system to
[00:51] agent writes and their eval system to ensure accuracy. Basically, we have this
[00:53] ensure accuracy. Basically, we have this
[00:53] ensure accuracy. Basically, we have this sub-agent which is this reviewer agent
[00:55] sub-agent which is this reviewer agent
[00:55] sub-agent which is this reviewer agent that just knows what a good report looks
[00:57] that just knows what a good report looks
[00:57] that just knows what a good report looks like. So, that's what we run it using
[00:58] like. So, that's what we run it using
[00:58] like. So, that's what we run it using the asynchronous runner. And then, in
[01:01] the asynchronous runner. And then, in
[01:01] the asynchronous runner. And then, in the live runner, we use it as an
[01:02] the live runner, we use it as an
[01:02] the live runner, we use it as an evaluation system. Listen has figured
[01:04] evaluation system. Listen has figured
[01:04] evaluation system. Listen has figured out how to run agents at scale, solving
[01:06] out how to run agents at scale, solving
[01:06] out how to run agents at scale, solving some tricky problems on breaking up
[01:08] some tricky problems on breaking up
[01:08] some tricky problems on breaking up tasks so that they can be massively
[01:09] tasks so that they can be massively
[01:10] tasks so that they can be massively parallelized.
[01:10] parallelized.
[01:10] parallelized. &gt;&gt; We have this hard-coded workflow. If you
[01:12] &gt;&gt; We have this hard-coded workflow. If you
[01:12] &gt;&gt; We have this hard-coded workflow. If you call this tool once, we spawn those 500
[01:14] call this tool once, we spawn those 500
[01:14] call this tool once, we spawn those 500 agents, and then we aggregate in a very
[01:15] agents, and then we aggregate in a very
[01:15] agents, and then we aggregate in a very specific way, and then it returns it.
[01:17] specific way, and then it returns it.
[01:17] specific way, and then it returns it. &gt;&gt; Welcome to Max Agency, the podcast that
[01:19] &gt;&gt; Welcome to Max Agency, the podcast that
[01:19] &gt;&gt; Welcome to Max Agency, the podcast that goes deep into how the best agents are
[01:21] goes deep into how the best agents are
[01:21] goes deep into how the best agents are being built by builders like you.
[01:28] At Listen, you guys actually have a
[01:28] At Listen, you guys actually have a bunch of agents that make up your
[01:30] bunch of agents that make up your
[01:30] bunch of agents that make up your platform. Would you mind talking about
[01:31] platform. Would you mind talking about
[01:31] platform. Would you mind talking about the different agents you have and what
[01:32] the different agents you have and what
[01:32] the different agents you have and what they do and how the user interacts and
[01:34] they do and how the user interacts and
[01:34] they do and how the user interacts and sees them? So, I think our platform is
[01:36] sees them? So, I think our platform is
[01:36] sees them? So, I think our platform is pretty broad. There's a lot of use
[01:38] pretty broad. There's a lot of use
[01:38] pretty broad. There's a lot of use cases, and everything is now agent
[01:39] cases, and everything is now agent
[01:39] cases, and everything is now agent first. The first step is you actually
[01:41] first. The first step is you actually
[01:41] first. The first step is you actually create your product, you create a study.
[01:43] create your product, you create a study.
[01:43] create your product, you create a study. Then we have this agent that is, you
[01:45] Then we have this agent that is, you
[01:45] Then we have this agent that is, you know, this interactive creation agent
[01:47] know, this interactive creation agent
[01:47] know, this interactive creation agent that, you know, we call composer. And it
[01:49] that, you know, we call composer. And it
[01:49] that, you know, we call composer. And it really works with a artifact on the
[01:51] really works with a artifact on the
[01:51] really works with a artifact on the side. It can modify this, but it's
[01:53] side. It can modify this, but it's
[01:53] side. It can modify this, but it's really like human and AI interacting on
[01:55] really like human and AI interacting on
[01:55] really like human and AI interacting on the same documents. There's some very
[01:56] the same documents. There's some very
[01:56] the same documents. There's some very interesting research challenges there.
[01:57] interesting research challenges there.
[01:57] interesting research challenges there. &gt;&gt; artifact on the side?
[01:59] &gt;&gt; artifact on the side?
[01:59] &gt;&gt; artifact on the side? &gt;&gt; So the artifact is your discussion
[02:00] &gt;&gt; So the artifact is your discussion
[02:00] &gt;&gt; So the artifact is your discussion guide, which will kind of be Those are
[02:02] guide, which will kind of be Those are
[02:02] guide, which will kind of be Those are the questions we will ask in the
[02:03] the questions we will ask in the
[02:03] the questions we will ask in the interview.
[02:04] interview.
[02:05] interview. And this then actually goes as an input
[02:07] And this then actually goes as an input
[02:07] And this then actually goes as an input to the next agent where she does the
[02:08] to the next agent where she does the
[02:08] to the next agent where she does the interview. So this is the the AI that
[02:10] interview. So this is the the AI that
[02:10] interview. So this is the the AI that has a conversation with our interviewee
[02:12] has a conversation with our interviewee
[02:12] has a conversation with our interviewee and goes back and forth. And you'll do
[02:13] and goes back and forth. And you'll do
[02:13] and goes back and forth. And you'll do this with like thousands of candidates
[02:16] this with like thousands of candidates
[02:16] this with like thousands of candidates or So yeah, so not not necessarily
[02:18] or So yeah, so not not necessarily
[02:18] or So yeah, so not not necessarily candidates. It's more users or customers
[02:22] candidates. It's more users or customers
[02:22] candidates. It's more users or customers we'll talk to talk to hundreds or
[02:23] we'll talk to talk to hundreds or
[02:23] we'll talk to talk to hundreds or thousands in parallel. And yeah, this
[02:26] thousands in parallel. And yeah, this
[02:26] thousands in parallel. And yeah, this agent it's a little bit less interesting
[02:28] agent it's a little bit less interesting
[02:28] agent it's a little bit less interesting from like a
[02:29] from like a
[02:29] from like a you know, agents building perspective
[02:30] you know, agents building perspective
[02:30] you know, agents building perspective because it doesn't have as many tools.
[02:32] because it doesn't have as many tools.
[02:32] because it doesn't have as many tools. It's more like a regular conversation.
[02:33] It's more like a regular conversation.
[02:34] It's more like a regular conversation. But it's also like multimodal. It has
[02:35] But it's also like multimodal. It has
[02:35] But it's also like multimodal. It has like image input and you can do screen
[02:37] like image input and you can do screen
[02:37] like image input and you can do screen sharing and those kind of things. Is it
[02:38] sharing and those kind of things. Is it
[02:39] sharing and those kind of things. Is it voice as well or I think it's that's
[02:40] voice as well or I think it's that's
[02:40] voice as well or I think it's that's voice based as well. Yeah.
[02:42] voice based as well. Yeah.
[02:42] voice based as well. Yeah. So so that's that's the second agent and
[02:44] So so that's that's the second agent and
[02:44] So so that's that's the second agent and then the third big step is on the
[02:46] then the third big step is on the
[02:46] then the third big step is on the analysis side and that's I think where
[02:47] analysis side and that's I think where
[02:47] analysis side and that's I think where we spend most of our time so far. It's
[02:49] we spend most of our time so far. It's
[02:49] we spend most of our time so far. It's building this what we call research
[02:50] building this what we call research
[02:50] building this what we call research agent.
[02:51] agent.
[02:51] agent. And that's really like imagine you have
[02:53] And that's really like imagine you have
[02:53] And that's really like imagine you have you've done, you know, 500 interviews
[02:55] you've done, you know, 500 interviews
[02:55] you've done, you know, 500 interviews now and those exist like you have the
[02:57] now and those exist like you have the
[02:57] now and those exist like you have the transcripts of the videos. But now you
[02:59] transcripts of the videos. But now you
[02:59] transcripts of the videos. But now you want to explore the data. You have
[03:00] want to explore the data. You have
[03:00] want to explore the data. You have questions about it. You can ask and this
[03:02] questions about it. You can ask and this
[03:02] questions about it. You can ask and this research agent is really powerful. It
[03:04] research agent is really powerful. It
[03:04] research agent is really powerful. It can create everything from, you know,
[03:06] can create everything from, you know,
[03:06] can create everything from, you know, charts. It can, you know, obviously
[03:07] charts. It can, you know, obviously
[03:07] charts. It can, you know, obviously summarize things. It can even like cut
[03:09] summarize things. It can even like cut
[03:09] summarize things. It can even like cut video clips for you. It can even now
[03:11] video clips for you. It can even now
[03:11] video clips for you. It can even now create PowerPoint slide decks in your
[03:13] create PowerPoint slide decks in your
[03:13] create PowerPoint slide decks in your own company template. And that's I think
[03:15] own company template. And that's I think
[03:15] own company template. And that's I think where we spend most of our time so far.
[03:16] where we spend most of our time so far.
[03:16] where we spend most of our time so far. Okay, so let's let's focus on that
[03:18] Okay, so let's let's focus on that
[03:18] Okay, so let's let's focus on that agent. So how do people interact with
[03:20] agent. So how do people interact with
[03:20] agent. So how do people interact with this? Do they chat with it? Is there
[03:22] this? Do they chat with it? Is there
[03:22] this? Do they chat with it? Is there some big background job that runs off
[03:25] some big background job that runs off
[03:25] some big background job that runs off after all of these and how many
[03:26] after all of these and how many
[03:26] after all of these and how many interviews are there? You said 500. Is
[03:27] interviews are there? You said 500. Is
[03:27] interviews are there? You said 500. Is that a typical amount? Do you see
[03:29] that a typical amount? Do you see
[03:29] that a typical amount? Do you see hundreds of thousands? Yeah, so in
[03:31] hundreds of thousands? Yeah, so in
[03:31] hundreds of thousands? Yeah, so in direction it's both. It is the you know,
[03:34] direction it's both. It is the you know,
[03:34] direction it's both. It is the you know, we do run like one analysis run up front
[03:37] we do run like one analysis run up front
[03:37] we do run like one analysis run up front and that can take like 30 minutes. Like
[03:38] and that can take like 30 minutes. Like
[03:39] and that can take like 30 minutes. Like we we use the same agent architecture
[03:40] we we use the same agent architecture
[03:40] we we use the same agent architecture for that as for the live interaction
[03:43] for that as for the live interaction
[03:43] for that as for the live interaction chat. There's some different parameters
[03:44] chat. There's some different parameters
[03:44] chat. There's some different parameters where you want to optimize for latency
[03:46] where you want to optimize for latency
[03:46] where you want to optimize for latency versus
[03:47] versus
[03:47] versus um, you know, just quality. What are
[03:49] um, you know, just quality. What are
[03:49] um, you know, just quality. What are those different parameters? Yeah, I mean
[03:50] those different parameters? Yeah, I mean
[03:50] those different parameters? Yeah, I mean sometimes we use different models. So,
[03:52] sometimes we use different models. So,
[03:52] sometimes we use different models. So, for some like live calls, we use like
[03:54] for some like live calls, we use like
[03:54] for some like live calls, we use like faster, smaller models, or we tune
[03:56] faster, smaller models, or we tune
[03:56] faster, smaller models, or we tune thinking parameters. So, you know, in
[03:59] thinking parameters. So, you know, in
[03:59] thinking parameters. So, you know, in the live run, we have like minimal
[04:00] the live run, we have like minimal
[04:00] the live run, we have like minimal thinking, whereas in the long run, we
[04:02] thinking, whereas in the long run, we
[04:02] thinking, whereas in the long run, we have like
[04:03] have like
[04:03] have like medium or even more thinking. And then
[04:04] medium or even more thinking. And then
[04:04] medium or even more thinking. And then there's some There's some things of like
[04:06] there's some There's some things of like
[04:06] there's some There's some things of like if you have more than 500, you have like
[04:08] if you have more than 500, you have like
[04:08] if you have more than 500, you have like thousands of interviews,
[04:09] thousands of interviews,
[04:09] thousands of interviews, you know, you can't always look at all
[04:11] you know, you can't always look at all
[04:11] you know, you can't always look at all of the interviews live because, you
[04:13] of the interviews live because, you
[04:13] of the interviews live because, you know, rate limits and and so on. Even if
[04:14] know, rate limits and and so on. Even if
[04:14] know, rate limits and and so on. Even if you spawn a lot of sub-agents, there's
[04:16] you spawn a lot of sub-agents, there's
[04:16] you spawn a lot of sub-agents, there's some limits to that. Whereas in the
[04:18] some limits to that. Whereas in the
[04:18] some limits to that. Whereas in the asynchronous workflow, you can actually
[04:19] asynchronous workflow, you can actually
[04:19] asynchronous workflow, you can actually look at most of them. So, then we're
[04:20] look at most of them. So, then we're
[04:20] look at most of them. So, then we're doing some things like maybe we just
[04:21] doing some things like maybe we just
[04:21] doing some things like maybe we just sub-sample some and we show you some
[04:23] sub-sample some and we show you some
[04:23] sub-sample some and we show you some results earlier. So, there's some slight
[04:25] results earlier. So, there's some slight
[04:25] results earlier. So, there's some slight differences, but the same architecture,
[04:27] differences, but the same architecture,
[04:27] differences, but the same architecture, um the same kind of agent tools overall
[04:29] um the same kind of agent tools overall
[04:29] um the same kind of agent tools overall for both of those tasks. And for the
[04:31] for both of those tasks. And for the
[04:31] for both of those tasks. And for the asynchronous run, like how do you decide
[04:33] asynchronous run, like how do you decide
[04:33] asynchronous run, like how do you decide what to kick it off with? Will the user
[04:36] what to kick it off with? Will the user
[04:36] what to kick it off with? Will the user set that ahead of time, or is that a
[04:37] set that ahead of time, or is that a
[04:37] set that ahead of time, or is that a standard template that you guys have
[04:39] standard template that you guys have
[04:39] standard template that you guys have that you run? Yeah, we know kind of what
[04:41] that you run? Yeah, we know kind of what
[04:41] that you run? Yeah, we know kind of what works best. So, there's a there's a
[04:42] works best. So, there's a there's a
[04:42] works best. So, there's a there's a standard template to it, but it's also
[04:44] standard template to it, but it's also
[04:44] standard template to it, but it's also something you can customize on your kind
[04:46] something you can customize on your kind
[04:46] something you can customize on your kind of organization level. So, if you have a
[04:47] of organization level. So, if you have a
[04:47] of organization level. So, if you have a specific format, if you have specific
[04:49] specific format, if you have specific
[04:49] specific format, if you have specific background information, you can input
[04:51] background information, you can input
[04:51] background information, you can input that before, and then it will take that
[04:52] that before, and then it will take that
[04:53] that before, and then it will take that into account. I mean, I think
[04:54] into account. I mean, I think
[04:55] into account. I mean, I think there's like different outputs.
[04:55] there's like different outputs.
[04:55] there's like different outputs. Sometimes you want to have like a long
[04:56] Sometimes you want to have like a long
[04:56] Sometimes you want to have like a long written document, sometimes you want to
[04:57] written document, sometimes you want to
[04:58] written document, sometimes you want to have like multiple documents or multiple
[04:59] have like multiple documents or multiple
[04:59] have like multiple documents or multiple sections for maybe you're have something
[05:01] sections for maybe you're have something
[05:01] sections for maybe you're have something that's multi-
[05:02] that's multi-
[05:02] that's multi- you know, it's like a study that's run
[05:04] you know, it's like a study that's run
[05:04] you know, it's like a study that's run in multi-country, and you want to have
[05:05] in multi-country, and you want to have
[05:05] in multi-country, and you want to have like a comparison between those
[05:07] like a comparison between those
[05:07] like a comparison between those countries. You can specify that up
[05:08] countries. You can specify that up
[05:08] countries. You can specify that up front, and you can have a tailored
[05:09] front, and you can have a tailored
[05:09] front, and you can have a tailored report to you. But again, if you don't
[05:11] report to you. But again, if you don't
[05:11] report to you. But again, if you don't have what you need, you can also just
[05:12] have what you need, you can also just
[05:12] have what you need, you can also just chat with the
[05:13] chat with the
[05:13] chat with the with it after. And how do you specify
[05:15] with it after. And how do you specify
[05:15] with it after. And how do you specify that up front? Is that in natural
[05:17] that up front? Is that in natural
[05:17] that up front? Is that in natural language, or are there some boxes to
[05:19] language, or are there some boxes to
[05:19] language, or are there some boxes to check?
[05:19] check?
[05:19] check? &gt;&gt; It's all natural language. It's all
[05:20] &gt;&gt; It's all natural language. It's all
[05:20] &gt;&gt; It's all natural language. It's all natural language. So, you write
[05:21] natural language. So, you write
[05:21] natural language. So, you write basically a paragraph of, "Hey, I want a
[05:23] basically a paragraph of, "Hey, I want a
[05:24] basically a paragraph of, "Hey, I want a detailed research report. There should
[05:25] detailed research report. There should
[05:25] detailed research report. There should be one for each country." Yeah, exactly.
[05:28] be one for each country." Yeah, exactly.
[05:28] be one for each country." Yeah, exactly. And the AI is really good at
[05:28] And the AI is really good at
[05:29] And the AI is really good at understanding. I mean, we used to have
[05:30] understanding. I mean, we used to have
[05:30] understanding. I mean, we used to have some
[05:31] some
[05:31] some some more rigid things, but I think
[05:32] some more rigid things, but I think
[05:32] some more rigid things, but I think we've all It's all gone to natural
[05:34] we've all It's all gone to natural
[05:34] we've all It's all gone to natural language now. Okay, so what does this
[05:36] language now. Okay, so what does this
[05:36] language now. Okay, so what does this agent look like under the hood? What is
[05:38] agent look like under the hood? What is
[05:38] agent look like under the hood? What is it doing? And if there's differences
[05:40] it doing? And if there's differences
[05:40] it doing? And if there's differences between the live and and the more
[05:42] between the live and and the more
[05:42] between the live and and the more long-running one, maybe let's focus on
[05:43] long-running one, maybe let's focus on
[05:43] long-running one, maybe let's focus on the long-running one specifically, but
[05:45] the long-running one specifically, but
[05:45] the long-running one specifically, but it sounds like they're pretty similar.
[05:46] it sounds like they're pretty similar.
[05:46] it sounds like they're pretty similar. Yeah, you know, um overall they're
[05:48] Yeah, you know, um overall they're
[05:48] Yeah, you know, um overall they're pretty similar. I mean, how does the
[05:49] pretty similar. I mean, how does the
[05:49] pretty similar. I mean, how does the agent work underneath? Um
[05:51] agent work underneath? Um
[05:51] agent work underneath? Um it's actually built our own harness,
[05:52] it's actually built our own harness,
[05:52] it's actually built our own harness, which is something we can talk about.
[05:54] which is something we can talk about.
[05:54] which is something we can talk about. And it basically has access to these,
[05:56] And it basically has access to these,
[05:56] And it basically has access to these, you know, the main level is the
[05:57] you know, the main level is the
[05:57] you know, the main level is the transcripts of these 500 conversations.
[05:59] transcripts of these 500 conversations.
[05:59] transcripts of these 500 conversations. And then the goal is to you know, really
[06:01] And then the goal is to you know, really
[06:01] And then the goal is to you know, really make that understandable. And it has,
[06:05] make that understandable. And it has,
[06:05] make that understandable. And it has, you know, a bunch of different tools.
[06:06] you know, a bunch of different tools.
[06:06] you know, a bunch of different tools. We're in this interesting domain where
[06:08] We're in this interesting domain where
[06:08] We're in this interesting domain where it's not infeasible to look at all of
[06:10] it's not infeasible to look at all of
[06:10] it's not infeasible to look at all of these individual interviews again. At
[06:12] these individual interviews again. At
[06:12] these individual interviews again. At least with like cheap LLM. We're not in
[06:14] least with like cheap LLM. We're not in
[06:14] least with like cheap LLM. We're not in like the millions of conversations where
[06:16] like the millions of conversations where
[06:16] like the millions of conversations where that's infeasible. So, we have some
[06:17] that's infeasible. So, we have some
[06:17] that's infeasible. So, we have some tools that can do like a, you know, more
[06:19] tools that can do like a, you know, more
[06:19] tools that can do like a, you know, more recursive summarization or even like
[06:22] recursive summarization or even like
[06:22] recursive summarization or even like classification of like, okay, if you
[06:24] classification of like, okay, if you
[06:24] classification of like, okay, if you want to know how many interviews mention
[06:26] want to know how many interviews mention
[06:26] want to know how many interviews mention a specific thing, we can actually look
[06:27] a specific thing, we can actually look
[06:28] a specific thing, we can actually look have a small model, you know, GPT mini
[06:29] have a small model, you know, GPT mini
[06:29] have a small model, you know, GPT mini or uh Haiku or something similar. They
[06:32] or uh Haiku or something similar. They
[06:32] or uh Haiku or something similar. They should look at all the interviews,
[06:34] should look at all the interviews,
[06:34] should look at all the interviews, classify it, and then you actually get
[06:35] classify it, and then you actually get
[06:35] classify it, and then you actually get robust quantitative data out of these
[06:37] robust quantitative data out of these
[06:37] robust quantitative data out of these like very open-end conversations. So,
[06:39] like very open-end conversations. So,
[06:39] like very open-end conversations. So, how are these files or how are these
[06:41] how are these files or how are these
[06:41] how are these files or how are these interviews presented to the LLM, to the
[06:43] interviews presented to the LLM, to the
[06:43] interviews presented to the LLM, to the agent? Are they presented as files? Are
[06:45] agent? Are they presented as files? Are
[06:45] agent? Are they presented as files? Are they presented as variables in some
[06:47] they presented as variables in some
[06:47] they presented as variables in some programmatic environment? Yeah, so we've
[06:50] programmatic environment? Yeah, so we've
[06:50] programmatic environment? Yeah, so we've been iterating a little bit on that and
[06:52] been iterating a little bit on that and
[06:52] been iterating a little bit on that and we're, you know, constantly thinking
[06:53] we're, you know, constantly thinking
[06:53] we're, you know, constantly thinking about if we should change it to more
[06:54] about if we should change it to more
[06:54] about if we should change it to more file structure. Right now in the main
[06:56] file structure. Right now in the main
[06:56] file structure. Right now in the main agent, it's it's not directly file
[06:58] agent, it's it's not directly file
[06:58] agent, it's it's not directly file structure. It's more we think of it more
[06:59] structure. It's more we think of it more
[06:59] structure. It's more we think of it more as a table. So, the table is every row
[07:02] as a table. So, the table is every row
[07:02] as a table. So, the table is every row is a response it's a it's a response.
[07:05] is a response it's a it's a response.
[07:05] is a response it's a it's a response. And every column is kind of like a
[07:06] And every column is kind of like a
[07:06] And every column is kind of like a question or a feature that we extract.
[07:09] question or a feature that we extract.
[07:09] question or a feature that we extract. And then the agent can basically create
[07:10] And then the agent can basically create
[07:10] And then the agent can basically create new columns. So, it can say something
[07:12] new columns. So, it can say something
[07:12] new columns. So, it can say something like, you know, what is the user
[07:13] like, you know, what is the user
[07:13] like, you know, what is the user sentiment towards the specific topic.
[07:15] sentiment towards the specific topic.
[07:15] sentiment towards the specific topic. And then please could be like an
[07:17] And then please could be like an
[07:17] And then please could be like an open-ended like summary of this the user
[07:19] open-ended like summary of this the user
[07:19] open-ended like summary of this the user sentiment or could be a categorical
[07:21] sentiment or could be a categorical
[07:21] sentiment or could be a categorical value like, you know, positive,
[07:22] value like, you know, positive,
[07:22] value like, you know, positive, negative, neutral. And then it will
[07:24] negative, neutral. And then it will
[07:24] negative, neutral. And then it will basically add this column into this,
[07:26] basically add this column into this,
[07:26] basically add this column into this, you know, table and you know, fill in
[07:28] you know, table and you know, fill in
[07:28] you know, table and you know, fill in the values for each one of them. And
[07:29] the values for each one of them. And
[07:29] the values for each one of them. And then you can use things like Python or
[07:32] then you can use things like Python or
[07:32] then you can use things like Python or things like, you know, like to to chart
[07:33] things like, you know, like to to chart
[07:34] things like, you know, like to to chart the data basically based on that. Super
[07:35] the data basically based on that. Super
[07:35] the data basically based on that. Super interesting. And so and and when it
[07:37] interesting. And so and and when it
[07:37] interesting. And so and and when it fills in the values for each row, it
[07:39] fills in the values for each row, it
[07:39] fills in the values for each row, it kicks off basically a small sub-agent or
[07:41] kicks off basically a small sub-agent or
[07:41] kicks off basically a small sub-agent or a small Are are those small LLM, small
[07:44] a small Are are those small LLM, small
[07:44] a small Are are those small LLM, small sub agent, are those the same things?
[07:45] sub agent, are those the same things?
[07:45] sub agent, are those the same things? Yeah, you could call it a sub agent, but
[07:47] Yeah, you could call it a sub agent, but
[07:47] Yeah, you could call it a sub agent, but it's really like a very constrained
[07:49] it's really like a very constrained
[07:49] it's really like a very constrained agent. It doesn't have to have, you
[07:50] agent. It doesn't have to have, you
[07:50] agent. It doesn't have to have, you know, room to decide what to do. It just
[07:52] know, room to decide what to do. It just
[07:52] know, room to decide what to do. It just does like a close classification call.
[07:54] does like a close classification call.
[07:54] does like a close classification call. So, that's one of the tools it have is
[07:55] So, that's one of the tools it have is
[07:55] So, that's one of the tools it have is basically like this
[07:56] basically like this
[07:56] basically like this you can think of it more as like a map
[07:57] you can think of it more as like a map
[07:57] you can think of it more as like a map produce call. I mean, there's something
[07:59] produce call. I mean, there's something
[07:59] produce call. I mean, there's something that that we have hardcoded as one of
[08:01] that that we have hardcoded as one of
[08:01] that that we have hardcoded as one of the as one of the tools. Yeah. So, you
[08:03] the as one of the tools. Yeah. So, you
[08:03] the as one of the tools. Yeah. So, you can call it a sub agent or you can call
[08:04] can call it a sub agent or you can call
[08:04] can call it a sub agent or you can call it just LLM. So, it's got this table.
[08:07] it just LLM. So, it's got this table.
[08:07] it just LLM. So, it's got this table. It's got a row for each of the
[08:09] It's got a row for each of the
[08:09] It's got a row for each of the transcripts each of the interviews. It
[08:11] transcripts each of the interviews. It
[08:11] transcripts each of the interviews. It it creates different columns. You
[08:12] it creates different columns. You
[08:12] it creates different columns. You mentioned like Python or plotting
[08:14] mentioned like Python or plotting
[08:14] mentioned like Python or plotting things. Like does it also have access to
[08:16] things. Like does it also have access to
[08:16] things. Like does it also have access to code? Can it write code? So, by So, by
[08:17] code? Can it write code? So, by So, by
[08:18] code? Can it write code? So, by So, by default we give it some Let's say you
[08:20] default we give it some Let's say you
[08:20] default we give it some Let's say you call this, you know, this classification
[08:22] call this, you know, this classification
[08:22] call this, you know, this classification tool like with the sentiment, right? And
[08:24] tool like with the sentiment, right? And
[08:24] tool like with the sentiment, right? And by default this tool actually returns a
[08:26] by default this tool actually returns a
[08:26] by default this tool actually returns a statistic on,
[08:28] statistic on,
[08:28] statistic on, you know, out of the 500
[08:30] you know, out of the 500
[08:30] you know, out of the 500 interviews you did, 325 were positive,
[08:32] interviews you did, 325 were positive,
[08:32] interviews you did, 325 were positive, you know, 100 were, you know, it returns
[08:35] you know, 100 were, you know, it returns
[08:35] you know, 100 were, you know, it returns some default values that you can then
[08:36] some default values that you can then
[08:36] some default values that you can then use and give an give the answer. Most of
[08:37] use and give an give the answer. Most of
[08:37] use and give an give the answer. Most of the time that's actually enough. Or you
[08:39] the time that's actually enough. Or you
[08:39] the time that's actually enough. Or you can use that. You know, we have some,
[08:40] can use that. You know, we have some,
[08:41] can use that. You know, we have some, you know, sophisticated way of creating
[08:43] you know, sophisticated way of creating
[08:43] you know, sophisticated way of creating charts based on columns. So, you can
[08:44] charts based on columns. So, you can
[08:44] charts based on columns. So, you can say, "Please create a column chart based
[08:47] say, "Please create a column chart based
[08:47] say, "Please create a column chart based on this column or a chart based on this
[08:49] on this column or a chart based on this
[08:49] on this column or a chart based on this column segmented by this column." So, we
[08:50] column segmented by this column." So, we
[08:50] column segmented by this column." So, we have some like logic to create charts
[08:52] have some like logic to create charts
[08:52] have some like logic to create charts and visualizations out of the box. But
[08:54] and visualizations out of the box. But
[08:54] and visualizations out of the box. But then obviously there's like an like a
[08:56] then obviously there's like an like a
[08:56] then obviously there's like an like a long tail of unlimited things people
[08:57] long tail of unlimited things people
[08:57] long tail of unlimited things people would want to do. And that's where the
[08:59] would want to do. And that's where the
[08:59] would want to do. And that's where the Python really comes into play. So, you
[09:00] Python really comes into play. So, you
[09:00] Python really comes into play. So, you can also
[09:02] can also
[09:02] can also write custom Python code. And it's a
[09:03] write custom Python code. And it's a
[09:03] write custom Python code. And it's a little bit, you know, it takes more
[09:05] little bit, you know, it takes more
[09:05] little bit, you know, it takes more duration. It it will not look as nice
[09:07] duration. It it will not look as nice
[09:07] duration. It it will not look as nice because it's not in our UI, but it can
[09:09] because it's not in our UI, but it can
[09:09] because it's not in our UI, but it can do more sophisticated, you know,
[09:11] do more sophisticated, you know,
[09:11] do more sophisticated, you know, statistical analysis, create very custom
[09:13] statistical analysis, create very custom
[09:13] statistical analysis, create very custom chart types that maybe we don't support
[09:15] chart types that maybe we don't support
[09:15] chart types that maybe we don't support in our platform. And then it can put
[09:18] in our platform. And then it can put
[09:18] in our platform. And then it can put either compute values or even create
[09:20] either compute values or even create
[09:20] either compute values or even create specific charts that we then return and
[09:22] specific charts that we then return and
[09:22] specific charts that we then return and show to the user. Second matplotlib or
[09:24] show to the user. Second matplotlib or
[09:24] show to the user. Second matplotlib or something like that. What percent of
[09:26] something like that. What percent of
[09:26] something like that. What percent of queries do you find need this more
[09:28] queries do you find need this more
[09:28] queries do you find need this more open-ended long tail kind of like just
[09:31] open-ended long tail kind of like just
[09:31] open-ended long tail kind of like just raw Python? When we see it using a lot
[09:34] raw Python? When we see it using a lot
[09:34] raw Python? When we see it using a lot of Python, it's sometimes worth to give
[09:36] of Python, it's sometimes worth to give
[09:36] of Python, it's sometimes worth to give it give it a specialized tool to do that
[09:38] it give it a specialized tool to do that
[09:38] it give it a specialized tool to do that task. So, I think the number has been
[09:40] task. So, I think the number has been
[09:40] task. So, I think the number has been going up and down. The long-running
[09:42] going up and down. The long-running
[09:42] going up and down. The long-running default reports, it actually doesn't use
[09:43] default reports, it actually doesn't use
[09:43] default reports, it actually doesn't use Python that often. Maybe in like 20% of
[09:46] Python that often. Maybe in like 20% of
[09:46] Python that often. Maybe in like 20% of the times. So, you would think it's
[09:48] the times. So, you would think it's
[09:48] the times. So, you would think it's maybe not as important, but actually it
[09:49] maybe not as important, but actually it
[09:49] maybe not as important, but actually it is super important even if it's just 20%
[09:51] is super important even if it's just 20%
[09:51] is super important even if it's just 20% of the time because we have this dynamic
[09:52] of the time because we have this dynamic
[09:52] of the time because we have this dynamic engine as well, which is I have a
[09:54] engine as well, which is I have a
[09:54] engine as well, which is I have a specific question and the given tools
[09:56] specific question and the given tools
[09:57] specific question and the given tools don't support that. So, then I fall back
[09:58] don't support that. So, then I fall back
[09:58] don't support that. So, then I fall back to Python and actually run their own
[09:59] to Python and actually run their own
[09:59] to Python and actually run their own analysis and and that's very powerful.
[10:01] analysis and and that's very powerful.
[10:02] analysis and and that's very powerful. So, even if it's not in the majority of
[10:03] So, even if it's not in the majority of
[10:03] So, even if it's not in the majority of cases, it's very powerful to have it so
[10:05] cases, it's very powerful to have it so
[10:05] cases, it's very powerful to have it so you can drill down if you want to.
[10:07] you can drill down if you want to.
[10:07] you can drill down if you want to. &gt;&gt; So, if you're writing this code, does
[10:09] &gt;&gt; So, if you're writing this code, does
[10:09] &gt;&gt; So, if you're writing this code, does this code run in a sandbox? How are How
[10:11] this code run in a sandbox? How are How
[10:11] this code run in a sandbox? How are How are you guys managing that? Yeah, so
[10:12] are you guys managing that? Yeah, so
[10:12] are you guys managing that? Yeah, so this code runs in a sandbox. We're using
[10:14] this code runs in a sandbox. We're using
[10:15] this code runs in a sandbox. We're using um E2B for for execution executing that
[10:17] um E2B for for execution executing that
[10:17] um E2B for for execution executing that code. There's some challenges on kind of
[10:20] code. There's some challenges on kind of
[10:20] code. There's some challenges on kind of making sure we get all the data because
[10:22] making sure we get all the data because
[10:22] making sure we get all the data because it's not tons of data, but it's still
[10:23] it's not tons of data, but it's still
[10:23] it's not tons of data, but it's still like a decent amount of data to, you
[10:25] like a decent amount of data to, you
[10:25] like a decent amount of data to, you know, spin up the sandbox, load the data
[10:27] know, spin up the sandbox, load the data
[10:27] know, spin up the sandbox, load the data fast enough, especially in the live uh
[10:29] fast enough, especially in the live uh
[10:29] fast enough, especially in the live uh live view. So, we do some like
[10:30] live view. So, we do some like
[10:30] live view. So, we do some like pre-warming and like setting up the
[10:32] pre-warming and like setting up the
[10:32] pre-warming and like setting up the sandbox ahead of time and those kind of
[10:33] sandbox ahead of time and those kind of
[10:33] sandbox ahead of time and those kind of things. So, you have the sandbox
[10:35] things. So, you have the sandbox
[10:35] things. So, you have the sandbox separate from the agent. So, the agent's
[10:36] separate from the agent. So, the agent's
[10:36] separate from the agent. So, the agent's kind of like running, doing its own
[10:37] kind of like running, doing its own
[10:37] kind of like running, doing its own stuff. It's got this table-like thing,
[10:40] stuff. It's got this table-like thing,
[10:40] stuff. It's got this table-like thing, which is uh yeah, it actually is that a
[10:42] which is uh yeah, it actually is that a
[10:42] which is uh yeah, it actually is that a real table under the hood? Like is it
[10:44] real table under the hood? Like is it
[10:44] real table under the hood? Like is it &gt;&gt; It's purely like a representation. So, I
[10:48] &gt;&gt; It's purely like a representation. So, I
[10:48] &gt;&gt; It's purely like a representation. So, I think the agent
[10:50] think the agent
[10:50] think the agent we we tell the agent that's a table, but
[10:51] we we tell the agent that's a table, but
[10:51] we we tell the agent that's a table, but you know, in in our database it's
[10:52] you know, in in our database it's
[10:53] you know, in in our database it's actually laid out differently. Uh but
[10:54] actually laid out differently. Uh but
[10:54] actually laid out differently. Uh but you can kind of synthesize it as a
[10:55] you can kind of synthesize it as a
[10:55] you can kind of synthesize it as a table. And then if it actually runs the
[10:57] table. And then if it actually runs the
[10:57] table. And then if it actually runs the Python, then it gets it gets basically
[10:59] Python, then it gets it gets basically
[10:59] Python, then it gets it gets basically gets this Pandas data frame, which is
[11:01] gets this Pandas data frame, which is
[11:01] gets this Pandas data frame, which is basically this table. But it it's never
[11:03] basically this table. But it it's never
[11:03] basically this table. But it it's never stored as like a table like a Since we
[11:05] stored as like a table like a Since we
[11:05] stored as like a table like a Since we fire something, it's just stored in our
[11:06] fire something, it's just stored in our
[11:06] fire something, it's just stored in our Postgres in a different format. Yeah,
[11:08] Postgres in a different format. Yeah,
[11:08] Postgres in a different format. Yeah, we've we've been experimenting with some
[11:09] we've we've been experimenting with some
[11:09] we've we've been experimenting with some stuff like virtual file systems and it
[11:11] stuff like virtual file systems and it
[11:11] stuff like virtual file systems and it seems like this is a virtual table
[11:13] seems like this is a virtual table
[11:13] seems like this is a virtual table basically.
[11:14] basically.
[11:14] basically. &gt;&gt; And so, you've got this agent running,
[11:16] &gt;&gt; And so, you've got this agent running,
[11:16] &gt;&gt; And so, you've got this agent running, it's got this table-like thing, and then
[11:17] it's got this table-like thing, and then
[11:17] it's got this table-like thing, and then it calls this this tool, and then that
[11:19] it calls this this tool, and then that
[11:19] it calls this this tool, and then that spins up a sandbox. So, it's not like
[11:21] spins up a sandbox. So, it's not like
[11:21] spins up a sandbox. So, it's not like the agent's always running in the
[11:22] the agent's always running in the
[11:22] the agent's always running in the sandbox. It's got like a sandbox as a
[11:24] sandbox. It's got like a sandbox as a
[11:24] sandbox. It's got like a sandbox as a tool. And this approach, exactly. So,
[11:26] tool. And this approach, exactly. So,
[11:26] tool. And this approach, exactly. So, So, most of the time
[11:27] So, most of the time
[11:28] So, most of the time it can actually just run on our backend
[11:29] it can actually just run on our backend
[11:29] it can actually just run on our backend and we don't need the sandbox because
[11:30] and we don't need the sandbox because
[11:30] and we don't need the sandbox because it's more hardcoded regular tools and
[11:33] it's more hardcoded regular tools and
[11:33] it's more hardcoded regular tools and then only for for the sake back off
[11:35] then only for for the sake back off
[11:35] then only for for the sake back off initially go to python. We also do have
[11:37] initially go to python. We also do have
[11:37] initially go to python. We also do have some some newer agents or sub agents
[11:39] some some newer agents or sub agents
[11:39] some some newer agents or sub agents that are using the sandbox more natively
[11:41] that are using the sandbox more natively
[11:41] that are using the sandbox more natively and definitely thinking about where is
[11:43] and definitely thinking about where is
[11:43] and definitely thinking about where is the future going? Definitely seems like
[11:45] the future going? Definitely seems like
[11:45] the future going? Definitely seems like the future is going to more, you know,
[11:46] the future is going to more, you know,
[11:46] the future is going to more, you know, agents that have it, you know, are built
[11:48] agents that have it, you know, are built
[11:48] agents that have it, you know, are built based on code and run continuously. So
[11:51] based on code and run continuously. So
[11:51] based on code and run continuously. So it's definitely always something we're
[11:53] it's definitely always something we're
[11:53] it's definitely always something we're experimenting with. What are some of
[11:54] experimenting with. What are some of
[11:54] experimenting with. What are some of those newer sub agents? Yeah, so one
[11:56] those newer sub agents? Yeah, so one
[11:56] those newer sub agents? Yeah, so one thing and we actually just posted a blog
[11:58] thing and we actually just posted a blog
[11:58] thing and we actually just posted a blog post about this is the powerpoint
[12:00] post about this is the powerpoint
[12:00] post about this is the powerpoint generation. So
[12:02] generation. So
[12:02] generation. So we've been working on the, you know,
[12:03] we've been working on the, you know,
[12:03] we've been working on the, you know, again if you guys take a step back, for
[12:05] again if you guys take a step back, for
[12:05] again if you guys take a step back, for our customers often times they the end
[12:07] our customers often times they the end
[12:07] our customers often times they the end result is is often like a powerpoint
[12:08] result is is often like a powerpoint
[12:08] result is is often like a powerpoint slide deck they want to present. And
[12:10] slide deck they want to present. And
[12:10] slide deck they want to present. And powerpoint is like weird format where
[12:13] powerpoint is like weird format where
[12:13] powerpoint is like weird format where it's not
[12:14] it's not
[12:14] it's not you could just create like an HTML like
[12:16] you could just create like an HTML like
[12:16] you could just create like an HTML like react page that looks like slides and
[12:18] react page that looks like slides and
[12:18] react page that looks like slides and then you can create a PDF out of that
[12:20] then you can create a PDF out of that
[12:20] then you can create a PDF out of that and that's great, but you can't really
[12:22] and that's great, but you can't really
[12:22] and that's great, but you can't really edit it. Like our customers can't edit
[12:23] edit it. Like our customers can't edit
[12:23] edit it. Like our customers can't edit it. They want to have something in
[12:24] it. They want to have something in
[12:24] it. They want to have something in powerpoint. So we've been struggling
[12:25] powerpoint. So we've been struggling
[12:26] powerpoint. So we've been struggling with this for a bit where we used to
[12:27] with this for a bit where we used to
[12:27] with this for a bit where we used to have
[12:28] have
[12:28] have our own
[12:29] our own
[12:29] our own hard coded pipeline where we create
[12:30] hard coded pipeline where we create
[12:30] hard coded pipeline where we create templates and then we basically have
[12:32] templates and then we basically have
[12:32] templates and then we basically have like text replace in this powerpoint
[12:33] like text replace in this powerpoint
[12:33] like text replace in this powerpoint slide decks and image replace and and
[12:35] slide decks and image replace and and
[12:35] slide decks and image replace and and you know, find the right templates and
[12:37] you know, find the right templates and
[12:37] you know, find the right templates and and so on. So we used to build that
[12:38] and so on. So we used to build that
[12:38] and so on. So we used to build that pipeline. Now we completely rethought it
[12:40] pipeline. Now we completely rethought it
[12:40] pipeline. Now we completely rethought it as we as we have seen
[12:42] as we as we have seen
[12:42] as we as we have seen the agents being able to
[12:44] the agents being able to
[12:44] the agents being able to use tool calling and especially code
[12:47] use tool calling and especially code
[12:47] use tool calling and especially code code generation to create powerpoint. So
[12:49] code generation to create powerpoint. So
[12:49] code generation to create powerpoint. So basically what we have now is this
[12:51] basically what we have now is this
[12:51] basically what we have now is this cloud code agent SDK that runs and
[12:54] cloud code agent SDK that runs and
[12:54] cloud code agent SDK that runs and writes python code and can then modify
[12:57] writes python code and can then modify
[12:57] writes python code and can then modify the powerpoint file and kind of do a lot
[13:00] the powerpoint file and kind of do a lot
[13:00] the powerpoint file and kind of do a lot of iterations in that. And the way we
[13:01] of iterations in that. And the way we
[13:01] of iterations in that. And the way we implemented it so far is it's a sub
[13:03] implemented it so far is it's a sub
[13:03] implemented it so far is it's a sub agent to our main agent. So the main
[13:05] agent to our main agent. So the main
[13:05] agent to our main agent. So the main agent decides, okay, I want to create a
[13:06] agent decides, okay, I want to create a
[13:06] agent decides, okay, I want to create a slide deck. It should have this content.
[13:09] slide deck. It should have this content.
[13:09] slide deck. It should have this content. It gives all the data and then the sub
[13:10] It gives all the data and then the sub
[13:10] It gives all the data and then the sub agent kind of iterates in the code on
[13:12] agent kind of iterates in the code on
[13:12] agent kind of iterates in the code on the code level with the specific skill
[13:13] the code level with the specific skill
[13:14] the code level with the specific skill of how to how to create a slide and then
[13:16] of how to how to create a slide and then
[13:16] of how to how to create a slide and then returns the powerpoint in the end. And
[13:17] returns the powerpoint in the end. And
[13:17] returns the powerpoint in the end. And that's this agent that
[13:19] that's this agent that
[13:19] that's this agent that actually runs in the
[13:21] actually runs in the
[13:21] actually runs in the in another sandbox. It sounds like
[13:23] in another sandbox. It sounds like
[13:23] in another sandbox. It sounds like definitely the sub agent, maybe the main
[13:25] definitely the sub agent, maybe the main
[13:25] definitely the sub agent, maybe the main agent, they can they can create like
[13:26] agent, they can they can create like
[13:26] agent, they can they can create like artifacts in addition to giving like the
[13:28] artifacts in addition to giving like the
[13:28] artifacts in addition to giving like the final response. How how how does that
[13:30] final response. How how how does that
[13:30] final response. How how how does that work? Yeah, I mean artifact in in some
[13:32] work? Yeah, I mean artifact in in some
[13:32] work? Yeah, I mean artifact in in some ways it's just, you know, JSON output of
[13:34] ways it's just, you know, JSON output of
[13:34] ways it's just, you know, JSON output of a of a specific thing. So, if it's like
[13:36] a of a specific thing. So, if it's like
[13:36] a of a specific thing. So, if it's like the basic artifact we have is a chart,
[13:39] the basic artifact we have is a chart,
[13:39] the basic artifact we have is a chart, which is again in our virtual table, we
[13:41] which is again in our virtual table, we
[13:41] which is again in our virtual table, we basically say create a chart. Like it's
[13:43] basically say create a chart. Like it's
[13:43] basically say create a chart. Like it's just a JSON tool call uh create a chart
[13:45] just a JSON tool call uh create a chart
[13:45] just a JSON tool call uh create a chart with you know, this column and this
[13:47] with you know, this column and this
[13:47] with you know, this column and this column and then we render the chart to
[13:49] column and then we render the chart to
[13:49] column and then we render the chart to the output. There's some other artifacts
[13:51] the output. There's some other artifacts
[13:51] the output. There's some other artifacts you can also create like memos or like
[13:53] you can also create like memos or like
[13:53] you can also create like memos or like you know, like basically like a written
[13:54] you know, like basically like a written
[13:54] you know, like basically like a written output that combines charts, combines
[13:56] output that combines charts, combines
[13:56] output that combines charts, combines other things. Can even create things
[13:58] other things. Can even create things
[13:58] other things. Can even create things like, you know, cut video clips from
[13:59] like, you know, cut video clips from
[13:59] like, you know, cut video clips from those interviews together. You know,
[14:01] those interviews together. You know,
[14:01] those interviews together. You know, based on the transcript it selects these
[14:02] based on the transcript it selects these
[14:03] based on the transcript it selects these are the some interesting quotes. You
[14:04] are the some interesting quotes. You
[14:04] are the some interesting quotes. You have some like retrieval pipeline for
[14:05] have some like retrieval pipeline for
[14:05] have some like retrieval pipeline for that. And then it it wraps that in a
[14:07] that. And then it it wraps that in a
[14:07] that. And then it it wraps that in a specific tool call and then we create
[14:09] specific tool call and then we create
[14:09] specific tool call and then we create this reel and it can reference that in
[14:10] this reel and it can reference that in
[14:10] this reel and it can reference that in the output. And then we render the reel.
[14:12] the output. And then we render the reel.
[14:12] the output. And then we render the reel. You mentioned tools and sub-agents
[14:15] You mentioned tools and sub-agents
[14:15] You mentioned tools and sub-agents already. Do you also use skills? Is that
[14:17] already. Do you also use skills? Is that
[14:17] already. Do you also use skills? Is that a concept that that's made its way into
[14:19] a concept that that's made its way into
[14:19] a concept that that's made its way into these agents yet?
[14:20] these agents yet?
[14:20] these agents yet? &gt;&gt; As you can tell like the really getting
[14:21] &gt;&gt; As you can tell like the really getting
[14:21] &gt;&gt; As you can tell like the really getting into like the longer tail of use cases
[14:24] into like the longer tail of use cases
[14:24] into like the longer tail of use cases where we've been struggling with, you
[14:25] where we've been struggling with, you
[14:25] where we've been struggling with, you know, the models getting smarter and the
[14:27] know, the models getting smarter and the
[14:27] know, the models getting smarter and the prompts are getting longer and
[14:29] prompts are getting longer and
[14:29] prompts are getting longer and that seems to kind of hold the balance,
[14:30] that seems to kind of hold the balance,
[14:30] that seems to kind of hold the balance, but if you want to go into the more
[14:32] but if you want to go into the more
[14:32] but if you want to go into the more detailed rare instances where we know
[14:35] detailed rare instances where we know
[14:35] detailed rare instances where we know this how it's supposed to supposed to
[14:37] this how it's supposed to supposed to
[14:37] this how it's supposed to supposed to work, but the agent maybe doesn't want
[14:39] work, but the agent maybe doesn't want
[14:39] work, but the agent maybe doesn't want to we don't want the agent to reinvent
[14:40] to we don't want the agent to reinvent
[14:40] to we don't want the agent to reinvent it every time, then we're using skill.
[14:42] it every time, then we're using skill.
[14:42] it every time, then we're using skill. Think in this specific instance we
[14:44] Think in this specific instance we
[14:44] Think in this specific instance we haven't used skills that much yet, but
[14:46] haven't used skills that much yet, but
[14:46] haven't used skills that much yet, but we are been relying more on contextual
[14:49] we are been relying more on contextual
[14:49] we are been relying more on contextual prompt engineering, I would call it,
[14:51] prompt engineering, I would call it,
[14:51] prompt engineering, I would call it, where like if you want to use a specific
[14:53] where like if you want to use a specific
[14:53] where like if you want to use a specific tool or I guess there're two things that
[14:55] tool or I guess there're two things that
[14:55] tool or I guess there're two things that we have the sub-agents which we're rely
[14:56] we have the sub-agents which we're rely
[14:56] we have the sub-agents which we're rely pretty heavily on. And then the
[14:58] pretty heavily on. And then the
[14:58] pretty heavily on. And then the contextual
[14:59] contextual
[14:59] contextual things of like if it's a study that has
[15:01] things of like if it's a study that has
[15:01] things of like if it's a study that has the specific data structure, then we,
[15:04] the specific data structure, then we,
[15:04] the specific data structure, then we, you know, include a specific, you know,
[15:05] you know, include a specific, you know,
[15:05] you know, include a specific, you know, how do you compare concepts in the
[15:07] how do you compare concepts in the
[15:07] how do you compare concepts in the prompt and those kind of things. And
[15:09] prompt and those kind of things. And
[15:09] prompt and those kind of things. And then we rely on sub-agents. So, for
[15:10] then we rely on sub-agents. So, for
[15:10] then we rely on sub-agents. So, for example, we don't have the instructions
[15:11] example, we don't have the instructions
[15:11] example, we don't have the instructions how to create the PowerPoint in the main
[15:13] how to create the PowerPoint in the main
[15:13] how to create the PowerPoint in the main agent, but we call the sub-agent and
[15:15] agent, but we call the sub-agent and
[15:15] agent, but we call the sub-agent and that has basically the, you know, the
[15:17] that has basically the, you know, the
[15:17] that has basically the, you know, the skill loaded like preloaded by default
[15:19] skill loaded like preloaded by default
[15:19] skill loaded like preloaded by default with all the all the context. We have
[15:21] with all the all the context. We have
[15:21] with all the all the context. We have some other agents that where we do
[15:22] some other agents that where we do
[15:22] some other agents that where we do skills a little more based on you know
[15:24] skills a little more based on you know
[15:24] skills a little more based on you know what we do and I think the the real
[15:25] what we do and I think the the real
[15:25] what we do and I think the the real opportunity is can you reduce the
[15:27] opportunity is can you reduce the
[15:27] opportunity is can you reduce the context? Can you make it more dynamic?
[15:29] context? Can you make it more dynamic?
[15:29] context? Can you make it more dynamic? But it also comes with some challenges.
[15:30] But it also comes with some challenges.
[15:30] But it also comes with some challenges. &gt;&gt; For the contextual prompt engineering,
[15:32] &gt;&gt; For the contextual prompt engineering,
[15:32] &gt;&gt; For the contextual prompt engineering, just to make sure I understand. So
[15:33] just to make sure I understand. So
[15:33] just to make sure I understand. So that's basically like you'll look at the
[15:35] that's basically like you'll look at the
[15:35] that's basically like you'll look at the study that was run and based on those
[15:37] study that was run and based on those
[15:37] study that was run and based on those properties, you'll you'll just insert
[15:39] properties, you'll you'll just insert
[15:39] properties, you'll you'll just insert different things into the prompt. And so
[15:41] different things into the prompt. And so
[15:41] different things into the prompt. And so the system prompt isn't really the same
[15:43] the system prompt isn't really the same
[15:43] the system prompt isn't really the same system prompt for every every study or
[15:47] system prompt for every every study or
[15:47] system prompt for every every study or every agent. It kind of varies a little
[15:48] every agent. It kind of varies a little
[15:48] every agent. It kind of varies a little bit depending on the study.
[15:49] bit depending on the study.
[15:49] bit depending on the study. &gt;&gt; Yeah, exactly. I mean, I think the main
[15:51] &gt;&gt; Yeah, exactly. I mean, I think the main
[15:51] &gt;&gt; Yeah, exactly. I mean, I think the main thing is just if you can cut out like a
[15:52] thing is just if you can cut out like a
[15:52] thing is just if you can cut out like a big chunk or like there's there's one
[15:55] big chunk or like there's there's one
[15:55] big chunk or like there's there's one one feature we have which is emotional
[15:56] one feature we have which is emotional
[15:56] one feature we have which is emotional understanding based on the video and the
[15:58] understanding based on the video and the
[15:58] understanding based on the video and the audio and not just the text. But then
[16:00] audio and not just the text. But then
[16:00] audio and not just the text. But then sometimes some of our studies don't have
[16:02] sometimes some of our studies don't have
[16:02] sometimes some of our studies don't have video and audio, right? And then we can
[16:03] video and audio, right? And then we can
[16:03] video and audio, right? And then we can remove all of these instructions from
[16:05] remove all of these instructions from
[16:05] remove all of these instructions from the prompt and then just have it less be
[16:07] the prompt and then just have it less be
[16:07] the prompt and then just have it less be less confusing. Again, there's there's
[16:08] less confusing. Again, there's there's
[16:08] less confusing. Again, there's there's no magic trick because in in the worst
[16:10] no magic trick because in in the worst
[16:10] no magic trick because in in the worst case, you have all of the cases in there
[16:12] case, you have all of the cases in there
[16:12] case, you have all of the cases in there and you don't save anything, so it
[16:14] and you don't save anything, so it
[16:14] and you don't save anything, so it doesn't really help you in in that case.
[16:15] doesn't really help you in in that case.
[16:16] doesn't really help you in in that case. But oftentimes we see that you know, it
[16:18] But oftentimes we see that you know, it
[16:18] But oftentimes we see that you know, it can help a little bit. How many
[16:19] can help a little bit. How many
[16:19] can help a little bit. How many different tools and how many different
[16:20] different tools and how many different
[16:20] different tools and how many different sub agents do you guys have? For this
[16:22] sub agents do you guys have? For this
[16:22] sub agents do you guys have? For this research agent, it's probably it's more
[16:24] research agent, it's probably it's more
[16:24] research agent, it's probably it's more than you think. It's probably like 15
[16:27] than you think. It's probably like 15
[16:27] than you think. It's probably like 15 tools or something like that. And are
[16:28] tools or something like that. And are
[16:28] tools or something like that. And are most of these tools like running
[16:30] most of these tools like running
[16:30] most of these tools like running something over the table, like a
[16:32] something over the table, like a
[16:32] something over the table, like a classification or or no? There's
[16:34] classification or or no? There's
[16:34] classification or or no? There's probably one or two that that run
[16:36] probably one or two that that run
[16:36] probably one or two that that run everything across the table. There's
[16:37] everything across the table. There's
[16:37] everything across the table. There's maybe one or two different retrieval
[16:39] maybe one or two different retrieval
[16:39] maybe one or two different retrieval modes. There's then maybe one for
[16:41] modes. There's then maybe one for
[16:41] modes. There's then maybe one for creating PowerPoints. There's one for
[16:42] creating PowerPoints. There's one for
[16:42] creating PowerPoints. There's one for creating highlight reels. There's one
[16:44] creating highlight reels. There's one
[16:44] creating highlight reels. There's one for outputting specific chart in
[16:46] for outputting specific chart in
[16:46] for outputting specific chart in specific way. There's one for creating
[16:48] specific way. There's one for creating
[16:48] specific way. There's one for creating like an other artifact like a different
[16:50] like an other artifact like a different
[16:50] like an other artifact like a different artifact. So I think most of them are
[16:52] artifact. So I think most of them are
[16:52] artifact. So I think most of them are either output related or like processing
[16:54] either output related or like processing
[16:54] either output related or like processing related. Like either compute new data or
[16:56] related. Like either compute new data or
[16:56] related. Like either compute new data or create some artifact that you can then
[16:57] create some artifact that you can then
[16:57] create some artifact that you can then use in the um in artifact. And one other
[17:01] use in the um in artifact. And one other
[17:01] use in the um in artifact. And one other thing we also have is this which is
[17:03] thing we also have is this which is
[17:03] thing we also have is this which is pretty interesting is this feedback
[17:04] pretty interesting is this feedback
[17:04] pretty interesting is this feedback tool. Hm. Which especially for the
[17:06] tool. Hm. Which especially for the
[17:06] tool. Hm. Which especially for the long-running task, you can't really do
[17:07] long-running task, you can't really do
[17:07] long-running task, you can't really do it in the live one, but in the
[17:08] it in the live one, but in the
[17:08] it in the live one, but in the long-running task, it can then
[17:09] long-running task, it can then
[17:10] long-running task, it can then self-request feedback. And so it's
[17:11] self-request feedback. And so it's
[17:11] self-request feedback. And so it's basically you have this sub agent which
[17:13] basically you have this sub agent which
[17:13] basically you have this sub agent which is this reviewer agent that just has a
[17:15] is this reviewer agent that just has a
[17:15] is this reviewer agent that just has a clear context, doesn't have all the
[17:17] clear context, doesn't have all the
[17:17] clear context, doesn't have all the complicated instructions on, you know,
[17:20] complicated instructions on, you know,
[17:20] complicated instructions on, you know, and then not necessarily sees all the
[17:21] and then not necessarily sees all the
[17:21] and then not necessarily sees all the history, but just has just knows what a
[17:23] history, but just has just knows what a
[17:23] history, but just has just knows what a good report looks like. And then has a
[17:25] good report looks like. And then has a
[17:25] good report looks like. And then has a little set of criteria, like, okay, it
[17:27] little set of criteria, like, okay, it
[17:27] little set of criteria, like, okay, it should not have any claims that are not
[17:29] should not have any claims that are not
[17:29] should not have any claims that are not backed up by citations or by data. And
[17:32] backed up by citations or by data. And
[17:32] backed up by citations or by data. And then it kind of goes through the report
[17:33] then it kind of goes through the report
[17:33] then it kind of goes through the report and gives feedback. And that's actually
[17:35] and gives feedback. And that's actually
[17:35] and gives feedback. And that's actually a loop that, you know, runs
[17:37] a loop that, you know, runs
[17:37] a loop that, you know, runs you know, you can run it quite often and
[17:39] you know, you can run it quite often and
[17:39] you know, you can run it quite often and it will actually catch a lot of things
[17:40] it will actually catch a lot of things
[17:40] it will actually catch a lot of things and will make things much better. So,
[17:42] and will make things much better. So,
[17:42] and will make things much better. So, that's what we run it using the
[17:43] that's what we run it using the
[17:43] that's what we run it using the asynchronous um runner.
[17:46] asynchronous um runner.
[17:46] asynchronous um runner. And then in the live runner, we use it
[17:47] And then in the live runner, we use it
[17:47] And then in the live runner, we use it as an evaluation system. So, basically,
[17:50] as an evaluation system. So, basically,
[17:50] as an evaluation system. So, basically, I mean, it we have to make some slight
[17:51] I mean, it we have to make some slight
[17:51] I mean, it we have to make some slight adjustments, but basically, you want to
[17:53] adjustments, but basically, you want to
[17:53] adjustments, but basically, you want to know how many issues does this
[17:55] know how many issues does this
[17:55] know how many issues does this evaluation agent find in the report and
[17:57] evaluation agent find in the report and
[17:57] evaluation agent find in the report and can you, you know, at least the first
[17:59] can you, you know, at least the first
[17:59] can you, you know, at least the first step is just at least know how bad it is
[18:01] step is just at least know how bad it is
[18:01] step is just at least know how bad it is or what the common issues are. And then
[18:03] or what the common issues are. And then
[18:03] or what the common issues are. And then if you make a change to the prompt, to
[18:05] if you make a change to the prompt, to
[18:05] if you make a change to the prompt, to the model,
[18:07] the model,
[18:07] the model, uh or maybe some change you think is not
[18:08] uh or maybe some change you think is not
[18:08] uh or maybe some change you think is not even related, you'll see if it actually
[18:10] even related, you'll see if it actually
[18:10] even related, you'll see if it actually increases things either on our benchmark
[18:12] increases things either on our benchmark
[18:12] increases things either on our benchmark set or even in production of like if
[18:13] set or even in production of like if
[18:13] set or even in production of like if there's a spike in a specific uh
[18:15] there's a spike in a specific uh
[18:15] there's a spike in a specific uh problem.
[18:16] problem.
[18:16] problem. &gt;&gt; When will you run this eval over the
[18:17] &gt;&gt; When will you run this eval over the
[18:17] &gt;&gt; When will you run this eval over the live things? Is it like offline evals
[18:19] live things? Is it like offline evals
[18:19] live things? Is it like offline evals that you run before production? Are you
[18:20] that you run before production? Are you
[18:20] that you run before production? Are you also running it over production data?
[18:22] also running it over production data?
[18:22] also running it over production data? And like if so, is that happening at the
[18:24] And like if so, is that happening at the
[18:24] And like if so, is that happening at the same time as it's chatting or like at
[18:26] same time as it's chatting or like at
[18:26] same time as it's chatting or like at the end of a day you do a big cron job
[18:27] the end of a day you do a big cron job
[18:27] the end of a day you do a big cron job and score a bunch of things? I mean, I
[18:29] and score a bunch of things? I mean, I
[18:29] and score a bunch of things? I mean, I think that's something where we're still
[18:31] think that's something where we're still
[18:31] think that's something where we're still optimizing right now. We we just kick
[18:33] optimizing right now. We we just kick
[18:33] optimizing right now. We we just kick that off after after each run in like an
[18:35] that off after after each run in like an
[18:35] that off after after each run in like an asynchronous runner, so it doesn't like
[18:36] asynchronous runner, so it doesn't like
[18:36] asynchronous runner, so it doesn't like block things, but it just gets eval'd
[18:39] block things, but it just gets eval'd
[18:39] block things, but it just gets eval'd live. I mean, there's probably some cost
[18:40] live. I mean, there's probably some cost
[18:40] live. I mean, there's probably some cost optimization we can do on batch
[18:42] optimization we can do on batch
[18:42] optimization we can do on batch inference, but hasn't been the the
[18:44] inference, but hasn't been the the
[18:44] inference, but hasn't been the the biggest priority right now. But it's
[18:45] biggest priority right now. But it's
[18:45] biggest priority right now. But it's just fast to kind of have internal
[18:47] just fast to kind of have internal
[18:47] just fast to kind of have internal internal metrics. And we might also move
[18:49] internal metrics. And we might also move
[18:49] internal metrics. And we might also move to, you know, subsampling, but it's the
[18:51] to, you know, subsampling, but it's the
[18:51] to, you know, subsampling, but it's the cost is not the biggest concern for us
[18:52] cost is not the biggest concern for us
[18:52] cost is not the biggest concern for us right now. I think it's really can we
[18:53] right now. I think it's really can we
[18:53] right now. I think it's really can we make the product better and yeah, that
[18:55] make the product better and yeah, that
[18:55] make the product better and yeah, that it's not the biggest concern right now.
[18:56] it's not the biggest concern right now.
[18:56] it's not the biggest concern right now. What does make the product better mean
[18:59] What does make the product better mean
[18:59] What does make the product better mean to you? Is it just increasing accuracy
[19:01] to you? Is it just increasing accuracy
[19:01] to you? Is it just increasing accuracy on the existing things? Is it spreading
[19:02] on the existing things? Is it spreading
[19:02] on the existing things? Is it spreading out to more challenges and more domains?
[19:05] out to more challenges and more domains?
[19:05] out to more challenges and more domains? &gt;&gt; that's something we we also thought
[19:06] &gt;&gt; that's something we we also thought
[19:06] &gt;&gt; that's something we we also thought about a bit recently because
[19:08] about a bit recently because
[19:08] about a bit recently because in some ways, if If have the signal all
[19:11] in some ways, if If have the signal all
[19:11] in some ways, if If have the signal all are all the things that are broken.
[19:12] are all the things that are broken.
[19:12] are all the things that are broken. Obviously, you want to fix them and and
[19:14] Obviously, you want to fix them and and
[19:14] Obviously, you want to fix them and and make progress on those. And that's going
[19:16] make progress on those. And that's going
[19:16] make progress on those. And that's going to be improving the reliability. That's
[19:18] to be improving the reliability. That's
[19:18] to be improving the reliability. That's very important. But sometimes you also
[19:21] very important. But sometimes you also
[19:21] very important. But sometimes you also want to take a step back and then maybe
[19:23] want to take a step back and then maybe
[19:23] want to take a step back and then maybe maybe just optimizing this local
[19:24] maybe just optimizing this local
[19:24] maybe just optimizing this local minimum. And maybe sometimes you
[19:26] minimum. And maybe sometimes you
[19:26] minimum. And maybe sometimes you actually want to, you know, change the
[19:28] actually want to, you know, change the
[19:28] actually want to, you know, change the architecture overall or change the
[19:29] architecture overall or change the
[19:29] architecture overall or change the approach overall. And then maybe the
[19:30] approach overall. And then maybe the
[19:30] approach overall. And then maybe the criteria is even changed. This hill
[19:32] criteria is even changed. This hill
[19:32] criteria is even changed. This hill climbing is very important because
[19:33] climbing is very important because
[19:33] climbing is very important because otherwise you ship a product that is
[19:35] otherwise you ship a product that is
[19:35] otherwise you ship a product that is aspirationally great, but then in
[19:36] aspirationally great, but then in
[19:36] aspirationally great, but then in practice doesn't work. Again,
[19:38] practice doesn't work. Again,
[19:38] practice doesn't work. Again, you can only test it in so many cases
[19:40] you can only test it in so many cases
[19:40] you can only test it in so many cases yourself. And the customer is the first
[19:41] yourself. And the customer is the first
[19:41] yourself. And the customer is the first customer who tries it will use it in a
[19:43] customer who tries it will use it in a
[19:43] customer who tries it will use it in a way that you didn't anticipate. So, I
[19:45] way that you didn't anticipate. So, I
[19:45] way that you didn't anticipate. So, I think it is very important to try to
[19:47] think it is very important to try to
[19:47] think it is very important to try to have those evolve in production. Are
[19:48] have those evolve in production. Are
[19:48] have those evolve in production. Are there any fun stories of how people were
[19:50] there any fun stories of how people were
[19:50] there any fun stories of how people were using it in ways that you didn't
[19:52] using it in ways that you didn't
[19:52] using it in ways that you didn't anticipate when you first launched it or
[19:53] anticipate when you first launched it or
[19:53] anticipate when you first launched it or that you're discovering now? There's a
[19:55] that you're discovering now? There's a
[19:55] that you're discovering now? There's a bunch of things. People definitely
[19:57] bunch of things. People definitely
[19:57] bunch of things. People definitely very soon try to like
[20:00] very soon try to like
[20:00] very soon try to like not break it in like a prompt injection
[20:02] not break it in like a prompt injection
[20:02] not break it in like a prompt injection way, but like really test the limits of
[20:03] way, but like really test the limits of
[20:04] way, but like really test the limits of like, you know, can you do like a
[20:05] like, you know, can you do like a
[20:05] like, you know, can you do like a cluster analysis? Can you do like can
[20:07] cluster analysis? Can you do like can
[20:07] cluster analysis? Can you do like can you run like a, you know, classification
[20:08] you run like a, you know, classification
[20:08] you run like a, you know, classification model in the Python side. And then, you
[20:10] model in the Python side. And then, you
[20:10] model in the Python side. And then, you know, usually the like the Python Python
[20:13] know, usually the like the Python Python
[20:13] know, usually the like the Python Python leverage um image we have is is limited.
[20:15] leverage um image we have is is limited.
[20:15] leverage um image we have is is limited. It can't do everything. And then like it
[20:17] It can't do everything. And then like it
[20:17] It can't do everything. And then like it tries to like create the code things up
[20:19] tries to like create the code things up
[20:19] tries to like create the code things up from scratch. I'm like, "Okay, sure. Let
[20:20] from scratch. I'm like, "Okay, sure. Let
[20:21] from scratch. I'm like, "Okay, sure. Let me write like a classification algorithm
[20:22] me write like a classification algorithm
[20:22] me write like a classification algorithm like myself in my own Python environment
[20:24] like myself in my own Python environment
[20:24] like myself in my own Python environment because it doesn't have access to those
[20:25] because it doesn't have access to those
[20:25] because it doesn't have access to those tools." And then we're like, "Okay,
[20:26] tools." And then we're like, "Okay,
[20:26] tools." And then we're like, "Okay, maybe we should give it some some more
[20:28] maybe we should give it some some more
[20:28] maybe we should give it some some more tools."
[20:29] tools."
[20:29] tools." So, it doesn't have to do those things
[20:30] So, it doesn't have to do those things
[20:30] So, it doesn't have to do those things um manually. It's always interesting and
[20:31] um manually. It's always interesting and
[20:32] um manually. It's always interesting and it happens much sooner than you than you
[20:33] it happens much sooner than you than you
[20:33] it happens much sooner than you than you expect. When you're like iterating on
[20:35] expect. When you're like iterating on
[20:36] expect. When you're like iterating on these insights from production usage,
[20:38] these insights from production usage,
[20:38] these insights from production usage, are the most common things you're
[20:39] are the most common things you're
[20:39] are the most common things you're iterating on like changing the prompt or
[20:41] iterating on like changing the prompt or
[20:41] iterating on like changing the prompt or giving it more tools or updating like
[20:43] giving it more tools or updating like
[20:43] giving it more tools or updating like the environment that it's running code
[20:45] the environment that it's running code
[20:45] the environment that it's running code in? Like where have you seen the
[20:46] in? Like where have you seen the
[20:46] in? Like where have you seen the distribution of of things go? I think
[20:48] distribution of of things go? I think
[20:48] distribution of of things go? I think obviously the updating the prompt is the
[20:50] obviously the updating the prompt is the
[20:50] obviously the updating the prompt is the lowest lift. The hard part is, you know,
[20:53] lowest lift. The hard part is, you know,
[20:53] lowest lift. The hard part is, you know, if you change the prompt,
[20:55] if you change the prompt,
[20:55] if you change the prompt, it hopefully improves the thing that you
[20:56] it hopefully improves the thing that you
[20:56] it hopefully improves the thing that you want to improve it on. Does it then
[20:58] want to improve it on. Does it then
[20:58] want to improve it on. Does it then especially if you're like change it to
[20:59] especially if you're like change it to
[20:59] especially if you're like change it to all caps and repeat it three times, does
[21:01] all caps and repeat it three times, does
[21:01] all caps and repeat it three times, does it then mean something else regresses?
[21:03] it then mean something else regresses?
[21:03] it then mean something else regresses? Right? Because of this less attention to
[21:04] Right? Because of this less attention to
[21:04] Right? Because of this less attention to the some and other intersections. I
[21:06] the some and other intersections. I
[21:06] the some and other intersections. I think that's the that's the hard part.
[21:07] think that's the that's the hard part.
[21:07] think that's the that's the hard part. How do you gain confidence in that right
[21:09] How do you gain confidence in that right
[21:09] How do you gain confidence in that right now?
[21:10] now?
[21:10] now? &gt;&gt; Yeah, it's I don't think we have a good
[21:11] &gt;&gt; Yeah, it's I don't think we have a good
[21:11] &gt;&gt; Yeah, it's I don't think we have a good solution. Um I think obviously as we
[21:13] solution. Um I think obviously as we
[21:13] solution. Um I think obviously as we deployed and sometimes we roll it out
[21:15] deployed and sometimes we roll it out
[21:15] deployed and sometimes we roll it out slowly and see, you know, other number
[21:17] slowly and see, you know, other number
[21:17] slowly and see, you know, other number of issues, but I mean we have like a
[21:19] of issues, but I mean we have like a
[21:19] of issues, but I mean we have like a example like test set of like maybe 20
[21:21] example like test set of like maybe 20
[21:21] example like test set of like maybe 20 different product we can always run it
[21:23] different product we can always run it
[21:23] different product we can always run it on, we can evaluate, we can see at least
[21:25] on, we can evaluate, we can see at least
[21:25] on, we can evaluate, we can see at least on that small sample size is anything
[21:26] on that small sample size is anything
[21:26] on that small sample size is anything and that's what we actually manually
[21:28] and that's what we actually manually
[21:28] and that's what we actually manually look through the outputs and see, okay,
[21:30] look through the outputs and see, okay,
[21:30] look through the outputs and see, okay, still seems good, but it's it's really
[21:32] still seems good, but it's it's really
[21:32] still seems good, but it's it's really hard to compare one like five-page
[21:34] hard to compare one like five-page
[21:34] hard to compare one like five-page output with another five-page output.
[21:36] output with another five-page output.
[21:36] output with another five-page output. They're different. People would probably
[21:37] They're different. People would probably
[21:37] They're different. People would probably argue this one is better, some people
[21:39] argue this one is better, some people
[21:39] argue this one is better, some people would argue this one's better, like I
[21:41] would argue this one's better, like I
[21:41] would argue this one's better, like I don't know, but at least you will see if
[21:42] don't know, but at least you will see if
[21:42] don't know, but at least you will see if something like clearly breaks. How many
[21:44] something like clearly breaks. How many
[21:44] something like clearly breaks. How many times, if at all, have you guys like
[21:46] times, if at all, have you guys like
[21:46] times, if at all, have you guys like completely re-architected this agent? It
[21:48] completely re-architected this agent? It
[21:48] completely re-architected this agent? It sounds like you maybe you're thinking of
[21:50] sounds like you maybe you're thinking of
[21:50] sounds like you maybe you're thinking of that now or starting to think of that.
[21:51] that now or starting to think of that.
[21:51] that now or starting to think of that. &gt;&gt; I've done it a bunch of times. I mean,
[21:53] &gt;&gt; I've done it a bunch of times. I mean,
[21:53] &gt;&gt; I've done it a bunch of times. I mean, over the last 2 years, I would say
[21:55] over the last 2 years, I would say
[21:55] over the last 2 years, I would say &gt;&gt; And what's what's like been the main
[21:56] &gt;&gt; And what's what's like been the main
[21:56] &gt;&gt; And what's what's like been the main impetus? Is the models just getting
[21:57] impetus? Is the models just getting
[21:57] impetus? Is the models just getting better or I don't know, you you hear a
[22:00] better or I don't know, you you hear a
[22:00] better or I don't know, you you hear a great talk from someone at LangChain
[22:02] great talk from someone at LangChain
[22:02] great talk from someone at LangChain maybe or something like that? But no,
[22:03] maybe or something like that? But no,
[22:03] maybe or something like that? But no, like what what what's been the impetus
[22:05] like what what what's been the impetus
[22:05] like what what what's been the impetus Um
[22:06] Um
[22:06] Um I mean, I think the first iteration was
[22:07] I mean, I think the first iteration was
[22:07] I mean, I think the first iteration was just like before kind of agents really
[22:09] just like before kind of agents really
[22:09] just like before kind of agents really worked. Like the the first version was
[22:11] worked. Like the the first version was
[22:11] worked. Like the the first version was just like a simple rack bot, which I
[22:13] just like a simple rack bot, which I
[22:13] just like a simple rack bot, which I guess probably most companies start out
[22:15] guess probably most companies start out
[22:15] guess probably most companies start out doing and that's still a primitive that
[22:16] doing and that's still a primitive that
[22:16] doing and that's still a primitive that we have, but I think both like smaller
[22:19] we have, but I think both like smaller
[22:19] we have, but I think both like smaller models getting good enough that you can
[22:22] models getting good enough that you can
[22:22] models getting good enough that you can actually do like look at all the data,
[22:24] actually do like look at all the data,
[22:24] actually do like look at all the data, classify things uh live, that's been a
[22:26] classify things uh live, that's been a
[22:26] classify things uh live, that's been a change and then the big models getting
[22:28] change and then the big models getting
[22:28] change and then the big models getting smart enough that it can really
[22:29] smart enough that it can really
[22:29] smart enough that it can really orchestrate those things uh has been the
[22:31] orchestrate those things uh has been the
[22:31] orchestrate those things uh has been the biggest change. And I don't think it was
[22:33] biggest change. And I don't think it was
[22:33] biggest change. And I don't think it was like a single thing. I think we've been
[22:35] like a single thing. I think we've been
[22:35] like a single thing. I think we've been talking about this a lot and it's been a
[22:36] talking about this a lot and it's been a
[22:36] talking about this a lot and it's been a big investment from on our side to
[22:38] big investment from on our side to
[22:38] big investment from on our side to re-architect this and we definitely did
[22:40] re-architect this and we definitely did
[22:40] re-architect this and we definitely did a lot of explorations before trying it
[22:42] a lot of explorations before trying it
[22:42] a lot of explorations before trying it out and yeah, now I mean, obviously, you
[22:44] out and yeah, now I mean, obviously, you
[22:44] out and yeah, now I mean, obviously, you know, most people are moving towards
[22:45] know, most people are moving towards
[22:45] know, most people are moving towards like a file system uh based agent,
[22:47] like a file system uh based agent,
[22:48] like a file system uh based agent, something we we have explored, you know,
[22:51] something we we have explored, you know,
[22:51] something we we have explored, you know, a couple months ago and there felt like
[22:53] a couple months ago and there felt like
[22:53] a couple months ago and there felt like especially in our specific use case, it
[22:55] especially in our specific use case, it
[22:55] especially in our specific use case, it wasn't like kind of still want to have
[22:57] wasn't like kind of still want to have
[22:57] wasn't like kind of still want to have these specific tools. Is that largely
[22:59] these specific tools. Is that largely
[22:59] these specific tools. Is that largely because of like the table that you guys
[23:01] because of like the table that you guys
[23:01] because of like the table that you guys have and the ability to quickly run over
[23:03] have and the ability to quickly run over
[23:03] have and the ability to quickly run over all things there.
[23:03] all things there.
[23:03] all things there. &gt;&gt; is is pretty powerful. But, there are
[23:05] &gt;&gt; is is pretty powerful. But, there are
[23:05] &gt;&gt; is is pretty powerful. But, there are arguments against that, especially if
[23:08] arguments against that, especially if
[23:08] arguments against that, especially if like the model companies start to, you
[23:10] like the model companies start to, you
[23:10] like the model companies start to, you know, post um
[23:12] know, post um
[23:12] know, post um you know, post-train on the specific
[23:14] you know, post-train on the specific
[23:14] you know, post-train on the specific harness or the specific protocols, it
[23:16] harness or the specific protocols, it
[23:16] harness or the specific protocols, it feels like you're kind of fighting
[23:18] feels like you're kind of fighting
[23:18] feels like you're kind of fighting against that movement if you have your
[23:19] against that movement if you have your
[23:19] against that movement if you have your own harness. I think right now all these
[23:21] own harness. I think right now all these
[23:21] own harness. I think right now all these like coding agent harnesses are pretty
[23:23] like coding agent harnesses are pretty
[23:23] like coding agent harnesses are pretty bad at like calling sub-agents
[23:25] bad at like calling sub-agents
[23:25] bad at like calling sub-agents programmatically. Like, they can call
[23:26] programmatically. Like, they can call
[23:27] programmatically. Like, they can call them one at a time, but what you guys
[23:28] them one at a time, but what you guys
[23:28] them one at a time, but what you guys really want, it sounds like, is to
[23:29] really want, it sounds like, is to
[23:29] really want, it sounds like, is to basically call it 500 times and have
[23:31] basically call it 500 times and have
[23:31] basically call it 500 times and have that always happening and this is
[23:33] that always happening and this is
[23:33] that always happening and this is similar to some of the stuff in like the
[23:34] similar to some of the stuff in like the
[23:34] similar to some of the stuff in like the recursive language model paper, but I
[23:36] recursive language model paper, but I
[23:36] recursive language model paper, but I don't think any of We're thinking a lot
[23:37] don't think any of We're thinking a lot
[23:38] don't think any of We're thinking a lot about this. How can we take those ideas
[23:39] about this. How can we take those ideas
[23:39] about this. How can we take those ideas and put them into like these coding
[23:40] and put them into like these coding
[23:40] and put them into like these coding agent harnesses? And there's some stuff
[23:42] agent harnesses? And there's some stuff
[23:42] agent harnesses? And there's some stuff we're thinking about, but I don't think
[23:43] we're thinking about, but I don't think
[23:43] we're thinking about, but I don't think we or anyone has really nailed that.
[23:44] we or anyone has really nailed that.
[23:45] we or anyone has really nailed that. Yeah, exactly. I mean, you know,
[23:46] Yeah, exactly. I mean, you know,
[23:46] Yeah, exactly. I mean, you know, obviously the way we do it is we don't
[23:47] obviously the way we do it is we don't
[23:47] obviously the way we do it is we don't actually the model doesn't actually call
[23:49] actually the model doesn't actually call
[23:49] actually the model doesn't actually call it 500 times. It just calls it once and
[23:50] it 500 times. It just calls it once and
[23:50] it 500 times. It just calls it once and then we have this hard-coded workflow.
[23:52] then we have this hard-coded workflow.
[23:52] then we have this hard-coded workflow. If you call this tool once, we spawn
[23:53] If you call this tool once, we spawn
[23:53] If you call this tool once, we spawn those 500 agents and then we aggregate
[23:55] those 500 agents and then we aggregate
[23:55] those 500 agents and then we aggregate it in a very specific way and then it
[23:57] it in a very specific way and then it
[23:57] it in a very specific way and then it returns it. Can I like call it over a
[23:58] returns it. Can I like call it over a
[23:58] returns it. Can I like call it over a subset of rows? Could it pass in some
[24:00] subset of rows? Could it pass in some
[24:00] subset of rows? Could it pass in some like filter criteria to filter things
[24:02] like filter criteria to filter things
[24:02] like filter criteria to filter things out?
[24:03] out?
[24:03] out? &gt;&gt; Exactly. So, that's that's one of the
[24:03] &gt;&gt; Exactly. So, that's that's one of the
[24:03] &gt;&gt; Exactly. So, that's that's one of the use cases and maybe also coming back to
[24:05] use cases and maybe also coming back to
[24:05] use cases and maybe also coming back to your question about what have we
[24:06] your question about what have we
[24:06] your question about what have we changed? Like, it's it's prompt changes,
[24:08] changed? Like, it's it's prompt changes,
[24:08] changed? Like, it's it's prompt changes, but then something like oh, often times
[24:10] but then something like oh, often times
[24:10] but then something like oh, often times it would have to filter. And what it
[24:12] it would have to filter. And what it
[24:12] it would have to filter. And what it used to do is run it on everything and
[24:14] used to do is run it on everything and
[24:14] used to do is run it on everything and then write a Python script to filter out
[24:16] then write a Python script to filter out
[24:16] then write a Python script to filter out instead of giving the aggregate results
[24:18] instead of giving the aggregate results
[24:18] instead of giving the aggregate results over all of the data, it would just with
[24:19] over all of the data, it would just with
[24:20] over all of the data, it would just with Python filter out the aggregate results.
[24:21] Python filter out the aggregate results.
[24:21] Python filter out the aggregate results. We're like, okay, this seems a little
[24:23] We're like, okay, this seems a little
[24:23] We're like, okay, this seems a little bit, you know, cumbersome. Like, let's
[24:25] bit, you know, cumbersome. Like, let's
[24:25] bit, you know, cumbersome. Like, let's add the specific additional fields in
[24:26] add the specific additional fields in
[24:26] add the specific additional fields in the tool call of like filter column.
[24:28] the tool call of like filter column.
[24:28] the tool call of like filter column. Right? And then you set it this column
[24:29] Right? And then you set it this column
[24:29] Right? And then you set it this column equals this field to filter. It works in
[24:31] equals this field to filter. It works in
[24:32] equals this field to filter. It works in like 90% of the filter cases. There
[24:33] like 90% of the filter cases. There
[24:33] like 90% of the filter cases. There might still be some advanced filters
[24:34] might still be some advanced filters
[24:34] might still be some advanced filters based on like combination of columns. It
[24:36] based on like combination of columns. It
[24:36] based on like combination of columns. It might need to write a Python script on,
[24:38] might need to write a Python script on,
[24:38] might need to write a Python script on, but that helps a lot. So, that's one of
[24:39] but that helps a lot. So, that's one of
[24:39] but that helps a lot. So, that's one of the other things that we obviously see
[24:42] the other things that we obviously see
[24:42] the other things that we obviously see as we as we deploy those. And that's but
[24:44] as we as we deploy those. And that's but
[24:44] as we as we deploy those. And that's but that's really something you have to look
[24:45] that's really something you have to look
[24:45] that's really something you have to look at traces yourself and you have to have
[24:47] at traces yourself and you have to have
[24:47] at traces yourself and you have to have good observability. You have to really
[24:49] good observability. You have to really
[24:49] good observability. You have to really go deep and see what did it do? Does it
[24:51] go deep and see what did it do? Does it
[24:51] go deep and see what did it do? Does it actually make sense? Sometimes even look
[24:52] actually make sense? Sometimes even look
[24:52] actually make sense? Sometimes even look at the reasoning traces of the model.
[24:53] at the reasoning traces of the model.
[24:53] at the reasoning traces of the model. Like, why did it call this thing? And
[24:55] Like, why did it call this thing? And
[24:55] Like, why did it call this thing? And then see, oh, I I wish I had this tool
[24:57] then see, oh, I I wish I had this tool
[24:57] then see, oh, I I wish I had this tool more or less and you're like okay, maybe
[24:59] more or less and you're like okay, maybe
[24:59] more or less and you're like okay, maybe I should give it that tool. What is
[25:01] I should give it that tool. What is
[25:01] I should give it that tool. What is trace analysis, trace observability look
[25:03] trace analysis, trace observability look
[25:03] trace analysis, trace observability look like for you guys? How do people do it?
[25:05] like for you guys? How do people do it?
[25:05] like for you guys? How do people do it? Who's doing it? Is it everyone on the
[25:07] Who's doing it? Is it everyone on the
[25:07] Who's doing it? Is it everyone on the team? Do you have like specific people
[25:08] team? Do you have like specific people
[25:08] team? Do you have like specific people who are focused on it? I imagine you
[25:10] who are focused on it? I imagine you
[25:10] who are focused on it? I imagine you guys have millions of traces. How do you
[25:12] guys have millions of traces. How do you
[25:12] guys have millions of traces. How do you know which traces to look look at and
[25:13] know which traces to look look at and
[25:13] know which traces to look look at and then when they find something what do
[25:14] then when they find something what do
[25:14] then when they find something what do what do they do with it? We want to
[25:16] what do they do with it? We want to
[25:16] what do they do with it? We want to trace every single
[25:18] trace every single
[25:18] trace every single um
[25:18] um
[25:18] um every single trace like we really store
[25:20] every single trace like we really store
[25:20] every single trace like we really store it we don't want to sub sample.
[25:21] it we don't want to sub sample.
[25:21] it we don't want to sub sample. But then we never look we only look at
[25:23] But then we never look we only look at
[25:23] But then we never look we only look at the point 01% or less.
[25:25] the point 01% or less.
[25:26] the point 01% or less. But it's like logging right? You want to
[25:27] But it's like logging right? You want to
[25:28] But it's like logging right? You want to see this specific case there's something
[25:30] see this specific case there's something
[25:30] see this specific case there's something weird. Let me debug why that is and then
[25:32] weird. Let me debug why that is and then
[25:32] weird. Let me debug why that is and then you go really deep and then
[25:34] you go really deep and then
[25:34] you go really deep and then you know, I think the the depth over the
[25:36] you know, I think the the depth over the
[25:36] you know, I think the the depth over the breadth definitely makes sense and then
[25:37] breadth definitely makes sense and then
[25:37] breadth definitely makes sense and then sometimes I mean we have had like Claude
[25:39] sometimes I mean we have had like Claude
[25:40] sometimes I mean we have had like Claude like Claude um
[25:41] like Claude um
[25:41] like Claude um just run analysis on all the traces like
[25:44] just run analysis on all the traces like
[25:44] just run analysis on all the traces like what are the common things that that
[25:45] what are the common things that that
[25:45] what are the common things that that like the the common paths or the common
[25:47] like the the common paths or the common
[25:47] like the the common paths or the common uh things that happen. That's also
[25:49] uh things that happen. That's also
[25:49] uh things that happen. That's also interesting but I think the most you
[25:51] interesting but I think the most you
[25:51] interesting but I think the most you learn the most by just going really deep
[25:52] learn the most by just going really deep
[25:52] learn the most by just going really deep on one or two traces and really looking
[25:54] on one or two traces and really looking
[25:54] on one or two traces and really looking at more or less every single tool call
[25:56] at more or less every single tool call
[25:56] at more or less every single tool call and if it's a 30-minute trace it
[25:57] and if it's a 30-minute trace it
[25:57] and if it's a 30-minute trace it actually takes you quite a while to go
[25:58] actually takes you quite a while to go
[25:58] actually takes you quite a while to go through those but that's that's how you
[26:00] through those but that's that's how you
[26:00] through those but that's that's how you learn if it works or it doesn't work and
[26:02] learn if it works or it doesn't work and
[26:02] learn if it works or it doesn't work and that's usually in in the development
[26:04] that's usually in in the development
[26:04] that's usually in in the development like you just run it on your own
[26:05] like you just run it on your own
[26:05] like you just run it on your own computer or um on your cloud um
[26:08] computer or um on your cloud um
[26:08] computer or um on your cloud um dev setup but it's also in production
[26:10] dev setup but it's also in production
[26:10] dev setup but it's also in production like debugging what went wrong. You
[26:12] like debugging what went wrong. You
[26:12] like debugging what went wrong. You mentioned sandboxes twice. It sounds
[26:13] mentioned sandboxes twice. It sounds
[26:13] mentioned sandboxes twice. It sounds like once you have a tool that like runs
[26:15] like once you have a tool that like runs
[26:15] like once you have a tool that like runs in the sandbox and then the other is a
[26:17] in the sandbox and then the other is a
[26:17] in the sandbox and then the other is a sub agent that spawns a sandbox with the
[26:19] sub agent that spawns a sandbox with the
[26:19] sub agent that spawns a sandbox with the agent inside of it. What what have you
[26:21] agent inside of it. What what have you
[26:21] agent inside of it. What what have you learned about working with sandboxes?
[26:23] learned about working with sandboxes?
[26:23] learned about working with sandboxes? Any yeah, lessons learned there? Our
[26:25] Any yeah, lessons learned there? Our
[26:25] Any yeah, lessons learned there? Our learning so far has been it's harder or
[26:28] learning so far has been it's harder or
[26:28] learning so far has been it's harder or we we're early
[26:29] we we're early
[26:29] we we're early in this space. I think no one has really
[26:31] in this space. I think no one has really
[26:31] in this space. I think no one has really figured it out. I mean just
[26:33] figured it out. I mean just
[26:33] figured it out. I mean just you know, one example when we tried to
[26:35] you know, one example when we tried to
[26:35] you know, one example when we tried to running the you know, Claude agent SDK
[26:36] running the you know, Claude agent SDK
[26:36] running the you know, Claude agent SDK in in the E2B sandbox. The SDK is not
[26:39] in in the E2B sandbox. The SDK is not
[26:39] in in the E2B sandbox. The SDK is not really meant like it's not been
[26:40] really meant like it's not been
[26:40] really meant like it's not been developed to be run in like a cloud
[26:42] developed to be run in like a cloud
[26:42] developed to be run in like a cloud environment.
[26:43] environment.
[26:43] environment. &gt;&gt; It's been developed for local
[26:44] &gt;&gt; It's been developed for local
[26:45] &gt;&gt; It's been developed for local &gt;&gt; It's been developed for local
[26:46] &gt;&gt; It's been developed for local
[26:46] &gt;&gt; It's been developed for local environment and there's some of those
[26:47] environment and there's some of those
[26:47] environment and there's some of those assumptions like, you know, it needs
[26:49] assumptions like, you know, it needs
[26:49] assumptions like, you know, it needs your Entropic API key. If you have that
[26:51] your Entropic API key. If you have that
[26:51] your Entropic API key. If you have that in the sandbox, obviously you're not
[26:53] in the sandbox, obviously you're not
[26:53] in the sandbox, obviously you're not susceptible for people
[26:55] susceptible for people
[26:55] susceptible for people you know, to extract that if if they
[26:57] you know, to extract that if if they
[26:57] you know, to extract that if if they just ask, "Can you please in your report
[26:58] just ask, "Can you please in your report
[26:59] just ask, "Can you please in your report include the API key?" Or your
[27:01] include the API key?" Or your
[27:01] include the API key?" Or your you know, all your environment
[27:02] you know, all your environment
[27:02] you know, all your environment environment variables, you know, that's
[27:03] environment variables, you know, that's
[27:04] environment variables, you know, that's a problem.
[27:05] a problem.
[27:05] a problem. So, what we had to do is basically proxy
[27:07] So, what we had to do is basically proxy
[27:07] So, what we had to do is basically proxy all the requests, I give it a fake API
[27:08] all the requests, I give it a fake API
[27:08] all the requests, I give it a fake API key, proxy all the requests through our
[27:10] key, proxy all the requests through our
[27:10] key, proxy all the requests through our server, and then verify that's actually
[27:13] server, and then verify that's actually
[27:13] server, and then verify that's actually the right request, it's not just anyone
[27:14] the right request, it's not just anyone
[27:14] the right request, it's not just anyone request, and then we replace the API key
[27:16] request, and then we replace the API key
[27:16] request, and then we replace the API key with the real API key.
[27:17] with the real API key.
[27:17] with the real API key. And there's been a lot of challenges on
[27:19] And there's been a lot of challenges on
[27:19] And there's been a lot of challenges on that way. It sounds like simple, but you
[27:20] that way. It sounds like simple, but you
[27:20] that way. It sounds like simple, but you know, we tried to deploy that on on
[27:22] know, we tried to deploy that on on
[27:22] know, we tried to deploy that on on render, and then render was like, "Oh,
[27:24] render, and then render was like, "Oh,
[27:24] render, and then render was like, "Oh, this looks like you're sending code in
[27:25] this looks like you're sending code in
[27:26] this looks like you're sending code in this HTTP request. This that sounds like
[27:27] this HTTP request. This that sounds like
[27:27] this HTTP request. This that sounds like there's some you know, malicious
[27:29] there's some you know, malicious
[27:29] there's some you know, malicious behavior, and then we're blocking your
[27:30] behavior, and then we're blocking your
[27:30] behavior, and then we're blocking your request for this." Like, there's like a
[27:32] request for this." Like, there's like a
[27:32] request for this." Like, there's like a lot of things that made us think, "Wow,
[27:34] lot of things that made us think, "Wow,
[27:34] lot of things that made us think, "Wow, this is still very early." Like it feels
[27:35] this is still very early." Like it feels
[27:35] this is still very early." Like it feels hacky almost to to deploy that. And I
[27:37] hacky almost to to deploy that. And I
[27:37] hacky almost to to deploy that. And I think some of the things that you've
[27:38] think some of the things that you've
[27:38] think some of the things that you've been working on sound like super
[27:40] been working on sound like super
[27:40] been working on sound like super relevant for this and making that much
[27:41] relevant for this and making that much
[27:41] relevant for this and making that much easier. So, I wish we had used that
[27:43] easier. So, I wish we had used that
[27:43] easier. So, I wish we had used that earlier. Do you guys have memory
[27:44] earlier. Do you guys have memory
[27:44] earlier. Do you guys have memory anywhere in any of the agents?
[27:46] anywhere in any of the agents?
[27:46] anywhere in any of the agents? &gt;&gt; Um yes, like certain ways you always do
[27:48] &gt;&gt; Um yes, like certain ways you always do
[27:48] &gt;&gt; Um yes, like certain ways you always do it. So,
[27:49] it. So,
[27:49] it. So, the way we solved it so far is like a
[27:51] the way we solved it so far is like a
[27:51] the way we solved it so far is like a relatively explicit version of memory
[27:53] relatively explicit version of memory
[27:53] relatively explicit version of memory where it kind of on your organization
[27:54] where it kind of on your organization
[27:54] where it kind of on your organization level you can give it instructions. I
[27:55] level you can give it instructions. I
[27:55] level you can give it instructions. I think that's a pattern that is seen in a
[27:57] think that's a pattern that is seen in a
[27:57] think that's a pattern that is seen in a lot of companies. You give some some
[27:59] lot of companies. You give some some
[27:59] lot of companies. You give some some general instructions, and they they will
[28:01] general instructions, and they they will
[28:01] general instructions, and they they will be applied for
[28:03] be applied for
[28:03] be applied for setting up new projects, they will be
[28:04] setting up new projects, they will be
[28:04] setting up new projects, they will be applied for analyzing
[28:06] applied for analyzing
[28:06] applied for analyzing um product in a specific way. And those
[28:08] um product in a specific way. And those
[28:08] um product in a specific way. And those are all like human genera humans type
[28:10] are all like human genera humans type
[28:10] are all like human genera humans type those things.
[28:10] those things.
[28:10] those things. &gt;&gt; Exactly. Exactly. You can you can define
[28:12] &gt;&gt; Exactly. Exactly. You can you can define
[28:12] &gt;&gt; Exactly. Exactly. You can you can define them yourself. And the biggest question
[28:14] them yourself. And the biggest question
[28:14] them yourself. And the biggest question for us on the analysis side is, what is
[28:16] for us on the analysis side is, what is
[28:16] for us on the analysis side is, what is actually something that's interesting
[28:17] actually something that's interesting
[28:17] actually something that's interesting versus something that's
[28:19] versus something that's
[28:19] versus something that's you know, obvious, right? And I can't
[28:21] you know, obvious, right? And I can't
[28:21] you know, obvious, right? And I can't really judge that from the outside. It's
[28:23] really judge that from the outside. It's
[28:23] really judge that from the outside. It's really something that the customer needs
[28:24] really something that the customer needs
[28:24] really something that the customer needs to needs to tell us because, you know,
[28:26] to needs to tell us because, you know,
[28:26] to needs to tell us because, you know, from the outside everything seems new
[28:28] from the outside everything seems new
[28:28] from the outside everything seems new and interesting, but then when you're
[28:29] and interesting, but then when you're
[28:29] and interesting, but then when you're inside you're like, "Yeah, that's the
[28:30] inside you're like, "Yeah, that's the
[28:30] inside you're like, "Yeah, that's the thing I I know. I've worked here for 10
[28:32] thing I I know. I've worked here for 10
[28:32] thing I I know. I've worked here for 10 years. Like, that's not something new to
[28:34] years. Like, that's not something new to
[28:34] years. Like, that's not something new to me." And over time you really build that
[28:36] me." And over time you really build that
[28:36] me." And over time you really build that through all the all the reports we're
[28:38] through all the all the reports we're
[28:38] through all the all the reports we're generating from other projects. You
[28:39] generating from other projects. You
[28:39] generating from other projects. You know, how do you how can we use that as
[28:41] know, how do you how can we use that as
[28:41] know, how do you how can we use that as an input for creating new studies? And
[28:44] an input for creating new studies? And
[28:44] an input for creating new studies? And there's a lot of complexity there
[28:45] there's a lot of complexity there
[28:45] there's a lot of complexity there because maybe someone else maybe you
[28:47] because maybe someone else maybe you
[28:47] because maybe someone else maybe you didn't even read this report that we
[28:48] didn't even read this report that we
[28:48] didn't even read this report that we assume we already know because someone
[28:50] assume we already know because someone
[28:50] assume we already know because someone another person, another business unit.
[28:52] another person, another business unit.
[28:52] another person, another business unit. So, it's not super easy to figure that
[28:54] So, it's not super easy to figure that
[28:54] So, it's not super easy to figure that out what is common knowledge, what is
[28:56] out what is common knowledge, what is
[28:56] out what is common knowledge, what is not. But, using some things across like
[28:59] not. But, using some things across like
[28:59] not. But, using some things across like you know, formatting preferences or um
[29:03] you know, formatting preferences or um
[29:03] you know, formatting preferences or um you know, in the way we set up projects,
[29:04] you know, in the way we set up projects,
[29:04] you know, in the way we set up projects, using some of that kind of previous
[29:06] using some of that kind of previous
[29:06] using some of that kind of previous knowledge that we try to distill. But,
[29:07] knowledge that we try to distill. But,
[29:07] knowledge that we try to distill. But, yeah, it's it's far from being solved. I
[29:09] yeah, it's it's far from being solved. I
[29:09] yeah, it's it's far from being solved. I think there's a lot more work to be done
[29:10] think there's a lot more work to be done
[29:10] think there's a lot more work to be done in that domain. Let's talk about UX for
[29:13] in that domain. Let's talk about UX for
[29:13] in that domain. Let's talk about UX for a little bit. And maybe here we can zoom
[29:15] a little bit. And maybe here we can zoom
[29:15] a little bit. And maybe here we can zoom out to the three or actually even like
[29:17] out to the three or actually even like
[29:17] out to the three or actually even like four different agents you have. So,
[29:18] four different agents you have. So,
[29:18] four different agents you have. So, maybe for the the first agent that you
[29:20] maybe for the the first agent that you
[29:20] maybe for the the first agent that you mentioned, the kind of onboarding agent,
[29:23] mentioned, the kind of onboarding agent,
[29:23] mentioned, the kind of onboarding agent, it sounded like there was a doc on like
[29:26] it sounded like there was a doc on like
[29:26] it sounded like there was a doc on like a Word doc on one side and then you
[29:27] a Word doc on one side and then you
[29:28] a Word doc on one side and then you would chat with it and it would fill out
[29:29] would chat with it and it would fill out
[29:29] would chat with it and it would fill out kind of like the study guide. Could you
[29:31] kind of like the study guide. Could you
[29:31] kind of like the study guide. Could you talk more about that UX and what that
[29:33] talk more about that UX and what that
[29:33] talk more about that UX and what that looks like? Yeah, exactly. We've been
[29:34] looks like? Yeah, exactly. We've been
[29:34] looks like? Yeah, exactly. We've been iterating
[29:35] iterating
[29:35] iterating a lot on that. I think the the first
[29:37] a lot on that. I think the the first
[29:37] a lot on that. I think the the first version you would you would think of
[29:38] version you would you would think of
[29:38] version you would you would think of this is you just prompt an LLM to write
[29:41] this is you just prompt an LLM to write
[29:41] this is you just prompt an LLM to write your discussion guide, your document,
[29:43] your discussion guide, your document,
[29:43] your discussion guide, your document, right? And then you do that and then you
[29:45] right? And then you do that and then you
[29:45] right? And then you do that and then you realize it never gets it right 100%. Not
[29:48] realize it never gets it right 100%. Not
[29:48] realize it never gets it right 100%. Not not to blame the model. I think the
[29:49] not to blame the model. I think the
[29:49] not to blame the model. I think the model is great. But, just like you give
[29:51] model is great. But, just like you give
[29:51] model is great. But, just like you give it one sentence, you
[29:52] it one sentence, you
[29:52] it one sentence, you expect it to write like a whole page out
[29:54] expect it to write like a whole page out
[29:54] expect it to write like a whole page out of it. Like that's probably not going to
[29:55] of it. Like that's probably not going to
[29:55] of it. Like that's probably not going to work. So, there needs to be some
[29:56] work. So, there needs to be some
[29:56] work. So, there needs to be some interaction. And then basically the
[29:58] interaction. And then basically the
[29:58] interaction. And then basically the second version we built is can we just
[30:00] second version we built is can we just
[30:00] second version we built is can we just have the AI can you just chat with it,
[30:02] have the AI can you just chat with it,
[30:02] have the AI can you just chat with it, right? And you can can it make
[30:03] right? And you can can it make
[30:03] right? And you can can it make modifications to that, right? And then
[30:05] modifications to that, right? And then
[30:05] modifications to that, right? And then you have the two
[30:06] you have the two
[30:06] you have the two basic principles that
[30:08] basic principles that
[30:08] basic principles that you have to decide between. It's like
[30:09] you have to decide between. It's like
[30:09] you have to decide between. It's like either the LLM rewrites your entire
[30:11] either the LLM rewrites your entire
[30:11] either the LLM rewrites your entire document and that works for shorter
[30:13] document and that works for shorter
[30:13] document and that works for shorter documents or it works if you're actually
[30:15] documents or it works if you're actually
[30:15] documents or it works if you're actually making like changes like can you change
[30:17] making like changes like can you change
[30:17] making like changes like can you change the tone or something like that. Or do
[30:19] the tone or something like that. Or do
[30:19] the tone or something like that. Or do you say like you have some kind of edit
[30:20] you say like you have some kind of edit
[30:20] you say like you have some kind of edit functionality that is either string
[30:22] functionality that is either string
[30:22] functionality that is either string replaces or you have some IDs that you
[30:24] replaces or you have some IDs that you
[30:24] replaces or you have some IDs that you replace only specific IDs, which usually
[30:26] replace only specific IDs, which usually
[30:26] replace only specific IDs, which usually works better, but sometimes can also be
[30:28] works better, but sometimes can also be
[30:28] works better, but sometimes can also be confusing if you're making a lot of
[30:29] confusing if you're making a lot of
[30:29] confusing if you're making a lot of changes, you stack them, you say like ID
[30:31] changes, you stack them, you say like ID
[30:31] changes, you stack them, you say like ID number two is now ID number three and
[30:32] number two is now ID number three and
[30:32] number two is now ID number three and then you inserted a new element here and
[30:34] then you inserted a new element here and
[30:34] then you inserted a new element here and then all the like it's also not perfect,
[30:36] then all the like it's also not perfect,
[30:36] then all the like it's also not perfect, but that's kind of the approach that
[30:37] but that's kind of the approach that
[30:37] but that's kind of the approach that that that we picked. Can we just make
[30:39] that that we picked. Can we just make
[30:39] that that we picked. Can we just make because our documents are pretty long,
[30:40] because our documents are pretty long,
[30:40] because our documents are pretty long, can we just make targeted changes and so
[30:42] can we just make targeted changes and so
[30:42] can we just make targeted changes and so on. That's pretty cool. And then you
[30:44] on. That's pretty cool. And then you
[30:44] on. That's pretty cool. And then you realize like sometimes chatting with it
[30:46] realize like sometimes chatting with it
[30:46] realize like sometimes chatting with it is not the fastest way to to to modify
[30:49] is not the fastest way to to to modify
[30:49] is not the fastest way to to to modify things. Sometimes you just want to
[30:50] things. Sometimes you just want to
[30:50] things. Sometimes you just want to delete that and then telling the AI
[30:52] delete that and then telling the AI
[30:52] delete that and then telling the AI please delete question number three
[30:54] please delete question number three
[30:54] please delete question number three feels a little bit cumbersome. Or
[30:56] feels a little bit cumbersome. Or
[30:56] feels a little bit cumbersome. Or sometimes you just want to reformulate
[30:57] sometimes you just want to reformulate
[30:57] sometimes you just want to reformulate it yourself. So you do you want to have
[30:59] it yourself. So you do you want to have
[30:59] it yourself. So you do you want to have a way of also manually modifying it and
[31:01] a way of also manually modifying it and
[31:01] a way of also manually modifying it and you know, OpenAI and Tropicana they have
[31:03] you know, OpenAI and Tropicana they have
[31:03] you know, OpenAI and Tropicana they have some version of that. I don't think the
[31:05] some version of that. I don't think the
[31:05] some version of that. I don't think the UI access like supernatural and they've
[31:07] UI access like supernatural and they've
[31:07] UI access like supernatural and they've also iterated a lot on those. I've seen
[31:08] also iterated a lot on those. I've seen
[31:08] also iterated a lot on those. I've seen like they rolled back some of the
[31:10] like they rolled back some of the
[31:10] like they rolled back some of the changes they did and so on.
[31:11] changes they did and so on.
[31:11] changes they did and so on. I think we have a pretty good solution
[31:12] I think we have a pretty good solution
[31:12] I think we have a pretty good solution now where you're both working on the
[31:14] now where you're both working on the
[31:14] now where you're both working on the same edit history. So you can actually
[31:16] same edit history. So you can actually
[31:16] same edit history. So you can actually undo undo changes and you kind of have
[31:18] undo undo changes and you kind of have
[31:18] undo undo changes and you kind of have the change log. You can compare things
[31:20] the change log. You can compare things
[31:20] the change log. You can compare things and you can manually make changes and
[31:21] and you can manually make changes and
[31:21] and you can manually make changes and then you can also make changes with the
[31:23] then you can also make changes with the
[31:23] then you can also make changes with the with the chat and it kind of knows about
[31:24] with the chat and it kind of knows about
[31:24] with the chat and it kind of knows about the changes you made so it doesn't undo
[31:26] the changes you made so it doesn't undo
[31:26] the changes you made so it doesn't undo the changes immediately and How how does
[31:28] the changes immediately and How how does
[31:28] the changes immediately and How how does it know about those changes? Are those
[31:29] it know about those changes? Are those
[31:29] it know about those changes? Are those inserted How do Yeah, how how does it
[31:31] inserted How do Yeah, how how does it
[31:31] inserted How do Yeah, how how does it know about this?
[31:32] know about this?
[31:32] know about this? &gt;&gt; Basically the way it works is
[31:34] &gt;&gt; Basically the way it works is
[31:34] &gt;&gt; Basically the way it works is every change we make is uh formatted as
[31:36] every change we make is uh formatted as
[31:36] every change we make is uh formatted as an edit operation. So you see a log of
[31:39] an edit operation. So you see a log of
[31:39] an edit operation. So you see a log of all the edit operations. So then it at
[31:41] all the edit operations. So then it at
[31:41] all the edit operations. So then it at least it knows, okay, you just modified
[31:42] least it knows, okay, you just modified
[31:42] least it knows, okay, you just modified this question. Because the main problem
[31:44] this question. Because the main problem
[31:44] this question. Because the main problem is you can't always have like this is
[31:46] is you can't always have like this is
[31:46] is you can't always have like this is the old appro like this is the old
[31:47] the old appro like this is the old
[31:47] the old appro like this is the old document this is the new document or
[31:49] document this is the new document or
[31:49] document this is the new document or somehow you need to modify the diff. So
[31:50] somehow you need to modify the diff. So
[31:50] somehow you need to modify the diff. So we kind of formalize that in like an
[31:52] we kind of formalize that in like an
[31:52] we kind of formalize that in like an edit operations way and then the model
[31:54] edit operations way and then the model
[31:54] edit operations way and then the model knows, okay, if you just touch that or
[31:56] knows, okay, if you just touch that or
[31:57] knows, okay, if you just touch that or if in the history you see that you
[31:58] if in the history you see that you
[31:58] if in the history you see that you haven't touched that and you probably
[31:59] haven't touched that and you probably
[31:59] haven't touched that and you probably don't want to rewrite that. Cuz those
[32:00] don't want to rewrite that. Cuz those
[32:00] don't want to rewrite that. Cuz those are passed like so like if I I I'm
[32:02] are passed like so like if I I I'm
[32:02] are passed like so like if I I I'm chatting with it it gets a document. I
[32:04] chatting with it it gets a document. I
[32:04] chatting with it it gets a document. I go into the document edit something and
[32:06] go into the document edit something and
[32:06] go into the document edit something and then I chat with it again. Like that
[32:08] then I chat with it again. Like that
[32:08] then I chat with it again. Like that edit is passed in like prior to my
[32:10] edit is passed in like prior to my
[32:10] edit is passed in like prior to my message in some way. It's the same like
[32:12] message in some way. It's the same like
[32:12] message in some way. It's the same like the LM writes out edit edit operations
[32:14] the LM writes out edit edit operations
[32:14] the LM writes out edit edit operations and the human edits also edit operations
[32:16] and the human edits also edit operations
[32:16] and the human edits also edit operations that kind of fit into the same kind of
[32:18] that kind of fit into the same kind of
[32:18] that kind of fit into the same kind of message history.
[32:19] message history.
[32:19] message history. Um yeah. So that's the approach that
[32:21] Um yeah. So that's the approach that
[32:21] Um yeah. So that's the approach that worked pretty well for us. Cool. So
[32:22] worked pretty well for us. Cool. So
[32:22] worked pretty well for us. Cool. So that's the onboarding agent then there's
[32:24] that's the onboarding agent then there's
[32:24] that's the onboarding agent then there's the interviewer agent and that sounds
[32:26] the interviewer agent and that sounds
[32:26] the interviewer agent and that sounds like you've got voice there. It's
[32:28] like you've got voice there. It's
[32:28] like you've got voice there. It's multimodal. It's more just like a
[32:30] multimodal. It's more just like a
[32:30] multimodal. It's more just like a chatbot style thing. Any anything
[32:31] chatbot style thing. Any anything
[32:31] chatbot style thing. Any anything interesting there that you guys have
[32:32] interesting there that you guys have
[32:33] interesting there that you guys have been playing with? The interface like
[32:34] been playing with? The interface like
[32:34] been playing with? The interface like the voice interface is still
[32:37] the voice interface is still
[32:37] the voice interface is still still not quite solved and we've seen
[32:39] still not quite solved and we've seen
[32:39] still not quite solved and we've seen even like open AI like the chat GPT app
[32:41] even like open AI like the chat GPT app
[32:41] even like open AI like the chat GPT app has been going back and forth where they
[32:43] has been going back and forth where they
[32:43] has been going back and forth where they used to have this like blue bubble that
[32:44] used to have this like blue bubble that
[32:44] used to have this like blue bubble that was speaking and now that their voice
[32:46] was speaking and now that their voice
[32:46] was speaking and now that their voice mode is actually you see the text and it
[32:48] mode is actually you see the text and it
[32:48] mode is actually you see the text and it writes out text as well. That's kind of
[32:50] writes out text as well. That's kind of
[32:50] writes out text as well. That's kind of the approach that we have been taking
[32:51] the approach that we have been taking
[32:52] the approach that we have been taking for a while as well because you can
[32:53] for a while as well because you can
[32:53] for a while as well because you can actually read text faster than you can
[32:55] actually read text faster than you can
[32:55] actually read text faster than you can you can listen to it and sometimes it
[32:56] you can listen to it and sometimes it
[32:56] you can listen to it and sometimes it can actually be annoying to like you
[32:58] can actually be annoying to like you
[32:58] can actually be annoying to like you know, I wanted the 2x speed or
[32:59] know, I wanted the 2x speed or
[32:59] know, I wanted the 2x speed or something.
[33:00] something.
[33:00] something. Um but then sometimes 2x speed is too
[33:02] Um but then sometimes 2x speed is too
[33:02] Um but then sometimes 2x speed is too fast and actually want to go back. So, I
[33:04] fast and actually want to go back. So, I
[33:04] fast and actually want to go back. So, I don't think it's fully solved yet and
[33:06] don't think it's fully solved yet and
[33:06] don't think it's fully solved yet and same time for our use case we really
[33:07] same time for our use case we really
[33:07] same time for our use case we really don't want to interrupt people in almost
[33:09] don't want to interrupt people in almost
[33:09] don't want to interrupt people in almost all cases. We just want to we listen
[33:11] all cases. We just want to we listen
[33:11] all cases. We just want to we listen company right you want to listen to the
[33:12] company right you want to listen to the
[33:12] company right you want to listen to the customers. We don't want to interrupt
[33:13] customers. We don't want to interrupt
[33:13] customers. We don't want to interrupt them even if they may be saying
[33:14] them even if they may be saying
[33:15] them even if they may be saying something that's you know, rambling or
[33:17] something that's you know, rambling or
[33:17] something that's you know, rambling or maybe going slightly off tangent. Often
[33:18] maybe going slightly off tangent. Often
[33:18] maybe going slightly off tangent. Often times there is a reason for that and in
[33:20] times there is a reason for that and in
[33:20] times there is a reason for that and in only very rare cases we actually want to
[33:21] only very rare cases we actually want to
[33:21] only very rare cases we actually want to interrupt. So, even if I would take a
[33:23] interrupt. So, even if I would take a
[33:23] interrupt. So, even if I would take a break for a second to think about
[33:25] break for a second to think about
[33:25] break for a second to think about something, I actually don't want the AI
[33:26] something, I actually don't want the AI
[33:26] something, I actually don't want the AI to jump in. And are you guys using kind
[33:28] to jump in. And are you guys using kind
[33:28] to jump in. And are you guys using kind of like the the speech-to-text,
[33:31] of like the the speech-to-text,
[33:31] of like the the speech-to-text, text-to-speech sandwich or you using the
[33:33] text-to-speech sandwich or you using the
[33:33] text-to-speech sandwich or you using the real-time APIs? But now we're we're
[33:35] real-time APIs? But now we're we're
[33:35] real-time APIs? But now we're we're mainly using the you know,
[33:37] mainly using the you know,
[33:37] mainly using the you know, speech-to-text, text-to-speech uh by
[33:39] speech-to-text, text-to-speech uh by
[33:39] speech-to-text, text-to-speech uh by then just because it's so important to
[33:41] then just because it's so important to
[33:41] then just because it's so important to have the smartest models and often times
[33:43] have the smartest models and often times
[33:43] have the smartest models and often times these real-time services and last time
[33:45] these real-time services and last time
[33:45] these real-time services and last time we evaluated them at least I think the
[33:47] we evaluated them at least I think the
[33:47] we evaluated them at least I think the models are now getting pretty good, but
[33:48] models are now getting pretty good, but
[33:48] models are now getting pretty good, but at least when we evaluated them they
[33:50] at least when we evaluated them they
[33:50] at least when we evaluated them they were like one or two tiers, you know,
[33:52] were like one or two tiers, you know,
[33:52] were like one or two tiers, you know, faster and dumber than they you know,
[33:54] faster and dumber than they you know,
[33:54] faster and dumber than they you know, top tier uh Opus and and and so on
[33:57] top tier uh Opus and and and so on
[33:57] top tier uh Opus and and and so on models that
[33:59] models that
[33:59] models that it is so important to ask like it sounds
[34:00] it is so important to ask like it sounds
[34:00] it is so important to ask like it sounds very simple to just have a conversation
[34:02] very simple to just have a conversation
[34:02] very simple to just have a conversation and then asking the right questions. I
[34:03] and then asking the right questions. I
[34:03] and then asking the right questions. I mean, guess that's what you're doing
[34:05] mean, guess that's what you're doing
[34:05] mean, guess that's what you're doing today. It is actually pretty hot hot
[34:07] today. It is actually pretty hot hot
[34:07] today. It is actually pretty hot hot task um and that's why we don't want to
[34:09] task um and that's why we don't want to
[34:09] task um and that's why we don't want to compromise on that and and rather
[34:11] compromise on that and and rather
[34:11] compromise on that and and rather compromise a little bit on the um you
[34:13] compromise a little bit on the um you
[34:13] compromise a little bit on the um you know, real-time aspect of it. Yeah, I
[34:15] know, real-time aspect of it. Yeah, I
[34:15] know, real-time aspect of it. Yeah, I you you've got the fast and dumb
[34:16] you you've got the fast and dumb
[34:16] you you've got the fast and dumb interviewer here today.
[34:18] interviewer here today.
[34:18] interviewer here today. Um I feel like most people myself
[34:20] Um I feel like most people myself
[34:20] Um I feel like most people myself included have largely stayed in kind of
[34:22] included have largely stayed in kind of
[34:22] included have largely stayed in kind of just like the text domain of agents.
[34:25] just like the text domain of agents.
[34:25] just like the text domain of agents. When you think about adding on voice,
[34:27] When you think about adding on voice,
[34:27] When you think about adding on voice, like how much extra work is that? Is it
[34:29] like how much extra work is that? Is it
[34:29] like how much extra work is that? Is it easy? Is Is hard? It depends.
[34:32] easy? Is Is hard? It depends.
[34:32] easy? Is Is hard? It depends. Um
[34:33] Um
[34:33] Um I think the hard part is not necessarily
[34:35] I think the hard part is not necessarily
[34:35] I think the hard part is not necessarily the AI. I think it's more like, you
[34:37] the AI. I think it's more like, you
[34:37] the AI. I think it's more like, you know, we're collecting facets It's the
[34:39] know, we're collecting facets It's the
[34:39] know, we're collecting facets It's the interview runs on like millions of
[34:42] interview runs on like millions of
[34:42] interview runs on like millions of people's devices, right? And the more
[34:43] people's devices, right? And the more
[34:43] people's devices, right? And the more modalities you have, the harder it
[34:45] modalities you have, the harder it
[34:45] modalities you have, the harder it becomes from a compatibility
[34:47] becomes from a compatibility
[34:47] becomes from a compatibility perspective. And kind of you see all
[34:48] perspective. And kind of you see all
[34:48] perspective. And kind of you see all kinds of issues on like somehow the
[34:50] kinds of issues on like somehow the
[34:50] kinds of issues on like somehow the microphone stopped working. Or you know
[34:52] microphone stopped working. Or you know
[34:52] microphone stopped working. Or you know how like everyone used to have like
[34:53] how like everyone used to have like
[34:53] how like everyone used to have like trouble with like Zoom like microphone
[34:55] trouble with like Zoom like microphone
[34:55] trouble with like Zoom like microphone not getting recognized and those kind of
[34:57] not getting recognized and those kind of
[34:57] not getting recognized and those kind of things. So we see all of that across the
[34:59] things. So we see all of that across the
[34:59] things. So we see all of that across the the globe, right? Globally. So I think
[35:01] the globe, right? Globally. So I think
[35:01] the globe, right? Globally. So I think those are more of the challenges with
[35:02] those are more of the challenges with
[35:02] those are more of the challenges with the multimodality for us than like on
[35:04] the multimodality for us than like on
[35:04] the multimodality for us than like on the AI side.
[35:06] the AI side.
[35:06] the AI side. And the AI models are getting pretty
[35:07] And the AI models are getting pretty
[35:07] And the AI models are getting pretty good. I think there's still some
[35:08] good. I think there's still some
[35:08] good. I think there's still some challenges on, you know, transcription.
[35:11] challenges on, you know, transcription.
[35:11] challenges on, you know, transcription. You'd think that it's a solved problem.
[35:13] You'd think that it's a solved problem.
[35:13] You'd think that it's a solved problem. And you know, our models are getting
[35:14] And you know, our models are getting
[35:14] And you know, our models are getting pretty good, but there's still something
[35:16] pretty good, but there's still something
[35:16] pretty good, but there's still something like you release a new product uh
[35:18] like you release a new product uh
[35:18] like you release a new product uh tomorrow, the transcription model
[35:20] tomorrow, the transcription model
[35:20] tomorrow, the transcription model doesn't know about, you know, that name.
[35:23] doesn't know about, you know, that name.
[35:23] doesn't know about, you know, that name. And it probably uses some other name.
[35:24] And it probably uses some other name.
[35:24] And it probably uses some other name. And you know, the only way we could
[35:26] And you know, the only way we could
[35:26] And you know, the only way we could solve that for now is actually having an
[35:28] solve that for now is actually having an
[35:28] solve that for now is actually having an LLM that has the context on the
[35:30] LLM that has the context on the
[35:31] LLM that has the context on the interview and maybe even knows some of
[35:32] interview and maybe even knows some of
[35:32] interview and maybe even knows some of the terms that might come up. Correct
[35:34] the terms that might come up. Correct
[35:34] the terms that might come up. Correct the transcription model basically on the
[35:36] the transcription model basically on the
[35:36] the transcription model basically on the fly just to give this additional like
[35:38] fly just to give this additional like
[35:38] fly just to give this additional like smartness that the transcription model
[35:39] smartness that the transcription model
[35:39] smartness that the transcription model itself can't can't use. So these are
[35:41] itself can't can't use. So these are
[35:41] itself can't can't use. So these are some of the challenges. And there's
[35:42] some of the challenges. And there's
[35:42] some of the challenges. And there's obviously like traditional things of
[35:43] obviously like traditional things of
[35:43] obviously like traditional things of like now we're storing like, you know,
[35:45] like now we're storing like, you know,
[35:45] like now we're storing like, you know, thousands of hours of video
[35:47] thousands of hours of video
[35:48] thousands of hours of video data and you need to,
[35:49] data and you need to,
[35:49] data and you need to, you know, do that. But those are more
[35:50] you know, do that. But those are more
[35:50] you know, do that. But those are more like traditional infrastructure
[35:51] like traditional infrastructure
[35:51] like traditional infrastructure problems. And then going on to UX, the
[35:53] problems. And then going on to UX, the
[35:53] problems. And then going on to UX, the final research agent in in the two
[35:56] final research agent in in the two
[35:56] final research agent in in the two different modes it has. So when it's
[35:57] different modes it has. So when it's
[35:57] different modes it has. So when it's running kind of like long in the
[35:58] running kind of like long in the
[35:58] running kind of like long in the background, how long does that take? And
[36:00] background, how long does that take? And
[36:00] background, how long does that take? And do you kick one off? How do you kick one
[36:02] do you kick one off? How do you kick one
[36:02] do you kick one off? How do you kick one off? Does it happen like automatically
[36:03] off? Does it happen like automatically
[36:03] off? Does it happen like automatically after all 500 interviews are done? Yeah,
[36:06] after all 500 interviews are done? Yeah,
[36:06] after all 500 interviews are done? Yeah, that's that's a big It's a big
[36:07] that's that's a big It's a big
[36:07] that's that's a big It's a big challenge. So
[36:09] challenge. So
[36:09] challenge. So again, it runs for like 30 minutes and
[36:10] again, it runs for like 30 minutes and
[36:10] again, it runs for like 30 minutes and so on. So the cost is like, you know,
[36:12] so on. So the cost is like, you know,
[36:12] so on. So the cost is like, you know, significant. It's nothing crazy. And you
[36:14] significant. It's nothing crazy. And you
[36:14] significant. It's nothing crazy. And you know, we're usually like a higher-priced
[36:17] know, we're usually like a higher-priced
[36:17] know, we're usually like a higher-priced uh
[36:17] uh
[36:17] uh offering. So it's not the biggest
[36:19] offering. So it's not the biggest
[36:19] offering. So it's not the biggest concern, but you don't want to re-kick
[36:20] concern, but you don't want to re-kick
[36:20] concern, but you don't want to re-kick it like after every time there's a new
[36:22] it like after every time there's a new
[36:22] it like after every time there's a new response or someone updates. And you
[36:23] response or someone updates. And you
[36:23] response or someone updates. And you know, you have 500 responses.
[36:25] know, you have 500 responses.
[36:25] know, you have 500 responses. At the same time, we do want to show you
[36:27] At the same time, we do want to show you
[36:27] At the same time, we do want to show you results early, right? You get the first
[36:28] results early, right? You get the first
[36:28] results early, right? You get the first 10 responses. That that's a magical
[36:30] 10 responses. That that's a magical
[36:30] 10 responses. That that's a magical moment and that might happen like 30
[36:32] moment and that might happen like 30
[36:32] moment and that might happen like 30 minutes after you launch the study or to
[36:33] minutes after you launch the study or to
[36:33] minutes after you launch the study or to get your first 10 people to respond,
[36:35] get your first 10 people to respond,
[36:35] get your first 10 people to respond, which is very magical. So, we do want to
[36:37] which is very magical. So, we do want to
[36:37] which is very magical. So, we do want to give you something.
[36:38] give you something.
[36:38] give you something. Um the way we do it right now is we run
[36:40] Um the way we do it right now is we run
[36:40] Um the way we do it right now is we run it at a certain thresholds of of
[36:42] it at a certain thresholds of of
[36:43] it at a certain thresholds of of interviews. We do like a full analysis
[36:45] interviews. We do like a full analysis
[36:45] interviews. We do like a full analysis and kind of rethink all the hypotheses
[36:46] and kind of rethink all the hypotheses
[36:46] and kind of rethink all the hypotheses and, you know, if the data has changed
[36:48] and, you know, if the data has changed
[36:48] and, you know, if the data has changed from 10 to 20 or from 20 to 100
[36:50] from 10 to 20 or from 20 to 100
[36:50] from 10 to 20 or from 20 to 100 interviews, we actually want to
[36:52] interviews, we actually want to
[36:52] interviews, we actually want to completely rerun this. And that's one
[36:54] completely rerun this. And that's one
[36:54] completely rerun this. And that's one part, but then now you have we run it
[36:56] part, but then now you have we run it
[36:56] part, but then now you have we run it after 100 interviews and now then 101st
[36:59] after 100 interviews and now then 101st
[36:59] after 100 interviews and now then 101st comes in, 102nd comes in. Like, you
[37:01] comes in, 102nd comes in. Like, you
[37:01] comes in, 102nd comes in. Like, you don't want to rerun everything. But, at
[37:04] don't want to rerun everything. But, at
[37:04] don't want to rerun everything. But, at the same time, you have we have like
[37:05] the same time, you have we have like
[37:05] the same time, you have we have like numbers in in our report, right? We have
[37:08] numbers in in our report, right? We have
[37:08] numbers in in our report, right? We have percentages, we have charts and all
[37:09] percentages, we have charts and all
[37:09] percentages, we have charts and all these kind of things. And those things
[37:11] these kind of things. And those things
[37:11] these kind of things. And those things we constructed in a way that we can
[37:13] we constructed in a way that we can
[37:13] we constructed in a way that we can actually replace those things. So, they
[37:15] actually replace those things. So, they
[37:15] actually replace those things. So, they LM never outputs those numbers. It only
[37:17] LM never outputs those numbers. It only
[37:17] LM never outputs those numbers. It only outputs placeholders. Hm. And then we
[37:19] outputs placeholders. Hm. And then we
[37:19] outputs placeholders. Hm. And then we can run all the classifications, all the
[37:20] can run all the classifications, all the
[37:20] can run all the classifications, all the Python code again.
[37:21] Python code again.
[37:21] Python code again. Um but keep the core
[37:23] Um but keep the core
[37:23] Um but keep the core uh thing the same. Um so, this way we
[37:26] uh thing the same. Um so, this way we
[37:26] uh thing the same. Um so, this way we always our numbers are always verifiable
[37:27] always our numbers are always verifiable
[37:27] always our numbers are always verifiable and updated. So, you can always click on
[37:29] and updated. So, you can always click on
[37:29] and updated. So, you can always click on them. You can see the data that's backed
[37:30] them. You can see the data that's backed
[37:30] them. You can see the data that's backed up. And if there's a new response coming
[37:31] up. And if there's a new response coming
[37:31] up. And if there's a new response coming in or you remove one response because,
[37:33] in or you remove one response because,
[37:33] in or you remove one response because, you know, maybe you don't like them or
[37:34] you know, maybe you don't like them or
[37:34] you know, maybe you don't like them or it's like low quality, uh the those
[37:36] it's like low quality, uh the those
[37:36] it's like low quality, uh the those things will update immediately.
[37:38] things will update immediately.
[37:38] things will update immediately. Obviously, there's there's like a limit
[37:39] Obviously, there's there's like a limit
[37:39] Obviously, there's there's like a limit to that. If you say like if in the text
[37:41] to that. If you say like if in the text
[37:41] to that. If you say like if in the text it says like, you know, this is
[37:42] it says like, you know, this is
[37:42] it says like, you know, this is definitely the best idea because 80% of
[37:44] definitely the best idea because 80% of
[37:44] definitely the best idea because 80% of people liked it and then more more
[37:46] people liked it and then more more
[37:46] people liked it and then more more responses come in and suddenly it's no
[37:47] responses come in and suddenly it's no
[37:47] responses come in and suddenly it's no longer 80%, it's only 20%, then actually
[37:49] longer 80%, it's only 20%, then actually
[37:49] longer 80%, it's only 20%, then actually the, you know, qualitative takeaways
[37:52] the, you know, qualitative takeaways
[37:52] the, you know, qualitative takeaways change so that you you do need to run it
[37:53] change so that you you do need to run it
[37:53] change so that you you do need to run it occasionally. Yeah, that's one of the
[37:55] occasionally. Yeah, that's one of the
[37:56] occasionally. Yeah, that's one of the one of the things we
[37:57] one of the things we
[37:57] one of the things we we work with. And, you know, at the end
[37:58] we work with. And, you know, at the end
[37:58] we work with. And, you know, at the end you usually in our use case you usually
[38:00] you usually in our use case you usually
[38:00] you usually in our use case you usually say like, "Okay, now I'm done." Um or
[38:02] say like, "Okay, now I'm done." Um or
[38:02] say like, "Okay, now I'm done." Um or you haven't seen any new responses for 2
[38:03] you haven't seen any new responses for 2
[38:03] you haven't seen any new responses for 2 days and then we run like a full new
[38:05] days and then we run like a full new
[38:05] days and then we run like a full new analysis. But, I think the real-time
[38:06] analysis. But, I think the real-time
[38:06] analysis. But, I think the real-time component, I really believe in this, you
[38:08] component, I really believe in this, you
[38:08] component, I really believe in this, you know, delayed gratification. Like, the
[38:10] know, delayed gratification. Like, the
[38:10] know, delayed gratification. Like, the faster you get your results, like the
[38:11] faster you get your results, like the
[38:11] faster you get your results, like the more
[38:12] more
[38:13] more uh the better the user experience is.
[38:14] uh the better the user experience is.
[38:14] uh the better the user experience is. So, we we really want to do that.
[38:16] So, we we really want to do that.
[38:16] So, we we really want to do that. &gt;&gt; Interesting. And then for the And then
[38:17] &gt;&gt; Interesting. And then for the And then
[38:17] &gt;&gt; Interesting. And then for the And then for the real-time kind of like asking if
[38:19] for the real-time kind of like asking if
[38:19] for the real-time kind of like asking if you if you ask questions, how does that
[38:20] you if you ask questions, how does that
[38:20] you if you ask questions, how does that work? Cuz I imagine it's doing a bunch
[38:22] work? Cuz I imagine it's doing a bunch
[38:22] work? Cuz I imagine it's doing a bunch of tool calling under the hood. Do you
[38:23] of tool calling under the hood. Do you
[38:23] of tool calling under the hood. Do you surface those to the user? Do you hide
[38:25] surface those to the user? Do you hide
[38:25] surface those to the user? Do you hide those? Like how how transparent are you
[38:28] those? Like how how transparent are you
[38:28] those? Like how how transparent are you about the agent's work that it's doing?
[38:30] about the agent's work that it's doing?
[38:30] about the agent's work that it's doing? But now we do show
[38:32] But now we do show
[38:32] But now we do show like an abstracted version. We don't
[38:33] like an abstracted version. We don't
[38:33] like an abstracted version. We don't like our customers don't really care
[38:35] like our customers don't really care
[38:35] like our customers don't really care about what happens under the hood too
[38:36] about what happens under the hood too
[38:36] about what happens under the hood too much, but they do want to see
[38:38] much, but they do want to see
[38:38] much, but they do want to see something's happening and maybe things
[38:39] something's happening and maybe things
[38:39] something's happening and maybe things are like, "Okay, I'm actually now
[38:40] are like, "Okay, I'm actually now
[38:40] are like, "Okay, I'm actually now looking at all the responses again and
[38:42] looking at all the responses again and
[38:42] looking at all the responses again and that's why it might take a while." And
[38:43] that's why it might take a while." And
[38:43] that's why it might take a while." And we have a loading state and all those
[38:44] we have a loading state and all those
[38:44] we have a loading state and all those kind of things.
[38:45] kind of things.
[38:45] kind of things. The more tricky thing there is what
[38:47] The more tricky thing there is what
[38:47] The more tricky thing there is what happens if it now starts writing Python
[38:49] happens if it now starts writing Python
[38:49] happens if it now starts writing Python code. Right? Because in in some way, if
[38:53] code. Right? Because in in some way, if
[38:53] code. Right? Because in in some way, if you ask it a complicated question it
[38:54] you ask it a complicated question it
[38:54] you ask it a complicated question it says, "You know, the answer is 42."
[38:56] says, "You know, the answer is 42."
[38:56] says, "You know, the answer is 42." You're like, "Okay,
[38:58] You're like, "Okay,
[38:58] You're like, "Okay, I guess."
[38:59] I guess."
[38:59] I guess." Uh usually all of our findings are very
[39:02] Uh usually all of our findings are very
[39:02] Uh usually all of our findings are very traceable. Like you can as I said, you
[39:03] traceable. Like you can as I said, you
[39:03] traceable. Like you can as I said, you can click on the numbers, you can see
[39:05] can click on the numbers, you can see
[39:05] can click on the numbers, you can see the breakdown, you can even
[39:06] the breakdown, you can even
[39:06] the breakdown, you can even go down to the individual level of this
[39:08] go down to the individual level of this
[39:08] go down to the individual level of this everyone we classified and why we did it
[39:09] everyone we classified and why we did it
[39:10] everyone we classified and why we did it and can really kind of explore the data.
[39:11] and can really kind of explore the data.
[39:11] and can really kind of explore the data. But the Python,
[39:13] But the Python,
[39:13] But the Python, that's no longer the case.
[39:14] that's no longer the case.
[39:14] that's no longer the case. And at the same time, you know, no one
[39:16] And at the same time, you know, no one
[39:16] And at the same time, you know, no one wants to read Python and in our case our
[39:18] wants to read Python and in our case our
[39:18] wants to read Python and in our case our customers will probably also not
[39:19] customers will probably also not
[39:19] customers will probably also not understand the Python. So, can we make
[39:21] understand the Python. So, can we make
[39:21] understand the Python. So, can we make it can we build the confidence that it's
[39:23] it can we build the confidence that it's
[39:23] it can we build the confidence that it's the right answer? And obviously there's
[39:24] the right answer? And obviously there's
[39:24] the right answer? And obviously there's always been there's always been some
[39:26] always been there's always been some
[39:26] always been there's always been some assumptions going into that. The
[39:28] assumptions going into that. The
[39:28] assumptions going into that. The instructions are never one
[39:30] instructions are never one
[39:30] instructions are never one completely clear. So, you know,
[39:32] completely clear. So, you know,
[39:32] completely clear. So, you know, basically we're
[39:34] basically we're
[39:34] basically we're currently summarizing
[39:35] currently summarizing
[39:35] currently summarizing exactly his assumptions we're taking
[39:37] exactly his assumptions we're taking
[39:37] exactly his assumptions we're taking when we're executing Python in like a
[39:40] when we're executing Python in like a
[39:40] when we're executing Python in like a little box that you can expand and if
[39:42] little box that you can expand and if
[39:42] little box that you can expand and if you want to look at that, but we don't
[39:43] you want to look at that, but we don't
[39:43] you want to look at that, but we don't show you the the raw Python script.
[39:45] show you the the raw Python script.
[39:45] show you the the raw Python script. Which, yeah, is something we're we're
[39:47] Which, yeah, is something we're we're
[39:47] Which, yeah, is something we're we're thinking about. It's It's kind of in the
[39:48] thinking about. It's It's kind of in the
[39:48] thinking about. It's It's kind of in the middle ground. It's not perfect, but it
[39:50] middle ground. It's not perfect, but it
[39:50] middle ground. It's not perfect, but it gives you some confidence that what it
[39:51] gives you some confidence that what it
[39:51] gives you some confidence that what it does is actually right.
[39:52] does is actually right.
[39:52] does is actually right. &gt;&gt; are you how are you summarizing? Is that
[39:54] &gt;&gt; are you how are you summarizing? Is that
[39:54] &gt;&gt; are you how are you summarizing? Is that another LLM call that's like looking at
[39:56] another LLM call that's like looking at
[39:56] another LLM call that's like looking at the trace so far and and generating
[39:58] the trace so far and and generating
[39:59] the trace so far and and generating something?
[39:59] something?
[39:59] something? &gt;&gt; Exactly. So, after the Python code is
[40:00] &gt;&gt; Exactly. So, after the Python code is
[40:00] &gt;&gt; Exactly. So, after the Python code is run, it will like first we show it as a
[40:03] run, it will like first we show it as a
[40:03] run, it will like first we show it as a message just like, you know, running
[40:04] message just like, you know, running
[40:04] message just like, you know, running Python. I don't think I don't think
[40:05] Python. I don't think I don't think
[40:05] Python. I don't think I don't think we're actually saying that anymore.
[40:07] we're actually saying that anymore.
[40:07] we're actually saying that anymore. We're saying like running some
[40:08] We're saying like running some
[40:08] We're saying like running some computations or something. And then
[40:09] computations or something. And then
[40:09] computations or something. And then after it's written the script and while
[40:11] after it's written the script and while
[40:11] after it's written the script and while it's executing the script we actually
[40:12] it's executing the script we actually
[40:12] it's executing the script we actually summarize it
[40:13] summarize it
[40:14] summarize it to have that text and that's more it's
[40:15] to have that text and that's more it's
[40:15] to have that text and that's more it's less for like the status what it's doing
[40:17] less for like the status what it's doing
[40:17] less for like the status what it's doing right now and it's more for you know,
[40:19] right now and it's more for you know,
[40:19] right now and it's more for you know, where does this come from? Let me go
[40:20] where does this come from? Let me go
[40:20] where does this come from? Let me go deeper
[40:21] deeper
[40:21] deeper and look at look at where it comes from.
[40:23] and look at look at where it comes from.
[40:23] and look at look at where it comes from. When you guys are running like these sub
[40:25] When you guys are running like these sub
[40:25] When you guys are running like these sub agents or small LLMs over the 500
[40:27] agents or small LLMs over the 500
[40:27] agents or small LLMs over the 500 documents, what if the documents are
[40:29] documents, what if the documents are
[40:29] documents, what if the documents are like really big or really massive? Do
[40:31] like really big or really massive? Do
[40:31] like really big or really massive? Do you do any chunking there and like
[40:32] you do any chunking there and like
[40:32] you do any chunking there and like further kind of like subsetting the text
[40:35] further kind of like subsetting the text
[40:35] further kind of like subsetting the text and and chunking into three things and
[40:37] and and chunking into three things and
[40:37] and and chunking into three things and then running the small LLM over all
[40:38] then running the small LLM over all
[40:39] then running the small LLM over all three things or do you always just treat
[40:40] three things or do you always just treat
[40:40] three things or do you always just treat it as as one big thing? Yeah. So,
[40:42] it as as one big thing? Yeah. So,
[40:42] it as as one big thing? Yeah. So, there's multiple layers. Our interviews
[40:44] there's multiple layers. Our interviews
[40:44] there's multiple layers. Our interviews are what we call semi-structured. So, we
[40:47] are what we call semi-structured. So, we
[40:47] are what we call semi-structured. So, we have a rough
[40:49] have a rough
[40:49] have a rough idea of what people are talking about.
[40:50] idea of what people are talking about.
[40:50] idea of what people are talking about. So, there's there's different sections
[40:52] So, there's there's different sections
[40:52] So, there's there's different sections that, you know, in this section we'll
[40:53] that, you know, in this section we'll
[40:53] that, you know, in this section we'll talk about, you know, this concept in
[40:55] talk about, you know, this concept in
[40:55] talk about, you know, this concept in this section we talk about this concept
[40:56] this section we talk about this concept
[40:56] this section we talk about this concept or we're talking about different ideas.
[40:58] or we're talking about different ideas.
[40:58] or we're talking about different ideas. And so, we basically interviews are
[41:00] And so, we basically interviews are
[41:00] And so, we basically interviews are annotated that way and we can filter
[41:02] annotated that way and we can filter
[41:02] annotated that way and we can filter through specific relevant sections. So,
[41:04] through specific relevant sections. So,
[41:04] through specific relevant sections. So, that helps. And that filter would be
[41:06] that helps. And that filter would be
[41:06] that helps. And that filter would be part of the filter that you pass into
[41:07] part of the filter that you pass into
[41:07] part of the filter that you pass into like the the main agent would decide,
[41:10] like the the main agent would decide,
[41:10] like the the main agent would decide, you know, for this question we don't
[41:11] you know, for this question we don't
[41:11] you know, for this question we don't need to look at the entire interview, we
[41:12] need to look at the entire interview, we
[41:12] need to look at the entire interview, we just need to look at their background
[41:14] just need to look at their background
[41:14] just need to look at their background information or something like that and
[41:15] information or something like that and
[41:15] information or something like that and then we just cut it to that section.
[41:17] then we just cut it to that section.
[41:18] then we just cut it to that section. It's not perfect, right? Sometimes
[41:19] It's not perfect, right? Sometimes
[41:19] It's not perfect, right? Sometimes people might say like, oh by the way, I
[41:20] people might say like, oh by the way, I
[41:20] people might say like, oh by the way, I forgot like they're very different
[41:22] forgot like they're very different
[41:22] forgot like they're very different setting. I was like, oh I actually
[41:23] setting. I was like, oh I actually
[41:23] setting. I was like, oh I actually forgot.
[41:24] forgot.
[41:25] forgot. I changed my mind, whatever. Again, not
[41:26] I changed my mind, whatever. Again, not
[41:26] I changed my mind, whatever. Again, not perfect, but I think that's that's a
[41:27] perfect, but I think that's that's a
[41:27] perfect, but I think that's that's a pretty reasonable assumption. We do use
[41:29] pretty reasonable assumption. We do use
[41:29] pretty reasonable assumption. We do use some chunking and some retrieval for if
[41:32] some chunking and some retrieval for if
[41:32] some chunking and some retrieval for if you ask a question like, oh did anyone
[41:34] you ask a question like, oh did anyone
[41:34] you ask a question like, oh did anyone mention something like this or can you
[41:35] mention something like this or can you
[41:35] mention something like this or can you find clips where people talk about this
[41:38] find clips where people talk about this
[41:38] find clips where people talk about this specific topic? Then, of course, in
[41:39] specific topic? Then, of course, in
[41:39] specific topic? Then, of course, in theory we could run this, you know, map
[41:41] theory we could run this, you know, map
[41:41] theory we could run this, you know, map reduce function call over all of them,
[41:43] reduce function call over all of them,
[41:43] reduce function call over all of them, but in practice it's usually hard, but
[41:45] but in practice it's usually hard, but
[41:45] but in practice it's usually hard, but especially if you're going to like the
[41:46] especially if you're going to like the
[41:46] especially if you're going to like the thousands and tens of thousands
[41:47] thousands and tens of thousands
[41:47] thousands and tens of thousands interviews, you use a retrieval like a
[41:49] interviews, you use a retrieval like a
[41:50] interviews, you use a retrieval like a semantic search on chunking. We do some
[41:52] semantic search on chunking. We do some
[41:52] semantic search on chunking. We do some hierarchical
[41:53] hierarchical
[41:53] hierarchical summarizations as well
[41:55] summarizations as well
[41:55] summarizations as well for this extraction step because
[41:56] for this extraction step because
[41:56] for this extraction step because sometimes, you know, if you if you
[41:58] sometimes, you know, if you if you
[41:58] sometimes, you know, if you if you imagine you're doing like a a thousand,
[42:00] imagine you're doing like a a thousand,
[42:00] imagine you're doing like a a thousand, you know, summaries on individual
[42:01] you know, summaries on individual
[42:01] you know, summaries on individual interviews, that's still a thousand
[42:02] interviews, that's still a thousand
[42:02] interviews, that's still a thousand times maybe 200 tokens. That's still a
[42:05] times maybe 200 tokens. That's still a
[42:05] times maybe 200 tokens. That's still a lot of text.
[42:06] lot of text.
[42:06] lot of text. So, then we're actually using like
[42:07] So, then we're actually using like
[42:07] So, then we're actually using like another layer to summarize that. How has
[42:10] another layer to summarize that. How has
[42:10] another layer to summarize that. How has your use of retrieval changed over time?
[42:12] your use of retrieval changed over time?
[42:12] your use of retrieval changed over time? So, it has to change a lot. We're still
[42:14] So, it has to change a lot. We're still
[42:14] So, it has to change a lot. We're still using retrieval.
[42:16] using retrieval.
[42:16] using retrieval. Again, like the first version of the
[42:17] Again, like the first version of the
[42:17] Again, like the first version of the research agent we built like 2 years
[42:18] research agent we built like 2 years
[42:18] research agent we built like 2 years ago, it was just a rack. I just say
[42:21] ago, it was just a rack. I just say
[42:21] ago, it was just a rack. I just say semantic search and then the second
[42:23] semantic search and then the second
[42:23] semantic search and then the second thing we added was can we add some
[42:25] thing we added was can we add some
[42:25] thing we added was can we add some robust filters? Can we just if you ask
[42:26] robust filters? Can we just if you ask
[42:27] robust filters? Can we just if you ask can we just filter for man like we
[42:28] can we just filter for man like we
[42:28] can we just filter for man like we extract metadata we filter based on
[42:29] extract metadata we filter based on
[42:30] extract metadata we filter based on that.
[42:31] that.
[42:31] that. That was the first version. The second
[42:32] That was the first version. The second
[42:32] That was the first version. The second version we like okay, we saw all the
[42:33] version we like okay, we saw all the
[42:33] version we like okay, we saw all the problems and we actually completely
[42:34] problems and we actually completely
[42:35] problems and we actually completely moved away from retrieval. We were only
[42:36] moved away from retrieval. We were only
[42:36] moved away from retrieval. We were only doing these like small LLMs looking at
[42:37] doing these like small LLMs looking at
[42:37] doing these like small LLMs looking at everything. We didn't have any retrieval
[42:39] everything. We didn't have any retrieval
[42:39] everything. We didn't have any retrieval pipeline there at all. But then we
[42:41] pipeline there at all. But then we
[42:41] pipeline there at all. But then we realized for some cases again especially
[42:43] realized for some cases again especially
[42:43] realized for some cases again especially if you're just scaling to larger
[42:44] if you're just scaling to larger
[42:44] if you're just scaling to larger samples, it's still useful and it's
[42:46] samples, it's still useful and it's
[42:46] samples, it's still useful and it's sometimes faster and in some cases it's
[42:48] sometimes faster and in some cases it's
[42:48] sometimes faster and in some cases it's better. But it's definitely less
[42:50] better. But it's definitely less
[42:50] better. But it's definitely less critical than it used to be. But even if
[42:51] critical than it used to be. But even if
[42:51] critical than it used to be. But even if it's not that critical it still means we
[42:53] it's not that critical it still means we
[42:53] it's not that critical it still means we embed everything and you know the cost
[42:55] embed everything and you know the cost
[42:55] embed everything and you know the cost is not um
[42:56] is not um
[42:56] is not um not prohibitive so we just do that and
[42:59] not prohibitive so we just do that and
[42:59] not prohibitive so we just do that and especially if you're if you're you know,
[43:00] especially if you're if you're you know,
[43:00] especially if you're if you're you know, we're working towards a platform where
[43:02] we're working towards a platform where
[43:02] we're working towards a platform where you can search to all of your findings
[43:04] you can search to all of your findings
[43:04] you can search to all of your findings not not scope to a specific product but
[43:06] not not scope to a specific product but
[43:06] not not scope to a specific product but kind of over time. And then of course
[43:08] kind of over time. And then of course
[43:08] kind of over time. And then of course the data, you know, becomes much like a
[43:10] the data, you know, becomes much like a
[43:10] the data, you know, becomes much like a much larger corpus and and then I think
[43:11] much larger corpus and and then I think
[43:11] much larger corpus and and then I think retrieval will continue to be important.
[43:13] retrieval will continue to be important.
[43:13] retrieval will continue to be important. I know the coding in the coding world
[43:15] I know the coding in the coding world
[43:15] I know the coding in the coding world it's you know, people now just use you
[43:17] it's you know, people now just use you
[43:17] it's you know, people now just use you know, keyword search or grep. Have you
[43:19] know, keyword search or grep. Have you
[43:19] know, keyword search or grep. Have you implemented that over your transcript?
[43:20] implemented that over your transcript?
[43:21] implemented that over your transcript? So, we haven't really implemented that.
[43:22] So, we haven't really implemented that.
[43:22] So, we haven't really implemented that. I think the the main thing is in code I
[43:24] I think the the main thing is in code I
[43:24] I think the the main thing is in code I guess you have symbols that are like
[43:26] guess you have symbols that are like
[43:26] guess you have symbols that are like types like it's strongly typed and you
[43:28] types like it's strongly typed and you
[43:28] types like it's strongly typed and you can actually search for exactly that
[43:29] can actually search for exactly that
[43:29] can actually search for exactly that string. In like a natural conversation
[43:32] string. In like a natural conversation
[43:32] string. In like a natural conversation it's much harder. If you want to think
[43:34] it's much harder. If you want to think
[43:34] it's much harder. If you want to think if you if you want to retrieve all cases
[43:35] if you if you want to retrieve all cases
[43:36] if you if you want to retrieve all cases where people are frustrated, that's
[43:37] where people are frustrated, that's
[43:37] where people are frustrated, that's maybe a semantic search but it's like
[43:38] maybe a semantic search but it's like
[43:38] maybe a semantic search but it's like really hard to
[43:39] really hard to
[43:39] really hard to I'm sure you can search for a list of
[43:41] I'm sure you can search for a list of
[43:41] I'm sure you can search for a list of adjective adjectives that people might
[43:43] adjective adjectives that people might
[43:43] adjective adjectives that people might have used but
[43:44] have used but
[43:44] have used but it's really hard. So, in our case we're
[43:46] it's really hard. So, in our case we're
[43:46] it's really hard. So, in our case we're just sticking with the regular
[43:48] just sticking with the regular
[43:48] just sticking with the regular retrieval. On a completely different
[43:50] retrieval. On a completely different
[43:50] retrieval. On a completely different note, what what does the team that does
[43:52] note, what what does the team that does
[43:52] note, what what does the team that does all this agent engineering look like for
[43:54] all this agent engineering look like for
[43:54] all this agent engineering look like for you guys? It's engineers right now.
[43:57] you guys? It's engineers right now.
[43:57] you guys? It's engineers right now. We're relatively small team but one
[43:58] We're relatively small team but one
[43:58] We're relatively small team but one thing I look for in in hiring engineers
[44:01] thing I look for in in hiring engineers
[44:01] thing I look for in in hiring engineers is kind of this product sense because I
[44:03] is kind of this product sense because I
[44:03] is kind of this product sense because I think what there's maybe like have types
[44:05] think what there's maybe like have types
[44:05] think what there's maybe like have types of engineers that do well in this this
[44:07] of engineers that do well in this this
[44:07] of engineers that do well in this this world. I think there's one that is like
[44:08] world. I think there's one that is like
[44:08] world. I think there's one that is like really good at building large scale
[44:10] really good at building large scale
[44:10] really good at building large scale systems and I have seen that have a good
[44:12] systems and I have seen that have a good
[44:12] systems and I have seen that have a good taste and maybe there's something that
[44:14] taste and maybe there's something that
[44:14] taste and maybe there's something that at Lambs at least right now can't do
[44:15] at Lambs at least right now can't do
[44:15] at Lambs at least right now can't do super well.
[44:16] super well.
[44:16] super well. And then the other side the other side
[44:18] And then the other side the other side
[44:18] And then the other side the other side is these, you know, product engineers
[44:19] is these, you know, product engineers
[44:19] is these, you know, product engineers that really, you know, understand the
[44:21] that really, you know, understand the
[44:21] that really, you know, understand the customer, iterate fast, and you know,
[44:24] customer, iterate fast, and you know,
[44:24] customer, iterate fast, and you know, try out things. I think
[44:25] try out things. I think
[44:25] try out things. I think it's super hard to whiteboard this is
[44:27] it's super hard to whiteboard this is
[44:27] it's super hard to whiteboard this is how the agent's going to work. And you
[44:29] how the agent's going to work. And you
[44:29] how the agent's going to work. And you know, these are going to be the problems
[44:30] know, these are going to be the problems
[44:30] know, these are going to be the problems and this is how it's going to work. You
[44:31] and this is how it's going to work. You
[44:31] and this is how it's going to work. You you have you need some part of that. You
[44:32] you have you need some part of that. You
[44:32] you have you need some part of that. You need to have some some idea of where you
[44:34] need to have some some idea of where you
[44:34] need to have some some idea of where you want to go, but then you need to try out
[44:36] want to go, but then you need to try out
[44:36] want to go, but then you need to try out things. How reliable is it? And you need
[44:38] things. How reliable is it? And you need
[44:38] things. How reliable is it? And you need to adapt. And for that, I think it's
[44:40] to adapt. And for that, I think it's
[44:40] to adapt. And for that, I think it's very important that the engineer itself
[44:42] very important that the engineer itself
[44:42] very important that the engineer itself is the one that that is evaluating, that
[44:44] is the one that that is evaluating, that
[44:44] is the one that that is evaluating, that is talking to the customer, and and and
[44:46] is talking to the customer, and and and
[44:46] is talking to the customer, and and and hearing how it's going, looking at the
[44:48] hearing how it's going, looking at the
[44:48] hearing how it's going, looking at the logs and the traces themselves. You
[44:49] logs and the traces themselves. You
[44:49] logs and the traces themselves. You mentioned you see is someone else
[44:51] mentioned you see is someone else
[44:51] mentioned you see is someone else looking at the logs. No, it's actually
[44:52] looking at the logs. No, it's actually
[44:52] looking at the logs. No, it's actually the person that that built the system
[44:53] the person that that built the system
[44:53] the person that that built the system that's looking at the logs and trying to
[44:55] that's looking at the logs and trying to
[44:55] that's looking at the logs and trying to understand does the model do what I want
[44:57] understand does the model do what I want
[44:57] understand does the model do what I want it to do. And I don't really believe in
[44:59] it to do. And I don't really believe in
[44:59] it to do. And I don't really believe in people that just prompt like just write
[45:02] people that just prompt like just write
[45:02] people that just prompt like just write the prompt because
[45:05] the prompt because
[45:05] the prompt because again, it's a very nuanced nuanced thing
[45:06] again, it's a very nuanced nuanced thing
[45:06] again, it's a very nuanced nuanced thing of yeah, if you change the prompt, then
[45:08] of yeah, if you change the prompt, then
[45:08] of yeah, if you change the prompt, then you also need to change the tools and
[45:09] you also need to change the tools and
[45:09] you also need to change the tools and then all the tools you need to
[45:10] then all the tools you need to
[45:10] then all the tools you need to understand you know, that some of part
[45:12] understand you know, that some of part
[45:12] understand you know, that some of part of the infrastructure and and so on. So,
[45:15] of the infrastructure and and so on. So,
[45:15] of the infrastructure and and so on. So, I think this end-to-end ownership is how
[45:16] I think this end-to-end ownership is how
[45:16] I think this end-to-end ownership is how we've been building the product and I
[45:17] we've been building the product and I
[45:17] we've been building the product and I think that's where I think it's going to
[45:20] think that's where I think it's going to
[45:20] think that's where I think it's going to stay the same even as we grow from the
[45:22] stay the same even as we grow from the
[45:22] stay the same even as we grow from the team. Do you have any non-engineers
[45:25] team. Do you have any non-engineers
[45:25] team. Do you have any non-engineers contributing to the agent, whether
[45:26] contributing to the agent, whether
[45:26] contributing to the agent, whether that's a product person or design or
[45:29] that's a product person or design or
[45:30] that's a product person or design or some subject matter expert? I don't
[45:31] some subject matter expert? I don't
[45:32] some subject matter expert? I don't know. Not directly. So, I think
[45:35] know. Not directly. So, I think
[45:35] know. Not directly. So, I think the problem I see is
[45:36] the problem I see is
[45:36] the problem I see is it's relatively easy to change something
[45:38] it's relatively easy to change something
[45:38] it's relatively easy to change something like the prompt that like, oh yeah, just
[45:39] like the prompt that like, oh yeah, just
[45:39] like the prompt that like, oh yeah, just add a sentence to the prompt, you know,
[45:41] add a sentence to the prompt, you know,
[45:41] add a sentence to the prompt, you know, and people definitely want to do that.
[45:43] and people definitely want to do that.
[45:43] and people definitely want to do that. But then from my perspective, I'm like,
[45:45] But then from my perspective, I'm like,
[45:45] But then from my perspective, I'm like, okay, sure, it's easy to change it, but
[45:46] okay, sure, it's easy to change it, but
[45:46] okay, sure, it's easy to change it, but what about the validation? Who's
[45:47] what about the validation? Who's
[45:48] what about the validation? Who's actually going to take the blame? And if
[45:49] actually going to take the blame? And if
[45:49] actually going to take the blame? And if it if it breaks, who's actually going to
[45:50] it if it breaks, who's actually going to
[45:50] it if it breaks, who's actually going to fix it?
[45:51] fix it?
[45:51] fix it? Um I don't know. Like the number of PRs
[45:53] Um I don't know. Like the number of PRs
[45:53] Um I don't know. Like the number of PRs we have in our in our organization has
[45:55] we have in our in our organization has
[45:55] we have in our in our organization has exploded. Like it's so easy to write
[45:57] exploded. Like it's so easy to write
[45:57] exploded. Like it's so easy to write code and everyone is like, oh, can I go
[45:58] code and everyone is like, oh, can I go
[45:58] code and everyone is like, oh, can I go get into the code and and write code?
[46:00] get into the code and and write code?
[46:00] get into the code and and write code? But, you know, I don't want the
[46:01] But, you know, I don't want the
[46:01] But, you know, I don't want the engineers to just be the ones that, you
[46:03] engineers to just be the ones that, you
[46:03] engineers to just be the ones that, you know, review code and approve changes
[46:04] know, review code and approve changes
[46:04] know, review code and approve changes and then later on the ones that fixing
[46:06] and then later on the ones that fixing
[46:06] and then later on the ones that fixing it. I think that's that's a little bit
[46:07] it. I think that's that's a little bit
[46:07] it. I think that's that's a little bit of the problem that I see. And we're
[46:09] of the problem that I see. And we're
[46:09] of the problem that I see. And we're obviously working closely with, you
[46:11] obviously working closely with, you
[46:11] obviously working closely with, you know, customer-facing um people and
[46:13] know, customer-facing um people and
[46:13] know, customer-facing um people and we're getting feedback, but then it's
[46:14] we're getting feedback, but then it's
[46:14] we're getting feedback, but then it's typically the engineer that will
[46:16] typically the engineer that will
[46:16] typically the engineer that will consolidate with that with all the other
[46:18] consolidate with that with all the other
[46:18] consolidate with that with all the other requirements and and try to improve that
[46:20] requirements and and try to improve that
[46:20] requirements and and try to improve that and then get feedback from them again.
[46:22] and then get feedback from them again.
[46:22] and then get feedback from them again. Do you care if people joining the the
[46:24] Do you care if people joining the the
[46:24] Do you care if people joining the the agent engineering team or the team that
[46:26] agent engineering team or the team that
[46:26] agent engineering team or the team that works at Do they have to have previous
[46:27] works at Do they have to have previous
[46:28] works at Do they have to have previous kind of like AI or agent experience or
[46:30] kind of like AI or agent experience or
[46:30] kind of like AI or agent experience or is that something that, hey, if you're
[46:32] is that something that, hey, if you're
[46:32] is that something that, hey, if you're like a good software engineer, I think
[46:34] like a good software engineer, I think
[46:34] like a good software engineer, I think you can pick this up on the fly? I
[46:36] you can pick this up on the fly? I
[46:36] you can pick this up on the fly? I changed my mind a little bit on that. Um
[46:38] changed my mind a little bit on that. Um
[46:38] changed my mind a little bit on that. Um maybe like a year ago I was like, we
[46:39] maybe like a year ago I was like, we
[46:39] maybe like a year ago I was like, we just want very smart people and if they
[46:41] just want very smart people and if they
[46:41] just want very smart people and if they haven't worked with AI, I think that's
[46:42] haven't worked with AI, I think that's
[46:42] haven't worked with AI, I think that's that's fine, they can learn that. Now I
[46:44] that's fine, they can learn that. Now I
[46:44] that's fine, they can learn that. Now I think we're at the time where like it's
[46:45] think we're at the time where like it's
[46:45] think we're at the time where like it's a bit strange if you've never worked
[46:47] a bit strange if you've never worked
[46:47] a bit strange if you've never worked with AI. It's been like 3 and 1/2 years
[46:49] with AI. It's been like 3 and 1/2 years
[46:49] with AI. It's been like 3 and 1/2 years now.
[46:49] now.
[46:49] now. &gt;&gt; Exactly, right? Or like or even if you
[46:51] &gt;&gt; Exactly, right? Or like or even if you
[46:51] &gt;&gt; Exactly, right? Or like or even if you haven't worked on your job because like
[46:52] haven't worked on your job because like
[46:52] haven't worked on your job because like for whatever reason your company, you
[46:54] for whatever reason your company, you
[46:54] for whatever reason your company, you know, you're not doing it like you
[46:55] know, you're not doing it like you
[46:55] know, you're not doing it like you should at least be intellectually
[46:57] should at least be intellectually
[46:57] should at least be intellectually interested and curious about how does it
[46:59] interested and curious about how does it
[46:59] interested and curious about how does it work behind the scenes and
[47:01] work behind the scenes and
[47:01] work behind the scenes and build something on the side or kind of
[47:02] build something on the side or kind of
[47:02] build something on the side or kind of at least know what is Claude doing if
[47:04] at least know what is Claude doing if
[47:04] at least know what is Claude doing if I'm asking it to kind of build my
[47:06] I'm asking it to kind of build my
[47:07] I'm asking it to kind of build my PowerPoint, like how does it actually
[47:08] PowerPoint, like how does it actually
[47:08] PowerPoint, like how does it actually build that? Uh so I think if you don't
[47:10] build that? Uh so I think if you don't
[47:11] build that? Uh so I think if you don't at least have that level of experience,
[47:12] at least have that level of experience,
[47:12] at least have that level of experience, I think, you know, it's no longer it's
[47:14] I think, you know, it's no longer it's
[47:14] I think, you know, it's no longer it's no longer a fit. Yeah, I think I'm kind
[47:16] no longer a fit. Yeah, I think I'm kind
[47:16] no longer a fit. Yeah, I think I'm kind of the same way. I also updated some
[47:18] of the same way. I also updated some
[47:18] of the same way. I also updated some beliefs in that way. I think that's
[47:19] beliefs in that way. I think that's
[47:19] beliefs in that way. I think that's great. Awesome. Thank you for that.
[47:21] great. Awesome. Thank you for that.
[47:21] great. Awesome. Thank you for that. Thanks for listening to Max Agency. If
[47:23] Thanks for listening to Max Agency. If
[47:24] Thanks for listening to Max Agency. If you liked this episode, leave a review
[47:26] you liked this episode, leave a review
[47:26] you liked this episode, leave a review and subscribe. Send feedback or
[47:28] and subscribe. Send feedback or
[47:28] and subscribe. Send feedback or questions to maxagency@langchain.dev.
[47:31] questions to maxagency@langchain.dev.
[47:31] questions to maxagency@langchain.dev. We want to hear from you.
