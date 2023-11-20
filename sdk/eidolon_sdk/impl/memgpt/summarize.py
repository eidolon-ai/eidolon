
def summarize_messages(
    model,
    context_window,
    message_sequence_to_summarize,
):
    """Summarize a message sequence using GPT"""

    summary_prompt = SUMMARY_PROMPT_SYSTEM
    summary_input = str(message_sequence_to_summarize)
    summary_input_tkns = count_tokens(summary_input)
    if summary_input_tkns > MESSAGE_SUMMARY_WARNING_FRAC * context_window:
        trunc_ratio = (MESSAGE_SUMMARY_WARNING_FRAC * context_window / summary_input_tkns) * 0.8  # For good measure...
        cutoff = int(len(message_sequence_to_summarize) * trunc_ratio)
        summary_input = str(
            [summarize_messages(model, context_window, message_sequence_to_summarize[:cutoff])] + message_sequence_to_summarize[cutoff:]
        )
    message_sequence = [
        {"role": "system", "content": summary_prompt},
        {"role": "user", "content": summary_input},
    ]

    response = create(
        model=model,
        messages=message_sequence,
        context_window=context_window,
    )

    printd(f"summarize_messages gpt reply: {response.choices[0]}")
    reply = response.choices[0].message.content
    return reply

