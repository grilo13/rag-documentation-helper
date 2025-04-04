"use client";

import type {ReactNode} from "react";
import {
    AssistantRuntimeProvider,
    useLocalRuntime,
    type ChatModelAdapter,
} from "@assistant-ui/react";

const MyModelAdapter: ChatModelAdapter = {
    async run({messages, abortSignal}) {
        console.log("here")
        console.log("print messages")
        console.log(JSON.stringify({
            messages,
        }))
        const result = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // forward the messages in the chat to the API
            body: JSON.stringify({
                messages,
            }),
            // if the user hits the "cancel" button or escape keyboard key, cancel the request
            signal: abortSignal,
        });

        console.log("result")
        console.log("result status code", result.status)

        const data = await result.json();
        return {
            content: [
                {
                    type: "text",
                    text: data.text,
                },
            ],
        };
    },
};

export function MyRuntimeProvider({
                                      children,
                                  }: Readonly<{
    children: ReactNode;
}>) {
    const runtime = useLocalRuntime(MyModelAdapter);

    return (
        <AssistantRuntimeProvider runtime={runtime}>
            {children}
        </AssistantRuntimeProvider>
    );
}