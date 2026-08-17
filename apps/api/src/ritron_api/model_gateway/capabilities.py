"""Provider-neutral model capabilities."""

from enum import StrEnum


class ModelCapability(StrEnum):
    TEXT_GENERATION = "text_generation"
    STREAMING = "streaming"
    TOOL_CALLING = "tool_calling"
    STRUCTURED_OUTPUT = "structured_output"
    VISION = "vision"
    AUDIO_INPUT = "audio_input"
    AUDIO_OUTPUT = "audio_output"
    IMAGE_GENERATION = "image_generation"
    REASONING = "reasoning"
    EMBEDDINGS = "embeddings"
