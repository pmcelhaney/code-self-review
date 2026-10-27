# Code Self-Review

A pull request can explain what changed and still leave a reviewer guessing about the decisions, assumptions, and gaps that matter.

**Prepare Code Self-Review** helps a coding agent review its own change before handing it to a human. It produces a few evidence-backed notes on the current diff, a precise account of what was tested, and specific questions that need human judgment. When publication is authorized, it posts actual PR review comments and reads them back to verify delivery.

It complements acceptance demos and independent review. It never approves its own PR or certifies that a change is ready to merge.

## Example

Before: “Added retries. Tests pass. Please review carefully.”

After: an inline note explains why only GET requests are retried, names the resulting limitation, and asks a concrete domain question. The review summary identifies the focused checks that passed and the load test that was not run.

See the [complete fictional before/after example](examples/review.md), including the exact diff and review anchors.

## Install with the skills CLI

Requires Git, network access, Node.js 22.20 or later, and npm/npx. In the project where you want the skill installed, run:

```sh
npx skills@1.7.4 add pmcelhaney/code-self-review --skill prepare-code-self-review
```

The CLI prompts for a supported agent and installation method. This installs into the current project by default. Review the proposed destination; add `-g` only if you want an installation across projects. The CLI version is pinned; repository content follows its default branch. Inspect the skill before installing and use a reviewed Git revision when you need reproducible content.

The CLI is third-party software. Its [installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) describes source formats and options; its [README](https://github.com/vercel-labs/skills#telemetry) describes telemetry and opt-out controls.

## Manual installation, for any agent

1. Clone this repository into a new directory:

   ```sh
   git clone https://github.com/pmcelhaney/code-self-review.git
   ```

2. Inspect [SKILL.md](skills/prepare-code-self-review/SKILL.md).
3. Copy the entire `skills/prepare-code-self-review` directory to the skill directory documented by your agent. Keep the folder name and `SKILL.md` filename intact. Do not replace an existing installation without reviewing it.
4. If your agent has no skill loader, explicitly supply that file as task instructions. This does not add native skill discovery or PR tooling to the agent.

No executable helper, API token, or agent-specific configuration is bundled. The layout follows the [Agent Skills specification](https://agentskills.io/specification); loader behavior and tool support vary by agent.

## Use

For a draft without publication:

> Use prepare-code-self-review on my current diff. Return draft inline comments with current anchors and a verification summary. Do not publish them.

For an authorized PR workflow:

> Create a PR for this change in the repository we are working in. Use prepare-code-self-review and publish the author review comments on that PR before handing it to me.

For an existing PR, identify the exact repository and PR number and explicitly authorize self-review comments there. The agent must inspect that destination and its current head before posting.

The agent needs access to the relevant diff, surrounding code, requirements, and test evidence. Publishing also requires an authenticated PR integration with permission to comment. Without suitable tools or publication authority, it returns drafts and reports the limitation. A PR-body section alone is not a posted review.

## Permissions and limits

Installing or invoking the skill grants no blanket permission to post, push, merge, deploy, request reviews, or share private information. The user's task determines the allowed actions and destinations. Repository and platform instructions still apply.

The workflow checks existing comments to avoid duplication, refreshes anchors after edits, distinguishes passed/failed/not-run checks, and verifies submitted comments by reading them back. These are instructions to an agent, not a security boundary or guarantee of compliance. Human review remains necessary.

Public availability on GitHub does not imply a skills.sh listing, OpenAI curation, or compatibility with every coding agent.

## Maintenance

Run the dependency-free packaging checks with Python 3:

```sh
python3 scripts/validate.py
```

CI runs the same checks. They verify packaging, local links, frontmatter, the fictional example's anchors, and permission safeguards; they do not prove how an agent will behave on a real PR.

## Attribution and license

Developed for Patrick McElhaney's custom coding-agent workflow with AI assistance. The published skill preserves that workflow, with an explicit installation-permissions and private-information safeguard. The example is fictional and contains no real PR discussion or project code.

Released under the [MIT License](LICENSE). This repository distributes the workflow instructions and its supporting documentation; it does not bundle the skills CLI or any agent software.
