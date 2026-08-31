# Inside DeepWiki: How Cognition Builds Wikis for Devin at Scale

- **Video:** https://www.youtube.com/watch?v=u8Im0l_vwqM
- **Generated:** 2026-08-31 20:41 UTC
- **Status:** Completed

## Technical brief

# Executive takeaway

The substantive material in the provided summaries is limited to the closing discussion of **context engineering for AI-assisted software development**. The speaker’s central claim is that **pre-computing and maintaining structured knowledge about a codebase**—described as a “wiki-style” or “pre-computation-style” approach—could materially improve codebase intelligence beyond relying only on live repository retrieval at prompt time.

Key opportunities identified by the speaker:

- Precomputed codebase knowledge and documentation
- Better context selection and retrieval efficiency
- Persistent user or team preferences
- Richer codebase intelligence overall

No specific product, reference architecture, implementation plan, benchmark, cost estimate, or quantified outcome was provided. Section 1 contains no technical content; it only requests the next transcript section.

For Superior Propane, the relevant implication is to evaluate a governed, source-grounded engineering knowledge layer for Azure, Databricks, infrastructure-as-code, data pipelines, and operational documentation—not to treat AI-generated technical summaries as authoritative system records.

# Technical details

## What the speaker explicitly claims

The speaker states that there is meaningful remaining opportunity in **context engineering**, particularly through:

- **Wiki-style or precomputed knowledge**
  - Maintaining useful codebase intelligence before a user asks a question, rather than constructing all context dynamically from raw repositories.

- **User preferences**
  - Retaining relevant preferences to improve assistant usefulness.
  - The transcript does not define whether this means individual preferences, team standards, coding conventions, role-based settings, or persistent agent memory.

- **Inference and retrieval efficiency**
  - The speaker believes efficiency can be improved, but does not specify whether this refers to:
    - Model-token consumption
    - Query latency
    - Retrieval relevance
    - Indexing/processing costs
    - Developer productivity

- **Continued work on codebase intelligence**
  - The speaker indicates active work in this area but provides no roadmap, product name, release timing, or technical design.

## Likely architecture pattern — inference, not stated in the transcript

A practical interpretation of “wiki-style” or “pre-computation-style” codebase intelligence would be an ingestion and enrichment pipeline that creates durable knowledge artifacts before runtime queries.

### Possible workflow

1. **Ingest authoritative engineering sources**
   - Source-code repositories
   - Internal technical documentation
   - Pull requests and issue trackers
   - Infrastructure-as-code repositories, such as Terraform, Bicep, or ARM
   - API specifications and event schemas
   - Build, deployment, and operational metadata

2. **Create derived artifacts**
   - Repository, service, module, or file summaries
   - Dependency and ownership maps
   - API and data-contract summaries
   - Architecture and data-flow descriptions
   - Embeddings for semantic search
   - Potential code graphs for call relationships and impact analysis

3. **Persist the artifacts**
   - Store source-linked summaries, metadata, graph relationships, embeddings, and access-control metadata.
   - Every derived artifact should retain links to its source and its version, such as repository, branch, commit SHA, deployment version, and refresh date.

4. **Refresh incrementally**
   - Update affected artifacts when commits merge, pull requests are approved, infrastructure is deployed, schemas change, or scheduled scans run.
   - Incremental processing is preferable to repeatedly reprocessing entire repositories for every user query.

5. **Retrieve targeted context at runtime**
   - Retrieve the smallest useful combination of:
     - Precomputed technical summaries
     - Authoritative source excerpts
     - Runbooks and approved documentation
     - Ownership and environment metadata
   - Require source citations in model responses.

## Operational trade-offs

| Approach | Advantages | Limitations and operating burden |
|---|---|---|
| Live repository/document retrieval | Uses current source material; avoids maintaining extensive derived content | Can be slow, token-intensive, noisy, and less effective for broad architecture questions |
| Precomputed summaries/wiki artifacts | Faster context assembly; better high-level system understanding; lower repeated inference effort | Can become stale, omit critical details, or introduce inaccurate inferred descriptions |
| Vector/embedding retrieval | Helps discover semantically related code and documents across large estates | Requires chunking, evaluation, re-indexing, permission enforcement, and monitoring |
| Dependency graphs/code graphs | Better impact analysis, service relationships, and call/data-flow reasoning | More complex parsers, metadata models, and incremental-update logic |
| Persistent user/team preferences | More tailored output and less repeated prompting | Requires privacy boundaries, governance, lifecycle management, and clear distinction between user preference and organizational policy |

## Security and governance requirements

The transcript does not address security controls. For enterprise implementation, these are essential:

- **Access control inheritance**
  - Derived summaries, embeddings, and graph artifacts must preserve source repository and document permissions.
  - A summary of restricted code can itself disclose sensitive information.

- **Identity and authorization**
  - Use Microsoft Entra ID and group-based authorization.
  - Enforce permissions at both ingestion and retrieval, rather than only at the chat application layer.

- **Secret and sensitive-data handling**
  - Scan repositories and documents before indexing.
  - Prevent credentials, connection strings, private endpoints, customer data, and sensitive implementation details from being exposed through retrieval or generated summaries.

- **Environment separation**
  - Keep development, test, and production knowledge stores and retrieval scopes appropriately segregated.
  - Production operational context should have more restrictive access and auditing.

- **Traceability**
  - Show source links, source versions, and refresh timestamps.
  - Clearly label generated summaries as AI-derived rather than authoritative documentation.

- **Auditability**
  - Log user queries, retrieved artifacts, authorization decisions, and model outputs where security and privacy policy permit.

# Potential applications for Superior Propane

## 1. Engineering intelligence for Azure and Databricks estates

A governed assistant could support questions that currently require cross-repository and cross-platform investigation, for example:

- Which Databricks jobs, pipelines, notebooks, or dashboards depend on a source table?
- What downstream data products could be affected by a schema change?
- Which Azure resources support a particular business integration, API, or operational workflow?
- Which repository or team owns a production pipeline, service, or infrastructure component?
- Where are a service principal, key vault reference, endpoint configuration, or data contract used?
- What deployment, rollback, and validation procedures apply to a data product?

Potential precomputed knowledge assets:

- Databricks job and pipeline summaries
- Unity Catalog metadata and lineage, where available and appropriately authorized
- Azure resource inventory and relationship mappings
- Terraform, Bicep, and ARM template summaries
- API specifications, event contracts, and schema metadata
- Repository ownership, service catalog, and on-call metadata
- Source-linked runbooks and incident knowledge

## 2. Better grounding for Azure AI Foundry assistants

An Azure AI Foundry-based engineering assistant should not depend solely on attaching large repositories or broad document collections at prompt time.

A stronger pattern would be:

- Ingest approved technical sources into a governed knowledge pipeline.
- Generate and maintain structured summaries, dependencies, ownership metadata, and source links.
- At runtime, provide the model with:
  - A concise service, pipeline, or domain summary
  - Relevant current source snippets
  - Approved operational documentation
  - Environment, owner, and last-refresh metadata
- Require citations in all engineering answers.

This may improve relevance, latency, and usability compared with raw repository context, but it needs measurement against a baseline approach.

## 3. Auto-maintained engineering and operations wiki

A source-linked technical wiki could reduce reliance on a small number of subject-matter experts and improve resilience during incidents, changes, and team transitions.

Useful content could include:

- Business capability and system purpose
- Service, repository, and product ownership
- Upstream and downstream dependencies
- Data flows and classifications
- Deployment, rollback, and recovery procedures
- Monitoring links and known failure modes
- Required approvals and operational controls

This could be valuable across customer platforms, billing, field-service processes, integration services, Azure infrastructure, and data-platform workflows, where dependencies may span multiple teams.

## 4. Controlled role- and team-based assistance

The speaker mentions user preferences. At Superior Propane, the safer implementation would focus on **approved role and team context**, rather than unrestricted individual memory.

Examples:

- **Data engineers:** Databricks, SQL, Python, pipeline, lineage, and data-quality guidance.
- **Cloud platform engineers:** Azure Policy, Terraform/Bicep, networking, identity, security, and deployment guidance.
- **Product owners:** ownership, dependency, release-impact, delivery risk, and operational-readiness summaries.
- **Engineering teams:** approved coding standards, architecture patterns, naming conventions, and documentation expectations.

# Risks/validation questions

## Principal risks

### Stale derived knowledge

Precomputed artifacts can drift from repositories, deployed resources, and actual production behavior.

**Controls to validate:**

- Trigger updates from merged pull requests, main-branch commits, releases, schema changes, and deployment events.
- Retain commit SHA, source URL, environment, and refresh time on every artifact.
- Define freshness service-level objectives by use case.
- Use direct source links and live metadata for production-impacting decisions.

### Hallucinated or lossy summaries

AI-generated summaries can omit edge cases, security logic, error handling, or operational behavior.

**Controls to validate:**

- Treat generated summaries as discovery and navigation aids, not system-of-record documentation.
- Ground answers in retrieved code, configuration, platform metadata, and approved runbooks.
- Require citations and expose evidence used for each answer.
- Add human review for high-value architecture artifacts and production runbooks.
- Evaluate response correctness using representative engineering scenarios.

### Access-control leakage

Embedding indexes, summaries, and graphs can leak information from restricted repositories, infrastructure definitions, or operational documentation.

**Controls to validate:**

- Enforce source permissions during ingestion and retrieval.
- Ensure summaries and embeddings inherit repository/document ACLs.
- Apply Entra ID authorization and group-based access controls.
- Scan, redact, or exclude secrets and sensitive material before indexing.
- Audit access to restricted operational and production knowledge.

### Cost and operational complexity

Precomputation reduces repeated prompt-time work but introduces continuous ingestion and maintenance costs.

Cost areas to model:

- LLM summarization of repositories, modules, and files
- Embedding generation and re-embedding after changes
- Vector index, graph, metadata, and document storage
- Databricks compute for parsing, transformation, lineage integration, or batch enrichment
- Azure Functions, containers, or other compute for event-driven indexing
- Azure AI Foundry inference, evaluation, and observability workloads
- Support effort for pipeline failures, index freshness, ACL synchronization, and quality evaluation

The appropriate design depends on repository size, change frequency, query volumes, required freshness, security classification, and the value of the supported workflows.

## Questions left unanswered by the source material

1. What exactly does “wiki-style” mean?
   - Human-authored documentation, AI-generated summaries, dependency maps, code graphs, or a combination?

2. What artifacts are precomputed?
   - Summaries, embeddings, ownership metadata, call graphs, diagrams, test coverage, or agent plans?

3. How are artifacts refreshed?
   - Per commit, pull request merge, release, scheduled batch, event-driven deployment, or on-demand?

4. What is the intended scope?
   - Single repository, a team’s repositories, or cross-enterprise engineering intelligence?

5. How are permissions propagated to generated summaries and vector indexes?

6. How is source truth distinguished from inferred documentation?

7. What evidence supports the claimed improvement?
   - No benchmarks or metrics are provided for answer quality, latency, model usage, cost, or developer productivity.

8. How should user preferences be governed?
   - What is retained, who can manage it, how long is it retained, and how does it interact with organizational standards?

# Action items

1. **Select bounded, high-value use cases**
   - Prioritize questions with known pain and measurable outcomes:
     - Data-pipeline impact analysis
     - Service and repository ownership lookup
     - Deployment and rollback discovery
     - Azure resource and infrastructure-as-code relationship discovery

2. **Run a limited pilot**
   - Start with one or two non-sensitive Azure/Databricks engineering domains.
   - Generate source-linked service and module summaries, ownership metadata, dependency information, and approved runbook links.

3. **Compare two context strategies**
   - Establish a baseline using conventional document/code RAG.
   - Compare it with precomputed summaries and metadata on:
     - Answer correctness
     - Citation quality
     - Retrieval relevance
     - Response latency
     - Token consumption
     - Indexing and refresh cost
     - Task completion time and user satisfaction

4. **Design authoritative grounding from the start**
   - Require citations to repositories, commits, Databricks assets, Azure resource metadata, and approved runbooks.
   - Clearly label AI-derived content and display last-refresh information.

5. **Define freshness and ownership controls**
   - Establish update triggers, staleness thresholds, artifact owners, failure handling, and monitoring for the enrichment pipeline.
   - Identify which artifacts require human approval before they are exposed broadly.

6. **Validate security architecture before broad ingestion**
   - Confirm Entra ID integration, ACL propagation, secret scanning, source-data classification, environment separation, retention rules, and audit logging.
   - Test whether restricted content can be inferred through summaries, embeddings, and cross-source retrieval.

7. **Assess Azure-native implementation options**
   - Evaluate Azure AI Foundry for model orchestration, evaluation, and governed application delivery.
   - Evaluate Databricks where scalable enrichment, metadata processing, Unity Catalog integration, or data-platform lineage are relevant.
   - Do not select a platform solely from this transcript; it provides no vendor-specific recommendation or comparative evidence.

## Full transcript

[00:01] [MUSIC]
[00:11] &gt;&gt; Hi everyone.
[00:12] First of all, thank you all for coming here.
[00:14] I'm Jacob. I work at Cognition.
[00:16] Now, working on Deepwiki as well as a lot of other things.
[00:19] First of all, thanks to Brace and
[00:20] the rest of the Lang chain team for
[00:22] help inviting me here and I'm very excited to come talk a bit about Deepwiki.
[00:26] Yeah, so just a show of hands,
[00:27] How many of you have heard of or used DeepWiki?
[00:31] Okay, good number. Yeah.
[00:32] So for those who haven't,
[00:34] it's basically a website,
[00:36] DeepWiki.com, where you're able to generate
[00:39] your own codebase documentation from a lot of open-source repos.
[00:43] So the way to do it is let's say you have
[00:44] an open-source repo that you want to explore.
[00:46] You can just change GitHub to DeepWiki in the name.
[00:50] From there, you'll be able to see auto-generated
[00:53] a codebase documentation and there's also a Q&amp;A feature on top of it as well.
[00:59] So you can ask Devin about basically anything you want about the repo.
[01:05] So I'll give a bit about the intro about the origin of how DeepWiki came about.
[01:09] I think it's pretty interesting that the first iteration of DeepWiki as well as
[01:14] our accompanying product,
[01:15] Ask Devin was actually first built for
[01:17] our main agent to get better macro understanding of our code base.
[01:21] I think that's how a lot of these new wiki related things
[01:25] have come about.
[01:26] And this is over a year ago.
[01:29] So we then realized while building it
[01:31] that it also became a very useful product for humans to read.
[01:35] People liked using it and using it
[01:37] to onboard on a code base or just ask questions about it.
[01:42] And yeah, so we decided we released it as part of a product.
[01:44] And later on, we decided we'll release for open source repos.
[01:48] So we actually took the first top 100k repos on GitHub.
[01:52] We indexed them and released it on deepwiki.com
[01:54] for people to use.
[01:56] I think that was a pretty big hit.
[01:57] So now, today, we have about 1.4 million repositories
[02:01] indexed on deepwiki.com.
[02:03] We served over 20 million queries.
[02:05] And yeah, if you guys haven't seen it yet,
[02:08] you should definitely try it out.
[02:10] So as part of that, it's also being built now
[02:13] into the context layer behind Devin, which
[02:15] is our cloud coding agent.
[02:17] Yeah, and I think there's a cool shout out from
[02:20] Karpathy here where he talked about DeepWiki.
[02:23] Yeah.
[02:27] So now I want to talk a bit about the DeepWiki algorithm
[02:30] and what goes on behind it.
[02:32] So I think a lot of just like Wikigeneration these days
[02:35] is almost fully kind of agent driven.
[02:39] And I think to a large part, that's like mostly true now.
[02:43] But I think there's still like some elements
[02:45] that we want to orchestrate.
[02:48] So the initial question is just why don't we just take a coding agent,
[02:51] prompt it, write me a wiki for this code base.
[02:54] Yeah, so that actually works pretty well these days.
[02:58] If you look at, you take one small or medium-sized repo,
[03:02] and I guess I think that's pretty reasonable for human reading.
[03:06] But I think the main problem comes when you have a bunch of constraints.
[03:10] So first one is scale and second one is quality.
[03:14] So I think at Cognition,
[03:16] we are working for a lot of big enterprises who have
[03:18] a very high scale of code bases.
[03:21] So we have some customers with
[03:23] like one repo which is like 20 gigabytes,
[03:26] and have like 10 to millions of lines,
[03:29] or some orgs have like 100K repos scaling horizontally,
[03:33] and there are like individual projects that need to
[03:35] touch like a thousand repos at the same time.
[03:38] So basically at this level,
[03:40] it becomes kind of like in practical to run
[03:42] your entire agent swarm on it,
[03:45] in turn, of cost and also latency.
[03:48] So there are a bunch of solutions that we work on to enable this.
[03:52] I won't go into too much detail,
[03:54] but a lot of it surrounds the infra of generating the wikis,
[03:57] some of the user-level product stuff to enable deeper customization.
[04:02] One thing I will talk about here is the wiki algorithm
[04:04] that's more robust to the size of repos.
[04:06] So as it scales larger,
[04:07] you want your wiki to get larger and get deeper at the same time.
[04:13] Yeah, so on the other side, you want your wikis
[04:15] to have good quality.
[04:17] So I think it's always kind of like a little ill-defined
[04:21] of what makes a good wiki.
[04:25] But generally, you want it to have this focus.
[04:27] You want it to be not super bloated.
[04:29] And correctness is a thing that's also very hard to define,
[04:32] because it's kind of like--
[04:33] It's what's most useful to whoever is using this wiki.
[04:37] And I think Brace has already talked a bunch about the distinguishing
[04:40] between wikis for humans and wikis for agents.
[04:46] So something we actually noticed is that the hardest part of creating a wiki
[04:51] is actually the table of contents.
[04:53] And I'll explain why.
[04:54] So the table of contents, once you set it in stone,
[04:57] actually informs how you set up the rest of the wiki, what you're writing,
[05:00] how you're connecting the different pieces with code base.
[05:03] And in fact, I think a lot of the problems
[05:04] we saw with early iterations of our Wiki algorithm
[05:06] is that it's generating the wrong content page leads
[05:10] to a bad Wiki no matter how good your individual page
[05:13] writing is.
[05:14] And so a few elements go into this.
[05:16] Firstly, what are the key systems?
[05:18] And what are the things that people care about?
[05:20] And instead of coverage, you can't possibly cover everything
[05:23] in the entire code base.
[05:24] So what's important?
[05:25] What's not?
[05:26] What deserves to be covered?
[05:27] And the last thing that we always try to keep in mind
[05:29] is there's a lot of canonical terminology
[05:33] goes into a code base.
[05:35] And so if you notice that every deep wiki actually
[05:37] has a glossary section at the end.
[05:40] And it's useful both for agents and for humans.
[05:43] And once you have your table of contents,
[05:45] you actually are able to very easily fan out
[05:49] and write the parts of your wiki individually
[05:53] with this contextualization within the bigger artifact
[05:57] you're going to create later.
[05:59] And this allows you to do things like cross page links
[06:02] and also citations.
[06:07] So this is a general overview of how we actually build up the wiki.
[06:11] So first of all, we have a bunch of heuristics
[06:14] that we use to score files and file connections.
[06:18] And these incorporate a bunch of different features,
[06:21] like directory structure, a symbol graph,
[06:24] git history, like Brace was talking about,
[06:26] and even runtime data for when we have access to it.
[06:29] So the difference is instead of just letting
[06:32] an LLM kind of like drove through it,
[06:34] we want to actually quantify it in some way
[06:37] because we need to do this at scale.
[06:39] And so with this kind of information,
[06:42] we can now create different forms of codebase graphs.
[06:47] And we can then do a bunch of clustering
[06:49] and create the different systems that we're
[06:51] going to track in a wiki.
[06:53] So this quantification is meant to be kind of a first pass
[06:56] into what we see is what are the important systems in the repo,
[07:01] what do people care about, not just how the files are structured
[07:05] in the codebase.
[07:07] And then from there on, we write the table of contents,
[07:09] which we talked about earlier.
[07:10] And then we scale up to write the individual pages.
[07:17] So the codebase graph is--
[07:19] I'll just give you just as a cool example of how these graphs actually
[07:22] look.
[07:22] So this is the one I generated from the OpenWiki repo.
[07:27] And you see this is pretty reasonable.
[07:30] But once you get to bigger repos, like the entire LangChain repo,
[07:35] it's basically a good breakdown initial first pass
[07:38] for the agent to actually process in order to better inform
[07:43] how it structures its repo.
[07:48] And so now this is the core of our Wiki algorithm,
[07:52] But it has actually evolved a bunch over time.
[07:55] So we actually recently kind of upgraded our wiki algorithm
[07:59] from v1 to v2.
[08:02] So the interesting thing is that from--
[08:04] v1 was first created about over a year ago.
[08:08] And a lot of the constraints actually haven't changed.
[08:10] So things like model context limits,
[08:12] which is basically one of the biggest bottlenecks
[08:14] of creating any kind of Wiki style outputs.
[08:20] And things like, people still have budget constraints.
[08:23] They're very real.
[08:24] And when you're producing output,
[08:26] things like people's attention spans, which
[08:28] arguably may have gone down.
[08:29] But yeah.
[08:31] So the first initial implementation of Wiki
[08:34] was very orchestration-led.
[08:36] With weaker models, we used a lot of thinking
[08:39] about how to orchestrate these model calls,
[08:40] how to construct the context properly.
[08:43] And basically have very tight control
[08:45] over every kind of model call we're doing.
[08:47] But Wiki v2 decided to pass a lot of this thinking
[08:52] over to the agent.
[08:53] So it forms an agentic core.
[08:55] It uses the same scored and clustered graph as the first pass.
[08:59] And then now the agent is able to adapt to the code base
[09:02] when it sees abnormalities.
[09:05] So this extra scaffolding, so things like pulling extra clusters
[09:09] or scoring extra files, it becomes a tool
[09:12] that the agent actually calls when it needs it.
[09:15] So basically, the key takeaway here
[09:16] is that as the models improve, you
[09:18] want to focus less on doing the orchestrating of the agent
[09:21] at such a micro level.
[09:23] And you just really want to enable it
[09:25] with providing the right context.
[09:29] And I think a very natural question is,
[09:30] how do you know if a wiki is good enough?
[09:33] And I think this is a lot from the lens
[09:35] of a human readable wiki.
[09:38] So we have a bunch of quantitative measures that we use.
[09:42] So look at wiki health and quality.
[09:44] So this is a few examples.
[09:45] So based on our scoring, we have some notion of, well,
[09:49] we consider the top most active files
[09:51] and see that it's more covered in the wiki.
[09:54] We also look at the depth of citations
[09:57] and also the quality of citations.
[09:58] And one important thing is the correlation
[10:01] of the wiki size versus the repo size.
[10:04] We want it to be better because what we're noticing
[10:08] with our initial versions was that when
[10:09] you had a super huge repo, the wiki size would get capped.
[10:14] Yeah. And one other thing is the wiki size stays the same on average.
[10:21] So yeah, notice that I think V2 saw a big improvement with a more agentic core.
[10:26] But one interesting thing is that we're actually using basically the same set of models.
[10:30] We're upgrading the model versions that we're using in V1,
[10:34] but just changing this architecture to become more
[10:36] agentic as the capabilities progressed basically gave us this new quality.
[10:42] and also actually give us some cost savings as well,
[10:46] because using the agentic version allows for better
[10:51] cache performance and all that.
[10:53] And yeah, so basically, this more agentic thing
[10:56] is more adaptive to new repos.
[10:58] And the last metric that we're kind of also thinking about
[11:01] is like, is this actually valuable to the user?
[11:04] And that's ultimately the one that matters.
[11:06] So as part of our wiki evaluation,
[11:08] a lot of it is just working with the end user
[11:11] to see what works for them.
[11:15] And we worked with a lot of our biggest customers
[11:18] with on big code bases and some senior experience
[11:21] engineers who knew what they were looking for in their repo.
[11:24] And I think from this, we were able to tweak the algorithm
[11:28] to get the right structure that people were looking for.
[11:33] So now I want to shift gears a bit
[11:34] and talk a bit about how we're thinking about Wiki for agents
[11:39] or the idea of codebase intelligence in general
[11:41] and how it's going to progress in the future.
[11:46] And yeah, so I guess many of you have probably seen this long-running
[11:50] debate of rag versus agentic search.
[11:53] As someone who works a lot on DeepWiki,
[11:54] I'm a big believer in indexing and precomputation as a whole.
[11:59] And I've had Ask Devin users use both of these.
[12:01] So I don't think it's really a dichotomy
[12:04] that you have to choose one or the other.
[12:06] And in reality, I think as models get better and better,
[12:09] basically have more and more context to intelligently use.
[12:13] So for example, we have more user-defined knowledge,
[12:18] we now have these precomputed wikis,
[12:20] and there's a bunch of live data you can access now with MCPs and all that.
[12:23] All of this, I consider falls under the realm of agent search.
[12:28] Basically, any other context source that you can think of, you can add it in.
[12:31] The key is you want to frame it as you're
[12:33] augmenting your agent rather than replacing the work it would usually do.
[12:40] And yeah, so I want to go through a few key context principles that we try to think about
[12:46] at a high level of when working with context engineering.
[12:51] And so yeah, so these are four of them.
[12:54] The first one is this idea of primary sources.
[12:58] And so primary source is basically whatever you consider trustable and the ground truth.
[13:02] So in a code base, it would be basically code files.
[13:04] It would be a commit.
[13:06] it'll be like anything that is like, you know it be correct.
[13:11] And conversely, anything that you
[13:14] kind of like process through, like a Wiki, for example,
[13:17] is no longer a primary source.
[13:18] You can't derive it.
[13:19] And it leads to potential for error and unreliability.
[13:25] And that's why you don't want your agents
[13:26] to be kind of basing it off.
[13:28] Because what we noticed is that once you get more and more
[13:30] levels of summarization or rephrasing,
[13:36] And then a lot of the meaning gets lost.
[13:38] And then this leads to a lot more sources of error.
[13:40] And this very ties in with the second one, context-poisoning.
[13:43] You kind of want to make sure that everything you're giving
[13:45] is correct.
[13:47] And basically, I think when you're thinking
[13:48] of wikis for agents, often not putting something
[13:52] that is kind of incorrect is better than purring something
[13:58] that might kind of mislead the agent in the wrong path.
[14:02] Yeah.
[14:04] So the next two are the two ways I think about providing context
[14:10] in a way that improves agent.
[14:12] So first one is path compression.
[14:15] And the idea is that the agent could already
[14:19] kind of do this itself.
[14:20] Like it would take a few steps, maybe to a few grep searches,
[14:23] and find this piece of information you want to look for.
[14:26] But by kind of providing this information upfront,
[14:29] you kind of skip a few steps.
[14:31] You get to save context and tokens.
[14:34] And yeah, it probably improves costs.
[14:37] It may improve performance a little bit.
[14:40] But yeah, the agent probably could have done it on its own.
[14:43] So this is some example where context poisoning is a very
[14:46] real risk.
[14:47] If you point the wrong way, you're actually actively
[14:50] harming the performance of the agent.
[14:54] On the other hand, the other motive
[14:56] of this is something that the agent would not have found on its own.
[14:59] It could be a tiny piece of knowledge in your code base
[15:02] or elsewhere that you had no idea existed.
[15:04] It's this whole concept of unknown unknowns.
[15:06] And I think this is by far the biggest unsolved problem
[15:09] in terms of context engineering.
[15:11] I think a lot of this stuff is like,
[15:14] the agent will get it if you give it a little hint,
[15:17] give it a little pointer.
[15:18] But I think this is why not everything
[15:20] can be just agent driven.
[15:23] You can't just give it the tools and expect
[15:26] it to find everything out on its own.
[15:29] And that's why I think there's still
[15:30] a role for a lot of orchestration and human thinking
[15:33] involved in this.
[15:36] So yeah, I think in my view, context engineering and codebase intelligence
[15:41] is very far from solved.
[15:42] And it's something we're actively working on at Cognition
[15:45] and our coding agent, Devin.
[15:47] And the truth is that agents, I'm sure, as you all know,
[15:50] can already complete most coding tasks correctly,
[15:53] at least functionally correctly.
[15:55] But I think there's still a lot more
[15:57] we've done to become a good software engineer.
[16:00] So I think, for example, one of the evals
[16:02] we released recently, FrontierCode,
[16:05] is the idea is that it's not just like,
[16:07] is the task correct, but also does it write the code in a way
[16:10] that this very open source maintainer would accept in a PR?
[16:14] And the answer is no, even like Fable gets only like 50%
[16:18] in this eval.
[16:19] And I think, basically, in these cases,
[16:22] the information is there for the agent to get.
[16:25] It's able to infer codebase patterns.
[16:27] It's just not doing it yet.
[16:29] And I think there's a big role for wiki style or just
[16:34] pre-computation style solutions to unlock this.
[16:38] And then there's other forms of improvement,
[16:40] more user preference things, and also efficiency
[16:43] gains in general.
[16:45] And I believe that basically there's
[16:48] a lot more to be unlocked with context engineering
[16:51] and code bases and just improving codebase intelligence
[16:56] and there's something that we're actively working on
[16:59] and very excited to see where this goes.
[17:02] Thank you.
[17:03] (audience applauding)
[17:06] [MUSIC PLAYING]
