## Building a PR Review Agent

multi-agent AI system that taps into GitHub’s API to pull code diffs, test outcomes, and dependency data. It then uses this information to catch obvious mistakes—lint violations, missing tests, and vulnerability flags—and produces a short, clear comment for each pull request. Finally, it posts the review back to GitHub, so reviewers can dedicate their effort to the deeper review tasks.


### Summary

This script can be added to a github workflow to automatically review and comment a Pull Request.
It implements a LlamaIndex workflow and it's fully functional

### To run the script
* You need to add a `secret` in your github repo to store  
`OPENROUTER_API_KEY=sk-xxxxx`

* You have to create a TOKEN for the agent, with read/write permissions on Issues and PR

* this agent has been tested with the repo [recipe-api](https://github.com/schmotDev/recipe-api) that can be used as tutorial
