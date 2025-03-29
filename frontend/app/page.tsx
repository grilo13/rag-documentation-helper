"use client";
import { Thread } from "@/components/assistant-ui/thread";
// import { useChatRuntime } from "@assistant-ui/react-ai-sdk";
// import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { ThreadList } from "@/components/assistant-ui/thread-list";
// import {MyRuntimeProvider} from "@/app/MyRuntimeProvider";
import  {MyRuntimeStreamingProvider} from "@/app/MyRuntimeStreamingProvider";

export default function Home() {
  // const runtime = useChatRuntime({ api: "/api/chat" });

  return (
    <MyRuntimeStreamingProvider>
      <main className="h-dvh grid grid-cols-[200px_1fr] gap-x-2 px-4 py-4">
        <ThreadList />
        <Thread />
      </main>
    </MyRuntimeStreamingProvider>
  );
}
