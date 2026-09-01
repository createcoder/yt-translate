# Stop Vibe Coding: Start Spec-Driven Development, with John Capobianco

- **Video:** https://www.youtube.com/watch?v=9iWDteEhYk0
- **Generated:** 2026-08-31 20:52 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The material demonstrates an **AI-assisted, spec-driven development (SDD)** workflow, apparently based on a **Spec Kit / Specify CLI-style framework** used with **Claude Desktop, Claude Code, VS Code, and Git**. Instead of asking an LLM to directly generate an application (“vibe coding”), the workflow creates durable, repository-based artifacts in stages:

1. **Constitution** — project-level principles and guardrails.
2. **Specification** — user stories, functional requirements, acceptance criteria, and open questions.
3. **Clarification** — LLM-led resolution of unresolved requirements.
4. **Plan** — selected technology stack, architecture, implementation approach, and possibly data/contracts.
5. **Tasks** — dependency-ordered work breakdown, commonly grouped by user story/MVP sequence.
6. **Implementation** — agent-generated code, tests, configurations, and project files.
7. **Validation and delivery** — local testing, Git commits, repository collaboration, and eventual hosting/deployment.

The demo’s example is a browser-based IPv4 subnetting-learning game. That application is not materially relevant to Superior Propane, but the delivery pattern is: **version-controlled requirements, architecture, constraints, tests, and implementation artifacts provide a better basis for governed AI-assisted development than unstructured chat prompts.**

The presenters claim this process produces higher-quality code faster—sometimes implying that an hour of AI-assisted work replaces months or years of conventional development. That claim is **not established by the demonstration**. The evidence shown is a small local prototype, not a production system with enterprise integrations, security controls, support obligations, or independently verified outcomes.

For Superior Propane, the practical opportunity is to adopt the **pattern, not necessarily the exact toolchain**:

- Use specifications and technical guardrails to guide AI-assisted application, data, and infrastructure development.
- Store artifacts in enterprise Git repositories and connect them to normal PR, CI/CD, security, architecture-review, and release processes.
- Use AI agents to draft requirements, tests, code, documentation, data-quality rules, and infrastructure scaffolding—but keep accountable humans and deterministic controls in the approval path.
- Prefer an Azure-aligned model and deployment posture where internal code, architecture, data contracts, or business context are involved.

The most important caution: a Markdown constitution or a green test suite is **not a security, governance, or correctness control by itself**. It becomes valuable only when linked to enforceable repository policies, CI/CD gates, review processes, testing evidence, environment permissions, and operational ownership.

---

# Technical details

## Workflow and artifact model

The demonstrated process is a staged requirements-to-code workflow, with natural-language and Markdown artifacts used as shared context between humans and coding agents.

| Stage | Purpose | Typical artifact/output | Enterprise interpretation |
|---|---|---|---|
| Constitution | Project guardrails and quality principles | `constitution.md` | Project-specific engineering, data, security, AI, and operational constraints |
| Specify | Define what and why | `spec.md`, often under `specs/001-feature-name/` | Business requirements, user stories, acceptance criteria, data classification, non-functional requirements |
| Clarify | Resolve ambiguity | Updated spec and clarification record | AI-assisted requirements elicitation; assumptions must be reviewed and approved |
| Plan | Define how it will be built | Plan/template output, architecture choices, data model, contracts | Technical design, integrations, Azure/Databricks architecture, test/deployment plan |
| Tasks | Derive implementable work | `tasks.md` | Dependency-ordered engineering backlog, ideally linked to stories and test evidence |
| Implement | Generate/modify code | Source, tests, configs, package files, project structure | AI-assisted scaffolding and implementation—still subject to SDLC controls |
| Validate/release | Run tests and package/deploy | Test results, commits, CI output, deployment artifacts | Standard engineering validation and controlled environment promotion |

The presenters refer to slash commands resembling:

```text
/speckit.constitution
/speckit.specify
/speckit.clarify
/speckit.plan
/speckit.tasks
/implement
```

The exact command syntax varies in the summaries and is not conclusively established. The tool may be an implementation of GitHub’s/open-source **Spec Kit** approach, but the exact package, version, licensing, model support, extension configuration, and runtime behavior must be validated before enterprise adoption.

## Tooling and operating model shown

The workflow appears to combine the following components:

| Component | Role in the demo | Key enterprise concern |
|---|---|---|
| VS Code | Workspace and terminal host | Extension governance, endpoint security, local execution permissions |
| Claude Desktop | Drafts/refines prompts and source material | Enterprise tenant, retention/training terms, data residency, approved use |
| Claude Code | Reads repository context, generates files, runs commands, requests approvals, may commit changes | File/system access, shell access, repository write permissions, data transmission |
| Spec Kit / templates | Structures constitution → spec → clarify → plan → tasks → implement | Whether controls are enforceable or advisory; tool maturity and maintainability |
| Git repository | Stores artifacts, code, and history | PRs, branch protection, required reviewers, signed commits, auditability |
| Node.js/npm/NVM | Demo runtime/dependency setup for browser app | Approved developer images, package supply-chain controls, runtime standardization |
| Vitest or similar | Test generation and execution | Test quality, independent assertions, coverage meaning, CI enforcement |

The presenters use both **Claude Desktop** and **Claude Code**, creating a two-agent/tool handoff:

```text
Human idea/template
  → Claude Desktop drafts source content or prompts
  → Local Markdown artifact
  → Claude Code reads repository context/templates
  → Structured specification/plan/tasks/code
  → Git commit and later deployment
```

This pattern is viable, but it increases data-governance complexity because requirements, source files, repository context, terminal output, and generated code may all be exposed to one or more model-provider services.

## Constitution: useful as a prompt artifact, insufficient as a control

The constitution is described as a repository-level document covering principles such as:

- Security
- Code quality
- Test standards
- Domain correctness
- Referenced standards or authoritative sources
- Required design constraints

In the subnetting example, the constitution reportedly included requirements for mathematically correct subnetting calculations and relevant RFC alignment.

For Superior Propane, an equivalent constitution should not be limited to broad language such as “security first.” It should include **testable, project-relevant constraints**, for example:

- Approved Azure subscriptions, regions, and environment tiers.
- Microsoft Entra ID authentication and managed identity requirements.
- No secrets in source, prompts, Markdown, notebooks, or local configuration.
- Azure Key Vault usage for secrets and certificates.
- Data classification and permitted data-source rules.
- Unity Catalog governance and governed Databricks data-access patterns where relevant.
- Private networking/private endpoint requirements where applicable.
- Logging, auditability, retention, and incident-management requirements.
- Required AI evaluation, red-teaming, and model/prompt versioning.
- Human approval requirements for customer-, pricing-, dispatch-, billing-, safety-, or operationally impacting actions.
- Cost tagging, budgets, quota expectations, and support ownership.

**Speaker claim:** The tool can evaluate a plan against the constitution and report “no constitution violations.”

**Assessment:** This should initially be treated as an advisory LLM judgment, not evidence of compliance. Natural-language controls are ambiguous unless mapped to deterministic checks and review evidence. A generated compliance statement can miss violations, misunderstand requirements, or be based on incomplete context.

## Specification and clarification

The specification stage converts a high-level idea into a structured feature definition. The demo reportedly creates:

- Prioritized user stories
- Functional requirements
- Acceptance scenarios
- Requirements checklists
- Open questions / “needs clarification” markers

The clarification stage asks the user targeted questions, one at a time, and writes answers back to the specification. In the game example, questions included:

- Intended audience
- IPv4 versus IPv6 scope
- Free-text versus multiple-choice answers
- Progression mechanics
- Training/feedback approach

This is a useful mechanism for surfacing gaps in loosely defined requirements. It is especially relevant for a Technical Product Owner because it can strengthen intake quality before engineering begins.

However, the LLM may also infer requirements when inputs are incomplete. In the demo, it selected a typing-tutor-like gameplay model because no core loop was specified.

**Enterprise implication:** AI may propose options and document assumptions, but it should not autonomously settle material business, security, data, architecture, or compliance decisions. Product, data, architecture, security, and operational owners must approve those decisions.

A Superior Propane specification should explicitly distinguish:

1. **Business requirements** — users, outcomes, scope, workflows, success measures.
2. **Enterprise and non-functional constraints** — data classification, identity, Azure platform, resiliency, observability, security, support, cost.
3. **Technical design** — services, integrations, schemas, model deployment, data flows, APIs, implementation choices.

The speakers recommend avoiding technology decisions during the specification stage. That is useful for avoiding premature design bias, but enterprise platform requirements often are non-negotiable. For example, “must use approved Azure regions,” “must use Entra ID,” and “must retrieve only documents the user is authorized to access” are requirements, not optional design choices.

## Plan, data model, contracts, and tasks

The planning stage is presented as the point at which the technology stack and architecture are selected. In the demo, the plan chose:

- Browser execution
- Vanilla HTML, CSS, and JavaScript
- SQL storage for metadata
- Images not uploaded externally

This is not a complete production architecture. The material does not show authentication, authorization, APIs, network design, SQL hosting, encryption, retention, backup, observability, deployment, cost, or support design.

The workflow can also generate:

- Data models
- Contract documents, such as an `engine.md`
- Quick-start documentation
- Dependency-ordered `tasks.md`
- Work grouped by user story and MVP sequencing

These artifacts can be useful inputs to an agent and helpful documentation for later maintainers. For enterprise adoption, plans should additionally require:

- Data sources, ownership, classification, and retention.
- API/service contracts and integration dependencies.
- Identity, authorization, and network paths.
- Threat model and privacy assessment.
- Reliability, latency, volume, RTO/RPO, and support model.
- Monitoring, alerts, audit logs, and failure behavior.
- CI/CD, Infrastructure as Code, environment promotion, and rollback.
- Cost estimates and FinOps controls.
- Tests mapped to requirements and risk.

## Implementation and local environment behavior

The implementation phase generates source files, tests, configuration, styles, package files, and runtime setup. In the demo, the agent created project folders resembling:

```text
/specs
/src
/styles
/tests
```

The code-generation phase encountered a local prerequisite failure: Node.js/npm was unavailable. The agent attempted to remediate by:

- Detecting missing Node/npm packages.
- Requesting permission to proceed.
- Providing a `curl` command for the user to run.
- Installing NVM.
- Continuing the Node setup after repeated approvals.

This exposes a significant enterprise operational issue: AI coding agents may do more than draft code. Depending on configuration, they may:

- Read local repository contents.
- Modify files.
- Create branches and commits.
- Run shell commands.
- Install packages.
- Download external scripts.
- Access local credentials, CLI tokens, environment variables, or mounted storage if not properly constrained.

The repeated prompts to approve actions, and references to bypassing prompts or “YOLO”/dangerous permission modes, should be treated as a warning. Productivity-oriented permission bypasses are not appropriate defaults for enterprise repositories, developer workstations, or cloud-connected environments.

## Testing claims and limitations

The presenters describe an agent that:

- Writes tests, potentially before implementation.
- Runs unit/regression tests with **Vitest** or a similar JavaScript testing framework.
- Applies formatting and type checks.
- Identifies missing test coverage.
- Iterates until tests pass.
- Reports results including:
  - 51 tests green
  - 77 tests green
  - 100% coverage
  - Type and lint checks clean
  - One remaining source error or lint issue in some stages

The workflow’s emphasis on tests, phased implementation, and regression checks is positive. It is materially better than accepting a one-shot generated demo with no test artifacts.

However:

- **100% coverage does not equal correctness.**
  - It means all measured lines/functions/branches have been exercised, depending on the configuration.
  - It does not prove correct business rules, complete edge-case coverage, resilience, accessibility, authorization, or security.
- **Self-generated tests are not independent assurance.**
  - An LLM can misunderstand a requirement, generate incorrect implementation, and then generate tests that validate the same misunderstanding.
- **Green tests do not prove production readiness.**
  - The demo does not demonstrate integration tests, end-to-end tests, performance tests, accessibility tests, SAST, DAST, dependency scanning, threat modeling, deployment validation, or operational monitoring.

The presenters occasionally imply that the agent can test its own code and users therefore do not need to test it. This is **not a safe or established engineering conclusion**.

## Git and traceability

The demo uses Git branches and commits to preserve specifications and implementation work. A feature folder such as:

```text
specs/001-subnetting-game
```

is paired with a feature branch, described as `subnetting-game`.

This supports a useful traceability chain:

```text
Business requirement
  → constitution / constraints
  → specification and clarification decisions
  → technical plan, contracts, tasks
  → generated source and tests
  → pull request / CI evidence
  → release artifact and deployment
```

However, the demonstration also shows a Git/GitHub authentication problem, likely involving 2FA, and an unresolved commit/push flow. This is a useful reminder that local generation is not a complete delivery process.

Git alone does not provide:

- Branch protection
- Required reviewers
- Code ownership
- Secret scanning
- Dependency scanning
- CI/CD approval gates
- Secure identities
- Deployment authorization
- Audit retention
- Operational support

These must be configured in GitHub Enterprise or Azure DevOps and associated pipelines.

## Hosting discussion

The speakers mention:

- Google Cloud Run
- Fly.io
- AWS/Amazon Cloud
- Azure as a general option

They claim Google Cloud Run can deploy from a Git repository and cite a simple hosting cost of approximately **US$0.07–$0.15/day**. That estimate is not suitable for planning because actual cost depends on requests, CPU/memory, concurrency, minimum instances, egress, logging, domains, builds, storage, identity, databases, monitoring, and support requirements.

The hosting discussion has limited direct relevance to Superior Propane’s Azure-oriented remit. If a prototype becomes production-worthy, Azure-native options should be assessed first:

- **Azure Static Web Apps** for static front ends.
- **Azure App Service** for managed web apps/APIs.
- **Azure Container Apps** for containerized/serverless applications.
- **Azure Functions** for event-driven components.
- **AKS** only where its operational complexity is justified.
- **Azure Container Registry** for approved images.
- **Key Vault**, **Entra ID**, **Azure Monitor/Application Insights**, and appropriate Defender/security tooling.

## Costs and model-routing claims

The speakers flag the workflow as token- and context-heavy. They mention:

- A claimed US$20/month plan may be insufficient for sustained artifact-heavy workflows.
- An anecdotal Gemini bill of approximately US$380.
- A purported “Max” plan around US$100/month.
- A video-generation example costing about US$8 per video and roughly US$300 for 30 videos.
- A suggested pattern of using a lower-cost model for most tasks and a higher-capability model for final implementation.

These are speaker anecdotes and not an enterprise cost model.

The key established point is that agentic, iterative workflows can create unpredictable spend through:

- Large repository/context ingestion.
- Multiple stages of artifact generation.
- Clarification/revision loops.
- Test/fix cycles.
- Long-running agent sessions.
- CI execution.
- Model evaluation workloads.
- Generated cloud infrastructure.

The claim that using an open-source model makes token use “irrelevant” is misleading. It may reduce external per-token billing, but costs shift to:

- GPU/CPU capacity.
- Model serving.
- Azure infrastructure.
- Networking.
- Monitoring.
- Reliability engineering.
- Security operations.
- Support and maintenance.

---

# Potential applications for Superior Propane

## 1. Governed AI-assisted delivery for internal apps and data products

The strongest application is a repeatable, controlled workflow for internal solutions—not unrestricted autonomous coding.

Potential candidates:

- Customer-service agent-assist prototypes.
- Field-service or technician workflow tools.
- Delivery/dispatch exception-management interfaces.
- Internal knowledge-navigation tools.
- Safety/compliance training utilities.
- Data-quality remediation tools.
- Internal analytics self-service interfaces over approved data products.
- Document extraction and workflow automation.
- Deterministic calculators or decision trees for internal use.

The subnetting game is only a demonstration vehicle. It does not prove the approach for customer-facing, operationally critical, financial, dispatch, safety, or regulated applications.

## 2. Standard constitution templates by solution pattern

Rather than having every project invent policy language, create reusable constitutions for common delivery patterns:

- Azure AI Foundry knowledge assistant/RAG application.
- Customer-service copilot.
- Databricks data product/pipeline.
- Operational workflow web app.
- Document intelligence/extraction workflow.
- API integration service.
- Internal training application.
- Infrastructure-as-Code change.

Each template should define mandatory, testable requirements around:

- Data classification and permissible data use.
- Approved Azure services and regions.
- Entra ID, RBAC, managed identity, and Key Vault.
- Private connectivity/network rules.
- Databricks/Unity Catalog data access and lineage requirements.
- AI model/provider restrictions and model deployment ownership.
- Prompt, retrieval, evaluation, and output-logging policies.
- Safety, escalation, and human-in-the-loop requirements.
- Monitoring, support ownership, incident response, rollback.
- Cost tags, budgets, quotas, and expected unit economics.

## 3. Improved intake for Azure AI Foundry and Databricks initiatives

The clarify/specification pattern could improve intake quality for AI and data work before cloud resources or pipelines are created.

A required spec could capture:

- Business owner and technical owner.
- Users, decisions, workflows, and success measures.
- Authoritative source systems.
- Data classification, residency, retention, and access restrictions.
- Databricks catalog/schema/table ownership and lineage expectations.
- Batch versus real-time requirements.
- Model provider/deployment, prompt/RAG approach, and evaluation dataset.
- Human approval and escalation rules.
- Availability, latency, cost, and support expectations.
- Acceptance criteria and explicit failure behavior.

For example, a “summarize propane delivery exceptions” request should specify whether customer data is involved, who can access summaries, allowable source data, whether generated summaries can trigger actions, acceptable accuracy, audit requirements, and fallback behavior if source systems or model endpoints are unavailable.

## 4. Databricks development assistance

Although Databricks is not demonstrated, the artifact-driven pattern maps well to data engineering:

- Generate initial PySpark/SQL transformation scaffolding from approved data contracts.
- Draft data-quality tests for nulls, duplicates, schema conformance, reconciliation, freshness, and referential integrity.
- Create documentation for tables, jobs, lineage assumptions, and runbooks.
- Generate Databricks Asset Bundle or deployment scaffolding.
- Convert existing notebooks/prototypes into modular, testable packages.

Guardrails are critical:

- Use only approved catalogs, schemas, tables, and classifications.
- Do not expose customer, payment, delivery, telemetry, or proprietary pricing data in unapproved model prompts.
- Prevent agent-driven production job deployment.
- Require development → test → production promotion and reconciliation evidence.

## 5. Azure AI Foundry model-routing and evaluation

The speaker’s idea of using a lower-cost model for routine work and a higher-capability model for complex tasks is worth piloting under controlled conditions.

Possible model-routing categories:

| Workload | Potential model posture |
|---|---|
| Requirements summarization, template filling, code explanation | Lower-cost approved model |
| Test-case drafting, documentation generation | Lower-cost or mid-tier model, subject to review |
| Complex multi-file refactoring, architecture critique, difficult debugging | Higher-capability approved model |
| Production customer/operational AI interactions | Model selected based on evaluated quality, safety, latency, and cost—not developer preference |

This should be implemented through approved Azure AI Foundry deployments or another enterprise-approved model path, with measured acceptance rates, latency, security findings, and cost per accepted outcome.

## 6. Rapid prototyping and technical enablement

A separate low-risk lane could use AI-assisted development for:

- Interactive safety/compliance learning tools.
- Azure/Databricks onboarding exercises.
- Python, SQL, and PySpark training with synthetic data.
- Technical troubleshooting simulations.
- Clickable workflow prototypes for stakeholder validation.

For these use cases, use deterministic logic and curated content where possible. A runtime LLM is not necessary merely because the application was built with AI assistance.

---

# Risks/validation questions

## Toolchain ambiguity and vendor assessment

The transcript does not reliably establish:

- Exact Spec Kit implementation/version.
- Claude Code/Desktop edition, model, and tenancy.
- IDE extension configuration.
- Licensing/support model.
- Authentication mechanism.
- Whether prompts, source code, local files, terminal output, or repository content leave the enterprise.
- Model training, retention, residency, or audit terms.
- Whether the agent operates locally, through a hosted environment, or through a controlled enterprise endpoint.

**Validate before adoption:**

- What exact tools, versions, commands, and integrations are required?
- Is the coding agent approved for Superior Propane source code and architecture content?
- Can it use an approved Azure AI Foundry model endpoint?
- What data retention, training-use, encryption, regional-processing, and audit commitments apply?
- Can it integrate with GitHub Enterprise and/or Azure DevOps under Entra ID and enterprise SSO?
- Is there a viable supported operating model, or is this dependent on personal accounts and unmanaged local setup?

## Data leakage and external model exposure

The demonstration uses local repository context and interactive AI services. This creates a high-risk path for accidental disclosure of:

- Customer PII and account information.
- Addresses, delivery history, consumption data, payment-related information.
- Pricing logic and business rules.
- Internal architecture, API patterns, credentials, and infrastructure definitions.
- Operational processes, safety procedures, or OT/SCADA-adjacent information.
- Production logs, configuration, `.env` files, cached credentials, or local cloud CLI tokens.

**Validation questions:**

- What files can the agent read by default?
- Are `.env`, secrets, local caches, logs, credential stores, and production extracts excluded technically?
- Does the agent have network access or access to cloud CLIs?
- Can prompt DLP, repository secret scanning, and content classification be applied before model submission?
- Are models, coding assistants, and developer plugins governed by an approved-tool catalogue?

## Agent permissions and execution safety

The material shows approvals for overwriting files, creating commits, installing packages, and running remote installation commands. It also implies “dangerously skip permissions” modes.

**Recommended enterprise posture:**

- Read-only repository access by default.
- Writes only in an isolated feature branch or ephemeral workspace.
- No direct changes to protected branches.
- No direct production deployment.
- No unrestricted shell, network, package install, or cloud CLI access.
- Human approval for:
  - dependency additions;
  - infrastructure changes;
  - external downloads;
  - secret access;
  - PR creation/merge;
  - cloud deployment;
  - data access;
  - costly/long-running agent execution.

**Validation questions:**

- Are agent tool calls logged with user/service identity and timestamp?
- Can the agent modify CI/CD definitions, IaC, permissions, or policy files?
- Can it invoke deployment commands against Azure or Databricks?
- Can it use existing browser sessions, SSH keys, environment variables, or CLI credentials?
- Is terminal execution sandboxed?

## Security and software supply chain

The Node/npm setup in the demo highlights ordinary but important supply-chain risks:

- `curl`-based remote script execution.
- Unreviewed package installation.
- Unpinned dependencies.
- Dependency confusion, typosquatting, compromised maintainers, and transitive vulnerabilities.
- AI-proposed outdated or incompatible libraries.
- Embedded client-side secrets or insecure configurations.

**Required controls:**

- Managed, approved developer environments with standard runtimes.
- Approved Node LTS and package-management configuration.
- Private package registry/proxy where appropriate.
- Lockfiles and dependency pinning.
- SCA/vulnerability scanning and license checks.
- SAST, secret scanning, container/IaC scanning where applicable.
- SBOM generation and artifact provenance.
- No ad hoc external script installation on managed corporate endpoints.

## Requirements inference and governance drift

The clarification process is useful, but it can generate false confidence:

- The LLM may offer a limited menu of options and constrain business thinking.
- It may infer missing requirements rather than force a decision.
- Documentation can drift from code.
- “No constitution violations” can be mistaken for a compliance certification.
- Users may be unclear whether they are approving a source prompt, a generated spec, or a final authoritative requirement.

**Mitigations:**

- Define canonical artifact names, locations, and approval status.
- Mark AI-generated content and record source/model/tool version.
- Require named business, architecture, data, security, and operational owners.
- Maintain an assumption/decision log.
- Use pull requests to update specs when behavior or architecture changes.
- Map constitutional requirements to deterministic CI/CD checks and evidence where feasible.

## Testing and quality risk

The most repeated overclaim is that generated tests or 100% coverage mean the solution is fully tested.

They do not.

For enterprise systems, require:

- Independent product acceptance criteria.
- SME-reviewed golden test cases for critical business rules.
- Unit, integration, end-to-end, negative-path, accessibility, resilience, and performance tests as appropriate.
- Security scans and threat modeling.
- Test data that represents realistic edge cases while protecting privacy.
- Human code review and UAT.
- Production monitoring, incident response, and rollback.

For AI applications, add:

- Groundedness and citation quality.
- Authorization-aware retrieval tests.
- Prompt-injection and jailbreak resilience.
- PII/sensitive-data leakage tests.
- Tool/action safety tests.
- Model/prompt/retrieval regression evaluation.
- Latency, throughput, quota, and fallback validation.

## Cost and operational trade-offs

Artifact-heavy agent workflows can improve documentation and quality, but they increase model usage, wait time, and review effort.

Cost drivers include:

- Seat/subscription licensing.
- Token/API consumption and long context windows.
- Model evaluation and iterative test-fix loops.
- CI runner time.
- Azure AI Foundry inference/evaluation usage.
- Azure storage, logging, networking, observability, and hosting.
- Databricks compute and vector/retrieval costs where relevant.
- Human review, security assessment, defect remediation, and maintenance.

**Validation questions:**

- What is the total cost per spec-to-implementation cycle?
- Which activities are covered by subscriptions versus metered API usage?
- Are hard spend caps available, or only alerts?
- Can usage be tagged by team, project, environment, and use case?
- Is model routing based on measured output quality and cost?
- Are there stop conditions for long-running autonomous loops?

## Prototype-to-production gap

The game was run locally at `localhost:8000`; there is no evidence of a production deployment, identity model, monitoring, secure configuration, or reproducible release.

A functional local prototype should not be treated as a production candidate until it has:

- A named technical/service owner.
- Source and build reproducibility.
- CI/CD and environment promotion.
- Security/privacy review proportional to risk.
- Identity/RBAC and secrets design.
- Observability, alerts, operational runbook, and support model.
- Backup/recovery and rollback, where relevant.
- Cost model and budget ownership.
- Customer/business UAT and acceptance evidence.

---

# Action items

## 1. Pilot the pattern, not the demo toolchain

Run a controlled pilot for one low-risk, non-production internal use case, such as:

- A training/knowledge-check application.
- A deterministic operational calculator using synthetic inputs.
- A Databricks data-quality enhancement.
- A documentation/runbook assistant with sanitized material.

Do not begin with customer-facing, pricing, billing, dispatch, safety-critical, production-control, or PII-heavy workflows.

Measure against a non-AI baseline:

- Requirement completeness.
- Time to prototype/MVP.
- Review effort.
- Defect and rework rate.
- Test quality and coverage of critical scenarios.
- Security findings.
- Cost per accepted task or release.
- Maintainability after handoff.

## 2. Define a Superior Propane AI project constitution

Create an enterprise Markdown template, owned jointly by product, architecture, security, data governance, and platform engineering.

Minimum sections:

- Business and technical owner.
- Data classification, source ownership, retention, and approved data paths.
- Approved Azure services, regions, subscriptions, and environments.
- Entra ID, managed identity, RBAC, and Key Vault requirements.
- Databricks/Unity Catalog requirements where governed data is used.
- Network/private connectivity requirements.
- AI model, provider, prompt, RAG, evaluation, and human-oversight requirements.
- Logging, audit, observability, incident response, and rollback.
- FinOps tagging, budgets, quotas, and support ownership.
- Prohibited actions and data types.
- Mandatory review and release gates.

## 3. Create specification and plan templates for AI/data workloads

Require project specifications to capture:

- Problem, users, scope, and success metrics.
- Functional and non-functional requirements.
- Acceptance criteria and business-owned test cases.
- Data sources, classifications, lineage, and access rules.
- Model/AI behavior, safety constraints, and evaluation criteria.
- Integration contracts and dependencies.
- Availability, latency, volume, resiliency, and support expectations.
- Cost estimate and consumption assumptions.
- Architecture, CI/CD, monitoring, security, and rollback plan.

Store these artifacts alongside code in Git, but never store secrets or sensitive production extracts in Markdown or prompt files.

## 4. Establish an approved AI coding-assistant control model

Classify tools by capability and apply increasing controls:

1. Chat/code completion only.
2. Repository read access.
3. Repository write access.
4. Terminal/package execution.
5. Cloud/data-platform access.
6. Deployment capability.

For each tier, define:

- Approved tools/models/tenants.
- Permitted data categories.
- Identity and logging requirements.
- Maximum permissions.
- Approval requirements.
- Allowed environments.
- Audit and retention requirements.

Initially prohibit agents from directly deploying to production Azure subscriptions, production Databricks workspaces, or production-connected systems.

## 5. Build enforced SDLC controls around generated code

Implement or confirm:

- Private repositories by default.
- Feature branches and protected main/release branches.
- Required pull-request reviewers and code owners.
- CI checks for build, test, lint/type checks, secret scanning, SAST, SCA/license scanning, and IaC/container scanning where relevant.
- Dependency pinning, lockfiles, SBOMs, and artifact provenance.
- Human sign-off for infrastructure, package additions, data access, and production releases.
- Environment-specific deployment identities rather than personal credentials.

## 6. Assess Azure AI Foundry as the governed model path

Evaluate whether approved Azure AI Foundry model deployments can support the intended coding, requirements, documentation, or evaluation use cases with:

- Entra ID integration.
- Centralized usage monitoring and budgets.
- Approved model selection and regional availability.
- Enterprise logging and policy controls.
- Appropriate data handling and network architecture.

Do not assume external Claude/Gemini/OpenAI consumer or subscription configurations meet enterprise requirements without a vendor/security review.

## 7. Establish AI FinOps controls

Implement:

- Separate experimentation and production subscriptions/workspaces.
- Required tags: `costCenter`, `productOwner`, `environment`, `useCase`, `dataClassification`.
- Per-project budgets and alerts.
- Model/request/token quotas where available.
- CI runtime limits.
- Dashboards for subscription, API/token, Azure infrastructure, and Databricks costs.
- Approval thresholds for expensive agent runs, evaluations, or infrastructure creation.

## 8. Create a prototype-to-production gate

Define a formal promotion checklist requiring:

- Named owner and support model.
- Reproducible build/deployment.
- Architecture/security/privacy review.
- Test and UAT evidence.
- Vulnerability and dependency scan results.
- Identity/RBAC and Key Vault implementation.
- Monitoring, alerting, logs, and runbooks.
- Rollback and incident procedures.
- Cost estimate and budget owner.

## 9. Use internal documentation-as-code selectively

Adopt the community contribution concept internally for approved platform materials:

- Version-control Azure, Databricks, AI Foundry, and engineering standards.
- Use issues for corrections and enhancement requests.
- Use PRs/code owners for review.
- Apply branch protection and secret scanning.
- Maintain clear separation between internal material and any public/open-source content.

This closing community practice has limited direct technical relevance, but it can support sustainable internal enablement if governed correctly.

## Full transcript

[00:02] The network engineers role is changing
[00:02] The network engineers role is changing [music] as fast as the job market. A1
[00:04] [music] as fast as the job market. A1
[00:04] [music] as fast as the job market. A1 Labs is how you keep up. Hands-on labs
[00:07] Labs is how you keep up. Hands-on labs
[00:07] Labs is how you keep up. Hands-on labs with new technologies built for
[00:09] with new technologies built for
[00:09] with new technologies built for engineers who can't afford to fall
[00:11] engineers who can't afford to fall
[00:11] engineers who can't afford to fall behind. Show up, suit up, and level up
[00:15] behind. Show up, suit up, and level up
[00:15] behind. Show up, suit up, and level up in A1 Labs. Welcome to the Art of
[00:18] in A1 Labs. Welcome to the Art of
[00:18] in A1 Labs. Welcome to the Art of Network Engineering podcast. My name is
[00:20] Network Engineering podcast. My name is
[00:20] Network Engineering podcast. My name is Andy Lapte and returning our favorite
[00:22] Andy Lapte and returning our favorite
[00:22] Andy Lapte and returning our favorite automation AI LLM guru, John Capabiano.
[00:27] automation AI LLM guru, John Capabiano.
[00:27] automation AI LLM guru, John Capabiano. How you doing, buddy? Man, it's so good
[00:28] How you doing, buddy? Man, it's so good
[00:28] How you doing, buddy? Man, it's so good to be here in Munich with you. I was the
[00:30] to be here in Munich with you. I was the
[00:30] to be here in Munich with you. I was the first smiley face when you got out of
[00:32] first smiley face when you got out of
[00:32] first smiley face when you got out of your taxi here. My bags have arrived, so
[00:34] your taxi here. My bags have arrived, so
[00:34] your taxi here. My bags have arrived, so I have a fresh set of clothes after 4
[00:37] I have a fresh set of clothes after 4
[00:37] I have a fresh set of clothes after 4 days.
[00:37] days.
[00:37] days. &gt;&gt; Was it four days without
[00:38] &gt;&gt; Was it four days without
[00:38] &gt;&gt; Was it four days without &gt;&gt; I was wearing the same Cisco. I was
[00:40] &gt;&gt; I was wearing the same Cisco. I was
[00:40] &gt;&gt; I was wearing the same Cisco. I was wearing my Vibe Ops shirt.
[00:42] wearing my Vibe Ops shirt.
[00:42] wearing my Vibe Ops shirt. &gt;&gt; Cool shirt. Cool shirt. Wandering around
[00:44] &gt;&gt; Cool shirt. Cool shirt. Wandering around
[00:44] &gt;&gt; Cool shirt. Cool shirt. Wandering around the streets of Munich explaining to
[00:45] the streets of Munich explaining to
[00:45] the streets of Munich explaining to random people what Vibops is. What is
[00:47] random people what Vibops is. What is
[00:47] random people what Vibops is. What is the Vibeops? Yeah,
[00:49] the Vibeops? Yeah,
[00:49] the Vibeops? Yeah, &gt;&gt; just for the audience, I get out of my
[00:51] &gt;&gt; just for the audience, I get out of my
[00:51] &gt;&gt; just for the audience, I get out of my car after a very long trip. I didn't
[00:52] car after a very long trip. I didn't
[00:52] car after a very long trip. I didn't sleep on blah blah blah. And as soon as
[00:54] sleep on blah blah blah. And as soon as
[00:54] sleep on blah blah blah. And as soon as I get out of the car, I hear your
[00:55] I get out of the car, I hear your
[00:55] I get out of the car, I hear your giggle.
[00:56] giggle.
[00:56] giggle. &gt;&gt; [laughter]
[00:57] &gt;&gt; [laughter]
[00:57] &gt;&gt; [laughter] &gt;&gt; And I looked over and John sitting there
[00:59] &gt;&gt; And I looked over and John sitting there
[00:59] &gt;&gt; And I looked over and John sitting there having a coffee said I'm like what a
[01:00] having a coffee said I'm like what a
[01:00] having a coffee said I'm like what a great
[01:01] great
[01:01] great &gt;&gt; introduction to getting here was you
[01:03] &gt;&gt; introduction to getting here was you
[01:03] &gt;&gt; introduction to getting here was you know my friend giggling saying hi and
[01:05] know my friend giggling saying hi and
[01:05] know my friend giggling saying hi and come on over. So all right so it's great
[01:06] come on over. So all right so it's great
[01:06] come on over. So all right so it's great to have you back. We're going to do some
[01:08] to have you back. We're going to do some
[01:08] to have you back. We're going to do some cool stuff. I have heard of spec driven
[01:10] cool stuff. I have heard of spec driven
[01:10] cool stuff. I have heard of spec driven development.
[01:11] development.
[01:11] development. &gt;&gt; I can't say I know what it is. I thought
[01:12] &gt;&gt; I can't say I know what it is. I thought
[01:12] &gt;&gt; I can't say I know what it is. I thought it was applying software development
[01:14] it was applying software development
[01:14] it was applying software development practices to what I've been doing which
[01:17] practices to what I've been doing which
[01:17] practices to what I've been doing which is like coding in LLMs. Is that kind of
[01:19] is like coding in LLMs. Is that kind of
[01:19] is like coding in LLMs. Is that kind of like
[01:19] like
[01:19] like &gt;&gt; it's like vibe matured with with some
[01:23] &gt;&gt; it's like vibe matured with with some
[01:23] &gt;&gt; it's like vibe matured with with some practices around it. Right. So this was
[01:25] practices around it. Right. So this was
[01:25] practices around it. Right. So this was introduced to me well it's been
[01:27] introduced to me well it's been
[01:27] introduced to me well it's been introduced maybe 8 months ago from
[01:29] introduced maybe 8 months ago from
[01:29] introduced maybe 8 months ago from Microsoft and GitHub and what we're
[01:31] Microsoft and GitHub and what we're
[01:31] Microsoft and GitHub and what we're looking at here is the spec kit which
[01:33] looking at here is the spec kit which
[01:33] looking at here is the spec kit which we're going to incorporate into cloud
[01:35] we're going to incorporate into cloud
[01:35] we're going to incorporate into cloud code. So specd driven development you
[01:37] code. So specd driven development you
[01:38] code. So specd driven development you may have heard of testdriven development
[01:39] may have heard of testdriven development
[01:39] may have heard of testdriven development which which kind of came out of the
[01:41] which which kind of came out of the
[01:41] which which kind of came out of the agile framework and the you know early
[01:43] agile framework and the you know early
[01:43] agile framework and the you know early DevOps days where you started writing
[01:45] DevOps days where you started writing
[01:45] DevOps days where you started writing small tests that failed and then you
[01:47] small tests that failed and then you
[01:47] small tests that failed and then you adjusted as little code as possible to
[01:49] adjusted as little code as possible to
[01:49] adjusted as little code as possible to make it pass. This is an approach and
[01:51] make it pass. This is an approach and
[01:51] make it pass. This is an approach and you're going to see that build
[01:52] you're going to see that build
[01:52] you're going to see that build highquality software faster, right?
[01:55] highquality software faster, right?
[01:55] highquality software faster, right? Instead of vibe coding every piece from
[01:57] Instead of vibe coding every piece from
[01:57] Instead of vibe coding every piece from scratch. Now, I'm going to be upfront.
[01:58] scratch. Now, I'm going to be upfront.
[01:58] scratch. Now, I'm going to be upfront. There's a lot more foreplay here.
[02:00] There's a lot more foreplay here.
[02:00] There's a lot more foreplay here. [snorts] There's a lot more patience
[02:01] [snorts] There's a lot more patience
[02:01] [snorts] There's a lot more patience involved and it takes about 40 30 to 40
[02:04] involved and it takes about 40 30 to 40
[02:04] involved and it takes about 40 30 to 40 minutes to get through a project. But
[02:05] minutes to get through a project. But
[02:05] minutes to get through a project. But what I thought, Andy, was let's build a
[02:07] what I thought, Andy, was let's build a
[02:07] what I thought, Andy, was let's build a network ccentric video game, right? And
[02:10] network ccentric video game, right? And
[02:10] network ccentric video game, right? And we can decide on what what network thing
[02:12] we can decide on what what network thing
[02:12] we can decide on what what network thing we do. Maybe quality of service or maybe
[02:14] we do. Maybe quality of service or maybe
[02:14] we do. Maybe quality of service or maybe subnetting. Let's do a subnetting video
[02:16] subnetting. Let's do a subnetting video
[02:16] subnetting. Let's do a subnetting video game.
[02:17] game.
[02:17] game. My first thought was we'll work a
[02:19] My first thought was we'll work a
[02:19] My first thought was we'll work a maintenance window and if we break
[02:21] maintenance window and if we break
[02:21] maintenance window and if we break anything like we fall into a pit of
[02:22] anything like we fall into a pit of
[02:22] anything like we fall into a pit of lava. [laughter]
[02:23] lava. [laughter]
[02:24] lava. [laughter] &gt;&gt; You die if you break something in a
[02:25] &gt;&gt; You die if you break something in a
[02:25] &gt;&gt; You die if you break something in a maintenance window. But we we'll keep it
[02:27] maintenance window. But we we'll keep it
[02:27] maintenance window. But we we'll keep it simple.
[02:27] simple.
[02:27] simple. &gt;&gt; So um we're going to scroll down a
[02:29] &gt;&gt; So um we're going to scroll down a
[02:29] &gt;&gt; So um we're going to scroll down a little bit and take a look at what is
[02:30] little bit and take a look at what is
[02:30] little bit and take a look at what is specriven development. We can keep
[02:32] specriven development. We can keep
[02:32] specriven development. We can keep going. So this is might be you know it
[02:33] going. So this is might be you know it
[02:34] going. So this is might be you know it might be interesting to read. Uh SD
[02:36] might be interesting to read. Uh SD
[02:36] might be interesting to read. Uh SD flips the script on traditional software
[02:37] flips the script on traditional software
[02:38] flips the script on traditional software development. For decades code has been
[02:40] development. For decades code has been
[02:40] development. For decades code has been king where specifications were just
[02:41] king where specifications were just
[02:41] king where specifications were just scaffolding we built and discarded once
[02:43] scaffolding we built and discarded once
[02:43] scaffolding we built and discarded once the real work of coding began. STD
[02:46] the real work of coding began. STD
[02:46] the real work of coding began. STD changes this where the specifications
[02:49] changes this where the specifications
[02:49] changes this where the specifications become executable. Now let's take a step
[02:51] become executable. Now let's take a step
[02:51] become executable. Now let's take a step back. This is networking. This is the
[02:52] back. This is networking. This is the
[02:52] back. This is networking. This is the art of network engineering. What do you
[02:55] art of network engineering. What do you
[02:55] art of network engineering. What do you do for a network change? You gather
[02:57] do for a network change? You gather
[02:57] do for a network change? You gather requirements, right? You come up with
[02:59] requirements, right? You come up with
[02:59] requirements, right? You come up with maybe an implementation plan, maybe a
[03:01] maybe an implementation plan, maybe a
[03:01] maybe an implementation plan, maybe a test plan, maybe a roll back plan, maybe
[03:04] test plan, maybe a roll back plan, maybe
[03:04] test plan, maybe a roll back plan, maybe a a success criteria plan. It's very
[03:07] a a success criteria plan. It's very
[03:07] a a success criteria plan. It's very close to what network engineers are
[03:09] close to what network engineers are
[03:09] close to what network engineers are already doing in their day-to-day job.
[03:11] already doing in their day-to-day job.
[03:11] already doing in their day-to-day job. &gt;&gt; Right? We might not say specifications.
[03:13] &gt;&gt; Right? We might not say specifications.
[03:13] &gt;&gt; Right? We might not say specifications. We might call them requirements. But the
[03:15] We might call them requirements. But the
[03:15] We might call them requirements. But the business comes down with some
[03:16] business comes down with some
[03:16] business comes down with some requirements. We turn that into an
[03:18] requirements. We turn that into an
[03:18] requirements. We turn that into an architecture. We turn that into a highle
[03:20] architecture. We turn that into a highle
[03:20] architecture. We turn that into a highle design, a low-level design. It mirrors
[03:22] design, a low-level design. It mirrors
[03:22] design, a low-level design. It mirrors that in a way.
[03:23] that in a way.
[03:23] that in a way. &gt;&gt; So that's what a spec specs are. This is
[03:26] &gt;&gt; So that's what a spec specs are. This is
[03:26] &gt;&gt; So that's what a spec specs are. This is the thing we need and this is the plan
[03:27] the thing we need and this is the plan
[03:27] the thing we need and this is the plan to get there.
[03:28] to get there.
[03:28] to get there. &gt;&gt; Exactly. So first thing we need to do is
[03:30] &gt;&gt; Exactly. So first thing we need to do is
[03:30] &gt;&gt; Exactly. So first thing we need to do is install the spec kit. Install the
[03:33] install the spec kit. Install the
[03:33] install the spec kit. Install the specify CLI. So let's copy that first
[03:35] specify CLI. So let's copy that first
[03:35] specify CLI. So let's copy that first line of code here, the UV line.
[03:37] line of code here, the UV line.
[03:38] line of code here, the UV line. &gt;&gt; So we're going to
[03:38] &gt;&gt; So we're going to
[03:38] &gt;&gt; So we're going to &gt;&gt; So let's just copy that. Yeah. And then
[03:40] &gt;&gt; So let's just copy that. Yeah. And then
[03:40] &gt;&gt; So let's just copy that. Yeah. And then paste it in. And if this hopefully this
[03:43] paste it in. And if this hopefully this
[03:43] paste it in. And if this hopefully this doesn't give us any problems. Oh, hang
[03:45] doesn't give us any problems. Oh, hang
[03:45] doesn't give us any problems. Oh, hang on. See that XYZ? Just press the up
[03:48] on. See that XYZ? Just press the up
[03:48] on. See that XYZ? Just press the up arrow and delete the
[03:50] arrow and delete the
[03:50] arrow and delete the &gt;&gt; XYZ.
[03:51] &gt;&gt; XYZ.
[03:51] &gt;&gt; XYZ. &gt;&gt; VXYZ thing. Yeah. Yeah. Uh, back to the
[03:54] &gt;&gt; VXYZ thing. Yeah. Yeah. Uh, back to the
[03:54] &gt;&gt; VXYZ thing. Yeah. Yeah. Uh, back to the at sign. Go back one more.
[03:56] at sign. Go back one more.
[03:56] at sign. Go back one more. &gt;&gt; Oh, one more.
[03:56] &gt;&gt; Oh, one more.
[03:56] &gt;&gt; Oh, one more. &gt;&gt; Yeah, try that. And that should grab the
[03:58] &gt;&gt; Yeah, try that. And that should grab the
[03:58] &gt;&gt; Yeah, try that. And that should grab the latest version. Okay, cool. So, it's
[04:00] latest version. Okay, cool. So, it's
[04:00] latest version. Okay, cool. So, it's going to install the spec kit. Now,
[04:02] going to install the spec kit. Now,
[04:02] going to install the spec kit. Now, what's neat, Andy, is you you've started
[04:04] what's neat, Andy, is you you've started
[04:04] what's neat, Andy, is you you've started to get the hang of Git.
[04:05] to get the hang of Git.
[04:05] to get the hang of Git. &gt;&gt; Mhm.
[04:05] &gt;&gt; Mhm.
[04:05] &gt;&gt; Mhm. &gt;&gt; So, this will naturally get track our
[04:08] &gt;&gt; So, this will naturally get track our
[04:08] &gt;&gt; So, this will naturally get track our specs. So today we're probably only
[04:10] specs. So today we're probably only
[04:10] specs. So today we're probably only going to have one specification, but
[04:11] going to have one specification, but
[04:12] going to have one specification, but let's say we wanted to improve it with a
[04:14] let's say we wanted to improve it with a
[04:14] let's say we wanted to improve it with a second specification. This will actually
[04:16] second specification. This will actually
[04:16] second specification. This will actually make a branch and track all of it for
[04:18] make a branch and track all of it for
[04:18] make a branch and track all of it for you.
[04:18] you.
[04:18] you. &gt;&gt; Question is the specification to make
[04:20] &gt;&gt; Question is the specification to make
[04:20] &gt;&gt; Question is the specification to make the game.
[04:21] the game.
[04:21] the game. &gt;&gt; Yes.
[04:21] &gt;&gt; Yes.
[04:21] &gt;&gt; Yes. &gt;&gt; Is that okay?
[04:22] &gt;&gt; Is that okay?
[04:22] &gt;&gt; Is that okay? &gt;&gt; Yeah. Yeah. Okay. So it's installed.
[04:24] &gt;&gt; Yeah. Yeah. Okay. So it's installed.
[04:24] &gt;&gt; Yeah. Yeah. Okay. So it's installed. Specify. So you see over here initialize
[04:27] Specify. So you see over here initialize
[04:27] Specify. So you see over here initialize a project.
[04:28] a project.
[04:28] a project. &gt;&gt; Yep.
[04:29] &gt;&gt; Yep.
[04:29] &gt;&gt; Yep. &gt;&gt; I would copy uh the first line there.
[04:32] &gt;&gt; I would copy uh the first line there.
[04:32] &gt;&gt; I would copy uh the first line there. &gt;&gt; Oh, gotcha.
[04:33] &gt;&gt; Oh, gotcha.
[04:33] &gt;&gt; Oh, gotcha. &gt;&gt; And instead of copilot for integration,
[04:35] &gt;&gt; And instead of copilot for integration,
[04:35] &gt;&gt; And instead of copilot for integration, we're going to choose claude.
[04:37] we're going to choose claude.
[04:37] we're going to choose claude. &gt;&gt; Okay. So, we're going to paste that in
[04:38] &gt;&gt; Okay. So, we're going to paste that in
[04:38] &gt;&gt; Okay. So, we're going to paste that in and change it from copilot to claude.
[04:41] and change it from copilot to claude.
[04:41] and change it from copilot to claude. &gt;&gt; Good.
[04:42] &gt;&gt; Good.
[04:42] &gt;&gt; Good. &gt;&gt; Yep. Okay, cool. So, we're going to
[04:44] &gt;&gt; Yep. Okay, cool. So, we're going to
[04:44] &gt;&gt; Yep. Okay, cool. So, we're going to press enter and use the shell. You could
[04:46] press enter and use the shell. You could
[04:46] press enter and use the shell. You could choose PowerShell, but let's just use
[04:47] choose PowerShell, but let's just use
[04:47] choose PowerShell, but let's just use bash and see the next steps. So, just
[04:51] bash and see the next steps. So, just
[04:51] bash and see the next steps. So, just see here. So, go into your project
[04:53] see here. So, go into your project
[04:53] see here. So, go into your project folder. We're already in the project
[04:54] folder. We're already in the project
[04:54] folder. We're already in the project folder. If you click the little double
[04:57] folder. If you click the little double
[04:57] folder. If you click the little double files here, Andy,
[04:58] files here, Andy,
[04:58] files here, Andy, &gt;&gt; are we done with this over here?
[04:59] &gt;&gt; are we done with this over here?
[04:59] &gt;&gt; are we done with this over here? &gt;&gt; No, not yet. Not yet. We're going to
[05:00] &gt;&gt; No, not yet. Not yet. We're going to
[05:00] &gt;&gt; No, not yet. Not yet. We're going to follow that the whole time. So, double
[05:02] follow that the whole time. So, double
[05:02] follow that the whole time. So, double click on the little files. See how we
[05:04] click on the little files. See how we
[05:04] click on the little files. See how we have a my project? And if you expand
[05:06] have a my project? And if you expand
[05:06] have a my project? And if you expand that, we have the claude and specify.
[05:09] that, we have the claude and specify.
[05:09] that, we have the claude and specify. &gt;&gt; So let's cd into my project here in the
[05:14] &gt;&gt; So let's cd into my project here in the
[05:14] &gt;&gt; So let's cd into my project here in the terminal. And we it's called my project
[05:16] terminal. And we it's called my project
[05:16] terminal. And we it's called my project cuz we pasted in my project. So we'll
[05:18] cuz we pasted in my project. So we'll
[05:18] cuz we pasted in my project. So we'll just roll with it. All right. So let's
[05:19] just roll with it. All right. So let's
[05:19] just roll with it. All right. So let's go back into the git guide. Now the very
[05:22] go back into the git guide. Now the very
[05:22] go back into the git guide. Now the very first thing we're going to build, if you
[05:23] first thing we're going to build, if you
[05:23] first thing we're going to build, if you scroll down, is the constitution.
[05:26] scroll down, is the constitution.
[05:26] scroll down, is the constitution. &gt;&gt; So establishing project principles. Now
[05:29] &gt;&gt; So establishing project principles. Now
[05:29] &gt;&gt; So establishing project principles. Now I don't have a constitution where I
[05:31] I don't have a constitution where I
[05:31] I don't have a constitution where I live, right? We have a constitutional
[05:32] live, right? We have a constitutional
[05:32] live, right? We have a constitutional monarchy. But you have an American
[05:34] monarchy. But you have an American
[05:34] monarchy. But you have an American constitution. Honestly, if you're an
[05:35] constitution. Honestly, if you're an
[05:35] constitution. Honestly, if you're an American, use this to frame your
[05:37] American, use this to frame your
[05:38] American, use this to frame your constitution. These are guard rails.
[05:40] constitution. These are guard rails.
[05:40] constitution. These are guard rails. These are security principles, code
[05:42] These are security principles, code
[05:42] These are security principles, code quality, testing. Now, you know what I
[05:44] quality, testing. Now, you know what I
[05:44] quality, testing. Now, you know what I like to do, Andy? I like to use claw
[05:46] like to do, Andy? I like to use claw
[05:46] like to do, Andy? I like to use claw desktop to write my constitution.
[05:50] desktop to write my constitution.
[05:50] desktop to write my constitution. &gt;&gt; So, you're going to copy this line. Go
[05:52] &gt;&gt; So, you're going to copy this line. Go
[05:52] &gt;&gt; So, you're going to copy this line. Go into cla.
[05:53] into cla.
[05:53] into cla. &gt;&gt; Can I go in there?
[05:53] &gt;&gt; Can I go in there?
[05:53] &gt;&gt; Can I go in there? &gt;&gt; Yeah. And say, I'm using the SD to build
[05:57] &gt;&gt; Yeah. And say, I'm using the SD to build
[05:57] &gt;&gt; Yeah. And say, I'm using the SD to build a video game related to computer
[05:59] a video game related to computer
[05:59] a video game related to computer networking subnetting or whatever. I
[06:01] networking subnetting or whatever. I
[06:01] networking subnetting or whatever. I know. on your there's a lot of pressure
[06:02] know. on your there's a lot of pressure
[06:02] know. on your there's a lot of pressure because everyone's watching
[06:03] because everyone's watching
[06:03] because everyone's watching &gt;&gt; STD to build a video game to uh
[06:05] &gt;&gt; STD to build a video game to uh
[06:05] &gt;&gt; STD to build a video game to uh &gt;&gt; uh for for computer networking
[06:07] &gt;&gt; uh for for computer networking
[06:07] &gt;&gt; uh for for computer networking &gt;&gt; simulate computer networking. I don't
[06:09] &gt;&gt; simulate computer networking. I don't
[06:09] &gt;&gt; simulate computer networking. I don't know. Is that bad?
[06:10] know. Is that bad?
[06:10] know. Is that bad? &gt;&gt; Um let's be specific. Let's say a video
[06:12] &gt;&gt; Um let's be specific. Let's say a video
[06:12] &gt;&gt; Um let's be specific. Let's say a video game to uh uh to help people to help
[06:15] game to uh uh to help people to help
[06:15] game to uh uh to help people to help educate people about subnetting. Don't
[06:17] educate people about subnetting. Don't
[06:18] educate people about subnetting. Don't worry about the typos. It'll figure it
[06:19] worry about the typos. It'll figure it
[06:19] worry about the typos. It'll figure it out about
[06:20] out about
[06:20] out about &gt;&gt; uh people about subnetting.
[06:22] &gt;&gt; uh people about subnetting.
[06:22] &gt;&gt; uh people about subnetting. &gt;&gt; About subnetting. I would like you to
[06:24] &gt;&gt; About subnetting. I would like you to
[06:24] &gt;&gt; About subnetting. I would like you to help me build a constitution. Here is an
[06:27] help me build a constitution. Here is an
[06:27] help me build a constitution. Here is an example of a constitution. and then
[06:29] example of a constitution. and then
[06:29] example of a constitution. and then paste in the example that we just
[06:31] paste in the example that we just
[06:31] paste in the example that we just copied. Yeah. And then send that off.
[06:33] copied. Yeah. And then send that off.
[06:33] copied. Yeah. And then send that off. Hit send. Now, this is going to take a
[06:35] Hit send. Now, this is going to take a
[06:35] Hit send. Now, this is going to take a couple seconds to generate the
[06:36] couple seconds to generate the
[06:36] couple seconds to generate the constitution. And then we're actually
[06:38] constitution. And then we're actually
[06:38] constitution. And then we're actually going to start to build this video game.
[06:39] going to start to build this video game.
[06:39] going to start to build this video game. And and while we're doing this, let's
[06:41] And and while we're doing this, let's
[06:41] And and while we're doing this, let's take a look at the next step. So the
[06:42] take a look at the next step. So the
[06:42] take a look at the next step. So the next step, you're going to use
[06:44] next step, you're going to use
[06:44] next step, you're going to use /specgetkit.specify
[06:46] /specgetkit.specify
[06:46] /specgetkit.specify to describe what you want to build.
[06:49] to describe what you want to build.
[06:49] to describe what you want to build. Focus on the what and the why, not
[06:52] Focus on the what and the why, not
[06:52] Focus on the what and the why, not things like I want it to be in Python or
[06:54] things like I want it to be in Python or
[06:54] things like I want it to be in Python or I want it to be in JavaScript or
[06:55] I want it to be in JavaScript or
[06:55] I want it to be in JavaScript or whatever. So, we're just going to take a
[06:57] whatever. So, we're just going to take a
[06:57] whatever. So, we're just going to take a second here. And we can see that it's
[06:59] second here. And we can see that it's
[06:59] second here. And we can see that it's churning here. Let me grab the actual
[07:00] churning here. Let me grab the actual
[07:00] churning here. Let me grab the actual spec kit constitution template. And it's
[07:03] spec kit constitution template. And it's
[07:03] spec kit constitution template. And it's going to give us a spec kit
[07:05] going to give us a spec kit
[07:05] going to give us a spec kit constitution. Now Andy, let's go back to
[07:07] constitution. Now Andy, let's go back to
[07:07] constitution. Now Andy, let's go back to VS Code and let's collapse the clawed
[07:10] VS Code and let's collapse the clawed
[07:10] VS Code and let's collapse the clawed folder and the specify folder. And what
[07:14] folder and the specify folder. And what
[07:14] folder and the specify folder. And what I would do is rightclick on my project
[07:16] I would do is rightclick on my project
[07:16] I would do is rightclick on my project and say new file and call this
[07:18] and say new file and call this
[07:18] and say new file and call this constitution.md.
[07:21] constitution.md.
[07:21] constitution.md. This is John's own personal way of doing
[07:23] This is John's own personal way of doing
[07:23] This is John's own personal way of doing it. I like to keep my constitution and
[07:25] it. I like to keep my constitution and
[07:26] it. I like to keep my constitution and my spec and my plan as artifacts in the
[07:29] my spec and my plan as artifacts in the
[07:30] my spec and my plan as artifacts in the git repo so that other people can see
[07:32] git repo so that other people can see
[07:32] git repo so that other people can see the exact code I use to build the video
[07:34] the exact code I use to build the video
[07:34] the exact code I use to build the video game. So in cloud desktop once we get
[07:36] game. So in cloud desktop once we get
[07:36] game. So in cloud desktop once we get the answer. Yeah, we're going to give
[07:38] the answer. Yeah, we're going to give
[07:38] the answer. Yeah, we're going to give this a little bit of time. This is going
[07:40] this a little bit of time. This is going
[07:40] this a little bit of time. This is going to churn for a bit.
[07:40] to churn for a bit.
[07:40] to churn for a bit. &gt;&gt; We'll put that in the constitution.
[07:41] &gt;&gt; We'll put that in the constitution.
[07:41] &gt;&gt; We'll put that in the constitution. &gt;&gt; We're going to put it in the
[07:42] &gt;&gt; We're going to put it in the
[07:42] &gt;&gt; We're going to put it in the constitution. And then down here, Andy,
[07:43] constitution. And then down here, Andy,
[07:44] constitution. And then down here, Andy, if you So let's launch claude code now.
[07:46] if you So let's launch claude code now.
[07:46] if you So let's launch claude code now. &gt;&gt; Uh down at the bottom in the terminal,
[07:48] &gt;&gt; Uh down at the bottom in the terminal,
[07:48] &gt;&gt; Uh down at the bottom in the terminal, just type in um claude code.
[07:51] just type in um claude code.
[07:51] just type in um claude code. &gt;&gt; Why is everything in markdown? Is that
[07:52] &gt;&gt; Why is everything in markdown? Is that
[07:52] &gt;&gt; Why is everything in markdown? Is that just like a machine readable?
[07:54] just like a machine readable?
[07:54] just like a machine readable? &gt;&gt; It's a mix between machine readable and
[07:56] &gt;&gt; It's a mix between machine readable and
[07:56] &gt;&gt; It's a mix between machine readable and human readable,
[07:56] human readable,
[07:56] human readable, &gt;&gt; right?
[07:57] &gt;&gt; right?
[07:57] &gt;&gt; right? &gt;&gt; Yeah. It and it allows for things like
[07:59] &gt;&gt; Yeah. It and it allows for things like
[07:59] &gt;&gt; Yeah. It and it allows for things like tables and bold and things like that.
[08:01] tables and bold and things like that.
[08:01] tables and bold and things like that. &gt;&gt; Like for instructions and in LLMs,
[08:03] &gt;&gt; Like for instructions and in LLMs,
[08:03] &gt;&gt; Like for instructions and in LLMs, people use markdown to give it.
[08:05] people use markdown to give it.
[08:05] people use markdown to give it. &gt;&gt; And you're not going to believe this.
[08:06] &gt;&gt; And you're not going to believe this.
[08:06] &gt;&gt; And you're not going to believe this. We're going to get a bunch of artifacts
[08:08] We're going to get a bunch of artifacts
[08:08] We're going to get a bunch of artifacts in Markdown through this process. So,
[08:11] in Markdown through this process. So,
[08:11] in Markdown through this process. So, let's just go ahead and set up the Andy
[08:13] let's just go ahead and set up the Andy
[08:13] let's just go ahead and set up the Andy just This is a fresh install of Claude
[08:15] just This is a fresh install of Claude
[08:15] just This is a fresh install of Claude Code. So, press enter. Do you have a
[08:17] Code. So, press enter. Do you have a
[08:17] Code. So, press enter. Do you have a key?
[08:17] key?
[08:17] key? &gt;&gt; Uh, I have a subscription.
[08:19] &gt;&gt; Uh, I have a subscription.
[08:19] &gt;&gt; Uh, I have a subscription. &gt;&gt; Yeah. So, do subscription. Okay, good.
[08:21] &gt;&gt; Yeah. So, do subscription. Okay, good.
[08:21] &gt;&gt; Yeah. So, do subscription. Okay, good. There it worked. You're already logged
[08:22] There it worked. You're already logged
[08:22] There it worked. You're already logged in.
[08:22] in.
[08:22] in. &gt;&gt; What's an artifact? You said that it's
[08:23] &gt;&gt; What's an artifact? You said that it's
[08:23] &gt;&gt; What's an artifact? You said that it's going to create artifact.
[08:24] going to create artifact.
[08:24] going to create artifact. &gt;&gt; Yeah, we're going to get a bunch of
[08:25] &gt;&gt; Yeah, we're going to get a bunch of
[08:26] &gt;&gt; Yeah, we're going to get a bunch of different markdown files and stuff and
[08:27] different markdown files and stuff and
[08:27] different markdown files and stuff and folders and everything. Okay. So, if you
[08:29] folders and everything. Okay. So, if you
[08:29] folders and everything. Okay. So, if you press enter to continue. Uh, sure.
[08:31] press enter to continue. Uh, sure.
[08:31] press enter to continue. Uh, sure. Recommended settings.
[08:32] Recommended settings.
[08:32] Recommended settings. &gt;&gt; Yes, I trust this folder.
[08:34] &gt;&gt; Yes, I trust this folder.
[08:34] &gt;&gt; Yes, I trust this folder. &gt;&gt; Okay. So, now if you do slashspec
[08:38] &gt;&gt; Okay. So, now if you do slashspec
[08:38] &gt;&gt; Okay. So, now if you do slashspec or specify,
[08:39] or specify,
[08:40] or specify, see how we have all these uh spec kit.
[08:42] see how we have all these uh spec kit.
[08:42] see how we have all these uh spec kit. &gt;&gt; Mhm.
[08:43] &gt;&gt; Mhm.
[08:43] &gt;&gt; Mhm. &gt;&gt; Specit constitution. Those are the
[08:45] &gt;&gt; Specit constitution. Those are the
[08:45] &gt;&gt; Specit constitution. Those are the commands we're going to use. All right.
[08:46] commands we're going to use. All right.
[08:46] commands we're going to use. All right. So, let's go see if we got a
[08:47] So, let's go see if we got a
[08:47] So, let's go see if we got a constitution yet from claw desktop. So,
[08:50] constitution yet from claw desktop. So,
[08:50] constitution yet from claw desktop. So, I would just hit copy. But if you want
[08:52] I would just hit copy. But if you want
[08:52] I would just hit copy. But if you want to kind of check out some of this to get
[08:54] to kind of check out some of this to get
[08:54] to kind of check out some of this to get a sense a lot.
[08:55] a sense a lot.
[08:55] a sense a lot. &gt;&gt; Yeah, [laughter] it's pretty big. But
[08:56] &gt;&gt; Yeah, [laughter] it's pretty big. But
[08:56] &gt;&gt; Yeah, [laughter] it's pretty big. But there's sort of core principles
[08:58] there's sort of core principles
[08:58] there's sort of core principles correctness before everything else and
[09:01] correctness before everything else and
[09:01] correctness before everything else and it talks about subnet math and it talks
[09:03] it talks about subnet math and it talks
[09:03] it talks about subnet math and it talks about RFC's and honestly like you can
[09:06] about RFC's and honestly like you can
[09:06] about RFC's and honestly like you can read it or edit it, but I just hit copy.
[09:08] read it or edit it, but I just hit copy.
[09:08] read it or edit it, but I just hit copy. &gt;&gt; Wow.
[09:09] &gt;&gt; Wow.
[09:09] &gt;&gt; Wow. &gt;&gt; Encode quality testing standards.
[09:11] &gt;&gt; Encode quality testing standards.
[09:11] &gt;&gt; Encode quality testing standards. &gt;&gt; I guess that's the magic of LLM. Like
[09:13] &gt;&gt; I guess that's the magic of LLM. Like
[09:13] &gt;&gt; I guess that's the magic of LLM. Like how did it do all this magic? So we gave
[09:15] how did it do all this magic? So we gave
[09:15] how did it do all this magic? So we gave it a template of an existing
[09:16] it a template of an existing
[09:16] it a template of an existing constitution and based on our idea of a
[09:19] constitution and based on our idea of a
[09:19] constitution and based on our idea of a video game for cedar or for subnetting
[09:21] video game for cedar or for subnetting
[09:21] video game for cedar or for subnetting this is the constitution.
[09:22] this is the constitution.
[09:22] this is the constitution. &gt;&gt; So it went out and researched
[09:24] &gt;&gt; So it went out and researched
[09:24] &gt;&gt; So it went out and researched subnetting. Yeah.
[09:25] subnetting. Yeah.
[09:25] subnetting. Yeah. &gt;&gt; And plugged it in
[09:26] &gt;&gt; And plugged it in
[09:26] &gt;&gt; And plugged it in &gt;&gt; and made it a constitution for our game.
[09:28] &gt;&gt; and made it a constitution for our game.
[09:28] &gt;&gt; and made it a constitution for our game. So you're going to hit copy in the top
[09:29] So you're going to hit copy in the top
[09:29] So you're going to hit copy in the top corner there. And let's paste this into
[09:32] corner there. And let's paste this into
[09:32] corner there. And let's paste this into our constitution.mmd file.
[09:34] our constitution.mmd file.
[09:34] our constitution.mmd file. &gt;&gt; Can I just right click that and paste
[09:35] &gt;&gt; Can I just right click that and paste
[09:35] &gt;&gt; Can I just right click that and paste or?
[09:35] or?
[09:35] or? &gt;&gt; Uh no. Just drag this down a little bit
[09:37] &gt;&gt; Uh no. Just drag this down a little bit
[09:37] &gt;&gt; Uh no. Just drag this down a little bit so we can see the inside of the file.
[09:39] so we can see the inside of the file.
[09:40] so we can see the inside of the file. &gt;&gt; We're trying to get into here, right?
[09:41] &gt;&gt; We're trying to get into here, right?
[09:41] &gt;&gt; We're trying to get into here, right? &gt;&gt; Yeah. So then paste it in. There we go.
[09:42] &gt;&gt; Yeah. So then paste it in. There we go.
[09:42] &gt;&gt; Yeah. So then paste it in. There we go. That's what we want. paste. So, just
[09:44] That's what we want. paste. So, just
[09:44] That's what we want. paste. So, just paste and save.
[09:45] paste and save.
[09:45] paste and save. &gt;&gt; Uh, that what is that? Command S. Yeah,
[09:47] &gt;&gt; Uh, that what is that? Command S. Yeah,
[09:47] &gt;&gt; Uh, that what is that? Command S. Yeah, I think my little dot there. Good.
[09:49] I think my little dot there. Good.
[09:49] I think my little dot there. Good. &gt;&gt; And then let's go back to the GitHub. I
[09:51] &gt;&gt; And then let's go back to the GitHub. I
[09:51] &gt;&gt; And then let's go back to the GitHub. I want to make sure we get the command
[09:52] want to make sure we get the command
[09:52] want to make sure we get the command right. You should be able to do /speckit
[09:56] right. You should be able to do /speckit
[09:56] right. You should be able to do /speckit constitution.
[09:57] constitution.
[09:57] constitution. &gt;&gt; So, don't grab this whole thing. Just
[09:58] &gt;&gt; So, don't grab this whole thing. Just
[09:58] &gt;&gt; So, don't grab this whole thing. Just &gt;&gt; No. No. Scroll up a little bit. Yeah.
[10:00] &gt;&gt; No. No. Scroll up a little bit. Yeah.
[10:00] &gt;&gt; No. No. Scroll up a little bit. Yeah. So, even if you just want to type in
[10:02] So, even if you just want to type in
[10:02] So, even if you just want to type in finish this specit
[10:07] &gt;&gt; constitution.
[10:08] &gt;&gt; constitution. Is it not highlighting that for you?
[10:09] Is it not highlighting that for you?
[10:09] Is it not highlighting that for you? &gt;&gt; Can I just scroll down and I update?
[10:11] &gt;&gt; Can I just scroll down and I update?
[10:12] &gt;&gt; Can I just scroll down and I update? &gt;&gt; You can try to type it in. So type spec
[10:13] &gt;&gt; You can try to type it in. So type spec
[10:13] &gt;&gt; You can try to type it in. So type spec kit-ash constitution.
[10:15] kit-ash constitution.
[10:15] kit-ash constitution. &gt;&gt; What is it?
[10:16] &gt;&gt; What is it?
[10:16] &gt;&gt; What is it? &gt;&gt; Dash
[10:17] &gt;&gt; Dash
[10:17] &gt;&gt; Dash &gt;&gt; constitution. And you should be able to
[10:19] &gt;&gt; constitution. And you should be able to
[10:19] &gt;&gt; constitution. And you should be able to tab that out maybe. And now say the
[10:22] tab that out maybe. And now say the
[10:22] tab that out maybe. And now say the constitution can be found in the
[10:24] constitution can be found in the
[10:24] constitution can be found in the constitution.mmd file.
[10:26] constitution.mmd file.
[10:26] constitution.mmd file. &gt;&gt; So I'm going to write this out.
[10:27] &gt;&gt; So I'm going to write this out.
[10:27] &gt;&gt; So I'm going to write this out. &gt;&gt; Yeah, the constitution can be found in
[10:29] &gt;&gt; Yeah, the constitution can be found in
[10:29] &gt;&gt; Yeah, the constitution can be found in the local constitution.mmd file. Please
[10:32] the local constitution.mmd file. Please
[10:32] the local constitution.mmd file. Please build me a constitution for this video
[10:34] build me a constitution for this video
[10:34] build me a constitution for this video game. I know. Constitution md file.
[10:37] game. I know. Constitution md file.
[10:37] game. I know. Constitution md file. &gt;&gt; And then and then say
[10:38] &gt;&gt; And then and then say
[10:38] &gt;&gt; And then and then say &gt;&gt; you just got to the limits of my working
[10:39] &gt;&gt; you just got to the limits of my working
[10:40] &gt;&gt; you just got to the limits of my working memory. Then say build me a constitution
[10:42] memory. Then say build me a constitution
[10:42] memory. Then say build me a constitution for this video game.
[10:43] for this video game.
[10:43] for this video game. &gt;&gt; So I have a question.
[10:44] &gt;&gt; So I have a question.
[10:44] &gt;&gt; So I have a question. &gt;&gt; Yeah. And then press enter.
[10:45] &gt;&gt; Yeah. And then press enter.
[10:46] &gt;&gt; Yeah. And then press enter. &gt;&gt; So we had it build us a constitution.
[10:48] &gt;&gt; So we had it build us a constitution.
[10:48] &gt;&gt; So we had it build us a constitution. &gt;&gt; Yeah. And now [clears throat] this is
[10:49] &gt;&gt; Yeah. And now [clears throat] this is
[10:49] &gt;&gt; Yeah. And now [clears throat] this is going to implement. See I'm going to
[10:51] going to implement. See I'm going to
[10:51] going to implement. See I'm going to explore the project structure. I'm
[10:52] explore the project structure. I'm
[10:52] explore the project structure. I'm reading the relevant file.
[10:53] reading the relevant file.
[10:53] reading the relevant file. &gt;&gt; So this the second constitution that
[10:55] &gt;&gt; So this the second constitution that
[10:55] &gt;&gt; So this the second constitution that we're creating or no?
[10:56] we're creating or no?
[10:56] we're creating or no? &gt;&gt; So three of the steps in the spec kit
[10:59] &gt;&gt; So three of the steps in the spec kit
[10:59] &gt;&gt; So three of the steps in the spec kit Andy constitution specification and
[11:02] Andy constitution specification and
[11:02] Andy constitution specification and planning require a prompt with it. So we
[11:05] planning require a prompt with it. So we
[11:05] planning require a prompt with it. So we use claude desktop to help generate the
[11:07] use claude desktop to help generate the
[11:08] use claude desktop to help generate the prompt
[11:09] prompt
[11:09] prompt &gt;&gt; that now Claude code is using okay
[11:11] &gt;&gt; that now Claude code is using okay
[11:11] &gt;&gt; that now Claude code is using okay &gt;&gt; to build the constitution. So we have to
[11:14] &gt;&gt; to build the constitution. So we have to
[11:14] &gt;&gt; to build the constitution. So we have to be a little patient here and and and
[11:16] be a little patient here and and and
[11:16] be a little patient here and and and through editing the magic of editing
[11:17] through editing the magic of editing
[11:17] through editing the magic of editing this might be a lot shorter but these
[11:19] this might be a lot shorter but these
[11:20] this might be a lot shorter but these each of these steps is going to take a
[11:21] each of these steps is going to take a
[11:21] each of these steps is going to take a bit of churn. It's reading the source
[11:23] bit of churn. It's reading the source
[11:23] bit of churn. It's reading the source constitution file the user mentioned the
[11:25] constitution file the user mentioned the
[11:25] constitution file the user mentioned the existing memory constitution and the
[11:27] existing memory constitution and the
[11:27] existing memory constitution and the template. So now it's going to take that
[11:29] template. So now it's going to take that
[11:29] template. So now it's going to take that markdown file we had and apply a
[11:31] markdown file we had and apply a
[11:31] markdown file we had and apply a template to it. So it has everything it
[11:33] template to it. So it has everything it
[11:33] template to it. So it has everything it needs. The repo is already a get repo
[11:36] needs. The repo is already a get repo
[11:36] needs. The repo is already a get repo and with an initial commit. No action
[11:38] and with an initial commit. No action
[11:38] and with an initial commit. No action needed. Let me check the dependent
[11:41] needed. Let me check the dependent
[11:41] needed. Let me check the dependent templates for alignment before writing.
[11:43] templates for alignment before writing.
[11:43] templates for alignment before writing. And now it's going to go ahead and write
[11:44] And now it's going to go ahead and write
[11:44] And now it's going to go ahead and write the constitution. And this is super dry
[11:45] the constitution. And this is super dry
[11:45] the constitution. And this is super dry and boring. I know it doesn't seem very
[11:47] and boring. I know it doesn't seem very
[11:47] and boring. I know it doesn't seem very exciting, but once we get through these
[11:49] exciting, but once we get through these
[11:49] exciting, but once we get through these steps, the very last step slashimplement
[11:53] steps, the very last step slashimplement
[11:53] steps, the very last step slashimplement generates the code. So all we're doing
[11:55] generates the code. So all we're doing
[11:55] generates the code. So all we're doing here is building up.
[11:57] here is building up.
[11:57] here is building up. &gt;&gt; I don't think this is boring. What
[11:58] &gt;&gt; I don't think this is boring. What
[11:58] &gt;&gt; I don't think this is boring. What happens for me sometimes is I get lost
[12:00] happens for me sometimes is I get lost
[12:00] happens for me sometimes is I get lost in the steps.
[12:01] in the steps.
[12:01] in the steps. &gt;&gt; Yes. like we created a constitution but
[12:03] &gt;&gt; Yes. like we created a constitution but
[12:04] &gt;&gt; Yes. like we created a constitution but we didn't we created a prompt for a
[12:05] we didn't we created a prompt for a
[12:05] we didn't we created a prompt for a constitution then we put it in our
[12:06] constitution then we put it in our
[12:06] constitution then we put it in our markdown and then we told it to create a
[12:08] markdown and then we told it to create a
[12:08] markdown and then we told it to create a constitution based on the constitution
[12:10] constitution based on the constitution
[12:10] constitution based on the constitution and the markdown
[12:11] and the markdown
[12:11] and the markdown &gt;&gt; there's a lot of recursion there I know
[12:13] &gt;&gt; there's a lot of recursion there I know
[12:13] &gt;&gt; there's a lot of recursion there I know &gt;&gt; but but I'm just saying it out loud that
[12:15] &gt;&gt; but but I'm just saying it out loud that
[12:15] &gt;&gt; but but I'm just saying it out loud that this isn't boring I think this is cool
[12:17] this isn't boring I think this is cool
[12:17] this isn't boring I think this is cool and kind of where I get lost in coding
[12:19] and kind of where I get lost in coding
[12:19] and kind of where I get lost in coding sometimes and I guess recursion is the
[12:21] sometimes and I guess recursion is the
[12:21] sometimes and I guess recursion is the word for it like you know I did a
[12:23] word for it like you know I did a
[12:23] word for it like you know I did a markdown or I I did a thing now I'm
[12:24] markdown or I I did a thing now I'm
[12:24] markdown or I I did a thing now I'm doing another thing so I'm just saying
[12:26] doing another thing so I'm just saying
[12:26] doing another thing so I'm just saying out loud where I get lost
[12:27] out loud where I get lost
[12:27] out loud where I get lost &gt;&gt; so it's asking here do we want to
[12:29] &gt;&gt; so it's asking here do we want to
[12:29] &gt;&gt; so it's asking here do we want to override the constitution I would say
[12:31] override the constitution I would say
[12:31] override the constitution I would say yes to that. I would say yes to that.
[12:33] yes to that. I would say yes to that.
[12:33] yes to that. I would say yes to that. &gt;&gt; I don't know if that's good development
[12:35] &gt;&gt; I don't know if that's good development
[12:35] &gt;&gt; I don't know if that's good development or not.
[12:35] or not.
[12:35] or not. &gt;&gt; No, no, I would say yes to that.
[12:36] &gt;&gt; No, no, I would say yes to that.
[12:36] &gt;&gt; No, no, I would say yes to that. &gt;&gt; I wish I could make the yeses go away
[12:37] &gt;&gt; I wish I could make the yeses go away
[12:38] &gt;&gt; I wish I could make the yeses go away and just make it do whatever it wants.
[12:39] and just make it do whatever it wants.
[12:39] and just make it do whatever it wants. &gt;&gt; So, constitution ratified version 1.0.
[12:42] &gt;&gt; So, constitution ratified version 1.0.
[12:42] &gt;&gt; So, constitution ratified version 1.0. Here's the five core principles. Here's
[12:45] Here's the five core principles. Here's
[12:45] Here's the five core principles. Here's the dependent templates. Do you want me
[12:46] the dependent templates. Do you want me
[12:46] the dependent templates. Do you want me to run spec kit to commit the
[12:48] to run spec kit to commit the
[12:48] to run spec kit to commit the constitution now? Yeah, you can say
[12:50] constitution now? Yeah, you can say
[12:50] constitution now? Yeah, you can say commit it. That would be fine.
[12:52] commit it. That would be fine.
[12:52] commit it. That would be fine. &gt;&gt; Can I tab or do I got to write it?
[12:53] &gt;&gt; Can I tab or do I got to write it?
[12:53] &gt;&gt; Can I tab or do I got to write it? &gt;&gt; You could tab that, I think.
[12:55] &gt;&gt; You could tab that, I think.
[12:55] &gt;&gt; You could tab that, I think. &gt;&gt; Cool.
[12:55] &gt;&gt; Cool.
[12:55] &gt;&gt; Cool. &gt;&gt; Yep. Commit it. So now that constitution
[12:57] &gt;&gt; Yep. Commit it. So now that constitution
[12:57] &gt;&gt; Yep. Commit it. So now that constitution is part of this git repository. You just
[13:00] is part of this git repository. You just
[13:00] is part of this git repository. You just say yes to this. Yes. And don't ask. I
[13:03] say yes to this. Yes. And don't ask. I
[13:03] say yes to this. Yes. And don't ask. I say yeah. So now let's go. While this is
[13:06] say yeah. So now let's go. While this is
[13:06] say yeah. So now let's go. While this is churning, let's generate our spec.
[13:09] churning, let's generate our spec.
[13:09] churning, let's generate our spec. &gt;&gt; So you see how this one here says the
[13:10] &gt;&gt; So you see how this one here says the
[13:10] &gt;&gt; So you see how this one here says the specification is build an application to
[13:12] specification is build an application to
[13:12] specification is build an application to help me organize my photos. And it's
[13:14] help me organize my photos. And it's
[13:14] help me organize my photos. And it's going to say blah blah blah. So copy
[13:15] going to say blah blah blah. So copy
[13:15] going to say blah blah blah. So copy that line here.
[13:17] that line here.
[13:17] that line here. &gt;&gt; Yeah. And let's go back to Claude.
[13:20] &gt;&gt; Yeah. And let's go back to Claude.
[13:20] &gt;&gt; Yeah. And let's go back to Claude. Yeah. Let's say yes to this thing.
[13:21] Yeah. Let's say yes to this thing.
[13:21] Yeah. Let's say yes to this thing. &gt;&gt; Aren't we already in cloud desktop?
[13:22] &gt;&gt; Aren't we already in cloud desktop?
[13:22] &gt;&gt; Aren't we already in cloud desktop? &gt;&gt; Okay. Next steps when you're ready. This
[13:24] &gt;&gt; Okay. Next steps when you're ready. This
[13:24] &gt;&gt; Okay. Next steps when you're ready. This is Claude code.
[13:25] is Claude code.
[13:25] is Claude code. &gt;&gt; We want to go back to Claude desktop.
[13:27] &gt;&gt; We want to go back to Claude desktop.
[13:28] &gt;&gt; We want to go back to Claude desktop. And now we're going to say thank you.
[13:30] And now we're going to say thank you.
[13:30] And now we're going to say thank you. &gt;&gt; Oh,
[13:30] &gt;&gt; Oh,
[13:30] &gt;&gt; Oh, &gt;&gt; here is an example of a specification.
[13:33] &gt;&gt; here is an example of a specification.
[13:33] &gt;&gt; here is an example of a specification. &gt;&gt; I love that you're thanking.
[13:34] &gt;&gt; I love that you're thanking.
[13:34] &gt;&gt; I love that you're thanking. &gt;&gt; I always thank. I know. I can't help
[13:36] &gt;&gt; I always thank. I know. I can't help
[13:36] &gt;&gt; I always thank. I know. I can't help myself.
[13:37] myself.
[13:37] myself. &gt;&gt; I' I've never thanked. Listen, when they
[13:39] &gt;&gt; I' I've never thanked. Listen, when they
[13:39] &gt;&gt; I' I've never thanked. Listen, when they take over the world and the robots come,
[13:42] take over the world and the robots come,
[13:42] take over the world and the robots come, &gt;&gt; they're going to be nice to you.
[13:43] &gt;&gt; they're going to be nice to you.
[13:43] &gt;&gt; they're going to be nice to you. &gt;&gt; They're going to make me part of the
[13:44] &gt;&gt; They're going to make me part of the
[13:44] &gt;&gt; They're going to make me part of the governing human council. They'll
[13:45] governing human council. They'll
[13:45] governing human council. They'll [laughter] keep me in a zoo with the
[13:47] [laughter] keep me in a zoo with the
[13:47] [laughter] keep me in a zoo with the other handful of humans.
[13:48] other handful of humans.
[13:48] other handful of humans. &gt;&gt; I'm saying thank you because I would
[13:49] &gt;&gt; I'm saying thank you because I would
[13:50] &gt;&gt; I'm saying thank you because I would also like to be in this zoo.
[13:51] also like to be in this zoo.
[13:52] also like to be in this zoo. &gt;&gt; So, thank you. Uh, next, I need the
[13:54] &gt;&gt; So, thank you. Uh, next, I need the
[13:54] &gt;&gt; So, thank you. Uh, next, I need the specification for this video game.
[13:56] specification for this video game.
[13:56] specification for this video game. Here's an example spec
[13:58] Here's an example spec
[13:58] Here's an example spec &gt;&gt; and then paste in what I grab.
[13:59] &gt;&gt; and then paste in what I grab.
[13:59] &gt;&gt; and then paste in what I grab. &gt;&gt; Paste that in and press and click the
[14:01] &gt;&gt; Paste that in and press and click the
[14:01] &gt;&gt; Paste that in and press and click the send. Now again, that's going to churn a
[14:03] send. Now again, that's going to churn a
[14:03] send. Now again, that's going to churn a little bit. So I would close hit the X
[14:07] little bit. So I would close hit the X
[14:07] little bit. So I would close hit the X in the top corner here cuz we're all
[14:08] in the top corner here cuz we're all
[14:08] in the top corner here cuz we're all done with the constitution.
[14:09] done with the constitution.
[14:09] done with the constitution. &gt;&gt; So what did we just ask for? We asked
[14:11] &gt;&gt; So what did we just ask for? We asked
[14:11] &gt;&gt; So what did we just ask for? We asked &gt;&gt; So if you look at the GitHub steps, the
[14:14] &gt;&gt; So if you look at the GitHub steps, the
[14:14] &gt;&gt; So if you look at the GitHub steps, the very first step is to generate your
[14:16] very first step is to generate your
[14:16] very first step is to generate your constitution, your highle guard rails.
[14:19] constitution, your highle guard rails.
[14:19] constitution, your highle guard rails. Then very next thing is the specify
[14:21] Then very next thing is the specify
[14:21] Then very next thing is the specify which is what we're doing now is the
[14:23] which is what we're doing now is the
[14:23] which is what we're doing now is the actual spec. So if you go back into VS
[14:27] actual spec. So if you go back into VS
[14:27] actual spec. So if you go back into VS Code, I would make a new file called
[14:30] Code, I would make a new file called
[14:30] Code, I would make a new file called spec.md
[14:31] spec.md
[14:31] spec.md &gt;&gt; in the project. Is that the right place?
[14:33] &gt;&gt; in the project. Is that the right place?
[14:33] &gt;&gt; in the project. Is that the right place? &gt;&gt; You and your markdowns.
[14:34] &gt;&gt; You and your markdowns.
[14:34] &gt;&gt; You and your markdowns. &gt;&gt; Yep.
[14:35] &gt;&gt; Yep.
[14:35] &gt;&gt; Yep. &gt;&gt; Now if we go back to the process, Andy,
[14:38] &gt;&gt; Now if we go back to the process, Andy,
[14:38] &gt;&gt; Now if we go back to the process, Andy, after the spec, our next step is a plan.
[14:43] after the spec, our next step is a plan.
[14:43] after the spec, our next step is a plan. So a command to provide your text stack
[14:45] So a command to provide your text stack
[14:45] So a command to provide your text stack and architectural choices. So if I want
[14:47] and architectural choices. So if I want
[14:47] and architectural choices. So if I want this to be a Python game, if I want it
[14:49] this to be a Python game, if I want it
[14:49] this to be a Python game, if I want it to be a based in a web browser game, are
[14:51] to be a based in a web browser game, are
[14:51] to be a based in a web browser game, are different architectural choices. But if
[14:53] different architectural choices. But if
[14:53] different architectural choices. But if you scroll up a little bit, there's a
[14:55] you scroll up a little bit, there's a
[14:55] you scroll up a little bit, there's a undocumented step we're going to do
[14:57] undocumented step we're going to do
[14:58] undocumented step we're going to do called clarify.
[15:00] called clarify.
[15:00] called clarify. &gt;&gt; So after we have our spec and our
[15:01] &gt;&gt; So after we have our spec and our
[15:01] &gt;&gt; So after we have our spec and our constitution, we can actually ask the
[15:03] constitution, we can actually ask the
[15:03] constitution, we can actually ask the LLM, is there anything you need to
[15:04] LLM, is there anything you need to
[15:04] LLM, is there anything you need to clarify so far? Like is everything clear
[15:06] clarify so far? Like is everything clear
[15:06] clarify so far? Like is everything clear to you or do you have any questions to
[15:08] to you or do you have any questions to
[15:08] to you or do you have any questions to me, the human developer?
[15:10] me, the human developer?
[15:10] me, the human developer? &gt;&gt; That seems pretty amazing.
[15:11] &gt;&gt; That seems pretty amazing.
[15:11] &gt;&gt; That seems pretty amazing. &gt;&gt; It's really neat. And it'll ask you up
[15:13] &gt;&gt; It's really neat. And it'll ask you up
[15:13] &gt;&gt; It's really neat. And it'll ask you up to five questions like, okay, you didn't
[15:15] to five questions like, okay, you didn't
[15:15] to five questions like, okay, you didn't tell me whether or not this should be
[15:16] tell me whether or not this should be
[15:16] tell me whether or not this should be Python or JavaScript. Which framework
[15:18] Python or JavaScript. Which framework
[15:18] Python or JavaScript. Which framework would you like to use? That kind of
[15:19] would you like to use? That kind of
[15:19] would you like to use? That kind of interrogation.
[15:20] interrogation.
[15:20] interrogation. &gt;&gt; I have another question. the software
[15:22] &gt;&gt; I have another question. the software
[15:22] &gt;&gt; I have another question. the software that I've been developing in cloud code.
[15:24] that I've been developing in cloud code.
[15:24] that I've been developing in cloud code. I haven't been doing this. Should this
[15:26] I haven't been doing this. Should this
[15:26] I haven't been doing this. Should this be my new way forward for things I
[15:29] be my new way forward for things I
[15:29] be my new way forward for things I built?
[15:29] built?
[15:29] built? &gt;&gt; So, I mean me personally, I would say
[15:32] &gt;&gt; So, I mean me personally, I would say
[15:32] &gt;&gt; So, I mean me personally, I would say yes.
[15:32] yes.
[15:32] yes. &gt;&gt; Like this is more structured than what
[15:34] &gt;&gt; Like this is more structured than what
[15:34] &gt;&gt; Like this is more structured than what I've been doing. This seems better cuz
[15:36] I've been doing. This seems better cuz
[15:36] I've been doing. This seems better cuz I'm I'm following a coding framework.
[15:38] I'm I'm following a coding framework.
[15:38] I'm I'm following a coding framework. &gt;&gt; Well, and just wait until we get to some
[15:40] &gt;&gt; Well, and just wait until we get to some
[15:40] &gt;&gt; Well, and just wait until we get to some of the markdown that this is going to
[15:42] of the markdown that this is going to
[15:42] of the markdown that this is going to generate. It generates user stories,
[15:44] generate. It generates user stories,
[15:44] generate. It generates user stories, Andy, with functional requirements. And
[15:47] Andy, with functional requirements. And
[15:47] Andy, with functional requirements. And it's like it's a real software
[15:48] it's like it's a real software
[15:48] it's like it's a real software development thing. And this following a
[15:51] development thing. And this following a
[15:51] development thing. And this following a real software development thing will
[15:53] real software development thing will
[15:53] real software development thing will give us better code, better results,
[15:56] give us better code, better results,
[15:56] give us better code, better results, right? It's not just
[15:57] right? It's not just
[15:57] right? It's not just &gt;&gt; and the spec matches your your intent
[16:00] &gt;&gt; and the spec matches your your intent
[16:00] &gt;&gt; and the spec matches your your intent always matches the code. There's
[16:02] always matches the code. There's
[16:02] always matches the code. There's &gt;&gt; very clear like our intent is very clear
[16:04] &gt;&gt; very clear like our intent is very clear
[16:04] &gt;&gt; very clear like our intent is very clear because of this,
[16:05] because of this,
[16:05] because of this, &gt;&gt; right? And when we're done this
[16:06] &gt;&gt; right? And when we're done this
[16:06] &gt;&gt; right? And when we're done this exercise, other people who want to know
[16:08] exercise, other people who want to know
[16:08] exercise, other people who want to know how we built this video game can read
[16:11] how we built this video game can read
[16:11] how we built this video game can read the specs and the and the artifacts that
[16:13] the specs and the and the artifacts that
[16:13] the specs and the and the artifacts that we generate, right? So let's say that
[16:15] we generate, right? So let's say that
[16:15] we generate, right? So let's say that the website you just made like you don't
[16:17] the website you just made like you don't
[16:17] the website you just made like you don't have to start a project as spec driven
[16:19] have to start a project as spec driven
[16:19] have to start a project as spec driven but you could finish it as spec driven.
[16:21] but you could finish it as spec driven.
[16:21] but you could finish it as spec driven. &gt;&gt; Well what I've done is I ask claude for
[16:24] &gt;&gt; Well what I've done is I ask claude for
[16:24] &gt;&gt; Well what I've done is I ask claude for a spec for something
[16:25] a spec for something
[16:25] a spec for something &gt;&gt; right
[16:26] &gt;&gt; right
[16:26] &gt;&gt; right &gt;&gt; but that's it. Then I just say okay
[16:28] &gt;&gt; but that's it. Then I just say okay
[16:28] &gt;&gt; but that's it. Then I just say okay let's use or maybe it's a pro. I don't
[16:30] let's use or maybe it's a pro. I don't
[16:30] let's use or maybe it's a pro. I don't know if it's a spec or a prompt.
[16:32] know if it's a spec or a prompt.
[16:32] know if it's a spec or a prompt. &gt;&gt; Pretty close. I've created spec
[16:33] &gt;&gt; Pretty close. I've created spec
[16:33] &gt;&gt; Pretty close. I've created spec &gt;&gt; and it's markdown, right?
[16:35] &gt;&gt; and it's markdown, right?
[16:35] &gt;&gt; and it's markdown, right? &gt;&gt; Most of the time.
[16:36] &gt;&gt; Most of the time.
[16:36] &gt;&gt; Most of the time. &gt;&gt; This is like the problem. Like maybe I
[16:38] &gt;&gt; This is like the problem. Like maybe I
[16:38] &gt;&gt; This is like the problem. Like maybe I think I'd have to look, but I I'm like,
[16:40] think I'd have to look, but I I'm like,
[16:40] think I'd have to look, but I I'm like, "Yes, let's create a specification." And
[16:41] "Yes, let's create a specification." And
[16:41] "Yes, let's create a specification." And then I feed that in and like, "Okay,
[16:43] then I feed that in and like, "Okay,
[16:43] then I feed that in and like, "Okay, let's build this."
[16:44] let's build this."
[16:44] let's build this." &gt;&gt; But I'm not following this framework.
[16:46] &gt;&gt; But I'm not following this framework.
[16:46] &gt;&gt; But I'm not following this framework. &gt;&gt; I'm basically just giving whatever spec
[16:47] &gt;&gt; I'm basically just giving whatever spec
[16:47] &gt;&gt; I'm basically just giving whatever spec it created to itself again. Okay.
[16:49] it created to itself again. Okay.
[16:49] it created to itself again. Okay. &gt;&gt; Say, "All right, let's go do that."
[16:50] &gt;&gt; Say, "All right, let's go do that."
[16:50] &gt;&gt; Say, "All right, let's go do that." &gt;&gt; Pretty close,
[16:51] &gt;&gt; Pretty close,
[16:51] &gt;&gt; Pretty close, &gt;&gt; but this is better.
[16:52] &gt;&gt; but this is better.
[16:52] &gt;&gt; but this is better. &gt;&gt; It's a little more formal. Yeah. Okay.
[16:54] &gt;&gt; It's a little more formal. Yeah. Okay.
[16:54] &gt;&gt; It's a little more formal. Yeah. Okay. So, here we go. I pulled the current
[16:55] So, here we go. I pulled the current
[16:55] So, here we go. I pulled the current spec template. One judgment call I had
[16:58] spec template. One judgment call I had
[16:58] spec template. One judgment call I had to make. your prompt doesn't pin down
[16:59] to make. your prompt doesn't pin down
[16:59] to make. your prompt doesn't pin down the core gameplay loop. That's fine. So,
[17:03] the core gameplay loop. That's fine. So,
[17:03] the core gameplay loop. That's fine. So, it's going to make a game that's a
[17:04] it's going to make a game that's a
[17:04] it's going to make a game that's a typing tutor like Dolingo, but for
[17:07] typing tutor like Dolingo, but for
[17:07] typing tutor like Dolingo, but for subnetting. Dual Lingo for subnetting
[17:09] subnetting. Dual Lingo for subnetting
[17:09] subnetting. Dual Lingo for subnetting sounds pretty kickass to me.
[17:11] sounds pretty kickass to me.
[17:11] sounds pretty kickass to me. &gt;&gt; Sounds really good.
[17:12] &gt;&gt; Sounds really good.
[17:12] &gt;&gt; Sounds really good. &gt;&gt; Yeah.
[17:12] &gt;&gt; Yeah.
[17:12] &gt;&gt; Yeah. &gt;&gt; The fact that we're going to open source
[17:14] &gt;&gt; The fact that we're going to open source
[17:14] &gt;&gt; The fact that we're going to open source this thing and people are going to steal
[17:15] this thing and people are going to steal
[17:15] this thing and people are going to steal it, make a million dollars makes me
[17:17] it, make a million dollars makes me
[17:17] it, make a million dollars makes me crazy, John.
[17:18] crazy, John.
[17:18] crazy, John. &gt;&gt; You and William and your open source
[17:20] &gt;&gt; You and William and your open source
[17:20] &gt;&gt; You and William and your open source nonsense. [laughter]
[17:22] nonsense. [laughter]
[17:22] nonsense. [laughter] &gt;&gt; I'm kidding. No, this it sounds really
[17:23] &gt;&gt; I'm kidding. No, this it sounds really
[17:23] &gt;&gt; I'm kidding. No, this it sounds really cool.
[17:24] cool.
[17:24] cool. &gt;&gt; Hey, it's not my code, it's our code.
[17:26] &gt;&gt; Hey, it's not my code, it's our code.
[17:26] &gt;&gt; Hey, it's not my code, it's our code. [laughter] I'm a dot communist.
[17:28] [laughter] I'm a dot communist.
[17:28] [laughter] I'm a dot communist. &gt;&gt; Once you said dual lingo for subnetting,
[17:30] &gt;&gt; Once you said dual lingo for subnetting,
[17:30] &gt;&gt; Once you said dual lingo for subnetting, I'm like, "Oh my god, we could get rich.
[17:32] I'm like, "Oh my god, we could get rich.
[17:32] I'm like, "Oh my god, we could get rich. Why are we doing this publicly?"
[17:33] Why are we doing this publicly?"
[17:33] Why are we doing this publicly?" &gt;&gt; Hey, you never know. You never know. You
[17:35] &gt;&gt; Hey, you never know. You never know. You
[17:35] &gt;&gt; Hey, you never know. You never know. You know, we actually, you know what we
[17:36] know, we actually, you know what we
[17:36] know, we actually, you know what we could do? We could build a service, a
[17:37] could do? We could build a service, a
[17:37] could do? We could build a service, a professional services layer on top of
[17:39] professional services layer on top of
[17:39] professional services layer on top of it. And the code is free, but the
[17:41] it. And the code is free, but the
[17:41] it. And the code is free, but the professional services cost.
[17:43] professional services cost.
[17:43] professional services cost. &gt;&gt; And I'm half joking. I had such a hard
[17:44] &gt;&gt; And I'm half joking. I had such a hard
[17:44] &gt;&gt; And I'm half joking. I had such a hard time learning subnetting. If this were
[17:46] time learning subnetting. If this were
[17:46] time learning subnetting. If this were useful and helpful to folks,
[17:47] useful and helpful to folks,
[17:47] useful and helpful to folks, &gt;&gt; right,
[17:47] &gt;&gt; right,
[17:48] &gt;&gt; right, &gt;&gt; great.
[17:48] &gt;&gt; great.
[17:48] &gt;&gt; great. &gt;&gt; I know. So, here we go. We have the spec
[17:51] &gt;&gt; I know. So, here we go. We have the spec
[17:51] &gt;&gt; I know. So, here we go. We have the spec review and acceptance checklist open
[17:54] review and acceptance checklist open
[17:54] review and acceptance checklist open questions to resolve and see how it says
[17:56] questions to resolve and see how it says
[17:56] questions to resolve and see how it says use clarify.
[17:57] use clarify.
[17:57] use clarify. &gt;&gt; Yeah.
[17:58] &gt;&gt; Yeah.
[17:58] &gt;&gt; Yeah. &gt;&gt; So these are the things it's going to
[17:59] &gt;&gt; So these are the things it's going to
[17:59] &gt;&gt; So these are the things it's going to clarify. So what I would do is copy
[18:01] clarify. So what I would do is copy
[18:01] clarify. So what I would do is copy this. Actually just hit copy in the top
[18:04] this. Actually just hit copy in the top
[18:04] this. Actually just hit copy in the top corner.
[18:04] corner.
[18:04] corner. &gt;&gt; Okay.
[18:05] &gt;&gt; Okay.
[18:05] &gt;&gt; Okay. &gt;&gt; And then we're going to paste this into
[18:07] &gt;&gt; And then we're going to paste this into
[18:07] &gt;&gt; And then we're going to paste this into the spec file spec.md
[18:10] the spec file spec.md
[18:10] the spec file spec.md &gt;&gt; and save it. And then we're going to do
[18:11] &gt;&gt; and save it. And then we're going to do
[18:11] &gt;&gt; and save it. And then we're going to do the same thing. So down here we're going
[18:13] the same thing. So down here we're going
[18:13] the same thing. So down here we're going to do slashspec or slspecit
[18:18] to do slashspec or slspecit
[18:18] to do slashspec or slspecit specify. And you could tab that out and
[18:20] specify. And you could tab that out and
[18:20] specify. And you could tab that out and say the the specs are in the spec.md
[18:23] say the the specs are in the spec.md
[18:23] say the the specs are in the spec.md file for this video game, let's say.
[18:25] file for this video game, let's say.
[18:25] file for this video game, let's say. Okay, enter. And let's just Okay, I'll
[18:26] Okay, enter. And let's just Okay, I'll
[18:26] Okay, enter. And let's just Okay, I'll start by handling pre-execution hooks,
[18:28] start by handling pre-execution hooks,
[18:28] start by handling pre-execution hooks, locating the spec source file. Let me
[18:30] locating the spec source file. Let me
[18:30] locating the spec source file. Let me read the spec file and the spec
[18:32] read the spec file and the spec
[18:32] read the spec file and the spec template. So, Andy, you see this
[18:34] template. So, Andy, you see this
[18:34] template. So, Andy, you see this specify? If you expand that, all it is
[18:36] specify? If you expand that, all it is
[18:36] specify? If you expand that, all it is is a bunch of templates.
[18:39] is a bunch of templates.
[18:39] is a bunch of templates. &gt;&gt; See, there's a constitution template, a
[18:40] &gt;&gt; See, there's a constitution template, a
[18:40] &gt;&gt; See, there's a constitution template, a spec template, a plan template. It's
[18:43] spec template, a plan template. It's
[18:43] spec template, a plan template. It's those are markdown files over here.
[18:45] those are markdown files over here.
[18:45] those are markdown files over here. Let's hit yes. We didn't we're not in
[18:47] Let's hit yes. We didn't we're not in
[18:47] Let's hit yes. We didn't we're not in yolo mode so we have to answer all this.
[18:49] yolo mode so we have to answer all this.
[18:49] yolo mode so we have to answer all this. Yeah. Go down and just say yes and don't
[18:51] Yeah. Go down and just say yes and don't
[18:51] Yeah. Go down and just say yes and don't ask again. So this is the specification
[18:54] ask again. So this is the specification
[18:54] ask again. So this is the specification which is I like our requirements for our
[18:56] which is I like our requirements for our
[18:56] which is I like our requirements for our video game. The specs that we want to
[18:58] video game. The specs that we want to
[18:58] video game. The specs that we want to guide the game.
[18:59] guide the game.
[18:59] guide the game. &gt;&gt; So we did the constitution first. This
[19:01] &gt;&gt; So we did the constitution first. This
[19:02] &gt;&gt; So we did the constitution first. This is
[19:02] is
[19:02] is &gt;&gt; high level guardrails. This is the spec.
[19:04] &gt;&gt; high level guardrails. This is the spec.
[19:04] &gt;&gt; high level guardrails. This is the spec. &gt;&gt; This is a little lower down. Yeah. Just
[19:06] &gt;&gt; This is a little lower down. Yeah. Just
[19:06] &gt;&gt; This is a little lower down. Yeah. Just say yes and don't ask again. There's a
[19:08] say yes and don't ask again. There's a
[19:08] say yes and don't ask again. There's a way to do that where you say dangerously
[19:10] way to do that where you say dangerously
[19:10] way to do that where you say dangerously skip permissions or whatever. We should
[19:11] skip permissions or whatever. We should
[19:11] skip permissions or whatever. We should maybe we should have done that.
[19:13] maybe we should have done that.
[19:13] maybe we should have done that. &gt;&gt; Answer that now or is it too late?
[19:14] &gt;&gt; Answer that now or is it too late?
[19:14] &gt;&gt; Answer that now or is it too late? &gt;&gt; Uh well it's not too late. We would have
[19:15] &gt;&gt; Uh well it's not too late. We would have
[19:15] &gt;&gt; Uh well it's not too late. We would have to break out of Claude, though. Here's
[19:17] to break out of Claude, though. Here's
[19:17] to break out of Claude, though. Here's what I want to show you. So, if you
[19:18] what I want to show you. So, if you
[19:18] what I want to show you. So, if you collapse specify,
[19:20] collapse specify,
[19:20] collapse specify, &gt;&gt; this is when it starts to get really
[19:21] &gt;&gt; this is when it starts to get really
[19:22] &gt;&gt; this is when it starts to get really exciting, Andy. Notice there's a new
[19:23] exciting, Andy. Notice there's a new
[19:23] exciting, Andy. Notice there's a new folder called specs.
[19:24] folder called specs.
[19:24] folder called specs. &gt;&gt; Mhm.
[19:25] &gt;&gt; Mhm.
[19:25] &gt;&gt; Mhm. &gt;&gt; Expand that. Notice how it's 001 and and
[19:28] &gt;&gt; Expand that. Notice how it's 001 and and
[19:28] &gt;&gt; Expand that. Notice how it's 001 and and it's called subnetting game. And you see
[19:30] it's called subnetting game. And you see
[19:30] it's called subnetting game. And you see how git has changed us into a new branch
[19:33] how git has changed us into a new branch
[19:33] how git has changed us into a new branch called subnetting game.
[19:34] called subnetting game.
[19:34] called subnetting game. &gt;&gt; How do I know that? Because of this
[19:36] &gt;&gt; How do I know that? Because of this
[19:36] &gt;&gt; How do I know that? Because of this thing here.
[19:37] thing here.
[19:37] thing here. &gt;&gt; So, it's handling all the version and
[19:38] &gt;&gt; So, it's handling all the version and
[19:38] &gt;&gt; So, it's handling all the version and source control for us.
[19:39] source control for us.
[19:40] source control for us. &gt;&gt; So, what did it branch? We were in the
[19:41] &gt;&gt; So, what did it branch? We were in the
[19:41] &gt;&gt; So, what did it branch? We were in the main branch of git and it actually made
[19:44] main branch of git and it actually made
[19:44] main branch of git and it actually made a subbranch
[19:46] a subbranch
[19:46] a subbranch &gt;&gt; but there was nothing there yet.
[19:47] &gt;&gt; but there was nothing there yet.
[19:47] &gt;&gt; but there was nothing there yet. &gt;&gt; There was nothing there yet. No
[19:48] &gt;&gt; There was nothing there yet. No
[19:48] &gt;&gt; There was nothing there yet. No &gt;&gt; sub branch nothing
[19:49] &gt;&gt; sub branch nothing
[19:49] &gt;&gt; sub branch nothing &gt;&gt; and now it's right. It branched nothing
[19:52] &gt;&gt; and now it's right. It branched nothing
[19:52] &gt;&gt; and now it's right. It branched nothing to track our work inside of this get
[19:54] to track our work inside of this get
[19:54] to track our work inside of this get branch.
[19:55] branch.
[19:55] branch. &gt;&gt; I thought you branched like the master
[19:56] &gt;&gt; I thought you branched like the master
[19:56] &gt;&gt; I thought you branched like the master which was the
[19:57] which was the
[19:57] which was the &gt;&gt; Yes. So we were in main
[19:59] &gt;&gt; Yes. So we were in main
[19:59] &gt;&gt; Yes. So we were in main &gt;&gt; but there was nothing [clears throat]
[20:00] &gt;&gt; but there was nothing [clears throat]
[20:00] &gt;&gt; but there was nothing [clears throat] there yet. Nothing in main but it's
[20:01] there yet. Nothing in main but it's
[20:01] there yet. Nothing in main but it's fine.
[20:01] fine.
[20:02] fine. &gt;&gt; It's fine.
[20:02] &gt;&gt; It's fine.
[20:02] &gt;&gt; It's fine. &gt;&gt; It doesn't matter.
[20:03] &gt;&gt; It doesn't matter.
[20:03] &gt;&gt; It doesn't matter. &gt;&gt; No, it just wants to track all the work
[20:05] &gt;&gt; No, it just wants to track all the work
[20:05] &gt;&gt; No, it just wants to track all the work for this very specific spec under this
[20:08] for this very specific spec under this
[20:08] for this very specific spec under this very specific branch. Okay,
[20:10] very specific branch. Okay,
[20:10] very specific branch. Okay, &gt;&gt; so let's say we we said we wanted to add
[20:12] &gt;&gt; so let's say we we said we wanted to add
[20:12] &gt;&gt; so let's say we we said we wanted to add quality of service to this game.
[20:14] quality of service to this game.
[20:14] quality of service to this game. &gt;&gt; This is version control for the spec.
[20:16] &gt;&gt; This is version control for the spec.
[20:16] &gt;&gt; This is version control for the spec. &gt;&gt; Version control for the spec.
[20:17] &gt;&gt; Version control for the spec.
[20:17] &gt;&gt; Version control for the spec. &gt;&gt; Branching code rep. But when we get the
[20:21] &gt;&gt; Branching code rep. But when we get the
[20:21] &gt;&gt; Branching code rep. But when we get the code generated, it will be in this
[20:23] code generated, it will be in this
[20:23] code generated, it will be in this branch.
[20:23] branch.
[20:23] branch. &gt;&gt; Okay. Thank you for bearing with me. My
[20:25] &gt;&gt; Okay. Thank you for bearing with me. My
[20:25] &gt;&gt; Okay. Thank you for bearing with me. My &gt;&gt; check this out. Click on the spec.md,
[20:27] &gt;&gt; check this out. Click on the spec.md,
[20:27] &gt;&gt; check this out. Click on the spec.md, not our spec.md, but this spec.md. Yep.
[20:30] not our spec.md, but this spec.md. Yep.
[20:30] not our spec.md, but this spec.md. Yep. And it's just a template right now. See
[20:33] And it's just a template right now. See
[20:33] And it's just a template right now. See how feature name and Right. So it's just
[20:35] how feature name and Right. So it's just
[20:35] how feature name and Right. So it's just a template.
[20:35] a template.
[20:35] a template. &gt;&gt; Clo's going to um populate that or
[20:38] &gt;&gt; Clo's going to um populate that or
[20:38] &gt;&gt; Clo's going to um populate that or answer these. let me write the spec. So,
[20:41] answer these. let me write the spec. So,
[20:41] answer these. let me write the spec. So, yes, it's going to change this whole
[20:44] yes, it's going to change this whole
[20:44] yes, it's going to change this whole markdown file to have all of our
[20:46] markdown file to have all of our
[20:46] markdown file to have all of our specifications for the game as soon as
[20:48] specifications for the game as soon as
[20:48] specifications for the game as soon as it's done uh churning here.
[20:50] it's done uh churning here.
[20:50] it's done uh churning here. &gt;&gt; This episode of The Art of Network
[20:52] &gt;&gt; This episode of The Art of Network
[20:52] &gt;&gt; This episode of The Art of Network Engineering is sponsored by Meter. If
[20:54] Engineering is sponsored by Meter. If
[20:54] Engineering is sponsored by Meter. If you've ever been through a major network
[20:56] you've ever been through a major network
[20:56] you've ever been through a major network refresh, you know the grind. New
[20:58] refresh, you know the grind. New
[20:58] refresh, you know the grind. New hardware, new contracts, new vendors,
[21:01] hardware, new contracts, new vendors,
[21:01] hardware, new contracts, new vendors, then a few years later, you're doing it
[21:03] then a few years later, you're doing it
[21:03] then a few years later, you're doing it all over again. Meter was built to break
[21:06] all over again. Meter was built to break
[21:06] all over again. Meter was built to break that cycle. They deliver internet
[21:08] that cycle. They deliver internet
[21:08] that cycle. They deliver internet infrastructure for the enterprise
[21:09] infrastructure for the enterprise
[21:09] infrastructure for the enterprise through a fully integrated platform that
[21:11] through a fully integrated platform that
[21:12] through a fully integrated platform that brings together the hardware, software,
[21:14] brings together the hardware, software,
[21:14] brings together the hardware, software, deployment, life cycle management, and
[21:16] deployment, life cycle management, and
[21:16] deployment, life cycle management, and support. Instead of managing complicated
[21:19] support. Instead of managing complicated
[21:19] support. Instead of managing complicated systems and multiple vendors, Meter
[21:21] systems and multiple vendors, Meter
[21:21] systems and multiple vendors, Meter gives enterprises a more unified
[21:23] gives enterprises a more unified
[21:23] gives enterprises a more unified operational model with predictable
[21:25] operational model with predictable
[21:25] operational model with predictable pricing, managed migration, upgrade
[21:27] pricing, managed migration, upgrade
[21:27] pricing, managed migration, upgrade credits for existing hardware, and 247
[21:30] credits for existing hardware, and 247
[21:30] credits for existing hardware, and 247 support. The result is a networking
[21:32] support. The result is a networking
[21:32] support. The result is a networking experience designed to reduce complexity
[21:34] experience designed to reduce complexity
[21:34] experience designed to reduce complexity and help IT teams focus less on
[21:36] and help IT teams focus less on
[21:36] and help IT teams focus less on low-level infrastructure management and
[21:38] low-level infrastructure management and
[21:38] low-level infrastructure management and more on enabling the business. Thanks to
[21:41] more on enabling the business. Thanks to
[21:41] more on enabling the business. Thanks to Meter for sponsoring this episode. Go to
[21:43] Meter for sponsoring this episode. Go to
[21:43] Meter for sponsoring this episode. Go to meter.com/aw1
[21:45] meter.com/aw1
[21:45] meter.com/aw1 to book a demo now. That's me.com/aw1.
[21:52] Now back to the show.
[21:52] Now back to the show. &gt;&gt; How long would this have taken?
[21:53] &gt;&gt; How long would this have taken?
[21:53] &gt;&gt; How long would this have taken? &gt;&gt; Oh, by hand?
[21:54] &gt;&gt; Oh, by hand?
[21:54] &gt;&gt; Oh, by hand? &gt;&gt; Yes.
[21:55] &gt;&gt; Yes.
[21:55] &gt;&gt; Yes. &gt;&gt; Huh.
[21:55] &gt;&gt; Huh.
[21:55] &gt;&gt; Huh. &gt;&gt; Yeah.
[21:56] &gt;&gt; Yeah.
[21:56] &gt;&gt; Yeah. &gt;&gt; I mean,
[21:57] &gt;&gt; I mean,
[21:57] &gt;&gt; I mean, &gt;&gt; insane. We would still be planning the
[21:59] &gt;&gt; insane. We would still be planning the
[21:59] &gt;&gt; insane. We would still be planning the game like we are planning the game right
[22:01] game like we are planning the game right
[22:01] game like we are planning the game right now but you know like to actually write
[22:03] now but you know like to actually write
[22:03] now but you know like to actually write a video game like I mean it might take
[22:05] a video game like I mean it might take
[22:05] a video game like I mean it might take you weeks to months to years depending
[22:07] you weeks to months to years depending
[22:07] you weeks to months to years depending on your proficiency as a coder right
[22:09] on your proficiency as a coder right
[22:10] on your proficiency as a coder right &gt;&gt; now you were a computer software major
[22:13] &gt;&gt; now you were a computer software major
[22:13] &gt;&gt; now you were a computer software major right
[22:13] right
[22:13] right &gt;&gt; the quality of code that this generates
[22:17] &gt;&gt; the quality of code that this generates
[22:17] &gt;&gt; the quality of code that this generates is it good
[22:18] is it good
[22:18] is it good &gt;&gt; it's good it works it runs I feel like
[22:21] &gt;&gt; it's good it works it runs I feel like
[22:21] &gt;&gt; it's good it works it runs I feel like we've entered another introduced the
[22:23] we've entered another introduced the
[22:23] we've entered another introduced the layer of abstraction
[22:25] layer of abstraction
[22:25] layer of abstraction &gt;&gt; do you really need to read the code as a
[22:27] &gt;&gt; do you really need to read the code as a
[22:27] &gt;&gt; do you really need to read the code as a networker like if the game works. Do you
[22:29] networker like if the game works. Do you
[22:29] networker like if the game works. Do you know what I mean? Like when I pip when I
[22:31] know what I mean? Like when I pip when I
[22:31] know what I mean? Like when I pip when I pip install a package for Python.
[22:33] pip install a package for Python.
[22:33] pip install a package for Python. &gt;&gt; Well, there's a punch down thing that
[22:34] &gt;&gt; Well, there's a punch down thing that
[22:34] &gt;&gt; Well, there's a punch down thing that happens like well you don't understand
[22:35] happens like well you don't understand
[22:35] happens like well you don't understand what you're doing. It's that's the thing
[22:37] what you're doing. It's that's the thing
[22:37] what you're doing. It's that's the thing that I'm playing with in my head like
[22:39] that I'm playing with in my head like
[22:39] that I'm playing with in my head like well I don't but if it works I mean I
[22:42] well I don't but if it works I mean I
[22:42] well I don't but if it works I mean I guess there's security and
[22:42] guess there's security and
[22:42] guess there's security and vulnerabilities but then there's a
[22:44] vulnerabilities but then there's a
[22:44] vulnerabilities but then there's a security thing that you can install that
[22:45] security thing that you can install that
[22:45] security thing that you can install that like for which I've been doing. So
[22:47] like for which I've been doing. So
[22:47] like for which I've been doing. So &gt;&gt; okay so let's maximize this screen
[22:50] &gt;&gt; okay so let's maximize this screen
[22:50] &gt;&gt; okay so let's maximize this screen actually. So it's actually it has some
[22:51] actually. So it's actually it has some
[22:52] actually. So it's actually it has some questions for us. Who is the primary
[22:53] questions for us. Who is the primary
[22:53] questions for us. Who is the primary audience here Andy? Complete beginners
[22:55] audience here Andy? Complete beginners
[22:55] audience here Andy? Complete beginners CCNA's classroom. So this isn't that
[22:58] CCNA's classroom. So this isn't that
[22:58] CCNA's classroom. So this isn't that clarification thing. So the spec passes
[23:01] clarification thing. So the spec passes
[23:01] clarification thing. So the spec passes all quality checks, but there's three
[23:03] all quality checks, but there's three
[23:03] all quality checks, but there's three deliberate needs clarification markers.
[23:06] deliberate needs clarification markers.
[23:06] deliberate needs clarification markers. So let's say complete beginners. Let's
[23:07] So let's say complete beginners. Let's
[23:07] So let's say complete beginners. Let's make this game for like very very
[23:10] make this game for like very very
[23:10] make this game for like very very beginners. Oh, do we want IPv6 core and
[23:13] beginners. Oh, do we want IPv6 core and
[23:13] beginners. Oh, do we want IPv6 core and IPv6? Just IPv4.
[23:15] IPv6? Just IPv4.
[23:15] IPv6? Just IPv4. &gt;&gt; Just four.
[23:16] &gt;&gt; Just four.
[23:16] &gt;&gt; Just four. &gt;&gt; So let's do the second one. No, let's do
[23:19] &gt;&gt; So let's do the second one. No, let's do
[23:19] &gt;&gt; So let's do the second one. No, let's do the third one.
[23:20] the third one.
[23:20] the third one. &gt;&gt; Core and supernetting.
[23:22] &gt;&gt; Core and supernetting.
[23:22] &gt;&gt; Core and supernetting. &gt;&gt; Is that like cider? How does the learner
[23:24] &gt;&gt; Is that like cider? How does the learner
[23:24] &gt;&gt; Is that like cider? How does the learner enter answers? Free text,
[23:26] enter answers? Free text,
[23:26] enter answers? Free text, multiplechoice, mix by tier. Let's do
[23:29] multiplechoice, mix by tier. Let's do
[23:29] multiplechoice, mix by tier. Let's do three. Mix by tier. Review your answers.
[23:31] three. Mix by tier. Review your answers.
[23:31] three. Mix by tier. Review your answers. Submit the answers. So if we if you want
[23:34] Submit the answers. So if we if you want
[23:34] Submit the answers. So if we if you want to look at this is the completed spec.
[23:36] to look at this is the completed spec.
[23:36] to look at this is the completed spec. Now notice how at the very top feature
[23:39] Now notice how at the very top feature
[23:39] Now notice how at the very top feature specification no longer has square
[23:40] specification no longer has square
[23:40] specification no longer has square brackets. Okay.
[23:41] brackets. Okay.
[23:41] brackets. Okay. &gt;&gt; Subnetting learning game. So look at
[23:43] &gt;&gt; Subnetting learning game. So look at
[23:44] &gt;&gt; Subnetting learning game. So look at it's just like software developers do.
[23:45] it's just like software developers do.
[23:45] it's just like software developers do. Andy user stories, functional
[23:48] Andy user stories, functional
[23:48] Andy user stories, functional requirements, why it's a priority. Right
[23:51] requirements, why it's a priority. Right
[23:51] requirements, why it's a priority. Right now this the LLM is going to use as an
[23:53] now this the LLM is going to use as an
[23:53] now this the LLM is going to use as an input later when we say implement to
[23:56] input later when we say implement to
[23:56] input later when we say implement to generate the code. Look at this
[23:58] generate the code. Look at this
[23:58] generate the code. Look at this independent testing acceptance scenarios
[24:01] independent testing acceptance scenarios
[24:01] independent testing acceptance scenarios blah blah blah. Right.
[24:02] blah blah blah. Right.
[24:02] blah blah blah. Right. &gt;&gt; I don't understand testing. Do do we do
[24:05] &gt;&gt; I don't understand testing. Do do we do
[24:05] &gt;&gt; I don't understand testing. Do do we do we test it or does it
[24:06] we test it or does it
[24:06] we test it or does it &gt;&gt; it will test its own code. Yeah. So we
[24:10] &gt;&gt; it will test its own code. Yeah. So we
[24:10] &gt;&gt; it will test its own code. Yeah. So we don't have to test any of it. It's going
[24:11] don't have to test any of it. It's going
[24:11] don't have to test any of it. It's going to test itself.
[24:12] to test itself.
[24:12] to test itself. &gt;&gt; Where does the testing happen?
[24:13] &gt;&gt; Where does the testing happen?
[24:13] &gt;&gt; Where does the testing happen? &gt;&gt; So check it out. So let's roll this back
[24:15] &gt;&gt; So check it out. So let's roll this back
[24:15] &gt;&gt; So check it out. So let's roll this back up again the divider. And here's what
[24:17] up again the divider. And here's what
[24:17] up again the divider. And here's what Cloud Code had to say. So, here's your
[24:18] Cloud Code had to say. So, here's your
[24:18] Cloud Code had to say. So, here's your spec file in this branch. And we even
[24:20] spec file in this branch. And we even
[24:20] spec file in this branch. And we even gave you a checklist with requirements.
[24:22] gave you a checklist with requirements.
[24:22] gave you a checklist with requirements. See the checklist folder here?
[24:24] See the checklist folder here?
[24:24] See the checklist folder here? &gt;&gt; There's a checklist in here of
[24:26] &gt;&gt; There's a checklist in here of
[24:26] &gt;&gt; There's a checklist in here of requirements. Now,
[24:27] requirements. Now,
[24:28] requirements. Now, &gt;&gt; what I did, I adapted your authored spec
[24:30] &gt;&gt; what I did, I adapted your authored spec
[24:30] &gt;&gt; what I did, I adapted your authored spec into the spec kit template format.
[24:33] into the spec kit template format.
[24:33] into the spec kit template format. Restructured a flat story into three
[24:35] Restructured a flat story into three
[24:35] Restructured a flat story into three prioritized independently testable user
[24:37] prioritized independently testable user
[24:37] prioritized independently testable user stories. And here's what we get. The
[24:39] stories. And here's what we get. The
[24:39] stories. And here's what we get. The question, topic, answer, spec kit to
[24:42] question, topic, answer, spec kit to
[24:42] question, topic, answer, spec kit to commit the spec. You can just tab and
[24:45] commit the spec. You can just tab and
[24:45] commit the spec. You can just tab and let's commit it. Let's go ahead and do
[24:47] let's commit it. Let's go ahead and do
[24:47] let's commit it. Let's go ahead and do the clarify step just in case there's
[24:50] the clarify step just in case there's
[24:50] the clarify step just in case there's more clarifications needed. Yeah. And
[24:53] more clarifications needed. Yeah. And
[24:53] more clarifications needed. Yeah. And say yes and don't ask.
[24:54] say yes and don't ask.
[24:54] say yes and don't ask. &gt;&gt; I can't imagine you wouldn't clarify.
[24:56] &gt;&gt; I can't imagine you wouldn't clarify.
[24:56] &gt;&gt; I can't imagine you wouldn't clarify. That seems like a pretty good thing,
[24:57] That seems like a pretty good thing,
[24:57] That seems like a pretty good thing, right?
[24:57] right?
[24:57] right? &gt;&gt; Yeah. So, I like to do that right now.
[24:59] &gt;&gt; Yeah. So, I like to do that right now.
[24:59] &gt;&gt; Yeah. So, I like to do that right now. So, if you do slashspec kit clarify, and
[25:03] So, if you do slashspec kit clarify, and
[25:03] So, if you do slashspec kit clarify, and there's no prompt here. You just say
[25:05] there's no prompt here. You just say
[25:05] there's no prompt here. You just say clarify. Enter. And it's the LLM now is
[25:08] clarify. Enter. And it's the LLM now is
[25:08] clarify. Enter. And it's the LLM now is going to evaluate our constitution and
[25:10] going to evaluate our constitution and
[25:10] going to evaluate our constitution and our spec to sus out anything that it's
[25:13] our spec to sus out anything that it's
[25:13] our spec to sus out anything that it's unclear about. if anything it needs
[25:15] unclear about. if anything it needs
[25:15] unclear about. if anything it needs clarity on. This is kind of like your
[25:17] clarity on. This is kind of like your
[25:17] clarity on. This is kind of like your junior, right? So, I've given you the
[25:19] junior, right? So, I've given you the
[25:19] junior, right? So, I've given you the spec. Let me, you know, review it and
[25:21] spec. Let me, you know, review it and
[25:21] spec. Let me, you know, review it and come back to me with questions before
[25:23] come back to me with questions before
[25:23] come back to me with questions before you do anything else.
[25:24] you do anything else.
[25:24] you do anything else. &gt;&gt; This is crazy in the best way possible.
[25:27] &gt;&gt; This is crazy in the best way possible.
[25:27] &gt;&gt; This is crazy in the best way possible. Like, this is like just I can't believe
[25:29] Like, this is like just I can't believe
[25:29] Like, this is like just I can't believe what I'm seeing happening in front of
[25:32] what I'm seeing happening in front of
[25:32] what I'm seeing happening in front of me. And I'm a broken record, but as
[25:34] me. And I'm a broken record, but as
[25:34] me. And I'm a broken record, but as someone who would never have had access
[25:37] someone who would never have had access
[25:37] someone who would never have had access to software development, I
[25:39] to software development, I
[25:39] to software development, I &gt;&gt; I know
[25:39] &gt;&gt; I know
[25:39] &gt;&gt; I know &gt;&gt; I would never have got to the point
[25:42] &gt;&gt; I would never have got to the point
[25:42] &gt;&gt; I would never have got to the point where I could do this.
[25:43] where I could do this.
[25:43] where I could do this. &gt;&gt; I know. And I want to give a special
[25:44] &gt;&gt; I know. And I want to give a special
[25:44] &gt;&gt; I know. And I want to give a special shout out if so if you're looking for
[25:46] shout out if so if you're looking for
[25:46] shout out if so if you're looking for more materials about spec driven there's
[25:48] more materials about spec driven there's
[25:48] more materials about spec driven there's a few people in the community doing a
[25:49] a few people in the community doing a
[25:49] a few people in the community doing a lot around this. Um one guy from Cisco
[25:51] lot around this. Um one guy from Cisco
[25:51] lot around this. Um one guy from Cisco Jason Belulk I don't know if you've ever
[25:53] Jason Belulk I don't know if you've ever
[25:53] Jason Belulk I don't know if you've ever met Jason.
[25:53] met Jason.
[25:54] met Jason. &gt;&gt; Yeah
[25:54] &gt;&gt; Yeah
[25:54] &gt;&gt; Yeah &gt;&gt; he actually had a session at Cisco Live
[25:56] &gt;&gt; he actually had a session at Cisco Live
[25:56] &gt;&gt; he actually had a session at Cisco Live in the catalog about this exact topic.
[25:59] in the catalog about this exact topic.
[25:59] in the catalog about this exact topic. &gt;&gt; So it's starting to to you know make
[26:01] &gt;&gt; So it's starting to to you know make
[26:01] &gt;&gt; So it's starting to to you know make noise out there. Okay. So what defines
[26:03] noise out there. Okay. So what defines
[26:03] noise out there. Okay. So what defines mastery to unlock the next tier? So how
[26:06] mastery to unlock the next tier? So how
[26:06] mastery to unlock the next tier? So how do we get to the next tier in the game?
[26:07] do we get to the next tier in the game?
[26:07] do we get to the next tier in the game? Streak of correct answers, a cumulative
[26:10] Streak of correct answers, a cumulative
[26:10] Streak of correct answers, a cumulative correct total. a past tier quiz
[26:12] correct total. a past tier quiz
[26:12] correct total. a past tier quiz checkpoint.
[26:13] checkpoint.
[26:13] checkpoint. &gt;&gt; I would say streak, right? Wouldn't that
[26:14] &gt;&gt; I would say streak, right? Wouldn't that
[26:14] &gt;&gt; I would say streak, right? Wouldn't that make sense?
[26:14] make sense?
[26:14] make sense? &gt;&gt; I think a streak would make the most
[26:16] &gt;&gt; I think a streak would make the most
[26:16] &gt;&gt; I think a streak would make the most sense.
[26:16] sense.
[26:16] sense. &gt;&gt; But that's a good question.
[26:17] &gt;&gt; But that's a good question.
[26:17] &gt;&gt; But that's a good question. &gt;&gt; So, it asks us five. It's going to ask
[26:19] &gt;&gt; So, it asks us five. It's going to ask
[26:19] &gt;&gt; So, it asks us five. It's going to ask five questions here.
[26:21] five questions here.
[26:21] five questions here. &gt;&gt; Okay. So, what defines mastery? Streak
[26:23] &gt;&gt; Okay. So, what defines mastery? Streak
[26:23] &gt;&gt; Okay. So, what defines mastery? Streak of correct answers. And now it's going
[26:25] of correct answers. And now it's going
[26:25] of correct answers. And now it's going to ask us question two of the uh Okay.
[26:28] to ask us question two of the uh Okay.
[26:28] to ask us question two of the uh Okay. So, let me integrate that into the spec
[26:30] So, let me integrate that into the spec
[26:30] So, let me integrate that into the spec now. And you see how it's green.
[26:32] now. And you see how it's green.
[26:32] now. And you see how it's green. &gt;&gt; Yeah.
[26:32] &gt;&gt; Yeah.
[26:32] &gt;&gt; Yeah. &gt;&gt; It's added that to the specification
[26:35] &gt;&gt; It's added that to the specification
[26:35] &gt;&gt; It's added that to the specification &gt;&gt; and then the red removes. Is that
[26:37] &gt;&gt; and then the red removes. Is that
[26:37] &gt;&gt; and then the red removes. Is that &gt;&gt; Yeah. Okay. So then when we go to build
[26:38] &gt;&gt; Yeah. Okay. So then when we go to build
[26:38] &gt;&gt; Yeah. Okay. So then when we go to build the game now the game knows, okay, to
[26:40] the game now the game knows, okay, to
[26:40] the game now the game knows, okay, to move to the next level, they've got to
[26:42] move to the next level, they've got to
[26:42] move to the next level, they've got to get three answers correct or whatever in
[26:43] get three answers correct or whatever in
[26:43] get three answers correct or whatever in a row.
[26:44] a row.
[26:44] a row. &gt;&gt; So what's question two? How does the
[26:47] &gt;&gt; So what's question two? How does the
[26:47] &gt;&gt; So what's question two? How does the game teach a concept before testing it?
[26:49] game teach a concept before testing it?
[26:49] game teach a concept before testing it? A brief lesson, explanations only, work
[26:52] A brief lesson, explanations only, work
[26:52] A brief lesson, explanations only, work example, and then practice.
[26:54] example, and then practice.
[26:54] example, and then practice. &gt;&gt; I would say just the recommended, right?
[26:56] &gt;&gt; I would say just the recommended, right?
[26:56] &gt;&gt; I would say just the recommended, right? Number one,
[26:56] Number one,
[26:56] Number one, &gt;&gt; recommended. We can go with that. And
[26:58] &gt;&gt; recommended. We can go with that. And
[26:58] &gt;&gt; recommended. We can go with that. And honestly, anyone at home, rewind to the
[27:00] honestly, anyone at home, rewind to the
[27:00] honestly, anyone at home, rewind to the start and install the same things that
[27:02] start and install the same things that
[27:02] start and install the same things that we've done and build your own video
[27:04] we've done and build your own video
[27:04] we've done and build your own video game. Build your own network video game.
[27:05] game. Build your own network video game.
[27:06] game. Build your own network video game. Don't do subnetting. Do uh routing. Do
[27:10] Don't do subnetting. Do uh routing. Do
[27:10] Don't do subnetting. Do uh routing. Do BGP as a video game. OPF as a video
[27:12] BGP as a video game. OPF as a video
[27:12] BGP as a video game. OPF as a video game. Open source it. Make it a better
[27:14] game. Open source it. Make it a better
[27:14] game. Open source it. Make it a better world for everyone else. Leave something
[27:16] world for everyone else. Leave something
[27:16] world for everyone else. Leave something behind for the next generation to learn
[27:18] behind for the next generation to learn
[27:18] behind for the next generation to learn from. I would have loved to learn
[27:20] from. I would have loved to learn
[27:20] from. I would have loved to learn subnetting from a video game.
[27:21] subnetting from a video game.
[27:21] subnetting from a video game. &gt;&gt; Yeah,
[27:22] &gt;&gt; Yeah,
[27:22] &gt;&gt; Yeah, &gt;&gt; I was doing it from flashcards and
[27:24] &gt;&gt; I was doing it from flashcards and
[27:24] &gt;&gt; I was doing it from flashcards and handwriting, cedar calculations in
[27:27] handwriting, cedar calculations in
[27:27] handwriting, cedar calculations in workbooks. Okay. So, is there a time
[27:29] workbooks. Okay. So, is there a time
[27:29] workbooks. Okay. So, is there a time pressure or is it speed only?
[27:32] pressure or is it speed only?
[27:32] pressure or is it speed only? &gt;&gt; Measure. I would say measure passively.
[27:34] &gt;&gt; Measure. I would say measure passively.
[27:34] &gt;&gt; Measure. I would say measure passively. Let's not make this a ch a time
[27:35] Let's not make this a ch a time
[27:36] Let's not make this a ch a time challenge.
[27:36] challenge.
[27:36] challenge. &gt;&gt; Yeah. I can remember writing out the
[27:38] &gt;&gt; Yeah. I can remember writing out the
[27:38] &gt;&gt; Yeah. I can remember writing out the binary and it was not
[27:40] binary and it was not
[27:40] binary and it was not &gt;&gt; right. And it was like remember they
[27:42] &gt;&gt; right. And it was like remember they
[27:42] &gt;&gt; right. And it was like remember they gave you a page of a page of different
[27:43] gave you a page of a page of different
[27:44] gave you a page of a page of different IP addresses and you had to do each one
[27:45] IP addresses and you had to do each one
[27:45] IP addresses and you had to do each one of them
[27:46] of them
[27:46] of them &gt;&gt; first usable, last usable.
[27:48] &gt;&gt; first usable, last usable.
[27:48] &gt;&gt; first usable, last usable. &gt;&gt; Yeah. Last top
[27:51] &gt;&gt; Yeah. Last top
[27:51] &gt;&gt; Yeah. Last top and all that stuff. Yeah.
[27:53] and all that stuff. Yeah.
[27:53] and all that stuff. Yeah. &gt;&gt; I almost quit over subnetting.
[27:55] &gt;&gt; I almost quit over subnetting.
[27:55] &gt;&gt; I almost quit over subnetting. &gt;&gt; So when I went to my I went to an IP
[27:58] &gt;&gt; So when I went to my I went to an IP
[27:58] &gt;&gt; So when I went to my I went to an IP routing boot camp after I'd passed
[27:59] routing boot camp after I'd passed
[28:00] routing boot camp after I'd passed switch. So my my generation of CCNP was
[28:02] switch. So my my generation of CCNP was
[28:02] switch. So my my generation of CCNP was route, switch, t-shirt, and I passed
[28:05] route, switch, t-shirt, and I passed
[28:05] route, switch, t-shirt, and I passed switch. And the routing instructor,
[28:06] switch. And the routing instructor,
[28:06] switch. And the routing instructor, Andy, was like, "What are you doing
[28:08] Andy, was like, "What are you doing
[28:08] Andy, was like, "What are you doing here?" I go, "I don't understand." He
[28:09] here?" I go, "I don't understand." He
[28:09] here?" I go, "I don't understand." He goes, "Well, you've passed switch.
[28:10] goes, "Well, you've passed switch.
[28:10] goes, "Well, you've passed switch. That's the hard one."
[28:12] That's the hard one."
[28:12] That's the hard one." &gt;&gt; If you can do the switching and the
[28:14] &gt;&gt; If you can do the switching and the
[28:14] &gt;&gt; If you can do the switching and the binary and the subnetting and the
[28:16] binary and the subnetting and the
[28:16] binary and the subnetting and the spanning tree, routing is just next,
[28:19] spanning tree, routing is just next,
[28:19] spanning tree, routing is just next, dude, you'll be just fine. And he was
[28:20] dude, you'll be just fine. And he was
[28:20] dude, you'll be just fine. And he was kind of right that the routing book was
[28:22] kind of right that the routing book was
[28:22] kind of right that the routing book was twice as big cuz you had a whole section
[28:24] twice as big cuz you had a whole section
[28:24] twice as big cuz you had a whole section on EIGRP, a whole section on OPF.
[28:27] on EIGRP, a whole section on OPF.
[28:27] on EIGRP, a whole section on OPF. Anyway, okay. So, what's the next one
[28:28] Anyway, okay. So, what's the next one
[28:28] Anyway, okay. So, what's the next one here? When does it switch from multiple
[28:29] here? When does it switch from multiple
[28:29] here? When does it switch from multiple choice to free text? Let's just go per
[28:32] choice to free text? Let's just go per
[28:32] choice to free text? Let's just go per concept. We can do with the recommended
[28:33] concept. We can do with the recommended
[28:33] concept. We can do with the recommended setting. And then we'll have one last
[28:35] setting. And then we'll have one last
[28:35] setting. And then we'll have one last question to clarify and we'll move on to
[28:37] question to clarify and we'll move on to
[28:37] question to clarify and we'll move on to the next step, which is planning.
[28:39] the next step, which is planning.
[28:39] the next step, which is planning. &gt;&gt; I had such a hard time with those old MP
[28:41] &gt;&gt; I had such a hard time with those old MP
[28:41] &gt;&gt; I had such a hard time with those old MP exams. I found route harder than I
[28:44] exams. I found route harder than I
[28:44] exams. I found route harder than I thought it would because route's
[28:45] thought it would because route's
[28:45] thought it would because route's intuitive for some reason to me. And I
[28:47] intuitive for some reason to me. And I
[28:47] intuitive for some reason to me. And I failed that one a couple times, too. I
[28:49] failed that one a couple times, too. I
[28:49] failed that one a couple times, too. I had a I learned a ton studying for those
[28:51] had a I learned a ton studying for those
[28:51] had a I learned a ton studying for those three exams, but man, I it was painful.
[28:54] three exams, but man, I it was painful.
[28:54] three exams, but man, I it was painful. &gt;&gt; It was tough. I got hung up on CCNA data
[28:56] &gt;&gt; It was tough. I got hung up on CCNA data
[28:56] &gt;&gt; It was tough. I got hung up on CCNA data center of all things. I failed the
[28:59] center of all things. I failed the
[28:59] center of all things. I failed the second of two like three times and I was
[29:02] second of two like three times and I was
[29:02] second of two like three times and I was like getting really desperate like
[29:04] like getting really desperate like
[29:04] like getting really desperate like telling to my wife like I don't think
[29:06] telling to my wife like I don't think
[29:06] telling to my wife like I don't think I'm ever going to pass CCNA data center.
[29:08] I'm ever going to pass CCNA data center.
[29:08] I'm ever going to pass CCNA data center. I've been studying this thing and
[29:09] I've been studying this thing and
[29:09] I've been studying this thing and writing tests for
[29:11] writing tests for
[29:11] writing tests for &gt;&gt; like a year to get that right. Okay, so
[29:13] &gt;&gt; like a year to get that right. Okay, so
[29:13] &gt;&gt; like a year to get that right. Okay, so we're all set. It's clarified
[29:15] we're all set. It's clarified
[29:15] we're all set. It's clarified everything. Hit tab and commit the the
[29:18] everything. Hit tab and commit the the
[29:18] everything. Hit tab and commit the the clarifications. Okay, so now the next
[29:20] clarifications. Okay, so now the next
[29:20] clarifications. Okay, so now the next step is plan. And let's go back to uh
[29:24] step is plan. And let's go back to uh
[29:24] step is plan. And let's go back to uh our get hub folder
[29:26] our get hub folder
[29:26] our get hub folder &gt;&gt; over in the
[29:27] &gt;&gt; over in the
[29:27] &gt;&gt; over in the &gt;&gt; um yes and scroll down and we're going
[29:29] &gt;&gt; um yes and scroll down and we're going
[29:29] &gt;&gt; um yes and scroll down and we're going to do the same thing except for plan.
[29:32] to do the same thing except for plan.
[29:32] to do the same thing except for plan. Now listen, plan provides your text
[29:35] Now listen, plan provides your text
[29:35] Now listen, plan provides your text stack and the architectural choices. So
[29:37] stack and the architectural choices. So
[29:37] stack and the architectural choices. So hit copy there and we're going to add a
[29:39] hit copy there and we're going to add a
[29:39] hit copy there and we're going to add a little bit to this. So let's go to cloud
[29:40] little bit to this. So let's go to cloud
[29:40] little bit to this. So let's go to cloud desktop. Oh, and don't forget to hit yes
[29:43] desktop. Oh, and don't forget to hit yes
[29:43] desktop. Oh, and don't forget to hit yes here on this this thing. Cloud desktop
[29:45] here on this this thing. Cloud desktop
[29:45] here on this this thing. Cloud desktop again. I would say thanks for the spec.
[29:47] again. I would say thanks for the spec.
[29:47] again. I would say thanks for the spec. &gt;&gt; Thanks.
[29:48] &gt;&gt; Thanks.
[29:48] &gt;&gt; Thanks. &gt;&gt; The next step is planning. Here is an
[29:51] &gt;&gt; The next step is planning. Here is an
[29:51] &gt;&gt; The next step is planning. Here is an example of a plan. And don't hit don't
[29:53] example of a plan. And don't hit don't
[29:53] example of a plan. And don't hit don't send it yet. And then paste in the plan.
[29:56] send it yet. And then paste in the plan.
[29:56] send it yet. And then paste in the plan. Press enter now. But this is might might
[29:58] Press enter now. But this is might might
[29:58] Press enter now. But this is might might be what we get. Use vanilla HTML CSS and
[30:02] be what we get. Use vanilla HTML CSS and
[30:02] be what we get. Use vanilla HTML CSS and JavaScript as much as possible. Images
[30:04] JavaScript as much as possible. Images
[30:04] JavaScript as much as possible. Images are not uploaded anywhere. Metadata
[30:06] are not uploaded anywhere. Metadata
[30:06] are not uploaded anywhere. Metadata stored in SQL. So this is where we
[30:07] stored in SQL. So this is where we
[30:07] stored in SQL. So this is where we actually get into like I'd like this to
[30:09] actually get into like I'd like this to
[30:09] actually get into like I'd like this to be a JavaScriptbased game that's in the
[30:11] be a JavaScriptbased game that's in the
[30:11] be a JavaScriptbased game that's in the web browser. I'd like it to be a Python
[30:12] web browser. I'd like it to be a Python
[30:12] web browser. I'd like it to be a Python game that's at the CLI. We get to choose
[30:15] game that's at the CLI. We get to choose
[30:15] game that's at the CLI. We get to choose our our framework and our architecture
[30:17] our our framework and our architecture
[30:17] our our framework and our architecture here. And for the interest of time,
[30:19] here. And for the interest of time,
[30:19] here. And for the interest of time, let's just go here into VS Code and do
[30:23] let's just go here into VS Code and do
[30:23] let's just go here into VS Code and do slashspec kit. And we're looking for
[30:25] slashspec kit. And we're looking for
[30:25] slashspec kit. And we're looking for plan this time. And then just space and
[30:28] plan this time. And then just space and
[30:28] plan this time. And then just space and say this should be a um this should be a
[30:31] say this should be a um this should be a
[30:31] say this should be a um this should be a basic HTML
[30:34] basic HTML
[30:34] basic HTML CSS JavaScript
[30:37] CSS JavaScript
[30:37] CSS JavaScript game in the browser.
[30:39] game in the browser.
[30:39] game in the browser. &gt;&gt; I hope I didn't break it.
[30:41] &gt;&gt; I hope I didn't break it.
[30:41] &gt;&gt; I hope I didn't break it. &gt;&gt; No, you didn't break it. We're going to
[30:42] &gt;&gt; No, you didn't break it. We're going to
[30:42] &gt;&gt; No, you didn't break it. We're going to be okay. So you see here now we have a
[30:44] be okay. So you see here now we have a
[30:44] be okay. So you see here now we have a new plan file. Right now it's just an
[30:47] new plan file. Right now it's just an
[30:47] new plan file. Right now it's just an empty template, but you can click on
[30:49] empty template, but you can click on
[30:49] empty template, but you can click on that. And now we're sort of starting to
[30:51] that. And now we're sort of starting to
[30:51] that. And now we're sort of starting to get like this, Andy. We're we're working
[30:53] get like this, Andy. We're we're working
[30:53] get like this, Andy. We're we're working down the funnel
[30:54] down the funnel
[30:54] down the funnel &gt;&gt; to implement where we get code, but
[30:56] &gt;&gt; to implement where we get code, but
[30:56] &gt;&gt; to implement where we get code, but right now it's going to break it into
[30:58] right now it's going to break it into
[30:58] right now it's going to break it into the technical specs on how to make CSS,
[31:01] the technical specs on how to make CSS,
[31:01] the technical specs on how to make CSS, JavaScript in a web browser.
[31:03] JavaScript in a web browser.
[31:03] JavaScript in a web browser. &gt;&gt; So we created the constitution which
[31:05] &gt;&gt; So we created the constitution which
[31:05] &gt;&gt; So we created the constitution which gave us guard rails and then we created
[31:07] gave us guard rails and then we created
[31:08] gave us guard rails and then we created the spec.
[31:09] the spec.
[31:09] the spec. &gt;&gt; Yep.
[31:09] &gt;&gt; Yep.
[31:09] &gt;&gt; Yep. &gt;&gt; Which is like where the stories and all
[31:11] &gt;&gt; Which is like where the stories and all
[31:11] &gt;&gt; Which is like where the stories and all that stuff came from, right?
[31:12] that stuff came from, right?
[31:12] that stuff came from, right? &gt;&gt; Yep. And then we clarified to make sure
[31:14] &gt;&gt; Yep. And then we clarified to make sure
[31:14] &gt;&gt; Yep. And then we clarified to make sure it had no question
[31:15] it had no question
[31:16] it had no question &gt;&gt; and it asked some good questions which I
[31:17] &gt;&gt; and it asked some good questions which I
[31:17] &gt;&gt; and it asked some good questions which I wouldn't have thought of.
[31:18] wouldn't have thought of.
[31:18] wouldn't have thought of. &gt;&gt; Yep.
[31:18] &gt;&gt; Yep.
[31:18] &gt;&gt; Yep. &gt;&gt; And now
[31:19] &gt;&gt; And now
[31:19] &gt;&gt; And now &gt;&gt; and now we're breaking it down into
[31:20] &gt;&gt; and now we're breaking it down into
[31:20] &gt;&gt; and now we're breaking it down into plans. This, by the way, any plan is the
[31:23] plans. This, by the way, any plan is the
[31:23] plans. This, by the way, any plan is the last step that requires a prompt.
[31:27] last step that requires a prompt.
[31:27] last step that requires a prompt. &gt;&gt; So the next two steps, you see how they
[31:29] &gt;&gt; So the next two steps, you see how they
[31:29] &gt;&gt; So the next two steps, you see how they just say tasks and implement.
[31:31] just say tasks and implement.
[31:31] just say tasks and implement. &gt;&gt; Yeah,
[31:31] &gt;&gt; Yeah,
[31:31] &gt;&gt; Yeah, &gt;&gt; you don't need to type any prompts
[31:33] &gt;&gt; you don't need to type any prompts
[31:33] &gt;&gt; you don't need to type any prompts there. So the first three, constitution
[31:35] there. So the first three, constitution
[31:35] there. So the first three, constitution spec plan, you feed it a prompt. And
[31:38] spec plan, you feed it a prompt. And
[31:38] spec plan, you feed it a prompt. And look it, check it out. The user resolved
[31:41] look it, check it out. The user resolved
[31:41] look it, check it out. The user resolved the answer, the text stack, basic HTML,
[31:44] the answer, the text stack, basic HTML,
[31:44] the answer, the text stack, basic HTML, CSS, JavaScript in a browser. I've read
[31:46] CSS, JavaScript in a browser. I've read
[31:46] CSS, JavaScript in a browser. I've read the spec and constitution and context.
[31:48] the spec and constitution and context.
[31:48] the spec and constitution and context. So now, really soon, all of these
[31:52] So now, really soon, all of these
[31:52] So now, really soon, all of these placeholders in the template will be
[31:54] placeholders in the template will be
[31:54] placeholders in the template will be filled in with the plans the the Claude
[31:56] filled in with the plans the the Claude
[31:56] filled in with the plans the the Claude code has come up with. So we see some
[31:58] code has come up with. So we see some
[31:58] code has come up with. So we see some red, some green. It's adding some
[31:59] red, some green. It's adding some
[31:59] red, some green. It's adding some changes here. No constitution
[32:01] changes here. No constitution
[32:01] changes here. No constitution violations. Good. And I hope this
[32:03] violations. Good. And I hope this
[32:03] violations. Good. And I hope this doesn't take too much longer. We're okay
[32:04] doesn't take too much longer. We're okay
[32:04] doesn't take too much longer. We're okay for time.
[32:05] for time.
[32:05] for time. &gt;&gt; Eric Cho has entered the chat.
[32:07] &gt;&gt; Eric Cho has entered the chat.
[32:07] &gt;&gt; Eric Cho has entered the chat. &gt;&gt; Eric Cho is here. Eric, come on over. Do
[32:09] &gt;&gt; Eric Cho is here. Eric, come on over. Do
[32:09] &gt;&gt; Eric Cho is here. Eric, come on over. Do you guys remember Mr. Rogers where the
[32:10] you guys remember Mr. Rogers where the
[32:10] you guys remember Mr. Rogers where the neighbors would come in? Hi, Eric. How
[32:12] neighbors would come in? Hi, Eric. How
[32:12] neighbors would come in? Hi, Eric. How you doing, buddy?
[32:12] you doing, buddy?
[32:12] you doing, buddy? &gt;&gt; I figure I need to step in otherwise
[32:14] &gt;&gt; I figure I need to step in otherwise
[32:14] &gt;&gt; I figure I need to step in otherwise John would just keep on talking.
[32:16] John would just keep on talking.
[32:16] John would just keep on talking. [laughter]
[32:17] [laughter]
[32:18] [laughter] &gt;&gt; So nice to see you.
[32:18] &gt;&gt; So nice to see you.
[32:18] &gt;&gt; So nice to see you. &gt;&gt; What's up, man? It's been a day. See?
[32:21] &gt;&gt; What's up, man? It's been a day. See?
[32:21] &gt;&gt; What's up, man? It's been a day. See? Yeah.
[32:21] Yeah.
[32:21] Yeah. &gt;&gt; No worries. Save your time.
[32:23] &gt;&gt; No worries. Save your time.
[32:24] &gt;&gt; No worries. Save your time. &gt;&gt; Okay, so implementation plan, subnetting
[32:26] &gt;&gt; Okay, so implementation plan, subnetting
[32:26] &gt;&gt; Okay, so implementation plan, subnetting learning game v1. And this is now all
[32:28] learning game v1. And this is now all
[32:28] learning game v1. And this is now all filled in the plan.
[32:30] filled in the plan.
[32:30] filled in the plan. &gt;&gt; All right. Now, this is going to break
[32:31] &gt;&gt; All right. Now, this is going to break
[32:31] &gt;&gt; All right. Now, this is going to break it down. Phase one, data model,
[32:33] it down. Phase one, data model,
[32:33] it down. Phase one, data model, contracts, quick start. So those three,
[32:36] contracts, quick start. So those three,
[32:36] contracts, quick start. So those three, see how it says phase one. So check it
[32:38] see how it says phase one. So check it
[32:38] see how it says phase one. So check it out. It's going to generate the data
[32:40] out. It's going to generate the data
[32:40] out. It's going to generate the data model and a few other artifacts that
[32:44] model and a few other artifacts that
[32:44] model and a few other artifacts that implement is going to use to build this
[32:46] implement is going to use to build this
[32:46] implement is going to use to build this video game. So we have a data model. Now
[32:48] video game. So we have a data model. Now
[32:48] video game. So we have a data model. Now you can actually click on the data
[32:50] you can actually click on the data
[32:50] you can actually click on the data model. I'm not sure if it's finished
[32:51] model. I'm not sure if it's finished
[32:51] model. I'm not sure if it's finished building it, but this is the data model
[32:53] building it, but this is the data model
[32:53] building it, but this is the data model for this subnet game. So you remember
[32:55] for this subnet game. So you remember
[32:55] for this subnet game. So you remember earlier you were asking me how long this
[32:57] earlier you were asking me how long this
[32:57] earlier you were asking me how long this would take to build by hand. Just the
[32:59] would take to build by hand. Just the
[32:59] would take to build by hand. Just the data model might take a few days to
[33:01] data model might take a few days to
[33:01] data model might take a few days to model the data. So now we've got
[33:03] model the data. So now we've got
[33:03] model the data. So now we've got contracts, a new folder and if you
[33:05] contracts, a new folder and if you
[33:05] contracts, a new folder and if you expand that we have an engine MD which
[33:08] expand that we have an engine MD which
[33:08] expand that we have an engine MD which is the subnet engine and this MD file
[33:12] is the subnet engine and this MD file
[33:12] is the subnet engine and this MD file explains persistence. See it's building
[33:14] explains persistence. See it's building
[33:14] explains persistence. See it's building all the things that the LLM is going to
[33:16] all the things that the LLM is going to
[33:16] all the things that the LLM is going to use to actually spit out code at the end
[33:18] use to actually spit out code at the end
[33:18] use to actually spit out code at the end of all this
[33:19] of all this
[33:19] of all this &gt;&gt; question.
[33:20] &gt;&gt; question.
[33:20] &gt;&gt; question. &gt;&gt; Yeah.
[33:20] &gt;&gt; Yeah.
[33:20] &gt;&gt; Yeah. &gt;&gt; If I just asked like a dum dum, hey
[33:25] &gt;&gt; If I just asked like a dum dum, hey
[33:25] &gt;&gt; If I just asked like a dum dum, hey build me a game and teach me subnetting.
[33:27] build me a game and teach me subnetting.
[33:27] build me a game and teach me subnetting. &gt;&gt; Yeah.
[33:27] &gt;&gt; Yeah.
[33:27] &gt;&gt; Yeah. &gt;&gt; Does it do all this on the back end and
[33:30] &gt;&gt; Does it do all this on the back end and
[33:30] &gt;&gt; Does it do all this on the back end and I'm just not seeing it? Like would it
[33:32] I'm just not seeing it? Like would it
[33:32] I'm just not seeing it? Like would it have built all this out but I wouldn't
[33:33] have built all this out but I wouldn't
[33:33] have built all this out but I wouldn't be aware of it? Like how would call
[33:35] be aware of it? Like how would call
[33:35] be aware of it? Like how would call build a game if I didn't tell it to do
[33:37] build a game if I didn't tell it to do
[33:37] build a game if I didn't tell it to do all this? It
[33:38] all this? It
[33:38] all this? It &gt;&gt; it you would just so you wouldn't get
[33:39] &gt;&gt; it you would just so you wouldn't get
[33:39] &gt;&gt; it you would just so you wouldn't get any of these artifacts or any of this
[33:41] any of these artifacts or any of this
[33:41] any of these artifacts or any of this structure. It would like be vibe coding.
[33:43] structure. It would like be vibe coding.
[33:43] structure. It would like be vibe coding. It'd go, "Yeah, sure. Here you go.
[33:45] It'd go, "Yeah, sure. Here you go.
[33:45] It'd go, "Yeah, sure. Here you go. Here's a 100 lines of Python, Andy. This
[33:46] Here's a 100 lines of Python, Andy. This
[33:46] Here's a 100 lines of Python, Andy. This would be a subnetting game. Might work,
[33:49] would be a subnetting game. Might work,
[33:49] would be a subnetting game. Might work, might not. Might be cool, might not."
[33:51] might not. Might be cool, might not."
[33:51] might not. Might be cool, might not." &gt;&gt; This is much more constrained.
[33:53] &gt;&gt; This is much more constrained.
[33:53] &gt;&gt; This is much more constrained. &gt;&gt; It's it's more polished. It's more
[33:55] &gt;&gt; It's it's more polished. It's more
[33:55] &gt;&gt; It's it's more polished. It's more mature,
[33:56] mature,
[33:56] mature, &gt;&gt; driven by the requirements. It's almost
[33:58] &gt;&gt; driven by the requirements. It's almost
[33:58] &gt;&gt; driven by the requirements. It's almost like somebody [laughter]
[34:00] like somebody [laughter]
[34:00] like somebody [laughter] thought it would be smart.
[34:02] thought it would be smart.
[34:02] thought it would be smart. &gt;&gt; Have you ever been in that tough meeting
[34:03] &gt;&gt; Have you ever been in that tough meeting
[34:04] &gt;&gt; Have you ever been in that tough meeting where you've got business folks and
[34:05] where you've got business folks and
[34:05] where you've got business folks and network folks and and and the whole and
[34:07] network folks and and and the whole and
[34:07] network folks and and and the whole and you're just like, listen, do you have
[34:09] you're just like, listen, do you have
[34:09] you're just like, listen, do you have requirements? What are your
[34:11] requirements? What are your
[34:12] requirements? What are your requirements? I can't just build a
[34:13] requirements? I can't just build a
[34:13] requirements? I can't just build a network without knowing what the
[34:15] network without knowing what the
[34:15] network without knowing what the requirements are, right? So, this is a
[34:17] requirements are, right? So, this is a
[34:17] requirements are, right? So, this is a really cool way to do things. Okay, so
[34:19] really cool way to do things. Okay, so
[34:19] really cool way to do things. Okay, so let's do the commit. And it's sort of
[34:21] let's do the commit. And it's sort of
[34:21] let's do the commit. And it's sort of broken down. There's a bit of a a recap
[34:23] broken down. There's a bit of a a recap
[34:23] broken down. There's a bit of a a recap on what it did. So, I would just say
[34:25] on what it did. So, I would just say
[34:25] on what it did. So, I would just say yes. And then it tells us run spec kit
[34:29] yes. And then it tells us run spec kit
[34:29] yes. And then it tells us run spec kit tasks to generate the tasks from these
[34:32] tasks to generate the tasks from these
[34:32] tasks to generate the tasks from these artifacts and they're dependencyordered
[34:35] artifacts and they're dependencyordered
[34:35] artifacts and they're dependencyordered tasks. Let's just do yes here again.
[34:38] tasks. Let's just do yes here again.
[34:38] tasks. Let's just do yes here again. Okay. Next is to run the tasks to turn
[34:41] Okay. Next is to run the tasks to turn
[34:41] Okay. Next is to run the tasks to turn these artifacts into a dependencyordered
[34:44] these artifacts into a dependencyordered
[34:44] these artifacts into a dependencyordered tasks.md
[34:45] tasks.md
[34:45] tasks.md organized by user story which is phase
[34:48] organized by user story which is phase
[34:48] organized by user story which is phase 1, phase 2, phase three. So you can
[34:51] 1, phase 2, phase three. So you can
[34:51] 1, phase 2, phase three. So you can build and validate the MVP first. So
[34:53] build and validate the MVP first. So
[34:53] build and validate the MVP first. So just press enter. There's no prompt
[34:55] just press enter. There's no prompt
[34:55] just press enter. There's no prompt required for tasks. Good news everybody.
[34:58] required for tasks. Good news everybody.
[34:58] required for tasks. Good news everybody. We're on the second last step, the
[35:00] We're on the second last step, the
[35:00] We're on the second last step, the penultimate step before we get to
[35:03] penultimate step before we get to
[35:03] penultimate step before we get to implement. And then once we implement,
[35:06] implement. And then once we implement,
[35:06] implement. And then once we implement, we're going to get all kinds of code and
[35:08] we're going to get all kinds of code and
[35:08] we're going to get all kinds of code and a working minimum viable product.
[35:11] a working minimum viable product.
[35:11] a working minimum viable product. &gt;&gt; I have never used penultimate in a
[35:12] &gt;&gt; I have never used penultimate in a
[35:12] &gt;&gt; I have never used penultimate in a sentence. That was impressive. Does that
[35:14] sentence. That was impressive. Does that
[35:14] sentence. That was impressive. Does that mean the second to the last second?
[35:15] mean the second to the last second?
[35:15] mean the second to the last second? &gt;&gt; Second to the last. That's right. You
[35:17] &gt;&gt; Second to the last. That's right. You
[35:17] &gt;&gt; Second to the last. That's right. You said penultimate and I thought of the
[35:19] said penultimate and I thought of the
[35:19] said penultimate and I thought of the Madagascar penguins because at one point
[35:21] Madagascar penguins because at one point
[35:21] Madagascar penguins because at one point one of them says penultimate and it's
[35:23] one of them says penultimate and it's
[35:23] one of them says penultimate and it's hilarious and I don't even know why.
[35:24] hilarious and I don't even know why.
[35:24] hilarious and I don't even know why. &gt;&gt; That might be where I I picked it up
[35:26] &gt;&gt; That might be where I I picked it up
[35:26] &gt;&gt; That might be where I I picked it up from.
[35:26] from.
[35:26] from. &gt;&gt; Well, it's a very good use of it. I'm
[35:28] &gt;&gt; Well, it's a very good use of it. I'm
[35:28] &gt;&gt; Well, it's a very good use of it. I'm now going to use penultimate.
[35:29] now going to use penultimate.
[35:29] now going to use penultimate. &gt;&gt; So, I used to read comic books and there
[35:30] &gt;&gt; So, I used to read comic books and there
[35:30] &gt;&gt; So, I used to read comic books and there was always like,
[35:32] was always like,
[35:32] was always like, &gt;&gt; you know, book 11 of 12 is the
[35:34] &gt;&gt; you know, book 11 of 12 is the
[35:34] &gt;&gt; you know, book 11 of 12 is the penultimate chapter in Spider-Man's
[35:36] penultimate chapter in Spider-Man's
[35:36] penultimate chapter in Spider-Man's story or whatever. Right
[35:37] story or whatever. Right
[35:37] story or whatever. Right &gt;&gt; now, [clears throat] I know.
[35:38] &gt;&gt; now, [clears throat] I know.
[35:38] &gt;&gt; now, [clears throat] I know. &gt;&gt; The other thing I want everyone to be
[35:40] &gt;&gt; The other thing I want everyone to be
[35:40] &gt;&gt; The other thing I want everyone to be aware of is that this is uh, as you
[35:41] aware of is that this is uh, as you
[35:41] aware of is that this is uh, as you might imagine, a lot heavier token
[35:44] might imagine, a lot heavier token
[35:44] might imagine, a lot heavier token consumption. Andy,
[35:45] consumption. Andy,
[35:45] consumption. Andy, &gt;&gt; you were just reading my mind. And it
[35:46] &gt;&gt; you were just reading my mind. And it
[35:46] &gt;&gt; you were just reading my mind. And it was going to ask you about token economy
[35:48] was going to ask you about token economy
[35:48] was going to ask you about token economy and
[35:49] and
[35:49] and &gt;&gt; yeah the token
[35:50] &gt;&gt; yeah the token
[35:50] &gt;&gt; yeah the token &gt;&gt; account. You're probably not going to do
[35:51] &gt;&gt; account. You're probably not going to do
[35:51] &gt;&gt; account. You're probably not going to do this. I don't know if the $20 a month at
[35:54] this. I don't know if the $20 a month at
[35:54] this. I don't know if the $20 a month at this current rate would be able to
[35:56] this current rate would be able to
[35:56] this current rate would be able to handle this.
[35:57] handle this.
[35:57] handle this. &gt;&gt; I would just be careful with your
[35:59] &gt;&gt; I would just be careful with your
[35:59] &gt;&gt; I would just be careful with your tokens. Now you don't have to use Opus,
[36:02] tokens. Now you don't have to use Opus,
[36:02] tokens. Now you don't have to use Opus, right? You can connect Claude with Gemma
[36:05] right? You can connect Claude with Gemma
[36:05] right? You can connect Claude with Gemma 4 or an open source model and then the
[36:07] 4 or an open source model and then the
[36:07] 4 or an open source model and then the token usage is irrelevant. Okay. So
[36:10] token usage is irrelevant. Okay. So
[36:10] token usage is irrelevant. Okay. So let's click on the tasks file here just
[36:11] let's click on the tasks file here just
[36:11] let's click on the tasks file here just to take a quick peek on what that looks
[36:13] to take a quick peek on what that looks
[36:13] to take a quick peek on what that looks like. Yeah. See, so tests and it's going
[36:15] like. Yeah. See, so tests and it's going
[36:15] like. Yeah. See, so tests and it's going to do the test the organization the
[36:18] to do the test the organization the
[36:18] to do the test the organization the format the path conventions
[36:21] format the path conventions
[36:21] format the path conventions shared infrastructure
[36:23] shared infrastructure
[36:23] shared infrastructure like all this stuff that you don't need
[36:25] like all this stuff that you don't need
[36:25] like all this stuff that you don't need that we don't need to think about.
[36:27] that we don't need to think about.
[36:27] that we don't need to think about. &gt;&gt; All right, check it out. We're ready to
[36:29] &gt;&gt; All right, check it out. We're ready to
[36:29] &gt;&gt; All right, check it out. We're ready to go. Run implement to execute the tasks.
[36:32] go. Run implement to execute the tasks.
[36:32] go. Run implement to execute the tasks. Let's do the commit. So I just say yes
[36:34] Let's do the commit. So I just say yes
[36:34] Let's do the commit. So I just say yes and then we're going to run into
[36:35] and then we're going to run into
[36:35] and then we're going to run into implement.
[36:36] implement.
[36:36] implement. &gt;&gt; Do you do anything different in your
[36:37] &gt;&gt; Do you do anything different in your
[36:38] &gt;&gt; Do you do anything different in your workflow to um be thoughtful about token
[36:41] workflow to um be thoughtful about token
[36:41] workflow to um be thoughtful about token usage or do you just throw money at it?
[36:42] usage or do you just throw money at it?
[36:42] usage or do you just throw money at it? Because the re the reason I'm asking
[36:43] Because the re the reason I'm asking
[36:43] Because the re the reason I'm asking there's like a caveman thing where you
[36:45] there's like a caveman thing where you
[36:45] there's like a caveman thing where you can talk to it like a caveman and you
[36:46] can talk to it like a caveman and you
[36:46] can talk to it like a caveman and you get better. But I don't know if it
[36:47] get better. But I don't know if it
[36:47] get better. But I don't know if it works. I don't know if it's any good.
[36:49] works. I don't know if it's any good.
[36:49] works. I don't know if it's any good. &gt;&gt; I I do have to be conscious of my token
[36:51] &gt;&gt; I I do have to be conscious of my token
[36:51] &gt;&gt; I I do have to be conscious of my token spend.
[36:51] spend.
[36:51] spend. &gt;&gt; Yeah.
[36:52] &gt;&gt; Yeah.
[36:52] &gt;&gt; Yeah. &gt;&gt; You know, I had a $380 Gemini bill out
[36:54] &gt;&gt; You know, I had a $380 Gemini bill out
[36:54] &gt;&gt; You know, I had a $380 Gemini bill out of the blue and I didn't know where it
[36:55] of the blue and I didn't know where it
[36:56] of the blue and I didn't know where it went. I didn't know what I was doing
[36:57] went. I didn't know what I was doing
[36:57] went. I didn't know what I was doing that cost me that much money. It was
[36:58] that cost me that much money. It was
[36:58] that cost me that much money. It was hard to explain to my family like token
[37:00] hard to explain to my family like token
[37:00] hard to explain to my family like token usage.
[37:00] usage.
[37:00] usage. &gt;&gt; Suddenly I get a bill like oh I was
[37:02] &gt;&gt; Suddenly I get a bill like oh I was
[37:02] &gt;&gt; Suddenly I get a bill like oh I was using V3 to make videos and I didn't
[37:04] using V3 to make videos and I didn't
[37:04] using V3 to make videos and I didn't realize they were $8 a video and I made
[37:06] realize they were $8 a video and I made
[37:06] realize they were $8 a video and I made 30 videos and suddenly I've got a $300
[37:09] 30 videos and suddenly I've got a $300
[37:10] 30 videos and suddenly I've got a $300 bill. Right.
[37:10] bill. Right.
[37:10] bill. Right. &gt;&gt; Yeah. Can you limit it like you did with
[37:11] &gt;&gt; Yeah. Can you limit it like you did with
[37:11] &gt;&gt; Yeah. Can you limit it like you did with cloud like the spending limits?
[37:13] cloud like the spending limits?
[37:13] cloud like the spending limits? &gt;&gt; You can put caps and limits and warnings
[37:15] &gt;&gt; You can put caps and limits and warnings
[37:15] &gt;&gt; You can put caps and limits and warnings and Yeah. Yeah. I've been that shock
[37:17] and Yeah. Yeah. I've been that shock
[37:17] and Yeah. Yeah. I've been that shock value and I was I it was it was it was
[37:20] value and I was I it was it was it was
[37:20] value and I was I it was it was it was amazing like you've been a pioneer with
[37:23] amazing like you've been a pioneer with
[37:23] amazing like you've been a pioneer with a lot of
[37:23] a lot of
[37:24] a lot of &gt;&gt; So that was okay. So let's I wouldn't
[37:25] &gt;&gt; So that was okay. So let's I wouldn't
[37:25] &gt;&gt; So that was okay. So let's I wouldn't worry about analyze here.
[37:27] worry about analyze here.
[37:27] worry about analyze here. &gt;&gt; Oh, don't do that.
[37:28] &gt;&gt; Oh, don't do that.
[37:28] &gt;&gt; Oh, don't do that. &gt;&gt; Well, let's just skip analyze for now
[37:29] &gt;&gt; Well, let's just skip analyze for now
[37:29] &gt;&gt; Well, let's just skip analyze for now and go to implement. Let's just go right
[37:31] and go to implement. Let's just go right
[37:31] and go to implement. Let's just go right to implement.
[37:32] to implement.
[37:32] to implement. &gt;&gt; Analyze is kind of like another
[37:34] &gt;&gt; Analyze is kind of like another
[37:34] &gt;&gt; Analyze is kind of like another interactive phase where it will
[37:35] interactive phase where it will
[37:35] interactive phase where it will &gt;&gt; So is it run spec implement?
[37:38] &gt;&gt; So is it run spec implement?
[37:38] &gt;&gt; So is it run spec implement? &gt;&gt; Yeah, implement. So, let's minimize this
[37:40] &gt;&gt; Yeah, implement. So, let's minimize this
[37:40] &gt;&gt; Yeah, implement. So, let's minimize this spec folder here, Andy, and you're not
[37:42] spec folder here, Andy, and you're not
[37:42] spec folder here, Andy, and you're not going to believe this. What we're going
[37:44] going to believe this. What we're going
[37:44] going to believe this. What we're going to start to get is code. Now,
[37:47] to start to get is code. Now,
[37:47] to start to get is code. Now, &gt;&gt; code. Now, did you have to know anything
[37:49] &gt;&gt; code. Now, did you have to know anything
[37:49] &gt;&gt; code. Now, did you have to know anything other than what we wanted to build to
[37:51] other than what we wanted to build to
[37:51] other than what we wanted to build to get started here?
[37:52] get started here?
[37:52] get started here? &gt;&gt; Nope.
[37:52] &gt;&gt; Nope.
[37:52] &gt;&gt; Nope. &gt;&gt; Right. No. Now, check this out. And
[37:54] &gt;&gt; Right. No. Now, check this out. And
[37:54] &gt;&gt; Right. No. Now, check this out. And pretty soon, we're going to start to get
[37:56] pretty soon, we're going to start to get
[37:56] pretty soon, we're going to start to get folders like source folders and things
[37:59] folders like source folders and things
[37:59] folders like source folders and things like that. Yes. And don't ask again.
[38:01] like that. Yes. And don't ask again.
[38:01] like that. Yes. And don't ask again. &gt;&gt; Yes.
[38:03] &gt;&gt; Yes.
[38:03] &gt;&gt; Yes. &gt;&gt; YOLO, baby. YOLO.
[38:04] &gt;&gt; YOLO, baby. YOLO.
[38:04] &gt;&gt; YOLO, baby. YOLO. &gt;&gt; So, I pay 100 a month for Max or
[38:06] &gt;&gt; So, I pay 100 a month for Max or
[38:06] &gt;&gt; So, I pay 100 a month for Max or whatever it is. Yeah. I can't get a bill
[38:08] whatever it is. Yeah. I can't get a bill
[38:08] whatever it is. Yeah. I can't get a bill &gt;&gt; say yes
[38:09] &gt;&gt; say yes
[38:09] &gt;&gt; say yes &gt;&gt; higher than that.
[38:10] &gt;&gt; higher than that.
[38:10] &gt;&gt; higher than that. &gt;&gt; No, you can't.
[38:10] &gt;&gt; No, you can't.
[38:10] &gt;&gt; No, you can't. &gt;&gt; Right. Whatever. You were you were only
[38:12] &gt;&gt; Right. Whatever. You were you were only
[38:12] &gt;&gt; Right. Whatever. You were you were only like a usage based thing at the time.
[38:14] like a usage based thing at the time.
[38:14] like a usage based thing at the time. Yeah.
[38:14] Yeah.
[38:14] Yeah. &gt;&gt; Usage based API based. Yeah.
[38:16] &gt;&gt; Usage based API based. Yeah.
[38:16] &gt;&gt; Usage based API based. Yeah. &gt;&gt; Right. Which is tricky to figure out. I
[38:17] &gt;&gt; Right. Which is tricky to figure out. I
[38:17] &gt;&gt; Right. Which is tricky to figure out. I was looking into that and like well
[38:18] was looking into that and like well
[38:18] was looking into that and like well maybe I'll just do this and you're
[38:20] maybe I'll just do this and you're
[38:20] maybe I'll just do this and you're trying to figure out the economy like
[38:21] trying to figure out the economy like
[38:21] trying to figure out the economy like which way to go.
[38:22] which way to go.
[38:22] which way to go. &gt;&gt; I know.
[38:23] &gt;&gt; I know.
[38:23] &gt;&gt; I know. &gt;&gt; But I guess just having that cap them
[38:24] &gt;&gt; But I guess just having that cap them
[38:24] &gt;&gt; But I guess just having that cap them out monthly. Whatever I do I won't get.
[38:26] out monthly. Whatever I do I won't get.
[38:26] out monthly. Whatever I do I won't get. &gt;&gt; And you can kind of mix and match like
[38:28] &gt;&gt; And you can kind of mix and match like
[38:28] &gt;&gt; And you can kind of mix and match like for most of this you could use Gemma 4
[38:30] for most of this you could use Gemma 4
[38:30] for most of this you could use Gemma 4 and then the very last implement step
[38:31] and then the very last implement step
[38:32] and then the very last implement step switch to a more capable model you know
[38:34] switch to a more capable model you know
[38:34] switch to a more capable model you know like kind of pick and choose. So, it's
[38:36] like kind of pick and choose. So, it's
[38:36] like kind of pick and choose. So, it's asking us npm packages aren't installed.
[38:38] asking us npm packages aren't installed.
[38:38] asking us npm packages aren't installed. How should I run the test coverage?
[38:40] How should I run the test coverage?
[38:40] How should I run the test coverage? Should I proceed with implement? Let's
[38:42] Should I proceed with implement? Let's
[38:42] Should I proceed with implement? Let's do one. I would press enter. And it's
[38:44] do one. I would press enter. And it's
[38:44] do one. I would press enter. And it's going to go ahead and install the NodeJS
[38:46] going to go ahead and install the NodeJS
[38:46] going to go ahead and install the NodeJS kit that it needs for the JavaScript.
[38:48] kit that it needs for the JavaScript.
[38:48] kit that it needs for the JavaScript. And that's fine. And that's why it's
[38:50] And that's fine. And that's why it's
[38:50] And that's fine. And that's why it's asking you cuz it it wanted to know if
[38:51] asking you cuz it it wanted to know if
[38:51] asking you cuz it it wanted to know if it was okay to install a couple things.
[38:53] it was okay to install a couple things.
[38:53] it was okay to install a couple things. &gt;&gt; You know what's funny with like the cost
[38:55] &gt;&gt; You know what's funny with like the cost
[38:55] &gt;&gt; You know what's funny with like the cost and tokens? It'll be like a day or two
[38:56] and tokens? It'll be like a day or two
[38:56] and tokens? It'll be like a day or two I'll go by that I don't use the tool.
[38:58] I'll go by that I don't use the tool.
[38:58] I'll go by that I don't use the tool. And I'm like, "Oh, damn.
[38:59] And I'm like, "Oh, damn.
[38:59] And I'm like, "Oh, damn. &gt;&gt; I know."
[38:59] &gt;&gt; I know."
[38:59] &gt;&gt; I know." &gt;&gt; Like, I got to like, you know, I got to
[39:02] &gt;&gt; Like, I got to like, you know, I got to
[39:02] &gt;&gt; Like, I got to like, you know, I got to use it every day to get my value, right?
[39:03] use it every day to get my value, right?
[39:03] use it every day to get my value, right? But I have no idea. I don't really look
[39:05] But I have no idea. I don't really look
[39:05] But I have no idea. I don't really look at the usage. I haven't hit it since I
[39:06] at the usage. I haven't hit it since I
[39:06] at the usage. I haven't hit it since I went to max, but I was hitting it at the
[39:08] went to max, but I was hitting it at the
[39:08] went to max, but I was hitting it at the tier under.
[39:09] tier under.
[39:09] tier under. &gt;&gt; So, can you scroll up a little bit? It's
[39:11] &gt;&gt; So, can you scroll up a little bit? It's
[39:11] &gt;&gt; So, can you scroll up a little bit? It's telling us something here. We've hit a
[39:13] telling us something here. We've hit a
[39:13] telling us something here. We've hit a bit of a problem here. Uh, I can't
[39:15] bit of a problem here. Uh, I can't
[39:15] bit of a problem here. Uh, I can't install node myself, but you can install
[39:17] install node myself, but you can install
[39:17] install node myself, but you can install this. Okay. Can you highlight this curl
[39:20] this. Okay. Can you highlight this curl
[39:20] this. Okay. Can you highlight this curl command?
[39:21] command?
[39:21] command? &gt;&gt; Yeah. Do I start with the
[39:23] &gt;&gt; Yeah. Do I start with the
[39:23] &gt;&gt; Yeah. Do I start with the &gt;&gt; uh No, just after the bang. Yeah.
[39:25] &gt;&gt; uh No, just after the bang. Yeah.
[39:25] &gt;&gt; uh No, just after the bang. Yeah. &gt;&gt; Right here.
[39:26] &gt;&gt; Right here.
[39:26] &gt;&gt; Right here. &gt;&gt; And copy that. And then let's open a new
[39:28] &gt;&gt; And copy that. And then let's open a new
[39:28] &gt;&gt; And copy that. And then let's open a new terminal. Just hit plus here, Andy.
[39:31] terminal. Just hit plus here, Andy.
[39:31] terminal. Just hit plus here, Andy. &gt;&gt; Oh, does it tell us to put it in the new
[39:32] &gt;&gt; Oh, does it tell us to put it in the new
[39:32] &gt;&gt; Oh, does it tell us to put it in the new terminal? Well, we don't want to break
[39:34] terminal? Well, we don't want to break
[39:34] terminal? Well, we don't want to break out of that clawed thing. So now just
[39:35] out of that clawed thing. So now just
[39:35] out of that clawed thing. So now just paste that in and see if that installs
[39:37] paste that in and see if that installs
[39:37] paste that in and see if that installs node. Things go off the rails, of
[39:39] node. Things go off the rails, of
[39:39] node. Things go off the rails, of course, at the very last step, but this
[39:40] course, at the very last step, but this
[39:40] course, at the very last step, but this is just because node's not installed in
[39:42] is just because node's not installed in
[39:42] is just because node's not installed in this machine
[39:43] this machine
[39:43] this machine &gt;&gt; right there.
[39:43] &gt;&gt; right there.
[39:43] &gt;&gt; right there. &gt;&gt; Yeah. And then I would do the same here.
[39:46] &gt;&gt; Yeah. And then I would do the same here.
[39:46] &gt;&gt; Yeah. And then I would do the same here. Bring this line back. Thanks for your
[39:48] Bring this line back. Thanks for your
[39:48] Bring this line back. Thanks for your patience, everyone. We're just
[39:50] patience, everyone. We're just
[39:50] patience, everyone. We're just &gt;&gt; man,
[39:51] &gt;&gt; man,
[39:51] &gt;&gt; man, &gt;&gt; just a node install issue. Say it again.
[39:52] &gt;&gt; just a node install issue. Say it again.
[39:52] &gt;&gt; just a node install issue. Say it again. &gt;&gt; I just press enter. Let's try that.
[39:54] &gt;&gt; I just press enter. Let's try that.
[39:54] &gt;&gt; I just press enter. Let's try that. &gt;&gt; Okay, there we go. Awesome. Close your
[39:57] &gt;&gt; Okay, there we go. Awesome. Close your
[39:57] &gt;&gt; Okay, there we go. Awesome. Close your terminal to restart NVM or fuse the
[39:59] terminal to restart NVM or fuse the
[39:59] terminal to restart NVM or fuse the following. Okay. So, go back into the
[40:01] following. Okay. So, go back into the
[40:01] following. Okay. So, go back into the original terminal and scroll all the way
[40:04] original terminal and scroll all the way
[40:04] original terminal and scroll all the way to the bottom. Say, can you check for
[40:06] to the bottom. Say, can you check for
[40:06] to the bottom. Say, can you check for node now?
[40:06] node now?
[40:06] node now? &gt;&gt; Still no.
[40:07] &gt;&gt; Still no.
[40:07] &gt;&gt; Still no. &gt;&gt; Still no node.
[40:09] &gt;&gt; Still no node.
[40:09] &gt;&gt; Still no node. &gt;&gt; Says enter. You say yes.
[40:10] &gt;&gt; Says enter. You say yes.
[40:10] &gt;&gt; Says enter. You say yes. &gt;&gt; So, it's doing so much other work for
[40:12] &gt;&gt; So, it's doing so much other work for
[40:12] &gt;&gt; So, it's doing so much other work for us. Why can't it install what it needs?
[40:14] us. Why can't it install what it needs?
[40:14] us. Why can't it install what it needs? &gt;&gt; It should be able to. It should be able
[40:16] &gt;&gt; It should be able to. It should be able
[40:16] &gt;&gt; It should be able to. It should be able to
[40:16] to
[40:16] to &gt;&gt; for whatever reason.
[40:17] &gt;&gt; for whatever reason.
[40:17] &gt;&gt; for whatever reason. &gt;&gt; Press enter there. Okay. See, nvm is
[40:20] &gt;&gt; Press enter there. Okay. See, nvm is
[40:20] &gt;&gt; Press enter there. Okay. See, nvm is installed and working, but no node is
[40:22] installed and working, but no node is
[40:22] installed and working, but no node is downloaded yet. Let me try to finish the
[40:24] downloaded yet. Let me try to finish the
[40:24] downloaded yet. Let me try to finish the node install via. So, press enter. Yes,
[40:27] node install via. So, press enter. Yes,
[40:27] node install via. So, press enter. Yes, it is trying to work it itself out now.
[40:28] it is trying to work it itself out now.
[40:28] it is trying to work it itself out now. It's going to try to install this stuff
[40:30] It's going to try to install this stuff
[40:30] It's going to try to install this stuff for us.
[40:31] for us.
[40:31] for us. &gt;&gt; I appreciate that.
[40:32] &gt;&gt; I appreciate that.
[40:32] &gt;&gt; I appreciate that. &gt;&gt; I really appreciate that. Especially
[40:35] &gt;&gt; I really appreciate that. Especially
[40:35] &gt;&gt; I really appreciate that. Especially things like node packages. I'm not the
[40:36] things like node packages. I'm not the
[40:36] things like node packages. I'm not the biggest JavaScript developer. Some of
[40:38] biggest JavaScript developer. Some of
[40:38] biggest JavaScript developer. Some of that gets a little bit
[40:39] that gets a little bit
[40:39] that gets a little bit &gt;&gt; going to keep hitting yes.
[40:40] &gt;&gt; going to keep hitting yes.
[40:40] &gt;&gt; going to keep hitting yes. &gt;&gt; Yeah, I would.
[40:41] &gt;&gt; Yeah, I would.
[40:41] &gt;&gt; Yeah, I would. &gt;&gt; I can almost smell the tokens burning.
[40:43] &gt;&gt; I can almost smell the tokens burning.
[40:43] &gt;&gt; I can almost smell the tokens burning. [laughter] Oh, wait. That's the fire I
[40:45] [laughter] Oh, wait. That's the fire I
[40:45] [laughter] Oh, wait. That's the fire I made.
[40:45] made.
[40:45] made. &gt;&gt; Okay, so now it's running. Notice what
[40:47] &gt;&gt; Okay, so now it's running. Notice what
[40:47] &gt;&gt; Okay, so now it's running. Notice what we got up here, Andy. Source files,
[40:49] we got up here, Andy. Source files,
[40:49] we got up here, Andy. Source files, styles, tests. So, claude GitHub specify
[40:54] styles, tests. So, claude GitHub specify
[40:54] styles, tests. So, claude GitHub specify were part of our install. Specs is part
[40:56] were part of our install. Specs is part
[40:56] were part of our install. Specs is part of our spec driven, but source styles
[40:58] of our spec driven, but source styles
[40:58] of our spec driven, but source styles and tests is code.
[41:01] and tests is code.
[41:01] and tests is code. &gt;&gt; Those are folders that are going to hold
[41:03] &gt;&gt; Those are folders that are going to hold
[41:03] &gt;&gt; Those are folders that are going to hold code once this is done cooking. And I
[41:05] code once this is done cooking. And I
[41:05] code once this is done cooking. And I don't know how long this is going to
[41:06] don't know how long this is going to
[41:06] don't know how long this is going to take. Implement is the longest of the
[41:09] take. Implement is the longest of the
[41:09] take. Implement is the longest of the phases. Call it 5 minutes, 6 minutes.
[41:11] phases. Call it 5 minutes, 6 minutes.
[41:11] phases. Call it 5 minutes, 6 minutes. We'll see.
[41:12] We'll see.
[41:12] We'll see. &gt;&gt; Time for me to use the restroom.
[41:13] &gt;&gt; Time for me to use the restroom.
[41:13] &gt;&gt; Time for me to use the restroom. &gt;&gt; Time for you to use the restroom.
[41:14] &gt;&gt; Time for you to use the restroom.
[41:14] &gt;&gt; Time for you to use the restroom. [laughter] And we might edit this out
[41:15] [laughter] And we might edit this out
[41:15] [laughter] And we might edit this out and trim it down. But what's neat is at
[41:17] and trim it down. But what's neat is at
[41:17] and trim it down. But what's neat is at the very end of this, we're going to be
[41:19] the very end of this, we're going to be
[41:19] the very end of this, we're going to be able to launch a subnetting video game
[41:21] able to launch a subnetting video game
[41:21] able to launch a subnetting video game in a browser. That is the whole point of
[41:23] in a browser. That is the whole point of
[41:23] in a browser. That is the whole point of this outcome. Now, we've done this in an
[41:26] this outcome. Now, we've done this in an
[41:26] this outcome. Now, we've done this in an hour on the fly. Andy's literally never
[41:28] hour on the fly. Andy's literally never
[41:28] hour on the fly. Andy's literally never done this before. We're try and we
[41:31] done this before. We're try and we
[41:31] done this before. We're try and we didn't prep for this at all. It was
[41:32] didn't prep for this at all. It was
[41:32] didn't prep for this at all. It was like, let's just do it, man. So, you can
[41:34] like, let's just do it, man. So, you can
[41:34] like, let's just do it, man. So, you can do this. That's the exciting thing.
[41:36] do this. That's the exciting thing.
[41:36] do this. That's the exciting thing. There is a little foreplay. There is a,
[41:38] There is a little foreplay. There is a,
[41:38] There is a little foreplay. There is a, you know, you need to devote 45 minutes
[41:39] you know, you need to devote 45 minutes
[41:39] you know, you need to devote 45 minutes to an hour of your time or like you
[41:42] to an hour of your time or like you
[41:42] to an hour of your time or like you don't have to do all these sequentially.
[41:44] don't have to do all these sequentially.
[41:44] don't have to do all these sequentially. Let's say you do the first three steps,
[41:46] Let's say you do the first three steps,
[41:46] Let's say you do the first three steps, then you go have lunch and you come back
[41:47] then you go have lunch and you come back
[41:47] then you go have lunch and you come back and you resume the steps after lunch or
[41:49] and you resume the steps after lunch or
[41:49] and you resume the steps after lunch or whatever. There's a lot of ways to break
[41:51] whatever. There's a lot of ways to break
[41:51] whatever. There's a lot of ways to break up the monotony of it, but look at all
[41:52] up the monotony of it, but look at all
[41:52] up the monotony of it, but look at all this stuff we're getting. Testing
[41:54] this stuff we're getting. Testing
[41:54] this stuff we're getting. Testing configs, JSON files, package files,
[41:57] configs, JSON files, package files,
[41:57] configs, JSON files, package files, index.html,
[41:59] index.html,
[41:59] index.html, uh, styles, source code. So, it just
[42:03] uh, styles, source code. So, it just
[42:03] uh, styles, source code. So, it just wrote, like it said, it wrote 200 lines
[42:05] wrote, like it said, it wrote 200 lines
[42:05] wrote, like it said, it wrote 200 lines of CSS for us. So, let's hit yes here,
[42:09] of CSS for us. So, let's hit yes here,
[42:09] of CSS for us. So, let's hit yes here, Andy. And because it installed Node,
[42:11] Andy. And because it installed Node,
[42:11] Andy. And because it installed Node, it's actually going to test and
[42:12] it's actually going to test and
[42:12] it's actually going to test and regression test the code it wrote. So it
[42:14] regression test the code it wrote. So it
[42:14] regression test the code it wrote. So it writes the code, it tests the code, and
[42:16] writes the code, it tests the code, and
[42:16] writes the code, it tests the code, and it gives us a runtime environment to run
[42:18] it gives us a runtime environment to run
[42:18] it gives us a runtime environment to run it in the browser. And you're looking at
[42:20] it in the browser. And you're looking at
[42:20] it in the browser. And you're looking at two network engineers doing this
[42:22] two network engineers doing this
[42:22] two network engineers doing this together. We haven't launched Python. We
[42:24] together. We haven't launched Python. We
[42:24] together. We haven't launched Python. We haven't written a single line of code.
[42:26] haven't written a single line of code.
[42:26] haven't written a single line of code. Everything has been in markdown.
[42:27] Everything has been in markdown.
[42:28] Everything has been in markdown. Markdown is kind of the universal
[42:30] Markdown is kind of the universal
[42:30] Markdown is kind of the universal language between humans and LLMs.
[42:32] language between humans and LLMs.
[42:32] language between humans and LLMs. &gt;&gt; Thank you for referring to me as a
[42:34] &gt;&gt; Thank you for referring to me as a
[42:34] &gt;&gt; Thank you for referring to me as a network engineer. The longer I'm in
[42:35] network engineer. The longer I'm in
[42:35] network engineer. The longer I'm in marketing, I don't know if I lose my
[42:37] marketing, I don't know if I lose my
[42:37] marketing, I don't know if I lose my network engineer card at some point. So
[42:38] network engineer card at some point. So
[42:38] network engineer card at some point. So I keep doing this to for street cred,
[42:41] I keep doing this to for street cred,
[42:41] I keep doing this to for street cred, you know,
[42:41] you know,
[42:41] you know, &gt;&gt; like I'm trying to do technical things,
[42:42] &gt;&gt; like I'm trying to do technical things,
[42:42] &gt;&gt; like I'm trying to do technical things, right? But
[42:43] right? But
[42:43] right? But &gt;&gt; it's funny people some people have said
[42:45] &gt;&gt; it's funny people some people have said
[42:45] &gt;&gt; it's funny people some people have said like I've turned my back on my
[42:46] like I've turned my back on my
[42:46] like I've turned my back on my networking history and I'm an AI
[42:48] networking history and I'm an AI
[42:48] networking history and I'm an AI engineer now. Right. And it's like well
[42:49] engineer now. Right. And it's like well
[42:50] engineer now. Right. And it's like well I mean we we've re we all reinvent
[42:51] I mean we we've re we all reinvent
[42:51] I mean we we've re we all reinvent ourselves. Right. So
[42:53] ourselves. Right. So
[42:53] ourselves. Right. So &gt;&gt; Scott Rob said it best. It's all
[42:54] &gt;&gt; Scott Rob said it best. It's all
[42:54] &gt;&gt; Scott Rob said it best. It's all additive.
[42:55] additive.
[42:55] additive. &gt;&gt; Right.
[42:56] &gt;&gt; Right.
[42:56] &gt;&gt; Right. &gt;&gt; Your networking knowledge is there.
[42:57] &gt;&gt; Your networking knowledge is there.
[42:57] &gt;&gt; Your networking knowledge is there. &gt;&gt; Right. Right. Right. Right.
[42:58] &gt;&gt; Right. Right. Right. Right.
[42:58] &gt;&gt; Right. Right. Right. Right. &gt;&gt; Cuz I like you know I'm going to give up
[43:00] &gt;&gt; Cuz I like you know I'm going to give up
[43:00] &gt;&gt; Cuz I like you know I'm going to give up on all the networking stuff to learn
[43:01] on all the networking stuff to learn
[43:01] on all the networking stuff to learn this coding. Like no no no no. It's all
[43:03] this coding. Like no no no no. It's all
[43:03] this coding. Like no no no no. It's all additive. It doesn't go away.
[43:05] additive. It doesn't go away.
[43:05] additive. It doesn't go away. &gt;&gt; So we're in phase two now. Foundational
[43:07] &gt;&gt; So we're in phase two now. Foundational
[43:07] &gt;&gt; So we're in phase two now. Foundational engine test first. I'll write the
[43:09] engine test first. I'll write the
[43:09] engine test first. I'll write the failing and it does TDD. It's so neat.
[43:12] failing and it does TDD. It's so neat.
[43:12] failing and it does TDD. It's so neat. I'm going to write failing tests then
[43:14] I'm going to write failing tests then
[43:14] I'm going to write failing tests then fix the code. So SDDD actually uses
[43:19] fix the code. So SDDD actually uses
[43:19] fix the code. So SDDD actually uses testdriven development. That is neat. I
[43:21] testdriven development. That is neat. I
[43:21] testdriven development. That is neat. I didn't realize that it's actually
[43:23] didn't realize that it's actually
[43:23] didn't realize that it's actually writing failed tests and then it's going
[43:24] writing failed tests and then it's going
[43:24] writing failed tests and then it's going to fix the code. See vi test. Yeah.
[43:27] to fix the code. See vi test. Yeah.
[43:27] to fix the code. See vi test. Yeah. Inner. Yes. Again. Sorry. So we're
[43:29] Inner. Yes. Again. Sorry. So we're
[43:29] Inner. Yes. Again. Sorry. So we're actually testing all the code and uh
[43:32] actually testing all the code and uh
[43:32] actually testing all the code and uh we're getting real close here. We've
[43:33] we're getting real close here. We've
[43:33] we're getting real close here. We've only been cooking for about 3 minutes. I
[43:35] only been cooking for about 3 minutes. I
[43:35] only been cooking for about 3 minutes. I know it feels like a longer.
[43:36] know it feels like a longer.
[43:36] know it feels like a longer. &gt;&gt; So the things I've built I don't think
[43:37] &gt;&gt; So the things I've built I don't think
[43:37] &gt;&gt; So the things I've built I don't think I've tested the code. I think if it
[43:39] I've tested the code. I think if it
[43:39] I've tested the code. I think if it works I'm happy,
[43:40] works I'm happy,
[43:40] works I'm happy, &gt;&gt; right? or as a vibe coder you have to
[43:42] &gt;&gt; right? or as a vibe coder you have to
[43:42] &gt;&gt; right? or as a vibe coder you have to say okay it looks pretty good can you
[43:45] say okay it looks pretty good can you
[43:45] say okay it looks pretty good can you generate a bunch of tests for me now and
[43:47] generate a bunch of tests for me now and
[43:47] generate a bunch of tests for me now and test the code right you can do that
[43:49] test the code right you can do that
[43:49] test the code right you can do that through vibe coding it's a built-in
[43:51] through vibe coding it's a built-in
[43:51] through vibe coding it's a built-in feature of this so I'm implementing the
[43:54] feature of this so I'm implementing the
[43:54] feature of this so I'm implementing the engine and these are tasks 11 through 15
[43:57] engine and these are tasks 11 through 15
[43:58] engine and these are tasks 11 through 15 so now if you expand source here and
[44:00] so now if you expand source here and
[44:00] so now if you expand source here and engine and just grab a random file
[44:03] engine and just grab a random file
[44:03] engine and just grab a random file addresses so look at this code we did
[44:06] addresses so look at this code we did
[44:06] addresses so look at this code we did not have to write
[44:08] not have to write
[44:08] not have to write I mean you've lost me on line 12,
[44:11] I mean you've lost me on line 12,
[44:11] I mean you've lost me on line 12, &gt;&gt; right? Like I'm not a JavaScript
[44:13] &gt;&gt; right? Like I'm not a JavaScript
[44:13] &gt;&gt; right? Like I'm not a JavaScript programmer. I mean, I could break I I
[44:14] programmer. I mean, I could break I I
[44:14] programmer. I mean, I could break I I could do this. I'm I I can read
[44:16] could do this. I'm I I can read
[44:16] could do this. I'm I I can read JavaScript, but the whole point is we
[44:18] JavaScript, but the whole point is we
[44:18] JavaScript, but the whole point is we did not have to do any of this
[44:19] did not have to do any of this
[44:20] did not have to do any of this ourselves, right?
[44:20] ourselves, right?
[44:20] ourselves, right? &gt;&gt; Not me, bro. [laughter]
[44:23] &gt;&gt; Not me, bro. [laughter]
[44:23] &gt;&gt; Not me, bro. [laughter] &gt;&gt; Right. Is this not crazy?
[44:25] &gt;&gt; Right. Is this not crazy?
[44:25] &gt;&gt; Right. Is this not crazy? &gt;&gt; Listen, this is all magic to me.
[44:27] &gt;&gt; Listen, this is all magic to me.
[44:27] &gt;&gt; Listen, this is all magic to me. &gt;&gt; And there's a subnet.js,
[44:30] &gt;&gt; And there's a subnet.js,
[44:30] &gt;&gt; And there's a subnet.js, so it's actually And there's our index,
[44:32] so it's actually And there's our index,
[44:32] so it's actually And there's our index, which is awesome, which means we're
[44:33] which is awesome, which means we're
[44:33] which is awesome, which means we're getting really close cuz we got the
[44:34] getting really close cuz we got the
[44:34] getting really close cuz we got the index.js file. So, we're pretty close
[44:37] index.js file. So, we're pretty close
[44:37] index.js file. So, we're pretty close here to having a a functional MVP of our
[44:40] here to having a a functional MVP of our
[44:40] here to having a a functional MVP of our video game.
[44:41] video game.
[44:41] video game. &gt;&gt; Eric, do [clears throat] you have an
[44:42] &gt;&gt; Eric, do [clears throat] you have an
[44:42] &gt;&gt; Eric, do [clears throat] you have an opinion on this stuff? LLMs and using AI
[44:44] opinion on this stuff? LLMs and using AI
[44:44] opinion on this stuff? LLMs and using AI to code and cuz you're like hardcore
[44:47] to code and cuz you're like hardcore
[44:47] to code and cuz you're like hardcore coder guy. I feel bad that you're
[44:49] coder guy. I feel bad that you're
[44:49] coder guy. I feel bad that you're sitting here waiting for us. So, here
[44:50] sitting here waiting for us. So, here
[44:50] sitting here waiting for us. So, here talking to talk into a microphone while
[44:52] talking to talk into a microphone while
[44:52] talking to talk into a microphone while we're vibing.
[44:53] we're vibing.
[44:53] we're vibing. &gt;&gt; No. Yeah. So, I I definitely I
[44:55] &gt;&gt; No. Yeah. So, I I definitely I
[44:55] &gt;&gt; No. Yeah. So, I I definitely I definitely think this is uh this is
[44:58] definitely think this is uh this is
[44:58] definitely think this is uh this is magic to me as well. Um like John, I
[45:00] magic to me as well. Um like John, I
[45:00] magic to me as well. Um like John, I don't I don't do a lot of JavaScript and
[45:02] don't I don't do a lot of JavaScript and
[45:02] don't I don't do a lot of JavaScript and I don't feel like I don't get stuck now,
[45:04] I don't feel like I don't get stuck now,
[45:04] I don't feel like I don't get stuck now, right, John? Um I don't know. I don't
[45:06] right, John? Um I don't know. I don't
[45:06] right, John? Um I don't know. I don't know if you feel the same way but
[45:08] know if you feel the same way but
[45:08] know if you feel the same way but essentially you know whatever it is if
[45:09] essentially you know whatever it is if
[45:09] essentially you know whatever it is if I'm writing a book uh writing a chapter
[45:12] I'm writing a book uh writing a chapter
[45:12] I'm writing a book uh writing a chapter if I writing some code or if I some
[45:14] if I writing some code or if I some
[45:14] if I writing some code or if I some ideas to generate some brainstorming I
[45:16] ideas to generate some brainstorming I
[45:16] ideas to generate some brainstorming I used to have these uh writer's block or
[45:19] used to have these uh writer's block or
[45:19] used to have these uh writer's block or or you know coders block or just uh
[45:22] or you know coders block or just uh
[45:22] or you know coders block or just uh procrastination whatever you want to
[45:24] procrastination whatever you want to
[45:24] procrastination whatever you want to call it I just kind of sit be behind and
[45:26] call it I just kind of sit be behind and
[45:26] call it I just kind of sit be behind and I usually have to just gun through it
[45:28] I usually have to just gun through it
[45:28] I usually have to just gun through it right like usually I used to just have
[45:30] right like usually I used to just have
[45:30] right like usually I used to just have to say sit in front of of of a blank
[45:33] to say sit in front of of of a blank
[45:33] to say sit in front of of of a blank page for for maybe two pomodoro
[45:36] page for for maybe two pomodoro
[45:36] page for for maybe two pomodoro or like I go get so whatever it is,
[45:38] or like I go get so whatever it is,
[45:38] or like I go get so whatever it is, right? Like so I have these gaps where
[45:39] right? Like so I have these gaps where
[45:40] right? Like so I have these gaps where I'm not productive but I know it's the
[45:42] I'm not productive but I know it's the
[45:42] I'm not productive but I know it's the necessary path toward productivity but
[45:44] necessary path toward productivity but
[45:44] necessary path toward productivity but but nowadays I don't I don't feel like
[45:46] but nowadays I don't I don't feel like
[45:46] but nowadays I don't I don't feel like get stuck anymore cuz AI will start to
[45:49] get stuck anymore cuz AI will start to
[45:49] get stuck anymore cuz AI will start to give you something. It [laughter] may
[45:50] give you something. It [laughter] may
[45:50] give you something. It [laughter] may not be correct, right? It may not be the
[45:53] not be correct, right? It may not be the
[45:53] not be correct, right? It may not be the perfect one, but it'll give you
[45:54] perfect one, but it'll give you
[45:54] perfect one, but it'll give you something. And from there, you could
[45:55] something. And from there, you could
[45:55] something. And from there, you could just say, "Oh, you idiot." Like, you
[45:57] just say, "Oh, you idiot." Like, you
[45:57] just say, "Oh, you idiot." Like, you know, this feeling is not going to get
[45:59] know, this feeling is not going to get
[45:59] know, this feeling is not going to get hurt, but you know, I feel like I don't
[46:01] hurt, but you know, I feel like I don't
[46:01] hurt, but you know, I feel like I don't get stuck anymore. And that's the main
[46:02] get stuck anymore. And that's the main
[46:02] get stuck anymore. And that's the main feeling I've had for the last, you know,
[46:04] feeling I've had for the last, you know,
[46:04] feeling I've had for the last, you know, maybe year and a half, two years of
[46:06] maybe year and a half, two years of
[46:06] maybe year and a half, two years of actively using AI all the time. So, so
[46:09] actively using AI all the time. So, so
[46:09] actively using AI all the time. So, so yeah, back to you, Mike.
[46:11] yeah, back to you, Mike.
[46:11] yeah, back to you, Mike. &gt;&gt; So, instead of staring at the blank
[46:12] &gt;&gt; So, instead of staring at the blank
[46:12] &gt;&gt; So, instead of staring at the blank page, you have something you can iterate
[46:15] page, you have something you can iterate
[46:15] page, you have something you can iterate on. I
[46:15] on. I
[46:15] on. I &gt;&gt; I read this quote that said, "Now after
[46:18] &gt;&gt; I read this quote that said, "Now after
[46:18] &gt;&gt; I read this quote that said, "Now after vibe coding, I don't have four
[46:19] vibe coding, I don't have four
[46:19] vibe coding, I don't have four unfinished projects. I've got 140
[46:21] unfinished projects. I've got 140
[46:21] unfinished projects. I've got 140 unfinished projects, [laughter]
[46:24] unfinished projects, [laughter]
[46:24] unfinished projects, [laughter] right? Okay. So, let's hit okay. I know
[46:27] right? Okay. So, let's hit okay. I know
[46:27] right? Okay. So, let's hit okay. I know we're getting really, really close here.
[46:28] we're getting really, really close here.
[46:28] we're getting really, really close here. I've been trying to keep an eye on it.
[46:30] I've been trying to keep an eye on it.
[46:30] I've been trying to keep an eye on it. So, you can let's maximize this, Andy.
[46:32] So, you can let's maximize this, Andy.
[46:32] So, you can let's maximize this, Andy. We're all done with the GitHub stuff in
[46:33] We're all done with the GitHub stuff in
[46:34] We're all done with the GitHub stuff in the background.
[46:35] the background.
[46:35] the background. &gt;&gt; And I just want to see Okay, so let me
[46:37] &gt;&gt; And I just want to see Okay, so let me
[46:37] &gt;&gt; And I just want to see Okay, so let me read the current line numbers. Uh, do
[46:39] read the current line numbers. Uh, do
[46:39] read the current line numbers. Uh, do you want to scroll up just a little bit?
[46:40] you want to scroll up just a little bit?
[46:40] you want to scroll up just a little bit? Let's see what the last bit of text it
[46:41] Let's see what the last bit of text it
[46:41] Let's see what the last bit of text it was saying here is. Let's go up a little
[46:43] was saying here is. Let's go up a little
[46:43] was saying here is. Let's go up a little bit more. Subnet test.js. It's fixing
[46:46] bit more. Subnet test.js. It's fixing
[46:46] bit more. Subnet test.js. It's fixing some things from the tests.
[46:47] some things from the tests.
[46:47] some things from the tests. &gt;&gt; How does it know what to test? I guess
[46:49] &gt;&gt; How does it know what to test? I guess
[46:49] &gt;&gt; How does it know what to test? I guess that's just stuff that I'd have to go to
[46:51] that's just stuff that I'd have to go to
[46:51] that's just stuff that I'd have to go to computer science school for, right? Like
[46:52] computer science school for, right? Like
[46:52] computer science school for, right? Like unit testing, regression testing.
[46:55] unit testing, regression testing.
[46:55] unit testing, regression testing. There's a a couple different things that
[46:56] There's a a couple different things that
[46:56] There's a a couple different things that it's probably doing for testing.
[46:58] it's probably doing for testing.
[46:58] it's probably doing for testing. &gt;&gt; They're just like testing frameworks
[47:00] &gt;&gt; They're just like testing frameworks
[47:00] &gt;&gt; They're just like testing frameworks that exist and it knows how to code.
[47:02] that exist and it knows how to code.
[47:02] that exist and it knows how to code. &gt;&gt; Yeah, it's using this framework called
[47:03] &gt;&gt; Yeah, it's using this framework called
[47:03] &gt;&gt; Yeah, it's using this framework called VI test, which I I don't know much
[47:06] VI test, which I I don't know much
[47:06] VI test, which I I don't know much about, but it tends to use VI test quite
[47:08] about, but it tends to use VI test quite
[47:08] about, but it tends to use VI test quite a bit. So, let's hit proceed.
[47:10] a bit. So, let's hit proceed.
[47:10] a bit. So, let's hit proceed. &gt;&gt; And it can't test while it's coding.
[47:13] &gt;&gt; And it can't test while it's coding.
[47:13] &gt;&gt; And it can't test while it's coding. &gt;&gt; No, it writes the code and then it
[47:14] &gt;&gt; No, it writes the code and then it
[47:14] &gt;&gt; No, it writes the code and then it regression and then it tests after.
[47:16] regression and then it tests after.
[47:16] regression and then it tests after. Right. So let's press okay. 7 minutes of
[47:20] Right. So let's press okay. 7 minutes of
[47:20] Right. So let's press okay. 7 minutes of implement. Like I said, we should be
[47:21] implement. Like I said, we should be
[47:21] implement. Like I said, we should be getting close. It it usually takes 7 to
[47:23] getting close. It it usually takes 7 to
[47:23] getting close. It it usually takes 7 to 10 minutes of of this very last step cuz
[47:26] 10 minutes of of this very last step cuz
[47:26] 10 minutes of of this very last step cuz it's doing so much.
[47:27] it's doing so much.
[47:27] it's doing so much. &gt;&gt; It's generating all the tests. It's
[47:29] &gt;&gt; It's generating all the tests. It's
[47:29] &gt;&gt; It's generating all the tests. It's generating all the code. It's testing
[47:30] generating all the code. It's testing
[47:30] generating all the code. It's testing all the code. And it even know so the
[47:32] all the code. And it even know so the
[47:32] all the code. And it even know so the variable length subnet mask wasn't
[47:34] variable length subnet mask wasn't
[47:34] variable length subnet mask wasn't tested. So it just tested variable
[47:35] tested. So it just tested variable
[47:35] tested. So it just tested variable length subnet mask. Kind of cool. So
[47:37] length subnet mask. Kind of cool. So
[47:37] length subnet mask. Kind of cool. So let's continue. And this is sort of what
[47:40] let's continue. And this is sort of what
[47:40] let's continue. And this is sort of what bothers me a little bit of some of the
[47:42] bothers me a little bit of some of the
[47:42] bothers me a little bit of some of the negative anti-AI stuff. It's bad code.
[47:45] negative anti-AI stuff. It's bad code.
[47:45] negative anti-AI stuff. It's bad code. It's slop. It's this testing it. It's
[47:48] It's slop. It's this testing it. It's
[47:48] It's slop. It's this testing it. It's testing itself. It's writing tests. It's
[47:49] testing itself. It's writing tests. It's
[47:49] testing itself. It's writing tests. It's doing tests.
[47:50] doing tests.
[47:50] doing tests. &gt;&gt; So, in the five or six things I've
[47:52] &gt;&gt; So, in the five or six things I've
[47:52] &gt;&gt; So, in the five or six things I've created, I haven't tested any of it.
[47:53] created, I haven't tested any of it.
[47:53] created, I haven't tested any of it. &gt;&gt; Right. And and it was fine though.
[47:56] &gt;&gt; Right. And and it was fine though.
[47:56] &gt;&gt; Right. And and it was fine though. &gt;&gt; Well, it was.
[47:56] &gt;&gt; Well, it was.
[47:56] &gt;&gt; Well, it was. &gt;&gt; But to give you more reassurance, if we
[47:58] &gt;&gt; But to give you more reassurance, if we
[47:58] &gt;&gt; But to give you more reassurance, if we wanted to move this to production or if
[48:00] wanted to move this to production or if
[48:00] wanted to move this to production or if you and I wanted to make the Dolingo for
[48:01] you and I wanted to make the Dolingo for
[48:01] you and I wanted to make the Dolingo for subnetting and make some money on the
[48:03] subnetting and make some money on the
[48:03] subnetting and make some money on the side, we'd really want to know that the
[48:05] side, we'd really want to know that the
[48:05] side, we'd really want to know that the code was tested. Right.
[48:06] code was tested. Right.
[48:06] code was tested. Right. &gt;&gt; Now that I see this, I can almost
[48:08] &gt;&gt; Now that I see this, I can almost
[48:08] &gt;&gt; Now that I see this, I can almost understand the people who know more than
[48:10] understand the people who know more than
[48:10] understand the people who know more than I do. Like, this is garbage. you're not
[48:11] I do. Like, this is garbage. you're not
[48:11] I do. Like, this is garbage. you're not do, but the amount of testing and and
[48:14] do, but the amount of testing and and
[48:14] do, but the amount of testing and and work that someone something is doing
[48:17] work that someone something is doing
[48:17] work that someone something is doing going through this. I don't know how you
[48:19] going through this. I don't know how you
[48:19] going through this. I don't know how you could trash you can trash me for vibing
[48:23] could trash you can trash me for vibing
[48:23] could trash you can trash me for vibing and not testing anything like
[48:25] and not testing anything like
[48:25] and not testing anything like &gt;&gt; I think that's fair cuz I don't know
[48:26] &gt;&gt; I think that's fair cuz I don't know
[48:26] &gt;&gt; I think that's fair cuz I don't know enough yet. But dude, this has been I
[48:29] enough yet. But dude, this has been I
[48:29] enough yet. But dude, this has been I mean it's testing the hell out of the
[48:30] mean it's testing the hell out of the
[48:30] mean it's testing the hell out of the code.
[48:30] code.
[48:30] code. &gt;&gt; I know. And it's actually it's still
[48:32] &gt;&gt; I know. And it's actually it's still
[48:32] &gt;&gt; I know. And it's actually it's still finding little things that it's fixing
[48:35] finding little things that it's fixing
[48:35] finding little things that it's fixing and it says it's pretty close. It said
[48:37] and it says it's pretty close. It said
[48:37] and it says it's pretty close. It said that there was three outstanding tests
[48:38] that there was three outstanding tests
[48:38] that there was three outstanding tests that it needed to write. So, we're down
[48:40] that it needed to write. So, we're down
[48:40] that it needed to write. So, we're down to three tests here. And because it's
[48:43] to three tests here. And because it's
[48:43] to three tests here. And because it's all in this git repo, all the tests are
[48:47] all in this git repo, all the tests are
[48:47] all in this git repo, all the tests are available, right? So, if you don't trust
[48:48] available, right? So, if you don't trust
[48:48] available, right? So, if you don't trust this thing, you could actually go over
[48:50] this thing, you could actually go over
[48:50] this thing, you could actually go over all of the code and see what it tested,
[48:53] all of the code and see what it tested,
[48:53] all of the code and see what it tested, how it tested it, what the spec was.
[48:54] how it tested it, what the spec was.
[48:54] how it tested it, what the spec was. It's all here be laid bare for everyone
[48:57] It's all here be laid bare for everyone
[48:57] It's all here be laid bare for everyone who wants to make this game better or
[48:59] who wants to make this game better or
[48:59] who wants to make this game better or try it on their own.
[48:59] try it on their own.
[48:59] try it on their own. &gt;&gt; You just read my mind. How would we
[49:01] &gt;&gt; You just read my mind. How would we
[49:01] &gt;&gt; You just read my mind. How would we share this? Let's say this is a useful
[49:02] share this? Let's say this is a useful
[49:02] share this? Let's say this is a useful thing and like, oh, great. I wish I had
[49:04] thing and like, oh, great. I wish I had
[49:04] thing and like, oh, great. I wish I had this like when I was studying. Do you
[49:05] this like when I was studying. Do you
[49:05] this like when I was studying. Do you just leave it on the repo and tell
[49:08] just leave it on the repo and tell
[49:08] just leave it on the repo and tell people it's there? Do you can you
[49:10] people it's there? Do you can you
[49:10] people it's there? Do you can you publish it to a website? Like
[49:11] publish it to a website? Like
[49:11] publish it to a website? Like &gt;&gt; so this little button here
[49:13] &gt;&gt; so this little button here
[49:13] &gt;&gt; so this little button here &gt;&gt; I wouldn't put it on our website. I
[49:14] &gt;&gt; I wouldn't put it on our website. I
[49:14] &gt;&gt; I wouldn't put it on our website. I would
[49:14] would
[49:14] would &gt;&gt; No, but you're gonna put on your GitHub.
[49:16] &gt;&gt; No, but you're gonna put on your GitHub.
[49:16] &gt;&gt; No, but you're gonna put on your GitHub. &gt;&gt; Yeah. And then but you got to tell
[49:17] &gt;&gt; Yeah. And then but you got to tell
[49:17] &gt;&gt; Yeah. And then but you got to tell people it's there.
[49:18] people it's there.
[49:18] people it's there. &gt;&gt; It's on this GitHub repo. Check this
[49:19] &gt;&gt; It's on this GitHub repo. Check this
[49:19] &gt;&gt; It's on this GitHub repo. Check this out. Clone the repo. They'll have all
[49:21] out. Clone the repo. They'll have all
[49:21] out. Clone the repo. They'll have all these files locally.
[49:22] these files locally.
[49:22] these files locally. &gt;&gt; So you can just clone, launch, and play
[49:24] &gt;&gt; So you can just clone, launch, and play
[49:24] &gt;&gt; So you can just clone, launch, and play the game.
[49:24] the game.
[49:24] the game. &gt;&gt; Launch. Play. And you know what we could
[49:26] &gt;&gt; Launch. Play. And you know what we could
[49:26] &gt;&gt; Launch. Play. And you know what we could do, Andy? As a second spec, maybe next
[49:29] do, Andy? As a second spec, maybe next
[49:29] do, Andy? As a second spec, maybe next time you have some time. I'd like to
[49:31] time you have some time. I'd like to
[49:31] time you have some time. I'd like to turn this video game into a web hosted
[49:33] turn this video game into a web hosted
[49:33] turn this video game into a web hosted game on Google Cloud or Amazon Cloud or
[49:35] game on Google Cloud or Amazon Cloud or
[49:36] game on Google Cloud or Amazon Cloud or Azure or whatever
[49:37] Azure or whatever
[49:37] Azure or whatever &gt;&gt; so that you don't have to clone it. It's
[49:38] &gt;&gt; so that you don't have to clone it. It's
[49:38] &gt;&gt; so that you don't have to clone it. It's just
[49:38] just
[49:38] just &gt;&gt; move it to the cloud.
[49:39] &gt;&gt; move it to the cloud.
[49:39] &gt;&gt; move it to the cloud. &gt;&gt; Well, that's where I was going with
[49:40] &gt;&gt; Well, that's where I was going with
[49:40] &gt;&gt; Well, that's where I was going with this. We can't just present a front end
[49:42] this. We can't just present a front end
[49:42] this. We can't just present a front end to the game on like our website.
[49:44] to the game on like our website.
[49:44] to the game on like our website. &gt;&gt; You we could we could that could be the
[49:46] &gt;&gt; You we could we could that could be the
[49:46] &gt;&gt; You we could we could that could be the next thing we vibe code is great. I know
[49:47] next thing we vibe code is great. I know
[49:47] next thing we vibe code is great. I know the game works. Now I want to host it on
[49:49] the game works. Now I want to host it on
[49:49] the game works. Now I want to host it on this website.
[49:50] this website.
[49:50] this website. &gt;&gt; Right.
[49:50] &gt;&gt; Right.
[49:50] &gt;&gt; Right. &gt;&gt; Right. And let this do it for you.
[49:53] &gt;&gt; Right. And let this do it for you.
[49:53] &gt;&gt; Right. And let this do it for you. &gt;&gt; Do you like Google Cloud? Is that your
[49:54] &gt;&gt; Do you like Google Cloud? Is that your
[49:54] &gt;&gt; Do you like Google Cloud? Is that your &gt;&gt; I like Google run of choice Google run
[49:57] &gt;&gt; I like Google run of choice Google run
[49:57] &gt;&gt; I like Google run of choice Google run because you can take your git repo and
[49:59] because you can take your git repo and
[49:59] because you can take your git repo and Google run will like build your code for
[50:02] Google run will like build your code for
[50:02] Google run will like build your code for you and put it up on the web. I also
[50:04] you and put it up on the web. I also
[50:04] you and put it up on the web. I also found it very inexpensive 7 to 15 cents
[50:07] found it very inexpensive 7 to 15 cents
[50:07] found it very inexpensive 7 to 15 cents to host a simple website a day kind of
[50:09] to host a simple website a day kind of
[50:09] to host a simple website a day kind of thing.
[50:09] thing.
[50:09] thing. &gt;&gt; Not bad.
[50:10] &gt;&gt; Not bad.
[50:10] &gt;&gt; Not bad. &gt;&gt; It's not bad.
[50:10] &gt;&gt; It's not bad.
[50:10] &gt;&gt; It's not bad. &gt;&gt; Have you heard of like fly IO? Like
[50:12] &gt;&gt; Have you heard of like fly IO? Like
[50:12] &gt;&gt; Have you heard of like fly IO? Like there's these other services that I
[50:14] there's these other services that I
[50:14] there's these other services that I think you can deploy things in.
[50:15] think you can deploy things in.
[50:15] think you can deploy things in. &gt;&gt; Right. Right.
[50:16] &gt;&gt; Right. Right.
[50:16] &gt;&gt; Right. Right. &gt;&gt; I have a hard time. Yeah. Like which I
[50:19] &gt;&gt; I have a hard time. Yeah. Like which I
[50:19] &gt;&gt; I have a hard time. Yeah. Like which I asked the LLM like where should I host
[50:20] asked the LLM like where should I host
[50:20] asked the LLM like where should I host this thing and it's like oh for reasons
[50:22] this thing and it's like oh for reasons
[50:22] this thing and it's like oh for reasons and fly.io And it's a Python native
[50:23] and fly.io And it's a Python native
[50:24] and fly.io And it's a Python native that's like containerized. So this is I
[50:26] that's like containerized. So this is I
[50:26] that's like containerized. So this is I don't So that's probably what I'll do,
[50:28] don't So that's probably what I'll do,
[50:28] don't So that's probably what I'll do, but I I know that people like I mean
[50:30] but I I know that people like I mean
[50:30] but I I know that people like I mean there's so many clouds you could put it
[50:32] there's so many clouds you could put it
[50:32] there's so many clouds you could put it in.
[50:32] in.
[50:32] in. &gt;&gt; Yeah, I I'm just comfortable with the
[50:35] &gt;&gt; Yeah, I I'm just comfortable with the
[50:35] &gt;&gt; Yeah, I I'm just comfortable with the Google the Google ecosystem and Google
[50:37] Google the Google ecosystem and Google
[50:37] Google the Google ecosystem and Google run was fun. I wanted to try it. I have
[50:39] run was fun. I wanted to try it. I have
[50:39] run was fun. I wanted to try it. I have a chess game hosted up on Google Run.
[50:42] a chess game hosted up on Google Run.
[50:42] a chess game hosted up on Google Run. Okay, come on. Let's finish these tests
[50:43] Okay, come on. Let's finish these tests
[50:43] Okay, come on. Let's finish these tests and let's give us our game. It's got to
[50:45] and let's give us our game. It's got to
[50:45] and let's give us our game. It's got to be there.
[50:45] be there.
[50:45] be there. &gt;&gt; So Google run's the name of the product.
[50:47] &gt;&gt; So Google run's the name of the product.
[50:47] &gt;&gt; So Google run's the name of the product. &gt;&gt; Yeah, the cloud product thing. Yeah,
[50:49] &gt;&gt; Yeah, the cloud product thing. Yeah,
[50:49] &gt;&gt; Yeah, the cloud product thing. Yeah, engine. Okay, check it out. Engine at
[50:51] engine. Okay, check it out. Engine at
[50:51] engine. Okay, check it out. Engine at 100. So, let's do yes and don't ask. But
[50:54] 100. So, let's do yes and don't ask. But
[50:54] 100. So, let's do yes and don't ask. But if you scrolled up, I thought it said
[50:56] if you scrolled up, I thought it said
[50:56] if you scrolled up, I thought it said something about 100% complete. Engine at
[50:59] something about 100% complete. Engine at
[50:59] something about 100% complete. Engine at 100% coverage. 51 tests. 51
[51:03] 100% coverage. 51 tests. 51
[51:04] 100% coverage. 51 tests. 51 tests are green. Type check clean.
[51:07] tests are green. Type check clean.
[51:07] tests are green. Type check clean. Foundation 2 is complete. Phases one and
[51:09] Foundation 2 is complete. Phases one and
[51:09] Foundation 2 is complete. Phases one and two are done. I'm going to commit this.
[51:11] two are done. I'm going to commit this.
[51:11] two are done. I'm going to commit this. And now we're on to the last phase. So,
[51:14] And now we're on to the last phase. So,
[51:14] And now we're on to the last phase. So, yes. And again, we included the testing
[51:17] yes. And again, we included the testing
[51:17] yes. And again, we included the testing as part of this. We could have skipped
[51:18] as part of this. We could have skipped
[51:18] as part of this. We could have skipped all these tests and just jumped right to
[51:20] all these tests and just jumped right to
[51:20] all these tests and just jumped right to let me see the game and let me try the
[51:21] let me see the game and let me try the
[51:22] let me see the game and let me try the game. I didn't realize it would take
[51:23] game. I didn't realize it would take
[51:23] game. I didn't realize it would take this extra couple minutes, but we're
[51:25] this extra couple minutes, but we're
[51:25] this extra couple minutes, but we're we're almost there everyone. All gates
[51:27] we're almost there everyone. All gates
[51:27] we're almost there everyone. All gates are green after formatting. Yes. Okay.
[51:29] are green after formatting. Yes. Okay.
[51:30] are green after formatting. Yes. Okay. So, now it's going to commit the game.
[51:31] So, now it's going to commit the game.
[51:31] So, now it's going to commit the game. Check it out. So, go down. Yes. And
[51:33] Check it out. So, go down. Yes. And
[51:33] Check it out. So, go down. Yes. And commit.
[51:34] commit.
[51:34] commit. &gt;&gt; Isn't it funny that we're apologizing
[51:35] &gt;&gt; Isn't it funny that we're apologizing
[51:35] &gt;&gt; Isn't it funny that we're apologizing that it took an hour to do like a year's
[51:37] that it took an hour to do like a year's
[51:37] that it took an hour to do like a year's worth of work?
[51:38] worth of work?
[51:38] worth of work? &gt;&gt; I know. I know, right? I know. And that
[51:40] &gt;&gt; I know. I know, right? I know. And that
[51:40] &gt;&gt; I know. I know, right? I know. And that we've brought thousands of people who
[51:42] we've brought thousands of people who
[51:42] we've brought thousands of people who are going to watch this into the new
[51:44] are going to watch this into the new
[51:44] are going to watch this into the new &gt;&gt; guys. This would have taken two years
[51:45] &gt;&gt; guys. This would have taken two years
[51:45] &gt;&gt; guys. This would have taken two years before. I'm sorry it took an hour.
[51:47] before. I'm sorry it took an hour.
[51:47] before. I'm sorry it took an hour. &gt;&gt; I know. I know. I know. So, that's
[51:49] &gt;&gt; I know. I know. I know. So, that's
[51:50] &gt;&gt; I know. I know. I know. So, that's funny. So, all the code's been pushed
[51:52] funny. So, all the code's been pushed
[51:52] funny. So, all the code's been pushed and now we're just waiting for the
[51:54] and now we're just waiting for the
[51:54] and now we're just waiting for the instructions on how to play the game.
[51:55] instructions on how to play the game.
[51:56] instructions on how to play the game. Did it make a read me? Can we scroll
[51:57] Did it make a read me? Can we scroll
[51:58] Did it make a read me? Can we scroll down here on the folders on the side?
[51:59] down here on the folders on the side?
[52:00] down here on the folders on the side? Okay. Not yet. All right. We may have
[52:01] Okay. Not yet. All right. We may have
[52:01] Okay. Not yet. All right. We may have &gt;&gt; How do you know it was pushed? Is that
[52:02] &gt;&gt; How do you know it was pushed? Is that
[52:02] &gt;&gt; How do you know it was pushed? Is that what this is?
[52:03] what this is?
[52:03] what this is? &gt;&gt; Yeah. All the files are gone. So, that
[52:05] &gt;&gt; Yeah. All the files are gone. So, that
[52:05] &gt;&gt; Yeah. All the files are gone. So, that means they've all been pushed up to uh
[52:06] means they've all been pushed up to uh
[52:06] means they've all been pushed up to uh Got
[52:07] Got
[52:07] Got &gt;&gt; I think you maybe you need to click that
[52:09] &gt;&gt; I think you maybe you need to click that
[52:09] &gt;&gt; I think you maybe you need to click that up arrow and that'll push it up to your
[52:11] up arrow and that'll push it up to your
[52:11] up arrow and that'll push it up to your GitHub.
[52:12] GitHub.
[52:12] GitHub. &gt;&gt; Yeah, there you go. Yeah. allow lapper
[52:14] &gt;&gt; Yeah, there you go. Yeah. allow lapper
[52:14] &gt;&gt; Yeah, there you go. Yeah. allow lapper 13 failed to authenticate.
[52:17] 13 failed to authenticate.
[52:17] 13 failed to authenticate. Weird.
[52:18] Weird.
[52:18] Weird. &gt;&gt; I got the whole 2FA thing. Is that like
[52:20] &gt;&gt; I got the whole 2FA thing. Is that like
[52:20] &gt;&gt; I got the whole 2FA thing. Is that like a
[52:21] a
[52:21] a &gt;&gt; uh we can we can deal with that. We'll
[52:23] &gt;&gt; uh we can we can deal with that. We'll
[52:23] &gt;&gt; uh we can we can deal with that. We'll commit to getting this up on GitHub by
[52:24] commit to getting this up on GitHub by
[52:24] commit to getting this up on GitHub by the end of the session. Everyone, so
[52:26] the end of the session. Everyone, so
[52:26] the end of the session. Everyone, so what is it doing here?
[52:27] what is it doing here?
[52:27] what is it doing here? &gt;&gt; It's accomplishing.
[52:29] &gt;&gt; It's accomplishing.
[52:29] &gt;&gt; It's accomplishing. &gt;&gt; All gates green. Now on to phase three.
[52:31] &gt;&gt; All gates green. Now on to phase three.
[52:32] &gt;&gt; All gates green. Now on to phase three. So phase three is the last phase. We're
[52:33] So phase three is the last phase. We're
[52:33] So phase three is the last phase. We're very close. Everyone, do you want to
[52:35] very close. Everyone, do you want to
[52:35] very close. Everyone, do you want to scroll up a little bit? Let's just read
[52:36] scroll up a little bit? Let's just read
[52:36] scroll up a little bit? Let's just read what it said it's going to do here.
[52:37] what it said it's going to do here.
[52:37] what it said it's going to do here. First, I'll refactor the engine's answer
[52:39] First, I'll refactor the engine's answer
[52:39] First, I'll refactor the engine's answer normalization into the shared and then
[52:41] normalization into the shared and then
[52:41] normalization into the shared and then build generational grading content
[52:43] build generational grading content
[52:43] build generational grading content session and the user interface, the UI.
[52:46] session and the user interface, the UI.
[52:46] session and the user interface, the UI. So, okay, if we scroll all the way to
[52:48] So, okay, if we scroll all the way to
[52:48] So, okay, if we scroll all the way to the bottom, now it's the US1 tests
[52:52] the bottom, now it's the US1 tests
[52:52] the bottom, now it's the US1 tests written first, starting with the
[52:54] written first, starting with the
[52:54] written first, starting with the generational grading tests. So, a bunch
[52:56] generational grading tests. So, a bunch
[52:56] generational grading tests. So, a bunch of more testing. We're getting really,
[52:58] of more testing. We're getting really,
[52:58] of more testing. We're getting really, really close. I'm really excited to see
[52:59] really close. I'm really excited to see
[53:00] really close. I'm really excited to see what this video game is going to look
[53:01] what this video game is going to look
[53:01] what this video game is going to look like and uh how it can help people.
[53:03] like and uh how it can help people.
[53:04] like and uh how it can help people. Okay, engine generation and grading is
[53:06] Okay, engine generation and grading is
[53:06] Okay, engine generation and grading is green. Now, let's do the game layer and
[53:10] green. Now, let's do the game layer and
[53:10] green. Now, let's do the game layer and the game controller. So, we're really
[53:12] the game controller. So, we're really
[53:12] the game controller. So, we're really close. I know this is taking 20 minutes
[53:14] close. I know this is taking 20 minutes
[53:14] close. I know this is taking 20 minutes instead of 10.
[53:15] instead of 10.
[53:15] instead of 10. &gt;&gt; I'm good, man. Now that
[53:16] &gt;&gt; I'm good, man. Now that
[53:16] &gt;&gt; I'm good, man. Now that &gt;&gt; So, honestly, when I'm doing this, I'm
[53:18] &gt;&gt; So, honestly, when I'm doing this, I'm
[53:18] &gt;&gt; So, honestly, when I'm doing this, I'm like, enter, go get a coffee, enter, alt
[53:21] like, enter, go get a coffee, enter, alt
[53:21] like, enter, go get a coffee, enter, alt tab over to my email, enter, do some
[53:23] tab over to my email, enter, do some
[53:23] tab over to my email, enter, do some doom scrolling or whatever. Right?
[53:25] doom scrolling or whatever. Right?
[53:25] doom scrolling or whatever. Right? &gt;&gt; This is not typically how it's done
[53:27] &gt;&gt; This is not typically how it's done
[53:27] &gt;&gt; This is not typically how it's done where you sit and stare at the thing.
[53:29] where you sit and stare at the thing.
[53:29] where you sit and stare at the thing. Right? So, I'm thinking of my son, too.
[53:31] Right? So, I'm thinking of my son, too.
[53:31] Right? So, I'm thinking of my son, too. When I I know that he has less patience
[53:33] When I I know that he has less patience
[53:33] When I I know that he has less patience than I do,
[53:34] than I do,
[53:34] than I do, &gt;&gt; right,
[53:35] &gt;&gt; right,
[53:35] &gt;&gt; right, &gt;&gt; at his age. So, I'll probably talk to
[53:37] &gt;&gt; at his age. So, I'll probably talk to
[53:37] &gt;&gt; at his age. So, I'll probably talk to him and say, "Hey, what would you know,
[53:38] him and say, "Hey, what would you know,
[53:38] him and say, "Hey, what would you know, do you want to make a game?"
[53:40] do you want to make a game?"
[53:40] do you want to make a game?" &gt;&gt; Yeah.
[53:40] &gt;&gt; Yeah.
[53:40] &gt;&gt; Yeah. &gt;&gt; I'll work on like the spec stuff with
[53:42] &gt;&gt; I'll work on like the spec stuff with
[53:42] &gt;&gt; I'll work on like the spec stuff with him like, "Oh, what do you want to do?
[53:43] him like, "Oh, what do you want to do?
[53:44] him like, "Oh, what do you want to do? What do you think?" Blah, blah, blah.
[53:45] What do you think?" Blah, blah, blah.
[53:45] What do you think?" Blah, blah, blah. And then I can go through this for him.
[53:47] And then I can go through this for him.
[53:47] And then I can go through this for him. &gt;&gt; I'll show him like, "Oh, look, a lot of
[53:49] &gt;&gt; I'll show him like, "Oh, look, a lot of
[53:49] &gt;&gt; I'll show him like, "Oh, look, a lot of work happened,
[53:50] work happened,
[53:50] work happened, &gt;&gt; right?
[53:50] &gt;&gt; right?
[53:50] &gt;&gt; right? &gt;&gt; It was an hour and I didn't want you to
[53:52] &gt;&gt; It was an hour and I didn't want you to
[53:52] &gt;&gt; It was an hour and I didn't want you to have to sit here and cuz he doesn't have
[53:53] have to sit here and cuz he doesn't have
[53:53] have to sit here and cuz he doesn't have that kind of patience right now,
[53:55] that kind of patience right now,
[53:55] that kind of patience right now, &gt;&gt; right?"
[53:55] &gt;&gt; right?"
[53:55] &gt;&gt; right?" &gt;&gt; But he can see like, "Oh, we created
[53:57] &gt;&gt; But he can see like, "Oh, we created
[53:57] &gt;&gt; But he can see like, "Oh, we created something." Yeah. with a tool that did a
[54:00] something." Yeah. with a tool that did a
[54:00] something." Yeah. with a tool that did a thing,
[54:01] thing,
[54:01] thing, &gt;&gt; which is pretty amazing.
[54:02] &gt;&gt; which is pretty amazing.
[54:02] &gt;&gt; which is pretty amazing. &gt;&gt; And if he gets excited, maybe he would
[54:04] &gt;&gt; And if he gets excited, maybe he would
[54:04] &gt;&gt; And if he gets excited, maybe he would want to sit in for 5 minutes of the
[54:05] want to sit in for 5 minutes of the
[54:05] want to sit in for 5 minutes of the process next time like, "Oh, you could
[54:07] process next time like, "Oh, you could
[54:07] process next time like, "Oh, you could do this, buddy. If if you're into this,
[54:09] do this, buddy. If if you're into this,
[54:09] do this, buddy. If if you're into this, if you're not, cool."
[54:10] if you're not, cool."
[54:10] if you're not, cool." &gt;&gt; Now, the other neat thing that you can
[54:11] &gt;&gt; Now, the other neat thing that you can
[54:11] &gt;&gt; Now, the other neat thing that you can do with this, particularly for video
[54:13] do with this, particularly for video
[54:13] do with this, particularly for video games, is um tie in the image generation
[54:16] games, is um tie in the image generation
[54:16] games, is um tie in the image generation feature
[54:17] feature
[54:17] feature &gt;&gt; like from OpenAI or Gemini or whatever
[54:19] &gt;&gt; like from OpenAI or Gemini or whatever
[54:19] &gt;&gt; like from OpenAI or Gemini or whatever who can make images, AI images.
[54:21] who can make images, AI images.
[54:21] who can make images, AI images. &gt;&gt; Yeah.
[54:22] &gt;&gt; Yeah.
[54:22] &gt;&gt; Yeah. &gt;&gt; And tell it to use that tool to generate
[54:24] &gt;&gt; And tell it to use that tool to generate
[54:24] &gt;&gt; And tell it to use that tool to generate the assets for the video game. So this
[54:27] the assets for the video game. So this
[54:27] the assets for the video game. So this video is going to look pretty,
[54:30] video is going to look pretty,
[54:30] video is going to look pretty, &gt;&gt; but you could like use AI to generate
[54:32] &gt;&gt; but you could like use AI to generate
[54:32] &gt;&gt; but you could like use AI to generate the actual assets for the game.
[54:34] the actual assets for the game.
[54:34] the actual assets for the game. &gt;&gt; So could we have incorporated that into
[54:36] &gt;&gt; So could we have incorporated that into
[54:36] &gt;&gt; So could we have incorporated that into our spec?
[54:38] our spec?
[54:38] our spec? &gt;&gt; Yeah. So even or another spec is to say,
[54:40] &gt;&gt; Yeah. So even or another spec is to say,
[54:40] &gt;&gt; Yeah. So even or another spec is to say, okay, the base game is great. Let's
[54:43] okay, the base game is great. Let's
[54:43] okay, the base game is great. Let's reskin it with OpenAI generated assets
[54:46] reskin it with OpenAI generated assets
[54:46] reskin it with OpenAI generated assets or something, right? Go through the
[54:48] or something, right? Go through the
[54:48] or something, right? Go through the whole process own
[54:49] whole process own
[54:50] whole process own &gt;&gt; I don't quad can't generate images.
[54:52] &gt;&gt; I don't quad can't generate images.
[54:52] &gt;&gt; I don't quad can't generate images. They're they they've really focused on
[54:54] They're they they've really focused on
[54:54] They're they they've really focused on coding,
[54:55] coding,
[54:55] coding, &gt;&gt; which I think is why they're doing so
[54:56] &gt;&gt; which I think is why they're doing so
[54:56] &gt;&gt; which I think is why they're doing so well is cuz they didn't go as wide,
[54:58] well is cuz they didn't go as wide,
[54:58] well is cuz they didn't go as wide, right?
[54:59] right?
[54:59] right? &gt;&gt; Yeah.
[54:59] &gt;&gt; Yeah.
[54:59] &gt;&gt; Yeah. &gt;&gt; Open AAI tried to be everything for
[55:01] &gt;&gt; Open AAI tried to be everything for
[55:01] &gt;&gt; Open AAI tried to be everything for everyone and they had Sora and a few
[55:03] everyone and they had Sora and a few
[55:03] everyone and they had Sora and a few other things. And
[55:04] other things. And
[55:04] other things. And &gt;&gt; I'm still paying for it. It was my
[55:06] &gt;&gt; I'm still paying for it. It was my
[55:06] &gt;&gt; I'm still paying for it. It was my first. I still have it.
[55:07] first. I still have it.
[55:07] first. I still have it. &gt;&gt; I know. I have it, too.
[55:08] &gt;&gt; I know. I have it, too.
[55:08] &gt;&gt; I know. I have it, too. &gt;&gt; I think I could probably cancel and
[55:09] &gt;&gt; I think I could probably cancel and
[55:09] &gt;&gt; I think I could probably cancel and still get what I need out of it.
[55:10] still get what I need out of it.
[55:10] still get what I need out of it. &gt;&gt; Yeah. I sort of bounce like I still use
[55:12] &gt;&gt; Yeah. I sort of bounce like I still use
[55:12] &gt;&gt; Yeah. I sort of bounce like I still use it.
[55:13] it.
[55:13] it. &gt;&gt; I do, too. But I almost wonder if the
[55:15] &gt;&gt; I do, too. But I almost wonder if the
[55:15] &gt;&gt; I do, too. But I almost wonder if the free tier would get me by, but I just
[55:17] free tier would get me by, but I just
[55:17] free tier would get me by, but I just feel like it was my first.
[55:19] feel like it was my first.
[55:19] feel like it was my first. &gt;&gt; I know. I know. I feel like, ah, let me,
[55:22] &gt;&gt; I know. I know. I feel like, ah, let me,
[55:22] &gt;&gt; I know. I know. I feel like, ah, let me, you know, I'm using it. Let me pay in.
[55:23] you know, I'm using it. Let me pay in.
[55:23] you know, I'm using it. Let me pay in. &gt;&gt; It's kind of like after you get Disney
[55:25] &gt;&gt; It's kind of like after you get Disney
[55:25] &gt;&gt; It's kind of like after you get Disney Plus and Amazon Prime that you keep
[55:27] Plus and Amazon Prime that you keep
[55:27] Plus and Amazon Prime that you keep Netflix around, right?
[55:28] Netflix around, right?
[55:28] Netflix around, right? &gt;&gt; Right. Exactly. Why do I have Netflix? I
[55:31] &gt;&gt; Right. Exactly. Why do I have Netflix? I
[55:31] &gt;&gt; Right. Exactly. Why do I have Netflix? I don't know. I think my in-laws use it,
[55:33] don't know. I think my in-laws use it,
[55:33] don't know. I think my in-laws use it, but I've always had it.
[55:34] but I've always had it.
[55:34] but I've always had it. &gt;&gt; Right. Right. Right. Okay. Now, let's
[55:36] &gt;&gt; Right. Right. Right. Okay. Now, let's
[55:36] &gt;&gt; Right. Right. Right. Okay. Now, let's run the full test end to end. Wrong test
[55:39] run the full test end to end. Wrong test
[55:40] run the full test end to end. Wrong test answer submitted. Okay. So, it's it's
[55:42] answer submitted. Okay. So, it's it's
[55:42] answer submitted. Okay. So, it's it's still fixing some subnetting.
[55:44] still fixing some subnetting.
[55:44] still fixing some subnetting. &gt;&gt; I'm fascinated by the testing aspect. I
[55:47] &gt;&gt; I'm fascinated by the testing aspect. I
[55:47] &gt;&gt; I'm fascinated by the testing aspect. I probably will never understand what's
[55:49] probably will never understand what's
[55:49] probably will never understand what's happening because coding is just so out
[55:53] happening because coding is just so out
[55:53] happening because coding is just so out of my wheelhouse. Like I don't
[55:55] of my wheelhouse. Like I don't
[55:55] of my wheelhouse. Like I don't understand code, let alone what testing.
[55:57] understand code, let alone what testing.
[55:57] understand code, let alone what testing. &gt;&gt; The more you see it, the more you're
[55:59] &gt;&gt; The more you see it, the more you're
[55:59] &gt;&gt; The more you see it, the more you're exposed to it, I think it'll, you know,
[56:00] exposed to it, I think it'll, you know,
[56:00] exposed to it, I think it'll, you know, like
[56:01] like
[56:01] like &gt;&gt; what's it testing? Is it syntax? Like
[56:04] &gt;&gt; what's it testing? Is it syntax? Like
[56:04] &gt;&gt; what's it testing? Is it syntax? Like again, like I have questions that can't
[56:05] again, like I have questions that can't
[56:05] again, like I have questions that can't be answered simply. Right.
[56:06] be answered simply. Right.
[56:06] be answered simply. Right. &gt;&gt; Right. Right.
[56:07] &gt;&gt; Right. Right.
[56:07] &gt;&gt; Right. Right. &gt;&gt; It's testing a lot of things, Andy. And
[56:09] &gt;&gt; It's testing a lot of things, Andy. And
[56:09] &gt;&gt; It's testing a lot of things, Andy. And you don't understand.
[56:10] you don't understand.
[56:10] you don't understand. &gt;&gt; All 77 tests are green.
[56:13] &gt;&gt; All 77 tests are green.
[56:14] &gt;&gt; All 77 tests are green. engine 100% overall type and lint. Okay,
[56:18] engine 100% overall type and lint. Okay,
[56:18] engine 100% overall type and lint. Okay, so I believe the game has been fully
[56:19] so I believe the game has been fully
[56:20] so I believe the game has been fully tested. Press enter again.
[56:22] tested. Press enter again.
[56:22] tested. Press enter again. &gt;&gt; But it said all tests were green
[56:23] &gt;&gt; But it said all tests were green
[56:23] &gt;&gt; But it said all tests were green earlier, like 50 something. So I wonder
[56:25] earlier, like 50 something. So I wonder
[56:25] earlier, like 50 something. So I wonder if it found something later.
[56:26] if it found something later.
[56:26] if it found something later. &gt;&gt; It's missed generate.js isn't fully. So
[56:29] &gt;&gt; It's missed generate.js isn't fully. So
[56:29] &gt;&gt; It's missed generate.js isn't fully. So it's looking for some gaps in the test
[56:31] it's looking for some gaps in the test
[56:31] it's looking for some gaps in the test coverage here,
[56:32] coverage here,
[56:32] coverage here, &gt;&gt; which I'm good with.
[56:33] &gt;&gt; which I'm good with.
[56:33] &gt;&gt; which I'm good with. &gt;&gt; I know. I'd love to know the game is
[56:35] &gt;&gt; I know. I'd love to know the game is
[56:35] &gt;&gt; I know. I'd love to know the game is 100% tested. You know, you know why? Cuz
[56:38] 100% tested. You know, you know why? Cuz
[56:38] 100% tested. You know, you know why? Cuz that kid
[56:39] that kid
[56:39] that kid &gt;&gt; Well, right. who does the subnet game
[56:41] &gt;&gt; Well, right. who does the subnet game
[56:41] &gt;&gt; Well, right. who does the subnet game and it tells them the wrong answer.
[56:43] and it tells them the wrong answer.
[56:43] and it tells them the wrong answer. That's on us.
[56:44] That's on us.
[56:44] That's on us. &gt;&gt; Yep.
[56:45] &gt;&gt; Yep.
[56:45] &gt;&gt; Yep. &gt;&gt; Do you know what I mean? It's not on the
[56:46] &gt;&gt; Do you know what I mean? It's not on the
[56:46] &gt;&gt; Do you know what I mean? It's not on the AI.
[56:47] AI.
[56:47] AI. &gt;&gt; Yeah.
[56:47] &gt;&gt; Yeah.
[56:47] &gt;&gt; Yeah. &gt;&gt; So, I love that it's fully tested. It's
[56:49] &gt;&gt; So, I love that it's fully tested. It's
[56:49] &gt;&gt; So, I love that it's fully tested. It's actually testing some answers and
[56:50] actually testing some answers and
[56:50] actually testing some answers and testing some scenarios before it just
[56:52] testing some scenarios before it just
[56:52] testing some scenarios before it just presents as a game that
[56:54] presents as a game that
[56:54] presents as a game that &gt;&gt; you know for education. You've got to be
[56:56] &gt;&gt; you know for education. You've got to be
[56:56] &gt;&gt; you know for education. You've got to be right.
[56:57] right.
[56:57] right. &gt;&gt; If you don't test or if something misses
[56:59] &gt;&gt; If you don't test or if something misses
[56:59] &gt;&gt; If you don't test or if something misses like is is that how bugs get out?
[57:01] like is is that how bugs get out?
[57:01] like is is that how bugs get out? &gt;&gt; Bugs get out. Memory leaks things crash.
[57:04] &gt;&gt; Bugs get out. Memory leaks things crash.
[57:04] &gt;&gt; Bugs get out. Memory leaks things crash. &gt;&gt; Security vulnerabilities. There's all
[57:06] &gt;&gt; Security vulnerabilities. There's all
[57:06] &gt;&gt; Security vulnerabilities. There's all kinds of stuff that could happen with
[57:07] kinds of stuff that could happen with
[57:07] kinds of stuff that could happen with untested code, right? really stringent
[57:09] untested code, right? really stringent
[57:09] untested code, right? really stringent testing should
[57:11] testing should
[57:11] testing should &gt;&gt; limit and eliminate those bugs and those
[57:13] &gt;&gt; limit and eliminate those bugs and those
[57:13] &gt;&gt; limit and eliminate those bugs and those gaps. Yeah, exactly.
[57:15] gaps. Yeah, exactly.
[57:15] gaps. Yeah, exactly. &gt;&gt; Which is more reliable software. It'll
[57:17] &gt;&gt; Which is more reliable software. It'll
[57:17] &gt;&gt; Which is more reliable software. It'll break less often, do weird stuff
[57:19] break less often, do weird stuff
[57:19] break less often, do weird stuff &gt;&gt; and also makes this whole approach more
[57:22] &gt;&gt; and also makes this whole approach more
[57:22] &gt;&gt; and also makes this whole approach more adoptable and more like popular because
[57:26] adoptable and more like popular because
[57:26] adoptable and more like popular because &gt;&gt; it's not like I don't know vibe coding
[57:28] &gt;&gt; it's not like I don't know vibe coding
[57:28] &gt;&gt; it's not like I don't know vibe coding can get it wrong and it's not testing
[57:30] can get it wrong and it's not testing
[57:30] can get it wrong and it's not testing and it's this is a little more formal,
[57:32] and it's this is a little more formal,
[57:32] and it's this is a little more formal, right? And I've always thought if it's
[57:33] right? And I've always thought if it's
[57:33] right? And I've always thought if it's good enough for Microsoft, [laughter]
[57:36] good enough for Microsoft, [laughter]
[57:36] good enough for Microsoft, [laughter] right? Like if it's good if this process
[57:38] right? Like if it's good if this process
[57:38] right? Like if it's good if this process is good enough for Microsoft and GitHub,
[57:40] is good enough for Microsoft and GitHub,
[57:40] is good enough for Microsoft and GitHub, I think it's good enough for me to make
[57:41] I think it's good enough for me to make
[57:41] I think it's good enough for me to make a little, you know, subnet video.
[57:43] a little, you know, subnet video.
[57:43] a little, you know, subnet video. &gt;&gt; I was going to ask you why do you say
[57:44] &gt;&gt; I was going to ask you why do you say
[57:44] &gt;&gt; I was going to ask you why do you say that? But it's cuz GitHub is are they
[57:47] that? But it's cuz GitHub is are they
[57:47] that? But it's cuz GitHub is are they owned?
[57:47] owned?
[57:47] owned? &gt;&gt; Yeah, Microsoft's own g owns GitHub now.
[57:50] &gt;&gt; Yeah, Microsoft's own g owns GitHub now.
[57:50] &gt;&gt; Yeah, Microsoft's own g owns GitHub now. But I'm just, you know,
[57:51] But I'm just, you know,
[57:51] But I'm just, you know, &gt;&gt; this testing suite part of Microsoft.
[57:54] &gt;&gt; this testing suite part of Microsoft.
[57:54] &gt;&gt; this testing suite part of Microsoft. &gt;&gt; Um, more at the Python level or
[57:57] &gt;&gt; Um, more at the Python level or
[57:57] &gt;&gt; Um, more at the Python level or JavaScript level. So, four gaps
[58:00] JavaScript level. So, four gaps
[58:00] JavaScript level. So, four gaps remaining. You know what we could do,
[58:01] remaining. You know what we could do,
[58:02] remaining. You know what we could do, Andy? The next time we get a chance,
[58:03] Andy? The next time we get a chance,
[58:04] Andy? The next time we get a chance, actually, type it in right now. ask it.
[58:06] actually, type it in right now. ask it.
[58:06] actually, type it in right now. ask it. Am I able just to to play the game to
[58:08] Am I able just to to play the game to
[58:08] Am I able just to to play the game to test it and see it? Cuz this testing
[58:10] test it and see it? Cuz this testing
[58:10] test it and see it? Cuz this testing might go on for another 20 minutes and I
[58:12] might go on for another 20 minutes and I
[58:12] might go on for another 20 minutes and I don't want to keep us all here for that
[58:13] don't want to keep us all here for that
[58:13] don't want to keep us all here for that long. I know you've had a really long
[58:14] long. I know you've had a really long
[58:14] long. I know you've had a really long day and this episode's building up to a
[58:17] day and this episode's building up to a
[58:17] day and this episode's building up to a climax and I want to get there and and
[58:19] climax and I want to get there and and
[58:19] climax and I want to get there and and now it should intercept this. I'll
[58:21] now it should intercept this. I'll
[58:21] now it should intercept this. I'll finish the last coverage fixes, then get
[58:23] finish the last coverage fixes, then get
[58:23] finish the last coverage fixes, then get your game running in a browser. Okay,
[58:25] your game running in a browser. Okay,
[58:25] your game running in a browser. Okay, even it's like Okay, I'm getting there.
[58:28] even it's like Okay, I'm getting there.
[58:28] even it's like Okay, I'm getting there. I'm getting there.
[58:30] I'm getting there.
[58:30] I'm getting there. &gt;&gt; Don't rush me, bro.
[58:31] &gt;&gt; Don't rush me, bro.
[58:31] &gt;&gt; Don't rush me, bro. &gt;&gt; Don't rush me, bro. Okay, it's really
[58:33] &gt;&gt; Don't rush me, bro. Okay, it's really
[58:33] &gt;&gt; Don't rush me, bro. Okay, it's really like going to fix those last couple
[58:35] like going to fix those last couple
[58:35] like going to fix those last couple things. It didn't care that I wanted to
[58:36] things. It didn't care that I wanted to
[58:36] things. It didn't care that I wanted to just play the game. [laughter]
[58:39] just play the game. [laughter]
[58:39] just play the game. [laughter] &gt;&gt; Yeah. Press enter one more time.
[58:41] &gt;&gt; Yeah. Press enter one more time.
[58:42] &gt;&gt; Yeah. Press enter one more time. &gt;&gt; I mean, this isn't bothering me. I'm
[58:43] &gt;&gt; I mean, this isn't bothering me. I'm
[58:43] &gt;&gt; I mean, this isn't bothering me. I'm &gt;&gt; You know what's funny? Look at the
[58:44] &gt;&gt; You know what's funny? Look at the
[58:44] &gt;&gt; You know what's funny? Look at the syntax of this like command to run.
[58:48] syntax of this like command to run.
[58:48] syntax of this like command to run. &gt;&gt; Like that syntax. Just learning how to
[58:50] &gt;&gt; Like that syntax. Just learning how to
[58:50] &gt;&gt; Like that syntax. Just learning how to do that as a testing is like weeks of
[58:53] do that as a testing is like weeks of
[58:53] do that as a testing is like weeks of reading testing books and
[58:55] reading testing books and
[58:55] reading testing books and &gt;&gt; gosh software.
[58:56] &gt;&gt; gosh software.
[58:56] &gt;&gt; gosh software. &gt;&gt; And there's people understand that and
[58:59] &gt;&gt; And there's people understand that and
[58:59] &gt;&gt; And there's people understand that and right like
[59:00] right like
[59:00] right like &gt;&gt; coverage is at 100%. There's one real
[59:02] &gt;&gt; coverage is at 100%. There's one real
[59:02] &gt;&gt; coverage is at 100%. There's one real source error to fix, too. It's really
[59:05] source error to fix, too. It's really
[59:05] source error to fix, too. It's really obsessed with fixing the test. Like,
[59:07] obsessed with fixing the test. Like,
[59:07] obsessed with fixing the test. Like, it's really wants to give us a good game
[59:08] it's really wants to give us a good game
[59:08] it's really wants to give us a good game here.
[59:09] here.
[59:09] here. &gt;&gt; Hey, let me know if you want me to stop
[59:11] &gt;&gt; Hey, let me know if you want me to stop
[59:11] &gt;&gt; Hey, let me know if you want me to stop pressing.
[59:12] pressing.
[59:12] pressing. &gt;&gt; No, I want you to press yes.
[59:13] &gt;&gt; No, I want you to press yes.
[59:13] &gt;&gt; No, I want you to press yes. &gt;&gt; No, I would be like, yes, yes, yes, yes,
[59:15] &gt;&gt; No, I would be like, yes, yes, yes, yes,
[59:15] &gt;&gt; No, I would be like, yes, yes, yes, yes, yes. So, 25 minutes of implement and
[59:18] yes. So, 25 minutes of implement and
[59:18] yes. So, 25 minutes of implement and probably 20 minutes of the three other
[59:19] probably 20 minutes of the three other
[59:19] probably 20 minutes of the three other or four five other phases together
[59:22] or four five other phases together
[59:22] or four five other phases together coming up on probably an hour, right?
[59:24] coming up on probably an hour, right?
[59:24] coming up on probably an hour, right? It's about an hour we've been doing
[59:25] It's about an hour we've been doing
[59:25] It's about an hour we've been doing this.
[59:25] this.
[59:25] this. &gt;&gt; Yep.
[59:26] &gt;&gt; Yep.
[59:26] &gt;&gt; Yep. &gt;&gt; Okay, cool. Cool. Engine, it's 100%. Uh,
[59:29] &gt;&gt; Okay, cool. Cool. Engine, it's 100%. Uh,
[59:29] &gt;&gt; Okay, cool. Cool. Engine, it's 100%. Uh, there's three linting errors left. Let
[59:32] there's three linting errors left. Let
[59:32] there's three linting errors left. Let me fix them. Okay.
[59:34] me fix them. Okay.
[59:34] me fix them. Okay. &gt;&gt; What's an engine? Is that what makes the
[59:36] &gt;&gt; What's an engine? Is that what makes the
[59:36] &gt;&gt; What's an engine? Is that what makes the game work?
[59:36] game work?
[59:36] game work? &gt;&gt; It's like the core of the game engine.
[59:37] &gt;&gt; It's like the core of the game engine.
[59:38] &gt;&gt; It's like the core of the game engine. Yeah. Yeah.
[59:38] Yeah. Yeah.
[59:38] Yeah. Yeah. &gt;&gt; I don't know anything about gaming.
[59:39] &gt;&gt; I don't know anything about gaming.
[59:39] &gt;&gt; I don't know anything about gaming. &gt;&gt; I would love to have learned how to
[59:41] &gt;&gt; I would love to have learned how to
[59:41] &gt;&gt; I would love to have learned how to write code for video games, you know,
[59:43] write code for video games, you know,
[59:43] write code for video games, you know, when you talk here about like the Unreal
[59:45] when you talk here about like the Unreal
[59:45] when you talk here about like the Unreal Engine and some of these video game
[59:46] Engine and some of these video game
[59:46] Engine and some of these video game studios and stuff.
[59:47] studios and stuff.
[59:47] studios and stuff. &gt;&gt; So, is that just different languages,
[59:49] &gt;&gt; So, is that just different languages,
[59:49] &gt;&gt; So, is that just different languages, different
[59:50] different
[59:50] different &gt;&gt; Yeah. You know, different syntax.
[59:53] &gt;&gt; Yeah. You know, different syntax.
[59:53] &gt;&gt; Yeah. You know, different syntax. Were you a gamer? Are you a gamer?
[59:55] Were you a gamer? Are you a gamer?
[59:55] Were you a gamer? Are you a gamer? &gt;&gt; Not anymore.
[59:56] &gt;&gt; Not anymore.
[59:56] &gt;&gt; Not anymore. &gt;&gt; What did you play on? Like my son has an
[59:58] &gt;&gt; What did you play on? Like my son has an
[59:58] &gt;&gt; What did you play on? Like my son has an Xbox. He loves it.
[59:59] Xbox. He loves it.
[59:59] Xbox. He loves it. &gt;&gt; I've got a PS5. I'm waiting for the
[60:01] &gt;&gt; I've got a PS5. I'm waiting for the
[60:01] &gt;&gt; I've got a PS5. I'm waiting for the Wolverine game to come out. That looks
[60:02] Wolverine game to come out. That looks
[60:02] Wolverine game to come out. That looks pretty good.
[60:03] pretty good.
[60:03] pretty good. &gt;&gt; But you were like a PC gamer, right?
[60:04] &gt;&gt; But you were like a PC gamer, right?
[60:04] &gt;&gt; But you were like a PC gamer, right? That's
[60:05] That's
[60:05] That's &gt;&gt; play World of Warcraft and all that
[60:07] &gt;&gt; play World of Warcraft and all that
[60:07] &gt;&gt; play World of Warcraft and all that stuff. Yeah. Okay. Do the down arrow.
[60:09] stuff. Yeah. Okay. Do the down arrow.
[60:09] stuff. Yeah. Okay. Do the down arrow. Yes.
[60:10] Yes.
[60:10] Yes. &gt;&gt; It looks like it wants to launch the
[60:11] &gt;&gt; It looks like it wants to launch the
[60:11] &gt;&gt; It looks like it wants to launch the game here.
[60:12] game here.
[60:12] game here. &gt;&gt; Okay.
[60:12] &gt;&gt; Okay.
[60:12] &gt;&gt; Okay. &gt;&gt; Now, let me start a local server.
[60:13] &gt;&gt; Now, let me start a local server.
[60:14] &gt;&gt; Now, let me start a local server. &gt;&gt; So, that's running on my machine right
[60:15] &gt;&gt; So, that's running on my machine right
[60:15] &gt;&gt; So, that's running on my machine right &gt;&gt; here. Says what you'll see. So, go to
[60:17] &gt;&gt; here. Says what you'll see. So, go to
[60:17] &gt;&gt; here. Says what you'll see. So, go to local. Click. Can you click on that?
[60:18] local. Click. Can you click on that?
[60:18] local. Click. Can you click on that? Actually, open up a new browser and go
[60:20] Actually, open up a new browser and go
[60:20] Actually, open up a new browser and go to localhost 8000 or click on this link
[60:22] to localhost 8000 or click on this link
[60:22] to localhost 8000 or click on this link here. Drum roll, please.
[60:24] here. Drum roll, please.
[60:24] here. Drum roll, please. &gt;&gt; Oh my god. Is it going to happen? So you
[60:25] &gt;&gt; Oh my god. Is it going to happen? So you
[60:25] &gt;&gt; Oh my god. Is it going to happen? So you can drag this down.
[60:27] can drag this down.
[60:27] can drag this down. &gt;&gt; It's open it up in VS Code as a browser.
[60:30] &gt;&gt; It's open it up in VS Code as a browser.
[60:30] &gt;&gt; It's open it up in VS Code as a browser. Subnet trainer learn IPv4 one step at a
[60:32] Subnet trainer learn IPv4 one step at a
[60:32] Subnet trainer learn IPv4 one step at a time. Binary and decimal explains it.
[60:35] time. Binary and decimal explains it.
[60:35] time. Binary and decimal explains it. Stark practice. Uhoh. Uhoh. The two of
[60:39] Stark practice. Uhoh. Uhoh. The two of
[60:39] Stark practice. Uhoh. Uhoh. The two of us being tested. We can stop the
[60:41] us being tested. We can stop the
[60:41] us being tested. We can stop the recording now.
[60:42] recording now.
[60:42] recording now. &gt;&gt; 186 32 64. [laughter]
[60:45] &gt;&gt; 186 32 64. [laughter]
[60:45] &gt;&gt; 186 32 64. [laughter] Oh my god. I hate math. I'm going to
[60:47] Oh my god. I hate math. I'm going to
[60:47] Oh my god. I hate math. I'm going to &gt;&gt; So the last one. So 2 4 6 8
[60:50] &gt;&gt; So the last one. So 2 4 6 8
[60:50] &gt;&gt; So the last one. So 2 4 6 8 &gt;&gt; 56. I don't know.
[60:52] &gt;&gt; 56. I don't know.
[60:52] &gt;&gt; 56. I don't know. &gt;&gt; So it' be 64.
[60:54] &gt;&gt; So it' be 64.
[60:54] &gt;&gt; So it' be 64. &gt;&gt; [laughter]
[60:55] &gt;&gt; [laughter]
[60:55] &gt;&gt; [laughter] &gt;&gt; 32 32 and 16 and 8 and 1. So it should
[61:00] &gt;&gt; 32 32 and 16 and 8 and 1. So it should
[61:00] &gt;&gt; 32 32 and 16 and 8 and 1. So it should end in a nine. No. Am I wrong?
[61:02] end in a nine. No. Am I wrong?
[61:02] end in a nine. No. Am I wrong? &gt;&gt; I'm going to say 114.
[61:03] &gt;&gt; I'm going to say 114.
[61:03] &gt;&gt; I'm going to say 114. &gt;&gt; Okay, correct answer. So it's telling us
[61:05] &gt;&gt; Okay, correct answer. So it's telling us
[61:05] &gt;&gt; Okay, correct answer. So it's telling us not quite. And it explains it all. Next.
[61:08] not quite. And it explains it all. Next.
[61:08] not quite. And it explains it all. Next. So now look at a different way. Type the
[61:10] So now look at a different way. Type the
[61:10] So now look at a different way. Type the whole number. Okay. We we don't need to
[61:12] whole number. Okay. We we don't need to
[61:12] whole number. Okay. We we don't need to show everyone how bad we are at
[61:13] show everyone how bad we are at
[61:13] show everyone how bad we are at subnetting in our in our later ages.
[61:15] subnetting in our in our later ages.
[61:15] subnetting in our in our later ages. [laughter]
[61:16] [laughter]
[61:16] [laughter] But is this not cool? We've just built a
[61:19] But is this not cool? We've just built a
[61:19] But is this not cool? We've just built a fully functional subnet trainer free to
[61:22] fully functional subnet trainer free to
[61:22] fully functional subnet trainer free to the community. Anybody can do it. We
[61:24] the community. Anybody can do it. We
[61:24] the community. Anybody can do it. We didn't write a single line of code. Look
[61:26] didn't write a single line of code. Look
[61:26] didn't write a single line of code. Look at all the artifacts we have. We know
[61:28] at all the artifacts we have. We know
[61:28] at all the artifacts we have. We know it's fully tested. So, let's go ahead
[61:30] it's fully tested. So, let's go ahead
[61:30] it's fully tested. So, let's go ahead and commit these in here. Click on this.
[61:33] and commit these in here. Click on this.
[61:33] and commit these in here. Click on this. &gt;&gt; What's cool, John, is I never would have
[61:35] &gt;&gt; What's cool, John, is I never would have
[61:35] &gt;&gt; What's cool, John, is I never would have been able to do this.
[61:36] been able to do this.
[61:36] been able to do this. &gt;&gt; No, me neither. Me neither. I would not
[61:39] &gt;&gt; No, me neither. Me neither. I would not
[61:39] &gt;&gt; No, me neither. Me neither. I would not have been able to do this.
[61:40] have been able to do this.
[61:40] have been able to do this. &gt;&gt; There was a subnet game. It's on a
[61:42] &gt;&gt; There was a subnet game. It's on a
[61:42] &gt;&gt; There was a subnet game. It's on a website somewhere. Whatever that
[61:43] website somewhere. Whatever that
[61:43] website somewhere. Whatever that subnetting exercises whatever was that
[61:45] subnetting exercises whatever was that
[61:45] subnetting exercises whatever was that we used to use in CCNA.
[61:46] we used to use in CCNA.
[61:46] we used to use in CCNA. &gt;&gt; Yes.
[61:46] &gt;&gt; Yes.
[61:46] &gt;&gt; Yes. &gt;&gt; And I guess somebody made that without
[61:48] &gt;&gt; And I guess somebody made that without
[61:48] &gt;&gt; And I guess somebody made that without this. Took them forever and it's there.
[61:50] this. Took them forever and it's there.
[61:50] this. Took them forever and it's there. I'm amazed by this. Like, not to
[61:52] I'm amazed by this. Like, not to
[61:52] I'm amazed by this. Like, not to minimize like, oh, okay. it's over. Like
[61:54] minimize like, oh, okay. it's over. Like
[61:54] minimize like, oh, okay. it's over. Like look at the stuff like we just people
[61:56] look at the stuff like we just people
[61:56] look at the stuff like we just people could use this to learn subnetting.
[61:58] could use this to learn subnetting.
[61:58] could use this to learn subnetting. &gt;&gt; I know
[61:58] &gt;&gt; I know
[61:58] &gt;&gt; I know &gt;&gt; that's amazing. I know like
[62:00] &gt;&gt; that's amazing. I know like
[62:00] &gt;&gt; that's amazing. I know like &gt;&gt; and and and to your earlier point about
[62:02] &gt;&gt; and and and to your earlier point about
[62:02] &gt;&gt; and and and to your earlier point about the hello world, right? It's not a like
[62:05] the hello world, right? It's not a like
[62:05] the hello world, right? It's not a like it's an exciting me message to network
[62:07] it's an exciting me message to network
[62:07] it's an exciting me message to network engineers or people in general. I'm not
[62:11] engineers or people in general. I'm not
[62:11] engineers or people in general. I'm not trying to minimize learning code. I'm
[62:13] trying to minimize learning code. I'm
[62:13] trying to minimize learning code. I'm not saying that's not important.
[62:15] not saying that's not important.
[62:15] not saying that's not important. &gt;&gt; But people have lives. people. Some of
[62:17] &gt;&gt; But people have lives. people. Some of
[62:17] &gt;&gt; But people have lives. people. Some of us are older and we've done networking
[62:19] us are older and we've done networking
[62:19] us are older and we've done networking and we've been asked to learn
[62:20] and we've been asked to learn
[62:20] and we've been asked to learn programming and take three years of our
[62:22] programming and take three years of our
[62:22] programming and take three years of our life to learn a new skill. We can
[62:24] life to learn a new skill. We can
[62:24] life to learn a new skill. We can achieve really amazing things now with
[62:25] achieve really amazing things now with
[62:26] achieve really amazing things now with just our ideas, you know, and our
[62:28] just our ideas, you know, and our
[62:28] just our ideas, you know, and our intent. We just explained that we wanted
[62:30] intent. We just explained that we wanted
[62:30] intent. We just explained that we wanted a subnet calculator as a video game,
[62:32] a subnet calculator as a video game,
[62:32] a subnet calculator as a video game, right?
[62:32] right?
[62:32] right? &gt;&gt; And and I want to clearly state I don't
[62:34] &gt;&gt; And and I want to clearly state I don't
[62:34] &gt;&gt; And and I want to clearly state I don't think they're mutually exclusive,
[62:36] think they're mutually exclusive,
[62:36] think they're mutually exclusive, meaning yes, I can do this, but I'm also
[62:39] meaning yes, I can do this, but I'm also
[62:39] meaning yes, I can do this, but I'm also about to sit in like 16 hours,
[62:41] about to sit in like 16 hours,
[62:41] about to sit in like 16 hours, &gt;&gt; you got it,
[62:42] &gt;&gt; you got it,
[62:42] &gt;&gt; you got it, &gt;&gt; of Python and coding and GitHub stuff in
[62:44] &gt;&gt; of Python and coding and GitHub stuff in
[62:44] &gt;&gt; of Python and coding and GitHub stuff in the next couple of days. So it's it's
[62:46] the next couple of days. So it's it's
[62:46] the next couple of days. So it's it's not like oh one or the other.
[62:48] not like oh one or the other.
[62:48] not like oh one or the other. &gt;&gt; Now that being said I could spend the
[62:50] &gt;&gt; Now that being said I could spend the
[62:50] &gt;&gt; Now that being said I could spend the next 3 years learning Python and never
[62:52] next 3 years learning Python and never
[62:52] next 3 years learning Python and never be able to do this.
[62:53] be able to do this.
[62:53] be able to do this. &gt;&gt; So it's both maybe look at all the cool
[62:55] &gt;&gt; So it's both maybe look at all the cool
[62:55] &gt;&gt; So it's both maybe look at all the cool stuff I can do but I'm a technical
[62:57] stuff I can do but I'm a technical
[62:57] stuff I can do but I'm a technical person. I've struggled with Python and I
[62:59] person. I've struggled with Python and I
[62:59] person. I've struggled with Python and I really want to understand the basics and
[63:02] really want to understand the basics and
[63:02] really want to understand the basics and I don't and that's something I want to
[63:03] I don't and that's something I want to
[63:04] I don't and that's something I want to do now or before like I had to and
[63:05] do now or before like I had to and
[63:05] do now or before like I had to and didn't. Right. So it's both probably.
[63:07] didn't. Right. So it's both probably.
[63:07] didn't. Right. So it's both probably. &gt;&gt; So let's just type in a message up here.
[63:09] &gt;&gt; So let's just type in a message up here.
[63:09] &gt;&gt; So let's just type in a message up here. You know working game and then hit
[63:11] You know working game and then hit
[63:11] You know working game and then hit commit. We'll take this offline. Oh,
[63:14] commit. We'll take this offline. Oh,
[63:14] commit. We'll take this offline. Oh, that's what's going on. Okay, hit cancel
[63:16] that's what's going on. Okay, hit cancel
[63:16] that's what's going on. Okay, hit cancel here.
[63:16] here.
[63:16] here. &gt;&gt; All right, so we'll figure out
[63:17] &gt;&gt; All right, so we'll figure out
[63:17] &gt;&gt; All right, so we'll figure out &gt;&gt; we'll figure this out. So, let's stop
[63:18] &gt;&gt; we'll figure this out. So, let's stop
[63:18] &gt;&gt; we'll figure this out. So, let's stop the recording. Thank you.
[63:19] the recording. Thank you.
[63:20] the recording. Thank you. &gt;&gt; Oh, we have to end the show.
[63:21] &gt;&gt; Oh, we have to end the show.
[63:21] &gt;&gt; Oh, we have to end the show. &gt;&gt; We got to end this show. We got to end
[63:22] &gt;&gt; We got to end this show. We got to end
[63:22] &gt;&gt; We got to end this show. We got to end the show. Can't just
[63:23] the show. Can't just
[63:23] the show. Can't just &gt;&gt; this guy.
[63:25] &gt;&gt; this guy.
[63:25] &gt;&gt; this guy. &gt;&gt; That's the That's the Irish goodbye they
[63:27] &gt;&gt; That's the That's the Irish goodbye they
[63:27] &gt;&gt; That's the That's the Irish goodbye they call that. I expect more of my Canadian
[63:29] call that. I expect more of my Canadian
[63:29] call that. I expect more of my Canadian polite friends here that the Irish guys
[63:31] polite friends here that the Irish guys
[63:31] polite friends here that the Irish guys just disappear in a party. So, this is
[63:33] just disappear in a party. So, this is
[63:34] just disappear in a party. So, this is awesome. Thank you for walking us
[63:35] awesome. Thank you for walking us
[63:35] awesome. Thank you for walking us through this. At the risk of repeating
[63:37] through this. At the risk of repeating
[63:37] through this. At the risk of repeating myself, I am excited to be living
[63:39] myself, I am excited to be living
[63:39] myself, I am excited to be living through a time that we can do some
[63:41] through a time that we can do some
[63:41] through a time that we can do some really amazing things that previously
[63:43] really amazing things that previously
[63:43] really amazing things that previously were out of reach for me. I get all the
[63:46] were out of reach for me. I get all the
[63:46] were out of reach for me. I get all the feelings about all the things. So, this
[63:48] feelings about all the things. So, this
[63:48] feelings about all the things. So, this isn't us saying like this is what you
[63:51] isn't us saying like this is what you
[63:51] isn't us saying like this is what you should do and abandon everything else.
[63:53] should do and abandon everything else.
[63:53] should do and abandon everything else. This is just another example of what you
[63:56] This is just another example of what you
[63:56] This is just another example of what you can do with this tooling. If you don't
[63:57] can do with this tooling. If you don't
[63:57] can do with this tooling. If you don't want to, don't. Like, I think this is
[64:00] want to, don't. Like, I think this is
[64:00] want to, don't. Like, I think this is amazing. I'm going to work on this with
[64:02] amazing. I'm going to work on this with
[64:02] amazing. I'm going to work on this with my son. I would like to continue to make
[64:03] my son. I would like to continue to make
[64:04] my son. I would like to continue to make cool stuff and if you want to make cool
[64:06] cool stuff and if you want to make cool
[64:06] cool stuff and if you want to make cool stuff, this is another way you can do
[64:08] stuff, this is another way you can do
[64:08] stuff, this is another way you can do it. I love that you showed me the specri
[64:10] it. I love that you showed me the specri
[64:10] it. I love that you showed me the specri development too. I think this is much
[64:11] development too. I think this is much
[64:11] development too. I think this is much better than anything I would have vibed
[64:13] better than anything I would have vibed
[64:13] better than anything I would have vibed and I am going to default to this. I
[64:15] and I am going to default to this. I
[64:15] and I am going to default to this. I don't think an hour or an hour and a
[64:17] don't think an hour or an hour and a
[64:17] don't think an hour or an hour and a half of time to build something that is
[64:19] half of time to build something that is
[64:19] half of time to build something that is high quality and rigorously tested is a
[64:21] high quality and rigorously tested is a
[64:21] high quality and rigorously tested is a bad thing. like
[64:23] bad thing. like
[64:23] bad thing. like &gt;&gt; I know
[64:23] &gt;&gt; I know
[64:23] &gt;&gt; I know &gt;&gt; I can give an hour and a half of my life
[64:25] &gt;&gt; I can give an hour and a half of my life
[64:25] &gt;&gt; I can give an hour and a half of my life to create better code
[64:27] to create better code
[64:27] to create better code &gt;&gt; and and think and and and I'm sure
[64:29] &gt;&gt; and and think and and and I'm sure
[64:29] &gt;&gt; and and think and and and I'm sure you've started thinking of internal
[64:31] you've started thinking of internal
[64:31] you've started thinking of internal projects and internal things at your job
[64:34] projects and internal things at your job
[64:34] projects and internal things at your job that this might be able to apply for.
[64:36] that this might be able to apply for.
[64:36] that this might be able to apply for. &gt;&gt; There's so much
[64:37] &gt;&gt; There's so much
[64:37] &gt;&gt; There's so much &gt;&gt; and the only other thing I want to
[64:38] &gt;&gt; and the only other thing I want to
[64:38] &gt;&gt; and the only other thing I want to mention is that I can't think of a
[64:40] mention is that I can't think of a
[64:40] mention is that I can't think of a better starting off point. Like if I was
[64:43] better starting off point. Like if I was
[64:43] better starting off point. Like if I was day one in AI, I've never done VIP
[64:45] day one in AI, I've never done VIP
[64:45] day one in AI, I've never done VIP coding. I I don't know what cloud code
[64:47] coding. I I don't know what cloud code
[64:47] coding. I I don't know what cloud code is. I don't know what an MCP server is.
[64:49] is. I don't know what an MCP server is.
[64:49] is. I don't know what an MCP server is. We didn't do any MCP servers today,
[64:51] We didn't do any MCP servers today,
[64:51] We didn't do any MCP servers today, &gt;&gt; right? We installed the simple extension
[64:53] &gt;&gt; right? We installed the simple extension
[64:53] &gt;&gt; right? We installed the simple extension for cloud code or copilot or Gemini or
[64:55] for cloud code or copilot or Gemini or
[64:55] for cloud code or copilot or Gemini or whatever. This is universal. We
[64:59] whatever. This is universal. We
[64:59] whatever. This is universal. We initialized our folder to say you're a
[65:01] initialized our folder to say you're a
[65:01] initialized our folder to say you're a spec folder. And then we ran through the
[65:03] spec folder. And then we ran through the
[65:03] spec folder. And then we ran through the seven steps, right?
[65:05] seven steps, right?
[65:05] seven steps, right? &gt;&gt; This is so I feel I just realized this
[65:08] &gt;&gt; This is so I feel I just realized this
[65:08] &gt;&gt; This is so I feel I just realized this and then we'll end the show. I think the
[65:10] and then we'll end the show. I think the
[65:10] and then we'll end the show. I think the reason I love the LLM stuff, I don't
[65:13] reason I love the LLM stuff, I don't
[65:13] reason I love the LLM stuff, I don't even know what to call it anymore. ALM
[65:15] even know what to call it anymore. ALM
[65:15] even know what to call it anymore. ALM machine learning. But the reason I love
[65:16] machine learning. But the reason I love
[65:16] machine learning. But the reason I love it so much is I feel like there is a
[65:19] it so much is I feel like there is a
[65:19] it so much is I feel like there is a teacher with me the whole time
[65:20] teacher with me the whole time
[65:20] teacher with me the whole time explaining things, clarifying, and I
[65:23] explaining things, clarifying, and I
[65:23] explaining things, clarifying, and I don't get that from a Python textbook,
[65:25] don't get that from a Python textbook,
[65:25] don't get that from a Python textbook, &gt;&gt; right?
[65:25] &gt;&gt; right?
[65:25] &gt;&gt; right? &gt;&gt; I don't I didn't get that in C++ at
[65:27] &gt;&gt; I don't I didn't get that in C++ at
[65:27] &gt;&gt; I don't I didn't get that in C++ at Temple University in Philadelphia. Like
[65:29] Temple University in Philadelphia. Like
[65:29] Temple University in Philadelphia. Like it was just here's the stuff,
[65:30] it was just here's the stuff,
[65:30] it was just here's the stuff, &gt;&gt; right?
[65:31] &gt;&gt; right?
[65:31] &gt;&gt; right? &gt;&gt; Learn it. And if you don't, so I feel
[65:34] &gt;&gt; Learn it. And if you don't, so I feel
[65:34] &gt;&gt; Learn it. And if you don't, so I feel like something is holding my hand as I
[65:36] like something is holding my hand as I
[65:36] like something is holding my hand as I learn. This isn't me not learning
[65:38] learn. This isn't me not learning
[65:38] learn. This isn't me not learning things. This is something going, okay,
[65:40] things. This is something going, okay,
[65:40] things. This is something going, okay, here. I mean, not necessarily here.
[65:42] here. I mean, not necessarily here.
[65:42] here. I mean, not necessarily here. which is pretty intense. But I could
[65:43] which is pretty intense. But I could
[65:43] which is pretty intense. But I could just go and say, "Hey, I want to learn
[65:45] just go and say, "Hey, I want to learn
[65:45] just go and say, "Hey, I want to learn Python. Can you help me?"
[65:46] Python. Can you help me?"
[65:46] Python. Can you help me?" &gt;&gt; Yeah.
[65:46] &gt;&gt; Yeah.
[65:46] &gt;&gt; Yeah. &gt;&gt; And just talk it out. And there's free
[65:48] &gt;&gt; And just talk it out. And there's free
[65:48] &gt;&gt; And just talk it out. And there's free models you can do that with. Like it's a
[65:50] models you can do that with. Like it's a
[65:50] models you can do that with. Like it's a teacher at your fingertips
[65:51] teacher at your fingertips
[65:51] teacher at your fingertips &gt;&gt; is that we built a Subnet game, for
[65:53] &gt;&gt; is that we built a Subnet game, for
[65:53] &gt;&gt; is that we built a Subnet game, for example, right?
[65:54] example, right?
[65:54] example, right? &gt;&gt; You might want to go home and build a
[65:56] &gt;&gt; You might want to go home and build a
[65:56] &gt;&gt; You might want to go home and build a learn Python game,
[65:57] learn Python game,
[65:57] learn Python game, &gt;&gt; right? That's Well, how about that,
[65:59] &gt;&gt; right? That's Well, how about that,
[65:59] &gt;&gt; right? That's Well, how about that, right? And and we're of an age. This
[66:01] right? And and we're of an age. This
[66:01] right? And and we're of an age. This didn't exist
[66:02] didn't exist
[66:02] didn't exist &gt;&gt; ago. This didn't exist eight months ago.
[66:04] &gt;&gt; ago. This didn't exist eight months ago.
[66:04] &gt;&gt; ago. This didn't exist eight months ago. months ago, let alone when I was 18 or
[66:07] months ago, let alone when I was 18 or
[66:07] months ago, let alone when I was 18 or 22 or like trying to learn this, you
[66:09] 22 or like trying to learn this, you
[66:09] 22 or like trying to learn this, you know, would my story and my narrative
[66:11] know, would my story and my narrative
[66:11] know, would my story and my narrative &gt;&gt; Stack Overflow and open up a question
[66:13] &gt;&gt; Stack Overflow and open up a question
[66:13] &gt;&gt; Stack Overflow and open up a question and someone would close it as a
[66:14] and someone would close it as a
[66:14] and someone would close it as a duplicate issue or call me a dummy
[66:16] duplicate issue or call me a dummy
[66:16] duplicate issue or call me a dummy because I didn't know that already or
[66:18] because I didn't know that already or
[66:18] because I didn't know that already or shame me, right?
[66:20] shame me, right?
[66:20] shame me, right? &gt;&gt; I am just having an epiphany that when I
[66:23] &gt;&gt; I am just having an epiphany that when I
[66:23] &gt;&gt; I am just having an epiphany that when I was in college getting my ass handed to
[66:25] was in college getting my ass handed to
[66:25] was in college getting my ass handed to me with calculus and C++, I did not have
[66:28] me with calculus and C++, I did not have
[66:28] me with calculus and C++, I did not have access. I had one college professor that
[66:30] access. I had one college professor that
[66:30] access. I had one college professor that was busy and couldn't spend endless time
[66:33] was busy and couldn't spend endless time
[66:33] was busy and couldn't spend endless time with me going at my pace so that I could
[66:36] with me going at my pace so that I could
[66:36] with me going at my pace so that I could learn at my pace,
[66:37] learn at my pace,
[66:37] learn at my pace, &gt;&gt; right?
[66:38] &gt;&gt; right?
[66:38] &gt;&gt; right? &gt;&gt; This tooling to me is that in a sense I
[66:42] &gt;&gt; This tooling to me is that in a sense I
[66:42] &gt;&gt; This tooling to me is that in a sense I have a full-time teacher that can walk
[66:44] have a full-time teacher that can walk
[66:44] have a full-time teacher that can walk me through things so you can learn
[66:45] me through things so you can learn
[66:45] me through things so you can learn anything you want
[66:47] anything you want
[66:47] anything you want &gt;&gt; and I love this and I'm very excited.
[66:49] &gt;&gt; and I love this and I'm very excited.
[66:49] &gt;&gt; and I love this and I'm very excited. Thank you so much.
[66:51] Thank you so much.
[66:51] Thank you so much. &gt;&gt; Hey, no problem.
[66:51] &gt;&gt; Hey, no problem.
[66:51] &gt;&gt; Hey, no problem. &gt;&gt; For doing this again with us. I love
[66:53] &gt;&gt; For doing this again with us. I love
[66:53] &gt;&gt; For doing this again with us. I love what you're doing. I'm sorry people give
[66:54] what you're doing. I'm sorry people give
[66:54] what you're doing. I'm sorry people give you a hard time about any of this. I
[66:57] you a hard time about any of this. I
[66:57] you a hard time about any of this. I understand why people feel threatened.
[66:59] understand why people feel threatened.
[66:59] understand why people feel threatened. I'm not a 100% like I don't know what's
[67:02] I'm not a 100% like I don't know what's
[67:02] I'm not a 100% like I don't know what's coming and are we all going to be
[67:04] coming and are we all going to be
[67:04] coming and are we all going to be batteries in the matrix? Is there going
[67:05] batteries in the matrix? Is there going
[67:05] batteries in the matrix? Is there going to be universal stuff? Like are all the
[67:07] to be universal stuff? Like are all the
[67:07] to be universal stuff? Like are all the jobs going to go away? I have no idea.
[67:08] jobs going to go away? I have no idea.
[67:08] jobs going to go away? I have no idea. &gt;&gt; You know, history's been pretty kind to
[67:10] &gt;&gt; You know, history's been pretty kind to
[67:10] &gt;&gt; You know, history's been pretty kind to me. I consciously made a career pivot
[67:15] me. I consciously made a career pivot
[67:15] me. I consciously made a career pivot into AI 3 years ago
[67:17] into AI 3 years ago
[67:17] into AI 3 years ago &gt;&gt; because
[67:18] &gt;&gt; because
[67:18] &gt;&gt; because &gt;&gt; well because I was because of what it
[67:20] &gt;&gt; well because I was because of what it
[67:20] &gt;&gt; well because I was because of what it did how it made me feel how it made me
[67:22] did how it made me feel how it made me
[67:22] did how it made me feel how it made me feel and the opportunity I think I saw
[67:25] feel and the opportunity I think I saw
[67:25] feel and the opportunity I think I saw at the time. Was there a thing you did
[67:26] at the time. Was there a thing you did
[67:26] at the time. Was there a thing you did that you were like, "Holy sh" like,
[67:28] that you were like, "Holy sh" like,
[67:28] that you were like, "Holy sh" like, "Whoa."
[67:29] "Whoa."
[67:29] "Whoa." &gt;&gt; Yeah. The the when I sent like show
[67:32] &gt;&gt; Yeah. The the when I sent like show
[67:32] &gt;&gt; Yeah. The the when I sent like show interfaces to an LLM and it just told me
[67:34] interfaces to an LLM and it just told me
[67:34] interfaces to an LLM and it just told me these three interfaces are not healthy
[67:36] these three interfaces are not healthy
[67:36] these three interfaces are not healthy and I didn't have to write the Python to
[67:37] and I didn't have to write the Python to
[67:37] and I didn't have to write the Python to do that.
[67:38] do that.
[67:38] do that. &gt;&gt; That was like your light bulb like wait
[67:39] &gt;&gt; That was like your light bulb like wait
[67:39] &gt;&gt; That was like your light bulb like wait a minute something's happening.
[67:42] a minute something's happening.
[67:42] a minute something's happening. &gt;&gt; And uh what better way to learn than
[67:44] &gt;&gt; And uh what better way to learn than
[67:44] &gt;&gt; And uh what better way to learn than gify the subject and we just showed you
[67:46] gify the subject and we just showed you
[67:46] gify the subject and we just showed you how to do that, right? So this episode
[67:48] how to do that, right? So this episode
[67:48] how to do that, right? So this episode has a lot of layers to it. So take your
[67:51] has a lot of layers to it. So take your
[67:51] has a lot of layers to it. So take your time and you know us. Reach out to Andy.
[67:54] time and you know us. Reach out to Andy.
[67:54] time and you know us. Reach out to Andy. Reach out to me. He did his first one
[67:56] Reach out to me. He did his first one
[67:56] Reach out to me. He did his first one now. I bet you in two weeks he'll
[67:58] now. I bet you in two weeks he'll
[67:58] now. I bet you in two weeks he'll probably have 10 or 15 of these things
[68:00] probably have 10 or 15 of these things
[68:00] probably have 10 or 15 of these things going, right?
[68:00] going, right?
[68:00] going, right? &gt;&gt; It's up on GitHub. It's public.
[68:03] &gt;&gt; It's up on GitHub. It's public.
[68:03] &gt;&gt; It's up on GitHub. It's public. &gt;&gt; Play the game. Make the game better. And
[68:05] &gt;&gt; Play the game. Make the game better. And
[68:06] &gt;&gt; Play the game. Make the game better. And uh thanks for joining us from Munich.
[68:08] uh thanks for joining us from Munich.
[68:08] uh thanks for joining us from Munich. &gt;&gt; Thanks for being here. It's been a
[68:10] &gt;&gt; Thanks for being here. It's been a
[68:10] &gt;&gt; Thanks for being here. It's been a pleasure. For all things Art of Netge,
[68:11] pleasure. For all things Art of Netge,
[68:11] pleasure. For all things Art of Netge, check out our link tree at
[68:12] check out our link tree at
[68:12] check out our link tree at linkree/arttofetge.s.
[68:14] linkree/arttofetge.s.
[68:14] linkree/arttofetge.s. Check out our shiny new website at the
[68:17] Check out our shiny new website at the
[68:17] Check out our shiny new website at the usual place arttoeng engineering.com.
[68:19] usual place arttoeng engineering.com.
[68:19] usual place arttoeng engineering.com. There's a really cool resources section
[68:21] There's a really cool resources section
[68:21] There's a really cool resources section that we're adding all kinds of cool
[68:23] that we're adding all kinds of cool
[68:23] that we're adding all kinds of cool stuff to things you can learn. It's
[68:25] stuff to things you can learn. It's
[68:25] stuff to things you can learn. It's mostly free. There's communities. If
[68:27] mostly free. There's communities. If
[68:27] mostly free. There's communities. If there's anything missing or wrong in
[68:28] there's anything missing or wrong in
[68:28] there's anything missing or wrong in there, submit an issue in GitHub. Do a
[68:31] there, submit an issue in GitHub. Do a
[68:31] there, submit an issue in GitHub. Do a pull. I don't even know if I'm saying it
[68:32] pull. I don't even know if I'm saying it
[68:32] pull. I don't even know if I'm saying it right. Do a pull request or send him a
[68:35] right. Do a pull request or send him a
[68:35] right. Do a pull request or send him a PR.
[68:35] PR.
[68:35] PR. &gt;&gt; Yes. Send me a PR. Send me an issue.
[68:37] &gt;&gt; Yes. Send me a PR. Send me an issue.
[68:37] &gt;&gt; Yes. Send me a PR. Send me an issue. We'll get it fixed. We can do this
[68:38] We'll get it fixed. We can do this
[68:38] We'll get it fixed. We can do this together. As always, thank you so much
[68:40] together. As always, thank you so much
[68:40] together. As always, thank you so much for watching and listening and we'll
[68:41] for watching and listening and we'll
[68:42] for watching and listening and we'll catch you next time on the Art of
[68:43] catch you next time on the Art of
[68:43] catch you next time on the Art of Network Engineering Podcast.
[68:45] Network Engineering Podcast.
[68:45] Network Engineering Podcast. Hey folks, if you like what you heard
[68:47] Hey folks, if you like what you heard
[68:47] Hey folks, if you like what you heard today, please subscribe to our podcast
[68:49] today, please subscribe to our podcast
[68:49] today, please subscribe to our podcast in your favorite podcast catcher. You
[68:51] in your favorite podcast catcher. You
[68:51] in your favorite podcast catcher. You can find us on socials at Art of Netge
[68:53] can find us on socials at Art of Netge
[68:53] can find us on socials at Art of Netge and you can visit linktree/artnetge
[68:56] and you can visit linktree/artnetge
[68:56] and you can visit linktree/artnetge for links to all of our content
[68:58] for links to all of our content
[68:58] for links to all of our content including the A1 merch store and our
[69:00] including the A1 merch store and our
[69:00] including the A1 merch store and our virtual community on Discord called it's
[69:02] virtual community on Discord called it's
[69:02] virtual community on Discord called it's all about the journey. You can see our
[69:04] all about the journey. You can see our
[69:04] all about the journey. You can see our pretty faces on our YouTube channel
[69:06] pretty faces on our YouTube channel
[69:06] pretty faces on our YouTube channel named The Art of Network Engineering.
[69:08] named The Art of Network Engineering.
[69:08] named The Art of Network Engineering. That's youtube.com/artnetenge.
[69:11] That's youtube.com/artnetenge.
[69:11] That's youtube.com/artnetenge. Thanks for listening.
