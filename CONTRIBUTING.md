# Contributing to LiteJsonDb

Hi there! We're genuinely excited that you're interested in contributing to LiteJsonDb. This document outlines the guidelines and procedures to ensure we can collaborate effectively and keep this project healthy and maintainable. Think of these as helpful tips from fellow developers – we're in this together!

## Reporting Issues

Before opening a new issue, please do a quick search to see if it's already been raised. When you do submit an issue, the more details you provide, the easier it is for us to understand and address it. Aim for:

*   **Clear and Concise Title:** A brief but informative title helps us quickly grasp the problem or suggestion.
*   **Detailed Description:** Take a moment to explain the issue, feature request, or question thoroughly. Provide as much context as you think is necessary.
*   **Reproducible Steps (if applicable):** If you've encountered a bug, a small code snippet demonstrating the issue helps us a great deal.
*   **Expected Behavior:** Share what you expected to happen. It helps us understand if we are on the same page.
*   **Actual Behavior:** Let us know what actually occurred, and don’t assume we know all the background details.
*   **Environment Details:** Please include your OS, Python version, and LiteJsonDb version. It's crucial for debugging.

The better the information, the quicker we can help. We appreciate your effort in providing a comprehensive report.

## Submitting Pull Requests (PRs)

We welcome contributions through PRs, but we've found the most successful collaborations start with a little planning. Here's the flow we'd like you to follow:

1.  **Open an Issue First:** Before diving into code, please open a new issue to discuss your proposed changes. This step allows us to:
    *   Align on whether the change is in line with the project's direction and goals.
    *   Ensure you are not spending time on something that may not be merged.
    *   Exchange ideas about implementation, and potential challenges. It’s a conversation.

2.  **Detailed Issue Explanation:** In your issue, clearly explain:
    *   What problem are you trying to solve with this change?
    *   How will your solution work?
    *   Are there any potential drawbacks or side effects you foresee?
    *   Are there any design trade-offs you have made?

3.  **Branching:**
    *   Create a new branch for your work, directly from `main`. Keeping your branch updated is good practice.
    *   Use a descriptive branch name, for example: `feature/add-index-support`, `fix/typo-in-readme`, or something similar that’s easy to understand.

4.  **Code Quality:**
    *   Please stick to the existing coding style. Consistency is key for maintainability.
    *   Write clear, well-commented code where necessary. Comments should be helpful and explain the “why” of your logic, not just the “what.”
    *   Please include unit tests for your changes. Good tests are the backbone of good software.
    *   Make sure all tests pass before you submit your PR. It's a basic expectation.

5.  **Dependencies:**
    *   **External Dependencies Are a Sensitive Area:** LiteJsonDb is designed to be lightweight, leveraging the standard library as much as possible.
    *   If, and only if, you absolutely require an external dependency, please:
        * Justify its necessity thoroughly in both the issue and the PR description.
        *  Explicitly declare the dependency with a version constraint in `pyproject.toml`.
        *  Be prepared to explain how this dependency is maintained, reliable and won't create future maintenance headaches. Opt for well-known, widely-used packages with active communities.
        * Use built-in Python functionality where possible, before reaching for an external solution.
   * **Keep It Lean:** We aim to keep LiteJsonDb as lightweight and dependency-free as possible. This is a core design choice.

6.  **Pull Request Details:**
    *   Reference the issue number in your PR description, linking the problem to the solution.
    *   Summarize the changes you have made. This helps the reviewers quickly grasp what’s going on.

7.  **Review Process:** We'll review your PR thoroughly, providing feedback and suggestions. Please be open to discussion and willing to make adjustments as necessary.

## Additional Notes

*   **Comments:** All comments within the code should be in English. This keeps the project accessible to more developers. They should be there to illuminate, not just state the obvious.
*   **Code Organization:**
    *   Structure your files into logical modules with descriptive names. Good organization promotes clarity.
    *   Let the code's structure tell a story.
*   **Error Messages:** Please maintain the project's style and tone when creating error messages. This makes the user experience consistent.
*   **Patience and Communication:** We're a small team, and we'll do our best to get back to you in a reasonable timeframe. Feel free to follow up if you haven’t heard from us.
*  **Collaboration:** We are here to help each other. Please always be respectful and open to discussion.

We believe that good software is a collaborative process and your insights and contributions are valuable. Following these guidelines will help us keep LiteJsonDb a great project for everyone. We look forward to working with you!