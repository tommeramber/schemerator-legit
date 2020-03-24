# schemerator

This is a cool project description

# How to run
TODO: write how to run

# Git workflow
In this project we use GitFlow as described [here](https://nvie.com/posts/a-successful-git-branching-model/).

We have two main branches **master** and **develop**.
- **master** is our "production ready" version of the code.
- **develop** is our "work in progress" version of the code.

For each new feature we create a feature branch (e.g. **add-red-nose-to-clowns**), each **feature** branch is branched out from **develop** and merged back into **develop**.

Once we are ready to release a new version we create a **release** branch (e.g. **v1.0**), each **release** branch is branched out from **develop** and merged into both **develop** and **master** once it's ready (also, creating a tag on master).

If there is an argent but in production and we need to fix it fast we can create **hotfix** branch (e.g. **make-red-nose-breathable**), each **hotfix** branch is branched out from **master** and merged into both **develop** and **master** (also creating a tag on master)

|Branch name|Created from:  |Merges back into:  |
|:---------:|:-------------:|:-----------------:|
|develop	|master	        |-                  |
|feature	|develop	    |develop            |
|release	|develop	    |master and develop |
|hotfix	    |master	        |master and develop |

