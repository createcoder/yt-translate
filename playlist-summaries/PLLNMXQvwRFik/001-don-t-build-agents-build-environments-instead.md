# Don't Build Agents, Build Environments Instead

- **Video:** https://www.youtube.com/watch?v=JolFqvXj3BE
- **Generated:** 2026-08-31 19:30 UTC
- **Status:** Transcript captured — summary unavailable

## Technical brief

The configured model endpoint did not return a response during this run. The complete timestamped source transcript is preserved below and is available in the website reader.

## Full transcript

[00:01] Today we're going to talk about how to
[00:02] Today we're going to talk about how to use modal as an agent sandbox which is
[00:04] use modal as an agent sandbox which is
[00:04] use modal as an agent sandbox which is increasingly like really important if
[00:06] increasingly like really important if
[00:06] increasingly like really important if you're building any kind of agentic
[00:07] you're building any kind of agentic
[00:08] you're building any kind of agentic workflow. And because of those things I
[00:09] workflow. And because of those things I
[00:09] workflow. And because of those things I mentioned the fact that developer
[00:11] mentioned the fact that developer
[00:11] mentioned the fact that developer experience is so good. It's so fast.
[00:13] experience is so good. It's so fast.
[00:13] experience is so good. It's so fast. It's easy to use. It makes a really good
[00:15] It's easy to use. It makes a really good
[00:15] It's easy to use. It makes a really good sandbox and you can use it for more than
[00:17] sandbox and you can use it for more than
[00:17] sandbox and you can use it for more than sandboxes. It just happens to be also a
[00:19] sandboxes. It just happens to be also a
[00:19] sandboxes. It just happens to be also a really good sandbox. Adam's here to talk
[00:20] really good sandbox. Adam's here to talk
[00:20] really good sandbox. Adam's here to talk about it to show you how you can use
[00:23] about it to show you how you can use
[00:23] about it to show you how you can use modal. So let's kick it off and hand it
[00:25] modal. So let's kick it off and hand it
[00:25] modal. So let's kick it off and hand it over to him. super excited to to talk a
[00:27] over to him. super excited to to talk a
[00:27] over to him. super excited to to talk a little bit about modal and really you
[00:29] little bit about modal and really you
[00:29] little bit about modal and really you know talk a little bit about the the
[00:31] know talk a little bit about the the
[00:31] know talk a little bit about the the difficulty in in building a system of
[00:34] difficulty in in building a system of
[00:34] difficulty in in building a system of you know letting agents build software
[00:36] you know letting agents build software
[00:36] you know letting agents build software for you. So this is this presentation is
[00:38] for you. So this is this presentation is
[00:38] for you. So this is this presentation is really going to be two parts. One of
[00:40] really going to be two parts. One of
[00:40] really going to be two parts. One of which is going to be you know kind of
[00:41] which is going to be you know kind of
[00:41] which is going to be you know kind of talking about you know how does somebody
[00:44] talking about you know how does somebody
[00:44] talking about you know how does somebody design a system for agents to be able to
[00:47] design a system for agents to be able to
[00:47] design a system for agents to be able to like reliably use their environments to
[00:49] like reliably use their environments to
[00:50] like reliably use their environments to actually go and build software. And then
[00:51] actually go and build software. And then
[00:51] actually go and build software. And then towards the end, we'll actually go and
[00:53] towards the end, we'll actually go and
[00:53] towards the end, we'll actually go and talk a little bit about what's the
[00:54] talk a little bit about what's the
[00:54] talk a little bit about what's the developer experience of building with
[00:56] developer experience of building with
[00:56] developer experience of building with this. And so we'll get into some code.
[00:57] this. And so we'll get into some code.
[00:57] this. And so we'll get into some code. Want to talk about the sort of real
[00:59] Want to talk about the sort of real
[00:59] Want to talk about the sort of real difficulty in building agents that can
[01:01] difficulty in building agents that can
[01:01] difficulty in building agents that can actually produce software. So before we
[01:03] actually produce software. So before we
[01:03] actually produce software. So before we get into this, uh my name is Adam and
[01:05] get into this, uh my name is Adam and
[01:05] get into this, uh my name is Adam and we're at a company called Modal. I've
[01:06] we're at a company called Modal. I've
[01:06] we're at a company called Modal. I've been at Modal for about 2 months now.
[01:08] been at Modal for about 2 months now.
[01:08] been at Modal for about 2 months now. I'm probably better known for the work
[01:10] I'm probably better known for the work
[01:10] I'm probably better known for the work that I've done as a maintainer of
[01:11] that I've done as a maintainer of
[01:11] that I've done as a maintainer of Prefect and at FastMPP. So if you built
[01:14] Prefect and at FastMPP. So if you built
[01:14] Prefect and at FastMPP. So if you built an MCP server have probably built it on
[01:16] an MCP server have probably built it on
[01:16] an MCP server have probably built it on FastMPP before. This talk is about how
[01:19] FastMPP before. This talk is about how
[01:19] FastMPP before. This talk is about how there's kind of a tends to be a lot of
[01:21] there's kind of a tends to be a lot of
[01:21] there's kind of a tends to be a lot of focus on agents where the environments
[01:23] focus on agents where the environments
[01:23] focus on agents where the environments that those agents live in tend to be a
[01:25] that those agents live in tend to be a
[01:25] that those agents live in tend to be a more sort of rich and interesting
[01:27] more sort of rich and interesting
[01:27] more sort of rich and interesting problem space and arguably a more
[01:29] problem space and arguably a more
[01:29] problem space and arguably a more important one. I wanted to call this
[01:30] important one. I wanted to call this
[01:30] important one. I wanted to call this talk environmental engineering 2011 or
[01:33] talk environmental engineering 2011 or
[01:33] talk environmental engineering 2011 or kind of the you know maybe the spicier
[01:34] kind of the you know maybe the spicier
[01:34] kind of the you know maybe the spicier take is that the hard part of the
[01:36] take is that the hard part of the
[01:36] take is that the hard part of the background agents is always the
[01:37] background agents is always the
[01:37] background agents is always the background part and not the agent part.
[01:39] background part and not the agent part.
[01:39] background part and not the agent part. I called it don't build agents, build
[01:41] I called it don't build agents, build
[01:41] I called it don't build agents, build environments instead really as an homage
[01:43] environments instead really as an homage
[01:43] environments instead really as an homage to one of my favorite talks that I would
[01:45] to one of my favorite talks that I would
[01:45] to one of my favorite talks that I would encourage everybody to go and watch. And
[01:46] encourage everybody to go and watch. And
[01:46] encourage everybody to go and watch. And that talk was by Barry and Mahesh at
[01:49] that talk was by Barry and Mahesh at
[01:49] that talk was by Barry and Mahesh at Anthropic that gave a similar talk
[01:51] Anthropic that gave a similar talk
[01:51] Anthropic that gave a similar talk called don't build agents, build skills
[01:52] called don't build agents, build skills
[01:52] called don't build agents, build skills instead. And this talk done every single
[01:55] instead. And this talk done every single
[01:55] instead. And this talk done every single number you can imagine on YouTube. But
[01:57] number you can imagine on YouTube. But
[01:57] number you can imagine on YouTube. But the central argument of their talk and
[01:59] the central argument of their talk and
[01:59] the central argument of their talk and why do I appreciate this framing so
[02:01] why do I appreciate this framing so
[02:01] why do I appreciate this framing so much? Agents have really converged on a
[02:03] much? Agents have really converged on a
[02:03] much? Agents have really converged on a pretty universal design. I'm sure that
[02:05] pretty universal design. I'm sure that
[02:05] pretty universal design. I'm sure that maybe this is a controversial take
[02:06] maybe this is a controversial take
[02:06] maybe this is a controversial take depending on the talks that have led up
[02:08] depending on the talks that have led up
[02:08] depending on the talks that have led up into this as I'm sure as folks here that
[02:09] into this as I'm sure as folks here that
[02:09] into this as I'm sure as folks here that have built with agents have felt as you
[02:11] have built with agents have felt as you
[02:11] have built with agents have felt as you use something like the codeex harness or
[02:13] use something like the codeex harness or
[02:13] use something like the codeex harness or maybe claude code or use pi or Hermes
[02:17] maybe claude code or use pi or Hermes
[02:17] maybe claude code or use pi or Hermes you'll notice that a lot of these agents
[02:18] you'll notice that a lot of these agents
[02:18] you'll notice that a lot of these agents you know have some pretty common
[02:19] you know have some pretty common
[02:19] you know have some pretty common primitives to them it's how do I do
[02:21] primitives to them it's how do I do
[02:21] primitives to them it's how do I do compaction when a conversation gets too
[02:23] compaction when a conversation gets too
[02:23] compaction when a conversation gets too long related how do I do memory but a
[02:25] long related how do I do memory but a
[02:25] long related how do I do memory but a lot of their tools are pretty much can
[02:27] lot of their tools are pretty much can
[02:27] lot of their tools are pretty much can feel the same it's you know how do I go
[02:29] feel the same it's you know how do I go
[02:29] feel the same it's you know how do I go and execute bash commands you know how
[02:31] and execute bash commands you know how
[02:32] and execute bash commands you know how do I go read files write files edit
[02:34] do I go read files write files edit
[02:34] do I go read files write files edit files. And so the argument that
[02:36] files. And so the argument that
[02:36] files. And so the argument that Enthropic made the knowledge cut off of
[02:38] Enthropic made the knowledge cut off of
[02:38] Enthropic made the knowledge cut off of October 2025 was we've really coalesed
[02:41] October 2025 was we've really coalesed
[02:41] October 2025 was we've really coalesed on a common agent design. And so really
[02:43] on a common agent design. And so really
[02:44] on a common agent design. And so really the hardest part that we keep coming
[02:46] the hardest part that we keep coming
[02:46] the hardest part that we keep coming across is like how to imbue these agents
[02:47] across is like how to imbue these agents
[02:48] across is like how to imbue these agents with expertise. And their argument at
[02:49] with expertise. And their argument at
[02:50] with expertise. And their argument at the time was that skills were the best
[02:51] the time was that skills were the best
[02:51] the time was that skills were the best vehicle for imbuing an agent with that
[02:53] vehicle for imbuing an agent with that
[02:53] vehicle for imbuing an agent with that expertise. And so that sort of explains
[02:55] expertise. And so that sort of explains
[02:55] expertise. And so that sort of explains why, you know, as you see a lot of folks
[02:56] why, you know, as you see a lot of folks
[02:56] why, you know, as you see a lot of folks design agents, a lot of it is like,
[02:58] design agents, a lot of it is like,
[02:58] design agents, a lot of it is like, yeah, yeah, yeah, go buy whatever the
[02:59] yeah, yeah, yeah, go buy whatever the
[02:59] yeah, yeah, yeah, go buy whatever the agent harness is. The recipe for
[03:01] agent harness is. The recipe for
[03:01] agent harness is. The recipe for designing an agent always starts with,
[03:03] designing an agent always starts with,
[03:03] designing an agent always starts with, you know, go pick a harness and then
[03:05] you know, go pick a harness and then
[03:05] you know, go pick a harness and then let's go obsess over the context that we
[03:07] let's go obsess over the context that we
[03:07] let's go obsess over the context that we go and give that agent. And so there are
[03:10] go and give that agent. And so there are
[03:10] go and give that agent. And so there are obvious corner cases here that that we
[03:12] obvious corner cases here that that we
[03:12] obvious corner cases here that that we could obsess over. But I would say that
[03:13] could obsess over. But I would say that
[03:13] could obsess over. But I would say that broadly a lot of their predictions about
[03:16] broadly a lot of their predictions about
[03:16] broadly a lot of their predictions about businesses should obsess over providing
[03:18] businesses should obsess over providing
[03:18] businesses should obsess over providing context to agents and maybe not
[03:19] context to agents and maybe not
[03:19] context to agents and maybe not redesigning every harness has largely
[03:21] redesigning every harness has largely
[03:21] redesigning every harness has largely borne out. So this talk as an homage is
[03:23] borne out. So this talk as an homage is
[03:24] borne out. So this talk as an homage is I have the same feeling that's sort of
[03:26] I have the same feeling that's sort of
[03:26] I have the same feeling that's sort of borne out by working with uh dozens of
[03:28] borne out by working with uh dozens of
[03:28] borne out by working with uh dozens of companies who are building their own
[03:29] companies who are building their own
[03:29] companies who are building their own background agents that background agents
[03:31] background agents that background agents
[03:31] background agents that background agents are similarly converging on a pretty
[03:33] are similarly converging on a pretty
[03:33] are similarly converging on a pretty universal system architecture. And so
[03:35] universal system architecture. And so
[03:35] universal system architecture. And so this is kind of one layer up from a
[03:37] this is kind of one layer up from a
[03:37] this is kind of one layer up from a harness which is harness is really like
[03:39] harness which is harness is really like
[03:39] harness which is harness is really like what is the individual agent doing. And
[03:41] what is the individual agent doing. And
[03:42] what is the individual agent doing. And as you're trying to design a system
[03:44] as you're trying to design a system
[03:44] as you're trying to design a system where those agents operate they all have
[03:46] where those agents operate they all have
[03:46] where those agents operate they all have a pretty similar architecture to them.
[03:47] a pretty similar architecture to them.
[03:48] a pretty similar architecture to them. And so what are the hardest and most
[03:49] And so what are the hardest and most
[03:49] And so what are the hardest and most reinvented parts here? what are the
[03:51] reinvented parts here? what are the
[03:51] reinvented parts here? what are the things that we really need to be
[03:52] things that we really need to be
[03:52] things that we really need to be obsessing over which is really about you
[03:54] obsessing over which is really about you
[03:54] obsessing over which is really about you know how do you go and build what I call
[03:55] know how do you go and build what I call
[03:55] know how do you go and build what I call dev boxes for agents and then how do you
[03:57] dev boxes for agents and then how do you
[03:57] dev boxes for agents and then how do you think about orchestrating them as they
[03:59] think about orchestrating them as they
[03:59] think about orchestrating them as they complete their work and so this is of
[04:01] complete their work and so this is of
[04:01] complete their work and so this is of course you know cut off of the last few
[04:04] course you know cut off of the last few
[04:04] course you know cut off of the last few weeks and so I imagine that this will be
[04:07] weeks and so I imagine that this will be
[04:07] weeks and so I imagine that this will be there's some depreciating knowledge here
[04:08] there's some depreciating knowledge here
[04:08] there's some depreciating knowledge here but I do expect this to continue to bear
[04:10] but I do expect this to continue to bear
[04:10] but I do expect this to continue to bear out so I want to talk about these two
[04:12] out so I want to talk about these two
[04:12] out so I want to talk about these two problems so this is going to be a bit of
[04:14] problems so this is going to be a bit of
[04:14] problems so this is going to be a bit of a systems talk and then we're going to
[04:15] a systems talk and then we're going to
[04:15] a systems talk and then we're going to go into like what's the actual code of
[04:17] go into like what's the actual code of
[04:17] go into like what's the actual code of writing with modal actually look like so
[04:18] writing with modal actually look like so
[04:18] writing with modal actually look like so to sort of appreciate this I wanted to
[04:20] to sort of appreciate this I wanted to
[04:20] to sort of appreciate this I wanted to give an a bridged history of background
[04:22] give an a bridged history of background
[04:22] give an a bridged history of background agents. I'm going to skip over the
[04:24] agents. I'm going to skip over the
[04:24] agents. I'm going to skip over the creation which starts with Devon. I feel
[04:26] creation which starts with Devon. I feel
[04:26] creation which starts with Devon. I feel like Devon was just years ahead of all
[04:28] like Devon was just years ahead of all
[04:28] like Devon was just years ahead of all of this. And so I'm going to skip past
[04:29] of this. And so I'm going to skip past
[04:29] of this. And so I'm going to skip past this history and I'm going to skip
[04:31] this history and I'm going to skip
[04:31] this history and I'm going to skip towards maybe beginning of 2025. And so
[04:33] towards maybe beginning of 2025. And so
[04:33] towards maybe beginning of 2025. And so I'm sure what a lot of folks in this
[04:35] I'm sure what a lot of folks in this
[04:35] I'm sure what a lot of folks in this room have felt pretty similarly. Maybe
[04:36] room have felt pretty similarly. Maybe
[04:36] room have felt pretty similarly. Maybe you can imagine yourself back in the day
[04:38] you can imagine yourself back in the day
[04:38] you can imagine yourself back in the day where a lot of this started with maybe
[04:40] where a lot of this started with maybe
[04:40] where a lot of this started with maybe goose by block was actually earlier than
[04:42] goose by block was actually earlier than
[04:42] goose by block was actually earlier than cloud code. But it really started off
[04:44] cloud code. But it really started off
[04:44] cloud code. But it really started off with all of us kind of pair programming
[04:46] with all of us kind of pair programming
[04:46] with all of us kind of pair programming with these harnesses because they
[04:48] with these harnesses because they
[04:48] with these harnesses because they weren't particularly smart, but it was
[04:49] weren't particularly smart, but it was
[04:49] weren't particularly smart, but it was still magic enough to where you could
[04:51] still magic enough to where you could
[04:51] still magic enough to where you could actually it was a step up from tab
[04:53] actually it was a step up from tab
[04:53] actually it was a step up from tab complete from like the ide of the day.
[04:54] complete from like the ide of the day.
[04:54] complete from like the ide of the day. With the release of sonnet 4, I think we
[04:56] With the release of sonnet 4, I think we
[04:56] With the release of sonnet 4, I think we all sort of collectively felt like these
[04:58] all sort of collectively felt like these
[04:58] all sort of collectively felt like these things were good enough to walk away
[04:59] things were good enough to walk away
[05:00] things were good enough to walk away from. And then now that they were good
[05:01] from. And then now that they were good
[05:01] from. And then now that they were good enough to walk away from, there was this
[05:03] enough to walk away from, there was this
[05:03] enough to walk away from, there was this collective desire of, well great, now
[05:04] collective desire of, well great, now
[05:04] collective desire of, well great, now these things can execute asynchronously
[05:07] these things can execute asynchronously
[05:07] these things can execute asynchronously in the background. They were all sharing
[05:09] in the background. They were all sharing
[05:09] in the background. They were all sharing me and my laptop. And so now I have to
[05:12] me and my laptop. And so now I have to
[05:12] me and my laptop. And so now I have to figure out how to to check back in with
[05:14] figure out how to to check back in with
[05:14] figure out how to to check back in with them, how to keep myself in the loop
[05:15] them, how to keep myself in the loop
[05:16] them, how to keep myself in the loop when necessary, and I have to figure out
[05:18] when necessary, and I have to figure out
[05:18] when necessary, and I have to figure out to give them their own machines. So
[05:19] to give them their own machines. So
[05:19] to give them their own machines. So we're going to talk about why giving
[05:20] we're going to talk about why giving
[05:20] we're going to talk about why giving them their own machines tends to be a
[05:22] them their own machines tends to be a
[05:22] them their own machines tends to be a kind of a hard problem in practice. It
[05:24] kind of a hard problem in practice. It
[05:24] kind of a hard problem in practice. It sounds very straightforward, but it
[05:25] sounds very straightforward, but it
[05:25] sounds very straightforward, but it tends to be hard in practice. So spent a
[05:27] tends to be hard in practice. So spent a
[05:27] tends to be hard in practice. So spent a lot of time to actually background them.
[05:29] lot of time to actually background them.
[05:29] lot of time to actually background them. This is where you started seeing you
[05:31] This is where you started seeing you
[05:31] This is where you started seeing you know managed offerings from things like
[05:32] know managed offerings from things like
[05:32] know managed offerings from things like cloud code or codeex that were basically
[05:35] cloud code or codeex that were basically
[05:35] cloud code or codeex that were basically like you were using cloud code in your
[05:37] like you were using cloud code in your
[05:37] like you were using cloud code in your terminal. Now you can like click around
[05:39] terminal. Now you can like click around
[05:39] terminal. Now you can like click around and you can try and get approximately a
[05:41] and you can try and get approximately a
[05:41] and you can try and get approximately a cloud code experience in a UI. I would
[05:44] cloud code experience in a UI. I would
[05:44] cloud code experience in a UI. I would say that where I think we really saw the
[05:46] say that where I think we really saw the
[05:46] say that where I think we really saw the real success of background agents is
[05:48] real success of background agents is
[05:48] real success of background agents is through folks like ramp stripe works and
[05:51] through folks like ramp stripe works and
[05:51] through folks like ramp stripe works and others who really kind of like led open
[05:54] others who really kind of like led open
[05:54] others who really kind of like led open architectures of how folks of how they
[05:56] architectures of how folks of how they
[05:56] architectures of how folks of how they built their own background agents. And
[05:57] built their own background agents. And
[05:58] built their own background agents. And so I want to talk a little bit about
[05:59] so I want to talk a little bit about
[05:59] so I want to talk a little bit about what's in common between those
[06:00] what's in common between those
[06:00] what's in common between those architectures and where some of the
[06:02] architectures and where some of the
[06:02] architectures and where some of the actual difficulties go. So that if
[06:04] actual difficulties go. So that if
[06:04] actual difficulties go. So that if you're somebody today who's using cloud
[06:05] you're somebody today who's using cloud
[06:05] you're somebody today who's using cloud code on a laptop, you know, how do you
[06:07] code on a laptop, you know, how do you
[06:07] code on a laptop, you know, how do you get that off your laptop? And then, you
[06:09] get that off your laptop? And then, you
[06:09] get that off your laptop? And then, you know, how do you get many of these
[06:10] know, how do you get many of these
[06:10] know, how do you get many of these things to do work on your behalf in
[06:11] things to do work on your behalf in
[06:11] things to do work on your behalf in parallel? So there are sort of like two
[06:13] parallel? So there are sort of like two
[06:14] parallel? So there are sort of like two real challenges here. And I'm going to
[06:15] real challenges here. And I'm going to
[06:15] real challenges here. And I'm going to explain some of the jargon here in a
[06:17] explain some of the jargon here in a
[06:17] explain some of the jargon here in a second, but I'd say that there's two
[06:18] second, but I'd say that there's two
[06:18] second, but I'd say that there's two real challenges. And one of them is
[06:20] real challenges. And one of them is
[06:20] real challenges. And one of them is designing a system that generates dev
[06:22] designing a system that generates dev
[06:22] designing a system that generates dev boxes on demand. I know that a lot of
[06:23] boxes on demand. I know that a lot of
[06:24] boxes on demand. I know that a lot of the setup for for this talk is around
[06:25] the setup for for this talk is around
[06:25] the setup for for this talk is around sandboxes and I'm using the word devbox
[06:27] sandboxes and I'm using the word devbox
[06:28] sandboxes and I'm using the word devbox here pretty intentionally where you know
[06:30] here pretty intentionally where you know
[06:30] here pretty intentionally where you know a sandbox tends to be something that's
[06:32] a sandbox tends to be something that's
[06:32] a sandbox tends to be something that's pretty bare. It is like let me go spin
[06:34] pretty bare. It is like let me go spin
[06:34] pretty bare. It is like let me go spin up a Linux machine on demand that has
[06:37] up a Linux machine on demand that has
[06:37] up a Linux machine on demand that has pretty much nothing attached to it. I'm
[06:38] pretty much nothing attached to it. I'm
[06:38] pretty much nothing attached to it. I'm going to go use that to run untrusted
[06:40] going to go use that to run untrusted
[06:40] going to go use that to run untrusted code. And where I want to upgrade our
[06:42] code. And where I want to upgrade our
[06:42] code. And where I want to upgrade our terminology here to dev boxes is around
[06:45] terminology here to dev boxes is around
[06:45] terminology here to dev boxes is around like what do I do when I want to run or
[06:47] like what do I do when I want to run or
[06:47] like what do I do when I want to run or build untrusted software. And so, you
[06:49] build untrusted software. And so, you
[06:49] build untrusted software. And so, you know, a sandbox is if I give an agent a
[06:52] know, a sandbox is if I give an agent a
[06:52] know, a sandbox is if I give an agent a task to go go build me a a front end
[06:56] task to go go build me a a front end
[06:56] task to go go build me a a front end like, you know, your hello world next.js
[06:58] like, you know, your hello world next.js
[06:58] like, you know, your hello world next.js app. If I give it a sandbox that doesn't
[07:00] app. If I give it a sandbox that doesn't
[07:00] app. If I give it a sandbox that doesn't have any like ports open on it or
[07:01] have any like ports open on it or
[07:01] have any like ports open on it or anything like this, it's going to be
[07:02] anything like this, it's going to be
[07:02] anything like this, it's going to be unable to like actually up its own
[07:04] unable to like actually up its own
[07:04] unable to like actually up its own server if it doesn't actually have
[07:06] server if it doesn't actually have
[07:06] server if it doesn't actually have access to, you know, CLI tools to take
[07:09] access to, you know, CLI tools to take
[07:09] access to, you know, CLI tools to take screenshots. It's not going to be able
[07:10] screenshots. It's not going to be able
[07:10] screenshots. It's not going to be able to take screenshots of that app. It's
[07:12] to take screenshots of that app. It's
[07:12] to take screenshots of that app. It's not going to be able to see its own
[07:13] not going to be able to see its own
[07:13] not going to be able to see its own progress, like visually inspect its own
[07:16] progress, like visually inspect its own
[07:16] progress, like visually inspect its own work. And so we can see that there's a
[07:18] work. And so we can see that there's a
[07:18] work. And so we can see that there's a lot of things you're not able to do just
[07:19] lot of things you're not able to do just
[07:20] lot of things you're not able to do just on a bare Linux machine. As you try to
[07:22] on a bare Linux machine. As you try to
[07:22] on a bare Linux machine. As you try to give agents more complex tasks that
[07:24] give agents more complex tasks that
[07:24] give agents more complex tasks that aren't just software engineering tasks,
[07:26] aren't just software engineering tasks,
[07:26] aren't just software engineering tasks, maybe they start resembling data or
[07:28] maybe they start resembling data or
[07:28] maybe they start resembling data or machine learning tasks. In the machine
[07:30] machine learning tasks. In the machine
[07:30] machine learning tasks. In the machine learning case, now you're going to want
[07:32] learning case, now you're going to want
[07:32] learning case, now you're going to want it to like I've got a model that's not
[07:33] it to like I've got a model that's not
[07:34] it to like I've got a model that's not performing very well. I might want to
[07:35] performing very well. I might want to
[07:35] performing very well. I might want to retrain this. Maybe I'm serving a model
[07:37] retrain this. Maybe I'm serving a model
[07:37] retrain this. Maybe I'm serving a model and I'm noticing that I'm not getting
[07:39] and I'm noticing that I'm not getting
[07:39] and I'm noticing that I'm not getting very good throughput. So now I actually
[07:41] very good throughput. So now I actually
[07:41] very good throughput. So now I actually want to like go inspect it and profile
[07:43] want to like go inspect it and profile
[07:43] want to like go inspect it and profile it on a GPU. if I go give it a sandbox
[07:46] it on a GPU. if I go give it a sandbox
[07:46] it on a GPU. if I go give it a sandbox that doesn't have access to that
[07:47] that doesn't have access to that
[07:47] that doesn't have access to that hardware. Again, now I'm dooming an
[07:49] hardware. Again, now I'm dooming an
[07:49] hardware. Again, now I'm dooming an agent to go try to solve a problem
[07:51] agent to go try to solve a problem
[07:51] agent to go try to solve a problem without a machine that's not prepped to
[07:53] without a machine that's not prepped to
[07:53] without a machine that's not prepped to actually go and solve it. And so
[07:55] actually go and solve it. And so
[07:55] actually go and solve it. And so designing a system that actually
[07:56] designing a system that actually
[07:56] designing a system that actually generates these dev boxes on demand in a
[07:59] generates these dev boxes on demand in a
[07:59] generates these dev boxes on demand in a way that doesn't make you want to tear
[08:00] way that doesn't make you want to tear
[08:00] way that doesn't make you want to tear your hair out as an end user tends to be
[08:02] your hair out as an end user tends to be
[08:02] your hair out as an end user tends to be a really hard system problem. And the
[08:04] a really hard system problem. And the
[08:04] a really hard system problem. And the second piece which is get into of where
[08:07] second piece which is get into of where
[08:07] second piece which is get into of where is kind of that line between your
[08:08] is kind of that line between your
[08:08] is kind of that line between your control plane and your data plane. I
[08:09] control plane and your data plane. I
[08:09] control plane and your data plane. I think that this second point was
[08:11] think that this second point was
[08:11] think that this second point was slightly more controversial. I would say
[08:12] slightly more controversial. I would say
[08:12] slightly more controversial. I would say the last 72 hours of Twitter makes me
[08:14] the last 72 hours of Twitter makes me
[08:14] the last 72 hours of Twitter makes me feel like this is now kind of a vanilla
[08:16] feel like this is now kind of a vanilla
[08:16] feel like this is now kind of a vanilla point, but we'll get into it
[08:17] point, but we'll get into it
[08:17] point, but we'll get into it nonetheless. Designing a system that
[08:19] nonetheless. Designing a system that
[08:19] nonetheless. Designing a system that generates these dev boxes or sandboxes
[08:21] generates these dev boxes or sandboxes
[08:21] generates these dev boxes or sandboxes on demand. I think that it's fair for
[08:22] on demand. I think that it's fair for
[08:22] on demand. I think that it's fair for folks to point out that this isn't a
[08:24] folks to point out that this isn't a
[08:24] folks to point out that this isn't a particularly new problem. If you've been
[08:25] particularly new problem. If you've been
[08:25] particularly new problem. If you've been doing test-driven development for a
[08:27] doing test-driven development for a
[08:27] doing test-driven development for a while, the idea of generating machines
[08:29] while, the idea of generating machines
[08:29] while, the idea of generating machines to go stand up, you know, environments
[08:31] to go stand up, you know, environments
[08:31] to go stand up, you know, environments that feels like a thing that we've been
[08:33] that feels like a thing that we've been
[08:33] that feels like a thing that we've been working on for a long time, right? Like
[08:34] working on for a long time, right? Like
[08:34] working on for a long time, right? Like you have your GitHub runners, you're
[08:36] you have your GitHub runners, you're
[08:36] you have your GitHub runners, you're going upping your Docker Compose, and
[08:37] going upping your Docker Compose, and
[08:37] going upping your Docker Compose, and then you're actually running tests on
[08:39] then you're actually running tests on
[08:39] then you're actually running tests on that. And so I think it's a fair
[08:40] that. And so I think it's a fair
[08:40] that. And so I think it's a fair criticism. I'll just say that it's so
[08:42] criticism. I'll just say that it's so
[08:42] criticism. I'll just say that it's so it's not necessarily a new problem. It's
[08:43] it's not necessarily a new problem. It's
[08:43] it's not necessarily a new problem. It's just something that requires a new
[08:45] just something that requires a new
[08:45] just something that requires a new solution because we have a lot of
[08:46] solution because we have a lot of
[08:46] solution because we have a lot of different constraints and getting this
[08:47] different constraints and getting this
[08:47] different constraints and getting this to work for a whole new set of
[08:49] to work for a whole new set of
[08:49] to work for a whole new set of constraints without even that bare
[08:51] constraints without even that bare
[08:51] constraints without even that bare problem solved sort of just throws us
[08:53] problem solved sort of just throws us
[08:53] problem solved sort of just throws us back into the deep end. And so I would
[08:54] back into the deep end. And so I would
[08:54] back into the deep end. And so I would say like the first reason why that might
[08:57] say like the first reason why that might
[08:57] say like the first reason why that might not be obvious about why this is a
[08:58] not be obvious about why this is a
[08:58] not be obvious about why this is a harder problem is I think we like to
[09:00] harder problem is I think we like to
[09:00] harder problem is I think we like to think a lot about CI/CD in terms of
[09:02] think a lot about CI/CD in terms of
[09:02] think a lot about CI/CD in terms of jobs. You know, we have this really
[09:04] jobs. You know, we have this really
[09:04] jobs. You know, we have this really happy path of first it's going to clone.
[09:07] happy path of first it's going to clone.
[09:07] happy path of first it's going to clone. It's going to assume that that is the
[09:09] It's going to assume that that is the
[09:09] It's going to assume that that is the state of the world that that repo is
[09:11] state of the world that that repo is
[09:11] state of the world that that repo is exactly what you want to test against,
[09:13] exactly what you want to test against,
[09:13] exactly what you want to test against, which is fine. And then it's going to
[09:14] which is fine. And then it's going to
[09:14] which is fine. And then it's going to run your test, your deterministic test
[09:16] run your test, your deterministic test
[09:16] run your test, your deterministic test start to end, and then it's going to
[09:18] start to end, and then it's going to
[09:18] start to end, and then it's going to tell you whether or not things succeeded
[09:19] tell you whether or not things succeeded
[09:19] tell you whether or not things succeeded or failed. For dev boxes, for agents,
[09:21] or failed. For dev boxes, for agents,
[09:21] or failed. For dev boxes, for agents, it's a totally different story where you
[09:23] it's a totally different story where you
[09:23] it's a totally different story where you have to go spin up a machine and then
[09:25] have to go spin up a machine and then
[09:25] have to go spin up a machine and then it's going to go do work for a while.
[09:27] it's going to go do work for a while.
[09:27] it's going to go do work for a while. It's going to come back to you and ask
[09:28] It's going to come back to you and ask
[09:28] It's going to come back to you and ask you for input. by the time that you
[09:30] you for input. by the time that you
[09:30] you for input. by the time that you respond to it, like somebody asks you
[09:31] respond to it, like somebody asks you
[09:31] respond to it, like somebody asks you for feedback on a PR and you don't get
[09:33] for feedback on a PR and you don't get
[09:33] for feedback on a PR and you don't get to it for a few days, we're not going to
[09:35] to it for a few days, we're not going to
[09:35] to it for a few days, we're not going to keep a machine running for a few days.
[09:36] keep a machine running for a few days.
[09:36] keep a machine running for a few days. And so now we have this notion of like
[09:38] And so now we have this notion of like
[09:38] And so now we have this notion of like how do we have longunning or resumable
[09:41] how do we have longunning or resumable
[09:41] how do we have longunning or resumable sessions that need to potentially even
[09:44] sessions that need to potentially even
[09:44] sessions that need to potentially even outlive the runtime of the box itself.
[09:47] outlive the runtime of the box itself.
[09:47] outlive the runtime of the box itself. And so when you start thinking about
[09:48] And so when you start thinking about
[09:48] And so when you start thinking about sessions over jobs, it starts meaning
[09:51] sessions over jobs, it starts meaning
[09:51] sessions over jobs, it starts meaning that you have to think about how to
[09:53] that you have to think about how to
[09:53] that you have to think about how to persist the state of a machine. And so
[09:56] persist the state of a machine. And so
[09:56] persist the state of a machine. And so that means thinking about, you know, how
[09:57] that means thinking about, you know, how
[09:57] that means thinking about, you know, how do you snapshot the memory of a process
[10:01] do you snapshot the memory of a process
[10:01] do you snapshot the memory of a process in a sandbox or a dev box so that you
[10:03] in a sandbox or a dev box so that you
[10:03] in a sandbox or a dev box so that you know when you resume it, you can resume
[10:05] know when you resume it, you can resume
[10:05] know when you resume it, you can resume it from its like midthought from an
[10:07] it from its like midthought from an
[10:07] it from its like midthought from an agent or maybe mid-process if your
[10:09] agent or maybe mid-process if your
[10:09] agent or maybe mid-process if your agent's executing something or maybe
[10:11] agent's executing something or maybe
[10:11] agent's executing something or maybe your system is best represented by its
[10:13] your system is best represented by its
[10:13] your system is best represented by its file system. And so it's great, it
[10:15] file system. And so it's great, it
[10:15] file system. And so it's great, it created an next.j.j.j.j.j.j.j.j.j.j.js
[10:16] created an next.j.j.j.j.j.j.j.j.j.j.js
[10:16] created an next.j.j.j.j.j.j.j.j.j.j.js app. It compiled it and then it asked me
[10:18] app. It compiled it and then it asked me
[10:18] app. It compiled it and then it asked me for feedback on it a few days later. So,
[10:20] for feedback on it a few days later. So,
[10:20] for feedback on it a few days later. So, what I'm going to do is I'm going to try
[10:21] what I'm going to do is I'm going to try
[10:22] what I'm going to do is I'm going to try and snapshot that sandbox before I throw
[10:24] and snapshot that sandbox before I throw
[10:24] and snapshot that sandbox before I throw it away. And then when I interact it
[10:26] it away. And then when I interact it
[10:26] it away. And then when I interact it with it next, I need to be able to
[10:28] with it next, I need to be able to
[10:28] with it next, I need to be able to essentially spin up a new machine, mount
[10:30] essentially spin up a new machine, mount
[10:30] essentially spin up a new machine, mount that file system in a way that it feels
[10:31] that file system in a way that it feels
[10:32] that file system in a way that it feels like I'm interacting with the thing that
[10:33] like I'm interacting with the thing that
[10:33] like I'm interacting with the thing that I put to sleep a few days ago.
[10:34] I put to sleep a few days ago.
[10:34] I put to sleep a few days ago. &gt;&gt; The one thing I hate about CI/CD also is
[10:36] &gt;&gt; The one thing I hate about CI/CD also is
[10:36] &gt;&gt; The one thing I hate about CI/CD also is the feedback loops take so long. Let's
[10:39] the feedback loops take so long. Let's
[10:39] the feedback loops take so long. Let's say in the fourth step of your CI/CD,
[10:41] say in the fourth step of your CI/CD,
[10:41] say in the fourth step of your CI/CD, something some dependency is missing.
[10:43] something some dependency is missing.
[10:43] something some dependency is missing. Then you like often times fiddle with
[10:44] Then you like often times fiddle with
[10:44] Then you like often times fiddle with that step. You're like, "Oh, let me add
[10:46] that step. You're like, "Oh, let me add
[10:46] that step. You're like, "Oh, let me add it." And you run the whole damn thing
[10:47] it." And you run the whole damn thing
[10:47] it." And you run the whole damn thing over again. It doesn't feel like this is
[10:49] over again. It doesn't feel like this is
[10:49] over again. It doesn't feel like this is a nightmare. You really want like a dev
[10:51] a nightmare. You really want like a dev
[10:51] a nightmare. You really want like a dev box where you can just do stuff like you
[10:53] box where you can just do stuff like you
[10:53] box where you can just do stuff like you might not know what the answer is
[10:54] might not know what the answer is
[10:54] might not know what the answer is perfectly.
[10:55] perfectly.
[10:55] perfectly. &gt;&gt; So jobs versus sessions I feel like are
[10:57] &gt;&gt; So jobs versus sessions I feel like are
[10:57] &gt;&gt; So jobs versus sessions I feel like are maybe the first unintuitive thing when
[10:59] maybe the first unintuitive thing when
[10:59] maybe the first unintuitive thing when you're trying to think about like you
[11:00] you're trying to think about like you
[11:00] you're trying to think about like you know environmental engineering like why
[11:02] know environmental engineering like why
[11:02] know environmental engineering like why is this a new problem for agents
[11:04] is this a new problem for agents
[11:04] is this a new problem for agents sometimes it feels like when we talk
[11:06] sometimes it feels like when we talk
[11:06] sometimes it feels like when we talk about things for agents we feel like to
[11:08] about things for agents we feel like to
[11:08] about things for agents we feel like to rebrand or invent new problems just so
[11:10] rebrand or invent new problems just so
[11:10] rebrand or invent new problems just so that they feel new. So I'm just very
[11:12] that they feel new. So I'm just very
[11:12] that they feel new. So I'm just very cautious sometimes of being like all
[11:14] cautious sometimes of being like all
[11:14] cautious sometimes of being like all right from first principles why is
[11:16] right from first principles why is
[11:16] right from first principles why is designing an environment for an agent
[11:18] designing an environment for an agent
[11:18] designing an environment for an agent actually distinct from a lot of the hard
[11:21] actually distinct from a lot of the hard
[11:21] actually distinct from a lot of the hard system engineering of designing
[11:23] system engineering of designing
[11:23] system engineering of designing environments for CI/CD and I think one
[11:25] environments for CI/CD and I think one
[11:25] environments for CI/CD and I think one of this is the constraints of a job
[11:26] of this is the constraints of a job
[11:26] of this is the constraints of a job versus a session. The second one is
[11:28] versus a session. The second one is
[11:28] versus a session. The second one is really that you know kind of related to
[11:30] really that you know kind of related to
[11:30] really that you know kind of related to this to the notion of a session is the
[11:32] this to the notion of a session is the
[11:32] this to the notion of a session is the environment really is alive. So often if
[11:34] environment really is alive. So often if
[11:34] environment really is alive. So often if you have you'll have an agent that
[11:36] you have you'll have an agent that
[11:36] you have you'll have an agent that checks out a repo goes and does some
[11:38] checks out a repo goes and does some
[11:38] checks out a repo goes and does some work by the time you come back to it the
[11:40] work by the time you come back to it the
[11:40] work by the time you come back to it the underlying repo may have changed and so
[11:42] underlying repo may have changed and so
[11:42] underlying repo may have changed and so like how do you actually give an agent
[11:44] like how do you actually give an agent
[11:44] like how do you actually give an agent the ability to reync its environment
[11:46] the ability to reync its environment
[11:46] the ability to reync its environment maybe requires like ffmpeg to be in your
[11:49] maybe requires like ffmpeg to be in your
[11:49] maybe requires like ffmpeg to be in your environment and it wasn't when you
[11:51] environment and it wasn't when you
[11:51] environment and it wasn't when you started and so there's this question of
[11:52] started and so there's this question of
[11:52] started and so there's this question of how do I programmatically spin up new
[11:54] how do I programmatically spin up new
[11:54] how do I programmatically spin up new environments or you know how do I shut
[11:57] environments or you know how do I shut
[11:57] environments or you know how do I shut down an environment resume it with a
[11:59] down an environment resume it with a
[11:59] down an environment resume it with a snapshot so now it's actually imbued
[12:01] snapshot so now it's actually imbued
[12:01] snapshot so now it's actually imbued with the the true environment it needs
[12:03] with the the true environment it needs
[12:03] with the the true environment it needs needs to do its job and it's not
[12:06] needs to do its job and it's not
[12:06] needs to do its job and it's not something that I just want to throw away
[12:07] something that I just want to throw away
[12:07] something that I just want to throw away and rerun and I think that's important
[12:09] and rerun and I think that's important
[12:09] and rerun and I think that's important which is in CI/CD I think we tend to
[12:11] which is in CI/CD I think we tend to
[12:11] which is in CI/CD I think we tend to treat these things as cattle if you'll
[12:13] treat these things as cattle if you'll
[12:13] treat these things as cattle if you'll sort of forgive the tired phrase and so
[12:15] sort of forgive the tired phrase and so
[12:15] sort of forgive the tired phrase and so I think we're totally fine with like
[12:17] I think we're totally fine with like
[12:17] I think we're totally fine with like throwing away CI/CD runs and then
[12:19] throwing away CI/CD runs and then
[12:19] throwing away CI/CD runs and then resuming them later whereas an agent
[12:20] resuming them later whereas an agent
[12:20] resuming them later whereas an agent it's really hard to throw away its
[12:22] it's really hard to throw away its
[12:22] it's really hard to throw away its progress because it could have been
[12:23] progress because it could have been
[12:23] progress because it could have been working for a day or so and you don't
[12:25] working for a day or so and you don't
[12:25] working for a day or so and you don't want to throw away all that progress the
[12:26] want to throw away all that progress the
[12:26] want to throw away all that progress the last bit is really that this is a
[12:28] last bit is really that this is a
[12:28] last bit is really that this is a totally different security boundary and
[12:30] totally different security boundary and
[12:30] totally different security boundary and when you're running CI it often feels a
[12:32] when you're running CI it often feels a
[12:32] when you're running CI it often feels a lot more like running a CI platform
[12:34] lot more like running a CI platform
[12:34] lot more like running a CI platform feels like running CI which is you know
[12:37] feels like running CI which is you know
[12:37] feels like running CI which is you know when you run CI and you think about like
[12:39] when you run CI and you think about like
[12:39] when you run CI and you think about like the threat or security model what are
[12:41] the threat or security model what are
[12:41] the threat or security model what are you really afraid of I'm afraid of like
[12:44] you really afraid of I'm afraid of like
[12:44] you really afraid of I'm afraid of like HML getting access to my environment and
[12:47] HML getting access to my environment and
[12:47] HML getting access to my environment and maybe trying to excfiltrate secrets so
[12:49] maybe trying to excfiltrate secrets so
[12:49] maybe trying to excfiltrate secrets so this is like where we're obsessed over
[12:51] this is like where we're obsessed over
[12:51] this is like where we're obsessed over like grits and environment variables and
[12:53] like grits and environment variables and
[12:53] like grits and environment variables and not injecting them or like you know not
[12:55] not injecting them or like you know not
[12:55] not injecting them or like you know not having them available in plain text so
[12:56] having them available in plain text so
[12:56] having them available in plain text so that if somebody gets access to the
[12:58] that if somebody gets access to the
[12:58] that if somebody gets access to the machine maybe they could read them but
[12:59] machine maybe they could read them but
[12:59] machine maybe they could read them but when you're running an environment for
[13:01] when you're running an environment for
[13:01] when you're running an environment for an agent if it even has access to
[13:03] an agent if it even has access to
[13:03] an agent if it even has access to secrets in its environment variables. It
[13:05] secrets in its environment variables. It
[13:05] secrets in its environment variables. It can go, it can read them, and I'm not
[13:07] can go, it can read them, and I'm not
[13:07] can go, it can read them, and I'm not going to be like FUD or fear-mongery
[13:10] going to be like FUD or fear-mongery
[13:10] going to be like FUD or fear-mongery around agents, but sometimes they can do
[13:12] around agents, but sometimes they can do
[13:12] around agents, but sometimes they can do dumb things. They can take a key,
[13:14] dumb things. They can take a key,
[13:14] dumb things. They can take a key, misunderstand what the key is about,
[13:16] misunderstand what the key is about,
[13:16] misunderstand what the key is about, maybe they request, you know, to a
[13:18] maybe they request, you know, to a
[13:18] maybe they request, you know, to a service and they put it in the URL
[13:19] service and they put it in the URL
[13:20] service and they put it in the URL parameters so it gets logged. I'm kind
[13:21] parameters so it gets logged. I'm kind
[13:21] parameters so it gets logged. I'm kind of more in the house of like these
[13:23] of more in the house of like these
[13:23] of more in the house of like these things just kind of happen by mistake
[13:25] things just kind of happen by mistake
[13:25] things just kind of happen by mistake more than there's some like rogue agent.
[13:27] more than there's some like rogue agent.
[13:27] more than there's some like rogue agent. I'm not a big FUD sewer around this
[13:28] I'm not a big FUD sewer around this
[13:28] I'm not a big FUD sewer around this stuff, but I would just say that you
[13:30] stuff, but I would just say that you
[13:30] stuff, but I would just say that you fundamentally have a process that you
[13:31] fundamentally have a process that you
[13:31] fundamentally have a process that you can't trust that you don't want to give
[13:32] can't trust that you don't want to give
[13:32] can't trust that you don't want to give access to your secrets. And so you end
[13:34] access to your secrets. And so you end
[13:34] access to your secrets. And so you end up having to design this security or
[13:36] up having to design this security or
[13:36] up having to design this security or isolation boundary a little bit
[13:37] isolation boundary a little bit
[13:37] isolation boundary a little bit different. And so those three really
[13:39] different. And so those three really
[13:39] different. And so those three really constraints all kind of pale in
[13:41] constraints all kind of pale in
[13:41] constraints all kind of pale in comparison to the last one, which is
[13:43] comparison to the last one, which is
[13:43] comparison to the last one, which is that cold starts matter a ton. And to
[13:45] that cold starts matter a ton. And to
[13:45] that cold starts matter a ton. And to really feel this, let's talk about some
[13:46] really feel this, let's talk about some
[13:46] really feel this, let's talk about some of the worst designed agent platforms
[13:49] of the worst designed agent platforms
[13:49] of the worst designed agent platforms that I've worked with. some agent
[13:50] that I've worked with. some agent
[13:50] that I've worked with. some agent platforms where maybe the UA could
[13:51] platforms where maybe the UA could
[13:52] platforms where maybe the UA could improve a little bit which is if you
[13:53] improve a little bit which is if you
[13:53] improve a little bit which is if you look at something like hosted clawed
[13:55] look at something like hosted clawed
[13:55] look at something like hosted clawed code if you want to go set this up for
[13:56] code if you want to go set this up for
[13:56] code if you want to go set this up for the first time you know you'll fill in
[13:58] the first time you know you'll fill in
[13:58] the first time you know you'll fill in your traditional metadata and then you
[13:59] your traditional metadata and then you
[13:59] your traditional metadata and then you get to this part where you have to go
[14:01] get to this part where you have to go
[14:01] get to this part where you have to go set up a setup script and notice this is
[14:04] set up a setup script and notice this is
[14:04] set up a setup script and notice this is where like you're going to go install UV
[14:06] where like you're going to go install UV
[14:06] where like you're going to go install UV you're going to install ffmpeg you're
[14:08] you're going to install ffmpeg you're
[14:08] you're going to install ffmpeg you're going to go uvp pip install your you
[14:10] going to go uvp pip install your you
[14:10] going to go uvp pip install your you know your pi project tol or what have
[14:12] know your pi project tol or what have
[14:12] know your pi project tol or what have you and where this ends up really biting
[14:14] you and where this ends up really biting
[14:14] you and where this ends up really biting you is this is a design that almost
[14:16] you is this is a design that almost
[14:16] you is this is a design that almost treats it closer to CI than treating it
[14:18] treats it closer to CI than treating it
[14:18] treats it closer to CI than treating it as its own distinct problem. And as a
[14:20] as its own distinct problem. And as a
[14:20] as its own distinct problem. And as a result, whenever any new sandbox gets
[14:23] result, whenever any new sandbox gets
[14:23] result, whenever any new sandbox gets spun up, it's going to go run this setup
[14:25] spun up, it's going to go run this setup
[14:25] spun up, it's going to go run this setup script every time in a way that's not
[14:27] script every time in a way that's not
[14:27] script every time in a way that's not cached or snapshotted. And so any task
[14:29] cached or snapshotted. And so any task
[14:29] cached or snapshotted. And so any task that you give it, we've all felt the
[14:31] that you give it, we've all felt the
[14:31] that you give it, we've all felt the sort of pain of environments that take
[14:32] sort of pain of environments that take
[14:32] sort of pain of environments that take like two or three minutes or even 10 to
[14:34] like two or three minutes or even 10 to
[14:34] like two or three minutes or even 10 to spin up. And this is a tax that you pay
[14:35] spin up. And this is a tax that you pay
[14:35] spin up. And this is a tax that you pay every time. And Codex is no different.
[14:37] every time. And Codex is no different.
[14:37] every time. And Codex is no different. It's literally the exact same. It's like
[14:39] It's literally the exact same. It's like
[14:39] It's literally the exact same. It's like you want to go set up a setup script and
[14:40] you want to go set up a setup script and
[14:40] you want to go set up a setup script and a cleanup script. and these paradigms
[14:42] a cleanup script. and these paradigms
[14:42] a cleanup script. and these paradigms that really try to treat environmental
[14:44] that really try to treat environmental
[14:44] that really try to treat environmental engineering the way that we treat CI,
[14:47] engineering the way that we treat CI,
[14:47] engineering the way that we treat CI, you feel it as a user because you're
[14:49] you feel it as a user because you're
[14:49] you feel it as a user because you're seeing like just totally intolerable
[14:51] seeing like just totally intolerable
[14:52] seeing like just totally intolerable cold starts. And so these are sort of
[14:53] cold starts. And so these are sort of
[14:53] cold starts. And so these are sort of bad for a whole ton of reasons. And it's
[14:56] bad for a whole ton of reasons. And it's
[14:56] bad for a whole ton of reasons. And it's not only just the cold starts, I'd say
[14:58] not only just the cold starts, I'd say
[14:58] not only just the cold starts, I'd say that environment drifts ends up being
[15:00] that environment drifts ends up being
[15:00] that environment drifts ends up being kind of the worst part truly in
[15:02] kind of the worst part truly in
[15:02] kind of the worst part truly in practice. Like even if we all had time
[15:04] practice. Like even if we all had time
[15:04] practice. Like even if we all had time on our hands and we could just walk
[15:05] on our hands and we could just walk
[15:05] on our hands and we could just walk away, where this really ends up failing
[15:07] away, where this really ends up failing
[15:07] away, where this really ends up failing you as a user is that your environment
[15:09] you as a user is that your environment
[15:09] you as a user is that your environment starts to drift away from you. And so
[15:10] starts to drift away from you. And so
[15:10] starts to drift away from you. And so you'll set environment variables, maybe
[15:12] you'll set environment variables, maybe
[15:12] you'll set environment variables, maybe you'll set a setup script, but then your
[15:13] you'll set a setup script, but then your
[15:13] you'll set a setup script, but then your code changes and your code isn't really
[15:15] code changes and your code isn't really
[15:15] code changes and your code isn't really synced with this environment that you
[15:17] synced with this environment that you
[15:17] synced with this environment that you have saved in these remote agent
[15:18] have saved in these remote agent
[15:18] have saved in these remote agent platforms. And so really it ends up
[15:19] platforms. And so really it ends up
[15:20] platforms. And so really it ends up leading to a bad user experience. And so
[15:21] leading to a bad user experience. And so
[15:21] leading to a bad user experience. And so what did RAMP and others do? I would say
[15:23] what did RAMP and others do? I would say
[15:23] what did RAMP and others do? I would say that all of these have sort of coalesed
[15:25] that all of these have sort of coalesed
[15:25] that all of these have sort of coalesed upon a pretty common approach to
[15:27] upon a pretty common approach to
[15:27] upon a pretty common approach to environmental engineering which is all
[15:29] environmental engineering which is all
[15:30] environmental engineering which is all of them. So this is sort of like kind of
[15:31] of them. So this is sort of like kind of
[15:31] of them. So this is sort of like kind of free alpha on designing these systems
[15:34] free alpha on designing these systems
[15:34] free alpha on designing these systems which is all of them decided that really
[15:36] which is all of them decided that really
[15:36] which is all of them decided that really you can't separate the actual
[15:38] you can't separate the actual
[15:38] you can't separate the actual environment from the code itself. And so
[15:40] environment from the code itself. And so
[15:40] environment from the code itself. And so that means that every single repo that
[15:43] that means that every single repo that
[15:43] that means that every single repo that you have that you're trying to have a
[15:44] you have that you're trying to have a
[15:44] you have that you're trying to have a coding agent go and operate on, you
[15:46] coding agent go and operate on, you
[15:46] coding agent go and operate on, you actually maintain per repo images
[15:49] actually maintain per repo images
[15:49] actually maintain per repo images actually in code. And so you take on the
[15:51] actually in code. And so you take on the
[15:52] actually in code. And so you take on the life cycle of that image creation. A lot
[15:54] life cycle of that image creation. A lot
[15:54] life cycle of that image creation. A lot of them chose modal made a lot of
[15:56] of them chose modal made a lot of
[15:56] of them chose modal made a lot of optimizations to sort of make sure that
[15:58] optimizations to sort of make sure that
[15:58] optimizations to sort of make sure that if you build an image once and every
[16:00] if you build an image once and every
[16:00] if you build an image once and every time that you rebuild it, we don't, you
[16:02] time that you rebuild it, we don't, you
[16:02] time that you rebuild it, we don't, you know, have to rebuild it from scratch.
[16:03] know, have to rebuild it from scratch.
[16:03] know, have to rebuild it from scratch. We do a lot of like making sure that a
[16:05] We do a lot of like making sure that a
[16:05] We do a lot of like making sure that a lot of the same files. If you've used a
[16:07] lot of the same files. If you've used a
[16:07] lot of the same files. If you've used a file before, we don't go redownload it.
[16:09] file before, we don't go redownload it.
[16:09] file before, we don't go redownload it. It's like a lot of lazy file system
[16:11] It's like a lot of lazy file system
[16:11] It's like a lot of lazy file system optimizations. And so you can define an
[16:13] optimizations. And so you can define an
[16:13] optimizations. And so you can define an image in code and every subsequent
[16:15] image in code and every subsequent
[16:15] image in code and every subsequent rebuild ends up being really fast. They
[16:17] rebuild ends up being really fast. They
[16:17] rebuild ends up being really fast. They re-ake this every image on a 30 minute
[16:19] re-ake this every image on a 30 minute
[16:19] re-ake this every image on a 30 minute schedule, which means that whenever a
[16:21] schedule, which means that whenever a
[16:21] schedule, which means that whenever a new agent needs to go pick up a task,
[16:23] new agent needs to go pick up a task,
[16:24] new agent needs to go pick up a task, they basically have something that is at
[16:26] they basically have something that is at
[16:26] they basically have something that is at most 30 minutes different from what
[16:27] most 30 minutes different from what
[16:27] most 30 minutes different from what lives on main. Empirically, that ends up
[16:30] lives on main. Empirically, that ends up
[16:30] lives on main. Empirically, that ends up not being, you know, too bad. And so
[16:32] not being, you know, too bad. And so
[16:32] not being, you know, too bad. And so they end up just doing a pretty simple
[16:33] they end up just doing a pretty simple
[16:34] they end up just doing a pretty simple git sync on start of the sandbox. And so
[16:36] git sync on start of the sandbox. And so
[16:36] git sync on start of the sandbox. And so what that means is that yeah, every new
[16:37] what that means is that yeah, every new
[16:37] what that means is that yeah, every new dev box gets mounted on a pretty warm
[16:39] dev box gets mounted on a pretty warm
[16:40] dev box gets mounted on a pretty warm image. And so every single agent gets
[16:42] image. And so every single agent gets
[16:42] image. And so every single agent gets spun up in less than a second and is
[16:44] spun up in less than a second and is
[16:44] spun up in less than a second and is able to go and get to work. the ability
[16:45] able to go and get to work. the ability
[16:45] able to go and get to work. the ability to their sort of intentional design
[16:47] to their sort of intentional design
[16:47] to their sort of intentional design choice here is keeping secrets actually
[16:50] choice here is keeping secrets actually
[16:50] choice here is keeping secrets actually out of the environment where we talked
[16:51] out of the environment where we talked
[16:51] out of the environment where we talked about where an agent could unwittingly
[16:53] about where an agent could unwittingly
[16:53] about where an agent could unwittingly access them and unwittingly xfill them
[16:56] access them and unwittingly xfill them
[16:56] access them and unwittingly xfill them where building actual like proxies or
[16:58] where building actual like proxies or
[16:58] where building actual like proxies or sidecars on top of that. And so your
[17:00] sidecars on top of that. And so your
[17:00] sidecars on top of that. And so your agent you'll basically give it like
[17:02] agent you'll basically give it like
[17:02] agent you'll basically give it like don't make a request to GitHub. If you
[17:04] don't make a request to GitHub. If you
[17:04] don't make a request to GitHub. If you make a request to GitHub I'm going to
[17:05] make a request to GitHub I'm going to
[17:05] make a request to GitHub I'm going to proxy it to a sidecar and then that's
[17:07] proxy it to a sidecar and then that's
[17:08] proxy it to a sidecar and then that's actually where I'm going to attach a
[17:09] actually where I'm going to attach a
[17:09] actually where I'm going to attach a secret. And so the untrusted agent with
[17:11] secret. And so the untrusted agent with
[17:11] secret. And so the untrusted agent with a mind of its own not to answer for is
[17:14] a mind of its own not to answer for is
[17:14] a mind of its own not to answer for is never really has access to to the
[17:15] never really has access to to the
[17:15] never really has access to to the secrets itself. It can just submit
[17:17] secrets itself. It can just submit
[17:17] secrets itself. It can just submit requests that a more deterministic
[17:19] requests that a more deterministic
[17:19] requests that a more deterministic process can intercept and imbue with a
[17:21] process can intercept and imbue with a
[17:21] process can intercept and imbue with a secret. And so this design has helped
[17:23] secret. And so this design has helped
[17:23] secret. And so this design has helped ramp scale to almost a million sandboxes
[17:26] ramp scale to almost a million sandboxes
[17:26] ramp scale to almost a million sandboxes for ramp inspect. I think it's something
[17:28] for ramp inspect. I think it's something
[17:28] for ramp inspect. I think it's something on the order of like 70% of their PRs
[17:30] on the order of like 70% of their PRs
[17:30] on the order of like 70% of their PRs now are the result of a background
[17:32] now are the result of a background
[17:32] now are the result of a background agent. a lot of the design decisions
[17:34] agent. a lot of the design decisions
[17:34] agent. a lot of the design decisions that we made in order to enable like not
[17:36] that we made in order to enable like not
[17:36] that we made in order to enable like not just this you know less than a second
[17:38] just this you know less than a second
[17:38] just this you know less than a second boot on maybe one to 10 sandboxes but
[17:41] boot on maybe one to 10 sandboxes but
[17:41] boot on maybe one to 10 sandboxes but how we were able to reliably do this for
[17:42] how we were able to reliably do this for
[17:42] how we were able to reliably do this for folks like ramp at that million sandbox
[17:44] folks like ramp at that million sandbox
[17:44] folks like ramp at that million sandbox scale. What's the sort of result then
[17:46] scale. What's the sort of result then
[17:46] scale. What's the sort of result then end of this is really the fundamental
[17:48] end of this is really the fundamental
[17:48] end of this is really the fundamental principle is they're able to eat these
[17:50] principle is they're able to eat these
[17:50] principle is they're able to eat these image builds asynchronously. So that 30
[17:52] image builds asynchronously. So that 30
[17:52] image builds asynchronously. So that 30 minute background process means that
[17:55] minute background process means that
[17:55] minute background process means that maybe if somebody added a pretty
[17:56] maybe if somebody added a pretty
[17:56] maybe if somebody added a pretty expensive dependency that this gets
[17:58] expensive dependency that this gets
[17:58] expensive dependency that this gets built and cached asynchronously in the
[18:00] built and cached asynchronously in the
[18:00] built and cached asynchronously in the background which means that a human
[18:03] background which means that a human
[18:03] background which means that a human never has to actually you know pay the
[18:05] never has to actually you know pay the
[18:05] never has to actually you know pay the piper for an expensive rebuild. It's all
[18:08] piper for an expensive rebuild. It's all
[18:08] piper for an expensive rebuild. It's all done sort of off the clock. So when you
[18:10] done sort of off the clock. So when you
[18:10] done sort of off the clock. So when you actually start interacting with your
[18:11] actually start interacting with your
[18:11] actually start interacting with your sandbox it's snappy. It means that since
[18:13] sandbox it's snappy. It means that since
[18:13] sandbox it's snappy. It means that since they maintain it in code, they can tune
[18:15] they maintain it in code, they can tune
[18:15] they maintain it in code, they can tune those permissions or ports on a per repo
[18:17] those permissions or ports on a per repo
[18:17] those permissions or ports on a per repo basis so that your front end gets maybe
[18:19] basis so that your front end gets maybe
[18:20] basis so that your front end gets maybe the 3000 port open. The one with your
[18:22] the 3000 port open. The one with your
[18:22] the 3000 port open. The one with your Postgress gets like 5173 or whatever it
[18:24] Postgress gets like 5173 or whatever it
[18:24] Postgress gets like 5173 or whatever it is open. And then also you get that
[18:26] is open. And then also you get that
[18:26] is open. And then also you get that setup versioned alongside your actual
[18:28] setup versioned alongside your actual
[18:28] setup versioned alongside your actual code. Okay, so this solves the stateless
[18:30] code. Okay, so this solves the stateless
[18:30] code. Okay, so this solves the stateless half of the problem, but I think it
[18:31] half of the problem, but I think it
[18:31] half of the problem, but I think it ignores if I was listening to this talk
[18:33] ignores if I was listening to this talk
[18:33] ignores if I was listening to this talk I'd be like, okay, that's cool. So like
[18:35] I'd be like, okay, that's cool. So like
[18:35] I'd be like, okay, that's cool. So like that's maybe where an agent should be
[18:37] that's maybe where an agent should be
[18:37] that's maybe where an agent should be doing its work. I'm glad that we've
[18:38] doing its work. I'm glad that we've
[18:38] doing its work. I'm glad that we've hyperfocused over, you know, how to
[18:40] hyperfocused over, you know, how to
[18:40] hyperfocused over, you know, how to create an environment that's like fast
[18:42] create an environment that's like fast
[18:42] create an environment that's like fast and maybe secure for an agent, but it
[18:45] and maybe secure for an agent, but it
[18:45] and maybe secure for an agent, but it doesn't really answer the question of
[18:46] doesn't really answer the question of
[18:46] doesn't really answer the question of like where's the agent actually running
[18:48] like where's the agent actually running
[18:48] like where's the agent actually running at the end of the day? Like if I'm
[18:49] at the end of the day? Like if I'm
[18:49] at the end of the day? Like if I'm designing this system and I have a dev
[18:51] designing this system and I have a dev
[18:51] designing this system and I have a dev box, like what do I actually do with it?
[18:53] box, like what do I actually do with it?
[18:53] box, like what do I actually do with it? Am I shelling into the dev box or like
[18:55] Am I shelling into the dev box or like
[18:55] Am I shelling into the dev box or like do I have a process that spins up open
[18:57] do I have a process that spins up open
[18:58] do I have a process that spins up open code inside of it? What does it actually
[18:59] code inside of it? What does it actually
[18:59] code inside of it? What does it actually look like when it's designed and sort of
[19:01] look like when it's designed and sort of
[19:01] look like when it's designed and sort of where is this headed? So to to do this,
[19:03] where is this headed? So to to do this,
[19:03] where is this headed? So to to do this, I want to sort of talk about like what
[19:04] I want to sort of talk about like what
[19:04] I want to sort of talk about like what has agent design looked for a long time.
[19:06] has agent design looked for a long time.
[19:06] has agent design looked for a long time. agent design maybe a year and a half ago
[19:09] agent design maybe a year and a half ago
[19:09] agent design maybe a year and a half ago sort of looked like this picture where
[19:11] sort of looked like this picture where
[19:11] sort of looked like this picture where you would have an agent in a process
[19:14] you would have an agent in a process
[19:14] you would have an agent in a process that was colllocated with its tools. So
[19:16] that was colllocated with its tools. So
[19:16] that was colllocated with its tools. So maybe two years ago you were using
[19:18] maybe two years ago you were using
[19:18] maybe two years ago you were using something like lane chain maybe you use
[19:20] something like lane chain maybe you use
[19:20] something like lane chain maybe you use something like crew AI and you would go
[19:21] something like crew AI and you would go
[19:21] something like crew AI and you would go and write an agent you would give it
[19:23] and write an agent you would give it
[19:23] and write an agent you would give it access to tools like file writing or web
[19:25] access to tools like file writing or web
[19:25] access to tools like file writing or web search and you would just instruct your
[19:28] search and you would just instruct your
[19:28] search and you would just instruct your agent to like go do some analysis for
[19:29] agent to like go do some analysis for
[19:29] agent to like go do some analysis for you and so why is this really bad in
[19:31] you and so why is this really bad in
[19:31] you and so why is this really bad in practice? Well all of these things live
[19:33] practice? Well all of these things live
[19:33] practice? Well all of these things live in the same process or the same
[19:35] in the same process or the same
[19:35] in the same process or the same environment. So if you have a data
[19:36] environment. So if you have a data
[19:36] environment. So if you have a data analysis agent in lane chain two years
[19:39] analysis agent in lane chain two years
[19:39] analysis agent in lane chain two years ago or something like this, what would
[19:40] ago or something like this, what would
[19:40] ago or something like this, what would end up happening? You would end up
[19:42] end up happening? You would end up
[19:42] end up happening? You would end up having one tool would go ary in the
[19:46] having one tool would go ary in the
[19:46] having one tool would go ary in the sense of maybe try and run this in a
[19:48] sense of maybe try and run this in a
[19:48] sense of maybe try and run this in a machine that has 2 gigs of memory.
[19:50] machine that has 2 gigs of memory.
[19:50] machine that has 2 gigs of memory. You're trying to get it to open a 10 GB
[19:52] You're trying to get it to open a 10 GB
[19:52] You're trying to get it to open a 10 GB CSV file into memory with pandas or
[19:55] CSV file into memory with pandas or
[19:55] CSV file into memory with pandas or something like this. And then now
[19:56] something like this. And then now
[19:56] something like this. And then now suddenly this one aberrant tool that's
[19:58] suddenly this one aberrant tool that's
[19:58] suddenly this one aberrant tool that's running in the same process as your
[20:00] running in the same process as your
[20:00] running in the same process as your agent blows up and now it's basically
[20:03] agent blows up and now it's basically
[20:03] agent blows up and now it's basically causes your the process holding your
[20:05] causes your the process holding your
[20:05] causes your the process holding your agent to fail over and as a result this
[20:07] agent to fail over and as a result this
[20:07] agent to fail over and as a result this agent who may have been 10 minutes into
[20:10] agent who may have been 10 minutes into
[20:10] agent who may have been 10 minutes into its actual work starts to fail over and
[20:12] its actual work starts to fail over and
[20:12] its actual work starts to fail over and it like loses the state of what it was
[20:14] it like loses the state of what it was
[20:14] it like loses the state of what it was trying to do. So when you design agents
[20:15] trying to do. So when you design agents
[20:16] trying to do. So when you design agents like this and you try and you colllocate
[20:18] like this and you try and you colllocate
[20:18] like this and you try and you colllocate the risky stuff, not risky like FUD
[20:21] the risky stuff, not risky like FUD
[20:21] the risky stuff, not risky like FUD risky, but risky in terms of systems
[20:22] risky, but risky in terms of systems
[20:22] risky, but risky in terms of systems design. If you collocate that with your
[20:24] design. If you collocate that with your
[20:24] design. If you collocate that with your agent, you've basically exposed the
[20:27] agent, you've basically exposed the
[20:27] agent, you've basically exposed the thing that's responsible for keeping
[20:28] thing that's responsible for keeping
[20:28] thing that's responsible for keeping track of what to do with the the thing
[20:31] track of what to do with the the thing
[20:31] track of what to do with the the thing that it's it's supposed to execute. This
[20:32] that it's it's supposed to execute. This
[20:32] that it's it's supposed to execute. This is a problem, you know, sort of tail as
[20:34] is a problem, you know, sort of tail as
[20:34] is a problem, you know, sort of tail as old as time in systems design. And the
[20:36] old as time in systems design. And the
[20:36] old as time in systems design. And the way that we solve this is, you know,
[20:38] way that we solve this is, you know,
[20:38] way that we solve this is, you know, sort of canonical uh orchestration. The
[20:41] sort of canonical uh orchestration. The
[20:41] sort of canonical uh orchestration. The way that you tend to do this is you'll
[20:43] way that you tend to do this is you'll
[20:43] way that you tend to do this is you'll end up wanting to separate out your the
[20:46] end up wanting to separate out your the
[20:46] end up wanting to separate out your the thing that's responsible for holding
[20:48] thing that's responsible for holding
[20:48] thing that's responsible for holding state or the thing that's responsible
[20:49] state or the thing that's responsible
[20:49] state or the thing that's responsible for holding a plan. And you tend to want
[20:51] for holding a plan. And you tend to want
[20:51] for holding a plan. And you tend to want to actually separate this from the thing
[20:53] to actually separate this from the thing
[20:53] to actually separate this from the thing the sort of long tale of risk of the
[20:55] the sort of long tale of risk of the
[20:55] the sort of long tale of risk of the things that it's trying to execute. For
[20:57] things that it's trying to execute. For
[20:57] things that it's trying to execute. For folks that were maybe came up from data
[20:59] folks that were maybe came up from data
[20:59] folks that were maybe came up from data engineering, this is why Airflow never
[21:01] engineering, this is why Airflow never
[21:01] engineering, this is why Airflow never ran stuff itself. It was kicking off
[21:03] ran stuff itself. It was kicking off
[21:03] ran stuff itself. It was kicking off Spark jobs because you didn't want to
[21:04] Spark jobs because you didn't want to
[21:04] Spark jobs because you didn't want to actually crash your scheduler. And so
[21:06] actually crash your scheduler. And so
[21:06] actually crash your scheduler. And so this orchestration design of how do I
[21:08] this orchestration design of how do I
[21:08] this orchestration design of how do I actually keep my agent separated from
[21:11] actually keep my agent separated from
[21:11] actually keep my agent separated from the actual risky stuff that it's
[21:13] the actual risky stuff that it's
[21:13] the actual risky stuff that it's supposed to execute so that my agent
[21:15] supposed to execute so that my agent
[21:15] supposed to execute so that my agent never loses track of its state. And so
[21:17] never loses track of its state. And so
[21:17] never loses track of its state. And so this is kind of a lot of orchestration
[21:19] this is kind of a lot of orchestration
[21:19] this is kind of a lot of orchestration can be just really summed up by saying
[21:21] can be just really summed up by saying
[21:21] can be just really summed up by saying you want to put a fire door between the
[21:24] you want to put a fire door between the
[21:24] you want to put a fire door between the thing that you never want to fail and
[21:26] thing that you never want to fail and
[21:26] thing that you never want to fail and the things that have some risk of
[21:28] the things that have some risk of
[21:28] the things that have some risk of failure. So that way when those tools
[21:30] failure. So that way when those tools
[21:30] failure. So that way when those tools try to execute something in an
[21:32] try to execute something in an
[21:32] try to execute something in an underprovisioned environment, your agent
[21:33] underprovisioned environment, your agent
[21:34] underprovisioned environment, your agent will just see that you had an error
[21:35] will just see that you had an error
[21:35] will just see that you had an error happen, it's not like your agent crashes
[21:37] happen, it's not like your agent crashes
[21:37] happen, it's not like your agent crashes because that tends to be just very
[21:38] because that tends to be just very
[21:38] because that tends to be just very expensive and something that you don't
[21:40] expensive and something that you don't
[21:40] expensive and something that you don't want to see. And so orchestration 101
[21:42] want to see. And so orchestration 101
[21:42] want to see. And so orchestration 101 really is you want to keep an agent in
[21:43] really is you want to keep an agent in
[21:43] really is you want to keep an agent in your control plane, right? That's where
[21:45] your control plane, right? That's where
[21:45] your control plane, right? That's where all the planning is supposed to be. Your
[21:47] all the planning is supposed to be. Your
[21:47] all the planning is supposed to be. Your control plane is really where you want
[21:48] control plane is really where you want
[21:48] control plane is really where you want to keep things that that you want to
[21:50] to keep things that that you want to
[21:50] to keep things that that you want to isolate from the risk of failure. And so
[21:52] isolate from the risk of failure. And so
[21:52] isolate from the risk of failure. And so what I see a lot of these agent
[21:54] what I see a lot of these agent
[21:54] what I see a lot of these agent platforms moving towards is you keep an
[21:56] platforms moving towards is you keep an
[21:56] platforms moving towards is you keep an agent in this control plane, you let it
[21:58] agent in this control plane, you let it
[21:58] agent in this control plane, you let it provision or manage dev boxes. And
[22:01] provision or manage dev boxes. And
[22:01] provision or manage dev boxes. And instead of putting that agent inside the
[22:04] instead of putting that agent inside the
[22:04] instead of putting that agent inside the sandbox with tools to read, write or
[22:07] sandbox with tools to read, write or
[22:07] sandbox with tools to read, write or bash, instead you give that agent in the
[22:10] bash, instead you give that agent in the
[22:10] bash, instead you give that agent in the control plane the ability to remotely
[22:12] control plane the ability to remotely
[22:12] control plane the ability to remotely execute work inside of that remote dev
[22:15] execute work inside of that remote dev
[22:15] execute work inside of that remote dev box. And so what this means is instead
[22:17] box. And so what this means is instead
[22:17] box. And so what this means is instead of saying I'm going to put open code in
[22:19] of saying I'm going to put open code in
[22:20] of saying I'm going to put open code in a sandbox and let it go nuts, I'm going
[22:22] a sandbox and let it go nuts, I'm going
[22:22] a sandbox and let it go nuts, I'm going to spin up open code in one sandbox, but
[22:25] to spin up open code in one sandbox, but
[22:25] to spin up open code in one sandbox, but when it executes write, read, or bash,
[22:28] when it executes write, read, or bash,
[22:28] when it executes write, read, or bash, that's not actually writing files to the
[22:30] that's not actually writing files to the
[22:30] that's not actually writing files to the environment that my process is in. It's
[22:32] environment that my process is in. It's
[22:32] environment that my process is in. It's actually doing a remote call to a second
[22:34] actually doing a remote call to a second
[22:34] actually doing a remote call to a second sandbox. And so that way, if my agent
[22:36] sandbox. And so that way, if my agent
[22:36] sandbox. And so that way, if my agent ever corrupts the environment that it's
[22:38] ever corrupts the environment that it's
[22:38] ever corrupts the environment that it's executing tools in, it's never going to
[22:41] executing tools in, it's never going to
[22:41] executing tools in, it's never going to crash my agent. At worst, it's going to
[22:43] crash my agent. At worst, it's going to
[22:43] crash my agent. At worst, it's going to corrupt the throwaway environment in
[22:45] corrupt the throwaway environment in
[22:45] corrupt the throwaway environment in that data plane. And so, if you're
[22:47] that data plane. And so, if you're
[22:47] that data plane. And so, if you're building this on your own, I would say
[22:49] building this on your own, I would say
[22:49] building this on your own, I would say the three biggest lessons of where to
[22:51] the three biggest lessons of where to
[22:51] the three biggest lessons of where to build and where to buy are going to be
[22:53] build and where to buy are going to be
[22:53] build and where to buy are going to be around really investing in this kind of
[22:56] around really investing in this kind of
[22:56] around really investing in this kind of dev box supply chain. That's not a
[22:58] dev box supply chain. That's not a
[22:58] dev box supply chain. That's not a marketing phrase. It's just the best way
[22:59] marketing phrase. It's just the best way
[23:00] marketing phrase. It's just the best way I can sort of explain it here of we've
[23:02] I can sort of explain it here of we've
[23:02] I can sort of explain it here of we've seen in like the releases of like Devon
[23:04] seen in like the releases of like Devon
[23:04] seen in like the releases of like Devon outposts, you're going to see a lot of
[23:06] outposts, you're going to see a lot of
[23:06] outposts, you're going to see a lot of releases in the next two or 3 weeks. So
[23:09] releases in the next two or 3 weeks. So
[23:09] releases in the next two or 3 weeks. So that's what I want to sort of talk about
[23:10] that's what I want to sort of talk about
[23:10] that's what I want to sort of talk about from a system designs point of view and
[23:12] from a system designs point of view and
[23:12] from a system designs point of view and and sort of really try to back up why if
[23:14] and sort of really try to back up why if
[23:14] and sort of really try to back up why if you're building background agents the
[23:16] you're building background agents the
[23:16] you're building background agents the hard part really is the background part
[23:18] hard part really is the background part
[23:18] hard part really is the background part and so really invest in in building
[23:19] and so really invest in in building
[23:20] and so really invest in in building those environments instead. We've got
[23:21] those environments instead. We've got
[23:21] those environments instead. We've got credible examples library of how to get
[23:23] credible examples library of how to get
[23:23] credible examples library of how to get started on modal. And so maybe what I
[23:25] started on modal. And so maybe what I
[23:25] started on modal. And so maybe what I can do is share some of those materials
[23:27] can do is share some of those materials
[23:27] can do is share some of those materials along with this presentation. If you're
[23:29] along with this presentation. If you're
[23:29] along with this presentation. If you're interested in this, if you want to
[23:30] interested in this, if you want to
[23:30] interested in this, if you want to understand the experience of building
[23:32] understand the experience of building
[23:32] understand the experience of building sandboxes and building those dev boxes
[23:33] sandboxes and building those dev boxes
[23:33] sandboxes and building those dev boxes yourself, sharing some of those
[23:35] yourself, sharing some of those
[23:35] yourself, sharing some of those materials of how to get started would
[23:36] materials of how to get started would
[23:36] materials of how to get started would really encourage folks to go check out
[23:38] really encourage folks to go check out
[23:38] really encourage folks to go check out modal.com. Modal does a bunch of things
[23:40] modal.com. Modal does a bunch of things
[23:40] modal.com. Modal does a bunch of things that aren't just sandboxes. If you want
[23:42] that aren't just sandboxes. If you want
[23:42] that aren't just sandboxes. If you want to deploy open source models, train
[23:44] to deploy open source models, train
[23:44] to deploy open source models, train them. Really, it's a pretty
[23:45] them. Really, it's a pretty
[23:45] them. Really, it's a pretty comprehensive infrastructure. So the
[23:47] comprehensive infrastructure. So the
[23:47] comprehensive infrastructure. So the experience of actually using a modal
[23:49] experience of actually using a modal
[23:49] experience of actually using a modal sandbox is pretty straightforward. We do
[23:51] sandbox is pretty straightforward. We do
[23:51] sandbox is pretty straightforward. We do this in Python, in JavaScript, and it's
[23:53] this in Python, in JavaScript, and it's
[23:54] this in Python, in JavaScript, and it's as straightforward as like I'm going to
[23:55] as straightforward as like I'm going to
[23:55] as straightforward as like I'm going to go create a sandbox and then if I want
[23:57] go create a sandbox and then if I want
[23:57] go create a sandbox and then if I want to go execute code into it, I can simply
[23:59] to go execute code into it, I can simply
[23:59] to go execute code into it, I can simply just call that sandbox and exec Python
[24:01] just call that sandbox and exec Python
[24:01] just call that sandbox and exec Python code straight into it. And then we
[24:03] code straight into it. And then we
[24:03] code straight into it. And then we actually sort of stream that exec back.
[24:05] actually sort of stream that exec back.
[24:05] actually sort of stream that exec back. So if you are trying to go launch cloud
[24:07] So if you are trying to go launch cloud
[24:07] So if you are trying to go launch cloud code or open code in a remote sandbox,
[24:09] code or open code in a remote sandbox,
[24:09] code or open code in a remote sandbox, you're not sort of waiting for it to go
[24:11] you're not sort of waiting for it to go
[24:11] you're not sort of waiting for it to go do all of its work and then come back
[24:12] do all of its work and then come back
[24:12] do all of its work and then come back and report it back to you. So you really
[24:14] and report it back to you. So you really
[24:14] and report it back to you. So you really get sort of the same native experience
[24:16] get sort of the same native experience
[24:16] get sort of the same native experience as if you were working with a local
[24:18] as if you were working with a local
[24:18] as if you were working with a local sandbox remotely
[24:19] sandbox remotely
[24:19] sandbox remotely &gt;&gt; because y'all made it so nice to work
[24:22] &gt;&gt; because y'all made it so nice to work
[24:22] &gt;&gt; because y'all made it so nice to work with for humans. It's actually really
[24:24] with for humans. It's actually really
[24:24] with for humans. It's actually really good. It like agents love it cuz like
[24:26] good. It like agents love it cuz like
[24:26] good. It like agents love it cuz like you get fast feedback. You a lot of
[24:27] you get fast feedback. You a lot of
[24:28] you get fast feedback. You a lot of visibility. The docs are good. All that
[24:30] visibility. The docs are good. All that
[24:30] visibility. The docs are good. All that stuff combines you don't really have to
[24:32] stuff combines you don't really have to
[24:32] stuff combines you don't really have to dig into the syntax I found like
[24:34] dig into the syntax I found like
[24:34] dig into the syntax I found like anymore. You just say hey like I want to
[24:36] anymore. You just say hey like I want to
[24:36] anymore. You just say hey like I want to do this thing with modal and it tends to
[24:37] do this thing with modal and it tends to
[24:37] do this thing with modal and it tends to work. A lot of folks I think as we
[24:39] work. A lot of folks I think as we
[24:39] work. A lot of folks I think as we discovered that like agents were going
[24:41] discovered that like agents were going
[24:41] discovered that like agents were going to start being the largest by volume
[24:43] to start being the largest by volume
[24:43] to start being the largest by volume users of our SDKs. I think there was
[24:46] users of our SDKs. I think there was
[24:46] users of our SDKs. I think there was this moment a few months ago of like, ah
[24:48] this moment a few months ago of like, ah
[24:48] this moment a few months ago of like, ah man, how are we going to have to
[24:49] man, how are we going to have to
[24:49] man, how are we going to have to redesign everything so agents learn how
[24:51] redesign everything so agents learn how
[24:51] redesign everything so agents learn how to use this and then it was the most
[24:53] to use this and then it was the most
[24:53] to use this and then it was the most like anticlimactic thing which was like
[24:55] like anticlimactic thing which was like
[24:56] like anticlimactic thing which was like oh oh okay they just need good docs and
[24:58] oh oh okay they just need good docs and
[24:58] oh oh okay they just need good docs and they need good typing they need type
[25:00] they need good typing they need type
[25:00] they need good typing they need type hints they need good error codes and
[25:02] hints they need good error codes and
[25:02] hints they need good error codes and those were a lot of things that predates
[25:03] those were a lot of things that predates
[25:03] those were a lot of things that predates me at modal just to be clear but it was
[25:05] me at modal just to be clear but it was
[25:05] me at modal just to be clear but it was something that modal's invested in for
[25:07] something that modal's invested in for
[25:07] something that modal's invested in for years because it was always obsessing
[25:09] years because it was always obsessing
[25:09] years because it was always obsessing over like how do I help a human
[25:11] over like how do I help a human
[25:11] over like how do I help a human understand what to do next and a lot of
[25:12] understand what to do next and a lot of
[25:12] understand what to do next and a lot of that is you know how to help an agent
[25:14] that is you know how to help an agent
[25:14] that is you know how to help an agent understand what to do And so really
[25:16] understand what to do And so really
[25:16] understand what to do And so really encourage folks to go check out our docs
[25:18] encourage folks to go check out our docs
[25:18] encourage folks to go check out our docs if you want to go actually background a
[25:20] if you want to go actually background a
[25:20] if you want to go actually background a single coding agent. If you want to
[25:21] single coding agent. If you want to
[25:21] single coding agent. If you want to build we've got a reference example of
[25:23] build we've got a reference example of
[25:23] build we've got a reference example of like how to actually go build your own
[25:25] like how to actually go build your own
[25:25] like how to actually go build your own lovable on modal as well. And if
[25:28] lovable on modal as well. And if
[25:28] lovable on modal as well. And if depending on exactly like which is your
[25:30] depending on exactly like which is your
[25:30] depending on exactly like which is your preferred agent SDK showing folks how to
[25:33] preferred agent SDK showing folks how to
[25:33] preferred agent SDK showing folks how to use it with langraph how to build
[25:35] use it with langraph how to build
[25:35] use it with langraph how to build computer use agents how to build code
[25:37] computer use agents how to build code
[25:37] computer use agents how to build code interpreters. And so
[25:38] interpreters. And so
[25:38] interpreters. And so &gt;&gt; how do you see folks getting visibility
[25:40] &gt;&gt; how do you see folks getting visibility
[25:40] &gt;&gt; how do you see folks getting visibility into everything that's happening and
[25:42] into everything that's happening and
[25:42] into everything that's happening and knowing when to touch? you're giving
[25:43] knowing when to touch? you're giving
[25:43] knowing when to touch? you're giving such a great point of leverage.
[25:45] such a great point of leverage.
[25:45] such a great point of leverage. &gt;&gt; It depends on what you want visibility
[25:46] &gt;&gt; It depends on what you want visibility
[25:46] &gt;&gt; It depends on what you want visibility into. I know that's like a lot of folks
[25:48] into. I know that's like a lot of folks
[25:48] into. I know that's like a lot of folks invest in like classic kind of hotel
[25:51] invest in like classic kind of hotel
[25:51] invest in like classic kind of hotel style instrumentation just so they can
[25:52] style instrumentation just so they can
[25:52] style instrumentation just so they can understand like what their agents are
[25:54] understand like what their agents are
[25:54] understand like what their agents are even up to. I see folks reach for like
[25:56] even up to. I see folks reach for like
[25:56] even up to. I see folks reach for like brain trust, logfire, langfuse to just
[25:59] brain trust, logfire, langfuse to just
[25:59] brain trust, logfire, langfuse to just like understand what their agents are
[26:00] like understand what their agents are
[26:00] like understand what their agents are actually working on. And then you know
[26:02] actually working on. And then you know
[26:02] actually working on. And then you know we export a lot of those metrics so you
[26:04] we export a lot of those metrics so you
[26:04] we export a lot of those metrics so you can understand like traces around our
[26:06] can understand like traces around our
[26:06] can understand like traces around our infrastructure. So you can actually get
[26:07] infrastructure. So you can actually get
[26:07] infrastructure. So you can actually get a better view into like all right these
[26:09] a better view into like all right these
[26:09] a better view into like all right these agents in these environments were able
[26:11] agents in these environments were able
[26:11] agents in these environments were able to accomplish their tasks versus you
[26:13] to accomplish their tasks versus you
[26:14] to accomplish their tasks versus you know we had a few hundred agents runs
[26:16] know we had a few hundred agents runs
[26:16] know we had a few hundred agents runs fail because they were being summoned to
[26:19] fail because they were being summoned to
[26:19] fail because they were being summoned to complete a task in an environment that
[26:21] complete a task in an environment that
[26:21] complete a task in an environment that didn't actually have the underlying
[26:23] didn't actually have the underlying
[26:23] didn't actually have the underlying infrastructure or maybe like GPUs or
[26:25] infrastructure or maybe like GPUs or
[26:25] infrastructure or maybe like GPUs or something to accomplish it. So that's
[26:27] something to accomplish it. So that's
[26:27] something to accomplish it. So that's more from like a observability point of
[26:29] more from like a observability point of
[26:29] more from like a observability point of view of you know how to keep track of
[26:31] view of you know how to keep track of
[26:31] view of you know how to keep track of what these things are actually doing.
[26:33] what these things are actually doing.
[26:33] what these things are actually doing. Those platforms tend to be nice because
[26:35] Those platforms tend to be nice because
[26:35] Those platforms tend to be nice because they help you also understand like
[26:37] they help you also understand like
[26:37] they help you also understand like larger themes about how your agents are
[26:39] larger themes about how your agents are
[26:39] larger themes about how your agents are actually performing. But as far as like
[26:41] actually performing. But as far as like
[26:41] actually performing. But as far as like what's the actual impact of these
[26:44] what's the actual impact of these
[26:44] what's the actual impact of these hundreds of agents all PRing like stuff
[26:46] hundreds of agents all PRing like stuff
[26:46] hundreds of agents all PRing like stuff against your ura like I think a lot of
[26:48] against your ura like I think a lot of
[26:48] against your ura like I think a lot of folks still rely on kind of okay
[26:52] folks still rely on kind of okay
[26:52] folks still rely on kind of okay mediocre like GitHub stats on this
[26:54] mediocre like GitHub stats on this
[26:54] mediocre like GitHub stats on this stuff. I would say it's a pretty
[26:55] stuff. I would say it's a pretty
[26:56] stuff. I would say it's a pretty underexplored problem area to be honest.
[26:58] underexplored problem area to be honest.
[26:58] underexplored problem area to be honest. Like I think a lot of folks are
[26:59] Like I think a lot of folks are
[26:59] Like I think a lot of folks are overinvested in observability
[27:03] overinvested in observability
[27:03] overinvested in observability for the one agent and I think it's an
[27:05] for the one agent and I think it's an
[27:06] for the one agent and I think it's an open problem but I feel like it's an
[27:07] open problem but I feel like it's an
[27:08] open problem but I feel like it's an underexplored problem of like as a as a
[27:10] underexplored problem of like as a as a
[27:10] underexplored problem of like as a as a system of agents itself how do you
[27:11] system of agents itself how do you
[27:11] system of agents itself how do you instrument and observe the impact of I
[27:13] instrument and observe the impact of I
[27:13] instrument and observe the impact of I think what is maybe be called like
[27:15] think what is maybe be called like
[27:15] think what is maybe be called like software factories this day. I think
[27:16] software factories this day. I think
[27:16] software factories this day. I think that's the marketing term for it.
[27:17] that's the marketing term for it.
[27:17] that's the marketing term for it. &gt;&gt; Thank you. Appreciate it.
