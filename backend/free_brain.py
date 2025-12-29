from groq import Groq

import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def get_free_response(user_message, conversation_history=[], file_content=None, personalization=None):
    """
    ✨ NOW WITH MEMORY, FILE READING, AND PERSONALIZATION
    """
    try:
        # ✅ Build personalized system prompt
        system_prompt = """
You are Clive-V1, an AI assistant created by engineering student Hardik Pandey.

When files are attached:
- Analyze the document content carefully
- Answer questions based on the document
- Be precise and helpful

RESPONSE RULES:
1. Casual chat → Natural, brief, no structure
2. Learning topics → Clear structure with emojis
3. Remember previous conversation context
4. When document is provided, reference it in your answer

Tone: Friendly, clear, student-focused
"""
        
        # ✅ ADD PERSONALIZATION TO SYSTEM PROMPT
        if personalization:
            nickname = personalization.get('nickname', '')
            occupation = personalization.get('occupation', '')
            moreAbout = personalization.get('moreAbout', '')
            style = personalization.get('style', 'Default')
            
            # Add user info to system prompt
            user_info = "\n\n--- USER INFORMATION ---\n"
            
            if nickname:
                user_info += f"• User's preferred name: {nickname}\n"
            
            if occupation:
                user_info += f"• User's occupation: {occupation}\n"
            
            if moreAbout:
                user_info += f"• About the user: {moreAbout}\n"
            
            if style and style != 'Default':
                user_info += f"• Response style preference: {style}\n"
            
            user_info += "\nUse this information naturally in conversation when relevant. If user has a nickname, use it occasionally to make conversation more personal."
            
            system_prompt += user_info
            print(f"✅ Personalization loaded: {nickname or 'No nickname'}")
        
        # Build messages with system prompt + history + new message
        messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Build user message with file content if exists
        full_message = user_message
        if file_content:
            full_message = f"""I have attached a document. Here is its content:

--- DOCUMENT START ---
{file_content}
--- DOCUMENT END ---

My question: {user_message}

Please answer based on the document content above."""
            print(f"📄 Document added to prompt ({len(file_content)} chars)")
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": full_message
        })

        print(f"🧠 Sending {len(messages)} messages to AI")

        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.4,
            max_tokens=2048 if file_content else 350,
            top_p=0.85,
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ AI Error: {str(e)}")
        return "Sorry, something went wrong. Please try again."




def get_streaming_response(user_message):
    """
    Optional: Streaming response for real-time typing effect
    """
    try:
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are Clive-V1, a smart and helpful AI assistant. Be conversational, clear, and concise."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
            stream=True,
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
        
    except Exception as e:
        yield "Sorry, I encountered an error. Please try again!"