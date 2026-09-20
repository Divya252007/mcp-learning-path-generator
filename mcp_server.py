from mcp.server import MCPServer

mcp = MCPServer(
    "LearningPathServer",
    instructions="MCP tools for generating personalized student learning paths.",
)


@mcp.tool()
def generate_learning_path(
    subject: str,
    days: int,
    level: str
) -> dict:
    """Generate a structured learning roadmap."""

    days = max(1, min(days, 60))

    topics = [
        "Foundations and Key Concepts",
        "Core Terminology",
        "Guided Examples",
        "Hands-on Practice",
        "Intermediate Concepts",
        "Problem Solving",
        "Practice Exercises",
        "Review and Debugging",
        "Applied Learning",
        "Mini Project",
    ]

    roadmap = []

    for day in range(1, days + 1):
        topic = topics[(day - 1) % len(topics)]

        roadmap.append({
            "day": day,
            "topic": f"{subject}: {topic}",
            "task": (
                f"Study {topic.lower()} and complete "
                f"one practical exercise at {level.lower()} level."
            ),
        })

    return {
        "goal": (
            f"Build a {level.lower()}-level foundation "
            f"in {subject}."
        ),
        "roadmap": roadmap,
    }


@mcp.tool()
def get_learning_resources(subject: str) -> list[dict]:
    """Return useful learning resources."""

    return [
        {
            "title": "Python Official Tutorial",
            "url": "https://docs.python.org/3/tutorial/",
            "purpose": "Official Python learning material.",
        },
        {
            "title": "Kaggle Learn",
            "url": "https://www.kaggle.com/learn",
            "purpose": "Hands-on courses and exercises.",
        },
        {
            "title": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/",
            "purpose": "Interactive programming practice.",
        },
    ]


@mcp.tool()
def suggest_project(
    subject: str,
    level: str
) -> dict:
    """Suggest a practical student project."""

    return {
        "title": f"{subject} Student Mini Project",
        "description": (
            f"Build a small practical application using "
            f"the main concepts of {subject}. "
            f"Start at {level.lower()} level and document "
            "the problem, approach, implementation and result."
        ),
    }
