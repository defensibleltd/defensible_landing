---
title: "Beyond The SOC (Part 2)"
url: "/beyond_the_soc_part_2"
description: "Trajectories in security. Challenges in the present."
hidemeta: true
draft: false
cover:
  image: "/images/push_me_pull_me.png"
  relative: false
  alt: "A colorful illustration of observability and controllability"
  caption: "Is your own C2 a weakness with unlimited reach?"
---
<style>
.post-description {
  font-size: 1.5em; color: var(--text, #666);
}
</style>

## The Present

### Volume and Velocity

At a macro level, the concept of a SOC is a system with inputs, processes, and outputs. It watches and controls aspects of another larger system, your organization. It is an OODA (Observe, Orient, Decide, Act) loop with interfaces that touch people, process, and technology. SecOps have the power to observe and control. The volume and scope of inputs in conjunction with the speed and accuracy of this OODA loop define the limits of your security observability and controllability.

Lifecycle management and the evolution of an organization mean that assets, interfaces, and systems change frequently over time. The traditional SOC was an inflexible stub with tightly coupled dependencies and point solutions. Onboarding new log stream formats or detection capabilities took days and weeks, rather than minutes and hours.

### Late to the Game

Security monitoring has traditionally been reactive, signature-based, and thresholds that generated events that roll up to dashboards leaving humans to attempt to figure out what's next. SOPs (Standard Operating Procedures) and playbooks were manually triggered and 'adhered' to by human operators and analysts. Scripts were run to slowly stitch together some semblance of situational awareness which left no time for proactive measures or prowling the shrinking perimeter.

### Burnout and Fatigue

Humans have an upper cognitive bound for processing information and symbols. Once exceeded we become ineffective, make mistakes, and require rest to reboot. We can not digest multiple information streams in parallel and are unable to manually refine raw data at scale. We can however create, write, and debug logic that fans out across wider surfaces (though some would argue not very well!). To have a security analyst manually responding to alerts including orienting and deciding what to do next is not scalable or realistic. Multiple analysts represent a common mode failure (they exhibit shared vulnerabilities) which then becomes a 'single' point of failure in the system.

Alert fatigue translates to false negatives and false positives. Further, a lack of agency to improve and control the system you're embedded in leads to burnout and churn. As things speed up, removing bottlenecks is key (and there's no room for any 'hero-complex'). The question then must be asked, where in the digital security OODA loop are humans fit-for-purpose and an asset, rather than a Mechanical Turk like liability? Far from considering humans to be widgets, it's time to take another hard look at the operational security activities that are best fit for our human reasoning and creativity.

### Change is Constant

Security is a continuous process in the face of ongoing internal and external change. If only for a moment, how would you take an accurate snapshot of the security of your organization? Would it involve a system-wide freezing of all states encompassing humans, processes, machines, interfaces, and all running code? This snapshot would be an ephemeral and fleeting state, almost immediately invalidated. Additionally, digital dependencies increasingly fall outside of the organization and are subject to multiple interwoven supply-chains. So, does total information awareness require omniscience and the total heat death of the universe, or can we learn to embrace change?

### Daedalus or Icarus

Infosec on one hand is learning from and leveraging useful DevOps approaches to automation and orchestration, yet attempts to give each host or service its own unique protection profile creates even more challenges. Micro-segmentation can work if everything is automated end-to-end, but then inspecting, maintaining, and troubleshooting this automation logic (and curating its lifecycle) incurs additional overheads and operational ‘taxes'. There is a balance between open and closed, grouping, and segmenting. Supervising humans must still be able to reason about overall risk, trust, and dependencies, whilst retaining a veto on certain decision paths and resultant automated actions. Grouping assets based on attributes and characteristics like risk rating, is still a valid approach to managing complexity.

<div style="background-color: var(--card-bg, #fff); border-radius: 20px; padding: 24px 20px 20px 20px; width: 100%; margin-bottom: 32px;">
  <img loading="lazy" class="img-fluid" src="/images/volume_overload.png" alt="Volume and overload" style="border-radius: 12px; margin: 16px 0;">
</div>

### Seeking Compliance

We know security is not compliance, and compliance is not security, but consistent and constant compliance form the bedrock that security teams require to build on and be effective. In the quest to protect an entity, can we actually prevent all harm (subject to constraints and available resources)? What is demonstrable for compliance sake and are there truly any acceptable losses or error budgets for security? If security teams could embrace internal and external regulatory requirements and constraints would this breed innovation? Most organizations seek to reduce overheads related to compliance while enabling an organization to adapt more quickly, but behavior change and process optimization tends to become harder over time (and even more so at scale). Adaptation, not just to threats, but to business needs, mean security itself needs to be more malleable when necessary and antifragile by default. Can security operations facilitate frictionless intra-team collaboration especially when asking other teams to demonstrate their own compliance?

### Practice, Profit, Power

Every organization is a target in some way. Your compute and data are worth something to someone somewhere, but who exactly? Connectivity has utility but what is this access worth. Threat actors include those learning and practicing their attack skills on your organization, those attempting to monetize you or your assets, and those using you as a stepping stone to other organizations (part of loftier geo-political power plays or nation-state goals). We like to try and steer clear of F.U.D. (Fear, Uncertainty, and Doubt) but just as there is climate change and weather, there is IBN (Internet Background Noise) and those using connectivity to further their nefarious activities. Defending against two out of three is better than none out of three. When script-kiddies and criminals are automating at scale maybe we should be too.

### Jiu-Jitsu

If we make our organization robust but brittle, they actually becomes less resilient to attack. It ossifies, unable to react, change, and adapt. If we constrain it too much, we are actually contributing to its demise. This is an undesirable outcome (and one we are fundamentally tasked to prevent). By optimizing for change, we optimize for culture and a technological fabric that allows for protection but is pliable enough to adapt. This adaptivity must also include our workflows, processes, and procedures. This is where the backbone of SecOps orchestration capabilities are key. With power and flexibility, loose coupling beats tight coupling. Speed and agility ensure better responses and outcomes, which result in increased survivability particularly during disruptive periods.

### Sliding Windows of Risk

Windows of exposure open and close. Minimizing risk in a shifting environment is an ongoing endeavor. It's not just managed assets in a private or public cloud at stake, there are physical access edges and user endpoints too. There are cameras and sensors, building management control systems and SCADA related enclaves. Devices may not all be managed by you, their flows may be controllable, at source, in transit, or maybe not at all. Differing zones and populations of devices grow and shrink. SaaS (Software as a Service) may be a clean consumption model but it's still someone else's stack. Constantly enumerating this morphing footprint of assets and services (while independently verifying it) is a challenge. Not everything auto-registers and Bring Your Own Device (BYOD) and Shadow I.T. don't count as Zero-Touch Provisioning! Ongoing asset and service discovery is a precursor for most forms of observability and detection.

### Ephemeral Echoes

In this new age of elasticity, hosts can no longer be counted on to be persistent and long-lived. Under the hood much is shifting, changing, and constantly migrating. More and more digital assets are ephemeral and intentionally so. This ephemerality might seem to raise the bar on both sides of the house, but as always, it depends. As we create more containers, we create more surfaces and boundaries to inspect. Attackers don't always seek or require a persistent foothold. If our ally rather than our foe, then we could close these sliding windows of risk faster and keep them shut. Opportunities involve tracking 'Best Current Practice' yet they are no longer centralized in IETF archives. Falling behind means continuing to repeat old mistakes. As always decisions are contingent on multiple factors and constraints. The underlying assumption (another elephant in the room) is that your culture, people, and process are optimized for, and ready for change. What is your SecOps team mean time for asset discovery and is it approaching → zero?

---

<div style="background-color: var(--card-bg, #fff); border-radius: 20px; padding: 20px; width: 100%;">
  <center>
    <a class="button" href="/beyond_the_soc_part_1" rel="noopener" title="Part 2">
      <span class="button-inner">Back to Part 1 (The Past)</span>
    </a>
    <a class="button" href="/beyond_the_soc_part_3" rel="noopener" title="Part 3">
      <span class="button-inner">Read Part 3 (The Future)</span>
    </a>
  </center>
</div>
