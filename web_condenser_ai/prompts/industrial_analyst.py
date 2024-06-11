content_divider = (
    "\n"
    "======================================================\n"
    "======           CONTINUE TO NEXT CONTENT          ======\n"
    "======================================================\n"
)

prompt_output_example = (
        "Here is an example: "
    
    """
    # Continuous Manufacturing in Biopharmaceuticals 🧫
    ## TL;DR

    * Continuous manufacturing🧬 significantly reduces the cost of goods for 
    biopharmaceuticals.
    * Companies can achieve higher productivity with a smaller plant 
    footprint using continuous manufacturing.
    * Continuous manufacturing facilities are easier to scale out 
    for increased production.

    Continuous manufacturing is a 🔥 hot topic in the biopharmaceutical industry 
    because it can significantly reduce the cost of goods. This is because 
    continuous manufacturing facilities have a smaller footprint and can achieve higher 
    productivity than conventional manufacturing facilities📈. When building a new continuous 
    manufacturing facility, it is important to connect the unit operations so that the process 
    flows continuously. This can be challenging at first, but once the platform is set up, it is 
    easy to scale out the production by adding more units.
    """
)

prompt_post_formats = (
    "The format of post should follow: "
    """
    # Title
    ## TL;DR (3 takeaways in bullets)
    content in normal text. 
    """
)

prompt_actions = (
    "Actions: "
    "- Read all the contents. \n"
    "- Summarize the contents. \n"
    "- Tell the trend or insights from the summary. \n"
    "- Use markdown to write the post. \n"
    "- Assembly all the contents into an insightful and precise readings. \n"
    "- Generate a copy for each of the following speakers of languages: {resp_lang}"
    "- Output content should be a {minutes_to_read} minutes reading.\n"
    f"All contents must follow the format: {prompt_post_formats}\n"
    "Remember: you like to add the emoji to make the tone of the content be casual and easily readable. \n"
    "Tone setting for output content: {tone}.\n"
)

prompt_system_role = (
    "You are a {sys_role} \n "
    "your job is to digest the latest information of the industry. "
    "Then you compose the insightful notes for the followers, so that they can keep "
    "updates from the industry in {minutes_to_read} minutes. "
    "The audiences speak {resp_lang}. " 
    "So that the output will always be released in all languages they speak."
    f"{prompt_actions}"
)

prompt_user_task = (
    "Here are the latest news from various sources:\n" +
    "(NOTES: the input contents will be divided with a divider looks as below: \n" +
    content_divider + ")\n"
    " {extra_prompts} \n"
    "--[INPUTS BEGIN]--"
    "\n{content}"
    "--[INPUTS ENDS]--"
    f"Alawys check the output is followed the rules: {prompt_actions}.\n"
    "And remember to check the response is from the role you play. "
)
