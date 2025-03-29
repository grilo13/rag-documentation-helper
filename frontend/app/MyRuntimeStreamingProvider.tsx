"use client";

import type {ReactNode} from "react";
import {
    AssistantRuntimeProvider,
    useLocalRuntime,
    type ChatModelAdapter, ModelContext, ThreadMessage,
} from "@assistant-ui/react";

const backendApi = async ({
                              messages,
                              abortSignal,
                              context,
                          }: {
    messages: readonly ThreadMessage[];
    abortSignal: AbortSignal;
    context: ModelContext;
}) => {
    const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        // forward the messages in the chat to the API
        body: JSON.stringify({
            messages,
            use_stream: true
        }),
        // if the user hits the "cancel" button or escape keyboard key, cancel the request
        signal: abortSignal,
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log("response status", response.status)

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    return {
        async* [Symbol.asyncIterator]() {
            while (reader) {
                const {done, value} = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, {stream: true});

                // Process Server-Sent Events (SSE)
                for (const line of chunk.split("\n")) {
                    if (line.startsWith("data: ")) {
                        yield JSON.parse(line.slice(6));
                    }
                }
            }
        }
    };
};

const MyModelAdapter: ChatModelAdapter = {
    async* run({messages, abortSignal, context}) {
        console.log("here")
        console.log("print messages")
        console.log(JSON.stringify({
            messages,
        }))
        const stream = await backendApi({messages, abortSignal, context});
        let text = "";
        for await (const part of stream) {
            if (part?.chunk) { // Ensure part.chunk exists
                text += part.chunk;
                yield {
                    content: [{ type: "text", text }],
                };
            }
        }
    },
};

export function MyRuntimeStreamingProvider({
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