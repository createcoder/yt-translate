# Persona Engineering: A Field Guide to AI Synthetic Personas — Ishan Anand, InsightSciences.ai

- **Video:** https://www.youtube.com/watch?v=YnNF55QV0zs
- **Generated:** 2026-08-31 21:15 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The presentation’s core message is that **LLM-based synthetic personas are useful for exploratory research, scenario generation, and AI-assistant testing—but are not reliable substitutes for real customer data, statistically valid surveys, or behavioural models**.

The speaker identifies several recurring weaknesses:

- **Missing context causes confounding:** If a scenario does not explicitly hold factors constant, the model may infer unstated conditions. For example, price may be interpreted as a proxy for product quality, urgency, competitor pricing, or service level.
- **Results can be prompt-sensitive:** Reordering options, changing wording, or altering scenario detail can materially change outputs.
- **More persona detail can worsen results:** Rich demographic or contextual descriptions may amplify model stereotypes or biases rather than improve realism.
- **LLMs are better aligned to language than behaviour:** They may simulate attitudes, stated preferences, and plausible rationales more effectively than actual purchasing, churn, payment, or service behaviour.
- **Repeated synthetic runs do not create new evidence:** Multiple generations estimate model variability; they do not add independent human observations or justify survey-style statistical significance.
- **Validation must be empirical and distributional:** Assess whether synthetic outputs align with held-out human data by segment and full response distribution—not merely whether average scores appear correct.

For Superior Propane, synthetic personas are most defensible as a **governed hypothesis-generation and evaluation-support capability**. They can accelerate customer-communication design, contact-centre scenario creation, self-service journey testing, and AI-agent evaluation.

They should **not** independently drive pricing, retention offers, credit/payment decisions, eligibility, customer prioritization, demand forecasting, or automated customer treatment. Those uses require governed first-party data, conventional predictive or causal models, controlled experimentation where appropriate, and Legal/Privacy/business oversight.

---

# Technical details

## 1. Synthetic personas are probabilistic model outputs, not independent respondents

### Speaker claim

The speaker argues that rerunning the same synthetic persona does not generate additional independent evidence. Repeated outputs may help estimate how the model behaves under a fixed prompt and configuration, but they do not create new human observations.

The speaker uses an analogy:

- Additional independent weather gauges can improve measurement of current rainfall.
- Re-running one weather forecast does not independently improve confidence in tomorrow’s weather.

### Implication

Synthetic outputs must not be:

- Added to a survey dataset as though they were respondents.
- Used to increase reported sample size.
- Used to calculate customer-population confidence intervals or statistical significance.
- Presented as representative customer research.

Repeated sampling is still useful for measuring:

- Output variance.
- Preference distribution under a scenario.
- Sensitivity to temperature/seeds, where supported.
- Stability across prompt variations.
- Model-version drift.

But this is **model uncertainty analysis**, not human research augmentation.

---

## 2. Incomplete scenario context creates latent confounding

### Speaker claim

The speaker describes an experiment in which synthetic purchase probability had an inverted U-shaped relationship with price: at some points, increasing price increased simulated purchase likelihood.

The speaker’s explanation is that the model inferred unstated variables associated with price, such as:

- Product expiry or freshness.
- Product quality.
- Competitor pricing.
- Service level.
- Other shopping or decision-context signals.

### Established principle

This is a valid experimental-design issue. An LLM completes a plausible textual scenario from learned correlations. Unless the prompt specifies which variables are fixed, it may treat an intended treatment variable—such as price—as a signal for other attributes.

### Implementation requirement

For every synthetic-persona experiment, explicitly define:

- **Persona profile**
  - Account/customer segment.
  - Household or business context.
  - Service territory.
  - Tenure.
  - Delivery type.
  - Channel preference.
  - Relevant—but approved and non-sensitive—needs or constraints.

- **Decision context**
  - Season and weather conditions.
  - Service availability.
  - Delivery/installation windows.
  - Current supplier relationship.
  - Contract/renewal status.
  - Recent service history.
  - Communication history.

- **Fixed variables**
  - Variables that must remain unchanged across variants.
  - Example: when testing price, explicitly state that delivery window, service level, equipment, payment terms, competitor offer, safety coverage, and product availability are identical.

- **Choice set**
  - Available alternatives.
  - Fees.
  - Discounts.
  - Service conditions.
  - Payment options.
  - Renewal terms.

- **Task definition**
  - Whether the requested output is an opinion, stated intent, ranked preference, or simulated choice.
  - Required structured output schema.

For a price-related scenario, a suitable instruction would explicitly state: *“Do not infer any difference other than price; all service, delivery, product, contract, and competitor conditions are equivalent.”*

---

## 3. Prompt sensitivity and order bias require durability testing

### Speaker claim

The speaker cites an example where changing answer-option order materially changed model results. Averaging across both orderings reportedly reduced the substantive apparent conclusion to approximately random 50/50 output.

The speaker’s point is that synthetic-persona conclusions can be artefacts of prompt structure rather than stable simulated preferences.

### Required robustness tests

Any scenario that informs product or communication decisions should be tested across controlled variants:

- Randomized answer ordering.
- Reworded but semantically equivalent instructions.
- Different output formats:
  - Binary choice.
  - Multiple choice.
  - Ranking.
  - Rating scale.
  - Free-text response followed by structured selection.
- Reordered context details.
- Explicit “all else equal” conditions.
- Counterfactual challenges:
  - “What would change your decision?”
  - “Assume the competing offer has the same delivery window.”
  - “Do not infer differences beyond those stated.”
- Repeated samples with fixed and varied inference settings.
- Multiple approved foundation models for material decisions.

### Suggested experiment harness

A repeatable evaluation harness should:

1. Store canonical scenarios, persona definitions, prompt templates, and variants in source control.
2. Generate prompt permutations programmatically.
3. Run repeated inferences by persona, scenario, and variant.
4. Capture:
   - Model and deployment version.
   - System prompt and user prompt version.
   - Temperature, top-p, seed, and other inference settings where available.
   - Source-data version.
   - Timestamp.
   - Raw output.
   - Parsed structured response.
   - Detected assumptions.
   - Confidence or rationale, if collected.
5. Calculate:
   - Variance by wording.
   - Variance by answer position.
   - Agreement across models.
   - Output entropy and distribution shape.
   - Sensitivity to omitted context.
   - Segment-level stability.
6. Flag unstable scenarios as unsuitable for decision support.

An Azure-oriented implementation could invoke approved **Azure AI Foundry model endpoints**, persist experiment artefacts in **ADLS Gen2/Delta tables**, and analyze results in **Databricks**. This architecture is a practical implementation recommendation; it was not specified by the speaker.

---

## 4. LLMs may simulate stated attitudes better than observed behaviour

### Speaker claim

The speaker argues that LLMs are trained primarily on human language—“what people say”—rather than direct observations of “what people do.”

Accordingly, they may be more useful for simulating:

- Survey responses.
- Stated beliefs.
- Perceived fairness.
- Language and likely objections.
- Narrative explanations of preferences.

They may be less reliable for predicting:

- Actual purchase behaviour.
- Renewal.
- Churn.
- Attendance.
- Payment behaviour.
- Operational compliance.
- Other real-world actions.

The speaker refers to research comparing LLM and expert predictions of social-science experiments, claiming stronger results on survey/attitude tasks than field/behaviour tasks. The transcript does not identify the research, models, datasets, metrics, or statistical significance; this should be treated as a cautionary claim rather than a validated benchmark.

### Superior Propane implication

Synthetic personas may help answer:

- “What terminology may customers find confusing?”
- “What concerns might a customer raise about auto-pay?”
- “How might a customer perceive the fairness of this message?”
- “What questions should a service agent or chatbot be prepared to answer?”

They should not answer, without real-data validation:

- “What percentage of customers will enroll in auto-pay?”
- “Which price will maximize renewal?”
- “Which customer will churn?”
- “Will this message reduce calls?”
- “Which customers should receive a retention offer?”

### Recommended dual-measure pattern

For behavioural questions, define both an attitudinal hypothesis and an observable behavioural outcome.

| Business objective | Synthetic-persona question | Required real-world validation |
|---|---|---|
| Increase auto-pay adoption | “What makes auto-pay feel trustworthy or risky?” | Enrolment rate by channel and segment |
| Improve renewal communications | “Which message feels clearest and fairest?” | Quote acceptance, renewal, and churn outcomes |
| Reduce contacts | “Would this self-service guidance appear sufficient?” | Deflection, repeat contacts, resolution rate |
| Improve billing explanation | “Which wording is easiest to understand?” | Billing-related calls, complaints, completion rates |
| Improve service notifications | “What questions or concerns does this notice trigger?” | Customer feedback, call reasons, digital engagement |

CRM, transaction, contact-centre, web analytics, and controlled experiment results remain the authoritative sources for behavioural prediction.

---

## 5. More detailed personas may amplify bias

### Speaker claim

The speaker describes research comparing several methods for constructing synthetic voting personas. In the cited results, adding more persona detail reportedly moved model outputs further from actual human behaviour.

The speaker’s proposed explanation is that detailed attributes can amplify the model’s existing biases and learned stereotypes.

### Implication

A longer persona prompt should not be assumed to be better. Plausible, richly detailed narratives can create false confidence while reducing predictive alignment.

This is particularly important for attributes such as:

- Rurality or geography.
- Income proxies.
- Age.
- Language.
- Household composition.
- Digital confidence.
- Commercial versus residential account status.
- Service history.

### Control approach

Use incremental testing:

1. Start with the minimum persona information required for the use case.
2. Add one field or attribute at a time.
3. Evaluate whether that attribute improves or degrades performance on an independent holdout dataset.
4. Prohibit attributes that introduce unacceptable bias, disparate performance, or unsupported inference.

Do not use protected or sensitive attributes, or proxies for them, unless there is a documented legal basis, clear business necessity, and Privacy/Legal approval.

---

## 6. Fine-tuning can align distributions but needs strict controls

### Speaker claim

The speaker references a paper called **“Subpop”**—the exact paper title and spelling should be verified. The described workflow is:

1. Provide demographic or segment information and a survey question.
2. Generate responses with a base LLM.
3. Compare the generated response distribution with known human survey distributions.
4. Fine-tune the model to improve alignment between synthetic and observed distributions.

The speaker says this improved results for both population groups included in tuning and unseen groups.

### Important distinction

This is **population-level distribution matching**, not a conventional model for individual-level behavioural prediction.

Fine-tuning may improve:

- Response-format compliance.
- Calibrated survey-style responses.
- Consistent classification.
- Controlled response patterns.

It does not prove that the model has gained reliable, proprietary knowledge about Superior Propane customers.

### Enterprise decision sequence

Before considering fine-tuning, evaluate in this order:

1. Structured prompting and constrained outputs.
2. Few-shot examples.
3. Retrieval-augmented generation for governed, changing company facts.
4. Fine-tuning only when:
   - The task is stable and repeatable.
   - Adequate governed labels exist.
   - Prompt/RAG approaches do not meet acceptance thresholds.
   - Privacy, bias, and drift risks are manageable.

For Superior Propane, RAG is generally more suitable than fine-tuning for changing operational knowledge, including policies, safety content, equipment information, service procedures, and account-service guidance.

Potential fine-tuning candidates, subject to validation, include:

- Contact-centre intent classification.
- Structured document extraction.
- Disposition-code mapping.
- Controlled drafting in approved formats.
- Narrow task-specific classification workflows.

### Fine-tuning validation requirements

- Time-based holdouts.
- Segment-based holdouts.
- Regional and service-type holdouts where applicable.
- Leakage checks.
- Performance comparison against non-tuned baselines.
- Calibration and distributional evaluation.
- Privacy/memorization testing.
- Safety and policy-compliance regression testing.

---

## 7. Text-first elicitation may be preferable to direct numeric prompts

### Speaker claim

The speaker describes a technique where the model produces a natural-language reaction rather than selecting a direct numeric rating, such as a 1–5 likelihood-to-purchase score.

Example free-text response:

> “I’m somewhat interested. If it works well and isn’t too expensive, I might give it a try.”

The process then:

1. Uses human-authored representative text anchors for each rating category.
2. Embeds both the generated response and rating-anchor texts.
3. Compares semantic similarity.
4. Converts similarity into a probability distribution across rating categories.

### Conceptual architecture

```text
Persona + controlled scenario
            |
            v
LLM generates free-text response
            |
            v
Embedding model creates response vector
            |
            +--> Compare to human-authored rating-anchor vectors
                           |
                           v
            Similarity-weighted rating distribution
                           |
                           v
Aggregate by persona, segment, scenario, and experiment
```

### Why it may help

The speaker’s reasoning is that LLMs are trained extensively on natural language, while direct survey-scale completion may be a less natural task. Free-text responses can preserve conditionality and uncertainty that a forced numeric answer may conceal.

### Limitations

The transcript does not provide:

- The embedding model.
- Similarity metric.
- Calibration method.
- Number or quality of rating anchors.
- Dataset size.
- Statistical results.
- Cross-language performance.

This method requires validation because semantic similarity can misread:

- Negation.
- Conditional language.
- Sarcasm.
- Tone differences.
- Price sensitivity.
- English/French differences.
- Segment-specific phrasing.

Anchor embeddings should be versioned and reused rather than recalculated for every run where possible, reducing cost and improving repeatability.

---

## 8. Evaluate full distributions, not only averages

### Speaker claim

The speaker warns that a model can match an average response while failing to reproduce meaningful variation across people or groups. For example, it may collapse responses toward the middle, masking tail risks or minority viewpoints.

The speaker describes a distribution-similarity measure where 1 represents identical distributions and 0 represents no similarity, but does not specify the metric.

### Evaluation requirements

Track more than average score or headline accuracy:

- Response distribution by approved segment.
- Calibration curves.
- Variance and entropy.
- Tail and minority-category behaviour.
- Differences across time periods.
- Disparate error rates.
- Stability under prompt/model changes.

Potential technical metrics—these are implementation options, not speaker-specified requirements—include:

- Jensen–Shannon divergence.
- Wasserstein distance.
- Kolmogorov–Smirnov statistic.
- Population Stability Index.
- Correlation of segment-level response rates.
- Brier score and expected calibration error for probability outputs.
- Confidence intervals from repeated inference runs.

A useful acceptance criterion is not “the average matched,” but rather: *“The model remained calibrated and acceptably stable across relevant segments, including high-risk and low-frequency outcomes.”*

---

## 9. Establish a ground-truth noise floor

### Speaker claim

The speaker states that human data itself is noisy. A cited example suggests humans repeated surveys/personality tests with roughly 80% self-consistency after two weeks. The speaker’s conclusion is that model performance should be interpreted relative to the consistency of the human benchmark.

The speaker also proposes a fallback where human data is repeatedly split into two subsets and agreement between them is measured to estimate a practical reliability ceiling.

### Practical interpretation

For a Superior Propane pilot:

- Prefer true test–retest data when available.
- If unavailable, Data Science can use split-sample or resampling reliability analysis to estimate how stable the observed dataset is.
- Do not present split-sample agreement as proof of actual behavioural stability; it measures internal sampling consistency, not necessarily real-world test–retest reliability.

This prevents setting unrealistic expectations that an LLM should exceed the consistency inherent in the human data used as ground truth.

---

## 10. Generative agent-based modelling is introduced but not substantiated

### Speaker claim

The speaker briefly introduces generative agent-based modelling, where synthetic personas act as interacting agents in a simulation, creating a “living, queryable asset” grounded in human research data.

### What was not provided

The transcript does not provide:

- A technical architecture.
- Agent orchestration method.
- Interaction protocol.
- Data model.
- Evaluation evidence.
- Predictive performance.
- Security controls.
- Cost model.
- Platform/vendor details.

### Relevance

This topic is potentially relevant for scenario design, but there is insufficient evidence in the transcript to justify roadmap investment beyond research or a tightly bounded proof of concept.

---

# Potential applications for Superior Propane

## Suitable lower-risk applications

### 1. Customer communication and content design

Use synthetic personas to generate hypotheses about potential reactions to:

- Billing, fees, and payment-plan explanations.
- Renewal and price-change notices.
- Auto-pay and paperless-billing communications.
- Delivery scheduling or automatic-delivery messages.
- Service interruption, weather, emergency, or safety notifications.
- Equipment-installation preparation materials.
- Portal, web, IVR, and chatbot wording.

Expected value:

- Identify confusing terms.
- Surface potential fairness concerns.
- Generate likely customer questions.
- Suggest segment-specific language alternatives.
- Produce candidate survey/interview questions.

Required caveat: outputs indicate possible concerns or hypotheses, not predicted conversion, comprehension, satisfaction, or call reduction.

---

### 2. Contact-centre and field-service scenario generation

Synthetic personas can support internal training and quality assurance scenarios, for example:

- A customer disputing a bill.
- A customer concerned about delivery timing.
- A commercial account with an urgent service issue.
- A new customer comparing service options.
- A customer with low digital confidence trying to use self-service.
- A customer asking safety or equipment-maintenance questions.

Appropriate use:

- Agent training-content ideation.
- QA test cases.
- IVR/chatbot scenario coverage.
- Knowledge-article gap identification.
- Escalation-path testing.

This should not replace customer research, agent SME review, or operational validation.

---

### 3. Digital product discovery and self-service journey testing

Potential questions include:

- What information might a customer need before booking service?
- Where might customers misunderstand a quote or renewal flow?
- Which portal steps could create friction for will-call versus automatic-delivery customers?
- What questions could arise following a policy or digital-workflow change?
- Which journey failures are absent from the current contact taxonomy?

Use personas to accelerate backlog refinement and hypothesis formation, then validate with:

- Web and mobile analytics.
- Funnel-completion data.
- Contact-centre call reasons.
- Customer feedback.
- Usability research.
- A/B tests where feasible.

---

### 4. Evaluation of Azure AI Foundry assistants

This is likely the most practical technical application.

Synthetic personas can generate diverse, repeatable test prompts for:

- Internal policy and knowledge assistants.
- Customer-service chatbots.
- Contact-centre copilots.
- Technician support assistants.
- Document-processing workflows.

Evaluation dimensions should include:

- Factual accuracy.
- Policy compliance.
- Appropriate escalation.
- Safety and emergency handling.
- Tone and empathy.
- Disclosure of uncertainty.
- Bilingual performance, if English and French are supported.
- Resistance to prompt injection and unsafe requests.
- Error distribution by customer/account/service scenario.

Synthetic test cases should be supplemented with approved, anonymized real interactions and expert-authored gold-standard cases.

---

### 5. Databricks-based evaluation and monitoring layer

Databricks can provide the governed experimentation and analytics layer:

- Versioned evaluation datasets.
- Segment definitions.
- Persona schema management.
- Delta tables for input/output data.
- Experiment metadata and lineage.
- Batch-run orchestration and scoring.
- Distribution-comparison notebooks/jobs.
- Segment-level monitoring dashboards.
- Drift analysis after model, prompt, policy, or source-content changes.

Specific Databricks products were not named in the transcript. Use of Unity Catalog, MLflow, Mosaic AI, or Databricks Model Serving would be an enterprise architecture choice, not a video claim.

---

# Risks and validation questions

## 1. Statistical misuse and false precision

**Risk:** Synthetic generations are presented as independent customer respondents.

Controls:

- Clearly label all reporting as:
  - Observed human/customer data.
  - Synthetic model output.
  - Expert interpretation/hypothesis.
- Prohibit use of synthetic output for:
  - Survey sample expansion.
  - Statistical-significance claims.
  - Market-size estimates.
  - Population-representative research claims.
- Do not let synthetic results override contradictory real customer or transaction data.

**Validation question:** Does the output improve product or research decisions compared with historical analysis, conventional user research, or expert review alone?

---

## 2. Prompt and model instability

**Risk:** Findings are driven by option order, wording, temperature, foundation model, retrieval context, or vendor model updates.

Controls:

- Source-control prompt templates.
- Store model/deployment/version metadata.
- Fix and document benchmark inference settings.
- Run prompt permutations and repeated samples.
- Establish change-management gates when changing:
  - Foundation model.
  - Prompt schema.
  - Persona schema.
  - Retrieval corpus.
  - Scoring method.
  - Fine-tuning dataset.

**Validation question:** At what variation threshold does a scenario become too unstable to use?

---

## 3. Bias, stereotyping, and discriminatory segmentation

**Risk:** The model produces stereotyped customer behaviours based on demographic or proxy attributes.

This risk can increase as persona descriptions become more detailed.

Controls:

- Use only necessary, approved attributes.
- Avoid protected characteristics and sensitive proxies unless approved for a narrowly defined, lawful purpose.
- Test performance and harmful outputs across relevant slices.
- Require review of persona taxonomies and segment labels.
- Do not use synthetic persona output to determine price, eligibility, credit, payment treatment, service priority, or customer access.

**Validation questions:**

- Which persona fields improve measured accuracy on independent holdouts?
- Do any fields increase bias or disparate error rates?
- Are rurality, age, language, geography, or income proxies being used without clear justification?
- Could a synthetic result cause unfair treatment if operationalized?

---

## 4. Ground-truth quality and drift

**Risk:** Synthetic personas reflect stale research, broad internet priors, or non-local customer patterns rather than Superior Propane’s current customer base.

Controls:

- Define the authoritative ground-truth source:
  - Surveys.
  - Interviews.
  - CRM data.
  - Contact-centre interactions.
  - Digital telemetry.
  - Transactions.
  - Controlled experiments.
- Use independent, held-out validation data.
- Evaluate by time period, region, account type, delivery type, and other approved segments.
- Revalidate after major changes in:
  - Prices.
  - Product offerings.
  - Service operations.
  - Weather/seasonality.
  - Policies.
  - Model versions.

**Validation question:** Is the benchmark recent and representative enough to reflect Canadian propane-customer conditions and current operating realities?

---

## 5. Fine-tuning risks

**Risk:** Fine-tuning improves one benchmark but degrades performance elsewhere, leaks private data, or creates misleading confidence about generalization.

Controls:

- Compare prompt-only, text-first, RAG, and fine-tuned approaches.
- Use strict time-based and segment-based holdouts.
- Check for data leakage and overlap.
- Test for memorization and privacy exposure.
- Re-run safety, policy-compliance, and bias evaluations.
- Maintain a rollback option.

**Validation question:** Does fine-tuning materially outperform simpler approaches on independent, business-relevant data—and is that gain worth the operational burden?

---

## 6. Privacy, security, and governance

The presentation does not provide an Azure, Databricks, or vendor security architecture. These controls must be designed independently.

Key requirements:

- Data minimization and purpose limitation.
- Synthetic or tokenized persona identifiers where possible.
- Pseudonymization/de-identification of research, CRM, and transcript data before model use.
- RBAC and least-privilege access.
- Separation of experimental and production data.
- Classification, retention, deletion, and audit controls.
- Logging of prompts/outputs with appropriate handling of potentially sensitive content.
- Verification of model-endpoint data handling, retention, residency, and diagnostics settings.
- Controls for prompt injection and unapproved retrieval sources.
- Human approval for customer-facing content and material use cases.

**Validation questions:**

- Does any customer data leave the approved enterprise and Canadian data boundary?
- Are Azure AI Foundry logs, diagnostics, and model endpoints configured to meet corporate retention and privacy requirements?
- What PII, payment, account, location, or transcript fields are permitted in experiments?
- Who approves persona creation, prompt changes, and use-case expansion?

---

## 7. Cost and operational trade-offs

The transcript provides no cost figures.

Likely cost drivers include:

- Number of personas × scenarios × prompt variants × repeated runs.
- LLM token and inference cost.
- Embedding cost for text-first scoring.
- Data preparation and de-identification.
- Evaluation pipeline compute.
- Human SME, UX Research, Data Science, Privacy, Legal, and Security review.
- Monitoring and revalidation after model or business changes.

Operational trade-off:

- Synthetic personas can reduce time to generate hypotheses and test scenarios.
- Robust validation and governance reduce that speed advantage.
- For high-impact decisions, direct human research or real-world experimentation may remain more defensible and cost-effective.

Cost should be assessed as **cost per validated decision improvement**, not cost per generated response.

---

# Action items

## 1. Establish a clear synthetic-persona policy

Define permitted use as:

- Hypothesis generation.
- Scenario generation.
- Content and communication stress testing.
- AI-assistant evaluation.
- Internal training and QA support.

Explicitly prohibit use as:

- Survey sample augmentation.
- Population-representative research.
- Pricing or offer optimization without empirical validation.
- Credit, eligibility, payment, or service-priority decisions.
- Automated targeting or treatment of customers.
- Replacement for primary research where statistically defensible evidence is required.

---

## 2. Select a bounded, low-risk pilot

Recommended pilot:

**Test a billing/payment self-service communication and associated AI-assistant content.**

Scope:

- Generate likely customer questions, confusion points, and alternative wording.
- Use approved synthetic personas representing broad operational segments only.
- Test an Azure AI Foundry assistant against synthetic and expert-authored scenarios.
- Benchmark against anonymized historical billing/contact themes where permitted.
- Do not use outputs to predict enrolment, payment behaviour, or customer value.

Other acceptable pilots:

- Contact-centre training scenario generation.
- FAQ/knowledge-assistant evaluation.
- Safety-content comprehension risk identification.
- Portal workflow test-case generation.

---

## 3. Build an evaluation framework before scaling

Implement a reusable Databricks/Azure evaluation capability with:

- Versioned persona specifications.
- Approved segment definitions.
- Versioned source data and ground-truth datasets.
- Prompt and scenario templates in source control.
- Model/deployment/inference metadata.
- Synthetic output capture and structured parsing.
- Prompt-variation and repeated-run testing.
- Distributional and calibration metrics.
- Time-based and segment-based holdouts.
- Drift and regression dashboards.
- Clear separation of synthetic and observed data in reporting.

Minimum recorded metadata per run:

```text
persona_version
scenario_version
prompt_version
source_data_version
model_provider
model_name
deployment_version
inference_parameters
retrieval_corpus_version, if applicable
run_timestamp
raw_output
parsed_output
evaluation_result
reviewer/approval status
```

---

## 4. Define acceptance criteria

Before a pilot begins, define:

- Intended decision/use case.
- Ground-truth dataset.
- Relevant segments.
- Required stability across prompt permutations.
- Maximum acceptable bias/disparate-performance thresholds.
- Distributional fidelity targets.
- Human-review requirements.
- Escalation and rollback conditions.
- Conditions under which synthetic output is explicitly non-decision-grade.

A scenario should be rejected or downgraded if conclusions reverse under minor wording/order changes or fail to align with held-out real data.

---

## 5. Evaluate progressively before fine-tuning

Compare:

1. Structured prompt-only outputs.
2. Text-first generation with semantic/embedding-based scoring.
3. RAG using governed internal content for factual enterprise knowledge.
4. Fine-tuning only if simpler approaches fail and adequate labelled data exists.

Require independent validation that any added complexity improves relevant outcomes.

---

## 6. Complete Privacy, Security, Legal, and model-risk review

Before using customer-derived data:

- Validate data classification and permitted purpose.
- Confirm PII minimization, de-identification, and retention design.
- Confirm Azure AI Foundry endpoint, logging, and residency settings.
- Define access controls and audit requirements.
- Review persona attributes for discriminatory or sensitive inference risk.
- Establish accountable owners for:
  - Persona definitions.
  - Prompt changes.
  - Evaluation criteria.
  - Customer-facing content approval.
  - Go/no-go decisions.

---

## 7. Verify cited research and vendor information

The speaker references research and a website stated as **insightsciences.ai**; both should be independently verified.

Before using cited conclusions in a roadmap:

- Confirm the exact “Subpop” paper.
- Review datasets, foundation models, evaluation metrics, and fine-tuning method.
- Determine whether findings generalize beyond political/survey contexts to customer-service and energy-sector use cases.
- Request any vendor technical documentation covering:
  - Persona-generation process.
  - Data sources and privacy model.
  - Hosting and residency.
  - Evaluation evidence.
  - Bias controls.
  - Enterprise integration model.
  - Security and retention practices.
  - Pricing and operational support.

## Full transcript

[00:16] &gt;&gt; Hello, I'm Ishan and welcome to can AI
[00:16] &gt;&gt; Hello, I'm Ishan and welcome to can AI predict people like we predict the
[00:19] predict people like we predict the
[00:19] predict people like we predict the weather. A field guide to the nascent
[00:21] weather. A field guide to the nascent
[00:21] weather. A field guide to the nascent field of synthetic personas.
[00:24] field of synthetic personas.
[00:24] field of synthetic personas. Now, I'm sure most of you in this room
[00:27] Now, I'm sure most of you in this room
[00:27] Now, I'm sure most of you in this room at some point or another have prompted a
[00:30] at some point or another have prompted a
[00:30] at some point or another have prompted a large language model with a role prompt.
[00:32] large language model with a role prompt.
[00:32] large language model with a role prompt. You are a fill in the blank and then the
[00:35] You are a fill in the blank and then the
[00:35] You are a fill in the blank and then the task.
[00:36] task.
[00:37] task. Believe it or not, that core principle
[00:38] Believe it or not, that core principle
[00:39] Believe it or not, that core principle of steering a model's outputs as if it
[00:41] of steering a model's outputs as if it
[00:41] of steering a model's outputs as if it were a particular person or persona
[00:44] were a particular person or persona
[00:44] were a particular person or persona has turned into an entire category that
[00:47] has turned into an entire category that
[00:47] has turned into an entire category that companies are using to test product
[00:49] companies are using to test product
[00:49] companies are using to test product concepts and messaging against synthetic
[00:52] concepts and messaging against synthetic
[00:52] concepts and messaging against synthetic respondents. And it has moved from a
[00:54] respondents. And it has moved from a
[00:54] respondents. And it has moved from a novelty to market momentum, as you can
[00:57] novelty to market momentum, as you can
[00:57] novelty to market momentum, as you can see from both these headlines as well as
[00:59] see from both these headlines as well as
[00:59] see from both these headlines as well as the increase in funding for the last few
[01:01] the increase in funding for the last few
[01:01] the increase in funding for the last few years.
[01:03] years.
[01:03] years. And the running analogy I want to leave
[01:05] And the running analogy I want to leave
[01:05] And the running analogy I want to leave you with is that synthetic personas are
[01:08] you with is that synthetic personas are
[01:08] you with is that synthetic personas are like weather forecasting.
[01:10] like weather forecasting.
[01:10] like weather forecasting. Like weather forecasting, they were
[01:12] Like weather forecasting, they were
[01:12] Like weather forecasting, they were unlocked thanks to an increase in
[01:14] unlocked thanks to an increase in
[01:14] unlocked thanks to an increase in compute and data.
[01:16] compute and data.
[01:16] compute and data. And like weather forecasting, they
[01:18] And like weather forecasting, they
[01:18] And like weather forecasting, they operate within a particular regime and
[01:21] operate within a particular regime and
[01:21] operate within a particular regime and going past that sometimes can go outside
[01:24] going past that sometimes can go outside
[01:24] going past that sometimes can go outside of where they're accurate. So, for
[01:25] of where they're accurate. So, for
[01:25] of where they're accurate. So, for example, you can only predict the
[01:28] example, you can only predict the
[01:28] example, you can only predict the weather a certain number of days in
[01:30] weather a certain number of days in
[01:30] weather a certain number of days in advance. Similarly with synthetic
[01:32] advance. Similarly with synthetic
[01:32] advance. Similarly with synthetic personas, there's only so far you can go
[01:34] personas, there's only so far you can go
[01:34] personas, there's only so far you can go before you'll run into issues. And
[01:36] before you'll run into issues. And
[01:36] before you'll run into issues. And understanding those issues are as
[01:38] understanding those issues are as
[01:38] understanding those issues are as important as understanding their promise
[01:40] important as understanding their promise
[01:40] important as understanding their promise and their potential.
[01:46] So, I'm Ishan Nand. I'm the chief AI
[01:46] So, I'm Ishan Nand. I'm the chief AI officer at Insight Sciences. We
[01:49] officer at Insight Sciences. We
[01:49] officer at Insight Sciences. We construct LLM synthetic personas for
[01:52] construct LLM synthetic personas for
[01:52] construct LLM synthetic personas for market research and market insights
[01:53] market research and market insights
[01:53] market research and market insights teams.
[01:55] teams.
[01:55] teams. And the reason for this talk is that
[01:57] And the reason for this talk is that
[01:57] And the reason for this talk is that most of the coverage in the space is
[01:59] most of the coverage in the space is
[01:59] most of the coverage in the space is very shallow, doesn't go into the
[02:00] very shallow, doesn't go into the
[02:00] very shallow, doesn't go into the technical details. It's either outright
[02:03] technical details. It's either outright
[02:03] technical details. It's either outright hype or outright dismissal. And
[02:07] hype or outright dismissal. And
[02:07] hype or outright dismissal. And it's really hard to separate the noise
[02:10] it's really hard to separate the noise
[02:10] it's really hard to separate the noise from what's real. So what I want to
[02:12] from what's real. So what I want to
[02:12] from what's real. So what I want to cover is that messy middle of the
[02:13] cover is that messy middle of the
[02:13] cover is that messy middle of the technical details. And you don't have to
[02:15] technical details. And you don't have to
[02:15] technical details. And you don't have to take my word for it, even though I'm a
[02:18] take my word for it, even though I'm a
[02:18] take my word for it, even though I'm a vendor in the space, because everything
[02:20] vendor in the space, because everything
[02:20] vendor in the space, because everything I'm going to talk about today is going
[02:22] I'm going to talk about today is going
[02:22] I'm going to talk about today is going to be based on published research. So
[02:24] to be based on published research. So
[02:24] to be based on published research. So we're going to cover why now for
[02:26] we're going to cover why now for
[02:26] we're going to cover why now for synthetic personas, how they fail, some
[02:28] synthetic personas, how they fail, some
[02:29] synthetic personas, how they fail, some techniques to inspire you, and then some
[02:31] techniques to inspire you, and then some
[02:31] techniques to inspire you, and then some metrics to judge whether your synthetic
[02:32] metrics to judge whether your synthetic
[02:33] metrics to judge whether your synthetic persona is accurate or not.
[02:35] persona is accurate or not.
[02:35] persona is accurate or not. Speaking of weather forecasting, another
[02:37] Speaking of weather forecasting, another
[02:37] Speaking of weather forecasting, another parallel is just like in the 1950s and
[02:40] parallel is just like in the 1950s and
[02:40] parallel is just like in the 1950s and '60s, we got computers that promised us,
[02:43] '60s, we got computers that promised us,
[02:43] '60s, we got computers that promised us, correctly, a future of accurate weather
[02:46] correctly, a future of accurate weather
[02:46] correctly, a future of accurate weather forecasts.
[02:48] forecasts.
[02:48] forecasts. We were also promised, believe it or
[02:50] We were also promised, believe it or
[02:50] We were also promised, believe it or not, people forecasts. This company,
[02:52] not, people forecasts. This company,
[02:52] not, people forecasts. This company, Simulmatics, were extensively covered by
[02:55] Simulmatics, were extensively covered by
[02:55] Simulmatics, were extensively covered by Jill Lepore,
[02:57] Jill Lepore,
[02:57] Jill Lepore, promised that they could simulate and
[02:59] promised that they could simulate and
[02:59] promised that they could simulate and predict the electorate using raw
[03:01] predict the electorate using raw
[03:01] predict the electorate using raw statistics and the computational power
[03:03] statistics and the computational power
[03:03] statistics and the computational power at the time. Fortunately, that turned
[03:05] at the time. Fortunately, that turned
[03:05] at the time. Fortunately, that turned out not to be the case. So you should
[03:07] out not to be the case. So you should
[03:07] out not to be the case. So you should approach claims like this with some
[03:09] approach claims like this with some
[03:09] approach claims like this with some humility. But we have something they did
[03:11] humility. But we have something they did
[03:11] humility. But we have something they did not have then. And that unlock is,
[03:14] not have then. And that unlock is,
[03:14] not have then. And that unlock is, again, more computational power, but
[03:16] again, more computational power, but
[03:16] again, more computational power, but also better modeling thanks to LLMs. And
[03:20] also better modeling thanks to LLMs. And
[03:20] also better modeling thanks to LLMs. And LLMs unlock a new kind of simulation.
[03:23] LLMs unlock a new kind of simulation.
[03:23] LLMs unlock a new kind of simulation. For the longest time, to simulate
[03:25] For the longest time, to simulate
[03:25] For the longest time, to simulate something meant to mathematize it in
[03:28] something meant to mathematize it in
[03:28] something meant to mathematize it in formulas or equations. But certain
[03:30] formulas or equations. But certain
[03:30] formulas or equations. But certain things, how we feel, how we act, what
[03:33] things, how we feel, how we act, what
[03:33] things, how we feel, how we act, what choices we make, aren't always
[03:36] choices we make, aren't always
[03:36] choices we make, aren't always succumbing to the equations. What LLMs
[03:39] succumbing to the equations. What LLMs
[03:39] succumbing to the equations. What LLMs offer us is a new medium, a new atomic
[03:42] offer us is a new medium, a new atomic
[03:42] offer us is a new medium, a new atomic unit of language itself that we can
[03:43] unit of language itself that we can
[03:43] unit of language itself that we can model against. Now granted, they are
[03:45] model against. Now granted, they are
[03:45] model against. Now granted, they are based on math under the hood, but it
[03:47] based on math under the hood, but it
[03:47] based on math under the hood, but it gives us this intermediary layer that we
[03:49] gives us this intermediary layer that we
[03:49] gives us this intermediary layer that we can construct and simulate against that
[03:51] can construct and simulate against that
[03:51] can construct and simulate against that we couldn't before.
[03:54] we couldn't before.
[03:54] we couldn't before. And the process can work.
[03:57] And the process can work.
[03:57] And the process can work. I want to share with you one of the most
[03:59] I want to share with you one of the most
[03:59] I want to share with you one of the most well-known demonstrations of this in the
[04:01] well-known demonstrations of this in the
[04:01] well-known demonstrations of this in the field.
[04:02] field.
[04:03] field. What they did is they took about a
[04:04] What they did is they took about a
[04:04] What they did is they took about a thousand humans.
[04:06] thousand humans.
[04:06] thousand humans. They put them through about two and a
[04:08] They put them through about two and a
[04:08] They put them through about two and a half hours of extensive interviews about
[04:11] half hours of extensive interviews about
[04:11] half hours of extensive interviews about their background and their views and
[04:12] their background and their views and
[04:13] their background and their views and their attitudes. And they put those
[04:15] their attitudes. And they put those
[04:15] their attitudes. And they put those people through a battery of personality
[04:17] people through a battery of personality
[04:17] people through a battery of personality tests and surveys.
[04:19] tests and surveys.
[04:19] tests and surveys. Then they took those transcripts and
[04:21] Then they took those transcripts and
[04:21] Then they took those transcripts and they passed it to an AI agent and they
[04:23] they passed it to an AI agent and they
[04:23] they passed it to an AI agent and they had the AI agent take the same set of
[04:26] had the AI agent take the same set of
[04:26] had the AI agent take the same set of surveys and personality tests.
[04:29] surveys and personality tests.
[04:30] surveys and personality tests. What they found was as the agents were
[04:32] What they found was as the agents were
[04:32] What they found was as the agents were basically about 83% aligned and
[04:35] basically about 83% aligned and
[04:35] basically about 83% aligned and predictive to the corresponding humans
[04:37] predictive to the corresponding humans
[04:37] predictive to the corresponding humans they were modeled against.
[04:39] they were modeled against.
[04:39] they were modeled against. Now one caveat is that number is
[04:41] Now one caveat is that number is
[04:41] Now one caveat is that number is normalized against the uncertainty and
[04:43] normalized against the uncertainty and
[04:43] normalized against the uncertainty and noise of the humans themselves. It's a
[04:46] noise of the humans themselves. It's a
[04:46] noise of the humans themselves. It's a theme we're going to come back to at the
[04:47] theme we're going to come back to at the
[04:47] theme we're going to come back to at the end of this talk.
[04:49] end of this talk.
[04:49] end of this talk. But don't get too excited because
[04:51] But don't get too excited because
[04:51] But don't get too excited because synthetic personas are different from
[04:53] synthetic personas are different from
[04:53] synthetic personas are different from regular experiments and they're liable
[04:55] regular experiments and they're liable
[04:55] regular experiments and they're liable to confuse and fool you if you don't
[04:57] to confuse and fool you if you don't
[04:57] to confuse and fool you if you don't know how they fail. So I'm going to
[04:59] know how they fail. So I'm going to
[04:59] know how they fail. So I'm going to cover three important failure modes that
[05:01] cover three important failure modes that
[05:01] cover three important failure modes that you need to know about when dealing with
[05:03] you need to know about when dealing with
[05:03] you need to know about when dealing with synthetic personas.
[05:05] synthetic personas.
[05:05] synthetic personas. To understand the first one,
[05:07] To understand the first one,
[05:07] To understand the first one, I want to consider this prompt these
[05:09] I want to consider this prompt these
[05:09] I want to consider this prompt these researchers gave. It's a very un It's a
[05:11] researchers gave. It's a very un It's a
[05:11] researchers gave. It's a very un It's a very ambiguous and very unsophisticated
[05:14] very ambiguous and very unsophisticated
[05:14] very ambiguous and very unsophisticated prompt. It basically says you're a
[05:16] prompt. It basically says you're a
[05:16] prompt. It basically says you're a customer, I'm going to show you a
[05:17] customer, I'm going to show you a
[05:18] customer, I'm going to show you a product, I'm going to tell you the
[05:19] product, I'm going to tell you the
[05:19] product, I'm going to tell you the category, I'm going to give you its
[05:21] category, I'm going to give you its
[05:21] category, I'm going to give you its price. Those are going to be the
[05:22] price. Those are going to be the
[05:22] price. Those are going to be the variables in the template and then I'm
[05:24] variables in the template and then I'm
[05:24] variables in the template and then I'm going to ask you to say whether you're
[05:25] going to ask you to say whether you're
[05:25] going to ask you to say whether you're going to purchase or not purchase.
[05:27] going to purchase or not purchase.
[05:27] going to purchase or not purchase. Willingness to pay, willingness to
[05:28] Willingness to pay, willingness to
[05:28] Willingness to pay, willingness to purchase is basically the test.
[05:32] purchase is basically the test.
[05:32] purchase is basically the test. What the researchers did is they
[05:33] What the researchers did is they
[05:33] What the researchers did is they recruited a panel of humans and put them
[05:34] recruited a panel of humans and put them
[05:35] recruited a panel of humans and put them through the same test and then they put
[05:36] through the same test and then they put
[05:36] through the same test and then they put the synthetic personas through the same
[05:38] the synthetic personas through the same
[05:38] the synthetic personas through the same test.
[05:39] test.
[05:39] test. What they found is very interesting.
[05:41] What they found is very interesting.
[05:41] What they found is very interesting. So the humans are here in red.
[05:43] So the humans are here in red.
[05:43] So the humans are here in red. They do exactly what you would expect
[05:44] They do exactly what you would expect
[05:44] They do exactly what you would expect from basic economic theory. As the
[05:46] from basic economic theory. As the
[05:46] from basic economic theory. As the purchase price increases, we see that
[05:50] purchase price increases, we see that
[05:50] purchase price increases, we see that the purchase probability goes down,
[05:52] the purchase probability goes down,
[05:52] the purchase probability goes down, slopes downward.
[05:53] slopes downward.
[05:53] slopes downward. But the LLMs did something different.
[05:56] But the LLMs did something different.
[05:56] But the LLMs did something different. They had this inverted U-shaped curve.
[05:58] They had this inverted U-shaped curve.
[05:58] They had this inverted U-shaped curve. And particularly problematic is this
[06:00] And particularly problematic is this
[06:00] And particularly problematic is this area right here, where as the price is
[06:03] area right here, where as the price is
[06:03] area right here, where as the price is increasing, the purchase probability is
[06:05] increasing, the purchase probability is
[06:05] increasing, the purchase probability is going up. That seems really bizarre.
[06:09] going up. That seems really bizarre.
[06:09] going up. That seems really bizarre. Through a series of additional
[06:10] Through a series of additional
[06:10] Through a series of additional experiments, what they discovered was
[06:12] experiments, what they discovered was
[06:12] experiments, what they discovered was that the LLM was using the price as a
[06:15] that the LLM was using the price as a
[06:15] that the LLM was using the price as a proxy for other properties about the
[06:17] proxy for other properties about the
[06:17] proxy for other properties about the product that the humans were considering
[06:19] product that the humans were considering
[06:19] product that the humans were considering were fixed.
[06:20] were fixed.
[06:20] were fixed. Things like the expiration date based on
[06:23] Things like the expiration date based on
[06:23] Things like the expiration date based on the price, what the price of competing
[06:25] the price, what the price of competing
[06:25] the price, what the price of competing products were also as the price changed.
[06:27] products were also as the price changed.
[06:28] products were also as the price changed. And those correlations, those latent
[06:30] And those correlations, those latent
[06:30] And those correlations, those latent confounders that weren't clear and
[06:31] confounders that weren't clear and
[06:32] confounders that weren't clear and immediate, were actually confusing the
[06:34] immediate, were actually confusing the
[06:34] immediate, were actually confusing the result.
[06:36] result.
[06:36] result. And the way to think about this is when
[06:37] And the way to think about this is when
[06:37] And the way to think about this is when an LLM is missing context, it has to
[06:40] an LLM is missing context, it has to
[06:40] an LLM is missing context, it has to potentially infer or invent confounders.
[06:44] potentially infer or invent confounders.
[06:44] potentially infer or invent confounders. Right? When we do a human experiment, if
[06:47] Right? When we do a human experiment, if
[06:47] Right? When we do a human experiment, if I put it like a gold watch on a table, I
[06:48] I put it like a gold watch on a table, I
[06:49] I put it like a gold watch on a table, I ask a human to walk in and estimate the
[06:50] ask a human to walk in and estimate the
[06:50] ask a human to walk in and estimate the price of it, everything about the
[06:52] price of it, everything about the
[06:52] price of it, everything about the environment is fairly fixed. The human
[06:54] environment is fairly fixed. The human
[06:54] environment is fairly fixed. The human and their decisions are the random
[06:56] and their decisions are the random
[06:56] and their decisions are the random variable. In a synthetic experiment, if
[06:58] variable. In a synthetic experiment, if
[06:58] variable. In a synthetic experiment, if you don't set it up properly, other
[07:01] you don't set it up properly, other
[07:01] you don't set it up properly, other parts of it actually become part of the
[07:03] parts of it actually become part of the
[07:03] parts of it actually become part of the random variable itself. I like to say if
[07:05] random variable itself. I like to say if
[07:05] random variable itself. I like to say if it's a poorly grounded persona, it's a
[07:07] it's a poorly grounded persona, it's a
[07:07] it's a poorly grounded persona, it's a little like the LLM is playing improv
[07:09] little like the LLM is playing improv
[07:09] little like the LLM is playing improv with you.
[07:10] with you.
[07:10] with you. It's like gold watch on a table? Oh,
[07:12] It's like gold watch on a table? Oh,
[07:12] It's like gold watch on a table? Oh, well, we must be in a jewelry store,
[07:14] well, we must be in a jewelry store,
[07:14] well, we must be in a jewelry store, right? It has to infer what's likely.
[07:16] right? It has to infer what's likely.
[07:16] right? It has to infer what's likely. And maybe this is a rich person, so
[07:17] And maybe this is a rich person, so
[07:17] And maybe this is a rich person, so they're more likely to purchase. And so
[07:19] they're more likely to purchase. And so
[07:20] they're more likely to purchase. And so the lesson is, we need to richly ground
[07:22] the lesson is, we need to richly ground
[07:22] the lesson is, we need to richly ground our personas in the personality, the
[07:25] our personas in the personality, the
[07:25] our personas in the personality, the context, and bizarrely, even the study's
[07:28] context, and bizarrely, even the study's
[07:28] context, and bizarrely, even the study's own construction. In a human subject
[07:30] own construction. In a human subject
[07:30] own construction. In a human subject experiment, you want to hide the study
[07:32] experiment, you want to hide the study
[07:32] experiment, you want to hide the study construction from the participant. But
[07:34] construction from the participant. But
[07:34] construction from the participant. But in the case of an LLM, they have no
[07:36] in the case of an LLM, they have no
[07:36] in the case of an LLM, they have no universe other than what's in the
[07:37] universe other than what's in the
[07:37] universe other than what's in the prompt, and you have to use the prompt
[07:39] prompt, and you have to use the prompt
[07:39] prompt, and you have to use the prompt to paint the world to prevent any type
[07:41] to paint the world to prevent any type
[07:41] to paint the world to prevent any type of confounders.
[07:43] of confounders.
[07:43] of confounders. Another failure mode is prompt
[07:45] Another failure mode is prompt
[07:45] Another failure mode is prompt sensitivity. So, here's a researcher
[07:47] sensitivity. So, here's a researcher
[07:47] sensitivity. So, here's a researcher that took a question, they give the same
[07:49] that took a question, they give the same
[07:49] that took a question, they give the same question, same choices, they just
[07:51] question, same choices, they just
[07:51] question, same choices, they just swapped the order of the choices. Yes
[07:54] swapped the order of the choices. Yes
[07:54] swapped the order of the choices. Yes was the first one in the first question,
[07:55] was the first one in the first question,
[07:55] was the first one in the first question, yes was the second option in the the
[07:57] yes was the second option in the the
[07:57] yes was the second option in the the second question. What they found was
[07:59] second question. What they found was
[07:59] second question. What they found was that the model had an extremely strong
[08:01] that the model had an extremely strong
[08:01] that the model had an extremely strong order bias.
[08:03] order bias.
[08:03] order bias. Basically, when they took the two
[08:04] Basically, when they took the two
[08:04] Basically, when they took the two results and they averaged them together,
[08:06] results and they averaged them together,
[08:07] results and they averaged them together, it washed out into noise, into 50/50.
[08:09] it washed out into noise, into 50/50.
[08:09] it washed out into noise, into 50/50. Now, humans do have a first order bias,
[08:11] Now, humans do have a first order bias,
[08:11] Now, humans do have a first order bias, but not to this extent. And so, the
[08:13] but not to this extent. And so, the
[08:13] but not to this extent. And so, the lesson here is that we need to
[08:16] lesson here is that we need to
[08:16] lesson here is that we need to durability test our personas to
[08:18] durability test our personas to
[08:18] durability test our personas to understand how they will change under
[08:20] understand how they will change under
[08:20] understand how they will change under reorderings, under rewordings, and even
[08:23] reorderings, under rewordings, and even
[08:23] reorderings, under rewordings, and even adversarial challenges to their
[08:25] adversarial challenges to their
[08:25] adversarial challenges to their opinions.
[08:27] opinions.
[08:27] opinions. The third and final area that I want to
[08:29] The third and final area that I want to
[08:29] The third and final area that I want to highlight is that LLMs are trained on
[08:31] highlight is that LLMs are trained on
[08:31] highlight is that LLMs are trained on what people say,
[08:33] what people say,
[08:33] what people say, and they're not trained on what people
[08:34] and they're not trained on what people
[08:34] and they're not trained on what people do.
[08:35] do.
[08:35] do. So, as a consequence, predicting stated
[08:38] So, as a consequence, predicting stated
[08:38] So, as a consequence, predicting stated attitudes tend to be easier than
[08:40] attitudes tend to be easier than
[08:40] attitudes tend to be easier than predicting actions or behaviors. Both
[08:42] predicting actions or behaviors. Both
[08:42] predicting actions or behaviors. Both because they're clear and likely to be
[08:45] because they're clear and likely to be
[08:45] because they're clear and likely to be in the text, but also because they are
[08:47] in the text, but also because they are
[08:47] in the text, but also because they are natively text themselves. So, this chart
[08:50] natively text themselves. So, this chart
[08:50] natively text themselves. So, this chart is from a bunch of researchers that used
[08:52] is from a bunch of researchers that used
[08:52] is from a bunch of researchers that used an LLM to try and predict known social
[08:54] an LLM to try and predict known social
[08:54] an LLM to try and predict known social science experiments.
[08:56] science experiments.
[08:56] science experiments. The original point of this chart is to
[08:57] The original point of this chart is to
[08:57] The original point of this chart is to show that the LLMs are about as good as
[08:59] show that the LLMs are about as good as
[08:59] show that the LLMs are about as good as the experts. LLM is in black in a
[09:02] the experts. LLM is in black in a
[09:02] the experts. LLM is in black in a circle, the experts are in blue, and you
[09:04] circle, the experts are in blue, and you
[09:04] circle, the experts are in blue, and you can see they're both doing about equally
[09:06] can see they're both doing about equally
[09:06] can see they're both doing about equally well in making the prediction. But, the
[09:07] well in making the prediction. But, the
[09:07] well in making the prediction. But, the point I want to draw you to is that
[09:09] point I want to draw you to is that
[09:09] point I want to draw you to is that there are two categories of experiments
[09:11] there are two categories of experiments
[09:11] there are two categories of experiments here. The top are surveys, those are
[09:13] here. The top are surveys, those are
[09:13] here. The top are surveys, those are natively language and text-based, and
[09:16] natively language and text-based, and
[09:16] natively language and text-based, and those reflect attitudes. And on the
[09:18] those reflect attitudes. And on the
[09:18] those reflect attitudes. And on the whole, the models tend to do better
[09:20] whole, the models tend to do better
[09:20] whole, the models tend to do better there.
[09:21] there.
[09:21] there. The bottom half is field experiments.
[09:23] The bottom half is field experiments.
[09:23] The bottom half is field experiments. Those are behaviors, and those are
[09:24] Those are behaviors, and those are
[09:24] Those are behaviors, and those are things that need to be transcribed into
[09:25] things that need to be transcribed into
[09:25] things that need to be transcribed into actions. They're less likely to be in
[09:27] actions. They're less likely to be in
[09:27] actions. They're less likely to be in the training data, and correspondingly,
[09:29] the training data, and correspondingly,
[09:29] the training data, and correspondingly, the LLM doesn't do as well.
[09:31] the LLM doesn't do as well.
[09:31] the LLM doesn't do as well. So,
[09:32] So,
[09:32] So, the lesson we often tell our clients is
[09:34] the lesson we often tell our clients is
[09:34] the lesson we often tell our clients is consider questions that triangulate to
[09:36] consider questions that triangulate to
[09:36] consider questions that triangulate to behavior from attitudes. As a
[09:38] behavior from attitudes. As a
[09:38] behavior from attitudes. As a hypothetical example, if you want to
[09:40] hypothetical example, if you want to
[09:40] hypothetical example, if you want to know about gym attendance, you might be
[09:41] know about gym attendance, you might be
[09:41] know about gym attendance, you might be better off, well, you can ask about
[09:43] better off, well, you can ask about
[09:43] better off, well, you can ask about both, but asking about attitudes towards
[09:46] both, but asking about attitudes towards
[09:46] both, but asking about attitudes towards working out rather than asking about
[09:48] working out rather than asking about
[09:48] working out rather than asking about attendance and see if that's a suitable
[09:50] attendance and see if that's a suitable
[09:50] attendance and see if that's a suitable proxy.
[09:51] proxy.
[09:51] proxy. Okay.
[09:52] Okay.
[09:52] Okay. Now, let's talk about three example
[09:54] Now, let's talk about three example
[09:54] Now, let's talk about three example techniques to kind of inspire your own
[09:57] techniques to kind of inspire your own
[09:57] techniques to kind of inspire your own synthetic personas.
[09:59] synthetic personas.
[09:59] synthetic personas. So, the first one is just prompting the
[10:01] So, the first one is just prompting the
[10:02] So, the first one is just prompting the model. Uh this right here is from the
[10:05] model. Uh this right here is from the
[10:05] model. Uh this right here is from the Argyle paper, which is really one of the
[10:07] Argyle paper, which is really one of the
[10:07] Argyle paper, which is really one of the seminal papers in this field. In fact,
[10:09] seminal papers in this field. In fact,
[10:09] seminal papers in this field. In fact, it's so early that the model they used
[10:12] it's so early that the model they used
[10:12] it's so early that the model they used was a text completion model. That's why
[10:14] was a text completion model. That's why
[10:14] was a text completion model. That's why this prompt isn't in the form of a chat.
[10:16] this prompt isn't in the form of a chat.
[10:16] this prompt isn't in the form of a chat. It's a statement of I am. So, they gave
[10:19] It's a statement of I am. So, they gave
[10:19] It's a statement of I am. So, they gave it a prompt that said, and for example,
[10:21] it a prompt that said, and for example,
[10:21] it a prompt that said, and for example, the middle column is basically where the
[10:23] the middle column is basically where the
[10:23] the middle column is basically where the context is. I am a strong liberal. I
[10:25] context is. I am a strong liberal. I
[10:25] context is. I am a strong liberal. I support progressive values, etc., etc.
[10:27] support progressive values, etc., etc.
[10:27] support progressive values, etc., etc. And at the end it says, "In 2016, I
[10:29] And at the end it says, "In 2016, I
[10:29] And at the end it says, "In 2016, I voted for." And they basically
[10:31] voted for." And they basically
[10:31] voted for." And they basically let the model sample its completions and
[10:33] let the model sample its completions and
[10:34] let the model sample its completions and it says, uh
[10:35] it says, uh
[10:35] it says, uh Hillary Clinton, Bernie Sanders, Hillary
[10:37] Hillary Clinton, Bernie Sanders, Hillary
[10:37] Hillary Clinton, Bernie Sanders, Hillary Clinton, and so forth. And you can see
[10:38] Clinton, and so forth. And you can see
[10:38] Clinton, and so forth. And you can see what happens with the conservative case
[10:40] what happens with the conservative case
[10:40] what happens with the conservative case on the top.
[10:41] on the top.
[10:41] on the top. Since this time, obviously, there've
[10:44] Since this time, obviously, there've
[10:44] Since this time, obviously, there've been a lot more prompting techniques.
[10:47] been a lot more prompting techniques.
[10:47] been a lot more prompting techniques. And a lot more models. And I can't tell
[10:50] And a lot more models. And I can't tell
[10:50] And a lot more models. And I can't tell you which prompting technique and which
[10:52] you which prompting technique and which
[10:52] you which prompting technique and which model is going to work best for your use
[10:54] model is going to work best for your use
[10:54] model is going to work best for your use case. What you are going to have to do
[10:56] case. What you are going to have to do
[10:56] case. What you are going to have to do is figure it out empirically by
[10:58] is figure it out empirically by
[10:58] is figure it out empirically by validating against some known human
[11:00] validating against some known human
[11:00] validating against some known human ground truth data. You'll have to do
[11:02] ground truth data. You'll have to do
[11:02] ground truth data. You'll have to do what these guys did. So, for example,
[11:04] what these guys did. So, for example,
[11:04] what these guys did. So, for example, here in this research, they're trying to
[11:06] here in this research, they're trying to
[11:06] here in this research, they're trying to figure out how well they can construct
[11:07] figure out how well they can construct
[11:07] figure out how well they can construct personas to represent voting patterns.
[11:10] personas to represent voting patterns.
[11:10] personas to represent voting patterns. What they found was they compared here
[11:13] What they found was they compared here
[11:13] What they found was they compared here on the left is reality and on the right
[11:15] on the left is reality and on the right
[11:15] on the left is reality and on the right is their four different types of persona
[11:17] is their four different types of persona
[11:17] is their four different types of persona constructions. And they didn't realize
[11:19] constructions. And they didn't realize
[11:19] constructions. And they didn't realize it at the time, but their persona
[11:20] it at the time, but their persona
[11:20] it at the time, but their persona construction was actually amplifying
[11:22] construction was actually amplifying
[11:22] construction was actually amplifying bias within the model as they got more
[11:24] bias within the model as they got more
[11:24] bias within the model as they got more and more detailed. And they found it was
[11:26] and more detailed. And they found it was
[11:26] and more detailed. And they found it was actually throwing it further and further
[11:28] actually throwing it further and further
[11:28] actually throwing it further and further astray from reality. So, you probably
[11:30] astray from reality. So, you probably
[11:30] astray from reality. So, you probably have a bunch of different ideas. The
[11:31] have a bunch of different ideas. The
[11:31] have a bunch of different ideas. The answer is you're going to have to test
[11:33] answer is you're going to have to test
[11:33] answer is you're going to have to test it and validate it against ground truth.
[11:37] it and validate it against ground truth.
[11:37] it and validate it against ground truth. The other natural thing you might expect
[11:38] The other natural thing you might expect
[11:38] The other natural thing you might expect is well, hey, we can fine-tune it,
[11:40] is well, hey, we can fine-tune it,
[11:40] is well, hey, we can fine-tune it, especially if it's missing data that
[11:41] especially if it's missing data that
[11:41] especially if it's missing data that isn't there, especially for example, if
[11:43] isn't there, especially for example, if
[11:43] isn't there, especially for example, if it's behaviors or something that
[11:45] it's behaviors or something that
[11:45] it's behaviors or something that wouldn't be in the training text. And
[11:47] wouldn't be in the training text. And
[11:47] wouldn't be in the training text. And this is a great paper to be inspired by
[11:49] this is a great paper to be inspired by
[11:49] this is a great paper to be inspired by for this. This is the Subpop paper.
[11:51] for this. This is the Subpop paper.
[11:51] for this. This is the Subpop paper. Basically, they construct a prompt
[11:53] Basically, they construct a prompt
[11:53] Basically, they construct a prompt template, which is the demographic
[11:54] template, which is the demographic
[11:54] template, which is the demographic information, then the survey question
[11:57] information, then the survey question
[11:57] information, then the survey question they want to ask, and then they compare
[11:59] they want to ask, and then they compare
[11:59] they want to ask, and then they compare the known human data distribution to the
[12:01] the known human data distribution to the
[12:01] the known human data distribution to the distribution that comes out of the
[12:02] distribution that comes out of the
[12:02] distribution that comes out of the model, and they do fine-tuning until the
[12:05] model, and they do fine-tuning until the
[12:05] model, and they do fine-tuning until the model and the human data align.
[12:09] model and the human data align.
[12:09] model and the human data align. Now, here's the interesting thing.
[12:11] Now, here's the interesting thing.
[12:11] Now, here's the interesting thing. When they did this, as you'd expect,
[12:14] When they did this, as you'd expect,
[12:14] When they did this, as you'd expect, the results that were from the
[12:15] the results that were from the
[12:15] the results that were from the populations they gave to the model,
[12:17] populations they gave to the model,
[12:17] populations they gave to the model, that's the ones in blue, improved.
[12:20] that's the ones in blue, improved.
[12:20] that's the ones in blue, improved. But very interestingly, the ones in
[12:22] But very interestingly, the ones in
[12:22] But very interestingly, the ones in white also improved by almost the same
[12:24] white also improved by almost the same
[12:24] white also improved by almost the same degree. Alignment improved even for the
[12:26] degree. Alignment improved even for the
[12:26] degree. Alignment improved even for the unseen groups. That seems almost
[12:29] unseen groups. That seems almost
[12:29] unseen groups. That seems almost magical.
[12:30] magical.
[12:30] magical. And some subsequent research has hinted
[12:33] And some subsequent research has hinted
[12:33] And some subsequent research has hinted that what might be really happening here
[12:35] that what might be really happening here
[12:35] that what might be really happening here is that the model itself has a latent
[12:38] is that the model itself has a latent
[12:38] is that the model itself has a latent understanding of these groups. It just
[12:40] understanding of these groups. It just
[12:41] understanding of these groups. It just didn't know how to express it in the
[12:42] didn't know how to express it in the
[12:42] didn't know how to express it in the format of surveys. And if you think
[12:44] format of surveys. And if you think
[12:44] format of surveys. And if you think about it,
[12:45] about it,
[12:45] about it, LLMs aren't used to doing surveys as a
[12:47] LLMs aren't used to doing surveys as a
[12:47] LLMs aren't used to doing surveys as a task. And so they aren't going to be as
[12:49] task. And so they aren't going to be as
[12:49] task. And so they aren't going to be as good as fitting it, especially to a
[12:51] good as fitting it, especially to a
[12:51] good as fitting it, especially to a prompt format they may not have seen
[12:53] prompt format they may not have seen
[12:53] prompt format they may not have seen on the first go-around. But fine-tuning
[12:55] on the first go-around. But fine-tuning
[12:55] on the first go-around. But fine-tuning actually is helping it learn the task or
[12:57] actually is helping it learn the task or
[12:57] actually is helping it learn the task or how to express itself. So, a lesson you
[13:00] how to express itself. So, a lesson you
[13:00] how to express itself. So, a lesson you can kind of take away is that your
[13:01] can kind of take away is that your
[13:01] can kind of take away is that your persona that you're looking for is in
[13:03] persona that you're looking for is in
[13:03] persona that you're looking for is in there. We just need to figure out the
[13:04] there. We just need to figure out the
[13:05] there. We just need to figure out the way to summon it or elicit it.
[13:08] way to summon it or elicit it.
[13:08] way to summon it or elicit it. And that lesson actually takes us to the
[13:09] And that lesson actually takes us to the
[13:09] And that lesson actually takes us to the third technique, which I want to
[13:11] third technique, which I want to
[13:11] third technique, which I want to highlight to show how sophisticated your
[13:13] highlight to show how sophisticated your
[13:13] highlight to show how sophisticated your techniques can get if you're just using
[13:16] techniques can get if you're just using
[13:16] techniques can get if you're just using so-called prompting alone, but using
[13:18] so-called prompting alone, but using
[13:18] so-called prompting alone, but using careful calibration and thinking.
[13:21] careful calibration and thinking.
[13:21] careful calibration and thinking. So,
[13:22] So,
[13:22] So, in this one, this team did something
[13:24] in this one, this team did something
[13:24] in this one, this team did something very clever. They set up a system prompt
[13:26] very clever. They set up a system prompt
[13:26] very clever. They set up a system prompt that was demographics. They showed a
[13:28] that was demographics. They showed a
[13:28] that was demographics. They showed a product concept. And then they asked how
[13:30] product concept. And then they asked how
[13:30] product concept. And then they asked how likely would you be to purchase this
[13:31] likely would you be to purchase this
[13:31] likely would you be to purchase this product?
[13:33] product?
[13:33] product? And they gave it the same scale from one
[13:35] And they gave it the same scale from one
[13:35] And they gave it the same scale from one to five, five being most likely, one
[13:36] to five, five being most likely, one
[13:36] to five, five being most likely, one being the least likely to purchase, like
[13:38] being the least likely to purchase, like
[13:38] being the least likely to purchase, like you'd expect, kind of your basic naive
[13:41] you'd expect, kind of your basic naive
[13:41] you'd expect, kind of your basic naive prompting pattern.
[13:42] prompting pattern.
[13:42] prompting pattern. And then they said, "Well, you know,
[13:44] And then they said, "Well, you know,
[13:44] And then they said, "Well, you know, hearkening back to that paper, although
[13:45] hearkening back to that paper, although
[13:45] hearkening back to that paper, although I don't know if they were inspired by
[13:46] I don't know if they were inspired by
[13:46] I don't know if they were inspired by it,
[13:47] it,
[13:47] it, they said, 'Well, large language models
[13:49] they said, 'Well, large language models
[13:49] they said, 'Well, large language models aren't used to doing surface, but they
[13:51] aren't used to doing surface, but they
[13:51] aren't used to doing surface, but they are more used to expressing themselves
[13:53] are more used to expressing themselves
[13:53] are more used to expressing themselves in text.'
[13:54] in text.'
[13:54] in text.' So, they said as instead of giving us a
[13:56] So, they said as instead of giving us a
[13:56] So, they said as instead of giving us a one to five rating, give us a set of
[13:58] one to five rating, give us a set of
[13:58] one to five rating, give us a set of text. So, the example here is, 'I'm
[14:00] text. So, the example here is, 'I'm
[14:00] text. So, the example here is, 'I'm somewhat interested. If it works well
[14:02] somewhat interested. If it works well
[14:02] somewhat interested. If it works well and isn't too expensive, I might give it
[14:04] and isn't too expensive, I might give it
[14:04] and isn't too expensive, I might give it a try.'
[14:05] a try.'
[14:05] a try.' And then to map that text to the one
[14:08] And then to map that text to the one
[14:08] And then to map that text to the one through five willingness to pay, they
[14:11] through five willingness to pay, they
[14:11] through five willingness to pay, they had humans write out corresponding text
[14:13] had humans write out corresponding text
[14:13] had humans write out corresponding text for what they would expect. So, if it's
[14:15] for what they would expect. So, if it's
[14:15] for what they would expect. So, if it's a one, "Hell no, I'll never buy that."
[14:17] a one, "Hell no, I'll never buy that."
[14:17] a one, "Hell no, I'll never buy that." Five, "Absolutely, I'll buy 20." Right?
[14:20] Five, "Absolutely, I'll buy 20." Right?
[14:20] Five, "Absolutely, I'll buy 20." Right? They had them write out examples of each
[14:22] They had them write out examples of each
[14:22] They had them write out examples of each one of the different options, and then
[14:23] one of the different options, and then
[14:23] one of the different options, and then they measured the semantic similarity
[14:26] they measured the semantic similarity
[14:26] they measured the semantic similarity between the text that came out of the
[14:27] between the text that came out of the
[14:27] between the text that came out of the model and those human examples. And that
[14:30] model and those human examples. And that
[14:30] model and those human examples. And that gave them a vector over which they can
[14:33] gave them a vector over which they can
[14:33] gave them a vector over which they can basically measure a probability
[14:35] basically measure a probability
[14:35] basically measure a probability distribution of where this text that
[14:36] distribution of where this text that
[14:36] distribution of where this text that came out of the model lands. So, what I
[14:38] came out of the model lands. So, what I
[14:38] came out of the model lands. So, what I like about this is it's actually a
[14:39] like about this is it's actually a
[14:39] like about this is it's actually a distribution. Kind of feels like, you
[14:41] distribution. Kind of feels like, you
[14:41] distribution. Kind of feels like, you know, human. Some days I might say four,
[14:43] know, human. Some days I might say four,
[14:43] know, human. Some days I might say four, some might Some days I might say five in
[14:44] some might Some days I might say five in
[14:44] some might Some days I might say five in this graph, but rarely would I say one,
[14:46] this graph, but rarely would I say one,
[14:46] this graph, but rarely would I say one, two, or three in this example.
[14:48] two, or three in this example.
[14:48] two, or three in this example. And what they were able to show is that
[14:50] And what they were able to show is that
[14:51] And what they were able to show is that they were not able to only reconstruct
[14:53] they were not able to only reconstruct
[14:53] they were not able to only reconstruct accurate values for willingness to pay.
[14:55] accurate values for willingness to pay.
[14:55] accurate values for willingness to pay. They were able to capture the
[14:57] They were able to capture the
[14:57] They were able to capture the distribution. Because one of the
[14:58] distribution. Because one of the
[14:58] distribution. Because one of the important failure modes we haven't
[14:59] important failure modes we haven't
[14:59] important failure modes we haven't talked about is that LLMs, even when
[15:01] talked about is that LLMs, even when
[15:02] talked about is that LLMs, even when they get the persona averages right,
[15:04] they get the persona averages right,
[15:04] they get the persona averages right, they very often lose the details. The
[15:06] they very often lose the details. The
[15:06] they very often lose the details. The variations get muddled together in the
[15:08] variations get muddled together in the
[15:08] variations get muddled together in the middle.
[15:09] middle.
[15:09] middle. This chart at the bottom,
[15:11] This chart at the bottom,
[15:11] This chart at the bottom, basically that horizontal axis is a
[15:13] basically that horizontal axis is a
[15:13] basically that horizontal axis is a measure of the entire shape similarity.
[15:16] measure of the entire shape similarity.
[15:16] measure of the entire shape similarity. And one means perfectly identical, and
[15:18] And one means perfectly identical, and
[15:18] And one means perfectly identical, and zero means not. And what you can see is
[15:21] zero means not. And what you can see is
[15:21] zero means not. And what you can see is the naive way, in the purple or I guess
[15:23] the naive way, in the purple or I guess
[15:23] the naive way, in the purple or I guess pink uh doesn't do as well as the yellow
[15:26] pink uh doesn't do as well as the yellow
[15:26] pink uh doesn't do as well as the yellow which is up near the top of the range.
[15:28] which is up near the top of the range.
[15:28] which is up near the top of the range. So that means it really did a good job
[15:29] So that means it really did a good job
[15:29] So that means it really did a good job not only understanding what the ultimate
[15:32] not only understanding what the ultimate
[15:32] not only understanding what the ultimate choice was but how well that choice
[15:34] choice was but how well that choice
[15:34] choice was but how well that choice varied.
[15:35] varied.
[15:35] varied. Okay. Let's talk about how to measure
[15:38] Okay. Let's talk about how to measure
[15:38] Okay. Let's talk about how to measure alignment from a synthetic persona.
[15:41] alignment from a synthetic persona.
[15:41] alignment from a synthetic persona. One of the things that our traditional
[15:43] One of the things that our traditional
[15:43] One of the things that our traditional market research clients are sometimes
[15:46] market research clients are sometimes
[15:46] market research clients are sometimes surprised by and disappointed is that
[15:48] surprised by and disappointed is that
[15:48] surprised by and disappointed is that you cannot use statistical
[15:50] you cannot use statistical
[15:50] you cannot use statistical synthetic personas to boost statistical
[15:52] synthetic personas to boost statistical
[15:52] synthetic personas to boost statistical significance. You can take an
[15:53] significance. You can take an
[15:53] significance. You can take an underrepresented population and get more
[15:56] underrepresented population and get more
[15:56] underrepresented population and get more values out of it but you can't say it's
[15:58] values out of it but you can't say it's
[15:58] values out of it but you can't say it's statistically significant. And to
[15:59] statistically significant. And to
[15:59] statistically significant. And to understand this it helps to go back to
[16:01] understand this it helps to go back to
[16:01] understand this it helps to go back to that weather analogy. If I want to know
[16:04] that weather analogy. If I want to know
[16:04] that weather analogy. If I want to know how much it rains today in San Francisco
[16:06] how much it rains today in San Francisco
[16:06] how much it rains today in San Francisco and I used to live here so I know it
[16:07] and I used to live here so I know it
[16:07] and I used to live here so I know it rains a lot, I'd stick a weather gauge.
[16:09] rains a lot, I'd stick a weather gauge.
[16:09] rains a lot, I'd stick a weather gauge. If I want to know with more certainty,
[16:11] If I want to know with more certainty,
[16:11] If I want to know with more certainty, I'd stick a thousand weather gauges and
[16:13] I'd stick a thousand weather gauges and
[16:13] I'd stick a thousand weather gauges and those would increase the accuracy of my
[16:15] those would increase the accuracy of my
[16:15] those would increase the accuracy of my estimate.
[16:16] estimate.
[16:16] estimate. But if I want to know if it's going to
[16:18] But if I want to know if it's going to
[16:18] But if I want to know if it's going to rain tomorrow, if I take a forecast and
[16:21] rain tomorrow, if I take a forecast and
[16:21] rain tomorrow, if I take a forecast and I rerun it a thousand times without
[16:22] I rerun it a thousand times without
[16:23] I rerun it a thousand times without changing the input, that doesn't change
[16:24] changing the input, that doesn't change
[16:24] changing the input, that doesn't change my certainty of that forecast. It
[16:26] my certainty of that forecast. It
[16:26] my certainty of that forecast. It improves my estimate of what the model
[16:29] improves my estimate of what the model
[16:29] improves my estimate of what the model is telling me but it doesn't make the
[16:30] is telling me but it doesn't make the
[16:30] is telling me but it doesn't make the forecast itself more accurate. And
[16:32] forecast itself more accurate. And
[16:32] forecast itself more accurate. And that's what happens when you basically
[16:34] that's what happens when you basically
[16:34] that's what happens when you basically are rerunning a synthetic persona with
[16:35] are rerunning a synthetic persona with
[16:35] are rerunning a synthetic persona with no changes to input. So the lesson is
[16:37] no changes to input. So the lesson is
[16:37] no changes to input. So the lesson is more synthetic samples aren't actually
[16:39] more synthetic samples aren't actually
[16:39] more synthetic samples aren't actually going to improve your statistical
[16:40] going to improve your statistical
[16:41] going to improve your statistical significance for the most part.
[16:43] significance for the most part.
[16:43] significance for the most part. So what you need to do is you need to do
[16:45] So what you need to do is you need to do
[16:45] So what you need to do is you need to do what you do with weather forecast. You'd
[16:46] what you do with weather forecast. You'd
[16:46] what you do with weather forecast. You'd basically check against what actually
[16:49] basically check against what actually
[16:49] basically check against what actually happened or in our case what humans
[16:51] happened or in our case what humans
[16:51] happened or in our case what humans actually said. And that's where we're
[16:52] actually said. And that's where we're
[16:52] actually said. And that's where we're going to basically be measuring
[16:54] going to basically be measuring
[16:54] going to basically be measuring distributions of data. Unlike classic
[16:56] distributions of data. Unlike classic
[16:56] distributions of data. Unlike classic e-vals where there's clearly a right and
[16:58] e-vals where there's clearly a right and
[16:58] e-vals where there's clearly a right and wrong and you can score how many were
[16:59] wrong and you can score how many were
[16:59] wrong and you can score how many were right and how many wrong, now we need to
[17:01] right and how many wrong, now we need to
[17:01] right and how many wrong, now we need to measure the data as a comparison of
[17:03] measure the data as a comparison of
[17:03] measure the data as a comparison of distributions. And there are many ways
[17:05] distributions. And there are many ways
[17:05] distributions. And there are many ways for distributions to get wrong. They
[17:07] for distributions to get wrong. They
[17:07] for distributions to get wrong. They could be completely wildly off. They can
[17:08] could be completely wildly off. They can
[17:08] could be completely wildly off. They can as we mentioned get the average right
[17:10] as we mentioned get the average right
[17:10] as we mentioned get the average right but the shape of the distribution wrong.
[17:12] but the shape of the distribution wrong.
[17:12] but the shape of the distribution wrong. And so you're going to need multiple
[17:14] And so you're going to need multiple
[17:14] And so you're going to need multiple metrics to capture how well your model
[17:16] metrics to capture how well your model
[17:16] metrics to capture how well your model is reflecting different personas. Um I
[17:19] is reflecting different personas. Um I
[17:19] is reflecting different personas. Um I recommend using a correlation type
[17:21] recommend using a correlation type
[17:21] recommend using a correlation type metric along with one of these shape
[17:23] metric along with one of these shape
[17:23] metric along with one of these shape type metrics which capture what the
[17:25] type metrics which capture what the
[17:25] type metrics which capture what the underlying shape of the distribution is.
[17:28] underlying shape of the distribution is.
[17:28] underlying shape of the distribution is. The other thing you need to do is
[17:29] The other thing you need to do is
[17:30] The other thing you need to do is estimate the fundamental noise in your
[17:31] estimate the fundamental noise in your
[17:31] estimate the fundamental noise in your ground truth data. That experiment I
[17:34] ground truth data. That experiment I
[17:34] ground truth data. That experiment I talked about in the beginning where they
[17:35] talked about in the beginning where they
[17:35] talked about in the beginning where they got 83% accuracy,
[17:38] got 83% accuracy,
[17:38] got 83% accuracy, the key smart thing they did is they
[17:40] the key smart thing they did is they
[17:40] the key smart thing they did is they took those humans and they brought them
[17:41] took those humans and they brought them
[17:41] took those humans and they brought them back 2 weeks later and they redid the
[17:44] back 2 weeks later and they redid the
[17:44] back 2 weeks later and they redid the battery of surveys and personality tests
[17:46] battery of surveys and personality tests
[17:46] battery of surveys and personality tests and they found that the humans on
[17:47] and they found that the humans on
[17:47] and they found that the humans on average were only 80% consistent to
[17:50] average were only 80% consistent to
[17:50] average were only 80% consistent to themselves.
[17:51] themselves.
[17:51] themselves. So that sets a noise floor as how
[17:54] So that sets a noise floor as how
[17:54] So that sets a noise floor as how accurate our models could ever get
[17:56] accurate our models could ever get
[17:56] accurate our models could ever get because the humans themselves are
[17:57] because the humans themselves are
[17:57] because the humans themselves are fundamentally noisy. And so the 83% is
[18:00] fundamentally noisy. And so the 83% is
[18:00] fundamentally noisy. And so the 83% is actually normalized against that.
[18:03] actually normalized against that.
[18:03] actually normalized against that. If you can do this and bring your humans
[18:05] If you can do this and bring your humans
[18:05] If you can do this and bring your humans back, that's great. Very often you
[18:07] back, that's great. Very often you
[18:07] back, that's great. Very often you can't. So the way you can kind of
[18:09] can't. So the way you can kind of
[18:09] can't. So the way you can kind of artificially do this is take your ground
[18:11] artificially do this is take your ground
[18:11] artificially do this is take your ground truth human data, break it into two
[18:13] truth human data, break it into two
[18:13] truth human data, break it into two chunks, and then pretend one is
[18:15] chunks, and then pretend one is
[18:15] chunks, and then pretend one is synthetic and one is human, and then
[18:17] synthetic and one is human, and then
[18:17] synthetic and one is human, and then measure the correlation and repeat that
[18:18] measure the correlation and repeat that
[18:18] measure the correlation and repeat that hundreds and thousands of times and
[18:20] hundreds and thousands of times and
[18:20] hundreds and thousands of times and average it, and that'll set kind of a
[18:21] average it, and that'll set kind of a
[18:21] average it, and that'll set kind of a noise floor that your ground truth data
[18:23] noise floor that your ground truth data
[18:23] noise floor that your ground truth data where half of it's synthetic, half of it
[18:25] where half of it's synthetic, half of it
[18:25] where half of it's synthetic, half of it real, could be the level of accuracy you
[18:27] real, could be the level of accuracy you
[18:27] real, could be the level of accuracy you could hope to get.
[18:29] could hope to get.
[18:29] could hope to get. So hopefully by now you have an
[18:30] So hopefully by now you have an
[18:31] So hopefully by now you have an appreciation for why I think weather
[18:33] appreciation for why I think weather
[18:33] appreciation for why I think weather forecasts are the best lens to
[18:36] forecasts are the best lens to
[18:36] forecasts are the best lens to understand synthetic personas. They are
[18:38] understand synthetic personas. They are
[18:38] understand synthetic personas. They are not people, they are forecasts, and we
[18:40] not people, they are forecasts, and we
[18:40] not people, they are forecasts, and we should treat them accordingly. Both
[18:42] should treat them accordingly. Both
[18:42] should treat them accordingly. Both systems are bounded, both systems will
[18:45] systems are bounded, both systems will
[18:45] systems are bounded, both systems will be improving over time, and they're most
[18:47] be improving over time, and they're most
[18:47] be improving over time, and they're most trustworthy when they're validated
[18:49] trustworthy when they're validated
[18:49] trustworthy when they're validated against reality.
[18:51] against reality.
[18:51] against reality. Um
[18:53] Um
[18:53] Um Now synthetic personas are very often
[18:55] Now synthetic personas are very often
[18:55] Now synthetic personas are very often cast in the market against human
[18:58] cast in the market against human
[18:58] cast in the market against human research. And I think that's unfortunate
[19:00] research. And I think that's unfortunate
[19:00] research. And I think that's unfortunate because they're actually complementary
[19:01] because they're actually complementary
[19:01] because they're actually complementary to each other. Let me give you two
[19:02] to each other. Let me give you two
[19:02] to each other. Let me give you two reasons why. One is that
[19:05] reasons why. One is that
[19:05] reasons why. One is that we're entering an era where humans are
[19:07] we're entering an era where humans are
[19:07] we're entering an era where humans are no longer the sole economic actor. Every
[19:10] no longer the sole economic actor. Every
[19:10] no longer the sole economic actor. Every action your human customer is taking in
[19:12] action your human customer is taking in
[19:12] action your human customer is taking in terms of awareness, consideration, or a
[19:14] terms of awareness, consideration, or a
[19:14] terms of awareness, consideration, or a purchase decision to buy is being
[19:17] purchase decision to buy is being
[19:17] purchase decision to buy is being increasingly mediated by AI agents. So,
[19:20] increasingly mediated by AI agents. So,
[19:20] increasingly mediated by AI agents. So, a human-only study is actually not the
[19:23] a human-only study is actually not the
[19:23] a human-only study is actually not the gold truth. What we really need to
[19:25] gold truth. What we really need to
[19:25] gold truth. What we really need to understand is what does the human plus
[19:27] understand is what does the human plus
[19:27] understand is what does the human plus agent ecosystem look like?
[19:33] And then finally, the alternative to a
[19:33] And then finally, the alternative to a synthetic persona is not human research.
[19:36] synthetic persona is not human research.
[19:36] synthetic persona is not human research. In most cases, it's no research or it's
[19:38] In most cases, it's no research or it's
[19:38] In most cases, it's no research or it's somebody's opinion. What really happens
[19:40] somebody's opinion. What really happens
[19:40] somebody's opinion. What really happens is you've done a survey of humans and
[19:42] is you've done a survey of humans and
[19:42] is you've done a survey of humans and you get a question and if it's in the
[19:43] you get a question and if it's in the
[19:43] you get a question and if it's in the survey, you can just answer it. That's
[19:45] survey, you can just answer it. That's
[19:45] survey, you can just answer it. That's very simple to do. But what typically
[19:47] very simple to do. But what typically
[19:47] very simple to do. But what typically happens is it's 2 months later and
[19:49] happens is it's 2 months later and
[19:49] happens is it's 2 months later and you're like, we need to answer this
[19:50] you're like, we need to answer this
[19:50] you're like, we need to answer this question which we didn't ask. Well, then
[19:52] question which we didn't ask. Well, then
[19:52] question which we didn't ask. Well, then somebody needs to be like, "Uh I think
[19:54] somebody needs to be like, "Uh I think
[19:54] somebody needs to be like, "Uh I think it would be this by extrapolation."
[19:57] it would be this by extrapolation."
[19:57] it would be this by extrapolation." Uh expert plus a synthetic persona is
[19:59] Uh expert plus a synthetic persona is
[19:59] Uh expert plus a synthetic persona is going to give you a better result to
[20:01] going to give you a better result to
[20:01] going to give you a better result to that. So, what we like to tell customers
[20:03] that. So, what we like to tell customers
[20:03] that. So, what we like to tell customers is synthetic extends your human data to
[20:05] is synthetic extends your human data to
[20:06] is synthetic extends your human data to more phases of your development process.
[20:08] more phases of your development process.
[20:08] more phases of your development process. It can go more places your existing
[20:10] It can go more places your existing
[20:10] It can go more places your existing research can't. One of the most exciting
[20:12] research can't. One of the most exciting
[20:12] research can't. One of the most exciting directions is to actually run
[20:14] directions is to actually run
[20:14] directions is to actually run simulations. We didn't get time for
[20:15] simulations. We didn't get time for
[20:15] simulations. We didn't get time for this, but it's called generative
[20:17] this, but it's called generative
[20:17] this, but it's called generative agent-based modeling where we can take
[20:19] agent-based modeling where we can take
[20:19] agent-based modeling where we can take each of these personas and simulate with
[20:21] each of these personas and simulate with
[20:21] each of these personas and simulate with the dynamics and how they'll interface
[20:23] the dynamics and how they'll interface
[20:23] the dynamics and how they'll interface interface and interact with each other.
[20:25] interface and interact with each other.
[20:25] interface and interact with each other. And ultimately, what this will let you
[20:26] And ultimately, what this will let you
[20:26] And ultimately, what this will let you do is turn your human data into a living
[20:30] do is turn your human data into a living
[20:30] do is turn your human data into a living queryable asset.
[20:33] queryable asset.
[20:33] queryable asset. If you're interested in doing that with
[20:34] If you're interested in doing that with
[20:34] If you're interested in doing that with your data, feel free to reach out to us.
[20:36] your data, feel free to reach out to us.
[20:36] your data, feel free to reach out to us. We help market research and insights
[20:38] We help market research and insights
[20:38] We help market research and insights teams generate and use synthetic
[20:40] teams generate and use synthetic
[20:41] teams generate and use synthetic personas in AI. You can find us on the
[20:43] personas in AI. You can find us on the
[20:43] personas in AI. You can find us on the web at insights sciences.ai
[20:45] web at insights sciences.ai
[20:45] web at insights sciences.ai and my contact information is on the
[20:47] and my contact information is on the
[20:47] and my contact information is on the slide. I hope you have a good
[20:49] slide. I hope you have a good
[20:49] slide. I hope you have a good conference. Thank you.
[20:51] conference. Thank you.
[20:51] conference. Thank you. &gt;&gt; [applause]
