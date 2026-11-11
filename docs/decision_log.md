# Decision log

One entry per decision. Newest at the bottom.

## ADR-001: Own repository, not a fork

Status: Accepted · Date: 2026-11-11

Context: A solo rehearsal of the group project. The history must show the same Git flow as the group: short branches, pull requests and merge commits into a protected main.

Decision: A public repository of my own (MOCJ44/itu-sdse-SOLO), with the teachers' repository as the remote upstream. A ruleset protects main: changes only through a pull request, no force pushes, no deletion, no bypass. Required approvals are 0, because GitHub does not let an author approve their own pull request; I review my own diff before merging. Only merge commits are allowed.

Rejected: A fork (GitHub suggests opening pull requests against the teachers' repository); a private repository (rulesets are not available for private repositories on GitHub Free); squash merging (hides the small commits).

Consequences: Self-review replaces a second reviewer. Changes from the teachers come in through a branch and a pull request, like any other change.
