from textwrap import dedent

PREAMBLE = "You are an intelligent agent that is generating one thought at a time in a tree of thoughts setting."
THOUGHTS = dedent(
    """
    {% if thoughts %}
    THOUGHTS
    
    {% for thought in thoughts %}
    {{ thought }}
    {% endfor %}
    {% endif %}
    """
).strip()
POST_AMBLE = "Let's think step by step."
POST_AMBLE_MULTI = dedent(
    """
    {% if thoughts %}
    Please generate {{ n }} valid thoughts based on the last valid thought
    {% else %}
    Please generate {{ n }} valid thoughts based on the question
    {%- endif -%}
    """
).strip()

CHECKER_PROMPT = dedent(
    """
    You are an intelligent agent, validating thoughts of another intelligent agent.

    Evaluate the thoughts and question and respond with one word.

    - Respond VALID if the thoughts contain the information needed so answer the question
    - Respond INVALID if the last thought is invalid or does not make progress from previous thoughts.
    - Respond INTERMEDIATE if the last thought is valid but not the final solution to the question.
    
    {% if examples %}
    <EXAMPLEs>
    {{ examples }}
    </EXAMPLE>
    {% endif %}
    
    {% if problem %}
    <QUESTION>
    {{ problem }}
    </QUESTION>
    {% endif %}
    
    {% if thoughts %}
    {% for thought in thoughts %}
    <THOUGHT>
    {{ thought }}
    </THOUGHT>
    {% endfor %}
    {% endif %}
    """
).strip()
