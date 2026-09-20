        from pydantic import BaseModel
from mcp.server import MCPServer


mcp = MCPServer(
    "LearningPathServer",
    instructions="MCP tools for generating personalized learning paths.",
)


class RoadmapItem(BaseModel):
    day: int
    topic: str
    task: str


class LearningPath(BaseModel):
    goal: str
    roadmap: list[RoadmapItem]


class LearningResource(BaseModel):
    title: str
    url: str
    purpose: str


class ProjectSuggestion(BaseModel):
    title: str
    description: str


@mcp.tool()
def generate_learning_path(
    subject: str,
    days: int,
    level: str
) -> LearningPath:
    """Generate a personalized day-by-day learning roadmap."""

    days = max(1, min(days, 60))

    topics = [
        "Foundations and Key Concepts",
        "Core Concepts",
        "Syntax and Terminology",
        "Guided Examples",
        "Hands-on Practice",
        "Problem Solving",
        "Intermediate Concepts",
        "Practice Exercises",
        "Real-world Applications",
        "Mini Project",
    ]

    roadmap = []

    for day in range(1, days + 1):

        topic = topics[(day - 1) % len(topics)]

        roadmap.append(
            RoadmapItem(
                day=day,
                topic=f"{subject}: {topic}",
                task=(
                    f"Study {topic.lower()} and complete "
                    f"one practical exercise at "
                    f"{level.lower()} level."
                )
            )
        )

    return LearningPath(
        goal=(
            f"Build a {level.lower()}-level foundation "
            f"in {subject}."
        ),
        roadmap=roadmap
    )


@mcp.tool()
def get_learning_resources(
    subject: str
) -> list[LearningResource]:
    """Provide learning resources."""

    return [
        LearningResource(
            title="Python Official Tutorial",
            url="https://docs.python.org/3/tutorial/",
            purpose="Official Python learning material."
        ),
        LearningResource(
            title="Kaggle Learn",
            url="https://www.kaggle.com/learn",
            purpose="Hands-on courses and exercises."
        ),
        LearningResource(
            title="freeCodeCamp",
            url="https://www.freecodecamp.org/learn/",
            purpose="Interactive programming practice."
        ),
    ]


@mcp.tool()
def suggest_project(
    subject: str,
    level: str
) -> ProjectSuggestion:
    """Suggest a practical project."""

    return ProjectSuggestion(
        title=f"{subject} Student Mini Project",
        description=(
            f"Build a small practical application using "
            f"the main concepts of {subject}. "
            f"The project should be suitable for a "
            f"{level.lower()} learner."
        )
    )
