# Building Governed Agents: A Framework for Cost, Control and Compliance

- **Video:** https://www.youtube.com/watch?v=o7SA6qD55DQ
- **Generated:** 2026-08-31 21:05 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The material presents **LangSmith/LangChain** as an “agent engineering” ecosystem for building, testing, deploying, monitoring, and governing AI agents. Its central architectural proposition is a **centralized LLM/agent gateway (runtime control plane)** placed between applications and model/tool providers to standardize policy enforcement, routing, observability, cost controls, and audit evidence.

The core operational message is credible and relevant to Superior Propane:

- Agentic systems are materially harder to govern than single-turn LLM applications because they can make repeated model calls, retrieve data, invoke tools/MCP servers, delegate to sub-agents, retry/fail over, and potentially perform business actions.
- Production controls should be designed into the lifecycle—**build → test/evaluate → deploy → monitor → iterate**—rather than retrofitted after deployment.
- Governance must cover more than LLM calls: it must include **identity, data retrieval, tool/MCP access, agent-to-agent delegation, action approvals, traceability, resiliency, and cost containment**.
- A centralized gateway can improve consistency and reduce duplicated implementation, but becomes a critical dependency requiring high availability, tested fallback behavior, clear ownership, and ongoing operational investment.

For Superior Propane, the recommended principle is to establish a reusable **AI runtime governance pattern**, whether implemented primarily with Azure-native capabilities, a specialized platform such as LangSmith, or a hybrid:

```text
Users / Business Systems
        |
Agent applications / workflows
(Azure AI Foundry, custom services, Databricks workloads, LangGraph, etc.)
        |
Central AI access and policy layer
- identity and workload attribution
- approved model routing
- data/egress policy
- quotas, rate limits, cost controls
- tool/MCP authorization
- tracing and audit events
- fallback and circuit-breaker policy
        |
Approved model endpoints, tools, MCP servers, and data services
```

**Important qualification:** Much of the LangSmith-specific capability discussion is based on speaker/vendor claims. The transcript does not establish current feature maturity, Azure compatibility, data residency, private networking, Entra ID support, auditability, pricing, SLA, or deployment architecture. In one section, the LangSmith LLM Gateway is described as being in **public beta at the time of the presentation**. It should not be adopted as a production control plane without formal security, architecture, and proof-of-concept validation.

---

# Technical details

## 1. Agent governance scope

The speaker characterizes LangSmith as a model-, cloud-, and framework-agnostic agent-engineering platform, within a broader LangChain ecosystem that includes:

- **LangChain**
- **LangGraph**
- **Deep Agents**
- **LangSmith**
- **LangSmith Fleet** — claimed no-code agent building
- **LangSmith Deployment** — claimed one-click deployment
- **LangSmith LLM Gateway**
- **LangSmith Engine** — described as an agent that can help improve agents

These are **vendor claims**. The transcript does not demonstrate interoperability with Azure AI Foundry, Azure OpenAI, Databricks, Microsoft Entra ID, Azure API Management, Unity Catalog, Azure Monitor, or Canadian data residency requirements.

The more durable architecture principle is to apply governance consistently across the full agent lifecycle:

1. **Build** — approved frameworks, identities, data sources, tool contracts.
2. **Test/evaluate** — quality, safety, groundedness, cost, latency, prompt injection, tool misuse, and failure-mode testing.
3. **Deploy** — environment separation, versioning, release approval, rollback.
4. **Monitor** — telemetry, tracing, anomalies, spend, policy events, reliability.
5. **Assure/audit** — evidence of what was deployed, what happened, who approved changes, and whether controls operated as intended.

## 2. Why agents need stronger controls than conventional LLM applications

The speaker highlights that agents may have:

- Nondeterministic outputs.
- Multi-step reasoning and execution.
- Repeated model calls and retries.
- Context growth from conversation history and retrieval.
- Tool/API calls with real-world effects.
- Recursive planning or delegation to sub-agents.
- Variable cost and latency across models/providers.

These are established operational concerns. Cost and risk can grow through:

- Large prompt/context windows.
- Multiple retrieval calls.
- Tool calls and downstream API usage.
- Retry storms after provider failures.
- Agent loops or excessive delegation depth.
- Parallel agent fan-out.
- Fallback calls after timeouts.
- Higher-cost model use for routine tasks.

A monthly cloud budget alone is insufficient protection. A malfunctioning agent can incur meaningful cost or overload shared quota within minutes.

## 3. Central LLM gateway / runtime control plane

The speaker describes an LLM gateway that intercepts a request before it reaches a model provider:

```text
Agent/application
      |
      | LLM request
      v
AI gateway / runtime policy layer
  - authenticate caller
  - apply approved model/provider policy
  - inspect/transform allowed payloads
  - enforce rate/token/spend limits
  - apply retries, circuit breakers, fallbacks
  - emit traces, policy events, usage data
      |
      +--> Primary model endpoint
      +--> Prevalidated alternate endpoint/model
```

### Intended gateway capabilities

The speaker claims the LangSmith gateway can provide:

- Model/provider routing.
- Fallback routing.
- Spend and rate limits.
- Retry and circuit-breaker policies.
- PII and secret redaction/data reduction.
- Request traces and spend dashboards.
- Integration with evaluations and analysis.

These functions are technically plausible, but require validation of feature coverage and enforcement semantics.

### Gateway benefits

A central control point can provide:

- Consistent policy enforcement across teams and applications.
- Reduced use of embedded provider credentials.
- Central model catalog and routing policy.
- More complete usage/cost attribution.
- Better control over direct calls to unapproved model endpoints.
- Shared observability across agents built in different frameworks.
- Central kill/containment capability for a model, prompt, agent, tool, or provider.

### Gateway trade-offs

A gateway also introduces:

- Another service in the critical request path.
- Incremental latency for every model call.
- High-availability, scaling, DR, and incident-response requirements.
- Potentially substantial telemetry storage/retention cost.
- Policy lifecycle and operational support burden.
- Possible delays supporting provider-specific features, streaming, structured outputs, tool calling, multimodal requests, or new models.
- Risk of practical lock-in to gateway-specific abstractions and tracing.

A gateway should be considered a **technical enforcement layer**, not a complete governance solution. It does not replace source-system authorization, data governance, network controls, security review, release management, or human approvals.

## 4. Data plane versus control plane

For a centralized AI access architecture, separate:

- **Data plane:** live inference and tool request path. It must be low-latency, scalable, resilient, and protected.
- **Control plane:** model catalog, policy configuration, approval workflows, dashboards, administration, and policy publication.

A practical resilience design is for the data plane to continue with a **last-known-valid, versioned policy configuration** if the management/control plane is unavailable. This avoids an administration outage taking down all AI workloads, while still preventing arbitrary policy changes.

This approach requires:

- Signed/versioned policy bundles.
- Configuration rollout controls.
- Emergency revocation/kill-switch design.
- Explicit behavior for stale policy configuration.
- Auditability of policy versions applied to each request.

## 5. Identity, authorization, and delegation

The transcript repeatedly emphasizes that governance becomes more difficult when agents call tools, MCP servers, or other agents.

Every production interaction should distinguish:

- **End-user identity** — the individual requesting or initiating the work.
- **Application/workload identity** — the deployed service or agent runtime.
- **Agent identity** — a distinct identity for an orchestrator or sub-agent where applicable.
- **Tool/MCP server identity** — the service being invoked.
- **Downstream service authorization** — the business system’s own enforcement of permissions.

A secure authorization pattern is:

```text
User identity + agent/workload identity
             |
             v
Policy decision and authorization check
             |
   +---------+----------+
   |                    |
 Deny        Permit only a scoped API operation
                          |
                          v
                 Tool/business-system action
                          |
                          v
               Correlated audit and trace event
```

### Agent-to-agent delegation

Multi-agent workflows create a potential **confused-deputy** problem: a less-trusted agent should not be able to induce a more privileged agent to act beyond the original user’s entitlement or the calling agent’s approved scope.

For every agent-to-agent call, define:

- Whether the downstream agent acts under:
  - delegated end-user permissions,
  - the calling agent’s identity,
  - or its own workload identity.
- Which downstream agents can be called.
- Maximum delegation depth.
- Tool and data permissions for each agent.
- Whether write actions require human approval.
- Trace propagation requirements across all hops.

The speaker emphasizes agent identity conceptually but does not provide a complete distributed enforcement architecture.

## 6. Tool and MCP governance

The speaker treats **tool calls** and **Model Context Protocol (MCP) server calls** as distinct high-risk boundaries.

MCP servers should be treated like APIs/connectors—not as inherently trusted because they use a standard protocol.

### Minimum tool/MCP registry

Maintain an approved inventory containing:

- Business and technical owner.
- Purpose and environment.
- Data classifications accessed.
- Read-only versus write/destructive operations.
- Allowed agents, applications, and user roles.
- Authentication method and secret lifecycle.
- Permitted operations and parameter constraints.
- Network/data-egress path.
- Logging, version, patching, and vulnerability-management ownership.
- Approval and retirement status.

### Tool action tiers

| Action tier | Example | Recommended control |
|---|---|---|
| Low-risk read | Approved knowledge-base retrieval | RBAC, source filtering, logging |
| Sensitive read | Customer, account, employee, pricing, or delivery information | Fine-grained authorization, masking, audit |
| Recommendation/draft | Draft customer response or proposed work order | Human review before commit |
| Business-impacting write | Change account details, delivery instructions, pricing, credits, payment status | Explicit confirmation, policy gate, strong audit |
| Safety-critical/regulated action | Actions affecting propane service safety or emergency communications | Human-led execution or formal dual-control workflow |

Do not give agents unrestricted database access or broad enterprise application permissions. Expose **narrow, purpose-specific APIs** with deterministic validation and authorization.

## 7. Cost, quota, and rate-limit controls

The speaker advocates layered controls at organization, workspace, API-key, user, application, and team levels. For Superior Propane, use **workload identities** rather than shared API keys wherever possible.

### Recommended control hierarchy

| Scope | Purpose |
|---|---|
| Request/agent run | Bound tokens, context, tool calls, runtime, and spend for one execution |
| User/session | Limit abuse or runaway interaction patterns |
| Agent/application | Contain a defect or excessive workload in one product |
| Team/cost centre | Enable showback/chargeback and accountable consumption |
| Environment | Prevent dev/test/batch work from consuming production capacity |
| Model/provider deployment | Protect shared quota and service capacity |
| Enterprise/platform | Emergency global cap and centralized kill switch |

Controls should include:

- Concurrent execution limits.
- Requests-per-minute and tokens-per-minute limits.
- Per-run maximum model calls, tool calls, agent steps, and delegation depth.
- Input/output token caps.
- Timeout and cancellation controls.
- Retry limits and circuit breakers.
- Per-minute/hour/day/month spend limits.
- Budget alerts before hard stops.
- Capacity isolation between production, experimentation, and batch workloads.

### Cost accounting limitations

The speaker correctly notes that LLM cost cannot always be inferred from simple prompt/output token counts. Cost may vary by:

- Model/version/provider/deployment/region.
- Input, output, cached, or other token categories.
- Retry/fallback behavior.
- Endpoint/request type.
- Provider pricing changes, discounts, and billing semantics.

Use two measures:

1. **Near-real-time estimated cost** for routing, budget controls, and alerts.
2. **Invoice-reconciled cost** for FinOps reporting and financial accounting.

The transcript does not explain whether gateway spend counters are strongly consistent, eventually consistent, or atomic across regions/nodes. This is a major validation topic: under concurrency, a budget can be exceeded before distributed counters converge.

## 8. Model routing, portability, and fallback

The speaker recommends a model portfolio rather than a universal model:

- Lower-cost models for classification, extraction, routine retrieval, and summarization.
- Higher-capability models for complex reasoning or higher-value outcomes.
- Approved fallbacks for outages, throttling, or budget exhaustion.

This is a reasonable pattern, but model substitution is not inherently safe. A common API abstraction does not guarantee equivalent:

- Output quality and reasoning.
- Tool/function-calling behavior.
- JSON/structured output reliability.
- Context-window capacity.
- Streaming and multimodal support.
- Safety/filtering behavior.
- Latency and throughput.
- Regional availability.
- Data residency and provider contractual terms.

### Fallback policy by risk

| Workload | Suggested behavior on provider failure/cap |
|---|---|
| Internal document Q&A | Use a prevalidated alternate model if permitted; disclose degraded capability if relevant |
| Batch extraction/classification | Queue/retry later or use approved lower-cost model |
| Employee assist | Conditional fallback if human review remains in the workflow |
| Customer-facing support | Fail gracefully or route to human support if equivalent quality cannot be assured |
| Tool-using operational workflow | Stop before external action; checkpoint state and request approval |
| Safety, pricing, financial, or account-changing workflow | Do not silently downgrade; human review or deterministic workflow required |

Fallback routing must also prevent sensitive data from being sent to an unapproved provider, region, or cloud.

## 9. Context minimization, PII, and secret controls

The speaker recommends minimizing context before inference using:

- Retrieval top-*k* limits and relevance thresholds.
- Metadata filtering.
- Removal of duplicate passages.
- Field-level extraction rather than full source records.
- Conversation-history summarization.
- Context/token budgets.
- Caching where appropriate.

This can reduce:

- Inference cost.
- Latency.
- Exposure of unnecessary customer, employee, financial, or operational data.
- Prompt-injection surface from irrelevant retrieved material.

However, pruning must be evaluated. Excessive reduction can omit exceptions, safety instructions, or policy context and reduce accuracy.

### PII and secret detection

The transcript identifies:

- **Structured detection:** regex/patterns for known formats such as phone numbers or national identifiers.
- **Unstructured detection:** NER or model-based classifiers for names, locations, affiliations, and context-dependent PII.
- **Secret detection:** API keys, tokens, credentials, and configuration secrets.

Limitations:

- Regex has false positives and false negatives.
- NER/LLM classification is probabilistic and adds cost/latency.
- Sending sensitive text to a classification model itself creates a data-processing boundary.
- Redaction does not replace source authorization.
- Post-request redaction does not undo prior exposure to an LLM endpoint.

Use layered controls:

1. Enforce entitlement before retrieval/tool access.
2. Minimize fields and context before prompt construction.
3. Detect/mask known sensitive patterns.
4. Apply semantic PII controls where justified.
5. Redact sensitive trace/log fields before persistence.
6. Use managed identity and Key Vault rather than embedding secrets.
7. Scan developer endpoints, source control, CI/CD, prompts, tool outputs, and logs.

## 10. Observability, evaluations, and auditability

The speaker positions tracing and evaluations as essential for understanding agent behavior.

Useful trace fields include:

- Correlation/trace IDs and parent-child agent spans.
- User, application, agent, and workload identity.
- Environment, owner, cost centre, and business workflow.
- Prompt/template version and retrieval/index/tool-schema version.
- Model/provider/deployment/version.
- Token counts, cache status, estimated cost, latency, retries, and fallback events.
- Tool/MCP invocation, authorization decision, and outcome.
- Guardrail/redaction/policy events.
- Evaluation outcome and human review result where applicable.
- Error type, loop count, cancellation, and recovery state.

Full prompt/response/tool-payload logging should not be the default. Traces can become a new sensitive-data repository requiring:

- Dedicated access roles.
- Redaction and minimization.
- Retention/deletion rules.
- Encryption and data-residency review.
- SIEM export for security-relevant events.
- Separation between developer debugging access and production operations access.

### Evaluation coverage

An enterprise evaluation suite should include:

- Golden tasks and expected outcomes.
- Groundedness/citation tests.
- Prompt injection and malicious-document tests.
- Unauthorized tool use and unsafe-action tests.
- PII/secret leakage tests.
- Retrieval quality and entitlement-filtering tests.
- Model/prompt/tool-schema/index regression tests.
- Cost and latency thresholds.
- Provider outage, tool failure, and fallback tests.
- Human-review and user-acceptance metrics.

The speaker refers to online/offline “evals,” but does not specify scoring methods, CI/CD gates, data retention, or security protections for evaluation datasets.

## 11. Fail-open versus fail-closed

The speaker emphasizes deciding in advance how controls behave when a policy service, DLP check, budget service, or provider is unavailable or slow.

| Condition | Typical posture |
|---|---|
| Authentication/authorization unavailable | Fail closed |
| Sensitive-data policy or egress decision unavailable | Usually fail closed |
| Write action or high-impact tool action | Fail closed and escalate |
| Non-critical telemetry unavailable | Fail open with alerting, if no sensitive payload is exposed |
| Primary model unavailable | Fail over only to a prevalidated, approved alternative |
| Budget service unavailable | Risk-dependent; cached quotas may be acceptable for essential low-risk workflows |
| Gateway instance failure | Recover through redundant deployment, not uncontrolled bypass |

A fail-open posture may improve availability but can permit uninspected or unsafe traffic. For customer data, pricing, financial decisions, dispatch, safety, or operational writes, a safe degraded experience or human escalation is generally preferable to bypassing controls.

## 12. Azure and Databricks mapping

The transcript does not prescribe Azure or Databricks architecture. A candidate mapping for Superior Propane is:

| Governance need | Azure / Databricks areas to evaluate |
|---|---|
| User/workload identity | Microsoft Entra ID, managed identities, service principals, RBAC |
| Model endpoints and lifecycle | Azure AI Foundry, Azure OpenAI, approved model catalog and deployment controls |
| API/tool governance | Azure API Management, scoped OAuth, narrowly defined APIs, allowlists |
| Secrets | Azure Key Vault, managed identity, rotation and access audit |
| Observability | Azure Monitor, Application Insights, Log Analytics, OpenTelemetry, Microsoft Sentinel |
| Network/data egress | Private Endpoints/Private Link, VNets, firewall and egress controls |
| Data governance | Databricks Unity Catalog, governed views, lineage, row/column controls where applicable |
| Data/AI workload telemetry analysis | Databricks lakehouse, system tables/audit logs, governed reporting |
| Cost allocation | Azure Cost Management plus application/gateway token and usage telemetry |
| Infrastructure/release discipline | Azure DevOps or GitHub Actions, Terraform/Bicep, environment separation |

For Databricks-connected agents, Unity Catalog and source-system entitlements must remain the authority for data access. The agent should initially use curated, read-only views or purpose-built service APIs—not broad raw-table, notebook, or workspace credentials.

---

# Potential applications for Superior Propane

## 1. Enterprise AI governance baseline

Create a common governance framework applicable to agents built in Azure AI Foundry, Databricks, custom Azure services, or third-party frameworks.

Minimum registration data for each agent/application:

- Business owner and technical owner.
- Use case and intended users.
- Risk tier.
- Data sources and classifications.
- Approved models/deployments/providers.
- Tool/MCP inventory and permitted actions.
- Workload identity and user-delegation approach.
- Evaluation and release criteria.
- Cost centre, budget, and service-level targets.
- Trace/audit retention and operational owner.
- Fallback, human-escalation, and incident runbook.

## 2. Internal knowledge and policy assistant

A low-risk initial use case could provide read-only assistance over approved policy, safety, procedure, and training documents.

Controls:

- Entra-based user authorization and document-level filtering.
- Curated content only; no open web access initially.
- Retrieval source citations.
- Context minimization and trace redaction.
- Read-only posture; no enterprise-system write tools.
- Evaluation for groundedness, safety-related completeness, and prompt injection from retrieved content.

This provides a bounded way to validate model quality, tracing, cost controls, and governance operations.

## 3. Customer-service agent assist

Potential capabilities:

- Summarize calls, chats, service notes, and account history.
- Retrieve approved policies and knowledge articles.
- Draft customer communications.
- Suggest next steps for customer-service representatives.

Recommended posture:

- Start with employee-facing **agent assist**, not unrestricted customer-facing autonomy.
- Retrieve only account fields required for the task.
- Preserve CRM/source-system authorization.
- Require human review before account updates, delivery changes, credits, billing decisions, or customer commitments.
- Record source IDs, tool calls, policy checks, and approvals.
- Establish human handoff when the model is unavailable, uncertain, or blocked by policy.

## 4. Field operations and dispatch support

Potential capabilities:

- Summarize service and delivery history.
- Retrieve approved safety and troubleshooting procedures.
- Assist technicians with diagnostics.
- Draft operational exceptions for dispatcher review.

Recommended guardrails:

- Read-only access by default.
- Scope data to assigned routes, work orders, or customer cases.
- Use structured APIs rather than direct database access.
- Require dispatcher/human approval for route changes, delivery changes, service commitments, or safety-adjacent actions.
- Do not allow autonomous changes to safety-critical records without formal business, safety, and security approval.

## 5. Databricks analytics assistant

Potential internal capabilities:

- Discover governed datasets and metric definitions.
- Generate draft SQL against curated data products.
- Explain reports and data-quality signals.
- Summarize demand, service, sales, delivery, or inventory trends.

Control model:

- Use Unity Catalog-governed Gold-layer tables, semantic views, or a governed service layer.
- Preserve row/column/data-masking controls.
- Start with read-only SQL access.
- Enforce query cost, timeout, and warehouse restrictions.
- Log generated SQL, tables/views accessed, result sensitivity, query cost/runtime, and user/agent identity.
- Do not place raw sensitive data into prompts, traces, or evaluation datasets unless explicitly approved.

## 6. Controlled multi-agent service workflow

A future workflow could separate responsibilities:

1. **Triage agent** — classifies the request.
2. **Knowledge agent** — retrieves approved procedures/policies.
3. **Account-context agent** — performs constrained read-only lookup.
4. **Action agent** — creates a proposed structured action for approval.

This design should enforce per-agent identities, allowlisted downstream agents, maximum delegation depth, per-agent budgets, and human approval before any consequential business-system commit.

---

# Risks/validation questions

## LangSmith/vendor validation

The following are speaker/vendor claims requiring validation:

- LangSmith is model-, cloud-, and framework-agnostic.
- LangSmith supports complete lifecycle governance.
- Fleet offers no-code agent development.
- Deployment offers one-click deployment.
- Engine can autonomously improve agents.
- The gateway provides the described policy, redaction, routing, and cost-control functions.
- LangSmith can support enterprise-scale controls across teams.
- The gateway requires only minor code changes for LangChain/LangGraph workloads.

Validate current product status, especially because the gateway was described as **public beta** in the presentation.

## Security, privacy, and residency

Before sending any Superior Propane prompt, trace, tool payload, evaluation dataset, or retrieval content to LangSmith or another third party, validate:

- SaaS, self-hosted, VNet/VPC, and private connectivity options.
- Canadian/required regional data residency.
- Physical storage locations for prompts, outputs, traces, attachments, and evaluation datasets.
- Data-use/training terms.
- Retention, deletion, backup, and selective purge support.
- Client-side versus server-side redaction and masking.
- Encryption, key-management, customer-managed-key options.
- SSO/SAML/OIDC, SCIM, Entra ID integration, and RBAC granularity.
- Service-account/API-key lifecycle management.
- SOC 2 Type II, ISO 27001, penetration-test evidence, vulnerability management, and incident-notification commitments.
- Audit-log immutability, retention, and Sentinel/SIEM export.

## Azure and Databricks integration

- Does the gateway support Azure OpenAI and Azure AI Foundry endpoint patterns required by Superior Propane?
- Can it authenticate via Entra ID/managed identities, or does it require static provider keys?
- Can it preserve streaming, JSON schema/structured outputs, tool calling, embeddings, and multimodal capabilities?
- How does it integrate with Azure API Management rather than duplicate or bypass it?
- Can it export OpenTelemetry-compatible telemetry to Azure Monitor/Application Insights/Log Analytics/Sentinel?
- Can it integrate with Databricks while preserving Unity Catalog authorization and audit trails?
- Can it apply policy to non-LangChain applications?
- How are prompt, retrieval index, model, tool-schema, and policy versions represented in release records?

## Gateway resiliency and enforcement precision

- Is the gateway zone- and region-redundant?
- What are gateway and end-to-end service SLOs, including p95/p99 latency?
- What latency does each control add: authentication, tracing, DLP/PII, prompt-injection inspection, tool authorization, and routing?
- What happens to streaming calls and in-flight requests during failover?
- Is there a tested control-plane outage mode using cached signed policies?
- Can applications bypass the gateway? If so, how is bypass restricted and audited?
- Are rate, token, and spend counters strongly consistent, eventually consistent, or configurable?
- What is the maximum possible budget overshoot under concurrent/multi-region traffic?
- Are budgets reserved before calls, estimated during streams, or reconciled after provider completion?
- What happens if the gateway’s budget/policy/telemetry store is unavailable?

## Fallback and model portability

- Which models are approved for each risk tier and data classification?
- Does fallback preserve required quality, structured output, tool calling, safety behavior, context limits, latency, and regional/data-processing requirements?
- Is a fallback model allowed to receive the same context/data as the primary endpoint?
- Can high-risk workflows be marked **no fallback / fail closed**?
- Are fallback decisions traceable and visible to operations teams/users where appropriate?
- Are provider-hosted variants of “the same” model evaluated as distinct deployments?

## Tool/MCP and agent-to-agent controls

- Is there an approved MCP/tool registry and owner for every integration?
- Are third-party/community MCP servers allowed? If so, what supply-chain review is required?
- Can agents dynamically discover tools, and how are unapproved tools prevented from execution?
- Are downstream business systems performing authorization independently of LLM prompts?
- How is original user context propagated in delegated flows?
- Can lower-trust agents invoke higher-privilege agents?
- Are write operations idempotent, checkpointed, and recoverable if a budget or model cap interrupts an agent mid-workflow?
- What compensating actions or human handoff exist after partial execution?

## Cost and operational ownership

No pricing or total-cost model is provided in the transcript. Assess:

- Gateway licensing or hosting costs.
- Log ingestion, retention, and high-cardinality trace costs.
- Evaluation dataset and execution costs.
- Multi-provider standby/egress costs.
- Additional cost from retries, timeouts, and fallback calls.
- Staffing for platform engineering, policy management, model evaluation, SecOps, and on-call support.
- Ownership of routing policy, model approval, budget thresholds, incident response, exceptions, and vendor management.

---

# Action items

1. **Define an AI agent risk taxonomy**
   - Low: internal summarization or approved non-sensitive knowledge retrieval.
   - Medium: employee assistants accessing governed business data.
   - High: customer-facing responses, account data, pricing, financial or operational workflow access.
   - Critical: autonomous customer-account, delivery, safety, or financial decisions; prohibit autonomy or require formal human/dual approval.

2. **Create a mandatory agent governance checklist**
   Include:
   - Business/technical ownership.
   - Data classification and permitted model endpoints.
   - Identity and delegated-access design.
   - Tool/MCP authorization matrix.
   - Human approval requirements.
   - Evaluation suite and release gates.
   - Logging/redaction/retention policy.
   - Cost, rate, token, and iteration limits.
   - Fallback/fail-open/fail-closed behavior.
   - Incident and rollback plan.

3. **Establish a reference architecture**
   - Use Entra ID and managed identities as the default identity model.
   - Use Key Vault for unavoidable secrets.
   - Preserve Unity Catalog/source-system authorization as the data-access authority.
   - Use Azure-native networking, monitoring, and SIEM controls as the foundation.
   - Evaluate whether Azure API Management, Azure AI Foundry capabilities, custom middleware, a specialized gateway, or a hybrid best meets requirements.

4. **Pilot a low-risk, read-only use case**
   Suggested pilot: internal knowledge or analytics assistant with:
   - Curated approved content.
   - No external web access.
   - No write/action tools.
   - Bounded evaluation corpus.
   - Trace redaction and controlled retention.
   - Explicit cost, latency, quality, and groundedness thresholds.

5. **Instrument end-to-end telemetry**
   Require correlated traces from:
   - User/application request.
   - Agent and sub-agent steps.
   - Model calls.
   - Retrieval.
   - Tool/MCP invocation.
   - Authorization decision.
   - Human approval.
   - Final business outcome.

6. **Implement minimum runtime guardrails**
   - Per-request token and time limits.
   - Maximum agent iterations, retries, tool calls, and delegation depth.
   - Per-agent/application/user rate limits.
   - Per-run/hour/day/month cost ceilings.
   - Circuit breakers and controlled retries.
   - Explicit human escalation when calls are blocked or uncertain.

7. **Create an approved tool/MCP registry**
   - Capture ownership, data scope, action tier, client agents, authentication, permitted operations, logging, and lifecycle status.
   - Require architecture/security review before production onboarding.
   - Restrict agents to allowlisted, narrow APIs.

8. **Run a LangSmith enterprise technical assessment**
   Request demonstration/documentation for:
   - Azure AI Foundry/Azure OpenAI integration.
   - Entra ID, managed identity, SSO, and SCIM.
   - Canadian residency/private networking.
   - Trace redaction before persistence.
   - RBAC, audit logs, SIEM export, and retention/deletion.
   - Gateway HA/DR, enforcement consistency, failover, and outage behavior.
   - Databricks/Unity Catalog interaction model.
   - Policy-as-code/versioning and environment promotion.
   - Full enterprise pricing and operational model.

9. **Benchmark middleware, gateway, and direct-call patterns**
   Measure direct Azure model calls against application middleware and any gateway candidate:
   - p50/p95/p99 latency and time-to-first-token.
   - Throughput and concurrency.
   - Incremental DLP/guardrail latency.
   - Availability and outage behavior.
   - Cost per request/workflow.
   - Budget-cap enforcement overshoot under loops and concurrent bursts.

10. **Do not enable autonomous high-impact actions initially**
   Keep account changes, pricing decisions, delivery/dispatch changes, financial commitments, and safety-related actions behind deterministic workflows and human approval until security, evaluation, transaction recovery, and operating controls have been proven.

## Full transcript

[00:13] Agents are a new kind of software.
[00:13] Agents are a new kind of software. Endless inputs and nondeterministic
[00:14] Endless inputs and nondeterministic
[00:14] Endless inputs and nondeterministic outputs. Build them the old way and they
[00:18] outputs. Build them the old way and they
[00:18] outputs. Build them the old way and they break.
[00:23] [music] Enter Langmith, the agent
[00:23] [music] Enter Langmith, the agent engineering platform. It's model
[00:25] engineering platform. It's model
[00:25] engineering platform. It's model agnostic, cloud agnostic, and framework
[00:28] agnostic, cloud agnostic, and framework
[00:28] agnostic, cloud agnostic, and framework agnostic. [music]
[00:30] agnostic. [music]
[00:30] agnostic. [music] Organizations shipping the best agents
[00:32] Organizations shipping the best agents
[00:32] Organizations shipping the best agents iterate with a system and we call that
[00:35] iterate with a system and we call that
[00:35] iterate with a system and we call that system the agent development life cycle.
[00:37] system the agent development life cycle.
[00:37] system the agent development life cycle. Build, test, deploy [music] and monitor.
[00:40] Build, test, deploy [music] and monitor.
[00:40] Build, test, deploy [music] and monitor. You build with our open source
[00:42] You build with our open source
[00:42] You build with our open source frameworks.
[00:44] frameworks.
[00:44] frameworks. Deep agents, Langchain or Langraph.
[00:47] Deep agents, Langchain or Langraph.
[00:47] Deep agents, Langchain or Langraph. Langmith fleet enables anyone to build
[00:49] Langmith fleet enables anyone to build
[00:50] Langmith fleet enables anyone to build agents [music]
[00:51] agents [music]
[00:51] agents [music] without code.
[00:58] Test agents using eval experiments.
[00:58] Test agents using eval experiments. &gt;&gt; [music]
[01:02] &gt;&gt; Deploy changes in one click with
[01:02] &gt;&gt; Deploy changes in one click with Langmith deployment.
[01:04] Langmith deployment.
[01:04] Langmith deployment. [music]
[01:10] Monitor every interaction from a single
[01:10] Monitor every interaction from a single dashboard.
[01:17] Governance is built into every stage of
[01:17] Governance is built into every stage of the agent development cycle [music] with
[01:19] the agent development cycle [music] with
[01:19] the agent development cycle [music] with Langmith O LM Gateway.
[01:22] Langmith O LM Gateway.
[01:22] Langmith O LM Gateway. Langsmith Engine helps you improve
[01:24] Langsmith Engine helps you improve
[01:24] Langsmith Engine helps you improve agents autonomously and move through the
[01:26] agents autonomously and move through the
[01:26] agents autonomously and move through the development life cycle more quickly.
[01:29] development life cycle more quickly.
[01:29] development life cycle more quickly. [music]
[01:31] [music]
[01:31] [music] Linksmith Engine is your agent for agent
[01:33] Linksmith Engine is your agent for agent
[01:33] Linksmith Engine is your agent for agent engineering.
[01:48] All right. Hi everyone. So excited to
[01:48] All right. Hi everyone. So excited to have you all here. Uh we're excited to
[01:51] have you all here. Uh we're excited to
[01:51] have you all here. Uh we're excited to talk about governance and building
[01:53] talk about governance and building
[01:53] talk about governance and building govern agents using lang chain and
[01:56] govern agents using lang chain and
[01:56] govern agents using lang chain and linksmith and the overall frameworks
[01:58] linksmith and the overall frameworks
[01:58] linksmith and the overall frameworks that you should consider as you think
[02:00] that you should consider as you think
[02:00] that you should consider as you think about cost control and compliance.
[02:05] about cost control and compliance.
[02:05] about cost control and compliance. I'm the product manager for our
[02:08] I'm the product manager for our
[02:08] I'm the product manager for our governance and LM gateway offering. I
[02:10] governance and LM gateway offering. I
[02:10] governance and LM gateway offering. I want to give a little bit of context for
[02:13] want to give a little bit of context for
[02:13] want to give a little bit of context for what we do here, who we are. So before
[02:16] what we do here, who we are. So before
[02:16] what we do here, who we are. So before we get into it, um, Langchain sits at
[02:19] we get into it, um, Langchain sits at
[02:19] we get into it, um, Langchain sits at the center of how a lot of teams are
[02:22] the center of how a lot of teams are
[02:22] the center of how a lot of teams are building agents. Langmith specifically
[02:24] building agents. Langmith specifically
[02:24] building agents. Langmith specifically is our platform for agent engineering.
[02:27] is our platform for agent engineering.
[02:27] is our platform for agent engineering. So we have over 7,000 active customers.
[02:30] So we have over 7,000 active customers.
[02:30] So we have over 7,000 active customers. Our open source frameworks are
[02:31] Our open source frameworks are
[02:31] Our open source frameworks are widespread with monthly downloads in the
[02:34] widespread with monthly downloads in the
[02:34] widespread with monthly downloads in the hundreds of millions.
[02:36] hundreds of millions.
[02:36] hundreds of millions. We work with also incredible companies
[02:38] We work with also incredible companies
[02:38] We work with also incredible companies as you can see all of the logos here. So
[02:40] as you can see all of the logos here. So
[02:40] as you can see all of the logos here. So anything from high growth startups like
[02:42] anything from high growth startups like
[02:42] anything from high growth startups like CLA and Ripling to large enterprises uh
[02:46] CLA and Ripling to large enterprises uh
[02:46] CLA and Ripling to large enterprises uh like Nvidia and Service Now were used by
[02:49] like Nvidia and Service Now were used by
[02:49] like Nvidia and Service Now were used by half of the Fortune 10 companies cutting
[02:52] half of the Fortune 10 companies cutting
[02:52] half of the Fortune 10 companies cutting across many regulated industries from uh
[02:56] across many regulated industries from uh
[02:56] across many regulated industries from uh HR to legal to financial services. So
[02:59] HR to legal to financial services. So
[02:59] HR to legal to financial services. So you can definitely trust us with your
[03:01] you can definitely trust us with your
[03:01] you can definitely trust us with your agent engineering.
[03:06] So today we're going to talk about why
[03:06] So today we're going to talk about why agent governance matters at all. Why are
[03:09] agent governance matters at all. Why are
[03:09] agent governance matters at all. Why are we here? Why are we thinking about this?
[03:11] we here? Why are we thinking about this?
[03:11] we here? Why are we thinking about this? Why are we lang chain working on this?
[03:14] Why are we lang chain working on this?
[03:14] Why are we lang chain working on this? So, we know that production agents
[03:16] So, we know that production agents
[03:16] So, we know that production agents introduce a different risk profile than
[03:19] introduce a different risk profile than
[03:19] introduce a different risk profile than traditional LLM apps. They have greater
[03:22] traditional LLM apps. They have greater
[03:22] traditional LLM apps. They have greater autonomy, meaning they have a greater
[03:24] autonomy, meaning they have a greater
[03:24] autonomy, meaning they have a greater need for visibility and control.
[03:27] need for visibility and control.
[03:27] need for visibility and control. Governance should enable teams to move
[03:29] Governance should enable teams to move
[03:29] Governance should enable teams to move faster, more safely. And it also with
[03:33] faster, more safely. And it also with
[03:34] faster, more safely. And it also with production agents in the mix, there's
[03:36] production agents in the mix, there's
[03:36] production agents in the mix, there's three main pressure costs that come up.
[03:38] three main pressure costs that come up.
[03:38] three main pressure costs that come up. There's cost, there's reliability, and
[03:41] There's cost, there's reliability, and
[03:41] There's cost, there's reliability, and then there's compliance.
[03:52] So, central policy enforcement becomes
[03:52] So, central policy enforcement becomes increasingly critical in this loop. We
[03:55] increasingly critical in this loop. We
[03:55] increasingly critical in this loop. We know that there is unpredictable spend
[03:58] know that there is unpredictable spend
[03:58] know that there is unpredictable spend that comes into the mix. So you know
[04:00] that comes into the mix. So you know
[04:00] that comes into the mix. So you know that agents can loop, they can retry,
[04:03] that agents can loop, they can retry,
[04:03] that agents can loop, they can retry, they can consume large contexts
[04:05] they can consume large contexts
[04:05] they can consume large contexts unexpectedly. Um so that makes cost
[04:08] unexpectedly. Um so that makes cost
[04:08] unexpectedly. Um so that makes cost harder to forecast.
[04:10] harder to forecast.
[04:10] harder to forecast. We also know that production agents need
[04:13] We also know that production agents need
[04:13] We also know that production agents need reliability. You need to make sure that
[04:15] reliability. You need to make sure that
[04:15] reliability. You need to make sure that when you send them out into the real
[04:17] when you send them out into the real
[04:17] when you send them out into the real world that they do things that you want
[04:19] world that they do things that you want
[04:19] world that they do things that you want them to do. So they need fallbacks, rate
[04:22] them to do. So they need fallbacks, rate
[04:22] them to do. So they need fallbacks, rate limits, and clear failure behavior that
[04:24] limits, and clear failure behavior that
[04:24] limits, and clear failure behavior that you can trace down and track to make
[04:26] you can trace down and track to make
[04:26] you can trace down and track to make sure that if something comes up, you can
[04:29] sure that if something comes up, you can
[04:29] sure that if something comes up, you can easily find the find what caused it and
[04:31] easily find the find what caused it and
[04:31] easily find the find what caused it and then fix it. And then finally,
[04:34] then fix it. And then finally,
[04:34] then fix it. And then finally, organizations need consistent documented
[04:37] organizations need consistent documented
[04:37] organizations need consistent documented policy enforcement and permissions.
[04:40] policy enforcement and permissions.
[04:40] policy enforcement and permissions. You need compliance in the loop to make
[04:42] You need compliance in the loop to make
[04:42] You need compliance in the loop to make sure that you're meeting all of your
[04:44] sure that you're meeting all of your
[04:44] sure that you're meeting all of your expected requirements wherever you are.
[04:48] expected requirements wherever you are.
[04:48] expected requirements wherever you are. So to sum it up, the key takeaway here
[04:50] So to sum it up, the key takeaway here
[04:50] So to sum it up, the key takeaway here is that these pressures create a need
[04:52] is that these pressures create a need
[04:52] is that these pressures create a need for centralized runtime controls rather
[04:55] for centralized runtime controls rather
[04:55] for centralized runtime controls rather than application by application
[04:57] than application by application
[04:57] than application by application policies, especially as you scale. And
[05:01] policies, especially as you scale. And
[05:01] policies, especially as you scale. And Langchain builds particularly towards
[05:03] Langchain builds particularly towards
[05:03] Langchain builds particularly towards that to make sure that at every step of
[05:05] that to make sure that at every step of
[05:05] that to make sure that at every step of the way from the beginning of your
[05:07] the way from the beginning of your
[05:07] the way from the beginning of your project as a solo developer all the way
[05:09] project as a solo developer all the way
[05:09] project as a solo developer all the way to a Fortune 10 company, we're by your
[05:12] to a Fortune 10 company, we're by your
[05:12] to a Fortune 10 company, we're by your side helping you on all three all three
[05:14] side helping you on all three all three
[05:14] side helping you on all three all three all three pillars.
[05:21] So governance as a whole, what are the
[05:21] So governance as a whole, what are the starting points to think about? Uh we
[05:23] starting points to think about? Uh we
[05:23] starting points to think about? Uh we think about it in five different areas.
[05:26] think about it in five different areas.
[05:26] think about it in five different areas. So on the first there is governance,
[05:28] So on the first there is governance,
[05:28] So on the first there is governance, there's the govern action, there's
[05:30] there's the govern action, there's
[05:30] there's the govern action, there's ownership, identity, risk tiers,
[05:32] ownership, identity, risk tiers,
[05:32] ownership, identity, risk tiers, policies to think about. Next, you're
[05:35] policies to think about. Next, you're
[05:35] policies to think about. Next, you're going to want to decide, you know,
[05:37] going to want to decide, you know,
[05:37] going to want to decide, you know, you're going to select models. You're
[05:38] you're going to select models. You're
[05:38] you're going to select models. You're going to figure out how to escalate.
[05:40] going to figure out how to escalate.
[05:40] going to figure out how to escalate. You're going to figure out when to fail
[05:41] You're going to figure out when to fail
[05:41] You're going to figure out when to fail over. So, you're going to make some
[05:43] over. So, you're going to make some
[05:44] over. So, you're going to make some decisions around how these models are
[05:46] decisions around how these models are
[05:46] decisions around how these models are going to act and how you're going to
[05:47] going to act and how you're going to
[05:47] going to act and how you're going to interact with them.
[05:49] interact with them.
[05:49] interact with them. Next, you need to think about protect
[05:51] Next, you need to think about protect
[05:51] Next, you need to think about protect protecting and enforcing controls at
[05:53] protecting and enforcing controls at
[05:53] protecting and enforcing controls at those interaction boundaries.
[05:56] those interaction boundaries.
[05:56] those interaction boundaries. After you do that, you're going to
[05:57] After you do that, you're going to
[05:57] After you do that, you're going to observe. You're going to measure
[05:58] observe. You're going to measure
[05:58] observe. You're going to measure behavior and outcomes. You're going to
[06:01] behavior and outcomes. You're going to
[06:01] behavior and outcomes. You're going to understand um understand what happened.
[06:05] understand um understand what happened.
[06:05] understand um understand what happened. And then finally, assure. So especially
[06:07] And then finally, assure. So especially
[06:07] And then finally, assure. So especially for those who are in more regulated
[06:08] for those who are in more regulated
[06:08] for those who are in more regulated industries, you need to make sure that
[06:10] industries, you need to make sure that
[06:10] industries, you need to make sure that there's evidence to manage changes over
[06:12] there's evidence to manage changes over
[06:12] there's evidence to manage changes over time. So even if you're a small
[06:14] time. So even if you're a small
[06:14] time. So even if you're a small engineer, you want to have a trace of
[06:16] engineer, you want to have a trace of
[06:16] engineer, you want to have a trace of what happened. If you're a large
[06:18] what happened. If you're a large
[06:18] what happened. If you're a large enterprise and you get audits or you
[06:20] enterprise and you get audits or you
[06:20] enterprise and you get audits or you have compliance requirements, you want
[06:22] have compliance requirements, you want
[06:22] have compliance requirements, you want to be able to assure those people who
[06:24] to be able to assure those people who
[06:24] to be able to assure those people who care that your agents are doing what
[06:26] care that your agents are doing what
[06:26] care that your agents are doing what they're expected to be doing.
[06:35] We also think of this as like part of
[06:35] We also think of this as like part of the life cycle and your Asian
[06:36] the life cycle and your Asian
[06:36] the life cycle and your Asian development life cycle, right? You build
[06:39] development life cycle, right? You build
[06:39] development life cycle, right? You build something, you test it, you deploy it,
[06:42] something, you test it, you deploy it,
[06:42] something, you test it, you deploy it, you monitor and governance falls within
[06:44] you monitor and governance falls within
[06:44] you monitor and governance falls within that entire cycle from the first step
[06:47] that entire cycle from the first step
[06:47] that entire cycle from the first step all the way to the end and as you loop
[06:48] all the way to the end and as you loop
[06:48] all the way to the end and as you loop back around to build some more. It
[06:51] back around to build some more. It
[06:51] back around to build some more. It touches on a lot of areas right across
[06:53] touches on a lot of areas right across
[06:53] touches on a lot of areas right across this life cycle. You're going to have
[06:55] this life cycle. You're going to have
[06:55] this life cycle. You're going to have things like cost controls. You're going
[06:56] things like cost controls. You're going
[06:56] things like cost controls. You're going to have to figure out tool access.
[06:59] to have to figure out tool access.
[06:59] to have to figure out tool access. You're going to think of audit trails.
[07:01] You're going to think of audit trails.
[07:01] You're going to think of audit trails. Human in the loop also needs governance
[07:03] Human in the loop also needs governance
[07:03] Human in the loop also needs governance and permissions, discoverability and who
[07:06] and permissions, discoverability and who
[07:06] and permissions, discoverability and who can use which tools, which which agents,
[07:08] can use which tools, which which agents,
[07:08] can use which tools, which which agents, which patterns. And then you want to
[07:11] which patterns. And then you want to
[07:11] which patterns. And then you want to share context skills across an
[07:13] share context skills across an
[07:13] share context skills across an organization, across your team in a way
[07:16] organization, across your team in a way
[07:16] organization, across your team in a way that is safe, auditable, auditable, and
[07:20] that is safe, auditable, auditable, and
[07:20] that is safe, auditable, auditable, and permissible.
[07:23] permissible.
[07:23] permissible. So what we want to make sure is that the
[07:25] So what we want to make sure is that the
[07:25] So what we want to make sure is that the key point here that falls in is that
[07:27] key point here that falls in is that
[07:27] key point here that falls in is that governance should really be part of how
[07:30] governance should really be part of how
[07:30] governance should really be part of how agents are built and how they're
[07:32] agents are built and how they're
[07:32] agents are built and how they're operated. It's really important that
[07:35] operated. It's really important that
[07:35] operated. It's really important that this falls into that main
[07:37] this falls into that main
[07:37] this falls into that main infrastructure.
[07:38] infrastructure.
[07:38] infrastructure. Problems come in when it's just bolted
[07:40] Problems come in when it's just bolted
[07:40] Problems come in when it's just bolted on because you miss that entire
[07:42] on because you miss that entire
[07:42] on because you miss that entire knowledge of step one all the way to
[07:44] knowledge of step one all the way to
[07:44] knowledge of step one all the way to step four. Um and in that you might miss
[07:48] step four. Um and in that you might miss
[07:48] step four. Um and in that you might miss really critical pathways. So you might
[07:50] really critical pathways. So you might
[07:50] really critical pathways. So you might miss really critical pathways that um
[07:54] miss really critical pathways that um
[07:54] miss really critical pathways that um your engineers need to fix and deploy
[07:56] your engineers need to fix and deploy
[07:56] your engineers need to fix and deploy later. In our case, we really think of
[07:59] later. In our case, we really think of
[07:59] later. In our case, we really think of it holistically and that the governance
[08:01] it holistically and that the governance
[08:01] it holistically and that the governance factors into every single aspect of how
[08:05] factors into every single aspect of how
[08:05] factors into every single aspect of how we build tools.
[08:14] &gt;&gt; So there's many areas of governance,
[08:14] &gt;&gt; So there's many areas of governance, right? I mean all the way from how your
[08:16] right? I mean all the way from how your
[08:16] right? I mean all the way from how your company signs on to how you measure
[08:19] company signs on to how you measure
[08:19] company signs on to how you measure permissions. All of those are really
[08:22] permissions. All of those are really
[08:22] permissions. All of those are really important areas of just using links as a
[08:24] important areas of just using links as a
[08:24] important areas of just using links as a whole. But then once you build those
[08:27] whole. But then once you build those
[08:27] whole. But then once you build those agents, you need to make sure that those
[08:29] agents, you need to make sure that those
[08:29] agents, you need to make sure that those interaction points with the outside
[08:31] interaction points with the outside
[08:31] interaction points with the outside world are measured and governed
[08:34] world are measured and governed
[08:34] world are measured and governed appropriately. So, while your ecosystem
[08:37] appropriately. So, while your ecosystem
[08:37] appropriately. So, while your ecosystem might be reliable and you know who's who
[08:39] might be reliable and you know who's who
[08:39] might be reliable and you know who's who and who's what within Langmith for
[08:41] and who's what within Langmith for
[08:41] and who's what within Langmith for instance or Lang Chain, as you start
[08:44] instance or Lang Chain, as you start
[08:44] instance or Lang Chain, as you start interacting with the outside world with
[08:46] interacting with the outside world with
[08:46] interacting with the outside world with an LLM, with an outside tool, with an
[08:49] an LLM, with an outside tool, with an
[08:49] an LLM, with an outside tool, with an MCP server, um, and as agents go talk to
[08:53] MCP server, um, and as agents go talk to
[08:53] MCP server, um, and as agents go talk to other agents, you need to make sure that
[08:55] other agents, you need to make sure that
[08:55] other agents, you need to make sure that you're authorizing and you're certain of
[08:58] you're authorizing and you're certain of
[08:58] you're authorizing and you're certain of how those calls are being made,
[09:00] how those calls are being made,
[09:00] how those calls are being made, especially when you don't have moment by
[09:02] especially when you don't have moment by
[09:02] especially when you don't have moment by moment a human in the loop, right? as
[09:05] moment a human in the loop, right? as
[09:05] moment a human in the loop, right? as those become more automated with AI,
[09:07] those become more automated with AI,
[09:07] those become more automated with AI, that's where really the pressure points
[09:08] that's where really the pressure points
[09:08] that's where really the pressure points start to come in. And as you start
[09:10] start to come in. And as you start
[09:10] start to come in. And as you start working at scale, that's where you start
[09:13] working at scale, that's where you start
[09:13] working at scale, that's where you start to see those moments where things could
[09:15] to see those moments where things could
[09:15] to see those moments where things could break or things could be unauthorized.
[09:18] break or things could be unauthorized.
[09:18] break or things could be unauthorized. And so the way that we think about it is
[09:20] And so the way that we think about it is
[09:20] And so the way that we think about it is across some various factors and we
[09:23] across some various factors and we
[09:23] across some various factors and we either have robust offerings here or
[09:24] either have robust offerings here or
[09:24] either have robust offerings here or building towards them. So the primary
[09:28] building towards them. So the primary
[09:28] building towards them. So the primary one is LM calls. This is the bread and
[09:30] one is LM calls. This is the bread and
[09:30] one is LM calls. This is the bread and butter of how AI works. It's calling out
[09:32] butter of how AI works. It's calling out
[09:32] butter of how AI works. It's calling out to the provider and saying, you know,
[09:35] to the provider and saying, you know,
[09:35] to the provider and saying, you know, making that LLM call to get um get some
[09:39] making that LLM call to get um get some
[09:39] making that LLM call to get um get some some AI back, right?
[09:42] some AI back, right?
[09:42] some AI back, right? When you're doing so, there's many
[09:44] When you're doing so, there's many
[09:44] When you're doing so, there's many things at risk. A way that we summarize
[09:45] things at risk. A way that we summarize
[09:45] things at risk. A way that we summarize it, and this is obviously not
[09:47] it, and this is obviously not
[09:47] it, and this is obviously not comprehensive, but to give examples and
[09:49] comprehensive, but to give examples and
[09:49] comprehensive, but to give examples and be as comprehensive as possible, we
[09:51] be as comprehensive as possible, we
[09:51] be as comprehensive as possible, we think about it on the side scale of
[09:53] think about it on the side scale of
[09:53] think about it on the side scale of cost. So, obviously, LLMs can become
[09:55] cost. So, obviously, LLMs can become
[09:56] cost. So, obviously, LLMs can become more expensive as context grows. Um
[09:59] more expensive as context grows. Um
[09:59] more expensive as context grows. Um those calls can become more expensive as
[10:02] those calls can become more expensive as
[10:02] those calls can become more expensive as models become more robust. They also the
[10:04] models become more robust. They also the
[10:04] models become more robust. They also the call gets more and more expensive as
[10:06] call gets more and more expensive as
[10:06] call gets more and more expensive as we've seen across some of the frontier
[10:07] we've seen across some of the frontier
[10:07] we've seen across some of the frontier providers.
[10:10] providers.
[10:10] providers. Model availability becomes also a crux.
[10:13] Model availability becomes also a crux.
[10:13] Model availability becomes also a crux. Your agent might become unavailable to
[10:16] Your agent might become unavailable to
[10:16] Your agent might become unavailable to your uh to your customers to your users
[10:19] your uh to your customers to your users
[10:19] your uh to your customers to your users to your internal staff because the
[10:21] to your internal staff because the
[10:22] to your internal staff because the provider went down the model went down
[10:24] provider went down the model went down
[10:24] provider went down the model went down credentials weren't verified. There's
[10:26] credentials weren't verified. There's
[10:26] credentials weren't verified. There's many reasons and they can have real
[10:28] many reasons and they can have real
[10:28] many reasons and they can have real production consequences.
[10:31] production consequences.
[10:31] production consequences. You think about private data, right? And
[10:33] You think about private data, right? And
[10:33] You think about private data, right? And you want to make sure that the LLM, the
[10:35] you want to make sure that the LLM, the
[10:35] you want to make sure that the LLM, the external model gets only the data that
[10:38] external model gets only the data that
[10:38] external model gets only the data that it should. And especially if you're
[10:40] it should. And especially if you're
[10:40] it should. And especially if you're working in a regulated industry or with
[10:42] working in a regulated industry or with
[10:42] working in a regulated industry or with sensitive data, you need to really be
[10:44] sensitive data, you need to really be
[10:44] sensitive data, you need to really be thinking about what data is going to
[10:46] thinking about what data is going to
[10:46] thinking about what data is going to these external providers. Particularly
[10:48] these external providers. Particularly
[10:48] these external providers. Particularly as your teams start to use a broader
[10:51] as your teams start to use a broader
[10:51] as your teams start to use a broader breath of LLMs and providers using
[10:54] breath of LLMs and providers using
[10:54] breath of LLMs and providers using openweight, not open weight, that data
[10:56] openweight, not open weight, that data
[10:56] openweight, not open weight, that data could really propagate across many
[10:58] could really propagate across many
[10:58] could really propagate across many different ecosystems. And so you want to
[11:00] different ecosystems. And so you want to
[11:00] different ecosystems. And so you want to be sure that only the things that you
[11:03] be sure that only the things that you
[11:03] be sure that only the things that you want to be going out that are
[11:04] want to be going out that are
[11:04] want to be going out that are unidentifiable are going out into the
[11:06] unidentifiable are going out into the
[11:06] unidentifiable are going out into the world.
[11:09] world.
[11:09] world. Typically, if you're trying to govern
[11:10] Typically, if you're trying to govern
[11:10] Typically, if you're trying to govern these, you're going to think of things
[11:11] these, you're going to think of things
[11:11] these, you're going to think of things like spend limits, redaction, routing.
[11:14] like spend limits, redaction, routing.
[11:14] like spend limits, redaction, routing. You're going to think about fallbacks
[11:16] You're going to think about fallbacks
[11:16] You're going to think about fallbacks and rate limits. You're going to want to
[11:18] and rate limits. You're going to want to
[11:18] and rate limits. You're going to want to make sure that your model your models
[11:20] make sure that your model your models
[11:20] make sure that your model your models are available when you need them and
[11:22] are available when you need them and
[11:22] are available when you need them and that you're staying within budget and
[11:23] that you're staying within budget and
[11:23] that you're staying within budget and you're being you're thinking about token
[11:26] you're being you're thinking about token
[11:26] you're being you're thinking about token optimization and economics as as those
[11:29] optimization and economics as as those
[11:29] optimization and economics as as those costs grow and as they become a more
[11:31] costs grow and as they become a more
[11:31] costs grow and as they become a more critical pathway in in decisions that
[11:34] critical pathway in in decisions that
[11:34] critical pathway in in decisions that you're making and access for your
[11:35] you're making and access for your
[11:35] you're making and access for your customers.
[11:43] Next on the scale um to a smaller extent
[11:43] Next on the scale um to a smaller extent but just as important
[11:45] but just as important
[11:45] but just as important tool calls also bring on risk and
[11:47] tool calls also bring on risk and
[11:47] tool calls also bring on risk and require governance right so there's
[11:50] require governance right so there's
[11:50] require governance right so there's unintended actions in production systems
[11:52] unintended actions in production systems
[11:52] unintended actions in production systems an unintended call or unauthorized call
[11:55] an unintended call or unauthorized call
[11:55] an unintended call or unauthorized call to a tool this person shouldn't have
[11:57] to a tool this person shouldn't have
[11:57] to a tool this person shouldn't have access to this tool or you know this
[12:00] access to this tool or you know this
[12:00] access to this tool or you know this type of prompt should only call this
[12:02] type of prompt should only call this
[12:02] type of prompt should only call this kind of tool. Those unintended actions
[12:04] kind of tool. Those unintended actions
[12:04] kind of tool. Those unintended actions can also bring in risks and are areas
[12:07] can also bring in risks and are areas
[12:07] can also bring in risks and are areas that you might want to think about
[12:08] that you might want to think about
[12:08] that you might want to think about governing. So typical typically what you
[12:11] governing. So typical typically what you
[12:11] governing. So typical typically what you might think about here is permissioning
[12:13] might think about here is permissioning
[12:13] might think about here is permissioning having an audit trail to make sure that
[12:14] having an audit trail to make sure that
[12:14] having an audit trail to make sure that you can see what tools were available
[12:17] you can see what tools were available
[12:17] you can see what tools were available who had permission to use them and
[12:19] who had permission to use them and
[12:19] who had permission to use them and access them and then once they were
[12:20] access them and then once they were
[12:20] access them and then once they were accessed how were they accessed.
[12:24] accessed how were they accessed.
[12:24] accessed how were they accessed. Another area is MCP calls. So similarly
[12:28] Another area is MCP calls. So similarly
[12:28] Another area is MCP calls. So similarly to LLM calls, this is once again data
[12:30] to LLM calls, this is once again data
[12:30] to LLM calls, this is once again data leaving your infrastructure boundary and
[12:33] leaving your infrastructure boundary and
[12:33] leaving your infrastructure boundary and you need to also be sure that the data
[12:35] you need to also be sure that the data
[12:35] you need to also be sure that the data that is leaving is both authorized, who
[12:37] that is leaving is both authorized, who
[12:37] that is leaving is both authorized, who has access to which MCPs and how are
[12:41] has access to which MCPs and how are
[12:41] has access to which MCPs and how are they being used, what MCPs are even
[12:43] they being used, what MCPs are even
[12:43] they being used, what MCPs are even available. Those are all critical areas
[12:45] available. Those are all critical areas
[12:45] available. Those are all critical areas of governance. And you're going to think
[12:47] of governance. And you're going to think
[12:47] of governance. And you're going to think about access control and logging once
[12:49] about access control and logging once
[12:49] about access control and logging once again.
[12:51] again.
[12:51] again. And then finally, um, agents are
[12:54] And then finally, um, agents are
[12:54] And then finally, um, agents are starting to call more agents, not just
[12:56] starting to call more agents, not just
[12:56] starting to call more agents, not just calling a provider directly, but your
[12:57] calling a provider directly, but your
[12:57] calling a provider directly, but your agent might call another agent or a sub
[12:59] agent might call another agent or a sub
[12:59] agent might call another agent or a sub agent. And you need to figure out what
[13:02] agent. And you need to figure out what
[13:02] agent. And you need to figure out what is the identity allowed. What is
[13:04] is the identity allowed. What is
[13:04] is the identity allowed. What is identity of this agent? What is this
[13:05] identity of this agent? What is this
[13:05] identity of this agent? What is this agent allowed to do? Which other agents
[13:07] agent allowed to do? Which other agents
[13:08] agent allowed to do? Which other agents is it allowed to call? Do they take on
[13:10] is it allowed to call? Do they take on
[13:10] is it allowed to call? Do they take on the identities of the existing agent
[13:13] the identities of the existing agent
[13:13] the identities of the existing agent that you that exists, the existing
[13:15] that you that exists, the existing
[13:15] that you that exists, the existing person who's making the call or do they
[13:17] person who's making the call or do they
[13:17] person who's making the call or do they have other permissions altogether? And
[13:19] have other permissions altogether? And
[13:19] have other permissions altogether? And this is where you might start seeing
[13:20] this is where you might start seeing
[13:20] this is where you might start seeing compounding errors because this really
[13:22] compounding errors because this really
[13:22] compounding errors because this really can scale up and snowball. So um you
[13:27] can scale up and snowball. So um you
[13:27] can scale up and snowball. So um you know those errors grow and snowball. You
[13:30] know those errors grow and snowball. You
[13:30] know those errors grow and snowball. You might get unauthorized access across
[13:32] might get unauthorized access across
[13:32] might get unauthorized access across those agent chains and especially as
[13:34] those agent chains and especially as
[13:34] those agent chains and especially as they start talking to each other. You
[13:36] they start talking to each other. You
[13:36] they start talking to each other. You can imagine that chain continuing for
[13:38] can imagine that chain continuing for
[13:38] can imagine that chain continuing for many agents before um before somebody
[13:41] many agents before um before somebody
[13:41] many agents before um before somebody catches it if you don't have the right
[13:43] catches it if you don't have the right
[13:43] catches it if you don't have the right governance layers in place. So here you
[13:45] governance layers in place. So here you
[13:45] governance layers in place. So here you might think about tracing policy
[13:47] might think about tracing policy
[13:47] might think about tracing policy enforcement and thinking about agent
[13:49] enforcement and thinking about agent
[13:49] enforcement and thinking about agent identity of how how that plays out for
[13:52] identity of how how that plays out for
[13:52] identity of how how that plays out for your individual agents and what
[13:54] your individual agents and what
[13:54] your individual agents and what permissions they take on.
[14:03] Now enforcing governance, right? So
[14:03] Now enforcing governance, right? So those are we've talked about like the
[14:04] those are we've talked about like the
[14:04] those are we've talked about like the areas where you might want to think
[14:05] areas where you might want to think
[14:06] areas where you might want to think about this. We've talked about um the
[14:10] about this. We've talked about um the
[14:10] about this. We've talked about um the types where this falls into the agent
[14:12] types where this falls into the agent
[14:12] types where this falls into the agent development life cycle. But now you kind
[14:14] development life cycle. But now you kind
[14:14] development life cycle. But now you kind of want to actually enforce it and what
[14:16] of want to actually enforce it and what
[14:16] of want to actually enforce it and what are the the areas and how to think about
[14:17] are the the areas and how to think about
[14:17] are the the areas and how to think about it. So three main considerations are
[14:21] it. So three main considerations are
[14:21] it. So three main considerations are around cost, integration and adoption.
[14:25] around cost, integration and adoption.
[14:25] around cost, integration and adoption. So to start um there's areas around cost
[14:28] So to start um there's areas around cost
[14:28] So to start um there's areas around cost and risk, right? So while building a
[14:31] and risk, right? So while building a
[14:31] and risk, right? So while building a simple proxy is really easy, maintaining
[14:34] simple proxy is really easy, maintaining
[14:34] simple proxy is really easy, maintaining controls and integrations and guard
[14:35] controls and integrations and guard
[14:36] controls and integrations and guard rails is harder. So you might want to
[14:38] rails is harder. So you might want to
[14:38] rails is harder. So you might want to think about um building versus
[14:41] think about um building versus
[14:41] think about um building versus maintaining, right? So there's ways to
[14:44] maintaining, right? So there's ways to
[14:44] maintaining, right? So there's ways to build in governance across the areas
[14:46] build in governance across the areas
[14:46] build in governance across the areas that I talked about previously and many
[14:49] that I talked about previously and many
[14:49] that I talked about previously and many companies build just their own proxies,
[14:52] companies build just their own proxies,
[14:52] companies build just their own proxies, build their own gateways for instance to
[14:55] build their own gateways for instance to
[14:55] build their own gateways for instance to manage those interactions or build them
[14:57] manage those interactions or build them
[14:57] manage those interactions or build them even into their agents themselves. And
[15:00] even into their agents themselves. And
[15:00] even into their agents themselves. And so you know a basic forwarder is simple,
[15:02] so you know a basic forwarder is simple,
[15:02] so you know a basic forwarder is simple, basic permissions are simple. When your
[15:04] basic permissions are simple. When your
[15:04] basic permissions are simple. When your company is three people, it's really
[15:06] company is three people, it's really
[15:06] company is three people, it's really easy to make sure that you're doing the
[15:08] easy to make sure that you're doing the
[15:08] easy to make sure that you're doing the right thing. But as you scale, that's
[15:10] right thing. But as you scale, that's
[15:10] right thing. But as you scale, that's where the real effort can come in and
[15:12] where the real effort can come in and
[15:12] where the real effort can come in and making sure that across your go your
[15:14] making sure that across your go your
[15:14] making sure that across your go your company, across your system. Um, you've
[15:17] company, across your system. Um, you've
[15:17] company, across your system. Um, you've really thought about across the board
[15:20] really thought about across the board
[15:20] really thought about across the board who is allowed to do what and that
[15:21] who is allowed to do what and that
[15:21] who is allowed to do what and that becomes just much harder once you reach
[15:23] becomes just much harder once you reach
[15:23] becomes just much harder once you reach the 100 to 200 person threshold. Um, and
[15:27] the 100 to 200 person threshold. Um, and
[15:27] the 100 to 200 person threshold. Um, and you have many different styles, you have
[15:29] you have many different styles, you have
[15:29] you have many different styles, you have many different models at play, you have
[15:31] many different models at play, you have
[15:31] many different models at play, you have many different agents at play, many
[15:33] many different agents at play, many
[15:33] many different agents at play, many different development styles. Um, so
[15:36] different development styles. Um, so
[15:36] different development styles. Um, so thinking about that as as you kind of
[15:38] thinking about that as as you kind of
[15:38] thinking about that as as you kind of consider how to apply this governance.
[15:41] consider how to apply this governance.
[15:42] consider how to apply this governance. Then with guardrails themselves, not
[15:43] Then with guardrails themselves, not
[15:44] Then with guardrails themselves, not everyone cares about them. You know,
[15:46] everyone cares about them. You know,
[15:46] everyone cares about them. You know, it's really the more regulated
[15:47] it's really the more regulated
[15:47] it's really the more regulated industries typically or or customers who
[15:50] industries typically or or customers who
[15:50] industries typically or or customers who are in um in more regulated parts of the
[15:53] are in um in more regulated parts of the
[15:53] are in um in more regulated parts of the world. Um they they might require
[15:56] world. Um they they might require
[15:56] world. Um they they might require guardrails. So thinking about um for
[15:58] guardrails. So thinking about um for
[15:58] guardrails. So thinking about um for instance secret detection and redaction,
[16:00] instance secret detection and redaction,
[16:00] instance secret detection and redaction, PII detection and redaction, other areas
[16:03] PII detection and redaction, other areas
[16:03] PII detection and redaction, other areas where you might want to make sure that
[16:04] where you might want to make sure that
[16:04] where you might want to make sure that your agents are behaving appropriately,
[16:06] your agents are behaving appropriately,
[16:06] your agents are behaving appropriately, various guard rails, those require
[16:08] various guard rails, those require
[16:08] various guard rails, those require precise optimization to eliminate false
[16:11] precise optimization to eliminate false
[16:11] precise optimization to eliminate false positives on those critical data. So
[16:13] positives on those critical data. So
[16:13] positives on those critical data. So you'd have to think about how to tune,
[16:14] you'd have to think about how to tune,
[16:14] you'd have to think about how to tune, how to make that available. The models
[16:17] how to make that available. The models
[16:17] how to make that available. The models themselves, even though there are many
[16:18] themselves, even though there are many
[16:18] themselves, even though there are many models out there, um it takes work to
[16:20] models out there, um it takes work to
[16:20] models out there, um it takes work to actually make sure that they're doing
[16:21] actually make sure that they're doing
[16:21] actually make sure that they're doing things correctly and that you're you're
[16:23] things correctly and that you're you're
[16:23] things correctly and that you're you're able to adjust them to your needs.
[16:26] able to adjust them to your needs.
[16:26] able to adjust them to your needs. And then finally, there's just the
[16:27] And then finally, there's just the
[16:27] And then finally, there's just the operational risk in setting this kind of
[16:29] operational risk in setting this kind of
[16:29] operational risk in setting this kind of governance up, right? If you're running
[16:31] governance up, right? If you're running
[16:31] governance up, right? If you're running a custom control plane, this while it
[16:34] a custom control plane, this while it
[16:34] a custom control plane, this while it might be easy to build it at the
[16:35] might be easy to build it at the
[16:36] might be easy to build it at the beginning, it introduces long-term
[16:37] beginning, it introduces long-term
[16:37] beginning, it introduces long-term costs, operational overhead, you have to
[16:40] costs, operational overhead, you have to
[16:40] costs, operational overhead, you have to have a team that's always monitoring it
[16:42] have a team that's always monitoring it
[16:42] have a team that's always monitoring it because this sits in your runtime. You
[16:45] because this sits in your runtime. You
[16:45] because this sits in your runtime. You know, you you need to be always on top
[16:47] know, you you need to be always on top
[16:47] know, you you need to be always on top of it if you're managing this kind of
[16:49] of it if you're managing this kind of
[16:49] of it if you're managing this kind of centralized tool. And we've seen this
[16:51] centralized tool. And we've seen this
[16:51] centralized tool. And we've seen this ourselves internally. We built a gateway
[16:54] ourselves internally. We built a gateway
[16:54] ourselves internally. We built a gateway that we've been using ourselves and
[16:55] that we've been using ourselves and
[16:56] that we've been using ourselves and there's a lot of work that goes into
[16:57] there's a lot of work that goes into
[16:57] there's a lot of work that goes into just making sure that even works for our
[16:58] just making sure that even works for our
[16:58] just making sure that even works for our own staff.
[17:01] own staff.
[17:01] own staff. Next, you're going to think about
[17:02] Next, you're going to think about
[17:02] Next, you're going to think about integration and integration in the
[17:04] integration and integration in the
[17:04] integration and integration in the broader agent stack, right? So,
[17:07] broader agent stack, right? So,
[17:07] broader agent stack, right? So, you're going to want to have full
[17:08] you're going to want to have full
[17:08] you're going to want to have full context on what calls happen, what
[17:11] context on what calls happen, what
[17:11] context on what calls happen, what agents did. Um, traces are a great way
[17:14] agents did. Um, traces are a great way
[17:14] agents did. Um, traces are a great way of managing that and noticing and
[17:16] of managing that and noticing and
[17:16] of managing that and noticing and debugging. You're able to set alerts
[17:19] debugging. You're able to set alerts
[17:19] debugging. You're able to set alerts when when certain things happen, when
[17:21] when when certain things happen, when
[17:21] when when certain things happen, when thresholds are passed. um and able to
[17:23] thresholds are passed. um and able to
[17:24] thresholds are passed. um and able to refer afterwards and see an aggregate
[17:26] refer afterwards and see an aggregate
[17:26] refer afterwards and see an aggregate potentially through evaluations how your
[17:29] potentially through evaluations how your
[17:29] potentially through evaluations how your agents behaved and if there are certain
[17:30] agents behaved and if there are certain
[17:30] agents behaved and if there are certain patterns that are inappropriate.
[17:37] You also might want to match this into
[17:37] You also might want to match this into monitoring and make sure that you put
[17:39] monitoring and make sure that you put
[17:39] monitoring and make sure that you put this into insights. So evolves are one
[17:41] this into insights. So evolves are one
[17:41] this into insights. So evolves are one way, general pattern noticing using
[17:44] way, general pattern noticing using
[17:44] way, general pattern noticing using tools within Langsmith for instance like
[17:46] tools within Langsmith for instance like
[17:46] tools within Langsmith for instance like engine if if you're doing so gives you
[17:49] engine if if you're doing so gives you
[17:49] engine if if you're doing so gives you the ability to notice those patterns as
[17:51] the ability to notice those patterns as
[17:51] the ability to notice those patterns as effectively as possible.
[17:54] effectively as possible.
[17:54] effectively as possible. And then finally there's instant
[17:56] And then finally there's instant
[17:56] And then finally there's instant debugging. So if there's an issue, if
[17:59] debugging. So if there's an issue, if
[17:59] debugging. So if there's an issue, if you suddenly have a runaway loop, you're
[18:01] you suddenly have a runaway loop, you're
[18:01] you suddenly have a runaway loop, you're going to want to be able to quickly and
[18:03] going to want to be able to quickly and
[18:03] going to want to be able to quickly and easily discover it, notice those policy
[18:06] easily discover it, notice those policy
[18:06] easily discover it, notice those policy violations, and inspect what happened.
[18:09] violations, and inspect what happened.
[18:09] violations, and inspect what happened. And especially if you're using
[18:11] And especially if you're using
[18:11] And especially if you're using centralized tool and centralized
[18:13] centralized tool and centralized
[18:13] centralized tool and centralized governance, you're going to want to make
[18:15] governance, you're going to want to make
[18:15] governance, you're going to want to make sure that it's not just the agents
[18:16] sure that it's not just the agents
[18:16] sure that it's not just the agents themselves that have that sort of
[18:18] themselves that have that sort of
[18:18] themselves that have that sort of monitoring, but those centralized tools
[18:20] monitoring, but those centralized tools
[18:20] monitoring, but those centralized tools should emit their own their own logs or
[18:24] should emit their own their own logs or
[18:24] should emit their own their own logs or traces to ensure that you can see
[18:27] traces to ensure that you can see
[18:27] traces to ensure that you can see whether the tool itself is also
[18:29] whether the tool itself is also
[18:29] whether the tool itself is also malfunctioning.
[18:31] malfunctioning.
[18:31] malfunctioning. And then finally, there's adoption. If
[18:33] And then finally, there's adoption. If
[18:33] And then finally, there's adoption. If you're just one person or a small team
[18:35] you're just one person or a small team
[18:35] you're just one person or a small team of three, then it's relatively easy to
[18:36] of three, then it's relatively easy to
[18:36] of three, then it's relatively easy to make sure you have access to the models
[18:38] make sure you have access to the models
[18:38] make sure you have access to the models that you need. And typically you're
[18:39] that you need. And typically you're
[18:39] that you need. And typically you're going to have a smaller scale of what
[18:41] going to have a smaller scale of what
[18:41] going to have a smaller scale of what those models are. But as you scale,
[18:43] those models are. But as you scale,
[18:43] those models are. But as you scale, you're going to really want to make sure
[18:44] you're going to really want to make sure
[18:44] you're going to really want to make sure that your system is configured for all
[18:47] that your system is configured for all
[18:47] that your system is configured for all of the types of models and all the
[18:49] of the types of models and all the
[18:49] of the types of models and all the configurations that might be possible,
[18:50] configurations that might be possible,
[18:50] configurations that might be possible, right? So you might want to have a
[18:53] right? So you might want to have a
[18:54] right? So you might want to have a seamless endpoint swap, right? So
[18:56] seamless endpoint swap, right? So
[18:56] seamless endpoint swap, right? So beginning adoption by updating the
[18:58] beginning adoption by updating the
[18:58] beginning adoption by updating the provider endpoint, point directly to
[19:00] provider endpoint, point directly to
[19:00] provider endpoint, point directly to administrative tools, right? Make sure
[19:02] administrative tools, right? Make sure
[19:02] administrative tools, right? Make sure that that it points to a gateway to
[19:04] that that it points to a gateway to
[19:04] that that it points to a gateway to other tools that centralize that. And
[19:07] other tools that centralize that. And
[19:07] other tools that centralize that. And you're going to want to make sure that
[19:08] you're going to want to make sure that
[19:08] you're going to want to make sure that it's as easy as possible for engineers
[19:10] it's as easy as possible for engineers
[19:10] it's as easy as possible for engineers to apply it to agents that they're
[19:12] to apply it to agents that they're
[19:12] to apply it to agents that they're building.
[19:18] The models themselves, uh, you want to
[19:18] The models themselves, uh, you want to make sure that securely you're managing
[19:20] make sure that securely you're managing
[19:20] make sure that securely you're managing their credentials, that your systems are
[19:23] their credentials, that your systems are
[19:23] their credentials, that your systems are fully accustomed and able to take in a
[19:26] fully accustomed and able to take in a
[19:26] fully accustomed and able to take in a variety of models. What we've seen
[19:28] variety of models. What we've seen
[19:28] variety of models. What we've seen across our customers and our use cases
[19:30] across our customers and our use cases
[19:30] across our customers and our use cases is that it's not just the frontier
[19:33] is that it's not just the frontier
[19:33] is that it's not just the frontier models that people are using.
[19:35] models that people are using.
[19:35] models that people are using. Increasingly there is desire for openw
[19:37] Increasingly there is desire for openw
[19:37] Increasingly there is desire for openw weight models or swapping or even
[19:40] weight models or swapping or even
[19:40] weight models or swapping or even swapping based on certain signals right
[19:42] swapping based on certain signals right
[19:42] swapping based on certain signals right so this model for this or cheap model
[19:44] so this model for this or cheap model
[19:44] so this model for this or cheap model for this type of work and you want to
[19:46] for this type of work and you want to
[19:46] for this type of work and you want to make sure that's as easy as possible. So
[19:48] make sure that's as easy as possible. So
[19:48] make sure that's as easy as possible. So saving the credentials in some
[19:50] saving the credentials in some
[19:50] saving the credentials in some centralized way within a centralized
[19:52] centralized way within a centralized
[19:52] centralized way within a centralized platform really helps with that.
[19:58] And then finally there's cohesive
[19:58] And then finally there's cohesive governance right so you want to make
[20:00] governance right so you want to make
[20:00] governance right so you want to make sure that that system where all this is
[20:02] sure that that system where all this is
[20:02] sure that that system where all this is playing out is trustworthy. You want to
[20:05] playing out is trustworthy. You want to
[20:05] playing out is trustworthy. You want to make sure that you're not duplicating
[20:07] make sure that you're not duplicating
[20:07] make sure that you're not duplicating governance that your roles and
[20:09] governance that your roles and
[20:09] governance that your roles and responsibilities that you set up, you
[20:10] responsibilities that you set up, you
[20:10] responsibilities that you set up, you don't have to duplicate in multiple
[20:12] don't have to duplicate in multiple
[20:12] don't have to duplicate in multiple systems. Ideally, you set this up once
[20:15] systems. Ideally, you set this up once
[20:16] systems. Ideally, you set this up once and then you have all the tools that you
[20:17] and then you have all the tools that you
[20:17] and then you have all the tools that you need in one place to apply them to all
[20:19] need in one place to apply them to all
[20:19] need in one place to apply them to all the different settings and situations
[20:21] the different settings and situations
[20:21] the different settings and situations where they might apply. So critical
[20:23] where they might apply. So critical
[20:23] where they might apply. So critical points there um in terms of how to think
[20:25] points there um in terms of how to think
[20:25] points there um in terms of how to think about basically how to apply this kind
[20:28] about basically how to apply this kind
[20:28] about basically how to apply this kind of governance in your ecosystem, how to
[20:30] of governance in your ecosystem, how to
[20:30] of governance in your ecosystem, how to enforce it um and some considerations
[20:32] enforce it um and some considerations
[20:32] enforce it um and some considerations for you know how that might apply to
[20:34] for you know how that might apply to
[20:34] for you know how that might apply to your system or to your structure and
[20:36] your system or to your structure and
[20:36] your system or to your structure and ecosystem based on the size you are the
[20:38] ecosystem based on the size you are the
[20:38] ecosystem based on the size you are the scale you are and how much effort it
[20:40] scale you are and how much effort it
[20:40] scale you are and how much effort it might take to apply that governance.
[20:49] Next is just reliability, right? You
[20:49] Next is just reliability, right? You want to make sure that a gateway or a
[20:52] want to make sure that a gateway or a
[20:52] want to make sure that a gateway or a central management structure is reliable
[20:55] central management structure is reliable
[20:55] central management structure is reliable under your production loads. And this
[20:58] under your production loads. And this
[20:58] under your production loads. And this obviously matters with scale and
[20:59] obviously matters with scale and
[20:59] obviously matters with scale and especially with many agents running. You
[21:01] especially with many agents running. You
[21:01] especially with many agents running. You want to make sure that everything that
[21:03] want to make sure that everything that
[21:03] want to make sure that everything that you're running through any sort of
[21:05] you're running through any sort of
[21:05] you're running through any sort of governance platform can take the load.
[21:08] governance platform can take the load.
[21:08] governance platform can take the load. So there's resilience and this comes
[21:10] So there's resilience and this comes
[21:10] So there's resilience and this comes through like many factors, right? So
[21:11] through like many factors, right? So
[21:11] through like many factors, right? So there's resilience, there's routing
[21:13] there's resilience, there's routing
[21:13] there's resilience, there's routing limits, there's cost and access and
[21:15] limits, there's cost and access and
[21:15] limits, there's cost and access and making sure that everything's accurate
[21:17] making sure that everything's accurate
[21:17] making sure that everything's accurate and how you're measuring it. So on the
[21:20] and how you're measuring it. So on the
[21:20] and how you're measuring it. So on the resilient side, uh you don't want to
[21:22] resilient side, uh you don't want to
[21:22] resilient side, uh you don't want to have a single point of failure because
[21:24] have a single point of failure because
[21:24] have a single point of failure because it sits in the critical path. You need
[21:25] it sits in the critical path. You need
[21:26] it sits in the critical path. You need to make sure that there's redundancy,
[21:28] to make sure that there's redundancy,
[21:28] to make sure that there's redundancy, that there's failovers, and that there's
[21:30] that there's failovers, and that there's
[21:30] that there's failovers, and that there's mechanics to ensure that your production
[21:33] mechanics to ensure that your production
[21:33] mechanics to ensure that your production agents will never go down, that your
[21:37] agents will never go down, that your
[21:38] agents will never go down, that your internal agents keep on working so your
[21:40] internal agents keep on working so your
[21:40] internal agents keep on working so your employees can work, that your engineers
[21:42] employees can work, that your engineers
[21:42] employees can work, that your engineers don't get stopped with unnecessary
[21:46] don't get stopped with unnecessary
[21:46] don't get stopped with unnecessary provider outages or cost controls that
[21:49] provider outages or cost controls that
[21:49] provider outages or cost controls that are blocking them from using it. So this
[21:51] are blocking them from using it. So this
[21:51] are blocking them from using it. So this can be done through things like
[21:52] can be done through things like
[21:52] can be done through things like timeouts, through balancing loads. You
[21:55] timeouts, through balancing loads. You
[21:55] timeouts, through balancing loads. You know, being explicit about which types
[21:57] know, being explicit about which types
[21:58] know, being explicit about which types of measurements should fail open or fail
[22:00] of measurements should fail open or fail
[22:00] of measurements should fail open or fail closed. Adding those types of
[22:02] closed. Adding those types of
[22:02] closed. Adding those types of determinations
[22:04] determinations
[22:04] determinations at the front helps you both be
[22:06] at the front helps you both be
[22:06] at the front helps you both be predictable in what works when with your
[22:09] predictable in what works when with your
[22:09] predictable in what works when with your teams that they understand what
[22:11] teams that they understand what
[22:11] teams that they understand what mechanics are at play, but then also
[22:14] mechanics are at play, but then also
[22:14] mechanics are at play, but then also make sure that you're ready for all
[22:15] make sure that you're ready for all
[22:15] make sure that you're ready for all scenarios regardless of what will
[22:17] scenarios regardless of what will
[22:17] scenarios regardless of what will happen.
[22:22] And then finally, it's just ma
[22:22] And then finally, it's just ma maintaining
[22:24] maintaining
[22:24] maintaining effective available centralized
[22:26] effective available centralized
[22:26] effective available centralized governance and making sure that it's
[22:27] governance and making sure that it's
[22:28] governance and making sure that it's always up and running. Um, and you've
[22:29] always up and running. Um, and you've
[22:29] always up and running. Um, and you've thought through that as well. So with
[22:32] thought through that as well. So with
[22:32] thought through that as well. So with routing on limits, um, you know, I what
[22:34] routing on limits, um, you know, I what
[22:34] routing on limits, um, you know, I what I mentioned in terms of resilience
[22:36] I mentioned in terms of resilience
[22:36] I mentioned in terms of resilience applies here too. So you have automatic
[22:38] applies here too. So you have automatic
[22:38] applies here too. So you have automatic failovers. If a model provider is out,
[22:43] failovers. If a model provider is out,
[22:43] failovers. If a model provider is out, if they're timed out, if they've reached
[22:46] if they're timed out, if they've reached
[22:46] if they're timed out, if they've reached a budget, if they've been rate limited,
[22:49] a budget, if they've been rate limited,
[22:49] a budget, if they've been rate limited, you need to make sure there's one or two
[22:51] you need to make sure there's one or two
[22:51] you need to make sure there's one or two models that are ready and tuned to the
[22:54] models that are ready and tuned to the
[22:54] models that are ready and tuned to the use case and ready to go as a backup in
[22:57] use case and ready to go as a backup in
[22:57] use case and ready to go as a backup in those scenarios. Even sometimes the same
[22:59] those scenarios. Even sometimes the same
[22:59] those scenarios. Even sometimes the same model through a different provider,
[23:01] model through a different provider,
[23:01] model through a different provider, right? So often what we see is customers
[23:03] right? So often what we see is customers
[23:03] right? So often what we see is customers who have Frontier models that they're
[23:05] who have Frontier models that they're
[23:05] who have Frontier models that they're using for like a production agent, but
[23:07] using for like a production agent, but
[23:07] using for like a production agent, but they might have them through like
[23:08] they might have them through like
[23:08] they might have them through like Bedrock for instance that um that acts
[23:11] Bedrock for instance that um that acts
[23:11] Bedrock for instance that um that acts as a backup, exact same model um tuned
[23:14] as a backup, exact same model um tuned
[23:14] as a backup, exact same model um tuned in the same way, but just coming from a
[23:16] in the same way, but just coming from a
[23:16] in the same way, but just coming from a different source just in case something
[23:17] different source just in case something
[23:17] different source just in case something goes out.
[23:20] goes out.
[23:20] goes out. You also want to set rate limits. Um, so
[23:24] You also want to set rate limits. Um, so
[23:24] You also want to set rate limits. Um, so a lot of a lot of customers we see just
[23:26] a lot of a lot of customers we see just
[23:26] a lot of a lot of customers we see just set them within the agents themselves.
[23:27] set them within the agents themselves.
[23:28] set them within the agents themselves. But if you have many going out of time
[23:29] But if you have many going out of time
[23:29] But if you have many going out of time or you have entire teams that are
[23:31] or you have entire teams that are
[23:31] or you have entire teams that are working together, uh, you want to make
[23:32] working together, uh, you want to make
[23:32] working together, uh, you want to make sure that you you enforce those partly
[23:35] sure that you you enforce those partly
[23:35] sure that you you enforce those partly obviously to catch runaway loops or
[23:37] obviously to catch runaway loops or
[23:37] obviously to catch runaway loops or agents that are misbehaving or sudden
[23:40] agents that are misbehaving or sudden
[23:40] agents that are misbehaving or sudden spikes of of traffic, but you actually
[23:43] spikes of of traffic, but you actually
[23:43] spikes of of traffic, but you actually also want to make sure that you don't
[23:44] also want to make sure that you don't
[23:44] also want to make sure that you don't hit the rate limits of your providers,
[23:47] hit the rate limits of your providers,
[23:47] hit the rate limits of your providers, right? You want to make sure that those
[23:49] right? You want to make sure that those
[23:49] right? You want to make sure that those continue to be accessible because
[23:50] continue to be accessible because
[23:50] continue to be accessible because there's many providers out there that
[23:52] there's many providers out there that
[23:52] there's many providers out there that when you hit their limit rate limit, uh
[23:54] when you hit their limit rate limit, uh
[23:54] when you hit their limit rate limit, uh you're out for some amount of time and
[23:56] you're out for some amount of time and
[23:56] you're out for some amount of time and that could be a real problem when you're
[23:58] that could be a real problem when you're
[23:58] that could be a real problem when you're trying to provide a product to your
[24:01] trying to provide a product to your
[24:01] trying to provide a product to your customers.
[24:03] customers.
[24:03] customers. And then finally, there's cost and
[24:05] And then finally, there's cost and
[24:05] And then finally, there's cost and access, right? So there's you want to
[24:07] access, right? So there's you want to
[24:07] access, right? So there's you want to make sure that what you're if you're
[24:09] make sure that what you're if you're
[24:09] make sure that what you're if you're especially if you're managing budgets
[24:10] especially if you're managing budgets
[24:10] especially if you're managing budgets and you care about budget management
[24:12] and you care about budget management
[24:12] and you care about budget management through something that through
[24:13] through something that through
[24:13] through something that through centralized governments uh you want to
[24:16] centralized governments uh you want to
[24:16] centralized governments uh you want to make sure that how you're measuring that
[24:18] make sure that how you're measuring that
[24:18] make sure that how you're measuring that is accurate and it comes a little bit
[24:20] is accurate and it comes a little bit
[24:20] is accurate and it comes a little bit harder than one might expect. It's not
[24:22] harder than one might expect. It's not
[24:22] harder than one might expect. It's not just the main token cost but there's
[24:26] just the main token cost but there's
[24:26] just the main token cost but there's factors such as caching costs um of
[24:29] factors such as caching costs um of
[24:29] factors such as caching costs um of various types. there are different types
[24:31] various types. there are different types
[24:31] various types. there are different types of interactions um compression um that
[24:35] of interactions um compression um that
[24:35] of interactions um compression um that come into play that change how much that
[24:37] come into play that change how much that
[24:37] come into play that change how much that call might actually cost. And if you're
[24:38] call might actually cost. And if you're
[24:38] call might actually cost. And if you're looking at just pure token count for a
[24:41] looking at just pure token count for a
[24:41] looking at just pure token count for a call that you're often likely to miss
[24:42] call that you're often likely to miss
[24:42] call that you're often likely to miss it. And you know in building our own
[24:44] it. And you know in building our own
[24:44] it. And you know in building our own tools in our own experience with using a
[24:47] tools in our own experience with using a
[24:47] tools in our own experience with using a gateway internally um and trying to
[24:50] gateway internally um and trying to
[24:50] gateway internally um and trying to govern and set budgets internally we
[24:52] govern and set budgets internally we
[24:52] govern and set budgets internally we found that um we had to put significant
[24:55] found that um we had to put significant
[24:55] found that um we had to put significant amount of work to make sure that um at
[24:58] amount of work to make sure that um at
[24:58] amount of work to make sure that um at all at all phases um in all scenarios
[25:02] all at all phases um in all scenarios
[25:02] all at all phases um in all scenarios our costs were accurate and that we are
[25:04] our costs were accurate and that we are
[25:04] our costs were accurate and that we are taking into consideration all particular
[25:07] taking into consideration all particular
[25:07] taking into consideration all particular aspects of how a model call is made and
[25:10] aspects of how a model call is made and
[25:10] aspects of how a model call is made and then keeping that updated. So as model
[25:12] then keeping that updated. So as model
[25:12] then keeping that updated. So as model providers make changes, release new
[25:14] providers make changes, release new
[25:14] providers make changes, release new models with new capabilities with new um
[25:18] models with new capabilities with new um
[25:18] models with new capabilities with new um saving techniques that those are applied
[25:20] saving techniques that those are applied
[25:20] saving techniques that those are applied within our central within our central
[25:22] within our central within our central
[25:22] within our central within our central management system. And we're quite proud
[25:24] management system. And we're quite proud
[25:24] management system. And we're quite proud of how far we've come in terms of
[25:25] of how far we've come in terms of
[25:25] of how far we've come in terms of ensuring accurate model counting and
[25:29] ensuring accurate model counting and
[25:29] ensuring accurate model counting and configurations within our own ecosystem.
[25:32] configurations within our own ecosystem.
[25:32] configurations within our own ecosystem. And then finally, you want to make sure
[25:34] And then finally, you want to make sure
[25:34] And then finally, you want to make sure that there's w really wide model access.
[25:37] that there's w really wide model access.
[25:37] that there's w really wide model access. We've heard from a lot of folks that
[25:39] We've heard from a lot of folks that
[25:39] We've heard from a lot of folks that provider lockin is a big fear and lang
[25:41] provider lockin is a big fear and lang
[25:41] provider lockin is a big fear and lang chain really stands on that ground that
[25:43] chain really stands on that ground that
[25:43] chain really stands on that ground that having access to a wide range of models
[25:45] having access to a wide range of models
[25:45] having access to a wide range of models is critical and very important. Um we
[25:49] is critical and very important. Um we
[25:49] is critical and very important. Um we internally have access built-in access
[25:52] internally have access built-in access
[25:52] internally have access built-in access to support Frontier models, openw
[25:55] to support Frontier models, openw
[25:55] to support Frontier models, openw weightight models across the board
[25:57] weightight models across the board
[25:57] weightight models across the board through providers such as fireworks and
[26:00] through providers such as fireworks and
[26:00] through providers such as fireworks and base 10 all the frontier models that you
[26:02] base 10 all the frontier models that you
[26:02] base 10 all the frontier models that you can think of and a variety of hosting
[26:04] can think of and a variety of hosting
[26:04] can think of and a variety of hosting model hosting providers as well to make
[26:07] model hosting providers as well to make
[26:07] model hosting providers as well to make sure that you can easily switch models
[26:10] sure that you can easily switch models
[26:10] sure that you can easily switch models as needed. You can route flexibly across
[26:13] as needed. You can route flexibly across
[26:13] as needed. You can route flexibly across all the models that you would need and
[26:15] all the models that you would need and
[26:15] all the models that you would need and for different uses, right? So choosing a
[26:17] for different uses, right? So choosing a
[26:17] for different uses, right? So choosing a cheap model for a particular task should
[26:20] cheap model for a particular task should
[26:20] cheap model for a particular task should be just as easy as using you know a
[26:22] be just as easy as using you know a
[26:22] be just as easy as using you know a cloud code um for your main your main
[26:25] cloud code um for your main your main
[26:25] cloud code um for your main your main work.
[26:33] So then finally
[26:33] So then finally governing on top of that right so you've
[26:36] governing on top of that right so you've
[26:36] governing on top of that right so you've allowed yourself the flexibility to set
[26:38] allowed yourself the flexibility to set
[26:38] allowed yourself the flexibility to set up this ecosystem and make sure that you
[26:41] up this ecosystem and make sure that you
[26:41] up this ecosystem and make sure that you allow your engineers as flexible an
[26:44] allow your engineers as flexible an
[26:44] allow your engineers as flexible an environment as possible. But there's
[26:46] environment as possible. But there's
[26:46] environment as possible. But there's many ways that you want to make sure
[26:47] many ways that you want to make sure
[26:47] many ways that you want to make sure this is in check based on what your
[26:49] this is in check based on what your
[26:49] this is in check based on what your internal policies and thought processes
[26:51] internal policies and thought processes
[26:51] internal policies and thought processes are. You have budgets and investor
[26:53] are. You have budgets and investor
[26:53] are. You have budgets and investor dollars that you need to make sure are
[26:55] dollars that you need to make sure are
[26:55] dollars that you need to make sure are used efficiently. And as we've said, as
[26:58] used efficiently. And as we've said, as
[26:58] used efficiently. And as we've said, as models get more expensive, um, as as as
[27:02] models get more expensive, um, as as as
[27:02] models get more expensive, um, as as as and as contexts grow larger and prompts
[27:05] and as contexts grow larger and prompts
[27:05] and as contexts grow larger and prompts go grow larger, you need to make sure
[27:07] go grow larger, you need to make sure
[27:07] go grow larger, you need to make sure that you're ensuring availability and
[27:10] that you're ensuring availability and
[27:10] that you're ensuring availability and that you're staying within budget and
[27:11] that you're staying within budget and
[27:11] that you're staying within budget and that token economics are taken into
[27:13] that token economics are taken into
[27:13] that token economics are taken into consideration.
[27:15] consideration.
[27:15] consideration. So multi-level limits help you find help
[27:18] So multi-level limits help you find help
[27:18] So multi-level limits help you find help you ensure that at all levels from the
[27:20] you ensure that at all levels from the
[27:20] you ensure that at all levels from the individual to the full organization
[27:22] individual to the full organization
[27:22] individual to the full organization you've caught any sort of runaway loops
[27:25] you've caught any sort of runaway loops
[27:25] you've caught any sort of runaway loops you've made sure to layer them based on
[27:27] you've made sure to layer them based on
[27:27] you've made sure to layer them based on daily weekly or monthly limits for
[27:29] daily weekly or monthly limits for
[27:29] daily weekly or monthly limits for instance. So you might say that during a
[27:31] instance. So you might say that during a
[27:31] instance. So you might say that during a single day you you spend $5 or $10. Um
[27:34] single day you you spend $5 or $10. Um
[27:34] single day you you spend $5 or $10. Um but that also over the month you want to
[27:35] but that also over the month you want to
[27:35] but that also over the month you want to make sure you don't go over some amount.
[27:38] make sure you don't go over some amount.
[27:38] make sure you don't go over some amount. And you want to make sure that these are
[27:39] And you want to make sure that these are
[27:39] And you want to make sure that these are like early indicators, right? So, it's
[27:41] like early indicators, right? So, it's
[27:41] like early indicators, right? So, it's really easy to see when you've hit
[27:43] really easy to see when you've hit
[27:43] really easy to see when you've hit limits because that might be really
[27:44] limits because that might be really
[27:44] limits because that might be really useful
[27:46] useful
[27:46] useful productive information for agents that
[27:48] productive information for agents that
[27:48] productive information for agents that are misbehaving, for agents that are
[27:51] are misbehaving, for agents that are
[27:51] are misbehaving, for agents that are working unexpectedly. Um, and you have a
[27:53] working unexpectedly. Um, and you have a
[27:53] working unexpectedly. Um, and you have a bunch of factors as you build agents to
[27:55] bunch of factors as you build agents to
[27:56] bunch of factors as you build agents to do so. But you want those early
[27:58] do so. But you want those early
[27:58] do so. But you want those early indicators and these and policy
[27:59] indicators and these and policy
[27:59] indicators and these and policy violations can be one of them, including
[28:01] violations can be one of them, including
[28:01] violations can be one of them, including if there's alerting associated with it.
[28:08] You also want to think about, you know,
[28:08] You also want to think about, you know, which model is used for which purposes.
[28:11] which model is used for which purposes.
[28:11] which model is used for which purposes. You might use a cheap model for a really
[28:13] You might use a cheap model for a really
[28:13] You might use a cheap model for a really cheap retrieval task or summary task, or
[28:16] cheap retrieval task or summary task, or
[28:16] cheap retrieval task or summary task, or you might use a more expensive model for
[28:18] you might use a more expensive model for
[28:18] you might use a more expensive model for truly the the highlevel thinking tasks
[28:21] truly the the highlevel thinking tasks
[28:21] truly the the highlevel thinking tasks that require that kind of model.
[28:23] that require that kind of model.
[28:23] that require that kind of model. Increasingly, what we're hearing from
[28:25] Increasingly, what we're hearing from
[28:25] Increasingly, what we're hearing from folks is that it's not really just a one
[28:27] folks is that it's not really just a one
[28:27] folks is that it's not really just a one model, one-sizefits-all, but that
[28:29] model, one-sizefits-all, but that
[28:29] model, one-sizefits-all, but that there's different models for different
[28:31] there's different models for different
[28:31] there's different models for different purposes. And you want to be able to
[28:33] purposes. And you want to be able to
[28:33] purposes. And you want to be able to switch easily between them and then
[28:34] switch easily between them and then
[28:34] switch easily between them and then eventually run evaluations and see how
[28:36] eventually run evaluations and see how
[28:36] eventually run evaluations and see how they're performing differently. Um, and
[28:38] they're performing differently. Um, and
[28:38] they're performing differently. Um, and have that all be within one ecosystem
[28:40] have that all be within one ecosystem
[28:40] have that all be within one ecosystem because you want to make sure that your
[28:42] because you want to make sure that your
[28:42] because you want to make sure that your quality isn't suffering while you're
[28:43] quality isn't suffering while you're
[28:44] quality isn't suffering while you're optimizing for cost.
[28:47] optimizing for cost.
[28:47] optimizing for cost. So you know areas where we see this as
[28:48] So you know areas where we see this as
[28:48] So you know areas where we see this as like matching on types of workload on
[28:50] like matching on types of workload on
[28:50] like matching on types of workload on task delegation um and really reserving
[28:53] task delegation um and really reserving
[28:53] task delegation um and really reserving the most expensive say frontier models
[28:55] the most expensive say frontier models
[28:56] the most expensive say frontier models and the most highly capable ones to
[28:58] and the most highly capable ones to
[28:58] and the most highly capable ones to those tasks that really require it and
[28:59] those tasks that really require it and
[29:00] those tasks that really require it and have complex reasoning needs but
[29:01] have complex reasoning needs but
[29:01] have complex reasoning needs but potentially going to you know a cheaper
[29:03] potentially going to you know a cheaper
[29:03] potentially going to you know a cheaper openweight model for some of the easier
[29:05] openweight model for some of the easier
[29:05] openweight model for some of the easier easier tasks that don't require the
[29:07] easier tasks that don't require the
[29:07] easier tasks that don't require the highest capabilities um or don't need to
[29:10] highest capabilities um or don't need to
[29:10] highest capabilities um or don't need to be forward facing or front-facing and
[29:13] be forward facing or front-facing and
[29:13] be forward facing or front-facing and can be something running behind the
[29:15] can be something running behind the
[29:15] can be something running behind the scenes.
[29:16] scenes.
[29:16] scenes. And then finally, you want to think
[29:17] And then finally, you want to think
[29:17] And then finally, you want to think about context um and being thoughtful
[29:22] about context um and being thoughtful
[29:22] about context um and being thoughtful about caching and token pruning. So you
[29:27] about caching and token pruning. So you
[29:27] about caching and token pruning. So you want to prune access data to minimize
[29:30] want to prune access data to minimize
[29:30] want to prune access data to minimize cost, to minimize latency, to minimize
[29:32] cost, to minimize latency, to minimize
[29:32] cost, to minimize latency, to minimize exposure. So thinking about are there
[29:35] exposure. So thinking about are there
[29:35] exposure. So thinking about are there ways in a central way to notice those
[29:37] ways in a central way to notice those
[29:37] ways in a central way to notice those types of patterns and reduce their
[29:39] types of patterns and reduce their
[29:40] types of patterns and reduce their existence in what you're calling to an
[29:41] existence in what you're calling to an
[29:41] existence in what you're calling to an LM to save on cost and save on save on
[29:44] LM to save on cost and save on save on
[29:44] LM to save on cost and save on save on how long it takes to make the call.
[29:48] how long it takes to make the call.
[29:48] how long it takes to make the call. Evals and tracing are really great tools
[29:51] Evals and tracing are really great tools
[29:51] Evals and tracing are really great tools in this regard as well. Running online
[29:53] in this regard as well. Running online
[29:53] in this regard as well. Running online or offline evals for instance to
[29:56] or offline evals for instance to
[29:56] or offline evals for instance to understand you know where your money is
[29:59] understand you know where your money is
[29:59] understand you know where your money is going. um running insights on how to
[30:03] going. um running insights on how to
[30:03] going. um running insights on how to establish safe thresholds for that
[30:05] establish safe thresholds for that
[30:05] establish safe thresholds for that context reduction for latency
[30:07] context reduction for latency
[30:07] context reduction for latency maintenance and m minimizing exposure to
[30:11] maintenance and m minimizing exposure to
[30:11] maintenance and m minimizing exposure to threats.
[30:17] As we think about this in central
[30:17] As we think about this in central governance, we also think about how
[30:19] governance, we also think about how
[30:19] governance, we also think about how sensitive data at runtime plays into
[30:21] sensitive data at runtime plays into
[30:21] sensitive data at runtime plays into things, right? So um there's a few
[30:25] things, right? So um there's a few
[30:25] things, right? So um there's a few regulation and this is just a short list
[30:27] regulation and this is just a short list
[30:27] regulation and this is just a short list but these are the main ones that
[30:28] but these are the main ones that
[30:28] but these are the main ones that customers have come to us with and this
[30:29] customers have come to us with and this
[30:29] customers have come to us with and this is really just to provide an example of
[30:31] is really just to provide an example of
[30:31] is really just to provide an example of areas that we ourselves consider and we
[30:33] areas that we ourselves consider and we
[30:33] areas that we ourselves consider and we think about how we how this works within
[30:36] think about how we how this works within
[30:36] think about how we how this works within not just for instance a central gateway
[30:38] not just for instance a central gateway
[30:38] not just for instance a central gateway but also within governance as a whole
[30:40] but also within governance as a whole
[30:40] but also within governance as a whole right we want to make sure that we're
[30:41] right we want to make sure that we're
[30:42] right we want to make sure that we're compliant with all of the newest
[30:43] compliant with all of the newest
[30:43] compliant with all of the newest regulations that our customers are going
[30:44] regulations that our customers are going
[30:44] regulations that our customers are going to be facing. So, some examples I'll
[30:47] to be facing. So, some examples I'll
[30:47] to be facing. So, some examples I'll walk through just to give you a taste
[30:48] walk through just to give you a taste
[30:48] walk through just to give you a taste are the CCPA, the California Consumer
[30:50] are the CCPA, the California Consumer
[30:50] are the CCPA, the California Consumer Privacy Act. This gives consumers the
[30:53] Privacy Act. This gives consumers the
[30:53] Privacy Act. This gives consumers the right to know what personal data is
[30:54] right to know what personal data is
[30:54] right to know what personal data is collected. Um, and it it's it runs
[30:59] collected. Um, and it it's it runs
[30:59] collected. Um, and it it's it runs within the state of California. There's
[31:01] within the state of California. There's
[31:01] within the state of California. There's GDPR that's been pretty famous for some
[31:03] GDPR that's been pretty famous for some
[31:03] GDPR that's been pretty famous for some time and a lot of people have worked
[31:04] time and a lot of people have worked
[31:04] time and a lot of people have worked towards meeting its its expectations. It
[31:07] towards meeting its its expectations. It
[31:07] towards meeting its its expectations. It applies to citizens of the European
[31:09] applies to citizens of the European
[31:09] applies to citizens of the European Union and residents. um and it governs
[31:13] Union and residents. um and it governs
[31:13] Union and residents. um and it governs basically the collection, storage, and
[31:14] basically the collection, storage, and
[31:14] basically the collection, storage, and processing of personal data. A new one
[31:17] processing of personal data. A new one
[31:17] processing of personal data. A new one that a lot of our customers are working
[31:18] that a lot of our customers are working
[31:18] that a lot of our customers are working with us to make sure that they're
[31:20] with us to make sure that they're
[31:20] with us to make sure that they're meeting the demands of is the EU AI act.
[31:23] meeting the demands of is the EU AI act.
[31:23] meeting the demands of is the EU AI act. Once again, it applies to the European
[31:24] Once again, it applies to the European
[31:24] Once again, it applies to the European Union and it classifies AI systems by
[31:27] Union and it classifies AI systems by
[31:27] Union and it classifies AI systems by Rick's level, imposes obligations. Um
[31:30] Rick's level, imposes obligations. Um
[31:30] Rick's level, imposes obligations. Um and it really is the next level of
[31:31] and it really is the next level of
[31:31] and it really is the next level of thinking about how to minimize the risks
[31:34] thinking about how to minimize the risks
[31:34] thinking about how to minimize the risks of AI systems, not just the data and how
[31:36] of AI systems, not just the data and how
[31:36] of AI systems, not just the data and how it's stored. And then finally for our
[31:39] it's stored. And then finally for our
[31:39] it's stored. And then finally for our more regulated colleagues, especially in
[31:41] more regulated colleagues, especially in
[31:41] more regulated colleagues, especially in the healthcare industries, HIPPA is the
[31:43] the healthcare industries, HIPPA is the
[31:43] the healthcare industries, HIPPA is the Health Insurance Portability and
[31:45] Health Insurance Portability and
[31:45] Health Insurance Portability and Accountability Act within the United
[31:47] Accountability Act within the United
[31:47] Accountability Act within the United States. It governs protected health
[31:49] States. It governs protected health
[31:49] States. It governs protected health information. So make sure there's
[31:50] information. So make sure there's
[31:50] information. So make sure there's safeguards for how people access and
[31:53] safeguards for how people access and
[31:53] safeguards for how people access and store it um and how it's transmitted.
[31:57] store it um and how it's transmitted.
[31:57] store it um and how it's transmitted. We think of this in, you know, as new
[31:59] We think of this in, you know, as new
[32:00] We think of this in, you know, as new policies and as new regulations come
[32:02] policies and as new regulations come
[32:02] policies and as new regulations come out, we realize that they have different
[32:05] out, we realize that they have different
[32:05] out, we realize that they have different data handling requirements and often we
[32:08] data handling requirements and often we
[32:08] data handling requirements and often we think about where sensitive data can go,
[32:10] think about where sensitive data can go,
[32:10] think about where sensitive data can go, who can access it and what control is
[32:12] who can access it and what control is
[32:12] who can access it and what control is applied before it leaves the system. And
[32:14] applied before it leaves the system. And
[32:14] applied before it leaves the system. And so within lang chain, this applies both
[32:17] so within lang chain, this applies both
[32:17] so within lang chain, this applies both in central governance layers, but also
[32:20] in central governance layers, but also
[32:20] in central governance layers, but also across the full linksmith platform. So
[32:22] across the full linksmith platform. So
[32:22] across the full linksmith platform. So we have many tools in place to make sure
[32:25] we have many tools in place to make sure
[32:25] we have many tools in place to make sure that roles are defined in ways to limit
[32:28] that roles are defined in ways to limit
[32:28] that roles are defined in ways to limit access that you think about or able to
[32:31] access that you think about or able to
[32:31] access that you think about or able to limit PII and tracing for instance in
[32:34] limit PII and tracing for instance in
[32:34] limit PII and tracing for instance in particular ways um that there's um audit
[32:39] particular ways um that there's um audit
[32:39] particular ways um that there's um audit logs to see how things and policies are
[32:41] logs to see how things and policies are
[32:41] logs to see how things and policies are changed so that any sort of suspicious
[32:44] changed so that any sort of suspicious
[32:44] changed so that any sort of suspicious changes are tracked in case there's
[32:46] changes are tracked in case there's
[32:46] changes are tracked in case there's enforcement requirements.
[32:48] enforcement requirements.
[32:48] enforcement requirements. And really the thought thinking is we're
[32:51] And really the thought thinking is we're
[32:51] And really the thought thinking is we're thinking about this in terms of risk
[32:53] thinking about this in terms of risk
[32:53] thinking about this in terms of risk based prevention versus trying to build
[32:56] based prevention versus trying to build
[32:56] based prevention versus trying to build out every possible control for every
[32:58] out every possible control for every
[32:58] out every possible control for every workload.
[33:00] workload.
[33:00] workload. We know that controls introduce
[33:02] We know that controls introduce
[33:02] We know that controls introduce trade-offs around latency, cost, and
[33:04] trade-offs around latency, cost, and
[33:04] trade-offs around latency, cost, and complexity. And we want to make sure to
[33:06] complexity. And we want to make sure to
[33:06] complexity. And we want to make sure to apply the right level of protection
[33:07] apply the right level of protection
[33:07] apply the right level of protection based on the agent and data involved.
[33:11] based on the agent and data involved.
[33:11] based on the agent and data involved. From this customers have talked to us
[33:13] From this customers have talked to us
[33:13] From this customers have talked to us about guardrails and we've built some
[33:15] about guardrails and we've built some
[33:16] about guardrails and we've built some basic ones and are broadening our our
[33:17] basic ones and are broadening our our
[33:17] basic ones and are broadening our our our our offering here to make sure that
[33:21] our our offering here to make sure that
[33:21] our our offering here to make sure that PII and secrets are protected and
[33:24] PII and secrets are protected and
[33:24] PII and secrets are protected and thinking about the broader range of what
[33:26] thinking about the broader range of what
[33:26] thinking about the broader range of what kind of guard rails should be available
[33:28] kind of guard rails should be available
[33:28] kind of guard rails should be available in a centralized way especially for our
[33:30] in a centralized way especially for our
[33:30] in a centralized way especially for our customers in protected industries. So
[33:33] customers in protected industries. So
[33:33] customers in protected industries. So there's many different ways to apply
[33:36] there's many different ways to apply
[33:36] there's many different ways to apply guardrails and to think about them. So
[33:37] guardrails and to think about them. So
[33:37] guardrails and to think about them. So if you're building this yourself or
[33:39] if you're building this yourself or
[33:39] if you're building this yourself or using existing models, um this is where
[33:41] using existing models, um this is where
[33:41] using existing models, um this is where this might apply. So think about it in
[33:44] this might apply. So think about it in
[33:44] this might apply. So think about it in structured PI detection. So this is
[33:45] structured PI detection. So this is
[33:45] structured PI detection. So this is stuff like reax and pattern based
[33:47] stuff like reax and pattern based
[33:47] stuff like reax and pattern based matching stuff like social security
[33:48] matching stuff like social security
[33:48] matching stuff like social security numbers, phone numbers or like very
[33:51] numbers, phone numbers or like very
[33:51] numbers, phone numbers or like very formatted identifiers that have
[33:52] formatted identifiers that have
[33:52] formatted identifiers that have predictable patterns. There's also
[33:54] predictable patterns. There's also
[33:54] predictable patterns. There's also unstructured PI detection and for this
[33:56] unstructured PI detection and for this
[33:56] unstructured PI detection and for this you might use something that's more LM
[33:58] you might use something that's more LM
[33:58] you might use something that's more LM based to be able to identify things
[34:00] based to be able to identify things
[34:00] based to be able to identify things within context. Um so stuff like named
[34:03] within context. Um so stuff like named
[34:03] within context. Um so stuff like named entity recognition for like names,
[34:05] entity recognition for like names,
[34:05] entity recognition for like names, locations, affiliations. there's not a
[34:07] locations, affiliations. there's not a
[34:07] locations, affiliations. there's not a really a fixed pattern or not like
[34:09] really a fixed pattern or not like
[34:09] really a fixed pattern or not like something that you could name very
[34:10] something that you could name very
[34:10] something that you could name very easily. An LLM is going to be much
[34:12] easily. An LLM is going to be much
[34:12] easily. An LLM is going to be much better at defining and noticing those
[34:15] better at defining and noticing those
[34:15] better at defining and noticing those patterns in a way that just basic code
[34:17] patterns in a way that just basic code
[34:17] patterns in a way that just basic code might not. And then finally, secrets
[34:19] might not. And then finally, secrets
[34:19] might not. And then finally, secrets detection. So, um this really even
[34:21] detection. So, um this really even
[34:21] detection. So, um this really even applies to any engineers who are working
[34:23] applies to any engineers who are working
[34:23] applies to any engineers who are working and making sure that you're not sending
[34:24] and making sure that you're not sending
[34:24] and making sure that you're not sending an OM. Your API keys, your tokens, your
[34:27] an OM. Your API keys, your tokens, your
[34:27] an OM. Your API keys, your tokens, your credentials, those can have real
[34:29] credentials, those can have real
[34:29] credentials, those can have real security consequences if if API keys are
[34:32] security consequences if if API keys are
[34:32] security consequences if if API keys are exposed and can run up a big dollar
[34:35] exposed and can run up a big dollar
[34:35] exposed and can run up a big dollar bill. um if if not if left unattended um
[34:38] bill. um if if not if left unattended um
[34:38] bill. um if if not if left unattended um by you know
[34:41] by you know
[34:41] by you know um by third parties who don't have good
[34:43] um by third parties who don't have good
[34:43] um by third parties who don't have good intentions. [laughter]
[34:45] intentions. [laughter]
[34:45] intentions. [laughter] Um and so yeah I mean long story short I
[34:48] Um and so yeah I mean long story short I
[34:48] Um and so yeah I mean long story short I mean we see these as reducing risk.
[34:50] mean we see these as reducing risk.
[34:50] mean we see these as reducing risk. They're not an entire governance system,
[34:52] They're not an entire governance system,
[34:52] They're not an entire governance system, but they help you make sure that you can
[34:54] but they help you make sure that you can
[34:54] but they help you make sure that you can give confidence to your customers that
[34:55] give confidence to your customers that
[34:55] give confidence to your customers that their data is going to be protected when
[34:57] their data is going to be protected when
[34:57] their data is going to be protected when that's necessary and that your engineers
[34:58] that's necessary and that your engineers
[34:58] that's necessary and that your engineers can work freely. Um, and that um you can
[35:04] can work freely. Um, and that um you can
[35:04] can work freely. Um, and that um you can pass on, you know, high impact actions
[35:07] pass on, you know, high impact actions
[35:07] pass on, you know, high impact actions to human approval as needed. Um, and
[35:10] to human approval as needed. Um, and
[35:10] to human approval as needed. Um, and figure out sort of where LLMs fall into
[35:13] figure out sort of where LLMs fall into
[35:13] figure out sort of where LLMs fall into that pattern, where tools fall into that
[35:15] that pattern, where tools fall into that
[35:15] that pattern, where tools fall into that pattern, and what you want to be sharing
[35:16] pattern, and what you want to be sharing
[35:16] pattern, and what you want to be sharing externally outside of your safe
[35:18] externally outside of your safe
[35:18] externally outside of your safe ecosystem.
[35:26] So internally uh we have built an LLM
[35:26] So internally uh we have built an LLM gateway and it does a lot of the things
[35:27] gateway and it does a lot of the things
[35:27] gateway and it does a lot of the things that we've talked about. It isn't the
[35:29] that we've talked about. It isn't the
[35:29] that we've talked about. It isn't the only solution but it is one that is
[35:30] only solution but it is one that is
[35:30] only solution but it is one that is built into Langmith. So if you're one of
[35:33] built into Langmith. So if you're one of
[35:33] built into Langmith. So if you're one of our customers this is something that is
[35:34] our customers this is something that is
[35:34] our customers this is something that is available to to you today in public
[35:36] available to to you today in public
[35:36] available to to you today in public beta. And this is an example of how a
[35:38] beta. And this is an example of how a
[35:38] beta. And this is an example of how a gateway might work. And there's you know
[35:41] gateway might work. And there's you know
[35:41] gateway might work. And there's you know we've talked to customers some of whom
[35:43] we've talked to customers some of whom
[35:43] we've talked to customers some of whom built it themselves some of whom have
[35:45] built it themselves some of whom have
[35:45] built it themselves some of whom have been interested in ours. And there's
[35:47] been interested in ours. And there's
[35:47] been interested in ours. And there's some basic functions that exist here.
[35:48] some basic functions that exist here.
[35:48] some basic functions that exist here. And then obviously we're expanding to
[35:51] And then obviously we're expanding to
[35:51] And then obviously we're expanding to bigger and better things um to make sure
[35:53] bigger and better things um to make sure
[35:53] bigger and better things um to make sure that we cover all of the needs of our
[35:56] that we cover all of the needs of our
[35:56] that we cover all of the needs of our broad range of customers as you
[35:58] broad range of customers as you
[35:58] broad range of customers as you mentioned at the beginning. So um the
[36:00] mentioned at the beginning. So um the
[36:00] mentioned at the beginning. So um the agent makes a request and that request
[36:02] agent makes a request and that request
[36:02] agent makes a request and that request is intercepted by the gateway before it
[36:04] is intercepted by the gateway before it
[36:04] is intercepted by the gateway before it actually reaches the provider whoever
[36:06] actually reaches the provider whoever
[36:06] actually reaches the provider whoever they may be. and there's various
[36:09] they may be. and there's various
[36:09] they may be. and there's various policies that run against that call to
[36:11] policies that run against that call to
[36:11] policies that run against that call to make sure that it is authorized to go to
[36:14] make sure that it is authorized to go to
[36:14] make sure that it is authorized to go to the provider and if so that the right
[36:15] the provider and if so that the right
[36:15] the provider and if so that the right data and the right structure of data is
[36:18] data and the right structure of data is
[36:18] data and the right structure of data is going to that provider. So there's
[36:20] going to that provider. So there's
[36:20] going to that provider. So there's elements such as fallback routing with
[36:22] elements such as fallback routing with
[36:22] elements such as fallback routing with retry policies, circuit breakers.
[36:26] retry policies, circuit breakers.
[36:26] retry policies, circuit breakers. There's spend limits. So making sure
[36:29] There's spend limits. So making sure
[36:29] There's spend limits. So making sure that across your organization workspace
[36:31] that across your organization workspace
[36:31] that across your organization workspace API keys and users or even custom
[36:34] API keys and users or even custom
[36:34] API keys and users or even custom headers if you're maybe charging
[36:36] headers if you're maybe charging
[36:36] headers if you're maybe charging customers that those spend limits are
[36:38] customers that those spend limits are
[36:38] customers that those spend limits are applied and that your budgets are
[36:40] applied and that your budgets are
[36:40] applied and that your budgets are maintained. So whether it's your budget
[36:42] maintained. So whether it's your budget
[36:42] maintained. So whether it's your budget for individual customers and how how
[36:44] for individual customers and how how
[36:44] for individual customers and how how much LLM calls they're about allowed to
[36:47] much LLM calls they're about allowed to
[36:47] much LLM calls they're about allowed to make or your own internal developers who
[36:49] make or your own internal developers who
[36:49] make or your own internal developers who are running coding agents or your
[36:51] are running coding agents or your
[36:51] are running coding agents or your production agent or internal agent and
[36:53] production agent or internal agent and
[36:53] production agent or internal agent and making sure that teams are not
[36:55] making sure that teams are not
[36:55] making sure that teams are not overspending their allotted abilities
[36:58] overspending their allotted abilities
[36:58] overspending their allotted abilities with rate limits. You want to make sure
[36:59] with rate limits. You want to make sure
[37:00] with rate limits. You want to make sure that you know a retry loop is caught,
[37:04] that you know a retry loop is caught,
[37:04] that you know a retry loop is caught, that sudden spikes in usage are caught,
[37:07] that sudden spikes in usage are caught,
[37:07] that sudden spikes in usage are caught, and that you might want to fall back if
[37:08] and that you might want to fall back if
[37:08] and that you might want to fall back if to a different model if for instance um
[37:11] to a different model if for instance um
[37:11] to a different model if for instance um one of your LLMs is overloaded with
[37:14] one of your LLMs is overloaded with
[37:14] one of your LLMs is overloaded with traffic. Uh this might this might mean
[37:16] traffic. Uh this might this might mean
[37:16] traffic. Uh this might this might mean that you um this might also allow you to
[37:19] that you um this might also allow you to
[37:19] that you um this might also allow you to prevent your LLM from making that
[37:21] prevent your LLM from making that
[37:21] prevent your LLM from making that decision for you and blocking you for
[37:23] decision for you and blocking you for
[37:23] decision for you and blocking you for some amount of time only extending the
[37:25] some amount of time only extending the
[37:25] some amount of time only extending the amount of time that for instance a
[37:26] amount of time that for instance a
[37:26] amount of time that for instance a customer doesn't have access to your
[37:28] customer doesn't have access to your
[37:28] customer doesn't have access to your product. And then finally data reduction
[37:31] product. And then finally data reduction
[37:31] product. And then finally data reduction we have it for our enterprise customers
[37:33] we have it for our enterprise customers
[37:33] we have it for our enterprise customers and you can redact PII and secrets and
[37:36] and you can redact PII and secrets and
[37:36] and you can redact PII and secrets and make sure that the data that's reaching
[37:38] make sure that the data that's reaching
[37:38] make sure that the data that's reaching the provider is only the stuff that you
[37:40] the provider is only the stuff that you
[37:40] the provider is only the stuff that you actually want to be sharing and doesn't
[37:41] actually want to be sharing and doesn't
[37:41] actually want to be sharing and doesn't have any negative consequences for your
[37:43] have any negative consequences for your
[37:43] have any negative consequences for your work.
[37:49] within this this these actions create a
[37:49] within this this these actions create a trace um and these can be used in in
[37:52] trace um and these can be used in in
[37:52] trace um and these can be used in in tools such as engine so running an agent
[37:55] tools such as engine so running an agent
[37:55] tools such as engine so running an agent over your agents to find insights you
[37:57] over your agents to find insights you
[37:58] over your agents to find insights you didn't even know were there to improve
[38:00] didn't even know were there to improve
[38:00] didn't even know were there to improve them create PRs and improve how your
[38:03] them create PRs and improve how your
[38:03] them create PRs and improve how your agents are running and how your gateways
[38:05] agents are running and how your gateways
[38:05] agents are running and how your gateways even running there is insights so a
[38:08] even running there is insights so a
[38:08] even running there is insights so a lower scale here to find certain
[38:10] lower scale here to find certain
[38:10] lower scale here to find certain patterns and identify patterns so one
[38:12] patterns and identify patterns so one
[38:12] patterns and identify patterns so one use case that one of our engineers use
[38:14] use case that one of our engineers use
[38:14] use case that one of our engineers use is he asked the insights tool to tell
[38:17] is he asked the insights tool to tell
[38:17] is he asked the insights tool to tell him why his LM cost was so high, what he
[38:19] him why his LM cost was so high, what he
[38:20] him why his LM cost was so high, what he was doing and where were there ways that
[38:21] was doing and where were there ways that
[38:21] was doing and where were there ways that he could optimize how he was using LLMs
[38:24] he could optimize how he was using LLMs
[38:24] he could optimize how he was using LLMs and when. And then finally, evaluations
[38:26] and when. And then finally, evaluations
[38:26] and when. And then finally, evaluations give you a really broad breath of
[38:29] give you a really broad breath of
[38:29] give you a really broad breath of abilities to detect outliers, to measure
[38:34] abilities to detect outliers, to measure
[38:34] abilities to detect outliers, to measure performance, to measure quality of your
[38:37] performance, to measure quality of your
[38:37] performance, to measure quality of your agents. And this is an area that we're
[38:40] agents. And this is an area that we're
[38:40] agents. And this is an area that we're very interested in because um there's a
[38:43] very interested in because um there's a
[38:43] very interested in because um there's a lot of there's a lot of availability
[38:44] lot of there's a lot of availability
[38:44] lot of there's a lot of availability here to really have a gateway be a
[38:46] here to really have a gateway be a
[38:46] here to really have a gateway be a central place to improve your agents
[38:49] central place to improve your agents
[38:49] central place to improve your agents that doesn't have to require every
[38:51] that doesn't have to require every
[38:51] that doesn't have to require every single agent um being developed in a
[38:54] single agent um being developed in a
[38:54] single agent um being developed in a particular way. And then finally, for
[38:56] particular way. And then finally, for
[38:56] particular way. And then finally, for those who care, who want to see
[38:58] those who care, who want to see
[38:58] those who care, who want to see aggregate spending, aggregate behavior,
[39:01] aggregate spending, aggregate behavior,
[39:01] aggregate spending, aggregate behavior, we have dashboards within this gateway,
[39:03] we have dashboards within this gateway,
[39:03] we have dashboards within this gateway, so you can see in granular ways reports
[39:06] so you can see in granular ways reports
[39:06] so you can see in granular ways reports on who's spending what and how much.
[39:10] on who's spending what and how much.
[39:10] on who's spending what and how much. And then just to bring it all together,
[39:13] And then just to bring it all together,
[39:13] And then just to bring it all together, um you know, the gateway is a runtime
[39:16] um you know, the gateway is a runtime
[39:16] um you know, the gateway is a runtime control plane. Uh it's centralized model
[39:18] control plane. Uh it's centralized model
[39:18] control plane. Uh it's centralized model access, spend controls, routing, data
[39:20] access, spend controls, routing, data
[39:20] access, spend controls, routing, data protection, and failure behavior. It
[39:22] protection, and failure behavior. It
[39:22] protection, and failure behavior. It separates governance logic from
[39:23] separates governance logic from
[39:24] separates governance logic from individual applications and more broadly
[39:27] individual applications and more broadly
[39:27] individual applications and more broadly strategically you get model provider
[39:29] strategically you get model provider
[39:29] strategically you get model provider optionality in the ecosystem. So you're
[39:32] optionality in the ecosystem. So you're
[39:32] optionality in the ecosystem. So you're not locked in to any particular
[39:33] not locked in to any particular
[39:33] not locked in to any particular providers and their budget their budget
[39:36] providers and their budget their budget
[39:36] providers and their budget their budget limit tools or um or their capabilities
[39:41] limit tools or um or their capabilities
[39:41] limit tools or um or their capabilities or their cost structures. Good
[39:43] or their cost structures. Good
[39:43] or their cost structures. Good governance should make switching models
[39:45] governance should make switching models
[39:45] governance should make switching models and providers safer, not harder, and
[39:48] and providers safer, not harder, and
[39:48] and providers safer, not harder, and should be built in to where you already
[39:50] should be built in to where you already
[39:50] should be built in to where you already are running and tracing your agents to
[39:52] are running and tracing your agents to
[39:52] are running and tracing your agents to make sure that you have the highest
[39:54] make sure that you have the highest
[39:54] make sure that you have the highest quality available to and the least
[39:57] quality available to and the least
[39:57] quality available to and the least headache available um and the entire
[39:59] headache available um and the entire
[39:59] headache available um and the entire process so you can focus on your
[40:01] process so you can focus on your
[40:01] process so you can focus on your customers um and not all the mechanics
[40:03] customers um and not all the mechanics
[40:03] customers um and not all the mechanics behind the scenes.
[40:06] behind the scenes.
[40:06] behind the scenes. All right,
[40:08] All right,
[40:08] All right, I think we have some time for questions
[40:10] I think we have some time for questions
[40:10] I think we have some time for questions and I've been seeing a lot of things
[40:11] and I've been seeing a lot of things
[40:11] and I've been seeing a lot of things coming in through. So,
[40:15] coming in through. So,
[40:15] coming in through. So, I'm wondering.
[40:24] All right.
[40:24] All right. Um, should I be I think I should be
[40:26] Um, should I be I think I should be
[40:26] Um, should I be I think I should be answering the one that's on the screen
[40:27] answering the one that's on the screen
[40:27] answering the one that's on the screen right now, right, Angeline?
[40:36] Yes. Okay, great. Thank you. Okay, so
[40:36] Yes. Okay, great. Thank you. Okay, so the an the question is if an agent makes
[40:38] the an the question is if an agent makes
[40:38] the an the question is if an agent makes a wrong decision or gets compromised,
[40:40] a wrong decision or gets compromised,
[40:40] a wrong decision or gets compromised, how can we make sure that this mistake
[40:41] how can we make sure that this mistake
[40:42] how can we make sure that this mistake doesn't spread to the tools, MCP servers
[40:44] doesn't spread to the tools, MCP servers
[40:44] doesn't spread to the tools, MCP servers or other agents it's interacting with.
[40:47] or other agents it's interacting with.
[40:47] or other agents it's interacting with. So at the end of the day, this depends
[40:50] So at the end of the day, this depends
[40:50] So at the end of the day, this depends on the agents and it depends on you, the
[40:53] on the agents and it depends on you, the
[40:53] on the agents and it depends on you, the engineer. So there's there's many
[40:56] engineer. So there's there's many
[40:56] engineer. So there's there's many different ways. Um there's it depends on
[41:01] different ways. Um there's it depends on
[41:01] different ways. Um there's it depends on what the signals might be in terms of
[41:03] what the signals might be in terms of
[41:03] what the signals might be in terms of that decision or compromise. So you can
[41:06] that decision or compromise. So you can
[41:06] that decision or compromise. So you can run evaluations um both within a gateway
[41:09] run evaluations um both within a gateway
[41:09] run evaluations um both within a gateway but frankly also even outside of it to
[41:11] but frankly also even outside of it to
[41:11] but frankly also even outside of it to notice patterns in how your agents are
[41:13] notice patterns in how your agents are
[41:13] notice patterns in how your agents are running to prevent them ahead of prevent
[41:15] running to prevent them ahead of prevent
[41:16] running to prevent them ahead of prevent them in the future.
[41:17] them in the future.
[41:18] them in the future. Um you could also add governance of tool
[41:22] Um you could also add governance of tool
[41:22] Um you could also add governance of tool access. So for instance adding a human
[41:25] access. So for instance adding a human
[41:25] access. So for instance adding a human in the loop element before certain calls
[41:27] in the loop element before certain calls
[41:27] in the loop element before certain calls are made. Um you might also think about
[41:30] are made. Um you might also think about
[41:30] are made. Um you might also think about um guard rails. So you might want to
[41:34] um guard rails. So you might want to
[41:34] um guard rails. So you might want to avoid sharing PII or secrets so that
[41:37] avoid sharing PII or secrets so that
[41:37] avoid sharing PII or secrets so that even if it gets compromised you're all
[41:39] even if it gets compromised you're all
[41:39] even if it gets compromised you're all that's releasing is information that is
[41:41] that's releasing is information that is
[41:41] that's releasing is information that is safe to release outside of your
[41:42] safe to release outside of your
[41:42] safe to release outside of your ecosystem.
[41:47] But I think evaluations and having
[41:47] But I think evaluations and having tracing and evaluations are your first
[41:49] tracing and evaluations are your first
[41:50] tracing and evaluations are your first stop shop to notice what actually
[41:51] stop shop to notice what actually
[41:51] stop shop to notice what actually happened and to be able to catch in the
[41:53] happened and to be able to catch in the
[41:53] happened and to be able to catch in the future. And then eventually to add
[41:56] future. And then eventually to add
[41:56] future. And then eventually to add runtime runtime monitoring for those
[41:58] runtime runtime monitoring for those
[41:58] runtime runtime monitoring for those types of behaviors like stuff like you
[42:00] types of behaviors like stuff like you
[42:00] types of behaviors like stuff like you know jailbreaks or um or hallucinations
[42:05] know jailbreaks or um or hallucinations
[42:06] know jailbreaks or um or hallucinations or that sort of thing so that in real
[42:07] or that sort of thing so that in real
[42:07] or that sort of thing so that in real time they can catch those those
[42:09] time they can catch those those
[42:09] time they can catch those those behaviors.
[42:11] behaviors.
[42:11] behaviors. I'm ready for the next one.
[42:14] I'm ready for the next one.
[42:14] I'm ready for the next one. All right, the question is what is the
[42:16] All right, the question is what is the
[42:16] All right, the question is what is the measured latency overhead introduced by
[42:18] measured latency overhead introduced by
[42:18] measured latency overhead introduced by lang chain compared to direct API API
[42:21] lang chain compared to direct API API
[42:21] lang chain compared to direct API API calls to each LM provider and how does
[42:23] calls to each LM provider and how does
[42:24] calls to each LM provider and how does that overhead vary by model workflow
[42:27] that overhead vary by model workflow
[42:27] that overhead vary by model workflow complexity and scale so I think the
[42:29] complexity and scale so I think the
[42:29] complexity and scale so I think the answer is in the question which is that
[42:31] answer is in the question which is that
[42:31] answer is in the question which is that it depends
[42:33] it depends
[42:33] it depends um so we work hard so within a I don't
[42:36] um so we work hard so within a I don't
[42:36] um so we work hard so within a I don't know if the question is just lang chain
[42:38] know if the question is just lang chain
[42:38] know if the question is just lang chain as a whole I mean I think really lang
[42:40] as a whole I mean I think really lang
[42:40] as a whole I mean I think really lang chain is a broad set of tools and
[42:41] chain is a broad set of tools and
[42:42] chain is a broad set of tools and ecosystems and So it's hard to answer
[42:44] ecosystems and So it's hard to answer
[42:44] ecosystems and So it's hard to answer one particular way. The gateway we keep
[42:48] one particular way. The gateway we keep
[42:48] one particular way. The gateway we keep uh it also depends on how it's set up
[42:50] uh it also depends on how it's set up
[42:50] uh it also depends on how it's set up and all the different policies you're
[42:52] and all the different policies you're
[42:52] and all the different policies you're running through. Um if you're running
[42:54] running through. Um if you're running
[42:54] running through. Um if you're running for instance data protection models
[42:57] for instance data protection models
[42:57] for instance data protection models against your calls. Um
[43:00] against your calls. Um
[43:00] against your calls. Um those were going to require are going to
[43:02] those were going to require are going to
[43:02] those were going to require are going to add more latency even like one or two or
[43:05] add more latency even like one or two or
[43:05] add more latency even like one or two or it could add many seconds. Um and we
[43:08] it could add many seconds. Um and we
[43:08] it could add many seconds. Um and we have tools internally to make decisions
[43:09] have tools internally to make decisions
[43:10] have tools internally to make decisions ahead of time that say after this amount
[43:12] ahead of time that say after this amount
[43:12] ahead of time that say after this amount of time maybe say five seconds either
[43:15] of time maybe say five seconds either
[43:15] of time maybe say five seconds either fail open or fail closed right so for
[43:17] fail open or fail closed right so for
[43:17] fail open or fail closed right so for the if you're using like data protection
[43:19] the if you're using like data protection
[43:19] the if you're using like data protection for instance um and then for other tools
[43:22] for instance um and then for other tools
[43:22] for instance um and then for other tools otherwise our policy you know running
[43:24] otherwise our policy you know running
[43:24] otherwise our policy you know running through actual policy like a spun policy
[43:26] through actual policy like a spun policy
[43:26] through actual policy like a spun policy things that are pretty um low resource
[43:28] things that are pretty um low resource
[43:28] things that are pretty um low resource those are pretty fast and so our numbers
[43:30] those are pretty fast and so our numbers
[43:30] those are pretty fast and so our numbers are um you know industry standard in
[43:33] are um you know industry standard in
[43:34] are um you know industry standard in terms of what you'd expect.
[43:36] terms of what you'd expect.
[43:36] terms of what you'd expect. All right, ready for the next one?
[43:44] What is the best governance middleware
[43:44] What is the best governance middleware at runtime? Do you follow a framework,
[43:47] at runtime? Do you follow a framework,
[43:47] at runtime? Do you follow a framework, policy as code, harness code?
[43:50] policy as code, harness code?
[43:50] policy as code, harness code? Well, I think it depends what you're
[43:51] Well, I think it depends what you're
[43:51] Well, I think it depends what you're trying to do, which of the governance
[43:52] trying to do, which of the governance
[43:52] trying to do, which of the governance policies you're trying to apply. So, we
[43:55] policies you're trying to apply. So, we
[43:55] policies you're trying to apply. So, we actually have a robust set if you're
[43:57] actually have a robust set if you're
[43:57] actually have a robust set if you're building especially with lang chain
[43:58] building especially with lang chain
[43:58] building especially with lang chain tools, we have a robust set of
[44:01] tools, we have a robust set of
[44:01] tools, we have a robust set of middleware. Um, for instance, even to do
[44:04] middleware. Um, for instance, even to do
[44:04] middleware. Um, for instance, even to do stuff like fallbacks. So we have um you
[44:06] stuff like fallbacks. So we have um you
[44:06] stuff like fallbacks. So we have um you can find in our docs uh you can find uh
[44:09] can find in our docs uh you can find uh
[44:09] can find in our docs uh you can find uh middleware to set a fallback um to set a
[44:13] middleware to set a fallback um to set a
[44:13] middleware to set a fallback um to set a fallback within your agent. So you
[44:15] fallback within your agent. So you
[44:15] fallback within your agent. So you wouldn't even need a gateway if you're
[44:16] wouldn't even need a gateway if you're
[44:16] wouldn't even need a gateway if you're like a one-off engineer or you're on a
[44:18] like a one-off engineer or you're on a
[44:18] like a one-off engineer or you're on a small team. Very honestly we would
[44:20] small team. Very honestly we would
[44:20] small team. Very honestly we would probably recommend just using our
[44:21] probably recommend just using our
[44:22] probably recommend just using our middleware because it's much much much
[44:24] middleware because it's much much much
[44:24] middleware because it's much much much easier to measure and understand and you
[44:26] easier to measure and understand and you
[44:26] easier to measure and understand and you can make changes as you need. Um it's
[44:28] can make changes as you need. Um it's
[44:28] can make changes as you need. Um it's really at scale or if you have many
[44:30] really at scale or if you have many
[44:30] really at scale or if you have many agents running at a time that you might
[44:31] agents running at a time that you might
[44:32] agents running at a time that you might want to start using a gateway. But I I
[44:33] want to start using a gateway. But I I
[44:33] want to start using a gateway. But I I would recommend I would recommend
[44:35] would recommend I would recommend
[44:35] would recommend I would recommend looking at our docs to seeing all of our
[44:36] looking at our docs to seeing all of our
[44:36] looking at our docs to seeing all of our availability. Um, and I think it just at
[44:40] availability. Um, and I think it just at
[44:40] availability. Um, and I think it just at the end of the day depends on what
[44:41] the end of the day depends on what
[44:41] the end of the day depends on what exactly you're trying to apply.
[44:49] What would be your suggested governance
[44:50] What would be your suggested governance MVP?
[44:51] MVP?
[44:51] MVP? Well, thank you, Alfredo. Um, my
[44:54] Well, thank you, Alfredo. Um, my
[44:54] Well, thank you, Alfredo. Um, my suggested governance MVP, I'm not sure I
[44:57] suggested governance MVP, I'm not sure I
[44:57] suggested governance MVP, I'm not sure I fully understand the question. I think
[44:59] fully understand the question. I think
[44:59] fully understand the question. I think as far as
[45:01] as far as
[45:01] as far as um your stack, maybe that's the
[45:03] um your stack, maybe that's the
[45:03] um your stack, maybe that's the question. Um I do I do think that um the
[45:10] question. Um I do I do think that um the
[45:10] question. Um I do I do think that um the you know, frankly uh if you're using if
[45:12] you know, frankly uh if you're using if
[45:12] you know, frankly uh if you're using if you're building with Langchain or
[45:14] you're building with Langchain or
[45:14] you're building with Langchain or Langmith, the LM gateway is right there.
[45:17] Langmith, the LM gateway is right there.
[45:17] Langmith, the LM gateway is right there. It's really easy to set up. It just
[45:20] It's really easy to set up. It just
[45:20] It's really easy to set up. It just requires a few changes in in your code
[45:22] requires a few changes in in your code
[45:22] requires a few changes in in your code and you automatically get policies and
[45:26] and you automatically get policies and
[45:26] and you automatically get policies and governance infrastructure built in. So
[45:28] governance infrastructure built in. So
[45:28] governance infrastructure built in. So if you're starting from scratch, that's
[45:30] if you're starting from scratch, that's
[45:30] if you're starting from scratch, that's a great place to start. Um, and we're
[45:32] a great place to start. Um, and we're
[45:32] a great place to start. Um, and we're trying to make it as easy as possible to
[45:34] trying to make it as easy as possible to
[45:34] trying to make it as easy as possible to apply all of these governance policies
[45:36] apply all of these governance policies
[45:36] apply all of these governance policies that I talked about throughout the
[45:38] that I talked about throughout the
[45:38] that I talked about throughout the presentation as easily as possible in
[45:40] presentation as easily as possible in
[45:40] presentation as easily as possible in the click of a button as much as
[45:41] the click of a button as much as
[45:41] the click of a button as much as possible um, within the within your
[45:43] possible um, within the within your
[45:43] possible um, within the within your agents and ecosystem.
[45:52] All right. The Langchain blog highlights
[45:52] All right. The Langchain blog highlights the need for an LLM gateway to enforce
[45:56] the need for an LLM gateway to enforce
[45:56] the need for an LLM gateway to enforce centralized policies
[45:58] centralized policies
[45:58] centralized policies on agentto agent interactions.
[46:01] on agentto agent interactions.
[46:01] on agentto agent interactions. How can you effectively enforce these
[46:03] How can you effectively enforce these
[46:03] How can you effectively enforce these centralized gateway policies with an
[46:04] centralized gateway policies with an
[46:04] centralized gateway policies with an emerging decentralized swarm
[46:06] emerging decentralized swarm
[46:06] emerging decentralized swarm architecture at work? We are facing
[46:08] architecture at work? We are facing
[46:08] architecture at work? We are facing these issues. So, I think this probably
[46:12] these issues. So, I think this probably
[46:12] these issues. So, I think this probably requires more one-on-one. So, feel free
[46:13] requires more one-on-one. So, feel free
[46:13] requires more one-on-one. So, feel free to send me an email, Claire. um we can
[46:17] to send me an email, Claire. um we can
[46:17] to send me an email, Claire. um we can think about how we can monitor and
[46:18] think about how we can monitor and
[46:18] think about how we can monitor and govern your your agent to agent
[46:20] govern your your agent to agent
[46:20] govern your your agent to agent interactions. Um but starting to think
[46:22] interactions. Um but starting to think
[46:22] interactions. Um but starting to think about just identity. So we're working on
[46:25] about just identity. So we're working on
[46:26] about just identity. So we're working on such as aspects and thinking about how
[46:28] such as aspects and thinking about how
[46:28] such as aspects and thinking about how to apply agent identity within our
[46:30] to apply agent identity within our
[46:30] to apply agent identity within our interactions and we have some tools
[46:32] interactions and we have some tools
[46:32] interactions and we have some tools within our within our existing ecosystem
[46:35] within our within our existing ecosystem
[46:35] within our within our existing ecosystem to think about agent identity and how
[46:38] to think about agent identity and how
[46:38] to think about agent identity and how how it's applied. So I would start with
[46:40] how it's applied. So I would start with
[46:40] how it's applied. So I would start with looking through our docs to see what's
[46:41] looking through our docs to see what's
[46:42] looking through our docs to see what's available and then if you have any more
[46:43] available and then if you have any more
[46:43] available and then if you have any more questions just send me an email. And we
[46:45] questions just send me an email. And we
[46:45] questions just send me an email. And we can think through, you know, how this
[46:47] can think through, you know, how this
[46:47] can think through, you know, how this applies to your exact use case.
[47:01] Interesting. Okay. When is lang going to
[47:02] Interesting. Okay. When is lang going to be self-healing from these problems?
[47:04] be self-healing from these problems?
[47:04] be self-healing from these problems? So, at the end of the day, governance is
[47:09] So, at the end of the day, governance is
[47:09] So, at the end of the day, governance is the point of governance is to make sure
[47:11] the point of governance is to make sure
[47:11] the point of governance is to make sure that the agents are not just working in
[47:12] that the agents are not just working in
[47:12] that the agents are not just working in agent world. You want to make sure
[47:14] agent world. You want to make sure
[47:14] agent world. You want to make sure there's a human decision of what these
[47:17] there's a human decision of what these
[47:17] there's a human decision of what these agents are allowed to do. And so engine
[47:20] agents are allowed to do. And so engine
[47:20] agents are allowed to do. And so engine is a great place to kind of automate
[47:24] is a great place to kind of automate
[47:24] is a great place to kind of automate that process of understanding what
[47:25] that process of understanding what
[47:25] that process of understanding what should be happening and when. But I
[47:28] should be happening and when. But I
[47:28] should be happening and when. But I would say that you actually probably
[47:29] would say that you actually probably
[47:29] would say that you actually probably want a human setting some of these
[47:31] want a human setting some of these
[47:31] want a human setting some of these policies. You don't want them to be
[47:32] policies. You don't want them to be
[47:32] policies. You don't want them to be completely determined by agentic
[47:34] completely determined by agentic
[47:34] completely determined by agentic systems. You want to make sure that the
[47:36] systems. You want to make sure that the
[47:36] systems. You want to make sure that the agents are responding to human signals
[47:39] agents are responding to human signals
[47:39] agents are responding to human signals um of what you want them to be doing.
[47:52] All right, next question is if we have a
[47:52] All right, next question is if we have a lang graph with a predefined set of
[47:54] lang graph with a predefined set of
[47:54] lang graph with a predefined set of models,
[47:57] models,
[47:57] models, um, how will LM gateway apply its
[48:00] um, how will LM gateway apply its
[48:00] um, how will LM gateway apply its fallback policies on top of it? So
[48:02] fallback policies on top of it? So
[48:02] fallback policies on top of it? So basically
[48:04] basically
[48:04] basically the the agent will make an LM call and
[48:08] the the agent will make an LM call and
[48:08] the the agent will make an LM call and it'll you'll you'll set the the URL that
[48:11] it'll you'll you'll set the the URL that
[48:11] it'll you'll you'll set the the URL that it's supposed to call instead of calling
[48:13] it's supposed to call instead of calling
[48:13] it's supposed to call instead of calling the provider directly. You're going to
[48:15] the provider directly. You're going to
[48:15] the provider directly. You're going to put a gateway URL and then it'll run the
[48:21] put a gateway URL and then it'll run the
[48:21] put a gateway URL and then it'll run the LM call through the gateway and then the
[48:23] LM call through the gateway and then the
[48:23] LM call through the gateway and then the gateway will apply that fallback policy.
[48:25] gateway will apply that fallback policy.
[48:25] gateway will apply that fallback policy. It'll basically monitor it'll say before
[48:27] It'll basically monitor it'll say before
[48:27] It'll basically monitor it'll say before I make this call is this provider
[48:29] I make this call is this provider
[48:29] I make this call is this provider actually available? Is there something
[48:30] actually available? Is there something
[48:30] actually available? Is there something else happening? there's a spend cap was
[48:31] else happening? there's a spend cap was
[48:31] else happening? there's a spend cap was a spend cap already reached. Um, if
[48:34] a spend cap already reached. Um, if
[48:34] a spend cap already reached. Um, if that's the case, then it'll either block
[48:36] that's the case, then it'll either block
[48:36] that's the case, then it'll either block the call to that provider and send it to
[48:38] the call to that provider and send it to
[48:38] the call to that provider and send it to some somewhere else that you defined.
[48:52] I don't know that I can read this whole
[48:52] I don't know that I can read this whole question. Oh, there it is. Okay. Um so
[48:56] question. Oh, there it is. Okay. Um so
[48:56] question. Oh, there it is. Okay. Um so my first your first point notes that an
[48:58] my first your first point notes that an
[48:58] my first your first point notes that an unmonitored loop can consume thousands
[49:01] unmonitored loop can consume thousands
[49:01] unmonitored loop can consume thousands of dollars in a single session
[49:02] of dollars in a single session
[49:02] of dollars in a single session essentially within minutes.
[49:05] essentially within minutes.
[49:05] essentially within minutes. The second proposes daily, weekly and
[49:07] The second proposes daily, weekly and
[49:07] The second proposes daily, weekly and monthly caps. These timelines do not
[49:10] monthly caps. These timelines do not
[49:10] monthly caps. These timelines do not align a daily limit does not prevent a
[49:12] align a daily limit does not prevent a
[49:12] align a daily limit does not prevent a loop from exhausting the entire month's
[49:14] loop from exhausting the entire month's
[49:14] loop from exhausting the entire month's budget in 10 minutes. What is the actual
[49:17] budget in 10 minutes. What is the actual
[49:17] budget in 10 minutes. What is the actual granularity of limit enforcement? And
[49:20] granularity of limit enforcement? And
[49:20] granularity of limit enforcement? And crucially, what is the lat latency of
[49:22] crucially, what is the lat latency of
[49:22] crucially, what is the lat latency of usage tracking? If your counters are
[49:24] usage tracking? If your counters are
[49:24] usage tracking? If your counters are distributed across gateway nodes with
[49:26] distributed across gateway nodes with
[49:26] distributed across gateway nodes with eventual consistency,
[49:28] eventual consistency,
[49:28] eventual consistency, what risk of overage exists during a
[49:32] what risk of overage exists during a
[49:32] what risk of overage exists during a simultaneous activity spike before the
[49:34] simultaneous activity spike before the
[49:34] simultaneous activity spike before the cap takes effect? Finally, when a limit
[49:37] cap takes effect? Finally, when a limit
[49:37] cap takes effect? Finally, when a limit is reached, what happens to running
[49:39] is reached, what happens to running
[49:39] is reached, what happens to running agents? Are they abruptly cut off
[49:40] agents? Are they abruptly cut off
[49:40] agents? Are they abruptly cut off midtransaction or do they shut down
[49:43] midtransaction or do they shut down
[49:43] midtransaction or do they shut down gracefully? Great. This is a very well
[49:46] gracefully? Great. This is a very well
[49:46] gracefully? Great. This is a very well thoughtout question. So
[49:54] the the point here is that you have I
[49:54] the the point here is that you have I think also frankly in this case a rate
[49:56] think also frankly in this case a rate
[49:56] think also frankly in this case a rate limit for the minuteby-minute big spike
[49:59] limit for the minuteby-minute big spike
[49:59] limit for the minuteby-minute big spike in traffic is probably your best bet to
[50:01] in traffic is probably your best bet to
[50:01] in traffic is probably your best bet to stop that first big runaway loop and
[50:04] stop that first big runaway loop and
[50:04] stop that first big runaway loop and then within if you can set dollar limits
[50:06] then within if you can set dollar limits
[50:06] then within if you can set dollar limits on minutes on days on weeks on months.
[50:10] on minutes on days on weeks on months.
[50:10] on minutes on days on weeks on months. The point here with the monthly for
[50:12] The point here with the monthly for
[50:12] The point here with the monthly for instance is that um the the the spend
[50:15] instance is that um the the the spend
[50:15] instance is that um the the the spend limits should interact with one another,
[50:17] limits should interact with one another,
[50:17] limits should interact with one another, right? So um the you would likely set a
[50:22] right? So um the you would likely set a
[50:22] right? So um the you would likely set a daily limit that would not be just as
[50:24] daily limit that would not be just as
[50:24] daily limit that would not be just as high as your monthly limit, right? You
[50:25] high as your monthly limit, right? You
[50:25] high as your monthly limit, right? You would make sure that it's much lower and
[50:27] would make sure that it's much lower and
[50:27] would make sure that it's much lower and so that you're actually pacing yourself
[50:28] so that you're actually pacing yourself
[50:28] so that you're actually pacing yourself against your monthly limit.
[50:32] against your monthly limit.
[50:32] against your monthly limit. In terms of enforcement, the latency of
[50:35] In terms of enforcement, the latency of
[50:35] In terms of enforcement, the latency of usage tracking is um I honestly it
[50:39] usage tracking is um I honestly it
[50:39] usage tracking is um I honestly it depends um of how you have it set up,
[50:41] depends um of how you have it set up,
[50:41] depends um of how you have it set up, what policies you're applying, but if
[50:43] what policies you're applying, but if
[50:43] what policies you're applying, but if you're just doing like very basic like
[50:45] you're just doing like very basic like
[50:45] you're just doing like very basic like spend limits, it's relatively low um and
[50:47] spend limits, it's relatively low um and
[50:47] spend limits, it's relatively low um and kind of within industry standards.
[50:49] kind of within industry standards.
[50:49] kind of within industry standards. And then
[50:52] And then
[50:52] And then um what risk of overage exists during a
[50:55] um what risk of overage exists during a
[50:55] um what risk of overage exists during a simultaneous activity spec before the
[50:56] simultaneous activity spec before the
[50:56] simultaneous activity spec before the count your counters? So you would apply
[50:59] count your counters? So you would apply
[50:59] count your counters? So you would apply you could apply the counters not just
[51:01] you could apply the counters not just
[51:01] you could apply the counters not just across your whole org but you could
[51:02] across your whole org but you could
[51:02] across your whole org but you could apply them on API keys. So what we have
[51:06] apply them on API keys. So what we have
[51:06] apply them on API keys. So what we have for instance a default so saying each
[51:07] for instance a default so saying each
[51:08] for instance a default so saying each user is only allowed to spend X Y and Z
[51:10] user is only allowed to spend X Y and Z
[51:10] user is only allowed to spend X Y and Z per hour per month per per day.
[51:13] per hour per month per per day.
[51:14] per hour per month per per day. Similarly each API key also has that
[51:16] Similarly each API key also has that
[51:16] Similarly each API key also has that default set. So it applies per API key.
[51:19] default set. So it applies per API key.
[51:19] default set. So it applies per API key. It's not just per for the entire org
[51:21] It's not just per for the entire org
[51:21] It's not just per for the entire org which I think is what maybe your
[51:22] which I think is what maybe your
[51:22] which I think is what maybe your question implies. And then when a limit
[51:25] question implies. And then when a limit
[51:25] question implies. And then when a limit is reached what happens to running
[51:26] is reached what happens to running
[51:26] is reached what happens to running agents? So right now they are shut down.
[51:28] agents? So right now they are shut down.
[51:28] agents? So right now they are shut down. You know they are stopped like that LM
[51:29] You know they are stopped like that LM
[51:29] You know they are stopped like that LM the LLM call itself is blocked before
[51:32] the LLM call itself is blocked before
[51:32] the LLM call itself is blocked before it's made. Um
[51:35] it's made. Um
[51:35] it's made. Um but in these cases a good idea is to set
[51:38] but in these cases a good idea is to set
[51:38] but in these cases a good idea is to set a fallback for instance. So if that spin
[51:40] a fallback for instance. So if that spin
[51:40] a fallback for instance. So if that spin limit is reached you fall you can fall
[51:42] limit is reached you fall you can fall
[51:42] limit is reached you fall you can fall back to another model to make sure
[51:43] back to another model to make sure
[51:43] back to another model to make sure you're not losing activity.
[51:52] All right, I think that was maybe our
[51:52] All right, I think that was maybe our last question
[51:54] last question
[51:54] last question and it was great chatting with you guys.
[51:57] and it was great chatting with you guys.
[51:57] and it was great chatting with you guys. Thank you for the really well thoughtout
[51:58] Thank you for the really well thoughtout
[51:58] Thank you for the really well thoughtout questions. Um, feel free to find me on
[52:01] questions. Um, feel free to find me on
[52:01] questions. Um, feel free to find me on LinkedIn. I think my email might have
[52:03] LinkedIn. I think my email might have
[52:03] LinkedIn. I think my email might have been shared somewhere. Um, but also find
[52:06] been shared somewhere. Um, but also find
[52:06] been shared somewhere. Um, but also find me on LinkedIn, send me a message, feel
[52:07] me on LinkedIn, send me a message, feel
[52:07] me on LinkedIn, send me a message, feel free to add me. um really happy to talk
[52:10] free to add me. um really happy to talk
[52:10] free to add me. um really happy to talk about this kind of stuff and we learn so
[52:12] about this kind of stuff and we learn so
[52:12] about this kind of stuff and we learn so much from our customers and our
[52:14] much from our customers and our
[52:14] much from our customers and our listeners who are sharing questions and
[52:16] listeners who are sharing questions and
[52:16] listeners who are sharing questions and asking all of these really thoughtful
[52:17] asking all of these really thoughtful
[52:17] asking all of these really thoughtful things. They help us understand where we
[52:19] things. They help us understand where we
[52:19] things. They help us understand where we need to be f focusing our attention. So
[52:21] need to be f focusing our attention. So
[52:21] need to be f focusing our attention. So look forward to hearing from all of you.
