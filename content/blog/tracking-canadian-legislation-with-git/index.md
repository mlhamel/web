+++
title = "Law as Code: Tracking Canadian Parliamentary Bills with Git and LEGISinfo"
date = 2026-08-24
description = "How civican/legisinfo turns the Parliament of Canada's open data into a versioned Git repository where MPs and Senators are the commit authors and git diff reveals the evolution of laws."
[taxonomies]
tags = ["civic-tech", "open-source", "git", "python", "parliament", "data-engineering"]
+++

Understanding how legislation evolves in parliament is notoriously difficult. When a bill moves through the House of Commons and the Senate—from **First Reading** to **Committee Stage**, **Third Reading**, and **Royal Assent**—clauses are rewritten, exceptions are added, and crucial provisions are quietly deleted.

Historically, tracking these changes required manual side-by-side comparisons of massive PDF documents and cross-referencing parliamentary _Hansard_ transcripts.

In the [Civican](https://github.com/civican) project, we asked a fundamental question: **What if we treated legislation like software source code, and parliamentary democracy like Git?**

The result is **[`civican/legisinfo`](https://github.com/civican/legisinfo)**: a structured, version-controlled repository of Canadian federal legislation where **every Git commit author is the actual Member of Parliament or Senator** responsible for that iteration of the bill.

Here is how the project works, how `civican-scraper` builds this history, and why using Git as a legislative database unlocks transparency for journalists, researchers, and citizens.

---

## The Concept: Law as Versioned Source Code

In software engineering, version control systems like Git allow us to inspect every change made to a codebase: who made the change, when it occurred, and the exact lines added or deleted (`git diff`).

Parliamentary law operates on the exact same principles of incremental mutation:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            PARLIAMENTARY LIFECYCLE                          │
│                                                                             │
│  [1st Reading]  ──►  [2nd Reading]  ──►  [Committee Stage] ──► [Royal Assent]│
│   Introductory        Debate &            Clause-by-Clause        Final Law  │
│      Draft           Principles              Amendments            Enacted   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CIVICAN/LEGISINFO GIT HISTORY                      │
│                                                                             │
│  Commit A             Commit B            Commit C            Commit D      │
│  Author: MP/Sponsor   Author: Minister    Author: Committee   Author: Crown │
│  "Bill Text: 1R"      "Bill Text: 2R"     "Amendments"        "Royal Assent"│
└─────────────────────────────────────────────────────────────────────────────┘
```

By ingesting structured XML data from the Parliament of Canada's **LEGISinfo** open data portal, `civican/legisinfo` reconstructs the history of parliamentary sessions (from the 35th Parliament through the current 45th Parliament) into clean Markdown documents (`bill_text.md`) and metadata records.

---

## Real Parliamentary Commits

Instead of generic bot commits, `civican/legisinfo` sets the Git commit author name, official parliamentary email, and commit timestamp to match the politician or minister who tabled the bill or amendment:

```bash
$ git log -n 4 --format="commit %h%nAuthor:  %an <%ae>%nDate:    %ad%nSubject: %s%n"

commit 4ee53b987
Author:  Minister of National Defence David J. McGuinty <minister.of.national.defence.david.j.mcguinty@parl.gc.ca>
Date:    Thu Jun 18 11:45:00 2026 -0400
Subject: Bill C-11: Royal Assent text update

commit 06bee62bc
Author:  Minister of Finance and National Revenue François-Philippe Champagne <minister.of.finance.and.national.revenue.franoisphilippe.champagne@parl.gc.ca>
Date:    Thu Jun 18 19:49:00 2026 -0400
Subject: Bill C-30: Royal Assent text update

commit d47d5a021
Author:  Senator Margo Greenwood <margo.greenwood@parl.gc.ca>
Date:    Thu Jun 18 13:30:00 2026 -0400
Subject: Bill S-250: Metadata update

commit 9948ba9e3
Author:  Minister of Transport Steven MacKinnon <minister.of.transport.steven.mackinnon@parl.gc.ca>
Date:    Thu Jun 18 11:45:00 2026 -0400
Subject: Bill C-25: Royal Assent text update
```

---

## Viewing Legislative Diffs: `git diff` for Democracy

Because bill texts are converted into normalized, human-readable Markdown (`bill_text.md`), any developer or citizen can use standard Git commands or GitHub's web interface to inspect the exact textual mutations between readings.

For example, comparing Bill C-11 (_An Act to amend the National Defence Act_) between its First Reading and Second Reading:

```diff
$ git diff dd86f90..063e8f4 -- 45-1/bills/C-11/bill_text.md

@@ -14,9 +14,9 @@

-remove the court martial's jurisdiction to try a person in relation to an offence under the `Criminal Code` that is alleged to have been committed in Canada and that is of a sexual nature or committed for a sexual purpose;
+remove the court martial's jurisdiction to try a person in relation to an offence under the `Criminal Code` that is alleged to have been committed in Canada and that is of a sexual nature or committed for a sexual purpose and provide for exceptions;

-remove the Canadian Armed Forces' authority to investigate an offence under the `Criminal Code` that is alleged to have been committed in Canada and that is of a sexual nature or committed for a sexual purpose;
+[*Deleted*]

 expand the class of persons who are eligible to be appointed as a military judge;
```

In a fraction of a second, the diff reveals crucial legal shifts:

1. An exception was introduced to the court martial jurisdiction clause.
2. The clause removing the Canadian Armed Forces' authority to investigate specific offences was completely deleted.

---

## Powerful Civic Analytics with Standard Developer Tools

By structuring civic data as a Git repository, we gain access to decades of built-in Git tooling:

### 1. `git log --author`: Track an Elected Official's Legislative Output

Want to analyze every legislative contribution by a specific minister or MP?

```bash
git log --author="François-Philippe Champagne" --oneline
```

### 2. `git blame`: Find Who Introduced a Specific Sub-clause

Run `git blame` on any clause in `bill_text.md` to see which reading introduced that wording and which MP or Minister sponsored it:

```bash
git blame 45-1/bills/C-27/bill_text.md -L 42,50
```

### 3. Visual Diffing on GitHub

Navigating to any bill on [GitHub](https://github.com/civican/legisinfo) allows using GitHub's rich visual diff viewer, file history, and commit search without needing to install specialized legal software.

---

## How It Works: `civican-scraper`

The automation engine powering `civican/legisinfo` is **`civican-scraper`**, an open-source Python tool that:

1. **Polls the Parliament of Canada API:** Queries active legislative sessions for newly introduced bills, stage transitions, and text publications.
2. **Parses & Normalizes Parliamentary XML:** Extracts bill metadata, sponsors, short titles, and converts XML body text into clean Markdown.
3. **Replays Chronological Commits:** Programmatically stages the bill files and commits using the sponsor's identity and timestamp via Git plumbing commands.

---

## Connecting Legislation with Lobbying Data

Legislation does not exist in a vacuum. In the Civican ecosystem, `civican/legisinfo` works hand-in-hand with **`civican/lobbycanada`** (tracking federal lobbyist registrations and monthly communications).

Through **`civican-schemas`** (our Protobuf/ConnectRPC contract layer), APIs can cross-reference any bill in `civican/legisinfo` with corresponding lobbying records:

```
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│        civican/legisinfo        │           │       civican/lobbycanada       │
│  (Bill C-27 Text Revisions &    │           │ (Lobbying Communications &      │
│   Parliamentary Commits)        │           │  Designated Public Office)      │
└────────────────┬────────────────┘           └────────────────┬────────────────┘
                 │                                             │
                 └──────────────────────┬──────────────────────┘
                                        ▼
                         ┌─────────────────────────────┐
                         │   CrossReferenceBill RPC    │
                         │ "Who lobbied on Bill C-27   │
                         │  and what text changed?"    │
                         └─────────────────────────────┘
```

This makes it possible to answer critical investigative questions: _Which corporate or non-profit organizations met with lawmakers during the exact week an amendment was committed to the bill text?_

---

## Conclusion & Open Civic Data

By applying modern software engineering patterns—version control, contract-first schemas, and automated continuous integration—to public records, we can transform static government portals into transparent, queryable infrastructure for all Canadians.

Explore the repository, inspect legislative diffs, or contribute at [github.com/civican/legisinfo](https://github.com/civican/legisinfo).
