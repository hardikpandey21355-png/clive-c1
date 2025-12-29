from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
import os
import json  # ✅ ADD THIS at top with other imports

# CONNECT BACKEND FOLDER
from backend.free_brain import get_free_response
from backend.paid_brain import get_paid_response
from backend.Read_file import read_file
from flask import Flask, jsonify, render_template, request





# CONNECT BACKEND FOLDER
from backend.free_brain import get_free_response
from backend.paid_brain import get_paid_response




app = Flask(__name__)
# ✨ CONVERSATION MEMORY STORAGE
# Stores conversation history for each chat session
conversation_sessions = {}




@app.route("/")
def home():
    return render_template("intro.html")

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/chat")
def chat():
    return render_template("index.html")





@app.route('/profile')
def profile():
    return render_template('yourprofile/yourprofile.html')





@app.route('/plan')
def plan():
    return render_template('plan.html')





@app.route('/login')
def login_page():
    return render_template('login.html')





@app.route('/settings')
def settings():
    return render_template('setting.html')





@app.route("/personalization")
def personalization():
    return render_template("personalization.html")





@app.route("/library")
def library():
    return render_template("library.html")




@app.route('/create-image')
def create_image():
    return render_template('create_image.html')




@app.route('/save-personalization', methods=['POST'])
def save_personalization():
    try:
        data = request.json
        user_id = "current_user_id"  # Get from session/auth
        
        # Save to database or file
        # For now, just print
        print(f"Saving personalization for user: {data}")
        
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500





# 🔥 MAIN AI ROUTE WITH MEMORY
@app.route("/ask", methods=["POST"])
def ask_clive():
    try:
        data = request.get_json()
        user_msg = data.get("message")
        user_type = data.get("type", "free")
        session_id = data.get("session_id", "default")  # ✨ Get unique chat ID
        personalization = data.get("personalization", None)  # ✅ ADD THIS LINE
        print(f"📩 Received: {user_msg}")
        print(f"🆔 Session: {session_id}")
        # ✨ Create conversation history if new session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []
        # Get conversation history for this session
        history = conversation_sessions[session_id]
        print(f"📚 History: {len(history)} messages")
        # ✨ Get AI response WITH history
        if user_type == "paid":
            reply = get_paid_response(user_msg, history)
        else:
            reply = get_free_response(user_msg, history, personalization=personalization)  # ✅ UPDATED
        # ✨ Save conversation to memory
        conversation_sessions[session_id].append({
            "role": "user",
            "content": user_msg
        })
        conversation_sessions[session_id].append({
            "role": "assistant",
            "content": reply
        })
        # ✨ Keep only last 20 messages (10 exchanges) to save memory
        if len(conversation_sessions[session_id]) > 20:
            conversation_sessions[session_id] = conversation_sessions[session_id][-20:]
        print(f"✅ Reply sent | History now: {len(conversation_sessions[session_id])} messages")
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"reply": "Sorry, something went wrong!"}), 500
    




# ✨ CLEAR HISTORY WHEN STARTING NEW CHAT
@app.route("/clear-history", methods=["POST"])
def clear_history():
    try:
        data = request.get_json()
        session_id = data.get("session_id", "default")
        if session_id in conversation_sessions:
            conversation_sessions[session_id] = []
            print(f"🗑️ Cleared history for: {session_id}")
        return jsonify({"status": "success"})
    except Exception as e:
        print(f"❌ Clear error: {str(e)}")
        return jsonify({"status": "error"}), 500
    



# 📄 FILE UPLOAD ROUTE
@app.route("/ask-with-file", methods=["POST"])
def ask_with_file():
    try:
        user_msg = request.form.get('message', '')
        session_id = request.form.get('session_id', 'default')
        user_type = request.form.get('type', 'free')
        personalization_json = request.form.get('personalization', None)  # ✅ ADD THIS
        personalization = json.loads(personalization_json) if personalization_json else None  # ✅ ADD THIS
        file_content = None
        
        print(f"📩 Received message with file")
        
        # Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = 'uploads'
                
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                
                print(f"📄 Reading file: {filename}")
                file_content = read_file(filepath)
                print(f"✅ File content extracted: {len(file_content)} characters")
                
                # Delete file after reading
                os.remove(filepath)
        
        # Create conversation history if new session
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []
        
        history = conversation_sessions[session_id]
        
        # Get AI response with file content
        reply = get_free_response(user_msg, history, file_content, personalization)  # ✅ UPDATED
        
        # Save conversation to memory
        conversation_sessions[session_id].append({
            "role": "user",
            "content": user_msg
        })
        conversation_sessions[session_id].append({
            "role": "assistant",
            "content": reply
        })
        
        if len(conversation_sessions[session_id]) > 20:
            conversation_sessions[session_id] = conversation_sessions[session_id][-20:]
        
        return jsonify({"reply": reply})
    
    except Exception as e:
        print(f"❌ File upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"reply": "Sorry, something went wrong with the file!"}), 500





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



