# Writing Style for This Project

## Core Principle: Show, Don't Tell

Do not tell the reader how defensible, important, or significant something is.
Do not tell the reader what something is not. Just state what it is and what it does.

## What to Avoid

- "The training method is defensible if framed as..." — That is for the reader to judge.
- "This does not prove that X, but it does show Y" — Just state Y.
- "TrayGuard should not claim to replace certification..." — Just state what TrayGuard does.
- "This boundary is important for the training pivot." — If it matters, show it; don't say it matters.
- "The marker does not need to prove that user can handle real instruments; it needs to..." — Just say what it does.
- "This is not a concession — it is a deliberate methodological choice." — Just say it is a methodological choice.
- "This direction was selected because it is useful, buildable, and testable." — Let the evidence speak.
- "not a substitute for X", "not a shortcut around Y", "not a claim that Z" — Any "not" that defends a design choice rather than describing a factual constraint.
- "This distinction is important for..." — Show the distinction; don't announce its importance.
- "Therefore the FDR claim should be narrow and testable:" — Just make it narrow and testable.

## What to Do Instead

- State findings directly: "Alfred et al. analyzed 3,900 tray defects..."
- State design decisions directly: "TrayGuard gives learners repeated practice before, during, or between supervised work."
- State facts without justification: "Assembly is the stage where cleaned instruments are identified, inspected, counted, and rebuilt."
- Let evidence conclude, don't conclude for the reader.
- If something is a limitation, state it as a limitation, not as a defense.
- If something is a design choice, state it as a choice, not as a response to a potential objection.

## Test: Can You Remove the "Not"?

Before every "not" statement, ask: is this a real necessary constraint (e.g., "no hints in assessment mode") or is it defending against an unstated objection? If it's defense, cut it.

## Housekeeping: \texttt{final\_paper/}

Keep only \texttt{trayguard\_paper.tex}, \texttt{trayguard\_refs.bib}, and
\texttt{trayguard\_paper.pdf} in \texttt{final\_paper/}. Delete all other files
(\texttt{.aux}, \texttt{.bbl}, \texttt{.blg}, \texttt{.log}, \texttt{.out},
\texttt{.toc}, \texttt{.tex.bak}, \texttt{bibliography\_mla.txt}) whenever
editing the paper — they are build artifacts that will be regenerated.

## Example Conversions

| Instead of saying | Say |
|---|---|
| "The training method is defensible if framed as a simulation proxy, not as proof of clinical competence." | "Health professions education provides a general precedent for simulation..." |
| "This does not prove that a training app will prevent delays, but it does show the target task is not cosmetic." | "When delays occurred, the average was 10 minutes — a recurrent operational consequence." |
| "TrayGuard should not claim to replace certification. Its value is earlier and narrower: give learners repeated practice..." | "TrayGuard gives learners repeated practice before, during, or between supervised work..." |
| "TrayGuard's differentiation is not that no one has count sheets. Its contribution is..." | "TrayGuard's contribution is a low-cost local training loop that..." |
| "The AprilTag card is not a concession — it is a deliberate methodological choice." | "The AprilTag card is a deliberate methodological choice that controls for instrument-access confounds..." |
