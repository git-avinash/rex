import wikipedia

from states.rex_state import RexState


def isMode(mode):
    modes = ("l", "p", "all")

    for mode_str in modes:
        if mode_str == mode:
            return True

    return False


def wiki(query, mode="l"):
    try:
        solved_query = []

        response = wikipedia.summary(query)
        parsed_paragraphs = response.split("\n")
        number_of_paragraphs = len(parsed_paragraphs)
        first_paragraph_lines = parsed_paragraphs[0].split(".")
        number_of_lines_in_first_paragraph = len(first_paragraph_lines)

        if mode == "all":
            return response

        if mode == "p":
            solved_query.append(parsed_paragraphs[0])

            if number_of_paragraphs > 1:
                solved_query.append("\n\n")
                solved_query.append(
                    f"\n📌 Showing *1/{number_of_paragraphs} paragraph* to read.")
                solved_query.append(
                    f"\n📌 Add **all** tag to get the whole article.")
                solved_query.append(
                    f"\n📌 *Example: @Rex search {query} all*")

            return " ".join(solved_query)

        if mode == "l":
            solved_query.append(first_paragraph_lines[0])

            if number_of_lines_in_first_paragraph > 1:
                solved_query.append("\n")
                solved_query.append(
                    f"\n📌 This query has total *{number_of_lines_in_first_paragraph - 1} more lines* ")

            if number_of_paragraphs > 1:
                solved_query.append(
                    f"and *{number_of_paragraphs} paragraphs* to read.")

            solved_query.append(
                f"\n📌 Add **p** tag to read first paragraph or **all** tag to get the whole article.")
            solved_query.append(f"\n📌 *Example: @Rex search {query} p/all*")

            return " ".join(solved_query)

    except:
        return f"Couldn't find results for *'{query}'* 😩"


def search_for(data, parsed_message):
    if len(parsed_message) > 2:

        if not isMode(parsed_message[-1]):
            parsed_message.append("l")

        result = wiki(" ".join(parsed_message[2:-1]), mode=parsed_message[-1])
        RexState.chat_bot_driver.send_message(data["messageid"], result)

    else:
        RexState.chat_bot_driver.send_message(
            data["messageid"], "Please pass a query to search!")
