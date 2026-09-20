from mcp.server import MCPServer

mcp = MCPServer(
    "Learning Path Generator",
    instructions="Provides tools for creating personalized learning paths and finding learning resources."
)

@mcp.tool()
def generate_learning_path(topic: str, days: int, level: str) -> dict:
    """Generate a structured learning roadmap for a topic."""
    days = max(1, min(int(days), 60))

    roadmap = []
    for day in range(1, days + 1):
        if day <= max(1, days // 4):
            phase = "Foundations"
            concepts = ["Core terminology", "Basic syntax/concepts", "Small examples"]
        elif day <= max(2, days // 2):
            phase = "Core Skills"
            concepts = ["Important concepts", "Hands-on exercises", "Debugging/problem solving"]
        elif day <= max(3, (days * 3) // 4):
            phase = "Applied Practice"
            concepts = ["Intermediate techniques", "Real-world examples", "Mini project work"]
        else:
            phase = "Project & Review"
            concepts = ["Revision", "Integration", "Final project"]

        roadmap.append({
            "day": day,
            "topic": f"{phase}: {topic}",
            "concepts": concepts,
            "practice": f"Spend 30–60 minutes practicing {topic} at {level} level.",
            "task": f"Complete one small exercise related to {topic}."
        })

    return {
        "goal": f"Build a {days}-day {level.lower()} learning path for {topic}.",
        "roadmap": roadmap,
        "project_ideas": [
            f"Build a small {topic} practice project",
            f"Create a portfolio project demonstrating {topic}",
            f"Document what you learned and the results"
        ]
    }


@mcp.tool()
def find_learning_resources(topic: str, level: str) -> dict:
    """Return learning-resource links relevant to a topic."""
    query = topic.replace(" ", "+")
    return {
        "resources": [
            {
                "title": f"YouTube search: {topic}",
                "url": f"https://www.youtube.com/results?search_query={query}+{level.lower()}",
                "type": "Video search"
            },
            {
                "title": f"Google search: {topic} documentation",
                "url": f"https://www.google.com/search?q={query}+documentation",
                "type": "Documentation search"
            }
        ]
    }


if __name__ == "__main__":
    mcp.run()
