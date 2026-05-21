import { ChatProvider } from "./context/ChatContext";
import ChatScreen from "./components/ChatScreen";
import "./index.css";

export default function App() {
  return (
    <ChatProvider>
      <div className="app-root">
        {/* Background decorative blurs */}
        <div className="bg-accent bg-accent--right" />
        <div className="bg-accent bg-accent--left" />
        <ChatScreen />
      </div>
    </ChatProvider>
  );
}
