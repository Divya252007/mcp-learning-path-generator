import asyncio
import json
import streamlit as st

from mcp import Client
from mcp_server import mcp

st.set_page_config(
    page_title="MCP Learning Path Generator",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 MCP-Powered AI Learning Path Generator")
st.caption("A student-friendly demonstration of AI + Model Context Protocol (MCP) tools")

with st.sidebar:
    st.header("Learning Plan")
    topic = st.text_input("What do you want to learn?", "Python and Machine Learning")
    days = st.slider("Learning duration (days)", 7, 60, 30)
    level = st.selectbox("Current level", ["Beginner", "Intermediate", "Advanced"])
    generate = st.button("🚀 Generate Learning Path", use_container_width=True)

def call_mcp_tool(tool_name, arguments):
    async def runner():
        async with Client(mcp) as client:
            result = await client.call_tool(tool_name, arguments)
            return result.structured_content
    return asyncio.run(runner())

if generate:
    with st.spinner("Calling MCP tools and building your roadmap..."):
        plan = call_mcp_tool(
            "generate_learning_path",
            {"topic": topic, "days": days, "level": level},
        )
        resources = call_mcp_tool(
            "find_learning_resources",
            {"topic": topic, "level": level},
        )

    st.success("Learning path generated through MCP tools.")

    st.subheader("🎯 Learning Goal")
    st.write(plan["goal"])

    col1, col2, col3 = st.columns(3)
    col1.metric("Duration", f"{days} days")
    col2.metric("Level", level)
    col3.metric("MCP Tools Used", "2")

    st.subheader("📅 Day-by-Day Roadmap")
    for item in plan["roadmap"]:
        with st.expander(f"Day {item['day']} — {item['topic']}"):
            st.write("**Concepts:**", ", ".join(item["concepts"]))
            st.write("**Practice:**", item["practice"])
            st.write("**Mini task:**", item["task"])

    st.subheader("🎥 Learning Resources")
    for resource in resources["resources"]:
        st.markdown(f"- [{resource['title']}]({resource['url']}) — {resource['type']}")

    st.subheader("💡 Project Ideas")
    for idea in plan["project_ideas"]:
        st.write("•", idea)

    st.download_button(
        "📥 Download Roadmap JSON",
        data=json.dumps(plan, indent=2),
        file_name="learning_path.json",
        mime="application/json",
    )
else:
    st.info("Enter a learning goal in the sidebar and click Generate Learning Path.")

    st.markdown("""
    ### How this demo works

    **User → Streamlit → MCP Client → MCP Server → Tools → Personalized Roadmap**

    This starter project uses the official Python MCP SDK. The two demo tools are
    `generate_learning_path` and `find_learning_resources`.

    The next integration stage can replace the resource tool with real YouTube,
    Google Drive, and Notion connections.
    """)
