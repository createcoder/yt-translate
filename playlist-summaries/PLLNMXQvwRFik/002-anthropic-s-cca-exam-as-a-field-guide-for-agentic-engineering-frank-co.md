# Anthropic's CCA Exam as a Field-Guide for Agentic Engineering — Frank Coyle, UC Berkeley

- **Video:** https://www.youtube.com/watch?v=Z-c11pV_uvU
- **Generated:** 2026-08-31 20:40 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The presentation’s central message is that production AI agents should be treated as **governed orchestration systems**, not autonomous LLMs. The LLM interprets context and proposes tool calls; application code must control execution, validate requests, manage iterative loops, enforce authorization, preserve evidence, and decide when to stop or escalate.

For Superior Propane, the most applicable pattern is a **bounded, evidence-grounded agent architecture** for internal support, customer-service assistance, log/incident triage, and developer productivity:

- Use narrowly scoped tools and least-privilege access.
- Explicitly process model stop reasons such as tool use, normal completion, token exhaustion, errors, and safety stops.
- Keep subagents isolated; pass structured summaries and evidence references rather than full histories, raw logs, or hidden reasoning.
- Use context budgets, retrieval, external artifact storage, and compaction for long workflows.
- Start with read-only, advisory workflows and human escalation—not autonomous updates to customer accounts, deliveries, payments, scheduling, or production systems.
- Benchmark multi-agent designs against simpler constrained single-agent designs; specialization can improve governance but increases orchestration complexity, cost, and latency.

The closing section of the source contains only applause and no additional technical content.

The speaker also frames the material around the Claude Certified Architect exam. The cited exam topics—agentic architecture, Claude Code/workflow configuration, prompt engineering and JSON output, tool/MCP integration, and context/reliability—are relevant skills areas. However, details such as a **US$99 fee**, retake timing, and exact domain weighting—including **agentic architecture at 27%**—should be verified with Anthropic’s current official certification documentation.

---

# Technical details

## 1. Core agent architecture: the LLM proposes; the application controls

A foundational distinction in the presentation is that an LLM does not directly execute enterprise tools or operational actions. It generates text and, where supported, structured tool/function-call requests. The surrounding application or orchestration service must:

1. Send the model the user request, relevant context, and an allowlisted set of tools.
2. Inspect the model response and its stop reason.
3. Parse and schema-validate any requested tool call.
4. Authorize the request independently of the model.
5. Execute the approved external tool.
6. Return a constrained tool result to the model.
7. Continue, conclude, escalate, or terminate based on explicit policy.

Conceptual pattern:

```python
while within_execution_budget(workflow_state):
    response = llm(messages, tools=allowed_tools)

    if response.stop_reason == "tool_use":
        request = validate_tool_call(response.tool_call)
        authorize(request, user_context, agent_policy)
        result = execute_tool(request)
        messages.append(constrain_tool_result(result))
        continue

    if response.stop_reason == "end_turn":
        return response.final_answer

    if response.stop_reason in ["max_tokens", "error", "safety"]:
        return handle_termination(response, workflow_state)

return escalate_or_fail_safely(workflow_state)
```

This is an architectural pattern from the speaker, not production-ready code or a prescribed SDK/framework.

### Recommended enterprise component model

| Component | Responsibility |
|---|---|
| User application/channel | Accepts requests and presents answers, citations, escalation status, and approval prompts |
| Agent orchestrator | Owns workflow state, loop logic, stop-reason handling, budgets, routing, retries, and escalation |
| LLM/model endpoint | Produces natural-language responses and structured tool-call requests |
| Tool gateway | Exposes typed, approved business operations and independently enforces API authorization |
| Retrieval/data layer | Provides governed access to knowledge, operational data, and analytics outputs |
| Artifact store | Retains raw logs, retrieved records, tool outputs, summaries, and evidence references outside model context |
| Governance/telemetry plane | Captures traces, policy decisions, token/cost usage, tool calls, quality outcomes, and audit history |

For Superior Propane, an Azure-oriented implementation could use an Azure-hosted orchestration service, models deployed through **Azure AI Foundry** or Azure OpenAI where appropriate, controlled APIs for business tools, and Databricks-curated data products. The source does not prescribe these Microsoft products; they are the relevant implementation interpretation.

---

## 2. Stop reasons and bounded execution are mandatory controls

The speaker specifically warns against treating any model response as a final answer without checking why generation stopped.

Relevant stop conditions include:

- **Tool use:** The model requests an external action or data retrieval. Validate and authorize before execution.
- **Normal completion/end turn:** Return the final response only if policy and quality checks pass.
- **Maximum tokens:** The output may be incomplete even if it appears coherent.
- **Safety/content-filter termination:** Do not silently present partial results as a completed answer.
- **Model/API error or timeout:** Preserve state, provide an appropriate response, and determine retry/escalation behavior.

Production systems should additionally define:

- Maximum loop iterations.
- Maximum number of tool calls.
- Maximum elapsed execution time.
- Per-session token and monetary budgets.
- Duplicate/repeated tool-call detection.
- Invalid schema or malformed parameter handling.
- Tool failures and partial responses.
- User cancellation.
- Rate limits and dependency outages.

These controls prevent runaway cost, repeated side effects, incomplete customer responses, and accidental execution of operational actions.

---

## 3. Tool governance: validate, authorize, and constrain every request

The primary security risk is not that a model can request a tool; it is that the platform may accept and execute a model-generated request without sufficient controls.

Required controls:

- **Typed tool schemas:** Define required fields, types, allowed values, length constraints, and business validations.
- **Allowlisting:** Give each agent only the one or two tools required for its function.
- **Independent authorization:** The downstream API/tool service must validate the user, workload identity, role, account scope, and environment. Do not trust the LLM or orchestrator as the sole authorization source.
- **Least privilege:** Begin with read-only tools and narrow API operations.
- **Confirmation and approvals:** Require user confirmation, workflow approval, or human review for irreversible or high-impact actions.
- **Idempotency and duplicate protection:** Prevent repeated tool calls from creating duplicate cases, updates, payments, or dispatch actions.
- **Input treatment as untrusted:** Tool arguments remain untrusted even when generated by the model.
- **Prompt-injection resistance:** Retrieved documents, logs, customer messages, tickets, and code may contain malicious instructions. They must not override system policy or cause unauthorized tool use.

Example low-risk, typed tool set for an initial support assistant:

```text
get_delivery_status(customer_id, delivery_id)
get_service_appointment(customer_id)
get_account_balance(customer_id)
search_approved_knowledge_base(query, category)
create_case_draft(customer_id, summary, suggested_next_steps)
```

The final tool should create a **draft**, not automatically submit or alter a customer record.

---

## 4. Specialize agents; do not default to a broadly tooled “do everything” agent

The speaker recommends avoiding an agent loaded with many unrelated tools. Instead, use narrowly scoped agents with a well-defined role, constrained context, and only relevant tool access.

Examples:

- Data retrieval agent: accesses approved operational data views.
- Knowledge agent: searches approved SOPs and policy documents.
- Log analysis agent: clusters errors and identifies affected services.
- Critic/validator agent: assesses whether a claim is supported by evidence.
- Coordinator: routes tasks but has no direct high-risk operational access.

This design aligns with least privilege, separation of duties, and single-responsibility principles.

### Trade-offs

Specialization can reduce tool ambiguity and improve auditability, but multi-agent systems are not automatically better:

| Potential benefit | Operational cost |
|---|---|
| Narrower permissions and easier policy enforcement | More model calls, tokens, latency, and cost |
| More focused prompts and evaluation | Agent handoff and state-management failures |
| Better separation of evidence gathering and action decisions | More complex tracing and incident diagnosis |
| Reduced context exposure | Harder end-to-end reproducibility |
| Independent critique | Critic may still produce plausible but incorrect feedback |

The speaker’s claim that specialized agents are preferable should be tested against a constrained single-agent baseline for each use case.

---

## 5. Context isolation and artifact passing

The presentation strongly emphasizes that context is an operational resource—not simply a model capacity to maximize.

### Anti-pattern

Do not allow all raw tool outputs, long logs, intermediate subagent responses, historical messages, and internal reasoning to accumulate in the main agent conversation. This can:

- Increase token consumption and inference cost.
- Introduce irrelevant or contradictory information.
- Increase exposure of customer or operational data.
- Make retrieval provenance unclear.
- Allow untrusted retrieved content to contaminate subsequent decisions.
- Cause agents to converge on prior framing rather than independently evaluate evidence.

### Recommended pattern: isolated context forks

1. The parent workflow assigns a bounded task.
2. A subagent receives a separate context/session.
3. The subagent can process raw artifacts such as logs, documents, or query results.
4. It writes outputs to controlled storage.
5. It returns only a compact structured artifact to the parent.
6. The parent receives source references rather than raw bulk content.

```text
Parent orchestrator / main agent
  └─ Assign bounded task
       |
       v
Isolated subagent context
  ├─ Reads approved raw artifacts
  ├─ Performs retrieval, filtering, or analysis
  ├─ Stores evidence and results externally
  └─ Returns structured summary + evidence pointers
       |
       v
Parent context
  └─ Receives minimum necessary result
```

Useful returned fields:

```json
{
  "summary": "Three recurring timeout signatures were found in the delivery integration.",
  "evidence_ids": ["log-query-284", "adls-artifact-912"],
  "affected_assets": ["pipeline-x", "api-y"],
  "severity": "medium",
  "known_gaps": ["No traces available for 02:00-02:15 UTC"],
  "recommended_next_action": "Run approved network diagnostic",
  "requires_human_review": true
}
```

The speaker advises not to pass full “thought processes” between agents. For enterprise use, this is appropriate: preserve **verifiable outputs, source IDs, tool results, and structured rationales**, not hidden chain-of-thought.

---

## 6. Critic agents should receive claims and evidence, not full upstream context

A specific pattern discussed is an independent critic agent.

The producer/worker agent should emit:

- A proposed claim, decision, or recommendation.
- Evidence references.
- Tool outputs or source IDs.
- Known limitations and missing data.
- A structured confidence/quality indicator.

The critic should receive the claim and evidence—not the worker’s entire intermediate history—and return a structured assessment.

```text
Worker agent
  └─ Claim + evidence references
       |
       v
Critic agent
  └─ Support/contradiction/missing-evidence assessment
       |
       v
Orchestrator
  └─ Accept, retry, retrieve more, revise, or escalate
```

Example critic schema:

```json
{
  "verdict": "supported | partially_supported | unsupported | insufficient_evidence",
  "evidence_assessment": [],
  "contradictions": [],
  "missing_evidence": [],
  "recommended_next_action": "accept | retrieve_more | revise_claim | human_review"
}
```

A critic model is not an authoritative validator on its own. It requires evaluation against known cases to determine whether it detects real errors rather than generating superficially plausible critiques.

---

## 7. Context budgets and compaction

The speaker states that increasing context increases token-related cost and may reduce answer quality through distraction or irrelevant material. The cost direction is established for token-priced inference, though exact pricing depends on provider, model, cache behavior, and batch terms. The quality assertion should be treated as a testable hypothesis, not a universal rule.

Recommended controls:

- Maximum input and output tokens per agent.
- Maximum documents, logs, and retrieval results attached to each invocation.
- Metadata filtering and reranking before retrieval.
- Time-window filtering for telemetry/log analysis.
- Structured extraction instead of entire-record injection.
- External storage of large artifacts, with IDs and excerpts supplied to the model.
- Periodic compaction of long-running sessions.

The speaker cites **150,000 tokens** as an example compaction threshold and references Claude compaction behavior without implementation details. This exact threshold, feature behavior, and cost model must not be assumed to apply to Azure AI Foundry, Azure OpenAI, or other providers.

### Provider-neutral compaction process

1. Track session token usage and workflow state.
2. At a defined workload-specific threshold:
   - retain critical facts, decisions, user authorization state, constraints, unresolved work, source references, and security policy state;
   - summarize lower-value historical exchanges;
   - archive raw content externally;
   - resume with a clean or reduced context.
3. Validate continuation quality against the archived evidence.

A compacted summary is a derived artifact, not a new source of truth. It should be versioned and linked to:

- Original source records.
- Prompt and model/deployment version.
- Workflow/run ID.
- Timestamp and authoring component.
- Validation results.

---

## 8. Customer-support flow and human escalation

The support example in the presentation follows a standard tool-use loop:

1. A customer asks a question.
2. The agent receives the conversation, relevant context, and approved tools.
3. The model requests data or an operation.
4. The platform validates and executes the request.
5. The result is returned to the model.
6. The model either performs another bounded step, answers, or escalates.

The speaker proposes checking quality/confidence before escalating. This requires caution: **self-reported LLM confidence is not a reliable standalone production control.**

More defensible escalation criteria include:

- Identity verification is incomplete.
- Required tools return errors, stale information, or no result.
- The scenario involves safety, payment disputes, complaints, regulatory matters, or delivery exceptions.
- Requested actions are irreversible or customer-impacting.
- The answer lacks an approved authoritative source.
- The request is ambiguous or conflicts with account context.
- Evaluation/calibration signals indicate low expected accuracy.
- Token, tool-call, latency, or spend budgets are exceeded.

---

## 9. Developer tooling, Claude Code, and CI/CD

The speaker discusses **Claude Code** and hierarchical `CLAUDE.md` instruction files, claiming Anthropic recommends instructions at:

1. The project root.
2. A project-folder level.
3. Lower directory/module levels.

The transferable engineering principle is useful: maintain **version-controlled, scoped instructions near the relevant code**. Exact `CLAUDE.md` inheritance and precedence behavior should be verified against current Anthropic documentation before standardizing it.

For Superior Propane engineering teams, analogous repository-scoped guidance can include:

- Approved Azure SDK and managed identity patterns.
- No secrets or production data in code, prompts, test fixtures, or logs.
- Required unit and integration tests for tools and schemas.
- Databricks and Unity Catalog coding/access standards.
- Threat-model requirements for new agent tools.
- Mandatory observability, correlation IDs, and audit events.
- Approved deployment and infrastructure-as-code practices.

### CI/CD implication

The speaker warns against interactive agent modes in unattended CI pipelines. Interactive confirmation requests can stall builds or deployments.

Use non-interactive execution only for tightly bounded tasks, such as:

- Pull-request review.
- Test generation.
- Summarization of build failures.
- Static review of Databricks notebooks, Python, SQL, Terraform, or Bicep.
- Detection of potential secrets, insecure patterns, or policy violations.

Non-interactive execution must not become blanket permission to change production resources. Maintain:

- Read-only or PR-scoped access by default.
- Least-privilege managed identities/service principals.
- Repository, branch, subscription, resource-group, and Databricks workspace allowlists.
- Pull requests and standard test gates.
- Human approval for production releases, infrastructure changes, deletions, broad updates, or safety/customer-impacting configuration changes.
- Audit logs for all agent actions and approvals.

---

## 10. Batch inference: cost/latency trade-off

The speaker claims batch prompting can provide **50% lower token cost** with delivery in **at least 24 hours**. These specific economics and timing are provider-, model-, region-, and contract-dependent. They should not be assumed for Azure AI Foundry or Azure OpenAI without confirming current service documentation and commercial terms.

The general principle is valid: asynchronous/batch processing can lower unit cost where immediate results are unnecessary.

Good candidate workloads:

- Offline evaluation of agent behavior.
- Large-scale log/error summarization.
- Nightly document classification and metadata enrichment.
- Knowledge-base summarization or backfill.
- Extraction of structured data from historical support notes, subject to privacy controls.
- Databricks data-quality issue triage.

Poor candidate workloads:

- Customer-facing real-time chat.
- Emergency or propane safety workflows.
- Time-sensitive dispatch or delivery decisions.
- Active production incident response where delay affects recovery.

---

# Potential applications for Superior Propane

## 1. Read-only customer-service copilot

A controlled assistant could support customer-service staff initially, and potentially customers for narrow low-risk intents later.

Potential use cases:

- Delivery-status questions.
- Service appointment information.
- Account/billing explanations using verified data.
- Approved policy and self-service guidance.
- Safety information drawn only from authoritative, approved sources.
- Case summarization and suggested next steps for support representatives.

Recommended first-release boundaries:

- Read-only account, delivery, and appointment lookup.
- Knowledge retrieval from approved and versioned content.
- Draft-only case creation.
- Mandatory identity verification before account-specific lookup.
- Escalation for safety, financial, complaint, regulatory, or exception scenarios.
- No autonomous changes to customer profile, delivery, scheduling, payment, or account status.

---

## 2. Databricks and Azure incident-analysis assistant

A bounded, context-forked agent workflow could improve platform and data-pipeline incident triage.

Possible architecture:

- **Sources:** Azure Monitor, Log Analytics, Databricks job logs, workflow records, runbooks, and curated operational metrics.
- **Analysis subagent:** Receives a bounded incident window and approved source access.
- **Artifact storage:** Raw logs and query results remain in ADLS Gen2, Log Analytics, or governed Databricks tables.
- **Output:** Error clusters, affected jobs/tables/services, timeline, severity, evidence IDs/query links, and suggested runbook steps.
- **Critic:** Evaluates whether recommendations are supported by the retrieved evidence.
- **Human engineer:** Approves any remediation.

This should remain advisory until measured performance demonstrates acceptable accuracy, security, and operator acceptance.

---

## 3. Governed enterprise knowledge assistant

A knowledge assistant could support internal users with operations, safety, customer-service, IT, and data-platform procedures.

Key design requirements:

- Entra ID-aware authorization at retrieval time.
- Authoritative-source controls, document versioning, and citations.
- Minimal, reranked evidence set rather than broad corpus injection.
- Context budgets and retention/redaction rules.
- Clear disclosure when evidence is missing or outdated.
- Evaluation against representative business questions and policy interpretations.

This is particularly relevant for safety procedures, field operations, IT runbooks, and customer-service policies, where incorrect or out-of-date advice could have operational consequences.

---

## 4. Governed data-access research assistant

A specialized workflow can support internal analysis of delivery exceptions, recurring support issues, operational trends, or data-pipeline anomalies.

Recommended separation:

- Data retrieval agent accesses only curated Databricks views or approved APIs.
- Knowledge agent searches SOPs and internal documentation.
- Analysis agent produces an evidence-linked summary.
- Coordinator sequences steps but has no direct broad data or write access.

Use **Unity Catalog** permissions, curated views/data products, and row/column controls rather than unrestricted access to raw operational tables.

---

## 5. AI-assisted engineering quality controls

Use constrained AI agents in development workflows to:

- Review pull requests.
- Generate or propose tests.
- Summarize CI failures.
- Detect data-governance, secrets, or security-policy issues.
- Check agent-tool schemas and prompt/configuration changes.
- Review Databricks notebooks, SQL, Python, Terraform/Bicep, and Azure configurations.

AI output should inform existing engineering governance, not replace it or independently deploy to production.

---

# Risks and validation questions

## Security and authorization

- Is every tool call schema-validated before execution?
- Are tools allowlisted by agent role, user role, environment, and use case?
- Does the downstream tool/API independently authorize the requester?
- Are high-risk actions gated by confirmation and human approval?
- Are tool calls idempotent and protected against duplicate execution?
- Can prompt injection in documents, logs, tickets, or user input manipulate tool selection?
- Are model-generated values treated as untrusted input?
- Are service identities restricted to required Azure subscriptions, resource groups, APIs, repositories, Databricks workspaces, and data assets?

## Data governance and privacy

- Which customer, billing, delivery, field-service, and operational records are permitted to reach the selected model endpoint?
- Are row-, column-, and document-level permissions enforced in Databricks/Unity Catalog and retrieval systems?
- Are prompts, tool outputs, traces, and evaluation datasets redacted and retained according to policy?
- Are model endpoint data handling, regional deployment, networking, retention, and enterprise terms appropriate for the data class?
- Can every answer be traced to an approved source version, query, tool result, or record ID?
- Are compaction summaries versioned and linked to their original evidence?

## Reliability and answer quality

- What is the expected behavior when a tool returns stale data, no data, malformed content, or an API error?
- Can the system distinguish an actual business result—such as “no delivery is scheduled”—from a technical lookup failure?
- Does the assistant ground final answers in approved sources and verified tool results?
- How will hallucination, unsupported claims, and incorrect escalation be measured?
- Does a critic agent catch meaningful errors in testing, or merely generate plausible commentary?
- How much quality is lost through context summarization or compaction?
- What happens when token, time, loop, or budget limits are reached?

## Cost and operational trade-offs

Track all-in cost per correctly completed workflow, including:

- Input, output, and cached tokens where relevant.
- Tool calls and orchestration compute.
- Retrieval/vector indexing and storage.
- Artifact retention and telemetry.
- Human-review and exception-handling effort.
- Latency, loop counts, repeated calls, and escalation rate.

Validate whether multi-agent architecture materially improves outcomes enough to justify greater operational complexity. Test:

1. A constrained single-agent design.
2. A specialized multi-agent design.
3. Retrieval-only or deterministic workflow alternatives.

## Speaker claims requiring validation

- **“Loops give agentic systems their power.”** Loops enable iterative workflows, but business value depends on tool quality, data access, controls, workflow design, and evaluation.
- **Specialized agents are better than broadly tooled agents.** Often beneficial for governance, but potentially slower, more expensive, and harder to operate.
- **More context makes models confused.** Plausible, but task-, model-, and prompt-dependent; test empirically.
- **150,000-token compaction threshold.** This is an example, not an enterprise standard.
- **Claude/Anthropic compaction behavior.** The speaker does not provide implementation details; verify current official documentation.
- **50% batch discount and 24-hour turnaround.** Provider-specific; validate for the selected Azure/AI Foundry service, model, region, and agreement.
- **Claude Code `CLAUDE.md` hierarchy.** Confirm exact current behavior and precedence before adopting it.
- **Claude certification cost, retake cadence, and exam-domain percentages.** Verify directly with Anthropic.

---

# Action items

1. **Define an enterprise agent orchestration standard**
   - Require explicit handling for tool use, end turn, max tokens, safety stops, API errors, timeouts, and cancellation.
   - Set standard limits for turns, tool calls, runtime, token usage, and per-workflow spend.
   - Define retry, escalation, and failure-response policies.

2. **Build or standardize a controlled tool gateway**
   - Implement small, typed, schema-validated APIs.
   - Enforce authorization at the API and data layer.
   - Apply read-only access by default.
   - Add idempotency, approval gates, immutable audit events, and policy-decision logging.

3. **Establish an agent context-management pattern**
   - Require context budgets, retrieval filtering/reranking, artifact references, and structured subagent outputs.
   - Prohibit unbounded accumulation of raw logs, documents, and subagent messages in parent contexts.
   - Define versioned compaction policies by use case.

4. **Pilot a narrow customer-service copilot**
   - Start with delivery status, approved policy Q&A, appointment information, or case-summary drafting.
   - Use verified identity, read-only tools, citations, and human escalation.
   - Exclude autonomous account, payment, delivery, and scheduling changes from the initial release.

5. **Pilot context-forked Azure/Databricks log triage**
   - Use non-production or sanitized data initially.
   - Compare full-context, retrieval-only, and isolated-subagent approaches.
   - Measure accuracy, evidence quality, latency, token consumption, cost, and engineer acceptance.

6. **Create a standard agent artifact contract**
   - Require claim/summary, evidence IDs, source versions, tool results, confidence limitations, and recommended next action.
   - Avoid persisting or relying on hidden chain-of-thought.

7. **Implement observability and FinOps telemetry**
   - Capture model/deployment version, prompts/context metadata, retrieval set size, tool calls, latency, token use, compaction events, policy decisions, costs, and human-review outcomes.
   - Publish operational dashboards for platform, product, security, and finance stakeholders.

8. **Define a safe AI-assisted CI operating model**
   - Permit non-interactive execution only for bounded, low-risk analysis or PR-scoped checks.
   - Enforce branch protections, testing, least privilege, tool allowlists, and human approval for production-impacting changes.
   - Add source-controlled engineering instructions for Azure, Databricks, secrets, testing, and governance patterns.

9. **Validate provider capabilities before product commitments**
   - Confirm Azure AI Foundry/Azure OpenAI model availability, regional deployment, data handling, batch options, pricing, quotas, and retention controls.
   - Separately verify Anthropic-specific claims if considering Claude, Claude Code, or the certification program.

## Full transcript

[00:14] &gt;&gt; Okay, I'm getting rolling and uh welcome
[00:14] &gt;&gt; Okay, I'm getting rolling and uh welcome aboard. We just had a little technical
[00:16] aboard. We just had a little technical
[00:16] aboard. We just had a little technical issues,
[00:17] issues,
[00:17] issues, but uh we resolved them. So, my name is
[00:18] but uh we resolved them. So, my name is
[00:19] but uh we resolved them. So, my name is Frank Coyle.
[00:20] Frank Coyle.
[00:20] Frank Coyle. Uh I am a computer science guy. I've
[00:23] Uh I am a computer science guy. I've
[00:23] Uh I am a computer science guy. I've been teaching computer science for over
[00:25] been teaching computer science for over
[00:25] been teaching computer science for over 30 years,
[00:26] 30 years,
[00:26] 30 years, and I'm now teaching at Berkeley. And
[00:29] and I'm now teaching at Berkeley. And
[00:29] and I'm now teaching at Berkeley. And one of the problems that uh all my
[00:30] one of the problems that uh all my
[00:30] one of the problems that uh all my students,
[00:31] students,
[00:32] students, past and present, are having is AI,
[00:34] past and present, are having is AI,
[00:34] past and present, are having is AI, because computer science is no longer
[00:37] because computer science is no longer
[00:37] because computer science is no longer the magic pathway to a job. So, I've
[00:41] the magic pathway to a job. So, I've
[00:41] the magic pathway to a job. So, I've been trying to figure out ways to uh
[00:43] been trying to figure out ways to uh
[00:43] been trying to figure out ways to uh help them come up with schemes to help
[00:46] help them come up with schemes to help
[00:46] help them come up with schemes to help them get ready for this world of agentic
[00:48] them get ready for this world of agentic
[00:48] them get ready for this world of agentic AI. And one of the things that sort of
[00:51] AI. And one of the things that sort of
[00:51] AI. And one of the things that sort of uh
[00:51] uh
[00:51] uh dropped into my uh plate was the
[00:55] dropped into my uh plate was the
[00:55] dropped into my uh plate was the something called the Claude Certified
[00:57] something called the Claude Certified
[00:57] something called the Claude Certified Architect exam, which I will be talking
[00:59] Architect exam, which I will be talking
[00:59] Architect exam, which I will be talking about today, and it has um a number of
[01:03] about today, and it has um a number of
[01:03] about today, and it has um a number of aspects to it. And I think if you're
[01:04] aspects to it. And I think if you're
[01:04] aspects to it. And I think if you're interested in a career in agentic AI,
[01:07] interested in a career in agentic AI,
[01:07] interested in a career in agentic AI, then certainly take a look at least what
[01:09] then certainly take a look at least what
[01:09] then certainly take a look at least what the exam is about, because I feel that
[01:12] the exam is about, because I feel that
[01:12] the exam is about, because I feel that um Anthropic knows how people are using
[01:16] um Anthropic knows how people are using
[01:16] um Anthropic knows how people are using their system and what the issues are
[01:18] their system and what the issues are
[01:18] their system and what the issues are going to be.
[01:19] going to be.
[01:19] going to be. So, before we jump into that, I want to
[01:21] So, before we jump into that, I want to
[01:21] So, before we jump into that, I want to give a little bit of my
[01:23] give a little bit of my
[01:23] give a little bit of my uh
[01:23] uh
[01:23] uh my philosophy.
[01:34] May have to do this manually, getting
[01:34] May have to do this manually, getting stuck.
[01:36] stuck.
[01:36] stuck. So,
[01:37] So,
[01:37] So, this is a quote from uh
[01:40] this is a quote from uh
[01:40] this is a quote from uh a woman named Sister Corita Kent.
[01:42] a woman named Sister Corita Kent.
[01:42] a woman named Sister Corita Kent. Nothing is a mistake. There's no win and
[01:45] Nothing is a mistake. There's no win and
[01:45] Nothing is a mistake. There's no win and no fail. There's only make.
[01:48] no fail. There's only make.
[01:48] no fail. There's only make. Bottom line here is experiment,
[01:50] Bottom line here is experiment,
[01:50] Bottom line here is experiment, experiment, experiment. Not only should
[01:53] experiment, experiment. Not only should
[01:53] experiment, experiment. Not only should you read, but you should do. You should
[01:55] you read, but you should do. You should
[01:55] you read, but you should do. You should make stuff. Now, what happens when you
[01:58] make stuff. Now, what happens when you
[01:58] make stuff. Now, what happens when you make stuff? A lot of times things don't
[02:01] make stuff? A lot of times things don't
[02:01] make stuff? A lot of times things don't work.
[02:03] work.
[02:03] work. Thomas Edison said, "I have not failed.
[02:07] Thomas Edison said, "I have not failed.
[02:07] Thomas Edison said, "I have not failed. I've only found 10,000 ways
[02:09] I've only found 10,000 ways
[02:09] I've only found 10,000 ways that don't work."
[02:11] that don't work."
[02:11] that don't work." And
[02:13] And
[02:13] And what I want to emphasize here is that
[02:15] what I want to emphasize here is that
[02:15] what I want to emphasize here is that what this shows us are something that in
[02:18] what this shows us are something that in
[02:18] what this shows us are something that in the design patterns movement, which came
[02:20] the design patterns movement, which came
[02:20] the design patterns movement, which came around in the early 1990s with
[02:22] around in the early 1990s with
[02:22] around in the early 1990s with object-oriented programming, we had
[02:24] object-oriented programming, we had
[02:24] object-oriented programming, we had patterns for objects. We now have
[02:27] patterns for objects. We now have
[02:27] patterns for objects. We now have patterns for agents, but there's also
[02:30] patterns for agents, but there's also
[02:30] patterns for agents, but there's also anti-patterns. And I think anti-patterns
[02:32] anti-patterns. And I think anti-patterns
[02:32] anti-patterns. And I think anti-patterns are a key
[02:34] are a key
[02:34] are a key to understanding what you should not do
[02:37] to understanding what you should not do
[02:37] to understanding what you should not do because understanding what you should
[02:38] because understanding what you should
[02:38] because understanding what you should not do is the key to leading you to what
[02:41] not do is the key to leading you to what
[02:41] not do is the key to leading you to what you should do.
[02:46] So, a little bit about the Claude
[02:46] So, a little bit about the Claude Certified Exam, released in March, so
[02:49] Certified Exam, released in March, so
[02:49] Certified Exam, released in March, so it's brand new.
[02:50] it's brand new.
[02:50] it's brand new. It is uh
[02:52] It is uh
[02:52] It is uh it is
[02:53] it is
[02:53] it is based on scenarios. It is timed. It is
[02:56] based on scenarios. It is timed. It is
[02:56] based on scenarios. It is timed. It is proctored.
[02:57] proctored.
[02:57] proctored. It is available to companies in the
[03:01] It is available to companies in the
[03:01] It is available to companies in the Claude ecosystem, the Anthropic
[03:03] Claude ecosystem, the Anthropic
[03:03] Claude ecosystem, the Anthropic ecosystem, but individuals can pay $99
[03:06] ecosystem, but individuals can pay $99
[03:06] ecosystem, but individuals can pay $99 and take the exam once every once every
[03:09] and take the exam once every once every
[03:09] and take the exam once every once every 6 months.
[03:11] 6 months.
[03:11] 6 months. And it's not just
[03:13] And it's not just
[03:13] And it's not just multiple-choice questions. It is
[03:15] multiple-choice questions. It is
[03:15] multiple-choice questions. It is multiple-choice, but they're
[03:17] multiple-choice, but they're
[03:17] multiple-choice, but they're they are based on
[03:19] they are based on
[03:19] they are based on uh realistic constraints and realistic
[03:22] uh realistic constraints and realistic
[03:22] uh realistic constraints and realistic scenarios.
[03:24] scenarios.
[03:24] scenarios. The five domains.
[03:26] The five domains.
[03:26] The five domains. There are five domains that are covered
[03:27] There are five domains that are covered
[03:28] There are five domains that are covered and they give you the percentages of
[03:29] and they give you the percentages of
[03:29] and they give you the percentages of each. So, agentic architecture, 27%.
[03:33] each. So, agentic architecture, 27%.
[03:33] each. So, agentic architecture, 27%. Claude code, how to configure the Claude
[03:35] Claude code, how to configure the Claude
[03:35] Claude code, how to configure the Claude code system and workflow, 20%. How to
[03:40] code system and workflow, 20%. How to
[03:40] code system and workflow, 20%. How to doing prompt engineering, structuring
[03:42] doing prompt engineering, structuring
[03:42] doing prompt engineering, structuring your output, using JSON all over the
[03:45] your output, using JSON all over the
[03:46] your output, using JSON all over the place.
[03:47] place.
[03:47] place. Tool design. Model context protocol
[03:50] Tool design. Model context protocol
[03:50] Tool design. Model context protocol integration. These are topics that you
[03:52] integration. These are topics that you
[03:52] integration. These are topics that you should understand and know whether
[03:54] should understand and know whether
[03:54] should understand and know whether you're going to take the exam or not.
[03:56] you're going to take the exam or not.
[03:56] you're going to take the exam or not. This is going to help you get ready for
[03:58] This is going to help you get ready for
[03:58] This is going to help you get ready for whatever
[04:00] whatever
[04:00] whatever the agentic world is going to throw at
[04:02] the agentic world is going to throw at
[04:02] the agentic world is going to throw at you. And then there's going to be
[04:03] you. And then there's going to be
[04:03] you. And then there's going to be contact management and reliability. So
[04:06] contact management and reliability. So
[04:06] contact management and reliability. So these are the
[04:07] these are the
[04:07] these are the areas of of the kind of questions you're
[04:10] areas of of the kind of questions you're
[04:10] areas of of the kind of questions you're going to run into.
[04:13] going to run into.
[04:13] going to run into. Then there are and they they provide you
[04:16] Then there are and they they provide you
[04:16] Then there are and they they provide you with six production scenarios and your
[04:20] with six production scenarios and your
[04:20] with six production scenarios and your the exam will randomly choose four and
[04:24] the exam will randomly choose four and
[04:24] the exam will randomly choose four and all the questions will be centered
[04:26] all the questions will be centered
[04:26] all the questions will be centered around the four that they choose.
[04:29] around the four that they choose.
[04:29] around the four that they choose. And what I'm going to do is walk you
[04:31] And what I'm going to do is walk you
[04:31] And what I'm going to do is walk you through
[04:32] through
[04:32] through um
[04:34] um
[04:34] um the production scenarios and give you
[04:36] the production scenarios and give you
[04:36] the production scenarios and give you some anti-patterns to be aware of
[04:38] some anti-patterns to be aware of
[04:38] some anti-patterns to be aware of because there's a number of ways you can
[04:40] because there's a number of ways you can
[04:40] because there's a number of ways you can solve the problem but one of the big
[04:41] solve the problem but one of the big
[04:41] solve the problem but one of the big things is what not to do and that often
[04:44] things is what not to do and that often
[04:44] things is what not to do and that often can be the key to getting these
[04:46] can be the key to getting these
[04:46] can be the key to getting these questions right. So, number one customer
[04:49] questions right. So, number one customer
[04:49] questions right. So, number one customer support resolution agent. So we have
[04:51] support resolution agent. So we have
[04:51] support resolution agent. So we have agentic loops, control, something called
[04:54] agentic loops, control, something called
[04:54] agentic loops, control, something called stop reason which is
[04:56] stop reason which is
[04:56] stop reason which is uh what Cloud Code has. Every time
[04:58] uh what Cloud Code has. Every time
[04:58] uh what Cloud Code has. Every time something happens, there's a stop reason
[05:01] something happens, there's a stop reason
[05:01] something happens, there's a stop reason and you need to take a look at that
[05:02] and you need to take a look at that
[05:02] and you need to take a look at that because that can give you a lot of
[05:03] because that can give you a lot of
[05:03] because that can give you a lot of information about what's going on.
[05:05] information about what's going on.
[05:05] information about what's going on. Uh scenario two, code generation.
[05:08] Uh scenario two, code generation.
[05:08] Uh scenario two, code generation. Three, multi-agent research system which
[05:11] Three, multi-agent research system which
[05:11] Three, multi-agent research system which we'll look at. How do you How do you
[05:14] we'll look at. How do you How do you
[05:14] we'll look at. How do you How do you distribute your agents? Hub and spoke.
[05:17] distribute your agents? Hub and spoke.
[05:17] distribute your agents? Hub and spoke. Who's the orchestrator? How much
[05:18] Who's the orchestrator? How much
[05:18] Who's the orchestrator? How much information should they know? All these
[05:20] information should they know? All these
[05:21] information should they know? All these are important factors. Um
[05:23] are important factors. Um
[05:23] are important factors. Um scenario four, developer
[05:26] scenario four, developer
[05:26] scenario four, developer productivity with code. So how do you do
[05:28] productivity with code. So how do you do
[05:28] productivity with code. So how do you do subtask isolation? Keep your tasks in
[05:31] subtask isolation? Keep your tasks in
[05:31] subtask isolation? Keep your tasks in their little universes. And this
[05:33] their little universes. And this
[05:33] their little universes. And this hearkens back to what we learn in
[05:35] hearkens back to what we learn in
[05:35] hearkens back to what we learn in computer science from doing
[05:36] computer science from doing
[05:36] computer science from doing multi-threaded programming.
[05:38] multi-threaded programming.
[05:39] multi-threaded programming. When you have multiple threads operating
[05:40] When you have multiple threads operating
[05:40] When you have multiple threads operating and sharing memory, then you get into
[05:43] and sharing memory, then you get into
[05:43] and sharing memory, then you get into issues with synchronization. You You to
[05:45] issues with synchronization. You You to
[05:45] issues with synchronization. You You to put locks
[05:47] put locks
[05:47] put locks Keep the little threads independent.
[05:50] Keep the little threads independent.
[05:50] Keep the little threads independent. Keep your agents independent.
[05:52] Keep your agents independent.
[05:52] Keep your agents independent. Um
[05:54] Um
[05:54] Um and then some cloud code for continuous
[05:56] and then some cloud code for continuous
[05:56] and then some cloud code for continuous integration.
[05:57] integration.
[05:58] integration. And then we'll look at some patterns for
[06:00] And then we'll look at some patterns for
[06:00] And then we'll look at some patterns for structured data extraction. Okay, that's
[06:04] structured data extraction. Okay, that's
[06:04] structured data extraction. Okay, that's kind of where we're going to go.
[06:06] kind of where we're going to go.
[06:06] kind of where we're going to go. Now, here's something that I I I like to
[06:09] Now, here's something that I I I like to
[06:09] Now, here's something that I I I like to point out. Everybody's talking about
[06:11] point out. Everybody's talking about
[06:11] point out. Everybody's talking about loops, right? Every The loop is the new
[06:13] loops, right? Every The loop is the new
[06:13] loops, right? Every The loop is the new thing.
[06:14] thing.
[06:14] thing. Um
[06:16] Um
[06:16] Um uh Boris Cherney says he doesn't write
[06:19] uh Boris Cherney says he doesn't write
[06:19] uh Boris Cherney says he doesn't write code, but his job is to write loops.
[06:22] code, but his job is to write loops.
[06:22] code, but his job is to write loops. And Peter Steinberger
[06:24] And Peter Steinberger
[06:24] And Peter Steinberger master of Open Claw says, "I don't I
[06:26] master of Open Claw says, "I don't I
[06:26] master of Open Claw says, "I don't I don't uh I don't code anymore. I just
[06:28] don't uh I don't code anymore. I just
[06:28] don't uh I don't code anymore. I just design loops
[06:30] design loops
[06:30] design loops that prompt your agents."
[06:32] that prompt your agents."
[06:32] that prompt your agents." So, loops are the new big thing, right?
[06:34] So, loops are the new big thing, right?
[06:34] So, loops are the new big thing, right? Well, no, they're not. Okay? Um
[06:38] Well, no, they're not. Okay? Um
[06:38] Well, no, they're not. Okay? Um back in the day
[06:40] back in the day
[06:40] back in the day uh early days of computing, we had
[06:43] uh early days of computing, we had
[06:43] uh early days of computing, we had programming languages were exploding. We
[06:45] programming languages were exploding. We
[06:45] programming languages were exploding. We had Fortran, we had COBOL, and there
[06:47] had Fortran, we had COBOL, and there
[06:47] had Fortran, we had COBOL, and there were big fights. My program My
[06:50] were big fights. My program My
[06:50] were big fights. My program My programming language is better than
[06:52] programming language is better than
[06:52] programming language is better than yours. It can do more. No, it can't. We
[06:55] yours. It can do more. No, it can't. We
[06:55] yours. It can do more. No, it can't. We can do this.
[06:56] can do this.
[06:56] can do this. Böhm and Jacopini, 1966
[06:59] Böhm and Jacopini, 1966
[06:59] Böhm and Jacopini, 1966 proved that if you want a language to be
[07:02] proved that if you want a language to be
[07:02] proved that if you want a language to be Turing complete, which means can compute
[07:05] Turing complete, which means can compute
[07:05] Turing complete, which means can compute anything that computers are possibly
[07:08] anything that computers are possibly
[07:08] anything that computers are possibly able to compute, then you need only
[07:11] able to compute, then you need only
[07:11] able to compute, then you need only three things.
[07:13] three things.
[07:13] three things. The ability to
[07:14] The ability to
[07:14] The ability to to to write statements sequentially,
[07:17] to to write statements sequentially,
[07:17] to to write statements sequentially, okay?
[07:18] okay?
[07:18] okay? To have if-then conditionals, and the
[07:21] To have if-then conditionals, and the
[07:21] To have if-then conditionals, and the third piece is the loop.
[07:24] third piece is the loop.
[07:24] third piece is the loop. If you add the loop,
[07:26] If you add the loop,
[07:26] If you add the loop, you have Turing computability. And now
[07:29] you have Turing computability. And now
[07:29] you have Turing computability. And now we are seeing this being resurrected in
[07:32] we are seeing this being resurrected in
[07:32] we are seeing this being resurrected in the agentic world with the focus on
[07:35] the agentic world with the focus on
[07:35] the agentic world with the focus on loops, cuz up to now we've had sort of
[07:37] loops, cuz up to now we've had sort of
[07:37] loops, cuz up to now we've had sort of sequences. You have prompts, you have
[07:39] sequences. You have prompts, you have
[07:39] sequences. You have prompts, you have maybe if-then, but now we have a loop.
[07:42] maybe if-then, but now we have a loop.
[07:42] maybe if-then, but now we have a loop. And now this is what's giving us the
[07:43] And now this is what's giving us the
[07:43] And now this is what's giving us the power. This is where the agentic stuff
[07:46] power. This is where the agentic stuff
[07:46] power. This is where the agentic stuff is getting very exciting.
[07:48] is getting very exciting.
[07:48] is getting very exciting. Okay.
[07:50] Okay.
[07:50] Okay. I'm start with uh
[07:52] I'm start with uh
[07:52] I'm start with uh with scenario one, customer support
[07:54] with scenario one, customer support
[07:54] with scenario one, customer support resolution.
[07:56] resolution.
[07:56] resolution. So here we have
[08:01] a loop operating and
[08:01] a loop operating and the I'm going to jump to the
[08:03] the I'm going to jump to the
[08:03] the I'm going to jump to the anti-pattern. What you don't want is
[08:05] anti-pattern. What you don't want is
[08:05] anti-pattern. What you don't want is just to let the agent go and do
[08:07] just to let the agent go and do
[08:07] just to let the agent go and do something and get the response back and
[08:11] something and get the response back and
[08:11] something and get the response back and use it, okay? What you want to do is you
[08:13] use it, okay? What you want to do is you
[08:13] use it, okay? What you want to do is you want to loop with something called the
[08:15] want to loop with something called the
[08:15] want to loop with something called the stop reason. So I'm going to show you a
[08:17] stop reason. So I'm going to show you a
[08:17] stop reason. So I'm going to show you a little code here.
[08:19] little code here.
[08:19] little code here. So here we have while loop. It's a while
[08:21] So here we have while loop. It's a while
[08:21] So here we have while loop. It's a while true, it's a loop. We're looping right
[08:23] true, it's a loop. We're looping right
[08:23] true, it's a loop. We're looping right here, okay? So the first little block is
[08:26] here, okay? So the first little block is
[08:26] here, okay? So the first little block is where we call uh we call the model,
[08:29] where we call uh we call the model,
[08:29] where we call uh we call the model, okay? And we pass it the messages. The
[08:31] okay? And we pass it the messages. The
[08:31] okay? And we pass it the messages. The messages are essentially the sequence of
[08:34] messages are essentially the sequence of
[08:34] messages are essentially the sequence of prompts that exist in the context
[08:37] prompts that exist in the context
[08:37] prompts that exist in the context window, okay? And we are asking the and
[08:42] window, okay? And we are asking the and
[08:42] window, okay? And we are asking the and we have a we have a prompt and we have
[08:45] we have a we have a prompt and we have
[08:45] we have a we have a prompt and we have we have the context and we have a tool.
[08:47] we have the context and we have a tool.
[08:47] we have the context and we have a tool. And we're asking the LLM
[08:50] And we're asking the LLM
[08:50] And we're asking the LLM to do something with this tool and help
[08:52] to do something with this tool and help
[08:52] to do something with this tool and help us out. The problem is the LLM can't do
[08:56] us out. The problem is the LLM can't do
[08:56] us out. The problem is the LLM can't do anything. It is just a probabilistic
[08:59] anything. It is just a probabilistic
[08:59] anything. It is just a probabilistic next word predictor.
[09:01] next word predictor.
[09:01] next word predictor. It can't execute tools. So what it does
[09:04] It can't execute tools. So what it does
[09:04] It can't execute tools. So what it does though is it can figure out
[09:08] though is it can figure out
[09:08] though is it can figure out if you point it to a tool, it can figure
[09:11] if you point it to a tool, it can figure
[09:11] if you point it to a tool, it can figure out how to set things up so that you or
[09:14] out how to set things up so that you or
[09:14] out how to set things up so that you or your code can execute it. So it's
[09:17] your code can execute it. So it's
[09:17] your code can execute it. So it's important to understand that the LLM is
[09:18] important to understand that the LLM is
[09:18] important to understand that the LLM is not executing these tools. It can't do
[09:20] not executing these tools. It can't do
[09:20] not executing these tools. It can't do anything except talk back to you, very
[09:23] anything except talk back to you, very
[09:23] anything except talk back to you, very intelligently sometimes, but all it can
[09:25] intelligently sometimes, but all it can
[09:25] intelligently sometimes, but all it can do is talk back to you. So
[09:28] do is talk back to you. So
[09:28] do is talk back to you. So when it finishes
[09:29] when it finishes
[09:29] when it finishes this
[09:31] this
[09:31] this task and has a result which is basically
[09:36] task and has a result which is basically
[09:36] task and has a result which is basically here is I've I know what you want. I
[09:39] here is I've I know what you want. I
[09:39] here is I've I know what you want. I know what the tool can do. Here's how I
[09:42] know what the tool can do. Here's how I
[09:42] know what the tool can do. Here's how I It sets up the parameters that can then
[09:45] It sets up the parameters that can then
[09:45] It sets up the parameters that can then be or that then used to actually execute
[09:48] be or that then used to actually execute
[09:48] be or that then used to actually execute the tool. So, the second block you see
[09:51] the tool. So, the second block you see
[09:51] the tool. So, the second block you see why did
[09:53] why did
[09:53] why did the LLM come back to us? That's our stop
[09:56] the LLM come back to us? That's our stop
[09:56] the LLM come back to us? That's our stop reason.
[09:57] reason.
[09:57] reason. Tool use. Oh, okay. We've stopped
[09:59] Tool use. Oh, okay. We've stopped
[09:59] Tool use. Oh, okay. We've stopped because
[10:00] because
[10:00] because the LLM it wants to use the tool.
[10:03] the LLM it wants to use the tool.
[10:03] the LLM it wants to use the tool. So, let's just run the tool. So, that's
[10:05] So, let's just run the tool. So, that's
[10:05] So, let's just run the tool. So, that's what the second block is. Run tool, the
[10:08] what the second block is. Run tool, the
[10:08] what the second block is. Run tool, the response is what the LLM said, and it's
[10:10] response is what the LLM said, and it's
[10:10] response is what the LLM said, and it's basically the parameters that it has
[10:13] basically the parameters that it has
[10:13] basically the parameters that it has extracted from the data that you
[10:15] extracted from the data that you
[10:15] extracted from the data that you provided it.
[10:17] provided it.
[10:17] provided it. Okay? Then it executes that.
[10:19] Okay? Then it executes that.
[10:19] Okay? Then it executes that. Then it goes back.
[10:20] Then it goes back.
[10:20] Then it goes back. That then it continues. Continues means
[10:23] That then it continues. Continues means
[10:23] That then it continues. Continues means the LLM sees it and says, "Oh,
[10:25] the LLM sees it and says, "Oh,
[10:25] the LLM sees it and says, "Oh, successful run. So, okay."
[10:28] successful run. So, okay."
[10:28] successful run. So, okay." Come back down.
[10:31] Come back down.
[10:31] Come back down. We're not running a tool anymore. We're
[10:32] We're not running a tool anymore. We're
[10:32] We're not running a tool anymore. We're end the end of our loop. Bingo.
[10:35] end the end of our loop. Bingo.
[10:35] end the end of our loop. Bingo. Now,
[10:36] Now,
[10:36] Now, then we take the answer, and this is an
[10:38] then we take the answer, and this is an
[10:38] then we take the answer, and this is an opportunity for you to
[10:39] opportunity for you to
[10:39] opportunity for you to have a human in the loop potentially.
[10:43] have a human in the loop potentially.
[10:43] have a human in the loop potentially. You check the confidence. If it looks
[10:45] You check the confidence. If it looks
[10:45] You check the confidence. If it looks good, you keep it. If you don't, then
[10:47] good, you keep it. If you don't, then
[10:47] good, you keep it. If you don't, then you escalate to a human.
[10:49] you escalate to a human.
[10:49] you escalate to a human. So, now there's another reason why you
[10:52] So, now there's another reason why you
[10:52] So, now there's another reason why you need to make sure you check your stop
[10:54] need to make sure you check your stop
[10:54] need to make sure you check your stop reason. One of the stop reasons may be
[10:57] reason. One of the stop reasons may be
[10:57] reason. One of the stop reasons may be you have run out of tokens, and this
[11:00] you have run out of tokens, and this
[11:00] you have run out of tokens, and this response is based on partial when the
[11:04] response is based on partial when the
[11:04] response is based on partial when the LLM had to stop.
[11:06] LLM had to stop.
[11:06] LLM had to stop. And it's going to give you a response,
[11:08] And it's going to give you a response,
[11:08] And it's going to give you a response, but if you have run out of tokens, then
[11:10] but if you have run out of tokens, then
[11:10] but if you have run out of tokens, then you need to take action.
[11:12] you need to take action.
[11:12] you need to take action. Okay.
[11:13] Okay.
[11:13] Okay. Um
[11:15] Um
[11:15] Um Next scenario.
[11:17] Next scenario.
[11:17] Next scenario. Uh code generation with Claude. So,
[11:19] Uh code generation with Claude. So,
[11:19] Uh code generation with Claude. So, Claude code has this has this concept of
[11:22] Claude code has this has this concept of
[11:22] Claude code has this has this concept of the Claude MD file, a markdown file,
[11:24] the Claude MD file, a markdown file,
[11:24] the Claude MD file, a markdown file, where you put all the things you wanted
[11:26] where you put all the things you wanted
[11:26] where you put all the things you wanted to know.
[11:27] to know.
[11:27] to know. What Anthropic recommends is you have
[11:31] What Anthropic recommends is you have
[11:31] What Anthropic recommends is you have three levels of Claude.
[11:34] three levels of Claude.
[11:34] three levels of Claude. One
[11:36] One
[11:36] One that you have at the top level of your
[11:37] that you have at the top level of your
[11:37] that you have at the top level of your project,
[11:39] project,
[11:39] project, the other that you have in inside your
[11:41] the other that you have in inside your
[11:41] the other that you have in inside your sort of the project folder, and then
[11:45] sort of the project folder, and then
[11:45] sort of the project folder, and then within directories you can also specify.
[11:48] within directories you can also specify.
[11:48] within directories you can also specify. So, the idea is to have a hierarchical
[11:50] So, the idea is to have a hierarchical
[11:50] So, the idea is to have a hierarchical set of rules that that can then control
[11:55] set of rules that that can then control
[11:55] set of rules that that can then control how the system is going to respond.
[11:58] how the system is going to respond.
[11:58] how the system is going to respond. Okay.
[12:00] Okay.
[12:00] Okay. Moving right along,
[12:02] Moving right along,
[12:02] Moving right along, uh we have a multi-agent research
[12:04] uh we have a multi-agent research
[12:04] uh we have a multi-agent research system. So, here we're going to have uh
[12:08] system. So, here we're going to have uh
[12:08] system. So, here we're going to have uh the problem is
[12:10] the problem is
[12:10] the problem is how do I how do I get my agents to to go
[12:12] how do I how do I get my agents to to go
[12:12] how do I how do I get my agents to to go off and do stuff and bring the answers
[12:14] off and do stuff and bring the answers
[12:14] off and do stuff and bring the answers back in a reasonable way? The
[12:16] back in a reasonable way? The
[12:16] back in a reasonable way? The anti-pattern
[12:18] anti-pattern
[12:18] anti-pattern you
[12:19] you
[12:19] you have one agent and you load it up with
[12:21] have one agent and you load it up with
[12:21] have one agent and you load it up with tools, all right? So, I like to think
[12:23] tools, all right? So, I like to think
[12:23] tools, all right? So, I like to think about you
[12:24] about you
[12:24] about you you know, you hire somebody to come to
[12:25] you know, you hire somebody to come to
[12:25] you know, you hire somebody to come to your house, you hire a carpenter to come
[12:27] your house, you hire a carpenter to come
[12:27] your house, you hire a carpenter to come to the house, and the guy shows up with
[12:30] to the house, and the guy shows up with
[12:30] to the house, and the guy shows up with uh
[12:31] uh
[12:31] uh plumbing tools, carpenter tools,
[12:33] plumbing tools, carpenter tools,
[12:33] plumbing tools, carpenter tools, electrical tools. He says, "I can do
[12:35] electrical tools. He says, "I can do
[12:35] electrical tools. He says, "I can do anything." Well, maybe you don't want
[12:36] anything." Well, maybe you don't want
[12:36] anything." Well, maybe you don't want this guy, maybe you want a a
[12:38] this guy, maybe you want a a
[12:38] this guy, maybe you want a a professional carpenter. So, that's the
[12:40] professional carpenter. So, that's the
[12:40] professional carpenter. So, that's the kind of idea. And this kind of back
[12:42] kind of idea. And this kind of back
[12:42] kind of idea. And this kind of back takes us back to some of the the
[12:44] takes us back to some of the the
[12:44] takes us back to some of the the functional programming
[12:46] functional programming
[12:46] functional programming uh
[12:47] uh
[12:47] uh ideas that functions should be do one
[12:50] ideas that functions should be do one
[12:50] ideas that functions should be do one thing. And if you can get your agents to
[12:53] thing. And if you can get your agents to
[12:53] thing. And if you can get your agents to do one thing,
[12:55] do one thing,
[12:55] do one thing, you with maybe one or two tools
[12:58] you with maybe one or two tools
[12:58] you with maybe one or two tools available to it, then that's going to be
[13:00] available to it, then that's going to be
[13:01] available to it, then that's going to be a win, and that's going to help you with
[13:02] a win, and that's going to help you with
[13:02] a win, and that's going to help you with this exam. So, specialize,
[13:05] this exam. So, specialize,
[13:05] this exam. So, specialize, don't overload.
[13:07] don't overload.
[13:07] don't overload. The other part of this is
[13:09] The other part of this is
[13:09] The other part of this is don't let your agents
[13:11] don't let your agents
[13:11] don't let your agents context spill over into the main context
[13:16] context spill over into the main context
[13:16] context spill over into the main context because context means tokens, tokens
[13:19] because context means tokens, tokens
[13:19] because context means tokens, tokens mean money,
[13:21] mean money,
[13:21] mean money, and the more context you have, the more
[13:23] and the more context you have, the more
[13:23] and the more context you have, the more confused the LLM is going to be in
[13:26] confused the LLM is going to be in
[13:26] confused the LLM is going to be in giving you an answer. So, even though
[13:28] giving you an answer. So, even though
[13:28] giving you an answer. So, even though oh, a million token context window, I
[13:31] oh, a million token context window, I
[13:31] oh, a million token context window, I can put everything in there. No, no,
[13:32] can put everything in there. No, no,
[13:32] can put everything in there. No, no, don't put everything in there.
[13:34] don't put everything in there.
[13:34] don't put everything in there. Limit what's going to go in there
[13:35] Limit what's going to go in there
[13:35] Limit what's going to go in there because then you're going to get
[13:37] because then you're going to get
[13:37] because then you're going to get a much more accurate system.
[13:44] So, here's a
[13:44] So, here's a Here's an example of a specialized sub
[13:47] Here's an example of a specialized sub
[13:47] Here's an example of a specialized sub agents.
[13:48] agents.
[13:48] agents. You're giving it
[13:50] You're giving it
[13:50] You're giving it So, this would be the critic. So, let's
[13:52] So, this would be the critic. So, let's
[13:52] So, this would be the critic. So, let's say you've run some stuff. Now, you want
[13:54] say you've run some stuff. Now, you want
[13:54] say you've run some stuff. Now, you want to get an agent to look at what's
[13:57] to get an agent to look at what's
[13:57] to get an agent to look at what's happened. What you want to do is just
[13:59] happened. What you want to do is just
[13:59] happened. What you want to do is just give it what it needs to solve that
[14:02] give it what it needs to solve that
[14:02] give it what it needs to solve that critic problem. I'm only giving it here
[14:05] critic problem. I'm only giving it here
[14:05] critic problem. I'm only giving it here the
[14:07] the
[14:07] the we're passing it
[14:08] we're passing it
[14:08] we're passing it the claim and the evidence. So, this is
[14:11] the claim and the evidence. So, this is
[14:11] the claim and the evidence. So, this is your claim is sort of how we're going to
[14:13] your claim is sort of how we're going to
[14:13] your claim is sort of how we're going to solve the problem. Here's Here's the
[14:14] solve the problem. Here's Here's the
[14:14] solve the problem. Here's Here's the evidence, but we're not giving it the
[14:18] evidence, but we're not giving it the
[14:18] evidence, but we're not giving it the the thought processes that went in to
[14:22] the thought processes that went in to
[14:22] the thought processes that went in to creating this claim. Why?
[14:25] creating this claim. Why?
[14:25] creating this claim. Why? When you
[14:27] When you
[14:27] When you When you get a bunch of agents together
[14:29] When you get a bunch of agents together
[14:29] When you get a bunch of agents together collaborating and talking to each other,
[14:32] collaborating and talking to each other,
[14:32] collaborating and talking to each other, there's a tendency to have group think.
[14:35] there's a tendency to have group think.
[14:35] there's a tendency to have group think. And
[14:36] And
[14:36] And all the agents seem to kind of devolve
[14:39] all the agents seem to kind of devolve
[14:39] all the agents seem to kind of devolve into one idea. I mean, it's it's like,
[14:42] into one idea. I mean, it's it's like,
[14:42] into one idea. I mean, it's it's like, you know, you're in a group, you know,
[14:43] you know, you're in a group, you know,
[14:43] you know, you're in a group, you know, you're at a party, and everybody wants
[14:46] you're at a party, and everybody wants
[14:46] you're at a party, and everybody wants pizza except you, but then people talk
[14:49] pizza except you, but then people talk
[14:49] pizza except you, but then people talk you into
[14:50] you into
[14:50] you into you you know, you don't want to be uh
[14:53] you you know, you don't want to be uh
[14:53] you you know, you don't want to be uh you don't want to spoil the party, so
[14:54] you don't want to spoil the party, so
[14:54] you don't want to spoil the party, so you'll go along. And it seems that
[14:55] you'll go along. And it seems that
[14:55] you'll go along. And it seems that agents kind of work in the same way.
[14:57] agents kind of work in the same way.
[14:58] agents kind of work in the same way. So, you're going to return
[15:00] So, you're going to return
[15:00] So, you're going to return Basically, you're going to give each
[15:02] Basically, you're going to give each
[15:02] Basically, you're going to give each agent only a slice. I didn't think about
[15:05] agent only a slice. I didn't think about
[15:05] agent only a slice. I didn't think about the pizza analogy, but yes. Every agent
[15:08] the pizza analogy, but yes. Every agent
[15:08] the pizza analogy, but yes. Every agent gets its own slice, and and it it should
[15:11] gets its own slice, and and it it should
[15:11] gets its own slice, and and it it should come through.
[15:12] come through.
[15:12] come through. Okay.
[15:19] Fourth scenario,
[15:19] Fourth scenario, developer productivity. So, the
[15:22] developer productivity. So, the
[15:22] developer productivity. So, the anti-pattern.
[15:25] anti-pattern.
[15:25] anti-pattern. Let every subtask dump its full output
[15:27] Let every subtask dump its full output
[15:27] Let every subtask dump its full output into the primary thread, crowding out
[15:29] into the primary thread, crowding out
[15:29] into the primary thread, crowding out the context. Again, this is what we're I
[15:31] the context. Again, this is what we're I
[15:31] the context. Again, this is what we're I was just talking about. This is bad. Let
[15:34] was just talking about. This is bad. Let
[15:34] was just talking about. This is bad. Let the context grow unbounded. Bad, right?
[15:38] the context grow unbounded. Bad, right?
[15:38] the context grow unbounded. Bad, right? For the reasons we just talked about.
[15:40] For the reasons we just talked about.
[15:40] For the reasons we just talked about. You want to isolate your subtask output,
[15:43] You want to isolate your subtask output,
[15:43] You want to isolate your subtask output, and you want to compact
[15:46] and you want to compact
[15:46] and you want to compact long sessions. I'm going to take a
[15:48] long sessions. I'm going to take a
[15:48] long sessions. I'm going to take a second to talk about that. So, here's
[15:51] second to talk about that. So, here's
[15:51] second to talk about that. So, here's here's a
[15:52] here's a
[15:52] here's a an example of a pattern.
[15:54] an example of a pattern.
[15:54] an example of a pattern. Uh
[15:55] Uh
[15:55] Uh you want to have your agent
[15:59] you want to have your agent
[15:59] you want to have your agent uh
[16:00] uh
[16:00] uh look at the logs and create a summary
[16:04] look at the logs and create a summary
[16:04] look at the logs and create a summary of where the problems are in the log.
[16:06] of where the problems are in the log.
[16:06] of where the problems are in the log. So, here's your task, scan all the logs
[16:09] So, here's your task, scan all the logs
[16:09] So, here's your task, scan all the logs for error.
[16:10] for error.
[16:10] for error. Context fork. So, you're forking the
[16:13] Context fork. So, you're forking the
[16:13] Context fork. So, you're forking the agent into a like a separate thread
[16:16] agent into a like a separate thread
[16:16] agent into a like a separate thread where
[16:17] where
[16:17] where whatever the agent does and thinks and
[16:20] whatever the agent does and thinks and
[16:20] whatever the agent does and thinks and adds tokens to does not come back and
[16:23] adds tokens to does not come back and
[16:23] adds tokens to does not come back and pollute the main
[16:25] pollute the main
[16:25] pollute the main uh
[16:26] uh
[16:26] uh the main context.
[16:28] the main context.
[16:28] the main context. Now,
[16:30] Now,
[16:30] Now, you see here what happens, then you take
[16:32] you see here what happens, then you take
[16:32] you see here what happens, then you take this
[16:33] this
[16:33] this summation, and then you add that
[16:35] summation, and then you add that
[16:35] summation, and then you add that summation without all the other stuff
[16:38] summation without all the other stuff
[16:38] summation without all the other stuff into the overriding context. Now, this
[16:42] into the overriding context. Now, this
[16:42] into the overriding context. Now, this last little block is kind of
[16:43] last little block is kind of
[16:43] last little block is kind of interesting, I think. Because
[16:46] interesting, I think. Because
[16:46] interesting, I think. Because you can check your token count,
[16:49] you can check your token count,
[16:49] you can check your token count, and you can determine how big the token
[16:51] and you can determine how big the token
[16:51] and you can determine how big the token count is.
[16:53] count is.
[16:53] count is. And
[16:55] And
[16:55] And if you can set some limit and you know,
[16:57] if you can set some limit and you know,
[16:57] if you can set some limit and you know, if if you have more than 150,000 tokens,
[16:59] if if you have more than 150,000 tokens,
[16:59] if if you have more than 150,000 tokens, then what you want to do is you can run
[17:01] then what you want to do is you can run
[17:01] then what you want to do is you can run a compact. So, Anthropic and Claude have
[17:04] a compact. So, Anthropic and Claude have
[17:04] a compact. So, Anthropic and Claude have these compaction algorithms
[17:08] these compaction algorithms
[17:08] these compaction algorithms that take this giant context and and
[17:10] that take this giant context and and
[17:10] that take this giant context and and compact it in some way, shape, or form.
[17:12] compact it in some way, shape, or form.
[17:12] compact it in some way, shape, or form. Not quite sure how the implementation is
[17:15] Not quite sure how the implementation is
[17:15] Not quite sure how the implementation is of that, but there is compaction. Now, a
[17:18] of that, but there is compaction. Now, a
[17:18] of that, but there is compaction. Now, a little side effect a little side channel
[17:21] little side effect a little side channel
[17:21] little side effect a little side channel I've been walking around when you walk
[17:23] I've been walking around when you walk
[17:23] I've been walking around when you walk outside, you see see these guys handing
[17:24] outside, you see see these guys handing
[17:24] outside, you see see these guys handing out these books.
[17:26] out these books.
[17:26] out these books. Okay? Anybody see these guys handing out
[17:28] Okay? Anybody see these guys handing out
[17:28] Okay? Anybody see these guys handing out these but take them. This is this is
[17:30] these but take them. This is this is
[17:30] these but take them. This is this is actually a pretty good little book. In
[17:32] actually a pretty good little book. In
[17:32] actually a pretty good little book. In fact, I was looking at it last night and
[17:35] fact, I was looking at it last night and
[17:35] fact, I was looking at it last night and one of the things it had in it was this
[17:37] one of the things it had in it was this
[17:37] one of the things it had in it was this is by this guy Sam
[17:39] is by this guy Sam
[17:39] is by this guy Sam Sam Bagwell. I have no connection I
[17:41] Sam Bagwell. I have no connection I
[17:41] Sam Bagwell. I have no connection I didn't even know Sam, but it there's a
[17:44] didn't even know Sam, but it there's a
[17:44] didn't even know Sam, but it there's a online page 32.
[17:46] online page 32.
[17:46] online page 32. It says
[17:47] It says
[17:47] It says uh his company provides custom logic for
[17:50] uh his company provides custom logic for
[17:50] uh his company provides custom logic for compression of context. So, he's got an
[17:54] compression of context. So, he's got an
[17:54] compression of context. So, he's got an and you can write your own. He's got a
[17:56] and you can write your own. He's got a
[17:56] and you can write your own. He's got a he's got he you can extend his base
[17:57] he's got he you can extend his base
[17:57] he's got he you can extend his base class and have your own
[18:00] class and have your own
[18:00] class and have your own compression of your data, whatever you
[18:01] compression of your data, whatever you
[18:01] compression of your data, whatever you think is important. So, I think that's
[18:03] think is important. So, I think that's
[18:03] think is important. So, I think that's kind of an interesting spin on this
[18:06] kind of an interesting spin on this
[18:06] kind of an interesting spin on this whole thing.
[18:07] whole thing.
[18:07] whole thing. Okay.
[18:09] Okay.
[18:09] Okay. Cloud code for
[18:12] Cloud code for
[18:12] Cloud code for uh uh continuous integration
[18:18] uh anti-pattern
[18:18] uh anti-pattern Always have interactive modes in a
[18:19] Always have interactive modes in a
[18:19] Always have interactive modes in a pipeline. Well, no no no cuz interactive
[18:22] pipeline. Well, no no no cuz interactive
[18:22] pipeline. Well, no no no cuz interactive modes mean uh
[18:25] modes mean uh
[18:25] modes mean uh Cloud will stop and ask you, "You want
[18:27] Cloud will stop and ask you, "You want
[18:27] Cloud will stop and ask you, "You want to do this? You want to do that? Can I
[18:28] to do this? You want to do that? Can I
[18:28] to do this? You want to do that? Can I have permission for that?" So, there are
[18:29] have permission for that?" So, there are
[18:29] have permission for that?" So, there are ways to set it up so that it'll just run
[18:32] ways to set it up so that it'll just run
[18:32] ways to set it up so that it'll just run straight through, okay?
[18:34] straight through, okay?
[18:34] straight through, okay? The other
[18:36] The other
[18:36] The other uh
[18:37] uh
[18:37] uh the other tip that I'll give you here
[18:41] the other tip that I'll give you here
[18:41] the other tip that I'll give you here is there's something called
[18:43] is there's something called
[18:43] is there's something called the uh
[18:45] the uh
[18:45] the uh the batch. So, you can take your
[18:47] the batch. So, you can take your
[18:47] the batch. So, you can take your prompts, you can take your work, and you
[18:50] prompts, you can take your work, and you
[18:50] prompts, you can take your work, and you can put them in a batch and for 50%
[18:54] can put them in a batch and for 50%
[18:54] can put them in a batch and for 50% fewer token cost you will get the result
[18:57] fewer token cost you will get the result
[18:57] fewer token cost you will get the result they promise in at at least 24 hours.
[19:00] they promise in at at least 24 hours.
[19:00] they promise in at at least 24 hours. So, if you're going to go take a nap,
[19:01] So, if you're going to go take a nap,
[19:01] So, if you're going to go take a nap, you're going to go on vacation, you're
[19:03] you're going to go on vacation, you're
[19:03] you're going to go on vacation, you're going to go out, take a a day off, run
[19:05] going to go out, take a a day off, run
[19:05] going to go out, take a a day off, run your stuff in batch mode, and you're
[19:07] your stuff in batch mode, and you're
[19:07] your stuff in batch mode, and you're going to have a a
[19:09] going to have a a
[19:09] going to have a a less to pay.
[19:15] Where am I here?
[19:15] Where am I here? All right, I've only got a few few
[19:17] All right, I've only got a few few
[19:17] All right, I've only got a few few minutes left, few seconds left, but I
[19:20] minutes left, few seconds left, but I
[19:20] minutes left, few seconds left, but I want to conclude with this.
[19:22] want to conclude with this.
[19:22] want to conclude with this. Remember, nothing is a mistake. There's
[19:25] Remember, nothing is a mistake. There's
[19:25] Remember, nothing is a mistake. There's no win, there's no fail, there's no
[19:26] no win, there's no fail, there's no
[19:26] no win, there's no fail, there's no exam,
[19:28] exam,
[19:28] exam, only make. You do it and you make it and
[19:31] only make. You do it and you make it and
[19:31] only make. You do it and you make it and you're going to succeed. If you want to
[19:33] you're going to succeed. If you want to
[19:33] you're going to succeed. If you want to reach out to me, reach out to me uh coil
[19:35] reach out to me, reach out to me uh coil
[19:35] reach out to me, reach out to me uh coil at Berkeley, look at my websites. I got
[19:38] at Berkeley, look at my websites. I got
[19:38] at Berkeley, look at my websites. I got a website co-supreme AI. I'm a big jazz
[19:41] a website co-supreme AI. I'm a big jazz
[19:41] a website co-supreme AI. I'm a big jazz fan and I named this website after John
[19:42] fan and I named this website after John
[19:43] fan and I named this website after John Coltrane, Love Supreme, if you know that
[19:44] Coltrane, Love Supreme, if you know that
[19:44] Coltrane, Love Supreme, if you know that song, great. Anyway, that's my story and
[19:47] song, great. Anyway, that's my story and
[19:47] song, great. Anyway, that's my story and I'm sticking to it and I'm about to zero
[19:49] I'm sticking to it and I'm about to zero
[19:49] I'm sticking to it and I'm about to zero time. Okay,
[19:50] time. Okay,
[19:50] time. Okay, &gt;&gt; [applause]
[19:50] &gt;&gt; [applause]
[19:51] &gt;&gt; [applause] &gt;&gt; thank you.
