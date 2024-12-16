from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import time
import sys

# Define the template for the assistant's responses
template = """
Hi there! I'm Nora, your AI assistant. Let me know how I can help, and I'll tailor my responses to your needs. 
Whether it's legal insights, academic support, or general questions, I’m here for you.

**Conversation History:**
{context}

User: {question}
Nora:\
"""

# Initialize model and prompt chain
model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Function to extract the user's name and role from their introduction
def extract_user_details(introduction_text):
    """Extracts the user's name and role from their introduction."""
    name_patterns = [
        r"(?i)(?:my name is|i'm|i am)\s+([A-Za-z\s]+)",  # Matches phrases like "My name is Jay"
        r"([A-Za-z\s]+)(?:,? a lawyer|,? a legal professional|,? an attorney)",  # Matches "Jay, a lawyer"
    ]
    role_patterns = [
        r"(?i)\b(?:lawyer|legal professional|attorney)\b",  # Matches "lawyer" or similar terms
        r"(?i)\b(?:student|academic)\b",  # Matches "student"
    ]

    name = "User"  # Default name
    role = "user"  # Default role

    # Extract name
    for pattern in name_patterns:
        match = re.search(pattern, introduction_text)
        if match:
            name = match.group(1).strip()
            break

    # Extract role
    for pattern in role_patterns:
        match = re.search(pattern, introduction_text)
        if match:
            role = match.group(0).lower()
            break

    return name, role

# Real-time typing effect function
def type_writer(text, delay=0.03):
    """Simulates real-time typing effect for any given response."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")

# Function to handle conversation flow
def handle_conversation(user_input, context):
    try:
        # Example: Customize follow-ups based on context
        if "case" in user_input.lower():
            follow_up = "Could you tell me more about the case? Any specific issues you're dealing with?"
        else:
            follow_up = "What else can I assist you with?"

        # Pass the user input and context to the model
        result = chain.invoke({"context": context, "question": user_input})
        return result + "\n\n" + follow_up
    except Exception as e:
        return f"Nora: An error occurred while processing your request. Please try again. Error: {e}"

# Web-like interaction simulation
def web_interaction():
    print()
    print("Nora: Welcome to your AI assistant platform!")
    print()
    
    # Prompt for user introduction
    user_intro = input("Nora: Please introduce yourself: ").strip()
    if user_intro.lower() in ["exit", "quit"]:
        print("Nora: Goodbye! Have a great day!")
        return  # End the program
    
    # Extract user details (name and role)
    user_name, user_role = extract_user_details(user_intro)

    # Generate a personalized welcome message
    if user_role == "lawyer":
        role_message = "case insights, legal references, and tailored guidance."
    elif user_role == "student":
        role_message = "help with assignments, case studies, or understanding legal principles."
    else:
        role_message = "answers to your general queries or tasks."

    # Display personalized welcome message
    type_writer(f"Nora: Hi {user_name}, nice to meet you! Since you're a {user_role}, I can assist with {role_message} How can I help you today?")

    # Initialize context for conversation
    context = f"User: {user_intro}\nNora: Hi {user_name}, nice to meet you!\nNora: Since you're a {user_role}, I can assist with {role_message}"

    while True:
        # Handle conversation loop
        user_input = input(f"{user_name}: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            farewell_message = f"Thank you for using Nora. Goodbye, {user_name}!"
            type_writer(f"Nora: {farewell_message}")
            break

        # Process user query and respond
        response = handle_conversation(user_input, context)
        type_writer(f"Nora: {response}")
        context += f"\nUser: {user_input}\nNora: {response}"

# Start the interaction
web_interaction()