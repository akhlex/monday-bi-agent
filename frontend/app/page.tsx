"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"

type Message = {
  role: "user" | "assistant"
  text: string
}

function TypingIndicator() {
  return (
    <div className="flex gap-1 items-center">
      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
      <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
    </div>
  )
}

const examplePrompts = [
  "How is our pipeline?",
  "Which sector performs best?",
  "How much receivable do we have?",
  "Deals closing this quarter",
  "Generate leadership update"
]

export default function Home() {

  const [input, setInput] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  async function sendMessage(customMessage?: string) {

      const message = customMessage ?? input

      if (!message.trim()) return

      const userMessage: Message = { role: "user", text: message }

      setMessages((prev) => [...prev, userMessage])
      setInput("")
      setLoading(true)

      try {

        const res = await fetch("https://monday-bi-agent.onrender.com/query", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ question: message })
        })

        const data = await res.json()

        const botMessage: Message = {
          role: "assistant",
          text: data.answer
        }

        setMessages((prev) => [...prev, botMessage])

      } catch {

        setMessages((prev) => [
          ...prev,
          { role: "assistant", text: "Error contacting backend." }
        ])

      }

      setLoading(false)
    }

  return (
    <main className="flex h-screen bg-slate-900 text-white">

      {/* Sidebar */}
      <div className="w-64 bg-slate-950 border-r border-slate-800 p-5">

        <h2 className="text-lg font-semibold mb-4">
          Example Questions
        </h2>

        <div className="space-y-2">

          {examplePrompts.map((prompt, i) => (

            <button
              key={i}
              onClick={() => sendMessage(prompt)}
              className="w-full text-left p-3 rounded-lg bg-slate-800 hover:bg-slate-700 transition"
            >
              {prompt}
            </button>

          ))}

        </div>

      </div>

      {/* Chat Area */}
      <div className="flex flex-col flex-1">

        {/* Header */}
        <div className="border-b border-slate-800 px-6 py-4">
          <h1 className="text-xl font-semibold">
            Monday BI Agent
          </h1>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">

          {messages.map((m, i) => (

            <div
              key={i}
              className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
            >

              <div
                className={`max-w-xl px-4 py-3 rounded-2xl ${
                  m.role === "user"
                    ? "bg-blue-600"
                    : "bg-slate-800"
                }`}
              >

                {m.role === "assistant" ? (
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown>{m.text}</ReactMarkdown>
                  </div>
                ) : (
                  <p>{m.text}</p>
                )}

              </div>

            </div>

          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-800 px-4 py-3 rounded-2xl">
                <TypingIndicator />
              </div>
            </div>
          )}

        </div>

        {/* Input */}
        <div className="border-t border-slate-800 p-4 flex gap-3">

          <input
            className="flex-1 bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage()
            }}
            placeholder="Ask about pipeline, receivables, projects..."
          />

          <button
            onClick={() => sendMessage()}
            className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg"
          >
            Send
          </button>

        </div>

      </div>

    </main>
  )
}