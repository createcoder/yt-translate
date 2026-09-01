# Stop Writing Prompts. Start Writing Specs.

- **Video:** https://www.youtube.com/watch?v=Orr7qadkZD8
- **Generated:** 2026-08-31 20:57 UTC
- **Status:** Completed

## Technical brief

# Consolidated Technical Brief: Spec-Driven AI Development with GitHub Copilot, SpecKit, and MCP

## Executive takeaway

The speaker demonstrates a **specification-driven approach to AI-assisted software development** using **GitHub Copilot in VS Code** and a tool referred to as **SpecKit / Specify CLI** (exact naming and command syntax should be validated). Rather than moving directly from a private developer prompt to generated code, the workflow creates a version-controlled chain of artifacts:

```text
Constitution → Functional specification → Technical plan → Tasks → Implementation → Tests/validation
```

The demonstration uses this approach to generate a local **HTTP-based Model Context Protocol (MCP) server** for querying Microsoft Build session data. The generated server is inspected locally using an MCP Inspector and exposes tools such as session search, session lookup, and time-oriented session queries.

The central enterprise value is **not autonomous code generation or MCP specifically**. It is the creation of durable, reviewable requirements, architecture decisions, AI instructions, tasks, code, and tests in Git. This could improve traceability and governance for Superior Propane teams building Azure AI Foundry applications, Databricks-backed data services, Azure-hosted APIs, and agent/tool integrations.

> **Speaker claim:** Prompt-first coding is useful for rapid adoption but is a weak foundation for larger enterprise work because prompts are private, transient, difficult to review, and can produce code that compiles without meeting the intended outcome.  
> **Established engineering fact:** Version-controlled requirements, designs, pull-request review, tests, and deployment evidence are standard governance practices.  
> **Not established by the demo:** That SpecKit, generated specifications, generated tests, or MCP output are inherently secure, compliant, production-ready, Azure-native, or less costly than existing delivery practices.

The video does not demonstrate Azure deployment, Azure AI Foundry integration, Databricks connectivity, Unity Catalog controls, Entra ID, CI/CD controls, model/provider data handling, production observability, performance testing, or cost outcomes.

---

## Technical details

### Tooling and demo context

The speaker names or demonstrates:

- **GitHub Enterprise**
- **GitHub Copilot**
- **Visual Studio Code**
- **SpecKit / Specify CLI** — terminology and exact commands are uncertain from the transcript
- **MCP (Model Context Protocol)**
- **MCP Inspector**, run locally as a Node.js module
- **Node.js** and **TypeScript** for the example server
- A **Dockerfile** generated as part of implementation
- A source data set containing Microsoft Build session information in JSON

The example begins with a session-planner CLI that reportedly lacks MCP support. The resulting MCP server exposes event/session data to an AI client through tools including:

- `search_sessions`
- `get_session`
- `get_happenings`
- A time-oriented tool, transcribed as something like `get_next_times`; exact name is uncertain

The example returns information such as an opening keynote from event data. This is a local functional demonstration only.

### Development lifecycle

#### 1. Constitution: durable engineering and safety principles

The workflow starts with a project “constitution”: a small, living set of non-negotiable engineering and safety rules. The speaker suggests beginning with approximately two to five principles and evolving them based on team learning and enterprise standards.

The demo constitution for the MCP session-planning service includes:

1. **Grounded data only**
   - Do not invent sessions that do not exist in source data.

2. **Time-aware correctness**
   - Handle time accurately, especially for concepts such as “currently active” or “starting soon.”

3. **Agent-safe tool design**
   - Tools exposed to agents should be designed with safety in mind.

4. **HTTP safety**
   - The HTTP interface must be safe to expose, particularly if deployed to a public endpoint.

5. **Testable by design**
   - Architecture should support testing from the outset.

6. **Privacy by default**
   - Preserve privacy even when the sample data is public.

The presenter describes the constitution as a Markdown artifact generated under a project memory location resembling:

```text
specify/memory/
```

> **Speaker claim:** The workflow incorporates supplied principles into a constitution and uses it while producing downstream specifications, plans, and tasks.  
> **Important limitation:** Markdown instructions are not a security boundary and do not independently enforce policy. An LLM can misinterpret or fail to follow instructions; enforcement must remain in architecture, CI/CD, identity, networking, and runtime controls.

#### 2. Initialization and repository structure

The presenter initializes the framework in a project directory using a command described as:

```text
specify init
```

The shown initialization flow includes:

1. Install the SpecKit/Specify CLI.
2. Run initialization in the target project directory.
3. Select the AI integration, in this case **GitHub Copilot**.
4. Select a scripting shell/language:
   - Bash
   - PowerShell
   - Python
5. The speaker selects **PowerShell** on Windows.
6. The tool reportedly checks prerequisites, configures tool-specific instructions, provides credential/token guidance, and creates a `specify` project folder.

The repository is described as containing Markdown, scripts, VS Code-specific content, `.gitignore`, a `.github` folder, and Copilot instruction files.

The speaker emphasizes that the framework is transparent rather than “magic”: it consists primarily of **project-local Markdown templates/instructions and scripts** that can be inspected and modified.

> **Needs validation:** Official documentation, licensing, current CLI syntax, supported GitHub Copilot integration, authentication/token handling, generated file structure, and release/support status.

#### 3. Specify phase: functional requirements

The **specify** phase captures what should be built, without prematurely deciding how it will be implemented.

For the demo MCP server, the functional requirements include:

- Loading or accessing Microsoft Build session data from JSON.
- Searching sessions.
- Retrieving session details.
- Identifying sessions currently happening or otherwise time-relevant.

The presenter invokes a slash command resembling:

```text
/speckit specify
```

The framework is said to compare the functional specification with the constitution, then either identify ambiguity or ask clarification questions. The resulting spec is stored as Markdown under a `specs` folder and includes user stories such as session search, session-detail lookup, and currently active sessions.

This is a lightweight, repository-backed requirements-management approach. It is not a formal specification language, executable proof, or guarantee that requirements are complete.

#### 4. Plan phase: technical design decisions

The **plan** phase records implementation choices and constraints. In the demonstration, these include:

- **Language:** TypeScript
- **Runtime:** Node.js
- **Protocol:** MCP server
- **Transport:** described as an HTTP-related transport; the transcript wording is unclear
- **Configuration approach**
- **Deployment target:** included in the prompt, though the exact target is not visible in the supplied material
- A generated **stateless HTTP server** design
- TypeScript and related version selections

The command is described as:

```text
/speckit plan
```

The plan is generated from the constitution, functional specification, and technical prompt, then written into the relevant feature `specs` area.

A useful caution from the speaker: if version requirements are not explicit, the AI may choose versions that are “current” but not necessarily latest, supported, approved, or secure.

**Implication:** Enterprise runtime, SDK, package, and framework versions should be centrally governed and explicitly referenced in the plan rather than accepting generated defaults.

#### 5. Tasks phase: implementation decomposition

The **tasks** phase breaks the plan into smaller development activities for an AI assistant or developer.

The command is described as:

```text
/speckit tasks
```

Tasks are stored as Markdown and organized into implementation phases. Examples shown include:

- Project/application boilerplate
- Node.js configuration
- Dependency setup
- Application requirements
- Creation of `package.json`

The intent is to prevent a coding assistant from attempting a large feature in one broad generation step.

#### 6. Clarify, analyze, and implement phases

The speaker describes optional intermediate steps resembling:

- `clarify`
- `analyze`
- `implement`

Exact command names are uncertain.

The implementation phase converts tasks into generated source code. The presenter claims this process can generate:

- Application source code
- MCP tool definitions
- Application prerequisites
- A Dockerfile
- Tests, when “testable by design” is explicitly included in the constitution/specification

The speaker’s advice is to review every generated artifact, especially the constitution, specification, plan, tasks, source code, Dockerfile, and tests.

#### 7. Local inspection and validation

The generated MCP server is started locally and connected to the **MCP Inspector**.

The Inspector is used to:

- Connect to the server
- List available tools
- Inspect tool input fields
- Invoke tools
- Inspect returned results

This is a useful developer feedback loop, but it validates only a narrow happy path. A successful local Inspector call does not validate production security, performance, data governance, resilience, or enterprise integration.

### Repository traceability model

The principal governance benefit is that the following artifacts can reside in Git and be reviewed through normal code-review practices:

- Constitution and AI instructions
- Functional specifications
- Technical plans
- Task breakdowns
- Source code
- Tests
- Dockerfiles and deployment-related artifacts

This can create an auditable path:

```text
Business need
  → Functional behavior and acceptance criteria
    → Technical design and platform constraints
      → Tasks
        → Code and tests
          → Build/deployment evidence
```

The approach is valuable only if teams establish clear ownership and expectations for updating artifacts when requirements, code, or infrastructure change.

### Cost and operational trade-offs

The transcript provides no pricing or quantitative productivity data for:

- GitHub Enterprise
- GitHub Copilot
- SpecKit/Specify CLI
- Models or token consumption
- MCP hosting
- Azure infrastructure
- Databricks compute
- API gateway or telemetry
- Ongoing support

Likely trade-offs to measure:

| Potential benefit | Countervailing cost/risk |
|---|---|
| Better requirements clarity and traceability | More upfront time for specs, plans, and review |
| Faster boilerplate and task generation | Human effort to validate generated output |
| More consistent team guidance | Governance-template maintenance effort |
| Reusable implementation patterns | Risk of propagating flawed templates or dependencies |
| Earlier validation of ambiguity | AI-generated artifacts can still be incorrect or incomplete |
| Smaller implementation chunks | More workflow/process steps for small changes |

---

## Potential applications for Superior Propane

### 1. Standardize AI-assisted application delivery

The strongest application is a repeatable delivery model for AI-enabled solutions—not necessarily an immediate MCP adoption.

This can apply to:

- **Azure AI Foundry** assistants, RAG applications, and agent solutions
- Azure-hosted APIs and internal services
- Databricks-backed data products and analytics assistants
- Customer-service knowledge assistants
- Field-service or technician support tools
- Data-product discovery tools
- Internal operations, sales, contact-centre, and IT-support copilots

A standard artifact flow could be:

| Artifact | Superior Propane use |
|---|---|
| Constitution | Mandatory engineering, privacy, AI safety, data, Azure, and Databricks guardrails |
| Functional specification | User outcome, business rules, in/out of scope, acceptance criteria, failure behavior |
| Technical plan | Azure landing zone, identity, data sources, networking, observability, integrations, cost model |
| Tasks | Developer work, infrastructure-as-code work, test plans, evaluations, release tasks |
| Code/tests | Reviewed implementation and CI evidence |

This is especially useful for preventing vague requests such as “build an agent for delivery status” from moving directly into code without resolving access control, authoritative source systems, freshness, error behavior, and audit requirements.

### 2. Establish an AI/MCP constitution template

A Superior Propane baseline constitution could include requirements such as:

- No customer PII, credentials, secrets, or sensitive operational data in prompts, repositories, committed environment files, logs, test fixtures, or container images.
- Use **Microsoft Entra ID**, managed identities, and least-privilege service authorization.
- Use **Azure Key Vault** or an approved secret-management pattern.
- Access only approved, governed data interfaces.
- For Databricks sources, use **Unity Catalog-governed** tables, views, permissions, classifications, lineage, and certified data products where applicable.
- Use private networking, private endpoints, or restricted ingress where required by the data classification and workload.
- Ensure all tool/API calls are authorized server-side, independent of model instructions.
- Use read-only tool access by default.
- Require explicit human confirmation or workflow approval for consequential actions.
- Log tool invocation, identity, authorization decision, source-system correlation ID, outcome, and error state without over-logging sensitive data.
- Include unit, integration, contract, security, data-leakage, prompt-injection, and AI evaluation tests.
- Require infrastructure as code, dependency scanning, container scanning, SAST/SCA, pull-request approval, and controlled production release.
- Define performance targets, error behavior, support ownership, cost tags/budgets, and data-freshness expectations.

These controls should be translated into enforcement points, not left solely as Copilot instructions.

### 3. Governed MCP tool development

MCP may be useful if Superior Propane adopts AI clients that need controlled access to enterprise data or APIs. Suitable initial tools should be narrow, read-only, and built around business-specific operations rather than broad database access.

Potential low-risk starting points:

- Search approved operational procedures or safety documentation.
- Retrieve policy and process knowledge for internal support teams.
- Search a curated data-catalog metadata set.
- Retrieve certified metric definitions, owners, lineage, or data-quality status.
- Query synthetic or non-sensitive operational reference data.

Potential future tools, only after strong authorization and governance are proven:

- Permission-trimmed delivery/service status lookup.
- Technician asset/service-history lookup.
- Internal incident/event status lookup.
- Customer-account information retrieval for authorized service agents.

Suggested tool tiers:

| Tool tier | Example | Recommended access model |
|---|---|---|
| Read-only, low sensitivity | Public or approved internal documentation search | Broad internal access, rate limits, logging |
| Read-only, sensitive | Delivery/account/service lookup | User authentication, server-side RBAC/ABAC, audit trail |
| Write, reversible | Create a draft service case | Scoped authorization, confirmation, idempotency, workflow integration |
| Write, high impact | Change delivery, pricing, billing, payment, or credit status | Human approval, segregation of duties, strong audit, restricted roles |

Do not begin with tools that modify deliveries, dispatch, pricing, payments, customer records, or safety-related processes.

### 4. Grounded and time-aware AI applications

The demo’s grounding and time principles translate well to propane operations.

For any system answering questions about delivery, service, scheduling, account status, price, or operational events:

- Identify the authoritative source system for each answer type.
- Enforce retrieval-time entitlement filtering.
- Provide source, record timestamp, and freshness information where material.
- Prefer “no authorized/current data found” over inferred answers.
- Define how conflicting source data is handled.
- Specify canonical time practices:
  - UTC storage convention
  - User-local display convention
  - Location-to-time-zone mapping
  - Daylight-saving handling
  - Service windows and operational cutoffs
  - Definition of “today,” “tomorrow,” “currently,” and “starting soon”
  - Late-arriving source events and freshness SLA

A grounded answer can still be stale, unauthorized, incomplete, or misinterpreted. Retrieval alone does not establish correctness.

### 5. Azure implementation implications

The video does not describe Azure architecture. For Superior Propane, a production-grade MCP or AI-service reference architecture would likely need to define:

- **Hosting:** approved Azure container/app platform, such as Azure Container Apps, App Service, AKS, or Functions, based on workload requirements.
- **Ingress:** private access by default for internal enterprise tools; public exposure only with explicit risk acceptance and controls.
- **Identity:** Entra ID, managed identities, user/delegated identity where appropriate, and workload identity.
- **API protection:** API Management, WAF/rate limiting where applicable, request validation, quotas, and consistent error handling.
- **Secrets/configuration:** Key Vault and managed configuration.
- **Networking:** VNet integration, private endpoints, controlled egress, and separation of development, test, and production.
- **Data governance:** Unity Catalog for Databricks sources; governed views and data products rather than unrestricted workspace/storage access.
- **Observability:** Azure Monitor/Application Insights or an approved central platform, with structured, privacy-conscious tool-call telemetry.
- **Delivery controls:** IaC, CI/CD, SAST, SCA, secret scanning, container scanning, artifact provenance, and policy checks.
- **Evaluation:** AI quality, grounding, tool-authorization, prompt-injection, harmful-output, load, timeout, retry, and failure-mode tests.

---

## Risks/validation questions

### Spec-driven workflow risks

#### Specifications are guidance, not enforcement

The presenter claims that the workflow uses the constitution when generating specs and plans. That does not prove that it enforces policy.

Validate:

- Which requirements are checked automatically before merge or deployment?
- Can a CI pipeline detect missing required sections such as data classification, threat model, cost estimate, test strategy, and support owner?
- Is constitution compliance assessed by deterministic checks, human review, LLM analysis, or all three?
- What is the process for exceptions and approvals?
- Who owns updates when the constitution, architecture, implementation, or deployed environment diverge?

Controls such as Azure Policy, RBAC, network segmentation, secret management, IaC checks, and CI gates remain necessary.

#### Artifact quality and review burden

AI can generate weak specifications, plans, tasks, tests, and code—not only weak implementation.

Questions:

- Who is accountable for approving each artifact?
- What changes require product, architecture, security, data-governance, or platform review?
- Is this workflow proportionate for small fixes and prototypes?
- How will specifications remain synchronized with code and deployed infrastructure?
- What Definition of Ready and Definition of Done will prevent non-functional requirements from being omitted?

### Dependency, package, and supply-chain governance

The speaker explicitly warns that generated plans may select versions not explicitly requested.

Validate:

- Are Node.js, TypeScript, MCP SDK, Azure SDK, and base image versions pinned to approved baselines?
- Is an SBOM generated?
- Are dependencies scanned and continuously monitored?
- Does CI reject vulnerable, unapproved, obsolete, or license-incompatible packages?
- Are container base images approved, patched, minimized, and scanned?
- Are build artifacts signed or otherwise managed under software supply-chain policy?

### MCP security and production design gaps

The video recognizes that MCP security/audit can be difficult but does not show an implementation.

Critical questions:

#### Identity and authorization
- Which MCP clients can connect?
- How does the client authenticate to the server?
- Can Entra ID identity be conveyed and validated?
- Is authorization evaluated on every server-side tool invocation?
- Is user identity propagated to downstream systems, or is a shared service identity used?
- How are account, region, role, tenant, and row/column entitlements enforced?

#### Tool safety
- Are tool inputs schema-validated, length-bounded, and protected against injection?
- Are tool outputs minimized and redacted?
- Are read and write capabilities separated?
- Are write operations idempotent where required?
- Can untrusted retrieved content influence tool selection or arguments?
- What controls reduce indirect prompt injection and confused-deputy scenarios?
- Are human confirmation and workflow approval required for consequential actions?

#### Network and API controls
- Is public exposure actually necessary?
- Can the service use private ingress and private endpoints?
- Is API Management, WAF, DDoS protection, rate limiting, throttling, and anomaly detection required?
- Are dev, test, and production resources isolated?
- Is egress controlled so the service cannot arbitrarily reach external systems?

#### Operations
- What Azure service will host the stateless HTTP server?
- How are autoscaling, concurrency, connection pooling, caching, timeout, retry, circuit-breaker, and back-pressure behaviors designed?
- What SLOs apply to each tool?
- How are tool schemas versioned and breaking changes managed?
- What is the incident-response and support ownership model?

“Stateless HTTP” can simplify horizontal scaling but does not itself make a service scalable, secure, or operationally sound.

### Data, grounding, privacy, and time risks

“Grounded data only” is valuable but insufficient.

Validate:

- What system is authoritative for each domain answer?
- What data freshness SLA applies?
- Are retrieval permissions enforced before data reaches the model?
- How does the solution behave when no data is found, data is stale, or sources conflict?
- Are citations, record IDs, source timestamps, and confidence/freshness information returned when appropriate?
- Are customer, payment, safety, and operational data classifications represented in the specification and runtime policy?
- What data is placed in prompts, model inputs, retrieval indexes, logs, traces, and evaluation datasets?
- Where are prompts, code, telemetry, and model requests processed and retained?

For time-related interactions, define and test UTC/local conversion, time zones, daylight-saving transitions, service windows, dispatch cutoffs, ambiguous dates, clock skew, and late-arriving operational events.

### Generated-code and testing limitations

A local MCP Inspector call shows that a server starts and responds. It does not establish:

- Functional completeness
- Correct business behavior
- Authorization correctness
- Prompt-injection resistance
- Privacy compliance
- Security posture
- Test quality or coverage
- Vulnerability posture
- Reliability under load
- Production deployment readiness

Generated tests may merely verify generated behavior rather than the intended business rule. Human review and independent test design remain required.

### Commercial and operating-model questions

The transcript offers no cost details. A pilot should model:

- GitHub Enterprise/Copilot licensing
- Model/token usage for specification, planning, code generation, revision, and testing
- CI runner, artifact, registry, and scanning costs
- Azure hosting, networking, API Management, monitoring, and log retention
- Databricks query/warehouse/compute costs where applicable
- Developer review, remediation, and support time
- Cost of maintaining templates, guardrails, approved versions, and reference architectures

Also validate whether the tool and Copilot configuration are approved for internal code, architecture, customer-related requirements, and operational process information under Superior Propane’s AI-use, privacy, procurement, and security policies.

---

## Action items

### 1. Validate the tooling before standardization

- Review official SpecKit/Specify CLI documentation, source repository, license, release cadence, roadmap, and support model.
- Confirm exact CLI commands, generated artifacts, Copilot integration behavior, and credential/token handling.
- Determine whether the tool is approved for use with Superior Propane source code, architecture information, and internal requirements.
- Treat preview or rapidly changing GitHub/Copilot capabilities separately from generally available features.

### 2. Establish a lightweight pilot

Select one bounded, read-only, low-sensitivity use case:

- Internal documentation search
- Curated policy/procedure assistant
- Databricks data-catalog metadata search
- Certified metric-definition and ownership lookup
- Synthetic operational-reference-data assistant

Avoid, initially:

- Customer record updates
- Delivery scheduling or dispatch changes
- Pricing, credit, billing, or payment actions
- Safety-critical operational decisions
- Broad direct access to production databases

Use a segregated non-production Azure environment and non-sensitive/synthetic data wherever feasible.

### 3. Create a Superior Propane AI-service constitution

Create a reusable baseline with domain-specific overlays for:

- Azure AI Foundry
- Azure API/MCP services
- Databricks-facing applications
- RAG and enterprise search solutions

Include security, privacy, identity, network, data classification, grounding, time handling, observability, testing, CI/CD, cost management, support ownership, and human-approval requirements.

For every rule, define:

- Accountable owner
- Technical implementation
- Automated validation/check
- Monitoring signal
- Exception path and approval authority

### 4. Define a formal artifact review process

For material AI or MCP changes:

1. Review functional specs with product, business, and data owners.
2. Review technical plans with architecture, security, cloud/platform, and data-governance stakeholders.
3. Review generated tasks before implementation.
4. Require pull-request review for source, tests, Dockerfiles, IaC, and configuration.
5. Require approval before production deployment.

Link, where practical:

- Work item
- Specification
- Architecture/threat model
- Code change
- Tests/evaluations
- Deployment manifest/IaC
- Release approval and operational runbook

### 5. Build an MCP reference architecture before exposing enterprise tools

Define a standard Azure pattern covering:

- Entra ID authentication and identity propagation
- Managed identities and least privilege
- Server-side, tool-level authorization
- API gateway/WAF/rate-limit policy where applicable
- Key Vault and secure configuration
- Private networking and environment isolation
- Structured audit and operational logging
- Input validation and output minimization
- Read/write tool tiers and approval requirements
- CI/CD, IaC, SAST, SCA, secret scanning, and container scanning
- Tool schema versioning, contract testing, and incident handling

Do not rely on model instructions as the authorization mechanism.

### 6. Pin platform and dependency standards

- Publish approved Node.js, TypeScript, MCP SDK, Azure SDK, and container base-image baselines.
- Make plans reference these standards explicitly.
- Require SBOM generation, dependency scanning, vulnerability remediation, and policy enforcement in CI.
- Use approved project templates to reduce variation in generated applications.

### 7. Add AI- and MCP-specific validation

At minimum, test:

- Tool authorization and entitlement boundaries
- Prompt injection and malicious retrieved-content scenarios
- Tool input validation and output redaction
- Data leakage across roles, regions, and accounts
- Missing, stale, conflicting, and unauthorized data scenarios
- Time-zone, daylight-saving, cutoff, and date-parsing edge cases
- Timeout, retry, concurrency, load, and downstream failure behavior
- Agent evaluation criteria: grounding, accuracy, refusal/no-data behavior, and task completion

### 8. Define pilot success measures and make a go/no-go decision

Measure against the current delivery approach:

- Time from story-ready to working prototype
- Specification and review effort
- Rework required after implementation
- Defects discovered before release
- Test and security findings
- Compliance with approved platform patterns
- Developer and reviewer acceptance
- Model, infrastructure, and operational cost per delivered feature

Proceed beyond one or two pilots only if the approach improves speed and traceability **without weakening security, architecture consistency, data governance, or supportability**.

## Full transcript

[00:01] Hi, I'm Udon Diva. I'm a Microsoft
[00:02] Hi, I'm Udon Diva. I'm a Microsoft Finary MPP and I'm a cloudier architect.
[00:04] Finary MPP and I'm a cloudier architect.
[00:04] Finary MPP and I'm a cloudier architect. And with my current clients, I solely
[00:07] And with my current clients, I solely
[00:07] And with my current clients, I solely work on getting development teams
[00:09] work on getting development teams
[00:09] work on getting development teams started improving with agentic software
[00:11] started improving with agentic software
[00:11] started improving with agentic software development and really embracing those
[00:13] development and really embracing those
[00:14] development and really embracing those specdriven development practices and for
[00:16] specdriven development practices and for
[00:16] specdriven development practices and for that we use we use GitHub. We love using
[00:18] that we use we use GitHub. We love using
[00:18] that we use we use GitHub. We love using GitHub. So we use GitHub enterprise,
[00:19] GitHub. So we use GitHub enterprise,
[00:20] GitHub. So we use GitHub enterprise, GitHub copilot and specit from GitHub.
[00:23] GitHub copilot and specit from GitHub.
[00:23] GitHub copilot and specit from GitHub. And the big drawback there is GitHub is
[00:26] And the big drawback there is GitHub is
[00:26] And the big drawback there is GitHub is releasing so many awesome features. it
[00:28] releasing so many awesome features. it
[00:28] releasing so many awesome features. it almost is a day job just to keep up. So
[00:31] almost is a day job just to keep up. So
[00:31] almost is a day job just to keep up. So definitely check out those release notes
[00:32] definitely check out those release notes
[00:32] definitely check out those release notes for those new features that will be
[00:35] for those new features that will be
[00:35] for those new features that will be definitely be there in the near future.
[00:38] definitely be there in the near future.
[00:38] definitely be there in the near future. And I want to get to Visual Studio Code
[00:39] And I want to get to Visual Studio Code
[00:39] And I want to get to Visual Studio Code to the demo part as soon as possible.
[00:41] to the demo part as soon as possible.
[00:41] to the demo part as soon as possible. But before that, we have to look back a
[00:44] But before that, we have to look back a
[00:44] But before that, we have to look back a bit just just to know where we're coming
[00:47] bit just just to know where we're coming
[00:47] bit just just to know where we're coming from. And it hasn't been that long. But
[00:49] from. And it hasn't been that long. But
[00:49] from. And it hasn't been that long. But prompt first AI coding got us started.
[00:52] prompt first AI coding got us started.
[00:52] prompt first AI coding got us started. It got us moving and it was fast and it
[00:54] It got us moving and it was fast and it
[00:54] It got us moving and it was fast and it was incredible. And as I said, it really
[00:57] was incredible. And as I said, it really
[00:57] was incredible. And as I said, it really helped to get us started for AI and
[00:59] helped to get us started for AI and
[00:59] helped to get us started for AI and software development. But for bigger
[01:01] software development. But for bigger
[01:01] software development. But for bigger projects, for real projects, for
[01:05] projects, for real projects, for
[01:05] projects, for real projects, for enterprises, for bigger teams, prompts
[01:07] enterprises, for bigger teams, prompts
[01:07] enterprises, for bigger teams, prompts can be a very weak foundation because
[01:09] can be a very weak foundation because
[01:10] can be a very weak foundation because these prompts are usually private.
[01:12] these prompts are usually private.
[01:12] these prompts are usually private. They're temporary. They're hard to
[01:13] They're temporary. They're hard to
[01:14] They're temporary. They're hard to review, and it produces something that
[01:17] review, and it produces something that
[01:17] review, and it produces something that usually builds, but sometimes completely
[01:19] usually builds, but sometimes completely
[01:19] usually builds, but sometimes completely misses the point. So, the shift I want
[01:22] misses the point. So, the shift I want
[01:22] misses the point. So, the shift I want to show today is is simple. Stop
[01:24] to show today is is simple. Stop
[01:24] to show today is is simple. Stop treating the prompt as the main artifact
[01:26] treating the prompt as the main artifact
[01:26] treating the prompt as the main artifact and start treating the specification as
[01:28] and start treating the specification as
[01:28] and start treating the specification as that main artifact. And that is the
[01:31] that main artifact. And that is the
[01:31] that main artifact. And that is the whole session in one quote. But there's
[01:32] whole session in one quote. But there's
[01:32] whole session in one quote. But there's so much more to explore. So let me head
[01:35] so much more to explore. So let me head
[01:35] so much more to explore. So let me head over to the next slide.
[01:41] And before I get to the demo, I have to
[01:41] And before I get to the demo, I have to clarify this dismantle model because
[01:43] clarify this dismantle model because
[01:43] clarify this dismantle model because this will make everything else make
[01:45] this will make everything else make
[01:45] this will make everything else make sense down the line. Because prompt
[01:48] sense down the line. Because prompt
[01:48] sense down the line. Because prompt first development looks like this. You
[01:51] first development looks like this. You
[01:51] first development looks like this. You write an instruction, the model writes
[01:53] write an instruction, the model writes
[01:53] write an instruction, the model writes some code and then you get a surprise.
[01:55] some code and then you get a surprise.
[01:56] some code and then you get a surprise. And a lot of the times that's a very
[01:58] And a lot of the times that's a very
[01:58] And a lot of the times that's a very nice surprise, but sometimes it is not.
[02:00] nice surprise, but sometimes it is not.
[02:00] nice surprise, but sometimes it is not. And you spend the rest of the afternoon
[02:02] And you spend the rest of the afternoon
[02:02] And you spend the rest of the afternoon working out why. And spectre spec first
[02:06] working out why. And spectre spec first
[02:06] working out why. And spectre spec first development looks at this differently.
[02:08] development looks at this differently.
[02:08] development looks at this differently. We start with a constitution, our
[02:10] We start with a constitution, our
[02:10] We start with a constitution, our unbreakable rules that are usually
[02:12] unbreakable rules that are usually
[02:12] unbreakable rules that are usually bigger than our project, usually bigger
[02:14] bigger than our project, usually bigger
[02:14] bigger than our project, usually bigger than our team. And this contains our
[02:16] than our team. And this contains our
[02:16] than our team. And this contains our information on our must-have things for
[02:19] information on our must-have things for
[02:19] information on our must-have things for our project. So things like testable by
[02:21] our project. So things like testable by
[02:21] our project. So things like testable by design, our security standards, our
[02:24] design, our security standards, our
[02:24] design, our security standards, our enterprise guidelines, our team specific
[02:26] enterprise guidelines, our team specific
[02:26] enterprise guidelines, our team specific rules.
[02:28] rules.
[02:28] rules. So everything are we want to to have
[02:31] So everything are we want to to have
[02:31] So everything are we want to to have that coding AI assistant to adhere to
[02:34] that coding AI assistant to adhere to
[02:34] that coding AI assistant to adhere to our musthaves. And then we have the
[02:36] our musthaves. And then we have the
[02:36] our musthaves. And then we have the spec. So our functional specification of
[02:39] spec. So our functional specification of
[02:39] spec. So our functional specification of our application, it describes what we
[02:41] our application, it describes what we
[02:41] our application, it describes what we want to build. So we specify all the
[02:44] want to build. So we specify all the
[02:44] want to build. So we specify all the features, the functional requirements,
[02:46] features, the functional requirements,
[02:46] features, the functional requirements, but we do not include anything
[02:47] but we do not include anything
[02:47] but we do not include anything technical. So no technical
[02:49] technical. So no technical
[02:49] technical. So no technical specifications we do not include the how
[02:51] specifications we do not include the how
[02:52] specifications we do not include the how we save that for the plan for the plan
[02:54] we save that for the plan for the plan
[02:54] we save that for the plan for the plan prompts. So in the plan we keep all our
[02:56] prompts. So in the plan we keep all our
[02:56] prompts. So in the plan we keep all our specifications around deployment targets
[02:58] specifications around deployment targets
[02:58] specifications around deployment targets your stack what frameworks we want to
[03:00] your stack what frameworks we want to
[03:00] your stack what frameworks we want to use the versioning we want to do uh and
[03:03] use the versioning we want to do uh and
[03:03] use the versioning we want to do uh and so on and so on and then we want to
[03:05] so on and so on and then we want to
[03:05] so on and so on and then we want to split this in manageable chunks and we
[03:07] split this in manageable chunks and we
[03:07] split this in manageable chunks and we do that in the task phase. So we chunk
[03:09] do that in the task phase. So we chunk
[03:10] do that in the task phase. So we chunk it in a logical order that makes sense
[03:12] it in a logical order that makes sense
[03:12] it in a logical order that makes sense when developing it in the code phase,
[03:13] when developing it in the code phase,
[03:14] when developing it in the code phase, the implement phase.
[03:16] the implement phase.
[03:16] the implement phase. And very important, and I cannot stress
[03:18] And very important, and I cannot stress
[03:18] And very important, and I cannot stress this enough, review everything. I mean,
[03:22] this enough, review everything. I mean,
[03:22] this enough, review everything. I mean, review everything AI puts out, but
[03:24] review everything AI puts out, but
[03:24] review everything AI puts out, but especially if you're using these
[03:25] especially if you're using these
[03:25] especially if you're using these backdriven development frameworks,
[03:27] backdriven development frameworks,
[03:27] backdriven development frameworks, review every single document. The thing
[03:30] review every single document. The thing
[03:30] review every single document. The thing trolls are gene. So check that
[03:31] trolls are gene. So check that
[03:32] trolls are gene. So check that constitution, check that specification,
[03:34] constitution, check that specification,
[03:34] constitution, check that specification, and check that plan. Make sure you
[03:36] and check that plan. Make sure you
[03:36] and check that plan. Make sure you understand what it says. Make sure you
[03:38] understand what it says. Make sure you
[03:38] understand what it says. Make sure you are on board. Make sure your team is on
[03:40] are on board. Make sure your team is on
[03:40] are on board. Make sure your team is on board so everything is on the same
[03:41] board so everything is on the same
[03:41] board so everything is on the same everyone is on the same page. So it
[03:44] everyone is on the same page. So it
[03:44] everyone is on the same page. So it actually produces something um of
[03:46] actually produces something um of
[03:46] actually produces something um of quality you would want down the line.
[03:49] quality you would want down the line.
[03:49] quality you would want down the line. And there are more specs to specs
[03:50] And there are more specs to specs
[03:50] And there are more specs to specs there's more steps to explore here. So
[03:53] there's more steps to explore here. So
[03:53] there's more steps to explore here. So this is not an exhaustive list. These
[03:54] this is not an exhaustive list. These
[03:54] this is not an exhaustive list. These are the things to get you started. These
[03:56] are the things to get you started. These
[03:56] are the things to get you started. These are the things um to cover when you're
[03:59] are the things um to cover when you're
[03:59] are the things um to cover when you're going through these specdriven
[04:00] going through these specdriven
[04:00] going through these specdriven development frameworks. So everything
[04:02] development frameworks. So everything
[04:02] development frameworks. So everything from constitution to code and for the
[04:04] from constitution to code and for the
[04:04] from constitution to code and for the other steps please check out that spec
[04:06] other steps please check out that spec
[04:06] other steps please check out that spec specit um documentation and I'll share a
[04:10] specit um documentation and I'll share a
[04:10] specit um documentation and I'll share a link on the last slide. So with this the
[04:13] link on the last slide. So with this the
[04:13] link on the last slide. So with this the spec becomes part of the repository part
[04:15] spec becomes part of the repository part
[04:15] spec becomes part of the repository part of the git history and the next time we
[04:18] of the git history and the next time we
[04:18] of the git history and the next time we implement a new feature we start with
[04:19] implement a new feature we start with
[04:19] implement a new feature we start with this base again. So we add the news
[04:21] this base again. So we add the news
[04:21] this base again. So we add the news feature specification and follow this
[04:23] feature specification and follow this
[04:23] feature specification and follow this process again. But enough slide for now
[04:26] process again. But enough slide for now
[04:26] process again. But enough slide for now I want to go to Visual Studio Code to
[04:28] I want to go to Visual Studio Code to
[04:28] I want to go to Visual Studio Code to actually show it uh to you in action.
[04:31] actually show it uh to you in action.
[04:31] actually show it uh to you in action. And what we're looking at here is the
[04:33] And what we're looking at here is the
[04:33] And what we're looking at here is the thing we're going to build. So this was
[04:35] thing we're going to build. So this was
[04:35] thing we're going to build. So this was a Microsoft build 2026 sess session and
[04:39] a Microsoft build 2026 sess session and
[04:39] a Microsoft build 2026 sess session and uh for that I created like the session
[04:41] uh for that I created like the session
[04:41] uh for that I created like the session planner NTP server. So Microsoft build
[04:43] planner NTP server. So Microsoft build
[04:43] planner NTP server. So Microsoft build of course has all these amazing session
[04:45] of course has all these amazing session
[04:45] of course has all these amazing session you can still watch online now. So
[04:47] you can still watch online now. So
[04:48] you can still watch online now. So please I encourage you to do so. But
[04:50] please I encourage you to do so. But
[04:50] please I encourage you to do so. But during such an event the session planner
[04:52] during such an event the session planner
[04:52] during such an event the session planner is is like your your um your agenda
[04:55] is is like your your um your agenda
[04:55] is is like your your um your agenda right? It really dictates what you want
[04:57] right? It really dictates what you want
[04:57] right? It really dictates what you want to do. What would you see that day? And
[05:00] to do. What would you see that day? And
[05:00] to do. What would you see that day? And of course, it featured an amazing CLI we
[05:02] of course, it featured an amazing CLI we
[05:02] of course, it featured an amazing CLI we could use, but it was lacking an MCP
[05:04] could use, but it was lacking an MCP
[05:04] could use, but it was lacking an MCP server. So, I created the MCP server, or
[05:06] server. So, I created the MCP server, or
[05:06] server. So, I created the MCP server, or better yet, we're going to create that
[05:08] better yet, we're going to create that
[05:08] better yet, we're going to create that during this demo today. And what we're
[05:10] during this demo today. And what we're
[05:10] during this demo today. And what we're looking at is here, and you see it from
[05:12] looking at is here, and you see it from
[05:12] looking at is here, and you see it from the branch name, and this is an empty
[05:14] the branch name, and this is an empty
[05:14] the branch name, and this is an empty project. And it's not really that empty,
[05:16] project. And it's not really that empty,
[05:16] project. And it's not really that empty, but to show you, there's nothing
[05:17] but to show you, there's nothing
[05:17] but to show you, there's nothing special. There's a GitHub folder that
[05:19] special. There's a GitHub folder that
[05:19] special. There's a GitHub folder that just contains our GitHub copilot
[05:21] just contains our GitHub copilot
[05:21] just contains our GitHub copilot instructions. We have the VS Code
[05:23] instructions. We have the VS Code
[05:23] instructions. We have the VS Code folder, which has my own VS Code
[05:25] folder, which has my own VS Code
[05:25] folder, which has my own VS Code settings. So, nothing to do with this
[05:27] settings. So, nothing to do with this
[05:27] settings. So, nothing to do with this MCP server. And I have this demo folder
[05:29] MCP server. And I have this demo folder
[05:29] MCP server. And I have this demo folder and this is just for me so you don't
[05:31] and this is just for me so you don't
[05:31] and this is just for me so you don't have to watch me type. I prepared some
[05:34] have to watch me type. I prepared some
[05:34] have to watch me type. I prepared some some of the prompts we're going to use
[05:36] some of the prompts we're going to use
[05:36] some of the prompts we're going to use today. And then there's the git ignore
[05:38] today. And then there's the git ignore
[05:38] today. And then there's the git ignore and of course this markdown. So there's
[05:39] and of course this markdown. So there's
[05:40] and of course this markdown. So there's no nothing else here in this project.
[05:43] no nothing else here in this project.
[05:43] no nothing else here in this project. And of course to get us started we have
[05:44] And of course to get us started we have
[05:44] And of course to get us started we have to install a specket. We have the
[05:47] to install a specket. We have the
[05:47] to install a specket. We have the specify CLI installed. But now we're
[05:50] specify CLI installed. But now we're
[05:50] specify CLI installed. But now we're going to open up a terminal and just
[05:53] going to open up a terminal and just
[05:53] going to open up a terminal and just copy over this very handy command
[05:55] copy over this very handy command
[05:55] copy over this very handy command specify in it because we want to install
[05:58] specify in it because we want to install
[05:58] specify in it because we want to install specket in this uh project. So we do
[06:01] specket in this uh project. So we do
[06:01] specket in this uh project. So we do specify in it here and we have to
[06:03] specify in it here and we have to
[06:03] specify in it here and we have to specify the integration for the the AI
[06:05] specify the integration for the the AI
[06:05] specify the integration for the the AI harness the AI tool we're using because
[06:08] harness the AI tool we're using because
[06:08] harness the AI tool we're using because it will wire up those those custom
[06:10] it will wire up those those custom
[06:10] it will wire up those those custom instructions based on the type of
[06:12] instructions based on the type of
[06:12] instructions based on the type of integration you choose. But because I'm
[06:14] integration you choose. But because I'm
[06:14] integration you choose. But because I'm using copilot, I'm using integration
[06:16] using copilot, I'm using integration
[06:16] using copilot, I'm using integration copilot here. And if I as execute this,
[06:19] copilot here. And if I as execute this,
[06:19] copilot here. And if I as execute this, we add this nice specify terminal
[06:21] we add this nice specify terminal
[06:22] we add this nice specify terminal window. And it actually says, well, it's
[06:24] window. And it actually says, well, it's
[06:24] window. And it actually says, well, it's not that empty. Are you sure you want to
[06:25] not that empty. Are you sure you want to
[06:25] not that empty. Are you sure you want to continue? And of course, you want to
[06:27] continue? And of course, you want to
[06:27] continue? And of course, you want to continue here. And it will ask me if I
[06:29] continue here. And it will ask me if I
[06:29] continue here. And it will ask me if I want to use bash or a PowerShell guy or
[06:33] want to use bash or a PowerShell guy or
[06:33] want to use bash or a PowerShell guy or want to use Python for the scripting.
[06:35] want to use Python for the scripting.
[06:35] want to use Python for the scripting. And because I'm on Windows, it makes
[06:36] And because I'm on Windows, it makes
[06:36] And because I'm on Windows, it makes sense to just go with PowerShell. And
[06:39] sense to just go with PowerShell. And
[06:39] sense to just go with PowerShell. And then it steps over and it does it very
[06:41] then it steps over and it does it very
[06:41] then it steps over and it does it very quickly. It initializes my specified
[06:43] quickly. It initializes my specified
[06:43] quickly. It initializes my specified project. It checks if every prere
[06:45] project. It checks if every prere
[06:45] project. It checks if every prere prerequisite is installed and goes ahead
[06:47] prerequisite is installed and goes ahead
[06:47] prerequisite is installed and goes ahead wiring up get a co copilot for me to use
[06:50] wiring up get a co copilot for me to use
[06:50] wiring up get a co copilot for me to use the speckit framework and it has some
[06:53] the speckit framework and it has some
[06:53] the speckit framework and it has some very of course um handy hints on the
[06:56] very of course um handy hints on the
[06:56] very of course um handy hints on the credentials on the off tokens but the
[06:59] credentials on the off tokens but the
[06:59] credentials on the off tokens but the things I wanted to show you was those
[07:00] things I wanted to show you was those
[07:00] things I wanted to show you was those other commands that in here know as well
[07:02] other commands that in here know as well
[07:02] other commands that in here know as well and this is also this is not an
[07:04] and this is also this is not an
[07:04] and this is also this is not an exhaustive list there's even more
[07:05] exhaustive list there's even more
[07:05] exhaustive list there's even more specket commands we can uh see in our
[07:08] specket commands we can uh see in our
[07:08] specket commands we can uh see in our documentation
[07:10] documentation
[07:10] documentation and with that install we actually got a
[07:12] and with that install we actually got a
[07:12] and with that install we actually got a new specify folder here. So in the
[07:14] new specify folder here. So in the
[07:14] new specify folder here. So in the specify folder and I highly encourage
[07:16] specify folder and I highly encourage
[07:16] specify folder and I highly encourage you to browse around because you really
[07:19] you to browse around because you really
[07:19] you to browse around because you really have to you want to demystify this to to
[07:22] have to you want to demystify this to to
[07:22] have to you want to demystify this to to take away kind of the magic that specket
[07:24] take away kind of the magic that specket
[07:24] take away kind of the magic that specket brings to the table because it's just
[07:27] brings to the table because it's just
[07:27] brings to the table because it's just markdown. It's just scripting and of
[07:30] markdown. It's just scripting and of
[07:30] markdown. It's just scripting and of course it's very powerful. Don't get me
[07:31] course it's very powerful. Don't get me
[07:31] course it's very powerful. Don't get me wrong I love using specket but in the
[07:34] wrong I love using specket but in the
[07:34] wrong I love using specket but in the end it's un it's it's very handy to to
[07:36] end it's un it's it's very handy to to
[07:36] end it's un it's it's very handy to to understand there there's no funny
[07:38] understand there there's no funny
[07:38] understand there there's no funny business going on. It's just markdown as
[07:41] business going on. It's just markdown as
[07:41] business going on. It's just markdown as scripting. [sighs]
[07:42] scripting. [sighs]
[07:42] scripting. [sighs] So with that I installed specket and
[07:45] So with that I installed specket and
[07:45] So with that I installed specket and we're ready to um move over to our
[07:48] we're ready to um move over to our
[07:48] we're ready to um move over to our constitution and as I said I prepared
[07:50] constitution and as I said I prepared
[07:50] constitution and as I said I prepared some some prompts here. So look at this
[07:52] some some prompts here. So look at this
[07:52] some some prompts here. So look at this prompts. Let me close the terminal and I
[07:54] prompts. Let me close the terminal and I
[07:54] prompts. Let me close the terminal and I have here a project constitution for
[07:56] have here a project constitution for
[07:56] have here a project constitution for that HTTP MCP server for the uh for the
[07:59] that HTTP MCP server for the uh for the
[07:59] that HTTP MCP server for the uh for the build session planner and I put some
[08:02] build session planner and I put some
[08:02] build session planner and I put some things in here. This is not like the
[08:04] things in here. This is not like the
[08:04] things in here. This is not like the list everyone has to use. These are
[08:06] list everyone has to use. These are
[08:06] list everyone has to use. These are things that made sense building this
[08:08] things that made sense building this
[08:08] things that made sense building this build session planner MCP. So I want to
[08:11] build session planner MCP. So I want to
[08:11] build session planner MCP. So I want to use grounded data only because I don't
[08:13] use grounded data only because I don't
[08:13] use grounded data only because I don't want it to to think up sessions that are
[08:16] want it to to think up sessions that are
[08:16] want it to to think up sessions that are not there. So very important ground your
[08:18] not there. So very important ground your
[08:18] not there. So very important ground your data. I wanted to be time aware. Time is
[08:21] data. I wanted to be time aware. Time is
[08:21] data. I wanted to be time aware. Time is a hard concept in software development.
[08:23] a hard concept in software development.
[08:23] a hard concept in software development. So making sure your um AI assistant
[08:28] So making sure your um AI assistant
[08:28] So making sure your um AI assistant understands how important time is for
[08:29] understands how important time is for
[08:30] understands how important time is for these sessions because if we're looking
[08:31] these sessions because if we're looking
[08:31] these sessions because if we're looking at starting soon, you don't want to get
[08:33] at starting soon, you don't want to get
[08:33] at starting soon, you don't want to get this wrong. I want you to be agent safe
[08:36] this wrong. I want you to be agent safe
[08:36] this wrong. I want you to be agent safe because well NCP sometimes is hard to to
[08:40] because well NCP sometimes is hard to to
[08:40] because well NCP sometimes is hard to to have security to have the odd in place.
[08:43] have security to have the odd in place.
[08:43] have security to have the odd in place. So I want you have to create a safe tool
[08:45] So I want you have to create a safe tool
[08:45] So I want you have to create a safe tool design. I want you to be HTTP safe
[08:47] design. I want you to be HTTP safe
[08:47] design. I want you to be HTTP safe because well it is MTP we can deploy
[08:50] because well it is MTP we can deploy
[08:50] because well it is MTP we can deploy that on a public endpoint. Sure make it
[08:53] that on a public endpoint. Sure make it
[08:53] that on a public endpoint. Sure make it safe it's safe to expose there. I want
[08:55] safe it's safe to expose there. I want
[08:55] safe it's safe to expose there. I want it to be testable by design because it's
[08:57] it to be testable by design because it's
[08:57] it to be testable by design because it's always a good idea and I want privacy by
[08:59] always a good idea and I want privacy by
[08:59] always a good idea and I want privacy by default. Well, it isn't public session
[09:01] default. Well, it isn't public session
[09:01] default. Well, it isn't public session list, but still this makes sense for me
[09:04] list, but still this makes sense for me
[09:04] list, but still this makes sense for me currently to have in the constitution.
[09:06] currently to have in the constitution.
[09:06] currently to have in the constitution. These are the things, my unbreakable
[09:08] These are the things, my unbreakable
[09:08] These are the things, my unbreakable rules I want my application to adhere
[09:10] rules I want my application to adhere
[09:10] rules I want my application to adhere to.
[09:12] to.
[09:12] to. And now it's just as easy. And of
[09:14] And now it's just as easy. And of
[09:14] And now it's just as easy. And of course, because I prepared this, you
[09:16] course, because I prepared this, you
[09:16] course, because I prepared this, you don't have to see me type because
[09:18] don't have to see me type because
[09:18] don't have to see me type because preparing these prompts can be quite
[09:20] preparing these prompts can be quite
[09:20] preparing these prompts can be quite some work. And of course, there is AI to
[09:22] some work. And of course, there is AI to
[09:22] some work. And of course, there is AI to help you there. But to get started with
[09:25] help you there. But to get started with
[09:25] help you there. But to get started with that um constitution, we can just use
[09:28] that um constitution, we can just use
[09:28] that um constitution, we can just use the spec command for constitution and
[09:31] the spec command for constitution and
[09:31] the spec command for constitution and paste in that prompt for my
[09:33] paste in that prompt for my
[09:33] paste in that prompt for my constitution.
[09:34] constitution.
[09:34] constitution. And now the fun thing is with genai this
[09:37] And now the fun thing is with genai this
[09:37] And now the fun thing is with genai this can take some time and for demo purposes
[09:40] can take some time and for demo purposes
[09:40] can take some time and for demo purposes it's hard to predict how long it will
[09:43] it's hard to predict how long it will
[09:43] it's hard to predict how long it will take. So I'll just have it running here
[09:45] take. So I'll just have it running here
[09:45] take. So I'll just have it running here for a couple of seconds so you can
[09:47] for a couple of seconds so you can
[09:47] for a couple of seconds so you can follow along what it's doing here. So,
[09:48] follow along what it's doing here. So,
[09:48] follow along what it's doing here. So, it's seeing my six principles. And what
[09:51] it's seeing my six principles. And what
[09:51] it's seeing my six principles. And what it's doing with this text is integrating
[09:53] it's doing with this text is integrating
[09:53] it's doing with this text is integrating this in the specified folder for the
[09:55] this in the specified folder for the
[09:55] this in the specified folder for the constitution we um uh we have in there.
[09:59] constitution we um uh we have in there.
[09:59] constitution we um uh we have in there. And let me get to that. Let me stop
[10:01] And let me get to that. Let me stop
[10:01] And let me get to that. Let me stop this. We don't want to wait for this.
[10:04] this. We don't want to wait for this.
[10:04] this. We don't want to wait for this. And I'll stash this just to get this out
[10:07] And I'll stash this just to get this out
[10:08] And I'll stash this just to get this out of the way.
[10:09] of the way.
[10:09] of the way. Let me go there and stash this so we can
[10:14] Let me go there and stash this so we can
[10:14] Let me go there and stash this so we can go to the next branch just to show you
[10:25] just to show you what it is like when
[10:25] just to show you what it is like when the constitution is generated. So I
[10:27] the constitution is generated. So I
[10:27] the constitution is generated. So I prepared these branches and it sometimes
[10:29] prepared these branches and it sometimes
[10:29] prepared these branches and it sometimes feels a bit like cheating but again
[10:31] feels a bit like cheating but again
[10:31] feels a bit like cheating but again watching these AI assistants it's much
[10:33] watching these AI assistants it's much
[10:33] watching these AI assistants it's much more fun if you do this in uh in real
[10:36] more fun if you do this in uh in real
[10:36] more fun if you do this in uh in real life and try it out for yourself. So if
[10:38] life and try it out for yourself. So if
[10:38] life and try it out for yourself. So if we look at uh the branch for the
[10:41] we look at uh the branch for the
[10:41] we look at uh the branch for the constitution created. So we have the
[10:43] constitution created. So we have the
[10:44] constitution created. So we have the constitution created here and in that
[10:45] constitution created here and in that
[10:45] constitution created here and in that memory folder now is the constitution
[10:47] memory folder now is the constitution
[10:47] memory folder now is the constitution markdown that actually has those six
[10:50] markdown that actually has those six
[10:50] markdown that actually has those six principles um integrated with the
[10:53] principles um integrated with the
[10:53] principles um integrated with the constitution for uh for this specdriven
[10:56] constitution for uh for this specdriven
[10:56] constitution for uh for this specdriven development effort. So again we see the
[10:59] development effort. So again we see the
[10:59] development effort. So again we see the grounded data only time aware
[11:00] grounded data only time aware
[11:00] grounded data only time aware correctness etc etc. We see all six here
[11:03] correctness etc etc. We see all six here
[11:03] correctness etc etc. We see all six here in the constitution in the specified
[11:05] in the constitution in the specified
[11:05] in the constitution in the specified folder created. So with that
[11:07] folder created. So with that
[11:07] folder created. So with that constitution created, we're now ready to
[11:09] constitution created, we're now ready to
[11:09] constitution created, we're now ready to move up to uh the specify phase. So
[11:13] move up to uh the specify phase. So
[11:13] move up to uh the specify phase. So specifying what we want our application
[11:15] specifying what we want our application
[11:15] specifying what we want our application to do. So the functional requirements
[11:17] to do. So the functional requirements
[11:17] to do. So the functional requirements and prepared it as well. So we have the
[11:19] and prepared it as well. So we have the
[11:19] and prepared it as well. So we have the specify prompt. And if we look at that,
[11:22] specify prompt. And if we look at that,
[11:22] specify prompt. And if we look at that, let me close this just to have a better
[11:24] let me close this just to have a better
[11:24] let me close this just to have a better view. So we wanted to have an MCP server
[11:27] view. So we wanted to have an MCP server
[11:27] view. So we wanted to have an MCP server that gives an AI agent access to the
[11:29] that gives an AI agent access to the
[11:29] that gives an AI agent access to the Microsoft build session data. So it
[11:32] Microsoft build session data. So it
[11:32] Microsoft build session data. So it explores the things we want to um this
[11:35] explores the things we want to um this
[11:35] explores the things we want to um this MCP server to do. We have the data
[11:37] MCP server to do. We have the data
[11:37] MCP server to do. We have the data modeling here. So some source fields
[11:39] modeling here. So some source fields
[11:39] modeling here. So some source fields from the JSON we're loading in. We have
[11:42] from the JSON we're loading in. We have
[11:42] from the JSON we're loading in. We have some MCP tools you wanted to expose. So
[11:45] some MCP tools you wanted to expose. So
[11:45] some MCP tools you wanted to expose. So we want to be able to search those
[11:47] we want to be able to search those
[11:47] we want to be able to search those sessions. We want to be able to get a
[11:49] sessions. We want to be able to get a
[11:49] sessions. We want to be able to get a session. We want to look at what's
[11:50] session. We want to look at what's
[11:50] session. We want to look at what's happening now. All these are MCP tools
[11:53] happening now. All these are MCP tools
[11:53] happening now. All these are MCP tools we're asking the speckit framework to
[11:56] we're asking the speckit framework to
[11:56] we're asking the speckit framework to create for us down the line. So this
[11:58] create for us down the line. So this
[11:58] create for us down the line. So this this is really the what we're going to
[12:00] this is really the what we're going to
[12:00] this is really the what we're going to build. So again, this is not the how.
[12:02] build. So again, this is not the how.
[12:02] build. So again, this is not the how. This is no technical um implementation
[12:05] This is no technical um implementation
[12:05] This is no technical um implementation details. This is only what we wanted to
[12:07] details. This is only what we wanted to
[12:07] details. This is only what we wanted to build. So if I open up my co-pilot
[12:10] build. So if I open up my co-pilot
[12:10] build. So if I open up my co-pilot again, we're ready for the next uh the
[12:13] again, we're ready for the next uh the
[12:14] again, we're ready for the next uh the next slash command, which is the specket
[12:16] next slash command, which is the specket
[12:16] next slash command, which is the specket specify. And again, it's the same
[12:18] specify. And again, it's the same
[12:18] specify. And again, it's the same recipe. We have that slash command and
[12:20] recipe. We have that slash command and
[12:20] recipe. We have that slash command and we paste in that uh specification for
[12:23] we paste in that uh specification for
[12:23] we paste in that uh specification for the specify. And again, it will start
[12:26] the specify. And again, it will start
[12:26] the specify. And again, it will start going and it will start um integrating
[12:29] going and it will start um integrating
[12:29] going and it will start um integrating that specification. go over it and if it
[12:31] that specification. go over it and if it
[12:31] that specification. go over it and if it needs clarification, it will either
[12:33] needs clarification, it will either
[12:33] needs clarification, it will either highlight that in the specification or
[12:35] highlight that in the specification or
[12:35] highlight that in the specification or ask those questions to you and the user
[12:37] ask those questions to you and the user
[12:37] ask those questions to you and the user and it either can be like an open
[12:39] and it either can be like an open
[12:39] and it either can be like an open question or some multiple choice
[12:41] question or some multiple choice
[12:41] question or some multiple choice questions in there as well. And if we
[12:44] questions in there as well. And if we
[12:44] questions in there as well. And if we created that that um that specify
[12:47] created that that um that specify
[12:47] created that that um that specify prompt. So if we had the spec created,
[12:50] prompt. So if we had the spec created,
[12:50] prompt. So if we had the spec created, we can actually inspect that phase as
[12:52] we can actually inspect that phase as
[12:52] we can actually inspect that phase as well. So this is when this if I just run
[12:56] well. So this is when this if I just run
[12:56] well. So this is when this if I just run this command and waited a couple of
[12:57] this command and waited a couple of
[12:57] this command and waited a couple of minutes for it it to be done and if we
[13:00] minutes for it it to be done and if we
[13:00] minutes for it it to be done and if we look at the specification we now have a
[13:03] look at the specification we now have a
[13:03] look at the specification we now have a specs folder. Uh so let me close this
[13:07] specs folder. Uh so let me close this
[13:07] specs folder. Uh so let me close this the spec is created.
[13:10] the spec is created.
[13:10] the spec is created. So I have a specs folder here which is
[13:13] So I have a specs folder here which is
[13:13] So I have a specs folder here which is the first spec I created the build now
[13:16] the first spec I created the build now
[13:16] the first spec I created the build now MCP. And if I open that spec again it's
[13:19] MCP. And if I open that spec again it's
[13:19] MCP. And if I open that spec again it's very familiar. It's those same spec
[13:21] very familiar. It's those same spec
[13:21] very familiar. It's those same spec specifications I prompted it for and it
[13:25] specifications I prompted it for and it
[13:25] specifications I prompted it for and it integrated it. It um looked at my
[13:28] integrated it. It um looked at my
[13:28] integrated it. It um looked at my constitution and it will change
[13:31] constitution and it will change
[13:31] constitution and it will change everything it needs to change to adhere
[13:33] everything it needs to change to adhere
[13:33] everything it needs to change to adhere to those must haves in my constitution
[13:35] to those must haves in my constitution
[13:35] to those must haves in my constitution and follow those specifications. So it
[13:37] and follow those specifications. So it
[13:37] and follow those specifications. So it created some nice user stories. So we
[13:39] created some nice user stories. So we
[13:39] created some nice user stories. So we have a user story for the session
[13:41] have a user story for the session
[13:41] have a user story for the session search. We have a user story for the
[13:43] search. We have a user story for the
[13:43] search. We have a user story for the session detail retrieval currently
[13:46] session detail retrieval currently
[13:46] session detail retrieval currently happening sessions etc etc.
[13:49] happening sessions etc etc.
[13:49] happening sessions etc etc. And then as I said we need the plan
[13:52] And then as I said we need the plan
[13:52] And then as I said we need the plan phase as well. So that's the last prompt
[13:55] phase as well. So that's the last prompt
[13:55] phase as well. So that's the last prompt I um I prepared. So for the plan phase
[13:59] I um I prepared. So for the plan phase
[13:59] I um I prepared. So for the plan phase these are our technical choices or
[14:01] these are our technical choices or
[14:01] these are our technical choices or technical details or technical
[14:03] technical details or technical
[14:03] technical details or technical requirements we have for our application
[14:05] requirements we have for our application
[14:05] requirements we have for our application for our feature. So this states things
[14:08] for our feature. So this states things
[14:08] for our feature. So this states things like use TypeScript, I want to use
[14:10] like use TypeScript, I want to use
[14:10] like use TypeScript, I want to use Node.js, JS I want to use an MCP server
[14:13] Node.js, JS I want to use an MCP server
[14:13] Node.js, JS I want to use an MCP server I wanted to uh have an HD pro transport
[14:17] I wanted to uh have an HD pro transport
[14:17] I wanted to uh have an HD pro transport support etc etc so all these technical
[14:20] support etc etc so all these technical
[14:20] support etc etc so all these technical details also where we want to deploy it
[14:23] details also where we want to deploy it
[14:23] details also where we want to deploy it um how we're going to configure those um
[14:27] um how we're going to configure those um
[14:27] um how we're going to configure those um uh settings for this application all
[14:30] uh settings for this application all
[14:30] uh settings for this application all technical details go in that plan phase
[14:32] technical details go in that plan phase
[14:32] technical details go in that plan phase and again it's the same recipe we're
[14:34] and again it's the same recipe we're
[14:34] and again it's the same recipe we're just going to prompt it so we have
[14:36] just going to prompt it so we have
[14:36] just going to prompt it so we have another command which is the tasks uh
[14:38] another command which is the tasks uh
[14:38] another command which is the tasks uh sorry the plan So we have the speckit
[14:41] sorry the plan So we have the speckit
[14:41] sorry the plan So we have the speckit plan and we just prompted with our plan
[14:44] plan and we just prompted with our plan
[14:44] plan and we just prompted with our plan prompt and again these things takes take
[14:46] prompt and again these things takes take
[14:46] prompt and again these things takes take time to to prepare to create um and we
[14:50] time to to prepare to create um and we
[14:50] time to to prepare to create um and we just execute it again. So we execute it
[14:54] just execute it again. So we execute it
[14:54] just execute it again. So we execute it again it will run for a couple of
[14:55] again it will run for a couple of
[14:55] again it will run for a couple of minutes. It will look at our
[14:56] minutes. It will look at our
[14:56] minutes. It will look at our constitution. It will look at our spec
[14:59] constitution. It will look at our spec
[14:59] constitution. It will look at our spec as at our um functional requirements and
[15:02] as at our um functional requirements and
[15:02] as at our um functional requirements and it will create the technical
[15:03] it will create the technical
[15:04] it will create the technical implementation details for it. And after
[15:07] implementation details for it. And after
[15:07] implementation details for it. And after that we're ready for the the
[15:10] that we're ready for the the
[15:10] that we're ready for the the um the plan that is created. So if we
[15:14] um the plan that is created. So if we
[15:14] um the plan that is created. So if we look again we have in our um specs
[15:18] look again we have in our um specs
[15:18] look again we have in our um specs folder we actually have a couple of
[15:20] folder we actually have a couple of
[15:20] folder we actually have a couple of markdowns extra concerning those things
[15:23] markdowns extra concerning those things
[15:23] markdowns extra concerning those things we added during the plan phase. So we
[15:25] we added during the plan phase. So we
[15:25] we added during the plan phase. So we now have all these technical details.
[15:27] now have all these technical details.
[15:27] now have all these technical details. It's a stateless HTTP server, the
[15:29] It's a stateless HTTP server, the
[15:29] It's a stateless HTTP server, the technical context. We want these
[15:31] technical context. We want these
[15:31] technical context. We want these versions of TypeScript. And even if I
[15:33] versions of TypeScript. And even if I
[15:33] versions of TypeScript. And even if I didn't specify it, it will either ask me
[15:36] didn't specify it, it will either ask me
[15:36] didn't specify it, it will either ask me for it, it will fill in those versions.
[15:39] for it, it will fill in those versions.
[15:39] for it, it will fill in those versions. And that is something to be mindful
[15:41] And that is something to be mindful
[15:41] And that is something to be mindful especially with those versions. It will
[15:44] especially with those versions. It will
[15:44] especially with those versions. It will get a version for you. So it's probably
[15:46] get a version for you. So it's probably
[15:46] get a version for you. So it's probably the current version, but maybe it's not
[15:48] the current version, but maybe it's not
[15:48] the current version, but maybe it's not the latest version. So maybe be more
[15:50] the latest version. So maybe be more
[15:50] the latest version. So maybe be more specific. If you want the latest version
[15:51] specific. If you want the latest version
[15:52] specific. If you want the latest version of a framework, be specific and say, "I
[15:54] of a framework, be specific and say, "I
[15:54] of a framework, be specific and say, "I want this version in your plan prompts."
[15:58] want this version in your plan prompts."
[15:58] want this version in your plan prompts." And after that, we're ready for the task
[16:00] And after that, we're ready for the task
[16:00] And after that, we're ready for the task phase. So, it's another slash command.
[16:03] phase. So, it's another slash command.
[16:03] phase. So, it's another slash command. So, I have special spec tasks and we can
[16:06] So, I have special spec tasks and we can
[16:06] So, I have special spec tasks and we can run it and it will chunk up all these
[16:10] run it and it will chunk up all these
[16:10] run it and it will chunk up all these user stories, all these uh technical
[16:13] user stories, all these uh technical
[16:13] user stories, all these uh technical implementations from our plan. it will
[16:16] implementations from our plan. it will
[16:16] implementations from our plan. it will adhere to our constitution and we create
[16:18] adhere to our constitution and we create
[16:18] adhere to our constitution and we create manageable chunks for our uh AI
[16:21] manageable chunks for our uh AI
[16:21] manageable chunks for our uh AI assistant to integrate. So if we run
[16:23] assistant to integrate. So if we run
[16:23] assistant to integrate. So if we run that run that flash command and we have
[16:25] that run that flash command and we have
[16:25] that run that flash command and we have our task created we have yet another
[16:27] our task created we have yet another
[16:28] our task created we have yet another markdown. So again there's nothing magic
[16:30] markdown. So again there's nothing magic
[16:30] markdown. So again there's nothing magic going on. It is markdown as scripts that
[16:33] going on. It is markdown as scripts that
[16:33] going on. It is markdown as scripts that is what it is but it does a beautiful
[16:35] is what it is but it does a beautiful
[16:35] is what it is but it does a beautiful job in chunking these and making it
[16:37] job in chunking these and making it
[16:37] job in chunking these and making it really approachable for these AI
[16:39] really approachable for these AI
[16:39] really approachable for these AI assistants to to work on these uh bigger
[16:42] assistants to to work on these uh bigger
[16:42] assistants to to work on these uh bigger features. So what you see here it split
[16:45] features. So what you see here it split
[16:45] features. So what you see here it split it into a couple of phases which creates
[16:47] it into a couple of phases which creates
[16:47] it into a couple of phases which creates a couple of user stories. Um so it will
[16:50] a couple of user stories. Um so it will
[16:50] a couple of user stories. Um so it will actually do the boiler plate. It will um
[16:53] actually do the boiler plate. It will um
[16:53] actually do the boiler plate. It will um get that node configuration in there. It
[16:56] get that node configuration in there. It
[16:56] get that node configuration in there. It will um create our requirements. So we
[16:58] will um create our requirements. So we
[16:58] will um create our requirements. So we have a package JSON with our
[17:00] have a package JSON with our
[17:00] have a package JSON with our requirements for the application we're
[17:01] requirements for the application we're
[17:02] requirements for the application we're going to create. Uh it has a docker
[17:04] going to create. Uh it has a docker
[17:04] going to create. Uh it has a docker file. So it will set everything up for
[17:06] file. So it will set everything up for
[17:06] file. So it will set everything up for the later stage. So we have foundational
[17:09] the later stage. So we have foundational
[17:09] the later stage. So we have foundational any prerequisites we have to do. And
[17:12] any prerequisites we have to do. And
[17:12] any prerequisites we have to do. And again it did a beautiful job in like
[17:14] again it did a beautiful job in like
[17:14] again it did a beautiful job in like making a logical uh ordering of these
[17:17] making a logical uh ordering of these
[17:17] making a logical uh ordering of these user stories to implement during the
[17:19] user stories to implement during the
[17:20] user stories to implement during the implement phase.
[17:22] implement phase.
[17:22] implement phase. So if we've when we created these tasks
[17:25] So if we've when we created these tasks
[17:25] So if we've when we created these tasks so after that task phase there are
[17:28] so after that task phase there are
[17:28] so after that task phase there are things like the specket analyze we could
[17:30] things like the specket analyze we could
[17:30] things like the specket analyze we could do but we're also we you could be ready
[17:33] do but we're also we you could be ready
[17:33] do but we're also we you could be ready for for uh the implementation. So I
[17:36] for for uh the implementation. So I
[17:36] for for uh the implementation. So I highly encourage you to run also the
[17:38] highly encourage you to run also the
[17:38] highly encourage you to run also the intermediate steps things like analyze
[17:40] intermediate steps things like analyze
[17:40] intermediate steps things like analyze things like clarify but if you want to
[17:42] things like clarify but if you want to
[17:42] things like clarify but if you want to you could start the implementation now
[17:44] you could start the implementation now
[17:44] you could start the implementation now and again that's just another slash
[17:46] and again that's just another slash
[17:46] and again that's just another slash command. So if we run this back slpecket
[17:49] command. So if we run this back slpecket
[17:49] command. So if we run this back slpecket implement
[17:52] implement
[17:52] implement and of course uh it's not doing
[17:55] and of course uh it's not doing
[17:55] and of course uh it's not doing IntelliSense until now. So what we have
[17:59] IntelliSense until now. So what we have
[17:59] IntelliSense until now. So what we have to spec it implement will actually take
[18:01] to spec it implement will actually take
[18:01] to spec it implement will actually take our tasks and convert that to um to code
[18:05] our tasks and convert that to um to code
[18:05] our tasks and convert that to um to code and it will if you of course I said it
[18:08] and it will if you of course I said it
[18:08] and it will if you of course I said it want to be testable design. So it will
[18:09] want to be testable design. So it will
[18:09] want to be testable design. So it will also set up those tests and those tests
[18:12] also set up those tests and those tests
[18:12] also set up those tests and those tests will also help him down the line to
[18:14] will also help him down the line to
[18:14] will also help him down the line to create code that actually compiles. So
[18:17] create code that actually compiles. So
[18:17] create code that actually compiles. So it actually works because it also has
[18:19] it actually works because it also has
[18:19] it actually works because it also has the test to verify if everything works.
[18:22] the test to verify if everything works.
[18:22] the test to verify if everything works. And after that stage we come to that
[18:25] And after that stage we come to that
[18:25] And after that stage we come to that implementation done. And what we see now
[18:27] implementation done. And what we see now
[18:27] implementation done. And what we see now is a lot of files. Uh let me go back to
[18:32] is a lot of files. Uh let me go back to
[18:32] is a lot of files. Uh let me go back to my files. Close those prompts.
[18:35] my files. Close those prompts.
[18:35] my files. Close those prompts. And what we see here is a lot of uh
[18:39] And what we see here is a lot of uh
[18:39] And what we see here is a lot of uh code. So we have the source code here.
[18:40] code. So we have the source code here.
[18:40] code. So we have the source code here. And this is everything that was created
[18:42] And this is everything that was created
[18:42] And this is everything that was created during that implement phase. And to show
[18:45] during that implement phase. And to show
[18:45] during that implement phase. And to show you it actually works, I can start it up
[18:55] and it will actually start which is
[18:55] and it will actually start which is always good during the demo. And let me
[18:57] always good during the demo. And let me
[18:57] always good during the demo. And let me get though that uh model context
[19:00] get though that uh model context
[19:00] get though that uh model context protocol inspector so we can actually
[19:02] protocol inspector so we can actually
[19:02] protocol inspector so we can actually view it running. So I'm going to start
[19:05] view it running. So I'm going to start
[19:05] view it running. So I'm going to start the model context protocol inspector and
[19:07] the model context protocol inspector and
[19:07] the model context protocol inspector and it's just a node uh program a node
[19:10] it's just a node uh program a node
[19:10] it's just a node uh program a node module you can execute on your local
[19:13] module you can execute on your local
[19:13] module you can execute on your local machine. Uh if you don't have it, it
[19:15] machine. Uh if you don't have it, it
[19:15] machine. Uh if you don't have it, it will actually download it. I already
[19:16] will actually download it. I already
[19:16] will actually download it. I already have it installed. So it will fire it up
[19:20] have it installed. So it will fire it up
[19:20] have it installed. So it will fire it up and I have it here. Um so here you have
[19:23] and I have it here. Um so here you have
[19:23] and I have it here. Um so here you have the MCP server the the MCP protocol
[19:25] the MCP server the the MCP protocol
[19:25] the MCP server the the MCP protocol inspector and here we have the MCP
[19:27] inspector and here we have the MCP
[19:27] inspector and here we have the MCP server already in place and we can
[19:29] server already in place and we can
[19:29] server already in place and we can connect to it and it actually works and
[19:31] connect to it and it actually works and
[19:31] connect to it and it actually works and we can do list tools and everything we
[19:33] we can do list tools and everything we
[19:33] we can do list tools and everything we we asked you to do. So we have the
[19:35] we asked you to do. So we have the
[19:35] we asked you to do. So we have the search session and the get happening now
[19:37] search session and the get happening now
[19:37] search session and the get happening now the get next time s and get session and
[19:39] the get next time s and get session and
[19:39] the get next time s and get session and if I execute this command you have all
[19:41] if I execute this command you have all
[19:42] if I execute this command you have all these beautiful fields to to search on.
[19:44] these beautiful fields to to search on.
[19:44] these beautiful fields to to search on. If I just run the tool fingers crossed
[19:46] If I just run the tool fingers crossed
[19:46] If I just run the tool fingers crossed it's actually says and of course it
[19:48] it's actually says and of course it
[19:48] it's actually says and of course it starts with the opening keynote which
[19:51] starts with the opening keynote which
[19:51] starts with the opening keynote which was already u a month ago but that's
[19:55] was already u a month ago but that's
[19:55] was already u a month ago but that's fine um just to show you that it works
[19:57] fine um just to show you that it works
[19:57] fine um just to show you that it works and that it actually created a working
[19:59] and that it actually created a working
[19:59] and that it actually created a working MCP server. What I want you to do is is
[20:03] MCP server. What I want you to do is is
[20:03] MCP server. What I want you to do is is try this try this out. Try this on a
[20:05] try this try this out. Try this on a
[20:05] try this try this out. Try this on a real feature. So don't rewrite your
[20:08] real feature. So don't rewrite your
[20:08] real feature. So don't rewrite your entire workflow tomorrow. Big run real
[20:11] entire workflow tomorrow. Big run real
[20:11] entire workflow tomorrow. Big run real feature you want to work on either this
[20:13] feature you want to work on either this
[20:14] feature you want to work on either this week, next month, next iteration cycle,
[20:16] week, next month, next iteration cycle,
[20:16] week, next month, next iteration cycle, something small but meaningful. And do
[20:18] something small but meaningful. And do
[20:18] something small but meaningful. And do these three things. So write that
[20:21] these three things. So write that
[20:21] these three things. So write that specification before the prompt. Capture
[20:25] specification before the prompt. Capture
[20:25] specification before the prompt. Capture what and why first, not how. and then
[20:28] what and why first, not how. and then
[20:28] what and why first, not how. and then put like two or three maybe four maybe
[20:32] put like two or three maybe four maybe
[20:32] put like two or three maybe four maybe five non-negotiable team rules in that
[20:34] five non-negotiable team rules in that
[20:34] five non-negotiable team rules in that constitution. So that constitution is is
[20:37] constitution. So that constitution is is
[20:37] constitution. So that constitution is is like a living document that will be
[20:40] like a living document that will be
[20:40] like a living document that will be changed over time. You will learn you
[20:42] changed over time. You will learn you
[20:42] changed over time. You will learn you will uh get things from the enterprise
[20:44] will uh get things from the enterprise
[20:44] will uh get things from the enterprise from other teams to put in there. Uh and
[20:47] from other teams to put in there. Uh and
[20:47] from other teams to put in there. Uh and sometimes again it's bigger than your
[20:48] sometimes again it's bigger than your
[20:48] sometimes again it's bigger than your project or your team. will work in that
[20:51] project or your team. will work in that
[20:51] project or your team. will work in that constitution. Just start small and just
[20:54] constitution. Just start small and just
[20:54] constitution. Just start small and just see how it works.
[20:56] see how it works.
[20:56] see how it works. And then
[20:58] And then
[20:58] And then the the third thing is just review all
[21:00] the the third thing is just review all
[21:00] the the third thing is just review all these things. Very very important. I
[21:02] these things. Very very important. I
[21:02] these things. Very very important. I can't stress this this enough. Review
[21:05] can't stress this this enough. Review
[21:05] can't stress this this enough. Review everything it puts out and then
[21:07] everything it puts out and then
[21:08] everything it puts out and then implement it and use it and try it just
[21:10] implement it and use it and try it just
[21:10] implement it and use it and try it just to get a feel for it. And if you're done
[21:13] to get a feel for it. And if you're done
[21:13] to get a feel for it. And if you're done with the first feature, you're going to
[21:15] with the first feature, you're going to
[21:15] with the first feature, you're going to be next to be ready for your next
[21:17] be next to be ready for your next
[21:17] be next to be ready for your next feature and implement your next feature
[21:19] feature and implement your next feature
[21:19] feature and implement your next feature using specket, which really makes sense
[21:23] using specket, which really makes sense
[21:23] using specket, which really makes sense if you're working with it. And with
[21:25] if you're working with it. And with
[21:25] if you're working with it. And with this, I have these three links to share
[21:27] this, I have these three links to share
[21:27] this, I have these three links to share with you. So I have a link to the
[21:29] with you. So I have a link to the
[21:29] with you. So I have a link to the specket documentation. I have a link to
[21:31] specket documentation. I have a link to
[21:31] specket documentation. I have a link to the working code. Um, you can actually
[21:33] the working code. Um, you can actually
[21:33] the working code. Um, you can actually follow along. So you saw me go through
[21:36] follow along. So you saw me go through
[21:36] follow along. So you saw me go through these steps for this repository. Uh, I
[21:38] these steps for this repository. Uh, I
[21:38] these steps for this repository. Uh, I put this on a git repository just for
[21:40] put this on a git repository just for
[21:40] put this on a git repository just for you to get a feel for the code and see
[21:43] you to get a feel for the code and see
[21:43] you to get a feel for the code and see no funny businesses going on there. And
[21:45] no funny businesses going on there. And
[21:45] no funny businesses going on there. And if you have any questions, um, I want
[21:47] if you have any questions, um, I want
[21:47] if you have any questions, um, I want you to connect after, um, please, uh,
[21:50] you to connect after, um, please, uh,
[21:50] you to connect after, um, please, uh, contact me and feel free to, to find me
[21:52] contact me and feel free to, to find me
[21:52] contact me and feel free to, to find me online. So, thank you so much for being
[21:55] online. So, thank you so much for being
[21:55] online. So, thank you so much for being with me here for this backdriven
[21:57] with me here for this backdriven
[21:57] with me here for this backdriven development and, uh, we'll talk soon.
