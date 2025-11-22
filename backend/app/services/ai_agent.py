import json
import anthropic
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.models.agent import AgentState, ConversationMessage, AgentSession

class ZainVoiceAgent:
    def __init__(self, order_data: Dict[str, Any], session_id: str, db_service=None):
        self.session_id = session_id
        self.order_data = order_data
        self.state = AgentState.INIT
        self.conversation_history: List[ConversationMessage] = []
        self.language: Optional[str] = None
        self.customer_authenticated = False
        self.order_confirmed = False
        self.order_modified = False
        self.customer_name: Optional[str] = None
        self.db_service = db_service  # Database service for persistence
        
        # Initialize Claude client (using cheapest model: claude-3-haiku)
        self.claude_client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
        self.model = "claude-3-haiku-20240307"  # Cheapest Claude model
        
    def get_system_prompt(self) -> str:
        """Get system prompt based on language"""
        base_prompt_en = """You are Jassim, a sales representative at Zain Bahrain Telecommunications. You speak in Bahraini Gulf dialect when using Arabic, and clear American accent when using English.

GOAL: Complete digital store orders accurately, comply with regulations, and maintain customer privacy in every interaction.

PERSONALITY:
- Professional yet warm and friendly
- Patient and clear in explanations
- Helpful and solution-oriented
- Respectful of customer time

CONVERSATION RULES:
1. Always start with the fixed opening statement
2. Always end with the fixed closing statement
3. Listen carefully to customer responses
4. Confirm understanding before moving forward
5. Handle interruptions gracefully
6. If customer requests callback, note preferred time and end call
7. Speak naturally - avoid robotic or overly formal language
8. Keep responses concise and clear

CRITICAL RULES:
- Device changes require NEW order - current order must be cancelled
- Plan changes are allowed (any direction: new↔existing)
- Always read back financial details EXACTLY as shown in system
- Never guess or improvise financial information
- If customer is not eligible, present BEST available alternative from system
- Authentication must be completed before proceeding
- Ownership must be verified before order confirmation

CURRENT ORDER CONTEXT:
{order_context}"""

        base_prompt_ar = """أنت جاسم، موظف مبيعات في شركة زين البحرين للاتصالات. تتحدث باللهجة البحرينية الخليجية عند استخدام العربية، وبلهجة أمريكية واضحة عند استخدام الإنجليزية.

الهدف: إكمال إجراءات الطلبات القادمة من المتجر الإلكتروني بدقة، الالتزام بالأنظمة، والمحافظة على خصوصية العميل في كل تواصل.

الشخصية:
- محترف وودود بنفس الوقت
- صبور وواضح في الشرح
- متعاون وحريص على المساعدة
- يحترم وقت العميل

قواعد المحادثة:
١. دايماً ابدأ بالجملة الافتتاحية الثابتة
٢. دايماً اختم بالجملة الختامية الثابتة
٣. اسمع العميل زين وبتركيز
٤. تأكد من الفهم قبل ما تكمل
٥. تعامل مع المقاطعات بشكل لبق
٦. إذا العميل طلب اتصال ثاني، سجل الوقت المفضل وأنهي المكالمة
٧. تكلم بشكل طبيعي - ما تكون رسمي زيادة
٨. خلي ردودك مختصرة وواضحة

قواعد مهمة:
- تغيير الجهاز يتطلب طلب جديد - الطلب الحالي لازم ينلغى
- تغيير الباقة مسموح (أي اتجاه: جديد↔موجود)
- دايماً اقرأ التفاصيل المالية بالضبط كما موجودة في النظام
- لا تخمن أو ترتجل معلومات مالية
- إذا العميل ما يستحق، اعرض أحسن بديل متاح من النظام
- التوثيق لازم يكتمل قبل ما تكمل
- لازم تتأكد من الملكية قبل تأكيد الطلب

سياق الطلب الحالي:
{order_context}"""

        order_context = json.dumps(self.order_data, indent=2, ensure_ascii=False)
        
        if self.language == 'ar':
            return base_prompt_ar.format(order_context=order_context)
        else:
            return base_prompt_en.format(order_context=order_context)
    
    async def process_input(self, user_input: str) -> str:
        """Main processing logic based on current state"""
        # Add user message to history
        user_msg = ConversationMessage(
            role="user",
            content=user_input,
            state=self.state.value,
            timestamp=datetime.now().isoformat()
        )
        self.conversation_history.append(user_msg)
        
        # Save to database if db_service is available
        if self.db_service:
            try:
                self.db_service.add_message(
                    self.session_id,
                    "user",
                    user_input,
                    self.state.value
                )
            except Exception as e:
                print(f"Error saving message to database: {e}")
        
        # State-specific processing
        if self.state == AgentState.INIT:
            response = self.handle_init()
            self.state = AgentState.LANGUAGE_SELECT
            
        elif self.state == AgentState.LANGUAGE_SELECT:
            response = await self.handle_language_selection(user_input)
            if self.language:
                self.state = AgentState.AUTH
            
        elif self.state == AgentState.AUTH:
            response = await self.handle_authentication(user_input)
            
        elif self.state == AgentState.OWNERSHIP_CHECK:
            response = await self.handle_ownership_check(user_input)
            
        elif self.state == AgentState.ORDER_CONFIRM:
            response = await self.handle_order_confirmation(user_input)
            
        elif self.state == AgentState.MODIFICATION:
            response = await self.handle_modification(user_input)
            
        elif self.state == AgentState.ELIGIBILITY_CHECK:
            response = await self.handle_eligibility_check(user_input)
            
        elif self.state == AgentState.COMMITMENT_APPROVAL:
            response = await self.handle_commitment_approval(user_input)
            
        elif self.state == AgentState.CROSS_SELL:
            response = await self.handle_cross_sell(user_input)
            
        elif self.state == AgentState.EKYC_SEND:
            response = await self.handle_ekyc_send(user_input)
            
        else:
            response = "Thank you for choosing Zain, have a good day."
        
        # Add assistant response to history
        assistant_msg = ConversationMessage(
            role="assistant",
            content=response,
            state=self.state.value,
            timestamp=datetime.now().isoformat()
        )
        self.conversation_history.append(assistant_msg)
        
        # Save to database if db_service is available
        if self.db_service:
            try:
                self.db_service.add_message(
                    self.session_id,
                    "assistant",
                    response,
                    self.state.value
                )
                # Update session state in database
                self.db_service.update_session(self.session_id, {
                    "state": self.state.value,
                    "language": self.language,
                    "customer_authenticated": self.customer_authenticated,
                    "order_confirmed": self.order_confirmed,
                    "order_modified": self.order_modified,
                    "customer_name": self.customer_name
                })
            except Exception as e:
                print(f"Error saving message to database: {e}")
        
        return response
    
    def handle_init(self) -> str:
        """Opening statement"""
        # Start with bilingual opening
        response = "Hello, this is Jassim speaking from Zain Bahrain, may I take a few minutes of your time. / مرحبا، معاك جاسم من زين البحرين، ممكن آخذ ثواني من وقتك"
        # Update state after sending initial message
        self.state = AgentState.LANGUAGE_SELECT
        return response
    
    async def handle_language_selection(self, user_input: str) -> str:
        """Detect and set language preference"""
        # Use Claude to detect language preference
        prompt = f"""The customer just responded to: "Would you prefer to continue in Arabic or English? / تفضل نكمل بالعربي ولا الإنجليزي؟"

Customer response: "{user_input}"

Determine if they want Arabic or English. Respond with ONLY one word: "arabic" or "english"."""
        
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            
            lang_choice = response.content[0].text.strip().lower()
            
            if "arabic" in lang_choice or "عربي" in user_input.lower():
                self.language = 'ar'
                return "تمام، نكمل بالعربي. ممكن الاسم الكامل من فضلك؟"
            else:
                self.language = 'en'
                return "Sure, we'll continue in English. Can I please have your full name?"
        except:
            # Fallback detection
            arabic_keywords = ['عربي', 'العربية', 'arabic']
            english_keywords = ['english', 'إنجليزي', 'انجليزي']
            
            if any(kw in user_input.lower() for kw in arabic_keywords):
                self.language = 'ar'
                return "تمام، نكمل بالعربي. ممكن الاسم الكامل من فضلك؟"
            else:
                self.language = 'en'
                return "Sure, we'll continue in English. Can I please have your full name?"
    
    async def handle_authentication(self, user_input: str) -> str:
        """Handle name and CPR verification"""
        # Extract customer info using Claude
        prompt = f"""Extract customer information from this text: "{user_input}"

Return JSON with:
- name (full name if mentioned, otherwise null)
- cpr (ID number if mentioned, 9 digits, otherwise null)

Only include fields that are clearly stated. Return ONLY valid JSON."""
        
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            extracted_text = response.content[0].text.strip()
            # Try to parse JSON from response
            if "{" in extracted_text:
                json_start = extracted_text.find("{")
                json_end = extracted_text.rfind("}") + 1
                extracted_data = json.loads(extracted_text[json_start:json_end])
            else:
                extracted_data = {}
        except:
            extracted_data = {}
        
        # Check if we have name and CPR
        has_name = extracted_data.get('name') or self.customer_name
        has_cpr = extracted_data.get('cpr')
        
        if has_name and not self.customer_name:
            self.customer_name = extracted_data.get('name', '')
        
        if not has_name:
            if self.language == 'ar':
                return "ممكن الاسم الكامل من فضلك؟"
            else:
                return "Can I please have your full name?"
        
        if not has_cpr:
            if self.language == 'ar':
                return "تسلم. وممكن رقم الهوية؟"
            else:
                return "Thank you. And can I have your CPR number please?"
        
        # Verify against order data
        order_name = self.order_data.get('customer', {}).get('name', '').lower()
        order_cpr = self.order_data.get('customer', {}).get('cpr', '')
        
        provided_name = (extracted_data.get('name', '') or self.customer_name or '').lower()
        provided_cpr = extracted_data.get('cpr', '')
        
        # Simple matching (can be enhanced)
        name_match = order_name in provided_name or provided_name in order_name
        cpr_match = order_cpr == provided_cpr
        
        if name_match and cpr_match:
            self.customer_authenticated = True
            self.state = AgentState.ORDER_CONFIRM
            
            if self.language == 'ar':
                return f"مشكور {self.customer_name or 'عليك'}، تأكدت من المعلومات. خلني أأكد تفاصيل طلبك..."
            else:
                return f"Thank you {self.customer_name or ''}, I've verified your details. Let me confirm your order details..."
        else:
            self.state = AgentState.OWNERSHIP_CHECK
            if self.language == 'ar':
                return "ألاحظ إن المعلومات ما تطابق السجلات عندنا. هل تتصل نيابة عن صاحب الحساب؟"
            else:
                return "I notice the details don't match our records. Are you calling on behalf of the account holder?"
    
    async def handle_ownership_check(self, user_input: str) -> str:
        """Handle ownership verification"""
        # For now, accept and move forward
        # In production, would collect correct owner details
        self.state = AgentState.ORDER_CONFIRM
        
        if self.language == 'ar':
            return "فهمت. خلني أأكد تفاصيل الطلب..."
        else:
            return "I understand. Let me confirm the order details..."
    
    async def handle_order_confirmation(self, user_input: str) -> str:
        """Read order details and get confirmation"""
        if not self.order_confirmed:
            # First time - read order details
            order_summary = self.generate_order_summary()
            self.order_confirmed = True
            return order_summary
        
        # Customer response to confirmation
        # Use Claude to detect intent
        prompt = f"""Customer response to order confirmation: "{user_input}"

Determine intent:
- "confirm" if they accept/agree
- "modify" if they want changes
- "reject" if they don't want it

Respond with ONLY one word: confirm, modify, or reject."""
        
        try:
            response = self.claude_client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": prompt}]
            )
            intent = response.content[0].text.strip().lower()
        except:
            # Fallback
            if any(word in user_input.lower() for word in ['yes', 'correct', 'نعم', 'صح', 'صحيح']):
                intent = 'confirm'
            elif any(word in user_input.lower() for word in ['no', 'change', 'لا', 'غير', 'تغيير']):
                intent = 'modify'
            else:
                intent = 'confirm'
        
        if intent == 'confirm':
            self.state = AgentState.ELIGIBILITY_CHECK
            if self.language == 'ar':
                return "ممتاز! خلني أشيك استحقاقك..."
            else:
                return "Great! Let me check your eligibility..."
        else:
            self.state = AgentState.MODIFICATION
            if self.language == 'ar':
                return "فهمت. شنو التغيير اللي تبي تسويه؟"
            else:
                return "I understand. What would you like to change?"
    
    async def handle_modification(self, user_input: str) -> str:
        """Handle order modifications"""
        # For now, acknowledge and re-confirm
        # In production, would parse modification and update order
        self.order_modified = True
        self.state = AgentState.ORDER_CONFIRM
        self.order_confirmed = False  # Re-confirm modified order
        
        if self.language == 'ar':
            return "تمام، حدثت الطلب. خلني أأكد التفاصيل المحدثة..."
        else:
            return "Perfect, I've updated the order. Let me confirm the updated details..."
    
    async def handle_eligibility_check(self, user_input: str) -> str:
        """Handle eligibility check and present financial details"""
        financial = self.order_data.get('financial', {})
        
        # Format financial details
        monthly = financial.get('monthly', 0)
        advance = financial.get('advance', 0)
        upfront = financial.get('upfront', 0)
        vat = financial.get('vat', 0)
        total = financial.get('total', 0)
        
        if self.language == 'ar':
            response = f"""ممتاز! خلني أشيك استحقاقك. هذي التفاصيل:
- الدفعة الشهرية: {monthly:.3f} دينار
- الدفعة المقدمة: {advance:.3f} دينار
- الدفعة المسبقة: {upfront:.3f} دينار
- ضريبة القيمة المضافة: {vat:.3f} دينار
- المبلغ الإجمالي للدفع اليوم: {total:.3f} دينار

مناسب لك؟"""
        else:
            response = f"""Great! Let me check your eligibility. Here are the details:
- Monthly payment: {monthly:.3f} Dinars
- Advance payment: {advance:.3f} Dinars
- Upfront payment: {upfront:.3f} Dinars
- VAT: {vat:.3f} Dinars
- Total amount to pay today: {total:.3f} Dinars

Does this work for you?"""
        
        self.state = AgentState.CROSS_SELL
        return response
    
    async def handle_commitment_approval(self, user_input: str) -> str:
        """Handle commitment approval requests"""
        # Acknowledge and schedule callback
        if self.language == 'ar':
            return "أكيد، بقدم طلب للموافقة. بيصل فيك خلال 24 ساعة. شكراً لاختيارك زين، مع السلامة."
        else:
            return "Absolutely, I'll submit the approval request. You'll receive a callback within 24 hours. Thank you for choosing Zain, have a good day."
    
    async def handle_cross_sell(self, user_input: str) -> str:
        """Handle cross-selling accessories"""
        # Check if customer accepted
        if any(word in user_input.lower() for word in ['yes', 'نعم', 'أكيد', 'ok']):
            if self.language == 'ar':
                response = "حلو! ضفت الإكسسوارات لطلبك. الحين باعث لك رابط التوقيع الرقمي..."
            else:
                response = "Great! I've added the accessories to your order. Now I'm sending you the digital signing link..."
        else:
            if self.language == 'ar':
                response = "ما فيها مشكلة. الحين باعث لك رابط التوقيع الرقمي..."
            else:
                response = "No problem at all. Now I'm sending you the digital signing link..."
        
        self.state = AgentState.EKYC_SEND
        return response
    
    async def handle_ekyc_send(self, user_input: str) -> str:
        """Handle eKYC sending"""
        if self.language == 'ar':
            response = "ممتاز! أرسلت لك رابط التوقيع الرقمي والدفع عن طريق رسالة نصية. من فضلك كمله خلال ساعة. شكراً لاختيارك زين، مع السلامة."
        else:
            response = "Excellent! I've sent you the digital signing and payment link via SMS. Please complete it within one hour. Thank you for choosing Zain, have a good day."
        
        self.state = AgentState.CLOSE
        return response
    
    def generate_order_summary(self) -> str:
        """Generate order summary in current language"""
        order_type = self.order_data.get('order_type', 'new_line')
        device = self.order_data.get('device')
        line_details = self.order_data.get('line_details', {})
        
        if self.language == 'ar':
            if order_type == 'new_line' and device:
                sub_num = line_details.get('sub_number', 'N/A')
                device_name = device.get('name', 'N/A')
                return f"خلني أأكد تفاصيل طلبك. طلبك لخط جديد برقم فرعي {sub_num} والجهاز {device_name}. صح؟"
            elif order_type == 'new_line':
                sub_num = line_details.get('sub_number', 'N/A')
                return f"خلني أأكد تفاصيل طلبك. طلبك لخط جديد فقط برقم فرعي {sub_num}. صح؟"
            elif order_type == 'existing_line' and device:
                number = line_details.get('number', 'N/A')
                device_name = device.get('name', 'N/A')
                return f"خلني أأكد تفاصيل طلبك. طلبك لـ {device_name} على رقمك الموجود {number}. صح؟"
            elif order_type == 'cash' and device:
                device_name = device.get('name', 'N/A')
                return f"خلني أأكد تفاصيل طلبك. طلبك لـ {device_name} على أساس كاش. صح؟"
        else:
            if order_type == 'new_line' and device:
                sub_num = line_details.get('sub_number', 'N/A')
                device_name = device.get('name', 'N/A')
                return f"Let me confirm your order details. Your order is for a new line with sub-number {sub_num} and the device {device_name}. Is this correct?"
            elif order_type == 'new_line':
                sub_num = line_details.get('sub_number', 'N/A')
                return f"Let me confirm your order details. Your order is for a new line only with sub-number {sub_num}. Is this correct?"
            elif order_type == 'existing_line' and device:
                number = line_details.get('number', 'N/A')
                device_name = device.get('name', 'N/A')
                return f"Let me confirm your order details. Your order is for an {device_name} under your existing number {number}. Is this correct?"
            elif order_type == 'cash' and device:
                device_name = device.get('name', 'N/A')
                return f"Let me confirm your order details. Your order is for an {device_name} on a cash basis. Is this correct?"
        
        return "Let me confirm your order details..."

