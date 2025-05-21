# 🤖 AI Agents Framework

<div align="center">

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/ed-donner/agents)
[![Python Support](https://img.shields.io/badge/Python-3.7+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-May%202025-brightgreen.svg)](https://github.com/ed-donner/agents)

<p align="center">
  <img src="./assets/autonomy.png" alt="AI Agents" width="200">
</p>

</div>

<p align="center">
  <strong>Exploring the world of AI agents, workflows, and autonomous systems</strong>
</p>

<hr style="height:2px;border-width:0;color:gray;background-color:#007ACC">

## Table of Contents 📋

- [Getting Started](#getting-started-)
- [What Are AI Agents?](#what-are-ai-agents-)
- [Agentic Systems Architecture](#agentic-systems-architecture-)
- [Five Workflow Design Patterns](#five-workflow-design-patterns-)
- [Agents: Beyond Structured Workflows](#agents-beyond-structured-workflows-)
- [Risk Considerations](#risk-of-agent-frameworks-)
- [Agentic AI Frameworks](#agentic-ai-frameworks-)
- [Complex Frameworks](#complex-ones-)
- [Top Level Complex Frameworks](#top-level-complex-)
- [Resources vs Tools](#resources-vs-tools-the-building-blocks-)
- [OpenAI Agents SDK](#openai-agents-sdk-)
- [Contributing](#contributing-)

<hr style="height:2px;border-width:0;color:gray;background-color:#007ACC">

## Getting Started 🚀

```bash
# Initialize your environment with dependencies
uv sync
```

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## What Are AI Agents? 🧠

AI Agents are programs where LLM outputs control the workflow, featuring:

- **Multiple LLM calls** — Chaining language model interactions
- **LLMs with ability to use Tools** — Extending capabilities beyond text
- **An environment where LLMs interact** — Creating collaborative AI systems
- **A Planner to coordinate activities** — Orchestrating complex workflows
- **Autonomy** — Self-directed problem solving

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Agentic Systems Architecture 🏗️

Anthropic distinguishes two types of systems:

1. **Workflows**: Systems where LLMs and tools are orchestrated through predefined code paths
2. **Agents**: Systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Five Workflow Design Patterns 📊

### 1. Prompt Chaining ⛓️
Decompose tasks into fixed sub-tasks

<div align="center">
  <img src="./assets/Prompt_Chaining.png" alt="Prompt Chaining" width="650">
  <p><em>Reference: 1_lab1.ipynb</em></p>
</div>

### 2. Routing 🔀
Direct an input into a specialized sub-task, ensuring separation of concerns

<div align="center">
  <img src="./assets/Routing.png" alt="Routing" width="650">
  <p><em>Routing pattern: Directing inputs to specialized handlers</em></p>
</div>

### 3. Parallelization ⚡
Breaking down tasks and running multiple subtasks concurrently, with code as the coordinator

<div align="center">
  <img src="./assets/Parrallelization.png" alt="Parallelization" width="650">
  <p><em>Parallelization pattern: Concurrent execution for efficiency</em></p>
</div>

### 4. Orchestrator-Worker 🎭
Complex tasks are broken down dynamically and combined, with LLM as the orchestrator

<div align="center">
  <img src="./assets/Orchestrator_Worker.png" alt="Orchestrator Worker" width="650">
  <p><em>Orchestrator-Worker pattern: LLM coordinates specialized workers</em></p>
</div>

### 5. Evaluator-Optimizer ✅
LLM output is validated by another LLM

<div align="center">
  <img src="./assets/Evaluator_Optimzer.png" alt="Evaluator Optimizer" width="650">
  <p><em>Evaluator-Optimizer pattern: Quality control through validation</em></p>
</div>

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Agents: Beyond Structured Workflows 🔄

Agents differ from workflows by being:

1. **Open-ended** — Not restricted to predefined pathways
2. **Driven by feedback loops** — Learning and adapting from results
3. **Not following fixed paths** — Dynamic problem-solving approaches

<div align="center">
  <img src="./assets/By_Contrasts_Agents.png" alt="By Contrasts Agents" width="650">
  <p><em>The fundamental differences between fixed workflows and agentic systems</em></p>
</div>

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Risk of Agent Frameworks ⚠️

<div align="center">
  <img src="./assets/Risks.png" alt="Risks" width="650">
  <p><em>Understanding and mitigating the inherent risks of autonomous AI systems</em></p>
</div>

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Agentic AI Frameworks 🛠️

1. **No Framework** — Reference implementation in [2_lab2.ipynb](./1_foundations/2_lab2.ipynb)
2. **MCP** (Model-Context-Protocol) — Standardized communication protocol for agent interactions

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Complex Ones 🧩

1. **OpenAI Agents SDK** — Building intelligent agents with OpenAI's technology
2. **Crew AI** — Multi-agent framework for collaborative AI systems

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Top Level Complex 🔝

1. **LangGraph** — Orchestration framework for LLM applications
2. **AutoGen** — Multi-agent conversation framework for AI applications

<p><em>Many, many more! Which to pick depends on the use case and preference</em></p>

<hr style="height:2px;border-width:0;color:gray;background-color:#007ACC">

## Resources vs Tools: The Building Blocks 🧰

<p align="center">
  <strong>Understanding the key components that power AI agent systems</strong>
</p>

### Resources: Knowledge & Data 📚

<div align="center">
  <img src="./assets/Resources.png" alt="Resources" width="700">
  <p><em>Information repositories that agents can access and utilize</em></p>
</div>

### Tools: Actions & Capabilities 🛠️

<div align="center">
  <img src="./assets/Tools.png" alt="Tools" width="700">
  <p><em>Functional abilities that enable agents to interact with their environment</em></p>
</div>

<div align="center">
  <h3>Theory vs Practice 📊</h3>
  <table>
    <tr>
      <td align="center" width="50%">
        <h4>The Theory 📝</h4>
        <img src="./assets/Tools_In_Theory.png" alt="Tools In Theory" width="600">
        <p><em>How tools are conceptualized in design</em></p>
      </td>
      <td align="center" width="50%">
        <h4>The Practice ⚙️</h4>
        <img src="./assets/Tools_In_Practice.png" alt="Tools In Practice" width="600">
        <p><em>How tools function in real-world applications</em></p>
      </td>
    </tr>
  </table>
</div>

<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## OpenAI Agents SDK 🤖

<div align="center">
  <img src="./assets/OpenAI_Agents_SDK.png" alt="OpenAI Agents SDK" width="700">
  <p><em>OpenAI's framework for building, deploying, and managing intelligent agents</em></p>
</div>

### Key Terminology 📚

<div align="center">
  <img src="./assets/Terminologies_SDK.png" alt="Terminologies SDK" width="700">
  <p><em>Essential concepts and vocabulary for working with the OpenAI Agents SDK</em></p>
</div>

### Implementation Steps 📋

<div align="center">
  <img src="./assets/Steps_SDK.png" alt="Steps SDK" width="700">
  <p><em>Workflow process for implementing agents with OpenAI's SDK</em></p>
</div>

<hr style="height:2px;border-width:0;color:gray;background-color:#007ACC">


<hr style="height:1px;border-width:0;color:gray;background-color:#e1e4e8">

## Contributing 🤝

We welcome contributions to this project! Feel free to:

- Submit pull requests for new features or improvements
- Report issues or bugs
- Suggest new ideas via the issue tracker

<div align="center">
  <img src="./assets/thanks.png" alt="Thank you" width="200">
  <p><em>We appreciate your interest and contributions!</em></p>
</div>

<div align="center">
  <p><em>Reference Repository: <a href="https://github.com/ed-donner/agents">https://github.com/ed-donner/agents</a></em></p>
</div>
