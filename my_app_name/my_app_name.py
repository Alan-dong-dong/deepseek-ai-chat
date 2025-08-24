"""DeepSeek智能问答应用"""

import reflex as rx
import httpx
import asyncio
from typing import List, Dict


class ChatMessage(rx.Base):
    """聊天消息模型"""
    role: str  # "user" 或 "assistant"
    content: str
    timestamp: str = ""


class ChatState(rx.State):
    """聊天应用状态"""
    
    messages: List[ChatMessage] = []
    current_input: str = ""
    is_loading: bool = False
    api_key: str = ""  # 需要设置DeepSeek API密钥
    
    def set_input(self, value: str):
        """设置当前输入"""
        self.current_input = value
    
    def set_api_key(self, key: str):
        """设置API密钥"""
        self.api_key = key
    
    async def send_message(self):
        """发送消息并获取AI回复"""
        if not self.current_input.strip():
            return
        
        # 添加用户消息
        user_message = ChatMessage(
            role="user",
            content=self.current_input.strip()
        )
        self.messages.append(user_message)
        
        # 清空输入框并显示加载状态
        current_question = self.current_input.strip()
        self.current_input = ""
        self.is_loading = True
        
        try:
            # 调用DeepSeek API
            response = await self.call_deepseek_api(current_question)
            
            # 添加AI回复
            ai_message = ChatMessage(
                role="assistant",
                content=response
            )
            self.messages.append(ai_message)
            
        except Exception as e:
            # 错误处理
            error_message = ChatMessage(
                role="assistant",
                content=f"抱歉，发生了错误：{str(e)}"
            )
            self.messages.append(error_message)
        
        finally:
            self.is_loading = False
    
    async def call_deepseek_api(self, message: str) -> str:
        """调用DeepSeek API"""
        if not self.api_key:
            return "请先设置DeepSeek API密钥"
        
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建消息历史
        api_messages = []
        for msg in self.messages[-10:]:  # 只发送最近10条消息作为上下文
            if msg.role in ["user", "assistant"]:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        data = {
            "model": "deepseek-chat",
            "messages": api_messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    def clear_chat(self):
        """清空聊天记录"""
        self.messages = []
    
    def set_example_question(self, question: str):
        """设置示例问题到输入框"""
        self.current_input = question


def message_bubble(message: ChatMessage) -> rx.Component:
    """消息气泡组件 - 科技感设计"""
    return rx.box(
        rx.box(
            rx.text(
                message.content,
                class_name="text-sm leading-relaxed whitespace-pre-wrap"
            ),
            class_name=rx.cond(
                message.role == "user",
                "max-w-[80%] px-5 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 to-blue-600 text-white ml-auto shadow-lg shadow-cyan-500/25 border border-cyan-400/30 backdrop-blur-sm hover:shadow-xl hover:shadow-cyan-500/40 transition-all duration-300",
                "max-w-[80%] px-5 py-4 rounded-2xl bg-gradient-to-r from-emerald-50 to-teal-50 text-gray-800 shadow-lg shadow-emerald-500/10 border border-emerald-200/50 backdrop-blur-sm hover:shadow-xl hover:shadow-emerald-500/20 transition-all duration-300"
            )
        ),
        class_name=rx.cond(
            message.role == "user",
            "flex w-full mb-6 justify-end animate-fade-in-right",
            "flex w-full mb-6 justify-start animate-fade-in-left"
        )
    )


def chat_header() -> rx.Component:
    """聊天头部 - 科技感设计"""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("🤖", class_name="text-2xl animate-pulse"),
                class_name="w-14 h-14 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/30 border border-cyan-400/30 backdrop-blur-sm hover:scale-105 transition-all duration-300"
            ),
            rx.vstack(
                rx.heading(
                    "DeepSeek AI Assistant",
                    size="6",
                    class_name="text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 to-blue-600 font-bold"
                ),
                rx.text(
                    "✨ 我是你的智能助手，可以帮你解决编程、写作、分析等各种问题",
                    class_name="text-gray-600 text-sm font-medium"
                ),
                spacing="1",
                align="start",
                class_name="flex-1"
            ),
            rx.box(
                rx.box(class_name="w-2 h-2 bg-emerald-400 rounded-full animate-ping"),
                rx.box(class_name="absolute w-2 h-2 bg-emerald-500 rounded-full"),
                class_name="relative flex items-center justify-center"
            ),
            spacing="4",
            align="center"
        ),
        class_name="p-6 border-b border-gradient-to-r from-cyan-200/50 to-emerald-200/50 bg-gradient-to-r from-white via-cyan-50/30 to-emerald-50/30 backdrop-blur-sm"
    )


def chat_messages() -> rx.Component:
    """聊天消息区域 - 科技感设计"""
    return rx.box(
        rx.cond(
            ChatState.messages.length() == 0,
            # 空状态设计 - 科技感
            rx.box(
                rx.vstack(
                    rx.box(
                        rx.text("💬", class_name="text-6xl mb-4 animate-bounce"),
                        class_name="relative"
                    ),
                    rx.heading(
                        "🚀 开始你的AI对话之旅",
                        size="5",
                        class_name="text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 to-emerald-600 font-bold text-center mb-2"
                    ),
                    rx.text(
                        "问我任何问题，我会为你提供详细的解答",
                        class_name="text-gray-600 text-center font-medium"
                    ),
                    rx.box(
                        rx.vstack(
                            rx.text("✨ 试试这些问题：", class_name="text-sm text-cyan-600 mb-3 font-semibold"),
                            rx.box(
                                rx.text("💻 帮我写一个Python函数", class_name="text-sm text-gray-700 hover:text-cyan-600 transition-colors duration-200 cursor-pointer"),
                                class_name="p-2 rounded-lg hover:bg-cyan-50/50 transition-all duration-200",
                                on_click=ChatState.set_example_question("帮我写一个Python函数")
                            ),
                            rx.box(
                                rx.text("🧠 解释一下机器学习的概念", class_name="text-sm text-gray-700 hover:text-emerald-600 transition-colors duration-200 cursor-pointer"),
                                class_name="p-2 rounded-lg hover:bg-emerald-50/50 transition-all duration-200",
                                on_click=ChatState.set_example_question("解释一下机器学习的概念")
                            ),
                            rx.box(
                                rx.text("✍️ 给我一些创意写作的建议", class_name="text-sm text-gray-700 hover:text-blue-600 transition-colors duration-200 cursor-pointer"),
                                class_name="p-2 rounded-lg hover:bg-blue-50/50 transition-all duration-200",
                                on_click=ChatState.set_example_question("给我一些创意写作的建议")
                            ),
                            spacing="2",
                            align="center",
                            class_name="mt-4"
                        ),
                        class_name="p-4 rounded-2xl bg-gradient-to-br from-white/80 to-gray-50/80 backdrop-blur-sm border border-gray-200/50 shadow-lg"
                    ),
                    spacing="4",
                    align="center"
                ),
                class_name="flex items-center justify-center h-full p-8"
            ),
            # 消息列表
            rx.vstack(
                rx.foreach(
                    ChatState.messages,
                    message_bubble
                ),
                spacing="0",
                class_name="p-6"
            )
        ),
        # 加载状态 - 科技感
        rx.cond(
            ChatState.is_loading,
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.spinner(size="2", class_name="text-cyan-500"),
                        class_name="animate-pulse"
                    ),
                    rx.text("🤖 DeepSeek 正在思考...", class_name="text-gray-700 text-sm font-medium"),
                    rx.box(
                        rx.box(class_name="w-1 h-1 bg-cyan-400 rounded-full animate-ping"),
                        rx.box(class_name="w-1 h-1 bg-emerald-400 rounded-full animate-ping animation-delay-100"),
                        rx.box(class_name="w-1 h-1 bg-blue-400 rounded-full animate-ping animation-delay-200"),
                        class_name="flex space-x-1"
                    ),
                    spacing="3",
                    align="center"
                ),
                class_name="p-4 bg-gradient-to-r from-cyan-50/80 to-emerald-50/80 mx-6 rounded-2xl border border-cyan-200/50 shadow-lg backdrop-blur-sm"
            )
        ),
        class_name="flex-1 overflow-y-auto bg-gradient-to-br from-slate-50 via-cyan-50/30 to-emerald-50/30",
        id="chat-messages"
    )


def chat_input() -> rx.Component:
    """聊天输入区域 - 科技感设计"""
    return rx.box(
        rx.hstack(
            rx.input(
                placeholder="💭 输入你的问题，按回车发送...",
                value=ChatState.current_input,
                on_change=ChatState.set_input,
                on_key_down=lambda key: rx.cond(
                    key == "Enter",
                    ChatState.send_message(),
                    rx.noop()
                ),
                class_name="flex-1 px-5 py-4 text-gray-800 bg-gradient-to-r from-white to-gray-50/50 border border-cyan-200/50 rounded-2xl focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400 min-h-[52px] leading-relaxed shadow-lg shadow-cyan-500/5 backdrop-blur-sm hover:shadow-xl hover:shadow-cyan-500/10 transition-all duration-300 placeholder:text-gray-500",
                disabled=ChatState.is_loading
            ),
            rx.button(
                rx.cond(
                    ChatState.is_loading,
                    rx.hstack(
                        rx.spinner(size="2", class_name="text-white"),
                        rx.text("思考中", class_name="text-white font-medium text-sm"),
                        spacing="2",
                        align="center"
                    ),
                    rx.hstack(
                        rx.text("🚀", class_name="text-lg"),
                        rx.text("发送", class_name="text-white font-medium"),
                        spacing="2",
                        align="center"
                    )
                ),
                on_click=ChatState.send_message,
                disabled=ChatState.is_loading,
                class_name="px-6 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-2xl hover:from-cyan-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed min-h-[52px] shadow-lg shadow-cyan-500/25 hover:shadow-xl hover:shadow-cyan-500/40 transition-all duration-300 hover:scale-105"
            ),
            spacing="4",
            align="center",
            class_name="w-full"
        ),
        class_name="p-6 border-t border-gradient-to-r from-cyan-200/30 to-emerald-200/30 bg-gradient-to-r from-white via-cyan-50/20 to-emerald-50/20 backdrop-blur-sm"
    )


def api_key_input() -> rx.Component:
    """API密钥输入 - 科技感设计"""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("🔑", class_name="text-lg animate-pulse"),
                class_name="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-xl flex items-center justify-center shadow-lg shadow-orange-500/30 border border-orange-400/30 backdrop-blur-sm hover:scale-105 transition-all duration-300"
            ),
            rx.vstack(
                rx.text("DeepSeek API Key", class_name="text-sm font-bold text-transparent bg-clip-text bg-gradient-to-r from-orange-600 to-red-600"),
                rx.text("🔐 安全连接", class_name="text-xs text-gray-500"),
                spacing="0",
                align="start"
            ),
            rx.input(
                placeholder="🔐 sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                type="password",
                on_change=ChatState.set_api_key,
                class_name="flex-1 px-4 py-3 text-gray-800 bg-gradient-to-r from-white to-orange-50/30 border border-orange-200/50 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-400/50 focus:border-orange-400 text-sm min-h-[44px] leading-relaxed shadow-lg shadow-orange-500/5 backdrop-blur-sm hover:shadow-xl hover:shadow-orange-500/10 transition-all duration-300 placeholder:text-gray-500"
            ),
            rx.button(
                rx.hstack(
                    rx.text("🗑️", class_name="text-sm"),
                    rx.text("清空", class_name="text-white font-medium text-sm"),
                    spacing="1",
                    align="center"
                ),
                on_click=ChatState.clear_chat,
                class_name="px-4 py-3 bg-gradient-to-r from-red-500 to-pink-600 text-white rounded-xl hover:from-red-600 hover:to-pink-700 text-sm min-h-[44px] shadow-lg shadow-red-500/25 hover:shadow-xl hover:shadow-red-500/40 transition-all duration-300 hover:scale-105"
            ),
            spacing="4",
            align="center",
            class_name="w-full"
        ),
        class_name="p-5 border-b border-gradient-to-r from-orange-200/30 to-red-200/30 bg-gradient-to-r from-white via-orange-50/20 to-red-50/20 backdrop-blur-sm"
    )


def index() -> rx.Component:
    """主页面 - 科技感设计"""
    return rx.box(
        # 背景装饰元素
        rx.box(
            rx.box(class_name="absolute top-0 left-0 w-72 h-72 bg-gradient-to-br from-cyan-400/20 to-blue-600/20 rounded-full blur-3xl animate-pulse"),
            rx.box(class_name="absolute top-20 right-0 w-96 h-96 bg-gradient-to-br from-emerald-400/15 to-teal-600/15 rounded-full blur-3xl animate-pulse animation-delay-1000"),
            rx.box(class_name="absolute bottom-0 left-1/4 w-80 h-80 bg-gradient-to-br from-purple-400/10 to-pink-600/10 rounded-full blur-3xl animate-pulse animation-delay-2000"),
            class_name="fixed inset-0 pointer-events-none overflow-hidden"
        ),
        # 主要内容区域
        rx.box(
            api_key_input(),
            chat_header(),
            chat_messages(),
            chat_input(),
            class_name="h-screen flex flex-col bg-gradient-to-br from-white via-slate-50/50 to-gray-100/30 max-w-5xl mx-auto w-full border-x border-gradient-to-b from-cyan-200/30 via-gray-200/50 to-emerald-200/30 shadow-2xl shadow-cyan-500/10 backdrop-blur-sm relative z-10"
        ),
        class_name="min-h-screen bg-gradient-to-br from-slate-100 via-cyan-50/30 to-emerald-50/30 relative overflow-hidden"
    )


app = rx.App(
    theme=rx.theme(
        accent_color="cyan",
        gray_color="slate",
        radius="large",
        scaling="100%"
    ),
    head_components=[
        rx.el.title("🚀 DeepSeek AI - 智能问答助手"),
        rx.el.meta(
            name="description",
            content="基于DeepSeek API的现代化智能问答应用 - 科技感UI设计"
        ),
        rx.el.meta(
            name="keywords",
            content="DeepSeek, AI, 人工智能, 聊天机器人, 智能助手"
        ),
        rx.el.meta(
            name="viewport",
            content="width=device-width, initial-scale=1.0"
        ),
        # 添加自定义CSS动画
        rx.el.style(
            """
            @keyframes fade-in-right {
                from { opacity: 0; transform: translateX(20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            @keyframes fade-in-left {
                from { opacity: 0; transform: translateX(-20px); }
                to { opacity: 1; transform: translateX(0); }
            }
            .animate-fade-in-right {
                animation: fade-in-right 0.5s ease-out;
            }
            .animate-fade-in-left {
                animation: fade-in-left 0.5s ease-out;
            }
            .animation-delay-100 {
                animation-delay: 100ms;
            }
            .animation-delay-200 {
                animation-delay: 200ms;
            }
            .animation-delay-1000 {
                animation-delay: 1000ms;
            }
            .animation-delay-2000 {
                animation-delay: 2000ms;
            }
            """
        )
    ]
)
app.add_page(index, route="/")
