import os

from eidos_sdk.agent.doc_manager.parsers.base_parser import DataBlob
from eidos_sdk.agent.doc_manager.parsers.pdf_parsers import PyPDFParser, PyPDFParserSpec


class TestPDFParser:

    def test_parse(self):
        data = DataBlob.from_path(os.path.dirname(os.path.abspath(__file__)) + "/AgentXOS.pdf")
        parser = PyPDFParser(PyPDFParserSpec())
        docs = list(parser.parse(data))
        assert len(docs) == 24
        doc = docs[0]
        assert doc.metadata["source"] == os.path.dirname(os.path.abspath(__file__)) + "/AgentXOS.pdf"
        assert doc.metadata["mime_type"] == "application/pdf"
        assert doc.page_content == """ Agent  X  OS 
 Overview 
 LLM Agents have been shown capable of solving a wide variety of tasks. 
 For example, in the paper  “Generative Agents: Interactive Simulacra of Human Behavior”  a group 
 of LLM agents were set up to mimic a town in the style of the video game “The SIMS”. In the 
 paper  “Ghost in the Minecraft: Generally Capable Agents for Open-World Environments via Large 
 Language Models with Text-based Knowledge and Memory”  a series of generally capable 
 agents were prompted to ﬁnd and craft items in the Minecraft world using a series of actions 
 and rewards for those actions. Finally in the paper  “VOYAGER: An Open-Ended Embodied Agent 
 with Large Language Models”  a group of LLMs work in concert to learn new code and 
 dynamically update their prompting strategies as they explore a Minecraft world. 
 Each of these papers implement their own framework to run, manage, and evaluate the multiple 
 agents running in these systems. They each have their own way to record memories, their own 
 way to abstract the LLM, and their own way to manage the agent runtime environment. 
 We propose a new system,  AgentXOS  , that introduces a series of abstractions for single or 
 multi-agent systems. 
 Goals 
 1.  Lorem ipsum dolor sit amet:  Duis autem vel eum iriure  dolor in hendrerit in vulputate 
 velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et 
 accumsan. 
 2.  Sed diam nonummy nibh euismod:  Nam liber tempor cum soluta nobis eleifend option 
 congue nihil imperdiet doming id quod mazim placerat facer possim assum. 
 What is an Agent? 
"""
