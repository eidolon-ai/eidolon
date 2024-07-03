# SQL Benchmarking Script

This document details the SQL benchmarking script usage, designed to integrate with the SQL Spider benchmark suite, accessible at [Yale-Lily's Spider project page](https://yale-lily.github.io/spider).

## Overview

The script is crafted for generating, deploying, and benchmarking Eidolon agents within the SQL Spider benchmark suite. Its primary goal is to assess the agents' efficiency in formulating SQL queries from natural language requests.

## Getting Started

### Prerequisites

- A Python environment with Poetry installed.
- The SQL Spider benchmark suite data, particularly `dev.json`, downloaded to your system.

### Steps

1. **Generate Eidolon Agents:**

   Generate the necessary resources for the Eidolon agents using the command below, substituting `~/Downloads/spider/test_data/dev.json` with your `dev.json` file path.

   ```bash
   poetry run python scripts/sql_baseline/main.py create-resources ~/Downloads/spider/test_data/dev.json
   ```

2. **Launch the Server:**

   Start the server hosting the Eidolon agents, a critical step for the benchmarking process.

3. **Run the Benchmark:**

   Execute the benchmark script to evaluate the Eidolon agents' performance. The script supports parallel execution and other configurations for an optimized benchmarking process.

   ```bash
   poetry run python scripts/sql_baseline/main.py benchmark
   ```

   Utilize the `--help` flag for additional options, including parallelism settings. A parallelism level of 100 is recommended for local execution, providing efficient and insightful trends without the need to run the entire suite. Testing between 100 to 300 tests is sufficient for clear trend analysis.

## Understanding the Results

Failures often occur due to ambiguous requests, where the generated query meets the request but varies in structure or results. A naive concept of "equivalence" is applied, sending queries to an LLM without schema information, to mitigate this issue.
