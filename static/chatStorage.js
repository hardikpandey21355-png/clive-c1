// chatStorage.js - Firebase Chat Management
import { auth, db } from "/static/firebase.js";
import {
  collection,
  addDoc,
  getDocs,
  query,
  orderBy,
  serverTimestamp,
  doc,
  setDoc,
  deleteDoc,
  updateDoc
} from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

/* ===============================
   SAVE ENTIRE CHAT HISTORY
================================ */
export async function saveChatHistoryToFirestore(chatHistory) {
  const user = auth.currentUser;
  if (!user) {
    console.log("⚠️ No user logged in, skipping Firebase save");
    return;
  }

  try {
    // Save each chat as a separate document
    for (const [chatId, chatData] of Object.entries(chatHistory)) {
      const chatRef = doc(db, "users", user.uid, "chats", chatId);
      
      await setDoc(chatRef, {
        title: chatData.title,
        messages: chatData.messages,
        timestamp: chatData.timestamp,
        updatedAt: serverTimestamp()
      });
    }
    
    console.log("💾 Chat history saved to Firestore");
  } catch (error) {
    console.error("❌ Error saving to Firestore:", error);
  }
}

/* ===============================
   LOAD ALL USER CHATS
================================ */
export async function loadChatsFromFirestore() {
  const user = auth.currentUser;
  if (!user) {
    console.log("⚠️ No user logged in, returning empty chat history");
    return {};
  }

  try {
    const q = query(
      collection(db, "users", user.uid, "chats"),
      orderBy("timestamp", "desc")
    );

    const snapshot = await getDocs(q);
    const chatHistory = {};

    snapshot.forEach(docSnap => {
      const data = docSnap.data();
      const chatId = docSnap.id;

      chatHistory[chatId] = {
        title: data.title || "Untitled Chat",
        messages: data.messages || [],
        timestamp: data.timestamp || Date.now(),
        animationPlayed: true // Don't replay animation on load
      };
    });

    console.log("📥 Loaded", Object.keys(chatHistory).length, "chats from Firestore");
    return chatHistory;
  } catch (error) {
    console.error("❌ Error loading from Firestore:", error);
    return {};
  }
}

/* ===============================
   SAVE SINGLE CHAT
================================ */
export async function saveSingleChat(chatId, chatData) {
  const user = auth.currentUser;
  if (!user) return;

  try {
    const chatRef = doc(db, "users", user.uid, "chats", chatId);
    
    await setDoc(chatRef, {
      title: chatData.title,
      messages: chatData.messages,
      timestamp: chatData.timestamp,
      updatedAt: serverTimestamp()
    });
    
    console.log("💾 Chat", chatId, "saved to Firestore");
  } catch (error) {
    console.error("❌ Error saving chat:", error);
  }
}

/* ===============================
   DELETE SINGLE CHAT
================================ */
export async function deleteChatFromFirestore(chatId) {
  const user = auth.currentUser;
  if (!user) return;

  try {
    const chatRef = doc(db, "users", user.uid, "chats", chatId);
    await deleteDoc(chatRef);
    console.log("🗑️ Chat", chatId, "deleted from Firestore");
  } catch (error) {
    console.error("❌ Error deleting chat:", error);
  }
}

/* ===============================
   UPDATE CHAT TITLE
================================ */
export async function updateChatTitle(chatId, newTitle) {
  const user = auth.currentUser;
  if (!user) return;

  try {
    const chatRef = doc(db, "users", user.uid, "chats", chatId);
    await updateDoc(chatRef, {
      title: newTitle,
      updatedAt: serverTimestamp()
    });
    console.log("✏️ Chat title updated in Firestore");
  } catch (error) {
    console.error("❌ Error updating title:", error);
  }
}

/* ===============================
   CLEAR ALL CHATS (for logout)
================================ */
export async function clearAllChats() {
  const user = auth.currentUser;
  if (!user) return;

  try {
    const q = query(collection(db, "users", user.uid, "chats"));
    const snapshot = await getDocs(q);
    
    const deletePromises = [];
    snapshot.forEach(docSnap => {
      deletePromises.push(deleteDoc(docSnap.ref));
    });
    
    await Promise.all(deletePromises);
    console.log("🗑️ All chats cleared from Firestore");
  } catch (error) {
    console.error("❌ Error clearing chats:", error);
  }
}

