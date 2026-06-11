# TrayGuard — Elevator Pitch Script

**Duration**: ~3:45  
**Target audience**: Hospital administrators, SPD managers, surgeons  
**Tone**: Product commercial, not design review

---

### 0:00 – Problem (45 sec)

Surgical trays can arrive at the operating room wrong or incomplete. Missing instruments. Wrong sizes. Damaged tools.

Published evidence reports 9 defects per 100 surgical cases. 55 percent of those happen during assembly — when a technician is visually identifying, sorting, and counting instruments by hand. When an error occurs, the delay averages to 10 minutes. That costs a single hospital an estimated 6 to 9 million dollars in lost OR time annually.

This is not a counting problem. It is a visual discrimination problem. A Kelly clamp and a Crile clamp differ only by how far the serrations run along the jaw. You cannot easily tell them apart at a quick glance. In one study, 44 percent of packaging errors were of wrong specification — the right instrument family, but the wrong variant. The total count was correct. The specific instrument was wrong.

Certification tests assess general instrument knowledge, but they do not cover the local names, aliases, and tray-specific rules that vary by hospital. Studies find certified sterile-processing professionals score as low as 41 percent on novel local tasks. The local tray knowledge that TrayGuard targets is learned separately from certification.

---

### 0:45 – CV failure (30 sec)

We started by trying to build a camera that would catch these errors automatically. We ran seven experiments to simulate real-world conditions to stress test the computer vision model. This included varying brightness, background reflectivity, and layout occlusion. Every condition degraded performance. When instruments overlapped in a tray, accuracy dropped by more than half. Additionally, due the limited amount of data we collected, the model learned to memorize instrument positions, not instrument shapes.

We learned that deployment-grade recognition would require site-specific data for every hospital, cross-manufacturer validation for every instrument, and institutional adoption. We cannot build a generalizable CV model in a single project.

---

### 1:15 – TrayGuard (1 min 15 sec)

So we built TrayGuard — a training platform that works with what every hospital already has: a laptop and a printer.

Each instrument gets a printed card with an AprilTag marker. The learner goes through a structured 7-step loop: pre-test, retrieval-first study cards, a quiz, a simulated tray sort using the physical cards, and a post-test. Each step is backed by learning-science evidence — retrieval practice, immediate feedback, confidence capture.

The camera scans which cards are on the table. The scoring engine classifies every selection into six categories that map directly to the published literature: correct, missing, extra, wrong, misidentified, and wrong count. After each sort, the learner rates their confidence, separating two very different failure modes — high-confidence errors mean someone is confidently wrong, low-confidence correct answers mean fragile knowledge that might not survive a week.

No special equipment. No hospital deployment required.

---

### 2:30 – Durable artifact (30 sec)

The core output is not the app. It is the tray module — a file that captures the local names, aliases, lookalike pairs, distinguishing features, and tray-specific counts for one hospital tray. That local knowledge is what every solution needs — whether it is training now or automated checking later. The training loop builds it at low cost.

This is the same pattern as computer vision annotation standards like COCO and Pascal VOC — formats created by university teams that became industry references because the structure was sound and the tooling worked.

---

### 3:00 – Next steps (45 sec)

The prototype is built. The study protocol is designed. We have not run a pilot yet — that is the next step.

The goal is straightforward: can a technician — even one who holds certification — improve on a simulated local tray task in one 60-minute session, and do those gains persist after weeks and months? If yes, that is measurable value for a workforce that already passed the exam but still makes errors daily. If the answer is no, that is useful evidence too.

We are looking for a hospital partner to pilot the first module with real tray content. The problem is documented. The tool is ready. The next step is putting it to work.

---

**Total**: ~3:45
