from textwrap import dedent

PREAMBLE = "You are an intelligent agent that is generating one thought at a time in a tree of thoughts setting.\nPROBLEM:"
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
    Possible next {{ n }} valid thoughts based on the last valid thought:
    {% else %}
    Possible next {{ n }} valid thoughts based on the PROBLEM:
    {%- endif -%}
    """
).strip()

CHECKER_PROMPT = dedent(
    """
    You are an intelligent agent, validating thoughts of another intelligent agent.

    Evaluate the thoughts and question and respond with one word.

    - Respond VALID if the last thought is a valid final solution to the question.
    - Respond INVALID if the last thought is invalid.
    - Respond INTERMEDIATE if the last thought is valid but not the final solution to the question.
    
    {% if problem %}
    <QUESTION>
    {{ problem }}
    </QUESTION>
    {% endif %}
    
    {% if thoughts %}
    <THOUGHTS>
    {% for thought in thoughts %}
    {{ thought }}
    {% endfor %}
    </THOUGHTS>
    {% endif %}
    """
).strip()
