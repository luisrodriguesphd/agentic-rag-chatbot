import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "agentic_rag_chatbot",
    version = "0.0.1",
    author = "Luis Rodrigues, PhD",
    author_email = "luisrodriguesphd@gmail.com",
    description = ("""Agentic RAG (Retrieval-Augmented Generation) Chatbot is an AI system \
    that injects intelligence and autonomy into the traditional chatbot framework \
    by combining three key elements: real-time information retrieval, advanced language \
    generation, and an agentic approach."""),
    license = "apache-2.0",
    keywords = ["NLP", "data indexing", "information retrieval", "agentic RAG", "text generation", "chatbot"],
    url = "https://huggingface.co/spaces/luisrodriguesphd/agentic-rag-chatbot",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=read('README.md'),
)
