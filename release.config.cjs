module.exports = {
    branches: ["master", "next"],
    plugins: [
        [
            "@semantic-release/commit-analyzer",
            {
                preset: "conventionalcommits",
                releaseRules: [
                    {
                        type: "refactor",
                        release: "patch",
                    },
                    {
                        type: "style",
                        release: "patch",
                    },
                    {
                        type: "ci",
                        release: "patch",
                    },
                    {
                        type: "build",
                        release: "patch",
                    },
                    {
                        type: "chore",
                        release: "patch",
                    },
                    {
                        type: "docs",
                        release: "patch",
                    },
                    {
                        type: "perf",
                        release: "patch",
                    },
                    {
                        type: "test",
                        release: "patch",
                    },
                    {
                        type: "revert",
                        release: "patch",
                    },
                    {
                        type: "fix",
                        release: "patch",
                    },
                    {
                        type: "feat",
                        release: "minor",
                    },
                    {
                        type: "BREAKING CHANGE",
                        release: "major",
                    },
                ],
            },
        ],
        [
            "@semantic-release/release-notes-generator",
            {
                preset: "conventionalcommits",
            },
        ],
        [
            "@semantic-release/changelog",
            {
                changelogTitle:
                    "# esiosapy\n\nAll notable changes to this project will be documented in this file. See\n[Conventional Commits](https://conventionalcommits.org) for commit guidelines.",
            },
        ],
        [
            "semantic-release-replace-plugin",
            {
                replacements: [
                    {
                        files: ["pyproject.toml"],
                        from: 'version = ".*"',
                        to: 'version = "${nextRelease.version}"',
                        countMatches: true,
                    },
                ],
            },
        ],
        [
            "@semantic-release/github",
        ],
        [
            "@semantic-release/git",
            {
                message:
                    "chore: release ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}",
                assets: ["CHANGELOG.md", "pyproject.toml"],
            },
        ],
    ],
};