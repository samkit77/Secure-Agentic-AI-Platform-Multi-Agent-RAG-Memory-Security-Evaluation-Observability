from guardrails import Guard
from guardrails.hub import DetectPII, ToxicLanguage


# ============================================================
# Input Guard
# ============================================================

input_guard = Guard(name="rag_input_guard").use(
    DetectPII(
        pii_entities=[
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD",
            "IP_ADDRESS",
        ],
        on_fail="exception",
    ),
    ToxicLanguage(
        threshold=0.5,
        validation_method="full",
        on_fail="exception",
    ),
)


# ============================================================
# Output Guard
# ============================================================

output_guard = Guard(name="rag_output_guard").use(
    DetectPII(
        pii_entities=[
            "EMAIL_ADDRESS",
            "PHONE_NUMBER",
            "CREDIT_CARD",
            "IP_ADDRESS",
        ],
        on_fail="exception",
    ),
    ToxicLanguage(
        threshold=0.5,
        validation_method="full",
        on_fail="exception",
    ),
)


def initialize_rails():
    """
    Compatibility function kept from the course structure.

    Guardrails are initialized when the guards above are created,
    so there is no additional startup initialization required.
    """
    return None


def guard(query: str):
    """
    Validates incoming user input.

    Returns:
        (True, response)  -> input blocked
        (False, None)     -> input allowed
    """

    try:
        result = input_guard.validate(query)

        if result.validation_passed:
            return False, None

        return (
            True,
            "I can't process that request because it "
            "did not pass the input safety checks.",
        )

    except Exception:
        return (
            True,
            "I can't process that request because it "
            "did not pass the input safety checks.",
        )


def validate_output(response: str):
    """
    Validates the final response before returning it to the user.

    Returns:
        (True, response)  -> response is safe
        (False, None)     -> response blocked
    """

    try:
        result = output_guard.validate(response)

        if result.validation_passed:
            validated_output = result.validated_output

            return True, (
                validated_output
                if isinstance(validated_output, str)
                else response
            )

        return False, None

    except Exception:
        return False, None