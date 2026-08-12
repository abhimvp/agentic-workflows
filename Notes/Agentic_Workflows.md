# Agentic Workflows - From AlgoMoster

> Build AI Agents from Scratch: Agentic Workflows Course

- From a software engineering perspective, an agent is not an independent entity, but a traditional software application that uses a language model as a dynamic routing and decision-making component. Building reliable agents does not require complex frameworks. Instead, it requires standard engineering rigor: state management, input validation, structured database queries, and error handling.

> central project: a **Customer Support Agent** for a commercial retail system.

- To perform effectively, the support agent must query a live database to verify transaction histories, search policy documents to evaluate refund eligibility, execute refunds within strict limits, and gracefully route unresolved or high-value claims to human support.

- **The Chatbot:** Relies on its internal parametric memory. When asked about a specific customer order ID, it fails or produces a generic message because it cannot access external databases.
- **The Agent:** Receives a tool schema signature defining `get_shipping_date`. When queried with the same order ID, the model analyzes the request, realizes it lacks shipping details, executes the registered function, and passes the result back to generate the final response.

---

## Three Architectural Patterns

### 1\. Workflows (Highly Fixed)

A **workflow** is a deterministic sequence of operations defined entirely in code. The application execution path is fixed. The language model is restricted to parsing inputs (e.g., extracting fields from a document) or generating text at predefined stages.

### 2\. Routers (Conditional Routing)

A **router** pattern uses a classification component (often a small, fast language model or a heuristic rule engine) to inspect incoming text and route the request to a pre-defined, deterministic workflow.

### . Agents (Highly Autonomous)

An **agent** is given a set of tool descriptions (functions) and an open-ended goal. The language model determines the sequence of tool executions dynamically. At each turn, it reviews previous outputs to decide the next step, terminating only when its goal is achieved.

> **The Rule of Parsimony: Use the least autonomous pattern that satisfies the system requirements.**
>
> If a business task can be executed using a workflow or a simple router, implementing an agent introduces unnecessary complexity. Autonomy should be reserved solely for tasks where the sequence of operations cannot be predicted before runtime.

---

## The Tool-Calling Interface

### Context Boundaries and Statelessness

> Large language models are inherently stateless and execute no computation outside their own network layers. When an agent system uses a tool—such as performing a database query, fetching a URL, or executing a calculation—the model does not run the tool directly. Instead, the interaction is structured as a coordinated round trip between the stateless model and the stateful execution environment.

### Schema Definition and Parameter Expose

> To enable tool selection, the application must pass a list of schema signatures to the completions API. These schemas define the name, purpose, and required parameters of each function using JSON Schema formatting. The model uses these definitions to format its output arguments.

- If the parameters are underspecified or incorrect, the execution environment will fail when parsing the values. If the schema is unclear, the model may hallucinate missing parameters or format them incorrectly.

---

## Structured Retrieval: Database Queries (SQL)

### Relational Retrieval and Text-to-SQL

Exposing relational databases to language models is a common pattern for structured retrieval. Unlike unstructured search, which relies on text similarity, databases require precise queries written in Structured Query Language (SQL). Under this pattern, the language model is used as a Text-to-SQL generator: it translates natural language requests into SQL statements, executes them via a tool, and reads the returned data to answer the user.

> To perform this translation, the model must understand the schema of the database. This is achieved by including metadata in the model's prompt instructions:

- **Table DDL:** The SQL statements used to create the tables (e.g., `CREATE TABLE customers ...`).
- **Column Descriptions:** Explanations of specific fields, units, and relationships.
- **Sample Queries:** Example inputs and their corresponding SQL outputs to establish formatting expectations.

### Relational Retrieval Architecture

> - **Generation:** The model parses the schema definition and compiles the user's natural language request into a `SELECT` statement.
> - **Privilege Enforcement:** The execution environment executes the query using a connection profile that rejects non-SELECT queries.
> - **Result Formatting:** The matching rows are converted to a structured format (like a JSON array) and appended to the context.

### The Write/Read Security Boundary

Exposing a database connection to an autonomous model introduces substantial security risks. While SQL is a powerful query language, it is not inherently read-only; it contains commands to write, modify, and delete data (`INSERT`, `UPDATE`, `DELETE`, `DROP`). Exposing an unrestricted database connection allows for potential SQL injection attacks or model hallucinations that can destroy data or compromise privacy.
>
> > \[!IMPORTANT\] **Exposing SQL tools requires database-level user privilege constraints.**
> >
> > Developers must never rely on prompt instructions (e.g., "only write SELECT queries") to secure a database. The database connection profile used by the agent tool must be programmatically restricted to read-only access (such as `SELECT` permissions on a specific read-replica or restricted user account). Any attempt to write or alter the schema must trigger a database permission exception.

## TODO: Module 2
