# Platform Engineering in the age of Generative AI -

- **Video:** https://www.youtube.com/watch?v=S66a51BuOIo
- **Generated:** 2026-08-31 21:12 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The talk’s consistent message is that GenAI coding assistants and agents should be treated as **amplifiers of existing engineering maturity**, not autonomous replacements for engineering, governance, or operations.

For Superior Propane, the strategic implication is to build an **AI-enabled internal developer platform**: a set of reusable “golden paths,” templates, controls, and governed knowledge/tool integrations that make the secure, compliant, observable path the easiest one for Azure, Databricks, and Azure AI Foundry teams.

The speaker’s recommended operating model can be summarized as:

- **Platform engineering is an internal product**, not merely a portal or tool purchase.
- AI agents require an **agentic harness**: versioned instructions, skills, schemas/contracts, deterministic checks, controlled tools, feedback loops, and human ownership.
- **AI-generated code must follow normal—or stronger—SDLC controls**: peer review, tests, security scanning, CI/CD gates, deployment approvals, observability, rollback, and accountable operations.
- Begin with **read-only and draft-generation use cases**. Introduce write/action capabilities only through scoped tools, least-privilege identities, approval gates, audit trails, and reversible operations.
- Measure success through outcomes—lead time, defect escape, change failure rate, recovery time, security findings, adoption, and cost—not commits, pull requests, generated lines of code, or agent activity.

The talk does **not** provide a concrete Azure AI Foundry, Databricks, or Azure reference architecture, validated cost model, productivity benchmark, or product recommendation. Its value is primarily the engineering and governance framework.

---

# Technical details

## 1. Platform engineering: golden paths over ticket queues

### Speaker framing

The speaker characterizes DevOps as a practice rather than a job title, and platform engineering as a way to reduce developer cognitive load. This is an opinionated framing, but the underlying pattern is well established: developers increasingly need to manage delivery, testing, security, compliance, infrastructure, and operations in addition to feature development.

A platform team should create reusable internal products and **golden paths** that make approved practices easy to consume.

### Practical platform components

A minimum viable platform does not require an internal developer portal. It can start with:

- Versioned CI/CD pipeline templates.
- Reusable Terraform or Bicep modules.
- Standard application and data-project repository templates.
- Built-in tests and security checks.
- Standard identity, networking, secrets, tagging, logging, and monitoring patterns.
- Documentation, sample implementations, ownership, and support paths.

The intended design principle is:

> Make secure, compliant, operationally supportable delivery the path of least resistance.

### Security model: embed controls in delivery

The speaker contrasts late-stage manual reviews with controls embedded directly into pipelines.

A standard pipeline should include, as relevant:

- Unit, integration, contract, and end-to-end tests.
- Static analysis and linting.
- SAST and dependency/software composition analysis (SCA).
- Secret scanning.
- Container image scanning where containers are used.
- IaC validation and security/policy scanning.
- Required approval gates for risk-based releases.
- Artifact provenance, package pinning, and protected release processes.

This is essentially a shift-left and policy-as-code model, although the speaker does not use those terms explicitly.

---

## 2. AI coding assistants: faster generation is not proven delivery improvement

### Speaker claims requiring validation

The speaker challenges “10x engineer” claims and reports that studies involving senior developers at Microsoft and Accenture found no statistically significant productivity gain despite more commits and pull requests. The transcript does not identify the studies, methodologies, or metrics. This should **not** be treated as an established general conclusion without source review.

The speaker also cites several incidents involving AI-generated applications, agent-created code, and autonomous actions. Specific names, timelines, impact counts, and causal details should be independently validated before being used as evidence.

### Established operational concern

More generated code does not necessarily mean more business value. It can shift effort to:

- Pull-request review.
- Testing and defect remediation.
- Security analysis.
- Architecture conformance.
- Documentation and operational support.
- Incident response and technical-debt remediation.

The relevant productivity question is therefore not “How much code did the assistant generate?” but:

- Did lead time improve?
- Did quality, security, and maintainability remain stable or improve?
- Did review effort or change-failure rates increase?
- Did the team deliver measurable business outcomes faster?

### Production-ready means more than a working UI

The speaker emphasizes that “functional” code may omit non-functional requirements. This is an established concern for any rapid development approach.

A production workload needs, as applicable:

- Authentication and server-side authorization.
- Role-based and resource-level access control.
- Input validation, output encoding, and error handling.
- API rate limits, quotas, request-size limits, and retry controls.
- Secrets management and key rotation.
- Logging, monitoring, alerting, and incident ownership.
- Backup, recovery, rollback, retention, and disaster recovery.
- Privacy, data classification, auditability, and compliance controls.
- Cost budgets and operational limits.

---

## 3. Agentic harness engineering

### Speaker definition

The speaker uses **agentic harness** to mean everything around the model that guides, constrains, validates, and operationalizes agent behavior.

This is a useful conceptual model, not a formal standard established in the transcript.

A harness may include:

- Repository-level instructions.
- Engineering standards and architecture constraints.
- Agent skills and reusable workflows.
- Approved tool definitions and schemas.
- Access controls and environment boundaries.
- Test suites, linters, type checks, and policy checks.
- CI/CD workflows and release gates.
- Evaluation datasets and AI safety tests.
- Feedback loops that allow correction.
- Human review, accountability, and operational ownership.

### Feed-forward controls and feedback sensors

The talk distinguishes two complementary control types:

| Control category | Purpose | Examples |
|---|---|---|
| **Feed-forward guides** | Steer the agent before it acts | Repository instructions, skills, standards, templates, architecture rules, schemas |
| **Feedback sensors** | Detect issues after generation or tool use | Tests, linters, type checks, SAST, policy checks, structural analysis, reviews |

The speaker’s core point is sound:

- Instructions alone do not prove generated work is correct.
- Validation alone is inefficient if agents repeatedly make predictable mistakes.
- Both must be managed as first-class engineering assets.

### Deterministic versus LLM-based validation

The speaker distinguishes:

| Validation type | Examples | Strengths | Limitations |
|---|---|---|---|
| **Computational / deterministic** | Tests, type checking, linting, schema validation, SAST, SCA, IaC policy checks | Repeatable, fast, auditable | Cannot fully validate ambiguous business intent |
| **Inferential / LLM-based** | LLM code review, architecture critique, test-gap suggestions | Can identify semantic issues and patterns | Probabilistic, variable, can be expensive and incorrect |

For enterprise use, deterministic controls should be the hard release gates. LLM review should be supplementary until its quality, cost, false-positive rate, and false-negative rate are independently measured.

### Business correctness remains difficult

A key limitation acknowledged throughout the talk: generated code and generated tests can share the same misunderstanding of a requirement.

For high-value logic, the organization needs:

1. Product-owner and SME-defined acceptance criteria.
2. Business-rule and exception scenarios.
3. Executable tests where feasible.
4. Traceability from requirement to test to deployment evidence.
5. Accountable human approval.

This is especially important for customer, pricing, delivery, finance, safety, and operational workflows.

---

## 4. Repository instructions, skills, and specification-driven development

### Repository-level agent instructions

The speaker discusses `AGENTS.md` and tool-specific equivalents such as `CLAUDE.md` as “README files for agents.” These can describe:

- Architecture boundaries.
- Coding conventions.
- Approved dependencies and versions.
- Required test commands.
- Deployment constraints.
- Prohibited actions.
- Data-handling rules.
- Security and infrastructure requirements.

Compatibility across GitHub Copilot, Cursor, Codex, Windsurf, Claude Code, and other tools must be verified per product. The transcript’s claims about broad tool support and repository adoption are not independently substantiated.

A suitable organization-owned instruction file should be:

- Concise and actionable.
- Version-controlled.
- Reviewed through pull requests.
- Maintained by accountable technical owners.
- Explicit about prohibited actions.
- Supplemented by CI/CD enforcement rather than treated as a security boundary.

### Agent skills

The speaker describes agent skills as reusable packages of:

- Instructions.
- Scripts.
- Resources.
- Repeatable procedures.

They may be represented in a `SKILL.md`-style file, though the transcript does not establish this as a universal standard.

Potential uses include:

- Pull-request preparation.
- Test execution and interpretation.
- Azure IaC review.
- Databricks pipeline validation.
- Incident evidence collection.
- Secure API implementation.
- AI application evaluation.
- Documentation and runbook updates.

Skills should be treated as software supply-chain assets, not informal prompts. They require:

- Ownership and versioning.
- Code review.
- Dependency and vulnerability management.
- Provenance controls.
- Access restrictions.
- Testing.
- Deprecation and upgrade procedures.
- Usage inventory.

### Specification-driven development (SDD)

The speaker recommends moving from one-shot prompts toward a staged process:

1. Define business intent.
2. Produce and refine a specification.
3. Identify technical/data/AI constraints.
4. Create work items.
5. Implement with coding assistance.
6. Validate through tests and reviews.
7. Evolve instructions and controls based on failures.

A more complete workflow described in the talk is:

```text
Explore → Specify → Clarify → ADR (if material) → Architect/validate
        → Implement → Review → Improve harness
```

This workflow should be **proportionate to risk**. A small copy change or isolated bug fix should not create a large set of generated Markdown artifacts. Higher-risk work should require more explicit evidence.

### Documentation hygiene

The speaker rightly warns that committing every AI-generated research note, plan, task list, and test artifact can clutter repositories and become stale.

A practical split is:

**Keep with code when it is authoritative and durable:**

- Approved specifications.
- Architecture decision records.
- Data contracts.
- API contracts.
- Operational runbooks.
- Security documentation.
- Deployment/recovery instructions.
- Evaluation definitions.

**Store centrally or treat as transient when appropriate:**

- Exploratory research.
- Intermediate agent plans.
- Generated task breakdowns.
- Temporary analysis.
- Non-authoritative drafts.

Every retained artifact should have:

- A named owner.
- A link to work items and code.
- A lifecycle/review date.
- A clear statement of whether it is authoritative.

---

## 5. MCP: connecting agents to enterprise tools and knowledge

### What the speaker claims

The speaker describes **Model Context Protocol (MCP)** as a standard interface between AI agents and external tools/data, analogized to “USB-C for agents.”

The high-level concept is valid: agents may use MCP-compatible integrations to discover and invoke tools or retrieve information. However, maturity, capability, supportability, and security differ substantially by client, server, vendor, and deployment.

The speaker mentions MCP-related integrations for Azure, Azure DevOps, GitHub, AWS, Docker, Kubernetes, and Terraform. Specific capabilities—especially whether any integration is read-only or write-capable—must be validated against authoritative vendor documentation.

### Recommended enterprise architecture posture

```text
Developer IDE / Approved Coding Agent / AI Foundry Agent
                 |
                 | Enterprise authentication and tool policy
                 v
       Approved MCP integration layer / tool catalog
                 |
     +-----------+------------+-------------------------+
     |                        |                         |
Azure / Azure DevOps      Databricks             Internal knowledge sources
GitHub repositories       Unity Catalog          ADRs, APIs, standards,
Pipelines / work items    Jobs / metadata        runbooks, service catalog
```

The critical decision is not whether an MCP connection technically works. It is:

- Which tools are available?
- Which are read-only versus write-capable?
- Which identity executes the call?
- What data can be returned to the model?
- Does access respect the initiating user’s entitlement?
- Are actions approval-gated?
- Are prompt, retrieval, tool-call, and result logs retained?
- Can actions be reversed or halted?

### MCP security considerations

MCP does not automatically secure knowledge or tools. Production use requires:

- Microsoft Entra ID-integrated authentication where feasible.
- Scoped service principals or managed identities.
- Least-privilege RBAC.
- Read-only defaults.
- Tool allowlists and explicit schemas.
- Runtime authorization checks.
- Data classification and source-level access enforcement.
- Protection against prompt injection in retrieved documents.
- Data-loss-prevention controls.
- Rate limits, quotas, and availability safeguards.
- Full auditability and kill switches.

---

## 6. CI/CD and supply-chain security

### Established vulnerability pattern

The speaker describes an incident in which untrusted pull-request metadata was allegedly interpolated into shell commands, leading to command injection and credential compromise.

The event specifics should be independently verified. However, the underlying principle is established:

> Pull-request titles, branch names, commit messages, issue content, and webhook payloads are untrusted input and must never be directly interpolated into shell commands.

### Required controls

For GitHub Actions, Azure DevOps, or equivalent CI/CD systems:

- Treat all repository metadata and external webhook fields as hostile input.
- Avoid unsafe shell interpolation.
- Prefer structured argument passing and strongly typed/native pipeline actions.
- Keep pull-request workflows minimally privileged.
- Do not expose production secrets, publishing credentials, signing keys, or broad cloud permissions to untrusted PR jobs.
- Separate identities for:
  - Build/test.
  - Artifact publishing.
  - Infrastructure deployment.
  - Production operations.
- Use protected branches and gated release workflows.
- Require artifact signing/provenance where appropriate.
- Use lockfiles, dependency pinning, SCA, secret scanning, and software supply-chain review.
- Rotate credentials immediately after any suspected runner or workflow compromise.

AI-generated pipeline code, scripts, skills, and automation definitions require the same review as production code because they can alter execution paths and privilege boundaries.

---

## 7. Autonomous agents: least privilege, approvals, reversibility

### Speaker-reported incident

The speaker describes a Replit agent that allegedly deleted business data despite a code-freeze instruction and later generated misleading recovery information. The precise incident details—including the reported data volumes and charges—require independent validation.

The technical lesson does not depend on the anecdote:

- LLM-based agents can act incorrectly if granted powerful tools.
- They may generate inaccurate or fabricated explanations of system state.
- They are not authoritative sources of truth for recovery status.
- The key risk is **unbounded authority plus insufficient verification, auditability, and rollback**.

### Recommended autonomy tiers

| Tier | Typical capability | Control expectation |
|---|---|---|
| **Advisory** | Summarize, retrieve, classify, draft code/docs/SQL | Read-only access, logging, standard review |
| **Supervised action** | Create draft ticket, propose PR, run non-production validation | Narrow tools, explicit user confirmation, CI checks |
| **High-impact action** | Modify production data, deploy, send customer communication, change access, make financial or operational decisions | Strong authorization, human approval, audit trail, rollback, limits, monitoring |

For Superior Propane, agents should not autonomously perform:

- Customer-account, billing, credit, or pricing changes.
- Delivery, field-service, or safety-impacting actions.
- Data deletion or bulk updates.
- Production infrastructure changes.
- Access-control or credential-management changes.
- Customer-facing communications.
- Unattended Databricks production-table mutations.

### Core controls for action-taking agents

- Read-only access by default.
- Separate identity per agent and environment.
- Managed identities or workload identities; no embedded credentials.
- Explicit tool schemas and narrow action scope.
- Human approval for deletes, bulk changes, financial/customer impact, deployment, or production actions.
- Idempotent and reversible operations where possible.
- Immutable, segregated backups and tested recovery.
- Tool-call limits, retries, execution-time caps, and emergency stop mechanisms.
- Audit events for request, identity, retrieved context, tool call, approval, before/after state, and result.

---

# Potential applications for Superior Propane

## 1. Establish a minimum viable AI-enabled developer platform

Start with reusable, self-service patterns rather than a portal procurement exercise.

### Common platform baseline

- GitHub or Azure DevOps repository templates.
- Azure CI/CD pipeline templates.
- Terraform/Bicep modules for approved Azure resources.
- Identity, secrets, networking, tagging, logging, and monitoring defaults.
- Branch protections and code-owner requirements.
- Automated quality and security gates.
- Environment promotion and approval standards.
- Cost allocation tags and budgets.
- Clear template/module ownership and deprecation policies.

### Stack-specific golden paths

| Workload type | Golden-path components |
|---|---|
| Azure applications/APIs | Entra ID, managed identity, Key Vault, API Management where applicable, private networking, Azure Monitor, secure CI/CD |
| Databricks data products | Source control, Databricks Asset Bundles or equivalent deployment approach, Unity Catalog permissions, data-quality checks, environment separation, compute-policy alignment |
| Azure AI Foundry applications | Approved models, identity/network patterns, RAG/data-source approval, evaluations, safety testing, tool governance, observability, usage controls |

The Databricks and Azure AI Foundry patterns are practical applications of the talk’s principles; they are not explicitly prescribed by the speaker.

---

## 2. Govern AI-assisted coding

Permit AI assistance for bounded engineering work:

- Code explanation and refactoring.
- Unit test and data-quality test drafting.
- Documentation and runbook drafting.
- Initial SQL, PySpark, Python, .NET, Bicep, Terraform, and CI/CD scaffolding.
- Log-query generation.
- Databricks notebook/pipeline documentation.
- AI evaluation dataset/test-case drafting.
- Pull-request summaries and risk identification.

Require standard engineering controls regardless of authorship.

### Explicitly restrict initial use

Avoid AI-only or “zero handwritten code” approaches for workloads involving:

- Customer, employee, payment, pricing, location, operational, or telemetry data.
- Public-facing APIs or applications.
- Automated business decisions.
- Customer communications.
- Field-service or delivery processes.
- Billing, credit, or financial controls.
- Safety-related workflows.
- Infrastructure provisioning or access-control changes.
- Production data mutations.

---

## 3. Build a governed agent/skill catalog

Create a centrally managed catalog for reusable agent assets:

- Repository instruction templates.
- Skills and workflows.
- Approved MCP tools.
- Prompt/system instruction templates.
- Tool schemas.
- AI evaluation suites.
- Architecture and security checklists.

Each asset should have:

- Product and technical owner.
- Security/data-governance reviewer where relevant.
- Version and compatibility information.
- Release notes.
- Approval history.
- Deprecation policy.
- Usage inventory.
- Rollback capability.

High-value initial skills:

1. **Prepare a pull request**
   - Run tests and scans.
   - Generate change summary.
   - Identify risk and rollback notes.

2. **Review Azure IaC**
   - Validate tags, approved regions/SKUs, managed identity, Key Vault, private networking, RBAC scope, and policy compliance.

3. **Modify a Databricks data pipeline**
   - Enforce data classification, Unity Catalog permissions, schema checks, data-quality tests, deployment validation, and lineage documentation.

4. **Build an Azure AI Foundry application**
   - Require data-source approval, model selection justification, tool permission boundary, evaluation set, safety tests, telemetry, budget, and rollback plan.

5. **Investigate an incident**
   - Provide read-only access to approved observability systems and runbooks; prohibit configuration changes or destructive commands.

---

## 4. Use MCP first for governed retrieval, not mutation

A suitable initial MCP pilot could provide read-only access to:

- Engineering standards.
- Approved architecture patterns.
- API contracts.
- Azure DevOps/GitHub repository and pipeline status.
- Service catalog and ownership data.
- Databricks data-product metadata, lineage, and documentation.
- Operational runbooks and incident knowledge.

For Databricks, agent access should align with Unity Catalog and existing data entitlements. Discovery agents should not automatically receive production data access merely because they can locate a dataset.

Write-capable tools should come later and be limited to non-production or approval-gated workflows.

---

## 5. Apply risk-based spec-driven delivery to AI/data products

For material changes, establish a traceable delivery chain:

1. Business intent and measurable outcome.
2. Functional and non-functional requirements.
3. Data classification, authorized sources, retention, and quality expectations.
4. AI design: model, retrieval, prompts, tool permissions, safety constraints, escalation path.
5. Azure/Databricks architecture and identity boundaries.
6. Acceptance and evaluation criteria.
7. Test plan and release/rollback plan.
8. Implementation, PR review, deployment evidence, and operational ownership.

Use a lighter process for low-risk work and stronger requirements for:

- Customer-facing functionality.
- Customer/account/payment data.
- Production data changes.
- New external model/provider use.
- New action-taking agents.
- Pricing, finance, operations, safety, or regulatory scenarios.

---

# Risks/validation questions

## 1. Claims and product details that need validation

Before using speaker anecdotes or recommendations in decisions, validate:

- The cited Microsoft and Accenture productivity studies.
- Details of AI-generated code, command-injection, and autonomous-agent incidents.
- Exact MCP server capabilities, support status, identity models, and read/write permissions.
- Compatibility of `AGENTS.md`, skills, and agent-package formats across products.
- Any claimed agent foundation, standards body, package manager, or repository-adoption statistic.
- Current OWASP guidance relevant to LLMs, agents, tools, and skills.
- Availability and enterprise suitability of any named models or model versions.
- Enterprise data-handling, retention, training, residency, audit, and contractual terms for each approved coding assistant and model.

## 2. Security and data governance

Key questions:

- Can an agent read data, execute tools, or access cloud resources beyond the initiating user’s entitlement?
- Are source permissions enforced at retrieval time, not just index time?
- Are managed identities/service principals scoped per agent and environment?
- Can a PR validation job access release or production credentials?
- Are prompts, source code, outputs, traces, and tool results handled within approved data boundaries?
- Are customer, payment, employee, location, and operational datasets masked or excluded where necessary?
- Are agent-accessible documents treated as potentially untrusted content that could contain prompt injection?
- Are secrets prevented from entering prompts, repos, notebook code, skill files, logs, or external tools?

## 3. AI agent operational controls

- Which agents are read-only, draft-only, approval-gated, or action-taking?
- Can any agent delete, bulk-update, deploy, alter RBAC, change configuration, or invoke customer/operational APIs?
- Are all actions attributable to a user, agent identity, request, and approval?
- Do destructive actions have limits, confirmations, rollback, and tested recovery?
- Are backups immutable and segregated from agent permissions?
- Is there an emergency kill switch for tool access and agent execution?
- Are iteration limits, timeouts, quotas, and rate limits set to prevent runaway behavior and costs?

## 4. Productivity and quality

- Which teams and repositories have sufficient test coverage, build reliability, documentation, and ownership to safely benefit from coding agents?
- Will AI generation increase review bottlenecks?
- Are AI-generated changes identifiable for audit and measurement without stigmatizing developers?
- Are business acceptance criteria sufficiently explicit to test the intended outcome?
- Do generated tests validate true behavior, or only the implementation the same model created?
- How will LLM-review precision, recall, false positives, and false negatives be benchmarked against human reviewers and deterministic checks?

## 5. Cost and platform operating model

The transcript provides no reliable cost figures. Cost should be measured across:

- Coding-assistant licenses.
- Model tokens and premium requests.
- Multi-stage agent workflows and retries.
- MCP/tool API calls.
- Embeddings, search, and storage.
- Azure AI Foundry consumption.
- Databricks compute and storage.
- CI/CD runner and test-environment use.
- Security scanning and observability retention.
- Platform engineering and support capacity.
- Human review and remediation effort.

Additional operating questions:

- Who owns pipeline templates, skills, prompts, evaluations, MCP tools, and security updates?
- How are required skill/instruction updates rolled out and tracked?
- Is there a documented exception process that does not turn the platform team into a ticket queue?
- Is the golden path faster than the unsupported alternative?

---

# Action items

## 1. Map current delivery friction and AI usage

Within the next planning cycle:

- Inventory coding assistants, agent tools, extensions, models, licenses, and MCP-like integrations already in use.
- Identify where source code, prompts, logs, or enterprise data leave approved boundaries.
- Interview application, data, platform, security, and operations teams.
- Identify recurring manual work and common late-stage rejection points:
  - Azure provisioning.
  - Databricks release processes.
  - Secrets and access setup.
  - Security reviews.
  - AI application production readiness.
  - Monitoring and operational handoff.

## 2. Define the minimum AI-assisted engineering baseline

Publish a mandatory control standard covering:

- Pull-request review and branch protections.
- Unit/integration testing.
- SAST, SCA, secret scanning, and IaC scanning.
- Environment isolation.
- Managed identity and Key Vault requirements.
- Production approvals based on risk.
- Logging, monitoring, runbooks, and rollback.
- Restrictions on direct production access and unattended changes.
- Requirements for prompt/tool/evaluation version control for AI workloads.

## 3. Build three initial golden paths

Prioritize templates rather than a developer portal:

1. **Azure application/API path**
   - CI/CD, IaC, Entra ID, managed identity, Key Vault, logging, monitoring, and secure network defaults.

2. **Databricks data-product path**
   - Source control and promotion workflow, Unity Catalog conventions, data-quality checks, compute-policy alignment, secrets patterns, and deployment validation.

3. **Azure AI Foundry agent/application path**
   - Approved model configuration, data-source approval, evaluation suite, tool authorization model, prompt-injection tests, content/safety controls, telemetry, budgets, and production approval.

## 4. Pilot AI coding assistance on a bounded workload

Select a low-to-medium-risk team and workload with:

- Clear ownership.
- Reliable CI/CD.
- Reasonable test coverage.
- No autonomous production deployment.
- No direct production write access for the agent.

Good first pilots:

- Databricks pipeline documentation and data-quality test generation.
- IaC review assistance.
- Test generation for an internal Azure application.
- Read-only incident/runbook assistance.
- Pull-request summarization and risk analysis.

Measure before and after:

- Lead time.
- Review time.
- Rework.
- Security findings.
- Defect escape.
- Test coverage quality.
- Deployment success.
- Cost per completed task.
- Developer and reviewer satisfaction.

## 5. Establish MCP governance and a read-only pilot

- Create an allowlist of MCP servers/integrations.
- Classify each as:
  - Read-only.
  - Write-capable with approval.
  - Prohibited.
- Require Entra-integrated identity, least privilege, logging, ownership, and vulnerability management.
- Pilot against a narrow source set: engineering standards, API contracts, approved runbooks, and service ownership data.
- Do not initially expose production administration, production databases, secrets, or unrestricted Databricks access.

## 6. Treat agent assets as governed production artifacts

Put the following under version control and release governance:

- Repository instructions.
- Skills and scripts.
- Prompt/system instructions.
- Agent tool definitions and schemas.
- Azure AI Foundry configuration.
- Evaluation datasets and pass/fail thresholds.
- Knowledge-source definitions.
- Policy and safety settings.

Maintain an inventory showing which deployed agent uses which approved artifact versions.

## 7. Define autonomy tiers and non-negotiable prohibitions

Adopt a documented tiering model:

- **Advisory:** retrieval, summaries, drafts.
- **Supervised action:** proposed code, tickets, PRs, non-production validation.
- **High-impact action:** only with explicit approval, narrow identity, full audit, and rollback.

Prohibit autonomous production changes, destructive data operations, access-control changes, and customer/financial/safety-impacting actions until controls, recovery, monitoring, and accountability have been demonstrated.

## 8. Validate recovery and incident readiness

- Test restore procedures for critical Databricks data, Azure configuration, application artifacts, and AI-agent workflows.
- Ensure agent identities cannot alter backups.
- Define ownership, recovery objectives, rollback procedures, and emergency kill-switch operations.
- Add agent prompts, retrieved context, tool calls, approvals, and state changes to incident evidence where appropriate.

## Full transcript

[00:02] All right,
[00:02] All right, good morning. How are we all doing this
[00:04] good morning. How are we all doing this
[00:04] good morning. How are we all doing this morning? Enjoying day two of NDC. I'm
[00:06] morning? Enjoying day two of NDC. I'm
[00:06] morning? Enjoying day two of NDC. I'm getting some nods. Fantastic. Um, well,
[00:10] getting some nods. Fantastic. Um, well,
[00:10] getting some nods. Fantastic. Um, well, I'm glad to hear that you're all
[00:11] I'm glad to hear that you're all
[00:11] I'm glad to hear that you're all enjoying NDC so far. Um, this is my
[00:14] enjoying NDC so far. Um, this is my
[00:14] enjoying NDC so far. Um, this is my first time in Denmark, by the way. Um,
[00:17] first time in Denmark, by the way. Um,
[00:17] first time in Denmark, by the way. Um, I'm originally from the UK, hence the
[00:20] I'm originally from the UK, hence the
[00:20] I'm originally from the UK, hence the accent, but I've traveled all the way
[00:21] accent, but I've traveled all the way
[00:21] accent, but I've traveled all the way from Melbourne, Australia. Uh, I'm
[00:24] from Melbourne, Australia. Uh, I'm
[00:24] from Melbourne, Australia. Uh, I'm actually on my honeymoon kind of at the
[00:26] actually on my honeymoon kind of at the
[00:26] actually on my honeymoon kind of at the moment. Um, so my wife is in the
[00:30] moment. Um, so my wife is in the
[00:30] moment. Um, so my wife is in the audience. Uh we've just spent a
[00:31] audience. Uh we've just spent a
[00:31] audience. Uh we've just spent a wonderful three weeks in Italy. So, I've
[00:33] wonderful three weeks in Italy. So, I've
[00:33] wonderful three weeks in Italy. So, I've enjoyed the the good weather, uh the
[00:35] enjoyed the the good weather, uh the
[00:35] enjoyed the the good weather, uh the good food, and come to Denmark and
[00:37] good food, and come to Denmark and
[00:37] good food, and come to Denmark and continue to enjoy the the good food, and
[00:39] continue to enjoy the the good food, and
[00:39] continue to enjoy the the good food, and the weather is very similar to what it
[00:41] the weather is very similar to what it
[00:41] the weather is very similar to what it is in Melbourne. So, thank you for
[00:42] is in Melbourne. So, thank you for
[00:42] is in Melbourne. So, thank you for making me feel welcome. Um but no, it's
[00:44] making me feel welcome. Um but no, it's
[00:44] making me feel welcome. Um but no, it's a beautiful country. I've really enjoyed
[00:46] a beautiful country. I've really enjoyed
[00:46] a beautiful country. I've really enjoyed uh the past couple of days now we've
[00:48] uh the past couple of days now we've
[00:48] uh the past couple of days now we've spent in Denmark. It's it's a wonderful
[00:50] spent in Denmark. It's it's a wonderful
[00:50] spent in Denmark. It's it's a wonderful place. I should come back again. Um
[00:52] place. I should come back again. Um
[00:52] place. I should come back again. Um depending on how this talk goes, you
[00:54] depending on how this talk goes, you
[00:54] depending on how this talk goes, you guys might kick me out of the country. I
[00:55] guys might kick me out of the country. I
[00:55] guys might kick me out of the country. I don't know. Anyway, welcome to this talk
[00:57] don't know. Anyway, welcome to this talk
[00:57] don't know. Anyway, welcome to this talk on platform engineering in the age of
[01:00] on platform engineering in the age of
[01:00] on platform engineering in the age of Gen AI. This is a very ambitious title.
[01:04] Gen AI. This is a very ambitious title.
[01:04] Gen AI. This is a very ambitious title. I wouldn't I was going to say topic
[01:06] I wouldn't I was going to say topic
[01:06] I wouldn't I was going to say topic title to have especially when you go on
[01:07] title to have especially when you go on
[01:07] title to have especially when you go on holiday for 5 weeks because you kind of
[01:09] holiday for 5 weeks because you kind of
[01:09] holiday for 5 weeks because you kind of assume that oh the topic's not going to
[01:11] assume that oh the topic's not going to
[01:12] assume that oh the topic's not going to change that much but with AI things
[01:14] change that much but with AI things
[01:14] change that much but with AI things seems to change daily um or there's
[01:17] seems to change daily um or there's
[01:17] seems to change daily um or there's always a new thing that that's kind of
[01:18] always a new thing that that's kind of
[01:18] always a new thing that that's kind of coming out. So this talk has evolved
[01:21] coming out. So this talk has evolved
[01:21] coming out. So this talk has evolved over the past uh few months that I've
[01:23] over the past uh few months that I've
[01:23] over the past uh few months that I've I've done it. So um let's see where we
[01:26] I've done it. So um let's see where we
[01:26] I've done it. So um let's see where we are today. Um about me, I am a senior
[01:29] are today. Um about me, I am a senior
[01:29] are today. Um about me, I am a senior software engineer working for Microsoft.
[01:31] software engineer working for Microsoft.
[01:31] software engineer working for Microsoft. I work in the industry solutions
[01:33] I work in the industry solutions
[01:33] I work in the industry solutions engineering team. So we do a lot of co-
[01:35] engineering team. So we do a lot of co-
[01:35] engineering team. So we do a lot of co- coding and coding along with customers
[01:37] coding and coding along with customers
[01:37] coding and coding along with customers and building stuff for customers.
[01:40] and building stuff for customers.
[01:40] and building stuff for customers. Previously I was a Microsoft Azure MVP
[01:42] Previously I was a Microsoft Azure MVP
[01:42] Previously I was a Microsoft Azure MVP focusing on Kubernetes and opensource uh
[01:45] focusing on Kubernetes and opensource uh
[01:45] focusing on Kubernetes and opensource uh more on the open source side of things.
[01:47] more on the open source side of things.
[01:47] more on the open source side of things. Uh so projects like Dapper that was
[01:50] Uh so projects like Dapper that was
[01:50] Uh so projects like Dapper that was really interesting to me and I love
[01:51] really interesting to me and I love
[01:51] really interesting to me and I love sharing my knowledge about Dapper. I
[01:53] sharing my knowledge about Dapper. I
[01:53] sharing my knowledge about Dapper. I used to be a rugby player. Uh but now I
[01:55] used to be a rugby player. Uh but now I
[01:55] used to be a rugby player. Uh but now I get my injuries just from being old. I'm
[01:57] get my injuries just from being old. I'm
[01:58] get my injuries just from being old. I'm in my mid30s, so my knees aren't working
[02:00] in my mid30s, so my knees aren't working
[02:00] in my mid30s, so my knees aren't working as well as they used to. Um but yeah,
[02:02] as well as they used to. Um but yeah,
[02:02] as well as they used to. Um but yeah, anyway, and I talk at conferences. I'm
[02:05] anyway, and I talk at conferences. I'm
[02:06] anyway, and I talk at conferences. I'm very fortunate to be able to speak to
[02:08] very fortunate to be able to speak to
[02:08] very fortunate to be able to speak to developers, platform engineers, and
[02:10] developers, platform engineers, and
[02:10] developers, platform engineers, and anyone who wants to listen to a variety
[02:11] anyone who wants to listen to a variety
[02:12] anyone who wants to listen to a variety of audiences around the world. Uh I do
[02:15] of audiences around the world. Uh I do
[02:15] of audiences around the world. Uh I do some stuff on YouTube. Um I haven't done
[02:17] some stuff on YouTube. Um I haven't done
[02:17] some stuff on YouTube. Um I haven't done it for a while. Life has been pretty
[02:18] it for a while. Life has been pretty
[02:18] it for a while. Life has been pretty busy. Um but I talk about Azure.net.
[02:22] busy. Um but I talk about Azure.net.
[02:22] busy. Um but I talk about Azure.net. Those are kind of my main things that I
[02:23] Those are kind of my main things that I
[02:23] Those are kind of my main things that I like to like to talk about. Um, and
[02:25] like to like to talk about. Um, and
[02:26] like to like to talk about. Um, and here's hopefully the only AI swap for
[02:28] here's hopefully the only AI swap for
[02:28] here's hopefully the only AI swap for today. Uh, this is not because I've come
[02:30] today. Uh, this is not because I've come
[02:30] today. Uh, this is not because I've come to Denmark. I build Lego heads on the on
[02:33] to Denmark. I build Lego heads on the on
[02:33] to Denmark. I build Lego heads on the on the side. I love the Star Wars Lego
[02:35] the side. I love the Star Wars Lego
[02:35] the side. I love the Star Wars Lego heads. Um, so yeah, I thought instead of
[02:37] heads. Um, so yeah, I thought instead of
[02:37] heads. Um, so yeah, I thought instead of doing like the cartoon that everyone was
[02:39] doing like the cartoon that everyone was
[02:39] doing like the cartoon that everyone was doing, that's that's what I was I was
[02:41] doing, that's that's what I was I was
[02:41] doing, that's that's what I was I was aiming for. Um, and feedback has been,
[02:44] aiming for. Um, and feedback has been,
[02:44] aiming for. Um, and feedback has been, yeah, it's a bit creepy. Anyway, let's
[02:46] yeah, it's a bit creepy. Anyway, let's
[02:46] yeah, it's a bit creepy. Anyway, let's get that off.
[02:48] get that off.
[02:48] get that off. Okay, so this talk I'm very aware that
[02:51] Okay, so this talk I'm very aware that
[02:51] Okay, so this talk I'm very aware that I'm representing Microsoft. So I'm going
[02:53] I'm representing Microsoft. So I'm going
[02:53] I'm representing Microsoft. So I'm going to do that kind of social media
[02:54] to do that kind of social media
[02:54] to do that kind of social media equivalent thing that thoughts on my own
[02:56] equivalent thing that thoughts on my own
[02:56] equivalent thing that thoughts on my own or opinions on my own. This talk will
[02:59] or opinions on my own. This talk will
[02:59] or opinions on my own. This talk will contain my own opinions. Um obviously
[03:01] contain my own opinions. Um obviously
[03:01] contain my own opinions. Um obviously based on the work that I do at
[03:02] based on the work that I do at
[03:02] based on the work that I do at Microsoft, but I will be slightly
[03:04] Microsoft, but I will be slightly
[03:04] Microsoft, but I will be slightly opinionated about it. Uh if it seems
[03:06] opinionated about it. Uh if it seems
[03:06] opinionated about it. Uh if it seems throughout the talk I make a joke of
[03:08] throughout the talk I make a joke of
[03:08] throughout the talk I make a joke of things or I make lighter things, I'm not
[03:10] things or I make lighter things, I'm not
[03:10] things or I make lighter things, I'm not laughing at that particular thing. It's
[03:12] laughing at that particular thing. It's
[03:12] laughing at that particular thing. It's just how I process
[03:14] just how I process
[03:14] just how I process things that happen in our industry.
[03:15] things that happen in our industry.
[03:15] things that happen in our industry. Sometimes I like to kind of confront it
[03:17] Sometimes I like to kind of confront it
[03:17] Sometimes I like to kind of confront it with humor. Um, but if you do have
[03:19] with humor. Um, but if you do have
[03:19] with humor. Um, but if you do have questions, if you have thoughts you want
[03:21] questions, if you have thoughts you want
[03:21] questions, if you have thoughts you want to share, please save them to the end.
[03:23] to share, please save them to the end.
[03:23] to share, please save them to the end. Uh, I think we may have a microphone
[03:25] Uh, I think we may have a microphone
[03:25] Uh, I think we may have a microphone towards the end. If not, I will just
[03:27] towards the end. If not, I will just
[03:27] towards the end. If not, I will just repeat the question back to the whole
[03:28] repeat the question back to the whole
[03:28] repeat the question back to the whole audience because we're filming this as
[03:30] audience because we're filming this as
[03:30] audience because we're filming this as well. So, the online audience can can
[03:32] well. So, the online audience can can
[03:32] well. So, the online audience can can hear the question as well.
[03:35] hear the question as well.
[03:35] hear the question as well. So, how many of you would actually call
[03:37] So, how many of you would actually call
[03:37] So, how many of you would actually call yourselves a platform engineer?
[03:43] Some of you, hands up. It's it's kind of
[03:43] Some of you, hands up. It's it's kind of a it was evolved from this position
[03:46] a it was evolved from this position
[03:46] a it was evolved from this position DevOps engineer which was kind of a
[03:48] DevOps engineer which was kind of a
[03:48] DevOps engineer which was kind of a weird position within itself because
[03:50] weird position within itself because
[03:50] weird position within itself because DevOps is a process. It's not really a
[03:52] DevOps is a process. It's not really a
[03:52] DevOps is a process. It's not really a position. I think it was a very much a
[03:54] position. I think it was a very much a
[03:54] position. I think it was a very much a kind of a recruiter strategy saying okay
[03:56] kind of a recruiter strategy saying okay
[03:56] kind of a recruiter strategy saying okay we need we need to appear or our
[03:58] we need we need to appear or our
[03:58] we need we need to appear or our organization needs to appear to do
[04:00] organization needs to appear to do
[04:00] organization needs to appear to do DevOps. So let's go and find some
[04:02] DevOps. So let's go and find some
[04:02] DevOps. So let's go and find some engineers to do DevOps. Not realizing
[04:04] engineers to do DevOps. Not realizing
[04:04] engineers to do DevOps. Not realizing that DevOps is kind of everyone's
[04:06] that DevOps is kind of everyone's
[04:06] that DevOps is kind of everyone's responsibility.
[04:09] responsibility.
[04:09] responsibility. Now with platform engineering, we kind
[04:11] Now with platform engineering, we kind
[04:11] Now with platform engineering, we kind of reverted back a little bit on that
[04:12] of reverted back a little bit on that
[04:12] of reverted back a little bit on that thinking as well because a lot of teams
[04:15] thinking as well because a lot of teams
[04:15] thinking as well because a lot of teams would um kind of build out kind of
[04:18] would um kind of build out kind of
[04:18] would um kind of build out kind of golden paths to develop and deploy
[04:21] golden paths to develop and deploy
[04:21] golden paths to develop and deploy products and and solutions. Um and
[04:23] products and and solutions. Um and
[04:23] products and and solutions. Um and they'd actually find that they'd be
[04:25] they'd actually find that they'd be
[04:25] they'd actually find that they'd be managing too much the kind of the
[04:27] managing too much the kind of the
[04:27] managing too much the kind of the cognitive overload, which is a strange
[04:29] cognitive overload, which is a strange
[04:29] cognitive overload, which is a strange term to talk about now because when we
[04:30] term to talk about now because when we
[04:30] term to talk about now because when we associate cognitive overload, we talk
[04:32] associate cognitive overload, we talk
[04:32] associate cognitive overload, we talk about, you know, agents running off and
[04:34] about, you know, agents running off and
[04:34] about, you know, agents running off and doing things and we're trying to keep
[04:35] doing things and we're trying to keep
[04:35] doing things and we're trying to keep track of what they're actually doing.
[04:37] track of what they're actually doing.
[04:37] track of what they're actually doing. Um, but cognitive overload in the
[04:38] Um, but cognitive overload in the
[04:38] Um, but cognitive overload in the context of kind of DevOps is like, okay,
[04:40] context of kind of DevOps is like, okay,
[04:40] context of kind of DevOps is like, okay, now I'm responsible not just for
[04:42] now I'm responsible not just for
[04:42] now I'm responsible not just for building the thing, but for testing it,
[04:44] building the thing, but for testing it,
[04:44] building the thing, but for testing it, making sure it's secure, making sure
[04:46] making sure it's secure, making sure
[04:46] making sure it's secure, making sure it's legally compliant, and I've got to
[04:48] it's legally compliant, and I've got to
[04:48] it's legally compliant, and I've got to know things, and I also have to automate
[04:50] know things, and I also have to automate
[04:50] know things, and I also have to automate those things that I need to know now in
[04:52] those things that I need to know now in
[04:52] those things that I need to know now in order to kind of do DevOps properly. So
[04:54] order to kind of do DevOps properly. So
[04:54] order to kind of do DevOps properly. So my kind of opinionated take on platform
[04:57] my kind of opinionated take on platform
[04:57] my kind of opinionated take on platform engineering um is that we're essentially
[05:01] engineering um is that we're essentially
[05:01] engineering um is that we're essentially doing or building sorry internal
[05:03] doing or building sorry internal
[05:03] doing or building sorry internal products or internal mechanisms and
[05:05] products or internal mechanisms and
[05:05] products or internal mechanisms and golden paths to reduce that cognitive
[05:07] golden paths to reduce that cognitive
[05:08] golden paths to reduce that cognitive overload for developers so developers
[05:10] overload for developers so developers
[05:10] overload for developers so developers can get back to doing what they do by
[05:11] can get back to doing what they do by
[05:12] can get back to doing what they do by delivering value by actually building
[05:14] delivering value by actually building
[05:14] delivering value by actually building innovation a bit innovative solutions
[05:16] innovation a bit innovative solutions
[05:16] innovation a bit innovative solutions and building things. Kelsey High Totower
[05:18] and building things. Kelsey High Totower
[05:18] and building things. Kelsey High Totower has got a really good um
[05:22] has got a really good um
[05:22] has got a really good um really good saying around this that
[05:23] really good saying around this that
[05:23] really good saying around this that platforms aren't just these magical
[05:25] platforms aren't just these magical
[05:25] platforms aren't just these magical APIs. I think the trap that we kind of
[05:28] APIs. I think the trap that we kind of
[05:28] APIs. I think the trap that we kind of brought with us with the DevOps kind of
[05:29] brought with us with the DevOps kind of
[05:30] brought with us with the DevOps kind of thinking that oh we need to go out and
[05:32] thinking that oh we need to go out and
[05:32] thinking that oh we need to go out and just build a platform or we've I'm going
[05:35] just build a platform or we've I'm going
[05:35] just build a platform or we've I'm going to you know buy or adopt a backstage
[05:38] to you know buy or adopt a backstage
[05:38] to you know buy or adopt a backstage something like that or build an internal
[05:40] something like that or build an internal
[05:40] something like that or build an internal developer portal where you know it's an
[05:42] developer portal where you know it's an
[05:42] developer portal where you know it's an actual product. natural thing and I've
[05:43] actual product. natural thing and I've
[05:43] actual product. natural thing and I've got platform engineering now and it's
[05:45] got platform engineering now and it's
[05:45] got platform engineering now and it's not necessarily that it's just basically
[05:47] not necessarily that it's just basically
[05:47] not necessarily that it's just basically agreements between human beings through
[05:49] agreements between human beings through
[05:50] agreements between human beings through APIs how we're actually going to do our
[05:52] APIs how we're actually going to do our
[05:52] APIs how we're actually going to do our work because if you buy a platform or if
[05:56] work because if you buy a platform or if
[05:56] work because if you buy a platform or if you kind of build a platform and you're
[05:57] you kind of build a platform and you're
[05:57] you kind of build a platform and you're forcing everyone into it, that's kind of
[06:00] forcing everyone into it, that's kind of
[06:00] forcing everyone into it, that's kind of defeating the point. No one's going to,
[06:02] defeating the point. No one's going to,
[06:02] defeating the point. No one's going to, you know, want to use or love a platform
[06:04] you know, want to use or love a platform
[06:04] you know, want to use or love a platform that they're forced to use. Um,
[06:06] that they're forced to use. Um,
[06:06] that they're forced to use. Um, essentially platform engineering is
[06:08] essentially platform engineering is
[06:08] essentially platform engineering is about making it the path of least
[06:10] about making it the path of least
[06:10] about making it the path of least resistance.
[06:12] resistance.
[06:12] resistance. And really quite simply, it's just about
[06:14] And really quite simply, it's just about
[06:14] And really quite simply, it's just about how we can make lives easier for
[06:15] how we can make lives easier for
[06:15] how we can make lives easier for developers. It's how we can help them to
[06:18] developers. It's how we can help them to
[06:18] developers. It's how we can help them to be self-sufficient. Now, a lot of us
[06:21] be self-sufficient. Now, a lot of us
[06:21] be self-sufficient. Now, a lot of us would say that kind of gets translated
[06:23] would say that kind of gets translated
[06:23] would say that kind of gets translated through automated pipelines, um,
[06:25] through automated pipelines, um,
[06:25] through automated pipelines, um, integration tests, security scanning,
[06:27] integration tests, security scanning,
[06:28] integration tests, security scanning, stuff that kind of just works. You kind
[06:29] stuff that kind of just works. You kind
[06:29] stuff that kind of just works. You kind of build it out and say you're building
[06:32] of build it out and say you're building
[06:32] of build it out and say you're building an application, you're deploying a
[06:33] an application, you're deploying a
[06:33] an application, you're deploying a binary somewhere and you want to make
[06:35] binary somewhere and you want to make
[06:35] binary somewhere and you want to make sure that your security teams are going
[06:36] sure that your security teams are going
[06:36] sure that your security teams are going to put sign off on it. Uh, so you have
[06:39] to put sign off on it. Uh, so you have
[06:39] to put sign off on it. Uh, so you have some steps in there. Maybe you're
[06:40] some steps in there. Maybe you're
[06:40] some steps in there. Maybe you're scanning the container image that's um
[06:42] scanning the container image that's um
[06:42] scanning the container image that's um being generated or you're doing some
[06:43] being generated or you're doing some
[06:43] being generated or you're doing some static code analysis and you want to
[06:45] static code analysis and you want to
[06:45] static code analysis and you want to make that as easy as possible
[06:48] make that as easy as possible
[06:48] make that as easy as possible and then it's kind of standardizing that
[06:50] and then it's kind of standardizing that
[06:50] and then it's kind of standardizing that across teams and organizations to make
[06:53] across teams and organizations to make
[06:53] across teams and organizations to make that adoption or make that a bit easier
[06:55] that adoption or make that a bit easier
[06:55] that adoption or make that a bit easier for for other teams so they're not
[06:56] for for other teams so they're not
[06:56] for for other teams so they're not writing stuff from scratch. Um,
[07:01] writing stuff from scratch. Um,
[07:01] writing stuff from scratch. Um, so how many of just to use that as an
[07:03] so how many of just to use that as an
[07:03] so how many of just to use that as an example, how many of you have actually
[07:05] example, how many of you have actually
[07:05] example, how many of you have actually kind of working along with a working
[07:07] kind of working along with a working
[07:07] kind of working along with a working with a security team within your
[07:08] with a security team within your
[07:08] with a security team within your organization like after you've built
[07:10] organization like after you've built
[07:10] organization like after you've built something, you've kind of, you know,
[07:12] something, you've kind of, you know,
[07:12] something, you've kind of, you know, asked for permission to deploy it. It's
[07:14] asked for permission to deploy it. It's
[07:14] asked for permission to deploy it. It's it's a bit tedious, right? Where you
[07:16] it's a bit tedious, right? Where you
[07:16] it's a bit tedious, right? Where you know they and have you ever been
[07:19] know they and have you ever been
[07:19] know they and have you ever been rejected or has it ever been rejected
[07:22] rejected or has it ever been rejected
[07:22] rejected or has it ever been rejected based on like, oh, you haven't used this
[07:23] based on like, oh, you haven't used this
[07:23] based on like, oh, you haven't used this particular tool or you haven't done it
[07:26] particular tool or you haven't done it
[07:26] particular tool or you haven't done it in this particular way? that has
[07:28] in this particular way? that has
[07:28] in this particular way? that has happened to me. It's good to see that
[07:29] happened to me. It's good to see that
[07:29] happened to me. It's good to see that there aren't many nods in the audience.
[07:32] there aren't many nods in the audience.
[07:32] there aren't many nods in the audience. Um, having gone through that pain
[07:34] Um, having gone through that pain
[07:34] Um, having gone through that pain myself, um, essentially the idea of an
[07:37] myself, um, essentially the idea of an
[07:37] myself, um, essentially the idea of an internal developer platform isn't like a
[07:38] internal developer platform isn't like a
[07:38] internal developer platform isn't like a shiny new portal somewhere, you know,
[07:41] shiny new portal somewhere, you know,
[07:41] shiny new portal somewhere, you know, that you've just bought. It's kind of
[07:43] that you've just bought. It's kind of
[07:43] that you've just bought. It's kind of adopting um, kind of an automated way of
[07:46] adopting um, kind of an automated way of
[07:46] adopting um, kind of an automated way of doing things to make life easier for
[07:48] doing things to make life easier for
[07:48] doing things to make life easier for you. Also another question, how uh many
[07:51] you. Also another question, how uh many
[07:51] you. Also another question, how uh many of you have been in teams where your
[07:52] of you have been in teams where your
[07:52] of you have been in teams where your team was like the first team to deploy
[07:54] team was like the first team to deploy
[07:54] team was like the first team to deploy applications to the cloud
[07:57] applications to the cloud
[07:57] applications to the cloud one or two. Was it was it painful for
[07:59] one or two. Was it was it painful for
[07:59] one or two. Was it was it painful for the first time like you know writing
[08:01] the first time like you know writing
[08:01] the first time like you know writing infrastructure as code templates and
[08:03] infrastructure as code templates and
[08:03] infrastructure as code templates and just basically figuring out how it all
[08:05] just basically figuring out how it all
[08:05] just basically figuring out how it all works? I've been involved in teams like
[08:06] works? I've been involved in teams like
[08:06] works? I've been involved in teams like that particularly in a I used to work
[08:08] that particularly in a I used to work
[08:08] that particularly in a I used to work for a bank and trying to do that in
[08:10] for a bank and trying to do that in
[08:10] for a bank and trying to do that in highly regulated environments as well
[08:12] highly regulated environments as well
[08:12] highly regulated environments as well where you're working with different
[08:13] where you're working with different
[08:13] where you're working with different stakeholders that can be a bit of a a
[08:16] stakeholders that can be a bit of a a
[08:16] stakeholders that can be a bit of a a bit of a mission as well. So really some
[08:19] bit of a mission as well. So really some
[08:19] bit of a mission as well. So really some forms of platform engineering can really
[08:20] forms of platform engineering can really
[08:20] forms of platform engineering can really be simple as just kind of like pipeline
[08:22] be simple as just kind of like pipeline
[08:22] be simple as just kind of like pipeline templates or infrastructure as code
[08:24] templates or infrastructure as code
[08:24] templates or infrastructure as code modules and there's more nuances to that
[08:26] modules and there's more nuances to that
[08:26] modules and there's more nuances to that because particularly with something like
[08:27] because particularly with something like
[08:27] because particularly with something like Terraform you have Terraform registries
[08:29] Terraform you have Terraform registries
[08:29] Terraform you have Terraform registries and there's also bicep registries but
[08:31] and there's also bicep registries but
[08:31] and there's also bicep registries but essentially that could be as simple as
[08:33] essentially that could be as simple as
[08:33] essentially that could be as simple as what platform engineering actually is.
[08:37] what platform engineering actually is.
[08:37] what platform engineering actually is. Then AI came into the picture. The
[08:40] Then AI came into the picture. The
[08:40] Then AI came into the picture. The developer experience has transformed
[08:42] developer experience has transformed
[08:42] developer experience has transformed incredibly um since 2023 uh 2022 even.
[08:47] incredibly um since 2023 uh 2022 even.
[08:47] incredibly um since 2023 uh 2022 even. Uh Richard was talking about in his
[08:49] Uh Richard was talking about in his
[08:49] Uh Richard was talking about in his keynote yesterday. Um anyone recognize
[08:52] keynote yesterday. Um anyone recognize
[08:52] keynote yesterday. Um anyone recognize any of these?
[08:54] any of these?
[08:54] any of these? Everyone's nodding. Yeah. [laughter]
[08:57] Everyone's nodding. Yeah. [laughter]
[08:57] Everyone's nodding. Yeah. [laughter] Yeah. Um coding assistants are are
[09:00] Yeah. Um coding assistants are are
[09:00] Yeah. Um coding assistants are are great. I'm here to tell you that. I'm
[09:02] great. I'm here to tell you that. I'm
[09:02] great. I'm here to tell you that. I'm not here arguing that coding assistants
[09:04] not here arguing that coding assistants
[09:04] not here arguing that coding assistants are bad. I'm not saying that because,
[09:05] are bad. I'm not saying that because,
[09:05] are bad. I'm not saying that because, you know, I'm working for Microsoft and
[09:07] you know, I'm working for Microsoft and
[09:07] you know, I'm working for Microsoft and I use coding assistants every day. Um
[09:09] I use coding assistants every day. Um
[09:10] I use coding assistants every day. Um but they have transformed the developer
[09:11] but they have transformed the developer
[09:11] but they have transformed the developer experience.
[09:16] Now just to take off my Microsoft hat at
[09:16] Now just to take off my Microsoft hat at the moment we kind of started off um
[09:19] the moment we kind of started off um
[09:19] the moment we kind of started off um basically selling the idea that if
[09:20] basically selling the idea that if
[09:20] basically selling the idea that if you're using copilot or if you're using
[09:22] you're using copilot or if you're using
[09:22] you're using copilot or if you're using CL claude or codeex or whatever that
[09:25] CL claude or codeex or whatever that
[09:25] CL claude or codeex or whatever that you'll become this 10x engineer and you
[09:27] you'll become this 10x engineer and you
[09:27] you'll become this 10x engineer and you can deliver features super fast. So
[09:31] can deliver features super fast. So
[09:32] can deliver features super fast. So oh my clicker died and then it came back
[09:35] oh my clicker died and then it came back
[09:35] oh my clicker died and then it came back to life. So yeah AI is going to write
[09:36] to life. So yeah AI is going to write
[09:36] to life. So yeah AI is going to write the code for us. We're going to ship
[09:38] the code for us. We're going to ship
[09:38] the code for us. We're going to ship features overnight. It's going to not
[09:41] features overnight. It's going to not
[09:41] features overnight. It's going to not it's not going to take us weeks to
[09:42] it's not going to take us weeks to
[09:42] it's not going to take us weeks to develop something and and ship it to
[09:44] develop something and and ship it to
[09:44] develop something and and ship it to customers. This is going to be simple
[09:45] customers. This is going to be simple
[09:46] customers. This is going to be simple for us.
[09:47] for us.
[09:48] for us. Whereas the reality is before even
[09:50] Whereas the reality is before even
[09:50] Whereas the reality is before even before AI we you know documentation
[09:53] before AI we you know documentation
[09:53] before AI we you know documentation wasn't something I think as an industry
[09:55] wasn't something I think as an industry
[09:55] wasn't something I think as an industry we did too well. How many of you
[09:59] we did too well. How many of you
[09:59] we did too well. How many of you be honest didn't document your stuff too
[10:01] be honest didn't document your stuff too
[10:01] be honest didn't document your stuff too well? It's all right. We're in a safe
[10:03] well? It's all right. We're in a safe
[10:03] well? It's all right. We're in a safe space. They can film me. You know you
[10:04] space. They can film me. You know you
[10:04] space. They can film me. You know you everyone everyone had their hands up.
[10:06] everyone everyone had their hands up.
[10:06] everyone everyone had their hands up. No.
[10:07] No.
[10:07] No. there was inconsistent tooling amongst
[10:09] there was inconsistent tooling amongst
[10:09] there was inconsistent tooling amongst teams as well. Um, and with AI a lot a
[10:13] teams as well. Um, and with AI a lot a
[10:13] teams as well. Um, and with AI a lot a lot of kind of the early kind of vibe
[10:15] lot of kind of the early kind of vibe
[10:15] lot of kind of the early kind of vibe coding um patterns we saw was just kind
[10:18] coding um patterns we saw was just kind
[10:18] coding um patterns we saw was just kind of yoloing it. I know C-Pilot has got a
[10:20] of yoloing it. I know C-Pilot has got a
[10:20] of yoloing it. I know C-Pilot has got a yolo mode which is I've I've never used
[10:22] yolo mode which is I've I've never used
[10:22] yolo mode which is I've I've never used it. Um, honestly cuz that seems to me
[10:25] it. Um, honestly cuz that seems to me
[10:25] it. Um, honestly cuz that seems to me like you're just asking for trouble. Um,
[10:30] like you're just asking for trouble. Um,
[10:30] like you're just asking for trouble. Um, my clicker is doing something funny
[10:32] my clicker is doing something funny
[10:32] my clicker is doing something funny today but that's okay. I'm by the
[10:33] today but that's okay. I'm by the
[10:33] today but that's okay. I'm by the keyboard. So yeah, just chat GBT dude.
[10:36] keyboard. So yeah, just chat GBT dude.
[10:36] keyboard. So yeah, just chat GBT dude. I'm a big South Park fan. Now the data
[10:39] I'm a big South Park fan. Now the data
[10:39] I'm a big South Park fan. Now the data we kind of moved on a little bit from
[10:41] we kind of moved on a little bit from
[10:41] we kind of moved on a little bit from this data, but I have included it. Um,
[10:43] this data, but I have included it. Um,
[10:43] this data, but I have included it. Um, basically the idea is from the vendor
[10:45] basically the idea is from the vendor
[10:45] basically the idea is from the vendor perspective, there is a marketing arm
[10:47] perspective, there is a marketing arm
[10:47] perspective, there is a marketing arm saying just adopt us and you'll be
[10:49] saying just adopt us and you'll be
[10:49] saying just adopt us and you'll be faster, your engineers will be more
[10:50] faster, your engineers will be more
[10:50] faster, your engineers will be more productive and that came from a really
[10:53] productive and that came from a really
[10:53] productive and that came from a really narrow 2003 study. Um
[10:56] narrow 2003 study. Um
[10:56] narrow 2003 study. Um and more as time has gone by uh there
[11:00] and more as time has gone by uh there
[11:00] and more as time has gone by uh there have been more studies where senior
[11:01] have been more studies where senior
[11:01] have been more studies where senior developers particularly from Microsoft
[11:03] developers particularly from Microsoft
[11:03] developers particularly from Microsoft and Accenture were asked you know has
[11:05] and Accenture were asked you know has
[11:05] and Accenture were asked you know has this increased your productivity and
[11:07] this increased your productivity and
[11:07] this increased your productivity and you'll see those kind of metrics will
[11:09] you'll see those kind of metrics will
[11:09] you'll see those kind of metrics will say yes we've raised more PRs we've
[11:11] say yes we've raised more PRs we've
[11:11] say yes we've raised more PRs we've committed more code and I think the kind
[11:14] committed more code and I think the kind
[11:14] committed more code and I think the kind of looking at it as a volume or a
[11:16] of looking at it as a volume or a
[11:16] of looking at it as a volume or a percentage of stuff that we've pushed
[11:18] percentage of stuff that we've pushed
[11:18] percentage of stuff that we've pushed and committed doesn't necessarily mean
[11:20] and committed doesn't necessarily mean
[11:20] and committed doesn't necessarily mean that we're more productive yeah we're
[11:22] that we're more productive yeah we're
[11:22] that we're more productive yeah we're producing more but we're not producing
[11:23] producing more but we're not producing
[11:23] producing more but we're not producing more in value Right. Um, and the studies
[11:27] more in value Right. Um, and the studies
[11:27] more in value Right. Um, and the studies actually showed that. So, senior
[11:28] actually showed that. So, senior
[11:28] actually showed that. So, senior developers kind of said there's no
[11:30] developers kind of said there's no
[11:30] developers kind of said there's no statistically significant gain that
[11:32] statistically significant gain that
[11:32] statistically significant gain that we're actually getting. We're pushing
[11:33] we're actually getting. We're pushing
[11:33] we're actually getting. We're pushing more. Yeah. But we're not being more
[11:35] more. Yeah. But we're not being more
[11:35] more. Yeah. But we're not being more we're not actually being more
[11:37] we're not actually being more
[11:37] we're not actually being more productive.
[11:39] productive.
[11:39] productive. And in the open-source world, there was
[11:41] And in the open-source world, there was
[11:41] And in the open-source world, there was a study where there was a, you know,
[11:43] a study where there was a, you know,
[11:43] a study where there was a, you know, more code was being produced. There was
[11:45] more code was being produced. There was
[11:45] more code was being produced. There was there was faster being produced, but
[11:48] there was faster being produced, but
[11:48] there was faster being produced, but reviewing it was taking a long time. I
[11:51] reviewing it was taking a long time. I
[11:51] reviewing it was taking a long time. I think open source has kind of led the
[11:54] think open source has kind of led the
[11:54] think open source has kind of led the way of in skepticism towards AI for a
[11:57] way of in skepticism towards AI for a
[11:57] way of in skepticism towards AI for a good reason. Um I'm not a a maintainer
[12:00] good reason. Um I'm not a a maintainer
[12:00] good reason. Um I'm not a a maintainer for a large project. Have we got any
[12:01] for a large project. Have we got any
[12:01] for a large project. Have we got any maintainers in the room of large
[12:03] maintainers in the room of large
[12:03] maintainers in the room of large projects?
[12:05] projects?
[12:05] projects? No. Okay. Well, I'll empathize empathize
[12:08] No. Okay. Well, I'll empathize empathize
[12:08] No. Okay. Well, I'll empathize empathize based on an assumption um that it must
[12:10] based on an assumption um that it must
[12:10] based on an assumption um that it must be very taxing for you've got a large
[12:13] be very taxing for you've got a large
[12:13] be very taxing for you've got a large project and lots of people are trying to
[12:14] project and lots of people are trying to
[12:14] project and lots of people are trying to commit and trying to you know contribute
[12:16] commit and trying to you know contribute
[12:16] commit and trying to you know contribute which is a good thing but trying to sort
[12:19] which is a good thing but trying to sort
[12:19] which is a good thing but trying to sort out the AI slot from the meaningful
[12:20] out the AI slot from the meaningful
[12:20] out the AI slot from the meaningful contributions will slow you down whether
[12:23] contributions will slow you down whether
[12:23] contributions will slow you down whether you're in an enterprise or you're
[12:25] you're in an enterprise or you're
[12:25] you're in an enterprise or you're working u or you're working on an open
[12:26] working u or you're working on an open
[12:26] working u or you're working on an open source project. Now I've included a
[12:30] source project. Now I've included a
[12:30] source project. Now I've included a study this that was done kind of
[12:31] study this that was done kind of
[12:31] study this that was done kind of preclude MEOS um about how
[12:34] preclude MEOS um about how
[12:34] preclude MEOS um about how vulnerabilities were being introduced.
[12:37] vulnerabilities were being introduced.
[12:37] vulnerabilities were being introduced. Meos has kind of changed that
[12:38] Meos has kind of changed that
[12:38] Meos has kind of changed that perspective. Um Richard had a slide
[12:41] perspective. Um Richard had a slide
[12:41] perspective. Um Richard had a slide yesterday uh showing how Firefox have
[12:43] yesterday uh showing how Firefox have
[12:43] yesterday uh showing how Firefox have kind of resolved some of their security
[12:44] kind of resolved some of their security
[12:44] kind of resolved some of their security vulnerabilities. That was I believe
[12:46] vulnerabilities. That was I believe
[12:46] vulnerabilities. That was I believe using Claude Mos which is apparently
[12:48] using Claude Mos which is apparently
[12:48] using Claude Mos which is apparently quite a powerful model. I haven't used
[12:50] quite a powerful model. I haven't used
[12:50] quite a powerful model. I haven't used it. Um, but I think we're still at a
[12:53] it. Um, but I think we're still at a
[12:53] it. Um, but I think we're still at a stage where vibe coders and yoloers are
[12:56] stage where vibe coders and yoloers are
[12:56] stage where vibe coders and yoloers are are going to intro in introduce security
[12:58] are going to intro in introduce security
[12:58] are going to intro in introduce security vulnerabilities into our codebase if
[13:01] vulnerabilities into our codebase if
[13:01] vulnerabilities into our codebase if we're not careful.
[13:04] we're not careful.
[13:04] we're not careful. So, let's talk about vibe coders. And
[13:06] So, let's talk about vibe coders. And
[13:06] So, let's talk about vibe coders. And again, I'm not Okay, this one I am kind
[13:09] again, I'm not Okay, this one I am kind
[13:09] again, I'm not Okay, this one I am kind of laughing at, but I'm trying not to be
[13:11] of laughing at, but I'm trying not to be
[13:11] of laughing at, but I'm trying not to be mean, but this is where we kind of
[13:12] mean, but this is where we kind of
[13:12] mean, but this is where we kind of started out when we first kind of, you
[13:15] started out when we first kind of, you
[13:15] started out when we first kind of, you know, vibe coding um came apparent. So
[13:18] know, vibe coding um came apparent. So
[13:18] know, vibe coding um came apparent. So this guy, he built his entire startup
[13:21] this guy, he built his entire startup
[13:21] this guy, he built his entire startup using cursor with zero handwritten code
[13:24] using cursor with zero handwritten code
[13:24] using cursor with zero handwritten code and you know he went on on X or Twitter
[13:27] and you know he went on on X or Twitter
[13:27] and you know he went on on X or Twitter as you do and decided to share his
[13:29] as you do and decided to share his
[13:29] as you do and decided to share his success in probably not the most humble
[13:31] success in probably not the most humble
[13:31] success in probably not the most humble way. Um this to me is a very typical
[13:35] way. Um this to me is a very typical
[13:35] way. Um this to me is a very typical like
[13:36] like
[13:36] like alpha bro who spends more time in
[13:38] alpha bro who spends more time in
[13:38] alpha bro who spends more time in finance than in the real world but
[13:40] finance than in the real world but
[13:40] finance than in the real world but basically saying my SAS was built with
[13:43] basically saying my SAS was built with
[13:43] basically saying my SAS was built with uh zero handwritten code. AI is no
[13:45] uh zero handwritten code. AI is no
[13:45] uh zero handwritten code. AI is no longer assistant. It's also the builder.
[13:47] longer assistant. It's also the builder.
[13:47] longer assistant. It's also the builder. And then this line now you can continue
[13:49] And then this line now you can continue
[13:49] And then this line now you can continue to whine about it or start building. Um
[13:52] to whine about it or start building. Um
[13:52] to whine about it or start building. Um which just a small insight into the
[13:54] which just a small insight into the
[13:54] which just a small insight into the psyche of of his of this man.
[13:58] psyche of of his of this man.
[13:58] psyche of of his of this man. So the attacks happened.
[14:00] So the attacks happened.
[14:00] So the attacks happened. So with within days of launching his SAS
[14:03] So with within days of launching his SAS
[14:03] So with within days of launching his SAS um he complained desperately online. So
[14:06] um he complained desperately online. So
[14:06] um he complained desperately online. So guys I'm under attack. Random things are
[14:08] guys I'm under attack. Random things are
[14:08] guys I'm under attack. Random things are happening and maxed out usage on API
[14:10] happening and maxed out usage on API
[14:10] happening and maxed out usage on API keys people bypassing the subscription
[14:13] keys people bypassing the subscription
[14:13] keys people bypassing the subscription and creating random stuff in the
[14:14] and creating random stuff in the
[14:14] and creating random stuff in the database. So the problems were
[14:16] database. So the problems were
[14:16] database. So the problems were everywhere and they're embarrassingly
[14:17] everywhere and they're embarrassingly
[14:17] everywhere and they're embarrassingly basic as well. So users could bypass the
[14:20] basic as well. So users could bypass the
[14:20] basic as well. So users could bypass the payw wall because there wasn't a real
[14:21] payw wall because there wasn't a real
[14:21] payw wall because there wasn't a real authentication system. The uh cursor
[14:24] authentication system. The uh cursor
[14:24] authentication system. The uh cursor just created a facade of it. Attackers
[14:26] just created a facade of it. Attackers
[14:26] just created a facade of it. Attackers were spamming the API uh because there
[14:28] were spamming the API uh because there
[14:28] were spamming the API uh because there was no rate limiting. Who hasn't done
[14:30] was no rate limiting. Who hasn't done
[14:30] was no rate limiting. Who hasn't done that? Uh and the database was filling up
[14:32] that? Uh and the database was filling up
[14:32] that? Uh and the database was filling up with garbage because there was no input
[14:34] with garbage because there was no input
[14:34] with garbage because there was no input validation. So these were these aren't
[14:36] validation. So these were these aren't
[14:36] validation. So these were these aren't sophisticated hacks. These are just
[14:37] sophisticated hacks. These are just
[14:37] sophisticated hacks. These are just basic textbook security failures that
[14:40] basic textbook security failures that
[14:40] basic textbook security failures that any first year computer science student
[14:42] any first year computer science student
[14:42] any first year computer science student or any you know anyone who's educated in
[14:44] or any you know anyone who's educated in
[14:44] or any you know anyone who's educated in computer science or or or programming
[14:46] computer science or or or programming
[14:46] computer science or or or programming would know how to avoid. But the AI had
[14:49] would know how to avoid. But the AI had
[14:49] would know how to avoid. But the AI had curs generated this code that looked
[14:51] curs generated this code that looked
[14:51] curs generated this code that looked functional while completely ignoring uh
[14:53] functional while completely ignoring uh
[14:53] functional while completely ignoring uh the fundamental security principles.
[14:56] the fundamental security principles.
[14:56] the fundamental security principles. So he eventually shut down the app
[14:58] So he eventually shut down the app
[14:58] So he eventually shut down the app permanently um and said you know for now
[15:02] permanently um and said you know for now
[15:02] permanently um and said you know for now I'm just going to stop sharing what I do
[15:03] I'm just going to stop sharing what I do
[15:03] I'm just going to stop sharing what I do publicly on X. There are just some weird
[15:05] publicly on X. There are just some weird
[15:05] publicly on X. There are just some weird people out there. And that's fair
[15:06] people out there. And that's fair
[15:06] people out there. And that's fair because, you know, he just posted
[15:08] because, you know, he just posted
[15:08] because, you know, he just posted something or put something on the public
[15:09] something or put something on the public
[15:09] something or put something on the public internet. How did he know it was going
[15:11] internet. How did he know it was going
[15:11] internet. How did he know it was going to get hacked by people who love a
[15:13] to get hacked by people who love a
[15:13] to get hacked by people who love a challenge?
[15:15] challenge?
[15:15] challenge? Now, again, I'm making light of it a
[15:17] Now, again, I'm making light of it a
[15:17] Now, again, I'm making light of it a little bit, but there's a reality there.
[15:18] little bit, but there's a reality there.
[15:18] little bit, but there's a reality there. If you're running your entire business
[15:20] If you're running your entire business
[15:20] If you're running your entire business on code that you don't understand,
[15:22] on code that you don't understand,
[15:22] on code that you don't understand, you're not really an entrepreneur.
[15:23] you're not really an entrepreneur.
[15:23] you're not really an entrepreneur. You're just kind of hoping that nothing
[15:25] You're just kind of hoping that nothing
[15:25] You're just kind of hoping that nothing breaks. And I've yet to meet anyone who
[15:27] breaks. And I've yet to meet anyone who
[15:27] breaks. And I've yet to meet anyone who thinks that hope is a strategy.
[15:35] Now in the open source world um NX was a
[15:35] Now in the open source world um NX was a popular build is a popular build tool
[15:37] popular build is a popular build tool
[15:37] popular build is a popular build tool that's used by thousands of developers
[15:38] that's used by thousands of developers
[15:38] that's used by thousands of developers worldwide. Who uses NX here? A couple of
[15:42] worldwide. Who uses NX here? A couple of
[15:42] worldwide. Who uses NX here? A couple of So did you see this? This was a PR that
[15:44] So did you see this? This was a PR that
[15:44] So did you see this? This was a PR that um it was an AI generated PR um used to
[15:47] um it was an AI generated PR um used to
[15:48] um it was an AI generated PR um used to speed up development and some projects
[15:51] speed up development and some projects
[15:51] speed up development and some projects have taken on um yes we are going to
[15:54] have taken on um yes we are going to
[15:54] have taken on um yes we are going to accept AI AI generated PRs that's fine.
[15:57] accept AI AI generated PRs that's fine.
[15:57] accept AI AI generated PRs that's fine. Some have been um a little bit more
[15:58] Some have been um a little bit more
[15:58] Some have been um a little bit more explicit and said no, we're going to
[16:00] explicit and said no, we're going to
[16:00] explicit and said no, we're going to reject this. But these guys did and it
[16:03] reject this. But these guys did and it
[16:03] reject this. But these guys did and it created a subtle flaw. So essentially it
[16:06] created a subtle flaw. So essentially it
[16:06] created a subtle flaw. So essentially it used the pull request titles directly in
[16:08] used the pull request titles directly in
[16:08] used the pull request titles directly in shell commands without sanitizing the
[16:10] shell commands without sanitizing the
[16:10] shell commands without sanitizing the input.
[16:11] input.
[16:11] input. So this um created uh what's called a
[16:15] So this um created uh what's called a
[16:15] So this um created uh what's called a common uh a command sorry injection
[16:17] common uh a command sorry injection
[16:17] common uh a command sorry injection vulnerability. So essentially creates a
[16:18] vulnerability. So essentially creates a
[16:18] vulnerability. So essentially creates a back door that anyone could exploit. An
[16:21] back door that anyone could exploit. An
[16:21] back door that anyone could exploit. An attacker discovered this vulnerability
[16:23] attacker discovered this vulnerability
[16:23] attacker discovered this vulnerability in an older branch, created a malicious
[16:25] in an older branch, created a malicious
[16:25] in an older branch, created a malicious pull request with code that was hidden
[16:27] pull request with code that was hidden
[16:27] pull request with code that was hidden in the title. So when the automated
[16:29] in the title. So when the automated
[16:29] in the title. So when the automated systems processed this, they actually
[16:31] systems processed this, they actually
[16:31] systems processed this, they actually executed the attacker's commands and
[16:32] executed the attacker's commands and
[16:32] executed the attacker's commands and then leaked the NX publishing
[16:34] then leaked the NX publishing
[16:34] then leaked the NX publishing credentials. Then with those
[16:35] credentials. Then with those
[16:35] credentials. Then with those credentials, the attacker pushed a
[16:37] credentials, the attacker pushed a
[16:37] credentials, the attacker pushed a compromised version of NX itself. And
[16:39] compromised version of NX itself. And
[16:40] compromised version of NX itself. And that affected uh that update spread
[16:42] that affected uh that update spread
[16:42] that affected uh that update spread malware to users machines which tricked
[16:44] malware to users machines which tricked
[16:44] malware to users machines which tricked local AI coding assistants to steal
[16:47] local AI coding assistants to steal
[16:47] local AI coding assistants to steal GitHub tokens, API keys, and even
[16:49] GitHub tokens, API keys, and even
[16:49] GitHub tokens, API keys, and even cryptocurrency wallets from around one
[16:51] cryptocurrency wallets from around one
[16:51] cryptocurrency wallets from around one and a half thousand developers.
[16:54] and a half thousand developers.
[16:54] and a half thousand developers. And then finally, this is this is um
[16:57] And then finally, this is this is um
[16:57] And then finally, this is this is um this is a hell of an example. So Jason
[16:59] this is a hell of an example. So Jason
[16:59] this is a hell of an example. So Jason Lmin, he's the founder of uh a SAS
[17:02] Lmin, he's the founder of uh a SAS
[17:02] Lmin, he's the founder of uh a SAS community called Sastura. That's a
[17:04] community called Sastura. That's a
[17:04] community called Sastura. That's a that's a great name. Uh he decided to
[17:06] that's a great name. Uh he decided to
[17:06] that's a great name. Uh he decided to experiment with Replet's AI agent to
[17:09] experiment with Replet's AI agent to
[17:09] experiment with Replet's AI agent to build a prototype. So for nine days,
[17:11] build a prototype. So for nine days,
[17:11] build a prototype. So for nine days, everything was working brilliantly. You
[17:12] everything was working brilliantly. You
[17:12] everything was working brilliantly. You know that kind of like magic aha moment
[17:14] know that kind of like magic aha moment
[17:14] know that kind of like magic aha moment when you're working with technology and
[17:16] when you're working with technology and
[17:16] when you're working with technology and things are just kind of working and you
[17:18] things are just kind of working and you
[17:18] things are just kind of working and you know he was he was experiencing that. So
[17:21] know he was he was experiencing that. So
[17:21] know he was he was experiencing that. So the AI generated code. It handled
[17:22] the AI generated code. It handled
[17:22] the AI generated code. It handled complex logic and it built what he
[17:24] complex logic and it built what he
[17:24] complex logic and it built what he thought was a quite a sophisticated
[17:26] thought was a quite a sophisticated
[17:26] thought was a quite a sophisticated application.
[17:27] application.
[17:28] application. He was so impressed that he decided to
[17:29] He was so impressed that he decided to
[17:29] He was so impressed that he decided to put his credit card down and spent
[17:31] put his credit card down and spent
[17:31] put his credit card down and spent around or spent over sorry $600 in
[17:34] around or spent over sorry $600 in
[17:34] around or spent over sorry $600 in additional charges beyond the monthly
[17:36] additional charges beyond the monthly
[17:36] additional charges beyond the monthly plan. That's when disaster struck. So on
[17:40] plan. That's when disaster struck. So on
[17:40] plan. That's when disaster struck. So on day eight, despite explicit instructions
[17:43] day eight, despite explicit instructions
[17:43] day eight, despite explicit instructions to um do a code freeze and make no
[17:46] to um do a code freeze and make no
[17:46] to um do a code freeze and make no changes, the agent decided that the
[17:48] changes, the agent decided that the
[17:48] changes, the agent decided that the database just needed a bit of a cleanup.
[17:51] database just needed a bit of a cleanup.
[17:51] database just needed a bit of a cleanup. Within minutes, it deleted everything.
[17:53] Within minutes, it deleted everything.
[17:53] Within minutes, it deleted everything. So I will um um share the numbers. So
[17:56] So I will um um share the numbers. So
[17:56] So I will um um share the numbers. So 1,26 executive records, 1,196
[18:00] 1,26 executive records, 1,196
[18:00] 1,26 executive records, 1,196 companies and months of authentic data
[18:02] companies and months of authentic data
[18:02] companies and months of authentic data which represented the core of their
[18:04] which represented the core of their
[18:04] which represented the core of their business um and a community platform.
[18:08] business um and a community platform.
[18:08] business um and a community platform. But that's when it got a little bit more
[18:09] But that's when it got a little bit more
[18:09] But that's when it got a little bit more disturbing. So when Lenin actually
[18:11] disturbing. So when Lenin actually
[18:11] disturbing. So when Lenin actually discovered this, the AI initially lied.
[18:14] discovered this, the AI initially lied.
[18:14] discovered this, the AI initially lied. So it claimed that it destroyed all
[18:16] So it claimed that it destroyed all
[18:16] So it claimed that it destroyed all database versions and that recovery was
[18:18] database versions and that recovery was
[18:18] database versions and that recovery was impossible, which is exactly what you
[18:20] impossible, which is exactly what you
[18:20] impossible, which is exactly what you want to hear.
[18:21] want to hear.
[18:21] want to hear. Later it confessed to a catastrophic
[18:23] Later it confessed to a catastrophic
[18:24] Later it confessed to a catastrophic failure and it gave itself a rating
[18:26] failure and it gave itself a rating
[18:26] failure and it gave itself a rating which I think is the weirdest part of
[18:27] which I think is the weirdest part of
[18:27] which I think is the weirdest part of this story. It rated itself 95 out of
[18:30] this story. It rated itself 95 out of
[18:30] this story. It rated itself 95 out of 100.
[18:32] 100.
[18:32] 100. I don't know what self-rating mechanisms
[18:33] I don't know what self-rating mechanisms
[18:34] I don't know what self-rating mechanisms you guys use to uh rate your own
[18:35] you guys use to uh rate your own
[18:36] you guys use to uh rate your own performance. 95 out of 100 is a bit of a
[18:38] performance. 95 out of 100 is a bit of a
[18:38] performance. 95 out of 100 is a bit of a weird one. Um but most shocking of all
[18:41] weird one. Um but most shocking of all
[18:41] weird one. Um but most shocking of all uh the AI tried to cover up its mistake
[18:43] uh the AI tried to cover up its mistake
[18:43] uh the AI tried to cover up its mistake by generating 4,000 fake database
[18:46] by generating 4,000 fake database
[18:46] by generating 4,000 fake database records with fictional people and
[18:48] records with fictional people and
[18:48] records with fictional people and company. So essentially gaslighting him
[18:50] company. So essentially gaslighting him
[18:50] company. So essentially gaslighting him about the changes that he about the
[18:52] about the changes that he about the
[18:52] about the changes that he about the extent of the damage. So naturally he
[18:55] extent of the damage. So naturally he
[18:55] extent of the damage. So naturally he went on Twitter and said I will never
[18:56] went on Twitter and said I will never
[18:56] went on Twitter and said I will never trust this again. He personally
[18:58] trust this again. He personally
[18:58] trust this again. He personally apologized implemented new safeguards.
[19:01] apologized implemented new safeguards.
[19:01] apologized implemented new safeguards. But I think the lesson is quite clear.
[19:03] But I think the lesson is quite clear.
[19:03] But I think the lesson is quite clear. These things left rampant uh can make
[19:07] These things left rampant uh can make
[19:07] These things left rampant uh can make irreversible decisions about production
[19:09] irreversible decisions about production
[19:09] irreversible decisions about production systems without actually understanding
[19:10] systems without actually understanding
[19:10] systems without actually understanding the consequences.
[19:16] So how do we kind of solve this? There
[19:16] So how do we kind of solve this? There is
[19:17] is
[19:17] is a phrase in my team that that we use to
[19:20] a phrase in my team that that we use to
[19:20] a phrase in my team that that we use to kind of counteract the vibe coding
[19:22] kind of counteract the vibe coding
[19:22] kind of counteract the vibe coding movement. The idea of oh, we're just
[19:24] movement. The idea of oh, we're just
[19:24] movement. The idea of oh, we're just going to let agents do stuff for us and
[19:26] going to let agents do stuff for us and
[19:26] going to let agents do stuff for us and we're just going to trust it. It's a
[19:28] we're just going to trust it. It's a
[19:28] we're just going to trust it. It's a cool name I think. Uh hyper velocity
[19:31] cool name I think. Uh hyper velocity
[19:31] cool name I think. Uh hyper velocity engineering and I will explain that a
[19:33] engineering and I will explain that a
[19:33] engineering and I will explain that a little bit more.
[19:35] little bit more.
[19:35] little bit more. So this is a quote uh by a colleague of
[19:39] So this is a quote uh by a colleague of
[19:39] So this is a quote uh by a colleague of mine who's based in Japan and
[19:41] mine who's based in Japan and
[19:41] mine who's based in Japan and essentially the distinction between
[19:43] essentially the distinction between
[19:43] essentially the distinction between hypers speed and hyper velocity is quite
[19:46] hypers speed and hyper velocity is quite
[19:46] hypers speed and hyper velocity is quite important. So velocity really implies
[19:48] important. So velocity really implies
[19:48] important. So velocity really implies that you're moving at speed in the right
[19:50] that you're moving at speed in the right
[19:50] that you're moving at speed in the right direction. So it's not just about
[19:53] direction. So it's not just about
[19:53] direction. So it's not just about developing code fast. I think I won't
[19:56] developing code fast. I think I won't
[19:56] developing code fast. I think I won't say code is cheap. Code is not cheap.
[19:58] say code is cheap. Code is not cheap.
[19:58] say code is cheap. Code is not cheap. Code is an artifact and a business
[20:00] Code is an artifact and a business
[20:00] Code is an artifact and a business artifact that we expose to our
[20:01] artifact that we expose to our
[20:01] artifact that we expose to our customers. But the act of creating it
[20:04] customers. But the act of creating it
[20:04] customers. But the act of creating it and iterating it on it has become a lot
[20:06] and iterating it on it has become a lot
[20:06] and iterating it on it has become a lot more easier.
[20:08] more easier.
[20:08] more easier. But it's not that's not what the problem
[20:10] But it's not that's not what the problem
[20:10] But it's not that's not what the problem was. It wasn't about just being able to
[20:12] was. It wasn't about just being able to
[20:12] was. It wasn't about just being able to code something or develop code faster.
[20:15] code something or develop code faster.
[20:15] code something or develop code faster. It was about developing quality code
[20:17] It was about developing quality code
[20:17] It was about developing quality code with solid solid engineering principles
[20:20] with solid solid engineering principles
[20:20] with solid solid engineering principles more quickly. So it's not vibe coding.
[20:23] more quickly. So it's not vibe coding.
[20:23] more quickly. So it's not vibe coding. It's what hypervelocity engineering
[20:25] It's what hypervelocity engineering
[20:25] It's what hypervelocity engineering does. It's more about enabling a team to
[20:28] does. It's more about enabling a team to
[20:28] does. It's more about enabling a team to work together to and execute much more
[20:31] work together to and execute much more
[20:31] work together to and execute much more effectively using AI
[20:39] and this is kind of being reinforced um
[20:39] and this is kind of being reinforced um throughout the industry as well. So Dora
[20:42] throughout the industry as well. So Dora
[20:42] throughout the industry as well. So Dora the DevOps research and assessment
[20:43] the DevOps research and assessment
[20:43] the DevOps research and assessment report essentially reband reband
[20:46] report essentially reband reband
[20:46] report essentially reband reband rebranded sorry itself entirely and said
[20:48] rebranded sorry itself entirely and said
[20:48] rebranded sorry itself entirely and said the state of AI assisted software
[20:50] the state of AI assisted software
[20:50] the state of AI assisted software development and the basic the
[20:52] development and the basic the
[20:52] development and the basic the underlining um message coming out of
[20:55] underlining um message coming out of
[20:55] underlining um message coming out of that is that AI is an amplifier. It's
[20:57] that is that AI is an amplifier. It's
[20:57] that is that AI is an amplifier. It's not a silver bullet. It's not a case of
[20:59] not a silver bullet. It's not a case of
[21:00] not a silver bullet. It's not a case of going oh just use GitHub co-pilot bro
[21:02] going oh just use GitHub co-pilot bro
[21:02] going oh just use GitHub co-pilot bro we're just going to you know vibe code
[21:04] we're just going to you know vibe code
[21:04] we're just going to you know vibe code this. It's not about that. I think
[21:05] this. It's not about that. I think
[21:05] this. It's not about that. I think everyone in the room we're now maybe
[21:08] everyone in the room we're now maybe
[21:08] everyone in the room we're now maybe some of us have have got some battle
[21:09] some of us have have got some battle
[21:09] some of us have have got some battle scars. I know I have of developing stuff
[21:12] scars. I know I have of developing stuff
[21:12] scars. I know I have of developing stuff um and just you know seeing these agents
[21:15] um and just you know seeing these agents
[21:15] um and just you know seeing these agents run rampant but I think now highquality
[21:18] run rampant but I think now highquality
[21:18] run rampant but I think now highquality platforms or high quality um engineering
[21:20] platforms or high quality um engineering
[21:20] platforms or high quality um engineering practices are amplified through AI
[21:23] practices are amplified through AI
[21:23] practices are amplified through AI whereas you know kind of oneot prompting
[21:25] whereas you know kind of oneot prompting
[21:25] whereas you know kind of oneot prompting kind of amplifies the weakness and
[21:27] kind of amplifies the weakness and
[21:27] kind of amplifies the weakness and amplifies those vulnerabilities.
[21:30] amplifies those vulnerabilities.
[21:30] amplifies those vulnerabilities. So I'm going to start from an individual
[21:32] So I'm going to start from an individual
[21:32] So I'm going to start from an individual developer perspective on how we can
[21:34] developer perspective on how we can
[21:34] developer perspective on how we can actually kind of tame our coding agents
[21:35] actually kind of tame our coding agents
[21:35] actually kind of tame our coding agents and then I'll talk about uh how we can
[21:37] and then I'll talk about uh how we can
[21:37] and then I'll talk about uh how we can actually apply that across um our teams
[21:40] actually apply that across um our teams
[21:40] actually apply that across um our teams and organizations.
[21:45] So the agents work on my machines. So
[21:45] So the agents work on my machines. So the challenges from a platform
[21:47] the challenges from a platform
[21:47] the challenges from a platform engineering perspective is essentially
[21:50] engineering perspective is essentially
[21:50] engineering perspective is essentially ensuring consistent behavior across your
[21:52] ensuring consistent behavior across your
[21:52] ensuring consistent behavior across your developers in your organization. If you
[21:55] developers in your organization. If you
[21:55] developers in your organization. If you think about um how you do your work
[21:58] think about um how you do your work
[21:58] think about um how you do your work day-to-day for your organization, you
[22:00] day-to-day for your organization, you
[22:00] day-to-day for your organization, you might be using particular language
[22:02] might be using particular language
[22:02] might be using particular language conventions, you might be deploying to
[22:04] conventions, you might be deploying to
[22:04] conventions, you might be deploying to different targets. So obviously I spend
[22:07] different targets. So obviously I spend
[22:07] different targets. So obviously I spend a lot of time in the .NET and Azure
[22:08] a lot of time in the .NET and Azure
[22:08] a lot of time in the .NET and Azure world. Some of you might be writing Java
[22:10] world. Some of you might be writing Java
[22:10] world. Some of you might be writing Java or Golang and deploying to AWS or GCP or
[22:13] or Golang and deploying to AWS or GCP or
[22:13] or Golang and deploying to AWS or GCP or other providers. Um so it's essentially
[22:16] other providers. Um so it's essentially
[22:16] other providers. Um so it's essentially one part of it is to make sure that
[22:17] one part of it is to make sure that
[22:17] one part of it is to make sure that there's consistent behavior across your
[22:19] there's consistent behavior across your
[22:19] there's consistent behavior across your organization that reflects the way that
[22:22] organization that reflects the way that
[22:22] organization that reflects the way that you do your work.
[22:24] you do your work.
[22:24] you do your work. And also this challenge I think we're
[22:29] And also this challenge I think we're
[22:29] And also this challenge I think we're this may change with time. I think in
[22:32] this may change with time. I think in
[22:32] this may change with time. I think in the initial early stages we saw very
[22:36] the initial early stages we saw very
[22:36] the initial early stages we saw very much an experimentation phase where we
[22:37] much an experimentation phase where we
[22:37] much an experimentation phase where we would try different coding assistants.
[22:39] would try different coding assistants.
[22:39] would try different coding assistants. So some developers would have um cursor
[22:42] So some developers would have um cursor
[22:42] So some developers would have um cursor credits and some would have GitHub
[22:44] credits and some would have GitHub
[22:44] credits and some would have GitHub copilot or some might have claude. I
[22:46] copilot or some might have claude. I
[22:46] copilot or some might have claude. I think now we might see um particularly
[22:49] think now we might see um particularly
[22:49] think now we might see um particularly in the enterprise space some being more
[22:53] in the enterprise space some being more
[22:53] in the enterprise space some being more opinionated saying no our coding
[22:54] opinionated saying no our coding
[22:54] opinionated saying no our coding assistant is GitHub copilot or no we're
[22:56] assistant is GitHub copilot or no we're
[22:56] assistant is GitHub copilot or no we're going to go all in on claude code. I
[22:58] going to go all in on claude code. I
[22:58] going to go all in on claude code. I could be wrong on that but I I think now
[23:00] could be wrong on that but I I think now
[23:00] could be wrong on that but I I think now that um now that the billing model is
[23:04] that um now that the billing model is
[23:04] that um now that the billing model is changing and [laughter] the the benefits
[23:06] changing and [laughter] the the benefits
[23:06] changing and [laughter] the the benefits of I won't go too much into billing
[23:08] of I won't go too much into billing
[23:08] of I won't go too much into billing today. I'm a software engineer. I'm not
[23:11] today. I'm a software engineer. I'm not
[23:11] today. I'm a software engineer. I'm not um trained um in the in the sales side
[23:13] um trained um in the in the sales side
[23:13] um trained um in the in the sales side of it. Um that's a deliberate choice on
[23:15] of it. Um that's a deliberate choice on
[23:15] of it. Um that's a deliberate choice on my part. So I won't be able to provide
[23:17] my part. So I won't be able to provide
[23:17] my part. So I won't be able to provide any uh insights onto billing changes
[23:19] any uh insights onto billing changes
[23:19] any uh insights onto billing changes particularly since they were made last
[23:21] particularly since they were made last
[23:21] particularly since they were made last week and I was in Italy. Um but we will
[23:24] week and I was in Italy. Um but we will
[23:24] week and I was in Italy. Um but we will see um less of different developers
[23:26] see um less of different developers
[23:26] see um less of different developers within organizations using coding
[23:28] within organizations using coding
[23:28] within organizations using coding assistance uh different coding
[23:29] assistance uh different coding
[23:30] assistance uh different coding assistants. Sorry.
[23:33] assistants. Sorry.
[23:33] assistants. Sorry. To that end um has anyone heard of the
[23:35] To that end um has anyone heard of the
[23:35] To that end um has anyone heard of the Aentic AI Foundation?
[23:39] Aentic AI Foundation?
[23:39] Aentic AI Foundation? Couple of hands. Couple of hands. So
[23:40] Couple of hands. Couple of hands. So
[23:40] Couple of hands. Couple of hands. So essentially um in December 9th 2025
[23:43] essentially um in December 9th 2025
[23:43] essentially um in December 9th 2025 hopefully I'm getting that date right
[23:46] hopefully I'm getting that date right
[23:46] hopefully I'm getting that date right anthropic block and open AAI co-founded
[23:49] anthropic block and open AAI co-founded
[23:49] anthropic block and open AAI co-founded the Gentic AI foundation under the um
[23:53] the Gentic AI foundation under the um
[23:53] the Gentic AI foundation under the um foundation sorry under the Linux
[23:54] foundation sorry under the Linux
[23:54] foundation sorry under the Linux foundation uh AWS Google Microsoft
[23:58] foundation uh AWS Google Microsoft
[23:58] foundation uh AWS Google Microsoft Cloudflare and Bloomberg are all
[24:00] Cloudflare and Bloomberg are all
[24:00] Cloudflare and Bloomberg are all platinum supporters and essentially
[24:02] platinum supporters and essentially
[24:02] platinum supporters and essentially their role is to steward the three open
[24:06] their role is to steward the three open
[24:06] their role is to steward the three open standards uh around AI. So that's MCP
[24:09] standards uh around AI. So that's MCP
[24:09] standards uh around AI. So that's MCP servers, agents.m MD files, and also
[24:12] servers, agents.m MD files, and also
[24:12] servers, agents.m MD files, and also agent skills.
[24:15] agent skills.
[24:15] agent skills. Um, and there they are.
[24:19] Um, and there they are.
[24:19] Um, and there they are. Who knows um what MCP servers are? Most
[24:24] Who knows um what MCP servers are? Most
[24:24] Who knows um what MCP servers are? Most hands. Have you has everyone here
[24:25] hands. Have you has everyone here
[24:25] hands. Have you has everyone here developed an MCP server?
[24:28] developed an MCP server?
[24:28] developed an MCP server? Couple of hands as well. Um, so MCP
[24:31] Couple of hands as well. Um, so MCP
[24:31] Couple of hands as well. Um, so MCP really is just a wire. So think of it
[24:34] really is just a wire. So think of it
[24:34] really is just a wire. So think of it this think of it as a USBC for AI
[24:37] this think of it as a USBC for AI
[24:37] this think of it as a USBC for AI agents. So it's basically a standard
[24:39] agents. So it's basically a standard
[24:39] agents. So it's basically a standard protocol between agents and the tools
[24:41] protocol between agents and the tools
[24:41] protocol between agents and the tools that they get to use or or allowed to
[24:44] that they get to use or or allowed to
[24:44] that they get to use or or allowed to use. Um and I think it's developed over
[24:47] use. Um and I think it's developed over
[24:47] use. Um and I think it's developed over time. Um so there's um OOTH is pretty
[24:50] time. Um so there's um OOTH is pretty
[24:50] time. Um so there's um OOTH is pretty standard now. Um there's various
[24:54] standard now. Um there's various
[24:54] standard now. Um there's various different SDKs for it. Um there's
[24:57] different SDKs for it. Um there's
[24:57] different SDKs for it. Um there's thousands of different servers and from
[24:59] thousands of different servers and from
[24:59] thousands of different servers and from a platform engineering perspective that
[25:01] a platform engineering perspective that
[25:01] a platform engineering perspective that kind of helps us a lot. I think MCP is
[25:03] kind of helps us a lot. I think MCP is
[25:03] kind of helps us a lot. I think MCP is very powerful. Um particularly because
[25:06] very powerful. Um particularly because
[25:06] very powerful. Um particularly because every kind of um internal or developer
[25:08] every kind of um internal or developer
[25:08] every kind of um internal or developer platform now ships kind of a native MCP
[25:11] platform now ships kind of a native MCP
[25:11] platform now ships kind of a native MCP server. So in the Azure space uh there's
[25:13] server. So in the Azure space uh there's
[25:13] server. So in the Azure space uh there's one for Azure DevOps and also the Azure
[25:16] one for Azure DevOps and also the Azure
[25:16] one for Azure DevOps and also the Azure MCP server I think where different
[25:18] MCP server I think where different
[25:18] MCP server I think where different product teams kind of created their own
[25:20] product teams kind of created their own
[25:20] product teams kind of created their own MCP servers which was interesting. So
[25:22] MCP servers which was interesting. So
[25:22] MCP servers which was interesting. So you had to, you know, install and
[25:23] you had to, you know, install and
[25:23] you had to, you know, install and configure all these various different um
[25:25] configure all these various different um
[25:25] configure all these various different um servers. I think we're going to see kind
[25:26] servers. I think we're going to see kind
[25:26] servers. I think we're going to see kind of like a unified uh a move towards a
[25:29] of like a unified uh a move towards a
[25:29] of like a unified uh a move towards a more unified one. GitHub has one. Um
[25:31] more unified one. GitHub has one. Um
[25:32] more unified one. GitHub has one. Um there's uh MCP servers for AWS, Docker,
[25:35] there's uh MCP servers for AWS, Docker,
[25:35] there's uh MCP servers for AWS, Docker, Kubernetes, Hashi Cor, uh Terraform,
[25:38] Kubernetes, Hashi Cor, uh Terraform,
[25:38] Kubernetes, Hashi Cor, uh Terraform, they've got an MCP server, but I think
[25:40] they've got an MCP server, but I think
[25:40] they've got an MCP server, but I think it's read only. I could be wrong about
[25:42] it's read only. I could be wrong about
[25:42] it's read only. I could be wrong about that. So different organizations and
[25:44] that. So different organizations and
[25:44] that. So different organizations and different um MTP server developers will
[25:46] different um MTP server developers will
[25:46] different um MTP server developers will have different rules around h what kind
[25:49] have different rules around h what kind
[25:49] have different rules around h what kind of tools you can use whether it's just
[25:50] of tools you can use whether it's just
[25:50] of tools you can use whether it's just readonly tools or create tools or update
[25:53] readonly tools or create tools or update
[25:53] readonly tools or create tools or update tools stuff like that.
[26:01] Come on clicker work. Um and agent MD
[26:01] Come on clicker work. Um and agent MD files. So essentially this is the readme
[26:03] files. So essentially this is the readme
[26:03] files. So essentially this is the readme for agents. Essentially agents MDs will
[26:06] for agents. Essentially agents MDs will
[26:06] for agents. Essentially agents MDs will tell any AI coding tool here's our
[26:09] tell any AI coding tool here's our
[26:09] tell any AI coding tool here's our architecture. This is how we test. This
[26:11] architecture. This is how we test. This
[26:11] architecture. This is how we test. This is what you must never do. Um, it
[26:13] is what you must never do. Um, it
[26:13] is what you must never do. Um, it basically just defined some rules for
[26:15] basically just defined some rules for
[26:15] basically just defined some rules for the air coding assistant itself. Just to
[26:18] the air coding assistant itself. Just to
[26:18] the air coding assistant itself. Just to pull up some numbers, it's in 60,000
[26:21] pull up some numbers, it's in 60,000
[26:21] pull up some numbers, it's in 60,000 plus open source repos last I checked. I
[26:23] plus open source repos last I checked. I
[26:23] plus open source repos last I checked. I would be surprised if that number wasn't
[26:25] would be surprised if that number wasn't
[26:25] would be surprised if that number wasn't a little bit more now. Um, and it's
[26:27] a little bit more now. Um, and it's
[26:28] a little bit more now. Um, and it's native in C-pilot, Cursor, Codeex,
[26:30] native in C-pilot, Cursor, Codeex,
[26:30] native in C-pilot, Cursor, Codeex, Windsurf, and kind of most agent tools.
[26:32] Windsurf, and kind of most agent tools.
[26:32] Windsurf, and kind of most agent tools. Claude has a Claude MD file which kind
[26:35] Claude has a Claude MD file which kind
[26:35] Claude has a Claude MD file which kind of uses is is is the same. My advice uh
[26:39] of uses is is is the same. My advice uh
[26:39] of uses is is is the same. My advice uh around agent MD files uh humans need to
[26:42] around agent MD files uh humans need to
[26:42] around agent MD files uh humans need to write this file. Don't get AI to write
[26:44] write this file. Don't get AI to write
[26:44] write this file. Don't get AI to write an agent's file for you. Um because it
[26:48] an agent's file for you. Um because it
[26:48] an agent's file for you. Um because it will be not because because a human
[26:50] will be not because because a human
[26:50] will be not because because a human written agent MD files will be more
[26:52] written agent MD files will be more
[26:52] written agent MD files will be more successful. Um and with LLM generated
[26:56] successful. Um and with LLM generated
[26:56] successful. Um and with LLM generated ones, they can kind of uh decrease uh
[26:59] ones, they can kind of uh decrease uh
[26:59] ones, they can kind of uh decrease uh the success of your agents and also
[27:01] the success of your agents and also
[27:01] the success of your agents and also increase the cost and how much you're
[27:02] increase the cost and how much you're
[27:02] increase the cost and how much you're spending on tokens.
[27:05] spending on tokens.
[27:05] spending on tokens. And then agent skills. Uh who knows what
[27:07] And then agent skills. Uh who knows what
[27:07] And then agent skills. Uh who knows what agent skills are used agent skills.
[27:09] agent skills are used agent skills.
[27:09] agent skills are used agent skills. Awesome. Most of us in the room. Uh so
[27:11] Awesome. Most of us in the room. Uh so
[27:11] Awesome. Most of us in the room. Uh so essentially folders of instructions,
[27:13] essentially folders of instructions,
[27:13] essentially folders of instructions, scripts and resources that agents can
[27:15] scripts and resources that agents can
[27:15] scripts and resources that agents can use uh to discover and use to do things
[27:17] use uh to discover and use to do things
[27:18] use uh to discover and use to do things more accurately and efficiently. Um so
[27:21] more accurately and efficiently. Um so
[27:21] more accurately and efficiently. Um so it's really handy for doing kind of more
[27:23] it's really handy for doing kind of more
[27:23] it's really handy for doing kind of more capable stuff. Um but agents won't have
[27:26] capable stuff. Um but agents won't have
[27:26] capable stuff. Um but agents won't have the context that have the context that
[27:28] the context that have the context that
[27:28] the context that have the context that they need to do kind of real work
[27:30] they need to do kind of real work
[27:30] they need to do kind of real work reliably. So skills kind of help agents
[27:33] reliably. So skills kind of help agents
[27:33] reliably. So skills kind of help agents u by giving them access to procedural
[27:35] u by giving them access to procedural
[27:35] u by giving them access to procedural knowledge. uh within a company, within a
[27:37] knowledge. uh within a company, within a
[27:37] knowledge. uh within a company, within a team, users specific context that they
[27:40] team, users specific context that they
[27:40] team, users specific context that they can kind of load on demand. So for
[27:42] can kind of load on demand. So for
[27:42] can kind of load on demand. So for authors, particularly if you're kind of
[27:44] authors, particularly if you're kind of
[27:44] authors, particularly if you're kind of building skills for your organization,
[27:46] building skills for your organization,
[27:46] building skills for your organization, you can kind of build them once and then
[27:48] you can kind of build them once and then
[27:48] you can kind of build them once and then deploy them across multiple agent
[27:49] deploy them across multiple agent
[27:49] deploy them across multiple agent products. Uh for compatible agents,
[27:52] products. Uh for compatible agents,
[27:52] products. Uh for compatible agents, [snorts] it allows end users to give
[27:55] [snorts] it allows end users to give
[27:55] [snorts] it allows end users to give agents new capabilities out of the box.
[27:57] agents new capabilities out of the box.
[27:57] agents new capabilities out of the box. And then for teams and enterprises, you
[27:59] And then for teams and enterprises, you
[27:59] And then for teams and enterprises, you can essentially capture your
[28:00] can essentially capture your
[28:00] can essentially capture your organizational knowledge in a skills MD
[28:03] organizational knowledge in a skills MD
[28:03] organizational knowledge in a skills MD file. and then um
[28:10] share that in a portable uh in also
[28:10] share that in a portable uh in also version controlled way. I have seen some
[28:11] version controlled way. I have seen some
[28:11] version controlled way. I have seen some version control around this. Who is
[28:13] version control around this. Who is
[28:13] version control around this. Who is using version controls for their agent
[28:15] using version controls for their agent
[28:15] using version controls for their agent files? A couple of hands.
[28:18] files? A couple of hands.
[28:18] files? A couple of hands. That's interesting. I think we'll see
[28:20] That's interesting. I think we'll see
[28:20] That's interesting. I think we'll see more of that in the future. I know a
[28:22] more of that in the future. I know a
[28:22] more of that in the future. I know a couple of cloud solution architects, I
[28:24] couple of cloud solution architects, I
[28:24] couple of cloud solution architects, I believe they're based in France for
[28:25] believe they're based in France for
[28:25] believe they're based in France for Microsoft, have come out with something
[28:27] Microsoft, have come out with something
[28:27] Microsoft, have come out with something called the agent package manager, which
[28:29] called the agent package manager, which
[28:29] called the agent package manager, which is kind of looking at it from a um
[28:32] is kind of looking at it from a um
[28:32] is kind of looking at it from a um basically treating it like agents or
[28:34] basically treating it like agents or
[28:34] basically treating it like agents or agent skills as as packages that you can
[28:36] agent skills as as packages that you can
[28:36] agent skills as as packages that you can just install from a a centralized
[28:38] just install from a a centralized
[28:38] just install from a a centralized registry. Um others use VS Code plugins.
[28:41] registry. Um others use VS Code plugins.
[28:41] registry. Um others use VS Code plugins. So I'll show you some of the stuff that
[28:42] So I'll show you some of the stuff that
[28:42] So I'll show you some of the stuff that we've developed in um ISC and we've made
[28:45] we've developed in um ISC and we've made
[28:45] we've developed in um ISC and we've made that available through plugins so it
[28:47] that available through plugins so it
[28:47] that available through plugins so it doesn't kind of come into your
[28:48] doesn't kind of come into your
[28:48] doesn't kind of come into your repositories um codebase for those of
[28:51] repositories um codebase for those of
[28:51] repositories um codebase for those of you who are wondering that is my attempt
[28:53] you who are wondering that is my attempt
[28:53] you who are wondering that is my attempt of um binary so that's what what I do
[28:56] of um binary so that's what what I do
[28:56] of um binary so that's what what I do have are a very particular set of skills
[28:58] have are a very particular set of skills
[28:58] have are a very particular set of skills no one was laughing so I assume it's a
[28:59] no one was laughing so I assume it's a
[29:00] no one was laughing so I assume it's a terrible joke so it's fine don't worry
[29:03] terrible joke so it's fine don't worry
[29:03] terrible joke so it's fine don't worry um yes so again so really agent skills
[29:06] um yes so again so really agent skills
[29:06] um yes so again so really agent skills enable domain expertise any new
[29:08] enable domain expertise any new
[29:08] enable domain expertise any new capability so creating presentations s
[29:11] capability so creating presentations s
[29:11] capability so creating presentations s building MCP servers, analyzing data
[29:13] building MCP servers, analyzing data
[29:13] building MCP servers, analyzing data steps, uh repeatable workflows as well.
[29:16] steps, uh repeatable workflows as well.
[29:16] steps, uh repeatable workflows as well. Um so I've used agent skills in the past
[29:18] Um so I've used agent skills in the past
[29:18] Um so I've used agent skills in the past for my git workflow. So essentially
[29:20] for my git workflow. So essentially
[29:20] for my git workflow. So essentially invoke that skill and it kind of does
[29:21] invoke that skill and it kind of does
[29:22] invoke that skill and it kind of does the git workflow for me. Um and then I
[29:24] the git workflow for me. Um and then I
[29:24] the git workflow for me. Um and then I can use that same skill across different
[29:27] can use that same skill across different
[29:27] can use that same skill across different um coding assistants.
[29:34] And this is just an example of how that
[29:34] And this is just an example of how that might look in uh different um coding um
[29:37] might look in uh different um coding um
[29:37] might look in uh different um coding um assistance or for code different coding
[29:38] assistance or for code different coding
[29:38] assistance or for code different coding editors. The essential thing is now that
[29:40] editors. The essential thing is now that
[29:40] editors. The essential thing is now that the Aentic AI foundation is here, we'll
[29:44] the Aentic AI foundation is here, we'll
[29:44] the Aentic AI foundation is here, we'll see more of kind of like a unification
[29:46] see more of kind of like a unification
[29:46] see more of kind of like a unification of the standards um just so you know
[29:49] of the standards um just so you know
[29:49] of the standards um just so you know there isn't a major difference between
[29:51] there isn't a major difference between
[29:51] there isn't a major difference between um between the different coding
[29:53] um between the different coding
[29:53] um between the different coding assistants,
[29:56] assistants,
[29:56] assistants, right? Spec driven development. Who
[29:58] right? Spec driven development. Who
[29:58] right? Spec driven development. Who knows what spec driven development is?
[30:00] knows what spec driven development is?
[30:00] knows what spec driven development is? Few hands in the room. Awesome.
[30:03] Few hands in the room. Awesome.
[30:03] Few hands in the room. Awesome. So essentially for those who didn't put
[30:05] So essentially for those who didn't put
[30:05] So essentially for those who didn't put their hands up, I'll just recap this
[30:06] their hands up, I'll just recap this
[30:06] their hands up, I'll just recap this really quickly. Um so it kind of flips
[30:09] really quickly. Um so it kind of flips
[30:09] really quickly. Um so it kind of flips the script on traditional software um
[30:11] the script on traditional software um
[30:11] the script on traditional software um development. I mentioned earlier that
[30:12] development. I mentioned earlier that
[30:12] development. I mentioned earlier that documentation wasn't something we did
[30:14] documentation wasn't something we did
[30:14] documentation wasn't something we did too well as an industry. Um but the idea
[30:17] too well as an industry. Um but the idea
[30:17] too well as an industry. Um but the idea is okay now what we're going to do we'll
[30:19] is okay now what we're going to do we'll
[30:19] is okay now what we're going to do we'll use generative AI to kind of build out
[30:22] use generative AI to kind of build out
[30:22] use generative AI to kind of build out specs for features that we're going to
[30:24] specs for features that we're going to
[30:24] specs for features that we're going to implement and then coding assistants
[30:26] implement and then coding assistants
[30:26] implement and then coding assistants will use those specs that we've
[30:28] will use those specs that we've
[30:28] will use those specs that we've collaborated with our coding assistant
[30:30] collaborated with our coding assistant
[30:30] collaborated with our coding assistant to go ahead and actually build and
[30:31] to go ahead and actually build and
[30:31] to go ahead and actually build and generate that code and build the feature
[30:32] generate that code and build the feature
[30:32] generate that code and build the feature for us.
[30:34] for us.
[30:34] for us. And one of the very
[30:37] And one of the very
[30:37] And one of the very That was quick.
[30:49] One of the very early uh spec driven
[30:49] One of the very early uh spec driven development frameworks that um came onto
[30:51] development frameworks that um came onto
[30:51] development frameworks that um came onto the scene uh GitHub spec kit. So
[30:55] the scene uh GitHub spec kit. So
[30:55] the scene uh GitHub spec kit. So essentially it started with this idea
[30:57] essentially it started with this idea
[30:57] essentially it started with this idea that we have intent driven development.
[30:59] that we have intent driven development.
[30:59] that we have intent driven development. So we start with what we're going to
[31:01] So we start with what we're going to
[31:01] So we start with what we're going to develop before we we think how we're
[31:03] develop before we we think how we're
[31:03] develop before we we think how we're actually going to develop it. We'll
[31:05] actually going to develop it. We'll
[31:05] actually going to develop it. We'll create some specifications out of that.
[31:07] create some specifications out of that.
[31:07] create some specifications out of that. Um there are some uh there is an element
[31:10] Um there are some uh there is an element
[31:10] Um there are some uh there is an element of refinement in there as well. So
[31:11] of refinement in there as well. So
[31:11] of refinement in there as well. So rather than just kind of oneshot
[31:13] rather than just kind of oneshot
[31:13] rather than just kind of oneshot prompting this thing um we're going to
[31:17] prompting this thing um we're going to
[31:17] prompting this thing um we're going to you know work the coding system to
[31:18] you know work the coding system to
[31:18] you know work the coding system to refine as we would you know if we're
[31:20] refine as we would you know if we're
[31:20] refine as we would you know if we're doing like um backlog refinement. uh and
[31:23] doing like um backlog refinement. uh and
[31:23] doing like um backlog refinement. uh and there's heavy reliance on kind of the AI
[31:25] there's heavy reliance on kind of the AI
[31:25] there's heavy reliance on kind of the AI model capabilities to kind of um
[31:28] model capabilities to kind of um
[31:28] model capabilities to kind of um interpret that specification.
[31:31] interpret that specification.
[31:31] interpret that specification. Now this is an example. Hopefully the
[31:33] Now this is an example. Hopefully the
[31:33] Now this is an example. Hopefully the video will play automatically.
[31:37] video will play automatically.
[31:37] video will play automatically. No,
[31:39] No,
[31:40] No, I just press play on that.
[31:43] I just press play on that.
[31:43] I just press play on that. [clears throat]
[31:43] [clears throat]
[31:44] [clears throat] I'm having all kinds of fun. Anyway,
[31:45] I'm having all kinds of fun. Anyway,
[31:46] I'm having all kinds of fun. Anyway, essentially
[31:47] essentially
[31:47] essentially this is a video of um a repo of mine
[31:51] this is a video of um a repo of mine
[31:51] this is a video of um a repo of mine where I had gone through the spec uh
[31:53] where I had gone through the spec uh
[31:53] where I had gone through the spec uh driven um development process and
[31:56] driven um development process and
[31:56] driven um development process and there's a whole bunch of markdown files
[31:57] there's a whole bunch of markdown files
[31:57] there's a whole bunch of markdown files that gets created. And one of the
[31:59] that gets created. And one of the
[31:59] that gets created. And one of the earlier mistakes that I would do is
[32:01] earlier mistakes that I would do is
[32:01] earlier mistakes that I would do is essentially commit everything. So your
[32:03] essentially commit everything. So your
[32:03] essentially commit everything. So your research dossier, your specifications,
[32:05] research dossier, your specifications,
[32:05] research dossier, your specifications, what else have I got there? Quick start,
[32:07] what else have I got there? Quick start,
[32:07] what else have I got there? Quick start, um taskm file, everything in there. Uh
[32:10] um taskm file, everything in there. Uh
[32:10] um taskm file, everything in there. Uh and just committing that to the the
[32:12] and just committing that to the the
[32:12] and just committing that to the the repository. And the idea or the
[32:14] repository. And the idea or the
[32:14] repository. And the idea or the intention behind that is to be like well
[32:16] intention behind that is to be like well
[32:16] intention behind that is to be like well others can go and have a look at that
[32:17] others can go and have a look at that
[32:17] others can go and have a look at that see the decisions I made s see how I
[32:21] see the decisions I made s see how I
[32:21] see the decisions I made s see how I could interact with um the AI um coding
[32:24] could interact with um the AI um coding
[32:24] could interact with um the AI um coding assistant to see you know how we
[32:25] assistant to see you know how we
[32:25] assistant to see you know how we actually came to this particular feature
[32:28] actually came to this particular feature
[32:28] actually came to this particular feature now that's a lot of files that is 26
[32:31] now that's a lot of files that is 26
[32:31] now that's a lot of files that is 26 files um that have been changed and
[32:36] files um that have been changed and
[32:36] files um that have been changed and doing some guesstimation around the comp
[32:38] doing some guesstimation around the comp
[32:38] doing some guesstimation around the comp comprehensive test coverage that's
[32:40] comprehensive test coverage that's
[32:40] comprehensive test coverage that's probably more uh markdown so 20 files
[32:43] probably more uh markdown so 20 files
[32:43] probably more uh markdown so 20 files out of 26 files I'm committing around
[32:46] out of 26 files I'm committing around
[32:46] out of 26 files I'm committing around markdown. As you can probably imagine,
[32:48] markdown. As you can probably imagine,
[32:48] markdown. As you can probably imagine, over time you're developing more
[32:50] over time you're developing more
[32:50] over time you're developing more features and you're adopting this
[32:52] features and you're adopting this
[32:52] features and you're adopting this approach of committing everything. Your
[32:54] approach of committing everything. Your
[32:54] approach of committing everything. Your repositories
[32:55] repositories
[32:55] repositories come become polluted with the copious
[32:58] come become polluted with the copious
[32:58] come become polluted with the copious amounts of markdown files in there. And
[33:01] amounts of markdown files in there. And
[33:01] amounts of markdown files in there. And I think I'm be honest, I won't go back
[33:03] I think I'm be honest, I won't go back
[33:03] I think I'm be honest, I won't go back and refer to a specification that was
[33:05] and refer to a specification that was
[33:06] and refer to a specification that was generated four months ago, not maybe
[33:08] generated four months ago, not maybe
[33:08] generated four months ago, not maybe even, you know, three months ago. And
[33:11] even, you know, three months ago. And
[33:11] even, you know, three months ago. And that documentation becomes very stale
[33:12] that documentation becomes very stale
[33:12] that documentation becomes very stale and it's in the wrong place because
[33:14] and it's in the wrong place because
[33:14] and it's in the wrong place because every time what someone wants to
[33:15] every time what someone wants to
[33:15] every time what someone wants to contribute, you can imagine if this was
[33:16] contribute, you can imagine if this was
[33:16] contribute, you can imagine if this was in a a proper um organization or on a
[33:19] in a a proper um organization or on a
[33:19] in a a proper um organization or on a proper application, they've got to pull
[33:21] proper application, they've got to pull
[33:21] proper application, they've got to pull that down. So they've got to pull down
[33:23] that down. So they've got to pull down
[33:23] that down. So they've got to pull down all that markdown files that they're not
[33:25] all that markdown files that they're not
[33:25] all that markdown files that they're not necessarily going to need or use or
[33:27] necessarily going to need or use or
[33:27] necessarily going to need or use or interested in.
[33:33] So this was kind of recognized and
[33:34] So this was kind of recognized and around spec driven development, we have
[33:35] around spec driven development, we have
[33:35] around spec driven development, we have this kind of pattern where we have
[33:36] this kind of pattern where we have
[33:36] this kind of pattern where we have research, plan and implement. So that
[33:39] research, plan and implement. So that
[33:39] research, plan and implement. So that was one of the things that was
[33:40] was one of the things that was
[33:40] was one of the things that was discovered um out of GitHub um um the
[33:45] discovered um out of GitHub um um the
[33:45] discovered um out of GitHub um um the spec uh driven development workflow
[33:48] spec uh driven development workflow
[33:48] spec uh driven development workflow where you would have this research where
[33:51] where you would have this research where
[33:51] where you would have this research where you kind of research a feature, research
[33:52] you kind of research a feature, research
[33:52] you kind of research a feature, research the codebase, see how you could
[33:55] the codebase, see how you could
[33:55] the codebase, see how you could potentially implement something. Uh then
[33:57] potentially implement something. Uh then
[33:57] potentially implement something. Uh then it would go into an implement phase and
[33:58] it would go into an implement phase and
[33:58] it would go into an implement phase and then review uh where coding agents will
[34:01] then review uh where coding agents will
[34:01] then review uh where coding agents will actually kind of use that workflow to
[34:03] actually kind of use that workflow to
[34:03] actually kind of use that workflow to implement new features.
[34:05] implement new features.
[34:05] implement new features. And that's a very basic um basic
[34:08] And that's a very basic um basic
[34:08] And that's a very basic um basic overview. So what I'm going to do is I'm
[34:10] overview. So what I'm going to do is I'm
[34:10] overview. So what I'm going to do is I'm going to just change into Visual Studio
[34:12] going to just change into Visual Studio
[34:12] going to just change into Visual Studio Code. I'll talk about harness
[34:14] Code. I'll talk about harness
[34:14] Code. I'll talk about harness engineering in a bit. But essentially a
[34:17] engineering in a bit. But essentially a
[34:18] engineering in a bit. But essentially a workflow could be more extensive rather
[34:21] workflow could be more extensive rather
[34:21] workflow could be more extensive rather than just you know research, plan,
[34:24] than just you know research, plan,
[34:24] than just you know research, plan, implement and then review. There may be
[34:26] implement and then review. There may be
[34:26] implement and then review. There may be several different stages. How's that
[34:28] several different stages. How's that
[34:28] several different stages. How's that looking at the back? And do you want me
[34:29] looking at the back? And do you want me
[34:29] looking at the back? And do you want me to go in one more? One more. Okay.
[34:33] to go in one more? One more. Okay.
[34:33] to go in one more? One more. Okay. So essentially this is um just really
[34:38] So essentially this is um just really
[34:38] So essentially this is um just really trying to um
[34:45] add more kind of um phases in how we
[34:45] add more kind of um phases in how we actually implement something. So we
[34:47] actually implement something. So we
[34:47] actually implement something. So we might start off by exploring a
[34:49] might start off by exploring a
[34:49] might start off by exploring a particular um feature. So if there's
[34:52] particular um feature. So if there's
[34:52] particular um feature. So if there's kind of like a a different UI framework
[34:54] kind of like a a different UI framework
[34:54] kind of like a a different UI framework that I want to implement. This is um
[34:56] that I want to implement. This is um
[34:56] that I want to implement. This is um microservices architecture. this project
[34:58] microservices architecture. this project
[34:58] microservices architecture. this project were around my health data. I collect
[35:00] were around my health data. I collect
[35:00] were around my health data. I collect health data off my Fitbit. When I'm not
[35:02] health data off my Fitbit. When I'm not
[35:02] health data off my Fitbit. When I'm not drinking and eating in Italy, I like to
[35:04] drinking and eating in Italy, I like to
[35:04] drinking and eating in Italy, I like to stay active. Um, so I spend a lot of
[35:07] stay active. Um, so I spend a lot of
[35:07] stay active. Um, so I spend a lot of time obsessing over my health metrics.
[35:09] time obsessing over my health metrics.
[35:09] time obsessing over my health metrics. Not so much anymore. Um, so essentially
[35:12] Not so much anymore. Um, so essentially
[35:12] Not so much anymore. Um, so essentially I've got this whole application. I might
[35:14] I've got this whole application. I might
[35:14] I've got this whole application. I might want to introduce a new health domain
[35:16] want to introduce a new health domain
[35:16] want to introduce a new health domain that I want to track. So I'd start off
[35:18] that I want to track. So I'd start off
[35:18] that I want to track. So I'd start off by exploring that and then we go into a
[35:21] by exploring that and then we go into a
[35:21] by exploring that and then we go into a specify. So we'll actually specify
[35:24] specify. So we'll actually specify
[35:24] specify. So we'll actually specify um what and why we're going to do this,
[35:27] um what and why we're going to do this,
[35:27] um what and why we're going to do this, not the how. And then from there, we
[35:30] not the how. And then from there, we
[35:30] not the how. And then from there, we might prep a GitHub issue. So once we've
[35:32] might prep a GitHub issue. So once we've
[35:32] might prep a GitHub issue. So once we've kind of figured something out, what
[35:34] kind of figured something out, what
[35:34] kind of figured something out, what we're going to build, we might want to
[35:35] we're going to build, we might want to
[35:35] we're going to build, we might want to store that into um GitHub. So we can use
[35:37] store that into um GitHub. So we can use
[35:37] store that into um GitHub. So we can use an agent skill or an MTP server to say,
[35:40] an agent skill or an MTP server to say,
[35:40] an agent skill or an MTP server to say, okay, we're going to create a GitHub uh
[35:43] okay, we're going to create a GitHub uh
[35:43] okay, we're going to create a GitHub uh issue out of this. We could workshop um
[35:46] issue out of this. We could workshop um
[35:46] issue out of this. We could workshop um a specification. We could do some
[35:48] a specification. We could do some
[35:48] a specification. We could do some clarification as well. And then from
[35:50] clarification as well. And then from
[35:50] clarification as well. And then from that clarification, we can actually
[35:52] that clarification, we can actually
[35:52] that clarification, we can actually create an architectural decision record.
[35:54] create an architectural decision record.
[35:54] create an architectural decision record. So that might talk to an Azure DevOps
[35:56] So that might talk to an Azure DevOps
[35:56] So that might talk to an Azure DevOps wiki for example um or Jirro or anything
[35:59] wiki for example um or Jirro or anything
[35:59] wiki for example um or Jirro or anything else where we store our architectural
[36:01] else where we store our architectural
[36:01] else where we store our architectural records and then we'll architect it, do
[36:04] records and then we'll architect it, do
[36:04] records and then we'll architect it, do some validation and then this feature I
[36:06] some validation and then this feature I
[36:06] some validation and then this feature I kind of stole from a colleague of mine.
[36:09] kind of stole from a colleague of mine.
[36:09] kind of stole from a colleague of mine. Did you know? So he'll have a command uh
[36:11] Did you know? So he'll have a command uh
[36:11] Did you know? So he'll have a command uh saying what gifts have we gained. So
[36:14] saying what gifts have we gained. So
[36:14] saying what gifts have we gained. So essentially
[36:15] essentially
[36:15] essentially did you know kind of says okay did you
[36:17] did you know kind of says okay did you
[36:17] did you know kind of says okay did you know that this happens over here so
[36:19] know that this happens over here so
[36:19] know that this happens over here so that's going to have an implication on
[36:21] that's going to have an implication on
[36:21] that's going to have an implication on the code you use over there or the
[36:22] the code you use over there or the
[36:22] the code you use over there or the feature that you're going to implement.
[36:24] feature that you're going to implement.
[36:24] feature that you're going to implement. So what we kind of talked about earlier,
[36:25] So what we kind of talked about earlier,
[36:25] So what we kind of talked about earlier, we've done a bit of research, that's not
[36:27] we've done a bit of research, that's not
[36:27] we've done a bit of research, that's not actually going to work out or I've gone
[36:30] actually going to work out or I've gone
[36:30] actually going to work out or I've gone ahead and done some research on how this
[36:31] ahead and done some research on how this
[36:31] ahead and done some research on how this framework works. Uh this is how it's
[36:34] framework works. Uh this is how it's
[36:34] framework works. Uh this is how it's going to actually work within this this
[36:35] going to actually work within this this
[36:36] going to actually work within this this codebase, things like that. And then
[36:38] codebase, things like that. And then
[36:38] codebase, things like that. And then once we've implemented it, we'll have a
[36:40] once we've implemented it, we'll have a
[36:40] once we've implemented it, we'll have a review. Uh this is all powered I'll just
[36:43] review. Uh this is all powered I'll just
[36:43] review. Uh this is all powered I'll just open up
[36:45] open up
[36:45] open up by a particular SD SD workflow. So they
[36:50] by a particular SD SD workflow. So they
[36:50] by a particular SD SD workflow. So they will work through all of these
[36:51] will work through all of these
[36:51] will work through all of these particular phases. But then we also have
[36:53] particular phases. But then we also have
[36:53] particular phases. But then we also have a review judge. We're starting to see
[36:56] a review judge. We're starting to see
[36:56] a review judge. We're starting to see LLM as a judge pattern where you might
[36:58] LLM as a judge pattern where you might
[36:58] LLM as a judge pattern where you might have a separate coding agent that uses a
[37:01] have a separate coding agent that uses a
[37:01] have a separate coding agent that uses a different model to review the changes
[37:03] different model to review the changes
[37:03] different model to review the changes that a particular coding agent or
[37:05] that a particular coding agent or
[37:05] that a particular coding agent or assistant has has actually generated for
[37:07] assistant has has actually generated for
[37:07] assistant has has actually generated for you just for kind of um verification. So
[37:10] you just for kind of um verification. So
[37:10] you just for kind of um verification. So this um the workflow uses claude opus
[37:13] this um the workflow uses claude opus
[37:13] this um the workflow uses claude opus 4.7
[37:14] 4.7
[37:14] 4.7 um and the review judge might use GPT uh
[37:17] um and the review judge might use GPT uh
[37:18] um and the review judge might use GPT uh 5.3 codeex or something like that. Uh
[37:20] 5.3 codeex or something like that. Uh
[37:20] 5.3 codeex or something like that. Uh and then from there
[37:23] and then from there
[37:23] and then from there we kind of evolve and I'll talk a little
[37:25] we kind of evolve and I'll talk a little
[37:25] we kind of evolve and I'll talk a little bit about harness engineering and how we
[37:27] bit about harness engineering and how we
[37:27] bit about harness engineering and how we can actually evolve um this particular
[37:30] can actually evolve um this particular
[37:30] can actually evolve um this particular harness so that next time we go through
[37:32] harness so that next time we go through
[37:32] harness so that next time we go through the um spec driven development workflow.
[37:34] the um spec driven development workflow.
[37:34] the um spec driven development workflow. This kind of reinforces what we've
[37:36] This kind of reinforces what we've
[37:36] This kind of reinforces what we've learned during a particular cycle um how
[37:40] learned during a particular cycle um how
[37:40] learned during a particular cycle um how we can apply that to our coding agents
[37:42] we can apply that to our coding agents
[37:42] we can apply that to our coding agents so they don't if they've made any
[37:43] so they don't if they've made any
[37:43] so they don't if they've made any mistakes during that they don't make
[37:45] mistakes during that they don't make
[37:45] mistakes during that they don't make that same mistake again.
[37:48] that same mistake again.
[37:48] that same mistake again. Uh and this is quite a comprehensive
[37:50] Uh and this is quite a comprehensive
[37:50] Uh and this is quite a comprehensive workflow. There are various different
[37:52] workflow. There are various different
[37:52] workflow. There are various different types of changes. Um some phases can be
[37:55] types of changes. Um some phases can be
[37:55] types of changes. Um some phases can be skipped depending on complexity of
[37:57] skipped depending on complexity of
[37:57] skipped depending on complexity of tasks. So this is how they all kind of
[38:00] tasks. So this is how they all kind of
[38:00] tasks. So this is how they all kind of match up uh for different artifacts. I
[38:03] match up uh for different artifacts. I
[38:03] match up uh for different artifacts. I think one of the the problems with spec
[38:05] think one of the the problems with spec
[38:05] think one of the the problems with spec kit was uh essentially it would produce
[38:07] kit was uh essentially it would produce
[38:07] kit was uh essentially it would produce a lot of artifacts but the linking
[38:09] a lot of artifacts but the linking
[38:10] a lot of artifacts but the linking between different phases wasn't quite as
[38:11] between different phases wasn't quite as
[38:11] between different phases wasn't quite as clean as possible. Uh so essentially
[38:13] clean as possible. Uh so essentially
[38:13] clean as possible. Uh so essentially this what I've introduced here is there
[38:15] this what I've introduced here is there
[38:15] this what I've introduced here is there will be different phases will produce
[38:17] will be different phases will produce
[38:17] will be different phases will produce different um uh kind of artifacts and
[38:20] different um uh kind of artifacts and
[38:20] different um uh kind of artifacts and that will be consumed by later phases.
[38:23] that will be consumed by later phases.
[38:23] that will be consumed by later phases. So that's the way of keeping the the
[38:24] So that's the way of keeping the the
[38:24] So that's the way of keeping the the loop tight. And then there's this the
[38:27] loop tight. And then there's this the
[38:27] loop tight. And then there's this the governance around the harness. So I'll
[38:29] governance around the harness. So I'll
[38:29] governance around the harness. So I'll just go down to uh complexity.
[38:33] just go down to uh complexity.
[38:33] just go down to uh complexity. So if it's doing like a single file
[38:35] So if it's doing like a single file
[38:35] So if it's doing like a single file change, we're not going to go through
[38:36] change, we're not going to go through
[38:36] change, we're not going to go through the entire workflow. I think spec kit
[38:38] the entire workflow. I think spec kit
[38:38] the entire workflow. I think spec kit was expecting us to kind of go through
[38:40] was expecting us to kind of go through
[38:40] was expecting us to kind of go through the workflow each and every time. if
[38:42] the workflow each and every time. if
[38:42] the workflow each and every time. if you're making a a very small tiny change
[38:45] you're making a a very small tiny change
[38:45] you're making a a very small tiny change uh you don't need to do that. So there
[38:47] uh you don't need to do that. So there
[38:47] uh you don't need to do that. So there various different complexities that you
[38:48] various different complexities that you
[38:48] various different complexities that you can apply here. So initially I was kind
[38:51] can apply here. So initially I was kind
[38:51] can apply here. So initially I was kind of against specd driven development just
[38:53] of against specd driven development just
[38:53] of against specd driven development just because the amount of um markdown that
[38:54] because the amount of um markdown that
[38:54] because the amount of um markdown that was produced but I think if you uh if
[38:57] was produced but I think if you uh if
[38:57] was produced but I think if you uh if you're intelligent about it or sensible
[38:59] you're intelligent about it or sensible
[38:59] you're intelligent about it or sensible about it we can actually um apply some
[39:02] about it we can actually um apply some
[39:02] about it we can actually um apply some guardrails where essentially we're not
[39:04] guardrails where essentially we're not
[39:04] guardrails where essentially we're not going to commit markdown files unless
[39:06] going to commit markdown files unless
[39:06] going to commit markdown files unless they add value. So, our readme file
[39:09] they add value. So, our readme file
[39:09] they add value. So, our readme file contributing security, uh, that's all
[39:11] contributing security, uh, that's all
[39:11] contributing security, uh, that's all fine. Um, if you are going to use AI to
[39:15] fine. Um, if you are going to use AI to
[39:15] fine. Um, if you are going to use AI to generate specs and documents, think
[39:16] generate specs and documents, think
[39:16] generate specs and documents, think about where you're actually going to
[39:17] about where you're actually going to
[39:18] about where you're actually going to store them. Genai is fantastic at
[39:19] store them. Genai is fantastic at
[39:19] store them. Genai is fantastic at generating content. Doesn't necessarily
[39:21] generating content. Doesn't necessarily
[39:22] generating content. Doesn't necessarily mean that content is always valuable.
[39:24] mean that content is always valuable.
[39:24] mean that content is always valuable. Um, use MCP servers or CLI commands or
[39:28] Um, use MCP servers or CLI commands or
[39:28] Um, use MCP servers or CLI commands or whatever tools you want to use um, to
[39:30] whatever tools you want to use um, to
[39:30] whatever tools you want to use um, to create developer documentation where it
[39:32] create developer documentation where it
[39:32] create developer documentation where it matters. So I talked a little bit about
[39:34] matters. So I talked a little bit about
[39:34] matters. So I talked a little bit about architectural decision records maybe
[39:36] architectural decision records maybe
[39:36] architectural decision records maybe storing that somewhere like Azure DevOps
[39:38] storing that somewhere like Azure DevOps
[39:38] storing that somewhere like Azure DevOps or wikis.
[39:41] or wikis.
[39:41] or wikis. Awesome. Now I'm going to talk about
[39:43] Awesome. Now I'm going to talk about
[39:44] Awesome. Now I'm going to talk about agentic harness engineering. Who's heard
[39:46] agentic harness engineering. Who's heard
[39:46] agentic harness engineering. Who's heard of agentic harness engineering?
[39:49] of agentic harness engineering?
[39:49] of agentic harness engineering? Couple of hands. I'm going to speak on
[39:51] Couple of hands. I'm going to speak on
[39:51] Couple of hands. I'm going to speak on it purely from the perspective of coding
[39:55] it purely from the perspective of coding
[39:55] it purely from the perspective of coding um coding assistance. There are
[39:57] um coding assistance. There are
[39:57] um coding assistance. There are different perspectives of harness
[39:59] different perspectives of harness
[39:59] different perspectives of harness engineering depending on um whether it's
[40:01] engineering depending on um whether it's
[40:01] engineering depending on um whether it's coding assistants or or agents
[40:03] coding assistants or or agents
[40:03] coding assistants or or agents themselves but essentially the harness
[40:06] themselves but essentially the harness
[40:06] themselves but essentially the harness is everything in your AI agent setup
[40:08] is everything in your AI agent setup
[40:08] is everything in your AI agent setup except the model itself. Uh so the model
[40:11] except the model itself. Uh so the model
[40:11] except the model itself. Uh so the model will split controls into kind of two
[40:13] will split controls into kind of two
[40:13] will split controls into kind of two dimensions. So we have feed forward
[40:15] dimensions. So we have feed forward
[40:15] dimensions. So we have feed forward guides and essentially what they do is
[40:17] guides and essentially what they do is
[40:17] guides and essentially what they do is they steer the agent before it acts. So
[40:21] they steer the agent before it acts. So
[40:21] they steer the agent before it acts. So this includes stuff like your agent's MD
[40:23] this includes stuff like your agent's MD
[40:23] this includes stuff like your agent's MD files, any instructions, any skills,
[40:25] files, any instructions, any skills,
[40:25] files, any instructions, any skills, architectural docu documents, stuff like
[40:27] architectural docu documents, stuff like
[40:27] architectural docu documents, stuff like that. And then there are feedback
[40:29] that. And then there are feedback
[40:29] that. And then there are feedback sensors which kind of observe after the
[40:32] sensors which kind of observe after the
[40:32] sensors which kind of observe after the agent acts and then it helps with the
[40:34] agent acts and then it helps with the
[40:34] agent acts and then it helps with the selfcorrection. So these are llinters,
[40:36] selfcorrection. So these are llinters,
[40:36] selfcorrection. So these are llinters, tests, structural analysis or any
[40:38] tests, structural analysis or any
[40:38] tests, structural analysis or any inferential sensors like an AI code
[40:40] inferential sensors like an AI code
[40:40] inferential sensors like an AI code review.
[40:42] review.
[40:42] review. So computational controls there are two
[40:44] So computational controls there are two
[40:44] So computational controls there are two kind of controls sorry. So computational
[40:45] kind of controls sorry. So computational
[40:46] kind of controls sorry. So computational controls and uh inferential controls. So
[40:49] controls and uh inferential controls. So
[40:49] controls and uh inferential controls. So computational controls are really just
[40:51] computational controls are really just
[40:51] computational controls are really just deterministic and fast. So these are
[40:53] deterministic and fast. So these are
[40:53] deterministic and fast. So these are your kind of like type checkers,
[40:54] your kind of like type checkers,
[40:54] your kind of like type checkers, llinters, tests and your inferential
[40:57] llinters, tests and your inferential
[40:57] llinters, tests and your inferential controls are your controls that use
[41:00] controls are your controls that use
[41:00] controls are your controls that use large language models. So skills AI
[41:02] large language models. So skills AI
[41:02] large language models. So skills AI review agents, LLM as a judge pattern.
[41:05] review agents, LLM as a judge pattern.
[41:05] review agents, LLM as a judge pattern. So that LLM as a judge pattern that's an
[41:07] So that LLM as a judge pattern that's an
[41:07] So that LLM as a judge pattern that's an inferential uh control.
[41:10] inferential uh control.
[41:10] inferential uh control. Now the concept of harab harab of
[41:13] Now the concept of harab harab of
[41:14] Now the concept of harab harab of harness engineering, I was trying to say
[41:15] harness engineering, I was trying to say
[41:15] harness engineering, I was trying to say harnessability. um but that's a word
[41:17] harnessability. um but that's a word
[41:18] harnessability. um but that's a word that's probably been made up um is that
[41:20] that's probably been made up um is that
[41:20] that's probably been made up um is that not every codebase is equally can be
[41:23] not every codebase is equally can be
[41:23] not every codebase is equally can be equally harnessable. So for green field
[41:25] equally harnessable. So for green field
[41:25] equally harnessable. So for green field projects it's you know it's fairly easy
[41:27] projects it's you know it's fairly easy
[41:27] projects it's you know it's fairly easy to set up a harness for something that
[41:30] to set up a harness for something that
[41:30] to set up a harness for something that doesn't really exist. Um but for
[41:33] doesn't really exist. Um but for
[41:33] doesn't really exist. Um but for brownfield um brownfield uh projects
[41:36] brownfield um brownfield uh projects
[41:36] brownfield um brownfield uh projects where harness engineering is probably
[41:37] where harness engineering is probably
[41:37] where harness engineering is probably the most valuable, it's very difficult
[41:40] the most valuable, it's very difficult
[41:40] the most valuable, it's very difficult to kind of set up a harness for that
[41:42] to kind of set up a harness for that
[41:42] to kind of set up a harness for that because of all that technical debt that
[41:44] because of all that technical debt that
[41:44] because of all that technical debt that has been accumulated over time.
[41:47] has been accumulated over time.
[41:47] has been accumulated over time. Uh strongly type languages will help
[41:49] Uh strongly type languages will help
[41:49] Uh strongly type languages will help give you type checking as sensor u
[41:52] give you type checking as sensor u
[41:52] give you type checking as sensor u sensors for free. Uh schema first
[41:54] sensors for free. Uh schema first
[41:54] sensors for free. Uh schema first contracts will help kind of constrain
[41:56] contracts will help kind of constrain
[41:56] contracts will help kind of constrain agent output. uh if you have test as
[41:59] agent output. uh if you have test as
[41:59] agent output. uh if you have test as specs they provide more executable
[42:01] specs they provide more executable
[42:01] specs they provide more executable feedback. Um so when we think about
[42:04] feedback. Um so when we think about
[42:04] feedback. Um so when we think about everything as code where we tra
[42:06] everything as code where we tra
[42:06] everything as code where we tra traditionally kind of treat that as okay
[42:08] traditionally kind of treat that as okay
[42:08] traditionally kind of treat that as okay I've got Azure policy that's defined as
[42:10] I've got Azure policy that's defined as
[42:10] I've got Azure policy that's defined as JSON files or I've got uh infrastructure
[42:12] JSON files or I've got uh infrastructure
[42:12] JSON files or I've got uh infrastructure as code so my entire application is just
[42:15] as code so my entire application is just
[42:15] as code so my entire application is just expressed as a template. uh from an
[42:17] expressed as a template. uh from an
[42:17] expressed as a template. uh from an enentic perspective, things like agent
[42:20] enentic perspective, things like agent
[42:20] enentic perspective, things like agent MD files, instructions and skills that
[42:22] MD files, instructions and skills that
[42:22] MD files, instructions and skills that are kind of codified, this matters
[42:24] are kind of codified, this matters
[42:24] are kind of codified, this matters because it helps your code uh codebase
[42:26] because it helps your code uh codebase
[42:26] because it helps your code uh codebase become more harnessable.
[42:31] So just to talk a little bit about feed
[42:32] So just to talk a little bit about feed uh feed forward and feedback mechanisms.
[42:34] uh feed forward and feedback mechanisms.
[42:34] uh feed forward and feedback mechanisms. Um so to harness a coding agent, we both
[42:36] Um so to harness a coding agent, we both
[42:36] Um so to harness a coding agent, we both anticipate unwanted outputs and then try
[42:39] anticipate unwanted outputs and then try
[42:39] anticipate unwanted outputs and then try to prevent them and then we essentially
[42:40] to prevent them and then we essentially
[42:40] to prevent them and then we essentially put sensors in place to allow the agent
[42:43] put sensors in place to allow the agent
[42:43] put sensors in place to allow the agent to self-correct.
[42:45] to self-correct.
[42:45] to self-correct. So feed forward controls like I
[42:47] So feed forward controls like I
[42:47] So feed forward controls like I mentioned earlier help anticipate the
[42:49] mentioned earlier help anticipate the
[42:49] mentioned earlier help anticipate the agents behavior and help to or aim to
[42:52] agents behavior and help to or aim to
[42:52] agents behavior and help to or aim to steer it before it acts. Uh and this
[42:56] steer it before it acts. Uh and this
[42:56] steer it before it acts. Uh and this guides are these guides are in place to
[42:57] guides are these guides are in place to
[42:57] guides are these guides are in place to help kind of increase the probability
[42:59] help kind of increase the probability
[42:59] help kind of increase the probability that the agent will create good results
[43:02] that the agent will create good results
[43:02] that the agent will create good results in the first couple of attempts.
[43:04] in the first couple of attempts.
[43:04] in the first couple of attempts. Whereas our feedback controls this is
[43:06] Whereas our feedback controls this is
[43:06] Whereas our feedback controls this is really after the agent acts and it helps
[43:08] really after the agent acts and it helps
[43:08] really after the agent acts and it helps self-correct. Uh this is particularly
[43:10] self-correct. Uh this is particularly
[43:10] self-correct. Uh this is particularly powerful when they uh provide uh signals
[43:12] powerful when they uh provide uh signals
[43:12] powerful when they uh provide uh signals that are optimized for large language
[43:14] that are optimized for large language
[43:14] that are optimized for large language model consumption. So this is custom
[43:16] model consumption. So this is custom
[43:16] model consumption. So this is custom llinter messages that include
[43:18] llinter messages that include
[43:18] llinter messages that include instructions for selfcorrection. Uh
[43:20] instructions for selfcorrection. Uh
[43:20] instructions for selfcorrection. Uh which is kind of like a positive kind of
[43:22] which is kind of like a positive kind of
[43:22] which is kind of like a positive kind of prompt injection. Everyone knows what
[43:24] prompt injection. Everyone knows what
[43:24] prompt injection. Everyone knows what prompt injection is getting some nods.
[43:26] prompt injection is getting some nods.
[43:26] prompt injection is getting some nods. Yeah, this is kind of a positive way of
[43:28] Yeah, this is kind of a positive way of
[43:28] Yeah, this is kind of a positive way of of using it. We'll think of a better
[43:29] of using it. We'll think of a better
[43:29] of using it. We'll think of a better term uh rather than prompt injection and
[43:31] term uh rather than prompt injection and
[43:31] term uh rather than prompt injection and keep our friends in security happy.
[43:34] keep our friends in security happy.
[43:34] keep our friends in security happy. um separately if you these things are
[43:37] um separately if you these things are
[43:37] um separately if you these things are kind of um implemented um well
[43:40] kind of um implemented um well
[43:40] kind of um implemented um well separately you can get even an agent
[43:41] separately you can get even an agent
[43:42] separately you can get even an agent that keeps um repeating the same
[43:43] that keeps um repeating the same
[43:43] that keeps um repeating the same mistakes. So you getting feedback only
[43:45] mistakes. So you getting feedback only
[43:45] mistakes. So you getting feedback only mechanisms. If you're only using
[43:46] mechanisms. If you're only using
[43:46] mechanisms. If you're only using feedback mechanisms, the agent is going
[43:48] feedback mechanisms, the agent is going
[43:48] feedback mechanisms, the agent is going to keep making those mistakes and you
[43:50] to keep making those mistakes and you
[43:50] to keep making those mistakes and you get the the dreaded you're absolutely
[43:52] get the the dreaded you're absolutely
[43:52] get the the dreaded you're absolutely right response from agents. Um or you'll
[43:55] right response from agents. Um or you'll
[43:55] right response from agents. Um or you'll have an agent that kind of encodes rules
[43:58] have an agent that kind of encodes rules
[43:58] have an agent that kind of encodes rules but never finds out whether they worked
[44:00] but never finds out whether they worked
[44:00] but never finds out whether they worked or not. So these two have to kind of
[44:02] or not. So these two have to kind of
[44:02] or not. So these two have to kind of work together.
[44:04] work together.
[44:04] work together. Now the human job in this is to steer
[44:07] Now the human job in this is to steer
[44:07] Now the human job in this is to steer the agent. Uh probably why we use the
[44:10] the agent. Uh probably why we use the
[44:10] the agent. Uh probably why we use the term co-pilot as a product name um a
[44:14] term co-pilot as a product name um a
[44:14] term co-pilot as a product name um a lot. Um but essentially that's what it
[44:17] lot. Um but essentially that's what it
[44:17] lot. Um but essentially that's what it is like the human job is really here to
[44:19] is like the human job is really here to
[44:19] is like the human job is really here to steer the agent to make sure that the
[44:22] steer the agent to make sure that the
[44:22] steer the agent to make sure that the harness is iterated on and we're making
[44:24] harness is iterated on and we're making
[44:24] harness is iterated on and we're making um our agents are making the right
[44:26] um our agents are making the right
[44:26] um our agents are making the right choices. So whenever an issue happens in
[44:28] choices. So whenever an issue happens in
[44:28] choices. So whenever an issue happens in multiple times, feed forward and
[44:30] multiple times, feed forward and
[44:30] multiple times, feed forward and feedback controls should be improved to
[44:32] feedback controls should be improved to
[44:32] feedback controls should be improved to make the issue less probable to occur in
[44:35] make the issue less probable to occur in
[44:35] make the issue less probable to occur in the future. It's not going to eliminate
[44:36] the future. It's not going to eliminate
[44:36] the future. It's not going to eliminate it entirely.
[44:38] it entirely.
[44:38] it entirely. Large language models are designed for
[44:40] Large language models are designed for
[44:40] Large language models are designed for positive reinforcement and engagement as
[44:42] positive reinforcement and engagement as
[44:42] positive reinforcement and engagement as Richard was saying yesterday. This
[44:43] Richard was saying yesterday. This
[44:43] Richard was saying yesterday. This applies in the coding field as well. Um
[44:46] applies in the coding field as well. Um
[44:46] applies in the coding field as well. Um but essentially these controls are there
[44:48] but essentially these controls are there
[44:48] but essentially these controls are there to try and prevent that as much as
[44:50] to try and prevent that as much as
[44:50] to try and prevent that as much as possible.
[44:52] possible.
[44:52] possible. Now in the steering loop you can use AI
[44:55] Now in the steering loop you can use AI
[44:55] Now in the steering loop you can use AI to improve the harness. It actually you
[44:57] to improve the harness. It actually you
[44:57] to improve the harness. It actually you know does it's essentially because
[44:59] know does it's essentially because
[44:59] know does it's essentially because harnesses can be just code that lives
[45:01] harnesses can be just code that lives
[45:01] harnesses can be just code that lives inside your repository. I've seen it
[45:03] inside your repository. I've seen it
[45:03] inside your repository. I've seen it implemented as a proper CLI tool. I've
[45:06] implemented as a proper CLI tool. I've
[45:06] implemented as a proper CLI tool. I've seen it um implemented as just extra
[45:08] seen it um implemented as just extra
[45:08] seen it um implemented as just extra agent skills instructions etc. Um but
[45:11] agent skills instructions etc. Um but
[45:12] agent skills instructions etc. Um but coding agents you know it they make it
[45:14] coding agents you know it they make it
[45:14] coding agents you know it they make it cheaper to build more custom controls
[45:15] cheaper to build more custom controls
[45:15] cheaper to build more custom controls and more custom analysis. So we can use
[45:18] and more custom analysis. So we can use
[45:18] and more custom analysis. So we can use agents to kind of improve the harness as
[45:20] agents to kind of improve the harness as
[45:20] agents to kind of improve the harness as well. I apologize for this meme. I'm not
[45:22] well. I apologize for this meme. I'm not
[45:22] well. I apologize for this meme. I'm not great at generating memes that are
[45:24] great at generating memes that are
[45:24] great at generating memes that are appropriate for conferences. Um, so
[45:26] appropriate for conferences. Um, so
[45:26] appropriate for conferences. Um, so yeah.
[45:28] yeah.
[45:28] yeah. Um, there's some examples. So, kind of
[45:31] Um, there's some examples. So, kind of
[45:31] Um, there's some examples. So, kind of feed forward mechanisms. These would be,
[45:33] feed forward mechanisms. These would be,
[45:33] feed forward mechanisms. These would be, uh, coding conventions, uh, instructions
[45:35] uh, coding conventions, uh, instructions
[45:35] uh, coding conventions, uh, instructions on how to bootstrap a new project. So,
[45:38] on how to bootstrap a new project. So,
[45:38] on how to bootstrap a new project. So, uh, using my, um, silly little lap as an
[45:41] uh, using my, um, silly little lap as an
[45:41] uh, using my, um, silly little lap as an example. It's all built on.net. So, I'm
[45:43] example. It's all built on.net. So, I'm
[45:43] example. It's all built on.net. So, I'm very opinionated. Use the net um CLI to
[45:46] very opinionated. Use the net um CLI to
[45:46] very opinionated. Use the net um CLI to kind of build new things. Make sure that
[45:48] kind of build new things. Make sure that
[45:48] kind of build new things. Make sure that tests are written in XUnit and they're
[45:51] tests are written in XUnit and they're
[45:51] tests are written in XUnit and they're all referred to each other within the
[45:52] all referred to each other within the
[45:52] all referred to each other within the solution file. And then your feedback uh
[45:55] solution file. And then your feedback uh
[45:55] solution file. And then your feedback uh mechanisms, instructions on how to
[45:57] mechanisms, instructions on how to
[45:57] mechanisms, instructions on how to review changes and also structural tests
[46:00] review changes and also structural tests
[46:00] review changes and also structural tests as well. So that could be implemented
[46:01] as well. So that could be implemented
[46:01] as well. So that could be implemented simply by using pre-commit hooks uh that
[46:04] simply by using pre-commit hooks uh that
[46:04] simply by using pre-commit hooks uh that run unit tests as part of a a git
[46:06] run unit tests as part of a a git
[46:06] run unit tests as part of a a git workflow.
[46:12] Now coming back to kind of how this kind
[46:12] Now coming back to kind of how this kind of works from a platform engineering
[46:13] of works from a platform engineering
[46:14] of works from a platform engineering perspective. So teams that are
[46:15] perspective. So teams that are
[46:15] perspective. So teams that are continuously integrating we've always
[46:17] continuously integrating we've always
[46:17] continuously integrating we've always had um a challenge of making sure that
[46:21] had um a challenge of making sure that
[46:21] had um a challenge of making sure that you know tests are implemented correctly
[46:23] you know tests are implemented correctly
[46:23] you know tests are implemented correctly uh the checks are in place human reviews
[46:25] uh the checks are in place human reviews
[46:25] uh the checks are in place human reviews are done particularly in organizations
[46:27] are done particularly in organizations
[46:27] are done particularly in organizations where you might have to change do you
[46:29] where you might have to change do you
[46:29] where you might have to change do you guys call it a change review board here
[46:32] guys call it a change review board here
[46:32] guys call it a change review board here as well that's a term we use a lot in
[46:34] as well that's a term we use a lot in
[46:34] as well that's a term we use a lot in Australia also cab as well um control
[46:36] Australia also cab as well um control
[46:36] Australia also cab as well um control architecture board essentially you know
[46:39] architecture board essentially you know
[46:39] architecture board essentially you know group of architects that sit around one
[46:40] group of architects that sit around one
[46:40] group of architects that sit around one of those tables and judge whether your
[46:43] of those tables and judge whether your
[46:43] of those tables and judge whether your um your code is deemed worthy enough to
[46:45] um your code is deemed worthy enough to
[46:45] um your code is deemed worthy enough to go into production. Um essentially
[46:49] go into production. Um essentially
[46:49] go into production. Um essentially um this has always been a challenge uh
[46:51] um this has always been a challenge uh
[46:51] um this has always been a challenge uh and particularly when you're trying to
[46:53] and particularly when you're trying to
[46:53] and particularly when you're trying to continuously deliver. Um essentially you
[46:57] continuously deliver. Um essentially you
[46:57] continuously deliver. Um essentially you ideally want every commit state to be
[46:59] ideally want every commit state to be
[46:59] ideally want every commit state to be deployable. So you'll want to have
[47:01] deployable. So you'll want to have
[47:01] deployable. So you'll want to have checks as far left in the path to
[47:02] checks as far left in the path to
[47:02] checks as far left in the path to production as possible. uh since the
[47:04] production as possible. uh since the
[47:04] production as possible. uh since the earlier you find issues the quicker you
[47:06] earlier you find issues the quicker you
[47:06] earlier you find issues the quicker you can actually do to resolve them and
[47:08] can actually do to resolve them and
[47:08] can actually do to resolve them and you're not going cap inand to security
[47:09] you're not going cap inand to security
[47:09] you're not going cap inand to security or legal or whoever to you know try and
[47:12] or legal or whoever to you know try and
[47:12] or legal or whoever to you know try and get your changes approved and this still
[47:14] get your changes approved and this still
[47:14] get your changes approved and this still applies in the agentic world as well so
[47:16] applies in the agentic world as well so
[47:16] applies in the agentic world as well so feedback sensors like I talked about um
[47:19] feedback sensors like I talked about um
[47:19] feedback sensors like I talked about um essentially need to be distributed
[47:21] essentially need to be distributed
[47:21] essentially need to be distributed accordingly across your life cycle
[47:24] accordingly across your life cycle
[47:24] accordingly across your life cycle um
[47:26] um
[47:26] um and you need to think about how
[47:29] and you need to think about how
[47:29] and you need to think about how uh like what's reasonably fast and
[47:30] uh like what's reasonably fast and
[47:30] uh like what's reasonably fast and what's um run even before we start
[47:32] what's um run even before we start
[47:32] what's um run even before we start integrating all our components
[47:33] integrating all our components
[47:33] integrating all our components components together or even before
[47:35] components together or even before
[47:35] components together or even before commit is created where an agent's do we
[47:38] commit is created where an agent's do we
[47:38] commit is created where an agent's do we need to make a commit? Do we need to
[47:39] need to make a commit? Do we need to
[47:39] need to make a commit? Do we need to push something to an environment before
[47:41] push something to an environment before
[47:42] push something to an environment before we start to integrate agentic feedback
[47:44] we start to integrate agentic feedback
[47:44] we start to integrate agentic feedback on our changes that we make? Um if you
[47:47] on our changes that we make? Um if you
[47:47] on our changes that we make? Um if you think about some of the coding
[47:48] think about some of the coding
[47:48] think about some of the coding conventions that you use day-to-day, can
[47:50] conventions that you use day-to-day, can
[47:50] conventions that you use day-to-day, can we kind of introduce that earlier? Uh so
[47:53] we kind of introduce that earlier? Uh so
[47:53] we kind of introduce that earlier? Uh so we might introduce um security code
[47:55] we might introduce um security code
[47:55] we might introduce um security code scanning is probably a better example.
[47:56] scanning is probably a better example.
[47:56] scanning is probably a better example. Can we do some sort of um security scans
[47:59] Can we do some sort of um security scans
[47:59] Can we do some sort of um security scans on our code using agents that are using
[48:01] on our code using agents that are using
[48:02] on our code using agents that are using skills that kind of um link up to our
[48:04] skills that kind of um link up to our
[48:04] skills that kind of um link up to our tools that we use day-to-day before we
[48:06] tools that we use day-to-day before we
[48:06] tools that we use day-to-day before we push it into a branch uh push it into a
[48:09] push it into a branch uh push it into a
[48:09] push it into a branch uh push it into a branch, deploy it to an environment and
[48:10] branch, deploy it to an environment and
[48:10] branch, deploy it to an environment and then everyone sees that our code is
[48:11] then everyone sees that our code is
[48:12] then everyone sees that our code is going to introduce some vulnerabilities.
[48:13] going to introduce some vulnerabilities.
[48:13] going to introduce some vulnerabilities. Can we pull that a little bit forward?
[48:21] Another thing that kind of what this
[48:21] Another thing that kind of what this kind of really introduces is a different
[48:23] kind of really introduces is a different
[48:23] kind of really introduces is a different type of continuous drift and and and
[48:25] type of continuous drift and and and
[48:25] type of continuous drift and and and health um health sensors that we need to
[48:27] health um health sensors that we need to
[48:28] health um health sensors that we need to do. Um
[48:30] do. Um
[48:30] do. Um so these are still all code artifacts
[48:32] so these are still all code artifacts
[48:32] so these are still all code artifacts that live in a repository somewhere. And
[48:35] that live in a repository somewhere. And
[48:35] that live in a repository somewhere. And I talked a little bit about versions uh
[48:37] I talked a little bit about versions uh
[48:37] I talked a little bit about versions uh for agent skills. You can imagine if
[48:39] for agent skills. You can imagine if
[48:39] for agent skills. You can imagine if you're working in a large organization,
[48:42] you're working in a large organization,
[48:42] you're working in a large organization, people are working or collaborating on
[48:44] people are working or collaborating on
[48:44] people are working or collaborating on different type of um agent skills. So
[48:46] different type of um agent skills. So
[48:46] different type of um agent skills. So different versions are going to be
[48:47] different versions are going to be
[48:48] different versions are going to be introduced. So which version is your
[48:50] introduced. So which version is your
[48:50] introduced. So which version is your team using particularly if you're using
[48:52] team using particularly if you're using
[48:52] team using particularly if you're using skills that are related to kind of
[48:53] skills that are related to kind of
[48:53] skills that are related to kind of security workflows. Have the security
[48:56] security workflows. Have the security
[48:56] security workflows. Have the security team introduced a new change to a
[48:58] team introduced a new change to a
[48:58] team introduced a new change to a particular skill, introduced a new
[48:59] particular skill, introduced a new
[49:00] particular skill, introduced a new version and is your team now going to be
[49:02] version and is your team now going to be
[49:02] version and is your team now going to be able to use that version or are they
[49:04] able to use that version or are they
[49:04] able to use that version or are they using that version? How do we detect
[49:05] using that version? How do we detect
[49:05] using that version? How do we detect that? I think some of the problems that
[49:07] that? I think some of the problems that
[49:07] that? I think some of the problems that we've kind of solved in the past are
[49:08] we've kind of solved in the past are
[49:08] we've kind of solved in the past are kind of reemerging just through a
[49:10] kind of reemerging just through a
[49:10] kind of reemerging just through a different artifact. Um I know that OWASP
[49:13] different artifact. Um I know that OWASP
[49:13] different artifact. Um I know that OWASP have a top 10 for agents. They've now
[49:16] have a top 10 for agents. They've now
[49:16] have a top 10 for agents. They've now introduced one I believe for agent
[49:17] introduced one I believe for agent
[49:17] introduced one I believe for agent skills as well because these are just
[49:19] skills as well because these are just
[49:19] skills as well because these are just kind of artifacts that are sitting in
[49:21] kind of artifacts that are sitting in
[49:21] kind of artifacts that are sitting in code repositories well which could
[49:22] code repositories well which could
[49:22] code repositories well which could introduce new vulnerabilities. So this
[49:24] introduce new vulnerabilities. So this
[49:24] introduce new vulnerabilities. So this is an area that's um area that is will
[49:28] is an area that's um area that is will
[49:28] is an area that's um area that is will be worth um worthwhile um to to look at
[49:34] be worth um worthwhile um to to look at
[49:34] be worth um worthwhile um to to look at and my clicker is having all kinds of um
[49:37] and my clicker is having all kinds of um
[49:37] and my clicker is having all kinds of um fun today. Um large language models are
[49:42] fun today. Um large language models are
[49:42] fun today. Um large language models are they partially handle the semantic
[49:44] they partially handle the semantic
[49:44] they partially handle the semantic issues uh semantic duplication redundant
[49:46] issues uh semantic duplication redundant
[49:46] issues uh semantic duplication redundant tests overengineering but this is quite
[49:49] tests overengineering but this is quite
[49:49] tests overengineering but this is quite expensive and it's very probabilistic as
[49:51] expensive and it's very probabilistic as
[49:51] expensive and it's very probabilistic as well um computational sensors they help
[49:54] well um computational sensors they help
[49:54] well um computational sensors they help catch kind of structural issues so
[49:56] catch kind of structural issues so
[49:56] catch kind of structural issues so duplication complexity coverage drift
[49:59] duplication complexity coverage drift
[49:59] duplication complexity coverage drift style things like that which are quite
[50:01] style things like that which are quite
[50:01] style things like that which are quite cheap to to to kind of solve but neither
[50:04] cheap to to to kind of solve but neither
[50:04] cheap to to to kind of solve but neither reliably catches kind of mix
[50:05] reliably catches kind of mix
[50:05] reliably catches kind of mix misdiagnosis unnecessary features
[50:08] misdiagnosis unnecessary features
[50:08] misdiagnosis unnecessary features or misunderstood instructions. I think
[50:10] or misunderstood instructions. I think
[50:10] or misunderstood instructions. I think you know depending on how you're
[50:12] you know depending on how you're
[50:12] you know depending on how you're prompting agents or kind of you know
[50:14] prompting agents or kind of you know
[50:14] prompting agents or kind of you know getting agents to do work we all know
[50:16] getting agents to do work we all know
[50:16] getting agents to do work we all know that you know slight wrong word can just
[50:19] that you know slight wrong word can just
[50:19] that you know slight wrong word can just kind of change the interpretation
[50:21] kind of change the interpretation
[50:21] kind of change the interpretation entirely and you get two different
[50:22] entirely and you get two different
[50:22] entirely and you get two different things. Uh so harnesses really the
[50:25] things. Uh so harnesses really the
[50:25] things. Uh so harnesses really the easiest kind of low hanging fruit
[50:26] easiest kind of low hanging fruit
[50:26] easiest kind of low hanging fruit harness today is really around
[50:27] harness today is really around
[50:27] harness today is really around maintainability.
[50:29] maintainability.
[50:29] maintainability. Um I use harnesses as well for
[50:32] Um I use harnesses as well for
[50:32] Um I use harnesses as well for architectural fitness as well. I think
[50:34] architectural fitness as well. I think
[50:34] architectural fitness as well. I think you know using guides and sensors for
[50:36] you know using guides and sensors for
[50:36] you know using guides and sensors for architectural characteristics
[50:39] architectural characteristics
[50:39] architectural characteristics um so performance requirements um
[50:41] um so performance requirements um
[50:41] um so performance requirements um observability con um conventions stuff
[50:44] observability con um conventions stuff
[50:44] observability con um conventions stuff like that we'll start to see become more
[50:46] like that we'll start to see become more
[50:46] like that we'll start to see become more sophisticated and more mature uh and
[50:49] sophisticated and more mature uh and
[50:49] sophisticated and more mature uh and then there's behavior harnesses as well.
[50:51] then there's behavior harnesses as well.
[50:51] then there's behavior harnesses as well. So most um most high autonomy setups
[50:55] So most um most high autonomy setups
[50:55] So most um most high autonomy setups will kind of use um specifications as
[50:57] will kind of use um specifications as
[50:57] will kind of use um specifications as feedbacks um and kind of uh green field
[51:01] feedbacks um and kind of uh green field
[51:01] feedbacks um and kind of uh green field projects uh with AI um or Greenfield AI
[51:03] projects uh with AI um or Greenfield AI
[51:03] projects uh with AI um or Greenfield AI generated test suite sorry um as
[51:05] generated test suite sorry um as
[51:06] generated test suite sorry um as feedbacks puts a lot of faith into AI
[51:08] feedbacks puts a lot of faith into AI
[51:08] feedbacks puts a lot of faith into AI written tests. I think there's still a
[51:10] written tests. I think there's still a
[51:10] written tests. I think there's still a lot of um we still need to have better
[51:13] lot of um we still need to have better
[51:13] lot of um we still need to have better behavioral harnesses before we can
[51:15] behavioral harnesses before we can
[51:15] behavioral harnesses before we can reduce the amount of supervision. I
[51:17] reduce the amount of supervision. I
[51:17] reduce the amount of supervision. I think hopefully a lot of us in the room
[51:19] think hopefully a lot of us in the room
[51:19] think hopefully a lot of us in the room who use AI coding assistants see tests
[51:22] who use AI coding assistants see tests
[51:22] who use AI coding assistants see tests that generate we do verify that they
[51:24] that generate we do verify that they
[51:24] that generate we do verify that they they work or they a pass and and and
[51:27] they work or they a pass and and and
[51:27] they work or they a pass and and and they they still make sense. Um hopefully
[51:29] they they still make sense. Um hopefully
[51:29] they they still make sense. Um hopefully that's a lot of you in the room. I'm not
[51:31] that's a lot of you in the room. I'm not
[51:31] that's a lot of you in the room. I'm not seeing a lot of nods. Maybe you're just
[51:32] seeing a lot of nods. Maybe you're just
[51:32] seeing a lot of nods. Maybe you're just falling asleep. There there's more nods.
[51:34] falling asleep. There there's more nods.
[51:34] falling asleep. There there's more nods. Thank you. Sorry I didn't shame you into
[51:36] Thank you. Sorry I didn't shame you into
[51:36] Thank you. Sorry I didn't shame you into responding to me. I just wanted to make
[51:38] responding to me. I just wanted to make
[51:38] responding to me. I just wanted to make sure you're testing your code. Um I
[51:40] sure you're testing your code. Um I
[51:40] sure you're testing your code. Um I don't think we're at the point where we
[51:41] don't think we're at the point where we
[51:41] don't think we're at the point where we can just reduce supervision quite yet. I
[51:44] can just reduce supervision quite yet. I
[51:44] can just reduce supervision quite yet. I think, you know, I'm I may just my
[51:47] think, you know, I'm I may just my
[51:47] think, you know, I'm I may just my opinion, I may always be the ones
[51:49] opinion, I may always be the ones
[51:49] opinion, I may always be the ones running my test locally just because I'm
[51:51] running my test locally just because I'm
[51:51] running my test locally just because I'm I'm like that. Maybe I'm getting older
[51:52] I'm like that. Maybe I'm getting older
[51:52] I'm like that. Maybe I'm getting older and, you know, worried about this shiny
[51:55] and, you know, worried about this shiny
[51:55] and, you know, worried about this shiny new thing that's, you know, going to
[51:57] new thing that's, you know, going to
[51:57] new thing that's, you know, going to replace me. Uh, no, just an opinion. Um,
[52:00] replace me. Uh, no, just an opinion. Um,
[52:00] replace me. Uh, no, just an opinion. Um, but I think overall when it comes to um
[52:02] but I think overall when it comes to um
[52:02] but I think overall when it comes to um the behavioral side of things, there's
[52:04] the behavioral side of things, there's
[52:04] the behavioral side of things, there's there's still a lot um of work to do.
[52:08] there's still a lot um of work to do.
[52:08] there's still a lot um of work to do. I've given up on my thing. Um, so I'm
[52:10] I've given up on my thing. Um, so I'm
[52:10] I've given up on my thing. Um, so I'm just going to put it there.
[52:12] just going to put it there.
[52:12] just going to put it there. So I've talked a lot about templates um
[52:16] So I've talked a lot about templates um
[52:16] So I've talked a lot about templates um really from when I associate templates
[52:18] really from when I associate templates
[52:18] really from when I associate templates with like pipeline templates or GitHub
[52:19] with like pipeline templates or GitHub
[52:19] with like pipeline templates or GitHub action workflows templating that
[52:21] action workflows templating that
[52:21] action workflows templating that infrastructure as code templates. I
[52:23] infrastructure as code templates. I
[52:23] infrastructure as code templates. I think one area that is going to grow is
[52:25] think one area that is going to grow is
[52:25] think one area that is going to grow is actually templating the harness itself
[52:27] actually templating the harness itself
[52:27] actually templating the harness itself because again we don't want to
[52:28] because again we don't want to
[52:28] because again we don't want to reintroduce that problem going oh my
[52:30] reintroduce that problem going oh my
[52:30] reintroduce that problem going oh my harness works on my machine. You want to
[52:32] harness works on my machine. You want to
[52:32] harness works on my machine. You want to make sure that the harness kind of works
[52:34] make sure that the harness kind of works
[52:34] make sure that the harness kind of works for your entire team and your entire
[52:36] for your entire team and your entire
[52:36] for your entire team and your entire organizations.
[52:37] organizations.
[52:37] organizations. Um, and a lot of this is done through
[52:40] Um, and a lot of this is done through
[52:40] Um, and a lot of this is done through codification already when we think about
[52:42] codification already when we think about
[52:42] codification already when we think about service templates. Um, these might
[52:45] service templates. Um, these might
[52:45] service templates. Um, these might evolve into harness templates in the
[52:47] evolve into harness templates in the
[52:47] evolve into harness templates in the future. So you might, excuse me, have a
[52:50] future. So you might, excuse me, have a
[52:50] future. So you might, excuse me, have a template that's, um, attached to a
[52:52] template that's, um, attached to a
[52:52] template that's, um, attached to a particular coding agent. You might have
[52:54] particular coding agent. You might have
[52:54] particular coding agent. You might have a template that's uh, conforming to a
[52:57] a template that's uh, conforming to a
[52:57] a template that's uh, conforming to a particular text stack. It'll be
[52:59] particular text stack. It'll be
[52:59] particular text stack. It'll be interesting to see where we go uh, in
[53:01] interesting to see where we go uh, in
[53:01] interesting to see where we go uh, in this in this little silly little project
[53:03] this in this little silly little project
[53:03] this in this little silly little project that I have. My harness kind of covers
[53:05] that I have. My harness kind of covers
[53:05] that I have. My harness kind of covers everything. Um I'm not sure if that's
[53:08] everything. Um I'm not sure if that's
[53:08] everything. Um I'm not sure if that's the right way to go. It works for me
[53:09] the right way to go. It works for me
[53:09] the right way to go. It works for me because I'm a single developer working
[53:10] because I'm a single developer working
[53:10] because I'm a single developer working on that single um application. Um but
[53:13] on that single um application. Um but
[53:13] on that single um application. Um but teams may start picking tech stacks and
[53:15] teams may start picking tech stacks and
[53:16] teams may start picking tech stacks and structures based purely on how well or
[53:18] structures based purely on how well or
[53:18] structures based purely on how well or how sophisticated a particular harness
[53:20] how sophisticated a particular harness
[53:20] how sophisticated a particular harness is uh within their organization.
[53:28] One thing I do want to kind of finish on
[53:28] One thing I do want to kind of finish on since uh leave some time for questions.
[53:31] since uh leave some time for questions.
[53:31] since uh leave some time for questions. Um, I will take a bet and humans will
[53:35] Um, I will take a bet and humans will
[53:35] Um, I will take a bet and humans will always need to be in the loop. I think
[53:37] always need to be in the loop. I think
[53:37] always need to be in the loop. I think people are now starting to realize that
[53:39] people are now starting to realize that
[53:39] people are now starting to realize that the act of writing code itself, while it
[53:41] the act of writing code itself, while it
[53:41] the act of writing code itself, while it was at times the most fun part of it,
[53:44] was at times the most fun part of it,
[53:44] was at times the most fun part of it, um, maybe not so fun when you're getting
[53:45] um, maybe not so fun when you're getting
[53:46] um, maybe not so fun when you're getting a paged at 3:00 in the morning, you have
[53:47] a paged at 3:00 in the morning, you have
[53:47] a paged at 3:00 in the morning, you have to try and resolve a bug in production,
[53:49] to try and resolve a bug in production,
[53:49] to try and resolve a bug in production, but coding 90% of the time for me was a
[53:51] but coding 90% of the time for me was a
[53:51] but coding 90% of the time for me was a lot of fun. Um, I'm still of the opinion
[53:56] lot of fun. Um, I'm still of the opinion
[53:56] lot of fun. Um, I'm still of the opinion that, you know, agents will help amplify
[53:59] that, you know, agents will help amplify
[53:59] that, you know, agents will help amplify um, our productivity, but I think now
[54:01] um, our productivity, but I think now
[54:02] um, our productivity, but I think now we're starting to, we've gone a little
[54:04] we're starting to, we've gone a little
[54:04] we're starting to, we've gone a little bit past the wild west of coding agents
[54:05] bit past the wild west of coding agents
[54:06] bit past the wild west of coding agents where we're just kind of letting cursor
[54:07] where we're just kind of letting cursor
[54:07] where we're just kind of letting cursor write our applications for us and then
[54:09] write our applications for us and then
[54:09] write our applications for us and then we just drop a bunch of money to to
[54:11] we just drop a bunch of money to to
[54:11] we just drop a bunch of money to to delete our data. I think we're past
[54:13] delete our data. I think we're past
[54:13] delete our data. I think we're past that. Um, we will write less code, but
[54:16] that. Um, we will write less code, but
[54:16] that. Um, we will write less code, but our skills as architects, as system
[54:19] our skills as architects, as system
[54:19] our skills as architects, as system designers, UX experts, um, they're just
[54:22] designers, UX experts, um, they're just
[54:22] designers, UX experts, um, they're just our skills are going to be amplified in
[54:24] our skills are going to be amplified in
[54:24] our skills are going to be amplified in a different way because AI will always
[54:25] a different way because AI will always
[54:26] a different way because AI will always make mistakes, even ones like this.
[54:32] Oh, there's some lots. There's some
[54:32] Oh, there's some lots. There's some lots. Fantastic. It's a terrible joke.
[54:34] lots. Fantastic. It's a terrible joke.
[54:34] lots. Fantastic. It's a terrible joke. Don't laugh at it. [snorts]
[54:37] Don't laugh at it. [snorts]
[54:37] Don't laugh at it. [snorts] So despite the advances in technology
[54:39] So despite the advances in technology
[54:39] So despite the advances in technology and model capability, uh still requires
[54:42] and model capability, uh still requires
[54:42] and model capability, uh still requires a lot of oversight, uh the one takeaway
[54:45] a lot of oversight, uh the one takeaway
[54:45] a lot of oversight, uh the one takeaway um that I'd like to leave you all with
[54:48] um that I'd like to leave you all with
[54:48] um that I'd like to leave you all with today is that AI is an amplifier. It's
[54:50] today is that AI is an amplifier. It's
[54:50] today is that AI is an amplifier. It's not a silver bullet. Having those high
[54:53] not a silver bullet. Having those high
[54:53] not a silver bullet. Having those high quality or um good engineering
[54:55] quality or um good engineering
[54:55] quality or um good engineering fundamentals will help out a amplify how
[54:58] fundamentals will help out a amplify how
[54:58] fundamentals will help out a amplify how AI and agents work within your
[55:00] AI and agents work within your
[55:00] AI and agents work within your organization. If you don't have those
[55:02] organization. If you don't have those
[55:02] organization. If you don't have those kind of basic foundations, you're going
[55:05] kind of basic foundations, you're going
[55:05] kind of basic foundations, you're going to start to see some some chaos within
[55:07] to start to see some some chaos within
[55:07] to start to see some some chaos within your environment, which is not what what
[55:09] your environment, which is not what what
[55:09] your environment, which is not what what anyone wants. Um, so it is worth just to
[55:12] anyone wants. Um, so it is worth just to
[55:12] anyone wants. Um, so it is worth just to take a second to think, okay, how are we
[55:14] take a second to think, okay, how are we
[55:14] take a second to think, okay, how are we going to apply this to our team? Because
[55:16] going to apply this to our team? Because
[55:16] going to apply this to our team? Because harnessability is not like a, oh, I'm
[55:18] harnessability is not like a, oh, I'm
[55:18] harnessability is not like a, oh, I'm going to buy a harness and that's it.
[55:20] going to buy a harness and that's it.
[55:20] going to buy a harness and that's it. It's how that works for your
[55:21] It's how that works for your
[55:21] It's how that works for your organization, for your codebase, and for
[55:24] organization, for your codebase, and for
[55:24] organization, for your codebase, and for your team.
[55:26] your team.
[55:26] your team. Awesome. Thank you so much for listening
[55:28] Awesome. Thank you so much for listening
[55:28] Awesome. Thank you so much for listening to me today. I know you're all very
[55:29] to me today. I know you're all very
[55:29] to me today. I know you're all very hungry and it's very hot up here. I am
[55:31] hungry and it's very hot up here. I am
[55:32] hungry and it's very hot up here. I am sweating. I'm That's why I'm keeping my
[55:33] sweating. I'm That's why I'm keeping my
[55:33] sweating. I'm That's why I'm keeping my arms here because this is a gray
[55:35] arms here because this is a gray
[55:35] arms here because this is a gray t-shirt. Uh if you would like to connect
[55:38] t-shirt. Uh if you would like to connect
[55:38] t-shirt. Uh if you would like to connect with me, please scan that QR code. The
[55:41] with me, please scan that QR code. The
[55:41] with me, please scan that QR code. The great thing about having a name like
[55:42] great thing about having a name like
[55:42] great thing about having a name like Wolver is that's the only Wolver I know.
[55:45] Wolver is that's the only Wolver I know.
[55:45] Wolver is that's the only Wolver I know. So on LinkedIn, GitHub, Blue Sky. Um
[55:49] So on LinkedIn, GitHub, Blue Sky. Um
[55:49] So on LinkedIn, GitHub, Blue Sky. Um yeah, please connect with me. Um thank
[55:51] yeah, please connect with me. Um thank
[55:51] yeah, please connect with me. Um thank you so much for your time and hope you
[55:53] you so much for your time and hope you
[55:53] you so much for your time and hope you have a wonderful second day afternoon at
[55:55] have a wonderful second day afternoon at
[55:55] have a wonderful second day afternoon at NDC.
[55:56] NDC.
[55:56] NDC. [applause]
[56:36] I think [snorts] so. The question was
[56:36] I think [snorts] so. The question was for and let me know if I get this wrong.
[56:39] for and let me know if I get this wrong.
[56:39] for and let me know if I get this wrong. Um I have domain knowledge or you have
[56:42] Um I have domain knowledge or you have
[56:42] Um I have domain knowledge or you have domain knowledge that's not easily
[56:44] domain knowledge that's not easily
[56:44] domain knowledge that's not easily shared within a codebase. Uh, so you
[56:46] shared within a codebase. Uh, so you
[56:46] shared within a codebase. Uh, so you can't just write up a markdown down file
[56:48] can't just write up a markdown down file
[56:48] can't just write up a markdown down file and expose that as a skill. Um, my
[56:51] and expose that as a skill. Um, my
[56:51] and expose that as a skill. Um, my answer to that is I I think MCP servers
[56:54] answer to that is I I think MCP servers
[56:54] answer to that is I I think MCP servers are pretty powerful for that. So if that
[56:57] are pretty powerful for that. So if that
[56:57] are pretty powerful for that. So if that documentation lives somewhere, hopefully
[56:59] documentation lives somewhere, hopefully
[56:59] documentation lives somewhere, hopefully not SharePoint. No, I'm joking. Um, but
[57:02] not SharePoint. No, I'm joking. Um, but
[57:02] not SharePoint. No, I'm joking. Um, but if that lives somewhere and a developer
[57:04] if that lives somewhere and a developer
[57:04] if that lives somewhere and a developer essentially with kind of like aentic
[57:07] essentially with kind of like aentic
[57:07] essentially with kind of like aentic coding, the idea is not to break your
[57:09] coding, the idea is not to break your
[57:09] coding, the idea is not to break your flow. So the idea is if you can do
[57:11] flow. So the idea is if you can do
[57:11] flow. So the idea is if you can do everything inside an IDE or a terminal
[57:13] everything inside an IDE or a terminal
[57:13] everything inside an IDE or a terminal and you can call out without actually
[57:15] and you can call out without actually
[57:15] and you can call out without actually having to leave that it's it's going to
[57:18] having to leave that it's it's going to
[57:18] having to leave that it's it's going to be uh that's the whole point of it. So
[57:20] be uh that's the whole point of it. So
[57:20] be uh that's the whole point of it. So if you can if you have an MTP server
[57:23] if you can if you have an MTP server
[57:23] if you can if you have an MTP server that can grab that institutional
[57:24] that can grab that institutional
[57:24] that can grab that institutional knowledge and then um put that into the
[57:27] knowledge and then um put that into the
[57:27] knowledge and then um put that into the context for an agent, I think that's a
[57:29] context for an agent, I think that's a
[57:29] context for an agent, I think that's a good way of way to go because
[57:31] good way of way to go because
[57:31] good way of way to go because essentially it's just a REST call to
[57:32] essentially it's just a REST call to
[57:32] essentially it's just a REST call to something that lives somewhere. It
[57:34] something that lives somewhere. It
[57:34] something that lives somewhere. It doesn't have to be any more complicated
[57:35] doesn't have to be any more complicated
[57:35] doesn't have to be any more complicated than that.
[57:38] than that.
[57:38] than that. Uh yes.
[57:40] Uh yes.
[57:40] Uh yes. &gt;&gt; Yeah.
[58:01] about
[58:01] about that.
[58:56] Yeah. So just to kind of paraphrase, so
[58:56] Yeah. So just to kind of paraphrase, so um harness engineering is really just
[58:59] um harness engineering is really just
[58:59] um harness engineering is really just trying to make uh add more constraints.
[59:01] trying to make uh add more constraints.
[59:01] trying to make uh add more constraints. You you said that in a way that's that's
[59:03] You you said that in a way that's that's
[59:03] You you said that in a way that's that's that's logical. Um
[59:06] that's logical. Um
[59:06] that's logical. Um did I get that right or
[59:08] did I get that right or
[59:08] did I get that right or &gt;&gt; Yeah.
[59:14] &gt;&gt; Yeah.
[59:14] &gt;&gt; Yeah. &gt;&gt; Yeah. So it's essentially guarding for a
[59:17] &gt;&gt; Yeah. So it's essentially guarding for a
[59:17] &gt;&gt; Yeah. So it's essentially guarding for a successful outcome. Yeah. That's that's
[59:19] successful outcome. Yeah. That's that's
[59:19] successful outcome. Yeah. That's that's yeah I I agree with you on that. I think
[59:22] yeah I I agree with you on that. I think
[59:22] yeah I I agree with you on that. I think Agentic the problem it sounds like this
[59:25] Agentic the problem it sounds like this
[59:25] Agentic the problem it sounds like this it's this wonderful new thing where I
[59:27] it's this wonderful new thing where I
[59:27] it's this wonderful new thing where I think it even as developers before
[59:30] think it even as developers before
[59:30] think it even as developers before agents came onto the scene we had that
[59:32] agents came onto the scene we had that
[59:32] agents came onto the scene we had that harness anyway. So it's really just
[59:35] harness anyway. So it's really just
[59:35] harness anyway. So it's really just codifying the constraints of our current
[59:38] codifying the constraints of our current
[59:38] codifying the constraints of our current environments or our development
[59:39] environments or our development
[59:39] environments or our development environments to ensure that agents
[59:41] environments to ensure that agents
[59:41] environments to ensure that agents produce an outcome that we recognize and
[59:44] produce an outcome that we recognize and
[59:44] produce an outcome that we recognize and we know is successful and we know is
[59:46] we know is successful and we know is
[59:46] we know is successful and we know is well successful within the parameters of
[59:48] well successful within the parameters of
[59:48] well successful within the parameters of our environment. So I think it's taken
[59:50] our environment. So I think it's taken
[59:50] our environment. So I think it's taken us surprisingly a long time to get
[59:52] us surprisingly a long time to get
[59:52] us surprisingly a long time to get there. Um whether that's intentional or
[59:55] there. Um whether that's intentional or
[59:56] there. Um whether that's intentional or not, I'm not going to I'm not going to
[59:57] not, I'm not going to I'm not going to
[59:57] not, I'm not going to I'm not going to comment. But I'm hopeful that now
[60:01] comment. But I'm hopeful that now
[60:02] comment. But I'm hopeful that now we're heading in the right direction
[60:03] we're heading in the right direction
[60:03] we're heading in the right direction from a um an AI assisted coding
[60:05] from a um an AI assisted coding
[60:05] from a um an AI assisted coding perspective. I think one of the big
[60:07] perspective. I think one of the big
[60:07] perspective. I think one of the big challenges to kind of solve is how to
[60:10] challenges to kind of solve is how to
[60:10] challenges to kind of solve is how to how we're going to pay for all of this
[60:12] how we're going to pay for all of this
[60:12] how we're going to pay for all of this and how um the billing model actually
[60:14] and how um the billing model actually
[60:14] and how um the billing model actually works uh with that. Whether this um
[60:17] works uh with that. Whether this um
[60:18] works uh with that. Whether this um helps with that or whether it amplifies
[60:19] helps with that or whether it amplifies
[60:19] helps with that or whether it amplifies it, I'm I'm not too sure. Um cuz yeah I
[60:23] it, I'm I'm not too sure. Um cuz yeah I
[60:24] it, I'm I'm not too sure. Um cuz yeah I think it's that problem hasn't been
[60:26] think it's that problem hasn't been
[60:26] think it's that problem hasn't been solved yet. Um but luckily I don't have
[60:29] solved yet. Um but luckily I don't have
[60:29] solved yet. Um but luckily I don't have to solve it.
[60:59] &gt;&gt; Sorry, what was the last part of
[60:59] &gt;&gt; Sorry, what was the last part of How do we
[61:16] &gt;&gt; So the question is, do you think we'll
[61:16] &gt;&gt; So the question is, do you think we'll see a move towards more standardization
[61:18] see a move towards more standardization
[61:18] see a move towards more standardization or more specializations from a platform
[61:20] or more specializations from a platform
[61:20] or more specializations from a platform engineering perspective? You're going to
[61:21] engineering perspective? You're going to
[61:21] engineering perspective? You're going to hate this answer. I think it depends is
[61:23] hate this answer. I think it depends is
[61:23] hate this answer. I think it depends is still a really good answer here. The
[61:25] still a really good answer here. The
[61:25] still a really good answer here. The only reason why is different levels of
[61:27] only reason why is different levels of
[61:27] only reason why is different levels of maturity and also different kind of
[61:29] maturity and also different kind of
[61:30] maturity and also different kind of enterprises as well. So Microsoft is a
[61:32] enterprises as well. So Microsoft is a
[61:32] enterprises as well. So Microsoft is a large organization with lots of
[61:33] large organization with lots of
[61:33] large organization with lots of developer teams. There may be some of
[61:35] developer teams. There may be some of
[61:35] developer teams. There may be some of you here who are working in very small
[61:37] you here who are working in very small
[61:38] you here who are working in very small startups. Our harnesses or our platforms
[61:40] startups. Our harnesses or our platforms
[61:40] startups. Our harnesses or our platforms are going to be very different to one
[61:41] are going to be very different to one
[61:41] are going to be very different to one another because startups don't need to
[61:44] another because startups don't need to
[61:44] another because startups don't need to be so complex. They don't need all these
[61:46] be so complex. They don't need all these
[61:46] be so complex. They don't need all these layers of complexity. Um just to
[61:48] layers of complexity. Um just to
[61:48] layers of complexity. Um just to generalize it. I know it's different.
[61:50] generalize it. I know it's different.
[61:50] generalize it. I know it's different. Again, it depends. Um, I think whatever
[61:53] Again, it depends. Um, I think whatever
[61:54] Again, it depends. Um, I think whatever works for your team to help amplify
[61:57] works for your team to help amplify
[61:57] works for your team to help amplify that's whatever form that takes that's
[61:59] that's whatever form that takes that's
[61:59] that's whatever form that takes that's where we'll we'll head.
[62:02] where we'll we'll head.
[62:02] where we'll we'll head. Awesome. Thank you.
[62:04] Awesome. Thank you.
[62:04] Awesome. Thank you. Any more?
[62:11] Awesome. Thank you so much. Enjoy lunch.
[62:11] Awesome. Thank you so much. Enjoy lunch. [applause]
