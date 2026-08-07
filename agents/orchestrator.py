"""
Master Orchestrator Agent: مسیریاب هوشمند و مدیر کل ایجنت‌ها
"""
from agents.edulead import EduLeadAgent
from agents.sourcing import SourcingAgent
from agents.risk_audit import RiskAuditAgent
from agents.logistics import LogisticsAgent
from agents.sales import SalesAgent

class MasterOrchestrator:
    @staticmethod
    async def route_request(user_message: str, target_agent: str = None, lang: str = "fa") -> dict:
        msg = user_message.lower().strip()

        # If English mode is enabled or message is in English, instruct agents to reply in English
        processed_message = user_message
        if lang == "en":
            processed_message = f"{user_message}\n\n[SYSTEM INSTRUCTION: User is using English interface. Please reply ENTIRELY in fluent English.]"

        # Check confirmation intent across all agents
        if any(w in msg for w in ["بله", "اره", "آره", "لطفا", "لطفاً", "میخوام", "می‌خوام", "بفرست", "تایید", "موافقم", "دریافت", "yes", "sure", "please", "send"]):
            response = await SalesAgent.process_chat(processed_message)
            return {
                "agent_id": "sales",
                "agent_name": "Sales & Conversion Agent",
                "response": response
            }

        # Explicit agent target or intelligent routing
        if not target_agent or target_agent == "auto":
            if any(w in msg for w in ["ltd", "co.", "co,", "inc", "corp", "shenzhen", "guangdong", "tech", "factory", "اعتبار", "استعلام", "قضایی", "ثبت", "دادگاه", "qcc", "چینی", "audit", "verify"]):
                target_agent = "risk"
            elif any(w in msg for w in ["کد", "hs", "تعرفه", "لاستیک", "تایر", "پزشکی", "دندان", "ماشین", "پلیمر", "پیدا", "قیمت", "خرید", "تامین", "quote", "price", "sourcing"]):
                target_agent = "sourcing"
            elif any(w in msg for w in ["حمل", "کانتینر", "کشتی", "گمرک", "ارز", "نیما", "ترخیص", "shipping", "customs", "freight"]):
                target_agent = "logistics"
            else:
                target_agent = "edulead"

        # Delegate to target agent
        if target_agent == "sourcing":
            response = await SourcingAgent.process_chat(processed_message)
            agent_name = "Sourcing & HS Specialist"
        elif target_agent == "risk":
            response = await RiskAuditAgent.process_chat(processed_message)
            agent_name = "Risk & Audit Analyst"
        elif target_agent == "logistics":
            response = await LogisticsAgent.process_chat(processed_message)
            agent_name = "Logistics & Customs Advisor"
        elif target_agent == "sales":
            response = await SalesAgent.process_chat(processed_message)
            agent_name = "Sales & Conversion Agent"
        else:
            response = await EduLeadAgent.process_chat(processed_message)
            agent_name = "EduLead Agent"

        return {
            "agent_id": target_agent,
            "agent_name": agent_name,
            "response": response
        }
