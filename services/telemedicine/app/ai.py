from .config import settings


class AIProvider:
    def summarize(self, notes: str) -> str:
        raise NotImplementedError


class MockAIProvider(AIProvider):
    def summarize(self, notes: str) -> str:
        cleaned = " ".join(notes.split())
        excerpt = cleaned[:220]
        return (
            "DEMO AI SUMMARY — not medical advice. "
            f"Visit note captured: {excerpt}. "
            "A clinician should review any generated summary before use."
        )


class BedrockAIProvider(AIProvider):
    """Provider seam for AWS Bedrock.

    Kept intentionally conservative for the portfolio demo. A production
    implementation should add model-specific validation, timeouts, retries,
    redaction, evaluation, audit logging, and explicit data-governance rules.
    """

    def summarize(self, notes: str) -> str:
        raise RuntimeError(
            "Bedrock provider is intentionally not enabled in this demo. "
            "Set up the AWS SDK/model invocation after reviewing cost and data controls."
        )


def get_ai_provider() -> AIProvider:
    if settings.ai_provider.lower() == "bedrock":
        return BedrockAIProvider()
    return MockAIProvider()
