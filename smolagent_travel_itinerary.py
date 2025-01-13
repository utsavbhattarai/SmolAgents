!pip install smolagents

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    ManagedAgent,
    DuckDuckGoSearchTool,
    HfApiModel
)

model_id = "mistralai/Mistral-7B-Instruct-v0.3"
token = "<HF ACCESS TOKEN>"

model = HfApiModel(model_id=model_id, token=token)

# Gather Trip information Agent (This agent uses JSON-like tool calls)
gather_trip_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    max_steps=20
)

managed_trip_agent = ManagedAgent(
    agent=gather_trip_agent,
    name="destination_super_researcher",
    description="Finds relevant topics verbosely using web scraping and web seraches. Provide the destination as input."
)

# Fact checker Agent
checker_agent = ToolCallingAgent(
    tools=[],
    model=model
)

managed_checker_agent = ManagedAgent(
    agent=checker_agent,
    name="research_checker",
    description="checks the research for relevance to the original taks request. If the research is not relevant, it will ask for more research."
)

# Writer Agent
writer_agent = ToolCallingAgent(
    tools=[],
    model=model
)

managed_writer_agent = ManagedAgent(
    agent=writer_agent,
    name="writer",
    description="Writes a detailed listed posts based on the checkedresearch. Provide the research findings and desired tone/style.",
)

#Format Agent
format_agent = ToolCallingAgent(
    tools=[],
    model=model
)

managed_format_agent = ManagedAgent(
    agent=format_agent,
    name="format_writing",
    description="Writes a detailed listed posts based on the managed_writer_agent. Format properly so that it's human readeable, Also Remove contents that is not relevant to the post"
)

# Main Itinerary Writer Manager
itinerary_manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_trip_agent, managed_checker_agent, managed_writer_agent, managed_format_agent],
    add_base_tools=True,
    additional_authorized_imports=['re', 'requests', 'bs4'],

    # system_prompt="""You are a travel agency manager. Your job is to create destinations for the user query.
    # Follow these steps:
    # 1. Use gather_trip_agent to collect information
    # 2. Use the information from gather_trip_agent to check for relevance using checker_agent
    # 3. Pass research trips to writer_agent to create the travel destination list
    # 4. Use the managed_format_agent to properly format to the output text.
    # """
)

def write_itinerary(topic, output_file="itinerary_post.md"):
    """
    Creates a travel itinerary from the topic using multiple agents

    Args:
        topic: The travel itinerary title
        output_file (str): The filename to save the markdown post
    """
    result = itinerary_manager.run(f"""Create a itinerary post about: {topic}
    1. First, research the topic thoroughly, focus on specific products and sources
    2. Then, write an engaging itinerary post not just a list
    3. Finally, edit and polish the content
    4.) The output should be in a well formatted which is easy to read
    """)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result.content)
    print(f"itinerary has been saved to {output_file}")

    return result

topic = "Create a travel itinerary for the trip to Hawaii. Please include specific details and tourist locations with ratings"
write_itinerary(topic)