---
title: "Beyond The SOC (Part 1)"
url: "/beyond_the_soc_part_1"
description: "Trajectories in security. Challenges of the past + status quo."
hidemeta: true
draft: false
cover:
  image: "/images/observability_busytown.png"
  relative: false
  alt: "A colorful illustration of observability and controllability"
  caption: "More defenders busywork!"
---
<style>
.post-description {
  font-size: 1.5em; color: var(--text, #666);
}
</style>

## Introduction

The Security Operations Centre (SOC) as we know it is a thing of the past. The SOC is not dead but is being reborn to avoid becoming obsolete. A SOC is an operational overlay of people, process, and technology built on your security model. When the environment and threat landscape changes, your security model must adapt and evolve, and so too must the SOC.

This operational overlay runs its own OODA (Observe, Orient, Decide, Act) loop. At its nexus is decision making. Decisions must be made rapidly. Supporting capabilities must evolve constantly. As the volume and velocity of your data and services multiply, so too do the digital surfaces that require protection.

Human and machine roles are shifting further towards their respective strengths, while still continuing to augment one other. Accelerating events are outpacing and overwhelming legacy architectures. On one side we are asked to do more with less, yet for human Security Operations (SecOps) to become sustainable, the irony is that we, as humans, must figure out how to do less with more. We must leverage new tools, patterns, and technologies to help us observe, orient, decide, and act faster.

Increased observability and better signals mean we can translate events to better outcomes. New hybrid strategies are emerging, ones that surveil ever more deeply and police ever closer to data sources. Those who can tame this growing complexity and velocity forge virtuous cycles not just for themselves but for their colleagues and teams.

Organizations also require this new protective overlay system to be antifragile, to improve and evolve ever more rapidly than before. Sentient attackers and digital contagion know no borders and continue to exploit human and machine vulnerabilities. As our information-rich circulatory systems pump digital value around an organization, how we respond to threats means the difference between barely keeping the lights on or thriving.

Cyber, as a domain of conflict, is one of the fastest-growing and accelerating spaces. It's one we all depend upon daily, one we can not afford to reject or ignore. For SecOps, there is increasingly no discrete or distinct center of operations. Resources, workflows, and defenses are elastic and unevenly distributed. So, as noble defenders, symbiotic with our technology, we must also adapt to our new environments and realities.

The economics of defense are being rewritten once more. As always it comes down to the survival of the 'fittest'. Time is of the essence and trust is the fulcrum. The future is distributed and physically SOC-less, so what is it we should be optimizing for?

> "Antifragility is beyond resilience or robustness. The resilient resists shocks and stays the same; the antifragile gets better."
> <em>— Nassim Nicholas Taleb</em>

---

## The Past?

### On Measuring Security

Before we start, let's call out the elephant in the room, that of measuring 'digital' and security-related risk. There is a lack of agreed, standardized, and easily measured security metrics. Security is traditionally a negative sell prone to F.U.D. (Fear, Uncertainty, and Doubt) mixed with snake-oil in little black boxes. Digital assets and services are malleable and perfectly replicable. This alters concepts like scarcity and intrinsic value. Security is a process. Security is a quality. Security is protection from harm and minimizing real rather than perceived risk. 

> "Security is the absence of unmitigatable suprise" 
> <em>— Dan Geer </em>

Get your head around that one! So what is it we are defending and why?

### Protecting Value

The digital realm supports real-world outcomes. We understand multiple types of value are produced and transit our organizations. Networks and systems weave the fabrics that provide the paths to value. This value can reside in silos (data at rest) but when in motion, is provided as flows for the ultimate use by actors (employees, contractors, guests, customers etc) and agents.

Value is created and consumed. We endeavor to protect this value from threats and harm. Threats are real, observable, and arise from a wide range of actors and agents. Threats can be automated or manual, local or remote, sentient, or mindless.

Measuring digital security in a networked world is not unachievable, it just requires new and complex maths and metrics for factoring in transitive trusts. In the interim, we group and grade, scan and categorize, differentiate, record, and prioritize as best we can. At its core, I.T. is asset and change management and SecOps must facilitate change, not block it, for the macroorganism to survive.

### Taxonomy as Tax

To reason about assets, one has to identify the similarities and differences between each. For operations to attribute some semblance of risk; assets, events, and incidents require classification ratings. This enables the correct procedures or responses to happen. One size does not fit all, so there must be tagging and the differentiation between herds of 'cattle' and any sized cluster of 'pets' is a bone of contention. The earth, and indeed the network, is not flat. A single herd (monoculture) shares vulnerabilities and can experience common mode failures. A zoo with one animal per enclosure creates immense overheads and complexity, moving work elsewhere, away from prying eyes. Micro-segmentation of our example groups of animals is expensive and does damage to their health as is factory farming in a super lot. Neither are resilient.

Micro-segmentation actually results in more pets, not cattle. Just like the imaginary 'Push Me Pull Me', there is a difference between back-end homogenous command and control channels and front-end unique service paths. Our resources are limited and decision making depends on priorities, severities, classifications, and the grouping of similar attributes. Taxonomies are hard, they are a tax, a feature overhead, not a bug.

### Transitive Trust

If A trusts B (A→B) but B trusts C (B→C) so now A implicitly trusts C (A→B→C). 

However, trust is not always an all or nothing proposition. Trust paths exist throughout code, interfaces, systems, networks, and people. These trusts are also seen by some as vulnerabilities and often exploited by attackers.

Organizationally we move sliders between open and closed, trusted and untrusted. We apply guardrails, partition failure domains, and attempt to manifest protection policies. Flows are opened to provide access to value and facilitate collaboration. Authorized entities execute workflows based upon attribution of identity. We extend limited trust or default to no (or zero) trust. We can refine trust to 'least privilege' but sometimes workloads move elsewhere and permissions or policies don't follow. We also need to know when it is time to revoke trust and especially when events accelerate out of normal tolerances.

Transitive trusts are the glue that holds society together. Zero trust, on the other hand, can be expensive, and is usually reserved for high-risk untrusted environments - though with increased automation, it is seen as a more secure starting point for many scenarios. The SOC itself has traditionally been a trusted nexus, one that ironically shouldn't be beyond healthy forms of doubt itself.


---

<div style="background-color: var(--card-bg, #fff); border-radius: 20px; padding: 20px; width: 100%;">
  <center>
    <a class="button" href="/beyond_the_soc_part_2" rel="noopener" title="Part 2">
      <span class="button-inner">Read Part 2 (The Present)</span>
    </a>
  </center>
</div>
