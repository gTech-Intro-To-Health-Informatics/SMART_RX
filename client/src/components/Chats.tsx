'use client'

import { useEffect, useState } from 'react';
import axios from 'axios';
import Link from 'next/link';

export default function Chats() {
  const [chats, setChats] = useState([]);

  useEffect(() => {
    const fetchChats = async () => {
      try {
        const response = await axios.get('/get_all_conversation_history');
        setChats(response.data);
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    };
    fetchChats();
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">All Patient Chats</h1>
      <div className="space-y-6 max-w-lg mx-auto bg-white p-8 rounded-lg shadow-md">
        {chats.length > 0 ? (
          <ul className="space-y-4">
            {chats.map((chat: any) => (
              <li
                key={chat.id}
                className="border border-gray-300 rounded-md p-4 hover:bg-gray-50 transition duration-200"
              >
                <Link href={`/chat/${chat.id}`} className="text-blue-600 font-semibold hover:underline">
                  {chat.name}'s Chat
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-center text-gray-600">No chats available.</p>
        )}
      </div>
    </div>
  );
}
