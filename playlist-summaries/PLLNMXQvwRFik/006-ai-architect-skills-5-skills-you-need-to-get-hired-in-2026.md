# AI Architect Skills: 5 Skills You Need to Get Hired in 2026

- **Video:** https://www.youtube.com/watch?v=Pq7_EDpQdbA
- **Generated:** 2026-08-31 20:54 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

Only Section 2 contains substantive content; Section 1 is a request for the remaining transcript and adds no technical material to consolidate.

The speaker’s central claim is that successful AI architecture is primarily a **business and operational leadership discipline**, not merely a matter of selecting tools such as RAG, vector databases, APIs, or LLMs. AI investments should be tied to measurable operational outcomes, explicit trade-offs, full lifecycle cost, governance, and resilience.

For Superior Propane, AI/GenAI initiatives should be treated as operational-improvement products—for example, customer-service agent assistance, document processing, or IT operations support—not as standalone “chatbot” deployments.

Each use case should have:

- A defined workflow, accountable business owner, baseline KPI, and target outcome.
- A full cost model that includes model consumption, data processing, integration, security, support, and change management.
- Clear data ownership, governance, access control, evaluation, and monitoring.
- Human fallback, incident handling, cost controls, and business-continuity procedures.
- Decision artifacts that align operations, IT, security, finance, data governance, and compliance.

The source material does **not** provide a prescriptive Azure, Databricks, or Azure AI Foundry architecture. Its value is in defining how Superior Propane should assess, govern, justify, operate, and communicate AI products built on those platforms.

# Technical details

## 1. Start with business outcomes, not AI components

**Speaker claim:** Architects should not lead with “we need a RAG architecture with a vector database and secure API integration.” They should describe the operational problem: agents searching multiple systems, inconsistent answers, longer handling times, escalations, and customer frustration.

This is a sound product and architecture principle. RAG, vector search, APIs, and models are implementation choices—not the business case.

A properly framed AI product requirement should establish:

- **User:** e.g., contact-centre agent, operations employee, field-service representative, or IT support analyst.
- **Job to be done:** retrieve approved policy, product, safety, customer-service, or operational guidance while completing work.
- **Business objective:** improve first-contact resolution, reduce average handling time, reduce rework, improve consistency, or reduce document-processing effort.
- **Risk level:** whether the system merely recommends information, drafts content, retrieves documents, or can take operational actions.
- **Technical enablers:** governed ingestion, retrieval, model orchestration, identity-aware access, integration, evaluation, monitoring, and fallback procedures.

### Product-owner implication

Use business language first, then specify technical requirements. For example:

> Enable service agents to retrieve current, authorized operational and policy guidance during customer interactions, reducing search time and escalation rates while maintaining safety, privacy, and service-quality controls.

That statement can later be implemented with Azure AI Foundry/Azure OpenAI, Databricks, Azure AI Search, or other approved components—but those technologies should not substitute for the product definition.

---

## 2. AI cost must be modeled as total cost of ownership

**Speaker claim:** AI can be expensive because costs extend beyond model usage to compute, storage, secure data pipelines, integration, and specialized talent.

This is an established production-AI reality. The transcript does not provide workload volumes, Azure pricing, Databricks consumption estimates, or validated savings figures.

### Cost categories

| Cost area | Include in the business case | Relevant Azure/Databricks considerations |
|---|---|---|
| Model consumption | Input/output tokens, embeddings, retries, tool calls, evaluations, load testing | Azure AI Foundry / Azure OpenAI model consumption, throughput and capacity choices |
| Compute | Data transformations, ingestion, batch jobs, orchestration, any hosted inference | Databricks jobs/clusters/serverless; Azure compute services |
| Storage and search | Raw and curated documents, embeddings, vector indexes, logs, evaluation results | ADLS, Databricks-managed storage, Azure AI Search or equivalent vector store |
| Data pipelines | Extraction, OCR, parsing, chunking, metadata enrichment, refreshes, error handling | Databricks Workflows/pipelines, Azure Data Factory, document processing services |
| Integration | CRM, customer-service tools, ERP, field-service systems, document repositories, APIs | API Management, Entra integration, private connectivity, custom development |
| Security and governance | Identity, logging, audit, network controls, secret management, content safety, compliance reviews | Microsoft Entra ID, Key Vault, Purview, Azure Policy, Foundry governance features |
| Operating support | Monitoring, incident response, prompt and knowledge updates, platform support, user training | Product, platform engineering, data engineering, security, operations, knowledge owners |

### Business-case structure

The speaker uses an example of a 40% reduction in manual/document-processing effort and $2M annual savings. This is an **illustrative hypothesis only**, not evidence applicable to Superior Propane.

A Superior Propane business case should include:

1. **Baseline**
   - Monthly case/document/contact volumes.
   - Labor time and cost per unit.
   - Current average handling time, escalations, rework, errors, and abandonment.
   - Customer or operational impact of delays and incorrect outcomes.

2. **Benefit scenarios**
   - Conservative, expected, and upside cases.
   - Segmentation by task complexity and customer channel.
   - Quality-adjusted savings: speed improvements do not count as benefits if errors, compliance risk, or review effort rise.

3. **Full costs**
   - One-time implementation and integration.
   - Recurring Azure/Databricks/model/search consumption.
   - Data cleanup and knowledge stewardship.
   - Security, compliance, support, training, and change management.

4. **Decision measures**
   - Payback period.
   - ROI or NPV where appropriate.
   - Cost per successful assisted interaction/document.
   - Quality, acceptance, escalation, and correction rates.

---

## 3. Platform and vendor management should optimize organizational fit

**Speaker claim:** AI solutions often involve cloud, model, data, network, and security providers. Selection should be based on organizational fit, not feature comparison alone.

This is established architectural guidance. For Superior Propane, selection and standardization should be evaluated against the existing Azure and Databricks estate.

### Evaluation criteria

- **Data integration fit**
  - Can the platform reliably use approved enterprise data from customer, operational, document, and knowledge systems?
  - Does it minimize unnecessary data duplication between Azure, Databricks, and downstream AI/search components?

- **Identity and security**
  - Microsoft Entra ID integration.
  - Least-privilege access to both source data and AI tools.
  - Private endpoints/network isolation where required.
  - Secret and key management.
  - Auditable data access and model interactions.

- **Governance, compliance, and residency**
  - Data retention and deletion controls.
  - Prompt/output logging controls.
  - Ability to demonstrate source-data access and usage.
  - Support for applicable customer-data, operational-data, contractual, and regulatory obligations.

- **Model capability and operational characteristics**
  - Quality for propane-sector terminology, internal policies, service workflows, and Canadian operating context.
  - Latency, availability, regional availability, rate limits, and capacity.
  - Controlled model/version upgrades with repeatable evaluations.

- **Cost predictability**
  - Token pricing and provisioned-capacity options where applicable.
  - Vector search, data pipeline, storage, egress, and support costs.
  - Budget allocation, tagging, quotas, and spend alerts.

- **Portability and concentration risk**
  - Separate application orchestration, retrieval/data layer, and model endpoint where practical.
  - Maintain a realistic—not merely contractual—ability to change models or providers.
  - Avoid introducing multi-provider complexity unless it materially improves resilience, cost, or capability.

---

## 4. Architecture is trade-off management

**Speaker claim:** Business teams seek speed, security seeks control, finance seeks lower cost, engineering seeks flexibility, and compliance requires governance. The architect’s job is to reconcile these objectives.

For a Technical Product Owner, material trade-offs should be explicit and recorded.

| Decision area | Speed-oriented option | Control-oriented option | Product decision |
|---|---|---|---|
| Knowledge onboarding | Rapidly ingest broad repositories | Start with a small, curated, approved corpus | Define source onboarding tiers and approval workflow |
| Customer responses | Auto-send generated answers | Agent review before responses are sent | Set human-in-the-loop requirements by risk class |
| Model selection | Use highest-capability model | Use lower-cost, lower-latency, or regionally constrained model | Define quality, latency, and unit-cost thresholds |
| Operational-system access | Broad AI access to tools and data | Read-only tools and restricted scopes first | Define tool permissions and approval controls |
| Observability | Retain detailed prompts and outputs | Minimize retention of sensitive content | Define redaction, retention, audit, and access policies |

Use Architecture Decision Records (ADRs) for significant choices. Each ADR should capture:

- Context and decision required.
- Options considered.
- Selected option and rationale.
- Security, operational, cost, and business implications.
- Accountable owner.
- Accepted risks.
- Review date or conditions that trigger reconsideration.

---

## 5. Production AI needs resilience and fallback planning

**Speaker claim:** AI systems can become operationally critical; architecture must account for model outages, data-pipeline failures, incorrect responses, and cost spikes.

These are credible, well-established production risks. The transcript does not prescribe exact resilience patterns; the following are practical implementation implications.

### Required failure scenarios

- **Model endpoint outage, throttling, or degradation**
  - Detect error-rate increases, latency changes, capacity issues, or quality degradation.
  - Fall back to traditional search, documented procedures, or human escalation.
  - Consider secondary models/providers only if the operational benefit outweighs added complexity.
  - Do not use a fallback model in production without safety and quality evaluation.

- **Knowledge ingestion or indexing failure**
  - Monitor pipeline completion, parsing failures, index failures, schema changes, and source-permission changes.
  - Track and expose knowledge freshness where it is relevant to decisions.
  - Retain a last-known-good index and support rollback.
  - Assign content correction ownership to source-system or knowledge owners.

- **Incorrect, unsafe, or ungrounded output**
  - Use grounded retrieval and source citations where appropriate.
  - Apply response policies, content-safety controls, and restricted tool permissions.
  - Require human review for safety-sensitive, customer-specific, financial, or operationally consequential tasks.
  - Capture feedback, incidents, and evaluation failures for remediation.

- **Runaway consumption costs**
  - Apply budgets, quotas, alerts, rate limits, and cost tags.
  - Monitor tokens per transaction, retries, large-context requests, embedding rebuilds, and vector-index growth.
  - Define degraded modes: reduced context, limited users, lower-cost model routing, or temporary feature disablement.

- **Integration outage or transactional failure**
  - Clearly distinguish read-only assistance from action-taking systems.
  - For actions, use confirmation, idempotency, transaction logs, exception queues, and manual recovery.

---

## 6. Architecture artifacts are operational alignment tools

**Speaker claim:** Target-state architecture, current-state assessments, roadmaps, and capability maps are decision and communication tools, not paperwork.

A practical artifact set for a Superior Propane AI initiative includes:

- **Current-state assessment**
  - Workflow map and systems currently searched.
  - Source repositories, data classification, and owners.
  - Volumes, effort, quality issues, current costs, and control gaps.

- **Target-state architecture**
  - Data sources → ingestion/curation → governed data platform → retrieval/vector index → model/orchestration → user experience.
  - Identity, secrets, network boundaries, logging, evaluation, safety, monitoring, human review, and support model.
  - Identify specific Azure, Databricks, AI Foundry, and third-party products only after requirements and platform decisions are made.

- **Capability map**
  - Knowledge management.
  - Document intelligence.
  - Model access.
  - Retrieval and search.
  - Orchestration/tool use.
  - Evaluation and observability.
  - Security/governance.
  - FinOps.
  - Incident management.

- **Roadmap**
  - Discovery and data readiness.
  - Controlled pilot with a bounded corpus and user group.
  - Evaluation, security review, and operational hardening.
  - Production rollout.
  - Expansion into additional domains and higher-risk capabilities.

- **Business case and operating model**
  - KPI baselines, benefits, costs, dependencies, risks, owners, and review cadence.
  - RACI for product, platform, data, knowledge, security, compliance, operations, and service desk.

# Potential applications for Superior Propane

## 1. Customer-service agent knowledge assistant

This is the closest fit to the speaker’s examples.

### Potential outcomes

- Reduce time agents spend searching across policy, product, service, safety, delivery, and operational sources.
- Improve consistency of responses.
- Improve first-contact resolution.
- Lower average handling time and escalations.
- Improve onboarding and support for newer agents.

### Indicative architecture

- Approved knowledge sources and operational documents.
- Ingestion, parsing, chunking, metadata enrichment, and scheduled freshness checks.
- Databricks and/or Azure data services for transformation and orchestration, depending on the selected enterprise pattern.
- Search/vector retrieval layer.
- Azure AI Foundry/Azure OpenAI model endpoint for answer synthesis, if approved and suitable.
- Agent-facing experience integrated with existing service tooling.
- Entra-based identity and source authorization, logging, evaluations, monitoring, and human-review controls.

### Key constraint

The assistant should provide answers only from current, authorized information and should make uncertainty visible. Safety-sensitive, account-specific, pricing-sensitive, or customer-impacting decisions require stronger controls and likely agent verification.

---

## 2. Document-processing automation

The transcript identifies manual document processing as a candidate for quantified operational savings.

Potential areas may include internal operational records, customer-submitted documents, forms, invoices, service records, or compliance documentation. Specific candidates require validation against actual workflows, document volumes, integration feasibility, and error tolerance.

### Potential workflow

1. Receive a document.
2. Extract information using OCR/document AI capabilities.
3. Validate extracted values against business rules and source systems.
4. Route low-confidence or invalid cases to a human exception queue.
5. Store confidence scores, evidence, audit events, and final disposition.
6. Measure straight-through processing, exception rate, cycle time, and quality.

The value proposition depends on more than extraction accuracy. It depends on document variation, downstream integration, exception handling, traceability, and the operational cost of erroneous processing.

---

## 3. IT, data, and platform operations copilot

The speaker references improving incident-handling time and access to technical knowledge.

A controlled internal copilot could support Azure and Databricks operations by retrieving:

- Runbooks and support procedures.
- Known errors and prior incident summaries.
- Architecture documentation.
- Data pipeline ownership and dependency information.
- Troubleshooting steps and escalation paths.

Start with read-only retrieval and recommendations. Do not allow autonomous production actions initially. Any later action capability should require authorization, confirmation, logging, rollback, and clearly assigned support ownership.

---

## 4. Reusable AI platform governance

This section is directly relevant to an AI platform product strategy across Azure, Databricks, and Azure AI Foundry.

Potential platform capabilities include:

- Standard approved model access and model onboarding.
- Governed RAG patterns and data-source onboarding.
- Shared evaluation, safety, monitoring, and audit patterns.
- Standard identity, secrets, network, and logging controls.
- FinOps tagging, quotas, alerting, and cost reporting.
- Reusable templates for production readiness and use-case intake.
- Decision criteria for choosing GenAI versus deterministic automation, search, analytics, rules engines, or workflow tooling.

# Risks and validation questions

## Business value

### Risks

- The speaker’s 40% effort reduction and $2M annual savings example is not validated for Superior Propane.
- Adoption metrics or prompt volumes can be mistaken for business value.
- Employee review/correction effort may eliminate productivity gains.
- Pilot estimates may omit data remediation, integration, security, platform, and support costs.

### Validation questions

- What is the baseline volume, effort, cost, error rate, and elapsed time for the target workflow?
- What proportion of work can be safely assisted versus automated?
- What quality threshold must be maintained or improved?
- Who owns benefits realization after launch?
- What is the maximum acceptable cost per assisted contact, transaction, or document?
- What is the expected payback under conservative and expected scenarios?

## Data, security, and governance

### Risks

- Unapproved, inaccurate, or stale sources can produce incorrect guidance.
- Over-broad retrieval could expose customer, pricing, safety, operational, or employee information.
- Prompt/output logging can create a separate sensitive-data retention problem.
- RAG reduces but does not eliminate hallucinations or misleading answers.
- Users may over-trust authoritative-sounding model output.

### Validation questions

- Who owns and approves each source for AI use?
- What data classifications, residency requirements, retention rules, and contractual commitments apply?
- Can retrieval enforce source-level and user-level authorization?
- What information is sent to the model endpoint and retained in logs or evaluation datasets?
- Which cases require citations, mandatory agent review, or prohibited-response policies?
- How are bad source documents corrected, re-indexed, and verified?
- How will model prompt injection and malicious/untrusted content in source repositories be addressed?

## Reliability and operations

### Risks

- Model outages, rate limits, capacity constraints, and provider/model changes may affect operations.
- Pipeline or indexing failures can silently make a knowledge base stale.
- Retries, long prompts, embedding jobs, and high-volume usage can create unplanned cost.
- Multi-vendor support can obscure incident ownership.

### Validation questions

- What are the service-level objectives for availability, latency, knowledge freshness, and answer quality?
- What is the manual fallback when retrieval or model services fail?
- Are model/version changes evaluated against a repeatable test set before release?
- Who owns incidents across application, pipeline, retrieval, model endpoint, and source systems?
- Which budget alerts, quotas, circuit breakers, and feature kill switches are required?
- What is the recovery plan for a corrupted index, source-data change, or erroneous automated action?

# Action items

1. **Implement a standardized AI use-case intake**
   - Require target user, business problem, workflow, baseline metrics, expected outcome, source data, risk classification, dependencies, and accountable business owner.
   - Do not accept “build a chatbot” or “use RAG” as a sufficient problem statement.

2. **Create a reusable AI business-case template**
   - Capture implementation cost, recurring platform cost, operational support, benefit scenarios, payback, quality thresholds, and sensitivity analysis.
   - Include Azure, Databricks, model, vector-search, storage, and integration assumptions where applicable.
   - Validate assumptions with measured workload volumes rather than generic AI ROI claims.

3. **Define a production AI operating model**
   - Establish responsibilities for product ownership, platform engineering, data ownership, knowledge stewardship, security, privacy, compliance, FinOps, monitoring, incident response, and end-user support.
   - Define correction and escalation processes for unsafe, incorrect, or stale AI output.

4. **Prioritize a controlled agent-assist pilot**
   - Select a high-value but bounded, lower-risk knowledge domain.
   - Start read-only, with a curated corpus and agent review.
   - Measure first-contact resolution, average handling time, response acceptance/correction rate, escalation rate, knowledge freshness, latency, and cost per interaction.

5. **Establish production-readiness gates**
   - Approved and owned data sources.
   - Security, privacy, and compliance review.
   - Evaluation results against predefined quality and safety thresholds.
   - Identity, network, audit, logging, and retention controls.
   - Monitoring, alerting, spend controls, rollback, and fallback procedures.
   - User training and change-management plan.

6. **Create decision-focused architecture artifacts**
   - Current-state workflow and system map.
   - Target-state Azure/Databricks/AI architecture.
   - Capability map and phased roadmap.
   - Risk register and ADRs for material trade-offs.
   - Executive narrative focused on operational value, cost, risk, dependencies, and timing—not component names alone.

## Full transcript

[00:00] If you want to become an AI architect.
[00:02] Stop training like an engineer.
[00:04] That may sound strange,
[00:05] but it's the biggest reason smart people fail to get architect roles.
[00:10] People learn Python, they learn prompt engineering and AI tools,
[00:13] and then they walk into an architect interview and get told.
[00:17] Come back when you have experience.
[00:19] But experience is never the issue.
[00:21] It's that AI architecture is not AI engineering.
[00:25] It's a different career
[00:26] with a different focus and a completely different set of skills.
[00:29] Now, if you possess all five types of AI architect skills,
[00:33] you'll have an incredible AI architect career
[00:36] with an average salary of over $240,000 a year.
[00:40] Hi, I'm Mike Gibbs.
[00:42] I'm a chief architect
[00:43] with a little over 20 years experience, and I want to be very clear.
[00:47] Architecture is not engineering with a better title.
[00:51] Engineers build and operate AI systems, but the focus of the architect
[00:55] is different.
[00:56] First, we don't build systems in the first place.
[00:59] We are hired to answer questions like this.
[01:02] How would we use AI to reduce our cost?
[01:04] Or maybe how can we use
[01:06] AI to enhance our operations or improve the customer experience?
[01:10] And when it comes to AI, we're there to determine should we build it?
[01:14] Why should we build it and what problem the AI will actually solve.
[01:18] And that's why the AI architect career is so powerful, because we help
[01:22] companies make the right AI decisions and create the best AI strategy,
[01:26] which takes a very different set of skills than I engineering.
[01:31] So the big question is this what skills do
[01:34] you actually need to become a great AI architect?
[01:37] Not an artificial intelligence engineer, but an artificial intelligence architect?
[01:43] And the key is a
[01:44] real AI architect can sit with executives, lead the corporate strategy,
[01:49] make design decisions and get hired for architectural level roles.
[01:54] But that requires five specific skill skill sets.
[01:57] Master all five,
[01:58] and you'll have an incredible high paying architecture career.
[02:01] Now, I'll begin with skill number one,
[02:03] which is going to sound a little bit obvious.
[02:05] And that is AI specific skills.
[02:08] And if you want to become an architect, you must understand AI.
[02:12] And in that area you means you need to understand AI ethics.
[02:16] Because I can create bias or privacy
[02:19] issues or legal issues or even reputational damage.
[02:22] And you need to understand the ethics behind that
[02:25] and what's appropriate and what's not.
[02:27] You need to understand model building.
[02:30] Now, it's not because you're going to be building AI models or coding,
[02:35] but it's because you must know how a model is created, how
[02:38] you would select a model, how you would evaluate a model and then govern it.
[02:42] You definitely need to understand
[02:44] AI model testing and AI model training,
[02:48] because you'll need to be able
[02:49] to understand how we're going to evaluate a model's performance,
[02:53] the accuracy of our systems, whether we're getting any drift
[02:57] or hallucinations with our AI systems.
[02:59] And will the systems fit into the business?
[03:01] You need to understand rag or retrieval augmented generation
[03:05] because in the enterprise, most AI systems
[03:08] cannot simply rely on a public model or public data.
[03:11] The AI systems need access to internal policies, internal documents,
[03:15] customer records, product data, and even service histories.
[03:19] And that means the AI architect must understand how retrieval works,
[03:23] how knowledge is chunked, how vector databases are used, and how the AI system
[03:28] will retrieve the right information in the right context at the right time.
[03:33] You'll also need to understand model Context protocol,
[03:36] because now AI systems are expected to connect to other tools.
[03:41] Other systems, other data sources, and other enterprise workflows.
[03:44] And when AI system start taking action and not just answering questions,
[03:49] the architecture will become even more important.
[03:52] Now why is that?
[03:53] Because once the AI system starts touching various business processes
[03:57] and it can start retrieving customer information, it may be opening
[04:01] tickets and updating records and triggering workflows.
[04:04] It's affecting operations.
[04:06] And if something were to occur at that point, it's not just an AI model problem.
[04:11] It is a problem for the business.
[04:14] You also need to have good strong
[04:16] knowledge of AI security and how to secure AI systems,
[04:20] because AI is going to create new attack surfaces.
[04:23] For example, prompt injection or data leakage or model abuse.
[04:28] And that's why the AI architect must know how to design secure AI systems.
[04:33] You also need big data skills
[04:35] because AI is only as good as the data that can access.
[04:38] Which means you will need to understand relational databases
[04:42] and NoSQL databases and data lakes and data warehouse as,
[04:47] vector databases, streaming databases,
[04:50] metadata and data lineage.
[04:53] And you definitely need to have a fair amount of knowledge on data hygiene.
[04:56] And that's going to be huge because, bad data creates bad AI, incomplete
[05:02] data creates weak AI, and inconsistent data
[05:05] creates unreliable AI.
[05:08] So lots of data specific skills and lots of AI specific skills.
[05:13] So I said specific skills are critical.
[05:16] But if you stop here,
[05:18] you won't become an architect
[05:20] and you've only learned the technology.
[05:22] And if you only know the technology without the rest of the architecture skills,
[05:27] you don't have any of the skills you need.
[05:29] So let's talk about the next set of skills the tech foundational skills.
[05:34] And this is where a lot of people get confused about the technology.
[05:38] They think, if I'm going to be an architect,
[05:41] why would I need to learn networking?
[05:43] Or why would I need to understand data centers and cloud computing?
[05:46] Why would I need to know security?
[05:48] Why would I need to understand application architecture?
[05:51] But these skills are critical.
[05:53] And here's the reason I does not live in isolation.
[05:57] I runs on infrastructure.
[05:59] It connects to applications.
[06:00] It consumes data.
[06:01] AI is dependent upon network compute and storage.
[06:05] So when I architect who does not understand the data center
[06:09] or cloud computing
[06:10] is incredibly limited in their ability to design and infrastructure,
[06:14] because I workloads run on these cloud and data center platforms.
[06:18] Now you also need to understand,
[06:22] compute,
[06:24] networking, identity
[06:26] APIs, cloud services, and cost models
[06:30] because that's what it's going to take to be able to design these systems.
[06:34] You'll need to know how to architect
[06:35] for scalability, availability and performance needs.
[06:39] And this knowledge helps you become more effective.
[06:42] And the critical architecture decisions that you will face as an AI architect.
[06:46] Like, should we run this architecture in the cloud or should it be on premises?
[06:52] Should we use a managed AI service,
[06:54] for example, or an open source model or even a private model?
[06:57] And these are key architectural questions.
[07:00] Now networking is going to matter because the AI systems
[07:03] are going to connect to users and applications and databases
[07:07] and APIs and SaaS platforms and other cloud services.
[07:11] And all of that happens over a network.
[07:13] So if you don't understand networking and you don't understand the connectivity,
[07:17] none of these systems will ever work.
[07:20] Now security matters.
[07:21] And I talked a little bit about it before,
[07:22] but now we're talking about much more security knowledge.
[07:25] Remember these AI systems are going to touch
[07:28] sensitive business data and sensitive parts of the organization.
[07:31] Customer data, financial data potentially health data or intellectual property.
[07:37] And that's why you need to understand strong security concepts
[07:40] like identity and access control and encryption
[07:44] and segmentation and micro segmentation and logging and monitoring and governance.
[07:50] Application architecture will also matter
[07:53] because I does not usually replace the whole business application.
[07:57] I get embedded into various
[07:59] business applications or it gets exposed through various APIs.
[08:02] I get connected to various workflows.
[08:05] I becomes part of the customer journey, part of the employee experience,
[08:09] and even the operational process in most businesses.
[08:11] So you need these strong technical foundations to bring credibility
[08:16] that will help you understand the technical design.
[08:19] It will make sure you don't design any unrealistic architecture,
[08:22] and it will help you know what's possible,
[08:24] what's risky, what's expensive, and what's likely going to fail.
[08:27] So technical skills are very necessary, but they're not sufficient.
[08:32] Technical knowledge will get you into the conversation,
[08:35] but they will not make you a trusted advisor.
[08:38] Now, here's the most important thing to understand.
[08:41] About 75% of the AI architect job is non-technical
[08:45] and comes from non-technical skills, which we're going to talk about next.
[08:49] They, in many cases,
[08:50] are the difference between getting hired and not getting hired.
[08:54] The third set of skills you need are executive skills.
[08:56] And this is where most aspiring AI architects are completely unprepared.
[09:01] And it often cost them the job.
[09:03] They think architecture means being the smartest person in the room.
[09:06] It does not.
[09:07] Architecture means being the person that executives trust,
[09:11] especially when that decision is expensive,
[09:14] risky, unclear, or complicated.
[09:16] And that's all I architecture see.
[09:20] All AI projects are full of uncertainty.
[09:23] Executives may not really understand what I can do or not do.
[09:27] Business leaders have very unrealistic expectations.
[09:30] Engineering teams I'm going to focus on a tool.
[09:33] Security teams may be overly focused on risk because that's their job.
[09:37] And and they block you from doing what you need to do.
[09:39] Legal teams may worry about compliance,
[09:43] and the job of the
[09:44] architect is to bring these groups together.
[09:47] And that takes executive skills because our job is an advisory role.
[09:50] We're providing direction and guidance.
[09:53] And that means you must be able to advise executives,
[09:56] not overwhelm them with jargon, not bury them in
[10:00] model names, not give the executives a technical lecture.
[10:04] Your job as an architect is to translate
[10:07] AI into business value.
[10:10] You must be able to say to the executive team, here's the business problem.
[10:14] Here is the AI opportunity, here are the risks.
[10:17] Here are the options.
[10:18] Here's the trade offs.
[10:19] And here's what we should do. Now.
[10:21] And it's equally important to be able to say
[10:23] we should not move forward at this time for this reason.
[10:27] That is your job as an architect, an advisor.
[10:31] Now in order to be successful in any kind of architectural role.
[10:36] You have to understand organizational change management.
[10:40] And here's the reason why I changed the way people work.
[10:44] AI changes various business processes.
[10:46] It change various job roles, even how decisions are made
[10:50] inside of an organization.
[10:51] And that creates fear.
[10:54] People will be very concerned that I may replace them.
[10:58] Managers may resist changing the way they do their jobs.
[11:01] Teams may not trust a model's output, and executives
[11:06] may want to change the organization faster than the organization can change.
[11:11] And that's why the AI architect must understand
[11:14] organizational change management.
[11:16] Because if we don't adapt the organization for the changes
[11:20] that are associated with
[11:22] our next architecture, what will happen is we'll have a beautifully designed
[11:25] AI solution that will fail.
[11:28] It will fail to be adopted and it will not work.
[11:31] You will also need executive presence.
[11:34] Executive presence doesn't mean wearing a fancy suit and using big words.
[11:39] Executive presence means you can communicate with clarity,
[11:43] confidence, relevance, and judgment and the manner that executives care about.
[11:48] And this is so critical because executives trust the people who understand
[11:53] what matters most to them and what matters to executives.
[11:56] It's not tech.
[11:57] It's, you know, how to increase revenue, how to reduce risks,
[12:01] how to lower our cost, how to make the business be able to do things faster,
[12:04] adhering to compliance regulations or even improving a customer experience.
[12:09] So if you walk into an executive meeting and spend 20 minutes
[12:13] talking about token windows or vector embeddings or model parameters,
[12:18] you may be correct about
[12:20] the technology, but you became irrelevant to the executives.
[12:23] And what happens is, when you're describing that,
[12:25] the executive will be thinking, how does this affect the business?
[12:29] And that's what you need to answer as an architect.
[12:32] You'll also need the executive skills to be able to influence others.
[12:37] And the reason is we architects do not always have
[12:40] direct authority over every team inside the organization.
[12:44] For example, as an architect,
[12:45] you're not going to be
[12:46] managing the developers or the data team or the security team, but
[12:50] you're still going to need everyone on board with the architecture,
[12:53] and that means you're going to have to influence without its authority,
[12:57] which means you must be able to sell the architecture.
[12:59] Explain why the design matters, and even handle objections when they occur.
[13:04] And your influence will build trust and get people to support your architecture.
[13:09] You must also be able to manage stakeholders.
[13:13] Because I architectures, like any architecture,
[13:16] touches many stakeholders through out the organization.
[13:19] Your architecture will affect the executives.
[13:23] It will affect product owners.
[13:24] It will affect business unit leaders
[13:26] and data owners, security leaders, even legal and compliance.
[13:30] And the key is every stakeholder in a business will have a different concern.
[13:34] The chief financial officer
[13:36] is going to want to lower the cost and increase the ROI.
[13:39] The chief information security officer is going to be very concerned
[13:42] about the risk.
[13:43] The business leaders are looking for speed and outcomes, and the legal team
[13:47] is trying to slow everything down to reduce risk and compliance.
[13:51] And as an AI architect, we bring all these things together.
[13:54] And that's why we architects are paid for decisions, not deployments.
[13:59] Now here is where it gets even more important.
[14:03] If you want to become an AI architect, you can't just sound technical,
[14:07] you must sound like someone who understands how businesses invest,
[14:11] how businesses operate, how businesses compete, and how businesses manage risk.
[14:16] And that brings us to skill set number four.
[14:19] Skill set number four for AI architects is business skills.
[14:23] And this in most cases the biggest differentiator.
[14:26] And separator between an AI engineer and an AI architect.
[14:31] C an AI engineer will ask this question how do we build this?
[14:36] What tools am I using?
[14:38] Now the AI architect is there to ask completely different questions.
[14:41] Should we build this in the first place?
[14:43] Why does this architecture matter?
[14:45] What business capability does this architecture enable?
[14:50] What value is the architecture going to create, for example,
[14:52] and what are the trade offs that we're making along the way?
[14:56] Now part of knowing business is understanding business strategy
[15:00] because I shouldn't
[15:02] be implemented just because it's cool, trendy or popular.
[15:06] I must support the business strategy and whether the business strategy
[15:10] is to reduce customer support costs, or maybe detect fraud,
[15:14] or accelerate software development, or improve sales forecasting.
[15:18] The AI architect must be able to connect that business
[15:21] strategy to an actual architecture.
[15:24] Now you really need to have a good
[15:26] knowledge of business architectures and business capabilities.
[15:30] A business architecture is how the business is structured, for example,
[15:34] and the key processes, procedures, what have you.
[15:37] Now, business capabilities are things
[15:39] that a business needs to be able to do to survive.
[15:44] And that could be, you know, onboarding new customers or processing
[15:47] claims or fraud detection or managing inventory or customer service.
[15:52] And AI architecture, like any other architecture,
[15:55] should be mapped to business capabilities.
[15:58] Because when you map AI to key business capabilities,
[16:02] you're no longer talking about random tools.
[16:05] You're now talking about how to increase business value,
[16:07] and that will dramatically increase your relevance and pay.
[16:11] Now, in an interview, for example, don't say
[16:14] I was building a chat pod because I chose you as a techie
[16:17] one don't look like an AI architect on the interview.
[16:20] Say something different.
[16:22] Say we are improving the customer support capability
[16:24] by using AI to reduce our incident handling time.
[16:29] Improve first contact resolution, and give agents access
[16:33] to architecture, thinking, architecture,
[16:34] knowledge and better tools to do their job.
[16:37] That's architecture.
[16:38] Thinking.
[16:39] Now you also need to be able to understand finance.
[16:43] Let's face it, I can be extremely expensive.
[16:47] Model usage costs money.
[16:49] Compute costs can get extremely high.
[16:51] Storage costs get fairly high fairly quickly.
[16:54] Data pipeline security, integration and talent.
[16:57] It's going to come at a cost.
[16:59] So our job as architects is to determine
[17:02] if it's worth it for the business to invest in AI.
[17:06] So that means we architects have to use our business skills
[17:09] to create a business case for the AI architecture investment
[17:12] that will include the architectures, costs you know, the amount of time
[17:16] it will take for the business to get paid back, the payback period,
[17:19] the expected return on investment, what have you.
[17:22] And a strong AI business case might say something like this
[17:25] AI solution will replace manual and document processing time by 40%.
[17:31] That will reduce our
[17:32] operational costs by $2 million a year.
[17:36] That's what we're realistically
[17:37] talking about as architects.
[17:41] We're talking about a way to show the executives
[17:43] when the solution will pay for itself, because that's the language of executives.
[17:48] Now there's an AI architect.
[17:50] You're going to need strong
[17:51] vendor management skills because most AI solutions involve multiple vendors.
[17:56] There's a cloud provider, there's a model provider.
[17:58] There's a data platform.
[18:00] There's networking security providers.
[18:02] And as an AI architect, you're going to have to help evaluate
[18:05] vendors and a completely non-biased manner not based on features,
[18:10] but based on fit, based on,
[18:12] you know, how those trade offs map to an organization, security
[18:16] or cost or integration ability or scalability or compliance.
[18:21] Now, as an AI architect, you know, under
[18:23] these business skills you'll need to negotiate some skills
[18:26] because architecture is full of trade offs.
[18:29] The business, once paid security, wants control.
[18:32] Finance wants to lower cost.
[18:33] Engineering wants flexibility.
[18:35] Compliance needs more governance.
[18:37] You get the point.
[18:38] And the AI architect must negotiate a design
[18:41] or a strategy that balances the needs of all that are concerned.
[18:46] And we're constantly working with that
[18:49] knowledge.
[18:49] AI architects, we do a lot of business continuity planning.
[18:52] So that's one of those business skills you need to understand.
[18:54] And here's the reason AI system become part of critical business operations.
[19:00] And once that occurs, what happens
[19:02] if a model provider has an outage or a data pipeline fails?
[19:06] What happens if the AI produces a bad output or the costs were to spike?
[19:10] See, these are concerns that we actually have.
[19:12] So architecture requires planning for failure
[19:15] not because we're negative people, but because we are responsible.
[19:18] And that's what the executives expect from the architect.
[19:22] Now you can have the AI skills.
[19:24] You can have the cloud skills.
[19:26] You can have the security skills, the executive skills and the business skills.
[19:30] But if you can't communicate clearly, you're still not going to be hired
[19:33] as an architect because architecture, they can't be communicated,
[19:39] won't be funded, approved, governed, or even implemented.
[19:42] And that brings us to skill set number five for the AI architect.
[19:47] Communication skills.
[19:50] This is where many technical professionals underestimate the career.
[19:54] They think communication is a soft skill in the architect role.
[19:58] Communication is a hard, critical skill
[20:01] because communication is how we architects create alignment,
[20:04] how we get funding for our architectures and reduce confusion.
[20:08] Communication is how we architects turn complex technology
[20:12] into something the executives can decide to fund or not.
[20:16] And in the AI architect role, you'll need to create
[20:19] architecture artifacts, which are really just another form of communication.
[20:24] Whether it's a target state architecture or a current state assessment,
[20:27] or a roadmap, or a capability map.
[20:30] These artifacts are not paperwork.
[20:32] They're tools that we're using to better communicate
[20:35] and help make better decisions.
[20:38] We are there with creating of these artifacts
[20:41] as a communication strategy to help stakeholders understand what's happening,
[20:46] why it matters, what decisions must be made,
[20:49] and what direction the organization should take.
[20:52] We architects will be writing proposals because we need funding as architects,
[20:56] and you will need to be able to justify the funding for your
[21:00] AI platform, security controls or even cloud architecture.
[21:04] And if you can't write the proposal in
[21:05] business language, which is communication, the project will never get funded.
[21:10] A lot of what we do is architecture, which is also communication
[21:12] is obtaining information.
[21:14] This is probably the most overlooked architect skill
[21:18] where architects have to ask the question what problem are we solving?
[21:23] What does success look like for you?
[21:25] What are the failure points? What are the current processes?
[21:28] For example, who owns the data?
[21:30] So we architects can assume,
[21:32] we discover
[21:33] and we discover by asking questions.
[21:36] Now there's a great architect.
[21:38] You need to be able to tell a story because an executive
[21:42] will remember a story, but they're not going to remember a diagram.
[21:46] Now here's one of the communication ways
[21:48] you can see if someone's ready for an architect role.
[21:53] Someone that's not ready for an architect role will say something like,
[21:56] we need a rag based architecture with a vector database and secure
[22:00] API integration.
[22:02] Very engineering work.
[22:03] Now a strong AI architect, the kind of architect that will get hired
[22:07] will say today your customer service agents are wasting time searching across
[22:11] 12 systems. This increases handle
[22:14] time, creates inconsistent answers, and frustrate customers.
[22:18] We can use AI to give agents trusted answers from a proof of knowledge basis.
[22:22] Now that will reduce our cost.
[22:23] It will improve our quality and lower risk.
[22:26] Now we're talking about the same thing,
[22:29] but the first response is not ready for an architect job.
[22:32] Sounds like an engineering response,
[22:34] which is great if you want to be an engineer.
[22:36] The second response I gave you sounds like an architect
[22:39] with the business skills, executive
[22:41] skills, communication skills, and architect skills to be an architect.
[22:45] And that's the difference that will get you hired.
[22:48] I want to leave you with us.
[22:49] And architects are not paid because they know a tool
[22:52] or know how to build something.
[22:54] And tools change models change, platforms change.
[22:58] But the need for architecture doesn't change.
[23:00] Businesses will always need people that can make decisions, reduce risk,
[23:05] control cost, and align technology with strategy,
[23:09] and be able to communicate whether it's risk, the value of the solution
[23:14] to executives and turn technology into business outcomes.
[23:18] Now, if you'd like to become an AI architect, a cloud architect, an
[23:22] enterprise architect, a security architect or another technology leader,
[23:26] I recommend start
[23:27] preparing like an engineer and to start preparing like an architect.
[23:31] No certification may help you learn a technology,
[23:33] a lab may help you learn how to configure a tool,
[23:36] but certifications will not create the executive trust.
[23:39] Labs will not teach you how to manage stakeholders.
[23:42] Memorizing services does not teach you business strategy,
[23:46] and clicking buttons does not teach you how to lead an architectural decision.
[23:49] I go cloud careers.
[23:50] We build real architecture careers.
[23:52] We don't just only focus on the tech.
[23:54] Our clients are prepared with the full set of architecture skills
[23:57] that means the business skills, the executive
[23:59] skills, the communication skills,
[24:00] and of course, the technical skills to get you hired.
[24:03] So if you're serious about becoming an AI architect or a cloud
[24:07] architect, or a security architect or an enterprise architect,
[24:10] join me on our next Free Architecture webinar
[24:12] where we discuss how did just get your first architect job?
[24:16] And we will cover the five steps you need to succeed.
[24:18] We will discuss what we do in our roles as architects,
[24:21] the skills you need to succeed, what hiring managers desire, what belongs
[24:25] in your architect portfolio, and even how to get more interviews.
[24:29] And because that free
[24:29] webinar is live on zoom, you can ask me any questions you desire.
[24:34] And it's live and free.
[24:35] You can register for the Free Architecture webinar
[24:37] by clicking the link in the description of this video.
[24:41] Now, if you enjoyed this video, please give it a like.
[24:43] Subscribe to our channel and hit the bell to be notified of new videos.
[24:47] To assist you in your architecture career.
[24:49] This is Mike signing off for now
[24:51] and I hope to see you in a free webinar live on zoom or in another video.
[24:55] Take care everyone.
[25:58] Go cloud careers.
[25:59] We built real architecture careers.
[26:00] We don't just focus on the tech, although we do
[26:02] provide strong technical background.
[26:04] Our clients are prepared with the full set of architect skills.
[26:07] That means business skills, executive skills, communication skills
[26:12] and all the technology they need to thrive.
[26:15] So if you're serious about becoming an AI architect or any other type of architect,
[26:20] visit Go Cloud careers.com and learn how we can help you build the skills,
[26:24] the confidence and the career strategy to build your architect career.
[26:27] Or join me on a free architecture webinar where we discuss
[26:31] how to get your first architect job
[26:33] and we will cover the five steps necessary to become an architect.
[26:37] We'll discuss what we do.
[26:38] Is that our in our role as an architect,
[26:39] the skills that you need to succeed as an architect, what hiring managers
[26:43] desire as an architect, even what to put in your architect portfolio.
[26:47] And this webinar is live and free on zoom, so you can ask me any questions
[26:50] you desire about getting hired for your first AI architect job.
[26:54] The link to register for this free webinar is in the description of this video.
[26:59] Now, if you enjoyed this video, please give this video a like.
[27:02] Subscribe to our channel and hit the bell to be notified of new videos
[27:06] to assist you in your architecture career.
