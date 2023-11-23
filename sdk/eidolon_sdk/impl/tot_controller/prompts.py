from textwrap import dedent

COT_PROMPT = {
    'preamble': "You are an intelligent agent that is generating one thought at a time in a tree of thoughts setting.\nPROBLEM:",
    'thoughts': dedent(
        """
        {% if thoughts %}
        THOUGHTS
        
        {% for thought in thoughts %}
        {{ thought }}
        {% endfor %}
        {% endif %}
        """
    ).strip(),
    'post-amble': "Let's think step by step."
}

PROPOSE_PROMPT = {
    'preamble': "You are an intelligent agent that is generating thoughts in a tree of thoughts setting.\nPROBLEM:",
    'thoughts': dedent(
        """
        {% if thoughts %}
        THOUGHTS
        
        {% for thought in thoughts %}
        {{ thought }}
        {% endfor %}
        {% endif %}
        """
    ).strip(),
    'post-amble': dedent(
        """
        {% if thoughts %}
        Possible next {{ n }} valid thoughts based on the last valid thought:
        {% else %}
        Possible next {{ n }} valid thoughts based on the PROBLEM:
        {%- endif -%}
        """
    ).strip(),
}

CHECKER_PROMPT = dedent(
    """
    You are an intelligent agent, validating thoughts of another intelligent agent.

    THOUGHTS
    
    {thoughts}

    Evaluate the thoughts and respond with one word.

    - Respond VALID if the last thought is a valid final solution to the
    problem.
    - Respond INVALID if the last thought is invalid.
    - Respond INTERMEDIATE if the last thought is valid but not the final
    solution to the problem.

    This chain of thoughts is"""
).strip(),
