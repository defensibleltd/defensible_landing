There are 3-4 main IPAM alternatives i.e. Microsoft Excel, Microsoft IPAM, Solarwinds, OSS projects

# E.g. Why use Micetro vs Microsoft IPAM
* Single global IPAM can be used across multiple forests e.g. multiple prod, multiple test 
* Future-proofed overlay that is DNS and DHCP agnostic
* Fine grained RBAC (over and above configuring limited GPOs)
* Choice of database (PostgreSQL, SQLite, MS SQL)
* Centralized auditing and logging (without additional configuration of servers)
* No limits to numbers of DHCP servers, scopes, DNS servers, or zones
* Utilization and trending across both IPv6 and IPv4
* Next free address across IPv6 and IPv4
* Discovery and scanning of IPs across routers and switches

# IDC Report Highlighted Incumbents

* Solarwinds
* Microsoft IPAM or Spreadsheets (Excel)?
  * It's not actually clear as it just says "Microsoft" in places (Pg.23)
* Open Source IPAM? (Which one: Netbox, NPIP, phpIPAM?)

**Note:** There's a lot to dig in to in the IDC report ("Men & Mice SMB DDI Survey") but I would challenge the familiarity with the term "DDI" (especially at the lower end of the market, love to see a breakdown on that one!)

**Note_II:** The IDC report is also not clear what facets of security relate to DDI? IR(Inicident Response), IP enrichment, micro-segmentation/policy enforcement, general SSoT/SoR?

**Note_II:** There also seems to be some ambiguous use of SSoT(Single Source of Truth) and SoR (System of Record)

**Note_III:** I found this Tines report very inspiring: [Voice of the SOC Analyst 2023](https://www.tines.com/reports/voice-of-the-soc-2023) in terms of content, presentation, and medium.
