# AI Agents for SQL and Databases in DataGrip

- **Video:** https://www.youtube.com/watch?v=QuQWOww0JNs
- **Generated:** 2026-08-31 20:58 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The material demonstrates **JetBrains DataGrip with an AI Assistant/agent** embedded in a database IDE. The demonstrated capabilities include natural-language SQL generation, database/schema exploration, query-history recap, stored-routine analysis, candidate schema cleanup, and local CSV data-quality assessment.

The most important pattern is an AI assistant that can access database metadata and, when explicitly permitted, query data or execute potentially modifying operations. The demo shows **granular permissions**—including separate schema-metadata and data-read access—and a confirmation step before destructive actions. It also treats stored-routine execution as a modification-risk operation because a routine’s side effects cannot be safely inferred.

For Superior Propane, this is best evaluated as a **developer and data-engineering productivity tool**, not as a replacement for Databricks, Azure AI Foundry, Microsoft Purview, or enterprise data-quality controls. Potential value includes faster legacy-schema discovery, SQL migration assessment, initial data profiling, data-quality rule discovery, and documentation. Durable production controls should remain in the governed Azure/Databricks platform.

The strongest near-term use case is a constrained, read-only pilot using **schema metadata and masked/non-sensitive development data**. AI findings should be treated as hypotheses and converted into deterministic, tested rules in Databricks only after review by data owners and domain SMEs.

> **Scope note:** The supplied summaries do not establish a DataGrip integration with Databricks, Azure networking/identity, Unity Catalog, Azure AI Foundry, Microsoft Purview, or Azure OpenAI. Those capabilities must not be assumed.

---

# Technical details

## DataGrip AI interaction model

### Natural-language SQL generation and execution

**Speaker demonstration / claim**
- The agent generated a read query, automatically executed it when permitted, returned an answer, and explained the query logic.
- Generated SQL can also be copied into DataGrip’s normal query console for inspection or manual execution.

**Architecture and operational behavior implied**
- The AI assistant is integrated into the DataGrip IDE and can invoke database-query capabilities.
- The standard query console remains distinct from the AI chat interface.
- Automatic execution is permission-based rather than necessarily always enabled.

**Operational trade-off**
- Natural-language-to-SQL can speed up ad hoc investigation and onboarding to unfamiliar schemas.
- However, even “read-only” AI-generated queries can:
  - Scan large tables and create database or warehouse cost.
  - Return sensitive records.
  - Introduce load on operational databases.
  - Use incorrect joins or filters while appearing plausible.

For enterprise usage, read operations should still be subject to connection restrictions, query timeouts, result-size limits, and non-production defaults.

---

## Permission model: schema metadata versus table data

**Speaker demonstration / claim**
- Permissions are managed through **IDE Settings → Database → AI Tools**.
- The agent has separately configurable permissions for:
  - **Read database data**
  - **Read database schemas**

**Practical distinction**
- Schema permission is described as access to metadata such as schemas, object names, and structure, without accessing actual table records.
- Data-read permission enables the agent to retrieve data/query results.

**Superior Propane governance implication**
- A **schema-only default** is the most defensible initial configuration. It can support:
  - Documentation generation.
  - SQL drafting.
  - Object and dependency exploration.
  - Legacy-system discovery.
  - Migration-readiness analysis.
- Data-read access should be restricted to approved identities, environments, and datasets—particularly because customer, service-location, billing, payment, tank/telemetry, employee, and pricing information may be sensitive.

The transcript does not establish whether these IDE settings can be centrally enforced through enterprise policy, rather than user-by-user configuration. That is a key validation item.

---

## Schema cleanup and destructive DDL workflow

**Speaker demonstration / claim**
- The presenter asks the AI to identify tables that do not belong in a Sakila sample schema.
- The agent identifies core versus outlier tables and explains its reasoning.
- When asked to delete unwanted tables, it checks at least for view and foreign-key dependencies.
- It generates `DROP TABLE` statements, requests confirmation, executes after approval, and summarizes the outcome.

**Demonstrated sequence**
1. Inspect schema and object metadata.
2. Infer which objects are anomalous.
3. Receive a cleanup request from the user.
4. Check dependencies, including views and foreign keys.
5. Generate DDL.
6. Ask for confirmation.
7. Execute only after user approval.
8. Report the result.

**Important limitation**
- The determination that a table “does not belong” is an AI inference. It was performed against a familiar sample schema and should not be considered reliable evidence that an enterprise table is unused or safe to delete.
- Checking foreign keys and views does not prove the absence of:
  - Application dependencies.
  - ETL/ELT pipeline references.
  - BI/reporting dependencies.
  - External service integrations.
  - Dynamic SQL.
  - Undocumented manual processes.
  - Downstream data extracts.

**Recommended enterprise posture**
- Do not permit AI-driven DDL or DML in production.
- Do not rely on an IDE confirmation dialog as a substitute for change management.
- Keep schema change deployment in migration-as-code and CI/CD processes.
- Require:
  - Separate credentials per environment.
  - Read-only roles by default.
  - Database-native RBAC.
  - Approved change tickets and review.
  - Tested backup/restore procedures.
  - Authoritative database audit logs.

---

## Query-history recap and auditability

**Speaker demonstration / claim**
- The user asks the assistant to list queries run over the last two days.
- The assistant returns a comprehensive recap, mostly corresponding to actions shown in the video.

**Potential value**
- Conversational activity recap could help developers understand:
  - What the agent executed.
  - Which changes were made.
  - The sequence of investigation steps.
  - How a database state may have been reached.

**Not established by the transcript**
- Whether history is stored locally in DataGrip, in a JetBrains/AI service, or retrieved from database query/audit logs.
- Whether it includes manual SQL, AI-generated SQL only, or both.
- Retention period, immutability, completeness, or exportability.
- Attribution model: individual user, service account, AI agent, or shared connection.
- Whether history can be centralized in an enterprise SIEM or observability platform.

For security investigations, compliance, and operational recovery, Superior Propane should treat **database-native and Azure-native audit sources** as authoritative—not an AI chat summary.

---

## Explicit object references using `@` mentions

**Speaker demonstration / claim**
- DataGrip allows database objects and local files to be explicitly referenced using `@` mentions.
- The presenter selects a stored routine, `get_customer_balance`, using an `@DB object` workflow and code completion.

**Practical benefit**
- Explicit object references reduce ambiguity in prompts.
- Likely useful for:
  - Explaining stored procedures or functions.
  - SQL code review.
  - Dependency exploration.
  - Migration assessment.
  - Technical documentation.
  - Refactoring analysis.

**Limitation**
- Providing precise context does not make generated explanations authoritative. The assistant can still misunderstand business semantics, miss dependencies, or hallucinate explanations.

---

## Stored-routine analysis and execution risk

**Speaker demonstration / claim**
- The agent analyzes a stored routine’s signature, behavior, return value, and notable implementation details.
- It asks permission before executing the procedure.
- Routine execution is categorized as requiring **modify data** permission because DataGrip cannot guarantee what a routine does internally.

**Established safety principle**
Treating unknown routine execution as a modification risk is sound. Procedures and functions may:
- Write data.
- Alter schema or session state.
- Call other routines with side effects.
- Trigger integrations.
- Create long-running workloads.
- Produce unexpected transactional behavior.

**Migration-defect example**
- The assistant identifies syntax it characterizes as MySQL-specific within a PostgreSQL procedure.
- It suggests the routine may have been incompletely migrated from the original Sakila database, including a likely need to convert logic to PostgreSQL-compatible `CASE WHEN` syntax.

**What requires validation**
- The presence of dialect-specific syntax is a candidate finding.
- The causal explanation—an incomplete MySQL-to-PostgreSQL migration—is an inference and must be verified by engineers.
- AI analysis should not replace:
  - SQL parsing and linting.
  - Database-native compilation.
  - Unit and regression tests.
  - Formal migration tooling.
  - Performance testing.

---

## Local-file analysis and CSV data-quality assessment

**Speaker demonstration / claim**
- The DataGrip Files tool window can attach and browse local directories.
- A local CSV file, `housing2.csv`, is referenced in AI chat using an `@` mention.
- The AI identifies data-quality issues, and the demo notes the analysis is a “heavy” task with noticeable processing time.

**Issues identified in the example**
- Physical-line and line-ending concerns.
- Column names containing spaces and periods.
- No apparent primary key or row identifier.
- Four records where bedroom count exceeded room count, described as semantically impossible.
- Mixed data granularity across rows, though the transcript does not define the exact grain inconsistency.

### Data-engineering implications of those findings

| Finding | Technical impact | Typical remediation |
|---|---|---|
| Spaces/periods in column names | Requires quoted identifiers in many SQL dialects; hurts portability and maintainability | Normalize curated fields to lowercase `snake_case`; retain raw names only where required |
| No primary key | Risks duplicates, ambiguous joins, weak lineage, and poor merge/upsert logic | Establish business/natural key, composite key, or surrogate key; document deduplication rules |
| Bedrooms > rooms | Cross-field semantic invalidity | Implement deterministic validation rule and exception handling |
| Mixed grain | Can create duplicate counts, incorrect joins, misleading aggregates, and unreliable ML features | Explicitly declare table grain; separate transactional, snapshot, event, and aggregate data |
| Line-ending/formatting problems | Can break ingestion or cause malformed-row handling differences | Standardize file parsing, encoding, delimiter, and newline expectations |

**Critical security issue**
The transcript does not say what local-file content is transmitted to the AI service, retained, logged, or used for model improvement. Referencing a file could expose data or excerpts of data depending on implementation.

Files containing customer, location, billing, payment, operational, telemetry, supplier, pricing, or employee information should not be used until vendor data-handling controls have passed security, privacy, and legal review.

---

## Data-quality and modeling workflow

The video supports an AI-assisted **initial profiling** workflow, not a production-grade data-quality platform.

A suitable governance pattern would be:

1. Ingest source data into a controlled landing/Bronze zone.
2. Use automated profiling and, where approved, AI-assisted discovery on masked or non-sensitive samples.
3. Capture findings in a reusable assessment artifact:
   - Source and owner.
   - Declared grain.
   - Candidate keys.
   - Sensitive-data classification.
   - Naming issues.
   - Data-quality hypotheses.
   - Required remediation.
   - Accepted business exceptions.
4. Have data stewards and source-system owners validate findings.
5. Encode approved rules as deterministic controls in Databricks SQL/PySpark pipelines.
6. Monitor rule failures, quarantine exceptions where appropriate, and retain lineage/audit records.

---

# Potential applications for Superior Propane

## 1. Schema discovery and legacy-system documentation

Use schema-only access to help data engineers and developers understand operational systems and legacy databases.

Potential uses:
- Explain tables, views, and stored procedures.
- Generate first-pass technical documentation.
- Identify likely relationships and object dependencies.
- Accelerate onboarding for teams supporting poorly documented systems.
- Translate database structures into business-readable summaries for product owners and data stewards.

This is especially relevant where source-system semantics and lineage are incomplete, but outputs should be reviewed before becoming documentation of record.

---

## 2. SQL migration and modernization assessment

The demonstrated MySQL/PostgreSQL issue suggests a useful role in legacy SQL inventory and modernization work.

Potential uses:
- Flag candidate dialect-specific syntax.
- Identify suspicious routines, stored procedures, functions, and deprecated SQL patterns.
- Create an inventory of procedures requiring human review.
- Draft candidate remediation approaches.
- Explain complex joins and legacy logic.

For Superior Propane, this could support migration from legacy operational databases toward Azure-hosted data services or lakehouse-oriented architectures. It should be paired with formal linting, compilation, CI testing, and regression validation.

---

## 3. Data intake and source onboarding into Databricks

AI can accelerate early assessment of source datasets from vendors, operational systems, acquired entities, spreadsheets, or manual extracts.

Potential first-pass checks:
- Nonstandard or ambiguous column names.
- Missing identifiers and candidate keys.
- Likely duplicate patterns.
- Basic null/type/range issues.
- Cross-field contradictions.
- Candidate PII or sensitive fields.
- Suspected mixed grain.
- Potential ingestion blockers, such as malformed rows or line-ending inconsistencies.

**Databricks implementation implication**
- Use AI for discovery only.
- Convert approved findings into repeatable Bronze-to-Silver validation logic using Databricks SQL and/or PySpark.
- Promote only validated and documented data structures to curated Silver/Gold layers and AI-ready datasets.

---

## 4. Propane-specific data-quality rule discovery

The “bedrooms greater than rooms” example generalizes to domain-specific cross-field rules.

Candidate areas to explore with business owners:
- Delivery quantity exceeding plausible tank capacity.
- Negative consumption or delivery volumes where operationally invalid.
- Delivery timestamps preceding order creation, customer activation, or service-point activation.
- Contradictory account, service-point, or tank assignment statuses.
- Multiple active tank/service assignments at a location where business process permits only one.
- Incompatible grain in analytical data—for example, hourly telemetry combined with monthly consumption aggregates in a single fact table.
- Duplicate delivery events across dispatch, billing, and telemetry feeds.

AI may help propose rules, but supply, operations, billing, safety, and customer-service owners must approve:
- Rule definitions.
- Valid exceptions.
- Severity classifications.
- Quarantine/rejection/correction behavior.
- Historical and late-arriving-data treatment.

---

## 5. Developer productivity in non-production environments

A constrained AI assistant can help with:
- Drafting read-only SQL.
- Explaining unfamiliar datasets.
- Investigating data anomalies.
- Reviewing query structure.
- Detecting possible Cartesian joins or duplicate join paths.
- Creating preliminary data-model documentation.
- Reviewing local, sanitized test files before ingestion development.

Recommended boundary: permit this only in sandbox/development environments with read-only or narrowly scoped credentials.

---

## 6. Relationship to Azure AI Foundry, Azure, and Databricks

The transcript does **not** demonstrate:
- Databricks SQL Warehouses, notebooks, jobs, Delta Lake, Delta Live Tables, Unity Catalog, or Databricks lineage/governance.
- Azure networking, Private Link, Azure Key Vault, Azure Monitor, Microsoft Entra ID, or Microsoft Purview.
- Azure AI Foundry model deployments, agent services, prompt flow, evaluations, content safety, or governance.
- Azure OpenAI or private model-endpoint integration.

Therefore:
- DataGrip AI should be assessed as an **IDE-level assistant**.
- It should not be assumed to meet Superior Propane’s Azure AI architecture, networking, identity, or governance standards.
- If approved for enterprise usage, determine whether it can route requests through an approved enterprise model/provider and whether this satisfies internal data-handling requirements.

---

# Risks and validation questions

## Data confidentiality, model routing, and retention

The primary unanswered question is what information leaves the developer workstation and database environment.

Validate:
- What is sent when a user references:
  - A schema.
  - A database object.
  - A query.
  - Query results.
  - A stored-procedure definition.
  - A local file.
- Whether full data, samples, metadata, or only selected excerpts are transmitted.
- Model provider(s), hosting region, tenant isolation, and residency.
- Prompt/result retention periods.
- Whether content is used for service improvement or model training.
- Encryption in transit and at rest.
- Ability to use an approved enterprise model endpoint or restrict model providers.
- Enterprise SSO, administrator controls, and policy enforcement.

Do not expose customer, location, billing, payment, tank/telemetry, employee, or commercially sensitive files until these questions are resolved.

---

## Identity, credentials, and authorization

Validate:
- Whether the agent acts under the developer’s database credentials, a separate service identity, or another model.
- Whether it fully honors:
  - Database RBAC.
  - Row-level security.
  - Column-level masking.
  - Environment separation.
  - Network access restrictions.
- Where and how connection secrets are stored locally.
- Whether administrator policies can centrally enforce permission settings.
- Whether users can bypass controls through local IDE configuration.

The safe baseline is database-native least privilege; an AI UI permission should not be treated as the primary security control.

---

## Execution safety and change management

Validate whether DataGrip can centrally disable or constrain:
- Automatic query execution.
- Data-read access.
- Routine execution.
- DML and DDL execution.
- Local-file access.
- Cross-database queries.
- Expensive full scans.
- Long-running statements.
- Large result sets.

Also determine:
- Whether confirmation is mandatory and whether it can be bypassed.
- Whether the tool distinguishes read queries, DML, DDL, stored-routine execution, privileged operations, and external calls.
- Availability of timeouts, cost thresholds, result-size limits, and environment-specific policies.

Production database modifications should continue through approved CI/CD and change-management paths.

---

## Auditability and operational governance

Validate whether AI activity logs include:
- User identity.
- Database connection/environment.
- Prompt text.
- Referenced objects/files.
- Generated SQL.
- Final executed SQL.
- Execution timestamp, duration, status, and result metadata.
- Approval/confirmation event.
- Any write/DDL impact.

Also validate:
- Immutability and retention.
- Exportability.
- Central ingestion into SIEM/observability tooling.
- Correlation with authoritative database audit logs.
- Completeness relative to manual query-console activity.

An AI query recap is useful for productivity, but it is not sufficient as an enterprise audit record unless its completeness and integrity are proven.

---

## Accuracy, false confidence, and domain semantics

AI can produce plausible but incorrect findings. Risks include:
- Incorrect SQL.
- Incorrect join interpretation.
- Missed business exceptions.
- False claims that a table is unused.
- Incorrect candidate keys.
- Misinterpreted grain.
- Incorrect assumption that anomalous-looking records are invalid.
- Hallucinated migration rationale or remediation.

Required controls:
- Treat findings as hypotheses.
- Validate using deterministic profiling, source-system documentation, and domain-owner review.
- Use database compilation, automated tests, and regression testing for SQL/routine changes.
- Require human approval before recommendations become data transformations, quality rules, or customer-impacting decisions.

---

## Cost, performance, and operating model

The transcript provides no pricing, token usage, model details, license structure, or database compute costs.

Validate:
- JetBrains/DataGrip AI licensing and enterprise pricing.
- AI/model usage charges, if applicable.
- Database/warehouse costs caused by generated queries.
- Latency for large schemas and local files; the demo explicitly characterizes CSV analysis as heavy.
- Need for query governance to avoid high-cost scans.
- Support and enablement cost.
- Operational noise created by untriaged AI-generated findings.

The likely productivity benefit is reduced time for exploration and documentation; the trade-off is a new governance surface and potential for noisy or inaccurate recommendations.

---

## Data-modeling decisions that cannot be delegated to AI

Before accepting AI recommendations for keys, duplicates, or mixed grain, resolve:
- What is the declared grain of the target table?
- Is each row a transaction, delivery, account, service location, tank, telemetry reading, snapshot, or aggregate?
- Is there a true business key?
- Would a surrogate key mask duplicate-source issues rather than solve them?
- What is the authoritative source when values conflict?
- What is the deduplication policy?
- Should invalid records be rejected, quarantined, corrected, or retained with an exception indicator?
- How are late-arriving records and historical corrections handled?

---

# Action items

## 1. Run a constrained DataGrip AI proof of concept

Set initial boundaries:
- Sandbox or development databases only.
- Masked, synthetic, or non-sensitive datasets only.
- Schema metadata access enabled first.
- Disable or do not grant:
  - Production access.
  - Data-read access initially, where feasible.
  - Routine execution.
  - DML.
  - DDL.
  - Local-file analysis involving company data.

Measure:
- SQL correctness.
- Quality of schema explanations.
- Migration-finding precision.
- Data-quality false-positive rate.
- Query latency and database load.
- Value for developer onboarding and documentation.

---

## 2. Complete vendor security and architecture assessment

Obtain and review documentation covering:
- Model/provider architecture.
- Data routing and residency.
- Prompt, schema, query-result, and file-content retention.
- Training/service-improvement usage.
- Tenant isolation.
- Encryption.
- Enterprise SSO.
- Administrative policy controls.
- Audit logging.
- Private networking or approved-endpoint options.
- Credential storage and secret handling.

Explicitly test what data is transmitted when `@` referencing database objects and local files.

---

## 3. Establish an AI database-access policy

Define a policy that includes:
- Read-only, non-production default.
- Schema-only access as the preferred baseline.
- No AI-driven DDL/DML or routine execution in production.
- Database-native RBAC as the primary control.
- Mandatory use of CI/CD and approved change management for schema changes.
- Query timeouts, result-size controls, and environment-specific restrictions.
- Required use of authoritative database audit logs.

---

## 4. Create a reusable source-data intake assessment

Create a standard artifact for every new source/dataset that records:
- Source system and accountable owner.
- Sensitivity classification.
- Declared grain.
- Candidate/business keys.
- Join behavior and known limitations.
- Deduplication policy.
- Naming-standard issues.
- Nullability, uniqueness, referential integrity, and range findings.
- Cross-field business-rule candidates.
- Data-quality exceptions and disposition.
- Remediation owner and target date.

AI can draft this assessment, but a data steward and source-system owner should approve it.

---

## 5. Convert validated findings into Databricks controls

For approved quality rules, implement deterministic checks in Databricks SQL/PySpark and governed pipeline workflows.

Include controls for:
- Key uniqueness.
- Nullability.
- Referential integrity.
- Valid ranges.
- Cross-field business rules.
- Duplicate patterns.
- Grain consistency.
- Schema conformance.
- Sensitive-data classification and handling.

Use the IDE assistant for exploratory triage, not as the production control plane.

---

## 6. Standardize curated schema conventions

Adopt or reinforce conventions for governed datasets:
- Lowercase `snake_case` field names.
- Avoid spaces, periods, and special characters in curated Silver/Gold tables.
- Preserve raw source column names only where source fidelity requires it, typically in Bronze/raw layers.
- Document field mappings and semantic definitions.
- Require declared grain and candidate-key review before promotion to curated or AI-ready layers.

---

## 7. Define authoritative logging and review requirements

Confirm that:
- Database/audit-platform logs remain the system of record.
- AI-generated and executed SQL can be correlated with user identity and environment.
- Any AI approval events are captured where required.
- Security and operations teams can review usage centrally.
- AI-proposed destructive changes cannot bypass established release and change-management processes.

## Full transcript

[00:04] Hello everyone. In this video, we'll
[00:04] Hello everyone. In this video, we'll show you how to work a data grip using
[00:06] show you how to work a data grip using
[00:06] show you how to work a data grip using AI agents.
[00:07] AI agents.
[00:07] AI agents. Once you install the AI assistant
[00:09] Once you install the AI assistant
[00:09] Once you install the AI assistant plugin, you'll see the AI assistant
[00:11] plugin, you'll see the AI assistant
[00:11] plugin, you'll see the AI assistant button in the top toolbar.
[00:13] button in the top toolbar.
[00:13] button in the top toolbar. Clicking it opens the tool window, where
[00:15] Clicking it opens the tool window, where
[00:15] Clicking it opens the tool window, where you can choose to work in chat mode or
[00:17] you can choose to work in chat mode or
[00:17] you can choose to work in chat mode or use any agent installed on your machine.
[00:20] use any agent installed on your machine.
[00:20] use any agent installed on your machine. As you can see, you can use Claude,
[00:22] As you can see, you can use Claude,
[00:22] As you can see, you can use Claude, Codex, Gemini, or any other agent
[00:24] Codex, Gemini, or any other agent
[00:24] Codex, Gemini, or any other agent available from the ACP registry.
[00:27] available from the ACP registry.
[00:27] available from the ACP registry. For this video, we'll be using Claude.
[00:30] For this video, we'll be using Claude.
[00:30] For this video, we'll be using Claude. There might be a need to configure the
[00:32] There might be a need to configure the
[00:32] There might be a need to configure the MCP server for the specific agent.
[00:35] MCP server for the specific agent.
[00:35] MCP server for the specific agent. Please refer to DataGrip's documentation
[00:36] Please refer to DataGrip's documentation
[00:36] Please refer to DataGrip's documentation to accomplish this. The link is in the
[00:38] to accomplish this. The link is in the
[00:38] to accomplish this. The link is in the video's description.
[00:41] video's description.
[00:41] video's description. First, Claude can create a data source
[00:43] First, Claude can create a data source
[00:43] First, Claude can create a data source directly inside DataGrip using the
[00:45] directly inside DataGrip using the
[00:45] directly inside DataGrip using the provided MCP tools.
[00:47] provided MCP tools.
[00:47] provided MCP tools. Let's look at a couple of ways to do
[00:48] Let's look at a couple of ways to do
[00:48] Let's look at a couple of ways to do this.
[00:49] this.
[00:49] this. The simplest method to create a data
[00:51] The simplest method to create a data
[00:51] The simplest method to create a data source is to use a JDBC URL.
[00:54] source is to use a JDBC URL.
[00:54] source is to use a JDBC URL. We just type create data source from URL
[00:57] We just type create data source from URL
[00:57] We just type create data source from URL and paste our URL into the agent chat.
[01:00] and paste our URL into the agent chat.
[01:00] and paste our URL into the agent chat. The first thing Claude asks for is
[01:01] The first thing Claude asks for is
[01:02] The first thing Claude asks for is permission to run a skill called
[01:03] permission to run a skill called
[01:03] permission to run a skill called database connection management.
[01:05] database connection management.
[01:05] database connection management. Once allowed, Claude does its job and
[01:08] Once allowed, Claude does its job and
[01:08] Once allowed, Claude does its job and then requests permission to run the MCP
[01:10] then requests permission to run the MCP
[01:10] then requests permission to run the MCP tool called create database connection.
[01:13] tool called create database connection.
[01:13] tool called create database connection. After allowing this, it asks for your
[01:15] After allowing this, it asks for your
[01:15] After allowing this, it asks for your credentials as they aren't transferred
[01:17] credentials as they aren't transferred
[01:17] credentials as they aren't transferred via the URL.
[01:19] via the URL.
[01:19] via the URL. I enter my username and password, click
[01:21] I enter my username and password, click
[01:21] I enter my username and password, click okay, and voila, the data source is
[01:23] okay, and voila, the data source is
[01:23] okay, and voila, the data source is created.
[01:25] created.
[01:25] created. You can see it in the left tool window
[01:27] You can see it in the left tool window
[01:27] You can see it in the left tool window called database explorer, complete with
[01:29] called database explorer, complete with
[01:29] called database explorer, complete with all of its objects. Success.
[01:32] all of its objects. Success.
[01:32] all of its objects. Success. I want to highlight that a connection is
[01:34] I want to highlight that a connection is
[01:34] I want to highlight that a connection is created within DataGrip, and we never
[01:36] created within DataGrip, and we never
[01:36] created within DataGrip, and we never ever pass credentials to the AI agent.
[01:40] ever pass credentials to the AI agent.
[01:40] ever pass credentials to the AI agent. Another straightforward way to create a
[01:42] Another straightforward way to create a
[01:42] Another straightforward way to create a data source is to simply provide the
[01:44] data source is to simply provide the
[01:44] data source is to simply provide the agent with all the connection details
[01:45] agent with all the connection details
[01:45] agent with all the connection details you know.
[01:46] you know.
[01:47] you know. I'll type okay,
[01:49] I'll type okay,
[01:49] I'll type okay, create another data source. It's MySQL,
[01:51] create another data source. It's MySQL,
[01:51] create another data source. It's MySQL, hosted locally, port 33081,
[01:55] hosted locally, port 33081,
[01:55] hosted locally, port 33081, database guest.
[01:57] database guest.
[01:57] database guest. Claude starts thinking and again asks to
[01:59] Claude starts thinking and again asks to
[01:59] Claude starts thinking and again asks to use the database connection management
[02:00] use the database connection management
[02:00] use the database connection management skill since I previously clicked allow
[02:03] skill since I previously clicked allow
[02:03] skill since I previously clicked allow instead of always allow.
[02:05] instead of always allow.
[02:05] instead of always allow. It does its job, then prompts me for
[02:07] It does its job, then prompts me for
[02:07] It does its job, then prompts me for credentials I haven't provided.
[02:10] credentials I haven't provided.
[02:10] credentials I haven't provided. I enter them,
[02:11] I enter them,
[02:11] I enter them, click okay,
[02:12] click okay,
[02:13] click okay, and the second data source is created.
[02:16] and the second data source is created.
[02:16] and the second data source is created. All the details are visible in the chat,
[02:18] All the details are visible in the chat,
[02:18] All the details are visible in the chat, the test connection is successful, and I
[02:20] the test connection is successful, and I
[02:20] the test connection is successful, and I can see the objects in the database
[02:21] can see the objects in the database
[02:22] can see the objects in the database explorer.
[02:24] explorer.
[02:24] explorer. Let's get to the third way to create
[02:26] Let's get to the third way to create
[02:26] Let's get to the third way to create data sources. Exporting connections from
[02:28] data sources. Exporting connections from
[02:28] data sources. Exporting connections from other tools.
[02:30] other tools.
[02:30] other tools. The agent can locate the relevant files
[02:31] The agent can locate the relevant files
[02:31] The agent can locate the relevant files for whatever database tools you have
[02:33] for whatever database tools you have
[02:33] for whatever database tools you have installed and import the connections for
[02:35] installed and import the connections for
[02:35] installed and import the connections for you.
[02:36] you.
[02:36] you. I'll type, "Great.
[02:38] I'll type, "Great.
[02:38] I'll type, "Great. Now find my connections in pgAdmin and
[02:40] Now find my connections in pgAdmin and
[02:40] Now find my connections in pgAdmin and import them here."
[02:42] import them here."
[02:42] import them here." Claude has to do a bit more work to find
[02:44] Claude has to do a bit more work to find
[02:44] Claude has to do a bit more work to find where the pgAdmin connections are stored
[02:46] where the pgAdmin connections are stored
[02:46] where the pgAdmin connections are stored on this computer.
[02:47] on this computer.
[02:47] on this computer. I grant a couple of permissions, and as
[02:49] I grant a couple of permissions, and as
[02:49] I grant a couple of permissions, and as you can see, two servers are found in
[02:51] you can see, two servers are found in
[02:52] you can see, two servers are found in pgAdmin and they appear on the left side
[02:54] pgAdmin and they appear on the left side
[02:54] pgAdmin and they appear on the left side of the screen.
[02:55] of the screen.
[02:55] of the screen. I need to enter my username and password
[02:57] I need to enter my username and password
[02:57] I need to enter my username and password for both.
[02:59] for both.
[02:59] for both. Once that's done, my data sources are
[03:00] Once that's done, my data sources are
[03:00] Once that's done, my data sources are ready to use.
[03:02] ready to use.
[03:02] ready to use. The agent provides some details about
[03:04] The agent provides some details about
[03:04] The agent provides some details about these connections in the chat and they
[03:06] these connections in the chat and they
[03:06] these connections in the chat and they appear in database explorer.
[03:08] appear in database explorer.
[03:08] appear in database explorer. They aren't automatically introspected,
[03:10] They aren't automatically introspected,
[03:10] They aren't automatically introspected, the agent decided against doing that,
[03:12] the agent decided against doing that,
[03:12] the agent decided against doing that, but I can manually refresh them to see
[03:14] but I can manually refresh them to see
[03:14] but I can manually refresh them to see all the underlying objects.
[03:21] Now let's get to the real work. Because
[03:21] Now let's get to the real work. Because the AI agent knows about your data
[03:23] the AI agent knows about your data
[03:23] the AI agent knows about your data sources, you can essentially talk to
[03:25] sources, you can essentially talk to
[03:25] sources, you can essentially talk to your connections.
[03:27] your connections.
[03:27] your connections. For example, I want to know which schema
[03:29] For example, I want to know which schema
[03:29] For example, I want to know which schema across all of my data sources contains
[03:31] across all of my data sources contains
[03:31] across all of my data sources contains employee data.
[03:33] employee data.
[03:33] employee data. I'll ask, "In which schema do I have
[03:35] I'll ask, "In which schema do I have
[03:35] I'll ask, "In which schema do I have data about employees?"
[03:37] data about employees?"
[03:37] data about employees?" Let's see what Claude says.
[03:39] Let's see what Claude says.
[03:39] Let's see what Claude says. First, it asks to use a skill.
[03:41] First, it asks to use a skill.
[03:41] First, it asks to use a skill. Then some magic happens behind the
[03:43] Then some magic happens behind the
[03:43] Then some magic happens behind the scenes using the MCP DataGrip tools.
[03:46] scenes using the MCP DataGrip tools.
[03:46] scenes using the MCP DataGrip tools. Finally, Claude asks if it's okay to
[03:48] Finally, Claude asks if it's okay to
[03:48] Finally, Claude asks if it's okay to read my database schema.
[03:50] read my database schema.
[03:50] read my database schema. This is DataGrip's built-in security
[03:52] This is DataGrip's built-in security
[03:52] This is DataGrip's built-in security layer in action.
[03:54] layer in action.
[03:54] layer in action. I click allow to give Claude permission.
[03:57] I click allow to give Claude permission.
[03:57] I click allow to give Claude permission. After a bit more thinking, Claude gives
[03:59] After a bit more thinking, Claude gives
[03:59] After a bit more thinking, Claude gives me the answer and even displays the
[04:01] me the answer and even displays the
[04:01] me the answer and even displays the relevant table.
[04:03] relevant table.
[04:03] relevant table. The layout is a bit cramped, so let's
[04:05] The layout is a bit cramped, so let's
[04:05] The layout is a bit cramped, so let's widen the tool window.
[04:07] widen the tool window.
[04:07] widen the tool window. Claude is correct.
[04:09] Claude is correct.
[04:09] Claude is correct. It tells me that the locally hosted
[04:11] It tells me that the locally hosted
[04:11] It tells me that the locally hosted MySQL data source contains a database
[04:13] MySQL data source contains a database
[04:13] MySQL data source contains a database with employee data.
[04:15] with employee data.
[04:15] with employee data. Let's try another request.
[04:18] Let's try another request.
[04:18] Let's try another request. Okay, cool.
[04:19] Okay, cool.
[04:19] Okay, cool. Now, let's work with the Sakila database
[04:21] Now, let's work with the Sakila database
[04:21] Now, let's work with the Sakila database and the PG AI data source.
[04:24] and the PG AI data source.
[04:24] and the PG AI data source. Tell me about this database. What is it
[04:26] Tell me about this database. What is it
[04:26] Tell me about this database. What is it about? What tables are there and how are
[04:28] about? What tables are there and how are
[04:29] about? What tables are there and how are they connected?
[04:31] they connected?
[04:31] they connected? Once again, Claude asked for permission
[04:33] Once again, Claude asked for permission
[04:33] Once again, Claude asked for permission to read the database schema and I allow
[04:35] to read the database schema and I allow
[04:35] to read the database schema and I allow it.
[04:36] it.
[04:36] it. Next, I see the actual SQL query that
[04:38] Next, I see the actual SQL query that
[04:38] Next, I see the actual SQL query that Claude intends to run.
[04:40] Claude intends to run.
[04:40] Claude intends to run. It warns me that the statement will read
[04:42] It warns me that the statement will read
[04:42] It warns me that the statement will read database data, which is fine.
[04:45] database data, which is fine.
[04:45] database data, which is fine. I review it and click allow.
[04:51] It prompts me again for a second and
[04:51] It prompts me again for a second and then a third query.
[04:53] then a third query.
[04:53] then a third query. At this point, since I'm perfectly fine
[04:55] At this point, since I'm perfectly fine
[04:55] At this point, since I'm perfectly fine with the agent running read-only
[04:56] with the agent running read-only
[04:56] with the agent running read-only queries,
[04:57] queries,
[04:57] queries, I check the box for always allow Claude
[04:59] I check the box for always allow Claude
[04:59] I check the box for always allow Claude code to read database data. This ensures
[05:02] code to read database data. This ensures
[05:02] code to read database data. This ensures I won't be bombarded with these
[05:03] I won't be bombarded with these
[05:03] I won't be bombarded with these confirmation prompts in the future.
[05:06] confirmation prompts in the future.
[05:06] confirmation prompts in the future. Finally, we get our answer.
[05:09] Finally, we get our answer.
[05:09] Finally, we get our answer. Claude provides a wealth of information
[05:10] Claude provides a wealth of information
[05:10] Claude provides a wealth of information about the database,
[05:12] about the database,
[05:12] about the database, where it's hosted, how tables are
[05:14] where it's hosted, how tables are
[05:14] where it's hosted, how tables are connected, and other important details,
[05:16] connected, and other important details,
[05:16] connected, and other important details, giving us a complete overview of the
[05:18] giving us a complete overview of the
[05:18] giving us a complete overview of the schema.
[05:24] Now, let's move on to the main event,
[05:25] Now, let's move on to the main event, actually querying some data.
[05:27] actually querying some data.
[05:27] actually querying some data. I'll use a new prompt. Give me a query
[05:29] I'll use a new prompt. Give me a query
[05:29] I'll use a new prompt. Give me a query to show actors who played in more than
[05:31] to show actors who played in more than
[05:31] to show actors who played in more than five traumas and never played in
[05:33] five traumas and never played in
[05:33] five traumas and never played in comedies.
[05:35] comedies.
[05:35] comedies. Claude starts thinking, asks to run the
[05:37] Claude starts thinking, asks to run the
[05:37] Claude starts thinking, asks to run the necessary skill, and after a short wait,
[05:39] necessary skill, and after a short wait,
[05:39] necessary skill, and after a short wait, it uses the MCP tools to generate a
[05:41] it uses the MCP tools to generate a
[05:41] it uses the MCP tools to generate a result.
[05:43] result.
[05:43] result. The output is a fairly long SQL query.
[05:46] The output is a fairly long SQL query.
[05:46] The output is a fairly long SQL query. Because I previously allowed Claude to
[05:48] Because I previously allowed Claude to
[05:48] Because I previously allowed Claude to run read queries automatically, it went
[05:50] run read queries automatically, it went
[05:50] run read queries automatically, it went ahead and executed query for me,
[05:52] ahead and executed query for me,
[05:52] ahead and executed query for me, returning exactly one row, Max Mastel,
[05:56] returning exactly one row, Max Mastel,
[05:56] returning exactly one row, Max Mastel, who starred in seven dramas.
[05:58] who starred in seven dramas.
[05:58] who starred in seven dramas. It even provided some helpful comments
[06:00] It even provided some helpful comments
[06:00] It even provided some helpful comments explaining the logic.
[06:03] explaining the logic.
[06:03] explaining the logic. If you prefer to work with this query
[06:05] If you prefer to work with this query
[06:05] If you prefer to work with this query the old-school way,
[06:06] the old-school way,
[06:06] the old-school way, you can easily copy it from the AI chat
[06:08] you can easily copy it from the AI chat
[06:08] you can easily copy it from the AI chat window and paste it into the standard
[06:10] window and paste it into the standard
[06:10] window and paste it into the standard query console to modify or run it
[06:13] query console to modify or run it
[06:13] query console to modify or run it manually.
[06:18] Let's talk a bit more about the agent's
[06:18] Let's talk a bit more about the agent's ability to run SQL automatically.
[06:21] ability to run SQL automatically.
[06:21] ability to run SQL automatically. I mentioned this earlier, but you can
[06:23] I mentioned this earlier, but you can
[06:23] I mentioned this earlier, but you can always manage these permissions by going
[06:25] always manage these permissions by going
[06:25] always manage these permissions by going to IDE settings,
[06:27] to IDE settings,
[06:27] to IDE settings, database,
[06:28] database,
[06:28] database, AI tools.
[06:30] AI tools.
[06:30] AI tools. Here, you can review and toggle the
[06:32] Here, you can review and toggle the
[06:32] Here, you can review and toggle the permissions granted to the agent.
[06:34] permissions granted to the agent.
[06:34] permissions granted to the agent. For instance, alongside the permission
[06:36] For instance, alongside the permission
[06:36] For instance, alongside the permission to read database data, I can also grant
[06:39] to read database data, I can also grant
[06:39] to read database data, I can also grant permission to read database schemas.
[06:41] permission to read database schemas.
[06:42] permission to read database schemas. This specific permission doesn't allow
[06:43] This specific permission doesn't allow
[06:43] This specific permission doesn't allow access to actual table data. Instead, it
[06:47] access to actual table data. Instead, it
[06:47] access to actual table data. Instead, it allows the agent to retrieve metadata,
[06:49] allows the agent to retrieve metadata,
[06:49] allows the agent to retrieve metadata, such as schema names, object names, and
[06:52] such as schema names, object names, and
[06:52] such as schema names, object names, and the overall structure.
[06:58] Here's another cool example of how AI
[06:58] Here's another cool example of how AI can help you manage databases.
[07:00] can help you manage databases.
[07:01] can help you manage databases. I've been using the schema on the left
[07:02] I've been using the schema on the left
[07:02] I've been using the schema on the left as a sandbox.
[07:04] as a sandbox.
[07:04] as a sandbox. While it contains the standard Sakila
[07:06] While it contains the standard Sakila
[07:06] While it contains the standard Sakila database, I've also added a few random
[07:08] database, I've also added a few random
[07:08] database, I've also added a few random tables here and there.
[07:11] tables here and there.
[07:11] tables here and there. Let's see if the AI can identify which
[07:12] Let's see if the AI can identify which
[07:13] Let's see if the AI can identify which tables don't actually belong to the
[07:14] tables don't actually belong to the
[07:15] tables don't actually belong to the Sakila schema.
[07:16] Sakila schema.
[07:16] Sakila schema. I'll prompt it.
[07:18] I'll prompt it.
[07:18] I'll prompt it. Which tables don't really belong to this
[07:20] Which tables don't really belong to this
[07:20] Which tables don't really belong to this database?
[07:22] database?
[07:22] database? This is a tricky task. The agent quickly
[07:24] This is a tricky task. The agent quickly
[07:24] This is a tricky task. The agent quickly recognizes that the core schema is the
[07:27] recognizes that the core schema is the
[07:27] recognizes that the core schema is the Sakila DVD rental database, and then it
[07:30] Sakila DVD rental database, and then it
[07:30] Sakila DVD rental database, and then it analyzes the rest to find the outliers.
[07:34] analyzes the rest to find the outliers.
[07:34] analyzes the rest to find the outliers. Eventually, it provides the answer,
[07:36] Eventually, it provides the answer,
[07:36] Eventually, it provides the answer, listing the tables that belong to
[07:37] listing the tables that belong to
[07:37] listing the tables that belong to Sakila, and pointing out the ones that
[07:39] Sakila, and pointing out the ones that
[07:39] Sakila, and pointing out the ones that are out of place, along with its
[07:41] are out of place, along with its
[07:41] are out of place, along with its reasoning.
[07:43] reasoning.
[07:43] reasoning. I'm satisfied with its analysis, so I'll
[07:46] I'm satisfied with its analysis, so I'll
[07:46] I'm satisfied with its analysis, so I'll ask the agent to clean them up.
[07:48] ask the agent to clean them up.
[07:48] ask the agent to clean them up. Okay. Let's drop all these tables.
[07:52] Okay. Let's drop all these tables.
[07:52] Okay. Let's drop all these tables. Notice how the agent performs safety
[07:53] Notice how the agent performs safety
[07:53] Notice how the agent performs safety checks first. It replies,
[07:56] checks first. It replies,
[07:56] checks first. It replies, "Before dropping, let me check whether
[07:58] "Before dropping, let me check whether
[07:58] "Before dropping, let me check whether anything else, like views or foreign
[08:01] anything else, like views or foreign
[08:01] anything else, like views or foreign keys, depends on these tables."
[08:03] keys, depends on these tables."
[08:03] keys, depends on these tables." This is a very logical precaution, so I
[08:05] This is a very logical precaution, so I
[08:05] This is a very logical precaution, so I let it proceed.
[08:08] let it proceed.
[08:08] let it proceed. Finally, Cloud generates the necessary
[08:10] Finally, Cloud generates the necessary
[08:10] Finally, Cloud generates the necessary drop table statements and asks for
[08:12] drop table statements and asks for
[08:12] drop table statements and asks for confirmation to run them.
[08:14] confirmation to run them.
[08:14] confirmation to run them. Since this is exactly what I wanted, I
[08:17] Since this is exactly what I wanted, I
[08:17] Since this is exactly what I wanted, I approve it.
[08:19] approve it.
[08:19] approve it. As you can see in the database explorer
[08:21] As you can see in the database explorer
[08:21] As you can see in the database explorer on the left, all those unnecessary
[08:23] on the left, all those unnecessary
[08:23] on the left, all those unnecessary tables are now gone from the public
[08:25] tables are now gone from the public
[08:25] tables are now gone from the public schema.
[08:26] schema.
[08:26] schema. The AI chat window also provides a
[08:28] The AI chat window also provides a
[08:28] The AI chat window also provides a summary of the actions performed and the
[08:30] summary of the actions performed and the
[08:30] summary of the actions performed and the final outcome.
[08:36] You can also ask the agent to recap past
[08:36] You can also ask the agent to recap past activities.
[08:37] activities.
[08:37] activities. I'll type this prompt.
[08:39] I'll type this prompt.
[08:39] I'll type this prompt. "Tell me all the queries you ran over
[08:41] "Tell me all the queries you ran over
[08:41] "Tell me all the queries you ran over the last 2 days."
[08:47] After a moment of thought, the agent
[08:47] After a moment of thought, the agent provides a comprehensive list of those
[08:49] provides a comprehensive list of those
[08:49] provides a comprehensive list of those queries and even politely asks for
[08:50] queries and even politely asks for
[08:50] queries and even politely asks for feedback.
[08:55] Let's widen the pane and review the
[08:55] Let's widen the pane and review the response.
[09:01] As expected, the majority of the queries
[09:01] As expected, the majority of the queries it lists are the ones we just executed
[09:03] it lists are the ones we just executed
[09:03] it lists are the ones we just executed for this video.
[09:05] for this video.
[09:05] for this video. Next, we'll cover mentioning database
[09:07] Next, we'll cover mentioning database
[09:07] Next, we'll cover mentioning database objects directly within the agent chat.
[09:10] objects directly within the agent chat.
[09:10] objects directly within the agent chat. Looking at the database explorer, I have
[09:13] Looking at the database explorer, I have
[09:13] Looking at the database explorer, I have several routines.
[09:15] several routines.
[09:15] several routines. Let's say I want to know more about the
[09:16] Let's say I want to know more about the
[09:16] Let's say I want to know more about the get customer balance function.
[09:19] get customer balance function.
[09:19] get customer balance function. I can type, "What does" and then by
[09:22] I can type, "What does" and then by
[09:22] I can type, "What does" and then by typing the at symbol,
[09:23] typing the at symbol,
[09:24] typing the at symbol, I trigger the mention feature.
[09:26] I trigger the mention feature.
[09:26] I trigger the mention feature. I select the at DB object identifier and
[09:30] I select the at DB object identifier and
[09:30] I select the at DB object identifier and code completion kicks in. I just start
[09:32] code completion kicks in. I just start
[09:32] code completion kicks in. I just start typing get C,
[09:34] typing get C,
[09:34] typing get C, select get customer balance from the
[09:37] select get customer balance from the
[09:37] select get customer balance from the suggestions and insert it.
[09:39] suggestions and insert it.
[09:39] suggestions and insert it. This is the easiest way to explicitly
[09:41] This is the easiest way to explicitly
[09:41] This is the easiest way to explicitly tell the agent exactly which database
[09:43] tell the agent exactly which database
[09:43] tell the agent exactly which database object you're asking about.
[09:46] object you're asking about.
[09:46] object you're asking about. Shortly after, the agent asks if it's
[09:48] Shortly after, the agent asks if it's
[09:48] Shortly after, the agent asks if it's okay to execute the routine to analyze
[09:50] okay to execute the routine to analyze
[09:50] okay to execute the routine to analyze it. Notice that this falls under the
[09:51] it. Notice that this falls under the
[09:52] it. Notice that this falls under the modify data permission because DataGrip
[09:54] modify data permission because DataGrip
[09:54] modify data permission because DataGrip can't guarantee what a stored procedure
[09:56] can't guarantee what a stored procedure
[09:56] can't guarantee what a stored procedure might do internally. Running any routine
[09:59] might do internally. Running any routine
[09:59] might do internally. Running any routine requires modification privileges just to
[10:01] requires modification privileges just to
[10:01] requires modification privileges just to be safe.
[10:03] be safe.
[10:03] be safe. Once approved, we get a comprehensive
[10:05] Once approved, we get a comprehensive
[10:05] Once approved, we get a comprehensive explanation of the routine.
[10:11] I have to admit, it's [clears throat] a
[10:11] I have to admit, it's [clears throat] a bit more complex than I expected. Let's
[10:14] bit more complex than I expected. Let's
[10:14] bit more complex than I expected. Let's widen the pane again to review its
[10:15] widen the pane again to review its
[10:15] widen the pane again to review its findings.
[10:22] First, it outlines the signature,
[10:22] First, it outlines the signature, intent, and what the body of the
[10:24] intent, and what the body of the
[10:24] intent, and what the body of the function actually does.
[10:26] function actually does.
[10:26] function actually does. But it also found something quite
[10:27] But it also found something quite
[10:27] But it also found something quite surprising.
[10:29] surprising.
[10:29] surprising. It detected MySQL specific syntax within
[10:32] It detected MySQL specific syntax within
[10:32] It detected MySQL specific syntax within this PostgreSQL procedure. It explains
[10:34] this PostgreSQL procedure. It explains
[10:34] this PostgreSQL procedure. It explains that this logic was likely inherited
[10:36] that this logic was likely inherited
[10:36] that this logic was likely inherited from the original Sakila database and
[10:38] from the original Sakila database and
[10:38] from the original Sakila database and was never properly converted to a case
[10:40] was never properly converted to a case
[10:40] was never properly converted to a case when statement during the migration to
[10:42] when statement during the migration to
[10:42] when statement during the migration to Postgres. That's a fascinating catch.
[10:45] Postgres. That's a fascinating catch.
[10:45] Postgres. That's a fascinating catch. The agent also breaks down what the
[10:47] The agent also breaks down what the
[10:47] The agent also breaks down what the function returns and highlights a few
[10:49] function returns and highlights a few
[10:49] function returns and highlights a few other things worth knowing.
[10:51] other things worth knowing.
[10:52] other things worth knowing. Finally, let's look at working with
[10:53] Finally, let's look at working with
[10:53] Finally, let's look at working with files.
[10:54] files.
[10:55] files. In DataGrip, you can use the files tool
[10:56] In DataGrip, you can use the files tool
[10:56] In DataGrip, you can use the files tool window to attach local directories and
[10:58] window to attach local directories and
[10:58] window to attach local directories and navigate your file system directly from
[11:00] navigate your file system directly from
[11:00] navigate your file system directly from the IDE.
[11:02] the IDE.
[11:02] the IDE. For example, I have a folder attached
[11:04] For example, I have a folder attached
[11:04] For example, I have a folder attached that contains some scripts and a CSV
[11:06] that contains some scripts and a CSV
[11:06] that contains some scripts and a CSV file named housing2.csv.
[11:09] file named housing2.csv.
[11:09] file named housing2.csv. This is just a random data set I
[11:11] This is just a random data set I
[11:11] This is just a random data set I downloaded from the internet. I've never
[11:13] downloaded from the internet. I've never
[11:13] downloaded from the internet. I've never looked at it and I have no idea what
[11:15] looked at it and I have no idea what
[11:15] looked at it and I have no idea what data it holds. This is a perfect use
[11:17] data it holds. This is a perfect use
[11:17] data it holds. This is a perfect use case for AI.
[11:19] case for AI.
[11:19] case for AI. Let's ask the agent to identify any data
[11:21] Let's ask the agent to identify any data
[11:21] Let's ask the agent to identify any data quality problems within the file. Just
[11:24] quality problems within the file. Just
[11:24] quality problems within the file. Just like with database objects, you can use
[11:26] like with database objects, you can use
[11:26] like with database objects, you can use the at symbol to mention files.
[11:28] the at symbol to mention files.
[11:28] the at symbol to mention files. I'll type at,
[11:30] I'll type at,
[11:30] I'll type at, search for the file name, and it gets
[11:32] search for the file name, and it gets
[11:32] search for the file name, and it gets linked directly in the chat prompt.
[11:34] linked directly in the chat prompt.
[11:34] linked directly in the chat prompt. I'll send the request and see what
[11:36] I'll send the request and see what
[11:36] I'll send the request and see what issues it uncovers.
[11:38] issues it uncovers.
[11:38] issues it uncovers. I'll heavily speed up the video here
[11:40] I'll heavily speed up the video here
[11:40] I'll heavily speed up the video here because this was a heavy task for the
[11:42] because this was a heavy task for the
[11:42] because this was a heavy task for the agent, but we finally have our answer.
[11:45] agent, but we finally have our answer.
[11:45] agent, but we finally have our answer. It confirms that there are indeed data
[11:46] It confirms that there are indeed data
[11:46] It confirms that there are indeed data problems in housing2.csv.
[11:49] problems in housing2.csv.
[11:49] problems in housing2.csv. Let's review them.
[11:51] Let's review them.
[11:51] Let's review them. The first issue it highlights relates to
[11:53] The first issue it highlights relates to
[11:53] The first issue it highlights relates to physical lines and line endings.
[11:55] physical lines and line endings.
[11:56] physical lines and line endings. Oh, I like this one.
[11:58] Oh, I like this one.
[11:58] Oh, I like this one. Header names are hostile to SQL. They
[12:00] Header names are hostile to SQL. They
[12:00] Header names are hostile to SQL. They contain spaces and periods, meaning
[12:02] contain spaces and periods, meaning
[12:02] contain spaces and periods, meaning every reference will require double
[12:04] every reference will require double
[12:04] every reference will require double quoting. Good to know.
[12:06] quoting. Good to know.
[12:06] quoting. Good to know. Next, it points out there's no primary
[12:09] Next, it points out there's no primary
[12:09] Next, it points out there's no primary key and no row ID, nothing to join on.
[12:12] key and no row ID, nothing to join on.
[12:12] key and no row ID, nothing to join on. That's easily fixable once we import it
[12:14] That's easily fixable once we import it
[12:14] That's easily fixable once we import it into a database.
[12:16] into a database.
[12:16] into a database. But the semantic issues are even more
[12:18] But the semantic issues are even more
[12:18] But the semantic issues are even more interesting. For instance, it was
[12:20] interesting. For instance, it was
[12:21] interesting. For instance, it was noticed that four rows have more
[12:23] noticed that four rows have more
[12:23] noticed that four rows have more bedrooms than rooms, logically
[12:25] bedrooms than rooms, logically
[12:25] bedrooms than rooms, logically impossible.
[12:26] impossible.
[12:26] impossible. It also spotted mixed granularity across
[12:28] It also spotted mixed granularity across
[12:28] It also spotted mixed granularity across rows.
[12:30] rows.
[12:30] rows. We won't deep dive into the entire
[12:31] We won't deep dive into the entire
[12:31] We won't deep dive into the entire report, but you get the idea. AI agents
[12:34] report, but you get the idea. AI agents
[12:34] report, but you get the idea. AI agents can process and analyze a tremendous
[12:36] can process and analyze a tremendous
[12:36] can process and analyze a tremendous amount of information, and DataGrip
[12:38] amount of information, and DataGrip
[12:38] amount of information, and DataGrip seamlessly integrates these capabilities
[12:40] seamlessly integrates these capabilities
[12:40] seamlessly integrates these capabilities directly into your database workflow.
[12:43] directly into your database workflow.
[12:43] directly into your database workflow. Whether you're untangling complex joins,
[12:45] Whether you're untangling complex joins,
[12:46] Whether you're untangling complex joins, optimizing slow queries, or just
[12:48] optimizing slow queries, or just
[12:48] optimizing slow queries, or just exploring a new data set, having an AI
[12:51] exploring a new data set, having an AI
[12:51] exploring a new data set, having an AI agent right inside your IDE completely
[12:53] agent right inside your IDE completely
[12:53] agent right inside your IDE completely changes the game.
[12:55] changes the game.
[12:55] changes the game. If you're already using DataGrip, make
[12:57] If you're already using DataGrip, make
[12:57] If you're already using DataGrip, make sure your IDE is up to date and enable
[12:59] sure your IDE is up to date and enable
[12:59] sure your IDE is up to date and enable the AI Assistant plugin to start
[13:01] the AI Assistant plugin to start
[13:01] the AI Assistant plugin to start experimenting today. All the links you
[13:03] experimenting today. All the links you
[13:03] experimenting today. All the links you need are in the description below.
[13:05] need are in the description below.
[13:05] need are in the description below. Thanks for watching and happy querying.
