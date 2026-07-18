<div align="center">

### <code>wassim@casablanca:~$ whoami</code>

<img src="./assets/ascii-portrait.svg" width="360" alt="Coat of arms of Morocco, rendered in ASCII">

<img src="./assets/info-card.svg" width="520" alt="Wassim Lazim — location, studies, stack and shipped work">

<br>

### <code>wassim@casablanca:~$ ./contributions.sh</code>

<img src="./assets/contrib-heatmap.svg" width="880" alt="Contribution graph, regenerated daily">

</div>

<br>

### <code>wassim@casablanca:~$ ls -lh ~/shipped</code>

Software engineering student in Casablanca. I'd rather ship one thing people
actually use than five tutorials, so everything below is in production or
headed there.

| | | |
|---|---|---|
| **[swhnegoce.ma](https://swhnegoce.ma)** | B2B storefront for hygiene supplies, workwear and IT equipment. Live, taking real quote requests, 130+ catalogued products. | `Next.js` `Sanity` `Vercel` |
| **SwhOffice** | Desktop invoicing built ahead of Morocco's DGI e-invoicing reform — clearance state machine, sequential official numbering, client snapshots at finalisation, ICE/IF/RC checksum validation. | `Tauri` `Rust` `React` `SQLite` |
| **[CDC pipeline](https://github.com/Wvssim/cdc-streaming-pipeline)** | Change-data-capture fan-out: one Postgres write feeds five independent consumers — audit, notification, blockchain, OCR, SIEM — with no coupling between them. | `Debezium` `Kafka` `Spring Boot` `Angular` |
| **[ISO 8583 load-test](https://github.com/Wvssim/iso8583-jmeter-loadtest)** | ISO 8583 load-testing bench in JMeter — authorisation client and server, timestamped jPOS traces with PAN masking, and an auto-generated transaction report. | `JMeter` `jPOS` `Java` |
| **[EMSI RAG assistant](https://github.com/Wvssim/Emsi-rag-assistant)** | Local retrieval-augmented assistant over EMSI's academic docs — contextual answers grounded in the source brochure, nothing leaves the machine. | `Python` `LangChain` `ChromaDB` `Groq` |
| **[Smart irrigation](https://github.com/Wvssim/Smart-Irrigation-System-iot)** | Soil-moisture-driven irrigation with real-time supervision, configurable watering logic, a REST API and a live dashboard. | `Flask` `MongoDB` `Charts.js` |

### <code>wassim@casablanca:~$ git log --author=Wvssim --oneline /oss</code>

- **[presenton/presenton](https://github.com/presenton/presenton)** — fixed an
  `OSError` on export when filenames exceed the filesystem byte limit
  (long CJK titles) via a `safe_export_basename()` helper; plus a
  troubleshooting section for the setup issues that kept resurfacing in issues.

<div align="center">

### <code>wassim@casablanca:~$ cat stack.txt</code>

<img src="https://img.shields.io/badge/TypeScript-0F0B18?style=flat-square&logo=typescript&logoColor=EDE9F7" alt="TypeScript">
<img src="https://img.shields.io/badge/Next.js-0F0B18?style=flat-square&logo=nextdotjs&logoColor=EDE9F7" alt="Next.js">
<img src="https://img.shields.io/badge/React-0F0B18?style=flat-square&logo=react&logoColor=EDE9F7" alt="React">
<img src="https://img.shields.io/badge/Angular-0F0B18?style=flat-square&logo=angular&logoColor=EDE9F7" alt="Angular">
<img src="https://img.shields.io/badge/Rust-0F0B18?style=flat-square&logo=rust&logoColor=EDE9F7" alt="Rust">
<img src="https://img.shields.io/badge/Tauri-0F0B18?style=flat-square&logo=tauri&logoColor=EDE9F7" alt="Tauri">
<br>
<img src="https://img.shields.io/badge/Java-0F0B18?style=flat-square&logo=openjdk&logoColor=EDE9F7" alt="Java">
<img src="https://img.shields.io/badge/Spring-0F0B18?style=flat-square&logo=spring&logoColor=EDE9F7" alt="Spring">
<img src="https://img.shields.io/badge/Python-0F0B18?style=flat-square&logo=python&logoColor=EDE9F7" alt="Python">
<img src="https://img.shields.io/badge/Kafka-0F0B18?style=flat-square&logo=apachekafka&logoColor=EDE9F7" alt="Kafka">
<img src="https://img.shields.io/badge/PostgreSQL-0F0B18?style=flat-square&logo=postgresql&logoColor=EDE9F7" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Docker-0F0B18?style=flat-square&logo=docker&logoColor=EDE9F7" alt="Docker">

<br><br>

### <code>wassim@casablanca:~$ ./links.sh</code>

<a href="https://www.linkedin.com/in/wassim-lazim-124aa935b"><img src="https://img.shields.io/badge/LinkedIn-8B5CF6?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://swhnegoce.ma"><img src="https://img.shields.io/badge/swhnegoce.ma-A78BFA?style=for-the-badge&logo=nextdotjs&logoColor=0F0B18" alt="swhnegoce.ma"></a>
<a href="mailto:wassim.lazim3@gmail.com"><img src="https://img.shields.io/badge/Email-0F0B18?style=for-the-badge&logo=maildotru&logoColor=EDE9F7" alt="Email"></a>

<br>

<sub>Open to freelance work and internships in data engineering.</sub>

</div>

<!--
─────────────────────────────────────────────────────────────────────────
Regenerating the art
─────────────────────────────────────────────────────────────────────────
  assets/ascii-portrait.svg   python scripts/make_ascii.py photo.jpg
  assets/info-card.svg        python scripts/make_info_card.py
  assets/contrib-heatmap.svg  GITHUB_TOKEN=… python scripts/make_heatmap.py

The heatmap and info card are rebuilt daily by
.github/workflows/update-profile-art.yml — see SETUP.md for the one secret
it needs. Palette lives in scripts/palette.py; change it there and every
asset follows.
-->
