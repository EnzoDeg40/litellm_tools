# litellm Tools Playground

This folder contains simple Python scripts to help you learn how to use function calling ("tools") with the [litellm](https://github.com/BerriAI/litellm) library and various LLMs.

## Purpose

The scripts demonstrate how to define and use tools (functions) with LLMs via litellm, including how to parse tool calls and execute corresponding Python functions.

## Scripts Overview

- **00_basic_function_calling.py**: Demonstrates basic function calling with two simple math functions: `add_numbers` and `subtract_numbers`. The script sends a subtraction request to the LLM and executes the returned function call.
- **01_weather_tool.py**: Shows how to define a tool for getting the weather in a city. The LLM is prompted with a weather question, and the script executes the corresponding function.
- **02_extract_flight_info.py**: Demonstrates extracting flight booking information from a user message using a tool schema. The script parses the LLM's tool call and prints the extracted booking info.
- **03_multiple_tool_calls.py**: Combines multiple math tools and demonstrates how to handle multiple tool calls in a single LLM response. It prints both the raw LLM response and the results of executing each function.
- **04_trip_planner_tool.py**: Demonstrates planning a trip between two cities with a departure date using a tool schema. The script parses the LLM's tool call and prints the planned trip.
- **05_interactive_list_manager.py**: Interactive script to manage a list of first names (add, remove, list) using LLM tool calls and corresponding Python functions.


## Requirements

Install dependencies with:

```sh
pip install -r requirements.txt
```

## Configuration

Copy your API keys and model names into a `.env` file in this folder. See `.env.example` for the required variables.
