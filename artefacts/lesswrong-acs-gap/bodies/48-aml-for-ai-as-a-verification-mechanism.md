# AML for AI as a verification mechanism

- URL: https://www.lesswrong.com/posts/AMTx3EBBgyGc32tKH/aml-for-ai-as-a-verification-mechanism
- Author: MarkelKori
- Date: 2026-06-13
- Karma: 9  Comments: 2  Words: 527
- Band: B  Tier: 2  Score: 33.8  Density: 9.49
- Anchors: \bmcp\b

---

The idea is to build a system that tracks key nodes in AI infrastructure in order to detect preparation for, or execution of, large training runs, and to monitor the overall situation more generally. In the future, if or when an international agreement limiting AI development appears — for example, via limits on FLOPs per training run ; the EU AI Act already uses a threshold of around 10²⁵ FLOPs for GPAI models with systemic risk[^6fdsex274h3], and providers are required to notify the AI Office without undue delay — such a system could be used to detect rogue data centers and hidden training runs.

Something similar either already exists or is being developed. As far as I know, one example is the SemiAnalysis AI Datacenter Model[^rrkcmmvv3v], although it is only available for a large amount of money. Some acquaintances of mine from Ukraine created an MCP[^q342iwalmzq] for the government public procurement website, with the goal of estimating the amount of compute capacity in the country.

For myself, I call this idea “AML for AI.” The analogy seems similar to me: we collect as much information as possible related to the domain of interest and try to combine it into a unified picture, instead of seeing only scattered fragments. This project would probably require a large number of people and significant funding, but people who are interested in it can start with MVP.

All information would be collected from open sources / OSINT.

What could we track? I should honestly say that I took the answers to “how” from GPT. Please do not treat them as a ready-made list of actual sources to monitor, but rather as examples.

1.  **Legal**: legal entities, shell companies used for procurement and leasing, ownership chains, the appearance of new suspicious companies or organizations, and so on.

**How**: OpenCorporates, OpenSanctions.

2.  **Hardware procurement**: GPUs, memory, racks, cooling, generators.

**How**: TED (Tenders Electronic Daily), SAM.gov Contract Opportunities.

3.  **Logistics**: import/export of server equipment, splitting orders between companies.

**How**: ImportGenius, Panjiva.

4.  **Construction**: building permits, leasing of new sites, upgrades to electrical and cooling infrastructure.

**How**: OpenStreetMap, NASA FIRMS, US Census Building Permits Survey.

5.  **Energy**: anomalous increases in electricity consumption, grid connection requests.

**How**: EIA Electricity Data Browser, FERC.

6.  **Hiring**: the appearance of relevant job openings, searches for data center employees / programmers, etc.

**How**: Greenhouse job boards, Lever job sites.

7.  **Satellite data**: expansion of existing sites, appearance of new buildings.

**How**: Copernicus Browser / Copernicus Data Space.

8.  **Water consumption.**

**How**: USGS Water Data, EPA ECHO + NPDES monitoring data.

All of this could be organized into a network of connected elements, making it possible to identify interacting entities and potentially detect hidden construction or model training. Such a system could become the basis for a more advanced high-level system in the future, acting as a verifier for international AI agreements.

As I present it here, the idea is still very raw, and I have spent very little time thinking it through. I suspect that people with a deeper understanding of AI infrastructure and policy would be much better suited to develop it.

[^6fdsex274h3]: https://artificialintelligenceact.eu/gpai-guidelines-overview/ 

[^rrkcmmvv3v]: https://semianalysis.com/datacenter-industry-model/ 

[^q342iwalmzq]: https://github.com/VladyslavMykhailyshyn/prozorro-mcp-server