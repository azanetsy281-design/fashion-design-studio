# Capability and portability notes

Use the open Agent Skills layout: a `fashion-design-studio` folder with one root
`SKILL.md`, optional `agents/openai.yaml`, and the referenced resources/scripts.
Keep file references relative to that folder. Do not require internal account IDs,
absolute creator paths, a companion plugin or a paid API for the SVG workflow.

## ChatGPT / Codex

Treat skill availability as product/account/workspace-dependent. Use installed
skills in supported surfaces. Follow the host's native image tool instructions
when image generation is available. Merely attaching a file to an ordinary chat
is not necessarily a persistent skill installation.

Official OpenAI documentation:
https://learn.chatgpt.com/docs/build-skills

For broader ChatGPT distribution, OpenAI's current guidance recommends plugins;
this package remains a standalone skill as requested. Do not claim a GitHub upload
automatically publishes or installs it in ChatGPT.

## Claude

Claude supports custom skill-folder ZIP uploads in supported accounts, subject to
code execution and organization controls. Its documented UI is Customize > Skills,
then add/create and upload a skill. For a ZIP, place the skill folder at the root;
do not upload a whole repository archive with extra enclosing folders.

Claude does not natively generate photographic images like an image generator.
Use SVG artifacts or execute the bundled standard-library renderer for fashion
flats. If an image connector is actually available and authorized, follow its
instructions; do not silently add external services or request API secrets.

Official Anthropic documentation:
https://support.claude.com/en/articles/12512180-use-skills-in-claude
https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
https://support.claude.com/en/articles/9002504-can-claude-produce-images

Recheck official instructions if asked for current installation steps; UI wording
can change. These notes were checked on 2026-11-01 and are not evidence of a live
installation test in Claude or of photographic-image testing in ChatGPT.
