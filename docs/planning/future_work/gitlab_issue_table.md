# GitLab Issue Planning Table

This table provides a compact view of the current training-platform work plan.
All issues start on a Thursday and are due the following Thursday.

| Issue Title | Status | Start Date | Due Date | Epic | Milestone | Category | Dependencies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Define first local tray module | planned | 2026-05-07 | 2026-05-14 | Training Module | Local Tray Data Ready | data | none |
| Add instrument cards with aliases and distinguishing features | planned | 2026-05-07 | 2026-05-14 | Training Module | Local Tray Data Ready | content | Define first local tray module |
| Add tray template quantities and distractors | planned | 2026-05-07 | 2026-05-14 | Training Module | Local Tray Data Ready | content | Define first local tray module |
| Build study-card view | planned | 2026-05-14 | 2026-05-21 | Training Module | Study And Quiz Flow Ready | ui | Add instrument cards with aliases and distinguishing features |
| Build identification quiz flow | planned | 2026-05-14 | 2026-05-21 | Training Module | Study And Quiz Flow Ready | ui | Add instrument cards with aliases and distinguishing features |
| Record quiz correctness, duration, and confidence | planned | 2026-05-14 | 2026-05-21 | Training Module | Study And Quiz Flow Ready | metrics | Build identification quiz flow |
| Build simulated tray sorting task | planned | 2026-05-21 | 2026-05-28 | Training Module | Practice Sorting Feedback Ready | ui | Add tray template quantities and distractors |
| Implement missing/extra/wrong/misidentified/wrong-count scoring | planned | 2026-05-21 | 2026-05-28 | Training Module | Practice Sorting Feedback Ready | scoring | Build simulated tray sorting task |
| Add practice-mode feedback | planned | 2026-05-21 | 2026-05-28 | Training Module | Practice Sorting Feedback Ready | ui | Implement missing/extra/wrong/misidentified/wrong-count scoring |
| Build pre-test assessment mode | planned | 2026-05-28 | 2026-06-04 | Training Module | Pre/Post Assessment Ready | assessment | Build simulated tray sorting task |
| Build post-test assessment mode | planned | 2026-05-28 | 2026-06-04 | Training Module | Pre/Post Assessment Ready | assessment | Build pre-test assessment mode |
| Suppress hints and feedback during assessment modes | planned | 2026-05-28 | 2026-06-04 | Training Module | Pre/Post Assessment Ready | assessment | Build pre-test assessment mode |
| Export learner metrics | planned | 2026-06-04 | 2026-06-11 | Evidence And Reporting | Metrics Export Ready | reporting | Build post-test assessment mode |
| Generate pre/post learner summary | planned | 2026-06-04 | 2026-06-11 | Evidence And Reporting | Metrics Export Ready | reporting | Export learner metrics |
| Add literature-gap and stakeholder slide content | planned | 2026-06-04 | 2026-06-11 | Evidence And Reporting | Literature Gaps And Stakeholders Ready | docs | none |
| Write pilot walkthrough script | planned | 2026-06-11 | 2026-06-18 | Pilot Evidence | Pilot Walkthrough Ready | study | Build post-test assessment mode |
| Run pilot walkthrough and record confusion points | planned | 2026-06-11 | 2026-06-18 | Pilot Evidence | Pilot Walkthrough Ready | study | Write pilot walkthrough script |
| Add limitation note about non-SPD participants | planned | 2026-06-11 | 2026-06-18 | Pilot Evidence | Pilot Walkthrough Ready | docs | Run pilot walkthrough and record confusion points |
| Lock final demo narrative | planned | 2026-06-18 | 2026-06-25 | Presentation | Demo Narrative Ready | demo | Generate pre/post learner summary |
