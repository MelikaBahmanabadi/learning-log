# Flashcards

<!-- Cards in Anki format: Question? ; Answer -->

---

## Ch1 — Data Versioning Motivation

Why is data versioning necessary in ML? ; Because a model result depends on data, code, and hyperparameters. Versioning only code cannot reliably reproduce or audit an ML experiment

What three components together determine an ML model's result? ; Code (algorithms and architecture), data (training inputs), and hyperparameters (pre-training configuration settings)

Why can two models trained on subsets of the same dataset produce different metrics? ; Because random partitioning creates different sample distributions; if a real distribution shift occurs, the metric difference can be significant

What is the key practical difference between code versioning and data versioning tools? ; Git is sufficient for code because codebases are small and text-based; data versioning requires additional software alongside Git to handle large, binary, and frequently changing datasets

When did the first practical implementations of data versioning appear? ; Around 2012

---

## Ch1 — Git and DVC Fundamentals

What is the relationship between Git and DVC? ; Git versions code and lightweight DVC metadata such as .dvc files, dvc.yaml, and dvc.lock; DVC manages the actual large data and model artifacts via its cache and remote storage

After `dvc add data.csv`, what does Git track and what does DVC manage? ; Git tracks data.csv.dvc (pointer) and .gitignore; DVC caches the actual bytes of data.csv and can upload them to a DVC remote

What is the correct sharing workflow after tracking a new dataset with DVC? ; Run `dvc add data.csv`, `git add data.csv.dvc .gitignore`, `git commit`, `dvc push`, and `git push`. Both dvc push and git push are required

What happens after `git clone` of a DVC project? ; You get code, .dvc config, .dvc pointer files, dvc.yaml, and dvc.lock — but not the actual DVC-tracked data or model artifacts

How does a teammate restore DVC-tracked data after `git clone`? ; Run `dvc pull`. It downloads artifacts from the DVC remote into the local cache and links or copies them into the workspace

What is the difference between `git push` and `dvc push`? ; `git push` uploads code and DVC metadata (pointers) to a Git remote; `dvc push` uploads actual cached data and model artifacts to DVC remote storage

What does `dvc add` do? ; It hashes and caches the current version of a standalone data file or directory, creates or updates its .dvc pointer file, and adds the tracked path to .gitignore

What is a `.dvc` file such as `data.csv.dvc`? ; Git-trackable metadata identifying a DVC-tracked artifact by its content hash; it is not the actual dataset, only a pointer to it

What is `dvc.yaml`? ; It declares a DVC pipeline: named stages, commands, dependencies (deps), outputs (outs), and optionally params, metrics, and plots

What is `dvc.lock`? ; It records the exact content hashes of pipeline dependencies and outputs from the last reproduction, enabling DVC to detect stale stages

Does `dvc.lock` make files read-only? ; No. dvc.lock records pipeline state and detects staleness via hash comparison; read-only protection can arise separately from cache link types such as hardlinks or symlinks

What makes a DVC pipeline stage stale? ; Any declared dependency changing so that its current hash differs from the hash recorded in dvc.lock

If `train.py` changes but training data does not, what does `dvc repro` run? ; It reruns the train stage (changed dependency) then reruns downstream stages that depend on the changed output; unaffected upstream stages are skipped

What is the difference between `dvc add` and `dvc repro`? ; `dvc add` tracks a standalone data file or directory; `dvc repro` checks the DAG and runs only stale pipeline stages in dependency order

What is the normal workflow for modifying data tracked with `dvc add`? ; Optionally run `dvc unprotect` to safely unlink from cache, make edits, run `dvc add` again, commit the updated .dvc pointer with Git, then `dvc push` and `git push`

Why should `dvc commit` not be your default command for changed standalone data? ; For `dvc add`-tracked data, rerunning `dvc add` is the correct default; for pipelines, `dvc repro` validates dependencies and executes the declared workflow — both are safer

Which two commands together show the full project state? ; `git status` shows code and DVC metadata changes; `dvc data status` shows DVC-tracked data changes and cache state

---

## Needs Review

<!-- Wrong answers from periodic quizzes go here -->

What is the difference between `dvc.lock` and cache protection? ; dvc.lock is a hash-based record of pipeline inputs and outputs used for staleness detection; cache protection may make workspace files read-only when link-based cache types (hardlinks, symlinks) are used
