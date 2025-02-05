# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""Data generatior constants."""

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


class TelemetryConstants:
    """Telemetry constants that describe various activities performed by the distillation components."""

    INVOKE_MODEL_ENDPOINT = "invoke_model_endpoint"
    BATCH_PROCESS_TRAINING_DATA = "batch_process_training_data"
    BATCH_PROCESS_VALIDATION_DATA = "batch_process_validation_data"
    PROCESS_DATASET_RECORD = "process_dataset_record"
