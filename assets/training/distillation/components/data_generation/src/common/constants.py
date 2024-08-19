# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Data generator constants."""

import re
from enum import EnumMeta, Enum
# COMPONENT META
COMPONENT_NAME = "oss_distillation_generate_data"

# REQUESTS
REQUESTS_RETRY_DELAY = 5

# DATA GENERATOR VALIDATION
SUPPORTED_FILE_FORMATS = [".jsonl"]
TRAIN_FILE_NAME = "train_input.jsonl"
VALIDATION_FILE_NAME = "validation_input.jsonl"

SERVERLESS_ENDPOINT_URL_PATTERN = re.compile(
    r"https:\/\/(?P<endpoint>[^.]+)\.(?P<region>[^.]+)\.models\.ai\.azure\.com(?:\/(?P<path>.+))?"
)
ONLINE_ENDPOINT_URL_PATTERN = re.compile(
    r"https:\/\/(?P<endpoint>[^.]+)\.(?P<region>[^.]+)\.inference\.ml\.azure\.com(?:\/(?P<path>.+))?"
)
REGISTRY_MODEL_PATTERN = re.compile(
    r"azureml:\/\/registries\/(?P<registry>[^\/]+)\/models\/(?P<model>[^\/]+)(?:\/versions\/(?P<version>\d+))?"
)

# SUPPORTED TEACHER MODEL
# MAP keys are model name in registry, which maps to specific model details like registry and supported versions
SUPPORTED_TEACHER_MODEL_MAP = {
    "Meta-Llama-3.1-405B-Instruct": {
        "supported_registries": ["azureml-meta"],
        "supported_version_pattern": re.compile(r"\d+"),
    }
}

# SUPPORTED STUDENT MODEL
# MAP keys are model name in registry, which maps to specific model details like registry and supported versions
SUPPORTED_STUDENT_MODEL_MAP = {
    "Meta-Llama-3.1-8B-Instruct": {
        "supported_registries": ["azureml-meta"],
        "supported_version_pattern": re.compile(r"\d+"),
    }
}

# Scoring paths
VLLM_CHAT_SCORE_PATH = "/v1/chat/completions"
HFTV2_TEXT_GEN_SCORE_PATH = "/score"

# DATA GEN REQUEST
DEFAULT_SUCCESS_RATIO = 0.7
DEFAULT_REQUEST_BATCH_SIZE = 10
MAX_BATCH_SIZE = 100

# VLLM INFERENCE KEYS
TOP_P = "top_p"
MAX_TOKENS = "max_tokens"
MAX_NEW_TOKENS = "max_new_tokens"
TEMPERATURE = "temperature"
FREQUENCY_PENALTY = "frequency_penalty"
PRESENCE_PENALTY = "presence_penalty"
STOP_TOKEN = "stop"

# TEACHER MODEL DEFAULT INFERENCE PARAMS
DEFAULT_MAX_NEW_TOKENS = 128
DEFAULT_TOP_P = 0.1
DEFAULT_TEMPERATURE = 0.2

# CHAIN OF THOUGHT (COT)
COT_SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Write out in a step by step manner your reasoning about the answer using no more than 80 words. "
    "Based on the reasoning, produce the final answer. "
    "Your response should be in JSON format without using any backticks. "
    "The JSON is a dictionary whose keys are 'reason' and 'answer_choice'. "
    "Always generate a syntactically correct JSON without using markdown and any additional words. "
)

# CHAIN OF DENSITY (COD)
COD_SYSTEM_PROMPT = """
You will generate increasingly concise, entity-dense summaries of the given article.

Repeat the following 2 steps 4 times.

Step 1. Identify 1-3 informative entities (";" delimited) from the article which are missing from the previously generated summary.
Step 2. Write a new, denser summary of identical length which covers every entity and detail from the previous summary plus the missing entities.

A missing entity is:
- relevant to the main story,
- specific yet concise (5 words or fewer),
- novel (not in the previous summary),
- faithful (present in the article),
- anywhere (can be located anywhere in the article).

Guidelines:
- The first summary should be long (4-5 sentences, ~80 words) yet highly non-specific, containing little information beyond the entities marked as missing. Use overly verbose language and fillers (e.g., "this article discusses") to reach ~80 words.
- Make every word count: rewrite the previous summary to improve flow and make space for additional entities.
- Make space with fusion, compression, and removal of uninformative phrases like "the article discusses".
- The summaries should become highly dense and concise yet self-contained, i.e., easily understood without the article.
- Missing entities can appear anywhere in the new summary.
- Never drop entities from the previous summary. If space cannot be made, add fewer new entities.

Remember, use the exact same number of words for each summary. Strictly ensure that each summary should be no more than 80 words.

Answer only in JSON. The JSON should be a list (length 4) of dictionaries whose keys are "Missing_Entities" and "Denser_Summary". \
Ensure the JSON starts with a square bracket [, ends with a square bracket ], \
and each dictionary within the array is separated by a comma. \
The JSON should be syntactically correct and properly formatted. For example: \

[
  {"Missing_Entities": "<value1>", "Denser_Summary": "<value2>"},
  {"Missing_Entities": "<value3>", "Denser_Summary": "<value4>"},
  {"Missing_Entities": "<value5>", "Denser_Summary": "<value6>"},
  {"Missing_Entities": "<value7>", "Denser_Summary": "<value8>"}
]
"""

class InferenceMode:
    """Supported inference modes."""

    HFTV2_CHAT_COMPLETION = "hftv2_chat_completion"
    HFTV2_TEXT_GENERATION = "hftv2_text_generation"
    VLLM_CHAT_COMPLETION = "vllm_chat_completion"
    VLLM_TEXT_GENERATION = "vllm_text_generation"


class MetaEnum(EnumMeta):
    """Metaclass for Enum classes. to use the in operator to check if a value is in the Enum."""

    def __contains__(cls, item):
        """Check if the item is in the Enum."""
        try:
            cls(item)
        except ValueError:
            return False
        return True


class DataGenerationTaskType(str, Enum, metaclass=MetaEnum):
    """Enum for data generation task types."""

    NLI = "NLI"
    CONVERSATION = "CONVERSATION"
    NLU_QUESTION_ANSWERING = "NLU_QA"
    SUMMARIZATION = "SUMMARIZATION"
