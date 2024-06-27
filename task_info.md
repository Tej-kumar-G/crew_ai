
### Task Information

**Goal**: Search for URLs related to the given vulnerability {vulnerability}.

**Agent**: URL Search Agent

**Tools**: Website Search Tool

**Expected Output**: A list of URLs related to the vulnerability.

**Asynchronous Execution**: False

### Task Information

**Goal**: Download and clean content from the list of URLs.

**Agent**: URL Download Agent

**Tools**: Website Download Tool

**Expected Output**: Cleaned text data from the URLs.

**Asynchronous Execution**: False

### Task Information

**Goal**: Generate a markdown vulnerability report based on downloaded data.

**Agent**: Report Generation Agent

**Tools**: Markdown Report Tool

**Expected Output**: A comprehensive markdown report.

**Asynchronous Execution**: False

### Task Information

**Goal**: Generate an HTML vulnerability report based on downloaded data.

**Agent**: Report Generation Agent

**Tools**: HTML Report Tool

**Expected Output**: A comprehensive HTML report.

**Asynchronous Execution**: False
    