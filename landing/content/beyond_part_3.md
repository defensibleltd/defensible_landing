---
title: "Beyond The SOC (Part 3)"
url: "/beyond_the_soc_part_3"
description: "Trajectories in security operations. The Future."
hidemeta: true
draft: false
---
<style>
.post-description {
  font-size: 1.5em; color: var(--text, #666);
}
</style>

<div style="background-color: var(--card-bg, #fff); border-radius: 20px; padding: 24px 20px 20px 20px; width: 100%; margin-bottom: 32px;">
  <img loading="lazy" class="img-fluid" src="/images/new_image.png" alt="Beyond the SOC Cover" style="border-radius: 12px; margin: 16px 0;">
</div>


##  The Future

### A Virtual Core

The traditional SOC, as the sole nexus of security operations, is dissipating. The SOC doesn't exist as a point in time or space any longer. It is digitally and unevenly distributed. It's wholly virtual and focuses on ever more endpoints with larger service surfaces. It refines and reduces exponentially growing noise to stronger signals and concrete decisions. Automated actions are triggered by highly trusted workflows. Employees themselves are crowdsourced from and considered intelligent sensors, not lacklustre liabilities. The modern SOC is SOC-less, we're beyond the SOC, there is no physical center.

For many, there hasn't been a traditional SOC for some time. The new core is composable, highly scalable, and itself, introspectable.

### The Middle Way

SecOps is now a hybrid affair. It leverages increased observability, is almost wholly automated and is supported and augmented by real-A.I. (Artificial Intelligence) capabilities. It still retains highly valued human decision making and supervisory roles. Evolving detection engineering means a mix of more intelligent sensors at the edge feeding a scalable and elastic processing core. This can result in optionally more or less telemetry, but the fidelity required is higher, the representation of state, better. Grouping and zoning of assets are still required for these new architectures to facilitate decision making. Extracting features, correlating, clustering, and leveraging mutual information is faster. Impermanence is better understood and embraced within the security model.

### Security Observability

Observability is a measure of how well internal states of a system can be inferred from knowledge of its external outputs. In a security context this means whether we can infer the system (or entity) can still be trusted to perform integral and secure operations and/or that it has not been subverted or compromised in any way. We may use passive or active measures to try and establish this. We may query the entity directly or use side-channels, signals, and second-order effects. We may also apply this quality or property of observability to larger parts of our organization such as aggregate groups of hosts or network segments. The degree to which we can observe and infer the security state of a device is crucial to SecOps and relies heavily on detection engineering.

### Deceptive Detection?

One of the primary concerns is that we are dealing with an active and sentient adversary (or their agent) who wishes to evade detection. This means the state space may be being intentionally misrepresented to us which makes the detection task even more difficult. It's not just a case of trust via transparency, but the even harder problem of provable security. Encryption can also render parts and paths of a system opaque to us (without the correct keys or access) so SecOps may not always get the required visibility.

Sometimes relying on indirect means of establishing the state and integrity of a system or segment must be embraced. Digital lures and tripwires now play a greater role in detection as they give higher fidelity signals about the presence and intent of any malicious actors (they also generate low to no noise when strategically placed). This turns the tables on attackers and reverses an age-old asymmetry where the attacker now needs to detect whether they are engaging with valid assets are not. Their TTPs (Tactics, Techniques, and Procedures) are disrupted and paths more tightly constrained. Internal honeypots are not a new detection technology but have become more usable and yield greater returns in the 'kill-chain'.

### Wake Up and Stream

At any time an organization can be growing, shrinking, or temporarily in homeostasis. Employees, contractors, and 3rd parties constantly require provisioning, onboarding, and de-provisioning. SecOps must diminish any unknown unknowns and retain timely hooks into a range of organizational processes, silos, and systems. Where templated cloud instances can wake up (preloaded with tooling, agents, or sidecars) and immediately call home to self-register, there are other pockets, pools, and populations of assets that take longer to register. In the interim, these assets may be dark, unobservable, and non-controllable. SecOps still requires a mix of push and pull access to a range of endpoints for situational awareness and enrichment purposes. Whether it's maintaining security service accounts on other teams systems or rotating dedicated API keys, it's not just datacenter resources in play. Independent service and asset discovery will continue to fill in the blind spots. Spurious firewall and routing changes, cowboy cabling, errors and omissions, B.Y.O.D. and shadow I.T. all mean your footprint may not be as clear-cut as a discrete range of AWS NETBLOCKs. Constant enumeration means a mix of active scanning capabilities and the ability to poll or update multiple registries and systems of record.

### CI/CD/CS

Continuous Improvement (CI) and Continuous Deployment (CD) have changed the game for developing and deploying applications, systems, and platforms. Implicit in the concept of CI is Continuous Security (CS) but this is not always the case. DevOps (Developer Operations) merges the roles and best practices of each previously distinct team. In a nutshell, those who make the thing are responsible for operating the thing (and best placed to quickly diagnose and fix the thing). Infrastructure and configuration also become managed and orchestrated as code (where possible). Software development practices and pipelines leverage tighter revision control, better testing, and automatic deploys to accelerate the 'shipping' and evolution of products and services.

This approach also helps to minimize risk and spot errors more quickly. Although the cadence increases, the magnitude and impact of each change is theoretically lowered, and feature velocity increases for consumers. Risk is also assumed to be lowered but only if security observability increases and mitigation occurs quickly. SecOps can also apply this approach to its own platforms, not just to the assets and channels it protects. Detection logic, platform operations, and workflows are all represented as readable and malleable code that's version controlled. Yet once risk is identified, the burden of classifying, tracking, and mitigating risk lands in different places depending upon the organization.

### C\&C Monoculture

Security operations exist as an overlay, of another services overlay, your organization. How do we ensure we mitigate the risk we ourselves may inject? Just as backup and malware software agents run with escalated privileges and create new attack surfaces, we must walk a fine line between connecting everything back to SecOps platforms with excessive privileges. Whether pushing and pulling, across trusted or untrusted fabrics, to managed or unmanaged endpoints, have we just created a new but ubiquitous attack surface for all our assets? It depends. There is an implicit assumption that security engineers and security operations platforms are more secure than 'regular' engineering and operations. Writing secure code is a hard problem. Building secure systems is even harder, as is maintaining trust. We must not forget to get our own house in order before pontificating to others about risk!

We also face a 'Portfolio Problem' where no single supplier can provide Best-in-Class (Best-in-Breed) solutions across all functional requirements for a modern SecOps practice. Cherry-picking security platforms and providers means a more heterogeneous environment, one that's connected with open standards, one that understands ecosystems and the value of secure flows. This then results in your security workflow logic becoming your secret sauce, as it is unique to your organization, just like a fingerprint. Sustainable and resilient SecOps must focus on composability built atop of an API first mindset. This also means first-class APIs (rather than a hastily cobbled-together afterthought).

### Not All Developers

New terms like SecDevOps assume internal developers write all tooling. Not every organization produces software, many just purchase and consume it. For some, internal tooling teams are a luxury though increasingly a basic requirement. Many wrestle with vendors and procurement yet all SecOps are, at a macro level, composing security services. Be it using rented cloud services or SaaS (Software as a Service), to consuming or offering these services via an API. 'Build or buy' may be the catch-cry but you still can not outsource your own risk, so whether you have the budget and resources or not, architecting and at least orchestrating your own macro security processes and workflows is crucial. This is the malleable logic that must be encoded and gotten right. It may start with an analyst, engineer, or manager, but low and no-code visual workflows do not require software engineering capabilities. Automation is increasingly accessible to all levels of expertise and required to overcome modern SecOps challenges.

### Idempotent Workflows

Where and how does our security logic evolve from? Ultimately we are outsourcing an increasing amount of compute stack management while moving closer to writing our own high-level application or business logic. We are writing in a more declarative way about our intent and desired outcomes. This is also where SecOps is moving towards. We are focusing on the workflows that leverage a range of specialized services and tools. We are shifting towards composing repeatable outcomes riding on top of trusted and untrusted fabrics. Consistent and integral responses are required not just from APIs but from our workflows. They should result in deterministic outcomes stemming from the same decision trees. Can you smoke test your security workflows end-to-end and easily simulate events that lead to an incident? Rather than waiting for an attacker or point in time penetration test, can you drill your digital procedures for consistent outcomes and adjust where necessary?

### Manual or A.I. Ops?

A.I. (Artificial Intelligence) has utility. It is not a panacea. The human fear of obsolescence mixed with rampant A.I. washing in the industry has resulted in hyper skepticism. This doubt is warranted and should be welcomed by vendors offering real-A.I. We already use A.I. daily in everything from search engines using NLU (Natural Language Understanding) and deep learning to EDR (Endpoint Detection and Response) malware detection. A.I. is ambiguous, it's an umbrella term for a set of technologies that mimic human intelligence. Machine Learning and Deep Learning are subsets with very useful applications, especially for certain problem spaces. Labeled data is commonly used in supervised learning (network protocols are well-labeled datasets). Unlabelled data is used in unsupervised learning and reinforcement learning uses rewards to constantly calibrate. The machine learning domain is vast and unfolding rapidly. Spotting real-A.I. versus snake-oil is a challenge but not an insurmountable one. Many fear the black box due to a lack of introspectability and explainability, so the power to surface raw datasets, features, and intermediary states, become the transparency challenge for engendering trust. A.I.-Ops provides a faster and more scalable OODA loop, but one that must overcome the trust issues that IPS (Intrusion Prevention System) faced when compared to IDS (Intrusion Detection System). Who is ultimately accountable and responsible for decision making and any resultant negative outcomes? There is a logical evolution from manual tasks, to automation, and then to augmentation and enhancement using A.I. SecOps is already an artificially enhanced and intelligent OODA loop, so the question is not when, but how much will we allow A.I. to drive?

### Bridging the Gap

There are no economies of scale if your team needs to grow linearly with the number of assets managed. Such a situation is not sustainable nor efficient. There is already a talent gap in Infosec and it's set to worsen. Freeing up human creativity from being stuck on security toil empowers teams to be more forward-looking, proactive, and nimble. A constrained talent pool means fewer people to deal with growing process and technology. This in itself becomes unsustainable without using force-multipliers such as smarter tools, automation, adaptable processes, and real-A.I.

SecOps may not manage all digital assets but must be able to at least observe them and investigate when necessary (including retrospectively). These activities all require orchestration and reach. Ever more complex logic and decision making must be executed rapidly, fast enough to identify and protect against an attacker's automation. There is an urgency that necessitates distributed human and machine OODA loops, both for incident response and threat hunting. Humans will continue to create and supervise, but may need to manage and operate less.

### The Meta-Security OS

People still make the most important decisions. Optimizing for the 'correct' or best decisions means optimizing around people. The human role in digital security is still manyfold and although certain forms of pattern recognition are best left to machines, others are not. Organizations primarily run on a meta-operating system composed of people, called culture. It's constantly patched, re-written, rebooted, sometimes vulnerable, but ever-evolving. To optimize for resilience and antifragility is to invest in people and culture. Where resources, skills, and experience are lacking, fostering a culture of constant learning and psychological safety is the best hedge against future risks. This is how one secures optimal outcomes.

---

## A Trust Experiment

### Your Risk is Your Risk

Everyone's personal and organizational risk tolerance is different (and subject to different contexts and constraints). In Infosec we traditionally operate from a risk-averse standpoint. This sometimes means we lag behind as disruptions overtake us. So, rather than try and espouse what you should do without knowing your exact situation, perhaps we could help to clarify your thinking by challenging you to map where your current risk tolerance and trust resides. A simple thought exercise?

<center>Put a mental tick in each box based on your current affirmative trust level ✔</center>

<div style="background-color: var(--card-bg, #fff); border-radius: 20px; padding: 24px 20px 20px 20px; width: 100%; margin-bottom: 32px;">
  <img loading="lazy" class="img-fluid" src="/images/bsoc_trust_100920.png" alt="Trust Experiment" style="border-radius: 12px; margin: 16px 0;">
</div>

<center><strong>Note:</strong> The above diagram is a simple mapping related to the OODA loop. It is designed to do one thing quickly, see
where your comfort level lies with regard to trusting people, process, and technology.</center>

---

## Key Takeaways

<div style="background: var(--card-bg, #fff); border-radius: 16px; padding: 20px; margin-bottom: 32px;">
  <ul style="font-size: 1.08em; color: var(--text, #333); line-height: 1.7;">
    <li>The traditional SOC is no longer fit-for-purpose, it must become more antifragile.</li>
    <li>Optimizing for change ensures adaptability and survival.</li>
    <li>The volume, velocity, and fidelity of data and events are set to grow not shrink.</li>
    <li>You can centralize much of the core technology platform, but the physical location is no more, it's distributed (towards the talent and towards the edge!).</li>
    <li>The staffing gap will continue, invest more in up-skilling existing teams.</li>
    <li>Interlock 'T' shaped skills in teams to form a lattice and leverage institutional knowledge.</li>
    <li>Optimize for security observability inc. active 'query-ability' around high cardinality events. (passive consumption of telemetry is not enough).</li>
    <li>Bring detection engineering closer to the data source. This helps with the flood of data by increasing the Signal-to-Noise Ratio (SNR) and reducing telemetry overheads.</li>
    <li>Leverage automation and real-A.I. for well-defined protocols, event states, and workflows.</li>
    <li>Pivot to measurable and demonstrable outcomes (hopefully aligned with OKRs and KPIs) with a focus on detection and response times.</li>
    <li>Embrace ephemerality as an ally, not as a foe. Plan for it head on, don't go around it.</li>
    <li>Leverage employees as intelligent sensors e.g. crowdsource event integrity and real time confirmations. Human in the Loop (HITL).</li>
    <li>Use what you have, build what you can, but always use (or buy) the best glue.</li>
    <li>Prioritize usage of 'API-first' platforms for integration, enhancement, and generative network effects.</li>
    <li>Identify or embed security champions in all operations teams.</li>
    <li>Best of Breed / Best in Class do fewer things better, while understanding and enabling ecosystems and interoperability.</li>
    <li>The single throat-to-choke is your own, as you can't outsource your business risk.</li>
    <li>'Culture-First' is your best hedge against the future.</li>
    <li>Did we mention up-skilling existing teams?</li>
  </ul>
</div>

---

## Final Thoughts

One size does not fit all. Model, adapt, and store your security workflow logic as code. Ensure it can be iterated on and evolved quickly - as this is your secret sauce, your domain-specific language, and your customizable OODA loop.

**Automate and assure.**

---

<div style="background-color: var(--card-bg, #fff); border-radius: 20px; padding: 20px; width: 100%;">
  <center>
    <a class="button" href="/contact" rel="noopener" title="Contact Defensible">
      <span class="button-inner">Contact Us</span>
    </a>
    or
    <a class="button" href="/beyond_the_soc_part_1" rel="noopener" title="Contact Defensible">
      <span class="button-inner">Back to Part 1</span>
    </a>
  </center>
</div>

---

**Author:** Donal O Duibhir, Security Architect, ~2020

---
