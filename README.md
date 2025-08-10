# bazel-repos

Datasets for (**NOT ONLY**) Bazel-Based Projects (Repositories) in GitHub.

## Overview

This project includes 5 datasets:

1. [**search_repos/repos**](search_repos/repos): We have collected 126082 repositories using GitHub Search API. Filter criteria is as follows (searching details will be explained later):
   ```
   size:>1000 pushed:>2025-01-01 stars:<={end_star} fork:false archived:false template:false mirror:false

   sort="stars"
   order="desc"
   ```

2. [**search_repos/trees**](search_repos/trees): We have collected the file entries in root directory for 126049 repositories (126049 < 126082, as some repositories may have been removed).

3. [**search_repos/filtered**](search_repos/filtered): We have filtered 560 Bazel-based repositories based on the following criteria on the file entries in root directory:
   ```py
      path in ['BUILD', '.bazelrc', '.bazelignore']
   or path.endswith('.bzl')
   or path.endswith('.bazel')
   ```

4. [**get_rebuild_costs/results**](get_rebuild_costs/results): We successfully cloned the 560
filtered repositories and executed the Bazel query command to extract the
dependency graph of 425 of them. Subsequently, we computed the rebuild costs using
the `depstat` tool, available at
[https://github.com/xuhongxu96/depreduce](https://github.com/xuhongxu96/depreduce)
(currently private).

5. [**get_rebuild_costs/sorted.txt**](get_rebuild_costs/sorted.txt): This file contains the list of
repositories sorted by their rebuild costs.

## Searching Strategy

Due to the GitHub Search API's limitation of returning only the first 1000 results
per query, we employ a slicing strategy based on repository star counts to
maximize data coverage. Specifically, we partition the search space into
intervals defined by the `stars` attribute. Beginning with a broad range
(e.g., `stars:<=1000000000`), we iteratively adjust the upper bound to the
star count of the last repository retrieved in the previous query. This
approach ensures that each query returns a distinct set of repositories,
minimizing overlap and maximizing coverage.

We terminate the search process when the upper bound (`end_star`) reaches 62,
as the final repository retrieved at this threshold also possesses 62 stars.
While this method may omit some repositories due to fluctuations in star
counts, the resulting datasets remain sufficiently comprehensive to represent
the majority of Bazel-based repositories, particularly those with higher
popularity.
