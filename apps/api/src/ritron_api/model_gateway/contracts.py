"""Stable, provider-independent model contracts."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from ritron_api.model_gateway.capabilities import ModelCapability


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class TextContent(BaseModel):
    type: Literal["text"] = "text"
    text: str = Field(min_length=1)


class ImageUrlContent(BaseModel):
    type: Literal["image_url"] = "image_url"
    url: str = Field(min_length=1)
    media_type: str | None = None


class AudioContent(BaseModel):
    type: Literal["audio"] = "audio"
    url: str = Field(min_length=1)
    media_type: str | None = None


class FileContent(BaseModel):
    type: Literal["file"] = "file"
    url: str = Field(min_length=1)
    name: str | None = None
    media_type: str | None = None


class JsonContent(BaseModel):
    type: Literal["json"] = "json"
    value: dict[str, object]


ContentPart = Annotated[
    TextContent | ImageUrlContent | AudioContent | FileContent | JsonContent,
    Field(discriminator="type"),
]


class ToolCall(BaseModel):
    id: str
    name: str
    arguments: dict[str, object] = Field(default_factory=dict)


class ModelMessage(BaseModel):
    role: MessageRole
    content: tuple[ContentPart, ...] = Field(min_length=1)
    tool_call_id: str | None = None
    tool_calls: tuple[ToolCall, ...] = ()

    @field_validator("content", mode="before")
    @classmethod
    def normalize_text_content(cls, value: object) -> object:
        if isinstance(value, str):
            return ({"type": "text", "text": value},)
        return value


class ToolDefinition(BaseModel):
    name: str = Field(pattern=r"^[A-Za-z_][A-Za-z0-9_-]{0,127}$")
    description: str | None = None
    input_schema: dict[str, object] = Field(default_factory=dict)


class ModelRequest(BaseModel):
    """The complete normalized input accepted by a model gateway."""

    model_config = ConfigDict(frozen=True)

    messages: tuple[ModelMessage, ...] = Field(min_length=1)
    model_id: str | None = Field(default=None, min_length=1)
    temperature: float | None = Field(default=None, ge=0, le=2)
    max_output_tokens: int | None = Field(default=None, ge=1)
    top_p: float | None = Field(default=None, gt=0, le=1)
    stop: tuple[str, ...] = ()
    seed: int | None = None
    response_format: dict[str, object] | None = None
    tools: tuple[ToolDefinition, ...] = ()
    tool_choice: str | None = None
    metadata: dict[str, object] = Field(default_factory=dict)
    timeout_seconds: float | None = Field(default=None, gt=0, le=600)
    request_id: str | None = None
    user_id: str | None = None
    session_id: str | None = None
    workspace_id: str | None = None

    def required_capabilities(self) -> frozenset[ModelCapability]:
        capabilities = {ModelCapability.TEXT_GENERATION}
        if self.tools:
            capabilities.add(ModelCapability.TOOL_CALLING)
        if self.response_format is not None:
            capabilities.add(ModelCapability.STRUCTURED_OUTPUT)
        if any(
            not isinstance(part, TextContent)
            for message in self.messages
            for part in message.content
        ):
            capabilities.add(ModelCapability.VISION)
        return frozenset(capabilities)


class Usage(BaseModel):
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)


class FinishReason(StrEnum):
    STOP = "stop"
    LENGTH = "length"
    TOOL_CALLS = "tool_calls"
    CONTENT_FILTER = "content_filter"
    CANCELLED = "cancelled"
    ERROR = "error"


class ModelResponse(BaseModel):
    content: tuple[ContentPart, ...] = ()
    finish_reason: FinishReason
    model_id: str
    provider_id: str
    request_id: str | None = None
    operation_id: str
    usage: Usage | None = None
    latency_ms: int = Field(ge=0)
    tool_calls: tuple[ToolCall, ...] = ()
    structured_output: dict[str, object] | None = None
    warnings: tuple[str, ...] = ()
    metadata: dict[str, object] = Field(default_factory=dict)


class ModelStatus(StrEnum):
    CONFIGURED = "configured"
    DISABLED = "disabled"
    UNKNOWN = "unknown"


class ModelDescriptor(BaseModel):
    id: str = Field(min_length=1)
    provider_id: str = Field(min_length=1)
    provider_model_id: str = Field(min_length=1)
    display_name: str | None = None
    capabilities: frozenset[ModelCapability] = Field(default_factory=frozenset)
    context_window: int | None = Field(default=None, ge=1)
    max_output_tokens: int | None = Field(default=None, ge=1)
    status: ModelStatus = ModelStatus.CONFIGURED
    metadata: dict[str, object] = Field(default_factory=dict)


class StreamEventBase(BaseModel):
    operation_id: str
    sequence: int = Field(ge=0)
    timestamp: datetime


class StreamStarted(StreamEventBase):
    type: Literal["started"] = "started"
    model_id: str
    provider_id: str


class ContentDelta(StreamEventBase):
    type: Literal["content_delta"] = "content_delta"
    text: str


class ReasoningDelta(StreamEventBase):
    type: Literal["reasoning_delta"] = "reasoning_delta"
    text: str


class ToolCallDelta(StreamEventBase):
    type: Literal["tool_call_delta"] = "tool_call_delta"
    call_id: str
    name: str | None = None
    arguments_delta: str = ""


class UsageUpdate(StreamEventBase):
    type: Literal["usage"] = "usage"
    usage: Usage


class StreamWarning(StreamEventBase):
    type: Literal["warning"] = "warning"
    message: str


class StreamCompleted(StreamEventBase):
    type: Literal["completed"] = "completed"
    finish_reason: FinishReason
    usage: Usage | None = None


class StreamFailed(StreamEventBase):
    type: Literal["failed"] = "failed"
    code: str
    message: str


class StreamCancelled(StreamEventBase):
    type: Literal["cancelled"] = "cancelled"


ModelStreamEvent = Annotated[
    StreamStarted
    | ContentDelta
    | ReasoningDelta
    | ToolCallDelta
    | UsageUpdate
    | StreamWarning
    | StreamCompleted
    | StreamFailed
    | StreamCancelled,
    Field(discriminator="type"),
]
