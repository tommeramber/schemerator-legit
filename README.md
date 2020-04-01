# schemerator

This is a cool project description

# How to run
TODO: write how to run

# Git workflow
## General flow
In this project we use GitFlow as described [here](https://nvie.com/posts/a-successful-git-branching-model/).

We have two main branches **master** and **develop**.
- **master** is our "production ready" version of the code.
- **develop** is our "work in progress" version of the code.

For each new feature we create a feature branch (e.g. **feature/add-red-nose-to-clowns**), each **feature** branch is branched out from **develop** and merged back into **develop**.

Once we are ready to release a new version we create a **release** branch (e.g. **release/1.0**), each **release** branch is branched out from **develop** and merged into both **develop** and **master** once it's ready (also, creating a tag on master).

If there is an argent but in production and we need to fix it fast we can create **hotfix** branch (e.g. **hotfix/1.0.1**), each **hotfix** branch is branched out from **master** and merged into both **develop** and **master** (also creating a tag on master)

|Branch name|Created from:  |Merges back into:  |
|:---------:|:-------------:|:-----------------:|
|develop	|master	        |-                  |
|feature	|develop	    |develop            |
|release	|develop	    |master and develop |
|hotfix	    |master	        |master and develop |


## Merge approval process

As mentioned above, each feature will be developed in a feature branch. After the feature is complete and the branch is ready for merge, a code review will be preformed. Every team member can be a reviewer, except the code writer, obviously.

After the code review, and the fixes if needed, the feature owner will request a merge, using "merge request" option in gitlab. Only the Team Leader (Alona) can approve merge to Develop.

Pls be responsible and follow the rules above, so the Repo won't fu**ed up.  


## Naming convention
For **feature**, **release** and **hotfix** branches we use the type of the branch as a prefix and then '/'.

For **feature** use human readable name for the feature.  
For **release** use the release version.  
For **hotfix** use the new release version.

In the names of the branches use all lower-cased letters, words should separated with dashes ('-').

### Examples
- **feature/proxy-log-messages**
- **release/1.2.0**
- **hotfix/1.2.1**

# Coding standart
The project code will be written according to pep8 python coding standart as described [here](https://realpython.com/python-pep8/).
