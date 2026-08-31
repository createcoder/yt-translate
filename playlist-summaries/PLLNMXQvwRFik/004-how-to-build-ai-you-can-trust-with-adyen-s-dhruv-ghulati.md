# How to Build AI You Can Trust, With Adyen's Dhruv Ghulati

- **Video:** https://www.youtube.com/watch?v=6IV5TQmazdQ
- **Generated:** 2026-08-31 20:44 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The material advocates a **governed, reusable AI/ML platform model** rather than isolated proofs of concept, unrestricted employee AI access, or bespoke infrastructure modeled on hyperscale firms.

For Superior Propane, the central implication is to create a practical **AI/ML “golden path”** across Databricks, Azure, and potentially Azure AI Foundry:

- Governed data products rather than raw-system access.
- Reusable ML/agent templates, evaluation practices, deployment controls, and observability.
- A controlled sandbox for low-risk experimentation, with a clear prototype-to-production route.
- Agents treated as **distinct digital workers** with workload identities, least privilege, restricted tools, auditability, and human approval for consequential actions.
- Outcome-led measurement: optimize for business resolution, safety, productivity, and operational impact—not generic benchmark scores or conversation quality alone.

The speakers make several broad claims—for example, that every SaaS provider needs an MCP strategy, that companies may soon operate huge numbers of developer agents, and that a broadly accessible AI sandbox should be a near-term investment. These are directional opinions, not established facts or a complete implementation blueprint.

Established principles underlying the discussion are stronger:

- ML/LLM systems require lifecycle management beyond data engineering: reproducibility, evaluation, deployment, monitoring, rollback, and retraining.
- Generative AI and agents introduce security risks through retrieval, prompt injection, tool invocation, and ungoverned derivative data.
- Removing a sensitive attribute does not eliminate bias when proxy variables remain.
- Model quality metrics must be tied to actual process and business outcomes.
- Production access and action authority should be tiered by data sensitivity and operational impact.

> **Transcript limitation:** Section 1 was not provided. This brief consolidates Sections 2–6 only.

---

# Technical details

## 1. Target operating model: AI/ML platform as a product

The speakers use Uber’s Michelangelo platform as an example of a shared ML platform that enabled multiple teams to reuse data features, pipelines, deployment mechanisms, and monitoring rather than rebuild them separately.

### Relevant pattern for Superior Propane

Do **not** replicate Uber’s bespoke, real-time platform by default. Superior Propane’s likely needs can be met initially through a managed, standardized platform built on existing services.

A minimum viable AI/ML platform should provide:

| Capability | Purpose |
|---|---|
| Governed data products | Reusable, quality-controlled datasets for customer, delivery, consumption, weather, service, commercial, and telemetry domains |
| Experimentation environment | Standard notebooks, source repositories, controlled compute, approved packages/models |
| ML lifecycle | Experiment tracking, model registry, versioning, promotion gates, rollback |
| GenAI/agent lifecycle | Prompt/version management, RAG evaluation, tool-use validation, safety testing, traceability |
| Observability | Data/model drift, task success, latency, cost, tool-call outcomes, security events |
| Governance | Identity, permissions, lineage, classification, logging, risk tiers, approvals |
| Enablement | Templates, documentation, use-case intake, training, support and ownership model |

### Databricks/Azure reference direction

Where available and approved in Superior Propane’s environment, a pragmatic architecture could include:

- **Databricks**
  - Governed Delta tables and curated “gold” data products.
  - Unity Catalog for discovery, permissions, lineage, and auditability.
  - MLflow for experiment tracking, model registry, model versioning, and promotion workflows.
  - Cluster policies, job clusters, tags, budgets, and idle-resource controls.

- **Azure**
  - Microsoft Entra ID for user, workload, and service identity.
  - Managed identities rather than embedded credentials.
  - Azure Key Vault for secrets.
  - Private networking and environment separation where required by data classification.
  - Azure Monitor / Log Analytics or equivalent centralized operational telemetry.

- **Azure AI Foundry / Azure OpenAI, if part of the approved estate**
  - Controlled model endpoint access.
  - Agent, prompt, and RAG experimentation.
  - Evaluation and safety controls assessed against Superior’s actual release requirements.
  - Project/environment-level governance and quota management.

The transcript does not establish exact product configurations, licensing, or service compatibility. These need architecture validation against the current Azure tenant, Databricks workspace configuration, security baseline, and procurement position.

---

## 2. MLOps is a distinct capability from data engineering

The speaker argues that data engineering alone is insufficient for production ML. This is directionally correct.

### Data engineering versus MLOps focus

| Data engineering / data platform | MLOps / AI platform |
|---|---|
| Data ingestion and transformation | Reproducible training and inference |
| Data availability and quality | Model evaluation, promotion, rollback |
| Catalogs and pipelines | Experiment tracking and model registry |
| Data versioning | Model, prompt, test-data, and artifact versioning |
| General orchestration | Training, deployment, retraining orchestration |
| Lineage | Model/data/evaluation lineage |
| Data monitoring | Drift, model performance, agent task quality |

### Required lifecycle controls

For predictive ML:

- Version code, data references, training environments, features, model artifacts, and evaluation datasets.
- Establish offline validation before deployment.
- Define model promotion criteria and accountable approvers.
- Monitor data drift, model drift, operational performance, and cost.
- Maintain rollback and retirement procedures.

For GenAI/RAG/agents:

- Version prompts, system instructions, retrieval configuration, model versions, tool schemas, and policy configurations.
- Evaluate groundedness, source/citation accuracy, tool-call correctness, safety, latency, and cost per task.
- Capture agent traces while applying privacy controls.
- Test prompt injection, tool misuse, data leakage, and refusal/escalation behavior.
- Maintain clear fallback behavior when source content is missing, stale, ambiguous, or safety-related.

---

## 3. Data-product and feature reuse

A recurring speaker theme is that multiple teams should not repeatedly recreate the same data features, pipelines, and workflows.

### Candidate propane-domain data products

High-reuse curated domains could include:

- **Customer and account**
  - Customer/account status, service plan, interactions, renewal indicators, account lifecycle events.

- **Delivery and dispatch**
  - Delivery history, route performance, service windows, route density, vehicle capacity, exception reasons, operational delays.

- **Consumption and demand**
  - Historical consumption, degree days, weather forecasts, tank level/telemetry where available, delivery frequency, regional patterns.

- **Service and equipment**
  - Service history, technician notes, asset/tank metadata, maintenance events, recurring issue patterns.

- **Commercial**
  - Price-plan context, offers, payment history, retention indicators and campaign exposure—subject to stronger access and use restrictions.

### Controls needed for reusable data products

Each product should have:

- Named business/data owner.
- Defined metric and entity semantics.
- Quality expectations and freshness SLA.
- Data classification.
- Approved use cases and access policy.
- Lineage to system of record.
- Clear handling for PII, payment-related, credit/collections, and employee data.

---

## 4. Evaluation: link AI quality to business outcomes

The speakers distinguish traditional ML evaluation from LLM/chat evaluation.

### Traditional ML

For classification/prediction use cases, metrics may include:

- Precision.
- Recall.
- False-positive and false-negative rates.
- Calibration.
- Forecast error.
- Threshold performance.
- Operational capacity impact.

The fraud example correctly illustrates the precision/recall trade-off: flagging every case can produce high recall but low precision, overwhelming human review capacity.

### GenAI and agent evaluation

LLM applications need more than “helpfulness” or generic benchmarks. Evaluate both:

**Offline quality**
- Correctness against approved answers.
- Groundedness in source content.
- Citation/source accuracy.
- Retrieval relevance.
- Policy adherence.
- Hallucination/unsupported-claim rate.
- Tool-call selection and parameter correctness.
- Safety/red-team test pass rate.

**Online outcome**
- Employee task completion.
- Contact-centre handle time.
- First-contact resolution.
- Customer self-service resolution.
- Repeat-contact reduction.
- Operational exception resolution time.
- User adoption by role and task.
- Escalation quality.
- Cost per resolved task.

### Evaluation design principles

- Use one or two primary AI quality metrics tied to a defined business KPI.
- Do not assume friendly tone, shorter conversations, containment, or benchmark performance equals business value.
- Compare against an existing baseline: business rules, human workflow, previous model, or controlled cohort.
- Build a **Superior Propane golden test set** for real operational questions and edge cases.
- Include expected answer/action, approved sources, access requirements, required escalation behavior, and prohibited actions.
- Calibrate automated “LLM-as-judge” scoring against domain expert review.

---

## 5. Agent and MCP tool-integration architecture

The speakers discuss MCPs, likely **Model Context Protocol**, as an emerging standard for exposing tools and contextual resources to AI clients.

### Important distinction

- An API exposes application functionality to applications.
- MCP can standardize the way AI-capable applications discover and call tools/resources.
- MCP does **not** make an integration inherently secure.
- An MCP server should be subject to the same—or stronger—security, governance, operational ownership, and supply-chain review as any API integration.

The speaker’s assertion that every SaaS company needs an MCP strategy is an opinion. However, a deliberate strategy for AI-to-system tool access is necessary if Superior Propane plans to deploy agents.

### Recommended tool-access pattern

Do not give agents broad direct access to production databases, CRM, dispatch, pricing, ERP, or ticketing systems.

Instead, expose constrained business functions through approved APIs/tools:

- `get_customer_summary(customer_id)` — read-only.
- `get_delivery_exception(route_id)` — read-only.
- `create_case_draft(...)` — draft-only.
- `update_ticket_status(ticket_id, allowed_status)` — constrained write.
- `submit_price_exception_request(...)` — starts an approval workflow, not a price change.
- `schedule_delivery_change(...)` — requires validation, confirmation, and designated approval.

### Required control model

Every agent should be a distinct workload identity—not a broadly privileged human account.

Use a tiered permission and action model:

| Tier | Example | Control expectation |
|---|---|---|
| Read | Search approved procedures, retrieve curated metrics | Least privilege, source authorization, logging |
| Draft | Draft service notes, create work-item draft | Human review before publication/action |
| Constrained write | Update approved ticket field/status | Explicit schema validation, limited values, audit trail |
| Approved write | Submit a service/price/delivery request | Workflow approval, named accountable approver |
| Prohibited | Direct database updates, irreversible financial or production changes | No agent authority by default |

For all tools:

- Enforce authorization outside the model.
- Validate tool input parameters and allowed values.
- Use idempotency protections where actions may be retried.
- Apply rate limits, quotas, and spend limits.
- Log user identity, agent identity, tool invocation, authorization decision, input/output metadata, approval, and final outcome.
- Maintain ownership, versioning, patching, monitoring, and decommissioning processes for every tool/MCP server.

---

## 6. Governance, privacy, fairness, and explainability

### Sensitive data and proxy bias

A central governance point is that excluding a protected/sensitive field does not guarantee fair or appropriate model behavior. Proxy signals can remain in location, language, tenure, payment behavior, operational history, or other correlated data.

For customer-impacting use cases, Superior Propane should:

- Identify sensitive attributes and plausible proxies relevant to the decision.
- Evaluate outcome disparities where legally, ethically, and operationally appropriate.
- Review feature attribution and correlations as investigation triggers—not proof of causation or fairness.
- Define when lower predictive performance is acceptable in exchange for interpretability, fairness, policy alignment, or regulatory defensibility.
- Prohibit informal use of experimental outputs in credit, collections, pricing, eligibility, or safety decisions without formal review.

### Explainability

Explainability can help identify:

- Data leakage.
- Spurious correlations.
- Data-quality issues.
- Inconsistent historical processes.
- Operational or customer-service disparities.

It is not, by itself, proof that a model is correct, compliant, causal, or fair.

### AI artifact governance

Inventory and govern more than source datasets. Include:

- Embeddings and vector indexes.
- Prompt/response logs and agent traces.
- Evaluation datasets.
- Derived features.
- Cached outputs.
- Background jobs.
- Model artifacts.
- Tool schemas and integration metadata.

For each artifact, define owner, classification, access policy, retention period, purpose limitation, deletion/retirement process, and audit requirements.

---

## 7. Sandbox and self-service model

The speakers recommend a sandbox, reusable model templates, LLM access, and a feedback loop rather than attempting to centrally predict every use case upfront.

This is useful, but “open access” must be interpreted as **governed enablement**, not unrestricted access to data, models, or production systems.

### Recommended sandbox structure

- Limited initial user cohort.
- Approved low- to medium-risk data domains.
- Pre-approved templates:
  - Logistic regression baseline.
  - XGBoost/tree-based model template.
  - Standard evaluation and feature-attribution report.
  - RAG template with citations, access filtering, evaluation, and trace logging.
  - Human-in-the-loop workflow template.
- Managed compute policies, quotas, budget tags, idle shutdown, and cost alerts.
- Formal feedback channel for use cases, blockers, data requests, incidents, and product improvements.
- Clear graduation criteria to move prototypes into supported production products.

---

# Potential applications for Superior Propane

## 1. Governed internal operations assistant

An internal Azure AI Foundry-based or equivalent assistant could support operations, contact-centre, field-service, and platform teams.

Initial capabilities:

- Search approved policies, SOPs, product information, and operational runbooks.
- Summarize delivery exceptions, service cases, or technician notes.
- Retrieve approved customer/account context through controlled APIs.
- Draft service-case notes, customer communications, or work items.
- Produce daily summaries from curated Databricks datasets.
- Help investigate Databricks job failures or infrastructure incidents using read-only logs, metrics, and documentation.

Initial constraints:

- Read-only and draft-first.
- No direct production database access.
- No autonomous customer-impacting, financial, pricing, safety, or dispatch commitments.
- Human approval before external communication or system-of-record changes.

## 2. Databricks governed analytics assistant

Enable business users to ask questions against curated data products rather than raw operational tables.

Pattern:

1. Curate and publish approved tables/views in Databricks.
2. Apply Unity Catalog or the organization’s chosen catalog/authorization layer.
3. Expose narrowly scoped query tools to the AI assistant.
4. Return metric definitions, freshness timestamps, source references, and caveats with every answer.
5. Limit exports, mask sensitive columns, and enforce source authorization.

Candidate queries:

- Delivery performance by region/time period.
- Service-volume trends.
- Demand/consumption trend summaries.
- Exception patterns.
- Contact-centre themes.
- Forecast-versus-actual operational reporting.

## 3. Batch-first predictive ML use cases

Prioritize use cases where batch scoring is sufficient before considering low-latency serving.

Candidates:

- **Runout-risk prioritization**
  - Bias toward recall, while controlling unnecessary outreach/expedited-delivery review workload.

- **Demand and delivery forecasting**
  - Use consumption history, weather/degree days, tank telemetry where available, region, and delivery patterns.

- **Delivery/service exception prioritization**
  - Predict likely exceptions or identify routes/customers needing operational review.

- **Retention/churn prioritization**
  - Support outreach prioritization, with controls for customer fairness, offer policy, and inappropriate proxy signals.

- **Service-volume forecasting**
  - Improve staffing and scheduling forecasts.

For each use case, define the cost of false positives and false negatives, human review capacity, target action, and measurable business result before model development.

## 4. Customer-service and employee knowledge RAG

A retrieval assistant can support billing, delivery, service-plan, appointment, policy, and internal process questions.

Requirements:

- Approved, current source content.
- Document-level access filtering.
- Citations and answer traceability.
- Defined uncertainty/refusal/escalation behavior.
- Strong safety escalation for propane safety questions.
- No improvisation on emergency, safety, regulatory, or technical-operating instructions.

## 5. Developer/platform-engineering assistants

Low-risk productivity opportunities include:

- Databricks pipeline and job troubleshooting.
- Codebase and documentation search.
- Test-case generation and pull-request review assistance.
- Infrastructure-as-code review.
- Runbook-guided incident evidence collection.
- Documentation drafting.

Keep remediation actions behind reviewed pull requests, CI/CD gates, or narrowly scoped approved runbooks.

---

# Risks/validation questions

## Security and access

- Are agents using distinct Entra workload identities and narrowly scoped permissions rather than shared human credentials?
- Is source-system authorization enforced at retrieval/query time, not merely when an index is created?
- Can an agent access only approved tools and approved operations for the active user/use case?
- Are direct production database writes prohibited by default?
- Are secrets held in Key Vault or equivalent rather than prompts, code, notebooks, or static configuration?
- Are dev, test/UAT, and production identities, data, endpoints, and permissions separated?
- Is private networking required for sensitive data flows and model endpoints?

## Prompt injection, data exfiltration, and tool misuse

- Can untrusted documents, emails, tickets, or web content instruct the agent to bypass policy or invoke unsafe tools?
- Are tool parameters validated independently of model output?
- Are instructions, retrieved content, and executable tool context segregated appropriately?
- Can users exploit the agent to access records they cannot access directly?
- Are data minimization, masking, DLP, logging redaction, retention, and export controls in place?

## Governance and model risk

- Which processes are retrieval-only, recommendation-only, draft-only, constrained-write, or prohibited from AI execution?
- Which actions require named approval for financial, pricing, collections, customer-account, safety, dispatch, or production-impacting decisions?
- Who owns data, model/agent behavior, tool integrations, security review, monitoring, support, and retirement?
- What decision logs, evidence, approvals, model versions, data references, and trace records are required for audit?
- How are proxy bias and unequal outcomes assessed for customer-impacting models?
- What are the rollback conditions for incorrect outputs, data-quality failures, unsafe content, excessive costs, or degraded operational outcomes?

## Evaluation and value

- What one or two business outcomes define success for each use case?
- Which offline AI metrics are expected to predict those outcomes?
- Is the system compared with current process performance, not only benchmark scores?
- What cases require mandatory escalation?
- Does the evaluation set include seasonal, regional, ambiguous, bilingual, safety-related, and operational exception scenarios where relevant?
- Are automated evaluation methods calibrated against human/domain-expert assessment?
- Are teams avoiding Goodhart effects, such as maximizing containment or minimizing conversation length at the expense of correct/safe resolution?

## Cost and operational trade-offs

The transcript provides no pricing figures. Validate:

- Databricks compute for feature engineering, training, batch inference, streaming, SQL queries, and notebooks.
- Azure AI Foundry/Azure OpenAI token and endpoint costs.
- Vector storage, embedding generation, retrieval, and index refresh costs.
- Trace/log storage and retention cost.
- API/MCP integration operation, support, patching, and security-review cost.
- Human-review cost caused by low-precision alerts or mandatory approvals.
- Cost of managed services versus a bespoke platform.

Key trade-off:

- More access and autonomy can reduce friction and improve speed.
- Stronger controls reduce blast radius and compliance risk but add engineering, review, and workflow overhead.

Use tiered controls rather than choosing either a fully locked-down or unrestricted model.

---

# Action items

1. **Define an AI/agent access-control standard**
   - Establish read, draft, constrained-write, approved-write, and prohibited tiers.
   - Explicitly ban direct agent access to production databases except through formally approved, exceptional patterns.
   - Require Entra workload identities, least privilege, environment separation, and audited tool calls.

2. **Create a minimum viable AI/ML golden path**
   - Standardize source control, data access, experiment tracking, model/prompt versioning, evaluations, deployment, monitoring, rollback, and retirement.
   - Favor managed Databricks and Azure capabilities before building bespoke platform components.

3. **Launch a two-quarter governed sandbox MVP**
   - Start with a limited internal cohort.
   - Define allowed data domains, user personas, templates, cost controls, and graduation criteria.
   - Include a formal feedback and use-case intake process.

4. **Publish reusable templates**
   - Transparent predictive-model template with threshold, precision/recall, calibration, and feature-attribution reporting.
   - XGBoost/tree-model template with standardized evaluation.
   - Secure RAG template with citations, authorization filtering, evaluation, and trace logging.
   - Human-in-the-loop agent workflow template.
   - Controlled tool/API integration template for read, draft, and constrained-write actions.

5. **Build curated propane data-product backlog**
   - Prioritize customer/account, delivery/dispatch, consumption/weather, service/equipment, and commercial domains.
   - Assign owners, quality standards, classification, lineage, and approved uses.

6. **Create Superior Propane evaluation standards and golden sets**
   - For predictive ML: business error costs, precision/recall or forecast metrics, thresholds, drift, and rollback criteria.
   - For GenAI/agents: groundedness, citation accuracy, safety, tool-use correctness, latency, cost/task, escalation behavior, and business KPI linkage.
   - Include customer, field, contact-centre, operations, and safety scenarios.

7. **Pilot one read/draft-first assistant**
   - Candidate: internal operations/service assistant that searches approved knowledge, summarizes delivery/service exceptions, and drafts case updates.
   - Success criteria: measurable handling-time or task-completion improvement, high grounded-answer accuracy, zero unauthorized writes, complete auditability, and acceptable Azure/Databricks cost.

8. **Select one batch-first predictive ML pilot**
   - Candidate: runout-risk prioritization, demand forecasting, delivery-exception prioritization, or service-volume forecasting.
   - Define business owner, baseline, error-cost assumptions, operational workflow, human review capacity, and measurable impact before development.

9. **Establish MCP/tool onboarding governance**
   - Maintain an approved registry of agent tools/MCP servers.
   - Require application-owner approval, security review, schema/input validation, data classification, authentication design, logging, patching, versioning, and support ownership.

10. **Implement cost and production controls before broad access**
   - Require project tags, quotas, budgets, token monitoring, endpoint limits, cluster policies, idle shutdown, and showback/chargeback visibility.
   - Require product owner, security/privacy review, business KPI, support model, and cost estimate before prototype promotion to production.

## Full transcript

[00:10] Hi, welcome to Blueprint Plus+ a webinar
[00:10] Hi, welcome to Blueprint Plus+ a webinar series in intersection of business and
[00:12] series in intersection of business and
[00:12] series in intersection of business and technology and our guest today is Duf
[00:15] technology and our guest today is Duf
[00:15] technology and our guest today is Duf Galati a product leader at Aden. Hi
[00:18] Galati a product leader at Aden. Hi
[00:18] Galati a product leader at Aden. Hi Droo, nice to see you here. So uh let's
[00:21] Droo, nice to see you here. So uh let's
[00:21] Droo, nice to see you here. So uh let's start with a little background. Could
[00:22] start with a little background. Could
[00:22] start with a little background. Could you tell a bit about yourself, how you
[00:24] you tell a bit about yourself, how you
[00:24] you tell a bit about yourself, how you got here and what you're working on
[00:26] got here and what you're working on
[00:26] got here and what you're working on right now?
[00:27] right now?
[00:27] right now? &gt;&gt; Sure. Um yeah so my background I
[00:29] &gt;&gt; Sure. Um yeah so my background I
[00:29] &gt;&gt; Sure. Um yeah so my background I actually started off my career in
[00:31] actually started off my career in
[00:31] actually started off my career in finance and banking. Uh I my first job
[00:33] finance and banking. Uh I my first job
[00:33] finance and banking. Uh I my first job was at Meil Lynch on the trading floor.
[00:36] was at Meil Lynch on the trading floor.
[00:36] was at Meil Lynch on the trading floor. So I have I had nothing to do with
[00:37] So I have I had nothing to do with
[00:37] So I have I had nothing to do with technology but this was around 2014 I
[00:40] technology but this was around 2014 I
[00:40] technology but this was around 2014 I got very interested in in tech and got
[00:43] got very interested in in tech and got
[00:43] got very interested in in tech and got into AI back then. Yeah. And then my
[00:45] into AI back then. Yeah. And then my
[00:46] into AI back then. Yeah. And then my career has spanned kind of being an
[00:48] career has spanned kind of being an
[00:48] career has spanned kind of being an early stage founder. Um I was in London
[00:50] early stage founder. Um I was in London
[00:50] early stage founder. Um I was in London and I was working on a company that was
[00:52] and I was working on a company that was
[00:52] and I was working on a company that was detecting misinformation, disinformation
[00:54] detecting misinformation, disinformation
[00:54] detecting misinformation, disinformation online. And then after exiting my first
[00:57] online. And then after exiting my first
[00:57] online. And then after exiting my first company um I decided to tune in and hone
[01:00] company um I decided to tune in and hone
[01:00] company um I decided to tune in and hone in some of the skill sets that I wanted
[01:02] in some of the skill sets that I wanted
[01:02] in some of the skill sets that I wanted to gain which is around AI product
[01:04] to gain which is around AI product
[01:04] to gain which is around AI product management because I think
[01:05] management because I think
[01:05] management because I think &gt;&gt; I felt that to be a great technical
[01:08] &gt;&gt; I felt that to be a great technical
[01:08] &gt;&gt; I felt that to be a great technical leader um and and be a great
[01:10] leader um and and be a great
[01:10] leader um and and be a great entrepreneur actually you have to
[01:12] entrepreneur actually you have to
[01:12] entrepreneur actually you have to understand product. Then I moved to
[01:14] understand product. Then I moved to
[01:14] understand product. Then I moved to Amsterdam uh where I was leading out um
[01:17] Amsterdam uh where I was leading out um
[01:17] Amsterdam uh where I was leading out um the Uber AI team on product um in
[01:19] the Uber AI team on product um in
[01:19] the Uber AI team on product um in Amsterdam. So I was the first site lead
[01:21] Amsterdam. So I was the first site lead
[01:21] Amsterdam. So I was the first site lead here. Um, so worked on a lot of
[01:23] here. Um, so worked on a lot of
[01:23] here. Um, so worked on a lot of interesting AI problems across mobility,
[01:25] interesting AI problems across mobility,
[01:25] interesting AI problems across mobility, Uber Eatats, delivery, forecasting
[01:27] Uber Eatats, delivery, forecasting
[01:27] Uber Eatats, delivery, forecasting problems, and we can talk talk a bit
[01:29] problems, and we can talk talk a bit
[01:29] problems, and we can talk talk a bit about those. Um, and currently I'm a
[01:31] about those. Um, and currently I'm a
[01:31] about those. Um, and currently I'm a principal PM at Aden. So I'm I'm leading
[01:33] principal PM at Aden. So I'm I'm leading
[01:33] principal PM at Aden. So I'm I'm leading out some of their their goals of
[01:35] out some of their their goals of
[01:35] out some of their their goals of becoming and and building out some of
[01:37] becoming and and building out some of
[01:37] becoming and and building out some of their their AI products u for payments.
[01:39] their their AI products u for payments.
[01:39] their their AI products u for payments. &gt;&gt; Mhm.
[01:40] &gt;&gt; Mhm.
[01:40] &gt;&gt; Mhm. &gt;&gt; Yeah. And you've been telling about the
[01:42] &gt;&gt; Yeah. And you've been telling about the
[01:42] &gt;&gt; Yeah. And you've been telling about the uh your first startup basically
[01:44] uh your first startup basically
[01:44] uh your first startup basically matter. Uh so how do you feel nowadays
[01:47] matter. Uh so how do you feel nowadays
[01:47] matter. Uh so how do you feel nowadays uh about the fact that you've started
[01:50] uh about the fact that you've started
[01:50] uh about the fact that you've started using um machine learning methods and
[01:52] using um machine learning methods and
[01:52] using um machine learning methods and PhD folks were uh in your company
[01:55] PhD folks were uh in your company
[01:55] PhD folks were uh in your company working on facteing but nowadays machine
[01:58] working on facteing but nowadays machine
[01:58] working on facteing but nowadays machine learning capabilities are more kind of a
[02:00] learning capabilities are more kind of a
[02:00] learning capabilities are more kind of a contributing into that problem. I'd say
[02:02] contributing into that problem. I'd say
[02:02] contributing into that problem. I'd say like a lot of my my my career has been
[02:04] like a lot of my my my career has been
[02:04] like a lot of my my my career has been about I guess like my company was
[02:06] about I guess like my company was
[02:06] about I guess like my company was detecting information that you just
[02:08] detecting information that you just
[02:08] detecting information that you just don't want to have on your website or on
[02:09] don't want to have on your website or on
[02:09] don't want to have on your website or on your ad network and it was kind of
[02:11] your ad network and it was kind of
[02:11] your ad network and it was kind of detecting bad things, right? Same thing
[02:12] detecting bad things, right? Same thing
[02:12] detecting bad things, right? Same thing with uh when I was at Onfido I was
[02:14] with uh when I was at Onfido I was
[02:14] with uh when I was at Onfido I was detecting counterfeits and forged
[02:16] detecting counterfeits and forged
[02:16] detecting counterfeits and forged documents. So um now even at at uh at
[02:20] documents. So um now even at at uh at
[02:20] documents. So um now even at at uh at Aden I'm working on chargeback fraud
[02:22] Aden I'm working on chargeback fraud
[02:22] Aden I'm working on chargeback fraud detection. So I've always been detecting
[02:24] detection. So I've always been detecting
[02:24] detection. So I've always been detecting kind of fraud bad things and I think
[02:26] kind of fraud bad things and I think
[02:26] kind of fraud bad things and I think that to understand and be able to do
[02:29] that to understand and be able to do
[02:29] that to understand and be able to do that effectively you have to understand
[02:30] that effectively you have to understand
[02:30] that effectively you have to understand how that information is generated.
[02:33] how that information is generated.
[02:33] how that information is generated. &gt;&gt; You have to go very deep into fraud
[02:35] &gt;&gt; You have to go very deep into fraud
[02:35] &gt;&gt; You have to go very deep into fraud patterns you know generative AI for
[02:38] patterns you know generative AI for
[02:38] patterns you know generative AI for disinformation creation. What is the
[02:40] disinformation creation. What is the
[02:40] disinformation creation. What is the motivation of the attacker? What is the
[02:42] motivation of the attacker? What is the
[02:42] motivation of the attacker? What is the motivation of the creator? What
[02:44] motivation of the creator? What
[02:44] motivation of the creator? What techniques are they likely to deploy?
[02:47] techniques are they likely to deploy?
[02:48] techniques are they likely to deploy? &gt;&gt; If you don't understand that you can't
[02:49] &gt;&gt; If you don't understand that you can't
[02:49] &gt;&gt; If you don't understand that you can't build detection systems for that. So,
[02:51] build detection systems for that. So,
[02:51] build detection systems for that. So, um, you know, a lot of this is is is
[02:53] um, you know, a lot of this is is is
[02:53] um, you know, a lot of this is is is actually a cat-and- mouse game. And I
[02:55] actually a cat-and- mouse game. And I
[02:55] actually a cat-and- mouse game. And I think we're going to still have this
[02:56] think we're going to still have this
[02:56] think we're going to still have this through the internet, right? There's
[02:58] through the internet, right? There's
[02:58] through the internet, right? There's always people who there's this wave of
[03:00] always people who there's this wave of
[03:00] always people who there's this wave of of creation of things. Um, and then
[03:03] of creation of things. Um, and then
[03:03] of creation of things. Um, and then there's this wave of regulation and
[03:04] there's this wave of regulation and
[03:04] there's this wave of regulation and moderation and and making sure that
[03:06] moderation and and making sure that
[03:06] moderation and and making sure that things are are safe. Talking about uh
[03:08] things are are safe. Talking about uh
[03:08] things are are safe. Talking about uh Aden actually, so you said chargeback uh
[03:10] Aden actually, so you said chargeback uh
[03:10] Aden actually, so you said chargeback uh fraud detection and it seems like coming
[03:13] fraud detection and it seems like coming
[03:13] fraud detection and it seems like coming through different companies, you've been
[03:15] through different companies, you've been
[03:15] through different companies, you've been getting in more and more government uh
[03:18] getting in more and more government uh
[03:18] getting in more and more government uh companies. So Aden for example is a
[03:20] companies. So Aden for example is a
[03:20] companies. So Aden for example is a financial corporation and probably
[03:22] financial corporation and probably
[03:22] financial corporation and probably chargeback uh detection is a lot more
[03:25] chargeback uh detection is a lot more
[03:25] chargeback uh detection is a lot more governed question and anti fraud
[03:27] governed question and anti fraud
[03:27] governed question and anti fraud detection than for example what was done
[03:29] detection than for example what was done
[03:29] detection than for example what was done in a fido or before that in a fact
[03:31] in a fido or before that in a fact
[03:31] in a fido or before that in a fact matter so how do you feel about that
[03:33] matter so how do you feel about that
[03:33] matter so how do you feel about that whole governance procedures that are
[03:35] whole governance procedures that are
[03:35] whole governance procedures that are being applied in aden how did it change
[03:37] being applied in aden how did it change
[03:37] being applied in aden how did it change from the other companies and how does it
[03:39] from the other companies and how does it
[03:39] from the other companies and how does it affect the AI capabilities that you are
[03:41] affect the AI capabilities that you are
[03:41] affect the AI capabilities that you are able to use in the company
[03:43] able to use in the company
[03:43] able to use in the company &gt;&gt; yeah interesting yeah I think I think um
[03:45] &gt;&gt; yeah interesting yeah I think I think um
[03:45] &gt;&gt; yeah interesting yeah I think I think um I think your question is a a lot about
[03:47] I think your question is a a lot about
[03:47] I think your question is a a lot about sort of what are the different ranges of
[03:49] sort of what are the different ranges of
[03:49] sort of what are the different ranges of security that you need to have towards
[03:50] security that you need to have towards
[03:50] security that you need to have towards towards AI models. Um
[03:53] towards AI models. Um
[03:53] towards AI models. Um &gt;&gt; the fact is I think in the last kind of
[03:56] &gt;&gt; the fact is I think in the last kind of
[03:56] &gt;&gt; the fact is I think in the last kind of probably and it's accelerated
[03:57] probably and it's accelerated
[03:57] probably and it's accelerated particularly in Europe, right? We've had
[03:59] particularly in Europe, right? We've had
[03:59] particularly in Europe, right? We've had the AI act that's been coming out and I
[04:01] the AI act that's been coming out and I
[04:01] the AI act that's been coming out and I think that's meant to go live. I I don't
[04:02] think that's meant to go live. I I don't
[04:02] think that's meant to go live. I I don't know the exact date, but I think that
[04:04] know the exact date, but I think that
[04:04] know the exact date, but I think that might actually be live now.
[04:05] might actually be live now.
[04:05] might actually be live now. &gt;&gt; Yeah.
[04:06] &gt;&gt; Yeah.
[04:06] &gt;&gt; Yeah. &gt;&gt; Um but but a lot of the wave has been to
[04:09] &gt;&gt; Um but but a lot of the wave has been to
[04:09] &gt;&gt; Um but but a lot of the wave has been to for AI regulators um and and and
[04:12] for AI regulators um and and and
[04:12] for AI regulators um and and and governments to be sort of trying to
[04:13] governments to be sort of trying to
[04:14] governments to be sort of trying to catch up, right? because AI has moved so
[04:17] catch up, right? because AI has moved so
[04:17] catch up, right? because AI has moved so quickly that um you know you don't want
[04:19] quickly that um you know you don't want
[04:19] quickly that um you know you don't want to be in a regulatory situation where
[04:22] to be in a regulatory situation where
[04:22] to be in a regulatory situation where effectively the regulation is is is
[04:24] effectively the regulation is is is
[04:24] effectively the regulation is is is slowing things down for no reason or the
[04:27] slowing things down for no reason or the
[04:27] slowing things down for no reason or the actual regulation makes zero sense. I
[04:29] actual regulation makes zero sense. I
[04:29] actual regulation makes zero sense. I think one of the the the key things that
[04:31] think one of the the the key things that
[04:31] think one of the the the key things that you typically had with AI is like what
[04:32] you typically had with AI is like what
[04:32] you typically had with AI is like what what data is it trained on?
[04:34] what data is it trained on?
[04:34] what data is it trained on? &gt;&gt; Mhm.
[04:35] &gt;&gt; Mhm.
[04:35] &gt;&gt; Mhm. &gt;&gt; So you know does it contain personal
[04:37] &gt;&gt; So you know does it contain personal
[04:37] &gt;&gt; So you know does it contain personal information? Is it trained on
[04:39] information? Is it trained on
[04:39] information? Is it trained on information that's kind of like a
[04:40] information that's kind of like a
[04:40] information that's kind of like a personally identifiable?
[04:41] personally identifiable?
[04:41] personally identifiable? &gt;&gt; Yeah. Does it have biases?
[04:43] &gt;&gt; Yeah. Does it have biases?
[04:43] &gt;&gt; Yeah. Does it have biases? &gt;&gt; For sure. does it have biases in the
[04:45] &gt;&gt; For sure. does it have biases in the
[04:45] &gt;&gt; For sure. does it have biases in the training data? But then there's the
[04:46] training data? But then there's the
[04:46] training data? But then there's the decision element, right? So if you have
[04:49] decision element, right? So if you have
[04:49] decision element, right? So if you have uh AI models that are taking real
[04:50] uh AI models that are taking real
[04:50] uh AI models that are taking real decisions where they actually affect
[04:52] decisions where they actually affect
[04:52] decisions where they actually affect people's lives, um that's where AI
[04:55] people's lives, um that's where AI
[04:55] people's lives, um that's where AI regulation has has has focused very
[04:56] regulation has has has focused very
[04:56] regulation has has has focused very heavily, right? So whether it's for
[04:58] heavily, right? So whether it's for
[04:58] heavily, right? So whether it's for example getting a loan application
[05:00] example getting a loan application
[05:00] example getting a loan application denied or accepted. Mhm.
[05:01] denied or accepted. Mhm.
[05:01] denied or accepted. Mhm. &gt;&gt; Um, we're going to go through a lot of
[05:03] &gt;&gt; Um, we're going to go through a lot of
[05:03] &gt;&gt; Um, we're going to go through a lot of that now because you're going to have
[05:05] that now because you're going to have
[05:05] that now because you're going to have agents, you know, as you have a world
[05:08] agents, you know, as you have a world
[05:08] agents, you know, as you have a world where the the the drive is to automate
[05:11] where the the the drive is to automate
[05:11] where the the the drive is to automate as many things as possible and manual
[05:12] as many things as possible and manual
[05:12] as many things as possible and manual processes. You got to remember they were
[05:14] processes. You got to remember they were
[05:14] processes. You got to remember they were manual for a reason. You had a human in
[05:16] manual for a reason. You had a human in
[05:16] manual for a reason. You had a human in a loop in for a reason to do that loan
[05:18] a loop in for a reason to do that loan
[05:18] a loop in for a reason to do that loan application or to do the mortgage
[05:20] application or to do the mortgage
[05:20] application or to do the mortgage application. Um and then I think now
[05:23] application. Um and then I think now
[05:23] application. Um and then I think now regulators are sort of looking at um
[05:25] regulators are sort of looking at um
[05:25] regulators are sort of looking at um what you know it is a human in the loop
[05:28] what you know it is a human in the loop
[05:28] what you know it is a human in the loop because you actually need the human
[05:29] because you actually need the human
[05:29] because you actually need the human expertise or actually could a could a
[05:31] expertise or actually could a could a
[05:31] expertise or actually could a could a machine be doing this in a more fair
[05:33] machine be doing this in a more fair
[05:33] machine be doing this in a more fair way. Um I think that's the question that
[05:35] way. Um I think that's the question that
[05:35] way. Um I think that's the question that regulators are are asking. I think
[05:37] regulators are are asking. I think
[05:37] regulators are are asking. I think another part of your question was around
[05:39] another part of your question was around
[05:39] another part of your question was around um you know how have I seen the
[05:41] um you know how have I seen the
[05:41] um you know how have I seen the different ranges of how AI company or or
[05:44] different ranges of how AI company or or
[05:44] different ranges of how AI company or or tech companies basically open up their
[05:46] tech companies basically open up their
[05:46] tech companies basically open up their data. I think um you have on the one
[05:49] data. I think um you have on the one
[05:49] data. I think um you have on the one hand of the spectrum you have very
[05:51] hand of the spectrum you have very
[05:51] hand of the spectrum you have very locked down closed user groups and user
[05:54] locked down closed user groups and user
[05:54] locked down closed user groups and user permissions where certain parts of the
[05:56] permissions where certain parts of the
[05:56] permissions where certain parts of the codebase are just not accessible to
[05:58] codebase are just not accessible to
[05:58] codebase are just not accessible to other people. Um you have um you know
[06:01] other people. Um you have um you know
[06:01] other people. Um you have um you know limitations on on downloading code or
[06:04] limitations on on downloading code or
[06:04] limitations on on downloading code or downloading files to local files. That's
[06:07] downloading files to local files. That's
[06:07] downloading files to local files. That's another thing that I've seen. Um you've
[06:09] another thing that I've seen. Um you've
[06:09] another thing that I've seen. Um you've had just access permissions denied. uh
[06:11] had just access permissions denied. uh
[06:11] had just access permissions denied. uh you've had sort of trying to ring fence
[06:14] you've had sort of trying to ring fence
[06:14] you've had sort of trying to ring fence access to data versus access to code
[06:16] access to data versus access to code
[06:16] access to data versus access to code versus access to um certain types of
[06:18] versus access to um certain types of
[06:18] versus access to um certain types of tools whether it's your CFKA pipelines
[06:20] tools whether it's your CFKA pipelines
[06:20] tools whether it's your CFKA pipelines or whether it's your um
[06:22] or whether it's your um
[06:22] or whether it's your um &gt;&gt; production databases
[06:23] &gt;&gt; production databases
[06:23] &gt;&gt; production databases &gt;&gt; production databases um I've seen and
[06:27] &gt;&gt; production databases um I've seen and
[06:27] &gt;&gt; production databases um I've seen and then on the other end of the spectrum
[06:28] then on the other end of the spectrum
[06:28] then on the other end of the spectrum when you have an early stage company um
[06:30] when you have an early stage company um
[06:30] when you have an early stage company um you have situations where just everyone
[06:32] you have situations where just everyone
[06:32] you have situations where just everyone has access to everything you don't have
[06:33] has access to everything you don't have
[06:33] has access to everything you don't have time to have that annoying thing where
[06:35] time to have that annoying thing where
[06:35] time to have that annoying thing where you're trying to access some information
[06:37] you're trying to access some information
[06:37] you're trying to access some information you don't have access that is a
[06:38] you don't have access that is a
[06:38] you don't have access that is a &gt;&gt; that's a pain right if you're trying to
[06:40] &gt;&gt; that's a pain right if you're trying to
[06:40] &gt;&gt; that's a pain right if you're trying to move move fast. I think that's basically
[06:43] move move fast. I think that's basically
[06:43] move move fast. I think that's basically the thing that companies are going
[06:44] the thing that companies are going
[06:44] the thing that companies are going through where they put all these access
[06:46] through where they put all these access
[06:46] through where they put all these access controls in place for a reason and now
[06:48] controls in place for a reason and now
[06:48] controls in place for a reason and now we're going to have to question like why
[06:50] we're going to have to question like why
[06:50] we're going to have to question like why are those what is the biggest risk that
[06:52] are those what is the biggest risk that
[06:52] are those what is the biggest risk that we can face by giving people access
[06:55] we can face by giving people access
[06:55] we can face by giving people access &gt;&gt; to that right whether it's a product
[06:56] &gt;&gt; to that right whether it's a product
[06:56] &gt;&gt; to that right whether it's a product manager whether it's a saleserson is the
[06:59] manager whether it's a saleserson is the
[06:59] manager whether it's a saleserson is the risk that they're going to for example
[07:00] risk that they're going to for example
[07:00] risk that they're going to for example interpret the data incorrectly and then
[07:02] interpret the data incorrectly and then
[07:02] interpret the data incorrectly and then that's going to lead to some some
[07:03] that's going to lead to some some
[07:03] that's going to lead to some some outcomes that incorrect
[07:05] outcomes that incorrect
[07:05] outcomes that incorrect &gt;&gt; um when they're you know from a data
[07:08] &gt;&gt; um when they're you know from a data
[07:08] &gt;&gt; um when they're you know from a data access perspective is it that your
[07:10] access perspective is it that your
[07:10] access perspective is it that your you're scared of someone basically
[07:11] you're scared of someone basically
[07:11] you're scared of someone basically accessing the code, deleting some code.
[07:14] accessing the code, deleting some code.
[07:14] accessing the code, deleting some code. Um, I think you can create I think
[07:17] Um, I think you can create I think
[07:17] Um, I think you can create I think agents actually have a chance to create
[07:18] agents actually have a chance to create
[07:18] agents actually have a chance to create these p permission layers automatically,
[07:21] these p permission layers automatically,
[07:21] these p permission layers automatically, right? Um, whereas in the past it's been
[07:24] right? Um, whereas in the past it's been
[07:24] right? Um, whereas in the past it's been really manual to make
[07:25] really manual to make
[07:26] really manual to make &gt;&gt; you have to have a security expert.
[07:27] &gt;&gt; you have to have a security expert.
[07:27] &gt;&gt; you have to have a security expert. Yeah,
[07:27] Yeah,
[07:27] Yeah, &gt;&gt; you had to security expert, but you also
[07:29] &gt;&gt; you had to security expert, but you also
[07:29] &gt;&gt; you had to security expert, but you also have lots lots of meetings internally of
[07:31] have lots lots of meetings internally of
[07:31] have lots lots of meetings internally of like who gets access to this, who gets
[07:33] like who gets access to this, who gets
[07:33] like who gets access to this, who gets access to that. Different levels of
[07:35] access to that. Different levels of
[07:35] access to that. Different levels of permissioning I've seen. I think it has
[07:37] permissioning I've seen. I think it has
[07:37] permissioning I've seen. I think it has a benefit, right? Um but I think um well
[07:41] a benefit, right? Um but I think um well
[07:41] a benefit, right? Um but I think um well like with any security problem like you
[07:43] like with any security problem like you
[07:43] like with any security problem like you only know uh when things go wrong,
[07:46] only know uh when things go wrong,
[07:46] only know uh when things go wrong, right? So so it's kind of one of those
[07:48] right? So so it's kind of one of those
[07:48] right? So so it's kind of one of those things of like okay do we keep all this
[07:50] things of like okay do we keep all this
[07:50] things of like okay do we keep all this architecture going of these like really
[07:52] architecture going of these like really
[07:52] architecture going of these like really intense user access permissions? What
[07:54] intense user access permissions? What
[07:54] intense user access permissions? What are the risks or is actually is that
[07:56] are the risks or is actually is that
[07:56] are the risks or is actually is that slowing down our progress? Um do you see
[07:59] slowing down our progress? Um do you see
[07:59] slowing down our progress? Um do you see the uh do you see there a parallel with
[08:01] the uh do you see there a parallel with
[08:01] the uh do you see there a parallel with basically an application of agents? So
[08:03] basically an application of agents? So
[08:03] basically an application of agents? So as far as far as I see that uh when you
[08:06] as far as far as I see that uh when you
[08:06] as far as far as I see that uh when you have a small startup you have indeed
[08:09] have a small startup you have indeed
[08:09] have a small startup you have indeed access to everything in a lot of cases
[08:11] access to everything in a lot of cases
[08:11] access to everything in a lot of cases founder is the only one who is able to
[08:13] founder is the only one who is able to
[08:13] founder is the only one who is able to fix production right now and the same is
[08:15] fix production right now and the same is
[08:15] fix production right now and the same is actually happening with the companies
[08:17] actually happening with the companies
[08:17] actually happening with the companies who are trying to become more of a
[08:19] who are trying to become more of a
[08:19] who are trying to become more of a companies. They do see actually influx
[08:20] companies. They do see actually influx
[08:20] companies. They do see actually influx of like tens of thousands of new
[08:23] of like tens of thousands of new
[08:23] of like tens of thousands of new developers agents which actually have
[08:26] developers agents which actually have
[08:26] developers agents which actually have the very similar problems with
[08:27] the very similar problems with
[08:27] the very similar problems with permissions with trying to access the
[08:29] permissions with trying to access the
[08:29] permissions with trying to access the production database or trying to drop
[08:31] production database or trying to drop
[08:31] production database or trying to drop something. Do you see the barrel here?
[08:33] something. Do you see the barrel here?
[08:33] something. Do you see the barrel here? &gt;&gt; Big time. I think I think one of the
[08:35] &gt;&gt; Big time. I think I think one of the
[08:35] &gt;&gt; Big time. I think I think one of the biggest things that that AI native
[08:37] biggest things that that AI native
[08:37] biggest things that that AI native companies are starting to do is is is
[08:39] companies are starting to do is is is
[08:39] companies are starting to do is is is for example just create MCPs create
[08:41] for example just create MCPs create
[08:41] for example just create MCPs create access to all these different tools that
[08:43] access to all these different tools that
[08:43] access to all these different tools that they were using.
[08:44] they were using.
[08:44] they were using. &gt;&gt; Um and it's magic when you can actually
[08:46] &gt;&gt; Um and it's magic when you can actually
[08:46] &gt;&gt; Um and it's magic when you can actually do that. You know uh you know I know
[08:48] do that. You know uh you know I know
[08:48] do that. You know uh you know I know that uh you know at a for example we
[08:50] that uh you know at a for example we
[08:50] that uh you know at a for example we have an internal team that's built this
[08:51] have an internal team that's built this
[08:52] have an internal team that's built this this this system for UTRA which is our
[08:54] this this system for UTRA which is our
[08:54] this this system for UTRA which is our kind of like task tracking system.
[08:57] kind of like task tracking system.
[08:57] kind of like task tracking system. &gt;&gt; Right. Yeah. So, so that basically, you
[08:59] &gt;&gt; Right. Yeah. So, so that basically, you
[08:59] &gt;&gt; Right. Yeah. So, so that basically, you know, like I was doing this yesterday,
[09:01] know, like I was doing this yesterday,
[09:01] know, like I was doing this yesterday, you know, a PM can basically start
[09:02] you know, a PM can basically start
[09:02] you know, a PM can basically start editing tickets, you know, on their
[09:04] editing tickets, you know, on their
[09:04] editing tickets, you know, on their terminal and and and adjusting them,
[09:06] terminal and and and adjusting them,
[09:06] terminal and and and adjusting them, changing the statuses, doing them in
[09:08] changing the statuses, doing them in
[09:08] changing the statuses, doing them in bulk. I mean, that would have taken so
[09:10] bulk. I mean, that would have taken so
[09:10] bulk. I mean, that would have taken so long,
[09:11] long,
[09:11] long, &gt;&gt; you know, pointing and clicking at at
[09:12] &gt;&gt; you know, pointing and clicking at at
[09:12] &gt;&gt; you know, pointing and clicking at at certain things. So, I think
[09:14] certain things. So, I think
[09:14] certain things. So, I think &gt;&gt; just that magical unlock of of unlocking
[09:17] &gt;&gt; just that magical unlock of of unlocking
[09:17] &gt;&gt; just that magical unlock of of unlocking access to your tools, I think every
[09:19] access to your tools, I think every
[09:19] access to your tools, I think every single um SAS company has to have an MCP
[09:22] single um SAS company has to have an MCP
[09:22] single um SAS company has to have an MCP strategy right now. And because the the
[09:25] strategy right now. And because the the
[09:25] strategy right now. And because the the the magic of of opening that up for like
[09:29] the magic of of opening that up for like
[09:29] the magic of of opening that up for like a new user base is is is huge, right?
[09:31] a new user base is is is huge, right?
[09:31] a new user base is is is huge, right? Like people really want to see, okay,
[09:32] Like people really want to see, okay,
[09:32] Like people really want to see, okay, does this that's how I think, right?
[09:34] does this that's how I think, right?
[09:34] does this that's how I think, right? Like does this tool have an MCP or not?
[09:36] Like does this tool have an MCP or not?
[09:36] Like does this tool have an MCP or not? Is it integrated? Is it open?
[09:38] Is it integrated? Is it open?
[09:38] Is it integrated? Is it open? &gt;&gt; Um in a way we're in the we're in the
[09:40] &gt;&gt; Um in a way we're in the we're in the
[09:40] &gt;&gt; Um in a way we're in the we're in the same kind of world of APIs, right? Like
[09:43] same kind of world of APIs, right? Like
[09:43] same kind of world of APIs, right? Like okay, does this thing is this is this
[09:45] okay, does this thing is this is this
[09:45] okay, does this thing is this is this promoting an open ecosystem? M um and I
[09:48] promoting an open ecosystem? M um and I
[09:48] promoting an open ecosystem? M um and I think that's where um companies can
[09:50] think that's where um companies can
[09:50] think that's where um companies can really start like actually like the the
[09:52] really start like actually like the the
[09:52] really start like actually like the the the unlock you can get from creating
[09:54] the unlock you can get from creating
[09:54] the unlock you can get from creating toolkits and skills for your tools MCPS
[09:57] toolkits and skills for your tools MCPS
[09:58] toolkits and skills for your tools MCPS you know and access um creating little
[10:00] you know and access um creating little
[10:00] you know and access um creating little use cases and builders for like
[10:02] use cases and builders for like
[10:02] use cases and builders for like interacting with your data information
[10:04] interacting with your data information
[10:04] interacting with your data information um that's going to be a real unlock I
[10:06] um that's going to be a real unlock I
[10:06] um that's going to be a real unlock I think for for for
[10:07] think for for for
[10:07] think for for for &gt;&gt; talking about unlock so uh you've been
[10:09] &gt;&gt; talking about unlock so uh you've been
[10:09] &gt;&gt; talking about unlock so uh you've been before in Uber and there is a very
[10:11] before in Uber and there is a very
[10:11] before in Uber and there is a very well-known nowadays Michelangelo
[10:13] well-known nowadays Michelangelo
[10:13] well-known nowadays Michelangelo platform uh that was created in Uber and
[10:15] platform uh that was created in Uber and
[10:15] platform uh that was created in Uber and that is as far as understand unlock
[10:16] that is as far as understand unlock
[10:16] that is as far as understand unlock talking a lot of EA capabilities inside
[10:18] talking a lot of EA capabilities inside
[10:18] talking a lot of EA capabilities inside of that. Could you tell a bit more about
[10:20] of that. Could you tell a bit more about
[10:20] of that. Could you tell a bit more about &gt;&gt; Yeah, I think I think Uber was is a very
[10:22] &gt;&gt; Yeah, I think I think Uber was is a very
[10:22] &gt;&gt; Yeah, I think I think Uber was is a very advanced company when it comes to and
[10:24] advanced company when it comes to and
[10:24] advanced company when it comes to and I've I've definitely now I've seen
[10:26] I've I've definitely now I've seen
[10:26] I've I've definitely now I've seen different ranges of people on the on the
[10:28] different ranges of people on the on the
[10:28] different ranges of people on the on the stack. Um Uber built Michelangelo where
[10:31] stack. Um Uber built Michelangelo where
[10:31] stack. Um Uber built Michelangelo where effectively the idea was they had they
[10:33] effectively the idea was they had they
[10:33] effectively the idea was they had they had a marketplace real-time algorithm
[10:34] had a marketplace real-time algorithm
[10:34] had a marketplace real-time algorithm where people you know drivers and and
[10:36] where people you know drivers and and
[10:36] where people you know drivers and and and riders are being matched in real
[10:38] and riders are being matched in real
[10:38] and riders are being matched in real time. M
[10:38] time. M
[10:38] time. M &gt;&gt; it's incredibly hard to do that you know
[10:41] &gt;&gt; it's incredibly hard to do that you know
[10:41] &gt;&gt; it's incredibly hard to do that you know you're running models at scale low
[10:43] you're running models at scale low
[10:43] you're running models at scale low latency you know in real time with with
[10:46] latency you know in real time with with
[10:46] latency you know in real time with with constant pinging different times
[10:48] constant pinging different times
[10:48] constant pinging different times different time zones uh you have to keep
[10:50] different time zones uh you have to keep
[10:50] different time zones uh you have to keep the systems up at all times and you have
[10:52] the systems up at all times and you have
[10:52] the systems up at all times and you have to have uh redundancy you have to check
[10:55] to have uh redundancy you have to check
[10:55] to have uh redundancy you have to check around observability at all times this
[10:58] around observability at all times this
[10:58] around observability at all times this this machine learning infrastructure
[11:00] this machine learning infrastructure
[11:00] this machine learning infrastructure they had to build systems to make that
[11:02] they had to build systems to make that
[11:02] they had to build systems to make that that easy and possible
[11:04] that easy and possible
[11:04] that easy and possible &gt;&gt; and that was the birth of Michelangelo u
[11:06] &gt;&gt; and that was the birth of Michelangelo u
[11:06] &gt;&gt; and that was the birth of Michelangelo u but since then what that enabled was
[11:08] but since then what that enabled was
[11:08] but since then what that enabled was that, you know, as as an organization,
[11:10] that, you know, as as an organization,
[11:10] that, you know, as as an organization, as the organization grew, you had all
[11:13] as the organization grew, you had all
[11:13] as the organization grew, you had all sorts of other teams saying, "Hey, we
[11:14] sorts of other teams saying, "Hey, we
[11:14] sorts of other teams saying, "Hey, we now need to do u marketplace matching of
[11:17] now need to do u marketplace matching of
[11:17] now need to do u marketplace matching of the drivers, but how do we do real-time
[11:19] the drivers, but how do we do real-time
[11:19] the drivers, but how do we do real-time pricing?"
[11:19] pricing?"
[11:19] pricing?" &gt;&gt; Mhm.
[11:20] &gt;&gt; Mhm.
[11:20] &gt;&gt; Mhm. &gt;&gt; You know, um how do we do real-time
[11:21] &gt;&gt; You know, um how do we do real-time
[11:22] &gt;&gt; You know, um how do we do real-time incentives that we give people? How do
[11:24] incentives that we give people? How do
[11:24] incentives that we give people? How do we, you know, run other models that we
[11:26] we, you know, run other models that we
[11:26] we, you know, run other models that we might want to have that do um you know,
[11:30] might want to have that do um you know,
[11:30] might want to have that do um you know, real-time prediction of of where a
[11:31] real-time prediction of of where a
[11:32] real-time prediction of of where a driver should go to predict demand and
[11:33] driver should go to predict demand and
[11:33] driver should go to predict demand and supply? So, the use cases started to
[11:35] supply? So, the use cases started to
[11:35] supply? So, the use cases started to grow. Um, and instead of all of these
[11:38] grow. Um, and instead of all of these
[11:38] grow. Um, and instead of all of these different internal model builders
[11:40] different internal model builders
[11:40] different internal model builders starting to have to compute features for
[11:42] starting to have to compute features for
[11:42] starting to have to compute features for their models again and again
[11:44] their models again and again
[11:44] their models again and again &gt;&gt; or tried to reuse, you know, all the
[11:46] &gt;&gt; or tried to reuse, you know, all the
[11:46] &gt;&gt; or tried to reuse, you know, all the different systems they had to build and
[11:48] different systems they had to build and
[11:48] different systems they had to build and pipelines, whether it was, you know, ML
[11:50] pipelines, whether it was, you know, ML
[11:50] pipelines, whether it was, you know, ML flow or airflow or different DAGs that
[11:53] flow or airflow or different DAGs that
[11:53] flow or airflow or different DAGs that they had to build out, why not reuse
[11:54] they had to build out, why not reuse
[11:54] they had to build out, why not reuse these components? And that was that was
[11:57] these components? And that was that was
[11:57] these components? And that was that was the benefit of Michelangelo. I see that
[11:59] the benefit of Michelangelo. I see that
[12:00] the benefit of Michelangelo. I see that you know the role of an MLOps person you
[12:02] you know the role of an MLOps person you
[12:02] you know the role of an MLOps person you know it's very hard to that was if you
[12:05] know it's very hard to that was if you
[12:05] know it's very hard to that was if you go on LinkedIn now it's actually very
[12:06] go on LinkedIn now it's actually very
[12:06] go on LinkedIn now it's actually very nowadays obviously it's it's a big role
[12:08] nowadays obviously it's it's a big role
[12:08] nowadays obviously it's it's a big role but I think a lot of large corporates
[12:11] but I think a lot of large corporates
[12:11] but I think a lot of large corporates don't sort of don't understand like that
[12:13] don't sort of don't understand like that
[12:13] don't sort of don't understand like that is an actual role it's not a data
[12:15] is an actual role it's not a data
[12:15] is an actual role it's not a data engineer it's an MLOps person um and
[12:17] engineer it's an MLOps person um and
[12:17] engineer it's an MLOps person um and that that goes into the language of
[12:19] that that goes into the language of
[12:19] that that goes into the language of features feature stores um you know uh
[12:22] features feature stores um you know uh
[12:22] features feature stores um you know uh model pipelines uh observability uh
[12:26] model pipelines uh observability uh
[12:26] model pipelines uh observability uh model evaluation metrics retraining
[12:29] model evaluation metrics retraining
[12:29] model evaluation metrics retraining systems, AutoML, it isn't just, you
[12:31] systems, AutoML, it isn't just, you
[12:31] systems, AutoML, it isn't just, you know, data cataloges, data pipelines,
[12:34] know, data cataloges, data pipelines,
[12:34] know, data cataloges, data pipelines, um, uh, it's it's a different language.
[12:36] um, uh, it's it's a different language.
[12:36] um, uh, it's it's a different language. It's
[12:36] It's
[12:36] It's &gt;&gt; a whole system.
[12:37] &gt;&gt; a whole system.
[12:37] &gt;&gt; a whole system. &gt;&gt; It's a whole system. And I think that
[12:39] &gt;&gt; It's a whole system. And I think that
[12:39] &gt;&gt; It's a whole system. And I think that role, um, a lot of, um, companies I'm
[12:42] role, um, a lot of, um, companies I'm
[12:42] role, um, a lot of, um, companies I'm seeing sort of, okay, let's let's hire
[12:43] seeing sort of, okay, let's let's hire
[12:44] seeing sort of, okay, let's let's hire some scientists to to fix, you know,
[12:45] some scientists to to fix, you know,
[12:45] some scientists to to fix, you know, build this model for us. But the model
[12:47] build this model for us. But the model
[12:47] build this model for us. But the model builders can't build a model if there
[12:49] builders can't build a model if there
[12:49] builders can't build a model if there isn't the architecture to run models
[12:51] isn't the architecture to run models
[12:51] isn't the architecture to run models effectively or or run experiments
[12:53] effectively or or run experiments
[12:53] effectively or or run experiments quickly or test them both offline and
[12:55] quickly or test them both offline and
[12:56] quickly or test them both offline and online um to instrument your your test
[12:59] online um to instrument your your test
[12:59] online um to instrument your your test data sets like how do you have
[13:00] data sets like how do you have
[13:00] data sets like how do you have versioning on your test data sets
[13:02] versioning on your test data sets
[13:02] versioning on your test data sets &gt;&gt; all of these things like are um sort of
[13:05] &gt;&gt; all of these things like are um sort of
[13:05] &gt;&gt; all of these things like are um sort of linked to data but they're a different
[13:06] linked to data but they're a different
[13:06] linked to data but they're a different language and so I think that's really
[13:08] language and so I think that's really
[13:08] language and so I think that's really really important for a big business to
[13:11] really important for a big business to
[13:11] really important for a big business to &gt;&gt; really build the infrastructure so that
[13:12] &gt;&gt; really build the infrastructure so that
[13:12] &gt;&gt; really build the infrastructure so that anyone can go in and say hey I have a
[13:14] anyone can go in and say hey I have a
[13:14] anyone can go in and say hey I have a machine learning problem I'm sitting in
[13:16] machine learning problem I'm sitting in
[13:16] machine learning problem I'm sitting in the sales sales department or I'm
[13:17] the sales sales department or I'm
[13:17] the sales sales department or I'm sitting in the marketing department. I
[13:19] sitting in the marketing department. I
[13:19] sitting in the marketing department. I want to build a model. Where do I start?
[13:21] want to build a model. Where do I start?
[13:21] want to build a model. Where do I start? And and you build this internal
[13:23] And and you build this internal
[13:23] And and you build this internal experience. It's really easy for them
[13:25] experience. It's really easy for them
[13:25] experience. It's really easy for them and how to create that model. So it
[13:26] and how to create that model. So it
[13:26] and how to create that model. So it would be production level already.
[13:28] would be production level already.
[13:28] would be production level already. &gt;&gt; Exactly. Yeah.
[13:29] &gt;&gt; Exactly. Yeah.
[13:29] &gt;&gt; Exactly. Yeah. &gt;&gt; Talking about like product culture and
[13:31] &gt;&gt; Talking about like product culture and
[13:31] &gt;&gt; Talking about like product culture and the fact that you are being amplified a
[13:33] the fact that you are being amplified a
[13:33] the fact that you are being amplified a lot with AI agents. You still have a lot
[13:36] lot with AI agents. You still have a lot
[13:36] lot with AI agents. You still have a lot of like standard product metrics and
[13:38] of like standard product metrics and
[13:38] of like standard product metrics and standard product approaches. Yeah. uh it
[13:41] standard product approaches. Yeah. uh it
[13:41] standard product approaches. Yeah. uh it doesn't probably matter whether you are
[13:43] doesn't probably matter whether you are
[13:43] doesn't probably matter whether you are like uh helping developers to understand
[13:44] like uh helping developers to understand
[13:44] like uh helping developers to understand what they should be doing and what
[13:46] what they should be doing and what
[13:46] what they should be doing and what product we are creating or agents. So
[13:48] product we are creating or agents. So
[13:48] product we are creating or agents. So how do you approach that especially in
[13:50] how do you approach that especially in
[13:50] how do you approach that especially in the era of AI and the agents?
[13:52] the era of AI and the agents?
[13:52] the era of AI and the agents? &gt;&gt; Yeah. So if you have traditional ML
[13:54] &gt;&gt; Yeah. So if you have traditional ML
[13:54] &gt;&gt; Yeah. So if you have traditional ML right like take let's take kind of you
[13:56] right like take let's take kind of you
[13:56] right like take let's take kind of you know fraud detection is a great example
[13:58] know fraud detection is a great example
[13:58] know fraud detection is a great example right you you have precision and you
[14:00] right you you have precision and you
[14:00] right you you have precision and you have recall right and then you have a
[14:02] have recall right and then you have a
[14:02] have recall right and then you have a curve
[14:03] curve
[14:03] curve &gt;&gt; rc curve where you can kind of tune
[14:05] &gt;&gt; rc curve where you can kind of tune
[14:05] &gt;&gt; rc curve where you can kind of tune those things in different ways.
[14:06] those things in different ways.
[14:06] those things in different ways. Precision is effectively in the case of
[14:08] Precision is effectively in the case of
[14:08] Precision is effectively in the case of fraud, you know, like how good how when
[14:10] fraud, you know, like how good how when
[14:10] fraud, you know, like how good how when you do flag something as a fraud, is it
[14:13] you do flag something as a fraud, is it
[14:13] you do flag something as a fraud, is it correct or not?
[14:15] correct or not?
[14:15] correct or not? &gt;&gt; Recall is of the things that you should
[14:17] &gt;&gt; Recall is of the things that you should
[14:17] &gt;&gt; Recall is of the things that you should be catching, what percentage did you
[14:19] be catching, what percentage did you
[14:19] be catching, what percentage did you catch? Um, you know, you could also have
[14:22] catch? Um, you know, you could also have
[14:22] catch? Um, you know, you could also have a system that flags everything and so
[14:24] a system that flags everything and so
[14:24] a system that flags everything and so your recall is 100%. You caught
[14:26] your recall is 100%. You caught
[14:26] your recall is 100%. You caught everything. Um, but then when you caught
[14:28] everything. Um, but then when you caught
[14:28] everything. Um, but then when you caught it, you're going to have a lot of false
[14:29] it, you're going to have a lot of false
[14:29] it, you're going to have a lot of false positives, right? you're going to be. So
[14:31] positives, right? you're going to be. So
[14:31] positives, right? you're going to be. So these these are just like basic
[14:32] these these are just like basic
[14:32] these these are just like basic frameworks that like I think people have
[14:35] frameworks that like I think people have
[14:35] frameworks that like I think people have to just understand like what are the
[14:36] to just understand like what are the
[14:36] to just understand like what are the core ML model metrics
[14:39] core ML model metrics
[14:39] core ML model metrics &gt;&gt; um that honestly like you can deduce by
[14:43] &gt;&gt; um that honestly like you can deduce by
[14:43] &gt;&gt; um that honestly like you can deduce by logic right like it's it's depending on
[14:45] logic right like it's it's depending on
[14:45] logic right like it's it's depending on the problem that that you have right
[14:46] the problem that that you have right
[14:46] the problem that that you have right predictions have the same thing
[14:47] predictions have the same thing
[14:47] predictions have the same thing classification has the same thing in the
[14:50] classification has the same thing in the
[14:50] classification has the same thing in the world of AI where you're building let's
[14:53] world of AI where you're building let's
[14:53] world of AI where you're building let's say a chat assistant uh or you're
[14:55] say a chat assistant uh or you're
[14:55] say a chat assistant uh or you're building you know let's say chat GPT
[14:57] building you know let's say chat GPT
[14:57] building you know let's say chat GPT &gt;&gt; Mhm. your evals are a little bit
[15:00] &gt;&gt; Mhm. your evals are a little bit
[15:00] &gt;&gt; Mhm. your evals are a little bit different, right? Because you have other
[15:03] different, right? Because you have other
[15:03] different, right? Because you have other types of things you have to to
[15:04] types of things you have to to
[15:04] types of things you have to to understand like, okay, was this
[15:05] understand like, okay, was this
[15:06] understand like, okay, was this conversation a good conversation?
[15:09] conversation a good conversation?
[15:09] conversation a good conversation? &gt;&gt; How many multi-turn conversations did
[15:11] &gt;&gt; How many multi-turn conversations did
[15:11] &gt;&gt; How many multi-turn conversations did you have versus one-shot conversations
[15:13] you have versus one-shot conversations
[15:13] you have versus one-shot conversations where you just answered it one time? Um,
[15:16] where you just answered it one time? Um,
[15:16] where you just answered it one time? Um, how many time like what was the average
[15:19] how many time like what was the average
[15:19] how many time like what was the average length of a conversation? um in terms of
[15:23] length of a conversation? um in terms of
[15:23] length of a conversation? um in terms of uh you know e we had this phrase of eval
[15:26] uh you know e we had this phrase of eval
[15:26] uh you know e we had this phrase of eval right and in LLM sort of like how do you
[15:28] right and in LLM sort of like how do you
[15:28] right and in LLM sort of like how do you measure that that response was a good
[15:30] measure that that response was a good
[15:30] measure that that response was a good response versus a bad response cuz it's
[15:32] response versus a bad response cuz it's
[15:32] response versus a bad response cuz it's a subjective thing right for some people
[15:35] a subjective thing right for some people
[15:35] a subjective thing right for some people that would have been a good response
[15:36] that would have been a good response
[15:36] that would have been a good response some people that wouldn't have been a
[15:37] some people that wouldn't have been a
[15:37] some people that wouldn't have been a good response so so there's this element
[15:39] good response so so there's this element
[15:39] good response so so there's this element of how do you kind of try to take a very
[15:42] of how do you kind of try to take a very
[15:42] of how do you kind of try to take a very subjective thing which is a conversation
[15:45] subjective thing which is a conversation
[15:46] subjective thing which is a conversation and try to put quantitative metrics on
[15:48] and try to put quantitative metrics on
[15:48] and try to put quantitative metrics on it yeah do you see the same problem
[15:50] it yeah do you see the same problem
[15:50] it yeah do you see the same problem actually with just uh training of large
[15:53] actually with just uh training of large
[15:53] actually with just uh training of large language models with RHLF and so on.
[15:57] language models with RHLF and so on.
[15:57] language models with RHLF and so on. &gt;&gt; Yeah. So, so as in RHLF used as an eval
[16:01] &gt;&gt; Yeah. So, so as in RHLF used as an eval
[16:01] &gt;&gt; Yeah. So, so as in RHLF used as an eval metric and mainly I think talk about the
[16:04] metric and mainly I think talk about the
[16:04] metric and mainly I think talk about the cases like for example in case of OpenAI
[16:06] cases like for example in case of OpenAI
[16:06] cases like for example in case of OpenAI or Antropic they've been tuning their
[16:08] or Antropic they've been tuning their
[16:08] or Antropic they've been tuning their models with GPT 5 5.1 5.2 trying to be
[16:13] models with GPT 5 5.1 5.2 trying to be
[16:13] models with GPT 5 5.1 5.2 trying to be less friendly more friendly and so on.
[16:14] less friendly more friendly and so on.
[16:14] less friendly more friendly and so on. It's also kind of a product work but for
[16:17] It's also kind of a product work but for
[16:17] It's also kind of a product work but for Language model we're trying to
[16:18] Language model we're trying to
[16:18] Language model we're trying to understand which personality should it
[16:21] understand which personality should it
[16:21] understand which personality should it have. I mean look a lot of those model
[16:24] have. I mean look a lot of those model
[16:24] have. I mean look a lot of those model the way that people are doing this is
[16:25] the way that people are doing this is
[16:25] the way that people are doing this is like like I said it's a subjective thing
[16:27] like like I said it's a subjective thing
[16:27] like like I said it's a subjective thing right so
[16:29] right so
[16:29] right so &gt;&gt; people forget that there's there's
[16:30] &gt;&gt; people forget that there's there's
[16:30] &gt;&gt; people forget that there's there's obviously people who are figuring out
[16:31] obviously people who are figuring out
[16:31] obviously people who are figuring out the model
[16:32] the model
[16:32] the model &gt;&gt; does the model work well and there's a
[16:34] &gt;&gt; does the model work well and there's a
[16:34] &gt;&gt; does the model work well and there's a lot of benchmarks that are built for AI
[16:36] lot of benchmarks that are built for AI
[16:36] lot of benchmarks that are built for AI agents right that that like open source
[16:38] agents right that that like open source
[16:38] agents right that that like open source benchmarks where they're how good are
[16:41] benchmarks where they're how good are
[16:41] benchmarks where they're how good are they on these specific hard-coded tasks
[16:43] they on these specific hard-coded tasks
[16:43] they on these specific hard-coded tasks right
[16:44] right
[16:44] right &gt;&gt; so you can try to close the domain and
[16:45] &gt;&gt; so you can try to close the domain and
[16:46] &gt;&gt; so you can try to close the domain and say okay uh we think that um most of our
[16:49] say okay uh we think that um most of our
[16:49] say okay uh we think that um most of our feedback that we got was that the
[16:51] feedback that we got was that the
[16:51] feedback that we got was that the conversation wasn't very friendly. So if
[16:53] conversation wasn't very friendly. So if
[16:53] conversation wasn't very friendly. So if we make the conversations more in a
[16:55] we make the conversations more in a
[16:55] we make the conversations more in a friendlier tone uh people will be be
[16:57] friendlier tone uh people will be be
[16:57] friendlier tone uh people will be be happier. The challenge is that you have
[16:59] happier. The challenge is that you have
[16:59] happier. The challenge is that you have these internal model metrics but then
[17:01] these internal model metrics but then
[17:01] these internal model metrics but then you have your online actual outcome is
[17:05] you have your online actual outcome is
[17:05] you have your online actual outcome is that is chat GPT growing.
[17:07] that is chat GPT growing.
[17:07] that is chat GPT growing. &gt;&gt; Yeah.
[17:08] &gt;&gt; Yeah.
[17:08] &gt;&gt; Yeah. &gt;&gt; That's what management cares about,
[17:10] &gt;&gt; That's what management cares about,
[17:10] &gt;&gt; That's what management cares about, right? Is is it and and and that may not
[17:13] right? Is is it and and and that may not
[17:13] right? Is is it and and and that may not be at all because of the fact that the
[17:15] be at all because of the fact that the
[17:15] be at all because of the fact that the conversations are friendlier.
[17:17] conversations are friendlier.
[17:17] conversations are friendlier. &gt;&gt; Yeah. It may be that that actually that
[17:19] &gt;&gt; Yeah. It may be that that actually that
[17:19] &gt;&gt; Yeah. It may be that that actually that the cohort that you're going for that
[17:21] the cohort that you're going for that
[17:21] the cohort that you're going for that the next growth segment if you're not
[17:23] the next growth segment if you're not
[17:23] the next growth segment if you're not against the next billion users maybe
[17:25] against the next billion users maybe
[17:25] against the next billion users maybe they don't want friendly conversations.
[17:27] they don't want friendly conversations.
[17:27] they don't want friendly conversations. Maybe they want more targeted um um
[17:32] Maybe they want more targeted um um
[17:32] Maybe they want more targeted um um rationalized conversations that achieve
[17:33] rationalized conversations that achieve
[17:33] rationalized conversations that achieve certain tasks. uh or maybe it's actually
[17:36] certain tasks. uh or maybe it's actually
[17:36] certain tasks. uh or maybe it's actually because the user experience is not very
[17:38] because the user experience is not very
[17:38] because the user experience is not very good um you know for chat or maybe
[17:41] good um you know for chat or maybe
[17:41] good um you know for chat or maybe actually the users that you're targeting
[17:42] actually the users that you're targeting
[17:42] actually the users that you're targeting they need to access spreadsheets very
[17:44] they need to access spreadsheets very
[17:44] they need to access spreadsheets very well and you know the tool calling for
[17:46] well and you know the tool calling for
[17:46] well and you know the tool calling for that isn't very good on on chatbt but
[17:48] that isn't very good on on chatbt but
[17:48] that isn't very good on on chatbt but it's very good for claude so the the the
[17:51] it's very good for claude so the the the
[17:51] it's very good for claude so the the the the the
[17:52] the the
[17:52] the the complexity and the vastness of the space
[17:54] complexity and the vastness of the space
[17:54] complexity and the vastness of the space of metrics that you can have is so so
[17:57] of metrics that you can have is so so
[17:57] of metrics that you can have is so so big I think most ML AI product building
[18:00] big I think most ML AI product building
[18:00] big I think most ML AI product building has to split find the ML metrics the one
[18:04] has to split find the ML metrics the one
[18:04] has to split find the ML metrics the one or two core ML metrics um that
[18:07] or two core ML metrics um that
[18:07] or two core ML metrics um that &gt;&gt; really drive like okay this is a good ML
[18:09] &gt;&gt; really drive like okay this is a good ML
[18:09] &gt;&gt; really drive like okay this is a good ML product
[18:10] product
[18:10] product &gt;&gt; but then the sort of online metrics you
[18:12] &gt;&gt; but then the sort of online metrics you
[18:12] &gt;&gt; but then the sort of online metrics you know which really
[18:13] know which really
[18:13] know which really &gt;&gt; align to them
[18:14] &gt;&gt; align to them
[18:14] &gt;&gt; align to them &gt;&gt; align and and and ideally and this is
[18:16] &gt;&gt; align and and and ideally and this is
[18:16] &gt;&gt; align and and and ideally and this is where people get it very wrong is like
[18:19] where people get it very wrong is like
[18:19] where people get it very wrong is like connecting that together so if I really
[18:21] connecting that together so if I really
[18:21] connecting that together so if I really make
[18:23] make
[18:23] make if if I was to make the um the responses
[18:26] if if I was to make the um the responses
[18:26] if if I was to make the um the responses perfect for every single conversation it
[18:29] perfect for every single conversation it
[18:29] perfect for every single conversation it answered every single question perfectly
[18:32] answered every single question perfectly
[18:32] answered every single question perfectly would that lead to growth of chat GBT
[18:35] would that lead to growth of chat GBT
[18:35] would that lead to growth of chat GBT But uh what do you see else like in a
[18:38] But uh what do you see else like in a
[18:38] But uh what do you see else like in a such a governed company? What are the
[18:40] such a governed company? What are the
[18:40] such a governed company? What are the main methods and things that you should
[18:42] main methods and things that you should
[18:42] main methods and things that you should be thinking about governing the AI
[18:43] be thinking about governing the AI
[18:43] be thinking about governing the AI inside the organization? Yeah. So AI
[18:46] inside the organization? Yeah. So AI
[18:46] inside the organization? Yeah. So AI inside the organization people have to
[18:48] inside the organization people have to
[18:48] inside the organization people have to think about access controls. Um you need
[18:51] think about access controls. Um you need
[18:51] think about access controls. Um you need to have a data catalog, right? What data
[18:54] to have a data catalog, right? What data
[18:54] to have a data catalog, right? What data is being spawned? What data already
[18:55] is being spawned? What data already
[18:55] is being spawned? What data already exists? What jobs are running in the
[18:58] exists? What jobs are running in the
[18:58] exists? What jobs are running in the background? What sub metadata sets are
[19:00] background? What sub metadata sets are
[19:00] background? What sub metadata sets are being created? You need to have a good
[19:01] being created? You need to have a good
[19:01] being created? You need to have a good handle of that. You need to be able to
[19:04] handle of that. You need to be able to
[19:04] handle of that. You need to be able to log it and understand what is actually
[19:05] log it and understand what is actually
[19:05] log it and understand what is actually in that data.
[19:07] in that data.
[19:07] in that data. &gt;&gt; Once you've logged that data, you have
[19:09] &gt;&gt; Once you've logged that data, you have
[19:09] &gt;&gt; Once you've logged that data, you have to understand what are the potential use
[19:10] to understand what are the potential use
[19:10] to understand what are the potential use cases that that data could be used for.
[19:14] cases that that data could be used for.
[19:14] cases that that data could be used for. &gt;&gt; Uh I mentioned before, you know, if you
[19:16] &gt;&gt; Uh I mentioned before, you know, if you
[19:16] &gt;&gt; Uh I mentioned before, you know, if you had data on previous loan applications
[19:18] had data on previous loan applications
[19:18] had data on previous loan applications and if they were reject accepted or
[19:20] and if they were reject accepted or
[19:20] and if they were reject accepted or rejected. Um and you also have features
[19:23] rejected. Um and you also have features
[19:23] rejected. Um and you also have features that tell you what race that person is
[19:26] that tell you what race that person is
[19:26] that tell you what race that person is is in or what country they're from. you
[19:28] is in or what country they're from. you
[19:28] is in or what country they're from. you can maybe you're not doing it now but
[19:30] can maybe you're not doing it now but
[19:30] can maybe you're not doing it now but you can possibly understand that that
[19:32] you can possibly understand that that
[19:32] you can possibly understand that that could be used you know as you're
[19:34] could be used you know as you're
[19:34] could be used you know as you're building a model that that learns from
[19:36] building a model that that learns from
[19:36] building a model that that learns from those features in an incorrect way.
[19:37] those features in an incorrect way.
[19:37] those features in an incorrect way. &gt;&gt; Yeah.
[19:38] &gt;&gt; Yeah.
[19:38] &gt;&gt; Yeah. &gt;&gt; So
[19:39] &gt;&gt; So
[19:39] &gt;&gt; So putting safeguards typically what people
[19:42] putting safeguards typically what people
[19:42] putting safeguards typically what people don't is put safeguards on like testing
[19:44] don't is put safeguards on like testing
[19:44] don't is put safeguards on like testing of the model. So you have kind of red
[19:47] of the model. So you have kind of red
[19:47] of the model. So you have kind of red teaming where the models basically are
[19:49] teaming where the models basically are
[19:49] teaming where the models basically are triple checking are they making
[19:50] triple checking are they making
[19:50] triple checking are they making decisions and learning from those
[19:51] decisions and learning from those
[19:51] decisions and learning from those features too much, right?
[19:53] features too much, right?
[19:53] features too much, right? &gt;&gt; Um or or if you only had those isolated
[19:56] &gt;&gt; Um or or if you only had those isolated
[19:56] &gt;&gt; Um or or if you only had those isolated those features and you just had that as
[19:58] those features and you just had that as
[19:58] those features and you just had that as the feature that that the model was
[20:00] the feature that that the model was
[20:00] the feature that that the model was learning from, would it take what would
[20:02] learning from, would it take what would
[20:02] learning from, would it take what would be the decision boundaries that were
[20:03] be the decision boundaries that were
[20:03] be the decision boundaries that were created from that?
[20:04] created from that?
[20:04] created from that? &gt;&gt; Mhm. Um
[20:07] &gt;&gt; Mhm. Um
[20:07] &gt;&gt; Mhm. Um the the challenge with this is that
[20:10] the the challenge with this is that
[20:10] the the challenge with this is that actually factually it is correct that
[20:13] actually factually it is correct that
[20:13] actually factually it is correct that let's say one race versus another race
[20:15] let's say one race versus another race
[20:15] let's say one race versus another race has been accepted from a loan
[20:17] has been accepted from a loan
[20:17] has been accepted from a loan application but then there was probably
[20:19] application but then there was probably
[20:19] application but then there was probably something wrong in your own system.
[20:21] something wrong in your own system.
[20:21] something wrong in your own system. &gt;&gt; Yeah. Like there is something wrong in
[20:22] &gt;&gt; Yeah. Like there is something wrong in
[20:22] &gt;&gt; Yeah. Like there is something wrong in society basically
[20:23] society basically
[20:23] society basically &gt;&gt; in society. In society but also maybe
[20:25] &gt;&gt; in society. In society but also maybe
[20:25] &gt;&gt; in society. In society but also maybe the way that you had been doing your own
[20:27] the way that you had been doing your own
[20:27] the way that you had been doing your own loan applications as a as a business. So
[20:30] loan applications as a as a business. So
[20:30] loan applications as a as a business. So it's not that you are that the system is
[20:33] it's not that you are that the system is
[20:33] it's not that you are that the system is wrong. it's sort of starting to unlock
[20:35] wrong. it's sort of starting to unlock
[20:35] wrong. it's sort of starting to unlock um changes in the overall actually
[20:38] um changes in the overall actually
[20:38] um changes in the overall actually online system itself. Um
[20:42] online system itself. Um
[20:42] online system itself. Um &gt;&gt; shows basically you something about your
[20:43] &gt;&gt; shows basically you something about your
[20:43] &gt;&gt; shows basically you something about your system. So exactly
[20:44] system. So exactly
[20:44] system. So exactly &gt;&gt; yeah I've actually heard a lot of uh
[20:47] &gt;&gt; yeah I've actually heard a lot of uh
[20:47] &gt;&gt; yeah I've actually heard a lot of uh feedback about some trained systems in
[20:49] feedback about some trained systems in
[20:49] feedback about some trained systems in the big corporations or even trained
[20:51] the big corporations or even trained
[20:51] the big corporations or even trained system in some domains where people are
[20:53] system in some domains where people are
[20:53] system in some domains where people are saying that yeah folks it's like it's
[20:55] saying that yeah folks it's like it's
[20:55] saying that yeah folks it's like it's not correct it should not be working
[20:56] not correct it should not be working
[20:56] not correct it should not be working that way but
[20:57] that way but
[20:57] that way but &gt;&gt; in in the end you find out that it's
[20:59] &gt;&gt; in in the end you find out that it's
[20:59] &gt;&gt; in in the end you find out that it's actually working the way the model is
[21:02] actually working the way the model is
[21:02] actually working the way the model is predicting the problem is not in the
[21:04] predicting the problem is not in the
[21:04] predicting the problem is not in the model the problem in the system
[21:05] model the problem in the system
[21:05] model the problem in the system &gt;&gt; system yeah and and then you can say
[21:06] &gt;&gt; system yeah and and then you can say
[21:06] &gt;&gt; system yeah and and then you can say well look let's even remove that feature
[21:09] well look let's even remove that feature
[21:09] well look let's even remove that feature it's not going to learn from that
[21:10] it's not going to learn from that
[21:10] it's not going to learn from that feature
[21:11] feature
[21:11] feature &gt;&gt; but then then you could then still train
[21:13] &gt;&gt; but then then you could then still train
[21:14] &gt;&gt; but then then you could then still train the system, it would work probably
[21:16] the system, it would work probably
[21:16] the system, it would work probably slightly worse for your task. And so
[21:18] slightly worse for your task. And so
[21:18] slightly worse for your task. And so you've taken a business decision to not
[21:20] you've taken a business decision to not
[21:20] you've taken a business decision to not learn from that feature.
[21:22] learn from that feature.
[21:22] learn from that feature. &gt;&gt; Mhm.
[21:22] &gt;&gt; Mhm.
[21:22] &gt;&gt; Mhm. &gt;&gt; You've effectively got worse at
[21:23] &gt;&gt; You've effectively got worse at
[21:24] &gt;&gt; You've effectively got worse at automated decisioning. Yeah. For loans
[21:26] automated decisioning. Yeah. For loans
[21:26] automated decisioning. Yeah. For loans because you've decided to ignore that
[21:27] because you've decided to ignore that
[21:27] because you've decided to ignore that feature. But then you can if you did a
[21:30] feature. But then you can if you did a
[21:30] feature. But then you can if you did a correlation
[21:32] correlation
[21:32] correlation and actually like actually it's still
[21:35] and actually like actually it's still
[21:35] and actually like actually it's still like even that system that you trained
[21:36] like even that system that you trained
[21:36] like even that system that you trained that didn't use that feature still
[21:38] that didn't use that feature still
[21:38] that didn't use that feature still correlated on if you had isolated that
[21:39] correlated on if you had isolated that
[21:40] correlated on if you had isolated that feature or not. So I think I think it's
[21:42] feature or not. So I think I think it's
[21:42] feature or not. So I think I think it's basically what I'm what I'm trying to
[21:43] basically what I'm what I'm trying to
[21:43] basically what I'm what I'm trying to say is that um by looking at governance
[21:46] say is that um by looking at governance
[21:46] say is that um by looking at governance and looking at what is actually driving
[21:48] and looking at what is actually driving
[21:48] and looking at what is actually driving a decision for an ML model,
[21:51] a decision for an ML model,
[21:51] a decision for an ML model, &gt;&gt; you can really improve that whole not
[21:53] &gt;&gt; you can really improve that whole not
[21:53] &gt;&gt; you can really improve that whole not just the you you will obviously not not
[21:56] just the you you will obviously not not
[21:56] just the you you will obviously not not just automate the system itself, but
[21:57] just automate the system itself, but
[21:57] just automate the system itself, but you'll start to actually rearchitect the
[21:59] you'll start to actually rearchitect the
[21:59] you'll start to actually rearchitect the way that you're doing loans or the way
[22:01] way that you're doing loans or the way
[22:01] way that you're doing loans or the way that you're doing fraud detection, for
[22:02] that you're doing fraud detection, for
[22:02] that you're doing fraud detection, for example. Um yeah, we we we've I can give
[22:07] example. Um yeah, we we we've I can give
[22:07] example. Um yeah, we we we've I can give you an example. You know, we've
[22:09] you an example. You know, we've
[22:09] you an example. You know, we've chargeback fraud detection. You might
[22:11] chargeback fraud detection. You might
[22:11] chargeback fraud detection. You might have, for example, if you were to dump
[22:13] have, for example, if you were to dump
[22:13] have, for example, if you were to dump all of the features that you had
[22:14] all of the features that you had
[22:14] all of the features that you had available to do this chargeback fraud
[22:16] available to do this chargeback fraud
[22:16] available to do this chargeback fraud dete detection,
[22:18] dete detection,
[22:18] dete detection, &gt;&gt; you might find that actually some
[22:19] &gt;&gt; you might find that actually some
[22:19] &gt;&gt; you might find that actually some features are really really predictive of
[22:21] features are really really predictive of
[22:21] features are really really predictive of that, but they make no explainable sense
[22:23] that, but they make no explainable sense
[22:24] that, but they make no explainable sense whatsoever. They just work. And so
[22:26] whatsoever. They just work. And so
[22:26] whatsoever. They just work. And so there's this decision for companies to
[22:28] there's this decision for companies to
[22:28] there's this decision for companies to be like, well, do I just build the most
[22:30] be like, well, do I just build the most
[22:30] be like, well, do I just build the most high highly precise and high high recall
[22:32] high highly precise and high high recall
[22:32] high highly precise and high high recall system or do I actually put sacrifice
[22:35] system or do I actually put sacrifice
[22:35] system or do I actually put sacrifice some performance on this wider test set
[22:38] some performance on this wider test set
[22:38] some performance on this wider test set to at least make the system more
[22:40] to at least make the system more
[22:40] to at least make the system more explainable?
[22:41] explainable?
[22:41] explainable? &gt;&gt; Yeah. To inter to make it a more
[22:42] &gt;&gt; Yeah. To inter to make it a more
[22:42] &gt;&gt; Yeah. To inter to make it a more interpretable. Yeah,
[22:44] interpretable. Yeah,
[22:44] interpretable. Yeah, &gt;&gt; that is actually a very important
[22:45] &gt;&gt; that is actually a very important
[22:45] &gt;&gt; that is actually a very important question because interpretability also
[22:48] question because interpretability also
[22:48] question because interpretability also helps you to improve the system.
[22:49] helps you to improve the system.
[22:49] helps you to improve the system. &gt;&gt; Yeah. Yeah. Exactly.
[22:51] &gt;&gt; Yeah. Yeah. Exactly.
[22:51] &gt;&gt; Yeah. Yeah. Exactly. &gt;&gt; Talking about the investments. Uh so you
[22:53] &gt;&gt; Talking about the investments. Uh so you
[22:53] &gt;&gt; Talking about the investments. Uh so you were saying that uh if you're like a big
[22:55] were saying that uh if you're like a big
[22:55] were saying that uh if you're like a big company, middle company and you have a
[22:57] company, middle company and you have a
[22:57] company, middle company and you have a flat budget right now for EI what where
[22:59] flat budget right now for EI what where
[23:00] flat budget right now for EI what where would you invest money? So Uber for
[23:01] would you invest money? So Uber for
[23:01] would you invest money? So Uber for example they've invested in Michelangelo
[23:03] example they've invested in Michelangelo
[23:03] example they've invested in Michelangelo like 10 years ago at least and nowadays
[23:05] like 10 years ago at least and nowadays
[23:05] like 10 years ago at least and nowadays they are able to deliver more and more
[23:08] they are able to deliver more and more
[23:08] they are able to deliver more and more machine learning models uh on any level
[23:10] machine learning models uh on any level
[23:10] machine learning models uh on any level basically both the developers and
[23:12] basically both the developers and
[23:12] basically both the developers and product managers whoever.
[23:14] product managers whoever.
[23:14] product managers whoever. &gt;&gt; Yeah. So what would be your advice to
[23:16] &gt;&gt; Yeah. So what would be your advice to
[23:16] &gt;&gt; Yeah. So what would be your advice to the CTO? My advice to CTO would be like
[23:19] the CTO? My advice to CTO would be like
[23:19] the CTO? My advice to CTO would be like you cannot predict all the use cases for
[23:20] you cannot predict all the use cases for
[23:20] you cannot predict all the use cases for machine learning in an organization. You
[23:22] machine learning in an organization. You
[23:22] machine learning in an organization. You got thousands of people who are who have
[23:24] got thousands of people who are who have
[23:24] got thousands of people who are who have tasks to automate or or jobs to be done
[23:27] tasks to automate or or jobs to be done
[23:27] tasks to automate or or jobs to be done that they take on in on their
[23:28] that they take on in on their
[23:28] that they take on in on their day-to-day. So instead of trying to map
[23:30] day-to-day. So instead of trying to map
[23:30] day-to-day. So instead of trying to map out all those AI use cases, which is
[23:33] out all those AI use cases, which is
[23:33] out all those AI use cases, which is what I see a lot of people do, it's like
[23:34] what I see a lot of people do, it's like
[23:34] what I see a lot of people do, it's like where where can we get value from AI?
[23:36] where where can we get value from AI?
[23:36] where where can we get value from AI? Let's like write it in a document
[23:38] Let's like write it in a document
[23:38] Let's like write it in a document &gt;&gt; and that will change in the next
[23:39] &gt;&gt; and that will change in the next
[23:39] &gt;&gt; and that will change in the next quarter.
[23:39] quarter.
[23:39] quarter. &gt;&gt; That will change in the next quarter.
[23:41] &gt;&gt; That will change in the next quarter.
[23:41] &gt;&gt; That will change in the next quarter. Build a sandbox environment. Invest for
[23:45] Build a sandbox environment. Invest for
[23:45] Build a sandbox environment. Invest for two quarters in a sandbox environment
[23:47] two quarters in a sandbox environment
[23:47] two quarters in a sandbox environment that enables anyone to build a machine
[23:49] that enables anyone to build a machine
[23:50] that enables anyone to build a machine learning model.
[23:51] learning model.
[23:51] learning model. &gt;&gt; Open up your data so that you have
[23:53] &gt;&gt; Open up your data so that you have
[23:53] &gt;&gt; Open up your data so that you have features that people can access. uh
[23:55] features that people can access. uh
[23:55] features that people can access. uh whether it's of data streams that are
[23:57] whether it's of data streams that are
[23:57] whether it's of data streams that are coming through of what the business is
[23:59] coming through of what the business is
[23:59] coming through of what the business is doing whether it's sales calls whether
[24:01] doing whether it's sales calls whether
[24:01] doing whether it's sales calls whether it's in the case of payments payments
[24:03] it's in the case of payments payments
[24:03] it's in the case of payments payments going through transactions
[24:06] going through transactions
[24:06] going through transactions you know information that's anonymized
[24:08] you know information that's anonymized
[24:08] you know information that's anonymized about shoppers who are doing those
[24:09] about shoppers who are doing those
[24:09] about shoppers who are doing those transa open that up to people
[24:11] transa open that up to people
[24:11] transa open that up to people &gt;&gt; mh make it easy for them to train models
[24:14] &gt;&gt; mh make it easy for them to train models
[24:14] &gt;&gt; mh make it easy for them to train models using sort of template simple xg boost
[24:16] using sort of template simple xg boost
[24:16] using sort of template simple xg boost logistic regression so simple models
[24:20] logistic regression so simple models
[24:20] logistic regression so simple models and just see what use cases come out
[24:23] and just see what use cases come out
[24:23] and just see what use cases come out obviously open up LLMs as well right
[24:25] obviously open up LLMs as well right
[24:25] obviously open up LLMs as well right open access
[24:33] and see what cases people want to do and
[24:33] and see what cases people want to do and create an open channel where those use
[24:35] create an open channel where those use
[24:36] create an open channel where those use cases and the issues that come up are
[24:38] cases and the issues that come up are
[24:38] cases and the issues that come up are fed through to you so you can patch them
[24:40] fed through to you so you can patch them
[24:40] fed through to you so you can patch them and fix them and you will learn so much
[24:42] and fix them and you will learn so much
[24:42] and fix them and you will learn so much about what people want to use AI for in
[24:45] about what people want to use AI for in
[24:45] about what people want to use AI for in your organization. That was a great nice
[24:47] your organization. That was a great nice
[24:47] your organization. That was a great nice discussion. Uh yeah, happy to talk to
[24:50] discussion. Uh yeah, happy to talk to
[24:50] discussion. Uh yeah, happy to talk to you. Uh thank you. So maybe you have I
[24:53] you. Uh thank you. So maybe you have I
[24:53] you. Uh thank you. So maybe you have I don't know any other advices to the
[24:55] don't know any other advices to the
[24:55] don't know any other advices to the folks who are listening to that. Yeah, I
[24:58] folks who are listening to that. Yeah, I
[24:58] folks who are listening to that. Yeah, I would say just yeah it's it's the age of
[25:00] would say just yeah it's it's the age of
[25:00] would say just yeah it's it's the age of building. It's the age of creation. Um I
[25:03] building. It's the age of creation. Um I
[25:03] building. It's the age of creation. Um I think that's a really big opportunity
[25:04] think that's a really big opportunity
[25:04] think that's a really big opportunity for not just people in the workplace but
[25:07] for not just people in the workplace but
[25:07] for not just people in the workplace but also people humanity in general.
[25:09] also people humanity in general.
[25:09] also people humanity in general. &gt;&gt; Uh and it's this like great opportunity
[25:11] &gt;&gt; Uh and it's this like great opportunity
[25:11] &gt;&gt; Uh and it's this like great opportunity to to recreate that that magic of of of
[25:13] to to recreate that that magic of of of
[25:14] to to recreate that that magic of of of creativity. So I think
[25:15] creativity. So I think
[25:15] creativity. So I think &gt;&gt; even if you are in a job or you are an
[25:17] &gt;&gt; even if you are in a job or you are an
[25:17] &gt;&gt; even if you are in a job or you are an entrepreneur, it doesn't really matter.
[25:19] entrepreneur, it doesn't really matter.
[25:19] entrepreneur, it doesn't really matter. try to bring that and weave that into
[25:21] try to bring that and weave that into
[25:21] try to bring that and weave that into your day in the way that you you you you
[25:23] your day in the way that you you you you
[25:23] your day in the way that you you you you work. So, it's basically be creative,
[25:25] work. So, it's basically be creative,
[25:25] work. So, it's basically be creative, have an agency, and be hands-on. Yeah.
[25:27] have an agency, and be hands-on. Yeah.
[25:27] have an agency, and be hands-on. Yeah. Yeah. Okay, great. Thank you. Thanks for
[25:29] Yeah. Okay, great. Thank you. Thanks for
[25:29] Yeah. Okay, great. Thank you. Thanks for joining. And if you want to know more
[25:30] joining. And if you want to know more
[25:30] joining. And if you want to know more about how AI may fit into your
[25:32] about how AI may fit into your
[25:32] about how AI may fit into your organization, check the link below.
